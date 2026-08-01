# Design — HDSD màn "Phê duyệt → Báo giá chờ duyệt"

## Mục tiêu
HDSD Word cho TP/BGĐ duyệt giá tại `/assign/quotations/pending-approval`, giải thích cả cơ chế
cấp duyệt tự tính chứ không chỉ liệt kê nút.

## Hiểu biết nghiệp vụ chốt được từ code
- Hàng đợi 2 nhóm: `status=2 Chờ TP duyệt` (lọc theo `department_id ∈ employee_manage_departments`
  của user) và `status=3 Chờ BGĐ duyệt` (lọc theo `company_id` của user). Không có quyền nào →
  `whereRaw('1=0')`; có quyền TP nhưng không quản phòng nào → cũng rỗng.
- Cấp duyệt = `max(levelV, levelM)` từ `BomPriceApprovalConfigService::calculateApprovalLevel`
  (ngưỡng min ≤ value < max; không match → mặc định cấp 3). C1 tự duyệt (không vào hàng đợi),
  C2 TP chốt, C3 TP → BGĐ.
- Không có màn duyệt riêng: nút Duyệt / Duyệt & chuyển BGĐ / BGĐ duyệt / Từ chối nằm ở footer màn
  chi tiết `/assign/quotations/{id}`; danh sách chỉ có nút mắt "Xem và duyệt".
- Duyệt xong (`status=4`): recomputeTotals, ghi approved_by/at, PricingRequest → Đã có báo giá,
  dự án TKT → Thương thảo giá, Solution → Đã duyệt giá, sync ERP, notify 3 nhóm, log history.
- Từ chối: về `status=1 Đang tạo`, lưu `rejected_reason`, XOÁ submitted_at/tp_approved_*/approved_*/
  **price_approval_level** → gửi lại sẽ tính lại cấp duyệt theo số liệu mới.
- Cột giá vốn/TSLN gate theo `can_view_cost_price`.
- Tuỳ chỉnh cột lưu theo user (`human/column-customizations`, table `quotations_pending_approval`)
  ⇒ bảng người dùng có thể khác thứ tự mặc định.

## Output
- `HDSD_luongchinh/HDSD_PheDuyet_BaoGiaChoDuyet.docx` — 12 Heading 1, 11 hình, 13 bảng, ~1.6MB
- Ảnh: `hdsd_bgchoduyet_shots/` (11 ảnh, 1440x900)
- Tái dựng: `/opt/homebrew/opt/python@3.14/bin/python3.14 <scratchpad>/gen_bg_choduyet.py` chạy từ
  thư mục gốc `HRM/`.
- **Style**: khung = `HDSD_KhachHang.docx` (bản gốc thư mục HRM/), dựng qua `hdsd_clean.HDSDClean`
  (subclass của `hdsd_p5_work/hdsd_lib.HDSD`) — KHÔNG áp direct formatting: Heading/List Bullet/ô bảng
  để nguyên style, body chỉ canh đều, ảnh canh giữa 6.0". Đây là điểm khác `hdsd_lib.HDSD` gốc (ép
  Times New Roman + line-spacing 1.5 + Heading canh giữa) — dùng bản clean để đồng bộ với file mẫu.

## Liên quan
- `HDSD_luongchinh/HDSD_CauHinhDuyetGia.docx` — màn cấu hình ngưỡng sinh ra cấp duyệt.
- `HDSD_luongchinh/HDSD_PheDuyet_YeuCauGiaiPhap.docx` — màn phê duyệt còn lại trong nhóm Phê duyệt.
