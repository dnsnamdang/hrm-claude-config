# Plan — #11908 Luồng nhập hàng loại "Nhập khác" (99): cột Ghi chú từng dòng hàng

**Người phụ trách:** @junfoke — 2026-10-28
Issue: http://quanly.dnsmedia.vn/issues/11908

## Ngày 28/10/2026 (@junfoke) — khảo sát

- [x] 28/10/2026 — Đọc issue (không có ảnh): YCNH loại Nhập khác có ô Ghi chú từng dòng — sửa được, không bắt buộc, nhận chữ / số / ký tự đặc biệt, placeholder "Mã số SX,.."; cùng phiếu, cùng mặt hàng mà trùng ghi chú → lỗi tại ô + toast "Nội dung ghi chú trùng nhau". ĐNNK, Phiếu dự kiến, PNK, PNH chỉ xem. Áp cho tạo / sửa / xem.
- [x] 28/10/2026 — Kiểm code `develop` (worktree gop-db): chưa có cột ghi chú ở `product_import_request_details`, `warehouse_import_request_details`, `warehouse_import_lot_details` (+ bảng `tmp_` của phiếu dự kiến), `product_import_details` → cần migration. Màn HRM đã port đủ 4 phiếu.
- [x] Chờ user chốt các điểm đã hỏi → làm BE (migration + validate trùng) + FE 5 phiếu (29/10).

## Checkpoint — 2026-10-28

- **Vừa hoàn thành:** khảo sát issue + code.
- **Bước tiếp theo:** user chốt → triển khai.
- **Blocked:** chờ user chốt.

## Ngày 29/10/2026 (@junfoke)
- [x] 29/10/2026 — User chốt: sửa cả ERP lẫn HRM (ERP vẫn đang dùng); ô trống không kiểm trùng. Đổi cách kiểm trùng: form YCNH không cho thêm cùng mặt hàng 2 lần nên so ghi chú trên CẢ phiếu (không phân biệt hoa thường, bỏ khoảng trắng đầu cuối, ô trống bỏ qua) → báo đỏ dưới 2 ô + toast "Nội dung ghi chú trùng nhau", không gửi lên server.
- [x] 29/10/2026 — Làm xong BE + FE: YCNH loại 99 có ô Ghi chú (gợi ý "Mã số SX,..", tối đa 255 ký tự); ĐNNK, Phiếu nhập kho (cả phiếu dự kiến, ghi chú gộp ô qua các vị trí cùng dòng hàng), Phiếu nhập hàng hiện ghi chú chỉ xem.
- [x] 29/10/2026 — Test đủ màn tạo/sửa ở ERP và HRM (sửa DB local để có phiếu loại 99 cho tài khoản test; đã xem ảnh).
- [x] 29/10/2026 — ERP: `02ae9a640f` nhánh `task_11908`, merge `develop_02` (`1f2f91cb04`) đã push. HRM: api `52a17fa86`, client `b489fb882` — đã lên origin/develop.
- [x] 29/10/2026 — Hỗ trợ: phiếu PYCNH-15588 (loại 99) "biến mất" sau khi bấm Không duyệt trên cổng dev (ERP `develop_02`) → phiếu trả về Đang tạo (status 3), người lập đang tìm ở màn "Phiếu YC nhập hàng chờ duyệt" (chỉ hiện status 2); hướng dẫn mở lại ở Kho → Phiếu Yêu cầu nhập hàng.
- [x] Merge `task_11908` vào `gop_db` của ERP khi cần. (30/10)

## Ngày 30/10/2026 (@junfoke)
- [x] 30/10/2026 — Fix phản hồi #11908: màn **tạo phiếu xuất lại** (từ PNK, `warehouse_reexports/create`) và màn xem phiếu xuất lại còn thiếu cột Ghi chú → thêm cột Ghi chú chỉ xem sau cột "Tổng SL", chỉ hiện với loại 99, gộp ô theo dòng hàng khi nhiều vị trí. Màn nhập lại dùng chung form PNK nên đã có từ 29/10. ERP `795c92d22a` (`task_11908` → merge `develop_02` `bf4eabf6ef`), HRM client `50b3af254` (`re-export.vue`) — đã lên origin/develop.
- [x] 30/10/2026 — Merge `task_11908` vào `gop_db` ERP (`0bf8e69dc5`) cho QA test; xoá worktree `hrm-client/.worktrees/task-11908` sau khi push.
- [x] 30/10/2026 — Xử lý môi trường `gop_db` thiếu cột `product_import_request_details.note` (migration chỉ nằm ở hrm-api, ERP `gop_db` không có file → không ai chạy). ERP và HRM dùng chung DB **và chung bảng `migrations`** → đặt **cùng 1 file migration, giữ nguyên tên, ở cả 2 repo**, kiểm `hasColumn` trước khi thêm. ERP `188cfe3697` merge vào `gop_db` + `develop_02`.
