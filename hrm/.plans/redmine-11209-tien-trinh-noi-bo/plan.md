# Redmine #11209 — Đổi "Tiến trình dự án" → "Tiến trình nội bộ" + cập nhật nhãn/logic trạng thái

Nhánh: `tpe-develop-assign_fix` (cả API và Client)

## Phase 1 — Đổi nhãn (AC1, AC2, AC3)

### BE
- [ ] `ProspectiveProject::STATUS` id 8: `Thương thảo dự án hợp đồng` → `Thương thảo hợp đồng`
- [ ] `resources/views/exports/prospective_projects.blade.php`: header cột + map id 8

### FE
- [ ] Nhãn `Tiến trình dự án` → `Tiến trình nội bộ`: danh sách dự án TKT (nhãn lọc, placeholder, cột), tab dự án con, chi tiết giải pháp, danh sách giải pháp, Việc của tôi (tab GP + modal sắp tới)
- [ ] Báo cáo tổng hợp dự án TKT theo Phòng ban - Nhân viên KD: nhãn lọc + placeholder + nhãn cụm thống kê `Trạng thái dự án` → `Tiến trình nội bộ`
- [ ] Giá trị id 8 → `Thương thảo hợp đồng` ở mọi nơi hardcode (danh sách, tab con, tasks, giải pháp, 2 màn báo cáo, `reportUtils.js`, pill ở màn quản lý dự án)

## Phase 2 — Logic tự chuyển trạng thái (AC4)

- [ ] `ProspectiveProjectService::finalizeSolution()` (nút **Chốt giải pháp**): đang set `Thương thảo dự án hợp đồng (8)` → phải là `Dự toán (6)`, chỉ tiến không lùi
- [ ] `QuotationService::finalize()` (nút **Chốt báo giá / Trúng thầu**): hiện KHÔNG đổi tiến trình dự án → phải set `Thương thảo hợp đồng (8)`, chỉ tiến không lùi
- [ ] Giữ nguyên 2 nhánh đã đúng: gửi YCXDG → Dự toán; báo giá được duyệt nội bộ → Thương thảo giá

## Kết quả

### BE (`hrm-api`)
- [x] `ProspectiveProject::STATUS` id 8 → `Thương thảo hợp đồng` (bộ **dự án cha** giữ nguyên `Thương thảo DA/Hợp đồng` — bảng trong task là "dự án thường (Nội bộ)")
- [x] `resources/views/exports/prospective_projects.blade.php`: header cột → `Tiến trình nội bộ`, map id 8 → `Thương thảo hợp đồng`
- [x] `ProspectiveProjectService::finalizeSolution()`: `Thương thảo hợp đồng (8)` → `Dự toán (6)`, guard chỉ tiến không lùi
- [x] `QuotationService::finalize()`: bổ sung nâng tiến trình dự án lên `Thương thảo hợp đồng (8)`, guard chỉ tiến không lùi

### FE (`hrm-client`) — 16 file
- [x] Nhãn → `Tiến trình nội bộ`: danh sách dự án TKT (lọc + placeholder + cột), tab dự án con, form Tạo/Sửa/Chi tiết, chi tiết giải pháp (`ProjectInfoTab`), danh sách giải pháp, Việc của tôi (tab GP + modal sắp tới), tasks
- [x] Báo cáo tổng hợp dự án TKT: nhãn lọc + placeholder + nhãn cụm thống kê + **cột bảng** `Cơ cấu trạng thái dự án` → `Cơ cấu tiến trình nội bộ` + nút `Cơ cấu trạng thái` → `Cơ cấu tiến trình` + modal danh sách (`Trạng thái` → `Tiến trình nội bộ`)
- [x] Giá trị id 8 → `Thương thảo hợp đồng` ở mọi nơi hardcode; `reportUtils.js` giữ thêm key tên cũ làm fallback màu

### Kiểm thử — 42 case, 0 FAIL
- [x] BE 17 case (tinker): nhãn id 6/7/8 + dự án cha không đổi · chốt báo giá từ bước 1 và bước 7 đều lên 8 · đang bước 9 KHÔNG lùi · báo giá chưa duyệt bị chặn và không đổi tiến trình · chốt giải pháp 5→6 · đang bước 7 KHÔNG lùi về 6 · 3 nhánh cũ (YCXDG, tạo báo giá, duyệt báo giá) còn nguyên
- [x] UI 25 case (Playwright): danh sách TKT · dropdown lọc · báo cáo (cột + lọc + dropdown) · danh sách giải pháp · form Tạo/Sửa/Chi tiết/Quản lý dự án · tab Thông tin của chi tiết giải pháp · API không còn tên cũ

### Quyết định đã chốt (user 2026-08-26)
1. **Hủy chốt báo giá PHẢI hạ tiến trình** → `QuotationService::unfinalize()` lùi dự án từ `Thương thảo hợp đồng (8)` về `Thương thảo giá (7)`, tương ứng báo giá quay lại `Đã duyệt`. Chỉ lùi khi dự án đang đứng đúng ở bước 8; đã đi tiếp (bước 9 trở lên) hoặc còn ở bước thấp hơn thì không đụng.
3. **Dự án cha cũng đổi** → `PARENT_STATUS` id 8: `Thương thảo DA/Hợp đồng` → `Thương thảo hợp đồng`. Các nhãn riêng khác của dự án cha giữ nguyên (id 7 vẫn `Trình duyệt hợp đồng`). FE lấy tên dự án cha từ `status_name` của BE nên không phải sửa thêm.

### Còn treo
2. **Duyệt thêm một báo giá khác sau khi đã chốt**: `cascadeApprovedStatus()` set thẳng `Thương thảo giá (7)` không guard → kéo dự án từ 8 lùi về 7. User chưa trả lời, đang GIỮ NGUYÊN.

### Kiểm thử lần 2 sau khi chốt — 49 case, 0 FAIL
- BE 24 case: thêm nhãn dự án cha (3 case) + nhóm hủy chốt báo giá (5 case: chốt→hủy quay đúng về 7, báo giá về Đã duyệt, dự án đã sang bước 9 không bị kéo lùi, hủy chốt thiếu lý do bị chặn và tiến trình giữ nguyên)
- UI 25 case: chạy lại toàn bộ, không hồi quy

## E2E một luồng trên UI thật (Playwright) — dự án `dự án test 28/7` (id 56)

Chạy hết chuỗi bằng thao tác người dùng, mỗi mốc đối chiếu **chữ trên màn** với **status trong DB**:

| # | Thao tác trên UI | Tiến trình nội bộ sau thao tác | Kết quả |
| - | --- | --- | --- |
| 1 | Mở màn Quản lý dự án | Đã duyệt giải pháp (5) | ✅ xuất phát |
| 2 | Nút **Chốt giải pháp** → chọn hồ sơ → Lưu & gửi thông báo | **Dự toán (6)** | ✅ (trước sửa: nhảy thẳng bước 8) |
| 3 | Tab Báo giá → **Tạo báo giá** → thêm hàng hoá → Lưu nháp | Dự toán (6) — không đổi | ✅ |
| 4 | **Gửi duyệt** → TP **Duyệt & chuyển BGĐ** → **BGĐ duyệt** | **Thương thảo giá (7)** | ✅ |
| 5 | Tab Báo giá → **Chốt báo giá (Trúng thầu)** | **Thương thảo hợp đồng (8)** | ✅ (trước sửa: không đổi gì) |
| 6 | Tab Báo giá → **Hủy chốt** + nhập lý do | **Thương thảo giá (7)** | ✅ (trước sửa: kẹt ở bước 8) |

- Báo giá thử: `BG-2026-00264`, đi đúng vòng `Đang tạo → Chờ TP duyệt → Chờ BGĐ duyệt → Đã duyệt → Trúng thầu → Đã duyệt`.
- Ảnh: `e2e-1-start.png` … `e2e-8-unfinalized.png` trong scratchpad.
- **Đã dọn sạch**: xoá báo giá 264 + dữ liệu con, trả dự án 56 về `Đã duyệt giải pháp (5)`, giải pháp 14 về 11, hồ sơ 16 về `approved`/`finalized_at = NULL`.
