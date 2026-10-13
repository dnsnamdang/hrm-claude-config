# Design chi tiết — Phase 1: Module phiếu YCCGKH + duyệt đổi KH trên HĐ

## 1. Phạm vi
7 màn (Hợp đồng action + lịch sử, Dashboard box, DS phiếu, DS chờ duyệt, Tạo/sửa, Duyệt, Chi tiết) + logic duyệt ghi đè snapshot KH trên HĐ + hủy duyệt revert. KHÔNG lan 13 luồng/báo cáo.

## 2. Database

### 2.1. `customer_handover_requests` (migration mới)
| Cột | Kiểu | Ghi chú |
|---|---|---|
| id | bigint PK | |
| code | string, nullable | `TPE.YCCGKH.mmyy.NNNNN`, sinh khi gửi duyệt (mã cty + YCCGKH + mmyy + 5 số tịnh tiến) |
| contractable_id | unsignedBigInteger | id HĐ |
| contractable_type | string | `App\Model\Sale\Firm\Contract\FirmContract` \| `App\Model\Customers\WrServiceContract` |
| contract_code | string | copy để hiển thị/lọc |
| old_customer_id | unsignedBigInteger, index | lọc list |
| new_customer_id | unsignedBigInteger, index | lọc list |
| old_customer_data | json | snapshot KH cũ trên HĐ tại thời điểm tạo phiếu |
| new_customer_data | json | KH mới đã chọn (xem 2.2) |
| reason | text | Lý do thay đổi KH (bắt buộc) |
| reject_reason | text nullable | Lý do không duyệt |
| status | tinyInteger | 1 Đang tạo, 2 Chờ duyệt, 3 Đã duyệt, 4 Không duyệt, 5 Hủy duyệt |
| company_id, department_id, part_id | unsignedBigInteger nullable | của người tạo (lọc phân quyền) |
| created_by, approved_by | unsignedBigInteger nullable | |
| approved_at | datetime nullable | |
| timestamps | | |

### 2.2. `new_customer_data` / `old_customer_data` (JSON)
Các field snapshot (map sang cột HĐ khi áp):
- customer_id, customer_code, customer_name, customer_type
- customer_address, customer_mobile, customer_fax, customer_tax_code/identity, grant_date, grant_location
- deputy_id, deputy_name, deputy_role (người đại diện + chức vụ)
- delivery_place_id / receiver_address (địa chỉ giao hàng / địa chỉ sửa chữa với HĐDV)
- account: {id, number, name, bank_name, bank_branch, bank_province_id}
- contact: {id, name, address, phone}
- vehicle_manufact_id (hãng)

### 2.3. `customer_handover_request_histories` (lịch sử duyệt)
| Cột | Ghi chú |
|---|---|
| id, customer_handover_request_id | |
| created_by | tài khoản thao tác |
| action | gửi duyệt / duyệt / không duyệt / hủy duyệt |
| content | mô tả (từ KH cũ → KH mới; lý do…) |
| created_at | thời gian |

### 2.4. Files
Dùng bảng `files` chung: `table='customer_handover_requests'`, `table_id=<id>`. Bắt buộc ≥1 file, mỗi file ≤60MB, loại: ảnh/word/excel/pdf.

## 3. Trạng thái + luồng nghiệp vụ

| Hành động | Từ trạng thái | Kết quả |
|---|---|---|
| Lưu | (mới) / Đang tạo | Đang tạo (chưa sinh code) |
| Lưu & gửi | Đang tạo | Chờ duyệt + sinh `code` + log "gửi duyệt" |
| Duyệt | Chờ duyệt | Đã duyệt → **áp `new_customer_data` lên HĐ** + set approved_by/at + log + ẩn action chuyển giao trên HĐ |
| Không duyệt | Chờ duyệt | Không duyệt + reject_reason (bắt buộc) + log; KHÔNG đổi HĐ |
| Hủy duyệt | Đã duyệt | Guard OK → **revert `old_customer_data` lên HĐ** → Hủy duyệt + log; Guard fail → chặn + msg |
| Sửa | Đang tạo | chỉ sửa khi Đang tạo (người tạo) |
| Hủy phiếu | Đang tạo | confirm → xóa/bỏ, không lưu |

**Guard hủy duyệt**: HĐ chưa phát sinh đề nghị xuất hóa đơn (tái dùng tiền điều kiện tạo phiếu). Nếu đã phát sinh → không cho hủy duyệt (msg).

## 4. Tiền điều kiện tạo phiếu (action "Chuyển giao khách hàng" trên HĐ)
- Loại HĐ ∈ {HĐ vật tư(1), HĐ dự án(4)} hoặc WrServiceContract; **không** nguyên tắc.
- HĐ status **Có hiệu lực**.
- **Chưa có** đề nghị xuất hóa đơn (ở mọi trạng thái) → nếu có: msg vàng "Hợp đồng đã có đề nghị xuất hóa đơn, không thể chuyển giao khách hàng".
- **Chưa có** phiếu YCCGKH (Đang tạo trở đi) cho HĐ đó.
- **Chỉ người tạo HĐ** mới được chuyển giao HĐ đó.
- HĐ đã chuyển giao thành công 1 lần → **ẩn** action (1 HĐ chỉ chuyển 1 lần).

## 5. Áp/Revert lên HĐ (CustomerHandoverService)
- `applyToContract($req)`: map `new_customer_data` → cột snapshot KH của HĐ theo loại:
  - FirmContract: customer_id, customer_name, customer_type, customer_address, customer_mobile, customer_fax, customer_contact_id/name, contact_address, customer_contact_phone, customer_deputy_id, deputy_name, deputy_role, customer_account_id + account_number/name + bank_name/branch/province_id, delivery_place, vehicle_manufact_id.
  - WrServiceContract: các cột tương ứng (customer_*, customer_deputy_*, customer_account_*, receiver_address, vehicle_manufact_id, customer_tax/identity/grant_*).
- `revertContract($req)`: map `old_customer_data` ngược lại.
- Ghi `customer_handover_request_histories` + đẩy event vào khu "lịch sử duyệt" trên màn view HĐ.
- Bọc transaction; rethrow ValidationException (không catch chung).

## 6. Backend
- Route prefix `admin/sale/customer-handover-requests` (menu Kinh doanh → Đơn hàng hợp đồng) + nhánh Chờ duyệt.
- `Sale\CustomerHandoverRequestController`: index, searchData (Yajra server-side), create, store, edit, update, show, approve, reject, cancelApprove, exportExcel; popup: searchContract, searchCustomer, searchContact (tái dùng logic báo giá).
- Model `Sale\CustomerHandoverRequest` (+ History), Service `Sale\CustomerHandoverService`, FormRequest `CustomerHandoverStoreRequest` (validate + rethrow ValidationException; FE hiện inline is-invalid).
- FirmContract/WrServiceContract: accessor `can_handover` (tiền điều kiện) + khu lịch sử duyệt trên view.
- Permissions seed (mục 8) + middleware `checkPermission` cho store/approve/reject/cancelApprove/exportExcel.

## 7. Frontend (Blade + AngularJS 1.3.9)
- **DS phiếu** + **DS chờ duyệt**: DataTable server-side; bộ lọc: công ty/phòng/bộ phận (ẩn/hiện theo quyền, mặc định theo người xem), số phiếu, từ-đến ngày lập, số HĐ, KH mới, KH cũ, trạng thái, người tạo, người duyệt; cột: STT, Số phiếu (link), KH mới, KH cũ, Số HĐ (link), Người lập, Ngày lập, Người duyệt, Ngày duyệt, Trạng thái (màu), Hành động; phân trang; Xuất Excel; Tạo mới.
- **Dashboard**: box "YC chuyển giao khách hàng" trong group Quản lý hợp đồng, đơn hàng — đếm Chờ duyệt, link DS chờ duyệt; chỉ hiện nếu có quyền Duyệt.
- **Tạo/sửa**: 2 tab (Thông tin thay đổi / Thông tin HĐ + mẫu in).
  - Tab thay đổi: Số HĐ (link/popup tìm HĐ), Lý do (bắt buộc); **KH trước** (readonly) | **KH sau** (popup chọn KH + đại diện + địa chỉ giao/sửa + TK NH + liên hệ + hãng) — 4 case DN/CN; 2 template: HĐ bán & HĐDV; File đính kèm bắt buộc.
  - Validate: inline is-invalid + "Chưa điền đủ thông tin"; "File vượt quá 60mb"; "Khách hàng không thuộc thị trường được phân công".
  - Popup chọn KH/liên hệ: tái dùng báo giá + **logic mới**: KH cá nhân show sẵn data do người đó tạo/đã phát sinh báo giá (không cần search SĐT).
- **Duyệt phiếu**: 2 cột KH trước/sau + nút Duyệt / Không duyệt (nhập lý do).
- **Xem chi tiết**: readonly toàn bộ + tải file + bảng lịch sử duyệt.

## 8. Phân quyền (group "Phiếu YC chuyển giao khách hàng")
- Xem DS theo **tổng công ty / công ty / phòng ban / bộ phận** (4 quyền).
- **Duyệt phiếu YC chuyển giao khách hàng** (duyệt/không duyệt/hủy duyệt trong phạm vi quản lý).
- Không quyền → chỉ thấy phiếu mình tạo.

## 9. Edge cases
- 1 HĐ chỉ chuyển giao 1 lần (ẩn action sau Đã duyệt).
- HĐ nguyên tắc loại trừ; HĐ đã có đề nghị xuất HĐ → chặn.
- Chỉ người tạo HĐ được chuyển giao.
- Hủy duyệt có guard.
- KH mới không thuộc thị trường được phân công → chặn lưu.

## 10. Ngoài phạm vi Phase 1
- Lan thay đổi sang 13 luồng + báo cáo (Phase 2+).
- Tab mẫu in nâng cao (chỉnh sửa + update view HĐ) — cân nhắc Phase sau nếu phức tạp.
- Biên bản nghiệm thu đã ký KH cũ.

---
## Ghi chú chốt khi implement (cập nhật sau Task 1)
- `customer_handover_request_histories`: cột log tên **`note`** (KHÔNG phải `content`) + có thêm `status`(nullable, log trạng thái tại action). Task 7/8 dùng `note`.
- Files dùng **File model ERP polymorphic** (`fileable_id`/`fileable_type`) → `morphMany(\App\Model\Common\File, 'fileable')`; khi lưu set `fileable_id/fileable_type` (KHÔNG dùng `table/table_id` như convention HRM). §2.4 điều chỉnh theo đây.

## Bổ sung yêu cầu (2026-07-04): áp cả PHỤ LỤC
- Khi duyệt (applyToContract) đổi KH trên HĐ chính → phải đổi luôn trên **TẤT CẢ phụ lục**: phụ lục giảm (PLG) + phụ lục bổ sung (PLBS). Áp cho CẢ HĐ hãng (FirmContract) và HĐ dịch vụ (WrServiceContract).
- Cấu trúc: phụ lục là record CÙNG MODEL (self-ref):
  - FirmContract: `->addition_annexes()` (type PL_BO_SUNG=2,HDDA_PLBS,HDNT_PLBS) + `->decrease_annexes()` (type PL_GIAM=3,HDDA_PLG,DHNT_PLG).
  - WrServiceContract: `->addition_annexes()` + `->annexes()`.
- => applyToContract/revertContract: dùng cùng mapping cột KH, áp cho HĐ chính + lặp qua tất cả phụ lục (addition + decrease/annexes). Vì phụ lục cùng model nên tái dùng hàm map 1 record.
- revert (hủy duyệt): áp old_customer_data lên HĐ chính + tất cả phụ lục.

## Ghi chú delivery_place (sau Task 7)
- FirmContract: `delivery_place` là ACCESSOR (getDeliveryPlaceAttribute, đọc từ báo giá/parent) — firm_contracts KHÔNG có cột thực → KHÔNG áp được "địa chỉ giao hàng" khi chuyển KH (dẫn xuất từ báo giá gốc, không đổi). Đúng behavior.
- WrServiceContract: `delivery_place` là CỘT THỰC (+ receiver_name/address/mobile) → áp được bình thường.
