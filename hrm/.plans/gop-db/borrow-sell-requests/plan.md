# Plan — Màn "Yêu cầu xuất bán hàng mượn" HRM không hiện dữ liệu + Phân quyền không có chức năng

> Nhánh: `gop_db` (hrm-api + hrm-client) · Tạo: 2026-10-10
> Màn HRM: `finance/borrow-sell-requests` · Màn ERP tương đương: `admin/warehouse/borrow_sell_requests?type=all`
> Phân loại brainstorming: **BOUNDED** · Hướng chốt với user: **B** (giữ quyền api mới, triển khai + gán lại — KHÔNG đổi tên quyền trong code)

## Bối cảnh / Triệu chứng

- Vào `finance/borrow-sell-requests` trên prod `hrm-crm.eteksofts.com` → **không thấy dữ liệu nào**.
- Vào màn Phân quyền (Chức vụ) → **không có** nhóm chức năng này.
- Cùng dữ liệu, màn ERP `borrow_sell_requests?type=all` vẫn hiển thị bình thường.

## Nguyên nhân gốc (đã xác minh trên DB dev `erp_hrm_check`)

**Không phải bug code.** `Modules/Finance/Entities/BorrowSellRequest/BorrowSellRequest.php::searchByFilter`
đã port đúng logic ERP. Vấn đề là **quyền chưa được tạo/gán**:

1. HRM kiểm tra quyền theo **TÊN** (`ChecksEmployeePermission::currentEmployeeHasPermission`
   match tên qua CẢ 2 guard, bỏ qua guard/model_type):
   - `Xem phiếu hàng mượn theo tổng công ty` = api **1565**
   - `Xem phiếu hàng mượn theo công ty` = api **1566**
   - `Xem phiếu hàng mượn theo phòng ban` = api **1567**
2. Trên dev: 1565-1567 đang gán cho **0 vai trò** → mọi user rơi xuống nhánh fallback
   `where('created_by', auth()->id())` → danh sách rỗng.
3. Các vai trò test đang giữ **quyền ERP** (web) tên KHÁC — `Xem tất cả phiếu yêu cầu xuất bán
   hàng mượn của {tổng công ty|công ty|phòng ban}` (web 100448-100450) → thấy ERP nhưng trống HRM:
   - `Quản trị hệ thống` (100019)
   - `Giám đốc công ty` (100034)
   - `Trợ lý giám đốc` (100035)
   - `Phó Giám đốc Dự án trọng điểm` (100118)
4. Màn Phân quyền chỉ liệt kê quyền **guard=api** gom theo `type`
   (`PermissionService::getLists()` = `where('guard_name','api')`). Prod "không có chức năng này"
   ⇒ **`PermissionsTableSeeder` CHƯA chạy trên prod** nên nhóm "Phiếu hàng mượn" (api, type 8) chưa tồn tại.
5. HRM `searchByFilter` KHÔNG có nhánh bypass super-admin — đúng theo port ERP.

### Vì sao `ChecksEmployeePermission` match theo tên:
Vai trò giữ quyền web `Xem phiếu hàng mượn theo ...` (web 100890-100892, nhóm ERP "Quản lý hàng
mượn") sẽ ĐƯỢC HRM nhận ra (vì cùng tên api 1565-1567). Do đó chỉ cần **gán đúng 1 trong 2 bộ
cùng tên** là màn hiện data. Chuẩn gop_db (erp-to-hrm-screen) dùng **bộ api 1565-1567**.

## Entry seeder liên quan (đã kiểm — ĐÚNG, không sửa)

`Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`:
- 1565 / 1566 / 1567 — Xem theo tổng công ty / công ty / phòng ban (`group='Phiếu hàng mượn'`, `type=8`)
- 1572 / 1573 — Trưởng phòng duyệt / Ban giám đốc duyệt xuất hàng vượt hạn mức công nợ (cùng group/type)

⚠️ `run()` xóa **toàn bộ** `guard_name='api'` rồi tạo lại tất cả (không chèn lẻ). An toàn vì:
- Chỉ đụng guard **api**, web (ERP) không động tới.
- Xóa bằng `DB::table()->delete()` (raw, không cascade qua model event) + tạo lại **đúng id cũ**
  → gán `role_has_permissions` / `employee_has_permissions` của quyền api vẫn trỏ đúng, không mất.
- Rủi ro chỉ khi seeder prod đang là bản CŨ hơn repo gop_db → phải chạy seeder NHƯ MỘT PHẦN của
  deploy code gop_db lên prod, không chạy lẻ trên prod cũ.

---

## Công việc (Hướng B — KHÔNG đổi code)

### Task 1 — [BÀN GIAO/VẬN HÀNH] Triển khai code gop_db + chạy seeder trên prod
- [ ] Deploy code nhánh `gop_db` (cả hrm-api + hrm-client) lên prod `hrm-crm.eteksofts.com`.
- [ ] Chạy seeder (một phần của bước deploy):
      `php artisan db:seed --class="Modules\Timesheet\Database\Seeders\PermissionsTableSeeder"`
- [ ] Kiểm: màn Phân quyền → Tài chính → xuất hiện nhóm **"Phiếu hàng mượn"** (1565-1567, 1572-1573).
- Người thực hiện: **user/devops** (Claude KHÔNG truy cập prod — chỉ có DB dev `erp_hrm_check`).

### Task 2 — [ADMIN] Gán quyền cho các vai trò cần xem
- [ ] Admin tự gán 1565-1567 (và 1572/1573 nếu muốn cho duyệt vượt hạn mức) cho các vai trò cần
      thấy màn — tối thiểu: Quản trị hệ thống, Giám đốc công ty, Trợ lý giám đốc, Phó GĐ Dự án trọng điểm.
- Người thực hiện: **admin**. Claude KHÔNG tự gán (CLAUDE.md: "Không tự thêm phân quyền theo cấp — phải hỏi").

### Task 3 — Xác minh sau khi gán
- [ ] Login bằng 1 tài khoản thuộc vai trò vừa gán → vào `finance/borrow-sell-requests` →
      dữ liệu hiển thị theo đúng phạm vi quyền (tổng công ty / công ty / phòng ban).

## Kết luận
Không có thay đổi code. Sự cố thuần **triển khai + phân quyền** trên prod. Code HRM (searchByFilter,
ChecksEmployeePermission, seeder) đã đúng.
