-- =============================================================================
-- Phase 7 (21/09/2026) — Khắc phục trên VPS: menu "Danh mục" thiếu "Danh sách phòng họp"
--
-- Nguyên nhân: tài khoản trên VPS KHÔNG có quyền `Khai báo phòng họp`.
--   - Registry menu gate mục này bằng đúng quyền đó
--     (hrm-client/components/subsystem-menu/meeting.js), nên thiếu quyền là mục ẩn im lặng —
--     kèm theo "Tiện nghi phòng họp" và "Mục đích sử dụng phòng" cũng ẩn.
--   - Quyền chỉ được tạo trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`,
--     mà seeder đó `DELETE` TOÀN BỘ permissions guard `api` rồi tạo lại — không chạy được trên
--     production một cách vô hại, nên trên VPS quyền này nhiều khả năng CHƯA BAO GIỜ tồn tại.
--   - ⚠️ Ngày 19/09/2026 quyền bị ĐÁNH SỐ LẠI 1574 -> 1586 (id 1574 nay là
--     "Xem danh mục tính chất hàng hóa"). Nếu VPS từng seed bản CŨ thì role đang giữ id 1574
--     = quyền hàng hoá, KHÔNG phải quyền phòng họp. Git không báo xung đột vụ này.
--
-- Chạy TỪNG BƯỚC, đọc kết quả bước 1 rồi mới quyết định. KHÔNG chạy cả file một lượt.
-- =============================================================================


-- ---------------------------------------------------------------------------
-- BƯỚC 1 — CHẨN ĐOÁN (chỉ đọc, an toàn)
-- ---------------------------------------------------------------------------

-- 1a. Quyền đã tồn tại chưa, id bao nhiêu?
SELECT id, name, `group`, guard_name
FROM permissions
WHERE name IN (
    'Khai báo phòng họp',
    'Xem báo cáo hiệu quả sử dụng phòng họp',
    'Xem tất cả phiếu đặt phòng họp',
    'Duyệt phiếu đặt phòng họp'
);

-- 1b. Dải id 1574-1589 trên VPS đang là quyền gì? (phát hiện vụ đánh số lại)
SELECT id, name, `group` FROM permissions WHERE id BETWEEN 1574 AND 1589 ORDER BY id;

-- 1c. Role nào đang giữ quyền phòng họp (nếu quyền đã tồn tại)?
SELECT rhp.role_id, r.name AS role_name, rhp.company_id, p.id AS permission_id, p.name
FROM role_has_permissions rhp
JOIN permissions p ON p.id = rhp.permission_id
LEFT JOIN roles r ON r.id = rhp.role_id
WHERE p.name = 'Khai báo phòng họp';

-- 1d. Tài khoản đang báo lỗi có quyền không? (thay <EMAIL> bằng email thật)
SELECT e.id, e.email, r.id AS role_id, r.name AS role_name
FROM employees e
JOIN employee_has_roles ehr ON ehr.employee_id = e.id
JOIN roles r ON r.id = ehr.role_id
WHERE e.email = '<EMAIL>';


-- ---------------------------------------------------------------------------
-- BƯỚC 2 — TẠO QUYỀN NẾU BƯỚC 1a KHÔNG TRẢ DÒNG NÀO
--
-- Cố ý KHÔNG khai id cứng: nếu id 1586-1589 trên VPS đã bị chiếm bởi quyền khác thì khai
-- cứng sẽ lỗi khoá chính. Middleware `CheckPermission` tra theo TÊN nên id là bao nhiêu
-- cũng chạy đúng. Ghi lại id thật sinh ra để lần sau đối chiếu với seeder.
-- ---------------------------------------------------------------------------

INSERT INTO permissions (name, guard_name, `group`, display_name, type, created_at, updated_at)
SELECT 'Khai báo phòng họp', 'api', 'Danh mục', 'Khai báo phòng họp', 4, NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM permissions WHERE name = 'Khai báo phòng họp' AND guard_name = 'api'
);

INSERT INTO permissions (name, guard_name, `group`, display_name, type, created_at, updated_at)
SELECT 'Xem tất cả phiếu đặt phòng họp', 'api', 'Quản lý phòng họp', 'Xem tất cả phiếu đặt phòng họp', 4, NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM permissions WHERE name = 'Xem tất cả phiếu đặt phòng họp' AND guard_name = 'api'
);

INSERT INTO permissions (name, guard_name, `group`, display_name, type, created_at, updated_at)
SELECT 'Duyệt phiếu đặt phòng họp', 'api', 'Quản lý phòng họp', 'Duyệt phiếu đặt phòng họp', 4, NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM permissions WHERE name = 'Duyệt phiếu đặt phòng họp' AND guard_name = 'api'
);

INSERT INTO permissions (name, guard_name, `group`, display_name, type, created_at, updated_at)
SELECT 'Xem báo cáo hiệu quả sử dụng phòng họp', 'api', 'Báo cáo phòng họp', 'Xem báo cáo hiệu quả sử dụng phòng họp', 4, NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM permissions WHERE name = 'Xem báo cáo hiệu quả sử dụng phòng họp' AND guard_name = 'api'
);


-- ---------------------------------------------------------------------------
-- BƯỚC 3 — CẤP QUYỀN CHO ROLE
--
-- `role_has_permissions` có khoá chính 3 cột (permission_id, role_id, company_id) và
-- company_id mặc định 1 — PHẢI khai company_id, thiếu là dòng cấp quyền vô tác dụng.
-- Thay <ROLE_ID> bằng role quản trị lấy từ bước 1c/1d. Chạy lại nhiều lần vô hại.
-- ---------------------------------------------------------------------------

INSERT IGNORE INTO role_has_permissions (permission_id, role_id, company_id)
SELECT p.id, <ROLE_ID>, 1
FROM permissions p
WHERE p.guard_name = 'api'
  AND p.name IN (
      'Khai báo phòng họp',
      'Xem tất cả phiếu đặt phòng họp',
      'Duyệt phiếu đặt phòng họp',
      'Xem báo cáo hiệu quả sử dụng phòng họp'
  );


-- ---------------------------------------------------------------------------
-- BƯỚC 4 — XOÁ CACHE QUYỀN (BẮT BUỘC)
--
-- spatie/laravel-permission cache danh sách quyền 24h. Không xoá thì cấp quyền xong
-- vẫn 403 / menu vẫn ẩn, rất dễ tưởng SQL không ăn. Chạy trên VPS, trong thư mục hrm-api:
--
--   php artisan permission:cache-reset
--   php artisan cache:clear
--
-- Rồi ĐĂNG XUẤT / ĐĂNG NHẬP LẠI trên trình duyệt: danh sách quyền của FE
-- (`$store.state.permissions`) chỉ nạp lúc đăng nhập, không tự làm mới.
-- ---------------------------------------------------------------------------


-- ---------------------------------------------------------------------------
-- BƯỚC 5 — KIỂM LẠI
-- ---------------------------------------------------------------------------

-- 5a. Tài khoản đó đã có quyền chưa?
SELECT e.email, p.id, p.name
FROM employees e
JOIN employee_has_roles ehr ON ehr.employee_id = e.id
JOIN role_has_permissions rhp ON rhp.role_id = ehr.role_id
JOIN permissions p ON p.id = rhp.permission_id
WHERE e.email = '<EMAIL>'
  AND p.name = 'Khai báo phòng họp';

-- 5b. Trên giao diện: menu MEETING > Danh mục phải hiện ĐỦ 3 mục
--     "Danh sách phòng họp", "Tiện nghi phòng họp", "Mục đích sử dụng phòng".
--     Thiếu cả 3 = quyền chưa ăn; thiếu đúng 1 mục = bản FE trên VPS cũ hơn Task 85 (20/09/2026),
--     khi đó phải deploy lại hrm-client chứ không phải sửa quyền.
