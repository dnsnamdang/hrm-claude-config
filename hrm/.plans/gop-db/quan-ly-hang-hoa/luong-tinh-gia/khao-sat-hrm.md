# Phase 7 — Khảo sát phía HRM trước khi design (11/10/2026)

> Chỉ đọc. Nguồn: worktree `wt-chuyen-doi-hang-hoa` (hrm-api / hrm-client @ `feat/chuyen-doi-hang-hoa`, HEAD hrm-api `b282d0829`),
> DB `hrm_erp_giacty` (chỉ SELECT), GitHub `DNS-Media/hrm-api@gop_db` (đọc qua `gh api`, commit mới nhất `61179896c` 10/10 14:07 — chưa fetch về máy).
> Đường dẫn BE tính từ `hrm-api/`, FE tính từ `hrm-client/`. Viết tắt: `upp` = product_unit_prices, `pep` = product_expected_prices,
> `pcu` = product_company_units, `pcc` = product_company_coefficients, `pa`/`pap` = product_approves / product_approve_prices.

---

## 1. Lớp ghi / đọc giá theo công ty (G2/G4/G5) — PTG duyệt phải gọi lại đúng chỗ này

Mọi file ở `Modules/MasterData/Services/ProductPrice/`.

### 1.1 Ghi thẳng bộ giá 6 loại × 1 ĐVT × 1 công ty — `ProductPriceUpdateService`

| Hàm | Dòng | Ghi chú |
|---|---|---|
| `update(int $productId, array $input): array` | :80–151 | Hàm DUY NHẤT public để ghi. **Công ty lấy từ `$this->list->companyId()` = công ty đang làm việc** (:82, `ProductPriceListService::companyId()` :50–53 → `currentCompanyId()`), KHÔNG nhận từ tham số |
| `assertTradingAt($companyRow)` | :154–171 | chỉ cho `pcc.status = 3`; **1 ⇒ 423, 2 (Chờ tính giá) ⇒ 423, 4 ⇒ 423, NULL ⇒ 403** |
| `validate()` | :177–261 | `cost_price` bắt buộc; `prices` đủ 6 loại; `expected_prices` ≤ 1 dòng/loại, `effect_date after:today` |
| `resolvePrices(array $prices, int $companyId): array` | :286–350 | **public** — chuẩn hoá "bộ giá mới" (TMĐT BE tự tính = Bán lẻ × `configs.coefficient_ecommerce_price`, giá hiệu lực TMĐT suy từ Bán lẻ). Đầu ra `[type => price, coefficient, sale_max_percent, manual_*, expected[], by_order]` — đây là định dạng "bộ giá mới" cả 2 nhánh dùng chung |
| `writePrices(unitId, companyId, resolved, by)` | :353–380 | **private** — ghi 6 dòng `upp` của công ty, xoá `*_wait_approve`, cờ về 0 |
| `writeExpected(...)` | :385–426 | **private** — ≤ 1 dòng tương lai/dòng giá, sửa tại chỗ, xoá dòng không gửi (+ `pap` trỏ tới) |
| `writeCompanyUnit(unitId, companyId, data, by)` | :428–441 | **private** — `pcu.cost_price` + `reason_edit_price`, cờ chờ duyệt về 0 |
| `dropPendingApprovals(productId, unitId, companyId)` | :444–452 | **private** — xoá `pa` + `pap` đang mở của (hàng, ĐVT, công ty) |
| `ecomCoefficient(companyId)` | :264–272 | đọc `configs` theo công ty, thiếu ⇒ dòng đầu, ≤ 0 ⇒ 1,3 |

Trình tự trong transaction (:104–141): `ensureUnitSet` → khoá `pcu` → đọc lại + khoá `pcc` → snapshot lịch sử → nhánh duyệt (`submitter->submit`) **hoặc** ghi thẳng (`writePrices` + `writeCompanyUnit` + `dropPendingApprovals`) → `history->logUpdate`. Thông báo gửi SAU commit (:144–148).

`ProductPriceSetWriter` (:19–101): `ensureUnitSet(productId, unitId, companyId, ?by): int` :39 (sinh đủ 6 dòng `upp` + `pcu` thiếu — BB3), `ensureProductSet(productId, companyId, ?by)` :66 (mọi ĐVT), `deleteProductSet` :80, `companiesWithStatus` :26.

`ProductPriceReader` (:19–216): `pricesByUnit` :26, `priceOf` :45, `costByUnit` :59, `retailPrices` :76, `costPrices` :96, `unitPrice` :159, `nearestExpectedDates` :186 — dùng cho khối "giá bán lẻ hiện hành", Chính sách (giá vốn công ty quản lý), Tạm tính.

**⇒ Chưa có hàm nào nhận "bộ giá mới + công ty tường minh" để ghi thẳng.** PTG phải tách một lối public, đề xuất:
`applyPriceSet(int $productId, int $productUnitId, int $companyId, array $resolved, float $cost, ?string $reason, int $by, array $allowStatuses)`
gom `ensureUnitSet + khoá + (submit | write*)` hiện nằm trong closure của `update()`; `update()` gọi lại nó với `companyId()` + `[3]`,
PTG gọi với công ty phiếu + `[1,2,3]` (hàng mới đang ở Chờ tính giá — cổng hiện tại chặn 423). Đây là refactor code G4 đã nghiệm thu ⇒ cần chạy lại PHPUnit MasterData (332 ca) + 2 spec e2e giá.

### 1.2 Nhánh gửi duyệt — `ProductPriceApprovalSubmitter`

- `submit(int $productId, int $productUnitId, int $companyId, array $resolved, array $data, int $by): array{approve_id, created}` :36 — public, công ty truyền tường minh (tốt cho PTG). Chạy TRONG transaction + khoá `pcu` của chỗ gọi.
- Ghi `*_wait_approve` + cờ 1 cho ô thực sự đổi (so giá đang chạy), giá vốn đổi ⇒ `pcu.price_wait_approve` + cờ 1.
- ≤ 1 `pa` mở / (hàng × ĐVT × công ty) — có thì **ghi đè** (BB6). **Không còn gì khác giá đang chạy ⇒ xoá `pa` cũ, trả `approve_id = null`** (:105–113).
- `createApprove(...)` :244–281 — snapshot mã/tên/model/thương hiệu/hãng, `department_id/part_id` lấy từ `auth()->user()->info` (người đang gửi), `status` để NULL.
- Quy chế: `ProductPriceListService::approvalRule(int $companyId)` :411–420 (đọc `companies.is_company_price`, `is_all_brand`, `brand_ids` CSV = id HÃNG SX) + `needsApproval(array $rule, $manufactureId)` :448–455. DB hiện: **cả 8 công ty `is_company_price = 0`** (không công ty nào bật).
- Bảng `pa` (DB): `id product_id product_unit_id … approved_id approved_time cost_price unit_coefficient created_by updated_by status company_id department_id part_id comment … reason_edit_price note_edit_price` — **không có cột nào trỏ về PTG**. `pa` hiện 0 dòng.

### 1.3 Duyệt / không duyệt — `ProductPriceApprovalService`

- `approve(array $items): array` :324, `applyApprove($pa, $edits, $showCost, $by)` :368–466; `reject(array $ids, $comment)` :491, `applyReject` :527–590. Công ty = công ty đang làm (`companyId()` :71) và chỉ `pa.company_id` của công ty đó.
- **Chuyển trạng thái hàng × công ty**: CHỈ ở :381–384 — khi `pa.company_id` = công ty QUẢN LÝ hàng **và** `products.status = 2` ⇒ `products.status = 1` + `markOwnerTrading()` :469–486 (ghi/tạo `pcc.status = 3` + `ensureProductSet`). Không duyệt :566–568 ⇒ `products.status = 5`. **Công ty khác: không đổi `pcc.status`** — docblock :27 ghi rõ "chốt ở Phase 7" (design G T3(c): duyệt khi `pcc` công ty mình = 2 ⇒ 3; không duyệt ⇒ giữ 2).
- Xong thì **xoá cứng `pa` + `pap`** (:454–455, :575–576) ⇒ sau khi duyệt, không còn dấu vết nào nối về PTG.
- Thông báo `[GIA]` cho `pa.updated_by` (người đề nghị) qua `ProductPriceNotifier::approved/rejected`.
- Điểm lệch 1–2 G5 (đã gỡ ở G6, commit `a26d16602`): bỏ đánh dấu nguồn bằng `pa.status = 1` và badge "Từ phiếu tính giá ERP"; mọi `pa` coi là HRM sinh, `status` NULL, duyệt/không duyệt LUÔN báo người đề nghị (Submitter docblock :20–23, ApprovalService :17–19, Notifier :16). Bản `pa` định dạng PTG ERP (`reason/note` NULL) vẫn đọc/duyệt được.

### 1.4 Hệ quả cho design PTG (phải chốt)

1. **Nối `pa` ↔ PTG**: Q5 cần "giá được duyệt ⇒ hàng Đang KD, YCTG/YCHG Đã tính giá, sinh KQ; từ chối ⇒ PTG mở lại". `pa` bị xoá cứng và không có cột PTG ⇒ phải (a) thêm cột vào `pa` (vd `price_calculate_id`, `price_calculate_product_id`) rồi `applyApprove/applyReject` gọi hook PTG trước khi xoá, hoặc (b) PTG tự giữ danh sách `pa_id` và nghe sự kiện duyệt. `pa` là bảng ERP dùng chung — thêm cột cần kiểm ERP không `insert` kiểu liệt kê cột cố định.
2. **1 PTG = nhiều `pa`** (mỗi hàng × ĐVT một `pa`). Trạng thái PTG "Đã duyệt" = khi mọi `pa` của phiếu được duyệt; một `pa` bị từ chối ⇒ cả phiếu hay chỉ dòng đó mở lại?
3. **Xung đột G4 ↔ PTG**: sửa giá nhanh ở G4 trên cùng (hàng, ĐVT, công ty) ⇒ `submit` ghi đè `pa` của PTG (BB6) hoặc nhánh ghi thẳng `dropPendingApprovals` xoá nó ⇒ PTG treo mãi ở "Chờ duyệt giá". Cần luật: chặn G4 khi hàng đang có PTG chờ duyệt, hoặc PTG coi `pa` mất = huỷ.
4. **PTG gửi đúng giá đang chạy** ⇒ `submit` trả `approve_id = null` (không có gì để duyệt). PTG phải coi là "đã áp ngay".
5. **Trạng thái "Đang tính giá" (K8) không tồn tại**: `ProductCompany` chỉ có 1 Đang nhập thông tin · 2 Chờ tính giá bán · 3 Đang KD · 4 Ngừng KD (`Entities/Product/ProductCompany.php:23–41`). DB: `pcc.status` = 3 (113.484 dòng) + NULL (298). Mockup dùng "Đang tính giá" ⇒ thêm mã 5, hay gộp vào 2?
6. `pcu.cost_price` = **giá nhập kho PTG theo ĐVT** (mockup: giá bán = tròn trăm(hệ số × giá nhập kho)) — duyệt ghi `pcu.cost_price = pa.cost_price` (:439–446), khớp.
7. Duyệt ở công ty KHÔNG quản lý hàng: phải bổ sung nhánh `pcc.status` 2 ⇒ 3 (T3(c)) vào `applyApprove`, nhánh ghi thẳng PTG cũng phải tự chuyển trạng thái (G4 không chuyển vì G4 chỉ chạy ở trạng thái 3).

---

## 2. Quyền

| Kiểm | Kết quả |
|---|---|
| Seeder chính | `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (1.590 dòng, **truncate cả bảng** — không chạy trên DB thật). Id lớn nhất (không tính dòng comment): **1675** (:1579). Id trùng `uniq -d` chỉ rơi vào dòng đã comment (7, 8, 16, 91…) ⇒ 0 trùng thật |
| 1092 | :1061 `Xem giá vốn hàng hoá`, nhóm "Báo giá", type 4 — có trong DB |
| 1652/1653/1655 | :1582–1584, nhóm "Hàng hoá", type 9 — có trong DB |
| 1654, 1656 | **giữ chỗ, chưa seed** (comment :1572, :1581). 1654 = *Xuất excel danh sách hàng hoá* (2-E), **1656 = *Cấu hình chính sách giá bán nội bộ*** (`man-danh-muc-hang-hoa/design.md:3200–3202`, :3226) |
| 1657/1658 | :1587–1588, type 8 (Tài chính), nhóm "Hàng hoá" — có trong DB |
| Bảng `permissions` (guard api) | max id **1678**, 813 dòng. 1676–1678 = báo cáo CSKH tiềm năng (nhánh khác, chưa có trong seeder nhánh này) |
| `origin/gop_db` (GitHub, mới nhất) | id ≥ 1650 đang dùng: 1650, 1651, 1660, 1661, **1676–1698**. Không có 1652–1659, 1662–1669 |
| Mọi nhánh local/remote đã fetch | không nhánh nào dùng 1659, 1662–1669 hay ≥ 1699 |
| ⚠️ DB local lệch seeder | DB còn quyền xe ở **1620–1631** (bản cũ), seeder nhánh đã đổi sang 1640–1651 (memory "danh mục hàng hoá + xe đã gộp gop_db") — không ảnh hưởng 3 id mới nhưng đừng dùng DB làm nguồn duy nhất |

**`ProductPricePermissionSeeder`** (`Modules/MasterData/Database/Seeders/ProductPricePermissionSeeder.php`, 77 dòng): hằng `PERMISSIONS = [id => tên]`, `GUARD='api'`, `GROUP='Hàng hoá'`, `TYPE=8`. Trong transaction: id đã có đúng tên+guard ⇒ bỏ qua; id bị quyền khác chiếm hoặc tên đã nằm ở id khác ⇒ `RuntimeException`, không ghi gì; chèn bằng `DB::table('permissions')->insert` (không truncate); xong `forgetCachedPermissions()` (bắt lỗi). **Không gán role** (kể cả Super admin 18). Có PHPUnit `ProductPricePermissionSeederTest` 4 ca. Khuôn Finance `*PermissionSeeder` khác: `updateOrInsert` + gán role 18 + role có quyền ERP cùng tên — Phase 7 KHÔNG theo khuôn đó.

**Đề xuất id Phase 7** (trống cả DB, seeder nhánh, `gop_db`):
- **1662, 1663, 1664** cho 3 quyền (1) *PTKD duyệt yêu cầu hỏi giá* · (2) *XNK xử lý yêu cầu hỏi giá* · (3) *Tính giá bán hàng hoá*.
- **1656** *Cấu hình chính sách giá bán nội bộ* (đã giữ chỗ) — seed cùng đợt T1.
- Cách làm: seeder riêng mới (vd `PriceCalculationPermissionSeeder`) chép khuôn `ProductPricePermissionSeeder` với 4 id, + thêm 4 dòng vào `PermissionsTableSeeder` cho khớp. Loại `type`: 8 (Tài chính) như 1657/1658 nếu 3 màn đặt ở phân hệ Kế toán.
- Trước khi merge: kiểm lại `gh api …/PermissionsTableSeeder.php?ref=gop_db` (gop_db đang tăng nhanh, 1679–1698 mới thêm trong vài ngày).

---

## 3. Phân công XNK (`assign_histories`, `assign_employee_ballots`)

- **HRM chưa có model/service/route nào** đọc `assign_histories`, `assign_employee_ballots`, `assign_employee_manufactures` hay `buy_employee_id` (grep toàn `Modules/` + `app/` = 0). Bảng có sẵn trong DB gộp.
- Cột `assign_histories`: `id, brand_id, manufactures_id, brand_department_id, buy_department_id, brand_employee_id, buy_employee_id, employee_date_from, employee_date_to, date_from, date_to, department_type, employee_type, created_by, updated_by, company_id`.
- Dữ liệu: 2.257 dòng, 1.135 dòng `employee_date_to IS NULL`; có `buy_employee_id` theo công ty: **Cty 1: 791 · Cty 3: 1 · Cty 4: 75** (ton.md ghi "chỉ 1 và 4" — thực tế Cty 3 có 1 cặp). **0 bộ (brand, manufacture, company) có 2 người hiệu lực** ⇒ tra 1 người/nhóm là an toàn.
- `buy_employee_id` = `employees.id` (bảng user HRM `App\Models\TpEmployee` → `employees`): 0 id mồ côi; ví dụ 581 thuyntt.xnk@…, 1073 namnd.xnk@… ⇒ so thẳng với `auth()->id()`, tên lấy qua `employees.employee_info_id → employee_infos.fullname`.
- `assign_employee_manufactures` (đã tồn tại — ERP, dòng chi tiết phiếu `assign_employee_ballots`): `assign_employee_ballot_id, brand_id, manufactures_id, brand_employee_id/name, buy_employee_id/name, …` — **không có `company_id`**, công ty nằm ở phiếu (`assign_employee_ballots.company_id`, có `status`, `approved_by/time`). §33q định tạo bảng mới cùng tên ⇒ **trùng tên bảng ERP**, đúng là không được tạo.
- **Truy vấn "XNK hiệu lực"** của (brand, manufacture, company phiếu):
  ```sql
  SELECT buy_employee_id FROM assign_histories
  WHERE brand_id = ? AND manufactures_id = ? AND company_id = ?
    AND employee_date_to IS NULL AND buy_employee_id IS NOT NULL
  ORDER BY id DESC LIMIT 1
  ```
  Nên thêm `employee_date_from <= CURDATE()` nếu ERP cho phép khai trước ngày (cần soát `AssignEmployeeController` ERP). Đặt 1 service đọc dùng chung (vd `Modules/MasterData/Services/PriceCalculation/BuyerAssignmentReader`) cho cả YCHG (chặn gửi nhóm chưa phân công), gate BE nhóm, và danh sách "nhóm chờ tôi lập YCTG".
- ⚠️ Đổi người phụ trách qua "Bàn giao công việc" (K7): HRM `Modules/Assign/Services/HandoverService.php` **không đụng** `assign_histories` ⇒ màn Phân công vẫn ở ERP; nhóm đã giao cho XNK cũ thì ai xử lý? (ERP ghi `buy_employee_id` vào phiếu lúc PTKD duyệt hay tra lại mỗi lần?) — cần chốt.

---

## 4. Thông báo

- Helper BE: `Modules/Timesheet/Services/EmployeeInfoService.php` `sendNotification($to_employee_info_id, $data, …)` :466 và `sendToAllNotification($employee_info_ids, $data, …)` :519. Nhận **`employee_info_id`**, không phải `employees.id`.
- Khuôn gần nhất để chép: `Modules/MasterData/Services/ProductPrice/ProductPriceNotifier.php` (149 dòng): `PREFIX`, `content($action, $object, $note)` :127–141 (tên ≤ 50, tổng ≤ 120, cắt ghi chú trước, `<b>` quanh tên, `e()` escape), `approverInfoIds($companyId)` :73–88 (người có quyền X **tại công ty** qua `role_has_permissions.company_id` + `employee_has_roles.company_id`), `infoIdsOfEmployees` :90–102, `send()` :105–115 nuốt lỗi + `report()`; gửi SAU commit.
- Skill `HRM/.claude/skills/notification-convention/SKILL.md`: `[PREFIX] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú}`; nhóm hành động **chỉ 14 giá trị** (Tạo mới · Cập nhật · Chờ duyệt · Đã duyệt · Từ chối · Yêu cầu làm lại · Góp ý · Sắp đến hạn · Quá hạn · Hủy · Tạm dừng · Tiếp tục · Thay đổi lịch · Nhắc báo cáo); prefix 3–5 ký tự viết hoa, **đối tượng mới phải hỏi user xác nhận prefix**; tên ≤ 50, tổng ≤ 120; `url` deep-link bắt buộc **kèm ID**; gửi ngay khi event.
- Áp vào Q16 (đề xuất, cần user chốt prefix): `[YCHG]` / `[YCTG]` / `[PTG]` (theo mã phiếu PYCHG-/YCTG-/PTG-), tên đối tượng = số phiếu (+ tên nhóm hãng ở thông báo theo nhóm). Ánh xạ hành động: gửi YCHG → `Chờ duyệt`; PTKD duyệt → `Đã duyệt` (gửi XNK từng nhóm); PTKD không duyệt → `Từ chối`; gửi YCTG → `Chờ duyệt` (người có quyền Tính giá bán của công ty phiếu); KTMH trả → `Yêu cầu làm lại`; giá được áp → `Đã duyệt` link `…/price-asking-requests/{id}?group={gid}&show_result=1`; đủ nhóm → `Cập nhật`? (không có nhóm "Hoàn thành" — cần chốt). Người nhận theo quyền: tái dùng `approverInfoIds()` đổi tên quyền.

---

## 5. Chính sách giá bán nội bộ (§28, quyền 1656)

- **HRM chưa có gì**: không bảng (`SHOW TABLES LIKE '%polic%'` chỉ ra `allowance_policies`, `business_policies`, `deduction_policies`; `'%internal%'` chỉ `internal_business_scopes`), không route, không page, không component (grep `internal_price|price_polic|PricePolic` = 0). Quyền 1656 chưa seed.
- Thiết kế §28 (`man-danh-muc-hang-hoa/design.md:1849–2022`) — tóm:
  - **Bản ghi** (§28c): `owner_company_id` (công ty BÁN = công ty đang làm) · `manufacture_id` (Hãng SX — bảng `manufactures`, 1.071 dòng) · `target_company_id` (MỘT công ty mua) · `base_type` (1 Theo giá vốn / 2 Theo giá bán) · `percent_import_lot` · `percent_stock` · audit. **UNIQUE (owner × hãng × công ty mua)**. Chỉ thấy/sửa cấu hình công ty mình — chặn BE.
  - ⚠️ Màn §28d chốt "Cách tính" **theo hãng** (1 lựa chọn cho cả hãng) trong khi bản ghi để `base_type` ở từng dòng công ty ⇒ design phải chọn: tách bảng cha `(owner, manufacture, base_type, mode)` + bảng con `(target_company, 2 %)`, hoặc lặp `base_type` và ép đồng nhất khi lưu. Tuỳ chọn toàn cục §28d-quater "Hệ số theo công ty / Hệ số chung" cũng cần chỗ lưu (theo owner).
  - **Công thức** (§28b): giá vốn ⇒ `giá vốn công ty bán × (1 + %)`; giá bán ⇒ `mỗi loại giá × (1 − %)` (đủ 6 loại), tròn trăm. **Chỉ là số gợi ý**, không ghi bảng giá; không ngày hiệu lực; lịch sử vào `catalog_histories`; độc lập `manufacture_expect_prices` / `company_price_types`.
  - **Màn** `/master-data/internal-price-policies`: 1 lưới hãng gộp dòng × công ty mua là dòng; nhập tại chỗ, lưu theo hãng; popup Chọn hãng (tick nhiều, tối đa 80 dòng/lượt), Xem trước giá, Lịch sử (khuôn entity-history), Import/Xuất Excel, unsaved popup; không cuộn ngang.
  - Tồn §28f chưa chốt: quyền riêng hay chung (đã có 1656 ⇒ coi như riêng) · trần % · khai hãng chưa có hàng · công ty mua ngừng hợp tác.
  - Phase 7 dùng ở khối **Chính sách** của PTG (Q2) và **chụp chính sách** vào dòng PTG (Q13) ⇒ dòng PTG cần cột chụp `base_type`, 2 %, công ty quản lý, giá vốn/giá bán công ty quản lý tại lúc lưu.

---

## 6. Danh mục cho form

| Danh mục | HRM đã có API? | Ghi chú |
|---|---|---|
| `costs` type 8 (GIA_HANG_HOA) | **Chưa có endpoint lọc type 8.** Hằng có: `Modules/CustomerCare/Entities/Cost/Cost.php:172` `TYPE_GIA_HH = 8`. Các API hiện: `GET /finance/product-import-requests/costs` (`ProductImportRequestService::costOptions()` :1370 — **mọi** `costs`, không lọc type/status), `GET /…/buy-service-requests/costs`, CRUD `customer-care/costs` (chỉ `kind_of = 2`) | DB: 7 dòng type 8 (id 56–62: Cước vận tải quốc tế, Vận chuyển nội địa, Phí kiểm định, Bốc vác, **Thuế nhập khẩu**, Chi phí khác, Bảo hiểm hàng hoá), `kind_of = 1`. ⚠️ "Thuế nhập khẩu" là 1 chi phí ⇒ trùng với ô thuế NK riêng? cần soát ERP |
| `currencies` + `exchange_rate` | Có: `GET /finance/currencies/getAll` (`CurrencyController`, `Modules/Finance/Routes/api.php:127`, không gate); `GET assign/bom-lists/currencies` (`BomListController::getCurrencies` :622, **`DB::connection('mysql2')`**) | DB: VNĐ 1, USD 26.180, EUR 30.800,59… Dùng `/finance/currencies/getAll` (đọc DB mặc định) |
| `price_types` | Có: `GET assign/quotations/price-types` (`QuotationController::priceTypes` :931, **`mysql2`**, cache 10′) | 6 loại (1 Bán lẻ … 6 TMĐT). FE `utils/productPriceModel.js:25` đã hard-code `PRICE_TYPES` + `TYPE_ORDER` ⇒ không cần API |
| `configs.coefficient_ecommerce_price` | Không có API đọc riêng; BE đọc trong `ProductPriceUpdateService::ecomCoefficient()` :264; màn Quy định ghi qua `RegulationTabRegistry.php:214` (store `config`) | 1,3 ở cả 8 công ty; FE hằng `ECOM = 1.3` (`productPriceModel.js:22`). PTG nên trả hệ số trong payload form |

⚠️ `.env` worktree: `DB_DATABASE_SECOND=erp2326` ⇒ mọi chỗ `connection('mysql2')` đọc **DB khác** `hrm_erp_giacty` (memory "Merge sang nhánh gộp DB → đổi cách query ERP"). Phase 7 chỉ dùng connection mặc định.

---

## 7. FE tái dùng + vị trí menu

- **`utils/productPriceModel.js`** (366 dòng): hằng `ECOM`, `PRICE_TYPES`, `TYPE_ORDER`, `ECOM_TYPE`, `RETAIL_TYPE`, `MONEY_MAX`; `Calc` :138–211 (T1 hệ số ⇒ giá tròn trăm `setCoef` · T2 Bán lẻ lan 2–5 `spread` · T3 TMĐT `ecom` · T4 `toggleManual` · T7 `setExpCoef` · `addExpected`); `unitFromApi` :96, `validateUnit` :238, `buildPayload` :272, `blockRows` :213, `coefToPrice` :331, `approvalRowsFromApi` :316. Hàm thuần — PTG dùng thẳng, coi "giá nhập kho" là `u.cost`. Đúng Q6.
- **Component G4/G5** (`components/product/price/`): `ProductPriceTable.vue` (839 dòng — gắn chặt màn danh sách: props `items/bases/drafts/unitIdx/locked/stock`, :373–390 ⇒ **khó nhúng vào form PTG**, nên dựng bảng PTG mới dùng `Calc`), `ProductPriceApprovalTable.vue` (519), `ProductPriceHistoryModal.vue` (55), `ProductRecipeModal.vue` (76 — popup "giá công thức", gần với popup Tạm tính).
- **Khuôn list-page**: `pages/finance/product-prices/index.vue` (625 dòng: `V2BaseSmartFilterPanel`, `V2BaseSelect`, `V2BasePagination`, `CheckPermission`, `unsavedChangesMixin`, `scrollToFirstError`) và `pages/finance/product-price-approvals/index.vue` (687). Nhớ memory "Skill vs repo thật (list-page)" + "2 lỗi bộ lọc âm thầm".
- **Popup in**: `components/print/ReportPrintPreviewModal.vue` + `utils/mixins/reportPrintPreviewMixin.js` (`openPrintDetail(endpointBase, id, title)` :59 gọi `{base}/{id}/print-data`; `openPrintList` :64 gọi `{base}/print-list-data`) + `utils/print/reportPrintStyle.js`.
- **Menu hiện có**:
  - `components/subsystem-menu/finance.js:437–451` nhóm rail **"Quản lý giá - CTKM"** → mục "Giá bán": `{ label: 'Phiếu tính giá' }` :444 (**chưa link**), Cập nhật giá bán :445, Duyệt giá bán :446, Cập nhật giá theo hãng (xám), 2 link ERP. Nhóm "Giá bán chờ duyệt" :586–594.
  - `components/subsystem-menu/presale.js:53–59` "**Yêu cầu tính giá bán**" → `/assign/pricing-requests` (màn khác hẳn — yêu cầu báo giá dự án, user chốt tên 25/09). `sale.js:43` gate nó bằng quyền "Xây dựng giá bán theo công ty/phòng".
  - `components/subsystem-menu/sale-hub.js:165` nhóm "Khởi tạo › Hàng hóa" có chữ **'YC hỏi giá'** chưa link (placeholder đúng chỗ cho YCHG — người KD lập phiếu).
  - `components/subsystem-menu/master-data.js:59–85` nhóm "Hàng hoá" (4 màn) + "Phân loại hàng hóa" :86–123.
- **Đề xuất vị trí**:
  - 3 chứng từ ở `finance.js` mục "Giá bán" (nhóm rail Quản lý giá - CTKM), thay dòng "Phiếu tính giá" bằng 3 mục theo thứ tự luồng: **Yêu cầu hỏi giá** (mọi người — không gate) · **Yêu cầu tính giá** (isShow: XNK xử lý | Tính giá bán | 1092) · **Phiếu tính giá** (isShow: Tính giá bán | XNK xử lý | 1092) · rồi Cập nhật giá bán · Duyệt giá bán. Khớp mockup "cụm tính giá" + D9 (2 màn giá đã ở đây).
  - Gắn link `sale-hub.js:165` 'YC hỏi giá' → `/finance/price-asking-requests` (lối vào cho KD), **giữ nguyên nhãn** (nhãn là `menuKey`, đổi là mất cấu hình bật/tắt menu — chú thích :146–147).
  - **Đổi tên/không đụng `presale.js:56`**: tên "Yêu cầu tính giá bán" trùng nghĩa với "Yêu cầu tính giá" mới ⇒ người dùng dễ nhầm. Không đổi được nhãn tuỳ tiện (user chốt 25/09 theo sheet) ⇒ hỏi user: giữ, hay đặt tên chứng từ mới khác đi (vd "Yêu cầu tính giá nhập" / giữ "Yêu cầu tính giá" + ghi chú).
  - **Chính sách giá bán nội bộ**: §28d chốt URL `/master-data/internal-price-policies` ⇒ thêm vào `master-data.js` nhóm "Hàng hoá" (sau "Hàng đang kinh doanh"), isShow `['Cấu hình chính sách giá bán nội bộ']`. Phương án khác: đặt cùng cụm "Giá bán" ở finance.js (gần nơi dùng). Cần user chốt.
  - Route FE đề xuất: `/finance/price-asking-requests`, `/finance/price-calculate-requests`, `/finance/price-calculates` (theo tên bảng ERP — tránh tên file `_ten-co-gach.vue`, memory "Nuxt route động có dấu gạch ngang"). Page phân hệ hub phải khai `layout: 'default-sidebar'` (memory "Topbar 2 cấp vs hub 3 cấp").

---

## 8. Bản in

- **Chuẩn hiện hành** (skill `print-page` mục 0, 8): nút In mở popup `ReportPrintPreviewModal`; BE trả `{ data: { template: '<html>' } }` qua `GET …/{id}/print-data`. Không dựng trang `/print`.
- **2 cách dựng HTML ở BE đang có**:
  1. Mẫu ERP trong bảng **`report_templates`** (476 dòng, cột `code, name, template, example`), điền placeholder + `{{HEADER}}` bằng trait `Modules/CustomerCare/Services/Concerns/PrintsCompanyLetterhead.php` (`letterheadUrl($companyId)` — theo `company_id` TRÊN CHỨNG TỪ). Ví dụ: `Modules/Assign/Services/ProductExportRequestPrintService.php`, `WarehouseExportRequestPrintService.php`, `Modules/Finance/Services/BillIncomeRequestPrintService.php`.
  2. **Blade tự dựng** `Modules/Finance/Resources/views/prints/_layout.blade.php` (25 file mẫu: `product-prepick-request`, `borrow-export-request`…; biến `$header, $title, $code, $createdAt, $infoRows[], $tableHtml, $signers[]`, CSS inline). Dùng khi ERP không có mẫu — vì `report_templates` là bảng dùng chung với ERP, HRM **không ghi thêm dòng** vào đó (docblock _layout :4–7). Controller mẫu: `WarehousePrepickRequestController::printData` :175–186.
- `print_templates` / `hrm_print_templates` là mẫu của chứng từ HRM gốc (biên bản họp…), không dùng cho luồng này.
- **Mẫu có sẵn cho 4 bản in**: `report_templates` id **98 `YC_HOI_GIA`** (975 byte) và **99 `YC_TINH_GIA`** (1.285 byte, gồm bảng hàng + bảng chi phí). **PTG (id 100) thiếu trong DB, KQ chưa có hằng** (khao-sat-be-erp.md:295) ⇒ PTG + "In kết quả" dựng bằng blade `_layout` (Q17 "thiết kế mẫu mới"). Mẫu YCHG ERP là phiếu 1 nhóm ⇒ YCHG gom nhóm La Mã/1-2-3 nhiều khả năng cũng phải dựng blade (mẫu 98 không có cấp nhóm).
- Định dạng theo skill: số `1,234,567`, chữ 13px / bảng 10px Times New Roman, A4 dọc, letterhead theo `company_id` phiếu, khối ký `pr-sign`. Ẩn giá vốn / giá NCC theo 1092 ở bản in YCTG/PTG; bản In kết quả chỉ giá bán (Q20).

---

## 9. Rủi ro tổng hợp

| # | Rủi ro | Mức |
|---|---|---|
| R1 | Lối ghi giá G4 gắn cứng công ty đang làm + chỉ trạng thái 3 + hàm ghi private ⇒ phải refactor code G4/G5 đã nghiệm thu (chạy lại 332 PHPUnit + e2e giá) | cao |
| R2 | `pa` xoá cứng, không có cột PTG ⇒ không biết khi nào PTG "được duyệt" nếu không thêm cột/hook vào bảng ERP dùng chung | cao |
| R3 | G4 sửa nhanh ghi đè/xoá `pa` của PTG ⇒ PTG treo | trung bình |
| R4 | Trạng thái "Đang tính giá" chưa có mã ⇒ thêm mã 5 kéo theo mọi chỗ đọc `pcc.status` (lọc 4 màn hàng hoá, `ProductCompany::STATUS_*`, popup lấy về, cron ERP 14:30?) | trung bình |
| R5 | Phân công XNK chỉ có ở Cty 1 (791), 4 (75), 3 (1) ⇒ Cty 2/5/6/7/8 gửi YCHG là bị chặn toàn bộ tới khi khai ở ERP | nghiệp vụ |
| R6 | Id quyền: `gop_db` vừa chiếm 1676–1698 trong vài ngày; 1662–1664 phải kiểm lại ngay trước merge | thấp |
| R7 | `mysql2` = `erp2326` ở worktree — copy API currencies/price-types cũ là đọc nhầm DB | thấp |
| R8 | DB local `permissions` lệch seeder (xe 1620–1631 vs 1640–1651) — e2e cấp quyền theo tên thì ổn, theo id thì sai | thấp |

## 10. Câu hỏi cần user chốt (ngoài Q1–Q20)

1. **Trạng thái "Đang tính giá"** (K8): thêm mã `pcc.status = 5`, hay giữ 4 trạng thái và hiểu "Đang tính giá" = vẫn 2 Chờ tính giá (chỉ phiếu đổi trạng thái)?
2. **Nối PTG ↔ duyệt giá**: cho thêm cột vào `product_approves` (bảng ERP, đang 0 dòng) để biết `pa` thuộc PTG nào — hay PTG tự giữ danh sách `pa`?
3. **Một dòng PTG bị từ chối** ở màn Duyệt giá bán: mở lại cả phiếu, hay chỉ dòng đó (các dòng đã duyệt giữ giá)?
4. **G4 sửa giá nhanh khi hàng đang có PTG chờ duyệt**: chặn G4, hay cho G4 thắng và PTG tự huỷ dòng đó?
5. **Prefix thông báo**: `[YCHG]` / `[YCTG]` / `[PTG]`? và mốc "đủ nhóm ⇒ báo người lập YCHG" dùng nhóm hành động nào trong 14 giá trị (đề xuất `Cập nhật`)?
6. **Id quyền**: dùng 1662/1663/1664 cho 3 quyền mới + seed 1656 cùng đợt T1, type 8 (Tài chính)?
7. **Menu**: 3 chứng từ vào `finance.js` mục "Giá bán" (thay "Phiếu tính giá") + gắn link 'YC hỏi giá' ở sale-hub; màn Chính sách vào `master-data.js` nhóm "Hàng hoá" (URL §28d) hay cụm "Giá bán" ở finance? Xử lý tên trùng `presale.js:56` "Yêu cầu tính giá bán" thế nào?
8. **Chi phí "Thuế nhập khẩu" (costs id 60)** đang là 1 dòng chi phí type 8, trong khi YCTG có ô thuế NK riêng — ẩn dòng 60 khỏi tab Chi phí hay giữ như ERP?
9. **§28 cấu trúc**: "Cách tính" theo hãng (màn) vs `base_type` theo dòng công ty (bản ghi) — tách bảng cha/con hay lặp cột? Và 4 tồn §28f (trần %, khai hãng chưa có hàng, công ty ngừng hợp tác).
10. **XNK đổi người giữa chừng**: nhóm đã giao (PTKD duyệt) cho XNK cũ thì ai lập YCTG — người ghi lúc duyệt, hay tra lại phân công hiệu lực tại thời điểm thao tác?
