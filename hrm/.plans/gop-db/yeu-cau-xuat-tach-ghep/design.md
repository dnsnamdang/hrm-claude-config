# Phiếu yêu cầu xuất tách / xuất ghép — tóm tắt (@junfoke)

Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-11-12-yeu-cau-xuat-tach-ghep-design.md`.

## Mục tiêu
Port 2 màn ERP "Phiếu yêu cầu xuất tách" + "Phiếu yêu cầu xuất ghép" sang HRM bằng **1 khung chung** (BE + FE), rồi nối
đủ chuỗi phía sau (ĐNXK → PXK → Phiếu xuất hàng → Phiếu nhập) để trạng thái phiếu tách/ghép được cập nhật khi làm ở HRM.

## Phase
| Phase | Nội dung |
|---|---|
| 1 | 2 màn: danh sách (Tất cả / Kế toán kho / Chờ duyệt / Của tôi), tạo/sửa, chi tiết, Không duyệt, Xóa, Excel, lịch sử, bản in, menu, quyền. Nút duyệt mở ERP tạm |
| 2 | ĐNXK HRM tạo từ phiếu tách/ghép; sửa/hủy/từ chối ĐNXK cập nhật trạng thái phiếu nguồn |
| 3 | PXK: lập / gửi / hủy cập nhật trạng thái |
| 4 | Phiếu xuất hàng: cập nhật trạng thái, tự sinh phiếu nhập tách/ghép, xuất thẳng (ghép); sửa lỗi đọc nhầm bảng |
| 5 | Phiếu nhập: duyệt nhập hoàn thành phiếu tách/ghép |

## Quyết định đã chốt (12/11/2026)
- Port đủ cả chuỗi (user).
- Quyền tạo như ERP (ai đăng nhập cũng tạo); xem theo `accounting.yeu_cau_xuat_tach.view` / `accounting.yeu_cau_xuat_ghep.view`
  (thêm `hrm`); duyệt / không duyệt = `accounting.ke_toan_kho.manage` cùng công ty (user).
- Sửa lỗi ERP trong bản HRM — bảng E1-E10 ở spec mục 2 (user).
- Sửa kèm lỗi Phiếu xuất hàng đọc nhầm bảng (user) — Phase 4.
- Làm bản in theo khuôn HRM (user).
- Mã trạng thái giữ số ERP, mỗi màn khai riêng (tách 8-9, ghép 8-10) — dùng chung DB (mình chốt).
- "Không duyệt" giữ như ERP: phiếu quay về Đang tạo + ghi lý do, người tạo sửa và gửi lại (mình chốt).
- Tồn: 1 nguồn duy nhất là tồn kế toán (ERP tách hiện 1 số, lưu kiểm số khác) — mình chốt.
- Phase 1 nút "Tạo đề nghị xuất kho / Tạo phiếu xuất hàng" mở ERP ở tab mới cho tới Phase 2 (mình chốt).
- Làm trên worktree riêng `.worktrees/yc-xuat-tach-ghep`, nhánh `feat/yc-xuat-tach-ghep` tách từ `origin/gop_db` (`--no-track`).
