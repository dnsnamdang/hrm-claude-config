# Design — Lịch sử xem phiếu đề xuất cung ứng

> Phụ trách: @khoipv · Ngày: 2026-09-18
> Spec chi tiết: `docs/superpowers/specs/2026-09-18-lich-su-xem-de-xuat-cung-ung-design.md`

## Mục tiêu

Popup "Lịch sử xem phiếu" mở từ cột Thao tác màn `supply/supply_proposals/inbox`:
biết được trong nhóm có quyền `Xử lý cung ứng hàng hóa`, ai đã ngó tới phiếu (kèm thời
điểm xem lần đầu) và ai đã lập phiếu xử lý (mã PXL + link sang chi tiết).

## Scope

**Trong scope**
- Bảng log mới `supply_proposal_views` (1 dòng/người/phiếu, chỉ lần xem đầu tiên).
- 2 API: `POST .../{id}/mark-viewed` (ghi log) và `GET .../{id}/view-history` (đọc danh sách).
- Nút mở popup + modal `ViewHistoryModal.vue` ở màn inbox.

**Ngoài scope**
- Không đụng màn danh sách đề xuất, màn chi tiết phiếu, module PXL.
- Không backfill lịch sử cũ (trước đây không lưu gì).
- Không siết phân quyền route inbox (lỗ hổng đã biết, việc riêng).

## Quyết định lớn

1. **Chỉ ghi log khi thao tác từ inbox** — bấm nút Xem (`source = 1`) hoặc bấm nút Tạo
   phiếu xử lý (`source = 2`). Mở phiếu từ nơi khác không tính. Vì vậy ghi log bằng API
   riêng do FE gọi, KHÔNG hook vào `GET /supply-proposals/{id}` (endpoint đó dùng chung
   cho mọi lối vào chi tiết).
2. **Chỉ lưu lần xem đầu** — `unique(supply_proposal_id, employee_id)` + `insertOrIgnore`.
   Không đếm số lần, không lưu lần cuối → bảng không phình.
3. **Danh sách NV toàn hệ thống** — mọi người có quyền 514 (qua vai trò + gán trực tiếp),
   không lọc công ty/phòng ban, khớp với thực tế inbox không phân phạm vi.
4. **Lịch sử bất biến** — danh sách còn cộng thêm người đã xem và người đã lập PXL, kể cả
   khi họ đã bị gỡ quyền hoặc nghỉ việc.
5. **Không sửa helper dùng chung** — query NV có quyền đặt riêng trong
   `SupplyProposalService::handlerEmployeeIds()`, không động vào `PermissionHelper.php`.

## Rủi ro đã biết

- Phiếu tạo trước khi deploy sẽ hiện "Chưa xem" cho tất cả — không có cách khôi phục.
- `mark-viewed` lỗi mạng thì lần xem đó mất; FE cố tình nuốt lỗi để không chặn điều hướng.
