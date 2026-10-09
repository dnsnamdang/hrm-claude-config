# Review package T7 — BASE 60674e96cf3319a0a89e44754e4890210d58f94c .. HEAD 99f08bf6ccb87ccd82e3d04af48fb6d8629f8827

## git log
99f08bf6c feat(finance): thêm BorrowSellService::store() - lập phiếu xuất bán hàng mượn (T7)

## diff --stat
 .../Services/BorrowSell/BorrowSellService.php      | 369 +++++++++++++++++++++
 .../Finance/Tests/Feature/BorrowSellStoreTest.php  | 210 ++++++++++++
 2 files changed, 579 insertions(+)

## diff -U10
diff --git a/Modules/Finance/Services/BorrowSell/BorrowSellService.php b/Modules/Finance/Services/BorrowSell/BorrowSellService.php
new file mode 100644
index 000000000..44b206af5
--- /dev/null
+++ b/Modules/Finance/Services/BorrowSell/BorrowSellService.php
@@ -0,0 +1,369 @@
+<?php
+namespace Modules\Finance\Services\BorrowSell;
+
+use Illuminate\Http\Request;
+use Illuminate\Support\Facades\DB;
+use Illuminate\Validation\ValidationException;
+use Modules\Finance\Entities\BorrowSell\BorrowSell;
+use Modules\Finance\Entities\BorrowSell\BorrowSellProduct;
+use Modules\Finance\Entities\BorrowSell\BorrowSellProductDetail;
+use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;
+use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequestProduct;
+use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequestProductDetail;
+use Modules\Finance\Entities\ProductImportRequest\ProductExportRequestDetail;
+use Modules\Finance\Services\BorrowSellRequest\BorrowSellRequestCalculator;
+
+/**
+ * Orchestrator lập phiếu XUẤT BÁN HÀNG MƯỢN thực tế (`BorrowSell`) từ 1 yêu cầu
+ * (`BorrowSellRequest`) đã ở trạng thái "Chờ kế toán kho" — port 1-1 ERP
+ * `App\Http\Controllers\Warehouse\BorrowSellsController::store()` + `BorrowSell::updateWarehouse()`.
+ *
+ * Đã bake 7 RULINGS chốt ở task T7 (xem task-p2-7-brief.md):
+ *   T7-1: header sums (sum_amount_*, vat_cost_allocated) TÍNH LẠI server-side, KHÔNG tin FE.
+ *   T7-2: generateCode dùng id THẬT sau save() đầu (KHÔNG dùng BorrowSell::generateCode() static
+ *         vì method đó dùng max('id')+1 trước insert → có race).
+ *   T7-3: cột cộng dồn (borrow_returned_qty, returned_by_sell, exported_qty) dùng increment() ATOMIC
+ *         (ERP gốc dùng += rồi save() — lost-update kinh điển, xem erp-borrowsell-lost-update-incident).
+ *   T7-4: 1 DB::transaction bọc toàn bộ; gọi postDeliveryTripAccounting() RỒI postAccounting();
+ *         check [ok,err] và throw để rollback nếu hạch toán lỗi.
+ *   T7-5: returningQty() loại trừ chính phiếu YC cha khỏi nhánh sell (bsr.status=2).
+ *   T7-6: CHỈ hỗ trợ HANG_THUONG — bỏ hẳn nhánh tabs/syncTabs (KM) của ERP.
+ *   T7-7: bỏ guard `need_check_exported` (cột không tồn tại trên DB gộp).
+ */
+class BorrowSellService
+{
+    // morph objectable của dòng SP (khớp borrow_sell_request_products.objectable_type) — cùng giá trị
+    // const OBJECTABLE_FIRM/OBJECTABLE_WR_SERVICE của BorrowSellRequestService (Phase 1).
+    const OBJECTABLE_FIRM = 'App\Model\Sale\Firm\Contract\FirmContractTabProduct';
+    const OBJECTABLE_WR_SERVICE = 'App\Model\Customers\WrServiceContractItem';
+
+    // ProductExportRequest::XUAT_MUON (ExportModel::XUAT_MUON) — dùng trong returningQty().
+    const XUAT_MUON = 3;
+
+    // ERP App\Model\Warehouse\ProductExportRequest::DA_TRA — HRM entity ProductExportRequest CHƯA
+    // khai const này (chỉ có DA_MUON=2) nên khai lại tại đây, verbatim giá trị ERP.
+    const PER_DA_TRA = 3;
+
+    /**
+     * Lập phiếu xuất bán hàng mượn thực tế từ 1 yêu cầu (BorrowSellRequest) đã ở CHO_KE_TOAN_KHO.
+     * Chạy trong 1 DB::transaction. Throw ValidationException khi không đủ điều kiện / tồn không đủ.
+     */
+    public function store(Request $request): BorrowSell
+    {
+        $parent = BorrowSellRequest::findOrFail($request->borrow_sell_request_id);
+
+        if (!$parent->canApprove()) {
+            throw ValidationException::withMessages([
+                'borrow_sell_request_id' => ['Yêu cầu không ở trạng thái Chờ kế toán kho hoặc bạn không có quyền Kế toán kho'],
+            ]);
+        }
+
+        // Ruling T7-6: Service này CHỈ port nhánh HANG_THUONG (bỏ tabs/KM) — chặn sớm nếu phiếu
+        // cha là hàng khuyến mãi để tránh tạo phiếu xuất bán thiếu logic tabs.
+        if ((int) $parent->type !== BorrowSellRequest::HANG_THUONG) {
+            throw ValidationException::withMessages([
+                'borrow_sell_request_id' => ['Chỉ hỗ trợ lập phiếu xuất bán cho yêu cầu hàng thường'],
+            ]);
+        }
+
+        return DB::transaction(function () use ($request, $parent) {
+            $object = new BorrowSell();
+            $object->code = 'TMP-' . uniqid();
+            $object->borrow_sell_request_id = $parent->id;
+            $object->type = $parent->type;
+            $object->status = BorrowSell::STATUS_DEFAULT;
+            $object->contractable_id = $parent->contractable_id;
+            $object->contractable_type = $parent->contractable_type;
+            $object->firm_contract_tab_id = $parent->firm_contract_tab_id;
+            $object->created_by = auth()->id();
+            $object->note = $request->note;
+            $object->vat_percent = $request->input('vat_percent');
+            $object->bear_the_shipping = $request->input('bear_the_shipping', 0);
+            $object->save();
+
+            // Ruling T7-2: generateCode bằng id THẬT sau save() đầu (KHÔNG dùng static generateCode()).
+            $object->code = BorrowSell::PREFIX . '-' . str_pad((string) $object->id, 5, '0', STR_PAD_LEFT);
+            $object->save();
+
+            $isFirm = $object->contractable_type === BorrowSell::CONTRACT_FIRM;
+
+            $hasChange = false;
+            $rowsForSums = [];
+
+            foreach ((array) $request->products as $product) {
+                if (!isset($product['details'])) {
+                    continue;
+                }
+
+                $requestProduct = BorrowSellRequestProduct::where('parent_id', $parent->id)
+                    ->where('objectable_id', $product['objectable_id'])
+                    ->where('objectable_type', $product['objectable_type'])
+                    ->firstOrFail();
+
+                $p = new BorrowSellProduct();
+                $p->parent_id = $object->id;
+                $p->objectable_id = $requestProduct->objectable_id;
+                $p->objectable_type = $requestProduct->objectable_type;
+                $p->contract_promotion_id = $requestProduct->contract_promotion_id;
+                $p->product_id = $requestProduct->product_id;
+                $p->product_name = $requestProduct->product_name;
+                $p->unit_id = $requestProduct->unit_id;
+                $p->unit_name = $requestProduct->unit_name;
+                $p->model_id = $requestProduct->model_id;
+                $p->model_name = $requestProduct->model_name;
+                $p->brand_id = $requestProduct->brand_id;
+                $p->brand_name = $requestProduct->brand_name;
+                $p->code = $requestProduct->code;
+                $p->contract_qty = $requestProduct->contract_qty;
+                $p->price = $requestProduct->price;
+                $p->extra_price = $requestProduct->extra_price;
+                $p->allocated_price = $requestProduct->allocated_price;
+                $p->unit_coefficient = $requestProduct->unit_coefficient;
+                $p->rebate_price = $requestProduct->rebate_price;
+                $p->vat_percent = $requestProduct->vat_percent;
+                $p->qty = 0;
+                $p->export_price = 0;
+                $p->save();
+
+                $qty = 0.0;
+                $totalExportPrice = 0.0;
+
+                foreach ((array) $product['details'] as $detail) {
+                    $requestDetail = BorrowSellRequestProductDetail::where('parent_id', $requestProduct->id)
+                        ->where('product_export_request_detail_id', $detail['product_export_request_detail_id'])
+                        ->firstOrFail();
+
+                    $borrowDetail = ProductExportRequestDetail::findOrFail($requestDetail->product_export_request_detail_id);
+
+                    // Ruling T7-5: loại trừ chính $parent khỏi nhánh sell (bsr.status=2) của returningQty.
+                    $returning = $this->returningQty(
+                        (int) $requestDetail->product_export_request_id,
+                        (int) $p->product_id,
+                        (int) $parent->id
+                    );
+                    $available = BorrowSellRequestCalculator::availableSellQty(
+                        (float) $borrowDetail->base_exported_qty,
+                        (float) $borrowDetail->borrow_returned_qty,
+                        (float) $returning,
+                        (float) $p->unit_coefficient
+                    );
+                    if (BorrowSellRequestCalculator::isQtyExceeded($available, (float) $p->unit_coefficient, (float) $detail['qty'])) {
+                        throw ValidationException::withMessages([
+                            'products' => ['Sản phẩm "' . $p->product_name . '" tồn không đủ để xuất bán'],
+                        ]);
+                    }
+
+                    $detailQty = (float) $detail['qty'];
+                    $qty += $detailQty;
+                    $totalExportPrice += $detailQty * (float) $p->unit_coefficient * (float) $borrowDetail->export_price;
+                    if ($detailQty > 0) {
+                        $hasChange = true;
+                    }
+
+                    $d = new BorrowSellProductDetail();
+                    $d->parent_id = $p->id;
+                    $d->product_export_request_id = $requestDetail->product_export_request_id;
+                    $d->product_export_request_detail_id = $requestDetail->product_export_request_detail_id;
+                    $d->unit_id = $requestDetail->unit_id;
+                    $d->product_id = $p->product_id;
+                    $d->qty = $detailQty;
+                    $d->save();
+                }
+
+                $p->qty = $qty;
+                $p->export_price = $qty > 0 ? $totalExportPrice / $qty : 0;
+                $p->save();
+
+                // Ghi ngược export_price bình quân gia quyền xuống dòng cha của phiếu YC (như ERP).
+                $requestProduct->export_price = $p->export_price;
+                $requestProduct->save();
+
+                $rowsForSums[] = [
+                    'is_firm' => $isFirm,
+                    'price' => (float) $p->price,
+                    'extra_price' => (float) $p->extra_price,
+                    'allocated_price' => (float) $p->allocated_price,
+                    'vat_percent' => (float) $p->vat_percent,
+                    'qty' => (float) $p->qty,
+                ];
+            }
+
+            if (!$hasChange) {
+                throw ValidationException::withMessages(['products' => ['Không có thay đổi']]);
+            }
+
+            // Ruling T7-1: tính LẠI header sums server-side từ dòng SP vừa build (KHÔNG tin request).
+            $sums = $this->computeHeaderSums($rowsForSums);
+            $object->sum_amount_after_extra = $sums['sum_amount_after_extra'];
+            $object->sum_amount_after_extra_vat = $sums['sum_amount_after_extra_vat'];
+            $object->sum_amount_after_extra_after_vat = $sums['sum_amount_after_extra_after_vat'];
+            $object->sum_amount_allocated = $sums['sum_amount_allocated'];
+            $object->sum_amount_allocated_after_vat = $sums['sum_amount_allocated_after_vat'];
+            $object->vat_cost_allocated = $sums['vat_cost_allocated'];
+            $object->save();
+
+            $this->updateWarehouse($object);
+
+            // Ruling T7-4: gọi postDeliveryTripAccounting() RỒI postAccounting(); check [ok,err]
+            // và throw để rollback outer transaction (2 service này tự mở transaction/savepoint riêng).
+            $postingService = app(BorrowSellPostingService::class);
+
+            [$okTrip, $errTrip] = $postingService->postDeliveryTripAccounting($object);
+            if (!$okTrip) {
+                throw new \RuntimeException($errTrip ?: 'Hạch toán vận chuyển thất bại');
+            }
+
+            [$okAcc, $errAcc] = $postingService->postAccounting($object);
+            if (!$okAcc) {
+                throw new \RuntimeException($errAcc ?: 'Hạch toán phiếu xuất bán thất bại');
+            }
+
+            // Port ERP $parent->approve() (KHÔNG có sẵn method trên entity/Service Phase 1).
+            $parent->status = BorrowSellRequest::DA_DUYET;
+            $parent->approver_id = auth()->id();
+            $parent->approved_time = now();
+            $parent->save();
+
+            return $object;
+        });
+    }
+
+    /**
+     * Trừ kho + cập nhật trạng thái mượn (port ERP BorrowSell::updateWarehouse()).
+     * Ruling T7-3: cột cộng dồn (borrow_returned_qty, returned_by_sell, objectable exported_qty)
+     * dùng increment() ATOMIC — KHÁC ERP gốc dùng `+= rồi save()` (lost-update, xem
+     * erp-borrowsell-lost-update-incident trong memory). Cột gán (approved_qty) dùng update()/save.
+     * Ruling T7-6: bỏ hẳn nhánh tabs (KM) — luôn đi path SP thường (HANG_THUONG).
+     * Ruling T7-7: bỏ guard need_check_exported (cột không tồn tại) — luôn cộng exported_qty.
+     */
+    private function updateWarehouse(BorrowSell $bs): void
+    {
+        $products = BorrowSellProduct::where('parent_id', $bs->id)->with('details')->get();
+
+        foreach ($products as $p) {
+            $requestProduct = BorrowSellRequestProduct::where('parent_id', $bs->borrow_sell_request_id)
+                ->where('objectable_id', $p->objectable_id)
+                ->where('objectable_type', $p->objectable_type)
+                ->firstOrFail();
+            $requestProduct->approved_qty = $p->qty;
+            $requestProduct->save();
+
+            $objectableTable = $p->objectable_type === self::OBJECTABLE_FIRM
+                ? 'firm_contract_tab_products'
+                : 'wr_service_contract_items';
+            DB::table($objectableTable)->where('id', $p->objectable_id)->increment('exported_qty', (float) $p->qty);
+
+            foreach ($p->details as $d) {
+                $requestDetail = BorrowSellRequestProductDetail::where('parent_id', $requestProduct->id)
+                    ->where('product_export_request_detail_id', $d->product_export_request_detail_id)
+                    ->firstOrFail();
+                $requestDetail->approved_qty = $d->qty;
+                $requestDetail->save();
+
+                $qty = (float) $d->qty * (float) $p->unit_coefficient;
+
+                DB::table('product_export_request_details')
+                    ->where('id', $d->product_export_request_detail_id)
+                    ->increment('borrow_returned_qty', $qty);
+                DB::table('product_export_request_details')
+                    ->where('id', $d->product_export_request_detail_id)
+                    ->increment('returned_by_sell', $qty);
+
+                $notFinished = DB::table('product_export_request_details')
+                    ->where('parent_id', $d->product_export_request_id)
+                    ->whereRaw('base_exported_qty > borrow_returned_qty')
+                    ->exists();
+                if (!$notFinished) {
+                    DB::table('product_export_requests')
+                        ->where('id', $d->product_export_request_id)
+                        ->update(['borrow_status' => self::PER_DA_TRA]);
+                }
+            }
+        }
+    }
+
+    /**
+     * Port Phase 1 `BorrowSellRequestService::returningQty()` + Ruling T7-5: loại trừ chính
+     * phiếu YC cha ($excludeParentRequestId) khỏi nhánh sell (bsr.status=2) — vì khi store() đang
+     * chạy, chính $parent vẫn còn status=2 (chỉ chuyển DA_DUYET ở cuối transaction) nên nếu không
+     * loại trừ, phiếu sẽ tự trừ tồn của chính nó lần 2.
+     */
+    private function returningQty(int $exportRequestId, int $productId, int $excludeParentRequestId): float
+    {
+        $parentType = DB::table('product_export_requests')->where('id', $exportRequestId)->value('type');
+        if ((int) $parentType !== self::XUAT_MUON) {
+            return 0;
+        }
+
+        $import = (float) DB::table('product_import_request_details as pird')
+            ->join('product_import_requests as pir', 'pird.parent_id', '=', 'pir.id')
+            ->where('pird.product_id', $productId)
+            ->where('pir.is_complete', false)
+            ->where('pir.product_export_request_id', $exportRequestId)
+            ->sum(DB::raw('pird.qty * pird.unit_coefficient'));
+
+        $sell = (float) DB::table('borrow_sell_request_product_details as bsrpd')
+            ->join('borrow_sell_request_products as bsrp', 'bsrpd.parent_id', '=', 'bsrp.id')
+            ->join('borrow_sell_requests as bsr', 'bsrp.parent_id', '=', 'bsr.id')
+            ->where('bsrp.product_id', $productId)
+            ->where('bsr.status', 2)
+            ->where('bsr.id', '!=', $excludeParentRequestId)
+            ->where('bsrpd.product_export_request_id', $exportRequestId)
+            ->sum(DB::raw('bsrpd.qty * bsrp.unit_coefficient'));
+
+        $other = (float) DB::table('borrow_export_request_product_details as berpd')
+            ->join('borrow_export_request_products as berp', 'berpd.parent_id', '=', 'berp.id')
+            ->join('borrow_export_requests as ber', 'berp.parent_id', '=', 'ber.id')
+            ->where('berp.product_id', $productId)
+            ->where('ber.status', 2)
+            ->where('berpd.product_export_request_id', $exportRequestId)
+            ->sum(DB::raw('berpd.qty * berp.unit_coefficient'));
+
+        return $import + $sell + $other;
+    }
+
+    /**
+     * Ruling T7-1 — mirror công thức `computeAmounts` của Phase 1 `BorrowSellRequestService`, nhưng
+     * tính từ dòng SP SERVER build (BorrowSellProduct đã copy giá từ BorrowSellRequestProduct) thay
+     * vì từ payload FE. Tách riêng (private, pure) để test trực tiếp qua reflection (không cần DB).
+     *
+     * @param array $rows mỗi phần tử: ['is_firm'=>bool,'price'=>float,'extra_price'=>float,
+     *                     'allocated_price'=>float,'vat_percent'=>float,'qty'=>float]
+     */
+    private function computeHeaderSums(array $rows): array
+    {
+        $sumAfterExtra = 0.0;
+        $sumAfterExtraVat = 0.0;
+        $sumAllocated = 0.0;
+        $sumAllocatedAfterVat = 0.0;
+        $vatCostAllocated = 0.0;
+
+        foreach ($rows as $row) {
+            $price = !empty($row['is_firm']) ? (float) ($row['price'] ?? 0) : 0.0;
+            $extraPrice = (float) ($row['extra_price'] ?? 0);
+            $allocatedPrice = (float) ($row['allocated_price'] ?? 0);
+            $vatPercent = (float) ($row['vat_percent'] ?? 0);
+            $qty = (float) ($row['qty'] ?? 0);
+
+            $amountAfterExtra = ($extraPrice + $price) * $qty;
+            $amountAfterExtraVat = $amountAfterExtra * $vatPercent / 100;
+            $amountAllocated = $allocatedPrice * $qty;
+            $vatAllocatedLine = $amountAllocated * $vatPercent / 100;
+
+            $sumAfterExtra += $amountAfterExtra;
+            $sumAfterExtraVat += $amountAfterExtraVat;
+            $sumAllocated += $amountAllocated;
+            $sumAllocatedAfterVat += $amountAllocated + $vatAllocatedLine;
+            $vatCostAllocated += $vatAllocatedLine;
+        }
+
+        return [
+            'sum_amount_after_extra' => $sumAfterExtra,
+            'sum_amount_after_extra_vat' => $sumAfterExtraVat,
+            'sum_amount_after_extra_after_vat' => $sumAfterExtra + $sumAfterExtraVat,
+            'sum_amount_allocated' => $sumAllocated,
+            'sum_amount_allocated_after_vat' => $sumAllocatedAfterVat,
+            'vat_cost_allocated' => $vatCostAllocated,
+        ];
+    }
+}
diff --git a/Modules/Finance/Tests/Feature/BorrowSellStoreTest.php b/Modules/Finance/Tests/Feature/BorrowSellStoreTest.php
new file mode 100644
index 000000000..48e601e9b
--- /dev/null
+++ b/Modules/Finance/Tests/Feature/BorrowSellStoreTest.php
@@ -0,0 +1,210 @@
+<?php
+
+namespace Modules\Finance\Tests\Feature;
+
+use Tests\TestCase;
+use Illuminate\Foundation\Testing\DatabaseTransactions;
+use Illuminate\Support\Facades\DB;
+use Modules\Finance\Services\BorrowSell\BorrowSellService;
+
+/**
+ * Test cho `BorrowSellService::store()` (Task P2-7 — orchestrator lập phiếu xuất bán hàng mượn).
+ * store() phụ thuộc auth()->id() + quyền "Kế toán kho" + dữ liệu HĐ/kho thật rất phức tạp
+ * (BorrowSellRequest → firm_contract_tab_products/wr_service_contract_items →
+ * product_export_request_details) nên KHÔNG test end-to-end store() ở đây. Test theo hướng
+ * đơn vị hoá 2 phần logic thuần (T7-1 computeHeaderSums, T7-5 returningQty exclude-parent) —
+ * cùng cách tiếp cận BorrowSellPostingWrServiceTest.
+ */
+class BorrowSellStoreTest extends TestCase
+{
+    use DatabaseTransactions;
+
+    /**
+     * T7-1 — QUAN TRỌNG NHẤT: header sums phải tính từ dòng SP server build, KHÔNG tin FE.
+     * Firm: price được tính vào amount_after_extra; WrService: price=0 (chỉ extra_price).
+     * Không cần DB — computeHeaderSums là pure function → test XANH THẬT, không skip.
+     */
+    public function test_compute_header_sums_firm_includes_price_and_wr_service_zeroes_price()
+    {
+        $service = new BorrowSellService();
+        $method = new \ReflectionMethod(BorrowSellService::class, 'computeHeaderSums');
+        $method->setAccessible(true);
+
+        // Firm: price=100, extra_price=10, allocated_price=5, vat_percent=10, qty=3
+        $rowsFirm = [[
+            'is_firm' => true,
+            'price' => 100,
+            'extra_price' => 10,
+            'allocated_price' => 5,
+            'vat_percent' => 10,
+            'qty' => 3,
+        ]];
+        $sumsFirm = $method->invoke($service, $rowsFirm);
+
+        // amount_after_extra = (extra+price)*qty = (10+100)*3 = 330
+        $this->assertEqualsWithDelta(330, $sumsFirm['sum_amount_after_extra'], 0.001);
+        // amount_after_extra_vat = 330*10/100 = 33
+        $this->assertEqualsWithDelta(33, $sumsFirm['sum_amount_after_extra_vat'], 0.001);
+        $this->assertEqualsWithDelta(363, $sumsFirm['sum_amount_after_extra_after_vat'], 0.001);
+        // amount_allocated = allocated_price*qty = 5*3 = 15
+        $this->assertEqualsWithDelta(15, $sumsFirm['sum_amount_allocated'], 0.001);
+        // vat_allocated_line = 15*10/100 = 1.5 -> allocated_after_vat = 15+1.5 = 16.5
+        $this->assertEqualsWithDelta(16.5, $sumsFirm['sum_amount_allocated_after_vat'], 0.001);
+        $this->assertEqualsWithDelta(1.5, $sumsFirm['vat_cost_allocated'], 0.001);
+
+        // WrService cùng số liệu nhưng is_firm=false -> price bị zero-hoá.
+        $rowsWr = [[
+            'is_firm' => false,
+            'price' => 100,
+            'extra_price' => 10,
+            'allocated_price' => 5,
+            'vat_percent' => 10,
+            'qty' => 3,
+        ]];
+        $sumsWr = $method->invoke($service, $rowsWr);
+
+        // amount_after_extra = (extra+0)*qty = 10*3 = 30 (KHÔNG cộng price=100)
+        $this->assertEqualsWithDelta(30, $sumsWr['sum_amount_after_extra'], 0.001);
+        $this->assertEqualsWithDelta(3, $sumsWr['sum_amount_after_extra_vat'], 0.001);
+        $this->assertEqualsWithDelta(33, $sumsWr['sum_amount_after_extra_after_vat'], 0.001);
+        // allocated_price không phụ thuộc is_firm -> giữ nguyên như Firm
+        $this->assertEqualsWithDelta(15, $sumsWr['sum_amount_allocated'], 0.001);
+    }
+
+    /** Nhiều dòng SP phải cộng dồn đúng (không phải chỉ lấy dòng cuối). */
+    public function test_compute_header_sums_accumulates_multiple_rows()
+    {
+        $service = new BorrowSellService();
+        $method = new \ReflectionMethod(BorrowSellService::class, 'computeHeaderSums');
+        $method->setAccessible(true);
+
+        $rows = [
+            ['is_firm' => true, 'price' => 100, 'extra_price' => 0, 'allocated_price' => 0, 'vat_percent' => 0, 'qty' => 2], // 200
+            ['is_firm' => true, 'price' => 50, 'extra_price' => 0, 'allocated_price' => 0, 'vat_percent' => 0, 'qty' => 4],  // 200
+        ];
+        $sums = $method->invoke($service, $rows);
+
+        $this->assertEqualsWithDelta(400, $sums['sum_amount_after_extra'], 0.001);
+    }
+
+    /**
+     * T7-5 — returningQty() phải LOẠI TRỪ chính phiếu YC cha ($excludeParentRequestId) khỏi
+     * nhánh sell (bsr.status=2), nếu không phiếu sẽ tự trừ tồn của chính nó lần 2 khi store()
+     * đang chạy (parent vẫn còn status=2 cho tới cuối transaction).
+     *
+     * Dựng fixture tối thiểu trực tiếp bằng DB::table() (không có FK ràng buộc thật trên các
+     * bảng liên quan — đã verify bằng SHOW CREATE TABLE, chỉ có index đặt tên "*_foreign").
+     * DatabaseTransactions tự rollback sau test.
+     */
+    public function test_returning_qty_excludes_parent_request()
+    {
+        $service = new BorrowSellService();
+        $method = new \ReflectionMethod(BorrowSellService::class, 'returningQty');
+        $method->setAccessible(true);
+
+        $productId = 900000001;
+
+        // 1 phiếu xuất mượn gốc (type=XUAT_MUON=3) — chỉ cần tồn tại để trả đúng "type".
+        $exportRequestId = DB::table('product_export_requests')->insertGetId([
+            'type' => BorrowSellService::XUAT_MUON,
+            'status' => 5,
+            'code' => 'TEST-PER-' . uniqid(),
+            'created_by' => 1,
+            'department' => 0,
+            'created_at' => now(),
+            'updated_at' => now(),
+        ]);
+
+        // Phiếu YC bán mượn CHA (đang được store() xử lý) — status=2 (CHO_KE_TOAN_KHO).
+        $parentBsrId = DB::table('borrow_sell_requests')->insertGetId([
+            'status' => 2,
+            'type' => 1,
+            'code' => 'TEST-BSR-PARENT-' . uniqid(),
+            'contractable_id' => 1,
+            'contractable_type' => 'App\Model\Sale\Firm\Contract\FirmContract',
+            'created_by' => 1,
+            'created_at' => now(),
+            'updated_at' => now(),
+        ]);
+        $parentBsrProductId = DB::table('borrow_sell_request_products')->insertGetId([
+            'parent_id' => $parentBsrId,
+            'objectable_type' => BorrowSellService::OBJECTABLE_FIRM,
+            'product_id' => $productId,
+            'product_name' => 'SP test T7-5',
+            'unit_id' => 1,
+            'unit_name' => 'Cái',
+            'brand_id' => 1,
+            'brand_name' => 'Test',
+            'model_id' => 1,
+            'model_name' => 'Test',
+            'code' => 'SP-TEST',
+            'price' => 0,
+            'contract_qty' => 100,
+            'qty' => 5,
+            'created_at' => now(),
+            'updated_at' => now(),
+        ]);
+        DB::table('borrow_sell_request_product_details')->insert([
+            'parent_id' => $parentBsrProductId,
+            'request_id' => $parentBsrId,
+            'product_export_request_id' => $exportRequestId,
+            'product_export_request_detail_id' => 1,
+            'product_id' => $productId,
+            'unit_id' => 1,
+            'qty' => 5, // 5 * unit_coefficient(mặc định BorrowSellRequestProduct=1) = 5
+            'created_at' => now(),
+            'updated_at' => now(),
+        ]);
+
+        // 1 phiếu YC bán mượn KHÁC (không phải parent) — cũng status=2, PHẢI được tính vào sum.
+        $otherBsrId = DB::table('borrow_sell_requests')->insertGetId([
+            'status' => 2,
+            'type' => 1,
+            'code' => 'TEST-BSR-OTHER-' . uniqid(),
+            'contractable_id' => 1,
+            'contractable_type' => 'App\Model\Sale\Firm\Contract\FirmContract',
+            'created_by' => 1,
+            'created_at' => now(),
+            'updated_at' => now(),
+        ]);
+        $otherBsrProductId = DB::table('borrow_sell_request_products')->insertGetId([
+            'parent_id' => $otherBsrId,
+            'objectable_type' => BorrowSellService::OBJECTABLE_FIRM,
+            'product_id' => $productId,
+            'product_name' => 'SP test T7-5',
+            'unit_id' => 1,
+            'unit_name' => 'Cái',
+            'brand_id' => 1,
+            'brand_name' => 'Test',
+            'model_id' => 1,
+            'model_name' => 'Test',
+            'code' => 'SP-TEST',
+            'price' => 0,
+            'contract_qty' => 100,
+            'qty' => 2,
+            'created_at' => now(),
+            'updated_at' => now(),
+        ]);
+        DB::table('borrow_sell_request_product_details')->insert([
+            'parent_id' => $otherBsrProductId,
+            'request_id' => $otherBsrId,
+            'product_export_request_id' => $exportRequestId,
+            'product_export_request_detail_id' => 2,
+            'product_id' => $productId,
+            'unit_id' => 1,
+            'qty' => 2,
+            'created_at' => now(),
+            'updated_at' => now(),
+        ]);
+
+        // Loại trừ chính $parentBsrId -> chỉ còn 2 (của $otherBsrId) trong nhánh sell.
+        $qty = $method->invoke($service, $exportRequestId, $productId, $parentBsrId);
+        $this->assertEqualsWithDelta(2.0, $qty, 0.001,
+            'Phải loại trừ 5 (của chính parent) khỏi tổng, chỉ còn 2 (của phiếu khác)');
+
+        // Không loại trừ ai (excludeParentRequestId không khớp gì) -> cộng cả 2 phiếu = 7.
+        $qtyNoExclude = $method->invoke($service, $exportRequestId, $productId, 0);
+        $this->assertEqualsWithDelta(7.0, $qtyNoExclude, 0.001,
+            'Không loại trừ -> phải cộng dồn cả parent (5) lẫn phiếu khác (2) = 7');
+    }
+}
