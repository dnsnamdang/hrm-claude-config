# Plan — Trường Trạng thái ở form Tạo mới/Sửa/Xem của mọi màn danh mục

Nhánh: `gop_db` · @namdangit · Bắt đầu 2026-09-23

Quy tắc: form Tạo mới / Cập nhật danh mục hiện trường **Trạng thái**, cho sửa (vẫn tuân điều kiện khoá như nút Khoá ở danh sách — BE chặn thật); form Xem vẫn hiện Trạng thái (khoá, chỉ đọc).
Khuôn: `/assign/solution-groups` — `components/modal/industry-modal.vue` + `IndustriesService::update()`.

## Phase 1 — Rà + sửa theo nhóm phân hệ
- [x] Giao việc (`pages/assign/*` danh mục)
- [x] Hành chính nhân sự (`pages/human/*` danh mục)
- [x] Quyết định + Phòng họp + Cơm + Ca làm việc
- [x] Tài chính + CSKH
- [x] Danh mục chung (`pages/master-data/*`, danh mục xe)
- [x] Đào tạo (`pages/training/*` danh mục)

## Phase 2 — Validate ký tự mã (`code_chars`) cho danh mục có mã
Khuôn: `/human/nations`. BE Rule dùng chung `app/Rules/CodeChars.php`; FE rule có sẵn `code_chars`. Sửa: **luôn kiểm, kể cả giữ nguyên mã cũ (user chốt 2026-09-23)**. **Chỉ áp màn MỚI dùng V2Base* (user chốt 2026-09-23)** — màn form cũ (input thô) không áp.
- [x] Tạo `App\Rules\CodeChars`
- [x] Giao việc + Danh mục chung + Nhân sự: Quốc gia (chuyển sang Rule chung), Ngân hàng; 6 màn Nhân sự cũ đã hoàn
- [x] Tài chính + CSKH: Tiền tệ, Loại TK, Mã phí, Vụ việc, Gói bảo dưỡng (Ca làm việc không áp)
- [x] Đào tạo — không màn nào (Năng lực là form cũ, đã hoàn)

## Phase 3 — Kiểm thử
- [x] Test API nhóm 1 + nhóm 2 (0 case không đạt sau khi sửa 6 lỗi phát sinh)
- [x] Test giao diện Playwright 14 màn mẫu (Phòng họp không test được: DB local không role nào có quyền)
- [x] Sửa lỗi nhỏ: đường dẫn 404 thiếu `/` ở capacity-framework edit; `:rows` ở DeviceErrorForm

## Checkpoint
### Checkpoint — 2026-09-23
Vừa hoàn thành: rà + sửa 6 nhóm (~60 màn). BE 121 file / FE 64 file, php -l sạch. Chưa test trình duyệt, chưa commit.
Đang làm dở: —
Bước tiếp theo: user chốt các câu hỏi mở (accounts #11300, source-capitals, operating-support, form-templates, customers, bản ghi khoá vẫn sửa được ở màn cũ, API lock/unlock thiếu gate) → test Playwright nếu user yêu cầu.
Blocked: 5 danh mục Xe chưa có trên gop_db (nằm ở nhánh danh_muc_xe).
