# Design — Đồng bộ quyền bằng seeder an toàn (HRM + ERP)

> Phụ trách: @namdangit · Nhánh: `gop_db` (`hrm-api` + `TanPhatDev`) · Bắt đầu: 2026-10-14
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-14-permission-seeder-sync-design.md`
> Plan: `.plans/gop-db/permission-seeder-sync/plan.md`

## Mục tiêu

Seeder quyền của HRM và ERP chạy được trên DB gộp **bất kỳ lúc nào, theo thứ tự bất kỳ**, mà không làm mất
quyền đã gán cho vai trò và không đụng quyền của bên kia.

## Vấn đề hiện tại

- Seeder HRM xoá mọi quyền `api` rồi tạo lại với id cố định → bỏ/đổi tên quyền là mất gán quyền (776 dòng pivot mồ côi), dev phải tự giành id.
- Seeder ERP (từ 05/10) đã chỉ xoá guard `web` + id +100000, nhưng vẫn xoá đi tạo lại theo id cố định → cùng bệnh như seeder HRM.
- Bảng `permissions` thiếu unique `(name, guard_name)`; seeder HRM đang khai trùng tên (1115/1117, 1116/1118).

## Quyết định lớn

1. **Định danh quyền = `(guard_name, name)`**. id do DB sinh, có rồi giữ nguyên. Seeder bỏ key `'id'`.
2. **Upsert, không xoá đi tạo lại.** Mỗi seeder chỉ đụng guard của mình (HRM `api`, ERP `web`).
3. **Xoá / đổi tên phải khai rõ** bằng `REMOVED` / `RENAMED` trong seeder. Quyền thừa trong DB chỉ cảnh báo.
4. Engine chung `PermissionSync` (bản giống hệt ở 2 repo) + lệnh `permission:sync --dry-run` xem trước thay đổi.
5. Thứ tự hiển thị lấy theo **vị trí dòng trong seeder** (cột mới `seed_order`), không theo id nữa.
6. Thêm unique `(name, guard_name)` sau khi dọn trùng; dọn pivot mồ côi bằng lệnh `permission:cleanup` (có xuất CSV backup).
7. Vẫn **1 file seeder** mỗi repo như CLAUDE.md quy định; chuyển 955 + ~1.004 dòng bằng script.

## Ngoài phạm vi

- Gộp 2 hệ phân quyền ERP/HRM làm một (113 tên trùng, 37 dòng gán chéo guard) — chỉ báo cáo, xử lý ở feature riêng.
- Nhánh ERP không chạy DB gộp.

## Quyết định đã chốt

- 14/10/2026: user đồng ý hướng upsert theo tên, làm cả seeder ERP trong cùng feature.

- 14/10/2026 ("làm đi"): dọn gán quyền mồ côi có CSV backup; chấp nhận thứ tự hiển thị theo dòng seeder; cập nhật CLAUDE.md + skill.
- Lần sync đầu dùng bảng tra id cũ (`permission_legacy_ids.php`) để tương đương seeder cũ chạy thêm 1 lần — không mất gán quyền.
- 9 quyền ERP có trong DB mà seeder không khai: CHỈ cảnh báo, không đưa vào `REMOVED` ("Xem tất cả PI" vẫn dùng trong code ERP).

## Câu hỏi còn mở

- Lịch chạy `permission:cleanup` trên prod (`hrm_erp_gop`): backup 3 bảng, dry-run, user duyệt trước.
- 9 quyền ERP cảnh báo: chủ màn quyết giữ hay đưa vào `REMOVED`.
