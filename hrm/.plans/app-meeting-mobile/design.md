# Design (tóm tắt) — App Meeting trên di động

**Sản phẩm:** bộ thiết kế giao diện cho `TPE_APP` (Flutter) — phân hệ Meeting.
**Không phải task code**: đầu ra là file `.pen` + PDF/PNG bàn giao, không sửa `hrm-api` / `hrm-client`.

| | |
|---|---|
| File thiết kế | `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen` |
| Bàn giao | `~/Documents/demo giao dien/pencil_design/exports/` (v11 · 16/09/2026) |
| Quy mô | **50 artboard**, khung bản đồ 2825 × 24617 |
| Nhánh code đối chiếu | `tpe-develop-assign` (cả 2 repo) |

## Mục tiêu

Đưa toàn bộ nghiệp vụ Meeting của bản web lên điện thoại 393px, **bám 100% logic web** — chỉ đổi
cách trình bày, không đổi luật nghiệp vụ. Mọi chỗ buộc phải khác web đều ghi rõ lý do và đánh dấu
cần chốt lại.

## Các quyết định lớn đã chốt

1. **Điều hướng Hub** — màn chi tiết meeting là bảng điều khiển liệt kê 9 khối, bấm từng khối mở màn con.
   Không bê 4 tab ngang của web sang điện thoại. Kéo theo nhu cầu **API lưu từng phần** (`api-luu-tung-phan.md`).
2. **Phạm vi dữ liệu = của tôi** — app chỉ quản lý meeting mình **chủ trì hoặc tham gia**; bỏ bộ lọc
   Công ty / Phòng ban. Tab cấp 1 tách theo **đúng vai trò**, hai tab rời nhau.
3. **Chọn khách hàng / người liên hệ / dự án TKT** có màn riêng + lối **thêm nhanh**, vì trên điện thoại
   không thể mở modal bảng nhiều cột như web.
4. **Thông báo chỉ một kiểu** — dải nằm trong luồng, 3 loại màu (đỏ lỗi · xám khoá · xanh thông tin).
   Không dùng toast đè. Hộp thoại hỏi ý kiến vẫn là popup.
5. **Dấu `*` bắt buộc theo trạng thái từng màn**, khác với thanh *Mức độ hoàn thiện hồ sơ* (đếm theo
   bộ khối cần cho Hoàn thành).
6. **Không viết chú thích logic vào trong khung điện thoại** — phần giải thích nằm ở caption artboard;
   ghi chú kỹ thuật cho dev nằm ở khối `DEV NOTE` bên ngoài khung máy (4 màn: 01 · 04a · 06 · 21).

## Tài liệu liên quan

| File | Nội dung |
|---|---|
| `plan.md` | 5 phase + **danh sách việc chuyển cho dev** + 6 câu cần chốt với khách |
| `chon-khach-hang-va-lien-he.md` | **Spec chi tiết** — 17 mục, ghi từng vòng sửa kèm căn cứ tra từ source web |
| `api-luu-tung-phan.md` | Đề xuất nhóm endpoint lưu từng phần + danh mục Lý do huỷ |
| `docs/superpowers/specs/2026-09-16-app-meeting-mobile-design.md` | Spec kỹ thuật gom đầu mối |
