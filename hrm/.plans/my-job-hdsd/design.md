# Design (tóm tắt) — HDSD màn "Công việc của tôi"

## Mục tiêu
Tài liệu hướng dẫn sử dụng (Word) chi tiết click-by-click cho màn "Công việc của tôi" (`/assign/my-job`), phục vụ người dùng cuối.

## Scope
- 6 tab được viết: Tổng quan, Giải pháp, Task, Issue, Meeting, Phiếu công tác.
- Tab **Chờ duyệt: tạm bỏ** theo yêu cầu user (30/06/2026).
- Ảnh minh hoạ **chụp thật** từ dev-hrm.eteksofts.com bằng Playwright, tài khoản huyenntt.qttt@tanphat.com (Nguyễn Thị Thu Huyền) — tài khoản có dữ liệu thật ở mọi tab.

## Cấu trúc tài liệu (theo format HDSD chuẩn)
Bìa "(Màn hình: Công việc của tôi)" → MỤC LỤC → DANH MỤC HÌNH ẢNH → TỔNG QUAN (thuật ngữ, cập nhật tài liệu, giới thiệu, đường dẫn, quyền & phạm vi) → PHẦN 1 Truy cập & bố cục → PHẦN 2 Tổng quan → PHẦN 3 Giải pháp → PHẦN 4 Task → PHẦN 5 Issue → PHẦN 6 Meeting → PHẦN 7 Phiếu công tác.

## Đặc điểm màn (ghi nhận từ code + UI thật)
- Màn layout=false (toàn màn hình, ẩn sidebar), thanh 7 tab dùng `V2BaseTabNavigation`, lưu tab theo query `?tab=`.
- **Tab Tổng quan**: 4 thẻ cảnh báo (Task/Issue/Meeting/Giải pháp sắp tới hạn) — click mở modal danh sách (có lọc thường + nâng cao Trạng thái/Độ ưu tiên); 2 bảng Task/Meeting hôm nay; 4 biểu đồ (đường 14 ngày, tròn trạng thái task, cột meeting theo ngày, cột issue theo ưu tiên) — click biểu đồ mở modal chi tiết.
- **Các tab danh sách** (Giải pháp/Task/Issue/Meeting/Phiếu công tác) cùng pattern: ô tìm nhanh + "Tìm kiếm nâng cao" + "Tìm kiếm"/"Làm mới"; bảng dữ liệu; thanh công cụ "Tạo mới"/"Xuất Excel"/"Cấu hình cột" (modal "Tuỳ chỉnh cột" tick + kéo sắp thứ tự); nút thao tác từng dòng hiển thị theo quyền + trạng thái.
- **Task** thêm thanh lọc nhanh: pill "Quá hạn: N" + 4 nút phạm vi "Tôi làm / Tôi giao / Tôi theo dõi / Tôi duyệt kết quả" (bật → nút xanh + nhãn "Đang lọc: …", có nút × bỏ lọc).
- **Phiếu công tác** dùng menu hành động "…" (3 chấm) thay cho dãy icon — chứa Xem/Sửa/Duyệt/Từ chối/Nhập-Duyệt kết quả/Lập hồ sơ-đề nghị TT/Gia hạn/Kết thúc sớm/Thêm NV-phiếu GV/Xóa tuỳ quyền.
- Mọi dữ liệu giới hạn theo người dùng đăng nhập; nút thao tác phụ thuộc quyền.

## Kỹ thuật dựng file (tái sử dụng được)
- Generator `scratchpad/gen_myjob.py` (python-docx 1.2.0 + PIL):
  1. Mở `HDSD_DanhMuc/HDSD_KhachHang.docx` làm khung (giữ bìa text + MỤC LỤC TOC field + DANH MỤC HÌNH TOF + styles + `updateFields=true`).
  2. Sửa bìa "(Danh mục Khách hàng)" → "(Màn hình: Công việc của tôi)".
  3. Clone proto Caption (run0 "Hình " + SEQ field + run2 ": text") để đánh số hình tự động.
  4. Strip body từ heading "TỔNG QUAN PHẦN MỀM" → hết (giữ sectPr), rebuild bằng helper H1/H2/P/BL/IMG.
  5. Bảng dùng style `Light Grid Accent 1`.
  6. Purge media mồ côi (quét r:embed trong document/header/footer → map qua .rels → bỏ media + Relationship không dùng): 27→14 ảnh, 6.2MB→2.1MB.
- Bìa file mẫu là **text** (không nhúng ảnh logo) nên purge media an toàn.

## Output
- `HDSD_luongchinh/HDSD_CongViecCuaToi.docx` (2.1MB; 10 Heading 1; 14 hình; 2 bảng).
- Ảnh nguồn: `hdsd_myjob_shots/01..15` (13 = Chờ duyệt, chưa dùng).
