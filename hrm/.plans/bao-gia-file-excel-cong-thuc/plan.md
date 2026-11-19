# Plan — File Excel bảng tính báo giá (@cuong61n)

Yêu cầu (chị Lệ, 19/10/2026): file Excel dựng lại bảng của màn Báo giá, nhập số → tự tính như màn (bổ sung cho SRS).

## Phase 1 — Dựng file
- [x] Đọc công thức đang chạy ở `hrm-client/pages/assign/quotations/_id/edit.vue` (dòng, cha–con, GG mặt hàng, GG tổng + phân bổ, vận chuyển, tổng hợp, TSLN, cấp duyệt)
- [x] Sinh `Bảng tính báo giá.xlsx` (3 sheet theo kiểu GG + Hướng dẫn + Cấu hình) bằng script
- [x] Đối chiếu số Excel (LibreOffice recalc) với bản port Python của logic JS

### Checkpoint — 2026-10-19
Vừa hoàn thành: `Bảng tính báo giá.xlsx` (sheet Hướng dẫn + 3 sheet theo kiểu GG + Cấu hình); verify.py đối chiếu 181 điểm với logic JS → khớp hết, 0 lỗi công thức
Đang làm dở:
Bước tiếp theo: gửi chị Lệ; nếu cần, nhập cùng bộ số mẫu trên màn thật để đối chiếu thêm
Blocked:
