# Báo cáo hạn mức công nợ nhân viên — plan

> Người phụ trách: @khoipv · Nhánh: `develop` (con của `gop_db`) cả 2 repo
> Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-10-14-report-limit-debt-employees-design.md`

## Quyết định đã chốt (14/10/2026)
- Hạn mức: y ERP `employees.limit_export_debt` (hiện chưa NV nào khai → màn trống).
- Phạm vi: không quyền, xem mọi công ty (y ERP).
- Sửa lỗi ERP như bản KH (công thức sổ 131 chung, ô lọc NV, popup theo KH).

## Phase 1 — Port màn

### BE (`hrm-api/Modules/Finance`)
- [x] `Services/CustomerDebt/ReportLimitDebtEmployeeService.php` — danh sách + lọc + sort + phân trang PHP, công nợ qua `CustomerDebtAggregator` (gom `contract_created_by`), popup theo KH, export-rows
- [x] `Http/Controllers/V1/ReportLimitDebtEmployeeController.php` — index / meta / export-rows / customers
- [x] Route `finance/report-limit-debt-employees` (không checkPermission — ERP không gate)
- [x] Docblock "Nơi đang dùng" của `CustomerDebtAggregator`
- [x] Smoke test service (transaction gán tạm hạn mức 5 NV rồi rollback) + HTTP kernel (200 / 404 / 422)

### FE (`hrm-client`)
- [x] `pages/finance/report-limit-debt-employees/index.vue` — SmartFilterPanel floating (Thời gian · Công ty/PB/BP/NV · Chỉ tiêu) + V2BaseDataTable + Cấu hình cột + Xuất Excel
- [x] `components/DebtByCustomerModal.vue` — popup dư nợ NV theo KH (lọc KH / Số tiền từ / đến)
- [x] Menu `components/subsystem-menu/finance.js` — gắn link mục "Báo cáo hạn mức công nợ nhân viên"
- [x] Compile check (vue-template-compiler + babel) + grep checklist skill

## Phase 2 — Ô nhập "Hạn mức công nợ xuất hàng" ở form Tài khoản nhân viên (user chốt 14/10/2026)

Lý do: ERP đã bỏ ô này khỏi form SỬA tài khoản từ 12/11/2022 (commit `a7e8387700`), chỉ còn ở form Thêm → không ai khai
được, báo cáo trống. Thêm vào form HRM `/human/employee` (Quản trị hệ thống › Người dùng & phân quyền › Tài khoản nhân viên).

- [x] BE `CreateEmployeeRequest` / `UpdateEmployeeRequest` — `limit_export_debt` nullable|numeric|min:0|max + message tiếng Việt
- [x] BE `EmployeeService::createEmployee/updateEmployee` — ghi `employees.limit_export_debt` (update chỉ ghi khi request có key)
- [x] BE lịch sử: thêm `limit_export_debt` vào `buildHistorySnapshot` + điều kiện `$nonStatusChanged`
- [x] FE `components/human-components/employee/EmployeeForm.vue` — ô tiền `V2BaseCurrencyInput` + lỗi inline
- [x] FE `EmployeeHistoryModal.vue` — nhãn trường + định dạng số `1,234,567` + option lọc trường
- [x] Smoke test (transaction rollback) + compile
- [x] (user báo 14/10) Vào `/human/employee/add` tự hiện "0 chức năng khớp <email>": Chrome tự điền tài khoản đã lưu, Email bị `disabled` nên email rơi vào ô "Tìm chức năng…" của `SaleHubSidebar` → 2 ô mật khẩu `autocomplete="new-password"` (lỗi có sẵn, không do Phase 2)
- [x] (user báo 14/10) Dời ô xuống cuối cột trái (sau Mã check in cơm); ép cỡ chữ/cao/padding về đúng `.form-control` (V2BaseCurrencyInput md là 14px/38px, form này 0.8rem)

## Phase 3 — Bộ lọc popup theo khuôn base (user yêu cầu 14/10/2026)

- [x] FE `DebtByCustomerModal.vue` — bỏ lưới ô lọc tự dựng, thay `V2BaseSmartFilterPanel floating in-modal` (skill modal-popup 4c): ô tìm nhanh + Khách hàng (chọn là tìm luôn) + Số tiền từ → đến gộp 1 ô (slot `#field-money_range`, khuôn `bill-adjust-dept-requests`), Enter/Tìm kiếm, Làm mới
- [x] BE `debtByCustomer` — thêm `keyword` (mã / tên KH, không phân biệt hoa thường); options ô Khách hàng vẫn là đủ KH
- [x] Compile + test service (kw mã 1 dòng, kw tên khớp đúng, kw rác 0, kw + số tiền kết hợp)
- [x] (user yêu cầu 14/10) Commit + push `develop` cả 2 repo: API `0b71cfa32`, Client `3da3329aa` (rebase lên origin, không xung đột)

### Checkpoint — 2026-10-14
Vừa hoàn thành: BE + FE + menu. Smoke test (dữ liệu tạm trong transaction, đã rollback): 5 NV ~1,2s; chỉ tiêu Trong 4 / Vượt 1; từ khoá, ô NV, Công ty, Phòng ban, sort đúng; popup 65 KH tổng 167,134,531 = cột chính; lọc Số tiền từ ăn; NV không hạn mức → 404; Đến ngày < Từ ngày → 422 tiếng Việt.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt kiểm `/finance/report-limit-debt-employees` (chưa bấm thật). DB không NV nào có hạn mức → muốn thấy dữ liệu phải tự khai `employees.limit_export_debt` cho vài NV.
Blocked:

### Checkpoint — 2026-10-14 (Phase 2)
Vừa hoàn thành: ô "Hạn mức công nợ xuất hàng" ở form Tài khoản nhân viên (`/human/employee` Thêm + Sửa) + ghi lịch sử. Smoke test HTTP (transaction, đã rollback): GET chi tiết trả `limit_export_debt`; nhập -5 → 400 "Hạn mức công nợ xuất hàng không được âm"; lưu 150,000,000 → DB đúng, log `update` 0 → 150000000, báo cáo NV ra 1 dòng; PUT không gửi khoá → giữ nguyên hạn mức. Compile FE pass.
Đang làm dở: —
Bước tiếp theo: user mở `/human/employee` → Sửa 1 tài khoản → nhập hạn mức → Lưu → mở `/finance/report-limit-debt-employees` kiểm (chưa bấm thật trình duyệt).
Blocked:

## Phase 4 — Chú thích ⓘ tiêu đề + đầu cột (Redmine #11724, 16/10/2026)

Yêu cầu: đồng bộ báo cáo với mẫu `/assign/report/customer-market-development` — tiêu đề + mọi đầu cột có icon ⓘ
popover mô tả, cột tính toán ghi cả cách tính. Dùng `components/report/ReportInfoTip.vue` (bản dùng chung, #11621).

- [x] FE `components/V2BaseDataTable.vue` — thêm tuỳ chọn KHÔNG bắt buộc: prop `titleTip` + khoá `tip` trên cột → vẽ `ReportInfoTip` (màn không truyền thì không đổi)
- [x] FE `pages/finance/report-limit-debt-employees/index.vue` — `titleTip` + `tip` cho 7 cột (công thức cột Tổng công nợ)
- [x] FE `components/DebtByCustomerModal.vue` — `tip` cho 4 cột popup + ⓘ cạnh tiêu đề popup (slot `title-suffix`)
- [x] Compile check (vue-template-compiler + babel)

### Checkpoint — 2026-10-16 (Phase 4, #11724)
Vừa hoàn thành: ⓘ tiêu đề "Báo cáo hạn mức công nợ nhân viên" + 7 đầu cột (cột Tổng công nợ ghi công thức dư cuối kỳ y `CustomerDebtAggregator::finalize`, điều kiện Trong/Vượt hạn mức); popup theo KH: ⓘ tiêu đề + 4 cột + dòng Tổng công nợ. `V2BaseDataTable` thêm opt-in `titleTip` + `column.tip` (grep: không màn nào khác đang khai `tip` trên cột → không ảnh hưởng). Compile 3 file pass.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt hover kiểm (chưa test thật); chưa commit.
Blocked:
- [x] (user chốt 16/10) CHỈ chú thích 2 cột "Hạn mức công nợ xuất hàng" + "Tổng công nợ khách hàng hiện tại": bỏ ⓘ tiêu đề, 5 cột còn lại và toàn bộ popup; gỡ prop `titleTip` khỏi `V2BaseDataTable` (chỉ giữ opt-in `column.tip`)

## Phase 5 — Xuất Excel khi không có dữ liệu (Redmine #11725, 16/10/2026)

Lỗi: 0 dòng → toast "Không có dữ liệu để xuất", không ra file. Yêu cầu: vẫn xuất đủ letterhead + tiêu đề + đầu cột + khối ký, phần dữ liệu để trống.
Nguyên nhân: `utils/export/listExportFile.js::exportListFile` `return 0` khi `rows` rỗng (không dựng file).

- [x] FE `utils/export/listExportFile.js` — opt-in `allowEmpty` (mặc định false: các màn khác giữ nguyên): rỗng vẫn dựng + tải file
- [x] FE `pages/finance/report-limit-debt-employees/index.vue` — truyền `allowEmpty: true`, bỏ toast lỗi khi 0 dòng
- [x] Compile + dựng thử file 0 dòng bằng node (ExcelJS) kiểm tiêu đề/đầu cột

### Checkpoint — 2026-10-16 (Phase 5, #11725)
Vừa hoàn thành: `exportListFile` thêm opt-in `allowEmpty` (headings rỗng thì vẫn không dựng); màn báo cáo hạn mức công nợ NV truyền `allowEmpty: true`, bỏ toast "Không có dữ liệu để xuất". Chạy thử bằng node (babel + ExcelJS, store giả trả 0 dòng): không opt-in → không ra file (giữ khuôn cũ cho ~20 màn khác); opt-in → file có dòng tiêu đề + 7 đầu cột + khối ký, không dòng dữ liệu. Compile pass.
Đang làm dở: —
Bước tiếp theo: user bấm Xuất Excel thật trên trình duyệt khi bảng trống (chưa test trình duyệt, letterhead chưa kiểm ở ca rỗng — cùng nhánh code với ca có dữ liệu); chưa commit.
Blocked:

## Phase 6 — Lỗi UI/UX (Redmine #11726, 16/10/2026)

- [x] Bug 1 — FE `DebtByCustomerModal.vue`: cột Công nợ mở popup đang hiện ↓ (như đã chọn sắp xếp) → mặc định icon trung tính ⇅ như các cột khác (dữ liệu vẫn lớn → nhỏ); bấm mới hiện ↑/↓
- [x] Bug 2 — BE `ReportLimitDebtEmployeeService::sort`: mặc định xếp theo `employees.updated_at` giảm dần (tài khoản vừa cập nhật lên đầu), hoà thì `id` giảm dần — thay cho ngày tạo NV (y ERP)
- [x] Verify: php -l + chạy service; compile FE

### Checkpoint — 2026-10-16 (Phase 6, #11726)
Vừa hoàn thành: Bug 1 popup — thêm `sortField` ('' lúc mở/mở lại) truyền vào `sortBy` của V2BaseDataTable → icon ⇅, bấm mới ↑/↓; dữ liệu mặc định vẫn lớn → nhỏ. Bug 2 — BE sort mặc định `employees.updated_at` DESC, hoà thì id DESC (bỏ `created_at` khỏi select). Test transaction (rollback): gán hạn mức tạm 2 NV, `Employee::save()` 1 NV → NV đó lên đầu; sort tay Hạn mức tăng dần vẫn đúng. php -l + compile FE pass.
Đang làm dở: —
Bước tiếp theo: user kiểm trình duyệt (sửa hạn mức 1 tài khoản ở /human/employee → mở báo cáo thấy lên đầu; mở popup thấy ⇅); chưa commit.
Blocked:

## Phase 7 — #11727 "Tổng công nợ KH hiện tại lệch ERP" (16/10/2026) — ĐÃ CHECK, CHỜ USER CHỐT

Tester: NV 11410102 Chu Khương Duy — ERP -20,000,000, HRM 28,001,006 (dev).
Nguyên nhân (đọc ERP `AccountDetail::getDebtEmployee` + dựng lại câu SQL trên DB local):
- ERP `whereHasMorph('contractable', [Contract, OpeningContract, LiquidationContract, ServiceContract, ProjectContract])` — `Contract` là `App\Contract` (class cũ), KHÔNG phải `FirmContract`. Đối chiếu `contractable_type` thật trong DB: chỉ `App\Model\Accounting\OpeningContract` khớp (3,986 dòng) → ERP CHỈ cộng dòng sổ của HĐ đầu kỳ, bỏ sót toàn bộ HĐ bán (FirmContract) + HĐ dịch vụ BH (WrServiceContract).
- ERP còn khác: chỉ TK con của 131 (không gồm 131 gốc), Σ Nợ − Σ Có mọi loại chứng từ, gắn NV qua `opening_contracts.created_by`.
- Local NV id 27: ERP-replica -31,702,773 (87 dòng, toàn OpeningContract) vs HRM 426,279,705 (= OpeningContract -31.7tr + FirmContract 467.6tr + WrServiceContract -9.65tr).
- [x] User chốt 16/10/2026: (B) làm Y ERP
- [x] BE `ReportLimitDebtEmployeeService::debts()` + `debtByCustomer()` — Σ Nợ − Σ Có, chỉ TK CON của 131, chỉ dòng có `contractable_type` ∈ 5 class ERP (App\Contract, OpeningContract, LiquidationContract, ServiceContract, ProjectContract), NV = `created_by` của HĐ đó. Giữ mốc "Đến ngày" (chốt 14/10) + popup tách đúng theo KH
- [x] FE `index.vue` — sửa chú thích ⓘ cột Tổng công nợ theo công thức mới
- [x] Verify: so ERP-replica SQL thuần vs service mới (NV 27), tổng popup = cột chính; php -l, compile

### Checkpoint — 2026-10-16 (Phase 7, #11727)
Vừa hoàn thành: công nợ NV Y ERP — `erpDebtQuery()` (left join 4 bảng HĐ theo đúng `contractable_type`, NV = `created_by` HĐ, chỉ TK con 131, Σ Nợ − Σ Có) dùng cho cả bảng chính + popup; bỏ `CustomerDebtAggregator` khỏi service. Giữ: mốc "Đến ngày" theo `invoiceable_date_accounting` (chốt 14/10), popup tách đúng theo KH. Test transaction (rollback) 5 NV: service = SQL dựng tay theo whereHasMorph ERP, tổng popup = cột chính (NV 27: -31,702,773). FE sửa ⓘ cột Tổng công nợ. php -l + compile pass.
Đang làm dở: —
Bước tiếp theo: user/tester so lại NV 11410102 trên dev với ERP (mong đợi -20,000,000); chưa commit.
Blocked:

## Phase 8 — #11728 "Chỉ tiêu Vượt hạn mức lấy sai" (16/10/2026) — check, KHÔNG sửa code

Tester: lọc Vượt hạn mức ra 11410102 Chu Khương Duy (28,001,006 > 47). Nguyên nhân = công thức công nợ cũ (#11727); ERP tính NV này -20,000,000 ⇒ Trong hạn mức. Logic lọc (`>` vượt / `<` trong) đã y ERP `searchDataEmployee`, không đổi.
- [x] Test transaction (rollback) sau fix #11727: Duy hạn mức 47, công nợ -31.7tr (local) → rơi vào Trong hạn mức; NV 41410780 (1.16 tỷ / hạn mức 1tr) → Vượt hạn mức. Đóng chung với #11727 khi lên dev.

## Phase 9 — #11729 "Popup chi tiết hạn mức dư nợ NV theo KH lệch ERP" (16/10/2026)

Nguyên nhân: ERP `AccountDetail::getDebtEmployeeByCustomer` dùng 1 biến `$result` CỘNG DỒN qua mọi KH (duyệt dòng sổ theo thứ tự, KH = số lũy kế tới lần cuối KH đó xuất hiện). HRM đang tách đúng theo KH (chốt 14/10). Mô phỏng ERP trên DB local NV 27 khớp ảnh tester từng dòng. User chốt 16/10/2026: **sửa y ERP**.
- [x] BE `ReportLimitDebtEmployeeService::debtByCustomer()` — duyệt dòng sổ theo `ad.id`, cộng dồn y ERP; lọc KH áp TRƯỚC khi cộng (ERP lọc trong query); Số tiền từ–đến + tìm nhanh áp SAU; thứ tự mặc định = thứ tự KH xuất hiện (y ERP), chỉ sắp theo Công nợ khi user bấm cột
- [x] FE `DebtByCustomerModal.vue` — chỉ gửi `sort_by` khi user bấm sắp xếp; bỏ dòng "Tổng công nợ" (ERP không có, số cộng dồn cộng lại vô nghĩa)
- [x] Verify: so service với mô phỏng ERP (NV 27); php -l, compile FE

### Checkpoint — 2026-10-16 (Phase 9, #11729)
Vừa hoàn thành: BE `debtByCustomer()` cộng dồn y ERP (duyệt `ad.id`, lọc KH trong query, Số tiền/tìm nhanh lọc sau, bỏ `total_debt`, mặc định thứ tự KH xuất hiện, sắp theo Công nợ chỉ khi có `sort_by=money_debt`). FE popup bỏ dòng "Tổng công nợ" + style `.total-line`, chỉ gửi `sort_by`/`sort_desc` khi user bấm cột. Verify NV 27 local: 18 KH khớp mô phỏng ERP từng dòng; dòng đầu 19TPHPVI-87 = số lũy kế cuối = cột chính (-31,702,773) — trên dev ERP là -20,000,000 đúng như ảnh tester. php -l + compile FE pass.
Đang làm dở: —
Bước tiếp theo: tester so lại popup NV 11410102 trên dev với ERP; chưa test trình duyệt; chưa commit.
Blocked:

## Phase 10 — Chú thích tiêu đề báo cáo (17/10/2026)

- [x] FE `pages/finance/report-limit-debt-employees/index.vue` — thêm computed `pageTitleInfo` (icon ⓘ cạnh tiêu đề, qua `PageTitleMixin`) như màn `assign/report/customer-market-development`

## Phase 11 — #11730 "Popup chi tiết lệch Báo cáo tổng hợp công nợ KH theo NV" (17/10/2026) — check, KHÔNG sửa code

Tester (ảnh chụp 15/10 11:44, TRƯỚC commit #11727/#11729): NV 11410102 Chu Khương Duy, lọc KH 24TLAPYE-50 — HRM -20,873,000, ERP -20,000,000, BC tổng hợp công nợ KH theo NV ra số dư cuối kỳ 20,000,000.
- [x] Đối chiếu dòng sổ local: KH 18575 + NV 27 có 7 dòng OpeningContract (TK 131 con) → Σ Nợ − Σ Có = -20,000,000; còn lại là FirmContract/WrServiceContract (ERP bỏ qua).
- [x] Chạy code mới (`bc97e1714`): lọc KH → -20,000,000 (khớp ERP). Chạy code cũ (`3b0054ebb`, CustomerDebtAggregator): -20,360,000 local (dev ra -20,873,000 do data dev khác) ⇒ lệch do công thức cũ, đã sửa ở #11727 + #11729.
- [ ] Tester test lại trên dev sau khi deploy develop có `43a05dba4` + `bc97e1714`; đóng chung #11727/#11729.

### Checkpoint — 2026-10-17 (Phase 11, #11730)
Vừa hoàn thành: xác minh #11730 trùng nguyên nhân #11727/#11729 (code mới local ra đúng -20,000,000).
Đang làm dở: —
Bước tiếp theo: deploy develop lên dev → tester kiểm lại popup NV 11410102 / KH 24TLAPYE-50.
Blocked: chưa kiểm được trực tiếp trên dev (không có API dev).

## Fix #11928 — Bỏ dòng "Không có nhân viên nào." dưới bảng (30/10/2026)

Dòng này do `V2BaseDataTable` (dùng chung) in khi 0 bản ghi; bảng đã có "Không có dữ liệu phù hợp" nên thừa. User chốt chỉ bỏ ở màn này.
- [x] `components/V2BaseDataTable.vue`: `itemLabel` rỗng ⇒ không in dòng "Không có … nào." (các màn khác giữ nguyên; 4 popup đang truyền `item-label=""` trước in lỗi "Không có  nào." nay để trống)
- [x] `pages/finance/report-limit-debt-employees/index.vue`: `itemLabel=""`
- [x] Verify: compile template
