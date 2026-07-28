# Plan — HDSD QLDA cập nhật

## Phase 0 — Rà soát (DONE)
- [x] Trích text 7 docx → doctxt/
- [x] 3 agent đối chiếu code → report_baogia/bom/tongquan.md
- [x] Chốt phạm vi với user

## Phase 1 — Kiểm chứng UI hiện hành (Playwright dev-hrm) — DONE
- [x] Đăng nhập sẵn (session còn hạn "DNS ADMIN update"), resize 1440x900
- [x] Xác minh danh sách Báo giá: cột "Mã BG • BOM" đã gộp; ảnh CŨ trong doc (hdsd_flow_shots/quotations/01_list.png) ĐÃ đúng → không cần thay
- [x] Xác minh BOM: danh sách cột "Mã • Tên BOM" gộp; form Tạo BOM mặc định "BOM LIST thành phần"; KHÔNG có nút Import Excel trên UI → bỏ ý định thêm mục Import
- [x] Kết luận: các sai lệch đều là TEXT; ảnh hiện có đủ dùng → chuyển sang sửa text tại chỗ (không thay ảnh). Ảnh kiểm chứng lưu hdsd_qlda_new/

## Phase 2+3 — Sửa text tại chỗ (python-docx) + verify — DONE
- [x] Backup 7 file gốc → HDSD_update/.bak_orig/ (khôi phục được; bản gốc cũng còn ở HDSD_luongchinh/)
- [x] QLDA_12 Làm báo giá — cấp duyệt=max 2 tiêu chí, ERP tự động, tiền tệ đổi được khi tạo mới, cột "Mã BG•BOM" gộp, điều kiện gửi duyệt, Lưu nháp VAT/CK, trạng thái Đóng/Dừng nguyên nhân, phân quyền cấp, từ chối→Đang tạo, chốt/huỷ chốt tab Báo giá màn Dự án
- [x] QLDA_16 Điều chỉnh — ghi chú KD (chỉ Đã duyệt + Sale), huỷ chốt nhập lý do + appendix
- [x] QLDA_16 Chuyển đổi — appendix (cấp duyệt max, tiền tệ, VAT)
- [x] QLDA_13 BOM — "Đã duyệt" mới lập báo giá, cơ chế gộp (không cộng dồn SL + ràng buộc), điều kiện nút Sửa/Xoá, hàng tạm mã tự sinh, Excel có cột giá, khoá loại Tổng hợp
- [x] QLDA_14 x3 — tên trạng thái đúng, 10 tab HUB, caption "tab Dự án"/"Thêm hạng mục dự án", 2 trường bắt buộc (Nhóm ngành/Nhóm giải pháp), task assignee toàn công ty, biến thể một phòng/liên phòng ban chính xác
- [x] Verify: img/table/Heading1 khớp bản gốc, broken=0 (7/7 OK); nội dung mới grep confirm

## Phase 4 — Wrap up
- [x] Cập nhật STATUS.md + checkpoint
- [ ] (chờ user) đồng bộ 7 file sang HDSD_luongchinh/ nếu muốn; mở file review + in thử
