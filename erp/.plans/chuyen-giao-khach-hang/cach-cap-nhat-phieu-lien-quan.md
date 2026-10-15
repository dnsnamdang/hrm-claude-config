# Cách hệ thống cập nhật phiếu liên quan khi DUYỆT yêu cầu chuyển giao khách hàng

> Tài liệu giải thích chi tiết cơ chế: khi **Duyệt** một phiếu YCCGKH, ngoài việc đổi khách hàng (KH) trên hợp đồng + phụ lục, hệ thống còn **tự động cập nhật KH mới xuống toàn bộ phiếu nghiệp vụ đã sinh ra từ hợp đồng đó**; khi **Hủy duyệt** thì **trả về KH cũ** (đối xứng).
>
> Code liên quan: `app/Services/Sale/CustomerHandoverDocumentSync.php`, `app/Services/Sale/CustomerHandoverService.php`, `app/Http/Controllers/Sale/CustomerHandoverRequestController.php`.

---

## 1. Toàn cảnh luồng khi bấm "Duyệt"

Trong `CustomerHandoverRequestController::approve()`, mọi thao tác nằm trong **1 transaction** (`DB::beginTransaction … commit`), theo thứ tự:

1. **Đổi KH trên hợp đồng + tất cả phụ lục** — `CustomerHandoverService::applyToContract($handover)`
   - Áp `new_customer_data` (KH mới) lên HĐ chính.
   - Áp lên phụ lục bổ sung (PLBS) và phụ lục giảm (PLG).
   - Áp mẫu in đã sửa (nếu có) vào HĐ.
2. **Lan KH mới xuống phiếu liên quan** — `CustomerHandoverDocumentSync::sync($contractable, $new_customer_data, 'apply', $handover)`
   - Duyệt **registry 32 bảng phiếu**, mỗi bảng chạy một câu `UPDATE` đổi cột KH sang KH mới.
   - Ghi log mỗi bảng vào `customer_handover_sync_logs`.
3. Chuyển trạng thái phiếu → **Đã duyệt**, ghi người/thời điểm duyệt + lịch sử.

Vì tất cả trong **1 transaction**: nếu bất kỳ bước nào lỗi → **rollback toàn bộ** (HĐ, phụ lục, mọi phiếu, log) → dữ liệu không bị cập nhật dở dang.

Khi **Hủy duyệt** (`cancelApprove()`): tương tự nhưng dùng `old_customer_data` (KH cũ) với `direction = 'revert'` → mọi phiếu trở lại KH cũ.

---

## 2. Nguồn dữ liệu khách hàng (`$data`)

- **Khi duyệt**: lấy từ `new_customer_data` (KH mới, đã lưu trên phiếu YCCGKH lúc tạo/sửa).
- **Khi hủy duyệt**: lấy từ `old_customer_data` (snapshot KH cũ lúc tạo phiếu).

Cấu trúc `$data` (do `CustomerHandoverService::snapshotContractCustomer()` sinh ra):

```
customer_id, customer_code, customer_name, customer_type, customer_address,
customer_mobile, customer_fax, customer_tax_code, customer_identity,
grant_date, grant_location, deputy_id, deputy_name, deputy_role,
delivery_place, receiver_address, vehicle_manufact_id,
account:  { id, number, name, bank_name, bank_branch, bank_province_id }
contact:  { id, name, address, phone }
```

---

## 3. Cách xác định cột nối phiếu ↔ hợp đồng (5 kiểu link)

Mỗi bảng phiếu nối về hợp đồng theo một trong 5 kiểu. `sync()` chọn đúng điều kiện `WHERE` theo **loại hợp đồng** đang chuyển giao (HĐ hãng `FirmContract` hay HĐ dịch vụ `WrServiceContract`):

| Kiểu link | Điều kiện WHERE | Áp cho loại HĐ |
| --- | --- | --- |
| `firm_fk` | `firm_contract_id = <id HĐ>` | Chỉ HĐ hãng |
| `wr_fk` | `wr_service_contract_id = <id HĐ>` | Chỉ HĐ dịch vụ |
| `dual` | HĐ hãng → `firm_contract_id`; HĐ dịch vụ → `wr_service_contract_id` | Cả hai |
| `polymorphic` | `contractable_id = <id HĐ>` **AND** `contractable_type = <class HĐ>` | Cả hai |
| `legacy_contract_id` | `contract_id = <id HĐ>` | Chỉ HĐ hãng |

**Class polymorphic thực tế** (đã kiểm trên DB production, không dùng morphMap):
- HĐ hãng = `App\Model\Sale\Firm\Contract\FirmContract`
- HĐ dịch vụ = `App\Model\Customers\WrServiceContract`

Nhờ điều kiện `contractable_type` khớp đúng class, các bảng dùng chung như `bill_payment_details` (chứa cả HĐ mua `InlandBuyContract`, `BuyContract2`…) **không bị đụng nhầm** — chỉ cập nhật đúng phiếu của HĐ đang chuyển giao.

> Ghi chú `legacy_contract_id`: 2 bảng `addition_accounting_requests` và `handover_acceptance_product_records` nối qua cột `contract_id` (đời cũ). Đã kiểm trên production: `contract_id` khớp **100% `firm_contracts.id`** (35/35 và 8/8) → chỉ áp cho HĐ hãng là chính xác.

---

## 4. Danh sách 32 bảng phiếu được cập nhật + cột KH

> Chỉ cập nhật cột nào bảng thực có. Giá trị lấy từ `$data` (mục 2). Cột không nằm trong bảng ánh xạ (mục 5) sẽ được **giữ nguyên**.

### Nhóm Kho / Xuất nhập
| Bảng | Kiểu link | Cột cập nhật |
| --- | --- | --- |
| `warehouse_exports` (Xuất kho) | dual | customer_id, customer_name, customer_type, customer_address, customer_mobile, customer_contact_name, contact_address, customer_contact_phone, delivery_place |
| `warehouse_export_requests` (YC xuất kho) | dual | *(như trên)* |
| `product_exports` (Xuất hàng) | dual | *(như trên)* |
| `product_export_requests` (YC xuất hàng) | dual | *(như trên)* + customer_short_name, identity_card_number |
| `product_prepick_requests` (YC soạn hàng) | polymorphic | *(như warehouse_exports)* |
| `product_import_requests` (YC nhập hàng) | dual | customer_id |
| `product_imports` (Nhập hàng) | dual | customer_id |
| `warehouse_import_requests` (YC nhập kho) | dual | customer_id |
| `warehouse_imports` (Nhập kho) | dual | customer_id |

### Nhóm Mượn bán
| Bảng | Kiểu link | Cột cập nhật |
| --- | --- | --- |
| `borrow_sell_requests` (YC xuất bán hàng mượn) | polymorphic | customer_id, customer_name, customer_type, customer_address, customer_mobile, customer_contact_name, contact_address, customer_contact_phone, delivery_place |

### Nhóm Bảo hành
| Bảng | Kiểu link | Cột cập nhật |
| --- | --- | --- |
| `firm_warranty_products` (SP bảo hành) | polymorphic | customer_id, customer_code, customer_name |
| `firm_warranty_request_products` (SP YC bảo hành) | polymorphic | customer_id, customer_code, customer_name |
| `firm_warranty_confirm_products` (SP xác nhận bảo hành) | polymorphic | customer_id, customer_code, customer_name |

### Nhóm Biên bản / Quyết toán
| Bảng | Kiểu link | Cột cập nhật |
| --- | --- | --- |
| `handover_acceptance_records` (BB nghiệm thu bàn giao) | polymorphic | customer_id, customer_name, customer_address, customer_mobile, identity_card_number |
| `handover_acceptance_product_records` (BB nghiệm thu — hàng) | legacy_contract_id | customer_id, customer_name, customer_address, customer_type, customer_identity |
| `liquidation_records` (BB thanh lý) | polymorphic | customer_id, customer_name, customer_address, customer_mobile, identity_card_number |
| `settlement_contracts` (Quyết toán HĐ) | polymorphic | customer_id, customer_name, customer_address, customer_mobile, identity_card_number |

### Nhóm Giao việc
| Bảng | Kiểu link | Cột cập nhật |
| --- | --- | --- |
| `assembly_requests` (YC lắp đặt bàn giao) | firm_fk | customer_id, customer_code, customer_name, customer_address, customer_contact_id, customer_contact_name, customer_contact_phones, delivery_place |
| `assign_other_requests` (YC giao việc khác) | firm_fk | *(như assembly_requests)* |
| `wr_assign_tasks` (Phiếu giao việc dịch vụ) | wr_fk | customer_id, customer_name, customer_mobile, customer_contact_id, customer_contact_name, customer_contact_phones, delivery_place |
| `wr_import_results` (Kết quả nhập dịch vụ) | firm_fk | customer_id, customer_code, customer_name, customer_contact_name, customer_contact_phones, delivery_place |

### Nhóm Kế toán / Công nợ
| Bảng | Kiểu link | Cột cập nhật |
| --- | --- | --- |
| `wr_accounting_service_requests` (YC hạch toán dịch vụ) | wr_fk | customer_id, customer_name |
| `wr_accounting_services` (Hạch toán dịch vụ) | wr_fk | customer_id, customer_name |
| `addition_accounting_requests` (YC hạch toán bổ sung) | legacy_contract_id | customer_id, customer_code, customer_name |
| `contract_waiting_monthly_accounting` (Chờ hạch toán theo tháng) | polymorphic | customer_id, customer_code, customer_name |
| `contract_waiting_settlements` (Chờ quyết toán) | polymorphic | customer_id, customer_code, customer_name |
| `account_details` (Sổ chi tiết công nợ) | polymorphic | customer_id |
| `bill_payment_details` (Chi tiết thanh toán) | polymorphic | customer_id, customer_code, customer_name |
| `bill_payment_request_details` (Chi tiết YC thanh toán) | polymorphic | customer_id, customer_code, customer_name |
| `bill_adjust_dept_details` (Chi tiết điều chỉnh công nợ) | polymorphic | customer_id, customer_code, customer_name |
| `bill_productivity_settlement_quarter_contracts` (Quyết toán năng suất quý) | polymorphic | customer_id, customer_code, customer_name |
| `bill_commission_settlement_quarter_contracts` (Quyết toán hoa hồng quý) | polymorphic | customer_id, customer_code, customer_name |

---

## 5. Bảng ánh xạ cột phiếu → giá trị `$data`

`sync()` dùng một hàm dùng chung (`aliasValue`/`buildSet`) để điền giá trị cho từng cột:

| Cột trên phiếu | Lấy từ `$data` |
| --- | --- |
| customer_id | customer_id |
| customer_code | customer_code |
| customer_name | customer_name |
| customer_type | customer_type |
| customer_address | customer_address |
| customer_mobile | customer_mobile |
| customer_fax | customer_fax |
| customer_tax_code | customer_tax_code |
| identity_card_number / customer_identity | customer_identity |
| customer_short_name | tra `Customer::find(customer_id)->short_name` (không có sẵn trong `$data`) |
| delivery_place | delivery_place |
| deputy_name | deputy_name |
| customer_contact_id | contact.id |
| customer_contact_name | contact.name |
| contact_address | contact.address |
| customer_contact_phone / customer_contact_phones | contact.phone |

**Các cột KHÔNG bao giờ đụng (giữ nguyên):** `delivery_place_id`, `receiver_id`, `receiver_name`, `receiver_phone` — vì đây là *id địa chỉ giao* / *người nhận*, không phải danh tính KH.

---

## 6. Ghi vết (audit) — bảng `customer_handover_sync_logs`

Mỗi bảng được cập nhật đều ghi 1 dòng log:

| Cột | Ý nghĩa |
| --- | --- |
| customer_handover_request_id | Phiếu YCCGKH nào |
| direction | `apply` (khi duyệt) / `revert` (khi hủy duyệt) |
| table_name | Tên bảng phiếu đã cập nhật |
| link_type | Kiểu link (firm_fk / wr_fk / dual / polymorphic / legacy_contract_id) |
| contract_id | Id hợp đồng |
| rows_affected | Số dòng (bản ghi) đã đổi ở bảng đó |
| created_by, created_at | Người + thời điểm |

**Xem trên giao diện:** vào **màn chi tiết phiếu YCCGKH đã Duyệt/Hủy duyệt** → panel **"Phiếu liên quan đã cập nhật"** (nằm trên "Lịch sử duyệt"): gộp theo *Khi duyệt / Khi hủy duyệt* + theo 6 nhóm nghiệp vụ, hiện số bản ghi mỗi loại phiếu (bỏ dòng 0).

---

## 7. Lưu ý & trường hợp đặc biệt

- **Chỉ chạm đúng phiếu của hợp đồng**: điều kiện `WHERE` theo link + `contractable_type` bảo đảm không đụng phiếu của hợp đồng/khách khác.
- **HĐ dịch vụ (Wr)**: các bảng `firm_fk`/`legacy_contract_id` được **bỏ qua** (không áp) → chỉ cập nhật các bảng `wr_fk`/`polymorphic`/`dual`.
- **Bản ghi ≠ phiếu**: một số bảng là *dòng chi tiết* (VD `firm_warranty_products`, `bill_*details`, `account_details`) nên `rows_affected` đếm **số dòng**, một phiếu có thể nhiều dòng.
- **Cập nhật cả bút toán kế toán đã hạch toán** (theo yêu cầu nghiệp vụ): công nợ sẽ chuyển sang KH mới. Cần thông báo bộ phận kế toán trước khi vận hành.
- **Số bản ghi = null/rỗng**: nếu `new_customer_data` thiếu khóa nào, cột tương ứng sẽ được ghi giá trị của khóa đó (có thể rỗng) — phản ánh đúng KH mới; dữ liệu KH mới do FE gửi lên luôn đủ khóa.
- **Phiếu tạo *sau* khi duyệt**: tự sinh theo KH mới của HĐ (không cần xử lý thêm).
- **Hiệu năng**: đã thêm migration index cho 16 bảng lớn (>5000 dòng) trên cột link để tránh full-scan + giữ lock lâu trong transaction khi duyệt.
- **Phiếu YCCGKH duyệt *trước* khi triển khai tính năng này**: không có dòng log (vì log ghi lúc duyệt) → panel sẽ ẩn. Nếu cần đồng bộ ngược cho các HĐ đã chuyển giao trước đó, cần script data-fix riêng.

---

## 8. Tóm tắt một câu

> **Duyệt YCCGKH** = đổi KH trên HĐ + phụ lục **+ tự động cập nhật 32 loại phiếu nghiệp vụ** (kho, bảo hành, biên bản, giao việc, kế toán/công nợ) sang KH mới, ghi log đầy đủ; **Hủy duyệt** thì đảo ngược tất cả về KH cũ — toàn bộ trong một transaction an toàn.
