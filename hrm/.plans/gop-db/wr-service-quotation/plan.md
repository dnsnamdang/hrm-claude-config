# Plan — Phiếu cung cấp thông tin làm báo giá (chứng từ 3)

> @namdangit · nhánh `gop_db` · phạm vi đã chốt ở `design.md` mục 8: **chỉ chứng từ 3**,
> tính tiền ở FE, giữ dữ liệu bảo hành nhưng chưa dựng màn Phiếu bảo hành.

## Phase 0 — Nền tảng
- [x] Rà 12 bảng ERP trên DB gộp, xác nhận không cần migration
- [x] Thêm 3 quyền xem vào `PermissionsTableSeeder` (id 1515–1517); quyền LẬP tái dùng id 1514
- [x] Khai 2 bảng chính + con vào `CatalogHistoryService::TABLES` cho Lịch sử

## Phase 1 — BE Entity
- [x] `WrServiceQuotation` (trạng thái, màu, canEdit/canView/canCreateQuotation/canDelete, generateCode)
- [x] 8 entity con (product, product_item, product_service, 3 bảng device_error, extend_product + service + item, cost)
- [x] Quan hệ + scope theo `type`

## Phase 2 — BE Service
- [x] `WrServiceQuotationService`: filteredQuery + 3 scope (mine / all / waiting_create_quotation)
- [x] `prefillFromHandleRequest()` — dựng dữ liệu từ Phiếu xử lý (tách dòng theo `device_error_old`)
- [x] `deviceErrorDetails()` — định mức công + vật tư + dịch vụ theo từng lỗi thiết bị
- [x] `store/update` + sync 3 cấp bảng con
- [x] `applyStatusSideEffects()` — đóng dấu ngược 2 chứng từ trước
- [x] `delete()` — trả trạng thái 2 chứng từ trước, xoá đủ 7 bảng con
- [x] `reject()` (Từ chối tiếp nhận)

## Phase 3 — BE Controller / Request / Resource
- [x] Request validate theo trạng thái
- [x] Controller: index, prefill, show, store, update, delete, unApprove, optionsData, exportRows, printData, printListData
- [x] 2 Resource (list + detail)
- [x] Notifier `[PCCTT]`

## Phase 4 — FE module tính tiền dùng chung
- [x] `utils/wrServiceQuotationMoney.js` — port công thức ERP
- [x] Đối chiếu số học với dữ liệu ERP thật

## Phase 5 — FE màn danh sách
- [x] `pages/customer-care/wr-information-requests/index.vue` (7 cột mặc định + Khách hàng)
- [x] Bộ lọc, xuất Excel chia trang, in danh sách, Lịch sử
- [x] Gắn menu phân hệ CSKH

## Phase 6 — FE màn form + chi tiết + in
- [x] Form 4 khối A/B/C/D theo ERP, toàn bộ V2Base*
- [x] Popup chọn lỗi thiết bị / vật tư / dịch vụ
- [x] Chi tiết + In phiếu (khung giấy chuẩn)

## Phase 7 — Kiểm thử & tài liệu
- [x] Test luồng BE đối chiếu ERP (API thật trên DB gộp)
- [x] Test giao diện thật trên cổng 3002 (trọn luồng, tìm & sửa 2 lỗi)
- [ ] testcase.xlsx (HRM + ERP) + mô tả nghiệp vụ — **chỉ làm khi user yêu cầu**


### Checkpoint — 2026-08-21
Vừa hoàn thành: trọn bộ chứng từ 3 (BE 8 file + FE 11 file + module tính tiền), đã chạy thử toàn
luồng bằng API thật trên DB gộp: danh sách/lọc/xuất/in · prefill · lưu nháp · gửi đi (kèm thông
báo đúng người) · từ chối tiếp nhận · xoá (trả trạng thái 2 chứng từ trước). Dữ liệu test đã dọn.
Đang làm dở: (không có)
Bước tiếp theo: chờ user chốt 2 việc — (1) có test giao diện không, (2) quyền "Xem giá vốn hàng
hoá" có cấp cho người lập phiếu không. Sau đó mới sinh testcase + mô tả nghiệp vụ.
Blocked:


### Checkpoint — 2026-08-21 (sau khi test giao diện)
Vừa hoàn thành: chạy trọn luồng trên trình duyệt — danh sách · chi tiết · lập mới từ phiếu xử lý ·
sửa số lượng · thêm dịch vụ (giá vốn tự suy từ tỉ lệ) · thêm thiết bị bảo dưỡng + gói bảo dưỡng ·
chuyển thiết bị Sửa chữa ↔ Bảo hành · lưu nháp · sửa · in phiếu · xoá · cảnh báo chưa lưu.
Số tiền trên màn hình = số tiền trên bản in = số lưu trong DB (94.825.599 trên phiếu thử).

**2 lỗi tìm ra khi test giao diện và đã sửa:**
1. Màn LẬP MỚI thiếu cột "Giá vốn" — `prefill` không trả cờ `can_view_cost_price` nên form luôn
   coi như không có quyền, trong khi màn Chi tiết lại hiện. Đã bổ sung cờ vào `prefillFromHandleRequest()`.
2. **Lưu nháp luôn thất bại** — `quotation_term` là cột `int NOT NULL` không default, màn nháp cho
   bỏ trống nên gửi `null` -> MySQL từ chối, người dùng chỉ thấy "Lưu thất bại". Đã thêm
   `fillDefaults()` bù giá trị cho toàn bộ cột NOT NULL không default (kể cả `code` lúc insert đầu).

Đã dọn: 2 phiếu thử + log lịch sử + thông báo; 2 chứng từ trước trả về đúng trạng thái ban đầu.
Bước tiếp theo: sinh testcase (HRM + ERP) + mô tả nghiệp vụ khi user yêu cầu.
Blocked:

### Checkpoint — 2026-08-21 (sửa chữ trên nút)
Đổi nút gửi phiếu từ "Lưu và gửi duyệt" sang **"Lưu và gửi"** (`V2Footer` có sẵn
`send_and_submit_form`, không phải sửa component dùng chung như tôi nhận định lúc đầu).
Chạy lại trọn luồng gửi phiếu: validate chặn đúng 2 ô bắt buộc khi gửi (không chặn lúc Lưu nháp),
popup xác nhận đúng chữ, phiếu sang "Chờ làm báo giá", 2 chứng từ trước đóng dấu đúng, thông báo
bắn đúng người yêu cầu. Dữ liệu thử đã dọn.
Blocked:

### Checkpoint — 2026-08-21 (test kỹ toàn màn)
Chạy **10 bảng kiểm** trên dữ liệu thật (DB gộp `local_hrm_erp`), 3 vai: người lập phiếu CCTT (13,
Super admin) · người lập Phiếu yêu cầu (235) · nhân viên KHÔNG quyền (789).

| Bảng | Nội dung | Kết quả |
| --- | --- | --- |
| 1 | Quyền & bảo mật — 10 phép thử trên phiếu nháp | đúng cả 10 (403/423/400) |
| 2 | Quyền trên phiếu ĐÃ GỬI + từ chối sai người | đúng |
| 3 | Validate — 11 ca (thiếu trường, trạng thái lạ, id không tồn tại, số âm, trùng serial) | đúng cả 11 |
| 4 | Round-trip: lưu rồi đọc lại, đối chiếu TỪNG trường kể cả lồng 3 cấp | khớp hoàn toàn |
| 5 | Tiền: giao diện (JS) vs máy chủ (PHP) trên **244 phiếu thật** | khớp tuyệt đối 5/5 chỉ tiêu |
| 6 | Bản in phiếu: đủ 8 khối, số khớp màn hình, gói SL=0 bị loại, bằng chữ | đúng |
| 7 | Danh sách: 16 bộ lọc · sắp xếp 3 cột · phân trang · trần `limit` 100 · xuất file · in danh sách khổ ngang | đúng |
| 8 | 3 phạm vi `?type=` × 3 vai + ẩn phiếu nháp người khác | đúng |
| 9 | Lịch sử: 3 nhóm hành động cố định, 4 ô lọc, timeline mới→cũ, ghi lý do từ chối | đúng |
| 10 | Giao diện: cấu hình cột · chi phí tự tính · thêm/xoá dòng con · URL trực tiếp | đúng |

**2 lỗi tìm ra và đã sửa trong đợt này:**
1. Ô **Số lượng nhận cả chữ và số âm** — tiền không vỡ (mọi phép tính qua `num()`) nhưng màn hiện
   "-0" và số âm gặp đơn giá > 0 sẽ **TRỪ vào tổng**; máy chủ chỉ chặn lúc bấm Lưu. Thêm
   `cleanQty()` vào module tính tiền, gắn cho cả 4 ô số lượng của 2 bảng (11 ca kiểm đều đúng).
2. Trước đó: thiếu cờ quyền giá vốn ở màn lập mới, và `quotation_term` NOT NULL làm Lưu nháp hỏng.

**Chốt chặn ERP được xác nhận lại**: 1 phiếu xử lý chỉ lập được 1 phiếu CCTT (lần 2 trả 403).

Dữ liệu thử đã dọn sạch; 3 chứng từ trở lại đúng trạng thái ban đầu.
Blocked:
