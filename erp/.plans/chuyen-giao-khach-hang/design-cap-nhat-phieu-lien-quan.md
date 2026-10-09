# Design — Cập nhật phiếu liên quan khi chuyển giao khách hàng

> Sub-feature của **Chuyển giao khách hàng (YCCGKH)**. Tài liệu tóm tắt: `design.md`. Phase 1 (đổi KH trên HĐ + phụ lục): `design-phase1.md`.
> Tài liệu này đặc tả việc **lan đổi KH xuống toàn bộ phiếu nghiệp vụ đã sinh ra từ hợp đồng** khi duyệt / hủy duyệt phiếu chuyển giao.

## 1. Mục tiêu & phạm vi

Hiện tại khi **duyệt** phiếu YCCGKH, `CustomerHandoverService::applyToContract()` chỉ cập nhật KH mới lên **HĐ chính + phụ lục** (PLBS/PLG). Các **phiếu nghiệp vụ đã snapshot thông tin KH từ HĐ** (xuất kho, bảo hành, biên bản, giao việc, kế toán...) vẫn giữ KH cũ → dữ liệu lệch.

**Yêu cầu:** sau khi đổi KH trên HĐ, cập nhật KH mới cho **tất cả phiếu liên quan đã tạo từ HĐ đó**; khi **hủy duyệt** thì revert về KH cũ (đối xứng).

### Quyết định đã chốt (brainstorming)

| # | Quyết định | Chọn |
|---|---|---|
| 1 | Phạm vi phiếu cập nhật | **Tất cả** phiếu, kể cả phiếu đã quyết toán/nghiệm thu |
| 2 | Hủy duyệt | **Revert** tất cả phiếu về KH cũ (đối xứng) |
| 3 | Cột KH cập nhật | **Đầy đủ** — mọi cột `customer_*`/liên hệ/địa chỉ mà bảng có |
| 4 | Bảng kế toán đã hạch toán | **Có** cập nhật (chấp nhận công nợ chuyển KH mới) |
| 5 | Nhập kho / `account_details` / `handover_acceptance_product_records` | **Đều cập nhật / giữ** |
| 6 | Audit | **Bảng log riêng** `customer_handover_sync_logs` |

## 2. Hiện trạng dữ liệu (khảo sát schema PROD `erp_new`)

- Cách link phiếu → HĐ **không đồng nhất**, gồm 4 kiểu:
  - `firm_fk` — cột `firm_contract_id`
  - `wr_fk` — cột `wr_service_contract_id`
  - `polymorphic` — cột `contractable_id` + `contractable_type`
  - `legacy_contract_id` — cột `contract_id` (đời cũ 2020)
- **Morph class thực tế trên prod** (KHÔNG có morphMap, lưu full class):
  - FirmContract → `App\Model\Sale\Firm\Contract\FirmContract`
  - WrServiceContract → `App\Model\Customers\WrServiceContract`
  - ⇒ filter polymorphic bằng `get_class($contractable)` là chính xác; các HĐ khác (`InlandBuyContract`, `BuyContract2`, `WarehouseImport`...) tự động không bị chạm.
- Đã quét **61 bảng** có đồng thời (cột snapshot KH) + (cột link HĐ). Sau khi lọc **bảng chết (0 bản ghi)**, **bảng ngừng dùng**, **cột không phải danh tính KH** → còn **32 bảng ACTIVE** cần cập nhật (bảng §4).

### Bảng LOẠI (không đưa vào registry)

- **Chết / 0 bản ghi trên prod:** `install_estimates`, `install_plans`, `install_requests`, `install_summaries`, `receipts`, `payment_requests`, `customer_depts`, `debt_reminders`, `delivery_requests`, `employee_delivery_payment_details`, `monthly_commission_accounting_request_details`, `bill_bonus_business_contracts`, `bill_commission_settlement_month_employee_contracts`, `bill_payment_advance_details`, `contract_accountings`, `service_contract_accounting`, `service_contract_payment_requests`, `settlement_contract_detail`, `support_accounting`, `project_contract_customer_infos`, `insurance_principle_accountings`, `insurance_principle_accounting_requests`, `tmp_borrow_sell_requests`.
- **Ngừng dùng / sai bản chất:** `assign_business` (bản ghi cuối 2024-04), `buy_service_accountings(_requests)` (phía mua dịch vụ/NCC, `contractable_type` rỗng), `contract_approver_histories` (cột `receiver_id` = người duyệt).
- **Audit đổi KH (không ghi đè):** `bill_adjust_dept_request_details` (`customer_old_*`), `bill_adjust_dept_request_detail_items` (`customer_new_*`).

## 3. Kiến trúc (Hướng 1 — registry cấu hình tập trung)

### 3.1 Nguồn dữ liệu

Cấu trúc `$data` = `new_customer_data` (khi duyệt) hoặc `old_customer_data` (khi hủy duyệt), CHÍNH LÀ mảng do `CustomerHandoverService::snapshotContractCustomer()` sinh ra:

```
customer_id, customer_code, customer_name, customer_type, customer_address,
customer_mobile, customer_fax, customer_tax_code, customer_identity,
grant_date, grant_location, deputy_id, deputy_name, deputy_role,
delivery_place, receiver_address, vehicle_manufact_id,
account: { id, number, name, bank_name, bank_branch, bank_province_id },
contact: { id, name, address, phone }
```

### 3.2 Resolver cột → giá trị (DRY, dùng chung mọi bảng)

Thay vì hand-map 32 bảng, dùng **1 alias map** ánh xạ **tên cột thực của bảng** → giá trị trong `$data`. Service duyệt danh sách cột của từng bảng, cột nào có trong alias map thì set:

| Cột (nhiều bảng dùng) | Nguồn `$data` |
|---|---|
| `customer_id` | `customer_id` |
| `customer_code` | `customer_code` |
| `customer_name` | `customer_name` |
| `customer_type` | `customer_type` |
| `customer_address` | `customer_address` |
| `customer_mobile` | `customer_mobile` |
| `customer_fax` | `customer_fax` |
| `customer_tax_code` | `customer_tax_code` |
| `identity_card_number` / `customer_identity` | `customer_identity` |
| `customer_short_name` | resolve `Customer::find(customer_id)->short_name` (không có sẵn trong `$data`) |
| `delivery_place` | `delivery_place` |
| `customer_contact_id` | `contact.id` |
| `customer_contact_name` | `contact.name` |
| `contact_address` | `contact.address` |
| `customer_contact_phone` / `customer_contact_phones` | `contact.phone` |
| `deputy_name` | `deputy_name` |

**Cột KHÔNG map (giữ nguyên, ghi chú):**
- `delivery_place_id` (`assembly_requests`) — `$data` chỉ có `delivery_place` dạng text, không có id địa chỉ giao của KH mới → **không đụng**.
- `receiver_id` (`warehouse_exports`), `receiver_name`/`receiver_phone` (`handover_acceptance_product_records`) — là **người nhận**, không phải danh tính KH → **không đụng**.

### 3.3 Registry entry & service

Class mới `app/Services/Sale/CustomerHandoverDocumentSync.php`:

```php
// Mỗi entry: [ 'table' => ..., 'link' => 'firm_fk'|'wr_fk'|'dual'|'polymorphic'|'legacy_contract_id', 'columns' => [...] ]
protected function registry(): array { /* §4 */ }

/**
 * @param FirmContract|WrServiceContract $contractable
 * @param array  $data      new_customer_data khi apply, old_customer_data khi revert
 * @param string $direction 'apply' | 'revert' (chỉ để ghi log)
 */
public function sync($contractable, array $data, string $direction, $handover): void
{
    $isFirm = $contractable instanceof FirmContract;
    $morphClass = get_class($contractable);
    $cid = $contractable->id;

    foreach ($this->registry() as $e) {
        [$whereCol, $whereVals] = $this->resolveLink($e['link'], $isFirm, $cid, $morphClass);
        if ($whereCol === null) continue;          // entry không áp cho loại HĐ này

        $set = $this->buildSet($e['columns'], $data);   // dùng alias map §3.2
        if (empty($set)) continue;

        $q = DB::table($e['table'])->where($whereCol, $whereVals['id']);
        if ($e['link'] === 'polymorphic') $q->where('contractable_type', $morphClass);

        $rows = $q->update($set);                   // mass update, không loop model

        // audit (Câu 6 = B)
        DB::table('customer_handover_sync_logs')->insert([
            'customer_handover_request_id' => $handover->id,
            'direction'    => $direction,
            'table_name'   => $e['table'],
            'link_type'    => $e['link'],
            'contract_id'  => $cid,
            'rows_affected'=> $rows,
            'created_by'   => auth()->id(),
            'created_at'   => now(),
        ]);
    }
}
```

**Resolve link theo loại HĐ:**
- `firm_fk` → chỉ áp khi HĐ Firm; where `firm_contract_id = cid`.
- `wr_fk` → chỉ áp khi HĐ Wr; where `wr_service_contract_id = cid`.
- `dual` → Firm dùng `firm_contract_id`, Wr dùng `wr_service_contract_id`.
- `polymorphic` → where `contractable_id = cid AND contractable_type = morphClass` (áp cả 2 loại).
- `legacy_contract_id` → chỉ áp khi HĐ Firm; where `contract_id = cid` — **cần verify lúc code** `contract_id` trỏ đúng id HĐ hãng (xem §6, rủi ro R1).

### 3.4 Tích hợp vào controller (transaction sẵn có)

- `approve()` (sau `applyToContract`): thêm
  `(new CustomerHandoverDocumentSync())->sync($handover->contractable, $handover->new_customer_data ?? [], 'apply', $handover);`
- `cancelApprove()` (sau `revertContract`): thêm
  `(new CustomerHandoverDocumentSync())->sync($handover->contractable, $handover->old_customer_data ?? [], 'revert', $handover);`
- Cả hai đã nằm trong `DB::beginTransaction()`/`commit()` → nguyên tử.

## 4. REGISTRY — 32 bảng ACTIVE

> Cột liệt kê = cột KH thực có (khảo sát schema). Service chỉ set cột nào nằm trong alias map §3.2; cột "không map" bỏ qua tự động.

### Nhóm KHO / XUẤT

| Bảng | link | Cột cập nhật |
|---|---|---|
| `warehouse_exports` | dual | customer_id, customer_name, customer_type, customer_address, customer_mobile, customer_contact_name, contact_address, customer_contact_phone, delivery_place |
| `warehouse_export_requests` | dual | (như trên) |
| `product_exports` | dual | (như trên) |
| `product_export_requests` | dual | (như trên) + customer_short_name, identity_card_number |
| `product_prepick_requests` | polymorphic | (như warehouse_exports) |
| `product_import_requests` | dual | customer_id |
| `product_imports` | dual | customer_id |
| `warehouse_import_requests` | dual | customer_id |
| `warehouse_imports` | dual | customer_id |

### Nhóm MƯỢN BÁN

| Bảng | link | Cột cập nhật |
|---|---|---|
| `borrow_sell_requests` | polymorphic | customer_id, customer_name, customer_type, customer_address, customer_mobile, customer_contact_name, contact_address, customer_contact_phone, delivery_place |

### Nhóm BẢO HÀNH

| Bảng | link | Cột cập nhật |
|---|---|---|
| `firm_warranty_products` | polymorphic | customer_id, customer_code, customer_name |
| `firm_warranty_request_products` | polymorphic | customer_id, customer_code, customer_name |
| `firm_warranty_confirm_products` | polymorphic | customer_id, customer_code, customer_name |

### Nhóm BIÊN BẢN / NGHIỆM THU / THANH LÝ / QUYẾT TOÁN

| Bảng | link | Cột cập nhật |
|---|---|---|
| `handover_acceptance_records` | polymorphic | customer_id, customer_name, customer_address, customer_mobile, identity_card_number |
| `handover_acceptance_product_records` | legacy_contract_id | customer_id, customer_name, customer_address, customer_type, customer_identity |
| `liquidation_records` | polymorphic | customer_id, customer_name, customer_address, customer_mobile, identity_card_number |
| `settlement_contracts` | polymorphic (Firm+Wr) | customer_id, customer_name, customer_address, customer_mobile, identity_card_number |

### Nhóm LẮP RÁP / GIAO VIỆC

| Bảng | link | Cột cập nhật |
|---|---|---|
| `assembly_requests` | firm_fk | customer_id, customer_code, customer_name, customer_address, customer_contact_id, customer_contact_name, customer_contact_phones, delivery_place |
| `assign_other_requests` | firm_fk | customer_id, customer_code, customer_name, customer_address, customer_contact_id, customer_contact_name, customer_contact_phones, delivery_place |
| `wr_assign_tasks` | wr_fk | customer_id, customer_name, customer_mobile, customer_contact_id, customer_contact_name, customer_contact_phones, delivery_place |
| `wr_import_results` | firm_fk | customer_id, customer_code, customer_name, customer_contact_name, customer_contact_phones, delivery_place |

### Nhóm KẾ TOÁN / CÔNG NỢ (Câu 4 = A)

| Bảng | link | Cột cập nhật |
|---|---|---|
| `wr_accounting_service_requests` | wr_fk | customer_id, customer_name |
| `wr_accounting_services` | wr_fk | customer_id, customer_name |
| `addition_accounting_requests` | legacy_contract_id | customer_id, customer_code, customer_name |
| `contract_waiting_monthly_accounting` | polymorphic | customer_id, customer_code, customer_name |
| `contract_waiting_settlements` | polymorphic (Firm+Wr) | customer_id, customer_code, customer_name |
| `account_details` | polymorphic | customer_id |
| `bill_payment_details` | polymorphic | customer_id, customer_code, customer_name |
| `bill_payment_request_details` | polymorphic | customer_id, customer_code, customer_name |
| `bill_adjust_dept_details` | polymorphic | customer_id, customer_code, customer_name |
| `bill_productivity_settlement_quarter_contracts` | polymorphic | customer_id, customer_code, customer_name |
| `bill_commission_settlement_quarter_contracts` | polymorphic | customer_id, customer_code, customer_name |

> `account_details` (935k dòng) và `bill_*` chỉ đụng số dòng thuộc HĐ đang chuyển giao (lọc theo link) → nhẹ.

## 5. Migration bảng log

`database/migrations/xxxx_create_customer_handover_sync_logs_table.php`:

```php
Schema::create('customer_handover_sync_logs', function (Blueprint $t) {
    $t->bigIncrements('id');
    $t->unsignedBigInteger('customer_handover_request_id')->index();
    $t->string('direction', 10);            // apply | revert
    $t->string('table_name', 100);
    $t->string('link_type', 20);            // firm_fk|wr_fk|dual|polymorphic|legacy_contract_id
    $t->unsignedBigInteger('contract_id');
    $t->integer('rows_affected')->default(0);
    $t->unsignedBigInteger('created_by')->nullable();
    $t->timestamp('created_at')->nullable();
});
```

## 6. Rủi ro & edge case

- **R1 — `legacy_contract_id`:** `addition_accounting_requests`, `handover_acceptance_product_records` link qua `contract_id`. Phải verify lúc code `contract_id` = id HĐ hãng (FirmContract) hay id bảng `contracts` cũ. Nếu không map đúng → **bỏ 2 bảng này khỏi registry** thay vì cập nhật sai. (`handover_acceptance_product_records` chỉ 8 dòng, rủi ro thấp.)
- **R2 — mass update bỏ qua model event:** chấp nhận (chỉ ghi cột snapshot, không kích hoạt observer). Không dùng `->update()` của Eloquent trên collection để tránh N query.
- **R3 — phiếu tạo sau khi duyệt:** tự sinh theo KH mới của HĐ → không cần xử lý; khi revert sẽ được đưa về KH cũ luôn (khớp WHERE theo HĐ) — chấp nhận.
- **R4 — công nợ theo KH:** cập nhật `account_details`/`bill_*`/`contract_waiting_*` chuyển công nợ sang KH mới (đúng chủ trương Câu 4=A). Cần thông báo nghiệp vụ kế toán biết trước khi go-live.
- **R5 — `customer_code`/`customer_short_name` không có trong `$data`:** `customer_code` CÓ trong `$data` (snapshot đã set). `customer_short_name` phải resolve từ `Customer` — cache 1 lần `Customer::find($data['customer_id'])` trong 1 lần sync để tránh query lặp.
- **R6 — HĐ Wr chỉ có cột `firm_fk`:** entry `firm_fk`/`legacy_contract_id` KHÔNG áp cho HĐ Wr (resolveLink trả null) → bỏ qua an toàn.

## 7. Testing

- **Unit** `buildSet()`: alias map ra đúng cột từ `$data` mẫu (Firm & Wr); cột không map bị loại.
- **Unit** `resolveLink()`: 5 kiểu link × (Firm/Wr) trả đúng cột where / hoặc null.
- **Integration (dev `dev_erp_2`)**: tạo HĐ Firm có sẵn vài phiếu (xuất kho, bảo hành, biên bản) → duyệt phiếu YCCGKH → assert mọi phiếu đổi sang KH mới + có dòng log; hủy duyệt → assert revert về KH cũ.
- **Verify prod-safe**: chạy thử trên copy, kiểm `customer_handover_sync_logs` khớp số dòng thực đổi.

## 8. File thay đổi

- **Create:** `app/Services/Sale/CustomerHandoverDocumentSync.php`, migration `customer_handover_sync_logs`.
- **Modify:** `app/Http/Controllers/Sale/CustomerHandoverRequestController.php` (`approve()`, `cancelApprove()` — mỗi chỗ +1 lời gọi `sync`).
- **Không đụng** `CustomerHandoverService` (giữ nguyên logic HĐ + phụ lục).
