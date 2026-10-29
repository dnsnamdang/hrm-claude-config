# HDSD — Luồng nhập mua hàng ngoài (3 phiếu đầu)

> Skill: `hdsd-documenter` (bản GỌN, khuôn `HDSD_MAU_GON.docx`)
> Nguồn chụp: local ERP `http://127.0.0.1:8000` (APP_ENV=local, DB hrm_erp_gop)

## Phạm vi — 3 phiếu đầu luồng mua ngoài
1. **Yêu cầu đặt hàng (mua ngoài) trong nước** — `InlandOrderRequest` — màn `admin/orders/inland_order_requests/forBuyer`
2. **Hợp đồng mua hàng ngoài** — `InlandBuyContract` — màn `admin/orders/inland_buy_contracts`
3. **Phiếu báo hàng về** — `ProductArrivedNotify` — màn `admin/orders/product_arrived_notifies`

## Lưu ý khác biệt với khuôn skill
- Skill `hdsd_gon.py` auto-build chỉ hợp **màn danh mục** (Thêm/Sửa/Xóa/Khóa/Mở khóa/Lịch sử/Chi tiết/Xuất/Import/Cột). 3 phiếu này là **chứng từ giao dịch** → chức năng khác (Tạo mới, Gửi duyệt, Duyệt/TP/BGD duyệt, Lập hợp đồng / Báo hàng về / Tạo YC nhập, In, Sửa, Hủy, Xem chi tiết) → phải **viết generator tay** bằng `QgWriter` trên khuôn gọn.
- Chụp ở ERP (`127.0.0.1:8000`) — KHÁC môi trường HRM (`127.0.0.1:3000`) mà skill mặc định. Cần phiên đăng nhập ERP cho Playwright.

## Quyết định đã chốt
- Output: **3 file riêng** (mỗi phiếu 1 file `HDSD_<tên phiếu>.docx`) — user chốt 2026-10-13.
- Phạm vi: **đầy đủ chức năng mỗi màn** (mặc định) — liệt kê theo code từng màn.
- **KHÔNG cần ảnh** — user chốt 2026-10-13. → HDSD chỉ chữ (bước thao tác), bỏ mọi img/cap. ⇒ GỠ điểm chặn đăng nhập ERP + Playwright (không còn cần).

## Tasks
- [x] ~~Tài khoản đăng nhập local ERP~~ — HẾT HIỆU LỰC vì không cần ảnh.
- [x] Đọc FE+BE từng màn → spec HDSD ra scratch (`hdsd_specs/phieu{1,2,3}_*.md`). (3 agent song song, xong)
- [x] Dựng Word bằng QgWriter trên khuôn gọn (role step/h1/h2/p/tbl, BỎ img/cap), 1 generator chung `gen_hdsd.py` → 3 file.
- [x] Mục lục (updateFields macOS osascript Word), strip font (no-op, file ~80KB không nhúng font).
- [x] Kiểm cấu trúc: TỔNG QUAN 4 mục, mỗi chức năng 1 PHẦN sang trang, 0 ảnh thân bài (3 ảnh còn lại = logo bìa khuôn), mục lục khớp PHẦN. (bỏ render PDF: máy không có soffice/PyMuPDF)
- [x] Giao 3 file cho user.

## Output (3 file riêng, không ảnh)
- `HDSD_Yeu_cau_dat_hang_mua_ngoai.docx` — 13 PHẦN
- `HDSD_Hop_dong_mua_hang_ngoai.docx` — 12 PHẦN
- `HDSD_Phieu_bao_hang_ve.docx` — 6 PHẦN

## Checkpoint — 2026-10-13
Vừa hoàn thành: dựng xong 3 HDSD gọn chỉ-chữ (không ảnh), cập nhật mục lục, kiểm cấu trúc đạt.
Đang làm dở: (không)
Bước tiếp theo: nếu user duyệt → đẩy Drive (chưa làm, chờ yêu cầu).
Blocked: máy local thiếu soffice + PyMuPDF nên không render PDF soi được (không ảnh hưởng file .docx).
