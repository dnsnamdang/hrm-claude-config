# Fix lỗi Redmine "Fix Bug – HRM (Nội bộ)" trạng thái Mới / Phản hồi (#12141, #11927, #11926, #11905, #11835, #11769, #11644, #11509, #11501) — @cuong61n

Nhánh: `gop_db` (worktree `worktrees/gop_db-api` + `worktrees/gop_db-client`). Ngày: 12/11/2026.
Trạng thái chung: code xong + đã test e2e Playwright (12/11) trên worktree gop_db, CHƯA commit/push. Đã đổi Redmine sang "Đang tiến hành" + note.

## Phase 1 — Sửa lỗi

- [x] #12141 DM khách hàng (12/11): thêm bộ lọc **Người tạo** (lọc `customers.created_by`, BE `CustomerService` thêm `creator_id`); thêm icon ⓘ giải thích ô **Nhân viên** của khối Công ty–Phòng ban ("KH có báo giá do nhân viên này tạo") qua prop mới `employee-hint` của `V2BaseCompanyDepartmentFilter`. Chưa test UI.
- [x] #11927 Popup Thêm nhanh công việc / lỗi thiết bị (12/11): bỏ dòng mô tả (tooltip) đầu popup; ô size `sm` đồng bộ chữ placeholder; Định mức công/ĐM đàm phán/VAT/Hệ số công nghệ dùng `type=number` (chặn chữ) + báo đỏ khi quá số lẻ (4 / 2 / 2 / 2), VAT ≤ 100; Định mức công + Hệ số công nghệ bắt buộc (mặc định hệ số = 1); Đơn giá bán để trống = tự tính (ghi chú công thức dưới ô), tối đa 4 số lẻ. BE `quickCreateDeviceError` validate lại y hệt. Lưu ý: spec ghi "làm tròn" — theo quy ước dự án KHÔNG tự sửa số user nhập nên báo đỏ thay vì làm tròn.
- [x] #11926 YC kiểm tra sửa chữa bảo hành – Tạo mới (12/11): Ghi chú đổi sang textarea (`V2BaseTextarea`, col-md-6) và dời xuống SAU "Phòng tiếp nhận xử lý". Phần "tiêu đề bị lệch": ảnh QA là bản dev cũ chưa có CSS header chuẩn (`body .card .card-header.section-header` flex-center) — code gop_db đã có, chờ QA test lại.
- [x] #11905 Quản lý vấn đề (12/11): file Excel đổi "issue" → "vấn đề" (Mã/Tiêu đề/Loại vấn đề, tiêu đề file `Danh sách vấn đề`, tên file `danh_sach_van_de.xlsx`); cột **Nhãn** hiện chữ `[]` khi rỗng — nguyên nhân: slot chỉ trả comment nên Vue 2 rơi về ô mặc định in `{{ [] }}`; sửa luôn render 1 phần tử gốc.
- [x] #11835 Quản lý báo giá (12/11): bộ lọc Loại báo giá có icon ⓘ + mô tả từng loại (component mới `QuotationTypeSelect` bọc `DescriptionInfoSelect`).
- [x] #11769 Quản lý báo giá (12/11): ô tìm kiếm trong dropdown Khách hàng có placeholder "Nhập mã/tên KH (KH cá nhân: nhập đủ SĐT)" (prop mới `searchPlaceholder` của `V2BaseSelectRemote`, mặc định rỗng).
- [x] #11644 Phiếu xử lý yêu cầu – Lịch sử (12/11, phản hồi): bảng thiết bị đã ghi lịch sử từ trước, bổ sung thêm 2 ô còn thiếu: **Nội dung xử lý** (Tư vấn điện thoại) và **File đính kèm** (ghi tên tệp) vào snapshot `LogsHandleRequestChildRows`.
- [x] #11509 Quản lý báo giá – Lưu nháp chỉ chọn dự án (12/11): nguyên nhân Bảng giá trống → BE `QuotationStoreRequest` bắt `price_type_id` required → 422 "The given data was invalid." Đổi thành `nullable` (đồng bộ `QuotationUpdateRequest`, Service đã có `?? 1`); Gửi duyệt vẫn bắt buộc chọn Bảng giá ở FE.
- [x] #11501 Tab Nhiệm vụ trong dự án TKT (12/11): thêm hàng lọc nhanh như màn Nhiệm vụ (Tổng + Quá hạn + 4 nút Tôi làm / Tôi giao / Tôi theo dõi / Tôi duyệt + chip "Đang lọc") và ô lọc Ngày cập nhật vào `TaskListTab` (dùng chung tab Meeting). Tag / Giải pháp / Hạng mục / Version / Phòng ban chưa thêm — cần xác nhận.

## Phase 2 — Chưa làm (cần chốt phạm vi)

- [ ] #11739 [ERP→HRM] Đồng bộ trạng thái trong xem chi tiết (Tài chính): tiêu đề `Chi tiết "tên màn": mã phiếu` + Badge trạng thái — ~60 màn chi tiết Tài chính, header chưa có chỗ gắn badge; cần chốt thiết kế (store key `pageTitleBadge` ở header) rồi quét đồng loạt.
- [ ] #11736 [ERP→HRM] Bộ lọc danh mục hiện cả danh mục đã khoá + icon khoá: quét toàn bộ màn danh sách, cần API trả "danh mục khoá nhưng còn bản ghi dùng" — cần chốt phạm vi.

## Đã kiểm (12/11/2026) — Playwright thật trên gop_db (API :8013 + client :3013, DB local_hrm_erp, tk namdangit)
- #12141: tab lọc có ô Người tạo; chọn 1 người → request `creator_id`, bảng chỉ còn KH của người đó; nhân viên không tồn tại → 0 dòng (đã sửa lỗi lộ 1 dòng created_by=0); "Làm mới" xoá lọc; icon ⓘ ở Nhân viên hiện đúng câu.
- #11927: popup không còn dòng mô tả; 7 ô cùng 12px (ô tiền trước lệch 13px + căn phải → đè CSS riêng trong popup); gõ chữ vào ô số bị chặn; ô trống báo "Bắt buộc phải nhập/chọn"; quá số lẻ / VAT 101 / hệ số 0 báo đỏ và GIỮ nguyên số gõ; lưu hợp lệ → 201, lỗi mới tự tích vào dòng. API: 11 ca hợp lệ/không hợp lệ đúng.
- #11926: xác nhận lỗi header THẬT: media ≤1400px của màn ép h6 `flex:1 1 100%` làm "Thông tin khách hàng" và dòng người tạo nằm 2 hàng lệch nhau — đã thêm class `wr-head-inline` chỉ cho khối này (đo ở 1200/1366/1600px: tiêu đề và người tạo cùng tâm 18px). Ghi chú là textarea sau Phòng tiếp nhận; lưu nháp trống vẫn 422 như cũ.
- #11905: không còn ô "[]" ở cột Nhãn; file tải về `danh_sach_van_de.xlsx`, header "Mã vấn đề / Tiêu đề vấn đề / Loại vấn đề", tiêu đề "Danh sách vấn đề"; popup chọn trường xuất khớp chữ.
- #11835: dropdown Loại báo giá có 2 icon ⓘ, rê chuột ra đúng mô tả; lọc `quotation_type=normal` ra 20 dòng.
- #11769: ô tìm trong dropdown Khách hàng có placeholder, tìm "Z131" ra KH; ô Dự án TKT không bị ảnh hưởng.
- #11644: sửa Nội dung xử lý + tải file đính kèm → popup Lịch sử hiện "Nội dung xử lý: lần 1 → lần 2; File đính kèm: (trống) → tên tệp".
- #11509: chỉ chọn dự án + xoá Bảng giá → Lưu nháp 200 tạo BG; không chọn gì → báo đỏ "Bắt buộc phải nhập" + toast; Gửi duyệt khi trống Bảng giá → chặn FE "Vui lòng chọn bảng giá", 0 request. API: price_type_id null → lưu bảng 1, giá trị 9 → 422.
- #11501: tab Nhiệm vụ dự án 151: Tổng 11; nút "tôi làm" → 8 (khớp DB), "tôi giao" → 11, "tôi theo dõi" → 0; bấm × bỏ lọc về 11; tab Nhiệm vụ của Meeting vẫn chạy (cùng component).
- Dọn dữ liệu test local (device_errors ZZ*, báo giá 238–240, trả phiếu xử lý 5293 + xoá 4 dòng lịch sử test). Đã tắt server :8013/:3013.
- Lỗi console còn lại đều có sẵn từ trước, không do bản sửa (vd `visibleExportFields` ở customers/index.vue, `errors` trùng trong CreateIssueModal, prop `hasCustomer` ở Meeting).
- `php -l` file PHP đã sửa: OK.
