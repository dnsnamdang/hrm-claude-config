# Plan — Duyệt hợp đồng kết xuất cung ứng

**Người phụ trách:** @khoipv · **Bắt đầu:** 16/09/2026

> Design tóm tắt: [design.md](design.md)
> Spec đầy đủ: [docs/superpowers/specs/2026-09-16-duyet-ket-xuat-hop-dong-cung-ung-design.md](../../docs/superpowers/specs/2026-09-16-duyet-ket-xuat-hop-dong-cung-ung-design.md)

## Phase 0 — Chuẩn bị tài liệu

- [x] Tạo `.plans/duyet-ket-xuat-hop-dong-cung-ung/design.md`
- [x] Tạo `.plans/duyet-ket-xuat-hop-dong-cung-ung/plan.md`
- [x] Tạo `docs/superpowers/specs/2026-09-16-duyet-ket-xuat-hop-dong-cung-ung-design.md`
- [x] Thêm entry vào `.plans/STATUS.md`
- [x] Brainstorming với user để chốt design (user duyệt: "ok làm đi")
- [x] Fill spec đầy đủ + design.md tóm tắt + plan.md chi tiết

## Phase 1 — Backend: Entity + hằng số

- [x] `Contract.php` — thêm `CHO_DUYET_KET_XUAT = 10`, `KHONG_DUYET_KET_XUAT = 11`, `PERM_APPROVE_RENDER_SUPPLY`
- [x] `Contract.php` — `$fillable` thêm `supply_render_requested_at`, `supply_render_requested_by`
- [x] `Contract.php` — `approvedStatuses()` trả `[3, 9, 10, 11]`
- [x] `Contract.php` — `canRenderSupply()` nhận status thuộc {3, 11}
- [x] `Contract.php` — thêm `canApproveRenderSupply()`, `canRejectRenderSupply()`, `canWithdrawRenderSupply()`
- [x] `Contract.php` — `canAssign()` thêm 10, 11

## Phase 2 — Backend: Migration + quyền

- [x] Migration `add_supply_render_request_to_contracts` (2 cột + index, không khóa ngoại)
- [x] `PermissionsTableSeeder.php` — thêm dòng quyền 525 (id 525, group Hợp đồng, type 8) — quy ước: quyền chỉ sửa ở seeder, KHÔNG viết migration
- [x] Chạy `php artisan migrate` và kiểm tra bảng `permissions`

## Phase 3 — Backend: Service

- [x] `ContractService::renderSupply()` — đích đến đổi sang status 10, ghi 2 cột request, xóa `reason_deny`
- [x] `ContractService::approveRenderSupply()` — ghi `supply_rendered_at/_by`, status 9
- [x] `ContractService::rejectRenderSupply()` — status 11 + `reason_deny`
- [x] `ContractService::withdrawRenderSupply()` — về status 3, xóa 2 cột request
- [x] `ContractService::notifyRenderSupplyApprovers()` + thông báo duyệt / từ chối tới người lập
- [x] `ContractService::getContracts()` — nhánh `request_type = 'wait-render-approve'`

## Phase 4 — Backend: Controller + Route + Resource

- [x] `RejectRenderSupplyContractRequest` — `reason_deny` required|string|max:1000
- [x] `ContractController` — 3 action `approveRenderSupply` / `rejectRenderSupply` / `withdrawRenderSupply`
- [x] `Routes/api.php` — 3 route PUT dưới `render-supply`
- [x] `ContractResource` + `ContractDetailResource` — 4 field mới
- [x] Nhãn trạng thái: `CategoryDashboardService.php:1445`, `Supply/.../PurchaseOrderController.php:388`

## Phase 5 — Frontend: Menu + màn duyệt

- [x] `utils/MenuContract.js` — mục thứ 6 trong "Phê duyệt"
- [x] `pages/contract/contract/approve-render-supply.vue` — màn mới (clone approve.vue)
- [x] Popup xác nhận Duyệt + popup nhập lý do Từ chối

## Phase 6 — Frontend: Màn kết xuất + pill + dropdown

- [x] `pages/contract/contract/_id/render.vue` — 3 chế độ (nhập / chỉ xem + duyệt / chặn), banner lý do từ chối
- [x] Pill 10, 11 ở 4 màn: `contract/index.vue`, `contract/approve.vue`, `detail-report/index.vue`, `reports/sale-product/index.vue`
- [x] 8 dropdown phụ lục đổi `status=3,9` thành `status=3,9,10,11`
- [x] `contract/index.vue` — nút "Thu hồi"

## Phase 8 — Bổ sung sau kiểm thử

- [x] Màn `approve-render-supply`: thêm trạng thái loading (b-spinner "Đang tải dữ liệu...") thay cho dòng "Không có dữ liệu" lúc đang gọi API
- [x] Bọc `<b-tr v-for>` bằng `<template v-if="!isLoading">` (bỏ anti-pattern v-for + v-if cùng thẻ), `isLoading` khởi tạo `true` để không nháy dòng trống
- [x] `getData()` bọc try/catch/finally — API lỗi không làm spinner quay mãi, có toast báo lỗi

## Phase 9 — Tối ưu API dropdown của màn duyệt

- [x] BE: `GET category/customers/options` — trả id/code/name, query thuần, không qua Resource
- [x] BE: `GET category/projects/options` — giữ nguyên scope `status != DANG_TAO OR created_by = me`
- [x] BE: `GET category/quotations/options` — trả id/code
- [x] BE: đăng ký 3 route TRƯỚC route `/{param}` để không bị nuốt
- [x] FE: `approve-render-supply.vue` gọi 3 endpoint options thay `?per_page=2000`
- [x] FE: lazy load — chỉ nạp dropdown khi mở bộ lọc lần đầu, không chặn màn lúc vào
- [x] FE: bộ lọc đã có giá trị lưu ở localStorage thì nạp ngay lúc mounted (Select2 không bị trống nhãn)
- [x] Đo lại thời gian trên Playwright, so với mốc cũ (~33s)

## Phase 10 — Đồng nhất icon nút thao tác

- [x] `approve-render-supply.vue`: nút X đổi `fa fa-times` → `fas fa-times text-danger` (khớp `bid_package/project`, `bid_package/quotation`, `sale/project`)
- [x] `approve-render-supply.vue`: nút "Xem nội dung kết xuất" bổ sung `variant="secondary"` cho khớp 2 nút cùng cột
- [x] `contract/index.vue`: nút Thu hồi đổi `fa fa-undo` → `fas fa-undo text-danger` (khớp `bid_package_render`, `quotation_render`)
- [x] `approve-render-supply.vue`: scoped style ép `.btn-small i` về hộp 20x20 (font-size 18px) để nút X bằng đúng 2 nút icon svg — 32x32, không đụng CSS chung `.btn-small`

## Phase 11 — Sửa các cột sai field ở màn chờ duyệt kết xuất

- [x] Cột Công ty: `main_company_name` (không có trong Resource) → `main_company_code`
- [x] Cột Giá trị hợp đồng: `total_after_vat` (không có) → `total_amount`
- [x] Cột Thời gian hợp đồng: `contract_time` (không có) → `contract_sign_time` – `contract_end_time`
- [x] Cột Gói thầu → đổi nhãn **"Gói thầu/ BG"**, dùng `objectable_code` + link theo `objectable_type`
- [x] Cột Dự toán: thêm fallback danh sách `projects` (HĐ lập từ gói thầu gộp có `project_id` null)
- [x] Cột "Số hợp đồng" đang hiển thị `code` (mã) → đổi nhãn thành "Mã hợp đồng"
- [x] **@khoipv duyệt: sửa luôn** `pages/contract/contract/approve.vue` (màn Duyệt hợp đồng) dính đúng 3 lỗi field này
  - [x] `main_company_name` → `main_company_code`
  - [x] `total_after_vat` → `total_amount`
  - [x] `contract_time` → `contract_sign_time` – `contract_end_time`
  - [x] Cột Gói thầu → "Gói thầu/ BG", dùng `objectable_code` + link theo `objectable_type` (đang dùng `bid_package_id` nên HĐ từ báo giá trống)
  - [x] Cột Dự toán: fallback danh sách `projects`
  - [x] Cột "Số hợp đồng" → "Mã hợp đồng"

---

## Phase 7 — Kiểm thử

- [x] Script tinker 10 ca (bọc beginTransaction + rollBack) — PASS toàn bộ
- [x] Gán quyền 525 cho vai trò ở màn Phân quyền — tick ở /timesheet/setting/roles/add/3, DB `role_has_permissions` có (3, 525)
- [x] Build lại client + hard refresh — chạy trên dev server 3001, menu + màn mới hiển thị đúng
- [x] Test Playwright: gửi duyệt → duyệt → HĐ hiện ở supply/contract_render — PASS trên HĐ 193 (HD-173/2026)
- [x] Test Playwright: từ chối → banner đỏ → gửi lại; thu hồi — PASS đủ vòng 3 → 10 → 11 → 10 → 3 → 10 → 9

---

### Checkpoint — 17/09/2026
Vừa hoàn thành: Phase 1-6 — toàn bộ backend (entity, migration, service, controller, route, resource) và frontend (menu, màn duyệt mới, render.vue 3 chế độ, pill/nhãn 4 màn, 8 dropdown phụ lục, nút Thu hồi). 7 file .vue đã qua vue-template-compiler + @babel/parser, mọi file .php qua `php -l`.
Đang làm dở: Phase 7 — script tinker 10 ca đã PASS; còn gán quyền 525 cho vai trò, build client, test Playwright.
Bước tiếp theo: gán quyền 525 ở màn Phân quyền, build lại client, chạy Playwright luồng gửi duyệt → duyệt → HĐ hiện ở supply/contract_render.
Blocked:

### Checkpoint — 17/09/2026 (Phase 7 hoàn tất)
Vừa hoàn thành: Toàn bộ Phase 7. Chạy E2E Playwright trên HĐ 193 (HD-173/2026) đủ vòng đời:
  3 --Kết xuất--> 10 --Từ chối--> 11 --Kết xuất lại--> 10 --Thu hồi--> 3 --Kết xuất--> 10 --Duyệt--> 9.
  - `supply_render_requested_at` chỉ set khi gửi duyệt, xoá khi thu hồi; `supply_rendered_at` CHỈ set lúc duyệt (09:43:06) — phân hệ Cung ứng không phải sửa dòng nào.
  - `/supply/rendered-contracts` sau khi duyệt có HD-173/2026 (total 5).
  - `history_approved_contracts` ghi đủ 6 dòng với `action`: Gửi duyệt kết xuất cung ứng / Không duyệt kết xuất cung ứng (kèm reason_deny) / Thu hồi kết xuất cung ứng / Duyệt kết xuất cung ứng.
  - Thông báo đủ 3 nhịp: gửi duyệt → người có quyền duyệt (url `/contract/contract/approve-render-supply`); từ chối → người lập kèm lý do; duyệt → người lập (url `/contract/contract/193`).
  - Màn `/contract/contract/193/render` tự đổi vai: status 10 → title "Duyệt kết xuất hợp đồng sang cung ứng", footer [Quay lại, Từ chối, Duyệt]; status 11 → banner đỏ nêu lý do, footer [Quay lại, Kết xuất].
  - Nút Thu hồi (fa-undo) trên `/contract/contract` hiện đúng khi status 10, xác nhận swal rồi trả HĐ về 3.
Đang làm dở: (không)
Bước tiếp theo: Feature xong. Chờ @khoipv review + tự commit (quy ước: không tự commit).
Blocked:

### Checkpoint — 17/09/2026 (Phase 8)
Vừa hoàn thành: Thêm loading cho màn `/contract/contract/approve-render-supply` (`pages/contract/contract/approve-render-supply.vue`).
  - Verify Playwright: mốc 6s bảng hiện spinner + "Đang tải dữ liệu..."; mốc 33s ra dữ liệu HD-194/2026 (pill "Chờ duyệt kết xuất"). Không còn cảnh hiện "Không có dữ liệu" trong lúc chờ.
Đang làm dở: (không)
Bước tiếp theo: Tối ưu API dropdown — xem Phase 9.
Blocked:

### Checkpoint — 17/09/2026 (Phase 9)
Vừa hoàn thành: Tối ưu API dropdown cho màn duyệt kết xuất.
  - BE: thêm `options()` vào `ProjectService` / `CustomerService` / `QuotationService` + action cùng tên ở 3 controller + 3 route `GET category/{projects,customers,quotations}/options` (đặt trước route `/{param}`).
  - FE: `approve-render-supply.vue` gọi `/options`, gom vào `loadFilterOptions()` chạy 1 lần khi `@show` của `b-collapse` bộ lọc; nếu localStorage đã có giá trị lọc thì nạp ngay lúc mounted.
  - Đo thực tế (gọi tuần tự, cùng máy):

    | Dropdown | Cũ `?per_page=2000` | Mới `/options` | Payload cũ → mới |
    |---|---|---|---|
    | projects | 6.105s | 1.101s | 364 KB → 12 KB |
    | quotations | 12.673s | 1.062s | 595 KB → 9 KB |
    | customers | 2.689s | 1.079s | 728 KB → 85 KB |

  - Số bản ghi khớp 100% giữa cũ và mới (278 / 336 / 1051) → không đổi phạm vi nhìn thấy.
  - Thời gian vào màn tới lúc có dữ liệu: 33s → 15s; lúc vào màn chỉ còn 2 request (`user-profile` + `contracts`).
  - Kiểm lại bộ lọc: chọn DT-251/2026 → 1 dòng; chọn DT-250/2026 → 0 dòng; bỏ lọc → 1 dòng.
Đang làm dở: (không)
Bước tiếp theo: Chờ @khoipv review + tự commit.
Blocked:

### Checkpoint — 17/09/2026 (Phase 10)
Vừa hoàn thành: Đồng nhất icon nút thao tác với các màn khác trong dự án.
  - Quy ước chung của dự án: nút từ chối `<i class="fas fa-times text-danger">`, nút thu hồi `<i class="fas fa-undo text-danger">`, đặt trong `<b-button variant="secondary" class="btn-small">`.
  - Verify Playwright: 3 nút cùng class `btn btn-small btn-secondary`; icon X là `fas fa-times text-danger`, màu tính ra `rgb(241, 85, 108)`.
  - Kích thước trước khi sửa: 2 nút svg 32x32 (icon 20x20), nút X 20x31 (icon 9x13). Sau khi sửa cả 3 đều 32x32 / icon 20x20, cùng `top`.
Đang làm dở: (không)
Bước tiếp theo: Chờ @khoipv review + tự commit.
Blocked:

### Checkpoint — 17/09/2026 (Phase 11)
Vừa hoàn thành: Sửa các cột trỏ sai field ở `approve-render-supply.vue`.
  - `main_company_name`, `total_after_vat`, `contract_time` KHÔNG tồn tại trong `ContractResource` → 3 cột trống. Field đúng: `main_company_code`, `total_amount`, `contract_sign_time`/`contract_end_time`.
  - Lưu ý: bảng `contracts` có cột `contract_time` nhưng Resource không trả, và form HĐ chỉ nhập "Ngày ký hợp đồng"/"Ngày kết thúc" → chọn dùng 2 field đã có thay vì thêm field vào Resource dùng chung.
  - Cột "Gói thầu" → "Gói thầu/ BG", dùng `objectable_code`; link `/bid_package/bid_package/{id}` khi `objectable_type` là BidPackage, ngược lại `/plan/quotation/{id}` (giống `contract/index.vue`).
  - Bẫy: chuỗi class PHP trong template Vue phải escape 2 lần — `'Modules\Category\Entities\BidPackage\BidPackage'`; viết 1 gạch chéo thì JS nuốt mất, so sánh luôn sai.
  - Verify Playwright: 11/11 cột có dữ liệu — VX / DT-251/2026 / BG-342 / 85.000.000 / 17/09/2026 - 30/09/2026 / Chờ duyệt kết xuất / DNS Admin / 17/09/2026.
  - Ép `objectable_type` = BidPackage → link đổi sang `/bid_package/bid_package/99`; ép `project_id` null + `projects` 2 phần tử → render 2 link dự toán.
Đang làm dở: (không)
Bước tiếp theo: Hỏi @khoipv có sửa luôn `contract/approve.vue` (cùng 3 lỗi field) không.
Blocked:

### Checkpoint — 17/09/2026 (Phase 11 bổ sung)
Vừa hoàn thành: Áp cùng bộ sửa cột sang `pages/contract/contract/approve.vue` (@khoipv duyệt sửa luôn).
  - Cột Gói thầu ở màn này còn nặng hơn: nó dùng `bid_package_id`/`bid_package_code` nên HĐ lập từ báo giá luôn trống → đã chuyển sang `objectable_*` như `contract/index.vue`.
  - Verify Playwright bằng cách gán `vm.tableData` 2 dòng mẫu (màn thật đang rỗng vì không có HĐ chờ duyệt):
    - Dòng quotation → `/plan/quotation/342 => BG-342`, `VX`, `85.000.000`, `17/09/2026 - 30/09/2026`
    - Dòng bid package + 2 dự toán → `/bid_package/bid_package/99 => GT-99/2026`, `/sale/project/11`, `/sale/project/12`, `contract_end_time` null chỉ hiện `01/09/2026`
  - Đã reload trang để xoá dữ liệu giả lập.
Đang làm dở: (không)
Bước tiếp theo: Chờ yêu cầu mới. Tồn đọng: 32 file trong `pages/` vẫn gọi `?per_page=2000` (task riêng).
Blocked:

### Ghi chú dữ liệu test (cần biết khi chạy lại)
- HĐ 193 (HD-173/2026) hiện đang ở **status 9 — Đã kết xuất**, đã nằm trong danh sách cung ứng. Muốn test lại phải đưa về 3.
- Đã thêm fixture 1 dòng `contract_results` id 740 cho HĐ 193 để qua `RenderSupplyContractRequest` (validate CŨ, không thuộc thay đổi lần này).
- ~~API dropdown ở local rất chậm~~ — đã xử lý ở Phase 9 bằng endpoint `/options`. Nguyên nhân gốc là N+1 trong `ProjectResource::toArray()` (~12 query/dòng) và các Resource tương tự; **các màn khác vẫn còn dùng `?per_page=2000` (32 file trong `pages/`)** nếu muốn tối ưu tiếp.
- `php artisan tinker <file>` treo trên máy này; dùng script bootstrap Laravel trực tiếp. `mysql` CLI cũng hay treo khi API đang bận — verify qua API hoặc script PHP.

### Checkpoint — 17/09/2026 (bỏ migration quyền)
Vừa hoàn thành: Xóa migration thao tác bảng `permissions` (sai quy ước dự án) — quyền chỉ khai ở `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`.
  - Xóa file `Modules/Category/Database/Migrations/2026_09_16_000011_add_permission_approve_render_supply.php`
  - Xóa dòng tương ứng trong bảng `migrations` của `thanhan_stag_07052026` (DB đã có sẵn dữ liệu quyền đúng, không cần chạy lại gì)
  - Cập nhật spec + plan + STATUS bỏ mọi tham chiếu tới migration quyền
Đang làm dở: không có.
Bước tiếp theo: user review luồng duyệt kết xuất hợp đồng sang cung ứng.
Blocked: không có.
