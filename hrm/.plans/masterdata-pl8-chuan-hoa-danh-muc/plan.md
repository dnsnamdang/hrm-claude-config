# Plan — Chuẩn hoá Master Data 4 danh mục (#11303)

## Phase 1 — Đổi tiền tố mã Lĩnh vực Công ty kinh doanh (LVKDNB. → LVCTKD.)

### BE
- [x] `InternalBusinessScope::CODE_PREFIX` = `'LVCTKD.'`
- [x] Rà `InternalBusinessScopeRequest` + `InternalBusinessScopeService` — đã dùng hằng số, không phải sửa

### FE
- [x] `internal-business-scopes/AddScopeModal.vue`: prefix + CODE_PATTERN + đổi tên rule `lvkdnb_code` → `lvctkd_code`
- [x] `internal-business-scopes/index.vue`: CODE_PATTERN + message lỗi import
- [x] `industry-groups/index.vue`: placeholder + regex + message lỗi ô "Mã lĩnh vực Công ty kinh doanh"

## Phase 2 — Seeder dữ liệu

### BE
- [x] Sinh `Modules/Assign/Database/Seeders/data/masterdata_pl8.php` từ file Excel khách gửi
- [x] Bước 1: đổi mã + tên 7 Lĩnh vực Công ty kinh doanh
- [x] Bước 2: gán lĩnh vực cho 21 Nhóm ngành cũ + tạo mới 13 Nhóm ngành (NN.0023–NN.0035)
- [x] Bước 3: remap 62 Nhóm giải pháp + khoá NGP.0167
- [x] Bước 4: dựng lại `application_scopes` + `application_industries` cho 145 Ứng dụng, đổi tên UD.0141/UD.0142
- [x] Bước 5: khoá Nhóm ngành NN.0012
- [x] Bước 6 (phát sinh, user chốt): đồng bộ `scope_id` 3 bảng nghiệp vụ theo ánh xạ `scope_remap`
- [x] Seeder idempotent + in báo cáo số dòng tác động + gom cảnh báo

## Phase 3 — Kiểm thử
- [x] Dựng env worktree `tpe`: API 8005 (PHP 7.4) + FE 3005 (Node 14.21.3), DB `hrm_prod_6_6`
- [x] Bộ kiểm thử tự động `runtests.py` — **53/53 PASS** (AC1–AC7 + toàn vẹn + audit + không đụng bộ danh mục cũ)
- [x] Kiểm tính tất định: khôi phục dữ liệu gốc → chạy lại → 7 bảng khớp 100% theo (code, name)
- [x] Kiểm idempotent: chạy lần 2 ra 0 dòng thay đổi ở cả 6 bước
- [x] Kiểm qua API thật: BE nhận `LVCTKD.`, từ chối `LVKDNB.` (422, câu lỗi đúng tiền tố mới)
- [x] Kiểm UI 5 màn: 4 màn danh mục + màn Yêu cầu giải pháp; cascading 3 tầng; nhóm ngành khoá không hiện khi tạo mới

### Checkpoint — 2026-09-04
Vừa hoàn thành: toàn bộ 3 phase, 53/53 testcase PASS trên DB `hrm_prod_6_6`.
Đang làm dở: không.
Bước tiếp theo: user review code + quyết định thời điểm chạy seeder trên môi trường thật. CHƯA commit.
Blocked: 1 điểm cần khách xác nhận — sheet lĩnh vực bỏ trống `LVCTKD.0003`; và NN.0012 (đã khoá)
vẫn gắn lĩnh vực "Khác" vì file ghi lĩnh vực không tồn tại cho dòng đó.
