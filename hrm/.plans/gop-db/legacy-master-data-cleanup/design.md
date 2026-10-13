# Dọn bộ danh mục cũ trùng mã — Nhóm ngành / Nhóm giải pháp

Phụ trách: @khoipv · Nhánh: `develop` (tách từ `gop_db`) · Tạo: 2026-10-09

## Hiện trạng (kiểm qua API, prod `hrm.eteksofts.com` + dev `dev-hrm.eteksofts.com` giống nhau)
- Ngày **24/04/2026 10:20** có 1 bộ danh mục cũ bị đổ thẳng vào DB (không qua form → không validate trùng,
  không có `created_by`/`updated_by`): **19 nhóm ngành** (`hrm_scopes`, id 36–54, mã `NN.0001`–`NN.0021`)
  + **117 nhóm giải pháp** (`industries`, id 402–518, mã `NGP.0001`–`NGP.0118`).
- Toàn bộ mã trùng với bộ chuẩn nhập 01/07; 4 tên nhóm ngành + 38 tên nhóm giải pháp trùng.
- Bộ cũ khép kín: 117 NGP cũ chỉ gắn 19 NN cũ, không NGP mới nào gắn NN cũ; `applications_count = 0`.
- KHÔNG do task Redmine #11303 (task bắt đầu 04/09, seeder `MasterDataPl8Seeder` chỉ né bộ cũ, không tạo/sửa).

## Quyết định
- Dọn bằng **seeder** (không chạy SQL tay): `Modules/Assign/Database/Seeders/CleanupLegacyDuplicateCatalogsSeeder.php`
- Nhận diện bộ cũ theo **tiêu chí**, không theo id cứng: người tạo/cập nhật không tra ra nhân viên
  + ngày tạo 2026-04-24 + **có bản ghi khác cùng MÃ** đã có người tạo (2026-10-09 đã thử đổi sang trùng TÊN, user cho revert về MÃ).
- Đang được dữ liệu nghiệp vụ tham chiếu → **khoá** (status=2); không ai dùng → **xoá** (kèm pivot `industry_scopes`).
- Backup JSON vào `storage/app/backups/` trước khi xoá; hỏi xác nhận, mặc định KHÔNG xoá.
