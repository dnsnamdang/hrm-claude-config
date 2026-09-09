# Plan — Đưa `gop_db` lên PROD (1 nhánh, 2 môi trường)

Spec: `docs/superpowers/specs/gop-db/2026-09-04-prod-cutover-design.md`

## Phase 0 — Khảo sát & spec
- [x] Đo ranh giới `gop_db` ↔ `tpe`: 17 thư mục `pages/` mới + 3 màn lẻ
- [x] Rà cơ chế FE có sẵn (`subsystems.js` cờ `hidden`, `checkPermission.js` nhánh allowlist, `feature-unavailable.vue`)
- [x] Rà 42 migration mới, đọc 2 cái ALTER bảng ERP đáng ngờ nhất → an toàn
- [x] Đo 58 bảng trùng tên, đối chiếu row-count ERP / HRM / bản gộp
- [x] Đọc pipeline gộp (`Seeders/GopDb/`), xác định 3 nhóm `KEEP_HRM` / `SHARE` / `TACH`
- [x] Đo hậu quả thật trên bản gộp: 736 dòng trỏ nhầm role, 1.820 mồ côi, FK 2.313 → 10
- [x] Viết spec chi tiết + design tóm tắt

## Phase 1 — Vá pipeline gộp (CHƯA LÀM — chờ chốt)
- [ ] Xác minh cách `local_hrm_erp` được tạo ra (vì sao mất 99,6% FK)
- [ ] `ReconcileAuthSeeder`: remap FK `roles`/`permissions` toàn bộ theo `information_schema` + assert 0 mồ côi
- [ ] `MergeProdSeeder`: `KEEP_HRM` đổi `DROP` → `RENAME erp_<t>`
- [ ] Chuyển `majors`/`areas`/`transport_types`/`moving_norm_*`/`attachment_types`/`quotations`/`assign_business_tasks`/`job_request*` sang nhóm `TACH` (cần chủ phân hệ chốt)
- [ ] `notifications`: archive trước khi TRUNCATE
- [ ] Bước khôi phục FK của ERP sau khi remap

## Phase 2 — Cổng nghiệm thu ✅ XONG
- [x] Command `gopdb:health-check` (`app/Console/Commands/GopDb/HealthCheckCommand.php`) — chỉ SELECT, không ghi
- [x] `--mode=pre`: bảng trùng tên chưa phân nhóm · bảng ERP sắp bị DROP + số dòng mất · nhóm SHARE id có cùng nghĩa không · MỌI nơi trỏ roles/permissions + bảng nào seeder chưa remap · dải id chồng nhau · mốc số FK · bảng sắp TRUNCATE
- [x] `--mode=post`: FK còn lại so với gốc · trỏ nhầm/mồ côi · bảng KEEP_HRM còn dữ liệu không · bảng nào ít dòng hơn ERP gốc
- [x] Đọc nhóm KEEP_HRM/SHARE/TACH từ `MergeProdSeeder` bằng Reflection (1 nguồn sự thật, không chép tay)
- [x] Sửa 2 lỗi tự phát hiện khi chạy thử: (1) post phải lấy danh sách cột từ schema GỐC vì FK đã mất sau gộp — thiếu thì hụt 318 dòng; (2) không gắn nhãn "hợp lệ" theo bảng — bản đầu báo động giả 12.599 dòng, nay chỉ 5 pivot auth mới là hợp lệ, cột có ở cả 2 hệ đẩy sang "RÀ TAY"
- [x] Exit code 0/1/2 — cắm được vào pipeline deploy
- [x] Chạy thử: `pre` ra 2 CHẶN + 6 cảnh báo; `post` ra 4 CHẶN + 537 bảng ít dòng hơn ERP
- [ ] Chạy trên clone PROD, đối chiếu số (chờ có DB PROD)

## Phase 3 — FE 1 nhánh 2 môi trường (CHƯA LÀM — độc lập, làm được ngay)
- [ ] BE: bảng/khoá cấu hình `enabled_subsystems` + `blocked_links` + endpoint đọc
- [ ] FE: lọc `components/subsystems.js` theo `enabled_subsystems` (fail-closed)
- [ ] FE: chặn route trong `middleware/checkPermission.js` → `/feature-unavailable`
- [ ] Kiểm: PROD chỉ còn 7 phân hệ, gõ URL `/finance/...` bị chặn, dev vẫn thấy đủ

## Phase 4 — Kỷ luật migration (CHƯA LÀM)
- [ ] Bổ sung luật vào `CLAUDE.md` mục "Phần GỘP DATABASE"
- [ ] Chốt PROD chạy `migrate` tay theo checklist

### Checkpoint — 2026-09-04
Vừa hoàn thành: Phase 0 (khảo sát + spec) và Phase 2 (command `gopdb:health-check`, đã chạy thử cả 2 chế độ)
Đang làm dở: —
Bước tiếp theo: Phase 1 (vá pipeline gộp) hoặc Phase 3 (ẩn menu PROD) — chờ user chọn
Đã chốt: PROD **CHƯA gộp DB** → còn kịp vá pipeline trước khi chạy thật
Blocked: quyết định nghiệp vụ về `majors`/`areas`/`transport_types` cần chủ phân hệ
