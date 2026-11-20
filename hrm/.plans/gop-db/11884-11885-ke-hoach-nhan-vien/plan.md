# Plan — Kế hoạch bán hàng + KH phát triển thị trường của nhân viên (#11884 + #11885)

**Người phụ trách:** @junfoke — 2026-11-14
**Design:** `design.md` · **Spec:** `docs/superpowers/specs/gop-db/2026-11-14-11884-11885-ke-hoach-nhan-vien-design.md`
**Nhánh:** `feat/ke-hoach-nhan-vien` ở hrm-api, hrm-client, TanPhatDev — tách từ `origin/gop_db` 14/11, không upstream.

Viết tắt: KHBH = KH bán hàng NV (`sales_employee_plans`) · KHTT = KH phát triển thị trường NV (`market_employee_plans`).
Khuôn: Giao chỉ tiêu theo nhân viên (`Modules/Finance` BusinessTarget*, `components/business-target/*`).

## Phase 1 — BE nền (dùng chung 2 kế hoạch)
- [x] 1.1 Migration: `customer_number` (6 bảng), `export_sale_value` (3 bảng KHBH), `form_version` (2 bảng phiếu), index KHTT + `sales_employee_plan_customers(sale_employee_plan_province_id)`
- [x] 1.2 Catalog `sale.php`: thêm `hrm` vào `platforms` của 4 mã (`ke_hoach_ban_hang.view`, `ke_hoach_ban_hang_nhan_vien.approve`, `ke_hoach_phat_trien_thi_truong.view`, `ke_hoach_phat_trien_thi_truong_nhan_vien.approve`) + `permission:catalog-sync` local
- [x] 1.3 Entity cha `EmployeePlan` (6 trạng thái, màu, mã phiếu, phạm vi xem §6.1, cờ is_can_*) + `SaleEmployeePlan`, `MarketEmployeePlan` (bảng ERP)
- [x] 1.4 `EmployeePlanTargetService`: chỉ tiêu NV theo năm/tỉnh, năm có chỉ tiêu (port `getDataTargetEmployee`)
- [x] 1.5 `EmployeePlanService` (abstract, cấu hình cột theo kế hoạch): list / find / save (tháng → tỉnh, tổng tháng + phiếu) / validate / detail (cả phiếu cũ `form_version=1`) / luồng send-approve-reject-sendDirector-cancel / lịch sử / thông báo (dùng `BusinessTargetNotifier`)
- [x] 1.6 `EmployeePlanConverter`: phiếu nguồn đã duyệt + quy đổi xuôi/ngược theo hệ số (spec §7)
- [x] 1.7 Controller base + 2 controller, Request, routes `finance/sale-plan-employees`, `finance/market-plan-employees`, middleware khoá
- [x] 1.8 Print blade (3 kiểu) + `ExportColumnRegistry` + export-rows
- [x] 1.9 Test feature `Tests/Feature/EmployeePlanFlowTest.php` (9 test / 58 assert xanh) — chỉ local, đã thêm `.git/info/exclude`

### Ghi chú Phase 1 (14/11)
- Smoke test tinker (rollback): lưu/tổng/validate/gửi/TP duyệt/từ chối/gửi BGĐ/quy đổi xuôi-ngược/phiếu ERP chỉ xem/người ngoài phòng không thấy — đạt.
- ⚠️ Bẫy: `Collection->map('intval')` truyền KHOÁ làm `base` của intval ⇒ chuỗi ở khoá ≠ 0 thành 0 (đếm khách phiếu cũ ra 0). Dùng closure `(int) $v`.
- Người duyệt cấp TP: có mã duyệt NV (như middleware route ERP) VÀ (quản lý phòng phiếu hoặc cùng phòng).
- `route:list` lỗi sẵn do `Modules\Rice\...\RiceController` không tồn tại — không liên quan.

## Phase 2 — FE dùng chung
- [x] 2.1 `utils/employee-plan.js`: cấu hình cột 2 kế hoạch, cộng tổng, cây tháng/tỉnh/thị trường
- [x] 2.2 `components/employee-plan/PlanTreeTable.vue` (bảng cây cột cấu hình được, ghim tiêu đề + TỔNG, nhập số, dòng/cột chỉ tiêu)
- [x] 2.3 `EmployeePlanList.vue` (danh sách theo `kind`) + `employeePlanActionsMixin.js`
- [x] 2.4 `EmployeePlanForm.vue` (3 tab, chặn tạo khi chưa có chỉ tiêu, đổi năm, thêm/xoá dòng, validate, footer theo cờ)
- [x] 2.5 `ConvertPlanModal.vue` (lấy dữ liệu chéo, xem trước, ghi đè)
- [x] 2.6 Xuất Excel phiếu `utils/export/employeePlanExcel.js`

## Phase 3 — 2 màn
- [x] 3.1 KHTT: `pages/finance/market-plan-employees/{index,create,_id/index,_id/edit}.vue`
- [x] 3.2 KHBH: `pages/finance/sale-plan-employees/...`
- [x] 3.3 Menu `sale-hub.js`: 2 mục màn + 2 mục chờ duyệt (`?type=for-approve`, `codes`)

## Phase 4 — ERP
- [x] 4.1 Menu ERP `topmenubar.blade.php`: 4 mục (danh sách + chờ duyệt 2 kế hoạch NV) đổi sang link HRM tab mới, khuôn Giao chỉ tiêu (giữ route ERP)

## Phase 5 — Verify
- [x] 5.1 Test BE xanh trên `gop_db_rbac`
- [x] 5.2 Playwright: tạo → gửi → TP duyệt / từ chối → gửi BGĐ → hủy; lấy dữ liệu chéo; in; Excel; phiếu cũ chỉ xem; chụp ảnh so demo
- [x] 5.3 Checklist skill `erp-to-hrm-screen` + grep tự kiểm

### Kết quả verify Playwright (16/11/2026, client tạm cổng 3010 + API 8002, DB `gop_db_rbac`)
- TP (namdangit = NV 13): danh sách chờ duyệt → Xem (3 tab, số khớp) → Duyệt (3) → Gửi BGĐ từ dòng (4); In chi tiết / theo thị trường (A4 ngang, letterhead); thông báo Gửi duyệt tới TP.
- Người lập (NV 13 + chỉ tiêu thử 2026): Tạo KHBH (tháng 11→12, báo đỏ Tỉnh/TP · SL khách · cặp SL HĐ ↔ DS) → Lưu → Sửa → Lấy dữ liệu từ KHTT hệ số 3 (xem trước đúng, hệ số 0 báo đỏ + ẩn Áp dụng, ghi đè hỏi) → Lưu và gửi (2) → Hủy phiếu (6).
- Phiếu ERP cũ: danh sách đếm SL khách, "Nhân viên mới N"; Xem chỉ còn Xuất Excel / In / Quay lại + dòng ghi chú.
- Sửa trong lúc verify: dấu * ô Năm khi Xem; bản in tên ký dính "Ngày" (popup gộp `<br>` ⇒ dùng `<div>`); ô 0 ở form Sửa hiện "0" ⇒ để trống; hệ số sai vẫn hiện bảng xem trước cũ.
- Grep tự kiểm CLAUDE.md (HTML thô, vi-VN, text-muted, cờ quyền true, number_format VN): sạch.
- Dọn: xoá 4 phiếu thử + chỉ tiêu thử id 119 + lịch sử + thông báo; gỡ worktree `.worktrees/verify`; đóng trình duyệt.

## Checkpoint — 2026-11-16
Vừa hoàn thành: code xong Phase 1–4, test BE 9/9, verify Playwright đủ luồng 2 màn, dọn dữ liệu thử.
Đang làm dở: —
Bước tiếp theo: user review + commit 3 repo (hrm-api, hrm-client, TanPhatDev nhánh `feat/ke-hoach-nhan-vien`); prod chạy migration `2026_11_14_000001_add_hrm_columns_to_employee_plans` + `permission:catalog-sync`; cấp mã duyệt NV cho TP ở `/admin/roles` nếu vai trò chưa có.
Blocked:

## Checkpoint — 2026-11-16 (chiều)
Vừa hoàn thành: commit 3 repo nhánh `feat/ke-hoach-nhan-vien` (hrm-api `a93eb7259`, hrm-client `a531ed52b`, TanPhatDev `b9abbeb0c5`), push nhánh; merge nguyên nhánh vào develop (hrm-api `b542a7797`, hrm-client `6052f391b`) + develop_02 (TanPhatDev `1b7dbf7c12`), push.
Đang làm dở: —
Bước tiếp theo: QA trên dev; chạy migration + `permission:catalog-sync` trên dev nếu deploy chưa tự chạy; lên gop_db khi user bảo.
Blocked:

## Ngày 16/11/2026 — sau merge dev (@junfoke)
- [x] 16/11/2026 — Hỗ trợ trả lời cần cấp quyền gì để test: mỗi kế hoạch chỉ dùng 2 mã ("Xem danh sách…" có phạm vi + "Trưởng phòng duyệt kế hoạch … nhân viên"); NV lập không cần quyền nhưng phải có phiếu giao chỉ tiêu NV đã duyệt; TP duyệt cần mã duyệt VÀ quản lý / cùng phòng người lập.
- [x] 16/11/2026 — Hỗ trợ kiểm dev bấm menu không vào màn (gõ URL thì vào được): bundle dev đã có link + route, nguyên nhân tab trình duyệt giữ bản JS cũ → Ctrl+F5.
- [x] 16/11/2026 — Xử lý footer màn chi tiết lệch (Xuất Excel / In bị đẩy lên, cách không đều): bỏ `mr-2 mb-2` ở 10 nút footer `EmployeePlanForm.vue` cho khớp gap 5px của `V2Footer` (giống màn Giao chỉ tiêu). Client feat `4a8917b00`, develop `b46474157` (đã push).
- [x] 16/11/2026 — Hỗ trợ rà migration khi đồng nghiệp merge đợt kế hoạch NV lên gop_db: 5 migration (employee_plans thêm 3 cột + 8 index, meetings `workspace_id`, `chat_message_links`, 2 bảng Agent) không ảnh hưởng luồng ERP; rủi ro chỉ ở quyền (4 mã thêm `hrm`) — user xác nhận menu đã ẩn theo quản lý phân hệ.
- [ ] `PlanTreeTable.vue` sửa ghim tiêu đề khi cuộn (cùng lỗi màn giao chỉ tiêu — xem plan `giao-chi-tieu-kinh-doanh` 16/11): đã có trên develop `571cd64db`; bản chép sang nhánh `feat/ke-hoach-nhan-vien` chưa commit.

## Ngày 18/11/2026 (@junfoke)
- [x] 18/11/2026 — Xử lý 3 file thay đổi lạ trong `hrm-client` chính (nhánh `feat/ke-hoach-nhan-vien`: `TargetTreeTable.vue`, `PlanTreeTable.vue`, `utils/stickyTheadRows.js`): là bản chép test của session 16/11 (fix dòng TỔNG lệch khi cuộn), nội dung trùng commit `571cd64db` đã có trên develop + gop_db → dọn trả nhánh về sạch. Mục `PlanTreeTable.vue` để ngỏ ngày 16/11 coi như xong.
- [x] 18/11/2026 — Xuất testcase 2 màn theo skill testcase-documenter (khuôn tab Quốc gia): `testcase - Kế hoạch bán hàng của nhân viên.xlsx` + `testcase - Kế hoạch phát triển thị trường của nhân viên.xlsx`, mỗi file 261 TC / 15 nhóm, P0 40.6%, check_tc 0 lỗi, sinh từ `gen_testcase.py` chung.
- [ ] Chờ user chọn sửa 8 điểm code lệch thiết kế ghi trong TC: người cùng phòng có quyền duyệt thấy nút Gửi BGĐ nhưng bị đẩy về DS; lịch sử ghi "Thay đổi thông tin" cả khi không đổi; hủy khi Chờ TP duyệt không báo TP; Từ chối chỉ có ở màn Xem; nút Tạo mới luôn hiện; Excel 1 phiếu luôn ra 3 sheet; năm không còn chỉ tiêu thì màn Sửa không hiện bảng; ô tìm gõ %/_ ra toàn bộ.

## Ngày 20/11/2026 (@junfoke)
- [x] 20/11/2026 — Xuất tài liệu Mô tả nghiệp vụ (skill business-flow-documenter, 12 chương) cho #11884 + #11885 để gửi người dùng: `Mô tả nghiệp vụ - Kế hoạch bán hàng của nhân viên.docx` + `… Kế hoạch phát triển thị trường của nhân viên.docx` (17 trang mỗi file), sinh từ `gen_mo_ta_nghiep_vu.py` (hàm `build(kind)` chung). Đọc code develop xác nhận 8 điểm lệch thiết kế ngày 18/11 vẫn còn, ghi vào chương 12. Phát hiện thêm: số phiếu 5 số cuối là id nội bộ (không đếm theo công ty + năm như spec), sửa đổi Năm thì phần năm trong số phiếu đổi theo; công ty/phòng ban trên phiếu lấy theo hồ sơ gốc người lập; Gửi BGĐ chỉ báo người lập, BGĐ chưa nhận; Hủy không báo ai; TP tự lập rồi gửi thì lên thẳng Chờ BGĐ duyệt mà không ai nhận thông báo. Chưa sửa code. Gửi user đường dẫn 4 file, gợi ý thứ tự đọc: phòng ban → nhân viên → 2 kế hoạch.
