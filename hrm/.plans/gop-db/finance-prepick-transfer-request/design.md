# Thiết kế — Port màn "Phiếu yêu cầu điều chuyển hàng giữ" ERP → HRM

Nguồn ERP: `warehouse/prepick_transfer2` (Controller 577 dòng, Model 577 dòng, 6 blade).
Đích HRM: Tài chính → nhóm **Giữ hàng**, route `/finance/prepick-transfer-requests`.
Bảng dùng chung trên `gop_db`: `prepick_transfer2` + `prepick_transfer2_details` (**giữ nguyên
schema ERP**, không migration đổi bảng — chỉ thêm bảng lịch sử của HRM).

## 1. Nghiệp vụ (Bước 1 của skill)

**Phiếu điều chuyển hàng giữ** = chuyển số lượng hàng **đang giữ** của người lập sang **người
nhận + khách hàng nhận** khác. Duyệt 3 cấp, **chỉ bước KT duyệt mới ghi tồn**:

- trừ dòng `prepick_details` NGUỒN (`from_prepick_detail_id`)
- cộng vào dòng ĐÍCH khớp `product_id + to_employee_id + to_customer_id + expire_date + company_id`,
  chưa có thì tạo mới (**hạn giữ lấy theo dòng nguồn**, không lấy theo header)
- ghi 2 dòng `prepick_logs` (trừ + cộng)

Rất giống màn **Yêu cầu gia hạn hàng giữ** đã port — khác ở chỗ gia hạn đổi *hạn giữ*, điều chuyển
đổi *người giữ / khách hàng*. ⇒ **tái sử dụng `PrepickStockService`** (xem Bước 3b của skill), thêm
một hàm chuyển chủ sở hữu bên cạnh `moveToExpireDate()`.

### Trạng thái (giữ nguyên số của ERP)

| Số | Tên | Màu HRM |
|---|---|---|
| 5 | Chờ TP duyệt | cam `#D97706` |
| 4 | Chờ BGĐ duyệt | cam `#D97706` |
| 2 | Chờ KT duyệt | cam `#D97706` |
| 1 | Đã duyệt | xanh `#16A34A` |
| 3 | Không duyệt | đỏ `#DC2626` |

⚠️ Màn này **không có trạng thái nháp** — lập phiếu là vào thẳng `CHO_TP_DUYET` (5).
Phiếu bị **Không duyệt (3)** mới sửa/xoá lại được (`canEdit()`), sửa xong quay lại 5.

### Cột màn danh sách (ERP `index.blade.php`)

STT · Mã phiếu · Ngày lập · Người nhận · Khách nhận · Người lập · Trạng thái · Người duyệt ·
Ngày duyệt · Hành động.
HRM bổ sung (mặc định ẩn ở Cấu hình cột): Ghi chú · Lý do từ chối · Phòng ban · Người sửa/Ngày sửa.

### Bộ lọc ERP

Mã phiếu (text) · Tên, mã hàng (text) · Người nhận (select nhân viên) · Khách nhận (select KH) ·
Trạng thái · Người lập · Người duyệt · khoảng thời gian · khối Công ty/Phòng ban.
BE còn đọc thêm `contract_code` (lọc theo `prepick_transfer2_details.contractable_code`) mà ERP
**không dựng ô lọc** → HRM bổ sung ô "Số hợp đồng".

### Phạm vi xem — gộp 1 màn như đã chốt

ERP có 3 `type` (`index` = của tôi, `all`, `approve`). HRM **gộp 1 màn**: `all` + `orWhereApprovable`
(giống màn gia hạn), phân cấp theo quyền:
`Xem phiếu hàng giữ theo tổng công ty` → toàn bộ · `... theo công ty` → `company_id` ·
`... theo phòng ban` → `EmployeeManageDepartment` · còn lại → `created_by = mình`.
Phiếu **Không duyệt** chỉ người lập thấy.

### Hành động & điều kiện

| Nút | Điều kiện ERP |
|---|---|
| Xem chi tiết | `canView()` — ERP **luôn true** (lỗi ERP #1) |
| Sửa / Xoá | `status == 3 (Không duyệt)` **và** người lập là mình |
| In | không điều kiện |
| TP duyệt / Không duyệt | `status == 5` + quyền `Trưởng phòng duyệt hàng giữ` + cùng công ty + **phòng ban của NGƯỜI NHẬN** thuộc phòng mình quản lý |
| BGĐ duyệt / Không duyệt | `status == 4` + quyền `Ban giám đốc duyệt hàng giữ` + cùng công ty |
| KT duyệt / Không duyệt | `status == 2` + quyền `Kế toán duyệt hàng giữ` + cùng công ty |

`checkSwitchApprove()` quyết định TP duyệt xong đi BGĐ (4) hay thẳng KT (2): theo % đã thu của hợp
đồng gắn ở từng dòng (`account_details.account_id = 22`, `invoiceable_type` ∈ BillIncome /
BillAdjustDept / BillIncomeReport) so với `prepick_contract_types` của công ty; dòng không gắn hợp
đồng thì cộng `base_price × qty` so với `prepick_other_value`.

### Bảng chi tiết (form + chi tiết) — 11 cột

STT · Tên hàng · Mã hàng · ĐVT · Từ xuất giữ (chọn lô) · **Có thể giữ** (`in_stock`) ·
SL Đang giữ (click ra lịch sử giữ hàng) · SL Chuyển · Hạn giữ · Hợp đồng · nút xoá dòng.

Validate lập phiếu (`validateProducts`): lô phải là hàng **mình đang giữ**, `qty ≤ qty đang giữ`,
lô **chưa hết hạn giữ**. Validate lúc duyệt (`validateApproveProducts`): còn đủ SL và
`checkAvailablePrepick` (trừ phần đã yêu cầu xuất).

## 2. Lỗi ERP phát hiện khi khảo sát — HRM sẽ vá

| # | Lỗi | Xử lý ở HRM |
|---|---|---|
| 1 | `canView()` luôn `return true` — ai cũng xem được phiếu công ty khác | Áp đúng 3 cấp quyền như `searchByFilter` |
| 2 | Bản in lọc `&& comment` → dòng duyệt **không ghi chú bị mất** khỏi bảng lịch sử duyệt | In đủ mọi dòng đã duyệt |
| 3 | Bảng lịch sử duyệt trên **bản in** thiếu cột Thời gian + mã phòng (màn xem có) | In đủ 4 cột như màn xem |
| 4 | `store()`/`update()` gán `code = randomString(10)` rồi mới `generateCode()` | Sinh mã 1 lần theo id |
| 5 | `update()` **không** reset 2 cấp duyệt TP/BGĐ (chỉ reset `approver_id`) | Reset đủ 3 cấp khi sửa lại phiếu bị từ chối |
| 6 | Dòng `prepick_details` đích lấy `company_id` của **người duyệt** | Lấy theo dòng **nguồn** (đã vá ở `PrepickStockService`) |
| 7 | `prepick_logs` dòng cộng ghi `objectable_type = PrepickTransfer2Detail`, dòng trừ ghi `PrepickTransfer2` — 2 kiểu khác nhau | Thống nhất 1 kiểu, ghi hằng trong `PrepickStockService` |
| 8 | Toast báo "Bạn có một yêu cầu **xuất giữ** cần duyệt" ở 3 chỗ (sai tên nghiệp vụ) | Đổi thành "điều chuyển hàng giữ" |
| 9 | `delete()` xoá cứng cả `prepick_transfer2_details` | Giữ lịch sử (user đã chốt ở màn trước) |
| 10 | `checkSwitchApprove()` chia `$contractable->total_after_vat` không chặn 0 → lỗi chia 0 | Chặn mẫu số 0 |
| 11 | `Product->data['base_price']` — accessor ERP **hỏng trên `gop_db`** (bảng `files` đổi schema) | Lấy giá qua `product_units.is_base` → `product_unit_prices.price_type_id = 1` (đã làm ở màn gia hạn) |
| 12 | Không có bảng lịch sử thao tác | Thêm bảng `prepick_transfer_request_histories` như 2 màn trước |
| 13 | Xuất Excel/In danh sách bỏ qua bộ lọc "Số hợp đồng" (không có ô lọc) | Có ô lọc + áp vào cả in/xuất |

## 2b. Quyết định đã chốt

| # | Vấn đề | Chốt |
|---|---|---|
| 1 | Popup chọn hàng dùng chung `PrepickStockSearchModal` khoá cứng endpoint màn Yêu cầu hủy | **Thêm prop** (`endpoint`, `requireCustomer`, `title`, `subtitle`, `emptyText`) thay vì chép bản thứ 2 — user chốt 24/08/2026, đã test lại màn Yêu cầu hủy |
| 2 | Hàm suy hợp đồng của lô đang `private` ở service màn Gia hạn | **Tách ra `PrepickLotContractService`** dùng chung — user chốt 24/08/2026, đã test lại màn Gia hạn (143 lô / 126 lô có mã HĐ) |
| 3 | Cột Hợp đồng: suy từ lô hay chọn tay | **Giữ popup chọn tay như ERP** — user chốt 24/08/2026 (port nhánh `can_prepick_product`) |
| 4 | Nhãn nút trả phiếu: ERP ghi "Không duyệt", skill `button-convention` quy định "Từ chối" | **Theo SKILL → nút ghi "Từ chối"** (CLAUDE.md: skill thắng spec về hình thức UI). Trạng thái phiếu vẫn hiển thị "Không duyệt" vì đó là dữ liệu ERP. ⏳ *chờ user xác nhận lần cuối* |

## 3. Cấu trúc file dự kiến (HRM)

BE `Modules/Finance/`:
`Entities/PrepickTransfer/{PrepickTransferRequest, PrepickTransferRequestDetail, PrepickTransferRequestHistory}.php` ·
`Services/PrepickTransferRequestService.php` + `PrepickTransferRequestHistoryService.php` ·
`Http/Controllers/V1/PrepickTransferRequestController.php` ·
`Transformers/PrepickTransferResource/*` · 2 blade in (khổ **ngang**) ·
1 migration bảng lịch sử.

FE `pages/finance/prepick-transfer-requests/`: `index.vue` · `create.vue` · `_id/index.vue` ·
`_id/edit.vue` · `_id/print.vue` · `print-list.vue` · `components/PrepickTransferRequestForm.vue` ·
`components/RejectModal.vue` · `components/export-excel.js`.

**Dùng lại, không viết mới**: `PrepickStockService` (ghi tồn hàng giữ) ·
`AccountingStockService::detail()` (cột Có thể giữ) · `BillPaymentAttachmentService` (đính kèm) ·
popup tìm hàng hoá dùng chung · `ChecksEmployeePermission`.

## 4. Chặn trước khi code

1. **Local `gop_db` có 0 dòng `prepick_transfer2`** (details vẫn còn 3.942 dòng mồ côi) — dev có
   1.411 phiếu. Cần dump bảng cha từ dev về mới đối chiếu được dữ liệu thật.
2. Nhánh mới: nhánh `feat/finance-prepick-extend-request` **đang còn thay đổi chưa commit** ở cả 2
   repo → phải commit xong mới tách nhánh `feat/finance-prepick-transfer-request`.
