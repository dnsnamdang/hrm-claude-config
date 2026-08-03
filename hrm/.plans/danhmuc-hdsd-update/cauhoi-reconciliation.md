# Đối chiếu code vs HDSD cũ — Màn "Ngân hàng câu hỏi khảo sát" (questions)

> Agent Opus 2026-07-16. Doc cũ: `scratchpad_doc_cauhoi.txt`. Ảnh: `hdsd_cauhoi_shots/`. Template CÓ Caption/List Bullet/Light Grid Accent 1 → generator kiểu gen_lvkh.py.

## Thay đổi lớn nhất
Bỏ hẳn **Nhóm ngành (scope) + Nhóm giải pháp (industry)** → thay bằng **Ứng dụng (application_id)** + **application_scope** (1=Tất cả, 2=Theo ứng dụng). Migration 2026_06_26_100001/100002. Giống hệt màn Phiếu/Ứng dụng.

## Route & bản đồ màn
- `/assign/questions` (list) · `/questions/add` (tạo, TRANG RIÊNG) · `/questions/:id` (xem) · `/questions/:id/edit` (sửa).
- Cột (9): STT — Tiêu đề câu hỏi (link chi tiết) — Loại dữ liệu — **Phạm vi câu hỏi** (Tất cả/Theo ứng dụng) — **Ứng dụng** (thay 2 cột nhóm cũ) — Người cập nhật — Ngày cập nhật — Trạng thái — Hành động (menu bánh răng).
- Toolbar: Tạo mới · Xuất excel · Bộ lọc (toggle). (Nút In đã comment, không hiện.)
- Menu bánh răng từng dòng: Xem (luôn) · Sửa (luôn) · Khóa (khi status=1) · Mở khóa (khi status=2) · Xóa (luôn).
- Bộ lọc (4): Tiêu đề câu hỏi (keyword) · **Ứng dụng** (thay Nhóm ngành+Nhóm giải pháp) · Trạng thái · Loại dữ liệu. Auto-search (trừ keyword bấm tìm).
- Quyền: `Xem danh mục câu hỏi khảo sát` (id 997) / `Quản lý danh mục câu hỏi khảo sát` (id 982). show/getAll không middleware (getAll trỏ method không tồn tại — báo team).

## Form Tạo/Sửa/Xem (QuestionForm, 2 cột — trang riêng)
Cột trái (cấu hình):
| Trường | Control | Bắt buộc | Mặc định | Điều kiện |
|---|---|---|---|---|
| Phạm vi áp dụng * | select2 (allowClear=false) | Có | **Theo ứng dụng (2)** | Chọn "Tất cả" → ẩn Ứng dụng |
| Ứng dụng * | select2 | Có (khi scope=2) | null | chỉ hiện khi Phạm vi = Theo ứng dụng |
| Loại dữ liệu * | select2 | Có | null | — |
| Trạng thái * | select2 | Có | Hoạt động | **BE luôn ép Active khi tạo** (chọn Khóa vẫn lưu Hoạt động) |
Cột phải: Tiêu đề câu hỏi * (textarea, max 1000, chống trùng) — Mô tả (textarea).
- **10 loại dữ liệu**: Text ngắn, Text dài, Số, Dropdown, Radio 1 lựa chọn, Checkbox nhiều lựa chọn, Ngày, File, Có/Không, Nhóm câu hỏi.
- **Danh sách đáp án** (dropdown/radio/checkbox): tự sinh 2 dòng, nút "Thêm đáp án", nút xóa (dấu trừ đỏ), mỗi đáp án bắt buộc nội dung ("Bắt buộc phải nhập").
- **Danh sách câu hỏi con** (Nhóm câu hỏi): nút "Thêm câu hỏi" → popup "Chọn câu hỏi" (tìm kiếm, checkbox chọn nhiều + "Chọn", hoặc click 1 dòng; cột Mã câu hỏi = **cau_hoi_{id}** ảo); kéo-thả sắp xếp; icon thùng rác bỏ.
- Nút: Tạo = Lưu / Lưu và tiếp tục / Quay lại. Sửa = Lưu / Quay lại (không có "Lưu và tiếp tục"). Xem = chỉ đọc, không footer.
- Toast: Thêm mới thành công / Cập nhật thành công / Xóa thành công / Khóa thành công / Mở khóa thành công.
- Validation: application_id required "Bắt buộc phải chọn ứng dụng"; answers.*.label "Bắt buộc phải nhập"; child_question_ids "Câu hỏi con chưa được lựa chọn"; **chống trùng theo tổ hợp [nội dung]+[loại]+[đáp án chuẩn hóa]+[phạm vi/ứng dụng]** → lỗi title "Câu hỏi đã tồn tại trong phạm vi này (trùng nội dung, loại dữ liệu và danh sách đáp án)". Khi lưu kiểm câu con tồn tại/không bị khóa.

## Popup khóa / xóa (câu chữ thật)
- Khóa: "Xác nhận khóa — Bạn có chắc chắn muốn khóa bản ghi này không?" (Huỷ/Khóa). Mở khóa tương tự.
- Xóa (được): "Xác nhận hủy/xóa — Bạn có chắc chắn muốn hủy/xóa bản ghi này không?" (Huỷ/Xóa).
- Xóa (đang dùng): "Xác nhận hủy/xóa — Không thể xóa câu hỏi này vì đang được sử dụng ở danh mục phiếu thu thập thông tin." (Đóng).
- Điều kiện xóa (code): chặn khi câu hỏi có câu con (là cha) HOẶC đang nằm trong form_questions/form_groups (mẫu phiếu). LƯU Ý: doc cũ ghi "chặn khi là con của câu khác" — code KHÔNG chặn theo hướng đó; chặn theo "có con" + "trong phiếu".

## Sửa
- Chặn sửa khi đang Khóa (BE báo "Dữ liệu đang bị khóa, không thể thay đổi dữ liệu"). Không đổi câu con nếu cha đã dùng trong phiếu ("Câu hỏi cha đã phát sinh ở phiếu thu nhập, không thể thay đổi câu hỏi con").

## Xuất Excel
Theo bộ lọc, file `danh_sach_cau_hoi_khao_sat.xls`, cần quyền Quản lý.

## Ảnh (hdsd_cauhoi_shots/)
01 danh-sách, 02 bộ-lọc, 03 tạo-mới, 04 đáp-án (dropdown), 05 popup-câu-hỏi-con, 06 menu-hành-động, 07 popup-khóa, 08 popup-xóa-không-được, 09 popup-xóa, 10 sửa.

## Thuật ngữ đổi
"Theo nhóm giải pháp" → "Theo ứng dụng"; bỏ cột/filter Nhóm ngành + Nhóm giải pháp → cột/filter "Ứng dụng"; cột phạm vi nhãn "Phạm vi câu hỏi".
