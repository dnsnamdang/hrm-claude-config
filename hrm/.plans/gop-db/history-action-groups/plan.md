# Plan — Chuẩn hoá bộ lọc "Loại hoạt động" của Lịch sử

Nhánh: `gop_db` · @dnsnamdang

## Phase 1 — BE (`worktrees/gop_db-api`)

- [x] `SystemLogService`: thêm `GROUP_CREATE/UPDATE/STATUS`, `ACTION_GROUP_LABELS` (3 nhãn), `ACTION_GROUP_MAP` (14 action)
- [x] `SystemLogService::groupOfAction()` — action chưa khai mặc định vào `status`
- [x] `SystemLogService::finalize()` — trả thêm `action_group` cho MỌI dòng log (áp cho cả 10 loại)
- [x] `SystemLogService::getFilterOptions()` — trả 3 nhóm cố định cho mọi `$type`
- [x] Giữ nguyên `performers`: chỉ trả cho `customer`, loại khác rỗng (tránh liệt kê 783 nhân viên)

## Phase 2 — FE (`worktrees/gop_db-client`)

- [x] `components/assign/SystemInfoSection.vue` (khối Lịch sử màn chi tiết): `actionOptions` = 3 nhóm cố định, bỏ suy từ log; lọc theo `action_group` (fallback `action`)
- [x] `components/assign/customer/CustomerHistoryModal.vue` (popup màn danh sách): sửa y hệt để 2 nơi khớp nhau (skill §5.1)

## Phase 3 — Áp nguyên tắc "đã khoá thì không cho sửa" cho màn Khách hàng

Phát hiện khi user hỏi lại: nguyên tắc mới ghi vào CLAUDE.md nhưng màn KH **chưa hề áp dụng**.
Đã kiểm chứng bằng API thật: `POST /assign/customers/43712` (KH `status = 0`) trả **HTTP 200** và
**ghi đè dữ liệu** — `save()` còn xoá luôn các field không gửi (hamlet, gara_name, apartment_number,
date_of_birth, is_supplier, is_manufacturer, short_name) và 2 quan hệ (nhóm KH, hãng xe).
Đã khôi phục nguyên trạng từ snapshot `customer_versions.id = 59083`.

### BE
- [x] `TpCustomer`: hằng `STATUS_ACTIVE/STATUS_LOCKED` + `isLocked()` / `isCanEdit()` — nguồn chân lý duy nhất
- [x] Middleware mới `CheckCustomerNotLocked` → trả **423** kèm message tiếng Việt
- [x] Đăng ký alias `customerNotLocked` ở `app/Http/Kernel.php`
- [x] Gắn cho **13 route ghi** của khách hàng (thông tin chung, người liên hệ, tài liệu/ảnh, xoá file, thiết bị cũ/ngoài, serial)
- [x] KHÔNG gắn cho: `unlock` (lối thoát duy nhất), `lock`, route tạo mới, mọi route chỉ đọc

Dùng middleware thay vì `if` trong từng controller vì 1 KH có ~18 endpoint ghi — rải điều kiện chắc chắn sót.

### FE
- [x] `pages/assign/customers/index.vue`: nút **Sửa** ở cột Hành động thêm điều kiện `&& isActive`
- [x] `components/assign-components/customer/CustomerForm.vue`: vào thẳng URL `/edit` của KH đã khoá → toast + `$router.replace` về màn Chi tiết (loại trừ `modalMode` = xem nhanh trong popup)
- [x] **Footer màn CHI TIẾT**: `:menu="{ edit: perm.edit && isCustomerActive }"` — user phát hiện lúc đầu
      tôi chỉ sửa màn danh sách, để lệch màn chi tiết (vẫn còn nút Sửa ở KH đã khoá)

**Đối xứng sau khi sửa** (cùng 1 bản ghi, 2 màn phải khớp):

| Bản ghi | Dòng ở màn danh sách | Footer màn chi tiết |
| --- | --- | --- |
| KH đã khoá (43712) | Mở khóa · Quản lý · Lịch sử | Quản lý · Mở khóa · Quay lại |
| KH hoạt động (8) | **Sửa** · Khóa · Quản lý · Lịch sử | **Sửa** · Quản lý · Khóa · Quay lại |

### Test
| Ca | Kết quả |
| --- | --- |
| Sửa thông tin chung KH đang khoá | **423** + DB không đổi |
| Thêm người liên hệ / cập nhật tài liệu KH đang khoá | **423** |
| GET chi tiết KH đang khoá | 200 (chỉ đọc vẫn xem được) |
| Mở khoá KH đang khoá | 200, `status` → 1 (không bị middleware chặn) |
| Sửa sau khi đã mở khoá | 200 |
| Vào URL `/43712/edit` trên trình duyệt | Đá về `/assign/customers/43712` + toast đúng |

⚠️ **Còn hở, chưa xử lý**: 3 route serial dùng param `{serialId}` (`updateSerial`, `changeSerial`,
`deleteSerial`) không mang `customer_id` nên middleware không suy ra được KH → **chưa được bảo vệ**.
Muốn chặn thì phải tra ngược serial → customer trong middleware hoặc trong controller. Chờ user chốt.

## Phase 4 — Tài sản chung

- [x] `.claude/skills/entity-history/SKILL.md`: thêm §0a + cập nhật câu hỏi §0.3 + checklist
- [x] `CLAUDE.md`: nguyên tắc "bản ghi đã khoá thì không cho sửa/xoá — chặn ở BE bằng 423, FE chỉ ẩn nút"
- [x] `CLAUDE.md` + `.claude/skills/list-page/SKILL.md` §7.2: nguyên tắc **hành động màn chi tiết phải
      khớp màn danh sách của đúng bản ghi đó — giống cả điều kiện hiện/ẩn, không chỉ giống danh sách nút**.
      Skill trước đây mới nói "footer có đủ hành động như dòng danh sách" nên không chặn được lỗi lệch
      điều kiện; đã bổ sung ví dụ sai điển hình + cách tự kiểm bằng 2 bản ghi khác trạng thái.

## Đã test (2026-08-15, FE :3002 / BE :8003, DB `local_hrm_erp`)

| Hạng mục | Kết quả |
| --- | --- |
| `filter-options` cho customer | 3 nhóm đúng thứ tự + 783 performers (giữ nguyên) |
| `filter-options` cho task / issue / handover / meeting / bom-list | **3 nhóm giống hệt nhau**, `performers` rỗng ✓ |
| Ánh xạ `groupOfAction` | Verify đủ **14 action** đang tồn tại + action lạ + `null` → đúng nhóm |
| Log KH 43712 | `lock` → `action_group = status`, `action_label` vẫn "Khóa khách hàng" |
| UI màn chi tiết KH 43712 | Dropdown đúng 3 option; timeline vẫn hiện "Khóa khách hàng" |
| Lọc thật | "Thay đổi trạng thái" → 1 mục; "Tạo mới" → 0 mục ✓ |
| Lint/compile | `php -l` sạch; 2 file `.vue` compile + parse OK |

### Checkpoint — 2026-08-15
Vừa hoàn thành: chuẩn hoá 3 nhóm hoạt động cho toàn bộ 10 màn có Lịch sử + ghi vào skill/CLAUDE.md.
Đang làm dở: —
Bước tiếp theo: user review. **Chưa port sang nhánh `tpe-develop-assign`** — nhánh đó cũng có
`SystemInfoSection.vue` + `SystemLogService`, nếu muốn đồng nhất cả 2 nhánh thì cần làm riêng
(xem mục dưới).
Blocked:

### Chưa làm — cần user quyết
Nhánh `tpe-develop-assign` (`hrm-client` + `hrm-api`) cũng có khối Lịch sử dùng chung. Thay đổi này
mới chỉ áp cho nhánh `gop_db`. Port sang nhánh kia hay để lần merge sau tự mang theo — chờ user chốt.
