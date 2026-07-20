# Soát tích hợp — Tính năng "Hợp đồng mua" (module Supply)

Reviewer: @khoipv · Ngày: 2026-07-20
Phạm vi: BE `Modules/Supply/*` + FE `pages/supply/purchase_contracts/*`, đối chiếu spec `2026-07-20-hop-dong-mua-design.md`, contract FE `fe-form-contract.md`, demo `demo-lap-hop-dong-mua.html`.

Kết luận nhanh: **Có 1 Critical + 3 Important.** Phần lớn luồng (payload keys, gộp theo mã, cảnh báo SL, phân quyền, badge trạng thái, Vuex actions) khớp spec/demo và nhất quán giữa các file.

---

## CRITICAL

### C1. Ngày ký / ngày kết thúc bị hỏng khi Sửa (sai định dạng round-trip)
- File: `Modules/Supply/Transformers/PurchaseContract/DetailPurchaseContractResource.php:53-54`
  (`'sign_time' => Helper::formatDate(...)`, `'end_time' => Helper::formatDate(...)`) → trả **`d/m/Y`** (vd `12/06/2026`).
- Đối chiếu: `components/BaseDatePicker.vue:30` `valueType` mặc định = **`YYYY-MM-DD`**; cột DB `sign_time`/`end_time` là kiểu `date` (cần `Y-m-d`).
- Hệ quả (màn `_id/edit.vue` → `PurchaseContractForm.applyInitial` gán thẳng `f.sign_time = d.sign_time`):
  1. Date-picker nhận `"12/06/2026"` nhưng value-type `YYYY-MM-DD` → **không hiển thị được ngày** (ô trống).
  2. Bấm Lưu gửi lại `"12/06/2026"` cho BE → `headerData()` fill thẳng vào cột `date` → MySQL strict lỗi / non-strict lưu `0000-00-00`. **Mất dữ liệu ngày mỗi lần sửa dù không đụng vào field.**
  3. `GeneralTab.durationText` (`new Date(e)-new Date(s)`) cũng sai.
- Lưu ý: cột `progress.time` KHÔNG dính lỗi (DetailResource trả raw `g->time` = `Y-m-d`), chỉ `sign_time`/`end_time` qua `formatDate`.
- Đề xuất: DetailResource trả raw `Y-m-d` cho `sign_time`/`end_time` (vd `optional($this->sign_time)->format('Y-m-d')`) — KHÔNG dùng `Helper::formatDate`. (List resource giữ `formatDate` để hiển thị vẫn OK vì list không nạp ngược vào picker.)

---

## IMPORTANT

### I1. goods-pool thiếu enrich → cột Quy cách / Hãng nước SX / Tên giao dịch luôn rỗng
- File: `Http/Controllers/Api/V1/PurchaseContractController.php:202-221` (`goodsPool`) — chỉ ghép `purchaseDemand()['rows']` + `goodsPool(2)` (catalog), **không gọi `productInfoMap()`** như spec §4 yêu cầu.
- Nguồn dữ liệu:
  - `SupplyReportService::purchaseDemand` (select tại `SupplyReportService.php:45-59`, row build `:114-128`): KHÔNG có `specification`, `producer_country`, `product_trade_name`, `unit_id`.
  - `SupplyProposalService::catalogItems` (`:227-259`): cũng KHÔNG có `specification`, `producer_country`, `product_trade_name`.
- Hệ quả: `GoodsPickerModal.buildCandidates` (`:213-217`, `:250-254`) map các field này về `''`/`null` → Tab Hàng hóa (`ProductsTab` cột "Quy cách", "Hãng, nước sản xuất") và Mẫu in (`PrintTab.goodsRows`) **luôn trống**. Lệch demo (mỗi hàng có spec + hãng) và spec §4/§6.
- Đề xuất: bổ sung enrich trong `goodsPool` (join `products` lấy `specification`/`producer_country`/`product_trade_name`/`unit_id` theo `product_id`), hoặc thêm các field này vào select của `purchaseDemand`/`catalogItems`.

### I2. Gửi lại sau khi bị Từ chối KHÔNG thông báo lại người duyệt
- File: `Services/PurchaseContractService.php:301-309` (`rejectApprove`) — set status=4 + `reason_deny` nhưng **không reset `sent_at`**.
- File: `Services/PurchaseContractService.php:105-125` (`update`) — `$alreadySent = !is_null($contract->sent_at)`; chỉ `sendNotification` khi `status==PENDING && !alreadySent`.
- Hệ quả: HĐ đã bị từ chối (sent_at còn giá trị từ lần gửi đầu) → sửa lại + "Lưu và gửi" (status=2) → status về Chờ duyệt nhưng **không gửi notification mới, sent_at không cập nhật**. Trái tinh thần spec §7/§8 ("sửa HĐ từ chối → gửi lại được"). Người duyệt không được báo.
- Đề xuất: trong `rejectApprove` set `sent_at = null`; hoặc trong `update` khi status chuyển sang PENDING thì luôn set lại `sent_at = now()` + notify (bỏ điều kiện `!alreadySent`, hoặc dựa trên status trước đó = Từ chối/Nháp).

### I3. (Kiểm lại chủ đích) — Không có lỗi hoán đổi mã, nhưng comment/spec bị ngược
Xem M2 (không phải bug chức năng, để ở Minor). Trọng tâm "product_code/product_hh_code không hoán đổi qua goods-pool→line→save→detail→hiển thị" **ĐẠT** — dữ liệu đi xuyên suốt nhất quán.

---

## MINOR

### M1. Sắp xếp danh sách khai báo nhưng không chạy (server bỏ qua sort)
- `index.vue`: cột `code`, `created_at` đặt `sortable: true`, `no-local-sorting`, gửi `sort_by/sort_desc`.
- `Services/PurchaseContractService.php:71` `getList` luôn `->orderBy('id','desc')`, KHÔNG áp `sort_by/sort_desc`. Click header không có tác dụng. (Spec §4 liệt kê 2 param này.)
- Đề xuất: áp sort trong getList hoặc bỏ `sortable` khỏi fields.

### M2. Comment DB + spec §2.2 ghi NGƯỢC ý nghĩa product_code / product_hh_code (không phải bug)
- Thực tế toàn module Supply: `product_code` = **mã nội bộ**, `product_hh_code` = **mã hàng hóa** (xem migration `supply_handling_products:20-21` "Snapshot mã nội bộ"/"mã hàng hóa"; `catalogItems:236-237` map `internal_code`→product_code, `product_code`→product_hh_code; demand giữ nguyên shp).
- Nhưng migration `create_purchase_contract_products_table:20-21` và spec §2.2 lại chú thích `product_code='Mã hàng hóa (NSX)'` / `product_hh_code='Mã nội bộ'` — **ngược**.
- Dữ liệu vẫn đúng vì FE pass-through và cột "Mã hàng" hiển thị `product_hh_code` (= mã hàng hóa, đúng ý nghĩa). Chỉ cần sửa comment/spec cho khỏi nhầm lẫn về sau.

### M3. `vat_percent` không có nguồn nhập & không nguồn cấp → luôn null
- Cột tồn tại (migration + resource) nhưng ProductsTab không có ô nhập VAT, goods-pool cũng không trả `vat_percent`. Nhất quán với demo (demo cũng không có cột nhập VAT riêng, "đơn giá đã gồm VAT"). Chỉ nêu nếu sau này cần tách VAT.

### M4. HĐ Nguyên tắc vẫn tạo 4 dòng payment_terms mặc định
- `syncPaymentTerms($contract, [])` nhánh `elseif count===0` (`PurchaseContractService.php:246-251`) tạo 4 dòng enabled=false kể cả type=1 / type=2 chế độ "dot". Vô hại (FE không đọc khi không phải mode 'don') nhưng là dữ liệu thừa.

### M5. approve()/rejectApprove() không kiểm tra status hiện tại ở BE
- `PurchaseContractService.php:287-309` đổi status không guard (chỉ chặn bằng middleware quyền + FE `is_can_approve`). Có quyền duyệt vẫn có thể approve HĐ đang Nháp/đã duyệt qua gọi API trực tiếp. Đề xuất guard `status==PENDING` trong `approve`.

### M6. `show()` và các endpoint dropdown/goods-pool không gate quyền Xem
- Route `GET /{purchaseContract}`, `/companies`, `/suppliers`, `/goods-pool`, `/next-code` chỉ có `auth:api`. User đã đăng nhập (không có "Xem hợp đồng mua") vẫn GET được chi tiết theo id. **Đúng theo spec §4 (cột checkPermission = "—")**, chỉ nêu để cân nhắc.

### M7. Lồng DB::transaction
- Controller `store/update` bọc `DB::transaction` trong khi Service `store/update` cũng mở `DB::transaction` (savepoint). Vô hại, có thể bỏ 1 lớp.

---

## Các điểm ĐÃ KIỂM & ĐẠT
- Payload FE (`PurchaseContractForm.buildPayload`) khớp cột BE; `headerData()` `except(['id','code','total_amount','products','payment_terms','progress'])` — không dư key lạ.
- Map goods-pool §5: demand→purposes (`proposal_code/customer_name/quantity`), `proposed_qty=total_buy_qty`, `order_qty=Σ buyQty`; catalog→`purposes=[]`, `proposed_qty=null`. ĐẠT (`GoodsPickerModal:199-277`).
- Thanh toán: 100PCT loại trừ (FE `GeneralTab.onToggleTerm` + BE `syncPaymentTerms` ép tắt 3 loại); `dot→progress` / `don→payment_terms` (buildPayload) khớp BE; Nguyên tắc dùng `pay_days/pay_max_debt/pay_nt_text`; `total_amount` BE tự tính, type=1→0 (`calcTotalAmount`, `syncProducts`). ĐẠT.
- Cảnh báo SL over/under (`oqWarn`), `order_qty=Σ buyQty` (`onBuyQtyInput`), gộp theo mã mutate in-place (push/splice/$set, KHÔNG reassign `products`). ĐẠT (`ProductsTab`).
- `status_color = text_type`; badge `:variant="item.status_color"`; `is_can_*` từ accessor entity. ĐẠT.
- Vuex actions apiGet / apiGetMethod / apiPostMethod / apiPutMethod / apiDelete đều tồn tại (`store/actions.js`).
- Phân quyền: `getList` checkPermissionList `[PERM_VIEW,null,null,null,null]` (holder thấy tất cả, không holder thấy rỗng); nút Thêm `hasAPermission('Lập hợp đồng mua')`; Duyệt `hasAPermission('Duyệt hợp đồng mua')`; `destroy` gate `is_can_delete` (Nháp/Từ chối + owner). ĐẠT.
- Migration đủ cột theo spec; `purposes` cast array; JSON encode thủ công trong `syncProducts` (insert thô). ĐẠT.
- `exclude_codes[]` (`buildQuery`) ⇄ BE `$request->input('exclude_codes', [])` lọc cả code & hh_code. ĐẠT.
- `docSo` (numberToWords) dùng chung ProductsTab/PrintTab/Form. ĐẠT.
