# Plan — Yêu cầu kiểm tra sửa chữa – bảo hành

## Phase 1 — Backend

### BE
- [x] Entity `WarrantyRepairRequest` (bảng `warranty_repair_requests`) — 9 trạng thái, accessor `canEdit/canHandleRequest/canTransferDepartmentReception/isCanDelete`, `generateCode()`
- [x] Entity `WarrantyRepairRequestProduct` (bảng `warranty_repair_request_products`)
- [x] `WarrantyRepairRequestService` — `list()` 3 tab + bộ lọc, `store/update/delete`, `syncProducts()`, `reject()`, `transferDepartmentReception()`
- [x] `WarrantyRepairRequestRequest` (FormRequest) — required theo `status` (Lưu nháp vs Gửi yêu cầu)
- [x] `WarrantyRepairRequestResource` + `WarrantyRepairRequestListResource`
- [x] `WarrantyRepairRequestController` — index/show/store/update/delete/reject/transfer/options/export/print
- [x] ~~API tra thiết bị của khách hàng~~ — DÙNG LẠI endpoint có sẵn `GET /v1/assign/customers/{id}/equipment` (`CustomerManagerService::equipmentList`, đủ 3 nguồn + serial), không viết mới
- [x] Routes `/v1/customer-care/warranty-repair-requests` + middleware checkPermission
- [x] Thêm 4 quyền vào `PermissionsTableSeeder` (id 1177–1180)
- [x] Thông báo khi chuyển "Chờ xử lý" + khi Từ chối (`WarrantyRepairRequestNotifier`, prefix `[YCSCBH]`)
- [x] Export Excel danh sách (`WarrantyRepairRequestExport`)
- [x] In 1 phiếu + In danh sách bằng mẫu ERP 277/278 (`WarrantyRepairRequestPrintService`)
- [x] Upload file đính kèm của dòng thiết bị lên S3 (`POST /upload-attachment`, thư mục `wr_requests` như ERP)

## Phase 2 — Frontend

### FE
- [x] Màn danh sách `pages/customer-care/warranty-repair-requests/index.vue` — 3 tab + filter + cột + hành động
- [x] Form dùng chung `components/WarrantyRepairRequestForm.vue` (tạo/sửa/chi tiết) + 3 màn mỏng `create.vue` / `_id/edit.vue` / `_id/index.vue`
- [x] Popup chọn khách hàng — DÙNG LẠI `components/modals/ChooseErpCustomerModal.vue` (modal global), không tự dựng
- [x] Bảng "II – Danh mục trang thiết bị hiện có của khách hàng" ngay trong form (như ERP), nguồn `assign/customers/{id}/equipment`
- [x] Người liên hệ: select từ `customer.contacts` (pattern Dự án TKT), không tạo popup riêng
- [x] Popup Chuyển phòng tiếp nhận + popup Từ chối (dựng trên `V2BaseModal`)
- [x] Cột File đính kèm trong bảng thiết bị (upload ngay khi chọn, hiện link + nút bỏ file)
- [x] Màn In phiếu (`_id/print.vue`, mẫu ERP 277) + In danh sách (`print.vue`, mẫu ERP 278, khổ ngang)
- [x] Thêm menu vào `components/subsystem-menu/sale-hub.js`

## Phase 3 — Sửa sau khi test thật (18/08)

### BE
- [x] **Quyền chuyển hẳn sang HRM** (user chốt): tạo 4 quyền guard `api` id 1177–1180, không dùng bản quyền ERP cùng tên
- [x] Sửa lỗi kiểm quyền: `auth()->user()` là `TpEmployee` **không có trait `HasRoles`** → `->can()` luôn false; thay bằng `Support/WarrantyRepairPermission` (nạp qua `Modules\Timesheet\Entities\Employee`)
- [x] `GET /options` trả thêm cờ `can_handle` để FE mở tab "Chờ xử lý"
- [x] Thêm `GET /customer-info/{customerId}` — người liên hệ / nơi giao nhận / loại hình tổ chức, thay cho `assign/customers/{id}` (endpoint đó gate bằng quyền ERP → 403)
- [x] `POST /upload-attachment` (S3, thư mục `wr_requests` như ERP)
- [x] In danh sách: "Thời gian: Tất cả" khi không lọc ngày (ERP in ra dấu `-` trơ)

### FE
- [x] Sửa lỗi **select2 mất liên kết khi options nạp bất đồng bộ** (Người liên hệ / Địa chỉ sửa chữa / Serial) — thêm `:key` để dựng lại component khi options về
- [x] Đổi form sang endpoint `customer-info` của chính màn
- [x] Bổ sung nút "Tạo phiếu xử lý yêu cầu" ở footer màn chi tiết cho khớp màn danh sách
- [x] Cột File đính kèm trong bảng thiết bị

## Phase 4 — Đặt đúng phân hệ (19/08)

User chốt: menu **đã có sẵn** ở CSKH → Kiểm tra bảo hành sửa chữa → Yêu cầu kiểm tra sửa chữa - bảo hành,
không tạo mục mới; code phải nằm đúng module tương ứng.

- [x] Chuyển 11 file BE `Modules/CustomerCare` → **`Modules/Sale`** (đổi namespace)
- [x] Chuyển route sang `Modules/CustomerCare/Routes/api.php`, prefix **`/v1/customer-care/warranty-repair-requests`** (thêm `middleware auth:api` cho group Sale vốn còn trống)
- [x] Chuyển 9 file FE `pages/customer-care/...` → **`pages/customer-care/warranty-repair-requests/`**; đổi hết đường dẫn API/link/`localStorageKey`/`columnScreenKey`
- [x] Gỡ mục menu tự thêm ở `customer-care.js`; nối `link` vào mục CÓ SẴN trong `sale-hub.js`
- [x] Deep-link thông báo đổi sang `/customer-care/warranty-repair-requests/{id}`
- [x] Quyền đổi `type` 24 (CSKH) → **23 (Bán hàng)**, group `Yêu cầu sửa chữa - bảo hành` (sửa cả seeder lẫn 4 bản ghi trên DB)
- [x] Test lại sau khi chuyển: 6 endpoint `/v1/sale/...` = 200 · route cũ `/v1/customer-care/...` = 404 · FE 3 tab + chi tiết chạy, 0 lỗi console · bấm từ menu Bán dịch vụ điều hướng đúng

## Phase 5 — Chuẩn hoá V2Base (19/08)

Rà lại theo câu hỏi của user: màn có dùng đủ component `V2Base*` chưa. Kết quả: **CHƯA** — còn
14 chỗ HTML thô. Đã thay hết:

### FE
- [x] `<input class="form-control">` (Khách hàng, Người liên hệ, SĐT, Địa chỉ, Loại hình tổ chức) → `V2BaseInput` + `disabled`
- [x] `<label class="v2-label">…<span class="text-danger">*</span>` (7 chỗ) → `V2BaseLabel required` (tự render `*` + icon ⓘ tooltip từ từ điển)
- [x] `<button class="btn btn-outline-secondary">` (kính lúp chọn KH) → `V2BaseIconButton`
- [x] `<button class="btn btn-link">` (Nhập serial tạm) → `V2BaseButton quaternary size="xs"`
- [x] `<input type="file">` + `<label class="btn">` tự dựng → `V2BaseFile` (không bật `autoUpload` vì phải vào đúng thư mục `wr_requests` như ERP)
- [x] **Lỗi thật**: upload trả **401** — `$axios` không tự gắn `Authorization`; đã tự đính token

### Tài sản chung
- [x] Bổ sung mục **1b** vào `.claude/skills/form-validate/SKILL.md`: bảng tra HTML thô → `V2Base*`, lý do (mixin `v2ValidateMixin`, kiểu ô khoá dùng chung, `V2BaseLabel` tự gắn tooltip), cảnh báo `$axios` 401, và lệnh grep tự kiểm
- [x] Bổ sung gạch đầu dòng tương ứng vào `CLAUDE.md`

Kiểm chứng: grep element thô → **0 kết quả**; 9 file `.vue` compile sạch; test trình duyệt: ô khoá
ra đúng `#f1f5f9`/`#475569`/opacity 1/`not-allowed`, 5 nhãn có dấu `*`, upload file lên đúng
`wr_requests/` và gỡ file chạy đúng.

## Phase 6 — Bỏ tab ở màn danh sách (19/08)

User hỏi "sao phải tách thành các tab, ERP có làm vậy đâu". Kiểm tra lại ERP: **đúng, ERP không có
tab** — 1 màn danh sách duy nhất, menu trỏ `?type=all`; `waiting_handle` không có mục menu (chỉ là
link Quay lại từ form); `all.blade.php` là code chết. Tôi đã tự suy 3 tab từ tham số `type`.

- [x] FE: gỡ `V2BaseTabNavigation` + `presetTabs` + `handlePresetChange`; `filters.type` cố định `'all'`
- [x] BE: đổi mặc định `type` từ `index` → **`all`** (đúng thứ menu ERP trỏ tới); đổi tên hằng `TAB_*` → `SCOPE_*` kèm ghi chú "KHÔNG phải 3 tab"
- [x] Gỡ `canHandle()` + cờ `can_handle` ở `/options` (chỉ phục vụ tab, giờ thành code chết)
- [x] Kiểm chứng: không gửi `type` và `type=all` đều ra 5.365 phiếu; lọc *Người yêu cầu = tôi* ra đúng con số của tab "Phiếu của tôi" cũ; màn hết thanh tab, 0 lỗi console

## Phase 7 — Đối chiếu 1:1 với ERP + nhận `?type=` (19/08)

User hỏi "làm như hiện tại đã đạt như ERP chưa, truyền thêm param như ERP được không". Đối chiếu
`index.blade.php` của ERP → phát hiện **thiếu 2 ô lọc** và **FE bỏ qua query `?type=`**.

### BE
- [x] `/options` trả thêm `provinces` (45 tỉnh — ERP dùng `Province::getForSelect()`) và `scope` (`is_all_company`/`is_company`/`is_department` — ERP truyền `is_big_boss`/`is_boss`/`is_manager`)
- [x] `scopeFlags()` ở service, đọc chung `can()` với `applyScope`

### FE
- [x] Thêm ô lọc **Tỉnh/TP** (BE đã hỗ trợ `province_id` từ đầu, FE chưa khai)
- [x] Thêm khối **Công ty – Phòng ban** (`V2BaseCompanyDepartmentFilter`), chỉ hiện theo phạm vi quyền BE trả về — đúng `search_by_info` của ERP
- [x] **Nhận `?type=` từ URL** (`applyQueryType()`, whitelist `index`/`all`/`waiting_handle`), query THẮNG bộ lọc đã lưu trong localStorage; "Làm mới" giữ nguyên phạm vi đang xem

Kiểm chứng: `?type=waiting_handle` → API gửi đúng `type=waiting_handle`; 3 giá trị `type` +
`province_id` + `company_id` + `department_id` đều lọc ra số liệu đúng; bộ lọc hiện đủ 9 ô khớp ERP.

### Còn khác ERP (có chủ ý, đã ghi ở design.md)
- Ô "Mã phiếu" riêng của ERP → gộp vào **ô tìm nhanh** (BE lọc `code` OR `customer_name`)
- 4 cột ERP hiện sẵn (Địa chỉ sửa chữa, Ngày xử lý, Người xử lý) → **ẩn mặc định**, user tự bật ở Cấu hình cột (skill list-page mục 6)
- Thêm cột "Ngày gửi yêu cầu" và hành động "Từ chối" ngay trên dòng (ERP để nút này trong màn form)

## Phase 8 — Rà toàn bộ skill list-page (19/08)

User chỉ ra 4 chỗ chưa tuân thủ skill. Rà lại `.claude/skills/list-page/SKILL.md` từng mục:

### Đã sửa
- [x] **Mục 6 — bộ cột mặc định sai**: đang hiện 8 cột (có "Tên thiết bị liên quan"). Skill: STT · Mã · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động (+ Khách hàng là ngoại lệ). → còn **7 cột**, cột nghiệp vụ chuyển sang `isVisible: false`
- [x] **Mục 6 — thiếu Người tạo / Ngày tạo**: 2 cột này đang mang nhãn nghiệp vụ "Người yêu cầu"/"Ngày yêu cầu" → đổi về đúng nhãn chuẩn
- [x] **Mục 6 — thiếu hẳn Người cập nhật / Ngày cập nhật**: BE `ListResource` bổ sung `updater_name` + `updated_at` (eager load `updater.info`), FE khai 2 cột (ẩn mặc định)
- [x] **Mục 14b — Xuất file phải hỏi chọn trường**: đang tải thẳng bằng `WarrantyRepairRequestExport` cứng cột → **xoá class đó**, chuyển sang `ExportColumnRegistry` + `DynamicExport` dùng chung + `exportFieldsMixin` + `ExportFieldsModal`. Thêm khối `warranty_repair_requests` (13 cột) vào registry
- [x] **Ô tìm nhanh thiếu**: BE chỉ tìm mã phiếu + tên KH → thêm **tên người tạo** (dùng `EXISTS`, không join, theo cảnh báo của skill); placeholder cập nhật thành "Tìm theo mã phiếu, tên khách hàng, người tạo"
- [x] **Mục 3b — thiếu sắp xếp theo ĐỘ KHỚP**: bổ sung `applyRelevanceOrder()` (khuôn `CustomerService`), chấm điểm Mã phiếu + Tên KH, đủ 4 chốt bắt buộc (bỏ qua khi user bấm sort · chỉ chạy khi từ khoá ≥ 2 ký tự · `id DESC` cuối cùng · không chấm trường ở bảng khác)

Kiểm chứng: cột mặc định ra đúng 7; xuất file mở popup, request gửi `fields=` đúng thứ tự tick,
BE trả file đúng cột đã chọn; tìm "HYUNDAI" → dòng khớp sát lên đầu; bấm sort cột thì tôn trọng
sort; từ khoá 1 ký tự thì về sắp theo ngày tạo. 0 lỗi console.

### ⚠️ Nêu ra, chưa xử lý — xuất TOÀN BỘ chậm
`DynamicExport` dùng `FromView` (dựng HTML rồi convert). Với **5.365 dòng × 13 cột mất ~10,8s**
(chuẩn bị dữ liệu chỉ 1,8s — 9s còn lại là render view). Có lọc thì nhanh: 106 dòng = 0,7s,
61 dòng = 0,37s. Vượt ngưỡng 2s của CLAUDE.md → cần user chốt hướng (giới hạn số dòng / chuyển
`FromCollection` cho màn lớn / chạy queue).

## Phase 9 — Xuất file theo đúng khuôn màn Khách hàng (19/08)

User hỏi "xuất excel đã làm giống ở khách hàng chưa" — **chưa**: tôi để BE dựng file, màn Khách
hàng chia nhỏ API và dựng file ở FE. Đã làm giống + ghi thành nguyên tắc chung.

### BE
- [x] `GET /customer-care/warranty-repair-requests/export-rows` — trả `{ headings, widths, rows, total, page, limit }` theo trang, `rows` là mảng ô ĐÃ MAP SẴN; cột lấy qua `ExportColumnRegistry::resolve()` (dùng chung whitelist với popup chọn trường); trần `limit` 5.000
- [x] `exportRows()` ở service; giữ nguyên endpoint `/export` (BE dựng file) để đối chiếu

### FE
- [x] `utils/export/listExportFile.js` — bản DÙNG CHUNG rút từ `customerExportFile.js` (màn KH có thêm CSV/PDF + letterhead nên giữ riêng): tải tuần tự từng trang, trần vòng lặp, thoát khi trang rỗng, dựng Excel bằng ExcelJS (import động), báo tiến độ 2 giai đoạn
- [x] Màn dùng `exportListFile(...)` thay `downloadExcel`; thêm dòng tiến độ `.export-progress` + khoá nút khi đang xuất

### Tài sản chung
- [x] Thêm **mục 14c** vào `.claude/skills/list-page/SKILL.md`: ngưỡng 2s, bảng số đo thật, hạ tầng dùng, 6 chốt bắt buộc (tuần tự · trần vòng lặp · xoá page/limit · 0 dòng không tạo file · giữ endpoint cũ · dòng tiến độ) và điểm yếu cố hữu
- [x] Thêm gạch đầu dòng tương ứng vào mục Hiệu năng của `CLAUDE.md`

Kiểm chứng trên trình duyệt: 3 lượt gọi `export-rows` (page 1-3 × 2.000 dòng, mỗi lượt ~1,2s) →
**~4s** thay vì 10,8s; file tải về 5.365 dòng × 14 cột, có tiêu đề, header nền xám, đóng băng dòng
tên cột (A3), tự lọc (A2:N2); toast "Xuất Excel thành công".

## Phase 10 — Sửa màn in bị hở đầu trang (19/08)

User báo trang in `/customer-care/warranty-repair-requests/print` hở 1 dải phía trên. Đo trên trình duyệt:

| Nguồn | Cao |
| --- | --- |
| `.navbar-custom` (topbar, chỉ hiện tên user trên nền gradient xanh) | 60px |
| `.content-page { padding-top: 70px }` | 70px |
| `.container.mt-3` | 16px |
| **Tổng** | **~136px** đẩy tờ giấy xuống |

Nguyên nhân: tôi copy khuôn từ `pages/finance/product-import-requests/_id/print.vue` — màn đó khai
`layout: 'default-sidebar'`, tức bọc trang in trong lớp vỏ ứng dụng.

- [x] Thêm `layouts/print.vue` — không topbar/sidebar, nền trắng, vẫn `@import` SCSS chung để `V2Base*` hiển thị đúng
- [x] 2 màn in của feature đổi sang `layout: 'print'`
- [x] Thêm **mục 2b** vào `.claude/skills/print-page/SKILL.md`: bắt buộc `layout: 'print'`, bảng đo chiều cao thừa, cảnh báo đừng bù `margin-top` âm, và 2 lệnh console tự kiểm

Bỏ topbar xong VẪN còn 16px xám ở đầu — nguyên nhân thứ 2: **margin collapsing**. `margin-top`
của `.container.mt-3` tràn ra ngoài, đẩy cả layout xuống và để lộ nền `body` (#f5f6f8).
- [x] `.print-layout { display: flow-root }` — tạo BFC, margin con nằm gọn trong vùng trắng
      (KHÔNG dùng `overflow: auto`: trang in rất dài, sẽ đẻ thanh cuộn lồng nhau)
- [x] `body:has(.print-layout) { background: #fff }` — chặn nền xám lộ khi cuộn quá đáy / trang ngắn

Kiểm chứng: cả 2 màn in (1 phiếu + danh sách) — `.navbar-custom` không còn; `.print-layout` bắt đầu
ở **y = 0**; lấy mẫu `elementFromPoint` tại y = 0/5/10/15 đều ra `.print-layout` nền
`rgb(255,255,255)`; `body` cũng trắng; 0 lỗi console.

⚠️ **Không sửa đại trà**: rà thấy ~24 màn `print.vue` khác trong repo cũng khai `default-sidebar`
hoặc không khai layout (rơi về `default`) → đều hở như vậy. Đã ghi vào skill để team sửa dần khi
đụng vào từng màn, KHÔNG tự sửa hàng loạt màn của người khác.

## Phase 11 — Khối ký tên bị dồn về trái (19/08)

User báo `NGƯỜI YÊU CẦU / TRƯỞNG PHÒNG YÊU CẦU / PHÒNG NHẬN YÊU CẦU / BAN GIÁM ĐỐC` không ngang
hàng. Đo bằng `getBoundingClientRect` (preview) + iframe khổ in (skill print-page mục 7):

| Bảng | Rộng (preview) |
| --- | --- |
| 4 bảng thân phiếu | 1110px |
| **bảng ký** | **827px** — hụt 283px, co về trái |

Nguyên nhân nằm trong MẪU IN của ERP, không phải code màn:
1. `<table class="block no-border" style="width:827px">` — khổ giấy cứng của ERP.
2. Snippet chuẩn chỉ ép `table:not(.no-border) { width:100% }`, mà bảng ký CÓ `.no-border` nên bị loại trừ.
3. 4 ô `width:20%` = 80%, thiếu 20%.

- [x] Ép `#content table.block { width:100%; table-layout:fixed }` + `td { width:auto }` — khai ở CẢ `options.styles` (cửa sổ in) lẫn `<style scoped>` (bản xem trước)
- [x] Áp cho cả 2 màn in cho đồng nhất (mẫu danh sách đang `width:100%` nên chưa lệch, nhưng phòng khi mẫu bị sửa)
- [x] Thêm **mục 3b** + 1 dòng vào bảng "Checklist debug nhanh" của `.claude/skills/print-page/SKILL.md`

⚠️ Bẫy khi sửa: comment CSS đặt trong template literal của `options.styles` **không được chứa dấu
backtick** — đứt chuỗi, cả file không compile.

Kiểm chứng — preview: bảng ký 1110px = thân phiếu, 4 ô chia đều 278px, cùng `top`.
Khổ in (iframe 190mm): bảng ký 683px = khung in = thân phiếu, 4 ô đều 171px, tràn mép phải = 0.

## Phase 12 — Cấp quyền tk namdangit + test toàn diện (19/08)

Cấp đủ 4 quyền cho `namdangit@gmail.com` (employee id 13, role `Super admin` id 18 +
`Quyền giám đốc kinh doanh`) rồi test lại toàn bộ. **Tìm ra 3 lỗi thật:**

### Lỗi 1 — `hasRole('Super Admin')` không bao giờ khớp
DB gộp có 2 role gần giống: id 18 `Super admin` (guard `api`, HRM) và id 100002 `Super Admin`
(guard `web`, ERP). Tôi so theo TÊN chữ hoa → trượt **im lặng**, nhánh bỏ qua điều kiện phòng ban
không bao giờ chạy.
- [x] Đổi sang dò theo **role id 18** (`WarrantyRepairPermission::SUPER_ADMIN_ROLE_ID`), đúng khuôn `Modules/Finance/Entities/ProductTransferRequest`

### Lỗi 2 — `canTransferDepartmentReception()` lệch ERP
Tôi thêm nhánh Super admin vào đây, nhưng ERP **không có** → Super admin chuyển được phiếu của
phòng khác. Test thật đã chuyển nhầm 1 phiếu sang phòng 51.
- [x] Bỏ nhánh Super admin; chỉ `canHandleRequest()` mới có (đúng ERP)

### Lỗi 3 — thiếu validate serial của ERP
ERP: dòng thiết bị KHÔNG chọn `serial_id` thì `serial` **bắt buộc**. FormRequest của tôi để
`nullable` cả 2 → gửi phiếu không serial vẫn lọt.
- [x] Thêm rule theo từng dòng (`productsWithoutSerialId()`), chỉ áp khi GỬI (lưu nháp vẫn để trống được)

### Đã test (tk namdangit, 15 nhóm kịch bản)
BE: 3 phạm vi `type` · options (9 trạng thái / 87 phòng / 45 tỉnh / scope) · 10 bộ lọc · 3 kiểu
sắp xếp · lưu nháp · gửi duyệt thiếu trường (422, 6 lỗi) · gửi duyệt đủ · sửa phiếu đã gửi (423) ·
xoá phiếu đã gửi (chặn) · chuyển phòng trùng (chặn) / phòng khác (OK) / trái phòng (chặn) · từ chối
thiếu lý do (422) / có lý do (về Đang tạo) · in 1 phiếu + in danh sách (hết placeholder) ·
export-rows (0,27s, lọc cột OK) · customer-info · chi tiết · xoá phiếu nháp.

FE: đăng nhập đúng DNS Admin · 7 cột + 9 ô lọc · hành động theo quyền · tạo mới đầy đủ qua giao
diện (popup KH → chọn thiết bị → chọn serial → gửi duyệt) → ra phiếu `Chờ xử lý` · lỗi serial hiện
đúng trong dòng thiết bị.

Dữ liệu test đã dọn sạch: 5.625 phiếu = đúng số gốc, 0 phiếu test còn sót.

## Phase 13 — Số hành động lệch ERP (19/08)

User so cùng 1 bản ghi giữa ERP và HRM thấy số hành động khác nhau. Đối chiếu
`WarrantyRepairRequestsController::searchData` của ERP:

- [x] **Lỗi gate**: ERP gate nút "Chuyển phòng tiếp nhận" bằng `canHandelRequest()` (y hệt nút "Tạo phiếu xử lý" — 2 khối `if` giống nhau), KHÔNG phải `canTransferDepartmentReception()`. Hàm đó trong ERP là **CODE CHẾT: 0 nơi gọi** (đã grep toàn `app/` + `resources/`). Guard endpoint transfer và footer màn form cũng dùng `canHandelRequest()`.
  → `canTransferDepartmentReception()` / `canReject()` của HRM đổi thành **alias** của `canHandleRequest()`; truyền sẵn cờ `has_handle_request` để không phát sinh query.
- [x] **Vị trí nút Từ chối** — ERP đặt ở footer màn form, danh sách chỉ 5 nút; skill HRM đòi 2 màn khớp nhau. **User chốt: giữ ở CẢ 2 nơi** (theo skill). Ghi vào design.md mục "Quyết định đã chốt".

Kiểm chứng — cùng phiếu `TPE.YCSCBH.26.005682` (Chờ xử lý, gửi về phòng của tài khoản):
- API: 3 cờ `is_can_handle_request` / `is_can_transfer_department` / `is_can_reject` giờ **luôn bằng nhau** (kiểm 8 dòng, 0 dòng lệch).
- Danh sách: Tạo phiếu xử lý · Chuyển phòng · Từ chối · In = **4 hành động**.
- Chi tiết: Tạo phiếu xử lý · Chuyển phòng · Từ chối · In = **4 hành động** (+ Quay lại do V2Footer tự render).

## Phase 14 — Khối nhóm dùng chung component (19/08)

User yêu cầu 3 khối ("Thông tin khách hàng", "I – Danh sách thiết bị…", "II – Danh mục trang thiết
bị…") dùng chung component như mục **"Địa chỉ giao hàng"** của `/assign/customers/{id}`.

Rà ra: khuôn đó **chưa phải component** — markup `card > card-header.section-header > h6` cùng khối
SCSS đang bị **copy-paste ở 35 file**.

- [x] Tạo `components/V2BaseFormSection.vue` — prop `title`, slot `#title` (tiêu đề cần markup riêng), slot `#actions` (nút/ô tìm bên phải), slot mặc định cho nội dung; bê nguyên CSS `.card-header.section-header` kèm ghi chú vì sao
- [x] Áp cho cả 3 khối của màn; khối II giữ nguyên ô tìm + 2 nút qua `#actions`
- [x] Thêm **mục 1c** vào `.claude/skills/form-validate/SKILL.md` + 1 gạch đầu dòng vào `CLAUDE.md`
- [x] KHÔNG sửa 35 màn cũ (quy tắc team) — ghi rõ "sửa dần khi có dịp đụng vào"

- [x] **Bảng trong form thừa khoảng trắng**: `assets/scss/default.scss` ép `.table-responsive { min-height: 50vh }` cho MỌI bảng → phiếu 1 thiết bị bảng chỉ 118px mà khung bị kéo lên 429px, thừa **311px trống có viền**. Ghi đè cục bộ `.v2-form-table-wrap { min-height: 0 }` (KHÔNG sửa rule global). Khối I: **517px → 213px**; khung vẫn nở đúng khi bảng dài (17 dòng → 1183px, không cắt, không cuộn).
- [x] **Padding dọc ô bảng**: Bootstrap để `.table td/th { padding: .75rem }` = 12,8px trên/dưới → dòng cao 81px dù chữ 1-2 dòng. Bóp còn **4px** (giữ ngang 8px). Khối I: 213px → **187px**, dòng **81px → 64px**; chữ không cắt, ô nhập trong bảng không méo (input 32px / textarea 53px giữ nguyên). Đã ghi cái bẫy này vào skill `form-validate` mục 1c.

Kiểm chứng: đo `getComputedStyle` khối của màn tôi vs mục "Địa chỉ giao hàng" màn khách hàng —
**trùng từng thuộc tính**: nền `rgb(255,255,255)` · viền dưới `rgb(229,231,235)` · padding-left
`10px` · h6 `14px` / `rgb(31,41,55)` / `700`. Màn chi tiết 2 khối, màn tạo mới 3 khối, 0 lỗi console.

## Checkpoint

### Phase 3 — Sửa sau khi test thật (18/08)

### BE
- [x] **Quyền chuyển hẳn sang HRM** (user chốt): tạo 4 quyền guard `api` id 1177–1180, không dùng bản quyền ERP cùng tên
- [x] Sửa lỗi kiểm quyền: `auth()->user()` là `TpEmployee` **không có trait `HasRoles`** → `->can()` luôn false; thay bằng `Support/WarrantyRepairPermission` (nạp qua `Modules\Timesheet\Entities\Employee`)
- [x] `GET /options` trả thêm cờ `can_handle` để FE mở tab "Chờ xử lý"
- [x] Thêm `GET /customer-info/{customerId}` — người liên hệ / nơi giao nhận / loại hình tổ chức, thay cho `assign/customers/{id}` (endpoint đó gate bằng quyền ERP → 403)
- [x] `POST /upload-attachment` (S3, thư mục `wr_requests` như ERP)
- [x] In danh sách: "Thời gian: Tất cả" khi không lọc ngày (ERP in ra dấu `-` trơ)

### FE
- [x] Sửa lỗi **select2 mất liên kết khi options nạp bất đồng bộ** (Người liên hệ / Địa chỉ sửa chữa / Serial) — thêm `:key` để dựng lại component khi options về
- [x] Đổi form sang endpoint `customer-info` của chính màn
- [x] Bổ sung nút "Tạo phiếu xử lý yêu cầu" ở footer màn chi tiết cho khớp màn danh sách
- [x] Cột File đính kèm trong bảng thiết bị

## Phase 4 — Đặt đúng phân hệ (19/08)

User chốt: menu **đã có sẵn** ở CSKH → Kiểm tra bảo hành sửa chữa → Yêu cầu kiểm tra sửa chữa - bảo hành,
không tạo mục mới; code phải nằm đúng module tương ứng.

- [x] Chuyển 11 file BE `Modules/CustomerCare` → **`Modules/Sale`** (đổi namespace)
- [x] Chuyển route sang `Modules/CustomerCare/Routes/api.php`, prefix **`/v1/customer-care/warranty-repair-requests`** (thêm `middleware auth:api` cho group Sale vốn còn trống)
- [x] Chuyển 9 file FE `pages/customer-care/...` → **`pages/customer-care/warranty-repair-requests/`**; đổi hết đường dẫn API/link/`localStorageKey`/`columnScreenKey`
- [x] Gỡ mục menu tự thêm ở `customer-care.js`; nối `link` vào mục CÓ SẴN trong `sale-hub.js`
- [x] Deep-link thông báo đổi sang `/customer-care/warranty-repair-requests/{id}`
- [x] Quyền đổi `type` 24 (CSKH) → **23 (Bán hàng)**, group `Yêu cầu sửa chữa - bảo hành` (sửa cả seeder lẫn 4 bản ghi trên DB)
- [x] Test lại sau khi chuyển: 6 endpoint `/v1/sale/...` = 200 · route cũ `/v1/customer-care/...` = 404 · FE 3 tab + chi tiết chạy, 0 lỗi console · bấm từ menu Bán dịch vụ điều hướng đúng

## Phase 5 — Chuẩn hoá V2Base (19/08)

Rà lại theo câu hỏi của user: màn có dùng đủ component `V2Base*` chưa. Kết quả: **CHƯA** — còn
14 chỗ HTML thô. Đã thay hết:

### FE
- [x] `<input class="form-control">` (Khách hàng, Người liên hệ, SĐT, Địa chỉ, Loại hình tổ chức) → `V2BaseInput` + `disabled`
- [x] `<label class="v2-label">…<span class="text-danger">*</span>` (7 chỗ) → `V2BaseLabel required` (tự render `*` + icon ⓘ tooltip từ từ điển)
- [x] `<button class="btn btn-outline-secondary">` (kính lúp chọn KH) → `V2BaseIconButton`
- [x] `<button class="btn btn-link">` (Nhập serial tạm) → `V2BaseButton quaternary size="xs"`
- [x] `<input type="file">` + `<label class="btn">` tự dựng → `V2BaseFile` (không bật `autoUpload` vì phải vào đúng thư mục `wr_requests` như ERP)
- [x] **Lỗi thật**: upload trả **401** — `$axios` không tự gắn `Authorization`; đã tự đính token

### Tài sản chung
- [x] Bổ sung mục **1b** vào `.claude/skills/form-validate/SKILL.md`: bảng tra HTML thô → `V2Base*`, lý do (mixin `v2ValidateMixin`, kiểu ô khoá dùng chung, `V2BaseLabel` tự gắn tooltip), cảnh báo `$axios` 401, và lệnh grep tự kiểm
- [x] Bổ sung gạch đầu dòng tương ứng vào `CLAUDE.md`

Kiểm chứng: grep element thô → **0 kết quả**; 9 file `.vue` compile sạch; test trình duyệt: ô khoá
ra đúng `#f1f5f9`/`#475569`/opacity 1/`not-allowed`, 5 nhãn có dấu `*`, upload file lên đúng
`wr_requests/` và gỡ file chạy đúng.

## Phase 6 — Bỏ tab ở màn danh sách (19/08)

User hỏi "sao phải tách thành các tab, ERP có làm vậy đâu". Kiểm tra lại ERP: **đúng, ERP không có
tab** — 1 màn danh sách duy nhất, menu trỏ `?type=all`; `waiting_handle` không có mục menu (chỉ là
link Quay lại từ form); `all.blade.php` là code chết. Tôi đã tự suy 3 tab từ tham số `type`.

- [x] FE: gỡ `V2BaseTabNavigation` + `presetTabs` + `handlePresetChange`; `filters.type` cố định `'all'`
- [x] BE: đổi mặc định `type` từ `index` → **`all`** (đúng thứ menu ERP trỏ tới); đổi tên hằng `TAB_*` → `SCOPE_*` kèm ghi chú "KHÔNG phải 3 tab"
- [x] Gỡ `canHandle()` + cờ `can_handle` ở `/options` (chỉ phục vụ tab, giờ thành code chết)
- [x] Kiểm chứng: không gửi `type` và `type=all` đều ra 5.365 phiếu; lọc *Người yêu cầu = tôi* ra đúng con số của tab "Phiếu của tôi" cũ; màn hết thanh tab, 0 lỗi console

## Phase 7 — Đối chiếu 1:1 với ERP + nhận `?type=` (19/08)

User hỏi "làm như hiện tại đã đạt như ERP chưa, truyền thêm param như ERP được không". Đối chiếu
`index.blade.php` của ERP → phát hiện **thiếu 2 ô lọc** và **FE bỏ qua query `?type=`**.

### BE
- [x] `/options` trả thêm `provinces` (45 tỉnh — ERP dùng `Province::getForSelect()`) và `scope` (`is_all_company`/`is_company`/`is_department` — ERP truyền `is_big_boss`/`is_boss`/`is_manager`)
- [x] `scopeFlags()` ở service, đọc chung `can()` với `applyScope`

### FE
- [x] Thêm ô lọc **Tỉnh/TP** (BE đã hỗ trợ `province_id` từ đầu, FE chưa khai)
- [x] Thêm khối **Công ty – Phòng ban** (`V2BaseCompanyDepartmentFilter`), chỉ hiện theo phạm vi quyền BE trả về — đúng `search_by_info` của ERP
- [x] **Nhận `?type=` từ URL** (`applyQueryType()`, whitelist `index`/`all`/`waiting_handle`), query THẮNG bộ lọc đã lưu trong localStorage; "Làm mới" giữ nguyên phạm vi đang xem

Kiểm chứng: `?type=waiting_handle` → API gửi đúng `type=waiting_handle`; 3 giá trị `type` +
`province_id` + `company_id` + `department_id` đều lọc ra số liệu đúng; bộ lọc hiện đủ 9 ô khớp ERP.

### Còn khác ERP (có chủ ý, đã ghi ở design.md)
- Ô "Mã phiếu" riêng của ERP → gộp vào **ô tìm nhanh** (BE lọc `code` OR `customer_name`)
- 4 cột ERP hiện sẵn (Địa chỉ sửa chữa, Ngày xử lý, Người xử lý) → **ẩn mặc định**, user tự bật ở Cấu hình cột (skill list-page mục 6)
- Thêm cột "Ngày gửi yêu cầu" và hành động "Từ chối" ngay trên dòng (ERP để nút này trong màn form)

## Phase 8 — Rà toàn bộ skill list-page (19/08)

User chỉ ra 4 chỗ chưa tuân thủ skill. Rà lại `.claude/skills/list-page/SKILL.md` từng mục:

### Đã sửa
- [x] **Mục 6 — bộ cột mặc định sai**: đang hiện 8 cột (có "Tên thiết bị liên quan"). Skill: STT · Mã · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động (+ Khách hàng là ngoại lệ). → còn **7 cột**, cột nghiệp vụ chuyển sang `isVisible: false`
- [x] **Mục 6 — thiếu Người tạo / Ngày tạo**: 2 cột này đang mang nhãn nghiệp vụ "Người yêu cầu"/"Ngày yêu cầu" → đổi về đúng nhãn chuẩn
- [x] **Mục 6 — thiếu hẳn Người cập nhật / Ngày cập nhật**: BE `ListResource` bổ sung `updater_name` + `updated_at` (eager load `updater.info`), FE khai 2 cột (ẩn mặc định)
- [x] **Mục 14b — Xuất file phải hỏi chọn trường**: đang tải thẳng bằng `WarrantyRepairRequestExport` cứng cột → **xoá class đó**, chuyển sang `ExportColumnRegistry` + `DynamicExport` dùng chung + `exportFieldsMixin` + `ExportFieldsModal`. Thêm khối `warranty_repair_requests` (13 cột) vào registry
- [x] **Ô tìm nhanh thiếu**: BE chỉ tìm mã phiếu + tên KH → thêm **tên người tạo** (dùng `EXISTS`, không join, theo cảnh báo của skill); placeholder cập nhật thành "Tìm theo mã phiếu, tên khách hàng, người tạo"
- [x] **Mục 3b — thiếu sắp xếp theo ĐỘ KHỚP**: bổ sung `applyRelevanceOrder()` (khuôn `CustomerService`), chấm điểm Mã phiếu + Tên KH, đủ 4 chốt bắt buộc (bỏ qua khi user bấm sort · chỉ chạy khi từ khoá ≥ 2 ký tự · `id DESC` cuối cùng · không chấm trường ở bảng khác)

Kiểm chứng: cột mặc định ra đúng 7; xuất file mở popup, request gửi `fields=` đúng thứ tự tick,
BE trả file đúng cột đã chọn; tìm "HYUNDAI" → dòng khớp sát lên đầu; bấm sort cột thì tôn trọng
sort; từ khoá 1 ký tự thì về sắp theo ngày tạo. 0 lỗi console.

### ⚠️ Nêu ra, chưa xử lý — xuất TOÀN BỘ chậm
`DynamicExport` dùng `FromView` (dựng HTML rồi convert). Với **5.365 dòng × 13 cột mất ~10,8s**
(chuẩn bị dữ liệu chỉ 1,8s — 9s còn lại là render view). Có lọc thì nhanh: 106 dòng = 0,7s,
61 dòng = 0,37s. Vượt ngưỡng 2s của CLAUDE.md → cần user chốt hướng (giới hạn số dòng / chuyển
`FromCollection` cho màn lớn / chạy queue).

## Phase 9 — Xuất file theo đúng khuôn màn Khách hàng (19/08)

User hỏi "xuất excel đã làm giống ở khách hàng chưa" — **chưa**: tôi để BE dựng file, màn Khách
hàng chia nhỏ API và dựng file ở FE. Đã làm giống + ghi thành nguyên tắc chung.

### BE
- [x] `GET /customer-care/warranty-repair-requests/export-rows` — trả `{ headings, widths, rows, total, page, limit }` theo trang, `rows` là mảng ô ĐÃ MAP SẴN; cột lấy qua `ExportColumnRegistry::resolve()` (dùng chung whitelist với popup chọn trường); trần `limit` 5.000
- [x] `exportRows()` ở service; giữ nguyên endpoint `/export` (BE dựng file) để đối chiếu

### FE
- [x] `utils/export/listExportFile.js` — bản DÙNG CHUNG rút từ `customerExportFile.js` (màn KH có thêm CSV/PDF + letterhead nên giữ riêng): tải tuần tự từng trang, trần vòng lặp, thoát khi trang rỗng, dựng Excel bằng ExcelJS (import động), báo tiến độ 2 giai đoạn
- [x] Màn dùng `exportListFile(...)` thay `downloadExcel`; thêm dòng tiến độ `.export-progress` + khoá nút khi đang xuất

### Tài sản chung
- [x] Thêm **mục 14c** vào `.claude/skills/list-page/SKILL.md`: ngưỡng 2s, bảng số đo thật, hạ tầng dùng, 6 chốt bắt buộc (tuần tự · trần vòng lặp · xoá page/limit · 0 dòng không tạo file · giữ endpoint cũ · dòng tiến độ) và điểm yếu cố hữu
- [x] Thêm gạch đầu dòng tương ứng vào mục Hiệu năng của `CLAUDE.md`

Kiểm chứng trên trình duyệt: 3 lượt gọi `export-rows` (page 1-3 × 2.000 dòng, mỗi lượt ~1,2s) →
**~4s** thay vì 10,8s; file tải về 5.365 dòng × 14 cột, có tiêu đề, header nền xám, đóng băng dòng
tên cột (A3), tự lọc (A2:N2); toast "Xuất Excel thành công".

## Phase 10 — Sửa màn in bị hở đầu trang (19/08)

User báo trang in `/customer-care/warranty-repair-requests/print` hở 1 dải phía trên. Đo trên trình duyệt:

| Nguồn | Cao |
| --- | --- |
| `.navbar-custom` (topbar, chỉ hiện tên user trên nền gradient xanh) | 60px |
| `.content-page { padding-top: 70px }` | 70px |
| `.container.mt-3` | 16px |
| **Tổng** | **~136px** đẩy tờ giấy xuống |

Nguyên nhân: tôi copy khuôn từ `pages/finance/product-import-requests/_id/print.vue` — màn đó khai
`layout: 'default-sidebar'`, tức bọc trang in trong lớp vỏ ứng dụng.

- [x] Thêm `layouts/print.vue` — không topbar/sidebar, nền trắng, vẫn `@import` SCSS chung để `V2Base*` hiển thị đúng
- [x] 2 màn in của feature đổi sang `layout: 'print'`
- [x] Thêm **mục 2b** vào `.claude/skills/print-page/SKILL.md`: bắt buộc `layout: 'print'`, bảng đo chiều cao thừa, cảnh báo đừng bù `margin-top` âm, và 2 lệnh console tự kiểm

Bỏ topbar xong VẪN còn 16px xám ở đầu — nguyên nhân thứ 2: **margin collapsing**. `margin-top`
của `.container.mt-3` tràn ra ngoài, đẩy cả layout xuống và để lộ nền `body` (#f5f6f8).
- [x] `.print-layout { display: flow-root }` — tạo BFC, margin con nằm gọn trong vùng trắng
      (KHÔNG dùng `overflow: auto`: trang in rất dài, sẽ đẻ thanh cuộn lồng nhau)
- [x] `body:has(.print-layout) { background: #fff }` — chặn nền xám lộ khi cuộn quá đáy / trang ngắn

Kiểm chứng: cả 2 màn in (1 phiếu + danh sách) — `.navbar-custom` không còn; `.print-layout` bắt đầu
ở **y = 0**; lấy mẫu `elementFromPoint` tại y = 0/5/10/15 đều ra `.print-layout` nền
`rgb(255,255,255)`; `body` cũng trắng; 0 lỗi console.

⚠️ **Không sửa đại trà**: rà thấy ~24 màn `print.vue` khác trong repo cũng khai `default-sidebar`
hoặc không khai layout (rơi về `default`) → đều hở như vậy. Đã ghi vào skill để team sửa dần khi
đụng vào từng màn, KHÔNG tự sửa hàng loạt màn của người khác.

## Phase 11 — Khối ký tên bị dồn về trái (19/08)

User báo `NGƯỜI YÊU CẦU / TRƯỞNG PHÒNG YÊU CẦU / PHÒNG NHẬN YÊU CẦU / BAN GIÁM ĐỐC` không ngang
hàng. Đo bằng `getBoundingClientRect` (preview) + iframe khổ in (skill print-page mục 7):

| Bảng | Rộng (preview) |
| --- | --- |
| 4 bảng thân phiếu | 1110px |
| **bảng ký** | **827px** — hụt 283px, co về trái |

Nguyên nhân nằm trong MẪU IN của ERP, không phải code màn:
1. `<table class="block no-border" style="width:827px">` — khổ giấy cứng của ERP.
2. Snippet chuẩn chỉ ép `table:not(.no-border) { width:100% }`, mà bảng ký CÓ `.no-border` nên bị loại trừ.
3. 4 ô `width:20%` = 80%, thiếu 20%.

- [x] Ép `#content table.block { width:100%; table-layout:fixed }` + `td { width:auto }` — khai ở CẢ `options.styles` (cửa sổ in) lẫn `<style scoped>` (bản xem trước)
- [x] Áp cho cả 2 màn in cho đồng nhất (mẫu danh sách đang `width:100%` nên chưa lệch, nhưng phòng khi mẫu bị sửa)
- [x] Thêm **mục 3b** + 1 dòng vào bảng "Checklist debug nhanh" của `.claude/skills/print-page/SKILL.md`

⚠️ Bẫy khi sửa: comment CSS đặt trong template literal của `options.styles` **không được chứa dấu
backtick** — đứt chuỗi, cả file không compile.

Kiểm chứng — preview: bảng ký 1110px = thân phiếu, 4 ô chia đều 278px, cùng `top`.
Khổ in (iframe 190mm): bảng ký 683px = khung in = thân phiếu, 4 ô đều 171px, tràn mép phải = 0.

## Phase 12 — Cấp quyền tk namdangit + test toàn diện (19/08)

Cấp đủ 4 quyền cho `namdangit@gmail.com` (employee id 13, role `Super admin` id 18 +
`Quyền giám đốc kinh doanh`) rồi test lại toàn bộ. **Tìm ra 3 lỗi thật:**

### Lỗi 1 — `hasRole('Super Admin')` không bao giờ khớp
DB gộp có 2 role gần giống: id 18 `Super admin` (guard `api`, HRM) và id 100002 `Super Admin`
(guard `web`, ERP). Tôi so theo TÊN chữ hoa → trượt **im lặng**, nhánh bỏ qua điều kiện phòng ban
không bao giờ chạy.
- [x] Đổi sang dò theo **role id 18** (`WarrantyRepairPermission::SUPER_ADMIN_ROLE_ID`), đúng khuôn `Modules/Finance/Entities/ProductTransferRequest`

### Lỗi 2 — `canTransferDepartmentReception()` lệch ERP
Tôi thêm nhánh Super admin vào đây, nhưng ERP **không có** → Super admin chuyển được phiếu của
phòng khác. Test thật đã chuyển nhầm 1 phiếu sang phòng 51.
- [x] Bỏ nhánh Super admin; chỉ `canHandleRequest()` mới có (đúng ERP)

### Lỗi 3 — thiếu validate serial của ERP
ERP: dòng thiết bị KHÔNG chọn `serial_id` thì `serial` **bắt buộc**. FormRequest của tôi để
`nullable` cả 2 → gửi phiếu không serial vẫn lọt.
- [x] Thêm rule theo từng dòng (`productsWithoutSerialId()`), chỉ áp khi GỬI (lưu nháp vẫn để trống được)

### Đã test (tk namdangit, 15 nhóm kịch bản)
BE: 3 phạm vi `type` · options (9 trạng thái / 87 phòng / 45 tỉnh / scope) · 10 bộ lọc · 3 kiểu
sắp xếp · lưu nháp · gửi duyệt thiếu trường (422, 6 lỗi) · gửi duyệt đủ · sửa phiếu đã gửi (423) ·
xoá phiếu đã gửi (chặn) · chuyển phòng trùng (chặn) / phòng khác (OK) / trái phòng (chặn) · từ chối
thiếu lý do (422) / có lý do (về Đang tạo) · in 1 phiếu + in danh sách (hết placeholder) ·
export-rows (0,27s, lọc cột OK) · customer-info · chi tiết · xoá phiếu nháp.

FE: đăng nhập đúng DNS Admin · 7 cột + 9 ô lọc · hành động theo quyền · tạo mới đầy đủ qua giao
diện (popup KH → chọn thiết bị → chọn serial → gửi duyệt) → ra phiếu `Chờ xử lý` · lỗi serial hiện
đúng trong dòng thiết bị.

Dữ liệu test đã dọn sạch: 5.625 phiếu = đúng số gốc, 0 phiếu test còn sót.

## Phase 13 — Số hành động lệch ERP (19/08)

User so cùng 1 bản ghi giữa ERP và HRM thấy số hành động khác nhau. Đối chiếu
`WarrantyRepairRequestsController::searchData` của ERP:

- [x] **Lỗi gate**: ERP gate nút "Chuyển phòng tiếp nhận" bằng `canHandelRequest()` (y hệt nút "Tạo phiếu xử lý" — 2 khối `if` giống nhau), KHÔNG phải `canTransferDepartmentReception()`. Hàm đó trong ERP là **CODE CHẾT: 0 nơi gọi** (đã grep toàn `app/` + `resources/`). Guard endpoint transfer và footer màn form cũng dùng `canHandelRequest()`.
  → `canTransferDepartmentReception()` / `canReject()` của HRM đổi thành **alias** của `canHandleRequest()`; truyền sẵn cờ `has_handle_request` để không phát sinh query.
- [x] **Vị trí nút Từ chối** — ERP đặt ở footer màn form, danh sách chỉ 5 nút; skill HRM đòi 2 màn khớp nhau. **User chốt: giữ ở CẢ 2 nơi** (theo skill). Ghi vào design.md mục "Quyết định đã chốt".

Kiểm chứng — cùng phiếu `TPE.YCSCBH.26.005682` (Chờ xử lý, gửi về phòng của tài khoản):
- API: 3 cờ `is_can_handle_request` / `is_can_transfer_department` / `is_can_reject` giờ **luôn bằng nhau** (kiểm 8 dòng, 0 dòng lệch).
- Danh sách: Tạo phiếu xử lý · Chuyển phòng · Từ chối · In = **4 hành động**.
- Chi tiết: Tạo phiếu xử lý · Chuyển phòng · Từ chối · In = **4 hành động** (+ Quay lại do V2Footer tự render).

## Phase 14 — Khối nhóm dùng chung component (19/08)

User yêu cầu 3 khối ("Thông tin khách hàng", "I – Danh sách thiết bị…", "II – Danh mục trang thiết
bị…") dùng chung component như mục **"Địa chỉ giao hàng"** của `/assign/customers/{id}`.

Rà ra: khuôn đó **chưa phải component** — markup `card > card-header.section-header > h6` cùng khối
SCSS đang bị **copy-paste ở 35 file**.

- [x] Tạo `components/V2BaseFormSection.vue` — prop `title`, slot `#title` (tiêu đề cần markup riêng), slot `#actions` (nút/ô tìm bên phải), slot mặc định cho nội dung; bê nguyên CSS `.card-header.section-header` kèm ghi chú vì sao
- [x] Áp cho cả 3 khối của màn; khối II giữ nguyên ô tìm + 2 nút qua `#actions`
- [x] Thêm **mục 1c** vào `.claude/skills/form-validate/SKILL.md` + 1 gạch đầu dòng vào `CLAUDE.md`
- [x] KHÔNG sửa 35 màn cũ (quy tắc team) — ghi rõ "sửa dần khi có dịp đụng vào"

- [x] **Bảng trong form thừa khoảng trắng**: `assets/scss/default.scss` ép `.table-responsive { min-height: 50vh }` cho MỌI bảng → phiếu 1 thiết bị bảng chỉ 118px mà khung bị kéo lên 429px, thừa **311px trống có viền**. Ghi đè cục bộ `.v2-form-table-wrap { min-height: 0 }` (KHÔNG sửa rule global). Khối I: **517px → 213px**; khung vẫn nở đúng khi bảng dài (17 dòng → 1183px, không cắt, không cuộn).
- [x] **Padding dọc ô bảng**: Bootstrap để `.table td/th { padding: .75rem }` = 12,8px trên/dưới → dòng cao 81px dù chữ 1-2 dòng. Bóp còn **4px** (giữ ngang 8px). Khối I: 213px → **187px**, dòng **81px → 64px**; chữ không cắt, ô nhập trong bảng không méo (input 32px / textarea 53px giữ nguyên). Đã ghi cái bẫy này vào skill `form-validate` mục 1c.

Kiểm chứng: đo `getComputedStyle` khối của màn tôi vs mục "Địa chỉ giao hàng" màn khách hàng —
**trùng từng thuộc tính**: nền `rgb(255,255,255)` · viền dưới `rgb(229,231,235)` · padding-left
`10px` · h6 `14px` / `rgb(31,41,55)` / `700`. Màn chi tiết 2 khối, màn tạo mới 3 khối, 0 lỗi console.

## Checkpoint — 2026-08-18
Vừa hoàn thành: **XONG CẢ PHASE 1 (BE) VÀ PHASE 2 (FE)**.
- BE smoke-test thật trên DB gộp: `warranty_repair_requests` 5.625 dòng, 3 tab đều chạy,
  Resource trả đúng `status_text` + `status_color` và đủ 5 cờ `is_can_*`; 2 mẫu in ERP
  (277 / 278) fill hết placeholder, không còn `{BIEN}` nào sót.
- FE: 9 file `.vue` đều compile sạch (template + script, Node 14.21.3).
Đang làm dở: không

### Phase 4 — Đặt đúng phân hệ (19/08)

User chốt: menu **đã có sẵn** ở CSKH → Kiểm tra bảo hành sửa chữa → Yêu cầu kiểm tra sửa chữa - bảo hành,
không tạo mục mới; code phải nằm đúng module tương ứng.

- [x] Chuyển 11 file BE `Modules/CustomerCare` → **`Modules/Sale`** (đổi namespace)
- [x] Chuyển route sang `Modules/CustomerCare/Routes/api.php`, prefix **`/v1/customer-care/warranty-repair-requests`** (thêm `middleware auth:api` cho group Sale vốn còn trống)
- [x] Chuyển 9 file FE `pages/customer-care/...` → **`pages/customer-care/warranty-repair-requests/`**; đổi hết đường dẫn API/link/`localStorageKey`/`columnScreenKey`
- [x] Gỡ mục menu tự thêm ở `customer-care.js`; nối `link` vào mục CÓ SẴN trong `sale-hub.js`
- [x] Deep-link thông báo đổi sang `/customer-care/warranty-repair-requests/{id}`
- [x] Quyền đổi `type` 24 (CSKH) → **23 (Bán hàng)**, group `Yêu cầu sửa chữa - bảo hành` (sửa cả seeder lẫn 4 bản ghi trên DB)
- [x] Test lại sau khi chuyển: 6 endpoint `/v1/sale/...` = 200 · route cũ `/v1/customer-care/...` = 404 · FE 3 tab + chi tiết chạy, 0 lỗi console · bấm từ menu Bán dịch vụ điều hướng đúng

## Phase 5 — Chuẩn hoá V2Base (19/08)

Rà lại theo câu hỏi của user: màn có dùng đủ component `V2Base*` chưa. Kết quả: **CHƯA** — còn
14 chỗ HTML thô. Đã thay hết:

### FE
- [x] `<input class="form-control">` (Khách hàng, Người liên hệ, SĐT, Địa chỉ, Loại hình tổ chức) → `V2BaseInput` + `disabled`
- [x] `<label class="v2-label">…<span class="text-danger">*</span>` (7 chỗ) → `V2BaseLabel required` (tự render `*` + icon ⓘ tooltip từ từ điển)
- [x] `<button class="btn btn-outline-secondary">` (kính lúp chọn KH) → `V2BaseIconButton`
- [x] `<button class="btn btn-link">` (Nhập serial tạm) → `V2BaseButton quaternary size="xs"`
- [x] `<input type="file">` + `<label class="btn">` tự dựng → `V2BaseFile` (không bật `autoUpload` vì phải vào đúng thư mục `wr_requests` như ERP)
- [x] **Lỗi thật**: upload trả **401** — `$axios` không tự gắn `Authorization`; đã tự đính token

### Tài sản chung
- [x] Bổ sung mục **1b** vào `.claude/skills/form-validate/SKILL.md`: bảng tra HTML thô → `V2Base*`, lý do (mixin `v2ValidateMixin`, kiểu ô khoá dùng chung, `V2BaseLabel` tự gắn tooltip), cảnh báo `$axios` 401, và lệnh grep tự kiểm
- [x] Bổ sung gạch đầu dòng tương ứng vào `CLAUDE.md`

Kiểm chứng: grep element thô → **0 kết quả**; 9 file `.vue` compile sạch; test trình duyệt: ô khoá
ra đúng `#f1f5f9`/`#475569`/opacity 1/`not-allowed`, 5 nhãn có dấu `*`, upload file lên đúng
`wr_requests/` và gỡ file chạy đúng.

## Phase 6 — Bỏ tab ở màn danh sách (19/08)

User hỏi "sao phải tách thành các tab, ERP có làm vậy đâu". Kiểm tra lại ERP: **đúng, ERP không có
tab** — 1 màn danh sách duy nhất, menu trỏ `?type=all`; `waiting_handle` không có mục menu (chỉ là
link Quay lại từ form); `all.blade.php` là code chết. Tôi đã tự suy 3 tab từ tham số `type`.

- [x] FE: gỡ `V2BaseTabNavigation` + `presetTabs` + `handlePresetChange`; `filters.type` cố định `'all'`
- [x] BE: đổi mặc định `type` từ `index` → **`all`** (đúng thứ menu ERP trỏ tới); đổi tên hằng `TAB_*` → `SCOPE_*` kèm ghi chú "KHÔNG phải 3 tab"
- [x] Gỡ `canHandle()` + cờ `can_handle` ở `/options` (chỉ phục vụ tab, giờ thành code chết)
- [x] Kiểm chứng: không gửi `type` và `type=all` đều ra 5.365 phiếu; lọc *Người yêu cầu = tôi* ra đúng con số của tab "Phiếu của tôi" cũ; màn hết thanh tab, 0 lỗi console

## Phase 7 — Đối chiếu 1:1 với ERP + nhận `?type=` (19/08)

User hỏi "làm như hiện tại đã đạt như ERP chưa, truyền thêm param như ERP được không". Đối chiếu
`index.blade.php` của ERP → phát hiện **thiếu 2 ô lọc** và **FE bỏ qua query `?type=`**.

### BE
- [x] `/options` trả thêm `provinces` (45 tỉnh — ERP dùng `Province::getForSelect()`) và `scope` (`is_all_company`/`is_company`/`is_department` — ERP truyền `is_big_boss`/`is_boss`/`is_manager`)
- [x] `scopeFlags()` ở service, đọc chung `can()` với `applyScope`

### FE
- [x] Thêm ô lọc **Tỉnh/TP** (BE đã hỗ trợ `province_id` từ đầu, FE chưa khai)
- [x] Thêm khối **Công ty – Phòng ban** (`V2BaseCompanyDepartmentFilter`), chỉ hiện theo phạm vi quyền BE trả về — đúng `search_by_info` của ERP
- [x] **Nhận `?type=` từ URL** (`applyQueryType()`, whitelist `index`/`all`/`waiting_handle`), query THẮNG bộ lọc đã lưu trong localStorage; "Làm mới" giữ nguyên phạm vi đang xem

Kiểm chứng: `?type=waiting_handle` → API gửi đúng `type=waiting_handle`; 3 giá trị `type` +
`province_id` + `company_id` + `department_id` đều lọc ra số liệu đúng; bộ lọc hiện đủ 9 ô khớp ERP.

### Còn khác ERP (có chủ ý, đã ghi ở design.md)
- Ô "Mã phiếu" riêng của ERP → gộp vào **ô tìm nhanh** (BE lọc `code` OR `customer_name`)
- 4 cột ERP hiện sẵn (Địa chỉ sửa chữa, Ngày xử lý, Người xử lý) → **ẩn mặc định**, user tự bật ở Cấu hình cột (skill list-page mục 6)
- Thêm cột "Ngày gửi yêu cầu" và hành động "Từ chối" ngay trên dòng (ERP để nút này trong màn form)

## Phase 8 — Rà toàn bộ skill list-page (19/08)

User chỉ ra 4 chỗ chưa tuân thủ skill. Rà lại `.claude/skills/list-page/SKILL.md` từng mục:

### Đã sửa
- [x] **Mục 6 — bộ cột mặc định sai**: đang hiện 8 cột (có "Tên thiết bị liên quan"). Skill: STT · Mã · Tên · Người tạo · Ngày tạo · Trạng thái · Hành động (+ Khách hàng là ngoại lệ). → còn **7 cột**, cột nghiệp vụ chuyển sang `isVisible: false`
- [x] **Mục 6 — thiếu Người tạo / Ngày tạo**: 2 cột này đang mang nhãn nghiệp vụ "Người yêu cầu"/"Ngày yêu cầu" → đổi về đúng nhãn chuẩn
- [x] **Mục 6 — thiếu hẳn Người cập nhật / Ngày cập nhật**: BE `ListResource` bổ sung `updater_name` + `updated_at` (eager load `updater.info`), FE khai 2 cột (ẩn mặc định)
- [x] **Mục 14b — Xuất file phải hỏi chọn trường**: đang tải thẳng bằng `WarrantyRepairRequestExport` cứng cột → **xoá class đó**, chuyển sang `ExportColumnRegistry` + `DynamicExport` dùng chung + `exportFieldsMixin` + `ExportFieldsModal`. Thêm khối `warranty_repair_requests` (13 cột) vào registry
- [x] **Ô tìm nhanh thiếu**: BE chỉ tìm mã phiếu + tên KH → thêm **tên người tạo** (dùng `EXISTS`, không join, theo cảnh báo của skill); placeholder cập nhật thành "Tìm theo mã phiếu, tên khách hàng, người tạo"
- [x] **Mục 3b — thiếu sắp xếp theo ĐỘ KHỚP**: bổ sung `applyRelevanceOrder()` (khuôn `CustomerService`), chấm điểm Mã phiếu + Tên KH, đủ 4 chốt bắt buộc (bỏ qua khi user bấm sort · chỉ chạy khi từ khoá ≥ 2 ký tự · `id DESC` cuối cùng · không chấm trường ở bảng khác)

Kiểm chứng: cột mặc định ra đúng 7; xuất file mở popup, request gửi `fields=` đúng thứ tự tick,
BE trả file đúng cột đã chọn; tìm "HYUNDAI" → dòng khớp sát lên đầu; bấm sort cột thì tôn trọng
sort; từ khoá 1 ký tự thì về sắp theo ngày tạo. 0 lỗi console.

### ⚠️ Nêu ra, chưa xử lý — xuất TOÀN BỘ chậm
`DynamicExport` dùng `FromView` (dựng HTML rồi convert). Với **5.365 dòng × 13 cột mất ~10,8s**
(chuẩn bị dữ liệu chỉ 1,8s — 9s còn lại là render view). Có lọc thì nhanh: 106 dòng = 0,7s,
61 dòng = 0,37s. Vượt ngưỡng 2s của CLAUDE.md → cần user chốt hướng (giới hạn số dòng / chuyển
`FromCollection` cho màn lớn / chạy queue).

## Phase 9 — Xuất file theo đúng khuôn màn Khách hàng (19/08)

User hỏi "xuất excel đã làm giống ở khách hàng chưa" — **chưa**: tôi để BE dựng file, màn Khách
hàng chia nhỏ API và dựng file ở FE. Đã làm giống + ghi thành nguyên tắc chung.

### BE
- [x] `GET /customer-care/warranty-repair-requests/export-rows` — trả `{ headings, widths, rows, total, page, limit }` theo trang, `rows` là mảng ô ĐÃ MAP SẴN; cột lấy qua `ExportColumnRegistry::resolve()` (dùng chung whitelist với popup chọn trường); trần `limit` 5.000
- [x] `exportRows()` ở service; giữ nguyên endpoint `/export` (BE dựng file) để đối chiếu

### FE
- [x] `utils/export/listExportFile.js` — bản DÙNG CHUNG rút từ `customerExportFile.js` (màn KH có thêm CSV/PDF + letterhead nên giữ riêng): tải tuần tự từng trang, trần vòng lặp, thoát khi trang rỗng, dựng Excel bằng ExcelJS (import động), báo tiến độ 2 giai đoạn
- [x] Màn dùng `exportListFile(...)` thay `downloadExcel`; thêm dòng tiến độ `.export-progress` + khoá nút khi đang xuất

### Tài sản chung
- [x] Thêm **mục 14c** vào `.claude/skills/list-page/SKILL.md`: ngưỡng 2s, bảng số đo thật, hạ tầng dùng, 6 chốt bắt buộc (tuần tự · trần vòng lặp · xoá page/limit · 0 dòng không tạo file · giữ endpoint cũ · dòng tiến độ) và điểm yếu cố hữu
- [x] Thêm gạch đầu dòng tương ứng vào mục Hiệu năng của `CLAUDE.md`

Kiểm chứng trên trình duyệt: 3 lượt gọi `export-rows` (page 1-3 × 2.000 dòng, mỗi lượt ~1,2s) →
**~4s** thay vì 10,8s; file tải về 5.365 dòng × 14 cột, có tiêu đề, header nền xám, đóng băng dòng
tên cột (A3), tự lọc (A2:N2); toast "Xuất Excel thành công".

## Phase 10 — Sửa màn in bị hở đầu trang (19/08)

User báo trang in `/customer-care/warranty-repair-requests/print` hở 1 dải phía trên. Đo trên trình duyệt:

| Nguồn | Cao |
| --- | --- |
| `.navbar-custom` (topbar, chỉ hiện tên user trên nền gradient xanh) | 60px |
| `.content-page { padding-top: 70px }` | 70px |
| `.container.mt-3` | 16px |
| **Tổng** | **~136px** đẩy tờ giấy xuống |

Nguyên nhân: tôi copy khuôn từ `pages/finance/product-import-requests/_id/print.vue` — màn đó khai
`layout: 'default-sidebar'`, tức bọc trang in trong lớp vỏ ứng dụng.

- [x] Thêm `layouts/print.vue` — không topbar/sidebar, nền trắng, vẫn `@import` SCSS chung để `V2Base*` hiển thị đúng
- [x] 2 màn in của feature đổi sang `layout: 'print'`
- [x] Thêm **mục 2b** vào `.claude/skills/print-page/SKILL.md`: bắt buộc `layout: 'print'`, bảng đo chiều cao thừa, cảnh báo đừng bù `margin-top` âm, và 2 lệnh console tự kiểm

Bỏ topbar xong VẪN còn 16px xám ở đầu — nguyên nhân thứ 2: **margin collapsing**. `margin-top`
của `.container.mt-3` tràn ra ngoài, đẩy cả layout xuống và để lộ nền `body` (#f5f6f8).
- [x] `.print-layout { display: flow-root }` — tạo BFC, margin con nằm gọn trong vùng trắng
      (KHÔNG dùng `overflow: auto`: trang in rất dài, sẽ đẻ thanh cuộn lồng nhau)
- [x] `body:has(.print-layout) { background: #fff }` — chặn nền xám lộ khi cuộn quá đáy / trang ngắn

Kiểm chứng: cả 2 màn in (1 phiếu + danh sách) — `.navbar-custom` không còn; `.print-layout` bắt đầu
ở **y = 0**; lấy mẫu `elementFromPoint` tại y = 0/5/10/15 đều ra `.print-layout` nền
`rgb(255,255,255)`; `body` cũng trắng; 0 lỗi console.

⚠️ **Không sửa đại trà**: rà thấy ~24 màn `print.vue` khác trong repo cũng khai `default-sidebar`
hoặc không khai layout (rơi về `default`) → đều hở như vậy. Đã ghi vào skill để team sửa dần khi
đụng vào từng màn, KHÔNG tự sửa hàng loạt màn của người khác.

## Phase 11 — Khối ký tên bị dồn về trái (19/08)

User báo `NGƯỜI YÊU CẦU / TRƯỞNG PHÒNG YÊU CẦU / PHÒNG NHẬN YÊU CẦU / BAN GIÁM ĐỐC` không ngang
hàng. Đo bằng `getBoundingClientRect` (preview) + iframe khổ in (skill print-page mục 7):

| Bảng | Rộng (preview) |
| --- | --- |
| 4 bảng thân phiếu | 1110px |
| **bảng ký** | **827px** — hụt 283px, co về trái |

Nguyên nhân nằm trong MẪU IN của ERP, không phải code màn:
1. `<table class="block no-border" style="width:827px">` — khổ giấy cứng của ERP.
2. Snippet chuẩn chỉ ép `table:not(.no-border) { width:100% }`, mà bảng ký CÓ `.no-border` nên bị loại trừ.
3. 4 ô `width:20%` = 80%, thiếu 20%.

- [x] Ép `#content table.block { width:100%; table-layout:fixed }` + `td { width:auto }` — khai ở CẢ `options.styles` (cửa sổ in) lẫn `<style scoped>` (bản xem trước)
- [x] Áp cho cả 2 màn in cho đồng nhất (mẫu danh sách đang `width:100%` nên chưa lệch, nhưng phòng khi mẫu bị sửa)
- [x] Thêm **mục 3b** + 1 dòng vào bảng "Checklist debug nhanh" của `.claude/skills/print-page/SKILL.md`

⚠️ Bẫy khi sửa: comment CSS đặt trong template literal của `options.styles` **không được chứa dấu
backtick** — đứt chuỗi, cả file không compile.

Kiểm chứng — preview: bảng ký 1110px = thân phiếu, 4 ô chia đều 278px, cùng `top`.
Khổ in (iframe 190mm): bảng ký 683px = khung in = thân phiếu, 4 ô đều 171px, tràn mép phải = 0.

## Phase 12 — Cấp quyền tk namdangit + test toàn diện (19/08)

Cấp đủ 4 quyền cho `namdangit@gmail.com` (employee id 13, role `Super admin` id 18 +
`Quyền giám đốc kinh doanh`) rồi test lại toàn bộ. **Tìm ra 3 lỗi thật:**

### Lỗi 1 — `hasRole('Super Admin')` không bao giờ khớp
DB gộp có 2 role gần giống: id 18 `Super admin` (guard `api`, HRM) và id 100002 `Super Admin`
(guard `web`, ERP). Tôi so theo TÊN chữ hoa → trượt **im lặng**, nhánh bỏ qua điều kiện phòng ban
không bao giờ chạy.
- [x] Đổi sang dò theo **role id 18** (`WarrantyRepairPermission::SUPER_ADMIN_ROLE_ID`), đúng khuôn `Modules/Finance/Entities/ProductTransferRequest`

### Lỗi 2 — `canTransferDepartmentReception()` lệch ERP
Tôi thêm nhánh Super admin vào đây, nhưng ERP **không có** → Super admin chuyển được phiếu của
phòng khác. Test thật đã chuyển nhầm 1 phiếu sang phòng 51.
- [x] Bỏ nhánh Super admin; chỉ `canHandleRequest()` mới có (đúng ERP)

### Lỗi 3 — thiếu validate serial của ERP
ERP: dòng thiết bị KHÔNG chọn `serial_id` thì `serial` **bắt buộc**. FormRequest của tôi để
`nullable` cả 2 → gửi phiếu không serial vẫn lọt.
- [x] Thêm rule theo từng dòng (`productsWithoutSerialId()`), chỉ áp khi GỬI (lưu nháp vẫn để trống được)

### Đã test (tk namdangit, 15 nhóm kịch bản)
BE: 3 phạm vi `type` · options (9 trạng thái / 87 phòng / 45 tỉnh / scope) · 10 bộ lọc · 3 kiểu
sắp xếp · lưu nháp · gửi duyệt thiếu trường (422, 6 lỗi) · gửi duyệt đủ · sửa phiếu đã gửi (423) ·
xoá phiếu đã gửi (chặn) · chuyển phòng trùng (chặn) / phòng khác (OK) / trái phòng (chặn) · từ chối
thiếu lý do (422) / có lý do (về Đang tạo) · in 1 phiếu + in danh sách (hết placeholder) ·
export-rows (0,27s, lọc cột OK) · customer-info · chi tiết · xoá phiếu nháp.

FE: đăng nhập đúng DNS Admin · 7 cột + 9 ô lọc · hành động theo quyền · tạo mới đầy đủ qua giao
diện (popup KH → chọn thiết bị → chọn serial → gửi duyệt) → ra phiếu `Chờ xử lý` · lỗi serial hiện
đúng trong dòng thiết bị.

Dữ liệu test đã dọn sạch: 5.625 phiếu = đúng số gốc, 0 phiếu test còn sót.

## Phase 13 — Số hành động lệch ERP (19/08)

User so cùng 1 bản ghi giữa ERP và HRM thấy số hành động khác nhau. Đối chiếu
`WarrantyRepairRequestsController::searchData` của ERP:

- [x] **Lỗi gate**: ERP gate nút "Chuyển phòng tiếp nhận" bằng `canHandelRequest()` (y hệt nút "Tạo phiếu xử lý" — 2 khối `if` giống nhau), KHÔNG phải `canTransferDepartmentReception()`. Hàm đó trong ERP là **CODE CHẾT: 0 nơi gọi** (đã grep toàn `app/` + `resources/`). Guard endpoint transfer và footer màn form cũng dùng `canHandelRequest()`.
  → `canTransferDepartmentReception()` / `canReject()` của HRM đổi thành **alias** của `canHandleRequest()`; truyền sẵn cờ `has_handle_request` để không phát sinh query.
- [x] **Vị trí nút Từ chối** — ERP đặt ở footer màn form, danh sách chỉ 5 nút; skill HRM đòi 2 màn khớp nhau. **User chốt: giữ ở CẢ 2 nơi** (theo skill). Ghi vào design.md mục "Quyết định đã chốt".

Kiểm chứng — cùng phiếu `TPE.YCSCBH.26.005682` (Chờ xử lý, gửi về phòng của tài khoản):
- API: 3 cờ `is_can_handle_request` / `is_can_transfer_department` / `is_can_reject` giờ **luôn bằng nhau** (kiểm 8 dòng, 0 dòng lệch).
- Danh sách: Tạo phiếu xử lý · Chuyển phòng · Từ chối · In = **4 hành động**.
- Chi tiết: Tạo phiếu xử lý · Chuyển phòng · Từ chối · In = **4 hành động** (+ Quay lại do V2Footer tự render).

## Phase 14 — Khối nhóm dùng chung component (19/08)

User yêu cầu 3 khối ("Thông tin khách hàng", "I – Danh sách thiết bị…", "II – Danh mục trang thiết
bị…") dùng chung component như mục **"Địa chỉ giao hàng"** của `/assign/customers/{id}`.

Rà ra: khuôn đó **chưa phải component** — markup `card > card-header.section-header > h6` cùng khối
SCSS đang bị **copy-paste ở 35 file**.

- [x] Tạo `components/V2BaseFormSection.vue` — prop `title`, slot `#title` (tiêu đề cần markup riêng), slot `#actions` (nút/ô tìm bên phải), slot mặc định cho nội dung; bê nguyên CSS `.card-header.section-header` kèm ghi chú vì sao
- [x] Áp cho cả 3 khối của màn; khối II giữ nguyên ô tìm + 2 nút qua `#actions`
- [x] Thêm **mục 1c** vào `.claude/skills/form-validate/SKILL.md` + 1 gạch đầu dòng vào `CLAUDE.md`
- [x] KHÔNG sửa 35 màn cũ (quy tắc team) — ghi rõ "sửa dần khi có dịp đụng vào"

- [x] **Bảng trong form thừa khoảng trắng**: `assets/scss/default.scss` ép `.table-responsive { min-height: 50vh }` cho MỌI bảng → phiếu 1 thiết bị bảng chỉ 118px mà khung bị kéo lên 429px, thừa **311px trống có viền**. Ghi đè cục bộ `.v2-form-table-wrap { min-height: 0 }` (KHÔNG sửa rule global). Khối I: **517px → 213px**; khung vẫn nở đúng khi bảng dài (17 dòng → 1183px, không cắt, không cuộn).
- [x] **Padding dọc ô bảng**: Bootstrap để `.table td/th { padding: .75rem }` = 12,8px trên/dưới → dòng cao 81px dù chữ 1-2 dòng. Bóp còn **4px** (giữ ngang 8px). Khối I: 213px → **187px**, dòng **81px → 64px**; chữ không cắt, ô nhập trong bảng không méo (input 32px / textarea 53px giữ nguyên). Đã ghi cái bẫy này vào skill `form-validate` mục 1c.

Kiểm chứng: đo `getComputedStyle` khối của màn tôi vs mục "Địa chỉ giao hàng" màn khách hàng —
**trùng từng thuộc tính**: nền `rgb(255,255,255)` · viền dưới `rgb(229,231,235)` · padding-left
`10px` · h6 `14px` / `rgb(31,41,55)` / `700`. Màn chi tiết 2 khối, màn tạo mới 3 khối, 0 lỗi console.

## Checkpoint — 2026-08-18 (sau khi TEST THẬT trên cổng 3002/8003)
Đã test end-to-end, phát hiện và sửa 4 lỗi thật (xem Phase 3).

**BE — 20 kịch bản qua HTTP thật trên :8003, tất cả đúng:**
3 tab · options · lưu nháp thiếu trường (201) · gửi duyệt thiếu trường (422, 6 lỗi đúng trường) ·
gửi duyệt đủ (200 + sinh mã + đóng dấu giờ gửi) · sửa phiếu đã gửi (423) · xóa phiếu đã gửi (chặn) ·
chuyển phòng trùng (chặn) · chuyển phòng khác (200) · từ chối trái phòng (chặn) · từ chối thiếu lý
do (422) · từ chối đúng (về Đang tạo + lưu lý do) · thông báo bắn đúng template `[YCSCBH]` cho cả
phòng tiếp nhận lẫn người lập · in 1 phiếu + in danh sách (hết placeholder) · xuất Excel (10 cột) ·
upload file lên S3 · xóa phiếu nháp (sạch cả bảng con).

**FE — Playwright trên :3002:** danh sách 3 tab · badge ra ĐÚNG mã màu chuẩn (#64748B / #D97706,
nền 10% viền 20%) · cột Hành động ẩn/hiện đúng theo trạng thái · màn chi tiết (5 nút khớp danh
sách) · form tạo mới (popup chọn KH 11.028 KH, bảng thiết bị KH 17 dòng, chọn thiết bị, validate
inline 422, lưu nháp thành công) · popup Chuyển phòng (86 option, validate) · popup Từ chối (đổi
trạng thái + hiện lý do màu xám đúng chuẩn) · 2 màn in · cảnh báo "chưa lưu" khi rời màn.
Console: 0 lỗi (chỉ còn 1 Vue warn `fields` của `ChooseErpCustomerModal` dùng chung, có sẵn từ trước).

Dữ liệu test đã dọn sạch (3 phiếu + 150 thông báo).

Bước tiếp theo: user nghiệm thu trên trình duyệt; sinh SRS + testcase nếu cần.
Blocked: màn "Phiếu xử lý yêu cầu" chưa port -> nút "Tạo phiếu xử lý yêu cầu" tạm báo toast
hướng dẫn xử lý trên ERP, cần bỏ nhánh này khi màn đó xong.

## Phase 15 — Rà lại UI form theo góp ý (2026-08-19)

- [x] **Cột "Chọn" / "Xóa" của 2 bảng I và II → đổi tên thành "Hành động"** (rộng 90px, canh giữa) cho khớp cột hành động màn danh sách.
- [x] **Icon trong 2 cột đó không hiện**: dùng `<V2BaseIconButton icon="..." />` nhưng component **không có prop `icon`**, chỉ nhận slot → render nút rỗng. Sửa 3 chỗ sang truyền slot (`ri-search-line` chọn KH · `ri-delete-bin-6-line` xóa dòng · `ri-add-line` chọn thiết bị).
- [x] **Nút "Tìm kiếm" ở khối II để `primary`** như nút tìm kiếm màn danh sách.
- [x] **Dòng trống "Chưa chọn thiết bị nào…" đang ĐỎ**: `.text-muted` bị 4 file SCSS toàn cục ép `color: #dc3545 !important`. Thay bằng `.v2-empty-row { color: #6b7280 }` (KHÔNG sửa rule global). Đã ghi bẫy này vào skill `list-page` mục 3b-2 + CLAUDE.md.
- [x] **Ô chọn file theo đúng khuôn màn Meeting** (`/assign/meeting/create` → tab Biên bản → "Import tài liệu kèm biên bản"): nâng cấp `components/V2BaseFile.vue` — nút `⬆ Chọn tệp` → spinner "Đang tải lên…" (prop `uploading`) → dòng file có **icon theo loại** + tên + **Tải xuống / Thay đổi / Xóa**. Form truyền `:uploading="uploadingIndex === index"`.
- [x] **Bẫy vừa dính khi làm việc trên**: `.v2-file__change` thiếu `position: relative; overflow: hidden` → `.v2-file__input` (absolute 100%/100%) thoát ra ngoài, **bấm đâu cũng bật hộp thoại chọn file**. Đã sửa + ghi vào skill.
- [x] **Ghi nguyên tắc vào tài sản chung**: `.claude/skills/form-validate/SKILL.md` **mục 1d** (chỗ nào chọn file cũng dùng `V2BaseFile`, cần bảng tài liệu thì `FileAttachmentTable`, không tự dựng `<input type="file">` + `<label class="btn">`) + bullet tương ứng trong `CLAUDE.md`.

Kiểm chứng trên trình duyệt (:3002, màn tạo mới): tiêu đề 2 cột = "Hành động"; icon ra đúng
(`ri-delete-bin-6-line`, `ri-add-line`); nút Tìm kiếm `primary`; upload PDF thật lên S3 → dòng file
hiện `ri-file-pdf-line text-danger` + tên file + đủ 3 nút Tải xuống/Thay đổi/Xóa; input file nằm
gọn trong nút (133×32 chứa 131×30).
- [x] **Bảng cuộn ngang có thanh cuộn ở CẢ TRÊN VÀ DƯỚI**: tách component dùng chung `components/V2BaseTableScroll.vue` (khuôn gốc lấy từ `V2BaseDataTable` — pattern này đang bị copy-paste ở 4 nơi với 4 tên class khác nhau), áp cho bảng I và II. Đo thật: khung 798px / bảng 1456px → thanh trên hiện, kéo trên chạy dưới (200↔200) và kéo dưới chạy trên (60↔60); bảng vừa khít thì thanh trên tự ẩn. Đã ghi nguyên tắc vào skill `list-page` mục 3b-1 + CLAUDE.md.
- [x] **Ô Khách hàng: bấm thẳng vào ô để mở popup chọn** (bỏ nút icon kính lúp bên cạnh). Copy pattern `.picker-input` đã dùng ở 6 file phân hệ Tài chính (`BillPaymentRequestForm.vue:1370`): `readonly` + `@click.native` + `cursor: pointer`, nền trắng khi sửa / `#f1f5f9` khi chỉ đọc, placeholder "Nhấn vào đây để chọn khách hàng". ⚠️ Phải dùng `readonly` chứ KHÔNG `disabled` — `disabled` thì trình duyệt nuốt luôn sự kiện click.

## Phase 16 — Rà soát & test lại TOÀN BỘ luồng, đối chiếu từng dòng với ERP (2026-08-19)

Đối chiếu code ERP thật (`TanPhatDev`): `WarrantyRepairRequestsController`, `WarrantyRepairStoreRequest`,
`Model/Customers/WarrantyRepairRequest` (`searchByFilter`, `syncProduct`, `canHandelRequest`, `canEdit`),
`SearchController@searchCustomer`, `CustomerManagerController@getListProductOfCustomer`, `form.blade.php`.

**BE — 30 kịch bản qua HTTP thật trên :8003, khớp ERP:**
- Phạm vi dữ liệu: `all` 5.366 = SQL công thức ERP (`company_id IS NOT NULL` + phiếu nháp chỉ chủ phiếu thấy) · `index` 1 · `waiting_handle` 0 (đúng: phòng 111 không có phiếu Chờ xử lý nào).
- Validate gửi xử lý: đúng 6 lỗi ERP (`customer_address`, `customer_contact_name`, `delivery_place`, `note`, `department_reception_id`, `products`); trùng serial cùng `type` → "Bị trùng serial thiết bị" ở CẢ 2 dòng; thiếu `serial` khi không có `serial_id` → chặn; thiếu `request_description` dòng thiết bị → chặn.
- Ghi dữ liệu: sinh mã, đóng dấu `send_request_time`, `customer_type` chép từ KH, `company_id`/`department_id` theo người tạo, `created_by`/`updated_by` = 13; bảng con ghi đúng `type` tp/tpc/ncck, serial lấy lại tên từ danh mục khi chọn `serial_id` (giống `syncProduct`).
- Guard: sửa phiếu đã gửi → **423**; xoá phiếu đã gửi → chặn; chuyển phòng trùng → chặn; phòng không tồn tại → 422; từ chối thiếu lý do → 422; từ chối xong về "Đang tạo" + lưu lý do + `is_can_edit` bật lại.
- Thông báo: 2 người phòng tiếp nhận nhận đúng `[YCSCBH] Chờ duyệt: <b>MÃ</b>. Khách hàng: …`.
- Bộ lọc: keyword (mã/tên KH/người tạo), status, created_by, customer_id, province_id, product_name, start_date/end_date, company_id, department_id — tất cả lọc đúng.
- In: 1 phiếu + danh sách, 0 placeholder sót. Xuất: `export-rows` 14 cột, trần 5.000 dòng/lượt; `export` (BE dựng file) 80KB/0,4s.

**FE — Playwright trên :3002 (luồng end-to-end thật):**
tạo mới → chọn KH qua popup (11k KH) → tự nạp liên hệ/nơi giao nhận/loại hình → chọn thiết bị →
lưu nháp → sửa → gửi duyệt thiếu trường (6 lỗi inline, 5 ô viền đỏ) → điền đủ → gửi duyệt (sang
"Chờ xử lý") → từ chối qua popup (validate lý do → về "Đang tạo") → xoá qua `$confirm` → DB sạch cả
bảng con. Kèm: badge màu chuẩn `#64748B`, hành động theo trạng thái khớp ERP, menu "Hành động khác",
màn chi tiết 4 hành động khớp danh sách, cảnh báo "chưa lưu" khi gõ tay rồi thoát, xuất Excel 5.368
dòng **4,9s**, in danh sách 5.377 dòng, in 1 phiếu (không hở mép, chữ ký ngang hàng), lọc tự chạy
khi chọn, dòng rỗng màu xám.

### Sửa trong đợt rà soát này
- [x] **Upload đính kèm không kiểm loại/kích thước file** — gọi thẳng API đẩy được `.txt` (hay bất kỳ gì) lên S3 vì `accept` chỉ là gợi ý của trình duyệt. Thêm validate BE `file|max:20480|mimes:pdf,png,jpg,jpeg,doc,docx,xls,xlsx` khớp `accept` của `V2BaseFile`. Đã test: `.txt` → 422, `.pdf` → 200.
- [x] **Bảng II thiếu phân trang (ERP có 10 dòng/trang)** — KH lớn nhất có **197 thiết bị**, đổ hết ra làm form dài lê thê. Cắt trang 10 dòng ở FE (dữ liệu đã tải sẵn, không gọi lại API), có dòng "Hiển thị x–y / tổng" + nút Trước/Sau, tự về trang 1 khi tìm lại. Đã test trên KH 56 thiết bị: trang 1 STT 1–10, trang 2 STT 11–20, chọn thiết bị ở trang 2 vẫn vào bảng I đúng.

### Khác biệt CÓ CHỦ ĐÍCH so với ERP (đã cân nhắc, không phải lỗi)
1. **Lưu nháp không bị chặn** — ERP validate required như nhau cho cả 2 nút; HRM cho lưu nháp thiếu trường theo `.claude/skills/form-validate`. (Đã chốt từ đầu feature.)
2. **Lọc `product_name`** — ERP `whereIn('id', <id BẢNG CON>)` là **bug** (so id dòng thiết bị với id phiếu): ERP ra 318 phiếu, đúng phải 344. HRM dùng `EXISTS` cho đúng.
3. **`type` lạ trên URL** — ERP không lọc gì (lộ toàn bộ dữ liệu), HRM fail-closed về phiếu của mình; FE đã whitelist 3 giá trị.
4. **"Từ chối" có mặt ở màn danh sách** — ERP chỉ để ở màn chi tiết, nhưng CLAUDE.md buộc 2 màn phải khớp số hành động.
5. **Ô tìm nhanh rộng hơn ERP** (mã phiếu + tên KH + người tạo, ERP chỉ mã phiếu) — theo skill `list-page`.
6. **Tên tham số lọc công ty/phòng ban** dùng `company_id` / `department_id` (ERP: `company` / `department`) cho khớp `V2BaseCompanyDepartmentFilter` dùng chung.

### Điểm cần user quyết (chưa đụng vào)
- **Popup chọn KH dùng chung `ChooseErpCustomerModal` hiện 17.188 KH, ERP hiện 12.406** — chênh 4.782 là KH cá nhân: ERP tách 2 tab và tab cá nhân bắt buộc nhập SĐT mới ra kết quả. Sửa riêng màn này hay sửa popup dùng chung (ảnh hưởng 8 màn) — chờ user chốt.
- **Chữ popup xác nhận "Bạn đồng ý lưu và duyệt ?"** nằm trong `components/V2Footer.vue` (dùng chung toàn hệ thống), thừa dấu cách trước `?` và không khớp nghiệp vụ "gửi phòng tiếp nhận xử lý". Không tự sửa file dùng chung.
- **In danh sách không lọc trả 6MB HTML / 1,7s** (ERP cũng `->get()` toàn bộ, không giới hạn). Cân nhắc bắt buộc chọn bộ lọc trước khi in.

Dữ liệu test đã dọn sạch: 4 phiếu (5690–5693) + bảng con + 11 thông báo. Tổng phiếu về đúng 5.625.
- [x] **Dấu `?` dính sát chữ trong popup xác nhận** (user chốt 2026-08-19 cho sửa file dùng chung): bỏ khoảng trắng thừa trước `?` ở `components/V2Footer.vue` và `components/Footer.vue` — 4 câu mỗi file (`Bạn xác nhận duyệt phiếu?`, `Bạn đồng ý lưu và gửi?`, `Bạn đồng ý lưu và duyệt?` ×2). Chỉ đổi chính tả, không đổi logic; 2 file là CRLF nên sửa bằng Python `newline=''`, `git diff --stat` đúng 8 dòng/file. Đã xem lại trên trình duyệt: "Bạn đồng ý lưu và duyệt?".
- [x] **Màn xem trước bản in thiếu KHUNG TỜ GIẤY như ERP**: `#content` trải hết bề ngang trình duyệt, không thấy nội dung rơi đâu trên A4. Dựng lại đúng thông số ERP — bản 1 phiếu (`print.blade.php`): rộng **210mm**, padding `15mm 22mm 22mm 20mm` (bằng lề `@page`), nền quanh trắng; bản danh sách (`print_landscape.blade.php`): rộng **297mm**, padding `15mm`, nền quanh **#eee**; cả hai viền `1px #d3d3d3` + bo 5px + bóng nhẹ, căn giữa. Đo lại: giấy dọc **794px** (=210mm), giấy ngang **1123px** (=297mm), viền `rgb(211,211,211)`, hàng nút In thẳng mép trái giấy (401↔401 và 236↔236). Ctrl+P thẳng trên preview thì khung tự bỏ. Đã ghi khuôn + bẫy "flex align-items:center làm trôi nút In" vào skill `print-page` mục 2c.
- [x] **Nút In ở màn xem trước: cỡ `xs` + căn PHẢI** (thẳng mép phải tờ giấy), dòng "Đang tải…"/lỗi đẩy sang trái bằng `mr-auto`. Bẫy vừa dính: đặt `width` cho thanh công cụ qua class `.no-print` thì kéo luôn CHÍNH CÁI NÚT rộng 794px (class đó nằm trên cả nút) → tách class riêng `.print-toolbar`. Đo lại: nút **47×24px**, mép phải nút trùng mép phải giấy ở cả 2 màn. Đã ghi vào skill `print-page` mục 2c + CLAUDE.md.
- [x] **Thống nhất nền 2 màn in + trả nút In về cỡ chuẩn**: ERP để bản dọc nền trắng, bản ngang nền `#eee` → mở cạnh nhau thấy mỗi màn một màu; HRM dùng chung **`#eee`** cho cả 2 (Ctrl+P thì về trắng). Nút In trả lại `V2BaseButton primary size="sm"` + icon 15px như mọi nút chính khác, vẫn căn phải. Đo lại: nền ngoài `rgb(238,238,238)` ở cả 2 màn, giấy trắng, nút **57×32px**, mép phải nút trùng mép phải giấy. Skill `print-page` mục 2c + CLAUDE.md đã cập nhật theo.
- [x] **Nền quanh giấy: TRẮNG cho cả 2 màn in** (user chốt 2026-08-20, thay cho #eee ở bước trước). Tờ giấy vẫn tách khỏi nền nhờ viền `#d3d3d3` + đổ bóng. Đo lại: `.print-preview`, `body` và `#content` đều `rgb(255,255,255)`, viền `rgb(211,211,211)`, giấy 794px (dọc) / 1123px (ngang). Skill `print-page` mục 2c + CLAUDE.md cập nhật theo.

## Phase 17 — Tài liệu bàn giao (2026-08-20)

- [x] **`testcase.xlsx`** — 97 test case, P0 chiếm 52%, sinh bằng `gen_testcase.py` (dùng engine chung `tc_engine.py` của skill `testcase-documenter`). Đủ 4 khối chuẩn: 9 mục mô tả · Test Summary (DNS + TP) · header 17 cột · 11 nhóm testcase (Phân quyền & truy cập 10 TC + 10 nhóm La Mã). Bộ kiểm tra thuật ngữ in "OK - sach" (không còn tên bảng/cột, mã lỗi kỹ thuật, đường dẫn nội bộ). Không trùng mã TC, không dùng freeze panes.
- [x] **`Mô tả nghiệp vụ - Yêu cầu kiểm tra sửa chữa - bảo hành.docx`** — 11 chương, 8 bảng, 8 trang: dùng để làm gì · ai tham gia · 9 trạng thái và ai làm phiếu chuyển trạng thái · luồng 4 bước (lập → gửi → phòng tiếp nhận xử lý theo 3 hướng → đi tiếp) · **bảng thông báo: sự kiện nào, ai nhận, nội dung, bấm vào đi đâu** · phân quyền (4 quyền + bảng điều kiện từng thao tác) · quy tắc bắt buộc (bắt buộc nhập theo nút bấm, serial, khóa sửa, danh mục khóa, số phiếu) · tra cứu/in/xuất · liên thông ERP + 3 điểm cố ý làm khác · giới hạn hiện tại. Sinh bằng `gen_mo_ta_nghiep_vu.py`, đã soát lại bản PDF chuyển từ file Word.

## Phase 18 — Chuyển màn về ĐÚNG phân hệ CSKH (2026-08-20)

Menu ERP xếp màn này ở **CSKH → Kiểm tra bảo hành sửa chữa** (`topmenubar.blade.php:1918`), không
phải Bán hàng — Phase 5 trước đây đặt nhầm sang Bán hàng. Đã chuyển **hẳn** (git mv, không để lại
bản sao ở chỗ cũ):

**BE** — 11 file từ `Modules/Sale` → `Modules/CustomerCare` (Entities · Http/Requests · Http/Controllers/V1 · Services ×3 · Support · Transformers), đổi toàn bộ namespace `Modules\Sale\` → `Modules\CustomerCare\`; khối route chuyển từ `Modules/Sale/Routes/api.php` sang `Modules/CustomerCare/Routes/api.php`, đổi prefix `/v1/sale` → `/v1/customer-care`; `URL_PREFIX` của thông báo đổi sang `/customer-care/warranty-repair-requests/`. Dọn thư mục rỗng còn sót (`Modules/Sale/Support`). Module `Sale` giữ nguyên (đã có sẵn trên nhánh, không phải do màn này tạo), route group để trống kèm ghi chú trỏ sang CSKH.

**FE** — `pages/sale/warranty-repair-requests` → `pages/customer-care/warranty-repair-requests`; đổi mọi đường dẫn nội bộ và URL gọi API; khóa lưu cấu hình cột đổi thành `customer_care_warranty_repair_requests`. Menu: gỡ khỏi `sale-hub.js` (Bán hàng → Bán dịch vụ) và thêm nhóm mới **"Kiểm tra bảo hành sửa chữa"** trong `customer-care.js` gồm 4 mục theo đúng menu ERP (mục đầu có link, 3 mục sau chưa port).

**Kiểm chứng thật:** đường dẫn cũ `/api/v1/sale/warranty-repair-requests` → **404**; đường dẫn mới `/api/v1/customer-care/...` → **200, 5.365 phiếu**. Trên trình duyệt (phải khởi động lại Nuxt vì router không tự nhận thư mục pages mới): danh sách 10 dòng / 5.365, đủ 7 cột; màn chi tiết, sửa và in phiếu đều mở đúng; menu CSKH hiện nhóm "Kiểm tra bảo hành sửa chữa" → "Yêu cầu kiểm tra sửa chữa – bảo hành"; đường dẫn FE cũ `/sale/warranty-repair-requests` trả về trang không tìm thấy.

**Tài liệu** — cập nhật `design.md`, `plan.md`, spec chi tiết và 2 generator; đã sinh lại `testcase.xlsx` (97 TC) và file mô tả nghiệp vụ theo vị trí menu mới.

## Phase 19 — Nền màn in đổi lại thành xám (2026-08-20)

- [x] **Nền quanh giấy: XÁM `#eee` cho cả 2 màn in** (user chốt lại 2026-08-20, thay cho nền trắng ở Phase 16). Lấy đúng màu của ERP `print_landscape.blade.php`. Sửa `.print-preview { background-color }` ở `pages/customer-care/warranty-repair-requests/print.vue` và `_id/print.vue`; tờ giấy `#content` giữ nền trắng + viền `#d3d3d3` + đổ bóng. Lưu ý: đây là **ngoại lệ có chủ đích** so với skill `print-page` mục 2c (mặc định nền trắng cho mọi màn in) — chỉ áp cho 2 màn in của chức năng này, không sửa skill và không sửa màn in khác.
- [x] **Fix dải trắng 16px ở đầu trang** phát hiện khi verify: `margin-top` của `.container.mt-3` bên trong tràn ra ngoài (margin collapsing) đẩy khối xám xuống, hở nền trắng của `.print-layout`. Thêm `display: flow-root` cho `.print-preview` ở cả 2 màn (KHÔNG dùng `overflow: auto` — trang in dài sẽ đẻ thanh cuộn lồng nhau).
- [x] **Verify Playwright** (login token-injection namdangit, FE :3002 / API :8003): cả 2 màn `.print-preview` = `rgb(238,238,238)`, `#content` = `rgb(255,255,255)` viền `rgb(211,211,211)`, giấy 794px (phiếu) / 1123px (danh sách), `.print-preview` top = 0 và element tại `(giữa màn, y=0)` là `print-preview` (hết dải trắng), nút In thẳng mép phải giấy (994px = mép phải `#content`). Ảnh: `wrr-print-phieu.png`, `wrr-print-danhsach.png`.
- [x] **Nâng lên CHUẨN CHUNG cho mọi màn in** (user yêu cầu): chuyển màu nền vào `layouts/print.vue` (`.print-layout` + `body:has(.print-layout)` = `#eee`) để màn in mới KHÔNG phải khai `background` riêng; 4 màn in hiện có (`warranty-repair-requests` + `warranty-repair-handle-requests`, mỗi bên 1 phiếu + 1 danh sách) bỏ `background-color` khỏi `.print-preview`, chỉ giữ `min-height: 100vh` + `display: flow-root`. Cập nhật skill `print-page` mục 2b/2c (mã màu, snippet, cách tự kiểm đổi sang `rgb(238,238,238)`, thêm cảnh báo margin collapsing lặp ở lớp `.print-preview`) và bullet màn IN trong `CLAUDE.md`. Verify Playwright cả 4 màn: `.print-layout` + `body` = `rgb(238,238,238)`, `#content` = `rgb(255,255,255)`, `.print-preview` top = 0, giấy 794px/1123px đúng khổ.

### Checkpoint — 2026-08-21 (đổi chữ nút gửi phiếu)
Đổi nút gửi phiếu từ **"Lưu và gửi duyệt"** sang **"Lưu và gửi"** (user chốt 2026-08-21): phiếu
được GỬI cho phòng tiếp nhận để họ xử lý — phòng đó chỉ Từ chối / Chuyển phòng tiếp nhận / lập
Phiếu xử lý, KHÔNG có thao tác "Duyệt" nào. `V2Footer` có sẵn `send_and_submit_form` kèm đúng câu
xác nhận — KHÔNG phải sửa component dùng chung.
Đã sinh lại `testcase.xlsx` (97 TC, 14 ô nhắc tên nút) và `Mô tả nghiệp vụ - Yêu cầu kiểm tra sửa
chữa - bảo hành.docx` (5 chỗ). Bản testcase ERP giữ nguyên vì ERP không đổi.
Đã kiểm trên giao diện: nút và popup ra đúng chữ; bấm Hủy nên phiếu thật không đổi trạng thái.
Cả 3 chứng từ của luồng dịch vụ nay dùng chung chữ "Lưu và gửi".
Blocked:
