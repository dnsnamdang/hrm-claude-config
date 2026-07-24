# Plan — Bỏ luồng tự sinh HĐ đào tạo từ QĐ cử đi đào tạo

@manhcuong · Spec: `docs/superpowers/specs/2026-07-15-assign-training-remove-autogen-contract-design.md`

## Phase 0 — Rà soát (XONG)

- [x] Định vị luồng: `AssignTrainingController::toggleApprove()` → `AssignTrainingService::autogenousTrainingContract()` → `CreateTrainingContractJob` (1 job/học viên)
- [x] Xác minh luồng TẠO TAY đã tồn tại đầy đủ: nút "Tạo HĐĐT" trong `StudentModal.vue` → `/decision/category/training-contract/add` → `TrainingContractService::store()`
- [x] Data thật: 4/4 học viên trên QĐ đã duyệt đều có cờ = 2 → nút "Tạo HĐĐT" hiện KHÔNG BAO GIỜ hiện được
- [x] Queue: 0 `CreateTrainingContractJob` trong `jobs` (20 chờ) và `failed_jobs` (399) → xoá class an toàn
- [x] Mẫu in `HOP_DONG_DAO_TAO` chỉ bị tra cứu hardcode bởi chính Job; màn tạo tay cho user tự chọn mẫu

## Phase 1 — Gỡ tự sinh

### BE
- [x] `AssignTrainingController::toggleApprove()`: bỏ khối `if ($request->status == Decision::STATUS_APPROVED) { autogenousTrainingContract(...) }`
- [x] `AssignTrainingService`: xoá method `autogenousTrainingContract()` + import `CreateTrainingContractJob` + import `EmployeeInfo` (chỉ method này dùng)
- [x] Xoá file `Modules/Decision/Jobs/CreateTrainingContractJob.php`
- [x] `PrintTemplate::PROTECTED_CODES`: giữ `HOP_DONG_DAO_TAO` (mẫu hệ thống, màn tạo tay vẫn cần) — sửa comment trỏ Job đã xoá

### KHÔNG làm
- [x] KHÔNG xoá 4 HĐĐT đã tự sinh (dữ liệu thật, đã duyệt) — chỉ dừng sinh mới
- [x] KHÔNG đụng cờ `training_contract_status` (luồng tay đã tự set: store→2, destroy→1)

## Phase 2 — Verify

- [x] `php -l` sạch; grep 0 tham chiếu `CreateTrainingContractJob` / `autogenousTrainingContract`
- [x] Runtime: duyệt QĐ → KHÔNG sinh HĐĐT nào, cờ học viên giữ nguyên 1 (control: trước khi sửa phải sinh ra)
- [x] Nút "Tạo HĐĐT" hiện lên sau khi duyệt (trước đây bị tự sinh che mất)
- [x] Tiến trình QĐ sau duyệt = "Chưa tạo" (thay vì "Đã hoàn thành" tức thì)
- [x] Data test khôi phục sạch

### Checkpoint — 2026-07-15
Vừa hoàn thành: Gỡ toàn bộ luồng tự sinh HĐĐT (3 file sửa + 1 file xoá + composer dump-autoload). Verify runtime 6/6 PASS + browser thật.
Đang làm dở: (không)
Bước tiếp theo: User verify — duyệt 1 QĐ cử đi đào tạo, xác nhận không sinh HĐĐT và nút "Tạo HĐĐT" hiện ra.
Blocked: (không)

### Bằng chứng
- `nut-tao-hddt.png` — popup học viên trên QĐ đã duyệt: cả 3 học viên đều hiện nút "Tạo HĐĐT" (trước đây tự sinh set cờ=2 tức thì nên nút này KHÔNG BAO GIỜ hiện được)
- Màn danh sách: QĐ "Đã duyệt" + Tiến trình "Chưa tạo" — trước đây duyệt xong nhảy thẳng "Đã hoàn thành"
