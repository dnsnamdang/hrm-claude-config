# Redmine #11734 — HSNS lọc theo công ty · QĐ sửa đổi phòng ban · HĐLĐ → Phân công nhiệm vụ (@cuong61n)

Nhánh: `develop` (hrm-api + hrm-client)

## Phase 1 — Fix
### BE
- [x] `decision/all-ranks`, `decision/all-working-positions`, `training/master-select/by-current-company` nhận `company_id` tuỳ chọn (không truyền = hành vi cũ)
- [x] DepartmentChangeService: `parent_department_id` cũ/mới cho phép rỗng (`?? null`), tránh 500
- [x] Duyệt HĐLĐ: chép nhiệm vụ HĐ sang `employee_salary_history_missions` (+ xoá nhiệm vụ của bản thu nhập bị thay)
- [x] Migration `2026_10_15_000001` bù nhiệm vụ cho HĐLĐ đã duyệt (chỉ bản thu nhập chưa có nhiệm vụ; dev: 234 bản)
### FE
- [x] HSNS `/human/employee_info`: Cấp bậc/Chức vụ/Chức danh nạp theo công ty đang lọc, đổi công ty bỏ giá trị không thuộc công ty mới
- [x] QĐ sửa đổi phòng ban: phòng ban cha đã ngừng hoạt động coi như không trực thuộc; ô "Trực thuộc" sau sửa đổi bỏ required, cho xoá
- [x] Test local 16/10/2026: chạy migration bù (206 bản), Playwright HSNS lọc 3 công ty + bỏ chức vụ khi đổi công ty, form QĐ phòng ban (HN_QTTT trực thuộc trống, xoá được), store/update BE với trực thuộc trống (rollback), Phân công nhiệm vụ hiện nhiệm vụ từ HĐLĐ
- [x] Kiểm dev 23/10/2026: migration đã chạy, HĐ 721 → bản thu nhập 09/2026 có nhiệm vụ 71; BE `all-ranks` lọc đúng (không truyền 76 · cty1 50 · cty3 18); bundle client có code mới
- [x] Bổ sung 23/10: HSNS chưa chọn công ty (hoặc user không có quyền xem mọi công ty → không thấy ô Công ty) thì Cấp bậc gửi công ty đang chọn ở header, khớp Chức vụ/Chức danh (trước đó ra cấp bậc cả 4 công ty) — chỉ sửa FE, không đụng `getAllRanks` dùng chung
- [x] Deploy bản bổ sung 23/10 lên dev (client `eba1ea198`)
- [x] Migration `2026_10_23_000001_sync_ranks_company_id_from_rank_groups`: đồng bộ `ranks.company_id` theo `rank_groups.company_id` (dev + prod lệch 41 dòng do `RankService::save()` để BaseModel điền công ty người thao tác) — api `a2c10d1f9`, đã chạy trên dev, lệch còn 0
- [ ] (Chưa làm, chờ user) `RankService::save()` gán company_id theo nhóm để không lệch lại; `getAllRanks` lọc theo công ty của nhóm
- [x] Khoá nhóm cấp bậc → `decision/all-ranks` chỉ trả cấp bậc của nhóm đang hoạt động + `include_ids` kèm `is_locked` (api `630455286`); HSNS gửi `include_ids` = cấp bậc đang lọc (client `430740f56`). Đã deploy dev, test khoá nhóm 15 trong transaction: cty4 14 → 11, include 35 trả is_locked=true
