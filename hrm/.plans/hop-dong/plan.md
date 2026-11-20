# Hợp đồng bán hàng HRM — Plan

> Tóm tắt + quyết định: `design.md`. Spec Phase 11: `design-phase11-firm-fields.md`.
> **Bản plan chi tiết cũ (1.359 dòng — từng task, code mẫu, kết quả verify)**: `git show 651bfa1:hrm/.plans/hop-dong/plan.md`
> trong repo `hrm-claude-config`. Plan này rút gọn ngày 27/10/2026: mỗi phase giữ lại việc đã làm, quyết định, commit.

## Ràng buộc chung (còn hiệu lực)
- Code trên `gop_db` (hrm-api + hrm-client). Bảng mới prefix `hrm_`; không FK cứng sang bảng ERP; không dùng `mysql2`.
- Bám ERP FirmContract (`FirmContractService`, `app/Contract.php`) cho luồng, validate, công thức HTHT.
- PHP 7.4 (không `?->`). Màn `_id/edit.vue` là màn CŨ: validate kiểu `touched` / `validateForm()`, khối `.c-section` + `.fld-grid`.
- Quyền mới sửa trong `PermissionsTableSeeder` (đồng bộ theo tên), không migration quyền.
- Không commit / push khi user chưa yêu cầu.

## Mục lục phase

| Phase | Nội dung | Ngày | Commit api / client | Trạng thái |
|---|---|---|---|---|
| 1–3 | DB 7 bảng, BE CRUD + trạng thái + đính kèm, FE danh sách/form/chi tiết, nút Lập HĐ ở báo giá | 10–11/08 | `47e91ca8c` / `af101e6d6` | ✅ |
| 4 | Doanh số vượt trội + giảm giá dòng cha, hạn mức → Giám đốc duyệt (+ `f43b5b6e7` 11/08: rule lập từ báo giá trúng thầu, gộp quyền) | 11/08 | gộp vào `245fe5e7d` / `a7d800aa1` (13/08) | ✅ |
| 5 | Form 1 cột; prefill Bên A/B; mã HĐ kiểu ERP; field bắt buộc như ERP; loại thanh toán; popup chọn báo giá | 12–13/08 | `245fe5e7d` / `a7d800aa1` | ✅ |
| 6 | HTHT: phòng thực hiện, bóc tách giá, phân bổ phòng/NV, màn HTHT, Duyệt = Có hiệu lực, sửa theo Excel | 13–14/08 | `82cb986f8` `dea15e134` `299c31d53` `d6d5bea45` `df727cde2` `45af93449` `a3c1812ea` `65548c945` / `d2c4cfbf8` `efcf7de37` `65a55e982` `fb707de34`… | ✅ (E còn mở) |
| 7.3 | Điều kiện hiệu lực + thời hạn thực hiện | 14/08 | `ac8cf78f4` / `802cb3241` | ✅ |
| 8 | Bỏ yêu cầu quyền khi lập HĐ (khớp ERP) | 17/09 | `6aea12365` / `7016c2133` | ✅ |
| 9 | Ngày ký không bắt buộc | 14/10 | `309feef6d` / `c6801fac4` | ✅ ⚠️ thiếu migration trên gop_db (xem Phase 17) |
| 10 | TK ngân hàng Bên A: dropdown, không chọn sẵn (`company_account_id` + snapshot) | 14/10 | `309feef6d` / `c6801fac4` | ✅ |
| 11 | 6 trường FirmContract còn thiếu (Bên B cá nhân/tổ chức, đại diện, TK Bên B, giao hàng, lắp đặt) | 14–15/10 | `81d3bdbf9` `40b31524a` / `b7026e198` `4a9fcc8a3` | ✅ |
| 12 | Chi tiết HĐ: hiển thị cha-con bảng hàng (STT 3.1, thụt lề) | 15/10 | — / `49548c4b5` | ✅ |
| 13 | DSTC = 0 ở HTHT (sai nguồn giá + return sớm) | 15/10 | `80f0a20c5` | ✅ |
| 14 | Lịch sử HĐ: hành động tiếng Việt, mặc định thu gọn | 15/10 | `463202acd` / `cfb8c1c95` | ✅ |
| 15 | Không duyệt bắt buộc lý do (màn HTHT) | 15/10 | `5ac149e31` / `0707731a4` | ✅ |
| 16 | Sửa/Xoá: người lập + Đang tạo, bỏ yêu cầu quyền | 15/10 | `99ec61fd9` / `40ef86dff` | ✅ |
| 17 | Bổ sung sau 15/10 (điều kiện TT, DSTC theo bản chất hàng, perf, STT form sửa, migration ngày ký) | 15–23/10 | xem dưới | ⚠️ 2 commit chỉ ở `develop` |

---

## Phase 1–3 — Nền tảng (10–11/08) ✅
- DB: `hrm_contracts` + 6 bảng con (`groups`, `product_prices`, `service_items`, `discounts`, `process_payments`, `histories`); đính kèm dùng bảng `files` (`table='hrm_contracts'`).
- BE: `ContractService::createFromQuotation` (snapshot đóng băng, remap cha-con), update chỉ trường riêng, submit/approve/reject/liquidate + lịch sử, danh sách phân quyền 4 cấp, xoá chỉ khi Đang tạo.
- FE: danh sách, tạo/sửa (dòng hàng read-only), chi tiết + thanh nút theo trạng thái, `ContractPaymentTermsTable`, nút Lập/Xem HĐ ở báo giá, menu.
- [ ] Chưa từng chạy: E2E trọn vòng, phân quyền 4 cấp với nhiều tài khoản, upload S3 thật.

## Phase 4 — Doanh số vượt trội + giảm giá (11/08) ✅
- Cột `hrm_contract_product_prices.extra_price` + `hrm_contracts.total_extra_amount`; số dẫn xuất tính lúc chạy.
- `recomputeTotals` (gồm dịch vụ + phí vận chuyển), `assertLinesNonNegative`, `assertExtraWithinLimitOrBgd` ở `approve()`.
- FE: 2 cột nhập trên dòng cha, box tổng có dòng vượt trội, gửi `line_adjustments`.

## Phase 5 — Form 1 cột + đồng bộ ERP (12–13/08) ✅
- 5: bố cục 1 cột 7 khối (Thông tin chung · Bên A · Bên B · Hàng hoá · Thanh toán · Ký · Đính kèm).
- 5b: `GET quotation-prefill/{id}` đổ Bên A/B từ công ty, khách, người đại diện.
- 5c: mã HĐ theo ERP, Số HĐ bắt buộc. 5d: field bắt buộc theo `FirmContractStoreRequest`.
- 5e: cột `payment_type` ở tiến độ thanh toán. 5f: popup `ContractQuotationSearchModal`, chip báo giá mở tab mới.

## Phase 6 — HTHT (13–14/08) ✅
- A: phòng/NV thực hiện (`implement_*` polymorphic), đủ 100% mới gửi duyệt; gộp Duyệt = Có hiệu lực (bỏ "Xác nhận hiệu lực").
- B–D: snapshot giá chuẩn lúc tạo HĐ; `ContractSupportAccountingService` (bóc tách 4 nhóm, quy chế, hoa hồng, ghi 4 bảng); unique `firm_support_accounting` đổi composite (contractable_id, contractable_type); màn `support-accounting.vue` (preview + duyệt).
- E: sửa theo Excel "1.HTHT 20-1-2025" (Thưởng NVKD = `sales_bonus`, mục 14.1 có trần, TNDN mặc định). Ẩn cột II/III khi không có quyền xem giá vốn.
- [ ] Đối chiếu số HTHT với 1 HĐ ERP thật; cấu hình đúng hệ số G/H theo công ty.

## Phase 7.3 — Hiệu lực + thời hạn thực hiện (14/08) ✅
- Cột `effective_condition`, `guarantee_approved_date`, `execution_deadline_*`, `execution_base_date`, `execution_end_date`; ngày hiệu lực tự tính theo điều kiện; accessor `can_export`.

## Phase 8 — Bỏ yêu cầu quyền khi lập HĐ (17/09) ✅
- Gỡ quyền "Lập hợp đồng" ở 2 nút FE + route + controller; giữ điều kiện trúng thầu + người lập. Quyền vẫn còn trong seeder nhưng không dùng.
- [ ] Bấm thử bằng tài khoản không có quyền.

## Phase 9 — Ngày ký không bắt buộc (14/10) ✅
- FE bỏ `*` + validate; BE Store/Update `nullable|date`. Lý do: ngày ký chỉ có khi xác nhận KH đã ký.

## Phase 10 — TK ngân hàng Bên A dạng dropdown (14/10) ✅
- Cột `company_account_id` + snapshot 4 cột; `GET company-accounts`; bỏ tự điền ở prefill; bắt buộc chọn.

## Phase 11 — Trường FirmContract còn thiếu (14–15/10) ✅
- Cột `customer_type`, `customer_deputy_id`, `customer_account_id`, `need_install`; `GET customer-deputies`, `GET customer-bank-accounts` (kiểm khách để chặn IDOR); bắt buộc theo loại khách; snapshot loại khách ưu tiên trên HĐ.
- FE: Bên B cá nhân/tổ chức, bảng giá read-only, TK Bên B dropdown, địa chỉ giao hàng, radio lắp đặt. Danh sách thêm cột khách hàng (mã + người liên hệ).
- Để lại: mục 3 (giao hàng + tiến độ TT #11252), mục 4 (điều kiện thời gian thực hiện).

## Phase 12–16 — Sửa theo phản hồi (15/10) ✅
- 12: chi tiết HĐ đánh STT cha-con kiểu báo giá (3.1), dòng con thụt lề + chữ nhạt.
- 13: `snapshotProductMasterPrice` đọc `product_units` + `product_unit_prices`, bỏ return sớm; `refreezeProductMasterPrices` khi sửa; vế min() cộng vượt trội. Không backfill HĐ cũ.
- 14: `action_label` tiếng Việt; khối Lịch sử thu gọn mặc định.
- 15: `/reject` bắt buộc `rejected_reason` (BE 422 + modal FE).
- 16: `is_can_edit` / `is_can_delete` = người lập + Đang tạo; middleware `contractEditable` cho PUT/DELETE/attachments; chi tiết đọc cờ BE, khớp danh sách.

## Phase 17 — Bổ sung sau 15/10 (ghi lại 27/10 từ commit, không có plan gốc)
- [x] Giá theo công ty ghi trên chứng từ (N137/N143) — api `176fa9206` (15/10, dnsnamdang).
- [x] Tiến độ thanh toán: điều kiện thanh toán + số ngày; bảng + seeder `payment_conditions`, `GET payment-conditions` — api `165f4a0fd` / client `e1b99dc88` (16/10).
- [x] Hệ số DSTC đọc `company_product_natures` (`ProductNatureDstcCoefficient`) — api `49318b57b` (19/10).
- [x] Chặn mở màn tạo khi còn hàng quá hạn (#11722) — client `bb913e1c8` (20/10, khoipv); route store/update gắn `dueConfig`.
- [x] Perf N153A: snapshot giá gốc nạp theo lô cả HĐ — api `cd6af7485` (20/10, dnsnamdang).
- [x] Migration `2026_10_23_000001_make_sign_effective_date_nullable_hrm_contracts_table` — api `9b0b9194f` (23/10). **Chỉ ở `develop`.** Thiếu bản này thì lưu HĐ không nhập ngày ký báo lỗi `Column 'sign_date' cannot be null`.
- [x] Form sửa đánh STT phân cấp (2.1, 2.1.1) khớp màn chi tiết — client `03b0626c0` (23/10). **Chỉ ở `develop`.**
- [x] 27/10: cherry-pick 2 commit trên vào nhánh `gop_db-hop-dong-ban` (api `dee622e27`, client `10a4ab567`); đã chạy riêng migration `2026_10_23_000001` vào DB local `hrm_erp_21_10_prod` (2 cột → NULL). Lên `gop_db` khi merge nhánh này.

## Phase 18 — Màn danh sách: quyền phân cấp chuẩn + bộ lọc đầy đủ
> Spec: `design-phase18-danh-sach.md` (chốt Q1–Q3 ngày 27/10). Nhánh `gop_db-hop-dong-ban`. User cho phép code 27/10. CHƯA commit.
- [x] 18.1 Seeder: đổi tên 4 quyền xem → `… Hợp đồng bán hàng …` + `RENAMED`. Dry-run: đổi tên 4 (kèm 13 thêm + 715 sửa của nhánh khác → KHÔNG chạy cả sync trên local; đổi tay đúng 4 dòng id 1144–1147 + `cache:clear`).
- [x] 18.2 BE scope `ContractController::scopedContractQuery`: 4 tên mới + ẩn Đang tạo của người khác ở mọi cấp (index + export dùng chung).
- [x] 18.3 Migration `2026_10_27_000001_add_list_indexes_to_hrm_contracts_table` (8 index) — đã chạy local.
- [x] 18.4 BE bộ lọc: keyword (mã HĐ, số HĐ, mã BG, mã KH, tên KH, MST) · status "2,6"/mảng · 5 khoảng ngày (`applyDateRange`) · bảng giá · người duyệt · hàng hoá (mã/tên/model) · giá trị từ–đến · lắp đặt · phòng thực hiện.
- [x] 18.5 FE `pages/assign/contracts/index.vue`: cờ quyền tên mới; 15 ô; nhãn "Người tạo"; 4 trạng thái chọn nhiều (gửi "2,6" qua `requestParams()` — buildQueryString ghép mảng PHP chỉ nhận giá trị cuối); slot tiền từ–đến; bảng giá nạp `assign/quotations/price-types`; người duyệt + phòng ban lấy Vuex; chuẩn hoá `status` đã lưu kiểu cũ.
- [x] 18.6 Verify: tinker transaction+rollback — 5 mức phạm vi + 13 ca bộ lọc ĐẠT; HTTP list/export 200; Playwright: 13 ô (tài khoản không quyền cấp) cao 32px, 4 trạng thái, chọn → `status=2,6`, ô gõ chờ Enter. Spec mới (CHƯA chạy, chờ user): `e2e/tests/assign/contracts-list.api.spec.ts` (phạm vi + lọc) + `contracts-filter.spec.ts` (UI).
- [x] 18.7 Kiểm cụm Công ty – Phòng ban – Bộ phận – Người tạo bằng tài khoản CÓ quyền: cấp tạm "Xem tất cả Hợp đồng bán hàng" cho id 50 qua role tạm `TẠM local P18 - Xem tất cả HĐ bán hàng` (id 108470, DB local — GỠ khi xong). 17 ô hiện đủ, cao 32px; nhãn ô 4 sửa "Nhân viên" → "Người tạo" bằng prop `label-employee` (không đụng component); chọn Công ty gửi `company_id`.
- [x] 18.8 5 ô khoảng ngày dồn MỘT cột bên phải (user chốt 27/10, cho phép sửa component chung). `V2BaseSmartFilterPanel` thêm tuỳ chọn opt-in field `column: 'right'`: `.form-row` thành CSS grid 4 cột (class `smart-filter-split`), ô cột phải `grid-column: 4; grid-row: var(--side-row)`, KHÔNG thêm lớp bọc (giữ mọi rule `.form-row > …`). Đo: `/lookup/stock-companies` trùng khớp từng pixel trước/sau; màn HĐ 5 ô ngày cùng x=1139, 12 ô còn lại 3 cột × 4 hàng, đều 341×32. Spec F1 kiểm thêm cột ngày.
- [x] 18.9 Thêm ô Nhóm ngành + Ứng dụng (user chốt 27/10: 2 ô độc lập như màn Dự án TKT, không sửa component chung). Nguồn: `hrm_contracts.project_id` → `prospective_projects.scope_id` (Nhóm ngành, hrm_scopes) / `application_id` (18/18 báo giá trúng thầu đều gắn dự án, 0 gắn giải pháp). BE `whereExists` prospective_projects; FE Nhóm ngành select + Ứng dụng `CheckboxMultiSelect` (gửi "a,b"), danh mục qua store `optionsSelect/fetchScopes|fetchApplications`. Verify: tinker rollback 5 ca đúng tập; Playwright 34 nhóm ngành / 145 ứng dụng, chọn là tìm (`scope_id=1`, `application_id=1,2`); 14 ô trái 3 cột + 5 ô ngày cột phải.
- [x] 18.10 Thêm ô "Phòng hỗ trợ" (`support_department_id`): chỉ khớp `implement_departments.is_main = 0`; ô "Phòng thực hiện" GIỮ khớp cả chính lẫn hỗ trợ (user chốt 27/10). Verify: tinker rollback 4/4; Playwright 78 phòng ban, chọn là tìm, nằm cạnh "Phòng thực hiện".
- ⚠️ Ngoài luồng (chưa sửa): ô `CheckboxMultiSelect` (Ứng dụng) cao 34px khi có chip, 32px khi trống — tái hiện y hệt ở `/assign/prospective-projects`.
- ⚠️ Ngoài luồng (chưa sửa): chọn 1 công ty ở cụm Công ty bắn **2 request giống hệt** — nghi cụm tự reset Phòng ban/Bộ phận/Người tạo ở nhịp khác làm deep watcher chạy 2 lần; không phải lỗi `per_page` chuỗi/số trong memory. Cần kiểm lại trên code gốc gop_db.
- ⚠️ Ngoài luồng (component dùng chung, chưa sửa): ô chọn nhiều trong `V2BaseFloatingField` cao 56–80px khi có chip (dòng ô tìm select2 rớt xuống) — tái hiện cả `/lookup/stock-companies`.

## Phase 19 — Màn Tạo/Sửa HĐ: bố cục gọn + header khối kiểu form meeting
> Yêu cầu user 27/10: xếp gọn phần thông tin phía trên để "Chi tiết hàng hoá" không bị đẩy sâu; header card dùng mẫu nhỏ
> của form meeting mới. Bước 1: mockup → user góp ý. CHƯA code.
- [x] 19.1 Mockup `mockup-form-hd-gon.html` (token đo thật từ `/assign/meeting/create` + sale-theme, ghi đầu file). 5 khối trên + Ký HĐ → 3 khối (① Thông tin HĐ lưới 4 cột · ② Các bên ký kết A|B, thông tin danh mục chỉ đọc, Người ký vào Bên A · ③ Thực hiện & giao hàng 1 hàng); ⑤ gộp Thông tin + Điều khoản thanh toán. Đo 1512×773: Chi tiết hàng hoá top 1514px → 574px; 1366 không tràn ngang.
- [x] 19.1b Vòng 2 (góp ý user 27/10): bỏ vòng số; mọi ô dùng nhãn floating như bộ lọc (token V2BaseFloatingField đo thật); Bên A/B cùng lưới 3 cột × 3 hàng, trường chỉ đọc cũng là ô floating xám (đo: 3 hàng A = B ở y 312/362/412); Thực hiện · Giao hàng · Thanh toán · Điều khoản thanh toán → 1 khối tab (V2BaseTabNavigation) SAU hàng hoá. Đo 1512×773: hàng hoá top 476px, thấy đủ 4 dòng hàng; 1366 không tràn.
- [x] 19.1c Vòng 3 (góp ý user 27/10): mọi header khối 1 màu (của "Các bên ký kết", rgba(2,132,199,.07)) + icon (ri-file-text / ri-shake-hands / ri-archive / ri-attachment-2; tab ri-team / ri-truck / ri-calendar-check); ô / ô bảng chữ dài 1 dòng "…" + tooltip hiện ngay (khuôn overflowTooltip, chỉ khi thực sự bị cắt); bảng hàng hoá chuẩn MISA đo thật (th #d8e7e1/#10141b 12px/700 32px, gạch #7cc7ae, viền #ced1d6, ô kẻ dọc chấm 1.5px, nền #fbfbfc, hover #e6f5ef) + đủ khung viền; dòng con lùi 14px; gộp tab Thanh toán thành bảng "Tổng hợp giá trị hợp đồng" (I–IV + Tổng + Thưởng NVKD) dưới bảng hàng, khối tab còn 3; header Thông tin HĐ hiện người lập (khuôn CreatorInfoLine "Tên - dd/mm/yyyy HH:mm"). Đo: hàng hoá top 476px; chỉ cột Tên hàng bị cắt (có tooltip).
- [x] 19.1d Vòng 4 (góp ý user 27/10): **mockup chỉ vẽ lại UI, mọi luật form hiện có giữ nguyên** (Bên A chỉ đọc = đúng hiện trạng). Header khối đậm hơn (nền rgba(2,132,199,.13), viền .38), icon trong ô vuông 22px nền #0284c7 icon trắng; bỏ bảng "Tổng hợp giá trị" cạnh bảng hàng → bảng hàng có dòng Tổng (tfoot, chỉ cộng dòng cha: Thành tiền · TT sau điều chỉnh · Giảm giá · TT sau GG) + thanh tổng hợp phẳng 8 ô (Hàng hoá · Dịch vụ · Chi phí · Vận chuyển · Trước thuế · VAT · Tổng giá trị HĐ · Thưởng NVKD), rê ô nhóm ra tooltip bóc tách; khối tab bỏ card header, tab nhỏ 28px/12.5px. Đo: dòng Tổng thẳng mép phải từng cột (1512 + 1366), thanh tổng không ô nào bị cắt, hàng hoá top 476px.
- [x] 19.1e Vòng 5 (góp ý user 27/10): tổng thanh toán = chân (tfoot) của chính bảng hàng, góc phải — dòng Tổng + 8 dòng (Giảm giá đơn hàng · Dịch vụ · Chi phí · Vận chuyển · Tổng trước thuế · VAT · Tổng giá trị HĐ · Thưởng NVKD), nhãn trải 3 cột / số trải 2 cột cuối (đo: mép trái = cột "TT sau điều chỉnh", mép phải = mép bảng); Đính kèm theo khuôn FileAttachmentTable; tab Thực hiện = thẻ phòng 460px (Chính / Hỗ trợ n) như ContractImplementSection, ô 260/290/96px; icon tiêu đề card về khuôn icon card của app (trơn, không khung, #0284c7).
- [x] 19.1f Vòng 6–7: dòng tiêu đề "Tổng hợp thanh toán" đầu bảng tổng, dính liền dòng Tổng (khe 0px), nền xanh nhạt #cfe8f7 chữ #075985; dòng hàng con thêm icon cấp con `ri-corner-down-right-line` xám #94a3b8 trước tên (khuôn ProductExportRequestForm / BomBuilderTableCard).
- [x] 19.1g Vòng 8: tab Thực hiện — mỗi thẻ phòng ban rộng 50% (2 thẻ / hàng, grid 2 cột), ô bên trong giữ vừa nội dung. Đo: 2 thẻ = 50% / 50% cùng hàng ở 1512 và 1366.
- [x] 19.1h Vòng 9: thẻ phòng ban — tag Chính / Hỗ trợ n dính góc trên-trái (bo 8px 0 8px 0, Chính #0284c7, Hỗ trợ #64748b chữ trắng); Σ% + xoá phòng góc trên-phải (thẻ Chính chừa chỗ nút xoá để Σ% thẳng hàng); bên trong 1 lưới [Nhân viên 1fr | % 120px | xoá 28px], Phòng ban trải 2 cột đầu. Đo: mép trái các ô cùng 13px, mép phải Phòng ban = mép phải ô %, Σ% 2 thẻ cùng toạ độ.
- [x] 19.1i Vòng 10: Chi tiết hàng hoá thành tab ĐẦU, Đính kèm thành tab CUỐI ⇒ khối tab 5 tab (Chi tiết hàng hoá · Thực hiện · Giao hàng · Điều khoản thanh toán · Đính kèm) nằm ngay sau "Các bên ký kết", mặc định mở tab hàng hoá; vùng bên phải hàng tab đổi theo tab (ghi chú lấy từ báo giá / + Thêm phòng hỗ trợ / + Thêm đợt / chip "n file" + Thêm file). Đo: hàng tab top 476px, bảng hàng 525px, hàng tab cao 32px không nhảy khi đổi tab.
- [x] 19.1j Vòng 11: bỏ số đếm ở cả 5 tab (giữ dấu * bắt buộc ở Điều khoản thanh toán); thêm icon người tạo (ri-user-line, xám #6b7280, 15px) trước dòng "Tên - dd/mm/yyyy HH:mm" trên header Thông tin hợp đồng.
- [x] 19.2 User duyệt mockup (27/10). Chốt thêm: Đính kèm GIỮ luồng API riêng của HĐ (POST/DELETE `assign/contracts/{id}/attachments`), chỉ vẽ theo khuôn FileAttachmentTable — không đụng BE. User cho phép code: hrm-client · `gop_db-hop-dong-ban` · `_id/edit.vue` + `ContractImplementSection.vue` (màn Chi tiết đổi theo) + `ContractPaymentTermsTable.vue`; không BE/DB/V2Base*.
  Chốt thêm khi code (27/10): Bên A 4 trường (Tên cty, MST, SĐT, Địa chỉ) ĐỔI thành chỉ đọc ở FE (trước sửa được) — user chọn; BE chưa chặn.
  Giữ đủ chi tiết màn thật dù mockup rút gọn: bảng hàng 16 cột + dòng nhóm + bảng Dịch vụ/Chi phí, ô điều kiện (Ngày bảo lãnh, Ngày mốc), nhánh Bên B tổ chức/cá nhân + Ngân hàng/Chi nhánh.
- [x] 19.3 Code (27/10, CHƯA commit) — hrm-client `gop_db-hop-dong-ban`:
  - `pages/assign/contracts/_id/edit.vue`: template mới (2 khối + `V2BaseTabNavigation` 5 tab thu nhỏ 28px bằng CSS trong màn), mọi ô `V2BaseFloatingField` (lỗi qua `error`, `errOf()` đọc cả mảng 422), Bên A chỉ đọc, Người ký vào Bên A, bảng hàng MISA 15 cột (bỏ cột Ghi chú → icon `ri-sticky-note-line` + tooltip cạnh tên hàng để bảng vừa khung, không cuộn ngang ở 1366/1512), dòng con icon cấp con + lùi 14px, tfoot = dòng Tổng (chỉ dòng cha) + bảng "Tổng hợp thanh toán" (gộp hộp Tổng giá trị + bảng Thông tin thanh toán cũ), tooltip `v-overflow-tooltip`, người tạo `CreatorInfoLine` + `ri-user-line`, validate lỗi ⇒ tab đỏ + tự mở tab lỗi khi khối trên không có lỗi; CSS viết lại (token đo mockup); ô `.is-disabled` nhận chuột lại để tooltip hiện (control vẫn khoá).
  - `ContractImplementSection.vue`: thẻ 50%, tag góc, lưới [NV | % | xoá], prop `toolbarOutside`; chế độ xem `impl-grid--view` (màn Chi tiết).
  - `ContractPaymentTermsTable.vue`: bảng MISA + prop `toolbarOutside` (nút "Thêm đợt" ở hàng tab gọi `addRow()` qua ref).
  - Verify Playwright (user 50, BG-2026-00311, chặn request ghi): 0 lỗi console; ô 32px; hàng tab top 475px (cũ: hàng hoá 1514px); bảng không cuộn ngang 1512/1366, dòng Tổng thẳng 6 cột, tổng hợp dính khe 0; 5 tab hàng tab 32px cố định; Trình duyệt trống ⇒ 5 ô đỏ + 2 tab đỏ, 0 request ghi, hàng ô vẫn thẳng ở trạng thái lỗi; tooltip ô chỉ đọc + tên hàng.
  - Spec mới (chưa chạy): `e2e/tests/assign/contracts-form-layout.spec.ts` (L1–L5).
  - CHƯA kiểm: màn Sửa + màn Chi tiết (DB local chưa có HĐ nào) — `ContractImplementSection` chế độ xem đổi theo.
  - ⚠️ Ngoài luồng (chưa sửa): option nhân viên ở Phòng thực hiện hiện "HN_KD2 - Nguyễn Văn Mởn", lệch chuẩn "Tên - Mã phòng - Mã NV" (`employeesFull` dùng `e.name`).
- [x] 19.4 Bảng "Tổng hợp thanh toán" (27/10, CHƯA commit; user cho phép FE + BE):
  - Lỗi cũ: `paymentSummary` dồn MỌI dịch vụ vào "Dịch vụ đi kèm", "Chi phí" gán cứng 0; bảng không có dòng Hàng hoá.
  - `edit.vue`: tách theo `revenue_calculation` (0 = Chi phí, 1/null = Dịch vụ — cùng luật `summaryBreakdown` màn báo giá + `QuotationService::computeSummaryBreakdown`); thứ tự Hàng hoá → Dịch vụ → Chi phí → Vận chuyển → Vượt trội → Giảm giá → Tổng trước thuế → VAT; **dòng giá trị 0 không hiện** (giữ tiêu đề, Tổng giá trị HĐ, Thưởng NVKD).
  - hrm-api `DetailContractResource::resolveServiceItems`: trả thêm `revenue_calculation` (1 query `costs` theo `cost_id`) — màn Sửa mới tách được; luồng Tạo đã có sẵn từ `DetailQuotationResource`.
  - Verify: BG-2026-00406 (id 408) ⇒ Hàng hoá 1,978,560,000 · Chi phí 8,640,000 · Vận chuyển 4,320,000 · Tổng 1,991,520,000, khớp `summary_breakdown` BE báo giá; Dịch vụ/Giảm giá/Vượt trội ẩn; 0 request ghi. Resource kiểm bằng tinker trong bộ nhớ (cost 36 ⇒ 0, cost khác ⇒ 1, không cost ⇒ null). Kiểm bằng script Playwright riêng (MCP treo).
  - Spec: thêm `P19-L6` (chưa chạy).
- [x] 19.6 Hàng hoá + Dịch vụ chung 1 bảng theo khuôn Báo giá (27/10, CHƯA commit; user cho phép màn Sửa + Chi tiết):
  - Tab / mục đổi tên **"Chi tiết hợp đồng"**. Bảng: dòng mục `A — Hàng hoá` + `B — Dịch vụ & Chi phí khác` (nền #e2f5ee, viền dưới #9bdcc6 như `q-section-row`) có tổng phụ ở 6 cột số; dòng dịch vụ chung cột hàng hoá, nhãn `V2BaseBadge` DV (#0EA5E9) / CP (#D97706) theo `isCostItem()` (revenue_calculation = 0); B trống ⇒ "Chưa có dịch vụ / chi phí". Bỏ bảng "Dịch vụ / Chi phí" riêng.
  - Dòng **Tổng = A + B** (`contractTotals` = `lineTotals` + `svcTotals`). Màn Sửa: "Giảm giá đơn hàng" lấy `paymentSummary.total.giam_gia` (cộng từ dòng, trước đây lấy `contract.total_discount_amount` đã lưu ⇒ không đổi khi sửa dòng); `tfoot` hiện cả khi HĐ chỉ có dịch vụ (vá ngoài luồng 19.4).
  - Màn Chi tiết (`_id/index.vue`): cùng cấu trúc (16 cột, giữ Ghi chú) + `tfoot` Tổng; `paymentSummary` tách Dịch vụ / Chi phí (trước gán cứng Chi phí = 0); cột Mã `text-nowrap`.
  - Verify: Sửa — BG-2026-00155 (hàng + 1 DV) A 883,515,152 + B 3,240,000 = Tổng 886,755,152; BG-2026-00185 (chỉ DV: 3 DV + 1 CP) Tổng 26,676,000, tổng hợp DV 24,516,000 · CP 2,160,000 · VC 1,836,000 · HĐ 28,512,000 = `summary_breakdown` BE; 1 bảng, mục/Tổng thẳng cột thead, không cuộn ngang, 0 lỗi console, 0 request ghi. Chi tiết — giả lập API chi tiết bằng dữ liệu 2 báo giá trên (page.route, không ghi DB): cùng số, thẳng cột, 0 lỗi.
  - Spec: L1 đổi tên tab, thêm `P19-L7` (chưa chạy).
  - Dữ liệu test (27/10, DB local `hrm_erp_21_10_prod`, user cho phép): **BG-2026-00442 (id 501)** do NV 50 tạo bằng Sao chép BG-2026-00311 trên giao diện + thêm 2 DV (cost 560, 259) + 1 CP (cost 533) + vận chuyển 1,500,000; rồi `UPDATE quotations SET status=7` đúng 1 dòng (bỏ qua luồng duyệt). Tổng 138,132,000 (HH 103,572,000 · DV 30,780,000 · CP 2,160,000 · VC 1,620,000). Xoá khi không dùng nữa.
- [x] 19.7 Bảng Tổng hợp thanh toán rộng thêm 2 cột (27/10, CHƯA commit; user cho phép): `edit.vue` tfoot ô trống colspan 11→9, nhãn 3→5, tiêu đề 4→6 ⇒ chiếm 6 cột cuối (từ cột GG %), rộng 524px ở 1512; đo: mép trái = cột GG %, mép phải = mép bảng, số thẳng cột cuối, khe 0 với dòng Tổng, 0 lỗi console. Spec L3 thêm kiểm mép trái.
- [x] 19.8 Ô chỉ đọc đúng chuẩn chung (27/10, CHƯA commit; user cho phép sửa GỐC component): đo 12 ô khoá màn Lập HĐ — nền #f1f5f9 / chữ #475569 / viền #e2e8f0 đã đúng nhưng **mờ 0.6** do `components/V2BaseFloatingField.vue` `.ff.is-disabled { opacity: .6 }` (commit 3b4dc465c 02/09) — trái skill select-and-input-state mục 3 "không opacity". Bỏ opacity (giữ pointer-events) + `.ff.is-disabled:not(.is-float) .ff__label { background: transparent }` (bỏ mờ làm lộ mảng nền notch trắng trên ô khoá TRỐNG). Ảnh hưởng mọi màn dùng ô floating khoá (10 file khác: bộ lọc báo cáo assign/report/*, sale/prepick-tracking, InternalPricePolicyPanel, ProductListPage, ProductPickerAdvancedFilters) — đo prepick-tracking + 2 báo cáo: opacity 1, không lỗi. Spec L2 thêm kiểm màu ô khoá.
- [x] 19.9 3 chỉnh UI (27/10, CHƯA commit; user ra lệnh "sửa 3 ý"): `edit.vue`
  - Bên B: chữ "Khách hàng · Tổ chức" → "Khách hàng" + `V2BaseBadge` (#0284c7) có icon theo loại KH (nhãn theo danh mục `customers/index.vue` renderCustomerType): 1 Cá nhân `ri-user-3-line` · 2 DN tư nhân `ri-building-2-line` · 3 DN nước ngoài `ri-global-line` · 4 Tổ chức phi chính phủ `ri-hand-heart-line` · 5 Cơ quan nhà nước `ri-bank-line` (đã render thử cả 5 glyph — không dính lệch codepoint remixicon).
  - Dấu * đỏ sau tên tab có trường bắt buộc: Thực hiện · Giao hàng · Điều khoản thanh toán (trước chỉ tab Điều khoản).
  - Radio Lắp đặt lệch 7.5px xuống (tâm radio 552.5 vs tâm khung 545, tràn đáy khung) do `V2BaseRadio` `.v2-radio__wrapper { margin-top: 15px }` ⇒ đè `margin-top: 0` trong `.hd-radio-box` (khuôn `InternalPricePolicyPanel.vue:1220`, không sửa component chung). Sau sửa: tâm 545/545.
  - Spec: thêm `P19-L8` (chưa chạy).
  - Lưu thử HĐ từ BG-2026-00442 (để kiểm màn Sửa/Chi tiết): đã điền đủ form trên MCP (Số HĐ `HĐ-TEST-27102026`, TK, người ký, phòng KDTM 100%, Lắp đặt Có, 1 đợt 100%) nhưng bước bấm "Lưu nháp" bị auto mode chặn (ghi DB dùng chung) ⇒ CHƯA lưu, chờ user.
- [x] 19.5 Chuẩn hoá lề nội dung ↔ topbar/sidebar theo màn mẫu `/finance/buy-service-requests` (27/10, CHƯA commit; user cho phép 7 màn):
  - Khuôn chuẩn: thẻ gốc `v2-styles min-vh-100 pt-2 > container-fluid` ⇒ rule chung `assets/scss/v2-styles.scss:100` bỏ padding ⇒ khối cách sidebar **10px**, bắt đầu **y = 70** (chỉ còn lề layout `default-sidebar`). Không sửa file chung.
  - Sửa: `contracts/_id/edit.vue` + `index.vue` (bỏ `px-3`, index `pt-1`→`pt-2`), `support-accounting.vue` (`container-fluid px-0`), `report/performance-by-employee` (bỏ `.perf-report-page{padding:16px}`), `finance/product-prices` + `product-price-approvals` (thêm `min-vh-100` để rule chung áp vào).
  - Phạm vi: `inventory.py --root <worktree> --format paths` ⇒ 329 route màn mới; đo DOM 268 route tĩnh (script `gap-sweep.cjs`, mở tạm 71 mục menu_settings — sao lưu `scratchpad/menu_hidden_all_backup.json`). 210 màn mở được, lệch thật chỉ 7 màn trên; sau sửa đo lại cả 7 = 10px / y 70 (2 màn HĐ cần id ⇒ đo mép trong khung).
  - Để nguyên (có chủ đích / user chọn): `assign/tasks/daily-report` (hàng công cụ ngày + "Lưu tất cả" phía trên, lề đã 10px); màn tiêu đề `PageHeader` kiểu cũ (`admin/setting/manpower`, `training/*/add`, `insurance/setting/insurance-rate`); layout `default` menu ngang (`human/settings`, `timesheet/setting/*`, `payroll/setting/*`, `assign/my-job`); `change_password`, `customer-care/service-price-config` (form hẹp căn giữa); màn mở đầu bằng hàng tab/nút.
  - Chưa đo: route động (chi tiết/sửa) — chỉ quét tĩnh khung gốc (bắt được 3 màn HĐ).
  - ⚠️ Ngoài luồng: `assign/settings/price-approval` chữ mô tả "Dưới mức này, báo giá sẽ hiện cảnh báo đỏ." đang tô ĐỎ (vi phạm luật chữ đỏ chỉ cho lỗi validate).
  - ✅ ĐÃ SỬA ở 19.6 — ngoài luồng (từ 19.4): báo giá chỉ có dịch vụ, không có hàng (vd BG-2026-00185) ⇒ `tfoot v-if="lineRows.length"` ẩn luôn cả bảng Tổng hợp thanh toán, HĐ không thấy tổng giá trị.

## Phase 20 — Mẫu in, chế độ in, QR, ẩn giá (27/10 — code xong 2 đợt + e2e xanh, CHƯA commit)
- [x] 20.1 Khảo sát ERP (`FirmContractPrint`, `print_templates` type 1/12, tab Mẫu in, modal chọn chế độ) + hạ tầng HRM (khuôn `wr-service-contracts`, `ReportPrintPreviewModal`, `PrintsCompanyLetterhead`) → `design-phase20-mau-in.md`.
- [x] 20.2 User chốt 11 câu (`design-phase20-mau-in.md` mục 5–6).
- [x] 20.3 Plan chi tiết B1–B8 / F1–F6 ở `design-phase20-mau-in.md` mục 7.
- [x] 20.4 User cho phép code theo 2 đợt (27/10). Đợt 1 = mẫu in + chế độ in + QR; Đợt 2 = ẩn giá.
- [x] 20.5 ĐỢT 1 (27/10, CHƯA commit; nhánh `gop_db-hop-dong-ban` cả 2 repo):
  - BE: `PrintTemplateVariable` loại 7 "Hợp đồng bán hàng" + 3 loại con `sale_contract` / `sale_contract_product_annex` / `sale_contract_handover`, biến = đúng tập mẫu ERP đang dùng (đo từ 25 mẫu + rt106); `PrintTemplateRequest` bắt sub_type cho loại 7; migration `2026_10_28_000001_add_print_template_columns_to_hrm_contracts_table` (print_template_id, template, template_print_product — ĐÃ CHẠY local, user cho phép); `PrintTemplateService::referencingTables` + hrm_contracts; seeder `Modules/Assign/Database/Seeders/SaleContractPrintTemplatesSeeder` chép 17 HĐ + 8 biên bản + PLHH_HDBH (ĐÃ CHẠY local: 26 mẫu); Store/Update nhận 3 trường (nullable), `ContractService::submit` → `assertPrintTemplatesFilled` (422 cả 3 ô); `DetailContractResource` + print_template_id/name/template/template_print_product; `GET assign/contracts/print-templates?sub_type=` + `GET assign/contracts/{id}/print-data?mode=contract|product_annex_1|product_annex_2|handover` (gate `scopedContractQuery` — KHÔNG công khai như ERP); `ContractPrintService` (port FirmContractPrint: bảng tổng hợp / theo nhóm, chi phí–dịch vụ–vận chuyển–tổng, đợt thanh toán + bằng chữ, biên bản 4 biến thể, letterhead theo company_id HĐ, escape `$`/`\` trước fillReport, qr theo status {6, 8, 12, 11}).
  - FE: màn quản lý mẫu (add/edit) mở loại con cho loại 7 ("Loại mẫu"); `edit.vue` tab "Mẫu in *" (trước Đính kèm) — `V2BaseSegmented` 2 tab con ở hàng tab, select mẫu HĐ (`$confirm` khi đổi lúc đã có nội dung) + `CompactReviewEditor` full toolbar, phụ lục điền sẵn mẫu đầu tiên, Trình duyệt bắt 3 ô (tab đỏ, mở đúng tab con); `ContractPrintModal` (chế độ in + Tổng hợp/Chi tiết theo nhóm + mẫu biên bản/người giao/người nhận/chức vụ/SĐT) + `contractPrintMixin` (gọi print-data, QR SVG 12mm bằng gói `qrcode` FE trỏ màn Chi tiết HĐ) ở màn Chi tiết (nút "In" secondary) + màn Danh sách (hành động "In" trong ⋮); màn Chi tiết thêm mục "Mẫu in" chỉ đọc.
  - Sửa kèm (user cho phép): `utils/directives/overflowTooltip.js` — `.always` + giá trị rỗng không lấy textContent (ô TK ngân hàng chưa chọn hiện tooltip 1,416 ký tự cả danh sách; rà 12 chỗ `.always` đều truyền giá trị).
  - Verify: endpoint 200/403/422; render 5 chế độ bằng HĐ dựng trong bộ nhớ từ BG-2026-00442 (không ghi DB), đối chiếu biến mẫu ↔ biến service: thiếu duy nhất `DANH_SACH_SAN_PHAM` (mẫu PHU_LUC_HOP_DONG_DAI_LY — ERP cũng không điền); FE màn Chi tiết (giả lập API): 5 chế độ gửi đúng tham số, xem trước có bảng + QR 45px (=12mm) sát mép phải, letterhead tải được, 0 lỗi console; tab Mẫu in 17 mẫu, chọn mẫu chép 3,888 ký tự; Lưu nháp 0 lỗi mẫu in, Trình duyệt tab Mẫu in đỏ; BE assert 3 ca (rỗng / chỉ &nbsp; / đủ); màn quản lý mẫu sửa HD-02A: loại + loại mẫu + 62 biến; tooltip TK: chưa chọn 0, đã chọn đúng tên.
  - Spec: L1/L4/L5/L8 theo tab mới + `P20-M1` (chưa chạy).
  - CHƯA kiểm với HĐ thật đã lưu (DB chưa có HĐ, lưu thử bị auto mode chặn).
  - ⚠️ Ngoài luồng (chưa sửa): `ContractController::show()` không gate quyền xem (ai biết id đều xem chi tiết); serial ở biên bản để trống (HĐ HRM chưa gắn serial — serial nằm ở phiếu xuất); `CHUC_VU_NGUOI_THEO_DOI_BEN_A` để trống (HRM chưa lưu chức vụ người liên hệ); màn edit.vue chưa dùng mixin cảnh báo chưa lưu.
- [x] 20.6 ĐỢT 2 — ẩn giá (27/10, CHƯA commit; user chốt mục 8 design-phase20 + dùng CHUNG quyền có sẵn "Xem hợp đồng ẩn giá" id 1571 nhóm HĐ dịch vụ như ERP ⇒ KHÔNG thêm quyền, KHÔNG ghi DB):
  - BE `ContractController`: `visibleContractQuery()` (có quyền ⇒ mọi HĐ trừ "Đang tạo" người khác + cột `hide_price` = CASE id IN (scopedContractQuery) — 1 truy vấn con, không N+1; không quyền ⇒ scopedContractQuery + hide_price 0) dùng cho index / export / print-data; `isPriceHidden()` cho show + support-accounting (403); print-data: ẩn giá ⇒ hợp đồng/phụ lục 403, biên bản in không giá; export ghi `*****` 2 cột tiền.
  - `ContractResource`: `hide_price`, `MONEY_FIELDS` null, `is_can_approve` false khi ẩn giá. `DetailContractResource::maskPrices()` null header (sales_bonus, shipping_*, total_*) + dòng hàng/dịch vụ (estimated/quoted/extra/discount_*/allocated) + giảm giá + số tiền đợt thanh toán (giữ %).
  - `ContractPrintService`: biên bản `CHI_TIET_CO_GIA*` không cột giá khi hide_price (vá lỗ ERP).
  - FE: danh sách 2 cột tiền `*****`; Chi tiết: `formatMoney`/% giảm giá `*****`, ẩn Hỗ trợ hạch toán + Duyệt (khớp is_can_approve); `ContractPaymentTermsTable` prop `hidePrice` (*****, tắt cảnh báo lệch tổng); popup In chỉ còn biên bản.
  - Verify: list + export 200 với SQL truy vấn con (NV 50 có quyền 1571); resource in-memory: ẩn ⇒ mọi tiền null (giữ % đợt), thường ⇒ số thật; biên bản CÓ GIÁ ẩn giá ⇒ 0 cột Đơn giá/Thành tiền; FE giả lập API: ẩn giá ⇒ 84 ô *****, 0 số tiền lọt, không nút HTHT, popup in 1 chế độ, danh sách *****; HĐ thường ⇒ số thật, đủ nút, 4 chế độ in; 0 lỗi console.
  - Spec mới `e2e/tests/assign/contracts-hide-price.api.spec.ts` (H1 không quyền · H2 chỉ quyền ẩn giá · H3 ẩn giá + xem tất cả — fixture SQL + role tạm, tự dọn) — CHƯA chạy (logic CASE với dữ liệu thật chỉ được kiểm khi chạy spec này).

- [x] 20.7 Chạy e2e (27/10, user yêu cầu; worktree: BASE_URL 3060 · API_BASE 8060 · API_REPO wt-hop-dong-ban/hrm-api, --workers=1):
  - `contracts-hide-price.api` 3/3 ✓ (H1 không quyền · H2 chỉ quyền ẩn giá · H3 + xem tất cả — logic CASE ẩn giá đúng với dữ liệu thật).
  - `contracts-list.api` 8 ✓ + 2 skip (Q2 bộ phận, Q3 phòng ban): tài khoản test NV13 có cờ tổng `company_employees.all_department = 1` ⇒ 2 cấp đó ra MỌI phòng, không kiểm được. Sửa spec: điều kiện "quản lý tất cả" xét cả 2 nguồn (trước chỉ xét dòng employee_manage_departments ⇒ Q2/Q3 đỏ giả); fixture implement_departments thiếu `department_name` (NOT NULL trên DB gộp).
  - `contracts-filter` 9/9 ✓ — sửa F6: chờ <select> Nhóm ngành / danh sách Ứng dụng nạp xong mới mở (danh mục nạp bất đồng bộ ⇒ đỏ ngẫu nhiên).
  - `contracts-form-layout` 9/9 ✓ — NV13 không có báo giá trúng thầu chưa lập HĐ ⇒ chạy bằng phiên NV50 (BG-2026-00442): sao lưu `.auth/user.json`, ghi token NV50, `--no-deps`, chạy xong trả lại.
  - Dữ liệu fixture tự dọn: 0 HĐ E2E, 0 role tạm.

## Phase 21 — Kiểm với HĐ THẬT đã lưu (28/10, user cho phép tạo HĐ test)
- [x] Tạo HĐ nháp id 83 từ BG-2026-00442 qua giao diện (NV 50): Lưu nháp thiếu ô ⇒ báo đỏ đồng thời mọi ô bắt buộc ✓; POST/PUT 200; chọn mẫu HD-02A lưu được.
- [x] Màn Sửa / Chi tiết: bảng gộp A/B, Tổng hợp thanh toán, khối Mẫu in, nút Quay lại · In · Sửa · Xoá · Trình duyệt ✓. In 5 chế độ (HĐ tổng hợp / chi tiết nhóm / phụ lục 1 / phụ lục 2 / biên bản BBBG-04A) đều 200, không sót `{{…}}`; HĐ nháp không QR (đúng).
- [x] Lỗi 1 — bản in đoạn thanh toán ra "0 đồng (Không đồng)": `ContractPrintService::paymentText()` đọc `amount` (= ô "Số tiền thanh toán", thường trống). Sửa: số tiền đợt = round(% × tổng sau VAT / 100) như ERP (`app.directive.js:768`), đợt không nhập % mới lấy `amount`. Kiểm lại: 100% ⇒ 138,132,000 + chữ đúng.
- [x] Lỗi 2 — chữ phụ `.text-muted` ra ĐỎ: "Chưa có tệp đính kèm", "Không tìm thấy hợp đồng.", "Đang tải lên..." (`_id/index.vue`), "Chưa có phòng thực hiện." (`support-accounting.vue`), 2 dòng `ContractExportRequestModal.vue` ⇒ class scoped `.hd-muted` #6b7280. Đo DOM: rgb(107,114,128) ✓ (popup đề nghị xuất kho chưa mở được trên HĐ nháp — cùng class, chưa đo).
- [x] Xoá HĐ 83 qua API Xoá; 0 dòng sót ở các bảng `hrm_contract_*`.
- [x] Gate QUYỀN XEM (user chốt "giống ERP" FirmContract::canView): `ContractController::findViewableContract()` dùng cho show / support-accounting / print-data — trong phạm vi danh sách (4 cấp + người lập + quyền ẩn giá) HOẶC được cấp truy cập `isViewableByAccessGrant()` (HĐ đã qua Đang tạo: quyền "Duyệt hợp đồng" khi Chờ duyệt · NV thuộc phòng HỖ TRỢ is_main=0; thấy giá như ERP). Không tồn tại 404, không quyền 403. Bỏ `isPriceHidden()` (hide_price lấy từ cột tính sẵn).
- [x] FE: màn Chi tiết 403 ghi "Bạn không có quyền xem hợp đồng này." (trước ghi "Không tìm thấy"); Chi tiết / Sửa / HTHT không toast lặp khi 403 (interceptor axios đã toast). Đo: chữ xám rgb(107,114,128), 1 toast; màn Sửa 403 về danh sách.
- [x] E2E `contracts-hide-price.api`: H1 thêm show/HTHT 403 + 404; P21-V1 người duyệt (Chờ duyệt 200 + thấy giá, trạng thái khác 403); P21-V2 phòng hỗ trợ (200, Đang tạo 403, gỡ phòng 403) — 5/5 ✓.
- [x] Cảnh báo thoát khi chưa lưu (skill unsaved-changes) ở màn Sửa + Lập (`create.vue` extends `edit.vue`): `unsavedChangesMixin`, snapshot = báo giá nguồn + form + đợt thanh toán + phòng thực hiện (đính kèm lưu ngay qua API ⇒ không tính); `markFormPristine()` cuối `mounted` (sau khi nạp TK ngân hàng / mẫu in) và sau mỗi lần lưu thành công; `markFormSaved()` trước khi sang Chi tiết (Lưu nháp / Trình duyệt). Playwright (điều hướng SPA): chưa sửa thoát thẳng ✓ · sửa Số HĐ → popup, Ở lại giữ "ABC", Thoát về danh sách ✓ · sửa rồi trả lại không hỏi ✓ · thêm đợt thanh toán hỏi ✓ · đổi route khác hỏi ✓ · màn Sửa (dữ liệu giả lập) nạp xong không hỏi ✓, Lưu nháp (PUT mock) sang Chi tiết không hỏi ✓, F5 khi đã sửa ⇒ hộp thoại beforeunload ✓. E2E: thêm ca `P21-U1` vào `contracts-form-layout` (chưa chạy).
- [x] E2E 4 spec hợp đồng (28/10): list + filter + hide-price 18 ✓ + 2 skip (Q2/Q3 tài khoản test) · form-layout 10/10 ✓ (phiên NV50; sửa spec P21-U1 chờ `$nuxt` sẵn sàng sau goto).
- [x] Commit Phase 21 (CHƯA push): api `3537a0c80`, client `c42bda740` trên `gop_db-hop-dong-ban`.
- [x] (28/10, sau commit) Nhãn nổi của ô CHỈ ĐỌC còn dải nền trắng lấn 5.5px vào ô xám — sửa GỐC `components/V2BaseFloatingField.vue` (áp mọi màn dùng ô floating): `.ff.is-disabled.is-float .ff__label` nền gradient nửa trên notch trắng / nửa dưới #f1f5f9 (nền chuẩn mọi ô khoá, `v2-styles.scss:51`). Đo màn Lập HĐ: 11/11 nhãn đúng, tâm nhãn = viền trên; nhãn ô thường + ô khoá trống không đổi. E2E L2 thêm kiểm. CHƯA commit.
- [x] (28/10) Cột Mã + Tên hàng bảng "Chi tiết hợp đồng" (màn Lập/Sửa) bị cắt "…" (khuôn MISA 1 dòng) — user yêu cầu hiện đủ: `edit.vue` ô Mã/Tên phần A + B thêm class `wrap` (white-space normal, overflow-wrap anywhere), bỏ v-overflow-tooltip ở 2 ô (giữ tooltip icon ghi chú), cột Mã 120→150px. Đo HĐ 94 ở 1512: trước 12/14 ô cắt (Tên 206px chứa tới 668px) → sau 0/14, mã 1 dòng (trừ mã dòng con lùi lề ngắt ở "-"), tên 2–5 dòng, bảng vẫn vừa khung (1407px, không cuộn ngang). Màn Chi tiết vốn đã xuống dòng — không sửa. E2E L7 thêm kiểm. CHƯA commit.
- [x] (28/10) Bảng "Chi tiết hợp đồng" (màn Lập/Sửa) trượt ngang với thanh cuộn TRÊN + DƯỚI theo chuẩn chung: bọc `components/V2BaseTableScroll.vue` (skill list-page mục 3b-1) thay `.hd-tbl-wrap`; cột Tên hàng cố định 300px, `.hd-goods` min-width 1340→1532px. Đo HĐ 94 ở 1512: bảng 1532 > khung 1407 ⇒ thanh trên hiện (cao 8px, ruột 1532px = bề rộng bảng), kéo thanh trên → bảng trượt (80), kéo bảng → thanh trên theo (30); trang không cuộn ngang; tên hàng 0 ô cắt. Đánh đổi: ở 1512 cột "TT sau VAT" + số của Tổng hợp thanh toán nằm ngoài khung đầu, phải trượt mới thấy. E2E L3 đổi từ "vừa khung" sang kiểm cuộn ngang + đồng bộ 2 chiều. CHƯA commit.
- [x] (28/10) E2E `contracts-form-layout` (--workers=1, phiên NV50, worktree 3060/8060): **10/10 passed** sau 3 sửa (nhãn ô khoá · Mã/Tên xuống dòng · trượt ngang). Lượt đầu L3 đỏ do locator `xpath=ancestor` trong spec (không phải lỗi màn) → đổi `locator(".v2-table-scroll", { has })`.
- [x] (28/10) Màn Chi tiết `/assign/contracts/{id}` dựng lại theo UI màn Tạo/Sửa (user chọn: dựng lại index.vue + dùng chung CSS; Lịch sử thành tab cuối; cho phép "Làm"): style màn Sửa tách ra `pages/assign/contracts/components/contract-form.scss` (edit.vue + index.vue cùng import; root thêm class `contract-form`; dấu * tab chỉ áp `.contract-edit`). index.vue: 2 khối (Thông tin hợp đồng · Các bên ký kết, ô floating KHOÁ) + 7 tab (Chi tiết HĐ · Thực hiện · Giao hàng · Điều khoản TT · Mẫu in · Đính kèm · Lịch sử n); "Ký hợp đồng" nhập vào Bên A (Người ký, Chức vụ); "Thông tin thanh toán" + "Tổng giá trị" → chân bảng như màn Sửa; footer/popup/logic duyệt-in-xuất hàng giữ nguyên. Đo HĐ 94 ở 1512: cao 4,409 → 1,550px, 31 ô floating đều 32px, 0 ô sửa được, 0 dấu *, mọi tab có nội dung, hàng tab không nhảy; màn Sửa đo lại không đổi (ô 32, khối/nền, dấu * 4 tab, nhãn gradient, thanh trượt). Spec mới `contracts-detail-layout.spec.ts` D1–D5 (D5: BE 403 ⇒ hiện câu BE). E2E (--workers=1, NV50, 3060/8060): detail-layout 5/5 + form-layout 10/10 = **15 passed**, 0 skip. CHƯA commit.
- [x] (28/10) Ghim cột cuối "TT sau VAT" bảng Chi tiết HĐ (cả màn Sửa + Chi tiết, `contract-form.scss`): `position: sticky; right: 0` cho th cuối + td cuối mọi dòng (trừ dòng nhóm / dòng trống colspan 15 và tiêu đề "Tổng hợp thanh toán" colspan 6), bóng mép trái. Tái hiện trước: lúc mở màn cột cuối + Tổng giá trị HĐ hiện 0/116px; sau: 19 ô cột cuối sát mép phải khung (1486px) cả khi scrollLeft 0 lẫn trượt hết, Tổng giá trị HĐ thấy đủ ngay; ô Thưởng NVKD (màn Sửa) vẫn bấm được. E2E L3 + D3 thêm kiểm.
- [x] (28/10) Việc tồn — e2e chữ thanh toán bản in: `contracts-hide-price.api` P21-T1 (HĐ fixture M: mẫu `{{THANH_TOAN}}`, vận chuyển 1,000,000 + VAT 10% = tổng 1,100,000; 3 đợt 30% / 70% / không % mà số tiền 50,000) ⇒ "330,000 đồng (Bằng chữ: Ba trăm ba mươi nghìn đồng)", "770,000 đồng", "50,000 đồng", không còn "là: 0 đồng". afterAll dọn `hrm_contract_process_payments`.
- [x] (28/10) Việc tồn — nhãn NV chuẩn "Tên - Mã phòng - Mã NV" (`utils/employeeOptionText`): edit.vue `employeeOptions` (Người ký) + `employeesFull` (Phòng thực hiện); index.vue cùng 2 computed + `employeeName` (ô Người ký chỉ đọc). Tái hiện trước: "HN_KD2 - Nguyễn Văn Mởn", "HDQT - Nguyễn Trung Phong" (BE ghép sẵn name = "Mã phòng - Tên"); sau: "Nguyễn Văn Mởn - HN_KD2 - 11710174", "Nguyễn Trung Phong - HDQT - 19910001", 646 option đúng khuôn. E2E P21-N1 (form) + D6 (chi tiết) so nhãn với dữ liệu NV trong store (lần đầu viết regex đỏ giả vì mã phòng có "-" / khoảng trắng: "HN-DATD", "Bộ Phận hỗ trợ KD_SG").
- [x] (28/10) E2E (--workers=1, NV50, 3060/8060): `contracts-hide-price.api` 6/6 (gồm P21-T1) · `contracts-detail-layout` 6/6 · `contracts-form-layout` 11/11. CHƯA commit.
- [ ] E2E: chưa có ca kiểm đoạn thanh toán trong bản in (fixture HĐ E2E không có dòng hàng ⇒ tổng 0) — bổ sung khi chạy lại bộ test.

## Việc còn mở
- [ ] Merge `gop_db-hop-dong-ban` về `gop_db` (Phase 18–20 ĐÃ commit + push 28/10: api `f43174d2e`, client `09a88e317` lên `origin/gop_db-hop-dong-ban`; nhánh còn mang 2 commit Phase 17 lấy từ `develop`). Deploy cần: migration `2026_10_23_000001` + `2026_10_27_000001` (index danh sách) + `2026_10_28_000001` (cột mẫu in) · seeder quyền (đổi tên 4 quyền Phase 18) · `SaleContractPrintTemplatesSeeder` (chép 26 mẫu ERP) · màn Cài đặt phân hệ nếu có mục menu mới.
- [x] Kiểm với HĐ THẬT đã lưu — xong 28/10 (Phase 21), sửa 2 lỗi.
- [ ] Đối chiếu HTHT với HĐ ERP thật.
- [ ] Để sau (design.md mục 4): duyệt đa cấp, cảnh báo, Chuyển duyệt BGD/notify, phụ lục (giảm/bổ sung), giao hàng #11252, quyết toán.
- [ ] Khi merge nhánh `rbac`: `ContractService` (kiểm role Giám đốc) + `ContractResource` (đệm quyền) đổi cách kiểm — thử lại Duyệt vượt hạn mức.
- [ ] Ngoài luồng (ghi lại, chưa sửa): ~~`show()` không gate quyền xem~~ (xong Phase 21) · ~~`edit.vue` chưa dùng mixin cảnh báo chưa lưu~~ (xong Phase 21) · biên bản: serial trống (serial ở phiếu xuất), `CHUC_VU_NGUOI_THEO_DOI_BEN_A` trống · ~~option NV ở Phòng thực hiện lệch chuẩn "Tên - Mã phòng - Mã NV"~~ (xong 28/10, kèm ô Người ký) · `assign/settings/price-approval` chữ mô tả tô đỏ · CheckboxMultiSelect / ô floating chọn nhiều cao lệch khi có chip · cụm Công ty bắn 2 request.
- [x] (29/10) TK ngân hàng Bên A màn Chi tiết thêm tiền tệ: BE `DetailContractResource.company_account_currency_name` (đọc `companyAccount.currency` — eager-load trong `DETAIL_RELATIONS`, không snapshot) + `_id/index.vue` `companyAccountLabel` cùng khuôn option màn Sửa. Đo HĐ 94: Chi tiết = option đang chọn ở Sửa ("0531100096008 - VNĐ tại …"), ô 32px, 0 lỗi console. E2E D7 (`contracts-detail-layout`, chưa chạy). CHƯA commit.
- [ ] Dọn DB local khi user báo test xong: role tạm 108470 + 108473 (gắn NV 50) · khôi phục `menu_settings` ẩn (2 bản sao lưu ở scratchpad session 27/10: `menu_hidden_sale_admin_backup.json` 54 mục, `menu_hidden_all_backup.json` 71 mục) · BG-2026-00442 (id 501, test) · xoá cache quyền.
- [ ] E2E chưa kiểm được: Q2/Q3 danh sách (cấp bộ phận / phòng ban) — cần tài khoản test KHÔNG có cờ `company_employees.all_department`.

### Khảo sát 29/10 — hiện trạng xuất hàng theo HĐ (chỉ đọc, chưa sửa)
- Luồng đã dựng từ 08/2026 (hồ sơ `gop-db/hop-dong-xuat-hang/plan.md`, checkpoint cuối 24/08): YCXH loại 21 (hàng cha) / 20 (hàng con) → ĐNXK → Phiếu xuất kho (màn HRM `/finance/warehouse-exports`) → Phiếu xuất hàng (hạch toán 8 cụm loại 21; loại 20 tự sinh phiếu nhập cha `ContractParentImportService`). Nút "Yêu cầu xuất hàng" ở Chi tiết HĐ (`can_export` = Có hiệu lực + có ngày hiệu lực + thời hạn thực hiện) + ô chọn HĐ HRM ở màn YCXH (`hrm-contracts`: cùng công ty, còn SL).
- DB local (dump prod 21/10): 0 phiếu loại 20/21 ở cả 4 bảng, 0 phiếu nhập cha; prod chưa có HĐ HRM ⇒ luồng CHƯA từng chạy với dữ liệu thật; Phase 3 E2E trọn vòng của hồ sơ cũ vẫn [ ].
- Lỗ hổng/điểm lệch: (1) `storeExportRequest` dùng `findOrFail` — không gate quyền xem / người lập (ai biết id HĐ Có hiệu lực đều lập YCXH được); (2) picker `hrm-contracts` không lọc người lập, trong khi loại 14 ERP bắt "đúng người" (commit `42e8779b6`) — cần chốt; (3) "SL còn được xuất" tính theo SL trên YCXH chưa huỷ, không theo SL đã xuất thật; (4) trạng thái HĐ không tự chuyển Đang/Đã xuất hàng (8/9) — ERP FirmContract cũng không tự chuyển ⇒ khớp ERP; (5) màn Chi tiết HĐ chưa có danh sách YCXH/ĐNXK/PXK/PXH liên quan (`onExportRequestCreated` để trống "bổ sung bước sau"); (6) quyết toán HĐ HRM (11/12) chưa có luồng.

- (29/10, user yêu cầu) Dữ liệu test xuất hàng: HĐ 94 `HĐ_TPE_HN_KD2_26_0001_NAMCHECK` (BG-2026-00442, cty 1, NV50) đưa lên **Có hiệu lực** qua luồng thật — đặt thời hạn 60 ngày theo hiệu lực (`recomputeEffectiveDates` ⇒ kết thúc 27/12/2026) → API submit → API approve bằng NV50 (NV13 bị middleware chặn quyền "Duyệt hợp đồng"). `can_export` = true; picker YCXH loại 21 + 20 đều ra HĐ 94. Tồn khả dụng kho 2: dòng 18 PULI (cha đơn) 53 · dòng 19 NAHU-NHXL-9102:01 (cha) **0** (tồn kế toán 1 nhưng bị ĐNXK đang chờ giữ) · dòng 20 con 8 · dòng 21 con 19.

- (29/10, user yêu cầu) Bơm tồn hàng cha 45616 NAHU-NHXL-9102:01 bằng chuỗi **Nhập hàng khác (99)** qua API thật: PYCNH-15589 (NV50, kho 2, 2 bộ) → PDNNK-11045 (NV50) → PNK-11609 (thủ kho NV311 Bùi Thị Thơm: lưu → xếp hàng vị trí 4639 LN-TACH-GHEP → Gửi; đính kèm = URL file sẵn có `warehouse_imports/pnk-10277pdf-…pdf`, KHÔNG upload S3) → PNH-15815 (NV50, Hoàn thành, 2 × 56,041,146 = giá vốn product_units, kho KT 1). Kết quả: YCNH status 5, PNK status 1; tồn vật lý cty 1 = 3, tồn KT kho 1 = 3; tồn khả dụng kho 2: cha 45616 = **2** (trước 0). Loại 99 không sinh bút toán (đúng ERP — chỉ hạch toán khi thuê ngoài bốc xếp). Dọn khi test xong: 4 phiếu trên + lô/tồn tương ứng.

### Phase 22 — Nút "Yêu cầu xuất hàng" ở danh sách HĐ (29/10, user cho phép code — XONG, CHƯA commit)
- Điều kiện: chỉ NGƯỜI LẬP HĐ (`created_by`) + HĐ Có hiệu lực (giữ `can_export`: có ngày hiệu lực + thời hạn thực hiện). Áp ở danh sách + Chi tiết + BE chặn API (cờ chung `is_can_create_export_request`).
- Bấm nút ở danh sách ⇒ sang màn Tạo YCXH đầy đủ (`/finance/product-export-requests/create?hrm_contract_id=`), loại 21, HĐ nạp sẵn (khuôn `prefillTransferRequest`).
- Picker HĐ HRM ở màn Tạo YCXH (`hrm-contracts`) lọc chỉ HĐ mình lập (khớp loại 14 ERP "đúng người").
- [x] BE: `Contract::getIsCanCreateExportRequestAttribute` (created_by = mình && can_export) · `ContractResource` + `DetailContractResource` trả `is_can_create_export_request` · `ContractController::storeExportRequest` 403 khi không phải người lập · `ProductExportRequestService::assertContractCreatedByMe` gọi ở `createFromContract` (mọi trạng thái, kể cả nháp) + `updateFromRequest` loại 20/21 · picker `hrm-contracts` lọc `c.created_by = auth()->id()` + nhận `id`.
- [x] FE: danh sách — hành động `export_request` (ri-truck-line, `to` màn Tạo YCXH, `visible` = cờ BE; rơi vào 2 nút chính khi không có Sửa/Xoá) · Chi tiết — nút cùng cờ, bấm ⇒ `$router.push` màn Tạo YCXH, bỏ dùng `ContractExportRequestModal` (giữ file) · `ProductExportRequestForm` — `prefillHrmContract()` từ `?hrm_contract_id` (khuôn `prefillTransferRequest`), nạp qua picker nên vẫn qua đủ điều kiện.
- [x] Verify API (NV50 người lập / NV13 không): cờ list + detail HĐ 94 = true (NV50); tinker: NV13 false, Chờ duyệt false, thiếu thời hạn false; NV13 POST contracts/94/export-requests 403, POST product-export-requests loại 21 nháp 422 "Chỉ người lập hợp đồng…", picker rỗng; không sinh phiếu.
- [x] Playwright (NV50, 1512): dòng HĐ 94 có nút icon 30×30 title "Yêu cầu xuất hàng" → màn Tạo YCXH loại 21, ô Hợp đồng `HĐ_TPE_HN_KD2_26_0001_NAMCHECK - …`, KH điền sẵn, 4 dòng hàng, `isFormDirty() = false`; nút ở Chi tiết → cùng màn, cùng kết quả; 0 lỗi console.
- [x] E2E mới `HRM/e2e/tests/assign/contracts-export-request.api.spec.ts` P22-X1…X5 (fixture `E2E-P22X-*` + role tạm "Xem tất cả", tự dọn).
- [ ] ĐỂ SAU (user 29/10): điều kiện "hàng hoá chưa xuất hết" — chưa chốt tính theo SL trên YCXH chưa huỷ hay SL đã xuất thật.

### Phase 23 — Bố cục phiếu YCXH loại 20/21 (29/10, user cho phép code — XONG, CHƯA commit)
- Mockup chốt: `mockup-ycxh-xuat-ban-hd.html` (6 vòng góp ý). Áp loại 20 + 21 (nguồn HĐ HRM), Tạo/Sửa + Chi tiết; 12 loại YCXH khác giữ nguyên.
- Khối Thông tin chung: Loại (4) · Hợp đồng (8, mã + ngày ký + hạn thực hiện) → KH chỉ đọc V2BaseInput disabled (KH 8 · MST 4 / Người liên hệ 3 · SĐT 3 · Địa chỉ 6), bỏ khung `ro-panel` → Hình thức xuất (V2BaseSegmented icon Qua kho / Xuất thẳng, 3) · Kho xuất (3) · Vận chuyển + km (3) · Cần lắp đặt (V2BaseSegmented, 3); Xuất thẳng ⇒ chỗ Kho + Vận chuyển thành dòng chú thích xám 6 cột (nút gạt không giãn) → Ghi chú = nút bút chì "Thêm ghi chú" mở textarea + "Bỏ ghi chú" (có chữ ⇒ `$confirm`); Chi tiết chỉ hiện khi có giá trị.
- Khối thu gọn được: thu gọn còn 1 dòng tóm tắt (HĐ · KH · cách xuất · lắp đặt).
- Bảng hàng: tiêu đề 2 tầng SỐ LƯỢNG (Theo HĐ · Đã YC · Còn lại · Tồn kho · SL xuất) / GIÁ TRỊ (loại 21); Model · Thương hiệu thành dòng phụ dưới Tên; hàng con thụt lề + icon `ri-corner-down-right-line` ở cột MÃ; V2BaseTableScroll; ghim "TT sau VAT", bóng chỉ khi đang trượt; dòng TỔNG = các dòng đang tick (SL xuất, TT bán, TT sau giảm, Tiền VAT, TT sau VAT). File đính kèm xuống sau bảng.
- User chốt 29/10: (1) tiêu đề khối GIỮ chữ thường 14px theo V2BaseFormCard (mockup vẽ IN HOA là lệch khuôn); (2) thu gọn = thêm prop `collapsible` (mặc định tắt) + slot `#summary` vào `V2BaseFormCard`; (3) icon người dùng thêm THẲNG vào `CreatorInfoLine` ⇒ hiện ở mọi màn (82 file).
- [x] `components/V2BaseFormCard.vue`: prop `collapsible` (mặc định tắt) + `collapsed` + slot `#summary` + sự kiện `toggle`; nút V2BaseIconButton ▾ trước tiêu đề, thân ẩn bằng v-show. Đo màn PNH-15815: head 38px, tiêu đề 14px, không nút thu gọn ⇒ màn cũ không đổi.
- [x] `components/CreatorInfoLine.vue`: icon `ri-user-3-line` 14px #94a3b8 trước dòng người tạo (mọi màn). Đo: glyph render đúng, tâm icon = tâm chữ.
- [x] `ProductExportRequestForm.vue` (Tạo/Sửa + Chi tiết, chỉ loại 20/21 — `isContractType` / `detailIsContractType`): khối Thông tin chung mới (thu gọn + tóm tắt), KH ô V2BaseInput disabled, V2BaseSegmented Hình thức xuất (icon) / Cần lắp đặt, chú thích Xuất thẳng 6 cột, Ghi chú bút chì + Bỏ ghi chú (`$confirm` khi có chữ; màn Chi tiết chỉ hiện khi có giá trị); bảng V2BaseTableScroll + tiêu đề 2 tầng (nhãn nhóm căn trái — căn giữa thì "GIÁ TRỊ" rơi khỏi vùng thấy) + STT 2.1 + icon lùi dòng cột Mã + V2BaseCheckbox/V2BaseInput + ghim TT sau VAT (bóng khi đang trượt, nghe scroll pha capture) + dòng TỔNG; File đính kèm sau bảng. Ô Hợp đồng: "mã · Ngày ký · Hạn thực hiện" (lấy từ picker; màn Sửa chỉ có mã vì `create-data`/show chưa trả ngày).
- [x] Sự cố giữa chừng: lần thay bảng 20/21 cắt nhầm tới "Box thông tin thanh toán" ⇒ mất bảng loại 14/15/4/17 (274 dòng) — đã khôi phục nguyên văn từ HEAD; so dòng HEAD↔hiện tại chỉ còn thiếu đúng phần cố ý thay; đổi loại 14/15/4/17/99 trên trình duyệt đều hiện đúng bảng cũ.
- [x] Playwright (NV50, 1512): mỗi hàng đủ 12 cột; Xuất thẳng 352/705/352, Cần lắp đặt không nhảy; thu gọn 424→42px, tóm tắt đủ chữ; ghi chú focus TEXTAREA, Bỏ trống không hỏi, có chữ hỏi (Hủy giữ / Bỏ xoá, form không bẩn); dòng TỔNG = paymentSummary (103,572,000 / 6,372,000), bỏ tick 1 dòng ⇒ SL khoá, dòng kia giữ tick; chọn/bỏ chọn tất cả đúng; bóng ghim nghỉ/đang trượt/cuối = không/có/không; loại 20 (không GIÁ TRỊ, không ghim, chọn hàng con); loại 99 bố cục cũ; Chi tiết 21 (giả lập API, không ghi DB) đúng bố cục + tổng; 0 lỗi console.
- [ ] Chưa tái hiện được: 1 lần (lượt kiểm bị lỗi giữa chừng) Cần lắp đặt tự thành "Có" (form.need_repair = 1); chạy lại từng bước (gạt hình thức xuất, thu gọn, ghi chú + popup, tick) đều giữ 0 — theo dõi khi user test.
- [x] (29/10, user cho phép) BE `ProductExportRequestController`: `create-data` loại 20/21 thêm `contract.sign_date`, `contract.execution_end_date`, `contract.customer_code`; `show()` thêm `customer_code` (theo `customer_id` phiếu — createFromContract có lưu). FE: `loadContractLines` nhận `customer_code` + `contractMeta` (2 mốc ngày) ⇒ ô Hợp đồng màn Sửa có ngày (màn Sửa cũng gọi create-data), ô Khách hàng "mã - tên" (Tạo/Sửa + Chi tiết). Sửa thêm `editData` (màn Sửa dựng form từ editData, KHÔNG gọi create-data — giả định ban đầu sai): trả `contract_sign_date`, `contract_execution_end_date`, `customer_code`; FE `applyInitialData` nhận vào `contractMeta`/`customerInfo`. Kiểm editData thật trong transaction rollback (2026-10-28 · 2026-12-27 · 29TPHPXU-1 · 4 dòng, 0 phiếu sót). Playwright: Tạo / Sửa / Chi tiết đều "mã · Ngày ký · Hạn thực hiện" + "mã KH - tên", form không bẩn, 0 lỗi console. E2E: L1 kiểm mã KH, ca mới L7 màn Sửa; chạy 2 spec **12/12 passed** (--retries=0), DB sạch.
- [x] (29/10, user yêu cầu) Bảng hàng bỏ nhóm cột SỐ LƯỢNG / GIÁ TRỊ ⇒ 1 hàng tiêu đề (Tạo/Sửa + Chi tiết); Địa chỉ dời xuống ngay dưới Khách hàng, cùng 8 cột; Người liên hệ gộp "Tên • SĐT" (4 cột, khuôn màn HĐ) để hàng đủ 12. Đo 1512: KH = Địa chỉ 939px cùng mép trái, MST = Người liên hệ 470px; thead 1 hàng, 0 ô gộp; ghim sát mép phải; 0 lỗi console. E2E L1 + L5 cập nhật.
- [x] (29/10) "Lần lọc đầu bị nuốt" ở danh sách HĐ = KẾT LUẬN NHẦM: spec bấm `getByRole('button', {name: /Tìm kiếm/}).first()` trúng nút "Tìm kiếm nâng cao". Đo lại bấm đúng nút lúc trang đang tải: request kèm keyword bắn đúng, 0 dòng ⇒ màn không lỗi, không sửa.
- [x] (29/10) Chạy e2e (worktree 3060/8060, NV13, --workers=1 --no-deps): lượt 1 4 passed · 2 failed · 5 did not run — cả 2 đỏ do SPEC: P23-L1 đọc innerText thay vì input.value (mã HĐ nằm trong ô input); P22-X5 chờ danh sách đúng 3 dòng sau ô tìm nhanh nhưng lần lọc đầu của list-page bị nuốt (lỗi có sẵn, memory hrm-list-page-2-loi-bo-loc-am-tham) ⇒ đổi sang chờ đủ 3 mã fixture. Lượt 2 (--retries=0): **11 passed**. DB sạch: 0 HĐ / dòng / role E2E, 0 YCXH gắn HĐ HRM.
- [x] (29/10, user cho phép) Nhãn form YCXH về chuẩn màn kho (đo PXG-02188 / Phiếu thu / PNH: nhãn 14px, cách ô 8px). Trước: `.fld { gap: 3px }` + `.v2-label { min-height: 18px }` ⇒ nhãn 18px, cách ô 11px. Bỏ 2 rule thì 5 loại (4, 14, 20, 21, 99) lệch hàng 4px ⇒ tìm GỐC: `<V2BaseLabel required>` vẽ * bằng span `.v2-label__required` không đặt line-height ⇒ 18px (màn mẫu dùng `<Required />` trong phần chữ ⇒ 14px). Sửa tại form: `.fld ::v-deep .v2-label__required { line-height: 1.2 }`. Đo 13 loại: nhãn 14px · cách ô 8px · 0 hàng lệch (trừ loại 14 — xem dưới); khối Thông tin chung 21 cao 403→398px. E2E L1 thêm kiểm nhãn; 2 spec 12/12 passed.
- [ ] Ngoài luồng (ghi lại, chưa sửa): (a) loại 14 hàng đầu — radio "Cần lắp đặt" tâm thấp hơn ô chọn 9px, ô tick "Xuất thẳng" 4px (có từ trước, bố cục cũ); (b) gốc chung: `components/V2BaseLabel.vue` `.v2-label__required` thiếu `line-height` ⇒ mọi `<V2BaseLabel required>` (181 chỗ) cao 18px thay vì 14px — sửa gốc là đổi cao nhãn ở 181 chỗ, cần user quyết.
- [ ] Để sau (user 29/10): chuẩn hoá toàn phần mềm ô "bấm mở popup tìm" — 2 kiểu song song: `V2BasePickerField` (6 file, chữ 13px) vs quy ước `.picker-input` (25 file, CSS chép tay 22 nơi) + ~11 chỗ tự làm; chưa chốt kiểu chuẩn (đề xuất: gom `.picker-input` thành component dùng chung).
- [x] E2E mới `HRM/e2e/tests/assign/contracts-export-request-layout.spec.ts` P23-L1…L6 (fixture `E2E-P23L-M1`, chặn request ghi).

### Checkpoint — 2026-10-28
Vừa hoàn thành: Phase 18 (danh sách: quyền 4 cấp + 17 ô lọc), Phase 19 (form gọn: 2 khối + 6 tab, bảng HĐ gộp hàng hoá/dịch vụ, tổng hợp thanh toán, lề chuẩn 7 màn, ô chỉ đọc không mờ, tooltip), Phase 20 (mẫu in loại "Hợp đồng bán hàng" + 26 mẫu ERP, tab Mẫu in, In hợp đồng / phụ lục mẫu 1-2 / biên bản, QR, ẩn giá dùng chung quyền "Xem hợp đồng ẩn giá"). E2E 4 spec: 29 passed, 0 failed, 2 skip (tài khoản test).
Đang làm dở: (không). Đã commit + push 28/10 (api `f43174d2e`, client `09a88e317`) lên `origin/gop_db-hop-dong-ban` (worktree `websites/wt-hop-dong-ban/`, API 8060 · client 3060 đang chạy).
Bước tiếp theo: kiểm với HĐ thật đã lưu → merge về gop_db (chờ user yêu cầu); hoặc sửa mục ngoài luồng (ưu tiên `show()` không gate quyền).
Blocked: lưu HĐ thử qua giao diện bị auto mode chặn (ghi DB dùng chung) — cần user tự lưu hoặc cho phép.

### Checkpoint — 2026-10-28 (chiều)
Vừa hoàn thành: Phase 21 — kiểm HĐ thật (id 83, đã xoá), sửa bản in đợt thanh toán 0 đồng + chữ phụ đỏ, gate quyền xem chi tiết/HTHT/in giống ERP, cảnh báo thoát khi chưa lưu ở màn Sửa/Lập.
Đang làm dở: (không). Phase 21 đã commit, CHƯA push: api `3537a0c80`, client `c42bda740`.
Bước tiếp theo: push Phase 21 khi user cho phép → merge về gop_db (chờ yêu cầu); hoặc mục ngoài luồng còn lại (biên bản serial trống, option NV Phòng thực hiện lệch chuẩn…).
Blocked:

### Checkpoint — 2026-10-28 (tối)
Vừa hoàn thành: sau commit Phase 21 — nền nhãn ô chỉ đọc (gốc V2BaseFloatingField) · Mã/Tên hàng xuống dòng · bảng Chi tiết HĐ trượt ngang (V2BaseTableScroll) + ghim cột "TT sau VAT" · màn Chi tiết dựng lại theo UI màn Sửa (style chung `pages/assign/contracts/components/contract-form.scss`, 2 khối + 7 tab) · nhãn NV chuẩn (Người ký + Phòng thực hiện) · e2e chữ thanh toán bản in. E2E: hide-price.api 6/6 · detail-layout 6/6 (spec mới) · form-layout 11/11.
Đang làm dở: (không). CHƯA commit (hrm-client: `components/V2BaseFloatingField.vue`, `pages/assign/contracts/_id/edit.vue`, `pages/assign/contracts/_id/index.vue`, mới `pages/assign/contracts/components/contract-form.scss`). Phase 21 (api `3537a0c80`, client `c42bda740`) đã commit, CHƯA push. Spec e2e nằm ngoài git (`HRM/e2e/tests/assign/contracts-*.ts`).
Bước tiếp theo: user báo commit đợt UI này → push nhánh `gop_db-hop-dong-ban` khi được cho phép → merge về gop_db (chờ yêu cầu). Mục ngoài luồng còn: biên bản serial trống / CHUC_VU_NGUOI_THEO_DOI_BEN_A trống, TK Bên A thiếu "VNĐ" ở màn Chi tiết.
Blocked:

### Checkpoint — 2026-10-29 (chiều)
Vừa hoàn thành: TK Bên A có tiền tệ (màn Chi tiết HĐ) · khảo sát xuất hàng theo HĐ · dữ liệu test HĐ 94 Có hiệu lực + chuỗi Nhập hàng khác (PYCNH-15589 → PDNNK-11045 → PNK-11609 → PNH-15815) cho hàng cha có tồn · Phase 22 nút "Yêu cầu xuất hàng" (người lập + Có hiệu lực, BE chặn 3 đường vào) · Phase 23 bố cục YCXH loại 20/21 (Tạo/Sửa + Chi tiết; V2BaseFormCard `collapsible`; icon CreatorInfoLine mọi màn; bảng 1 hàng tiêu đề; Địa chỉ dưới KH; BE create-data / editData / show trả ngày ký · hạn thực hiện · mã KH; nhãn về chuẩn 14px / cách ô 8px). E2E 2 spec 12/12 passed.
Đang làm dở: (không). ĐÃ commit + push 29/10 lên `origin/gop_db-hop-dong-ban`: api `29fae59d7` · client `2bdf1a8cf` (màn HĐ) + `1057d2f92` (YCXH), kèm Phase 21 (api `3537a0c80`, client `c42bda740`). Hết commit chờ push. Spec e2e ngoài git (`HRM/e2e/tests/assign/contracts-export-request*.ts`).
Bước tiếp theo: user test tay YCXH 20/21 → user báo commit (theo từng phần) → push khi được cho phép. Chờ user quyết: (1) lệch radio/ô tick YCXH loại 14 · (2) sửa gốc `V2BaseLabel` `.v2-label__required` line-height (181 chỗ) · (3) điều kiện "hàng hoá chưa xuất hết" · (4) chuẩn hoá ô "bấm mở popup tìm" toàn phần mềm. Dọn DB local khi test xong: HĐ 94 (Có hiệu lực), 4 phiếu chuỗi nhập 99, role tạm 108470 + 108473, BG-2026-00442.
Blocked:

### Checkpoint — 2026-10-29 (cuối ngày)
Vừa hoàn thành: commit + push nhánh `gop_db-hop-dong-ban` cả 2 repo — api `29fae59d7` (Phase 21–23), client `2bdf1a8cf` + `1057d2f92` (màn HĐ, YCXH 20/21); 0 commit chờ push, 0 file chưa commit. E2E `contracts-export-request{,-layout}` 12/12 passed (spec ngoài git).
Đang làm dở: (không).
Bước tiếp theo: user test tay YCXH 20/21 trên worktree (3060/8060) → merge `gop_db-hop-dong-ban` về `gop_db` khi user yêu cầu (deploy: 3 migration `2026_10_23_000001` / `2026_10_27_000001` / `2026_10_28_000001` + seeder quyền + `SaleContractPrintTemplatesSeeder`). Chờ user quyết: lệch radio YCXH loại 14 · sửa gốc V2BaseLabel dấu * (181 chỗ) · điều kiện "hàng chưa xuất hết" · chuẩn hoá ô bấm-mở-popup.
Blocked:

## Phase 24 — Bộ trạng thái Hợp đồng mới (30/10/2026 — BRAINSTORM, chưa code)
User gửi 15 trạng thái cần xây dựng: Đang tạo · Không duyệt · Chờ TP duyệt · Chờ pháp chế duyệt · Chờ BGĐ duyệt · Chờ KH ký (+ Hủy duyệt) · KH đã ký (popup bắt buộc file + ngày ký, cho chọn quá khứ) · Có hiệu lực (từ ngày hiệu lực) · Đóng (chỉ từ Chờ KH ký) · Đang thực hiện (khi xuất hàng / hạch toán DV / CP / thu tiền…) · Hết hiệu lực (quá thời hạn thực hiện) · Gia hạn chờ duyệt · Chờ quyết toán · Đang quyết toán · Đã quyết toán.

Khảo sát hiện trạng (chỉ đọc code + DB local):
| Trạng thái | Mức | Hiện trạng |
|---|---|---|
| Đang tạo | ✅ có | — |
| Không duyệt | 🟢 làm ngay | reject + `rejected_reason` có, nhưng trả về Đang tạo (3) ⇒ tách status riêng, đủ action như Đang tạo |
| Chờ TP duyệt | 🟢 | = Chờ duyệt (2); quyền "Duyệt hợp đồng" chưa ràng buộc phải trưởng phòng |
| Chờ KH ký | 🟢 | `approve()` đang nhảy thẳng Có hiệu lực (6) ⇒ đổi đích + action Hủy duyệt |
| KH đã ký | 🟢 | `sign_date` + bảng `files` có ⇒ popup xác nhận |
| Đóng | 🟢 | action mới, chỉ từ Chờ KH ký |
| Có hiệu lực | 🟢 | `effective_date` tự tính (ký / đặt cọc / bảo lãnh — `recomputeEffectiveDates`) ⇒ cần lệnh lịch hằng ngày (app/Console/Kernel chưa có lệnh cho HĐ) |
| Hết hiệu lực | 🟢 | `execution_end_date` có ⇒ cùng lệnh lịch |
| Chờ pháp chế duyệt | 🟡 cần chốt | phát hiện sửa mẫu in làm được (so `template` với mẫu gốc `print_template_id`); chưa có quyền / vai trò Pháp chế, chưa có bước duyệt |
| Chờ BGĐ duyệt | 🟡 | chỉ có điều kiện vượt hạn mức doanh số vượt trội ⇒ chỉ role "Giám đốc" duyệt (`assertExtraWithinLimitOrBgd`), không có bước/status riêng; "quy chế bắt buộc chuyển BGĐ" chưa có cấu hình (regulation-config chỉ có % đặt cọc, BGĐ duyệt giá hàng) |
| Đang thực hiện | 🟡 | YCXH / PXH 20/21 có (chưa chạy dữ liệu thật), thu tiền chọn được HĐ HRM (`BillIncomeRequestService::HRM_CONTRACT_SELECTABLE_STATUSES`)… nhưng KHÔNG nơi nào cập nhật status HĐ ⇒ chốt danh sách nghiệp vụ kích hoạt rồi móc từng nơi |
| Gia hạn chờ duyệt | 🔴 chưa có | chưa có Yêu cầu gia hạn HĐ (tham khảo `ProspectiveProjectExtensionRequest`) |
| Chờ / Đang / Đã quyết toán | 🔴 chưa có | chưa có quyết toán HĐ bán; `hrm_settlement_contracts` là module cũ, không gắn `hrm_contracts` (4 dòng, 0 trỏ HĐ bán); "đủ điều kiện quyết toán" chưa định nghĩa |

Lưu ý khi đổi bộ trạng thái: (1) status cũ không còn trong danh sách mới — Chờ hiệu lực (7), Đang xuất hàng (8), Đã xuất hàng (9), **Thanh lý (10, đang có nút + quyền "Thanh lý hợp đồng")**; (2) mã status ghi cứng ở nhiều nơi: `Contract::getCanExportAttribute` (6), picker `hrm-contracts` (6), `BillIncomeRequestService` (6/8/9/10/11/12), `ContractPrintService` QR (6/8/12/11), luồng nhập hàng bán trả lại (11/12), FE danh sách (bộ lọc 4 status); (3) dữ liệu cần chuyển đổi gần như không có (local chỉ HĐ test 94; dump prod 21/10 chưa có HĐ HRM).
- [x] (02/11) Chốt: GIỮ Thanh lý thành trạng thái thứ 16, chạy song song bộ mới — giữ mã status 10 (`STATUS_DA_THANH_LY`), nút + quyền "Thanh lý hợp đồng" như cũ; thu tiền vẫn chọn được HĐ Đã thanh lý. Hiện `liquidate()` chỉ cho từ Có hiệu lực (6) — còn hỏi: được Thanh lý từ những trạng thái nào trong bộ mới.
- [x] (02/11) Nguyên tắc user chốt: MỌI trạng thái HĐ do code tự chuyển khi một điều kiện / nghiệp vụ được hoàn thành — KHÔNG có chỗ cho user tự chọn trạng thái. Mỗi trạng thái trong design phải ghi rõ sự kiện kích hoạt. Thanh lý cũng theo luật này ⇒ cần chốt sự kiện kích hoạt thay cho nút bấm tự do hiện nay.
- [x] (02/11) User: "khai báo đủ bộ trạng thái trước, làm dần từng trạng thái". Chốt bảng mã (giữ 2/3/6/10/11/12, mới 13–22, bỏ 1/7/8/9 khỏi danh sách) — `design-phase24-trang-thai.md`.
- [x] 24.1 Khai báo đủ 16 trạng thái (02/11, user cho phép "Làm"; CHƯA commit) — nhánh `gop_db-hop-dong-ban` (worktree `wt-hop-dong-ban`):
  - api `Contract.php`: hằng số 13–22 (`STATUS_KHONG_DUYET` … `STATUS_CHO_QUYET_TOAN`), `getStatusList()` 16 mục theo thứ tự vòng đời, màu theo bảng chuẩn 3c-2; "Chờ duyệt" → "Chờ TP duyệt"; mã 1/7/8/9 `@deprecated`, bỏ khỏi danh sách. Đã quyết toán đổi màu #0EA5E9 → #16A34A (Hoàn thành).
  - client `pages/assign/contracts/index.vue`: `statusOptions` 16 mục.
  - BE lọc `whereIn` nhận mọi mã — không phải sửa. Không đổi luồng chuyển trạng thái (approve vẫn → 6, reject vẫn → 3, nút Thanh lý giữ).
  - Verify: tinker 16 mục; API NV50 `status=13` → 0 dòng, `status=6` / `2,6` → HĐ 94 "Có hiệu lực" #2563EB; Playwright 3060/8060: ô lọc 16 lựa chọn đúng thứ tự, chọn Không duyệt → request `status=13`, màn "Không có dữ liệu phù hợp bộ lọc.", badge rgb(37,99,235).
  - E2E: sửa `HRM/e2e/tests/assign/contracts-filter.spec.ts` P18-F2 theo 16 trạng thái (CHƯA chạy).
- [x] (02/11) User chốt THỨ TỰ làm tiếp: (1) logic mẫu in ⇒ quyết định khi nào qua Pháp chế duyệt · (2) logic duyệt từng bước tới Có hiệu lực · (3) luồng xuất hàng.
- [x] 24.2 Bước 1 — Mẫu in ⇒ cờ "cần Pháp chế duyệt" (02/11, user cho phép "Làm"; CHƯA commit) — thiết kế `design-phase24-trang-thai.md` mục Bước 1:
  - api: migration `2026_11_02_000001_add_legal_approval_to_hrm_contracts_table` (`need_legal_approval` tinyint 0, `template_original` longText) — ĐÃ CHẠY riêng (--path) vào DB local `hrm_erp_21_10_prod`. `ContractService::resolveTemplateFields` (BE tự chụp mẫu từ `hrm_print_templates`; cờ 0 ⇒ ép lời văn = bản chụp; đổi mẫu ⇒ chụp lại) + `logLegalFlagChange` (lịch sử `legal_edit_on/off`); Store/Update Request nhận `need_legal_approval`; `DetailContractResource` trả cờ + bản chụp + nhãn lịch sử; mới `ContractTemplateDiffService` (so CHỮ: bỏ thẻ, NFC, nbsp, theo từ, ngắt đoạn không tính; cắt đầu/cuối + Myers, trần 1000 bước) + `POST assign/contracts/template-diff`.
  - client: `_id/edit.vue` tab Mẫu in chỉ xem (`.hd-tpl-readonly`) + nút Sửa mẫu in (xác nhận) / nhãn Cần pháp chế duyệt / Xem thay đổi / Khôi phục mẫu gốc; `_id/index.vue` nhãn + Xem thay đổi; mới `components/ContractTemplateDiffModal.vue` (tô xanh/đỏ gạch, đếm chỗ, ↑↓ nhảy giữa các chỗ, tự cuộn chỗ đầu); `.print-tpl-view` chuyển sang `contract-form.scss` dùng chung.
  - Verify: tinker rollback 6 ca update (cờ 0 ép lời văn kể cả gửi "HACKED"; cờ 1 nhận lời văn; tắt cờ về bản chụp; admin sửa mẫu sau không ảnh hưởng; đổi mẫu chụp lại; bỏ mẫu ⇒ null) + lịch sử; diff HĐ 94 vs mẫu 65 = 0 chỗ (HTML khác do NFD/NFC), ca sửa 3 chỗ đúng; HTTP diff 200 / không token 401. Playwright 3060/8060 (chặn GET để HĐ 94 thành Đang tạo, chặn PUT): Huỷ giữ chỉ xem, Đồng ý ⇒ CKEditor sẵn sàng + nhãn + 2 nút, diff 0 → 1 chỗ (nền rgba(22,163,74,.15)), 3 chỗ nhảy 1/3→2/3→3/3 (scrollTop 0→1617→3251, chỗ chọn luôn trong khung), Khôi phục ⇒ cờ 0 + lời văn = bản chụp, PUT gửi cờ 1 không gửi template_original; màn Chi tiết cờ 1 có nhãn + nút, HĐ thật không có; `.print-tpl-view` giữ style (480px). Bắt + sửa trong lúc kiểm: popup thiếu đăng ký V2BaseModal; icon `ri-git-compare-line`/`ri-scales-3-line` không có trong Remix bundled ⇒ `ri-file-search-line`/`ri-scales-line`; viền chỗ chọn lòi dấu xuống dòng. phpunit `MeetingTargetSourceTest` 4/4.
  - E2E: thêm ca P24-M2 vào `HRM/e2e/tests/assign/contracts-form-layout.spec.ts` (CHƯA chạy).
  - Lưu ý: HĐ cũ (cờ 0, chưa có bản chụp) — lần lưu tới BE chụp mẫu hiện tại và ép lời văn về mẫu ⇒ lời văn từng sửa tay sẽ mất (chỉ có HĐ test; prod chưa có HĐ HRM).
  - Deploy thêm migration `2026_11_02_000001`.
- [x] 24.3 (03/11, user cho phép "Làm: commit rồi merge") — commit Phase 24.1+24.2: api `c49064aef`, client `1ec5ab23e`; MERGE gop_db LOCAL (đã có rbac GĐ3b) vào `gop_db-hop-dong-ban`: api `1d46e711d`, client `132ab5d8d`. CHƯA push — nhánh HĐ giờ mang rbac ⇒ hook `block_rbac_push` chặn push nhánh này; HĐ lên prod cùng đợt go-live rbac.
  - Gỡ xung đột api: `scopedContractQuery` ⇒ `PresaleViewScope::applyWithColumn(…, 'sale.hop_dong_du_an_tkt.view', …)` + giữ lọc Đang tạo (Q1) + hàm ẩn giá/quyền xem 1 HĐ; tên → mã: "Xem hợp đồng ẩn giá" → `sale.hop_dong_an_gia.view`, "Duyệt hợp đồng" → `sale.hop_dong_du_an_tkt.approve`; ContractService giữ mẫu in/cờ Pháp chế + #11932 chức danh người ký; `PermissionsTableSeeder` nhận bản xoá (đổi tên 4 quyền Phase 18 bỏ — tên hiển thị theo Catalog `sale.php`: "Xem danh sách hợp đồng dự án TKT", feature "Hợp đồng (dự án TKT)").
  - Gỡ xung đột client (gop_db sửa bố cục CŨ): giữ bố cục tab; danh sách `permissionScope('sale.hop_dong_du_an_tkt.view')`; Chi tiết Duyệt theo mã + giữ ẩn khi hide_price, nhãn "Chức danh người ký"; màn Sửa #11932 ô "Chức vụ người ký" → droplist "Chức danh người ký" (`company_signer_title_id`, BE required|exists:titles).
  - Quét: dòng nhánh HĐ thêm so với gop_db không còn kiểm quyền bằng tên (api + client).
  - CHƯA kiểm chạy thật: DB worktree `hrm_erp_21_10_prod` chưa có schema rbac ⇒ mọi API 500 (`allowed_scopes`/`permission_aliases`). `route:list` hỏng do `RiceController` thiếu — có sẵn ở gop_db chính, không do merge.
  - Rehearsal `hrm_erp_rbac_rehearsal` còn 21 migration pending, trong đó của HĐ: `2026_10_23_000001`, `2026_10_27_000001` (index), `2026_10_28_000001` (cột mẫu in), `2026_11_02_000001` (cờ pháp chế), #11932: `2026_10_30_000001/000002(backfill UPDATE)/000003`.
  - E2E cần sửa theo rbac: `contracts-list.api`, `contracts-export-request.api`, `contracts-hide-price.api` cấp quyền bằng tên + `role_has_permissions.company_id` (schema cũ) ⇒ hỏng trên DB đã convert.
- [ ] Đang hỏi user (sau bước 1, theo từng trạng thái): Còn hỏi tiếp: điều kiện chuyển BGĐ, vai trò Pháp chế, nghiệp vụ nào kích hoạt Đang thực hiện, thứ tự làm (đề xuất: đợt 1 = 7 trạng thái 🟢 + Không duyệt; đợt sau 🟡; 🔴 tách feature Gia hạn / Quyết toán).

- [x] 24.4 Bước 2 — Luồng duyệt tới Có hiệu lực (03/11, user "làm + cho phép chạy migrate"; DB kiểm `hrm_erp_rbac_rehearsal`) — thiết kế `design-phase24-trang-thai.md` mục "Chốt bước 2":
  - [x] a. Chạy lẻ (--path) 7 migration HĐ pending vào rehearsal: 2026_10_23_000001, 2026_10_27_000001, 2026_10_28_000001, 2026_10_30_000001/000002/000003, 2026_11_02_000001
  - [x] b. Migration mới `2026_11_03_000001_add_approval_flow_to_hrm_contracts_table` (legal_approver_id/at, bgd_approver_id/at, signed_file_name/path, customer_signed_at) — đã chạy vào rehearsal (CHƯA chạy `hrm_erp_21_10_prod`)
  - [x] c. Catalog `sale.php`: đổi tên TP approve, thêm `sale.hop_dong_du_an_tkt_phap_che.approve`, `sale.hop_dong_du_an_tkt_ban_giam_doc.approve`; `sale.hop_dong_vuot_han_muc.approve` platforms → ['erp']; ghi ĐÚNG 4 mã vào bảng permissions rehearsal (script chọn lọc — `permission:catalog-sync` đầy đủ sẽ kéo thêm 21 mã + 864 sửa không thuộc HĐ): đổi tên id 1141, thêm 101253 Pháp chế + 101254 BGĐ, vượt hạn mức on_hrm 1→0
  - [x] d. BE ContractService: submit (người lập, từ 3/13), approve theo bước (TP → 14/15-chặn/16; Pháp chế → 15-chặn/16; BGĐ → 16), transferToBgd, reject → 13, confirmSigned → 17 + tryActivate → 6; ĐK BGĐ ①②③
  - [x] e. BE Controller (approve/transfer-bgd/bgd-approvers/reject/customer-signed, gỡ checkPermission 1 mã ở route) + DetailContractResource (approval_step, is_can_*, bgd_reasons, is_bgd_required…) + ContractResource is_can_approve theo bước + HTHT preview trả bgd_reasons + lệnh `assign:activate-signed-contracts` 00:20 hằng ngày; Không duyệt sửa được như Đang tạo (isEditableStatus 3|13)
  - [x] f. FE: chi tiết HĐ + màn HTHT — nút theo bước, popup Chuyển duyệt (chọn người BGĐ), popup Xác nhận KH đã ký (file + ngày)
  - [ ] g. Verify tinker + API + Playwright (rehearsal); sửa/thêm spec e2e (không chạy)
    - [x] tinker rollback 48/48 ca (gửi duyệt người lập/403 · TP phòng quản lý/không quản lý · cờ Pháp chế · ĐK ① chặn + chuyển + chỉ người được chọn duyệt · ① + Pháp chế chặn ở bước Pháp chế · Không duyệt → 13 → sửa + gửi lại · quyền BGĐ duyệt thẳng · ② quy chế / ③ dưới giá net từ HTHT lưu + preview · cờ Resource · xác nhận ký: ĐK ngày ký → 6 luôn, ĐK cọc → 17, bảo lãnh tương lai → 17 rồi lệnh lịch → 6)
    - [x] sửa test `tests/Feature/Rbac/RoleNameCodesHrmTest.php` F10 theo assertNoBgdNeeded + mã BGĐ — CHƯA chạy được: `GateFixture` chèn `role_has_permissions.company_id` mà rehearsal đã bỏ cột (lỗi có sẵn của bộ test rbac)
    - [x] e2e mới `HRM/e2e/tests/assign/contracts-approval-flow.spec.ts` F1–F7 (CHƯA chạy)
    - [x] Playwright MCP 3060/8060 (rehearsal, tài khoản namdangit — NV50 bị Cài đặt phân hệ ẩn màn HĐ trên rehearsal; GET chi tiết HĐ 94 dựng từ Resource thật rồi vá cờ, mọi request ghi giả lập): bước TP = "Duyệt (Hỗ trợ hạch toán)" + "Không duyệt"; Pháp chế dính ĐK = dải vàng 2 lý do, ẩn Duyệt, Chuyển duyệt BGĐ → popup (2 lý do, footer trong màn) bấm khi trống ⇒ lỗi tại ô + 0 request, chọn "Giám Đốc B - BGD - GD002" + ghi chú ⇒ POST transfer-bgd {bgd_approver_id, note}, popup đóng; BGĐ = dải "Chờ Giám Đốc B (Ban giám đốc) duyệt" + Duyệt; Chờ KH ký = popup ngày mặc định hôm nay, gợi ý theo điều kiện hiệu lực, trống ⇒ 2 lỗi CÙNG LÚC + 0 request, đủ ⇒ POST multipart (ngày + file); Không duyệt = dải lý do + Sửa/Xoá/Trình duyệt; không quyền bước ⇒ không nút duyệt; đã ký ⇒ dải ngày ký + link file; HTHT: bình thường Không duyệt/Chuyển duyệt (phụ)/Duyệt, dính ĐK ⇒ ẩn Duyệt + Chuyển duyệt nổi bật, POST gửi kèm số HTHT. Gọi thật 6 route mới ⇒ 422 đúng câu, không 500.
    - Bắt + sửa trong lúc kiểm: `errors` trong data popup trùng computed `errors` của vee-validate (Vue warn) ⇒ đổi `fieldErrors`; `rows="3"` chuỗi ⇒ `:rows`; id người BGĐ select2 trả chuỗi ⇒ ép Number; dải cảnh báo HTHT nằm cuối trang (y 1000 > 773) ⇒ dời lên đầu (y 70); 2 confirm duyệt `msgBoxConfirm` ⇒ `$confirm` (CLAUDE.md).
  - [x] 24.4 XONG code + kiểm (03/11) — CHƯA commit. Còn mở: (1) migration `2026_11_03_000001` chưa chạy `hrm_erp_21_10_prod`; (2) thông báo cho người duyệt bước kế (chưa làm — cần skill notification-convention); (3) Pháp chế / BGĐ không có quyền xem danh sách thì chỉ mở được HĐ từ link (chưa có hộp "chờ tôi duyệt"); (4) chạy bộ e2e khi user yêu cầu.

- [x] 24.5 Thông báo luồng duyệt HĐ (03/11, user "làm" — chốt bảng + tiền tố `HDB`; CHƯA commit):
  - api mới `Modules/Assign/Services/ContractNotificationService.php` (khuôn PricingRequestService: `NotificationMeta::build` phân hệ Công việc + `EmployeeInfoService`), gọi từ `ContractService` qua `notify()` = `DB::afterCommit` (approve/transfer bước TP chạy trong transaction cùng ghi HTHT ⇒ rollback thì không báo).
  - Người nhận: Gửi duyệt → có quyền TP ∩ quản lý phòng của HĐ; TP duyệt có cờ Pháp chế → mọi người có quyền Pháp chế ở công ty HĐ; Chuyển duyệt → đúng người BGĐ được chọn; Đã duyệt (→ Chờ KH ký) / Không duyệt (kèm lý do) / Có hiệu lực (nhóm "Cập nhật") → người lập. Bỏ chính người thao tác. Link `/assign/contracts/{id}`.
  - Lệnh lịch (không đăng nhập): `sendToAllNotification` đọc `auth()->user()` ⇒ Notice → exception khi chạy artisan ⇒ nuốt thông báo; service tự gọi `sendNotification(..., $command = true)` (nhánh có sẵn), KHÔNG sửa hàm dùng chung.
  - Verify tinker rehearsal (rollback, `Bus::fake` + `Queue::fake` + mock `Redis::publish` — local `QUEUE_CONNECTION=sync` sẽ bắn push thật): 13/13 (chưa commit chưa báo; tập người nhận TP = có quyền ∩ quản lý phòng 42 = 5 người, có T không có T2 quản lý phòng khác; Pháp chế 2 người; BGĐ đúng 1; người lập nhận Đã duyệt / Không duyệt + lý do / Có hiệu lực từ lệnh lịch; người lập tự xác nhận ký không tự báo mình; transaction lỗi ⇒ 0 thông báo) + chạy lại 48/48 ca luồng duyệt.

- [x] 24.6 Bước 3 — Luồng xuất hàng theo bộ trạng thái mới (03/11, user "làm"; thiết kế design-phase24 mục "Bước 3"; CHƯA commit):
  - `Contract::EXPORTABLE_STATUSES` = {6 Có hiệu lực, 19 Đang thực hiện} cho `can_export` (nút YCXH Danh sách/Chi tiết, `storeExportRequest`, `createFromContract`), picker `hrm-contracts`, Yêu cầu giao hàng (`DeliveryRequestService`).
  - `is_can_create_export_request` thêm `hasLinesLeftToRequest()` (SL HĐ − SL trên YCXH chưa huỷ, cha hoặc con) ⇒ ẩn nút khi đã yêu cầu đủ.
  - `ContractService::markInProgress()` 6 → 19 (idempotent, lịch sử `in_progress` + nhãn "Đang thực hiện"), gọi ở `WarehouseExportService::send()` (PXK Gửi) khi YCXH thuộc HĐ HRM; lệnh `assign:activate-signed-contracts` quét bù HĐ 6 có YCXH 20/21 ở 8/9/5 (PXK làm trên ERP).
  - Thu tiền `HRM_CONTRACT_SELECTABLE_STATUSES` = {17, 6, 19, 20, 21, 22, 12, 11, 10} (cũng dùng ở `BillAdjustDeptFastPickService`); QR {6, 19, 22, 12, 11}.
  - Verify tinker rehearsal rollback 20/20 (can_export 6 trạng thái; còn hàng 0/1/2 + huỷ; picker có 19 không có 17; PXK Gửi ⇒ 19 + lịch sử mã PXK, PXK lần 2 không lặp; PXK phiếu không gắn HĐ không đụng; quét bù đã xuất kho ⇒ 19, chờ duyệt giữ 6; danh sách thu tiền / QR) + chạy lại 48/48 luồng duyệt + 13/13 thông báo. FE không sửa (nút đọc cờ BE) ⇒ chưa mở Playwright lại.

- [x] 24.7 Hết hiệu lực (20) — chốt 05/11 (HHL-Q1..Q4, design-phase24 mục "Hết hiệu lực"); user "làm" 05/11; CHƯA commit — chỉ hrm-api, nhánh `gop_db-hop-dong-ban`:
  - [x] a. `ContractService::EXPIRABLE_STATUSES` {6, 19} + `expireIfOverdue()` (execution_end_date < hôm nay; lịch sử `expire` ghi chú "Quá thời hạn thực hiện (dd/mm/yyyy)"; `notify('expired')` afterCommit) · `DetailContractResource` nhãn `expire` ⇒ "Hết hiệu lực"
  - [x] b. `ContractNotificationService::expired()` → người lập: `[HDB] Cập nhật: <b>{mã}</b>. Hết hiệu lực — quá thời hạn thực hiện (dd/mm/yyyy)`, type `contract_expired`, link chi tiết
  - [x] c. Lệnh `assign:activate-signed-contracts` bước 3 SAU quét bù 19 (chunkById, --dry-run chỉ liệt kê); lịch 00:20 giữ nguyên
  - [x] d. Verify tinker rehearsal rollback 30/30 (fixture chép HĐ 94 từ hrm_erp_21_10_prod, FOREIGN_KEY_CHECKS=0 trong phiên; Notification/Bus fake + mock Redis; chạy callback afterCommit bằng `app('db.transactions')->commit()`): 6/19 quá hạn ⇒ 20 · kết thúc hôm nay / ngày mai / không có ngày giữ · 17/16/3/10 không đụng · idempotent · can_export + is_can_create_export_request false + createFromContract Chờ duyệt ⇒ 422 · nhãn Resource · lệnh dry-run / chạy thật / lần 2 = 0 · có PXK + quá hạn ⇒ lịch sử in_progress rồi expire · chưa commit chưa báo, sau commit 5 thông báo đúng tiêu đề + link · smoke activateIfEffective 17→6, markInProgress 6→19. Sau chạy: 0 HĐ / 0 YCXH / 0 lịch sử rác. Script: scratchpad phiên 05/11 `hhl_verify.php`.
    - ⚠️ KHÔNG chạy lại được bộ 48/13/20 ca cũ (script ở scratchpad đã bị dọn) — chỉ smoke 2 hàm luồng cũ.
  - [x] e. E2E F8 thêm vào `HRM/e2e/tests/assign/contracts-approval-flow.spec.ts` (CHƯA chạy)
  - FE không sửa ⇒ không mở Playwright. Người thực hiện ở dòng lịch sử do lệnh lịch để trống (actor 0) — giống activate / in_progress từ lệnh lịch.

- [x] 24.8 Hủy duyệt + Đóng (18) ở Chờ KH ký — chốt 05/11 (HD-Q1..Q6); user "làm" 05/11; CHƯA commit — nhánh `gop_db-hop-dong-ban` (api 5 file, client 1 file, không migration):
  - [x] a. BE `ContractService`: `lastApproverId` (BGĐ đã duyệt › Pháp chế đã duyệt › TP), `approverIdsOfRound`, `canCancelApprove`, `canClose` (người lập · `manageDepartmentIdsOf` phòng HĐ · người duyệt cuối), `cancelApprove` (16 → 13, rejected_reason, xoá bgd_approver_id, lịch sử `cancel_approve`), `close` (16 → 18, lịch sử `close`); Controller `cancelApprove` / `close` (`reason` required|string|max:255, 403 qua flowError); route `POST {id}/cancel-approve`, `POST {id}/close` (không checkPermission — quyền theo dữ liệu)
  - [x] b. `DetailContractResource`: `is_can_cancel_approve`, `is_can_close`, `rejected_by_cancel`, `closed_reason` (lịch sử mới nhất — relation đã nạp, không query thêm) + nhãn "Hủy duyệt" / "Đóng hợp đồng"; `ContractNotificationService::approvalCancelled` (nhóm "Không duyệt") / `closed` (nhóm "Cập nhật") → người lập + người đã duyệt trong lượt (chụp TRƯỚC khi chuyển), bỏ người thao tác
  - [x] c. FE `_id/index.vue`: nút "Hủy duyệt" / "Đóng hợp đồng" (danger, `ri-close-circle-line` / `ri-forbid-line`); popup Không duyệt cũ thành popup lý do 3 chế độ (`REASON_MODES`: tiêu đề / nhãn / nút / url / khoá payload; reject giữ `rejected_reason` + câu lỗi cũ); dải "Hủy duyệt: …" (13 do hủy) và dải xám `.note-muted` "Đã đóng: …" (18); 403 không bắn toast thứ 2 (interceptor đã bắn)
  - [x] d. Verify: tinker rehearsal rollback 50/50 (bước cuối 4 ca · ai hủy được 10 ca · ai đóng được 7 ca · hủy/đóng thực thi + lịch sử + Resource · controller 422/200/403 · thông báo đúng người, bỏ người thao tác, tiêu đề, 403 không báo) + chạy lại Hết hiệu lực 30/30. Playwright (Chrome hệ thống, 3060/8060 rehearsal, NV13, GET chi tiết dựng từ Resource thật của HĐ fixture rồi vá cờ, mọi request ghi giả lập) 25/25: 2 nút danger rgb(220,38,38), glyph `ri-forbid-line` rộng 15px font remixicon; popup tiêu đề/nhãn/nút theo chế độ; trống ⇒ "Bắt buộc phải nhập" + 0 request; POST cancel-approve/close {reason} đã trim; dải "Hủy duyệt: …" / "Đã đóng: …" nền rgb(243,244,246); không cờ ⇒ không nút; Không duyệt cũ giữ payload + câu lỗi; 403 ⇒ lỗi dưới ô + đúng 1 toast. Script: scratchpad phiên 05/11 `hd_close_verify.php`, `pw_close.cjs`.
    - Bắt + sửa trong lúc kiểm: 403 ra 2 toast trùng (catch của popup + interceptor) ⇒ bỏ toast ở catch khi 403.
  - [x] e. E2E F9/F10 thêm vào `contracts-approval-flow.spec.ts` (`--list` đọc được 12 ca; CHƯA chạy)
  - Ghi nhận ngoài luồng (chưa sửa): thanh nút `.contract-actionbar__btns` dùng `gap: 6px` cho MỌI nút (CLAUDE.md chuẩn 12px) — có từ trước; popup lý do là `b-modal` cũ (chưa lên `V2BaseModal`). Cache trình duyệt Playwright (`~/Library/Caches/ms-playwright`) đã bị dọn ⇒ bộ e2e cần `npx playwright install chromium` trước khi chạy.

- [x] 24.9 Đang thực hiện từ thu tiền / mượn bán — chốt 05/11 (DTH-Q1..Q3); user "làm" 05/11; CHƯA commit — chỉ hrm-api (2 file, không migration, không đụng Finance):
  - [x] a. `ContractService::IN_PROGRESS_LEDGER_TYPES` (BillIncome · BillIncomeReport · BillAdjustDept · BorrowSell ⇒ nhãn phiếu thu / báo có / điều chỉnh công nợ / mượn bán) + `firstLedgerSinceEffective()` (account_details gắn HĐ, created_at > lịch sử vào 6 mới nhất; không có lịch sử ⇒ invoiceable_date_accounting > effective_date). Lệnh `assign:activate-signed-contracts`: sau bước PXK, lọc HĐ 6 bằng whereExists (index contractable) ⇒ `markInProgress` ghi chú "Đã hạch toán <loại> <mã>"; TRƯỚC bước Hết hiệu lực
  - [x] b. Verify tinker rehearsal rollback 25/25: 4 loại chứng từ ⇒ 19 · cọc trước hiệu lực / phiếu chi / UNC / không chứng từ giữ 6 · 16, 17 không bị đẩy sang 19 · HĐ không lịch sử theo ngày hạch toán (đúng ngày hiệu lực không tính) · cọc trước + báo có sau ⇒ ghi chú mã báo có · thu tiền + quá hạn ⇒ lịch sử activate → in_progress → expire · dry-run không ghi · lần 2 không lặp. Chạy lại Hết hiệu lực 30/30 + Hủy duyệt/Đóng 50/50. Lệnh dry-run thật trên rehearsal 0,4s. Script: scratchpad phiên 05/11 `dth_verify.php`.
  - Còn: hạch toán DV / CP cho HĐ HRM chưa có (feature riêng) — có rồi thì thêm loại vào `IN_PROGRESS_LEDGER_TYPES`.

- [x] 24.10 Sửa e2e HĐ theo rbac + chạy bộ HĐ trên rehearsal (05/11, user "làm 2"; e2e ngoài git):
  - [x] `HRM/e2e/utils/rbacRole.ts` MỚI (vai trò tạm schema rbac: roles.company_id + base_name, employee_has_roles model App\Employee, role_has_permissions.scope, cấp theo `permissions.code`, `preExistingGrants` chặn tài khoản có sẵn mã)
  - [x] `contracts-list.api` (4 tên → mã xem + phạm vi 1–4), `contracts-hide-price.api` (mã ẩn giá / xem / TP duyệt; P21-V1 viết lại theo luật Phase 24: mã TP + quản lý phòng HĐ; ca in hợp đồng của mình dời trước skip), `contracts-export-request.api` (mã xem phạm vi 4; chạy bằng namdangit vì X5 cần màn HĐ — NV thường bị Cài đặt phân hệ chặn)
  - [x] User chọn 05/11: spec phân quyền chạy bằng NV24 (JWT qua E2E_RBAC_TOKEN) — namdangit có sẵn phạm vi 4
  - [x] `contracts-approval-flow`: F2+F3 / F5 tìm component qua cây $nuxt.$root (b-modal portal); F5 đếm `.v2-error__text` (`.v2-error` nằm cả trên khung ô lẫn gốc V2BaseError)
  - [x] Chạy (Chrome hệ thống qua config tạm scratchpad, video/trace tắt — cache ms-playwright + ffmpeg đã bị dọn; dữ liệu tạm: HĐ E2E-RUN-HD94 chép HĐ 94 + báo giá 339 tạm created_by 13): list 6/6 · hide-price 5/6 (H2 skip: chưa có mẫu in loại 7) · export-request 5/5 · approval-flow 9/9 · detail-layout 7/7 · export-request-layout 7/7 · filter 6/6 · form-layout 2/12 (L3+ chặn: thiếu bảng quotation_promotions ⇒ API báo giá lỗi SQL)
  - [x] User cho phép 05/11: chạy lẻ migration `2026_10_26_000002_create_quotation_promotions_table` (--path) + seeder `SaleContractPrintTemplatesSeeder` (26 mẫu loại 7) vào `hrm_erp_rbac_rehearsal` — 13 migration pending khác KHÔNG chạy
  - [x] `contracts-form-layout` sửa spec: (a) `openCreate` cho qua `POST assign/contracts/template-diff` (POST chỉ đọc, bị route.abort ⇒ popup "Xem thay đổi" báo mất mạng); (b) M2 điền đủ ô Lưu nháp vẫn bắt (Số HĐ, Bên A, người đại diện, lắp đặt, đợt TT) trước khi Lưu nháp; (c) N1 bỏ ô Tài khoản ngân hàng khỏi nhận diện select NV (id TK trùng id NV) + gán phòng thực hiện có NV trong store
  - [x] Chạy lại: hide-price 6/6 · form-layout 12/12 ⇒ cả bộ HĐ xanh (list 6 · hide-price 6 · export-request 5 · approval-flow 9 · detail-layout 7 · export-request-layout 7 · filter 6 · form-layout 12 = 58/58)
  - [x] Dọn: HĐ #312 E2E-RUN-HD94 xoá, báo giá 339 trả created_by 428, vai trò tạm spec đã gỡ, tắt server 8060/3060
- [x] 24.11 Sửa nhãn "NV #<id>" ở Phòng thực hiện màn Lập HĐ (05/11, user "làm"): nguyên nhân — NV phòng CTV (cooperation_type 2) bị lọc khỏi state.employees ở phân hệ Assign, prefill người lập chỉ có employee_id ⇒ fallback `'NV #' + id` (ContractImplementSection.vue:158). Sửa `pages/assign/contracts/_id/edit.vue` (prefill tạo mới): kèm `employee_name` = employeeOptionText(current_employee_info). Kiểm: DOM "NV #13" → "DNS Admin - DNS01" (phòng CTV không có trong store.departments nên nhãn thiếu mã phòng — đúng luật bỏ phần thiếu); e2e P21-N1 thêm khẳng định nhãn người lập; form-layout 12/12. BE tự dựng employee_name khi lưu ⇒ trường FE gửi thừa bị bỏ qua.

- [x] 24.12 Merge gop_db mới nhất vào worktree (05/11, user cho phép; mục đích: HĐ HRM thay FirmContract ⇒ dùng chung YCHTDV/Phiếu HTDV-HĐBH đã port trên gop_db). Merge gop_db local (dùng lại cách gỡ 04/11 + Catalog aac684f92) rồi origin/gop_db: api `488074abb`, client `5f0e3005e`. Gỡ: PermissionsTableSeeder giữ đã xoá; DeliveryContractService::searchSuppliers lấy origin. Thay đổi chưa commit của HĐ (24.7–24.11) giữ nguyên (đối chiếu patch trước/sau).
- [x] 24.13 Vá chỗ gop_db chưa theo rbac (user "làm 1" + "làm luôn 2", CHƯA commit):
  - (1) 11 file Finance/Transport gọi `currentEmployeeIsSuperAdmin()` (rbac đã gỡ ⇒ 500): bỏ nhánh Super admin, chỉ giữ kiểm quyền; xoá 2 hàm `isSuperAdmin()` không ai gọi (ServiceAccounting, WrAccountingService). Kiểm: 6 endpoint finance 200 (trước 500); RawPermissionLookupGuardTest không còn vi phạm ở Finance/Transport.
  - (2) Catalog khai 17 tên api mới vào mã có sẵn (theo mã ERP thật đang gate): HĐ bán đầu kỳ → sale.hop_dong_ban_dau_ky.view; Phiếu HTDV-HĐBH xem → customer_care.hach_toan_dich_vu.view; "Hạch toán dịch vụ HĐBH" → accounting.hach_toan_yeu_cau_lam_dich_vu.create; QT thưởng NS quý → accounting.quyet_toan_hoa_hong_quy.create/.view; QT thưởng năm → customer_care.quyet_toan_nam.create/.view + quyet_toan_nam_ban_giam_doc.approve; + platforms hrm. catalog-sync --dry-run exit 0 (CHƯA ghi DB).
  - (3) (user "làm") CSKH: 6 file (WaitingAssignTaskService, WrAssignTaskService, WrImportResultService, WrAssignTaskSourceService, HandoverAcceptanceRecordService, HandoverAcceptanceRecordStoreService) bỏ cờ `super_admin` + lời gọi `WarrantyRepairPermission::isSuperAdmin()` (rbac đã xoá); WrImportResultNotifier đổi người nhận từ spatie `PermissionEmployee::permission` sang `PermissionLookup::infoIdsOf(holders(name, companyId))`. Kiểm: tests/Unit/Rbac 13/13 OK; API CSKH (wr-assign-tasks, wr-import-results, handover-acceptance-records, waiting-assign-tasks 5 tab) 200; holders 2 quyền chạy không lỗi.
  - Còn: route Finance còn gate bằng tên (permission:scan legacy 23); Catalog mới chưa catalog-sync vào DB.

## Phase 25 — Hạch toán dịch vụ / chi phí / vận chuyển cho HĐ HRM (XONG 06/11 — 25.1–25.9 + review cuối sửa I1–I3; đã commit, CHƯA push)

> **For agentic workers:** dùng superpowers:executing-plans (hoặc subagent-driven-development) chạy từng task; checkbox `- [ ]`.

**Goal:** HĐ bán HRM tạo được yêu cầu hạch toán Dịch vụ / Chi phí / Vận chuyển và ghi sổ qua 2 màn HĐBH có sẵn (YCHTDV / Phiếu HTDV), ERP bỏ qua phiếu của HĐ HRM.
**Architecture:** 2 màn HĐBH rẽ nhánh theo `contractable_type`; mọi logic riêng HĐ HRM gom vào 1 class nguồn `HrmContractServiceAccountingSource`; engine ghi sổ dùng chung, chỉ thêm nhánh lấy % VAT + loại HTHT; giá vốn D7 quy về `coefficient_cost_price` lúc chụp dòng nên công thức 632 của engine giữ nguyên.
**Tech Stack:** Laravel 8 (hrm-api, nwidart Modules), Nuxt 2 / Vue 2 (hrm-client), Laravel ERP `TanPhatDev`, PHPUnit, Playwright.
**Spec:** `design-phase25-hach-toan-dich-vu.md` (D1–D7, C1–C4).

### Global Constraints
- Đụng source mỗi repo phải được user "làm" riêng (hrm-api · hrm-client · ERP); migration hỏi riêng, chạy lẻ `--path` vào `hrm_erp_rbac_rehearsal`.
- KHÔNG commit / push trừ khi user ra lệnh (nhánh mang rbac, hook chặn push) — mỗi task kết thúc ở "để nguyên chưa commit".
- Nhánh HĐ hãng KHÔNG đổi hành vi: mọi nhánh mới rẽ theo `contractable_type`; test HĐ hãng có sẵn phải xanh.
- `contractable_type` HĐ HRM = `Modules\Assign\Entities\Contract\Contract` (= `AccountDetail::CONTRACTABLE_HRM_CONTRACT`), KHÔNG map sang chuỗi ERP.
- Phân loại: `costs.revenue_calculation === 0` ⇒ Chi phí; 1 / NULL / không `cost_id` ⇒ Dịch vụ (C2).
- Trạng thái HĐ được tạo yêu cầu: `Contract::EXPORTABLE_STATUSES` (6, 19) + người lập = người đăng nhập + có `support_accounting` (D5).
- Giá vốn dòng HĐ HRM = `estimated_price × qty` (D7); vận chuyển không giá vốn.
- PHPUnit chạy với `DB_DATABASE=hrm_erp_rbac_rehearsal` (+ `_SECOND`, `_TPE`), `DatabaseTransactions`.
- FE: V2Base*, `button-convention`, nút không dùng được thì ẨN; Playwright đo DOM; e2e `--workers=1`, tài khoản namdangit.

### Review Focus
1. Kế toán **Không duyệt** rồi người lập gửi lại cùng dòng — cờ phải gỡ đúng và gửi lại được (test ở 25.3).
2. Id `hrm_contract_service_items` trùng id `firm_contract_costs` — tra nguồn phải theo cặp (type, id), không lẫn HĐ hãng (test ở 25.3).
3. HĐ HRM không có dòng Chi phí / không có phí vận chuyển — nút tương ứng ẩn, API trả lỗi rõ (test ở 25.2, 25.6).
4. HĐ chuyển trạng thái (Hết hiệu lực) khi yêu cầu đang Chờ duyệt — kế toán vẫn lập phiếu được (gate chỉ ở lúc TẠO; test ở 25.4).
5. Danh sách / dashboard ERP không còn thấy phiếu HĐ HRM nhưng phiếu HĐ hãng vẫn đủ (test ở 25.8).

---

### Task 25.1: Migration cờ + Contract model (hrm-api)
**Files:** Create `database/migrations/2026_11_06_000001_add_service_accounting_flags_to_hrm_contracts.php` · Modify `Modules/Assign/Entities/Contract/ContractServiceItem.php` (`$casts['exported'=>'boolean']`, fillable), `Modules/Assign/Entities/Contract/Contract.php` (`$casts['shipping_exported'=>'boolean']`).
**Produces:** cột `hrm_contract_service_items.exported` bool default false (after `note`), `hrm_contracts.shipping_exported` bool default false (after `shipping_discount`); `down()` drop 2 cột.
- [x] Hỏi user cho chạy đúng migration này (`migrate --pretend` kèm) ⇒ `php artisan migrate --path=database/migrations/2026_11_06_000001_add_service_accounting_flags_to_hrm_contracts.php --force` trên rehearsal.
- [x] Kiểm: `Schema::hasColumn` 2 cột = true; `migrate:status` bản này "Yes".

### Task 25.2: HTHT tách Chi phí (D4)
**Files:** Modify `Modules/Assign/Services/ContractSupportAccountingService.php:58-71` · Test `Modules/Assign/Tests/Feature/ContractSupportAccountingSplitCostTest.php`.
**Produces:** `getAccountingInfo` — dòng service item có `cost.revenue_calculation === 0` cộng vào nhóm `other` (⇒ `*_other_cost`), còn lại `repair`.
- [x] Test `test_cost_items_go_to_other_cost_group`: HĐ 1 dòng DV (quoted 1,000,000 × 2) + 1 dòng CP (500,000 × 1) ⇒ `before_vat_repair_service == 2000000`, `before_vat_other_cost == 500000`, `before_vat_total` không đổi so với trước.
- [x] Test `test_null_revenue_calculation_counts_as_service` (cost NULL / không cost_id ⇒ repair).
- [x] Chạy FAIL ⇒ sửa (tách vòng `$repair` theo `isCostItem`, tra `costs.revenue_calculation` 1 query `whereIn`) ⇒ PASS.
- [x] grep nơi đọc `*_repair_service` / `*_other_cost` của HĐ HRM (`ProductExportPostingService::prepareData`, màn HTHT FE, `ContractPrintService`) — ghi vào plan nơi nào đổi số.

### Task 25.3: Nguồn dòng HĐ HRM + cờ (core)
**Files:** Create `Modules/Finance/Services/ServiceAccounting/HrmContractServiceAccountingSource.php` · Test `Modules/Finance/Tests/Feature/HrmContractServiceAccountingSourceTest.php`.
**Produces:**
- `const CONTRACT_TYPE = Contract::class;`
- `assertCanRequest(Contract $c, int $type): void` — ném `\Exception` câu: "Hợp đồng không có hỗ trợ hạch toán" · "Không thể chọn hợp đồng này" (sai trạng thái / không phải người lập) · "Không thể yêu cầu hạch toán chi phí vận chuyển cho hợp đồng này" (đã `shipping_exported` hoặc `shipping_cost` = 0 và `shipping_discount` = 0).
- `buildCosts(Contract $c, int $type, bool $forEdit = false): array` — dòng chuẩn hoá cùng khoá `ServiceAccountingRequestService::normalizeCostRow` + `contract_costable_type`. Type 1/2: service items theo C2; `price = quoted_price × qty`, `value_discount` = giảm giá dòng theo đúng công thức `$disc` của 25.2 (method 1/2), `value_extra = 0`, `total_price = price − value_discount`, `vat_percent` = của dòng, `exported` = cờ dòng, `coefficient_cost_price = price > 0 ? round(estimated_price × qty / price × 100, 6) : 0` (D7 quy đổi). Type 3: 1 dòng ảo `name = 'Chi phí vận chuyển'`, `contract_costable_type = Contract::class`, `contract_costable_id = $c->id`, `price = shipping_cost`, `value_discount = shipping_discount`, `vat_percent = shipping_vat_percent`, `coefficient_cost_price = 0`, `cost_id` = id Cost 'Chi phí vận chuyển' (orderBy id, không tạo mới), `exported = shipping_exported`.
- `findSource(string $type, int $id): ?Model` (ContractServiceItem | Contract) · `isExported(Model $src): bool` · `setExported(Model $src, bool $on): void` (ServiceItem ⇒ `exported`; Contract ⇒ `shipping_exported`).
- `pickerQuery(Request $r): Builder` — HĐ HRM `whereIn status EXPORTABLE_STATUSES`, `created_by = auth()->id()`, `whereHas support_accounting`, lọc `q`/`code`/`customer`.
- [x] Test: type 1 chỉ dòng DV, type 2 chỉ dòng CP; giá trị `price/value_discount/total_price/coefficient_cost_price` (dòng quoted 1,000,000 × 2, estimated 600,000 ⇒ coef 60); type 3 dòng ảo đúng số; gate 3 câu lỗi; `setExported` 2 loại nguồn; `findSource(Contract::class, id)` không trả FirmContractCost cùng id (Review Focus 2).
- [x] FAIL ⇒ code ⇒ PASS.

### Task 25.4: Yêu cầu hạch toán nhận HĐ HRM
**Files:** Modify `Modules/Finance/Services/ServiceAccountingRequestService.php` (`buildCostsFromContract`, `store`, `update`, `syncCosts`, `rollbackAccounting`, `contractData`, `findForShow`/`detailData`, `snapshotOf`), `Modules/Finance/Entities/ServiceAccountingRequest/ServiceAccountingRequest.php` (searchByFilter morphWith + hiển thị mã/KH/NVKD), `Http/Requests/ServiceAccountingRequest/ServiceAccountingRequestStoreRequest.php`, `Http/Controllers/V1/ServiceAccountingRequestController.php`, `Modules/Finance/Routes/api.php` · Test `Modules/Finance/Tests/Feature/ServiceAccountingRequestHrmContractTest.php`.
**Consumes:** 25.3. **Produces:**
- Payload store: `contract_type` ∈ `firm|hrm` (mặc định `firm`), `contract_id` (bắt buộc khi `hrm`; `firm` vẫn nhận `firm_contract_id` cũ); `costs[].contract_costable_type` (mặc định FirmContractCost).
- `GET finance/service-accounting-requests/hrm-contracts` (picker) · `GET .../contract-data/{contractId}?contract_type=hrm&type=` .
- `syncCosts`/`rollbackAccounting` tra nguồn qua `findSource`/`setExported` khi type HRM; rollback KHÔNG gọi `update()` trên morph Contract.
- [x] Test: tạo nháp HĐ HRM type 1 ⇒ `contractable_type = Contract::class`, cờ chưa bật; gửi duyệt ⇒ dòng `exported = 1`; Không duyệt ⇒ gỡ; gửi lại được (Review Focus 1); dòng đã cờ ⇒ 422 cả phiếu; type 3 bật/gỡ `shipping_exported`; HĐ HRM chuyển 20 sau khi gửi ⇒ `show` + Không duyệt vẫn chạy (Review Focus 4); HĐ hãng: chạy lại `ServiceAccountingReadApiTest` + checkpoint test xanh.
- [x] FAIL ⇒ code ⇒ PASS.

### Task 25.5: Phiếu hạch toán + ghi sổ HĐ HRM
**Files:** Modify `Modules/Finance/Services/ServiceAccountingService.php` (nhánh ghi sổ `:202-260`, `findForShow` morphWith, detail), `Modules/Finance/Entities/ServiceAccounting/ServiceAccounting.php` (`searchByFilter` nhận cả 2 type, `syncCosts` chỉ bật `accounted_delivery_cost` khi HĐ hãng), `Modules/Finance/Services/FirmContractServiceAccountingPostingService.php` (`prepareData` % VAT HĐ HRM: type 1/2 = `vat_percent` dòng service item đầu tiên đúng loại, type 3 = `shipping_vat_percent`; `loadRichSupportAccounting` theo `contractable_type` của phiếu) · Test `Modules/Finance/Tests/Feature/HrmContractServiceAccountingPostingTest.php`.
**Produces:** `account_details` của phiếu HĐ HRM: `invoiceable_type = ServiceAccounting::INVOICEABLE_TYPE`, `contractable_type = AccountDetail::CONTRACTABLE_HRM_CONTRACT`, `contractable_code` = mã HĐ, tổ chức theo cột `company_id/department_id/part_id` của HĐ; không nhánh PLBS.
- [x] Test type 1 (dòng DV quoted 1,000,000 × 2, giảm 200,000, VAT 8%, estimated 600,000 ⇒ coef 60): doanh thu Nợ 1311 2,160,000 / Có 5113 2,000,000 + Có 33311 160,000 · giảm trừ Nợ 5213 200,000 + Nợ 33311 16,000 / Có 1311 216,000 · giá vốn Nợ 632 1,200,000 / Có 1541 1,200,000 (= estimated × qty, D7) · cụm nặng có dòng Work 12/13/14/6 khi HTHT có phòng. Tổng Nợ = tổng Có từng `group`.
- [x] Test type 2: không cụm nặng; type 3: không 632, VAT = `shipping_vat_percent`.
- [x] Test meta: mọi dòng `contractable_type/id/code` = HĐ HRM, `company_id` = HĐ.
- [x] Chạy lại `FirmContractServiceAccountingPostingTest`, `ServiceAccountingPostingReconcileTest` xanh.
- [x] FAIL ⇒ code ⇒ PASS.

### Task 25.6: HĐ — Đang thực hiện + cờ nút
**Files:** Modify `Modules/Assign/Services/ContractService.php` (`IN_PROGRESS_LEDGER_TYPES` + `ServiceAccounting::INVOICEABLE_TYPE => 'dịch vụ'`), `Modules/Assign/Transformers/DetailContractResource.php` · Test `Modules/Assign/Tests/Feature/ContractServiceAccountingFlagsTest.php`.
**Produces:** resource `is_can_request_service_accounting`, `is_can_request_cost_accounting`, `is_can_request_shipping_accounting` (bool) = gate 25.3 + còn ≥1 dòng đúng loại chưa `exported` (type 3: `assertCanRequest` qua).
- [x] Test: HĐ 6 người lập có DV chưa cờ ⇒ cờ DV true, CP false khi không có dòng CP (Review Focus 3); người khác ⇒ false; HĐ 20 ⇒ false; phiếu HTDV ghi sổ sau hiệu lực ⇒ `assign:activate-signed-contracts` chuyển 19, ghi chú "Đã hạch toán dịch vụ <mã HTDV>" (nhãn trong `IN_PROGRESS_LEDGER_TYPES` = 'dịch vụ').
- [x] FAIL ⇒ code ⇒ PASS.

- Kết quả hrm-api (06/11): 5 file test mới xanh 23/23 (Split 2 · Source 8 · Request 7 · Posting 3 · Flags 3) + test HĐ hãng (Posting 7 · Reconcile 1 · Checkpoint 2) + Rbac 13 xanh. Ruling: thêm customer()/employeeCreate()/customer_mobile vào HĐ HRM để dùng chung code hiển thị; store HĐ HRM kiểm đủ cổng ở server. Có sẵn từ gop_db: 13 ca ServiceAccountingReadApiTest/WriteApiTest đỏ 403 vì cấp quyền qua employee_has_permissions (rbac bỏ) — không do Phase 25.

### Task 25.7: FE hrm-client
**Files:** Modify `pages/assign/contracts/_id/index.vue` (3 nút, khuôn `goToCreateExportRequest`), `pages/finance/service-accounting-requests/components/ServiceAccountingRequestForm.vue` + `FirmContractPickerModal.vue` (thêm lựa chọn loại HĐ / gộp danh sách 2 loại, cột "Loại HĐ"; prefill `?hrm_contract_id=&type=`), `pages/finance/service-accounting-requests/_id/*.vue` + `pages/finance/service-accounting/_id/*.vue` (link mã HĐ HRM ⇒ `/assign/contracts/{id}`), màn HTHT HĐ (dòng Chi phí khác) · Test e2e `HRM/e2e/tests/assign/contracts-service-accounting.spec.ts`.
- [x] Nút: "Yêu cầu hạch toán dịch vụ" / "Yêu cầu hạch toán chi phí" / "Yêu cầu hạch toán vận chuyển" — đặt tên/màu/icon theo `button-convention`, hiện theo 3 cờ 25.6.
- [x] Playwright (namdangit, rehearsal + HĐ tạm): đo số nút hiện đúng cờ; picker có HĐ HRM; tạo nháp từ HĐ HRM chặn ghi bằng route; chi tiết phiếu link đúng. Tái hiện trước khi sửa nơi nào là lỗi giao diện.
- [x] Spec e2e mới + chạy lại bộ e2e HĐ (`contracts-*`) xanh.

### Task 25.8: ERP bỏ qua phiếu HĐ HRM (D6/C4)
**Files:** Modify `ERP/TanPhatDev/app/Model/Sale/ServiceAccountingRequest.php:180` + `app/Model/Sale/ServiceAccounting.php:170` (`searchByFilter` + `getDataForExport` nguồn), `app/Http/Controllers/Sale/ServiceAccountingRequestController.php` (`show/edit/update/reject/delete/getDataForServiceAccounting`), `app/Http/Controllers/Sale/ServiceAccountingController.php` (`create/store/edit/update/show/delete`), `app/Http/Controllers/HomeController.php:1410-1418` (đếm chờ duyệt).
**Produces:** scope `scopeExcludeHrmContract($q)` trên 2 model: `where('contractable_type', '!=', 'Modules\Assign\Entities\Contract\Contract')`; controller gặp phiếu HĐ HRM ⇒ `abort(404)` / redirect kèm "Phiếu của hợp đồng HRM — xử lý trên HRM". Không đổi morphMap.
- [x] Hỏi user "làm" riêng cho repo ERP.
- [x] Kiểm (tinker ERP trên DB có 1 phiếu HĐ HRM + 1 phiếu HĐ hãng tạm): danh sách / đếm dashboard chỉ còn phiếu HĐ hãng (Review Focus 5); mở phiếu HĐ HRM ⇒ chặn; dọn dữ liệu tạm.

- Kết quả FE + ERP (06/11): Playwright 15/15 (3 nút đo DOM, form điền sẵn, payload hrm, ô chọn HĐ) + menu dòng danh sách; e2e mới contracts-service-accounting 4/4; cả bộ HĐ UI 45/45, api 12/12 + 5/5. ERP: tinker rehearsal (rollback) — danh sách / đếm / tải theo id bỏ phiếu HĐ HRM, HĐ hãng giữ. Ruling: không thêm link mã HĐ ở chi tiết YC/phiếu; thêm 3 hành động ở menu dòng danh sách HĐ; ô chọn HĐ có select "Loại hợp đồng" mặc định HĐ bán HRM.
- Review cuối (opus, 06/11): 0 Critical · sửa 3 Important (I1 giá vốn chụp tuyệt đối cost_price; I2 lọc phiếu theo HĐ HRM; I3 báo "không còn dịch vụ / chi phí cần yêu cầu hạch toán") — mỗi lỗi có test RED→GREEN. Minor để sau: M1 kiểm loại dòng khớp type YC · M2 ~4 query/HĐ ở danh sách · M3 VAT theo dòng đầu (như ERP) · M4 câu lỗi "dịch vụ sửa chữa" · M5 khoá dòng khi gửi đồng thời · M6 ghi chú Đang thực hiện luôn "dịch vụ". Ngoài luồng: form YC nút "Chọn hợp đồng" thiếu icon + xuống dòng; phiếu nháp giữ id dòng YC cũ sau gửi lại (gop_db); 13 test Read/WriteApi đỏ 403 (cấp quyền kiểu cũ).

### Task 25.9: Tổng kiểm + tài liệu
- [x] Chạy toàn bộ test Finance ServiceAccounting* + test mới 25.2–25.6 trên rehearsal; `tests/Unit/Rbac` xanh.
- [x] Luồng thật trên rehearsal (HĐ tạm): YC 3 loại → kế toán Không duyệt 1 phiếu → gửi lại → lập Phiếu "Lưu và duyệt" → đối chiếu `account_details` → chạy lệnh 00:20 ⇒ HĐ 19; dọn dữ liệu tạm.
- [x] Cập nhật design (mục đã làm), checkpoint plan; ghi lệch `QuotationExcelExport` (C2) vào danh sách sửa sau.
Thiết kế: `design-phase25-hach-toan-dich-vu.md` (D1–D7 + quyết định của Claude C1–C4). Dùng chung 2 màn YCHTDV / Phiếu HTDV-HĐBH (gop_db, nguyentrancu97) — mở rộng cho HĐ HRM; ERP lọc bỏ phiếu của HĐ HRM.
- Kết quả 25.9 (06/11): permission:catalog-sync THẬT vào rehearsal (user cho phép: thêm 20 · sửa 869 · ngừng 0). Luồng thật qua API bằng namdangit 13/13: YC DV gửi duyệt (cờ bật) → Không duyệt (gỡ) → gửi lại → phiếu "Lưu và duyệt" ⇒ sổ 1311 9,180,000 / 5113 8,500,000 / 33311 680,000 / 632-1541 85,000 (= giá vốn HĐ) gắn HĐ HRM #530 cty 1 → YC Đã hạch toán → lọc danh sách theo mã HĐ → YC vận chuyển, chặn tạo tiếp → lệnh 00:20 ⇒ HĐ 19 "Đã hạch toán dịch vụ TPE.HTDV.02754". Đã dọn sạch (YC, phiếu, sổ, lịch sử, 86 thông báo thử, HĐ tạm).
- Commit (06/11, user "làm cả 2"; CHƯA push — nhánh mang rbac):
  - hrm-api `gop_db-hop-dong-ban`: d674aca4a (24.7–24.9) · 881fe0b7b (rbac 24.13) · 987fff916 (Phase 25)
  - hrm-client `gop_db-hop-dong-ban`: a600fd582 (24.8 FE) · a5cf4fdce (24.11) · 50ca18435 (Phase 25 FE)
  - ERP `gop_db` local: 8e3f46c42c (bỏ qua phiếu HĐ HRM) — gop_db local đang hơn origin 27 commit
  - Không vào git: HRM/e2e (spec mới contracts-service-accounting + 3 spec sửa theo rbac), .plans
  - 06/11: + hrm-api 7318e1714 (25.10 lỗi nhỏ). PUSH (user "làm 1 + 2"): hrm-api → origin/gop_db-hop-dong-ban 7318e1714 · hrm-client → 50ca18435. ERP: user chọn CHƯA push (gop_db local mang 26 commit rbac chưa push + 8e3f46c42c).

### Checkpoint — 2026-10-30
Vừa hoàn thành: mở app worktree cho user (Playwright + Chrome của user, đăng nhập NV50 bằng JWT ghi localStorage 127.0.0.1:3060); khảo sát 15 trạng thái HĐ mới — bảng mức độ sẵn sàng ở Phase 24.
Đang làm dở: brainstorm Phase 24 — chờ user trả lời câu hỏi về trạng thái Thanh lý.
Bước tiếp theo: hỏi tiếp lần lượt các câu tồn (BGĐ / Pháp chế / Đang thực hiện / thứ tự đợt) → viết design-phase24-trang-thai.md → xin phép code. Nhánh `gop_db-hop-dong-ban` đã push hết (api `29fae59d7`, client `1057d2f92`), 0 file chưa commit.
Blocked:


### Checkpoint — 2026-11-03 (wrap up)
Vừa hoàn thành: Phase 24 bước 2 (luồng duyệt + thông báo, 24.4–24.5) + bước 3 (xuất hàng, 24.6); commit CHƯA push: api `f1dabaaea`, client `1f43b7405`.
Đang làm dở: không.
Bước tiếp theo: hỏi user làm Hết hiệu lực (lệnh lịch quá ngày kết thúc thực hiện) hay mục còn mở khác (hộp chờ tôi duyệt, Hủy duyệt, mốc Đang thực hiện cho thu tiền/DV/CP). Push chỉ khi user ra lệnh (nhánh mang rbac).
Blocked: ổ đĩa máy còn ~0.4GB — dọn trước khi chạy Nuxt/e2e.

### Checkpoint — 2026-11-05
Vừa hoàn thành: 24.7 Hết hiệu lực + 24.8 Hủy duyệt / Đóng hợp đồng + 24.9 Đang thực hiện từ thu tiền / mượn bán — CHƯA commit, worktree `wt-hop-dong-ban`.
Đang làm dở: không.
(cập nhật cuối ngày) 24.10 xong — bộ e2e HĐ 58/58 trên rehearsal.
Bước tiếp theo: (05/11 user: hộp "chờ tôi duyệt" ĐỂ SAU — user đang lên kế hoạch màn duyệt tập trung cho mọi loại phiếu) hỏi user làm tiếp (sửa e2e theo rbac + chạy bộ HĐ / hạch toán DV-CP cho HĐ HRM / Gia hạn – Quyết toán). Commit/push chỉ khi user báo.
Blocked:

- [x] 25.10 Sửa lỗi nhỏ review (06/11, user "sửa nốt các lỗi nhỏ"; hrm-api, CHƯA commit): M1 syncCosts HĐ HRM chặn nguồn lạ / khác HĐ / sai loại YC + chặn gửi duyệt rỗng · M2 requestFlags ≤ 3 truy vấn (nhớ dòng theo HĐ) · M4 câu lỗi riêng HĐ HRM "Dòng đã được yêu cầu hạch toán hoặc không thuộc loại yêu cầu này" · M5 khoá dòng nguồn FOR UPDATE khi gửi duyệt · M6 ghi chú Đang thực hiện theo loại phiếu (dịch vụ / chi phí / vận chuyển — ContractService::ledgerLabel). M3 (VAT theo dòng đầu) GIỮ — cách ERP, spec chốt. Test mới 5 ca RED→GREEN; bộ Phase 25 + HĐ hãng + Rbac xanh.

### Checkpoint — 2026-11-06
Vừa hoàn thành: Phase 25 (hạch toán DV / CP / VC cho HĐ bán HRM) 25.1–25.9 trên hrm-api + hrm-client + ERP; catalog-sync rehearsal; luồng thật API 13/13; commit 7 commit (chưa push).
Đang làm dở: không.
Bước tiếp theo: (tuỳ user) push ERP khi rbac sẵn sàng (hoặc cherry-pick riêng 8e3f46c42c lên origin/gop_db) · ngoài luồng (nút "Chọn hợp đồng" thiếu icon, phiếu nháp giữ id dòng YC cũ, 13 test Read/WriteApi 403) · Gia hạn – Quyết toán HĐ.
Blocked:

### Checkpoint — 2026-11-06 (wrap up)
Vừa hoàn thành: Phase 24.7–24.13 + Phase 25 (25.1–25.10) — commit + push nhánh riêng (api 7318e1714, client 50ca18435); ERP 8e3f46c42c commit local, chưa push (user chọn).
Đang làm dở: không.
Bước tiếp theo: Gia hạn – Quyết toán HĐ (chờ user brainstorm); push ERP khi rbac sẵn sàng.
Blocked:

### Checkpoint — 2026-11-05 (tối)
Vừa hoàn thành: khảo sát nhanh cho Gia hạn — ERP FirmContract không có gia hạn; HRM có khuôn gần giống `ProspectiveProjectExtensionRequest` (xin N ngày, ≤ ngưỡng TP duyệt, > ngưỡng chuyển BGĐ, duyệt xong dời ngày kết thúc).
Đang làm dở: không.
Quyết định: user **ĐỂ SAU** brainstorm Gia hạn (21) — chưa hỏi câu nào, chưa có design.
Bước tiếp theo: hỏi user chọn việc khác (Quyết toán 22/12/11 · lỗi nhỏ ngoài luồng · push ERP 8e3f46c42c).
Blocked:

## 25.11 Lỗi nhỏ ngoài luồng + push ERP (05/11 tối, user "làm tất cả các lỗi" + "sửa cả cho ERP") — đã commit + push 07/11: hrm-api `b48aed273`, hrm-client `37a4fbd87` (origin/gop_db-hop-dong-ban), ERP `722dd0b6a1` (origin/gop_db, cherry-pick qua worktree tạm; local gop_db có bản `f82ef7421d` cùng nội dung)
- [x] 2a hrm-client `ServiceAccountingRequestForm.vue`: nút "Chọn hợp đồng" thêm icon `ri-file-list-3-line` + `.pick-contract-btn { flex-shrink:0; white-space:nowrap }`. Playwright 3060/8060 rehearsal, NV13: TRƯỚC 0 icon, chữ 2 dòng (nút 75–77px ở 1280/1440); SAU 1 dòng ở 1440/1280/1024, icon 13px có glyph, cùng hàng + cùng cao ô mã HĐ, không tràn cột (ô mã HĐ hẹp lại: 176px @1440, 72px @1024). E2E: thêm S5 vào `HRM/e2e/tests/assign/contracts-service-accounting.spec.ts` (chưa chạy).
- [x] 2b Phiếu hạch toán nháp giữ id dòng YC cũ — **lỗi gốc ERP** (`ServiceAccountingRequest::syncCosts` xoá–tạo lại từ 2021, `reject` bỏ mặc phiếu nháp), port 1-1 sang HRM 02/11. User chọn: TỰ ĐỒNG BỘ phiếu nháp khi YC lưu lại.
  - hrm-api `ServiceAccountingRequestService::syncCosts` → `resyncDraftVouchers()` (phiếu Đang tạo của YC chép lại đủ dòng YC hiện tại; phiếu đã duyệt không đụng; giữ `payed_cost` do kế toán nhập). Test RED→GREEN `test_draft_voucher_follows_request_costs_after_reject_and_resubmit` (đỏ: phiếu trỏ [3903], YC còn [3904]).
  - ERP `app/Model/Sale/ServiceAccountingRequest.php` `syncCosts` → `resyncDraftAccountings()` cùng logic (bỏ qua syncItems — luồng service_contract cũ không dùng). Kiểm: `php -l` + đối chiếu form sửa phiếu ERP gửi đủ `revenue_costs` của YC (`getDataForEdit` dòng 296), màn chi tiết đọc dòng chụp (dòng 359). CHƯA chạy thử ERP (config cache local trỏ prod). Sửa ở checkout chính `ERP/TanPhatDev` nhánh `gop_db` local, CHƯA commit.
- [x] 2c 13 test Read/WriteApi 403: cấp quyền kiểu `employee_has_permissions` (rbac bỏ). Mới `tests/Concerns/GrantsLegacyPermissionByRole.php` (tên cũ → alias → mã + min_scope; vai trò tạm `roles.company_id` + `employee_has_roles` + `company_employees`); `AdoptsLegacyRbacFixture` không dùng được trên rehearsal vì `role_has_permissions` đã bỏ `company_id`. Kết quả: Read 13/13, Write 16/16; bộ hạch toán DV (8 file) 63/63; tests/Unit/Rbac 13/13.
- [x] 3 Push ERP: cherry-pick `8e3f46c42c` lên origin/gop_db bằng worktree tạm (merge-tree sạch, php -l 5 file, không phụ thuộc rbac) ⇒ **origin/gop_db `976a994a51`**. Worktree tạm đã gỡ; gop_db local giữ nguyên (vẫn còn 8e3f46c42c riêng — khi đẩy rbac sẽ trùng nội dung, git tự bỏ qua khi rebase/cherry-pick).
- Ngoài luồng (ghi lại, chưa sửa): `Modules/Finance/Tests` trên rehearsal còn 170 ca đỏ (160 lỗi + 10 fail) do fixture quyền kiểu cũ (`employee_has_permissions` / `role_has_permissions.company_id`) — ArrangeReport, BeginningStock, OpeningContract, FastDelivery, Prepick… có sẵn, không thuộc hạch toán DV. Có thể chuyển dần sang `GrantsLegacyPermissionByRole`.

### Checkpoint — 2026-11-05 (đêm)
Vừa hoàn thành: 25.11 (2a, 2b HRM+ERP, 2c) + push ERP origin/gop_db 976a994a51.
Đang làm dở: không.
Bước tiếp theo: user kiểm/commit (hrm-api 4 file, hrm-client 1 file, ERP 1 file — đều chưa commit); push ERP sửa 2b khi user cho; chạy e2e S5 khi user yêu cầu; brainstorm Quyết toán / Gia hạn (đang để sau).
Blocked:

### Checkpoint — 2026-11-06 (e2e 25.11)
Vừa hoàn thành: chạy bộ `contracts-service-accounting` trên worktree 3060/8060, rehearsal, NV13, `--workers=1`: **5/5** (S1–S5, gồm S5 mới của 2a).
- Rehearsal `hrm_contracts` rỗng ⇒ S1–S4 tự skip; dựng HĐ tạm `E2E-P25-TMP` (id 732, 2 dòng DV + phí VC), chạy xong đã xoá.
- Sửa spec S2: `V2BaseRowActions` để 2 hành động hiện đầu tiên thành icon trên dòng ⇒ đếm cả icon lẫn menu, đúng 1 lần (không phải lỗi app).
- Máy mất browser Playwright (`~/Library/Caches/ms-playwright`) ⇒ chạy bằng Chrome hệ thống, tắt video/trace, config tạm ở scratchpad; không chạy provision.
Bước tiếp theo: user kiểm/commit; push ERP sửa 2b khi user cho; brainstorm Quyết toán / Gia hạn.

### Dữ liệu test màn Duyệt hợp đồng — 2026-11-06
DB `hrm_erp_rbac_rehearsal`: HĐ id **734** `HĐ_TPE_HN_KD2_26_0001_TEST-BGD`, Chờ BGĐ duyệt (15), người duyệt NV13 (namdangit). Từ BG-2026-00001 qua service thật (tạo → gửi duyệt → TP ghi HTHT + chuyển BGĐ), thông báo bị fake. 9 hàng + 2 dòng dịch vụ/chi phí chèn riêng vào HĐ (không báo giá nào đã trúng thầu vừa có dịch vụ vừa qua guard DSTC). Vai trò tạm `ZZDEV-BGD-duyet-HD` (công ty 1) cấp "Ban giám đốc duyệt hợp đồng bán hàng" cho NV13 — rehearsal chưa ai có quyền này. Script: scratchpad `mk-bgd.php`.

### Màn Duyệt hợp đồng — brainstorm (06/11/2026, chưa code)
User chốt:
- Bấm Duyệt ⇒ luôn vào màn duyệt rồi mới duyệt (ERP: nút Duyệt nằm trong màn HTHT `sale/firm/accounting/index`).
- Màn duyệt có tab: Hỗ trợ hạch toán / Bản in hợp đồng / Phân tích lãi lỗ (= ERP `report.analysisProfitContract`, lọc theo HĐ; KHÔNG phải tab Tính lãi của paymentManage). HRM chưa có báo cáo này.
- Bước Pháp chế: chỉ xem bản in, duyệt thông tin.
- Đề xuất đánh dấu: bôi đen đoạn trên bản in ⇒ ý kiến (+ ý kiến chung), danh sách bên phải, bật so với mẫu gốc; còn ý kiến mở ⇒ ẩn Duyệt, chỉ Trả lại sửa; người lập đánh dấu Đã sửa; lưu theo vòng duyệt. Chờ user duyệt mô tả.
- Sau khi người lập sửa ⇒ đi lại đủ các bước từ TP (HĐ đã đổi phải duyệt lại).

Mockup: `HRM/.plans/hop-dong/mockup-man-duyet-hd.html` (4 vai trò, số liệu HĐ 734).
Sổ quyết định logic màn Duyệt (chờ user):
- L1 BGĐ có được sửa HTHT khi duyệt không? ERP: được (duyệt tính lại HTHT). HRM hiện chỉ xem. Mockup: chỉ xem.
- L2 Tab Phân tích lãi lỗ theo quyền nào? ERP: `accounting.bao_cao_phan_tich_lai_lo_theo_htht_hop_dong.view` phạm vi công ty trở lên; không có quyền thì ẩn tab — hay người duyệt luôn xem được?
- L3 HĐ ẩn giá: tab bản in / lãi lỗ hiển thị thế nào với người duyệt.

Mockup bản 2 (06/11): dải tuyến trình ký thay callout + khối thông tin; thêm Gửi duyệt (05:29, đã chờ); thông tin phụ mở bằng Chi tiết; tóm tắt hiệu quả + cơ cấu giá trị trên tab HTHT; tab đúng mẫu V2BaseTabNavigation.

Mockup bản 3 (06/11): đúng layout app; khối thông tin + tuyến trình ký có 3 phương án trong vùng nội dung (A thẻ ngang, B một dòng, C cột phải) — chờ user chọn. Bảng bản in có viền theo reportPrintStyle.

Mockup bản 4 (06/11): user chốt phương án C (panel thông tin + tuyến trình ký cột phải 262px) + nút thu gọn còn 46px (chấm quy trình + tooltip), nhớ trạng thái theo người xem. Còn hỏi L1–L3.

L1 chốt nguyên tắc (06/11): phần nào ERP cho sửa khi duyệt thì HRM giữ nguyên logic — khảo sát kỹ ERP sau.
Vấn đề mới: soạn HĐ chưa biết số trang + chỗ ngắt trang. Hiện trạng: CKEditor 5 không có trang; xem trước 1 tờ dài (min-height A4); in bằng print() của iframe, `@page A4 12mm 10mm`; mẫu không có ngắt trang tay. Đề xuất: Paged.js cho xem trước + in (chưa thử).

Bản thử ngắt trang (06/11, ngoài source; Paged.js 0.4.3 MIT): HĐ 734 5 trang, 250 dòng 19 trang 0,36s; PDF in ra bằng đúng các tờ xem trước. 42 bố cục (9–250 dòng): không mất/lặp chữ, không tách khối ký, 0 trang trống. Mockup bản 5 đã gắn tờ A4 + Trang x/y + ngắt trang tay (vai Người lập).
Bẫy khi code thật:
- Paged.js bỏ wrapper ngoài: gốc CSS in phải là `.pagedjs_page_content`; CSS nội dung nạp style thường, chỉ @page + break-* đưa qua Previewer.
- `break-after: avoid` KHÔNG có tác dụng ⇒ tự dò tiêu đề là dòng chữ cuối trang (TreeWalker text + getClientRects, chỉ phần strong/b/u vì Điều 8 gộp tiêu đề + nội dung 1 đoạn) rồi thêm break-before và chia lại.
- Tiêu đề bảng không tự lặp ⇒ Handler afterPageLayout chèn thead vào table[data-split-from].
- Chia lại phải gọi page.removeListeners(), không thì lỗi findEndToken (ResizeObserver).
- Gắn chú thích sau khi chia không được làm đổi layout (ghim position:absolute).
- Bản min export `PagedModule`, bản thường export `Paged`.
- So với print() cũ: trang 1 ít hơn 1 dòng hàng, cùng 5 trang.
Chưa kiểm: máy Windows/font khác, Safari/Firefox, Nuxt 2 thật, HĐ nhiều ô bảng dài hơn 1 trang.

Mockup: thêm zoom bản in − / % / + (50–200%, bấm % về vừa khung, giữ đúng trang đang xem, không ảnh hưởng bản in).
Thêm bẫy Paged.js: đoạn bị cắt sang trang được gắn `text-align-last: justify`, đoạn có <br> sẽ giãn chữ mọi dòng ⇒ override `[data-align-last-split-element]{text-align-last:auto!important}`.

Yêu cầu mới (06/11): ở mỗi bước, người xem đọc được ý kiến duyệt/không duyệt của các bước khác, có lịch sử.
Mockup: ý kiến mới nhất hiện ngay dưới bước trên tuyến duyệt (panel phải); nút "Lịch sử duyệt (n)" mở ngăn kéo bên phải, chia theo lần gửi duyệt, mới nhất ở trên, không che thanh nút Duyệt; panel thu gọn còn icon + số. Vai đổi thành 1 câu chuyện: Pháp chế (lần 1) → Người lập → TP (lần 2) → BGĐ. BGĐ không còn minh hoạ ca bỏ qua Pháp chế.
Khi code thật (đối chiếu code 06/11):
- ERP: ô `approve_comment` + khối "Lịch sử duyệt" (Tài khoản, Nội dung, Hành động, Thời gian) từ `log_approves` trên màn HTHT.
- HRM đã có `hrm_contract_histories` (note, actor, action) và `histories` trong DetailContractResource; tab Lịch sử ở chi tiết HĐ.
- HRM còn thiếu: `approve()` và `submit()` không nhận ghi chú ⇒ Duyệt/Gửi duyệt chưa lưu được ý kiến. Không duyệt (`rejected_reason`, tối đa 255) và Chuyển BGĐ (`note`, tối đa 255) đã lưu.
- Lần gửi duyệt: chưa có cột, suy từ số dòng action `submit`. Lọc bỏ action không thuộc duyệt (update, legal_edit_on...).
- Ý kiến đánh dấu trên bản in của Pháp chế chưa có nơi lưu.

Phase 26 (06/11): khảo sát ERP xong, tài liệu `design-phase26-man-duyet.md` đã qua builder check, chờ user chốt Q1–Q5. Mockup: BGĐ sửa được HTHT như ERP, bỏ chữ đỏ ở lịch sử.
Phase 26 (06/11): user chốt D11–D15 (Pháp chế trước rồi mới chuyển BGĐ; tách `is_market`; quyền tab lãi lỗ; Paged.js cả In ở chi tiết; chỉ HĐ chính). Bước tiếp: user duyệt tài liệu, rồi viết plan.


## Phase 26 — Màn Duyệt hợp đồng bán (06/11/2026 — PLAN, CHƯA code)

> **For agentic workers:** dùng superpowers:subagent-driven-development hoặc superpowers:executing-plans chạy từng task; checkbox `- [ ]`.

**Goal:** Mọi bước duyệt HĐ bán HRM đi qua một màn Duyệt có 3 tab, ý kiến và lịch sử đọc được ở mọi bước, HTHT sửa theo đúng logic ERP giữa TP và BGĐ.
**Architecture:** Giữ URL `/assign/contracts/:id/support-accounting`, tách trang thành các component nhỏ theo tab. BE mở rộng `ContractService` + `ContractSupportAccountingService`, lịch sử đọc từ `hrm_contract_histories`, 1 bảng mới cho ý kiến Pháp chế, 1 service mới cho lãi lỗ. Bản in chia tờ bằng Paged.js nạp từ `static/`.
**Tech Stack:** Laravel 8 (hrm-api), Nuxt 2 / Vue 2 (hrm-client), Paged.js 0.4.3, PHPUnit, Playwright.
**Spec:** `design-phase26-man-duyet.md` (D1–D17, C1–C8). Mockup: `mockup-man-duyet-hd.html`.

### Global Constraints
- Đụng source phải được user "làm" riêng từng giai đoạn, nêu repo · nhánh · file. Migration hỏi riêng, liệt kê tên, chạy lẻ `--path` vào `hrm_erp_rbac_rehearsal`.
- Nhánh `gop_db-hop-dong-ban`, worktree `wt-hop-dong-ban`. KHÔNG commit / push trừ khi user ra lệnh: mỗi task kết thúc ở "để nguyên chưa commit".
- Sửa hàm / component dùng chung (`ReportPrintPreviewModal`, `contractPrintMixin`) phải hỏi trước.
- PHPUnit: `DB_DATABASE=hrm_erp_rbac_rehearsal DB_DATABASE_SECOND=hrm_erp_rbac_rehearsal DB_DATABASE_TPE=hrm_erp_rbac_rehearsal /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit <file>`, trait `DatabaseTransactions`.
- Ghi chú Duyệt / Gửi duyệt / Chuyển BGĐ / lý do Không duyệt: tối đa 255 ký tự. Chuyển BGĐ và Không duyệt bắt buộc, FE và BE cùng chặn.
- Nhãn action lịch sử lấy từ `historyActionLabel`. Nút theo `button-convention` ("Gửi duyệt", không "Trình duyệt"). Chữ đỏ chỉ cho lỗi validate. Nút không dùng được thì ẩn.
- Duyệt / Chuyển duyệt / Không duyệt / Gửi duyệt lại xong về màn danh sách.
- FE: `V2Base*`, `V2Footer`, `V2BaseModal`, `$confirm`, `V2BaseTabNavigation`. Kiểm bằng Playwright đo DOM ở 1440 và 1366. Có quyền và không quyền đều phải kiểm. Tài khoản namdangit, HĐ 734, e2e `--workers=1` chỉ chạy khi user yêu cầu.

### Review Focus
1. Hai người mở cùng HĐ, người kia duyệt trước: bấm Duyệt báo "Trạng thái không hợp lệ", HTHT không bị ghi đè (test ở 26.2).
2. HĐ đang Chờ BGĐ từ trước khi deploy, HTHT chỉ có detail type 3: cột Đề xuất lấy từ type 3, không rỗng (test ở 26.2).
3. Không duyệt ở BGĐ rồi gửi lại: TP mở ra tính lại từ quy chế, dòng Đề xuất cũ không lẫn vào lượt mới (test ở 26.2).
4. Đoạn ý kiến xuất hiện nhiều lần trong HĐ, hoặc vắt qua 2 tờ: ghim đúng chỗ theo `quote_before` / `quote_after` (test ở 26.10).
5. HĐ 250 dòng hàng: tab Bản in có trạng thái đang tải, trang vẫn thao tác được, không mất / lặp chữ (test ở 26.7).

### GĐ 1 — BE luồng duyệt (hrm-api, không đụng DB)

### Task 26.1: Ghi chú duyệt + `approval_history`
**Files:** Modify `Modules/Assign/Services/ContractService.php`, `Http/Controllers/Api/V1/ContractController.php`, `Transformers/DetailContractResource.php`. Test `Modules/Assign/Tests/Feature/ContractApprovalHistoryTest.php`.
**Produces:** `approve(Contract $c, ?string $note = null)`, `submit(Contract $c, ?string $note = null)`, `transition(..., ?string $note = null, ?array $meta = null)`. Trường `approval_history[]`: `round, step, action, action_label, actor_name, created_at, note, opinions`.
- [x] Test: `test_approve_ghi_note_vao_lich_su`, `test_transfer_thieu_note_tra_422`, `test_submit_ghi_note`, `test_history_hai_vong_dung_round` (submit → approve → reject → submit: round 1,1,1,2), `test_history_loc_bo_action_update`, `test_history_sap_theo_id_khi_trung_giay`, `test_reject_step_lay_tu_from_status`, `test_hide_price_khong_tra_note` (cả `approval_history` và `histories`). Chạy, thấy FAIL.
- [x] Thêm `note` nullable max 255 cho approve, submit; `required|max:255` cho transfer. Chỉ lấy action `submit, approve, legal_approve, bgd_approve, reject, transfer_bgd, cancel_approve`.
- [x] Chạy test mới + `ContractServiceAccountingFlagsTest`, thấy PASS. Để nguyên chưa commit.

### Task 26.2: Đề xuất / Đã duyệt và nguồn số HTHT (mục 5.3, 5.3a)
**Files:** Modify `Services/ContractSupportAccountingService.php`, `ContractController.php` (`approve`, `transferBgd`, `supportAccounting`), `Services/ContractService.php`. Test `Tests/Feature/ContractHthtStepFlowTest.php`.
**Produces:** `loadSavedInputs(Contract $c): ?array` (số đã lưu dạng payload form), `promoteToApproved(Contract $c): void` (status 2, thêm detail type 3 từ số đã lưu, giữ type 2). `GET support-accounting` trả thêm `input_source` (`regulation|saved`) và mỗi phòng có `regulation_values`, `proposed_values` (type 2, thiếu thì lấy type 3).
**Consumes:** `calculate(Contract, array, bool $isAccept)` có sẵn.
- [x] Test: `test_tp_chuyen_bgd_luu_de_xuat` (status 1, type 2), `test_tp_duyet_sang_phap_che_luu_de_xuat`, `test_tp_duyet_cuoi_luu_da_duyet`, `test_phap_che_duyet_cuoi_promote`, `test_bgd_mo_man_thay_so_tp`, `test_bgd_sua_roi_duyet_so_luu_bang_so_xem_truoc`, `test_bgd_duyet_giu_dong_de_xuat` (D16), `test_tp_luot_gui_lai_tinh_lai_tu_quy_che`, `test_hd_cu_chi_co_type3_cot_de_xuat_khong_rong`, `test_nguoi_khac_duyet_truoc_thi_khong_ghi_de_htht`. Chạy, thấy FAIL.
- [x] `calculate` ở bước `tp` (isAccept theo việc HĐ có kết thúc ở Chờ KH ký không) và bước `bgd` (true). Bước `tp` khi lưu xoá hết detail cũ. Bước `bgd` giữ type 2.
- [x] `supportAccounting`: bước `tp` tính từ quy chế; bước `bgd` và chỉ xem dùng `loadSavedInputs`, chưa có thì tính từ quy chế.
- [x] Chạy test, thấy PASS. Để nguyên chưa commit.

### Task 26.3: Chốt chặn theo ERP (mục 4, 5.3a, D11)
**Files:** Modify `ContractService.php`, `ContractSupportAccountingService.php`, `ContractController.php`. Test `Tests/Feature/ContractApproveGuardsTest.php`.
**Produces:** `assertHthtValid(array $preview, bool $isBgd, bool $isTransfer): void` (ValidationException), lý do `regulation_changed` trong `composeBgdReasons`, payload `confirm_bonus_over`.
- [x] Test: tổng %DS khác 100 chặn; tổng phân chia khác 100 chặn; phòng thiếu quy chế chặn; 20.1 hoặc 20.2 bằng 0 KHÔNG chặn; đổi 14.1 mà mục 15 khác 0 chặn cả BGĐ; TP không quyền BGĐ đổi 1 trong 5 tỷ lệ phòng chính, không Pháp chế: Duyệt bị chặn, Chuyển được; đổi %DS hoặc 21.1.x: Duyệt được; có Pháp chế: TP Duyệt được, Pháp chế chỉ Chuyển được (D11); BGĐ đổi tỷ lệ Duyệt được; 14.1 vượt % công ty thiếu `confirm_bonus_over` chặn; thiếu giá vốn công ty báo rõ mã. Chạy, thấy FAIL.
- [x] Thêm các chặn. 5 khoá so sánh: `month_percent, after_commission_percent, month_employee_percent, month_part_lead_percent, month_department_lead_percent`, chỉ phòng chính, so detail type 1.
- [x] Rà `ProductImportRequestService`, `BorrowSellRequestService` có đọc `status` / detail type của HTHT không. Có thì nêu user trước khi đi tiếp.
- [x] Chạy test mới + toàn bộ test Contract của `Modules/Assign/Tests`, thấy PASS. Để nguyên chưa commit.

### GĐ 2 — Khung màn Duyệt (hrm-client, không đụng DB)

### Task 26.4: Lối vào, panel, tab, thanh nút
**Files:** Modify `pages/assign/contracts/_id/support-accounting.vue`, `_id/index.vue`, `index.vue`; `hrm-api .../ContractNotificationService.php` (url sự kiện chờ duyệt). Create `pages/assign/contracts/components/approval/ApprovalInfoPanel.vue`, `ApprovalRoute.vue`, `ContractHthtTab.vue` (chuyển nguyên phần HTHT sang).
**Produces:** prop `contract`, computed `approvalTabs` theo bảng 5.2; panel nhớ `duyet-hd-panel`.
- [x] Đo trước trên HĐ 734: chi tiết có nút Duyệt thẳng, Bước BGĐ không qua màn. Ghi số.
- [x] Dựng trang theo mockup: tiêu đề `Duyệt hợp đồng: <mã> (<trạng thái>)`, `V2BaseTabNavigation`, panel 262px / 46px, `V2Footer`. Tab theo vai, tab Bản in và Lãi lỗ để khung rỗng.
- [x] Chi tiết chỉ còn 1 nút Duyệt chuyển sang màn. Bỏ Duyệt thẳng, Chuyển BGĐ, Không duyệt. Danh sách action Duyệt đi thẳng màn Duyệt. "Trình duyệt" đổi "Gửi duyệt" + ô ghi chú.
- [x] Playwright: đo số nút ở danh sách và chi tiết khớp; panel không tràn ở 1366; 0 lỗi console; người không duyệt chỉ có Quay lại. Sửa spec e2e bị ảnh hưởng, chưa chạy nếu user chưa yêu cầu.

### Task 26.5: Tab HTHT sửa được theo vai
**Bắt buộc từ GĐ 1:** nạp form từ GET rồi mới gửi lại (`buildParams` hiện gửi 0 mặc định); gửi `approval_step` khi approve / transfer-bgd / reject; gửi `confirm_bonus_over` sau xác nhận (cả Chuyển BGĐ và Pháp chế duyệt cuối, với người có quyền BGĐ); hiện lỗi theo khoá `regulation, commission_sale_percent, diff_percent, month_share_percent, bonus_contract_before_vat, bgd, confirm_bonus_over, cost`; không gửi `contract_execution_costs` khi không có quyền giá vốn; nhãn ghi chú Chuyển BGĐ có dấu `*`; `step` của `cancel_approve` là null.
**Files:** Modify `components/approval/ContractHthtTab.vue`. Create `components/approval/ApprovalBrief.vue` (dải hiệu quả + cơ cấu).
**Consumes:** `input_source`, `regulation_values`, `proposed_values` (26.2). Payload `department_main`, `departments_support`, `confirm_bonus_over`.
- [x] `isPreview` = không `is_can_approve`, hoặc `approval_step` khác `tp`, `bgd`.
- [x] Thêm ô % phòng chính + phòng hỗ trợ theo `department-main.blade.php`: TP cột Quy chế / Đề xuất; BGĐ thêm cột Duyệt, cột Đề xuất chỉ đọc. Lỗi hiện dưới ô, giữ số user nhập.
- [x] Dialog Duyệt có ô ghi chú. Xác nhận thưởng vượt quy chế dùng `$confirm`. Xong về danh sách.
- [x] `ApprovalBrief` ẩn khi `can_view_full = false`.
- [x] Playwright với HĐ 734: BGĐ sửa 1 ô %, số xem trước đổi, Duyệt xong số lưu khớp; không có quyền giá vốn thì không thấy dải và cột II, III.

### Task 26.6: Lịch sử trên tuyến duyệt + ngăn kéo
**Files:** Modify `components/approval/ApprovalRoute.vue`. Create `components/approval/ApprovalHistoryDrawer.vue`.
**Consumes:** `approval_history` (26.1).
- [x] Ý kiến mới nhất dưới mỗi bước duyệt, trừ bước đang chờ và bước Lập, tối đa 3 dòng; lần cũ ghi "Lần 1, không duyệt:".
- [x] Ngăn kéo 384px, chia theo lần, mới nhất ở trên, dòng đang chờ, liệt kê `opinions`. Không che `V2Footer`, Esc đóng và trả focus. Panel thu gọn còn icon + số.
- [x] Playwright đo như mockup: rect ngăn kéo, nút footer bấm được khi mở, focus, 2 vòng trả lại đúng số lượt.

### GĐ 3 — Bản in chia tờ (hrm-client)

### Task 26.7: `ContractPagedView` trên tab Bản in
**Files:** Create `static/pagedjs/paged.min.js`, `components/print/ContractPagedView.vue`, `utils/print/pagedContract.js`. Modify `pages/assign/contracts/_id/support-accounting.vue`.
**Produces:** props `html`, `readonly`; sự kiện `paged({ pageCount })`; method `repaginate()`; prop slot cho lớp ghim.
- [x] Port từ mockup: Handler lặp thead, dò tiêu đề cuối trang, `removeListeners`, override `text-align-last`, gốc CSS `.pagedjs_page_content`. Nạp script khi mở tab, có trạng thái đang tải.
- [x] Pager, zoom − % + (`0.5, .75, .9, 1, 1.1, 1.25, 1.5, 2`), bấm % về vừa khung, giữ trang đang xem. Dữ liệu `print-data` mode `contract`, không gửi `group`.
- [x] Playwright: HĐ 734 ra 5 tờ; so toàn văn với HTML nguồn không mất / lặp chữ; 250 dòng còn thao tác được; PDF cùng số tờ; zoom không đổi số tờ.
- [x] Kiểm thêm Safari, Firefox, ô bảng dài hơn 1 trang. Ghi kết quả; Windows nhờ user kiểm.

### Task 26.8: In hợp đồng ở chi tiết dùng cùng cách chia tờ (D14)
**Files:** Modify `contractPrintMixin`, `components/print/ReportPrintPreviewModal.vue` (hỏi user trước, file dùng chung).
- [x] Đo trước các chế độ in hợp đồng: số tờ, QR, chỗ ký. Ghi số.
- [x] Chỉ mode `contract` đi qua Paged.js. Giữ QR, `markSignatureSpace`. Phụ lục, biên bản giữ nguyên.
- [x] Playwright: bản in chi tiết cùng số tờ với màn Duyệt; 1 màn in khác dùng `ReportPrintPreviewModal` không đổi. Không bấm In thật trong MCP (khoá trình duyệt), kiểm bằng PDF.

### GĐ 4 — Ý kiến Pháp chế (cả 2 repo, 1 migration)

### Task 26.9: Bảng + API ý kiến
**Files:** Create migration `create_hrm_contract_legal_notes_table`, `Entities/Contract/ContractLegalNote.php` (`extends BaseModel`), `Services/ContractLegalNoteService.php`. Modify `Routes/api.php`, `ContractController.php`, `ContractService.php`, `ContractNotificationService.php`. Test `Tests/Feature/ContractLegalNoteTest.php`.
**Produces:** `GET|POST /{id}/legal-notes`, `POST /{id}/legal-notes/{noteId}/fix` (`reply`), `/reopen`, `/close`, `DELETE /{id}/legal-notes/{noteId}`. Status 1 Cần sửa, 2 Đã sửa, 3 Đạt. Cột theo mục 5.5.
- [x] Hỏi user cho chạy đúng migration trên vào rehearsal.
- [x] Test: chỉ Pháp chế ở bước `legal` tạo / xoá / đạt; chỉ người lập ở Không duyệt bấm Đã sửa; xoá chỉ khi Cần sửa; Pháp chế không Duyệt / Chuyển được khi còn ý kiến chưa Đạt; người lập không gửi lại được khi còn Cần sửa; reject chụp ý kiến vào `meta.opinions`; không tắt được `need_legal_approval` khi còn ý kiến chưa Đạt (C5). Chạy, thấy FAIL.
- [x] Làm cho test xanh. Thông báo theo `notification-convention`. Để nguyên chưa commit.

### Task 26.10: Đánh dấu trên bản in
**Files:** Create `components/approval/LegalNotesPanel.vue`, `utils/print/legalNoteAnchor.js`. Modify `components/print/ContractPagedView.vue`.
**Consumes:** API 26.9, `paged` (26.7). **Produces:** `findAnchor(root, { quote, before, after }): Range|null`.
- [x] Unit / Playwright: đoạn lặp 2 lần chọn đúng theo ngữ cảnh; đoạn vắt 2 tờ tìm được; đoạn đã sửa trả null, hiện "Đoạn đã thay đổi" kèm chữ gốc; ghim không đổi số tờ.
- [x] Lối vào của Người lập: chi tiết có nút Xem ý kiến cần sửa khi Không duyệt có ý kiến; `canViewHtht` và link thông báo `contract_rejected` trỏ đúng màn Duyệt.
- [x] Bôi đen hiện nút Đánh dấu, ô nhập, Ý kiến chung, cột ý kiến 300px, xem khác mẫu gốc qua `template-diff`. Vai Người lập: Đã sửa + phản hồi, nút Sửa hợp đồng, Gửi duyệt lại.
- [x] Playwright chạy đủ 2 vòng trên HĐ thử: đánh dấu → trả lại → sửa → TP → Pháp chế Đạt → chuyển BGĐ.

### GĐ 5 — Tab Phân tích lãi lỗ (cả 2 repo)

### Task 26.11: API lãi lỗ + quyền
**Files:** Create `Services/ContractProfitAnalysisService.php`. Modify `ContractController.php`, `Routes/api.php`, `app/Support/Permissions/Catalog/accounting.php` (theo skill `permission-seeder`). Test `Tests/Feature/ContractProfitAnalysisTest.php`.
**Produces:** `GET /{id}/profit-analysis` → `{ rows[], total }`, 15 cột theo mục 5.7.
- [x] Test: công thức trên HĐ 734 đối chiếu tay; dòng dịch vụ có giảm giá được trừ; có giá nhập gần nhất / không có thì lấy giá vốn công ty; cổng D13: TP đang duyệt có Xem giá vốn được, không có Xem giá vốn 403 kể cả BGĐ, người khác cần quyền báo cáo, `hide_price` 403. Chạy, thấy FAIL.
- [x] Làm cho test xanh. `permission:sync --dry-run` xem trước, nêu user trước khi chạy seeder. Để nguyên chưa commit.

### Task 26.12: FE tab + tổng kiểm
**Files:** Create `components/approval/ContractProfitTab.vue`. Modify trang màn Duyệt.
- [x] Bảng theo mẫu dữ liệu chung, số `en-US`, cuộn ngang 2 thanh qua `V2BaseTableScroll`, tiêu đề cột 1 dòng. Tab chỉ tải khi mở.
- [x] Playwright: có quyền / không quyền; tổng khớp API.
- [x] Soát cả màn theo bảng tab 5.2 với 4 vai, đo DOM ở 1440 và 1366. Nêu user chạy e2e toàn màn.
- [x] Gỡ role `ZZDEV-BGD-duyet-HD`, xoá cache quyền khi user đồng ý. Cập nhật `design-phase26-man-duyet.md`, checkpoint.

### Checkpoint — 2026-11-06 (plan Phase 26)
Vừa hoàn thành: khảo sát ERP, tài liệu thiết kế, plan Phase 26.
Đang làm dở: không.
Bước tiếp theo: user duyệt plan, rồi cho phép GĐ 1 (hrm-api, không migration).
Blocked: chờ user "làm".

### Checkpoint — 2026-11-06 (GĐ 1 xong)
Vừa hoàn thành: 26.1–26.3 (hrm-api, chưa commit, không migration). 100 test mới xanh. Rà từng task + rà tổng.
Đang làm dở: không.
Bước tiếp theo: user cho phép GĐ 2 (26.4–26.6). GĐ 1 KHÔNG deploy riêng: 110/497 quy chế có phân chia 0/0/0 nên TP cần ô % của 26.5; FE chưa gửi `confirm_bonus_over`.
Blocked: chờ user "làm GĐ 2". `ProductExportOverLimitApiTest` đỏ 5/6 (3 lỗi khoá ngoại ở fixture), chưa đo trên code gốc. Test mới dùng `tests/Concerns/GrantsLegacyPermissionByRole.php` chưa track, commit phải đi cùng. Bảng detail chỉ có khoá chính, cần index thì hỏi migration riêng.

### Checkpoint — 2026-11-06 (GĐ 2 xong)
Vừa hoàn thành: 26.4–26.6 (hrm-client + `ContractNotificationService` hrm-api, chưa commit). Đã rà từng task + rà tổng. Chạy thật trên trình duyệt: BGĐ sửa rồi Duyệt, TP Duyệt có sửa %, Pháp chế Duyệt; HĐ 734 đã khôi phục, role tạm đã gỡ.
Đang làm dở: không.
Bước tiếp theo: user cho phép GĐ 3 (26.7–26.8).
Blocked: nhãn "Từ chối" (button-convention) hay "Không duyệt" (design, mockup, code cũ) chờ user. Người xem thật không có quyền mới chứng minh được API 403, chưa đo giao diện (đăng nhập NV khác bị chặn). GĐ 1–2 chưa lên riêng được: Pháp chế, Người lập mới thấy tab Bản in rỗng. e2e đã sửa spec, chưa chạy. Bảng giá trong panel đang trống vì `price_types` chưa nạp.

### Lưu ý khi merge Phase 26 (06/11, tin từ phiên go-live RBAC, chưa tự kiểm)
- origin/gop_db đã có RBAC: hrm-api `7b71f6462`, hrm-client `66871e570`. Kéo gop_db mới trước khi merge nhánh này.
- Seeder quyền HRM đã gỡ; quyền khai ở `app/Support/Permissions/Catalog/*.php`, tên cũ ở `legacy`. Task 26.11 (mở quyền báo cáo lãi lỗ) làm theo Catalog; thiếu khai báo thì quyền luôn false.
- Không bypass theo Super Admin / role 18.
- Code gop_db mới cần DB đã chuyển đổi (bảng `permission_aliases`), DB local `db_gop_6_11`. Rehearsal chưa chuyển đổi có thể lỗi 500 sau khi kéo.
- `.tp-card` không có trong CSS toàn cục, kiểm trên nuxt build.
- Chi tiết: `.plans/gop-db/quan-ly-vai-tro-quyen/gd1-nen-du-lieu/chuan-bi-go-live-06-11.md`.

### Checkpoint — 2026-11-06 (GĐ 3 xong)
Vừa hoàn thành: 26.7–26.8 (hrm-client, chưa commit). Bản in chia tờ trên màn Duyệt, In hợp đồng ở chi tiết và dòng danh sách dùng chung.
Đang làm dở: không.
Bước tiếp theo: user xác nhận phạm vi nút In ở danh sách; rồi GĐ 4 (cần liệt kê migration `hrm_contract_legal_notes`).
Blocked: chưa kiểm hộp thoại in thật, Safari, Firefox, Windows; spec F27–F30 chưa chạy. `br + br` trong `buildReportPrintCss` vẫn làm mất xuống dòng ở các bản in khác (ngoài luồng, chưa sửa).

### Checkpoint — 2026-11-07 (GĐ 4 xong)
Vừa hoàn thành: 26.9–26.10 (hrm-api + hrm-client, chưa commit). Migration `2026_11_06_000001_create_hrm_contract_legal_notes_table` đã chạy lẻ vào rehearsal (batch 457).
Đang làm dở: không.
Bước tiếp theo: GĐ 5 (26.11–26.12), nhớ quyền khai ở Catalog.
Blocked: sự cố push khi kiểm 26.10: 2 lần Gửi duyệt lại báo TP 34, 867, 1084 (đã xoá 6 dòng notifications, push không thu hồi được). Không có thông báo khi người lập bấm Đã sửa. Chưa kiểm hộp thoại in thật, Safari, Firefox, Windows; F27–F34 chưa chạy.

### Checkpoint — 2026-11-07 (GĐ 5)
Vừa hoàn thành: 26.11–26.12 (hrm-api + hrm-client, chưa commit). GĐ 4 đã commit: api `9951f8c7b`, client `488fb9f38`. Tab Lãi lỗ theo cờ BE `can_view_profit_analysis`, HĐ 734 khớp tính tay.
Đã commit + push GĐ 5 (07/11): api `8f63fb868`, client `a4d53845b` lên origin/gop_db-hop-dong-ban. Role tạm `ZZDEV-BGD-duyet-HD` đã gỡ khỏi rehearsal 07/11 (3 dòng).
Đã chốt 5 điểm lệch ERP (design 5.7, 07/11) và code: vốn DV = `estimated_price`, ≤ 0 là chưa có vốn, HĐ Đang tạo 403. HĐ 734 nay vốn 148.604.356,75, lãi 86.731.643,25. Thêm e2e F39. E2E `contracts-approval-flow` 39/39 xanh (07/11, worktree 3060/8060, `--workers=1`, không chạy provision; spec thêm lưới chặn lệnh ghi, sửa F26 route bắt nhầm URL trang + `openWith` dùng fallback, F25 dùng HTHT giả, F27 đo chữ ngoài khung thay scrollWidth).
Ngoài luồng đã sửa 07/11 (hrm-client, CHƯA commit): `ContractPagedView.measure` cộng scrollY; màn Duyệt bỏ min-height 1550px của theme (class `hd-approval-fit` trên body, chỉ màn này) + bỏ `min-vh-100 pb-5` và padding 80px trùng với `body.has-v2-footer`; `FOOTER_GAP` 62→66 (bản in + lãi lỗ); Paged.js `checkUnderflowAfterResize` bọc try/catch trong handler (hết lỗi getAttribute, kết quả chia tờ không đổi). E2E thêm F40 + F27 kiểm getAttribute: 40/40.
Đã commit + push 07/11: hrm-client `3ee34942c` (origin/gop_db-hop-dong-ban) (3 lỗi ngoài luồng màn Duyệt); ERP `0932118973` local ⇒ origin/gop_db `b7d0b352c8` (cherry-pick) — báo cáo lãi lỗ HTHT trừ giảm giá dòng dịch vụ (đọc allocated_price do UNION; 111 dòng / 104 HĐ / 366.303.218 đ trên db_gop_6_11), kiểm tinker trước/sau + màn báo cáo ERP 8094 dòng Tổng cộng khớp. ERP gop_db local ahead 2 / behind 5 ⇒ push phải cherry-pick qua worktree tạm.
Bước tiếp theo: merge phải pull RBAC gop_db trước; deploy nhớ `permission:catalog-sync`.
Blocked: chưa đo tài khoản thật không quyền trên trình duyệt (chỉ giả lập + test BE). Việc ngoài luồng: `$body-min-height: 1550px` của theme làm trang cuộn thừa; lỗi `getAttribute` trong `paged.min.js` chỉ là nhiễu console, không mất nội dung; lỗi giảm giá dịch vụ ERP (đọc `allocated_price` của UNION) còn chờ task riêng.

## Phase 27 — Soạn mẫu in hợp đồng theo trang A4 như Word (07/11/2026 — THIẾT KẾ, chưa plan, chưa code)
Thiết kế: `design-phase27-soan-theo-trang.md`. Giai đoạn 1 = tab Mẫu in → "Mẫu in hợp đồng" của form Sửa HĐ; CKEditor 4 inline +
chia tờ bằng chính `paginateContract`. User chốt 07/11: bố cục A (giống Word), thay hẳn editor cũ, biến hiện dữ liệu thật, bảng hàng
hoá khoá tuyệt đối, đoạn văn không cắt đôi (đoạn = cụm tách `<br>`), chia lại toàn bộ (chưa làm chia từng phần), dàn trang không bật cờ
Pháp chế, hiện ý kiến Pháp chế trên trang soạn, độ rộng cột bảng hàng hoá = nên có.
HĐ test: 3443 `HĐ_TPE_HN_KD2_26_0001_TEST-PAGING` (rehearsal, Đang tạo, người lập 13) + báo giá tạm 546; id ở scratchpad `hd-clone-ids.json` — xoá khi xong.
Bước tiếp theo: user duyệt plan bên dưới → chọn cách chạy → hỏi "làm" + phạm vi trước khi code.

# Phase 27 — Implementation Plan (07/11/2026, CHƯA code)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tab Mẫu in → "Mẫu in hợp đồng" của form Sửa HĐ soạn trực tiếp trên các tờ A4 như Word, chỗ ngắt trùng bản in.
**Architecture:** CKEditor 4 inline trong khung CSS của bản in; sau mỗi lần ngừng gõ gọi `paginateContract` trên bản sao để biết khối mở đầu từng trang, rồi chèn khoảng trống hiển thị (không lưu) để vùng soạn thành tờ rời. Biến hiện bằng widget khoá chứa giá trị thật lấy từ API; lưu ra lại `{{BIEN}}`. Đổi quy tắc in: đoạn (cụm tách `<br>`) không cắt đôi.
**Tech Stack:** Nuxt 2 / Vue 2 (node 12), CKEditor 4.22.1 (`static/ckeditor`), Paged.js 0.4.3 (`static/pagedjs`), Laravel 8 + PHP 7.4 (hrm-api), PHPUnit, Playwright.
**Spec:** `design-phase27-soan-theo-trang.md` (cùng thư mục).

## Global Constraints
- Repo: worktree `wt-hop-dong-ban` (hrm-api + hrm-client). Nhánh: hỏi user khi bắt đầu (đề xuất nhánh mới tách từ `gop_db-hop-dong-ban`).
- Code chỉ khi user nói "làm" + phạm vi; migration chỉ đúng bản đã nêu, chạy lẻ `--path`; không commit / push khi user chưa bảo.
- PHP 7.4 (không `?->`, không `match`). Node 12: không cú pháp `?.` / `??` trong file `.js` thường không qua babel (kiểm cách repo đang viết).
- Bảng hàng hoá và mọi biến `{{X}}`: **không sửa được** trên trang soạn (luật tuyệt đối). Dữ liệu lưu giữ đúng định dạng HTML + `{{X}}` hiện tại.
- Một nguồn CSS: vùng soạn dùng `contentCss()` + gốc `.contract-paged .pagedjs_page_content`, rộng `SHEET_BODY_WIDTH` = 190mm.
- Dữ liệu lưu **không** chứa `data-ed`, khoảng trống hiển thị, thead bản sao, đánh dấu ý kiến Pháp chế.
- Kiểm FE bằng Playwright MCP đo DOM; e2e chỉ chạy khi user yêu cầu, `--workers=1`, không chạy provision (dùng config tạm như 07/11).
- Test BE: `DB_DATABASE=hrm_erp_rbac_rehearsal DB_DATABASE_SECOND=hrm_erp_rbac_rehearsal DB_DATABASE_TPE=hrm_erp_rbac_rehearsal /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit <file>`.
- HĐ test: 3443 (Đang tạo, người lập NV13 namdangit), 734 (Chờ BGĐ). Mục tiêu tốc độ: ≤ 10 trang ≤ 300ms, 32 trang ≤ 2 giây sau khi ngừng gõ; gõ không giật.

## Review Focus
1. Dán nội dung copy từ Word (style `mso-*`, `<o:p>`, bảng lồng) → chia tờ vẫn khớp bản in, không phá vùng khoá; style lạ không làm lệch (Task 4 thêm ca).
2. Undo / redo qua các lần chèn khoảng trống hiển thị → khoảng trống không vào lịch sử undo, không vào dữ liệu lưu (Task 4).
3. Lời văn cũ có `<div style="page-break-after: always">` hoặc biến không có trong bảng giá trị → hiện nguyên chữ `{{X}}`, không mất, lưu lại y nguyên (Task 3, Task 4).
4. Gõ tiếp trong lúc lượt chia tờ trước đang chạy → lượt mới nhất thắng, con trỏ không nhảy, không chèn khoảng trống theo kết quả cũ (Task 4).
5. HĐ ẩn giá → API biến trả 403 như `print-data`; trang soạn hiện biến dạng tên `{{X}}` + dòng báo "Không hiện được dữ liệu thật vì HĐ ẩn giá; chỗ ngắt chỉ gần đúng", vẫn soạn được (Task 2, Task 5).

---

### Task 0: Chốt cách lưu dàn trang (design 5.6) — HỎI USER, không code
- [x] Hỏi user (07/11: chọn **(a)**): (a) **đề xuất** — cỡ chữ / giãn dòng / ngắt trang nằm trong `template`; cờ Pháp chế so theo chữ (Task 3), không migration; (b) lưu lớp dàn trang riêng (migration, bản in áp lớp). Ghi quyết định vào design 5.6.
- [x] Không áp dụng (đã chọn a).

### Task 1: Quy tắc in mới — đoạn (cụm `<br>`) không cắt đôi + ngắt tay
**Files:** Modify `hrm-client/utils/print/pagedContract.js` (`prepareContent`, `PAGE_CSS`, `localRulesCss`). Test: `HRM/e2e/tests/assign/contracts-approval-flow.spec.ts` (ca mới F41) + đo Playwright MCP.
**Produces:** `paginateContract(html)` giữ chữ ký hàm; trong bản sao: mỗi cụm dòng giữa các `<br>` của khối lá được bọc tạm `<span class="hd-line" style="display:block; break-inside:avoid">`; cụm cao > nửa trang (`TALL_LINE_LIMIT = 516` px = 1032/2) không bọc `avoid`. `<div style="page-break-after: always">` và phần tử `.hd-pb` ⇒ ngắt trang (đổi sang `.pb` cho phần tử ngay sau).
- [ ] Viết ca F41 (mẫu giả): 1 khối 40 cụm `<br>` vắt cuối trang ⇒ không cụm nào bị cắt ngang (mỗi `.hd-line` nằm trọn 1 tờ); khoảng trắng cuối tờ ≤ chiều cao 1 cụm; toàn văn không mất / lặp (dùng lại phép so F27); cụm cao > 516px vẫn cắt; `<div style="page-break-after: always">` sang tờ mới.
- [ ] Đo trước trên HĐ 734 + 3443: số tờ, vị trí ngắt (ghi số).
- [ ] Làm `prepareContent` bọc cụm + quy tắc CSS; giữ `findOrphanHeading`, `splitTallRows`, `markSignatureSpace` như cũ.
- [ ] Đo lại HĐ 734 / 3443: không trang nào bắt đầu giữa cụm dòng; ghi số tờ mới (báo user nếu đổi). Chạy F27–F30 bằng config tạm (khi user cho chạy e2e).

### Task 2: API giá trị biến cho trang soạn
**Files:** Modify `hrm-api/Modules/Assign/Services/ContractPrintService.php`, `Http/Controllers/Api/V1/ContractController.php`, `Routes/api.php`. Test: Create `hrm-api/Modules/Assign/Tests/Feature/ContractPrintVariablesTest.php`.
**Produces:** `ContractPrintService::contractVariableValues(Contract $c): array` (`['TEN_BIEN' => html]`, đúng bộ `render()` dùng cho `MODE_CONTRACT`, chưa escape `$`); `GET /api/v1/assign/contracts/{id}/print-variables` → `{data: {variables: {...}}}`; quyền như `printData` (`findViewableContract`; `hide_price` ⇒ 403 cùng câu).
- [ ] Test `test_bien_trung_voi_ban_in`: với HĐ dựng trong test, `fillReport(template, variables)` == `render(..., MODE_CONTRACT)['template']`.
- [ ] Test `test_an_gia_403`, `test_khong_xem_duoc_hd_403_404`, `test_bang_hang_hoa_co_trong_bien` (`CHI_TIET_HOP_DONG_HANG_HOA_THIET_BI` chứa tên hàng của HĐ).
- [ ] Làm cho xanh; tách phần dựng `$data` của `render()` ra method dùng chung (không đổi kết quả `render`). Chạy cả `ContractPrint*` test cũ.

### Task 3: Cờ Pháp chế theo chữ (dàn trang không bật cờ) — chỉ chạy nếu Task 0 = (a)
**Files:** Modify `hrm-api/Modules/Assign/Services/ContractService.php` (`resolveTemplateFields`). Test: Create `hrm-api/Modules/Assign/Tests/Feature/ContractTemplateLayoutFlagTest.php`.
**Consumes:** `ContractTemplateDiffService::tokenize(?string): array` (so mảng `w`).
**Produces:** luật mới của `resolveTemplateFields`: cờ 0 + `template` gửi lên có cùng dãy từ với `template_original` ⇒ **nhận** `template` (giữ định dạng), cờ giữ 0; khác chữ mà cờ 0 ⇒ bật cờ 1 + ghi lịch sử như "Sửa mẫu in" (không lách được Pháp chế); các nhánh cũ giữ nguyên.
- [ ] Test: đổi `font-size` / `line-height` / thêm `<div class="hd-pb"></div>` ⇒ lưu đúng HTML mới, cờ 0; đổi 1 từ ⇒ cờ 1 + lịch sử; còn ý kiến chưa Đạt ⇒ cờ 1 như cũ; "Khôi phục mẫu gốc" như cũ.
- [ ] Làm cho xanh; chạy lại `ContractLegalNoteTest`, `ContractApproveGuardsTest`, test lưu HĐ hiện có.

### Task 4: Component trang soạn theo tờ
**Files:** Create `hrm-client/components/print/ContractPageEditor.vue`, `hrm-client/utils/print/pageEditorLayout.js`, `hrm-client/static/ckeditor/plugins/hdvar/plugin.js`. Modify `plugins/ckeditor-print.js` nếu cần hàm nạp inline.
**Consumes:** `paginateContract`, `contentCss`, `loadPagedJs` (Task 1); biến từ Task 2.
**Produces:**
- `<ContractPageEditor :value="html" :variables="map|null" :text-locked="bool" :notes="[]" @input="html" @paged="{pageCount}" @blocked-text-edit />`
- `pageEditorLayout.js`: `tagBlocks(root): void` (gắn `data-ed`), `pageStarts(sheets): Array<{ed: string, tag: string, midLine: bool}>`, `applySheetGaps(root, starts): void`, `clearSheetGaps(root): void`, `cleanData(html): string` (bỏ `data-ed`, khoảng trống, thead bản sao, đánh dấu ý kiến).
- Plugin `hdvar`: `{{X}}` ⇒ widget khoá (`span`/`div` `contenteditable=false`, `data-var="X"`, nội dung = `variables[X]`, không có giá trị thì hiện chữ `{{X}}`); `getData()` ⇒ trả lại `{{X}}`.
- [ ] Đo trước (bản thử 07/11): dòng thead bảng hàng hoá 32px ở vùng soạn vs 20px bản in — tìm quy tắc CSS khác nhau, ghi lại.
- [ ] Viết ca Playwright MCP (rồi chép thành e2e F42): HĐ 3443 — mỗi tờ trên trang soạn có **cùng khối đầu / cuối** với tờ tương ứng của tab Bản in, chênh vị trí ≤ 1px; `getData()` không chứa `data-ed`/khoảng trống/`hd-var`, biến là `{{X}}`; gõ / xoá / dán / Ctrl+A rồi gõ không đổi được nội dung widget; undo không mang khoảng trống; gõ liên tục 2 lần trong lúc đang chia ⇒ chỉ lượt cuối được áp, con trỏ giữ vị trí; dán HTML có `mso-*` vẫn khớp; biến lạ hiện `{{X}}`.
- [ ] Làm component: CKEditor `inline` (`allowedContent: true`, `enterMode: ENTER_DIV`, toolbar đủ cỡ chữ, `lineheight`, bảng, nút ngắt trang chèn `<div class="hd-pb"></div>`), debounce 300ms, chạy nền, lượt mới huỷ lượt cũ (`runId` như `ContractPagedView`), dấu "đang cập nhật"; trang bắt đầu giữa cụm dòng (`midLine`, cụm > 516px) ⇒ vẽ vạch ngắt ngang + "Trang x" thay vì tách tờ; zoom và "Trang x/y" dùng lại `ContractPagedToolbar`; thead bản sao chỉ xem ở đầu tờ có bảng tách.
- [ ] `text-locked=true`: mọi thay đổi đổi dãy từ (so như `tokenize` phía FE) ⇒ `undo` ngay + emit `blocked-text-edit`; thay đổi chỉ định dạng / ngắt trang được giữ.
- [ ] Đo tốc độ: HĐ 3443 và HĐ 32 trang dựng trong bộ nhớ đạt mục tiêu ở Global Constraints.

### Task 5: Gắn vào tab Mẫu in
**Files:** Modify `hrm-client/pages/assign/contracts/_id/edit.vue` (khối ~565–630 + data/methods liên quan).
**Consumes:** `ContractPageEditor` (Task 4), `GET /print-variables` (Task 2), luật cờ (Task 3).
- [ ] Tab con "Mẫu in hợp đồng": thay cả `CompactReviewEditor` lẫn `.print-tpl-view` bằng `ContractPageEditor`; `text-locked = !form.need_legal_approval`; `blocked-text-edit` ⇒ toast "Bấm Sửa mẫu in để sửa lời văn"; "Sửa mẫu in" chỉ mở khoá chữ (xác nhận + cờ như cũ); "Xem thay đổi", "Khôi phục mẫu gốc" giữ nguyên. Tab "Mẫu in phụ lục hàng hoá" giữ `CompactReviewEditor`.
- [ ] Biến: gọi `print-variables` khi mở tab; dữ liệu theo **bản đã lưu**; tab Chi tiết đang có thay đổi chưa lưu ⇒ dòng nhắc "Lưu nháp để cập nhật bảng hàng hoá trên trang soạn" (phương án dự phòng design 5.3 — báo user khi review nếu muốn theo form chưa lưu). Ẩn giá ⇒ Review Focus 5.
- [ ] Playwright MCP trên HĐ 3443 (chặn mọi lệnh ghi trừ Lưu nháp có chủ đích, không bấm Gửi duyệt): đổi cỡ chữ 1 đoạn + chèn ngắt trang ⇒ Lưu nháp ⇒ cờ Pháp chế vẫn tắt, tab Bản in ở màn Duyệt ngắt đúng như trang soạn; bấm Sửa mẫu in, đổi 1 từ ⇒ lưu ⇒ cờ bật; cảnh báo "chưa lưu" khi rời trang vẫn chạy.

### Task 6: Ý kiến Pháp chế trên trang soạn
**Files:** Modify `ContractPageEditor.vue`, `edit.vue`; dùng lại `utils/print/legalNoteAnchor.js` (`applyMarks(root, notes)`, `clearMarks(root)`, `findAnchor`), `pages/assign/contracts/components/approval/LegalNotesPanel.vue` (prop `contract`).
- [ ] Ca Playwright MCP (rồi e2e F43, giả lập `legal-notes`): 2 ý kiến ghim hiện tô + số trên tờ và ở cột ý kiến; gõ / chia lại tờ ⇒ ghim lại đúng; sửa đoạn đã ghim ⇒ "Đoạn đã thay đổi" + chữ gốc; `getData()` không chứa đánh dấu.
- [ ] Làm: sau mỗi lượt chia ⇒ `clearMarks` + `applyMarks` trên vùng soạn; cột ý kiến dùng `LegalNotesPanel` nếu chạy được với dữ liệu form Sửa — thao tác "Đã sửa" ở đây; nếu panel phụ thuộc màn Duyệt quá nhiều ⇒ chỉ xem + link "Mở màn Duyệt", ghi lý do vào checkpoint.

### Task 7 (nên có): Độ rộng cột bảng hàng hoá — HỎI USER migration trước
- [x] Migration `2026_11_08_000001_add_print_col_widths_to_hrm_contracts_table` (hrm_contracts.print_col_widths JSON nullable) — đã chạy lẻ `--path` vào DB local `hrm_erp_rbac_rehearsal` 08/11. **Deploy: chạy migration này trên prod TRƯỚC khi deploy code hrm-api** (Lập HĐ luôn ghi cột này).
- [x] User chốt 08/11: 1 bộ độ rộng cho cả HĐ (mọi bảng 8 cột của bản in HĐ: tổng hợp, từng nhóm, Chi phí, Tổng; phụ lục / biên bản giữ cũ); chỉnh bằng kéo mép cột.
- [x] BE: `ContractPrintService::goodsTableOpen()` (class `hd-goods` + `<colgroup>` 8 cột, ô Tên chia đôi, `table-layout: fixed`; null ⇒ như cũ), `normalizeColWidths()`; request Store/Update: 7 số, 3–80%, tổng 100 ± 0,5; update chỉ đổi khi payload có khoá; không đụng cờ Pháp chế. Test `ContractPrintColWidthsTest` (12).
- [x] FE: `utils/print/goodsColWidths.js` (khớp chuỗi BE); edit.vue `editorVariables` áp độ rộng đang kéo vào giá trị biến; ContractPageEditor kéo mép ô tiêu đề (↔, vạch + chú thích %, tối thiểu 3%, Esc huỷ) + nút "Độ rộng cột mặc định". E2E F46.
- Kiểm 08/11: Playwright kéo thật HĐ 3443 ⇒ trang soạn 5 tờ = Xem bản in 5 tờ = popup In màn Chi tiết (sau Lưu nháp) 5 tờ, độ rộng cột trùng ≤ 0,1%; print-data group=0/1 có colgroup; Lưu nháp cờ Pháp chế 0; đã trả 3443 về null. PHPUnit 8 bộ HĐ xanh.

### Task 8: E2E + review cuối
- [ ] Cập nhật spec (F41–F43, ca tab Mẫu in cũ nếu có) — chạy cả bộ `contracts-approval-flow` khi user cho, `--workers=1`, config tạm, lưới chặn ghi.
- [x] E2E cả bộ `contracts-approval-flow` 52/52 xanh (08/11, sau Task 7).
- [x] Review toàn nhánh (reviewer mới, 08/11): Approved with fixes. Đã sửa (user chọn cả 4): ghi chú deploy (migration TRƯỚC code hrm-api); kẹp cả 7 cột 3–80% (`fitColWidths`) + nhả chuột ngoài cửa sổ / chuyển cửa sổ kết thúc lần kéo; đổi mốc `hd-goods` ⇒ `hd-print-goods` (trùng bảng UI form); chuỗi % BE bằng sprintf (không phụ thuộc ini precision; so 19.400 giá trị PHP = JS); `ContractService::fillPrintColWidths` + test luồng sửa. PHPUnit ColWidths 14, LayoutFlag 36, ApproveGuards 63, LegalNote 55, PrintVariables 6; e2e F42–F46 11/11.
- [x] ~~Dọn HĐ test 3443 + báo giá 546~~ — user chốt 08/11: GIỮ LẠI (e2e F40–F46 dùng HĐ này) (CHỈ bảng hrm_* + quotations 546; `account_details` / `assign_task_progress` / `bill_adjust_dept_details` có contract_id=3443 là của HĐ ERP khác từ 2025 — KHÔNG xoá).


### Checkpoint — 2026-11-08 (Phase 27 Task 1–6 xong, CHƯA commit)
Nhánh `gop_db-soan-theo-trang` (api tách b48aed273, client tách 3ee34942c), worktree wt-hop-dong-ban. Task 1–6 qua review từng task + review toàn nhánh + 1 đợt sửa cuối. Sổ SDD: scratchpad `sdd-phase27/progress.md`.
User chốt thêm 08/11: cỡ chữ = class `hd-fs-9..16`; HĐ cũ chưa có bản chụp ⇒ lần lưu đầu chụp lời văn hiện tại.
Đã kiểm: PHPUnit LayoutFlag 32, LegalNote 55, ApproveGuards 63, PrintVariables 6 xanh; Playwright: màn Duyệt 734 không đổi (5 tờ, 17.138 ký tự); trang soạn 3443 5 tờ = bản in; Lưu nháp thật: dàn trang cờ 0, đổi chữ cờ 1.
Đã sửa 08/11 (user "làm 1 + 2"): (a) thẻ rỗng theo danh sách cho phép; (b) nhãn Trang k/N luôn hiện (re-review đạt, Claude chụp xác nhận). (c) user chọn lưu lại mẫu 62/85/86 ở màn danh mục khi deploy (design mục 9) — HĐ đã chụp mẫu cũ vẫn có thể bật cờ khi chỉ dàn trang.
E2E `contracts-approval-flow` 45/45 xanh (08/11, worktree 3060/8060, `--workers=1`, không provision). Trong lúc chạy lộ và đã sửa: chữ nhập không qua phím (bộ gõ tiếng Việt) gộp bước hoàn tác + Ctrl+Y hỏng (saveUndoStep); F42 test sai thứ tự bước.
Còn mở: ContractHthtStepFlowTest 5 lỗi + 1 đỏ do đã gỡ role tạm (test phụ thuộc DB); chưa thử bộ gõ thật macOS (mới CDP/insertText).
Bước tiếp theo: commit khi user báo; deploy nhớ lưu lại mẫu 62/85/86 (design mục 9).

### Checkpoint — 2026-11-08 (Phase 27 Task 1–8 xong, đã commit: api 4dc9ac027 + c773e4506, client 00f5275df + 281d97028; CHƯA push)
Vừa hoàn thành: Task 7 (độ rộng cột bảng hàng hoá) + review toàn nhánh + 4 điểm sửa sau review.
Đang làm dở: không.
Bước tiếp theo: push / merge nhánh gop_db-soan-theo-trang về gop_db khi user báo (merge phải pull RBAC trước); deploy: migration 2026_11_08_000001 TRƯỚC code hrm-api, lưu lại mẫu 62/85/86 (design mục 9).
Blocked:

### Checkpoint — 2026-11-08 (đã merge + PUSH origin/gop_db: api 7ee51d6a5..063399d9d, client 2a4b888ff..a4352e863)
Vừa hoàn thành: merge origin/gop_db vào gop_db-soan-theo-trang (api 063399d9d, client a4352e863) rồi fast-forward gop_db ở checkout chính
HRM/hrm-api + HRM/hrm-client (việc dở meeting của session khác ở checkout chính giữ nguyên: api 12 file, client 6 file).
gop_db giờ mang cả HĐ bán Phase 24–27 (16 commit api, 18 commit client chưa từng lên gop_db).
Xung đột Catalog quyền: "Hạch toán dịch vụ HĐBH" + 4 tên "QT thưởng năng suất quý" theo mã riêng của gop_db, bỏ bí danh trùng
từ 881fe0b7b. Kiểm: 940 mã / 0 bí danh trùng, catalog-sync --dry-run exit 0; PHPUnit HĐ (202) + ServiceAccounting (42) xanh.
Deploy gop_db cần 7 migration (chạy TRƯỚC code hrm-api): 2026_10_27_000001 list_indexes · 2026_10_28_000001 print_template_columns ·
2026_11_02_000001 legal_approval · 2026_11_03_000001 approval_flow · 2026_11_06_000001 service_accounting_flags (database/migrations) ·
Modules/Assign 2026_11_06_000001 contract_legal_notes · 2026_11_08_000001 print_col_widths. + lưu lại mẫu 62/85/86; catalog-sync.
Vấn đề ngoài luồng (CÓ SẴN trên origin/gop_db, không do merge, chưa sửa): DivisionMarketDepartment(.Employee) gọi
self::currentEmployeeIsSuperAdmin(), AssignOtherRequestService gọi WarrantyRepairPermission::isSuperAdmin() — cả 2 hàm không tồn tại
(rbac đã gỡ) ⇒ 500 khi chạy tới; tests/Unit/Rbac RawPermissionLookupGuardTest đỏ vì đúng các chỗ này.
Đã sửa 08/11 (user giao): 500 super admin ở DivisionMarket / AssignOtherRequest — commit a496f5e71 (nhánh gop_db-fix-super-admin-500), đã push origin/gop_db (063399d9d..a496f5e71). tests/Unit/Rbac 13/13. tests/Feature/Rbac lỗi sẵn trên DB rehearsal (role_has_permissions thiếu company_id), không liên quan.
Bước tiếp theo: deploy theo các bước trên khi user báo.
Blocked:


## Phase 28 — Tab Mẫu in màn Chi tiết HĐ hiện dạng xem trước bản in (08/11/2026, user "làm")
Phạm vi: chỉ hrm-client, nhánh `gop_db` checkout chính; không BE / migration / DB; không commit.
User chốt 08/11: (1) phụ lục cũng chia tờ A4 như HĐ — popup In phụ lục đổi theo; (2) phụ lục có ô chọn mẫu 1 / mẫu 2;
(3) HĐ ẩn giá ⇒ tab chỉ hiện câu 403 của BE. Bản HĐ dùng bảng Tổng hợp (không gửi `group`) như tab Bản in màn Duyệt.
- [x] 28.1 `pages/assign/contracts/_id/index.vue`: tab Mẫu in bỏ `.print-tpl-view` thô ⇒ `ContractPagedView` theo `print-data`
  (mode `contract` / `product_annex_1` / `product_annex_2`), mở tab lần đầu mới tải, mỗi bản tải 1 lần (v-show giữ tờ);
  thanh `ContractPagedToolbar` ở hàng tab; ô gạt mẫu 1/2 khi đang ở phụ lục; lỗi 403/422 hiện trong tab (header
  `X-Silent-Errors`, không toast; 401 vẫn về login qua `handleError`).
- [x] 28.2 `contractPrintMixin.js`: popup In phụ lục mẫu 1/2 cũng chia tờ (`paged` cho `product_annex_*`).
- [x] 28.3 Playwright MCP: tab = popup In (số tờ, chữ đầu/cuối từng tờ), toàn văn không mất; ca ẩn giá (403) và chưa có mẫu phụ lục (422) giả lập; 0 toast, 0 lỗi console.
- [x] 28.4 Spec e2e (ngoài git) thêm ca tab Mẫu in — không tự chạy.
- [x] 28.5 (user "làm" thêm 08/11) `utils/print/pagedContract.js` `hideTrailingBlanks`: khối cuối không chữ/ảnh/bảng (bỏ qua chữ trong
  `<style>`) ⇒ class `hd-tail-blank` (display:none) ở bản sao lúc chia — mẫu phụ lục ERP kết thúc bằng `<div><span 24px><style>` đẻ tờ trắng
  (HĐ 3443 mẫu 2: 2 tờ ⇒ 1). `<style>` vẫn áp dụng (viền bảng giữ 1px solid).
- [x] 28.6 (user "làm" thêm 08/11) `ContractPagedView` prop `fitAnchor` (selector hàng tab): khung cao = cửa sổ − (header + 8 + khoảng hàng tab→khung) − 66;
  không truyền thì như cũ. Ô Mẫu 1 / Mẫu 2 chuyển xuống dòng đầu khung (ở hàng tab tràn 59px), nhãn "Mẫu 1 - Theo nhóm" / "Mẫu 2 - Tổng hợp".

### Checkpoint — 2026-11-08 (Phase 28 xong, CHƯA commit)
Vừa hoàn thành: 28.1–28.6 trên checkout chính `HRM/hrm-client` nhánh `gop_db` (5 file: `pages/assign/contracts/_id/index.vue`,
`components/contractPrintMixin.js`, `components/contract-form.scss`, `components/print/ContractPagedView.vue`, `utils/print/pagedContract.js`).
Kiểm (Playwright script Node 20, áp tạm patch vào worktree wt-hop-dong-ban 3060/8060 DB rehearsal — đã trả worktree sạch; DB `db_gop_6_11` của :8000
chưa có cột mẫu in / 0 HĐ nên không đo ở đó): HĐ 3443 + 734 — tab = popup In cả 3 bản (số tờ + chữ đầu/cuối từng tờ + tổng ký tự); chưa mở tab 0
request, 3 bản 3 request, quay lại không tải; khung đáy 834 = 900 − 66; hàng tab không tràn; giả lập 403/422 ⇒ câu BE trong tab, 0 toast;
hồi quy: màn Duyệt 734 5 tờ 17.138 ký tự, khung không đổi; trang soạn 3443 5 tờ. Phụ lục mẫu 1 HĐ 3443 tờ 2 chỉ có khối ký = đúng luật giữ khối ký.
E2E: sửa F30 (phụ lục chia tờ), thêm F47 + F47b. Chạy 08/11 (user "chạy luôn", worktree 3060/8060 áp tạm patch, config tạm
scratchpad `pw3060.config.ts`, --workers=1, không provision): F30 / F47 / F47b xanh; bỏ F42 ⇒ 51 xanh; F42, F45c, F46 ĐỎ — đỏ y hệt
trên code gốc worktree (a4352e863, đã trả sạch) ⇒ không do Phase 28. Nghi do dữ liệu: HĐ 3443 bị sửa 08/11 16:09 bởi NV13
(need_legal_approval = 1, print_col_widths = [5.59, 56.88, …] — checkpoint Phase 27 đã trả về null / cờ 0). Chưa lần hết F45c.
Worktree đã trả sạch (0 file đổi).
Đã commit + PUSH 08/11: hrm-client `6de64b621` lên origin/gop_db (dda38e17a..6de64b621, chỉ đẩy đúng commit này — commit f3055c8e1
Nhiệm vụ v2 của phiên khác nằm trên, KHÔNG đẩy). Spec e2e ngoài git.
08/11 (user "có"): đưa HĐ 3443 về fixture bằng UPDATE thẳng (need_legal_approval 1→0, print_col_widths →null; trước đó bị sửa 16:09)
⇒ F42/F45c/F46 xanh; chạy lại cả bộ `contracts-approval-flow` **54/54 passed** (6.2m, worktree áp tạm patch, đã trả sạch). Kết luận: 3 ca đỏ do dữ liệu HĐ 3443 lệch, không do code.
Bước tiếp theo: không còn việc mở của Phase 28. Lưu ý: ai thử tay trên HĐ 3443 (Lưu nháp sau Sửa mẫu in / kéo cột) sẽ làm F42/F45c/F46 đỏ lại.
Blocked:
- 08/11 (user chọn): worktree wt-hop-dong-ban/hrm-client fast-forward `gop_db-soan-theo-trang` → origin/gop_db `6de64b621` (2 commit: Phase 28 +
  meeting dda38e17a), không push. 3060 HĐ 3443: tab Mẫu in 5 / 2 / 1 tờ, khớp popup In, 0 lỗi. hrm-api worktree không đổi.

## Phase 29 — Logic xuất hàng cha / con theo HĐ (08/11/2026 — KHẢO SÁT, chưa code)
Yêu cầu user 08/11: (1) xuất hàng cha đi như bình thường; (2) xuất hàng con KHÔNG hạch toán công nợ 131x mà Nợ 1541 / Có 156;
(3) đủ SL hàng con ⇒ tự tạo phiếu nhập kho kế toán hàng cha (Nợ 156 / Có 1541) ⇒ tự tạo phiếu xuất bán hàng cha (Nợ 632 / Có 156);
(4) lưu được hàng con xuất cho DÒNG cha nào (HĐ có 2 dòng cha trùng mã).

Hiện trạng (đọc code hrm-api gop_db 08/11; DB local 0 phiếu loại 20/21 ⇒ chưa đối chiếu dữ liệu):
| Ý | Code hiện tại | Đúng yêu cầu? |
|---|---|---|
| 1 Xuất cha (loại 21) | `ProductExportPostingService` đủ 8 cụm (doanh thu Nợ 1311/Có 5111+33311 …), giá vốn **Nợ 632 / Có 155** (`costAccounting(..., 155)`, dòng 346) — kể cả hàng cha mua sẵn nằm ở 1561 | Lệch TK: 155 ≠ 156 |
| 2 Xuất con (loại 20) | `costAccountingProduction`: chỉ **Nợ 1541 / Có 1561**, không 131 | ĐÚNG |
| 3a Nhập cha | `ContractParentImportService::createParentImport` chạy ngay khi MỖI PXH loại 20 hoàn tất; số bộ = min(xuất/định mức) CHỈ qua các con CÓ trong phiếu đó (con chưa xuất bị bỏ qua), không cộng dồn các phiếu trước, không làm tròn xuống (ra bộ lẻ); hạch toán **Nợ 155 / Có 1541** | Sai điều kiện "đủ" + lệch TK 155 |
| 3b Xuất bán cha tự động | KHÔNG có — user tự lập YCXH loại 21 | Thiếu |
| 4 Con thuộc dòng cha nào | YCXH lưu `contract_product_id` ở tab_products; nhưng `product_export_request_details` → ĐNXK → PXK → PXH chỉ có `product_id`; nhập cha tra `ContractProductPrice where erp_product_id ->first()` ⇒ 2 dòng cha trùng mã / con trùng mã ⇒ gán nhầm dòng đầu | Thiếu |

Thiết kế: `design-phase29-xuat-hang-cha-con.md` — user chốt 08/11: Q1 TK hàng cha 1561 mọi trường hợp (bỏ 155) · Q2 phiếu xuất bán cha tự
động đủ 8 cụm · Q3 đủ bộ nào làm bộ đó (cộng dồn, làm tròn xuống) · Q4 thêm cột dòng HĐ xuyên chuỗi chi tiết YCXH→ĐNXK→PXK→PXH · Q5 chỉ sinh PXH loại 21 Hoàn tất.

### Checkpoint — 2026-11-08 (Phase 29 thiết kế)
Vừa hoàn thành: khảo sát code + 5 câu chốt + tài liệu thiết kế (mục 2 = điểm Claude tự chọn, chờ user duyệt).
Đang làm dở: không.
Cập nhật 08/11: user duyệt mục 2; đổi hạch toán (design mục 1b): con Nợ 1541/Có 1561 (sửa lại từ 156) · nhập cha Nợ 155/Có 1541 · xuất cha tự động
Có 155 · loại 21 lập tay (cha mua sẵn) Có 1561.
Bước tiếp theo: viết plan task Phase 29 → hỏi "làm" + phạm vi (liệt kê migration) trước khi code.
Blocked:

# Phase 29 — Implementation Plan (08/11/2026, CHƯA code)

**Goal:** Xuất con (loại 20) cộng dồn theo DÒNG cha ⇒ đủ bộ nào tự nhập cha (Nợ 155/Có 1541) + tự xuất bán cha (PXH loại 21, 8 cụm, Có 155); TK theo design mục 1b.
**Spec:** `design-phase29-xuat-hang-cha-con.md`. Repo: hrm-api (chính) + hrm-client (hiển thị nhỏ), nhánh hỏi user (đề xuất nhánh mới từ `gop_db`).

Chuỗi bảng chi tiết (rehearsal 08/11): YCXH `product_export_request_details` (tab_products ĐÃ có `contract_product_id`) → ĐNXK
`warehouse_export_request_details` → PXK `warehouse_export_lots` → PXH `product_export_details` (đã có `product_export_request_detail_id`,
`lot_id`). Khuôn ERP: mỗi loại HĐ 1 cột dòng riêng chép xuyên 4 bảng (`firm_contract_tab_product_id`, `project_contract_tab_product_id`).

### Task 0: Khảo sát còn thiếu — KHÔNG code — XONG 08/11 (kết quả ngay dưới)
**Kết quả 08/11 (đọc code, chưa chạy dữ liệu):**
- Chép dòng HRM: YCXH→ĐNXK `WarehouseExportRequestService::buildDetailAttributes` (danh sách cột pass-through cố định, đã có
  `firm_contract_tab_product_id`/`project_contract_tab_product_id` ⇒ thêm cột mới vào đây); ĐNXK→lô PXK `WarehouseExportService::buildTmpLots`
  + rebuild (:346) cũng pass-through cột; PXK→PXH `ProductExportService` :231 + xuất thẳng YCXH→PXH :583 (đã ghi `product_export_request_detail_id`).
- **Lỗi gom theo mã hàng** (phải sửa cùng Task 2): chọn dòng ĐNXK (`collectSelectedLines` key `product_id`), khớp lô PXK (`matchLotPayload`
  theo product_id+unit_id), PXH (`priceMap`/`inputByProduct` keyBy product_id) ⇒ 1 phiếu có 2 dòng cùng mã (con cùng mã dưới 2 dòng cha) bị
  gộp / lấy giá dòng đầu. Tiền lệ sửa: loại 15 khớp theo id dòng chi tiết YCXH (`product_export_request_detail_id`) — áp cho 20/21.
- ERP: PXK loại 20/21 HIỆN LẬP ĐƯỢC trên ERP (chỉ bước PXH mới chuyển sang HRM — WarehouseExportsController :164). 3 lối vào: nút "Tạo phiếu
  xuất kho" ở danh sách ĐNXK (WarehouseExportRequestsController :136), nút ở màn xem ĐNXK (warehouse_export_requests/show.blade.php :697),
  màn Tạo mới PXK có ô tìm ĐNXK (`warehouseExportRequest.searchData`); BE `WarehouseExportsController@store` (:279) / `update` (:707).
  HRM đã có màn PXK `/finance/warehouse-exports/create` ⇒ Task 7 = ERP trỏ link sang HRM (khuôn PXH :164) + lọc ĐNXK 20/21 khỏi searchData +
  chặn store/update 422. Kiểm thêm: PXK 20/21 đã lập trên ERP ở prod, ĐNXK gộp (JoinExportRequests), điều chuyển kho từ ĐNXK 20/21.
- Hoá đơn: không thấy luồng hoá đơn VAT đọc PXH loại 21; ERP quyết toán hoa hồng tháng/quý đọc product_exports ⇒ phiếu tự động tính như loại 21 tay (kiểm khi làm).
- `Contract::hasLinesLeftToRequest` chỉ đếm SL trên YCXH (tab_products theo dòng) ⇒ phải cộng SL cha xuất tự động.
- Đếm bộ đã nhập: cộng `product_import_details.hrm_contract_product_id` (dòng cha) của phiếu nhập cha ⇒ không cần bảng mới.
- [x] PXK của YCXH 20/21 có lập được trên ERP không (lệnh quét bù nói "PXK làm trên ERP")? Nếu có: ERP không chép cột mới ⇒ PXH phải lấy dòng HĐ qua `product_export_details.product_export_request_detail_id` → YCXH detail (kiểm cột này có được điền ở luồng HRM).
- [x] Đọc nơi tạo dòng ĐNXK từ YCXH, dòng lô PXK từ ĐNXK (HRM `WarehouseExportService::rebuildLots` ~:346), dòng PXH (`ProductExportService` :231/:583).
- [x] Luồng hoá đơn / yêu cầu thu tiền đọc PXH loại 21 thế nào (phiếu tự động có lọt vào không).
- [x] Tên cột: `hrm_contract_product_id` (theo khuôn ERP, tránh trùng nghĩa `contract_product_id` của tab_products) — chốt khi hỏi phạm vi.

### Task 1: Migration cột dòng HĐ (HỎI USER, liệt kê file + DB trước khi chạy)
- [x] 1 migration: thêm `hrm_contract_product_id` unsignedBigInteger nullable + index vào `product_export_request_details`, `warehouse_export_request_details`, `warehouse_export_lots`, `product_export_details`, `product_import_details`. `--pretend` trước, chạy lẻ `--path`.

### Task 2: Chép dòng HĐ xuyên chuỗi
- [x] YCXH `writeContractLines`: ghi cột vào details. ĐNXK / PXK lô / PXH: chép từ dòng nguồn. Fallback theo Task 0.
- [x] PHPUnit: 2 dòng cha trùng mã, con trùng mã ⇒ PXH mỗi dòng mang đúng id dòng HĐ.

### Task 3: TK hạch toán (design 1b)
- [x] Loại 20: GIỮ Nợ 1541 / Có 1561 (user sửa lại 08/11, bỏ chốt 156). Loại 21 lập tay: `costAccounting(..., 155)` ⇒ 1561. Nhập cha giữ Nợ 155/Có 1541. Xuất cha tự động Có 155.
- [x] PHPUnit: mỗi phiếu tổng Nợ = tổng Có; đúng số hiệu TK từng vế.

### Task 4: Nhập cha theo dòng cha, cộng dồn, đủ bộ
- [x] Viết lại `ContractParentImportService`: nhóm theo dòng cha (`hrm_contract_product_id` của con → `parent_id`), cộng dồn SL + giá vốn con từ MỌI PXH loại 20 Hoàn tất của dòng cha; số bộ = floor(min(xuất/định mức)); bộ mới = số bộ − đã nhập (bảng/ cột theo dõi số bộ đã nhập — chốt ở Task 0); giá vốn = Σ đơn giá bình quân con × SL con dùng; dư nằm 1541. Idempotent theo PXH nguồn.
- [x] PHPUnit: A+B 2 phiếu (phiếu 1 chỉ A ⇒ không nhập); 2 bộ qua 2 phiếu; bộ lẻ không nhập; dư 1541 đúng số; 2 dòng cha trùng mã tách riêng.

### Task 5: Xuất bán cha tự động
- [x] Service mới: sau nhập cha ⇒ tạo PXH loại 21 Hoàn tất (kho kế toán nhập/xuất thẳng, giá từ dòng cha, gắn phiếu nhập nguồn + dòng cha), trừ tồn FIFO lớp vừa nhập, `postAccounting` 8 cụm với giá vốn Có 155. Thiếu HTHT / kho thẳng ⇒ rollback cả lần hoàn tất PXH con, câu báo rõ.
- [x] SL cha xuất tự động tính vào đã xuất ⇒ `hasLinesLeftToRequest` / picker loại 21 trừ đi.
- [x] Giới hạn chung dòng cha (chốt 08/11): YCXH loại 21 + YCXH con quy ra bộ ≤ SL HĐ − loại 21 tay − đã lắp tự động; chặn 422 lúc lập/sửa YCXH. PHPUnit: 1 tay + 3 bộ con ⇒ chặn.
- [x] PHPUnit: 8 cụm đủ, giá vốn = giá vốn nhập cha; rollback khi thiếu HTHT.

### Task 6: FE (nhỏ) + kiểm
- [-] (10/11 user chọn BỎ QUA) Chi tiết PXH / phiếu nhập: hiện dòng cha nguồn + phiếu nguồn.
- [x] Chạy thật trên rehearsal (tinker transaction rollback) HĐ có cha–con: số dư 1541 / 155 / 156 / 632 / 1311 khớp tính tay.

### Task 7: Chặn ERP lập PXK cho YCXH loại 20/21 (user yêu cầu 08/11 — BẮT BUỘC trước prod)
- [x] (GĐ B 08/11, ERP 6b545fc64d) Khảo sát ERP (TanPhatDev, gop_db): màn / API lập PXK từ ĐNXK (`JoinExportRequestsController`, WarehouseExports…) — chặn khi ĐNXK
  thuộc YCXH loại 20/21 (HĐ HRM): ẩn nút + chặn BE 422 câu "Phiếu xuất kho của hợp đồng HRM phải lập trên HRM". Hỏi "làm" + phạm vi ERP.
- [x] (10/11 đánh giá: GIỮ, không sửa code) Bỏ phần quét bù "PXK làm trên ERP" của lệnh `assign:activate-signed-contracts`? — Hook WarehouseExportService::send đã phủ PXK mới (YCXH chỉ lập được khi HĐ Có hiệu lực/Đang thực hiện); quét bù vẫn cần cho PXK lập trên ERP TRƯỚC deploy + làm lưới an toàn; truy vấn rẻ, idempotent.

Khảo sát kho 08/11: design-phase29 mục 5 (R1 không; R2 cao nếu prod đã có PXH loại 20; R3 FIFO trộn lớp kho thẳng; R4 ⇒ Task 7).

### Task 8: Kho kế toán lắp ráp HĐ riêng (chốt R3 08/11)
- [x] Hỏi user (08/11): cờ `accounting_warehouses.is_contract_assembly` (migration) · ô tick màn kho kế toán HRM, kế toán tự tạo kho prod · ẩn ở mọi danh sách chọn kho của ERP + HRM.
- [x] (sửa 08/11) Migration cờ + lệnh artisan idempotent tạo "Kho lắp ráp hợp đồng" (<mã cty>-LRHD) cho mỗi công ty đang hoạt động, chạy lúc deploy. KHÔNG ô tick. Màn kho kế toán HRM (+ ERP ở GĐ B): kho có cờ không sửa cờ / xoá / ngừng hoạt động (BE chặn).
- [x] Rà mọi chỗ lấy danh sách kho kế toán để chọn (ERP + HRM) ⇒ bỏ kho có cờ; liệt kê đủ file khi hỏi phạm vi.
- [x] `ContractParentImportService` + xuất cha tự động dùng kho này; công ty chưa có kho ⇒ chặn hoàn tất PXH con, câu báo rõ.

### Checkpoint — 2026-11-08 (Phase 29 khảo sát kho)
Vừa hoàn thành: khảo sát cấu trúc kho (design-phase29 mục 5), chốt R3 = kho kế toán riêng, thêm Task 7 (chặn ERP lập PXK) + Task 8.
Đang làm dở: không.
Bước tiếp theo: Task 0 (khảo sát còn thiếu, chỉ đọc) → hỏi các câu Task 8 → hỏi "làm" + phạm vi (repo, nhánh, migration) trước khi code.
Blocked:

### Checkpoint — 2026-11-08 (Phase 29 Task 0 xong)
Vừa hoàn thành: Task 0 (kết quả ghi trong Task 0); chốt giới hạn chung theo dòng cha (design mục 5 cuối).
Đang làm dở: không.
Bước tiếp theo: (3 câu Task 8 đã chốt) → hỏi "làm" + phạm vi (repo hrm-api/hrm-client/ERP, nhánh, từng migration + DB).
Blocked: cần đếm trên PROD: PXH loại 20/21 gắn HĐ HRM, PXK loại 20/21 lập trên ERP (user / người có quyền DB prod).

### Checkpoint — 2026-11-08 (Phase 29 GĐ A — BE xong, đang FE)
Nhánh `gop_db-xuat-hang-cha-con` (worktree wt-hop-dong-ban, api tách d80c68dd8, client tách 4b347f17b). User "làm GĐ A" + cho thêm payload 4 màn FE
(PXK tạo/sửa, PXH tạo, Sửa ĐNXK). Đã chạy vào `hrm_erp_rbac_rehearsal`: migration 2026_11_09_000001 (batch 459) + 000002 (batch 460);
`assign:ensure-contract-assembly-warehouses --created-by=13` tạo 6 kho *-LRHD (cty 1,2,3,4,8,9). Deploy prod: truyền --created-by=<id quản trị>.
BE xong (lint sạch, CHƯA test): cột dòng HĐ xuyên chuỗi + khớp theo dòng (ĐNXK contractLineSelection, lô PXK matchLotPayload, PXH lot_id /
product_export_request_detail_id); giới hạn chung dòng cha (`sharedParentRemaining`, Contract::hasLinesLeftToRequest dùng chung);
giá vốn loại 21 theo kho (`costAccountingContractSale`: kho lắp ráp Có 155, khác Có 1561); ContractParentImportService viết lại
(cộng dồn, floor, khoá dòng cha, nhập Nợ155/Có1541 vào kho lắp ráp, xuất bán cha tự động 8 cụm); ẩn kho lắp ráp ở 5 danh sách chọn
(PXH xuất thẳng, StockService xuất thẳng, phiếu nhập thẳng, lọc điều chuyển, kho hàng gửi quy chế); danh mục kho: cờ is_can_* false + 423.
Còn: picker HĐ ở màn YCXH vẫn lọc thô từng dòng (thừa, không sai số). FE + PHPUnit + chạy thật rehearsal.

### Checkpoint — 2026-11-08 (Phase 29 GĐ A xong, CHƯA commit)
Vừa hoàn thành: GĐ A (HRM) — nhánh `gop_db-xuat-hang-cha-con` worktree wt-hop-dong-ban, CHƯA commit.
- hrm-api 18 file + 2 migration + lệnh `assign:ensure-contract-assembly-warehouses` + test `ContractParentAssemblyTest` (6 ca, 40 assertion xanh).
- hrm-client 4 file (payload id dòng): warehouse-export-requests/_id/edit.vue, warehouse-exports/create.vue + _id/edit.vue, product-exports/create.vue.
- Kiểm: tinker rehearsal rollback (3 phiếu con ⇒ nhập 2 + 1 cha, 10tr + 6tr; Nợ155 = Có1541 = Có155 = Nợ632 = 16tr; 5111 30tr; mỗi PXH Nợ = Có;
  kho lắp ráp về 0, stock_id NULL; 2 dòng cha trùng mã tách đúng, giá bán theo dòng; thiếu kho ⇒ 422 câu rõ, 0 phiếu). Sửa 1 lỗi tự phát hiện:
  "còn lại" dòng cha chỉ tính YCXH con ⇒ thêm số cha đã lắp thật. PHPUnit 33 bộ liên quan: 18 bộ đỏ = đỏ y hệt trên code gốc (checkout chính
  d80c68dd8, cùng DB) — lỗi môi trường có sẵn; còn lại xanh. Playwright (script, giả lập 2 dòng cùng mã, chặn ghi): 4 màn gửi đúng id dòng,
  0 lỗi JS; danh mục kho: 6 dòng LRHD chỉ còn Xem + Lịch sử, API Sửa/Xoá/Khoá/Mở khoá 423 (PHPUnit). E2E spec mới
  `HRM/e2e/tests/finance/export-contract-line-payload.spec.ts` X1–X5 — CHƯA chạy.
Còn để lại (báo user): màn Xuất lại PXK (re-export.vue) chưa gửi id dòng (BE chạy như cũ); picker HĐ màn YCXH lọc thô từng dòng (có thể
liệt kê HĐ đã hết phần xuất, BE vẫn chặn lúc gửi); lệnh tạo kho trên prod cần `--created-by=<id quản trị>`.
Bước tiếp theo: user review / test tay → commit khi user báo → hỏi GĐ B (ERP: chặn PXK 20/21, ẩn + khoá kho lắp ráp).
Deploy (ghi lại): migration 2026_11_09_000001 + 000002 TRƯỚC code hrm-api → `assign:ensure-contract-assembly-warehouses --created-by=<id>`
→ GĐ B ERP lên CÙNG đợt (chặn PXK trên ERP trước prod).
Blocked:

### GĐ B (ERP) — khảo sát 08/11 (đọc origin/gop_db; checkout chính ERP kém origin 6, hơn 2 commit)
1. Chặn PXK loại 20/21 trên ERP: (a) nút "Tạo phiếu xuất kho" danh sách ĐNXK (`WarehouseExportRequestsController` :136) + màn xem
   ĐNXK (`warehouse_export_requests/show.blade.php` :697) ⇒ loại 20/21 trỏ màn HRM `/finance/warehouse-exports/create?warehouse_export_request_id=`
   (khuôn nút PXH → HRM ở WarehouseExportsController :164); (b) `WarehouseExportsController@create` mở bằng ĐNXK 20/21 ⇒ chuyển sang HRM;
   `@store` / `@update` / xuất lại PXK 20/21 ⇒ 422 "Phiếu xuất kho của hợp đồng HRM lập trên HRM"; (c) PXK 20/21 đã có trên ERP: nút Sửa / Xuất kho /
   Xuất lại trỏ HRM (`/finance/warehouse-exports/{id}/edit`, `/re-export`).
2. Ẩn kho lắp ráp ở form ERP liệt kê kho nhập/xuất thẳng: product_imports create/edit (nhập thẳng), product_exports create/edit (xuất thẳng),
   `JoinExportRequestsController` :429, `ProductStockService` :51/:128 (tồn kho thẳng). KHÔNG sửa hàm chung `AccountingWarehouse::getForSelect()`
   (màn XEM dùng tra tên kho — loại ở đó thì phiếu xuất bán cha tự động mất tên kho).
3. Danh mục kho kế toán ERP (`AccountingWarehousesController` edit / update / delete + nút ở danh sách): kho cờ ⇒ ẩn nút + chặn BE.

### Checkpoint — 2026-11-08 (Phase 29 GĐ B — ERP xong, CHƯA commit)
Worktree ERP `websites/wt-xuat-hang-cha-con/TanPhatDev`, nhánh `gop_db-xuat-hang-cha-con` tách origin/gop_db `b7d0b352c8` (vendor copy cp -Rc,
.env chép từ checkout chính; chạy kiểm với env DB_DATABASE=hrm_erp_rbac_rehearsal APP_ENV=local HRM_URL_FE=http://127.0.0.1:3060).
13 file: ExportModel (`isHrmContractExportType`, `hrmUrl`), WarehouseExportRequestsController + show.blade (nút Tạo PXK 20/21 → HRM, ẩn điều chuyển
kho cho 20/21), WarehouseExportsController (create/edit/reExport → HRM; store/update/reExportStore success=false trước validate; nút Sửa / Xuất lại
ở danh sách → HRM), AccountingWarehouse (thêm cột is_contract_assembly vào 4 hàm chọn), 4 blade phiếu nhập / xuất hàng (lọc JS kho thẳng bỏ kho
lắp ráp), JoinExportRequestsController + ProductStockService (bỏ kho lắp ráp ở kho thẳng), AccountingWarehousesController (ẩn Sửa/Xoá, chặn
edit/update/delete). Không migration.
Kiểm (tinker transaction rollback, đổi tạm ĐNXK 39058 / PXK sang loại 21): 6 lối PXK 21 ⇒ chuyển HRM / success=false; ĐNXK thường vẫn form ERP;
màn xem + danh sách ĐNXK (thủ kho NV311) loại 21 trỏ HRM; kho lắp ráp: sửa / lưu / xoá bị chặn, không đổi; kho thẳng cty 1 chỉ còn HN-NXT.
Playwright ERP 8097 (phiên NV13): searchData danh mục kho — TPE-LRHD không nút, kho thường Sửa/Xóa. ERP 8097 đã tắt.
Ghi chú: ERP trả lỗi khuôn `success=false` (không HTTP 422) để màn AngularJS hiện câu báo; màn "Tạo mới" PXK chung (chọn ĐNXK trong popup)
chặn ở bước lưu.
Bước tiếp theo: user review → commit khi user báo (3 repo: hrm-api, hrm-client, ERP — cùng nhánh gop_db-xuat-hang-cha-con).
Blocked:

### Checkpoint — 2026-11-08 (Phase 29 — e2e + 2 điểm còn lại, CHƯA commit)
- E2E `export-contract-line-payload` (worktree 3060/8060, --workers=1): X1–X5 5/5 xanh; sau khi thêm X6 (Xuất lại PXK) chạy lại 6/6 xanh.
- (user "làm cả a + b") (a) hrm-client `warehouse-exports/_id/re-export.vue` gửi `warehouse_export_request_detail_id` (BE reExportData đã trả).
  (b) hrm-api `ProductExportRequestPickerService::hrmContracts`: SQL thô làm vòng lọc đầu, lọc lại theo `contractRemainingByLine`
  (giới hạn chung dòng cha) đúng loại 20 / 21, phân trang lại trên tập HĐ của người lập. PHPUnit `ContractParentAssemblyTest` 7/7 (44 assertion,
  ca mới: lập tay đủ cha ⇒ HĐ biến mất ở ô chọn loại 20 + 21); `HrmContractPickerTest` 5 ca / 4 lỗi = y hệt mốc code gốc (môi trường).
Bước tiếp theo: user review / test tay → commit khi user báo (3 repo, nhánh gop_db-xuat-hang-cha-con).
Blocked:

### Checkpoint — 2026-11-09 (Phase 29 đã commit, CHƯA push)
Nhánh `gop_db-xuat-hang-cha-con` (tách origin/gop_db) ở 3 repo: hrm-api `69cab76f9` (worktree wt-hop-dong-ban), hrm-client `bac53f563`
(worktree wt-hop-dong-ban), ERP `6b545fc64d` (worktree wt-xuat-hang-cha-con/TanPhatDev). Spec e2e ngoài git.
Bước tiếp theo: push / merge về gop_db khi user báo; deploy: 2 migration TRƯỚC code hrm-api → `assign:ensure-contract-assembly-warehouses
--created-by=<id quản trị>` → ERP cùng đợt; đếm PXH / PXK loại 20/21 trên prod trước deploy.
Blocked:
- 09/11 (user chọn "push nhánh riêng"): đã PUSH `origin/gop_db-xuat-hang-cha-con` 3 repo (hrm-api 69cab76f9, hrm-client bac53f563,
  ERP 6b545fc64d) — CHƯA merge gop_db. Merge sau: kéo origin/gop_db mới nhất, làm qua worktree (checkout chính có việc dở phiên khác).

### Checkpoint — 2026-11-10 (Phase 29 — đồng bộ gop_db vào nhánh riêng)
- Quét bù trong `assign:activate-signed-contracts`: đánh giá GIỮ (không sửa code). Task 6 hiện dòng cha nguồn: user BỎ QUA.
- User chọn merge NGƯỢC: origin/gop_db → `gop_db-xuat-hang-cha-con` (nhánh dùng cho tester trên VPS), KHÔNG merge vào gop_db.
  Merge sạch, đã push: hrm-api 441cc225e · hrm-client f7e998884 · ERP 374900fc15. php -l sạch, PHPUnit ContractParentAssemblyTest 7/7.
- Deploy VPS nhánh này: migration mới kéo theo từ gop_db — hrm-api `2026_11_06_000001_create_business_target_department_parts_table`,
  ERP `2026_11_06_000001_add_service_quotation_print_template_type` — cùng 2 migration Phase 29 + lệnh tạo kho lắp ráp.

---

# Phase 30 — Tab "Xuất hàng" trên màn xem HĐ — Implementation Plan (10/11/2026, CHƯA code)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development hoặc superpowers:executing-plans. Checkbox `- [ ]`.
> ⚠ CLAUDE.md: CHƯA được phép code. Trước khi bắt tay phải hỏi riêng "làm" + phạm vi (repo · nhánh · file · migration nào chạy DB nào).

**Goal:** Kinh doanh phụ trách HĐ thấy toàn cảnh xuất hàng của HĐ (theo dòng hàng + các đợt xuất) mà không làm chậm lúc mở HĐ.

**Architecture:** 1 service đọc `ContractExportProgressService` gom số theo `hrm_contract_product_id` (vài truy vấn GROUP BY, tái dùng
`ProductExportRequestService::contractRemainingByLine`), 2 endpoint GET dưới `assign/contracts/{id}`; FE 1 component tab tải lười.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Nuxt 2 / Vue 2 (hrm-client), PHPUnit, Playwright.

**Spec:** `.plans/hop-dong/design-phase30-tab-xuat-hang.md` · mockup `mockup-tab-xuat-hang.html`.

**Nhánh đề xuất:** `gop_db-xuat-hang-cha-con` (worktree wt-hop-dong-ban; phụ thuộc cột Phase 29) — hỏi user khi xin "làm".

## Global Constraints
- KHÔNG thêm truy vấn nào vào `GET assign/contracts/{id}` (show). Tab tải lười khi bấm lần đầu.
- "Còn lại" = `remaining_qty` của `contractRemainingByLine`; "Đã yêu cầu" lấy cùng hàm. Không công thức thứ 2.
- Ẩn giá: dùng `hide_price` của `ContractController::findViewableContract`; ẩn ở BE (không trả tiền), không chỉ ẩn FE.
- Quyền endpoint = quyền xem HĐ (`findViewableContract`) — test cả có quyền + không quyền.
- Không hiện tài khoản kế toán / kho LRHD / phiếu nhập cha tự động như chứng từ cho kinh doanh.
- Phiếu huỷ không tính vào số nào. Trả lại: chỉ tính hàng cha mua sẵn + hàng thường (phương án 1).
- Trạng thái dòng theo thứ tự: Hoàn tất (done ≥ qty) → Chưa yêu cầu (req = 0) → Đang xử lý (wh < req) → Đã xuất kho. Thẻ đếm chỉ dòng cấp 1.
- Tab hiện khi status ∈ {6,19,20,21,22,12,11,10} hoặc (18 và HĐ đã có YCXH).
- Endpoint tab < 300 ms trên HĐ nhiều dòng nhất của rehearsal.

## Review Focus
1. 2 dòng cha trùng mã ⇒ số không gộp nhầm sang nhau (gom theo dòng HĐ, không theo product_id).
2. Dòng cha lắp từ con: Đã xuất kho = số bộ lắp + PXK 21 tay; "Đã lắp x/y" đúng khi lắp dở.
3. HĐ không có YCXH nào / HĐ chỉ có phiếu huỷ ⇒ tab rỗng sạch, không lỗi chia 0 ở % tiến độ.
4. Người bị ẩn giá ⇒ payload không có trường tiền (kiểm JSON, không chỉ DOM).
5. Mở HĐ không đổi số request / thời gian (tab chưa bấm ⇒ 0 request export-progress).

### Task 1 (BE): Service tổng hợp + test
**Files:** Create `hrm-api/Modules/Assign/Services/ContractExportProgressService.php`;
Test `hrm-api/Modules/Assign/Tests/Feature/ContractExportProgressTest.php` (fixture dựng theo khuôn `ContractParentAssemblyTest`).
**Interfaces — Produces:**
- `summary(Contract $c, bool $hidePrice): array` ⇒ `['lines'=>[...], 'summary'=>[...], 'timeline'=>[...]]`
  - line: `id, parent_id, code, name, unit_name, qty, requested, warehouse_out, done, returned, remaining, assembled (cha lắp từ con | null), status (0..3)`
  - summary: `counts[4]` (dòng cấp 1), `returned_lines`, `progress_pct`, `done_value`, `total_value` (2 trường tiền = null khi hidePrice), `can_request` (= `hasLinesLeftToRequest`)
  - timeline: mỗi YCXH: `id, code, created_at, type (20|21), line_count, step (0 Đã yêu cầu,1 Kho đang soạn,2 Đã xuất khỏi kho,3 Hoàn tất,-1 Huỷ)`
- `documents(Contract $c, int $lineId, string $column): array` — column ∈ `requested|warehouse_out|done|returned`; mỗi phiếu `id, code, date, qty, status_name, url`.
**Nguồn số (theo dòng HĐ):** requested/remaining = `contractRemainingByLine`; warehouse_out = `warehouse_export_lots` của PXK status ∈ {1 Đã hạch toán, 7 Đang hạch toán} (+ số bộ từ `product_import_details` phiếu nhập cha Hoàn tất cho dòng cha lắp);
done = `product_export_details` của PXH status ∈ {1 Hoàn tất, 12, 13}; returned = phiếu `ProductImportRequest::BAN_TRA_LAI` đã hạch toán, nối dòng qua `product_export_request_detail_id` → `product_export_request_details.hrm_contract_product_id` (kiểm tên bảng chi tiết phiếu trả lại trước khi viết).
Step timeline từ status YCXH: 1/2/3/7/10/11 ⇒ 0; 4 ⇒ 1; 8 ⇒ 2; 9/5 ⇒ 3; 6 ⇒ -1 (kiểm lại STATUS_* trong `ProductExportRequest` khi viết).
- [x] Test `test_hai_dong_cha_trung_ma_khong_gop` — 2 dòng cha TĐ-01, YCXH 3 bộ cho dòng 1 ⇒ dòng 1 requested 3, dòng 2 requested 0.
- [ ] Test `test_cha_lap_do_tu_con` — con xuất đủ 3/5 bộ ⇒ cha `assembled=3`, `warehouse_out=3`, `done=3`, status 1 hoặc 3 đúng luật.
- [ ] Test `test_phieu_huy_khong_tinh` + `test_hd_khong_co_ycxh` (progress_pct 0, không lỗi chia 0).
- [ ] Test `test_remaining_bang_contractRemainingByLine` (so từng dòng, cả dòng con).
- [ ] Test `test_an_gia_khong_tra_tien` (done_value/total_value null).
- [ ] Test `test_tra_lai_hang_thuong` (returned = SL phiếu trả lại hoàn tất; requested/done không đổi).
- [ ] Chạy fail → viết service → chạy pass: `DB_DATABASE=hrm_erp_rbac_rehearsal php vendor/bin/phpunit Modules/Assign/Tests/Feature/ContractExportProgressTest.php`
- [ ] Đo: tinker `summary()` trên HĐ nhiều dòng nhất rehearsal < 300 ms (ghi số vào checkpoint).

### Task 2 (BE): Endpoint + quyền
**Files:** Modify `hrm-api/Modules/Assign/Routes/api.php` (nhóm `/assign/contracts`, sau `/{id}/profit-analysis`);
`hrm-api/Modules/Assign/Http/Controllers/Api/V1/ContractController.php` thêm `exportProgress($id)`, `exportProgressDocuments($id, Request)`.
- `GET /assign/contracts/{id}/export-progress` ⇒ `findViewableContract($id)` rồi `summary($c, $c->hide_price)`.
- `GET /assign/contracts/{id}/export-progress/documents?line_id=&column=` ⇒ validate column (422), line thuộc HĐ (404).
- [ ] Test feature: có quyền 200 · không quyền 403/404 như `show` · column sai 422 · line HĐ khác 404.
- [ ] Đảm bảo show KHÔNG đổi: test đếm query `show` trước/sau (DB::enableQueryLog) bằng nhau.

### Task 3 (BE, TÁCH — hỏi riêng): Index migration
Migration `hrm-api/database/migrations/2026_11_10_000001_add_contract_indexes_for_export_progress.php`:
index `product_export_requests(emplement_contract_type, emplement_contract_id)`, `product_exports(emplement_contract_type, emplement_contract_id)`,
`product_export_request_tab_products(contract_product_id)`. Bảng dùng chung ERP — `--pretend` + đo thời gian ALTER trên rehearsal, nêu tên file + DB đích khi hỏi.
- [ ] Đo `contractRemainingByLine(3443)` trước (111 ms) / sau.
- 10/11 user "làm": EXPLAIN thực tế ⇒ đổi bộ index: BỎ `product_exports` (tab không lọc PXH theo HĐ), THÊM `product_export_request_tab_products(product_export_request_id)`
  + `product_import_request_details(product_export_request_detail_id)`. File đã viết + `--pretend` OK (4 ALTER INPLACE/LOCK=NONE, bỏ qua nếu đã có index mở đầu bằng cột đó).
  Đo TRƯỚC (rehearsal, HĐ 734, lần đầu): summary 865 ms / 9 query — remaining 101 ms, returned 543 ms, timeline 141+58 ms, đều quét toàn bảng. User "ok" ⇒ đã chạy lẻ --path vào rehearsal (1,7 s). SAU: 68 ms, không còn quét toàn bảng (remaining 2 ms, returned 20 ms, timeline 3+1 ms). Deploy hrm_crm/prod: chạy cùng đợt deploy nhánh.

### Task 4 (FE): Component tab + tải lười
**Files:** Create `hrm-client/components/assign/contract/ContractExportTab.vue` (+ `ContractExportDocumentsModal.vue`);
Modify `hrm-client/pages/assign/contracts/_id/index.vue` (thêm tab `{ key: 'export', label: 'Xuất hàng', icon: 'ri-truck-line' }` sau Giao hàng — đổi icon Giao hàng nếu trùng; `v-if` theo luật hiện tab; tải khi `activeTab === 'export'` lần đầu, khuôn `loadPrintDoc`).
- Props: `contractId`, `active` (bool). Emit: không. Nút "Yêu cầu xuất hàng" trong tab gọi cùng hàm route hiện có (`/finance/product-export-requests/create?hrm_contract_id=`), bật theo `summary.can_request`.
- Bố cục theo mockup: dải thẻ (thẻ lọc bấm lại bỏ lọc), bảng cây (V2BaseDataTable nếu dựng được cây, nếu không bảng thường theo mẫu MISA `_misa-grid.scss`), dòng thời gian thu gọn (mặc định mở khi ≤ 5 đợt). Popup: modal theo skill modal-popup.
- [ ] Playwright MCP: mở HĐ ⇒ 0 request `export-progress`; bấm tab ⇒ đúng 1 request; đổi tab qua lại ⇒ không gọi lại.
- [ ] Đo DOM: số dòng bảng = số dòng payload; tổng 4 thẻ = số dòng cấp 1; bấm thẻ lọc ⇒ đếm dòng; popup mở đúng số phiếu; ẩn giá ⇒ không có thẻ tiến độ; HĐ trạng thái Đang tạo ⇒ không có tab.
- [ ] So "Còn lại" trên tab với số picker màn Tạo YCXH cho phép (cùng HĐ).

### Task 5: e2e + tài liệu
- [ ] Thêm ca vào `HRM/e2e/tests/assign/contracts-approval-flow.spec.ts` (hoặc spec mới `contract-export-tab.spec.ts`): tải lười, hiện/ẩn tab, ẩn giá, khớp Còn lại. Chạy `--workers=1` CHỈ khi user yêu cầu.
- [ ] Checkpoint plan.md; ghi vấn đề ngoài luồng: "trả lại hàng cha lắp tự động chưa làm được (PXH tự động không có YCXH)".

### Fix 10/11 — Form Lập/Sửa HĐ: lỗi 422 BE không hiện (VPS dev báo "The given data was invalid.")
- [x] Tái hiện (Playwright, giả lập 422 `products`): chỉ có toast tiếng Anh, 0 dòng lỗi trên màn.
- [x] `pages/assign/contracts/_id/edit.vue`: khối lỗi đầu tab Chi tiết (`products` | `line_adjustments`, tách dòng từng mặt hàng — computed `goodsErrorLines`); lỗi `quotation_id` dưới ô Báo giá nguồn; 422 ⇒ toast "Vui lòng kiểm tra lại thông tin đã nhập" + mở đúng tab + cuộn; `scrollToFirstError` chỉ chọn lỗi đang hiện + có chữ.
- [x] Đo lại: tab goods, khối lỗi trong khung nhìn, icon cùng hàng (lệch ≤ 2px), màu list = màu chữ lỗi; ca có cả quotation_id ⇒ cuộn tới ô Báo giá nguồn.
- [x] e2e `HRM/e2e/tests/assign/contracts-form-422.spec.ts` E422-1/E422-2 (CHƯA chạy). Đã commit + push `8275d6a0c` lên origin/gop_db-xuat-hang-cha-con (10/11).

### Checkpoint — 2026-11-10 (Phase 30 Task 1-2-4-5 xong, CHƯA commit) — nhánh gop_db-xuat-hang-cha-con, KHÔNG migration
Vừa hoàn thành (user "Làm 1-2-4-5, index để sau"):
- hrm-api: `Modules/Assign/Services/ContractExportProgressService.php` (summary/documents, VISIBLE_STATUSES, LINE_STATUSES chữ+màu BE, STEPS);
  ContractController `exportProgress` / `exportProgressDocuments` + 2 route `GET assign/contracts/{id}/export-progress[/documents]`.
  PHPUnit `ContractExportProgressTest` 10 ca + `ContractExportProgressApiTest` 5 ca xanh; ContractParentAssemblyTest 7 + ContractProfitAnalysisTest 28 vẫn xanh.
  Thử đột biến (tính cả PXK đang tạo) ⇒ test đỏ đúng ca. Đo HĐ 734 (9 dòng): 120–224 ms, 8 query (66 ms là contractRemainingByLine có sẵn;
  returned + timeline ~25 ms mỗi cái — cột chưa index, Task 3).
- hrm-client: `pages/assign/contracts/components/ContractExportTab.vue` + `ContractExportDocumentsModal.vue`; `_id/index.vue` tab sau Giao hàng,
  `showExportTab` theo trạng thái, tải lười, reset khi HĐ tải lại, hàng tab chỉ nút icon Tải lại.
  Playwright (giả lập payload, show 734 đổi status 6, chặn ghi): mở HĐ 0 request · bấm tab 1 · đổi tab vẫn 1; 7 dòng STT 1/1.1/1.2…;
  lọc "Đang xử lý" ⇒ 3 dòng; popup 2 phiếu 1 link; ẩn giá mất thẻ tiến độ; 0 lỗi JS. Sửa sau đo: hàng tab tràn 34px @1200 (bỏ nút chữ),
  STT 44px bị cắt (⇒ 56px).
- e2e `HRM/e2e/tests/assign/contracts-export-tab.spec.ts` EX-1..3 (list OK, CHƯA chạy).
Bước tiếp theo: user xem → commit/push nhánh; Task 3 (index) hỏi riêng.
- 10/11 user: cột "Hoàn tất" ⇒ "Đã hạch toán" = SL qua PXH đã duyệt (số đã đúng: status 1/12/13; chỉ đổi tên ở BE LINE_STATUSES/STEPS + FE cột/chú thích + e2e mock). Kiểm trên dữ liệu mẫu HĐ 734: 12 tiêu đề cột không cắt chữ.
- 10/11 user: dòng con thể hiện rõ cấp — nhánh cây ├/└ nối từ nút thu gọn của dòng cha, nền con #f7f9fb chữ xám, cha đậm Mã+Tên + nhãn "N hàng con", thu gọn/mở từng cha; con cuối kẻ đậm tách nhóm. Đo: 15→13→15 dòng, nhánh └ dừng giữa dòng, chỉ Mã/Tên đậm. e2e EX-2 thêm ca thu gọn.
- 10/11 user: áp kiểu cây cho tab Chi tiết hợp đồng màn xem — gom CSS cây vào contract-form.scss (.hd-tree-parent/.hd-tree-child/.hd-branch/.hd-caret/.hd-kids), tab Xuất hàng dùng chung; buildLineRows (index.vue) thêm _key/_parentKey/_childCount/_isLast, computed goodsRows ẩn con khi thu gọn (tổng tiền vẫn trên lineRows). Đo HĐ 734: 2 cha/4 con/2 is-last cả 2 bảng, thu gọn 19→17 dòng, tfoot không đổi, 0 lỗi JS. Màn Sửa/Lập CHƯA áp.
- 10/11 user "làm": áp kiểu cây cho bảng hàng hoá màn Lập/Sửa (edit.vue; create.vue extends) — buildLineRows thêm _key/_parentKey/_childCount/_isLast, goodsRows (lọc giữ nguyên object ⇒ ô Vượt trội/Giảm giá ghi đúng dòng), toggleGoodsRow. Đo /734/edit (show giả lập Đang tạo, chặn ghi): 2 cha/4 con, thu gọn 19→17, nhập 12,345 ở dòng cha vẫn đúng dòng sau thu gọn/mở, 0 lỗi JS.

---

# Phase 31 — Bắt buộc nhập khi gửi duyệt + 9 điều kiện chuyển BGĐ — Implementation Plan (11/11/2026, CHƯA code)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development hoặc superpowers:executing-plans. Checkbox `- [ ]`.
> ⚠ CLAUDE.md: CHƯA được phép code. Trước khi bắt tay phải hỏi riêng "làm" + phạm vi (repo · nhánh · file · migration nào chạy DB nào).

**Goal:** HĐ bán gửi duyệt phải đủ điều kiện hiệu lực + thời gian thực hiện; HĐ dính 1 trong 9 điều kiện (I–IX yêu cầu KH 10/11) phải lên BGĐ,
cấu hình theo phòng ở tab "Quy chế khác" với chế độ nói rõ nghĩa.

**Architecture:** BE gom mọi điều kiện ở `ContractService::composeBgdReasons` (1 chỗ cho cả bước TP từ preview HTHT và bước sau từ HTHT đã lưu);
công nợ tách service dùng chung với YCXH. Cấu hình = 3 field mới trong `RegulationTabRegistry` tab `khac` + 2 cột chế độ trên `departments`.
FE: renderer form scalar của `RegulationConfigScreen` thêm kiểu chọn + ô tích; khối cảnh báo BGĐ đổi sang danh sách.

**Tech Stack:** Laravel 8 / PHP 7.4 (hrm-api), Nuxt 2 / Vue 2 (hrm-client), PHPUnit, Playwright.

**Spec:** `.plans/hop-dong/design-phase31-dieu-kien-duyet.md` · mockup `mockup-dieu-kien-duyet.html` · gap `yeu-cau-bo-sung-10-11-gap.md`.

**Nhánh đề xuất:** `gop_db-xuat-hang-cha-con` (worktree wt-hop-dong-ban, đang chứa Phase 30 chưa commit) hoặc nhánh mới tách từ đó — hỏi user khi xin "làm".

## Global Constraints
- Không có giá trị ngầm "để trống / 0 = không xét": tắt/bật xét bằng cột chế độ riêng (`extra_price_approval_mode` 0/1/2, `max_value_contract_mode` 0/1).
- Migration đặt sẵn chế độ theo số đang có (`max_extra_price_percent > 0` ⇒ 2 else 0; `max_value_contract > 0` ⇒ 1 else 0) ⇒ sau deploy 0 HĐ đổi hành vi.
- Không sửa ERP. ERP không đọc 2 cột mới; `department_lead_disapprove_contract` 2 nơi cùng ghi 1 cột.
- Bắt buộc khi gửi duyệt: `effective_condition`, `execution_deadline_days` (> 0), `execution_deadline_base` — câu `Bắt buộc phải nhập`. Lưu nháp vẫn nullable. `execution_base_date` không bắt.
- Câu lý do đúng nguyên văn bảng design mục 4 (kèm số: `%.2f%%`, tiền định dạng nghìn dấu phẩy).
- Công nợ = số đã hạch toán TK 131 (type 1 − type 2, `identify_number_parent = 131`), KHÔNG cộng giá trị HĐ. Hạn mức ≤ 0 / không có ⇒ bỏ qua (đây là nghĩa ERP của bảng hạn mức, không phải cấu hình mới).
- Cổng giữ nguyên: có lý do + không quyền BGĐ ⇒ chỉ còn Chuyển duyệt BGĐ; có quyền BGĐ ⇒ Duyệt thẳng.
- Migration: liệt kê + `--pretend` + chạy lẻ `--path`, chỉ vào DB user nêu.

## Review Focus
1. Phòng có `max_extra_price_percent = 0` (102 phòng) ⇒ sau migration mode 0 ⇒ HĐ có vượt trội KHÔNG bị bắt BGĐ (so với trước deploy).
2. Đổi chế độ sang "Không xét" nhưng ô số còn giữ giá trị cũ ⇒ không xét (BE đọc mode trước, bỏ qua số).
3. HĐ không có `customer_id` công ty / KH không có dòng `declare_limit_debts` ⇒ không lỗi, không lý do công nợ.
4. Hai lượt gọi `bgdReasons` (màn duyệt + `assertNoBgdNeeded`) cho cùng kết quả — preview và đã lưu không lệch ở II.
5. Gửi duyệt từ màn chi tiết thiếu 3 ô ⇒ sang Sửa có đủ 3 lỗi dưới ô (không chỉ toast), lưu nháp ở Sửa vẫn được.

### Task 1 (BE + migration — hỏi riêng trước khi chạy): Cột chế độ + tab Quy chế khác
**Files:** Create `hrm-api/database/migrations/2026_11_11_000001_add_contract_approval_modes_to_departments.php`;
Modify `hrm-api/Modules/MasterData/Support/RegulationTabRegistry.php` (tab `khac` ~dòng 321), `RegulationConfigService.php` nếu cần option `inline:` mới;
Test `hrm-api/Modules/MasterData/Tests/Feature/RegulationKhacApprovalTest.php`.
- Migration: `extra_price_approval_mode` tinyint default 0, `max_value_contract_mode` tinyint default 0 (bảng ERP dùng chung ⇒ `ALGORITHM=INPLACE`), UPDATE đặt sẵn như Global Constraints; down drop cột.
- Registry `khac` thêm: `extra_price_approval_mode` (input select, `inline:extra_price_approval_mode` = 0 Không xét / 1 Có vượt trội là chuyển / 2 Vượt hạn mức),
  `max_extra_price_percent` (% decimal), `max_value_contract_mode` (`inline:max_value_contract_mode` = 0 Không giới hạn / 1 Có giới hạn),
  `department_lead_disapprove_contract` (bool). Nhãn đúng design mục 3 (đổi nhãn `max_value_contract` thành "Giá trị HĐ tối đa").
- Validate khi lưu: mode 2 ⇒ `max_extra_price_percent` bắt buộc, 0 < x ≤ 100; `max_value_contract_mode` 1 ⇒ `max_value_contract` bắt buộc > 0; mode khác ⇒ không bắt số.
- [ ] Test: migration đặt sẵn (phòng 5% ⇒ 2, phòng 0 ⇒ 0); lưu mode 2 thiếu % ⇒ 422 `Bắt buộc phải nhập`; lưu % = 120 ⇒ 422; hẹn ngày áp ⇒ áp đúng ngày + có lịch sử.
- [ ] `migrate:status` + `--pretend --force` ⇒ báo user tên file + DB rehearsal, chờ "ok" rồi chạy lẻ `--path`.

### Task 2 (FE): Tab Quy chế khác
**Files:** Modify `hrm-client/components/regulation-config/data.js` (khối `khac` ~dòng 396), `RegulationConfigScreen.vue` (renderer form scalar).
- 2 khối "Quỹ & lợi nhuận" / "Duyệt hợp đồng bán", mỗi hàng đủ 12 cột; chọn chế độ = `V2BaseSegmented`; ô số chỉ hiện khi mode cần, khi ẩn hiện câu giải thích như mockup; ô tích `V2BaseCheckbox`.
- Nhãn khớp 1-1 BE (join theo label). Lỗi 422 hiện dưới đúng ô.
- [ ] Playwright (rehearsal, :3060): đổi mode ⇒ đếm ô số hiện/ẩn; lưu + nạp lại giữ giá trị; lỗi dưới ô khi thiếu %; đo không tràn ngang @1200.

### Task 3 (BE): Service công nợ dùng chung
**Files:** Create `hrm-api/Modules/Assign/Services/DebtLimitService.php`; Modify `ProductExportOverLimitService.php` (gọi service mới, không đổi kết quả);
Test `hrm-api/Modules/Assign/Tests/Feature/DebtLimitServiceTest.php`; `ProductExportOverLimitApiTest` phải vẫn xanh.
- `customerDebt(int $employeeId, int $customerId): float`, `employeeDebt(int $employeeId): float`, `customerLimit(int $customerId, int $companyId): ?float`, `employeeLimit(int $employeeId, int $companyId): ?float`
  (≤ 0 / không có ⇒ null). Công thức như design mục 4 IX.
- [ ] Test: có hạch toán type 1 & 2 ⇒ số đúng; KH khác không cộng vào; hạn mức 0 ⇒ null; NV không có hạn mức riêng ⇒ lấy của công ty.
- [ ] EXPLAIN 2 truy vấn trên rehearsal + đo ms ⇒ chậm (> 100 ms) thì DỪNG, báo user đề xuất index (hỏi riêng). Kiểm `account_details.created_by` của bút toán HĐ HRM.

### Task 4 (BE): 9 điều kiện ở composeBgdReasons
**Files:** Modify `hrm-api/Modules/Assign/Services/ContractService.php` (`bgdReasons` ~1128, `bgdReasonsFromPreview` ~1153, `composeBgdReasons` ~1165),
`ContractSupportAccountingService.php` (`previewDiffersFromRegulation` ~559, `savedDiffersFromRegulation`: thêm 21.1.x + 19);
Test `hrm-api/Modules/Assign/Tests/Feature/ContractBgdReasonsTest.php`; `ContractApproveGuardsTest`, `ContractHthtStepFlowTest` vẫn xanh.
- Đổi chữ ký nhận cả `redundancy_cost` (preview / đã lưu). Thứ tự khoá = I…IX như design. Phòng = `contract.department_id`, công ty = công ty HĐ.
- VIII: KH thuộc nhóm `configs.customer_groups` (chỉ nhóm KH).
- `assertNoBgdNeeded` giữ, chỉ đổi cách nối câu (xuống dòng thay `; `).
- [ ] Test mỗi khoá 1 ca có + 1 ca không; I đủ 3 mode (gồm mode 0 có số cũ còn giữ); VII 2 mode; IX hạn mức 0 bỏ qua; có quyền BGĐ ⇒ Duyệt thẳng; không quyền ⇒ 422 `bgd`.
- [ ] Đo `bgdReasons` trên HĐ 734 trước/sau (số query + ms).

### Task 5 (BE + FE): Bắt buộc khi gửi duyệt
**Files:** Modify `ContractService.php` (`submit` ~825, thêm `assertExecutionTermsFilled`); `hrm-client/pages/assign/contracts/_id/edit.vue` (map 422 vào 3 ô tab Thông tin chung),
`_id/index.vue` (nút Gửi duyệt: bắt 422 ⇒ toast liệt kê tên ô thiếu ⇒ lưu lỗi vào store ⇒ `router.push` sang Sửa ⇒ edit đọc store, hiện lỗi + mở tab + cuộn ô đầu, xoá store);
Test thêm ca vào `ContractApproveGuardsTest` hoặc `ContractSubmitRequiredTest.php`.
- Lỗi đi cùng các assert khác của submit trong 1 lần 422 (không nhỏ giọt).
- [ ] Test: thiếu cả 3 ⇒ 422 đủ 3 khoá; days = 0 ⇒ lỗi; đủ ⇒ qua; lưu nháp thiếu ⇒ OK.
- [ ] Playwright: gửi duyệt từ chi tiết HĐ thiếu ô ⇒ sang Sửa, đếm 3 `V2BaseError` có chữ, ô đầu trong khung nhìn; reload Sửa ⇒ hết lỗi.

### Task 6 (FE): Danh sách lý do trên màn duyệt
**Files:** Modify `hrm-client/pages/assign/contracts/_id/support-accounting.vue` (~dòng 12), `_id/index.vue` (~dòng 25), modal Chuyển duyệt (giữ `bgd_reasons` vào lịch sử).
- [ ] Playwright (giả lập payload 4 lý do): đếm 4 `li`, không còn chuỗi `; `, nút Duyệt ẩn / Chuyển duyệt hiện với user không quyền BGĐ; user có quyền BGĐ thấy Duyệt.

### Task 7: e2e + tài liệu
- [ ] e2e `HRM/e2e/tests/assign/contracts-bgd-reasons.spec.ts` + ca tab Quy chế khác; liệt kê, CHƯA chạy (chạy `--workers=1` chỉ khi user yêu cầu).
- [ ] Checkpoint plan.md; cập nhật gap doc trạng thái I–IX.

### Checkpoint — 2026-11-11 (Phase 31 code xong BE + FE, ĐANG kiểm Playwright, CHƯA commit)
Nhánh `gop_db-hd-dieu-kien-duyet` (tách origin/gop_db 0c3c67484), worktree `websites/wt-hd-dieu-kien-duyet` — API :8061, Nuxt :3061, DB rehearsal.
User 11/11: "làm trên nhánh riêng, khi nào yêu cầu mới merge gop_db" · migration chạy vào hrm_erp_rbac_rehearsal.
- Task 1: migration `2026_11_11_000001_add_contract_approval_modes_to_departments` ĐÃ CHẠY lẻ --path vào rehearsal (sau: 1 phòng mode 2, 20 phòng max_value mode 1, 82 tắt).
  Registry `khac` +4 field (2 chế độ select inline, required_if + gt:0 ở ScheduleRegulationVersionRequest). Test RegulationKhacApprovalTest 6 ca xanh.
- Task 2: RegulationConfigScreen — kiểu field mới head / seg (V2BaseSegmented) / check (V2BaseCheckbox) / modeNum (showIf + câu giải thích), group `cols12`.
- Task 3: `DebtLimitService` — lọc theo NGƯỜI LẬP HĐ (whereHasMorph như ERP), không theo account_details.created_by. Lấy trước id HĐ rồi quét bút toán
  (bản nối subquery 1,1 s ⇒ 228 ms tối đa với NV lập 1.424 HĐ; KH ≤ 15 ms). 75 cặp NV×KH khớp 100% công thức YCXH cũ. YCXH gọi service mới.
  ⚠ công ty 1-4,8,9 có limit_export_debt_employee ⇒ employeeDebt chạy mỗi lần xét lý do (nhớ theo request). Chưa thêm index — hỏi user.
- Task 4: composeBgdReasons 9 điều kiện; II mở rộng 21.1.x + mục 19 (mọi phòng). Sửa 3 ca cũ ContractApproveGuardsTest theo hành vi mới + 7 ca p31.
- Task 5: submit gom lỗi 3 ô + mẫu in trong 1 lần 422. ⚠ `effective_condition`, `execution_deadline_base` NOT NULL default 1 (BE + FE tự điền 1) ⇒ thực tế chỉ
  "Thời hạn thực hiện (ngày)" thiếu được — hỏi user. FE: ContractSubmitModal emit `invalid` ⇒ index/support-accounting toast tên ô + sang Sửa
  (contractSubmitErrors.js), edit.vue hiện lỗi dưới ô; FE validateForm(isSubmit) bắt 3 ô.
- Task 6: khối cảnh báo BGĐ index.vue + support-accounting.vue thành danh sách `.hd-bgd-reasons`.
- Lỗi test có sẵn (bản gốc cũng lỗi, dữ liệu rehearsal): ContractHthtStepFlowTest 6, ProductExportOverLimitApiTest 5, MasterData Regulation* 13 (role_has_permissions.company_id).
- Playwright MCP (11/11, :3061 rehearsal): tab Quy chế khác — lưới 12 cột, tiêu đề khối 997px trọn hàng, đổi chế độ ⇒ ô số / câu giải thích đúng,
  "Vượt hạn mức" thiếu % ⇒ 422 dưới ô; lưu 3% + 500,000,000 + ô tích ⇒ nạp lại giữ đúng (phòng 58, đã trả về giá trị gốc + xoá version 446 / history 244);
  390px không cuộn trang (nút chế độ cuộn ngang trong ô). Sửa sau đo: `.f.wide` bị `span 6` đè; V2BaseCheckbox có slot = chế độ nhiều ô ⇒ dùng prop label.
  HĐ 734 (giả lập payload, chặn ghi): 4 lý do ⇒ 4 li, không còn "; "; Gửi duyệt 422 ⇒ toast tên ô ⇒ /734/edit, lỗi dưới "Thời hạn thực hiện (ngày)" trong khung nhìn,
  lỗi mẫu in ở tab Mẫu in; màn Duyệt bước Pháp chế 3 li. bgdReasons HĐ 734 thật: 2 truy vấn công nợ ~48 ms, lần 2 cùng request 6 ms.
  ⚠ HĐ 734 thật dính VIII; ~7% HĐ hãng 2026 (1.284/17.621) có KH nhóm 9 "Khách hàng thương mại" / 30 "Trung tâm đăng kiểm".
- e2e `HRM/e2e/tests/assign/contracts-bgd-reasons.spec.ts` BGD-1..4 (CHƯA chạy).
Bước tiếp theo: user xem + trả lời 3 câu (2 ô chọn mặc định 1; VIII 7% HĐ; index công nợ) → commit khi user báo.
- 11/11 user chọn bỏ mặc định 2 ô chọn + "làm": migration `2026_11_11_000002_make_contract_execution_terms_nullable` ĐÃ CHẠY lẻ --path vào rehearsal
  (2 cột nullable, không default; HĐ 734/3443 giữ 1/1). Bỏ `?? 1` ở ContractService (tạo/sửa), DetailContractResource, edit.vue (form mới + nạp Sửa);
  recomputeEffectiveDates: chưa chọn ⇒ effective_date / execution_end_date = null (không đoán). Ô "Ngày mốc" chỉ hiện khi đã chọn mốc ≠ 1.
  Test: ContractApproveGuardsTest 71 xanh (ca thiếu ô dùng null thật + ca lưu nháp để trống không tự tính ngày). ContractProfitAnalysisTest 1 lỗi có sẵn (bản gốc cũng lỗi, demo HĐ 734).
  Playwright /734/edit (giả lập 2 ô null, chặn ghi): 2 select trống, không có ô Ngày mốc, Ngày hiệu lực trống; Gửi duyệt ⇒ 3 ô "Bắt buộc phải nhập" cùng lúc;
  validateForm(Lưu nháp) không bắt 2 ô, payload gửi null.
- 11/11 user: điều kiện VIII giữ như khách yêu cầu (~7% HĐ lên BGĐ). Còn chờ: index công nợ.
- 11/11 user: không thêm index công nợ. Phase 31 hết câu hỏi tồn.
Bước tiếp theo: user xem trên :3061 (worktree wt-hd-dieu-kien-duyet) → commit khi user báo; chạy e2e contracts-bgd-reasons khi user yêu cầu;
  deploy: 2 migration 2026_11_11_000001 / 000002 chạy cùng đợt deploy nhánh; merge gop_db khi user yêu cầu.

---

# Phase 32 — Xác nhận bảo lãnh · Ngày mốc nhập sau · Xuất hàng khi chưa đủ mốc — Implementation Plan (11/11/2026, CHƯA code)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development hoặc superpowers:executing-plans. Checkbox `- [ ]`.
> ⚠ CLAUDE.md: CHƯA được phép code. Trước khi bắt tay phải hỏi riêng "làm" + phạm vi (repo · nhánh · file · migration nào chạy DB nào).

**Goal:** Ngày bảo lãnh duyệt và ngày mốc thực hiện nhập bằng nút riêng sau khi ký (có file + lịch sử); HĐ có hiệu lực nhưng thiếu mốc vẫn lập YCXH, đổi lại phiếu qua TP → BGĐ.

**Architecture:** 2 action mới trên `ContractService` + 2 route POST dưới `assign/contracts/{id}`, 2 popup khuôn `ContractCustomerSignedModal`. `can_export` nới bỏ vế ngày kết thúc;
YCXH 20/21 dùng lại luồng trạng thái 10/11 của vượt hạn mức công nợ (#11900), rẽ quyền theo loại phiếu.

**Tech Stack:** Laravel 8 / PHP 7.4, Nuxt 2 / Vue 2, PHPUnit, Playwright.

**Spec:** `.plans/hop-dong/design-phase32-moc-bao-lanh-xuat-hang.md` · mockup `mockup-moc-bao-lanh-xuat-hang.html`.

**Nhánh đề xuất:** tiếp `gop_db-hd-dieu-kien-duyet` (Phase 31 chưa commit cùng đụng `edit.vue` / `ContractService`) — hỏi khi xin "làm".

## Global Constraints
- 2 nút chỉ **người lập** HĐ (403 khác người); điều kiện hiện nút đọc từ cờ BE `is_can_confirm_guarantee` / `is_can_update_execution_base` (danh sách + chi tiết cùng nguồn).
- Bảo lãnh: HĐ trạng thái 17 + `effective_condition = 3`; ngày ≤ hôm nay + file bắt buộc. Ngày mốc: `execution_deadline_base ∈ {2,3,4}` + trạng thái ∈ {17, 6, 19}; ngày ≤ hôm nay bắt buộc, file không bắt buộc, sửa lại được.
- Store/Update HĐ KHÔNG còn nhận `guarantee_approved_date`, `execution_base_date` (chỉ đi qua nút).
- Mỗi lần xác nhận / cập nhật ghi lịch sử HĐ (meta cũ → mới), gọi `recomputeEffectiveDates` (+ `activateIfEffective` cho bảo lãnh).
- `can_export` = trạng thái ∈ EXPORTABLE_STATUSES + có `effective_date` (bỏ vế `execution_end_date`). Thiếu mốc = có hiệu lực, `execution_deadline_days > 0`, chưa có `execution_end_date`.
- YCXH 20/21 thiếu mốc: gửi duyệt ⇒ 409 `type = contract_missing_execution_base` ⇒ đồng ý ⇒ status 10. Quyền TP = `sale.hop_dong_du_an_tkt.approve` + phòng phiếu thuộc phòng quản lý; BGĐ = `sale.hop_dong_du_an_tkt_ban_giam_doc.approve` cùng công ty. Loại 14/17 giữ nguyên hành vi.
- Không thêm cột vào bảng YCXH (dùng chung ERP). Migration chỉ trên `hrm_contracts`.
- Lỗi dưới ô theo form-validate; câu "Bắt buộc phải nhập".

## Review Focus
1. HĐ điều kiện 3 đã xác nhận bảo lãnh với ngày tương lai ⇒ chưa Có hiệu lực; lệnh `contracts:activate` hôm đó chuyển đúng.
2. Sửa ngày mốc khi HĐ Đang thực hiện ⇒ ngày kết thúc tính lại, trạng thái không lùi.
3. YCXH 20/21 lập lúc thiếu mốc, rồi người lập nhập mốc trước khi TP duyệt ⇒ TP/BGĐ vẫn duyệt được, không hỏi lại, không kẹt.
4. Người có quyền "duyệt vượt hạn mức công nợ" nhưng KHÔNG có quyền duyệt HĐ ⇒ không thấy nút ở phiếu 20/21 (và ngược lại ở phiếu 14/17).
5. HĐ cũ đã nhập `guarantee_approved_date` / `execution_base_date` trong form trước Phase 32 ⇒ màn xem vẫn hiện ngày, nút cập nhật hiện đúng.

### Task 1 (BE + migration — hỏi riêng trước khi chạy): 2 action trên HĐ
**Files:** Create `hrm-api/database/migrations/2026_11_11_000003_add_guarantee_and_execution_base_files_to_hrm_contracts.php` (5 cột nullable: `guarantee_file_name`, `guarantee_file_path`, `guarantee_confirmed_at`, `execution_base_file_name`, `execution_base_file_path`);
Modify `Modules/Assign/Services/ContractService.php` (store ~218, update ~527 bỏ 2 khoá; thêm `confirmGuaranteeApproved(Contract, string $date, string $fileName, string $filePath): Contract`, `updateExecutionBaseDate(Contract, string $date, ?string $fileName, ?string $filePath): Contract`),
`Modules/Assign/Entities/Contract/Contract.php` (accessor `is_can_confirm_guarantee`, `is_can_update_execution_base`, `is_missing_execution_base`; `can_export`),
`Http/Controllers/Api/V1/ContractController.php` (2 action, khuôn `customerSigned` :1280 — upload file như HĐ đã ký), `Routes/api.php` (cạnh `customer-signed` :941),
`Transformers/DetailContractResource.php` (3 cờ + 5 cột file), Request store/update (bỏ 2 rule);
Test `Modules/Assign/Tests/Feature/ContractGuaranteeExecutionBaseTest.php`.
- [ ] Test: bảo lãnh đúng người / khác người 403 / sai trạng thái 422 / sai điều kiện 422 / thiếu file 422 `file` / ngày tương lai 422; hôm nay ⇒ Có hiệu lực; ngày mốc nhập ⇒ execution_end_date = mốc + số ngày; sửa lại ⇒ lịch sử 2 dòng meta cũ→mới; store/update gửi 2 khoá ⇒ bị bỏ qua.
- [ ] `--pretend` ⇒ báo user tên file + DB, chờ "ok" rồi chạy lẻ `--path`.

### Task 2 (FE): 2 popup + màn xem HĐ + bỏ 2 ô ở form
**Files:** Create `hrm-client/pages/assign/contracts/components/ContractGuaranteeModal.vue`, `ContractExecutionBaseModal.vue` (copy khuôn `ContractCustomerSignedModal.vue`);
Modify `pages/assign/contracts/_id/index.vue` (2 nút trong V2Footer slot `#custom-actions`, khối Hiệu lực & thời hạn hiện ngày + link file, note-warning thiếu mốc cạnh nút YCXH), `_id/edit.vue` (bỏ ô Ngày bảo lãnh :84, Ngày mốc :91 + khoá form/payload), danh sách `pages/assign/contracts/index.vue` (2 hành động nếu cột Hành động có luồng duyệt — khớp màn chi tiết).
- [ ] Playwright: bấm Xác nhận khi trống ⇒ 2 ô đỏ cùng lúc; lưu ⇒ màn xem có ngày + link file; ngày mốc sửa lại được; form Lập/Sửa không còn 2 ô; nút ẩn với người không phải người lập.

### Task 3 (BE): YCXH 20/21 khi HĐ thiếu mốc
**Files:** Modify `Modules/Assign/Http/Controllers/Api/V1/ProductExportRequestController.php` (`overLimitOnSubmit` :1567 rẽ thêm nhánh HĐ HRM — gọi ở store :1545 + update :2199; rule status :1740 cho phép 10 với 20/21; `notifyIfWaitingManager`),
`Modules/Assign/Entities/Warehouse/ProductExportRequest.php` (`canManagerApprove` :423, `canBoardOfManagerApprove` :445 rẽ theo loại — 20/21 dùng quyền duyệt HĐ; `canReject` dùng lại),
`Modules/Assign/Services/ProductExportOverLimitService.php` (`notifyManagers` / `notifyBoard` lấy người nhận theo quyền của loại phiếu), `ProductExportRequestService::assertContractCanExport` :1063 (câu chặn mới);
Test `Modules/Assign/Tests/Feature/ProductExportContractMissingBaseTest.php`; `ProductExportOverLimitApiTest` không thêm lỗi so với bản gốc (5 lỗi có sẵn).
- [ ] Test: HĐ đủ mốc ⇒ gửi duyệt thẳng 2; thiếu mốc ⇒ 409 đúng type + câu có tên mốc; gửi 10 ⇒ Đợi TP; TP quyền HĐ đúng phòng chuyển ⇒ 11; TP khác phòng 403; người chỉ có quyền vượt hạn mức 403; BGĐ duyệt ⇒ 2; nhập mốc giữa chừng vẫn duyệt được; HĐ chưa hiệu lực vẫn 422.

### Task 4 (FE): YCXH
**Files:** Modify `hrm-client/pages/finance/product-export-requests/components/over-limit.js` (thêm `CONTRACT_MISSING_BASE_TYPE`), `components/ProductExportRequestForm.vue` (:4596 nhận cả 2 type, hộp xác nhận base-confirm-modal), màn chi tiết `_id/index.vue` (note-warning lý do khi 20/21 ở 10/11).
- [ ] Playwright (giả lập 409 + payload, chặn ghi): gửi duyệt ⇒ hộp xác nhận đúng câu ⇒ Đồng ý gửi lại status 10; chi tiết phiếu 10 có khối lý do + nút Chuyển BGĐ duyệt cho TP.

### Task 5: e2e + tài liệu
- [ ] e2e `HRM/e2e/tests/assign/contracts-guarantee-execution-base.spec.ts` (2 popup + màn xem) và ca YCXH thiếu mốc — liệt kê, CHƯA chạy.
- [ ] Checkpoint plan.md; cập nhật gap doc 4a / 5 / 6.

### Checkpoint — 2026-11-11 (Phase 32 code xong BE + FE, ĐANG kiểm Playwright, CHƯA commit)
User "làm" (11/11) — nhánh `gop_db-hd-dieu-kien-duyet` (cùng Phase 31), DB rehearsal.
- Task 1: migration `2026_11_11_000003_add_guarantee_and_execution_base_files_to_hrm_contracts` ĐÃ CHẠY lẻ --path vào rehearsal (5 cột nullable).
  ContractService `canConfirmGuarantee` / `canUpdateExecutionBase` / `confirmGuaranteeApproved` / `updateExecutionBaseDate` (lịch sử `guarantee_approved`,
  `execution_base_date` meta cũ→mới); store/update + Request bỏ 2 khoá; route POST `guarantee-approved`, `execution-base-date` (S3 contract_guarantee /
  contract_execution_base, chặn người lập + trạng thái TRƯỚC khi đẩy file); Contract `can_export` bỏ vế ngày kết thúc + `is_missing_execution_base`,
  `EXEC_BASE_EVENT_NAMES`; Resource 3 cờ + 5 cột + 2 nhãn lịch sử. Test ContractGuaranteeExecutionBaseTest 6 xanh.
- Task 3: ProductExportRequestController `contractMissingBaseOnSubmit` (409 `contract_missing_execution_base`; 10 khi đủ mốc ⇒ 422; rule status 20/21 cho 10);
  ProductExportRequest `isHrmContractType` / `hrmContractRecord`, canManagerApprove / canBoardOfManagerApprove rẽ 20/21 theo quyền duyệt HĐ, canViewLikeErp;
  ProductExportOverLimitService notifyManagers / notifyBoard rẽ 20/21; Resource `manager_approval_reason`. Test ProductExportContractMissingBaseTest 5 xanh.
  ProductExportOverLimitApiTest 5 lỗi + ProductExportRequestProductUnitsGateTest 3 lỗi = fixture quyền / rehearsal (roles FK, role_has_permissions.company_id), không do code.
- Task 2/4 FE: ContractGuaranteeModal / ContractExecutionBaseModal; index.vue 2 nút + callout bảo lãnh / biên bản / thiếu mốc, nhãn "Ngày <sự kiện>";
  edit.vue bỏ 2 ô; over-limit.js nhận thêm type mới (create/edit YCXH dùng chung hộp xác nhận); chi tiết YCXH khối `.ro-approval-reason`.
- Playwright HĐ 734 (giả lập, chặn ghi): 2 nút + callout; popup bảo lãnh trống ⇒ 2 lỗi; popup ngày mốc ⇒ gửi đúng ngày, gợi ý ngày kết thúc 03/02/2027, đóng + toast.
  Sửa sau đo: dòng nhắc thiếu mốc in "kh" (toLowerCase) ⇒ chỉ hạ chữ "Ngày".
- Playwright tiếp (11/11): chi tiết YCXH 44689 (giả lập status 10 + lý do ở data.detail) ⇒ khối `.ro-approval-reason` nền #fffbeb, rộng bằng card, cách 12px;
  nút Chuyển BGĐ duyệt / Không duyệt. Hàm `isOverLimitError` (node 20): 409 cả 2 type = true, type lạ / 422 = false. Form Sửa HĐ không còn 2 ô.
  Không kiểm được hộp xác nhận trên màn Sửa YCXH bằng phiếu demo (không phải phiếu của user 13 ⇒ trang tự chuyển về chi tiết) — luồng dùng chung code vượt hạn mức.
  Sửa sau đo: Resource lấy số HĐ từ HĐ khi phiếu chưa lưu `emplement_contract_code`.
- e2e `HRM/e2e/tests/assign/contracts-guarantee-execution-base.spec.ts` GEB-1..5 (CHƯA chạy).
Bước tiếp theo: user xem → commit khi user báo (nhánh có cả Phase 31 + 32); deploy kèm 3 migration 2026_11_11_000001..3.
- 11/11: e2e 7/7 xanh (config tạm, JWT, :3061). Commit nhánh gop_db-hd-dieu-kien-duyet: api `c03184f1c`, client `b7dc4a69d`.
  User: merge vào nhánh môi trường tester hrm_crm, KHÔNG merge gop_db khi chưa yêu cầu ⇒ merge + push `origin/gop_db-xuat-hang-cha-con`
  (api `d74c27621` +5 commit gồm 3 fix gop_db; client `fadb467ae`, xung đột edit.vue topKeys đã gộp). Chờ user deploy VPS + 3 migration vào hrm_crm.
  ⚠ wt-hop-dong-ban (local gop_db-xuat-hang-cha-con, Phase 30 chưa commit) giờ CHẬM hơn origin — pull trước khi commit Phase 30.

### Checkpoint — 2026-11-11 (wrap up)
Vừa hoàn thành: Phase 31 + 32 code, test (PHPUnit mới 6+6+5+6+7 ca, e2e 7/7), commit nhánh `gop_db-hd-dieu-kien-duyet`, merge + push `origin/gop_db-xuat-hang-cha-con` (môi trường tester hrm_crm).
Đang làm dở: — (Phase 30 tab Xuất hàng vẫn CHƯA commit ở `wt-hop-dong-ban`, nhánh local chậm hơn origin — pull trước khi commit, có thể xung đột index.vue / edit.vue / ContractController).
Bước tiếp theo: user deploy VPS hrm_crm (pull 2 repo + 3 migration `sudo -u www-data php artisan migrate --path=…` + build client); sau đó đợt 3 yêu cầu KH (tiến độ thanh toán chi tiết, kế hoạch giao hàng, cảnh báo HĐ sắp hết hiệu lực). Merge gop_db chỉ khi user yêu cầu.
Blocked:

### Checkpoint — 2026-11-11 (đính chính mục I + đồng bộ số tab Quy chế khác)
Vừa xong: kiểm ERP bằng chạy thật (design-phase31 mục 7) ⇒ ERP định mức "0.00" vẫn xét. hrm-api `489bc4823` (nhánh gop_db-hd-dieu-kien-duyet):
migration `2026_11_11_000004` (phòng 0.00 chế độ 0 ⇒ 1) + `normalizeValues` tab khac ghi số theo chế độ. Đã chạy 000004 vào rehearsal (102 phòng ⇒ 1).
Test: RegulationKhacApprovalTest 8/8, ContractApproveGuards 71, ApprovalHistory 9, GuaranteeExecutionBase 6, LegalNote 55 — xanh; Regulation* 13 lỗi cũ (role_has_permissions.company_id).
Merge vào gop_db-xuat-hang-cha-con ở worktree tạm `wt-merge-tester-p31fix` (`8d55a41de`), CHƯA push.
Đang dở: chờ user cho push. Bước tiếp: push → user deploy VPS hrm_crm chạy thêm migration 000004 (`sudo -u www-data php7.4 artisan migrate --path=… --force`).
VI giữ xét phòng của HĐ (chốt). Không sửa ERP (lỗ `?? 0` ở màn Phòng ban ERP ghi nhận ở design mục 7).

## Phase 33 — Cảnh báo HĐ sắp hết hiệu lực (đợt 3 phần d) — design-phase33-canh-bao-het-hieu-luc.md
- [x] Migration `2026_11_12_000001` companies.contract_expiry_warning_days (default 30) — chạy rehearsal
- [x] Registry tab baogia + ô FE (tab chuyển lưới 12 cột, 9 ô số × span 4 — tránh ô lẻ 1 hàng)
- [x] ContractService::warnExpiringContracts + ContractNotificationService::expiringSoon/expiringNote + lệnh assign:warn-expiring-contracts 08:00
- [x] PHPUnit ContractExpiryWarningTest 6/6; RegulationTabRegistryTest 11/11; Contract* xanh; Regulation* còn 13 lỗi cũ (role_has_permissions.company_id)
- [x] Playwright MCP :3061 (1440/1280/390): ô đọc 30 từ API; 3 hàng × 3 ô; nhập 0 ⇒ "Giá trị phải lớn hơn 0" dưới ô (BE 422 thật, không ghi DB)
- [x] e2e mới `e2e/tests/assign/contracts-expiry-warning.spec.ts` (EXP-1) — CHƯA chạy bộ e2e (chờ user)

### Checkpoint — 2026-11-12 (Phase 33 xong code)
Vừa hoàn thành: Phase 33 — api `29e313d03`, client `1b1f62b6c` (nhánh gop_db-hd-dieu-kien-duyet); merge tester ở worktree tạm `wt-merge-tester-p33` (api `a2b3db1c1`, client `ec28358fc`), CHƯA push.
Đang dở: chờ user cho push.
Bước tiếp theo: push → deploy hrm_crm (pull 2 repo, migration 2026_11_12_000001, queue:restart, build client) → đợt 3 phần (b)+(c) kế hoạch + cảnh báo giao hàng (xem design-phase33 mục 6: companies.warning_product_delivery).
Blocked:
### Checkpoint — 2026-11-12 (Phase 33 đã push + deploy hrm_crm)
Vừa hoàn thành: push origin/gop_db-xuat-hang-cha-con (api `a2b3db1c1`, client `ec28358fc`); VPS dev hrm_crm: pull 2 repo, migration 2026_11_12_000001 (10 công ty = 30), queue:restart, build client Node 14 + pm2 reload hrm-client-crm; kiểm Chrome: tab Báo giá – Hợp đồng có ô mới = 30, 3 hàng × 3 ô.
Sự cố: lần build đầu dùng Node 12 ⇒ lỗi node-sass, dist client bị xoá trong ~5 phút tới khi build lại bằng Node 14 (đã ghi memory).
Đang dở: —
Bước tiếp theo: đợt 3 phần (b) kế hoạch giao hàng + (c) cảnh báo giao hàng — brainstorm/hỏi tồn (xem design-phase33 mục 6).
Blocked:

## Phase 34 — Kế hoạch giao hàng + Cảnh báo giao hàng (đợt 3 b+c) — design-phase34-ke-hoach-giao-hang.md · mockup-ke-hoach-giao-hang.html

Nhánh `gop_db-hd-dieu-kien-duyet` (chỉ ĐỌC bảng ERP `handover_acceptance_product_records(+_details)` — đã có trong DB gộp, không cần code màn BBGN).
Global: chỉ dòng hàng CHA (`parent_id IS NULL`), dịch vụ không vào kế hoạch; "đã giao" = BBGN status 2 của HĐ HRM (`contract_type` = class Contract HRM),
cộng theo `product_id-unit_id`, đắp FIFO theo ngày đợt (mốc = date_to ?? date_from), dòng trùng product-unit đắp theo thứ tự dòng.

### Task 1 — Migration + Entity
- [x] `2026_11_12_000002_add_delivery_warning_days_to_hrm_contracts` (smallint unsigned NULL) · `2026_11_12_000003_create_hrm_contract_delivery_batches`
      (id, contract_id idx, sort_order, date_from, date_to NULL, note, audit) · `..._items` (batch_id idx, contract_product_price_id, product_id, unit_id, qty decimal(15,2)).
- [x] Entity `ContractDeliveryBatch` / `ContractDeliveryBatchItem` (extends BaseModel), quan hệ `Contract::deliveryBatches()`.
### Task 2 — Lưu + bắt buộc khi gửi duyệt
- [x] Store/UpdateRequest nhận `delivery_warning_days` (integer min:0) + `delivery_batches.*` (date, date_to after_or_equal, items.*.qty numeric gt:0) — định dạng chặn cả nháp.
- [x] ContractService store/update ghi đè đợt (replace-all) khi HĐ còn sửa được; `executionTermsErrors` thêm: thiếu N, không có đợt, đợt rỗng, dòng cha xếp ≠ SL HĐ (key `delivery_batches`, `delivery_batches.{i}.date_from`, `delivery_batches.rows`).
### Task 3 — Tính trạng thái + Resource
- [x] `ContractDeliveryPlanService::summary(Contract)`: đợt (stt, ngày, items, delivered/plan theo dòng, status: da_giao(+ngày BBGN làm đủ)/qua_han/sap_den_han/chua_giao, status_text/color 9 mã) + tổng theo dòng. 1 truy vấn BBGN gộp.
- [x] DetailContractResource: `delivery_warning_days`, `delivery_batches` (sửa), `delivery_plan` (xem), cờ `is_can_update_delivery_plan`.
### Task 4 — Cập nhật sau ký
- [x] `POST assign/contracts/{id}/delivery-plan` (người lập; 17/6/19): đợt đã giao đủ khoá; SL đợt ≥ SL đã đắp vào đợt; tổng = SL HĐ; lý do bắt buộc; lịch sử `delivery_plan` meta cũ→mới.
### Task 5 — Nhắc
- [x] `ContractNotificationService::deliveryDueSoon/deliveryOverdue` · `ContractService::warnDeliveryBatches(?Carbon)` · lệnh `assign:warn-delivery-batches` 08:00 (HĐ 6/19, đợt chưa đủ: còn đúng N ngày / hôm qua là hạn).
### Task 6 — FE
- [x] Component `ContractDeliveryPlanEditor.vue` (dải thẻ đợt + ma trận + popup `ContractDeliveryBatchModal.vue` V2BaseModal: V2BaseSegmented, V2BaseDatePicker, bảng chọn hàng V2BaseCheckbox/V2BaseInput, kiểm SL khi gõ) — dùng ở edit.vue + popup cập nhật sau ký.
- [x] Màn xem `_id/index.vue`: khối Kế hoạch giao hàng (thẻ + ma trận đã giao/kế hoạch + note sắp hạn) + nút Cập nhật.
- [x] Map 422 gửi duyệt (contractSubmitErrors: "Kế hoạch giao hàng"), chuyển màn Sửa hiện lỗi (khuôn Phase 31).
### Task 7 — Kiểm
- [x] PHPUnit `ContractDeliveryPlanTest`: lưu/replace, gửi duyệt thiếu/thừa/đợt rỗng/N, FIFO 2 đợt + BBGN status 1 không tính, ngày đã giao, chỉ hàng cha, cập nhật sau ký (khoá, ≥ đã giao, quyền, lịch sử), lệnh nhắc (N ngày / quá hạn / đã đủ không nhắc).
- [x] Playwright :3061 đo DOM (thêm đợt, lỗi đồng thời, ma trận vượt, màn xem, 390px) + e2e `contracts-delivery-plan.spec.ts`.

### Checkpoint — 2026-11-12 (Phase 34 xong code, chưa push)
Vừa hoàn thành: Phase 34 — api `434bbbce1`, client `be9c9a7d0` (nhánh gop_db-hd-dieu-kien-duyet). Migration 000002 + 000003 chạy rehearsal
(000003 lần đầu lỗi tên index > 64 ký tự MySQL 1059 ⇒ đặt tên ngắn `hcdbi_contract_product_price_idx`, xoá 2 bảng rỗng tạo dở, chạy lại).
Thêm so với plan: HĐ không có dòng hàng cha ⇒ không bắt kế hoạch; dòng hàng đặt trong tab Giao hàng có sẵn (không thêm tab); tên hàng dài cắt "…" + tooltip.
Test: ContractDeliveryPlanTest 10/10 (gồm API delivery-plan 422/200/403); ApproveGuards 71 · ApprovalHistory 9 · LegalNote 55 · Guarantee 6 · ExpiryWarning 6 xanh.
ContractHthtStepFlowTest: 6 lỗi cũ + 1 ca `test_tp_duyet_cuoi_luu_da_duyet` hỏng do DỮ LIỆU rehearsal — NV 13 không còn vai trò có quyền BGĐ duyệt HĐ (không do code).
Playwright :3061: form Sửa HĐ 3443 (thêm đợt, lỗi đồng thời, SL vượt, ma trận, Gửi duyệt chặn, payload), màn xem HĐ 734 (giả lập plan), popup cập nhật, 390px không tràn.
e2e mới `e2e/tests/assign/contracts-delivery-plan.spec.ts` (DLV-1, DLV-2) — CHƯA chạy bộ e2e.
Merge tester ở worktree tạm `wt-merge-tester-p34` (api `8b5f8f18b`, client `092bdde54`), CHƯA push.
Bước tiếp theo: user cho push → deploy hrm_crm (2 migration 2026_11_12_000002/000003, queue:restart, route:cache, build client Node 14 + pm2 reload hrm-client-crm).
Sau đó: đợt 3 phần (a) tiến độ thanh toán chi tiết (mốc "Giao hàng" lấy ngày đã giao từ Phase 34).
Blocked:
### Checkpoint — 2026-11-12 (Phase 34 đã push + deploy hrm_crm)
Vừa hoàn thành: push origin/gop_db-xuat-hang-cha-con (api `8b5f8f18b`, client `092bdde54`); hrm_crm: 2 migration 2026_11_12_000002/000003, route:cache
(route delivery-plan có trong cache, gọi thử 401), queue:restart, build client Node 14 + pm2 reload; Chrome: HĐ 1 tab Giao hàng hiện khối (chưa có kế hoạch — HĐ gửi duyệt trước tính năng).
Lưu ý: `artisan route:list` trên VPS lỗi chung (không riêng route này) ⇒ kiểm route bằng file cache / gọi HTTP.
Bước tiếp theo: đợt 3 phần (a) tiến độ thanh toán chi tiết — brainstorm/hỏi tồn (mốc Giao hàng lấy ngày đã giao từ Phase 34; companies.warning_due_date ERP).
Blocked:

## Phase 35 — Tiến độ thanh toán chi tiết + cảnh báo thu tiền (đợt 3 a) — design-phase35-tien-do-thanh-toan.md · mockup-tien-do-thanh-toan.html
User "làm" 12/11. Nhánh `gop_db-hd-dieu-kien-duyet`, DB rehearsal. Chốt kỹ thuật lúc làm:
- Gắn mốc Giao hàng theo SỐ THỨ TỰ đợt (`delivery_batch_no`, 0 = toàn bộ kế hoạch) — id đợt đổi mỗi lần lưu (replace-all Phase 34).
- Đã thu = Σ Có − Σ Nợ trên TK con 131 của phiếu thu / báo có / điều chỉnh công nợ gắn HĐ (rehearsal: thu ghi Có 131, điều chỉnh 2 chiều), ≥ 0; đắp FIFO theo hạn.
- Tổng phải thu các lần (amount ?? % × giá trị HĐ sau VAT) = giá trị HĐ (lệch ≤ 1đ) khi gửi duyệt.
### Task 1 — Migration
- [x] `2026_11_12_000004_add_schedule_fields_to_hrm_contract_process_payments` (delivery_batch_no, event_date, event_file_name/path, event_updated_at)
- [x] `2026_11_12_000005_merge_delivery_payment_conditions` (dữ liệu: GIAO_HANG_1 đổi tên "Giao hàng có chữ ký KH", dòng dùng GIAO_HANG_2 ⇒ _1, GIAO_HANG_2 is_active=0) + seeder đồng bộ
### Task 2 — BE
- [x] `ContractPaymentScheduleService`: summary (hạn thực tế/dự kiến, phải thu, đã thu FIFO, trạng thái) · submitErrors (thứ tự mốc, mốc + số ngày / đợt, tổng) · updateEvent · warn
- [x] Request + ContractService lưu `delivery_batch_no`; submit gom lỗi; Resource `payment_schedule` + `is_can_update_payment_event`; POST `/{id}/payment-events/{paymentId}` (ngày + biên bản bắt buộc, người lập); 3 thông báo; lệnh `assign:warn-payment-schedule` 08:10
### Task 3 — FE
- [x] ContractPaymentTermsTable: mốc Giao hàng ⇒ chọn đợt; cột Hạn dự kiến; lỗi gửi duyệt dưới ô · ContractPaymentScheduleView (màn xem) + ContractPaymentEventModal
### Task 4 — Kiểm
- [x] PHPUnit ContractPaymentScheduleTest · Playwright :3061 · e2e contracts-payment-schedule.spec.ts

### Checkpoint — 2026-11-12 (Phase 35 xong code, chưa push)
Vừa hoàn thành: Phase 35 — api `d77925d8e`, client `6c1f1901c` (nhánh gop_db-hd-dieu-kien-duyet). Migration 000004 (5 cột) + 000005 (dữ liệu: GIAO_HANG_1 đổi tên,
GIAO_HANG_2 tắt; rehearsal 0 dòng phải chuyển) chạy rehearsal. Test: ContractPaymentScheduleTest 8/8 (gồm API payment-events 422), ApproveGuards 71 · ApprovalHistory 9 ·
LegalNote 55 · DeliveryPlan 10 · Guarantee 6 · ExpiryWarning 6 · AccountingFlags 5 xanh.
Playwright :3061: form Sửa HĐ 3443 (hạn dự kiến, mốc Giao hàng chọn đợt, lỗi thứ tự mốc dưới ô, tab đỏ, 1440/1280 không tràn, khung bảng 430 → 156px),
màn xem HĐ 734 (thật: 2 lần "Chưa xác định"; giả lập đủ trạng thái + popup cập nhật mốc bắt buộc). e2e mới contracts-payment-schedule.spec.ts — CHƯA chạy.
Merge tester ở worktree tạm `wt-merge-tester-p35` (api `dd48db00e`, client `c568a7e99`), CHƯA push.
Bước tiếp theo: user cho push → deploy hrm_crm (migration 2026_11_12_000004 + 000005, route:cache, queue:restart, build client Node 14 + pm2 reload).
Blocked:
### Checkpoint — 2026-11-12 (wrap up)
Vừa hoàn thành: Phase 35 đã push tester (api `dd48db00e`, client `c568a7e99`) — CHƯA deploy hrm_crm (user chỉ cho push).
Trong ngày: Phase 33 (cảnh báo hết hiệu lực) + Phase 34 (kế hoạch giao hàng) đã push + deploy hrm_crm; Phase 35 push.
Đang dở: —
Bước tiếp theo: (1) user cho deploy Phase 35 lên hrm_crm: pull 2 repo, pretend + chạy lẻ 2026_11_12_000004 + 000005 (đếm dòng GIAO_HANG_2 trên hrm_crm trước),
route:cache, queue:restart, build client Node 14 + pm2 reload hrm-client-crm; (2) chạy bộ e2e mới (contracts-expiry-warning, contracts-delivery-plan,
contracts-payment-schedule) khi user yêu cầu; (3) đợt 4 phụ lục điều chỉnh điều khoản, đợt 5 mẫu in (bàn với a Nam).
Ghi nhận: ContractHthtStepFlowTest 1 ca hỏng do dữ liệu rehearsal (NV 13 mất quyền BGĐ duyệt HĐ), không do code. Merge gop_db chỉ khi user yêu cầu.
Blocked:
### Checkpoint — 2026-11-12 (deploy Phase 35)
Vừa hoàn thành: deploy Phase 35 lên hrm_crm — migration 2026_11_12_000004 + 000005 chạy lẻ (0 dòng dùng GIAO_HANG_1/2; mã 5 is_active=0), route:cache (route payment-events → 401 không token),
queue:restart, lịch assign:warn-payment-schedule 08:10, client build Node 14 + pm2 reload hrm-client-crm.
Bước tiếp theo: chạy bộ e2e mới khi user yêu cầu; đợt 4 phụ lục / đợt 5 mẫu in.

## Fix 17/11 — Lịch sử HĐ bán theo khuôn chuẩn (TPE báo 23/10: "Lịch sử không theo form chuẩn SRS"; nhãn tiếng Việt đã xong từ trước)
Nhánh `gop_db-hd-dieu-kien-duyet` (worktree wt-hd-dieu-kien-duyet), KHÔNG migration. Khuôn copy: Báo giá (`QuotationHistoryService` + `SystemLogService::quotationLogs` + `QuotationHistoryModal`).
- [x] BE `ContractHistoryService` (mới): snapshot giá trị hiển thị form Sửa (24 ô + 4 bảng con: Điều chỉnh giá hàng hoá · Phòng thực hiện · Kế hoạch giao hàng · Tiến độ thanh toán; lời văn mẫu in chỉ ghi "Đã chỉnh sửa"), diff dùng `QuotationHistoryService::diff`, lưu `meta.old_value/new_value` (cột meta có sẵn). Không đổi ⇒ không ghi (trước đây mỗi lần Lưu đẻ 1 dòng "Chỉnh sửa" trống).
- [x] BE `ContractService::update` gọi snapshot trước/sau; `ContractController` upload/xoá đính kèm ghi "File đính kèm" thêm/bớt.
- [x] BE nhãn action 1 nguồn `ContractHistory::ACTION_LABELS` (update = "Thay đổi thông tin") + `ACTION_COLORS`; Resource dùng lại.
- [x] BE `SystemLogService::contractLogsFor` (TYPE_CONTRACT): 3 nhóm lọc (dòng không đổi trạng thái ⇒ update), ngày mốc / bảo lãnh / mốc thanh toán / kế hoạch giao hàng cũ → mới, ý kiến Pháp chế vào ghi chú, ẩn giá ⇒ bỏ ô tiền + ghi chú.
- [x] Route `assign/system-logs/contract/{id}` (+ filter-options) khai TRƯỚC route chung, trỏ `ContractController::histories` ⇒ đi qua `findViewableContract` (403/404 + hide_price).
- [x] FE màn xem HĐ: tab Lịch sử = `SystemInfoSection` (default-opened, hide-header, dựng khi mở tab lần đầu, key theo số dòng). Màn danh sách: menu ⋮ "Lịch sử" ⇒ `CatalogHistoryModal` "Lịch sử hợp đồng: <mã>".
- [x] PHPUnit `ContractHistoryLogTest` 4/4 (có ca không quyền 403) + 8 bộ HĐ cũ xanh. Playwright :3061 đo DOM. e2e mới `contracts-history.spec.ts` 3/3; sửa D4 `contracts-detail-layout`; chạy lại detail-layout + filter + history: 16 passed.

### Ghi nhận ngoài luồng (chưa sửa — lỗi có sẵn, lộ ra khi kiểm lịch sử)
- ~~**Ngày hết hạn lùi 1 ngày mỗi lần Lưu nháp HĐ**~~ ĐÃ SỬA 17/11 (xem Fix bên dưới): DB `expiry_date=2027-10-24` ⇒ API chi tiết trả `"2027-10-23T17:00:00.000000Z"` (UTC) ⇒ form hiện 23/10 ⇒ Lưu gửi nguyên chuỗi ⇒ BE lưu 2027-10-23. Kiểm bằng Playwright chặn PUT (17/11, HĐ 3443). Chưa lần tới cast/serialize của cột (chưa kiểm xong gốc ở `$casts`/`serializeDate`). Có thể cùng lỗi với `sign_date` / ngày khác dạng date.
- Lưu nháp không sửa lời văn vẫn bật cờ "Sửa mẫu in (cần Pháp chế duyệt)" (HĐ 3443) — chưa kiểm gốc.
- Console: `[Vue warn] computed "errors" already defined in data` ở `ContractDeliveryPlanUpdateModal`.

### Checkpoint — 2026-11-17 (fix Lịch sử HĐ xong, CHƯA commit)
Vừa hoàn thành: lịch sử HĐ theo khuôn chuẩn (BE + FE + PHPUnit + e2e), worktree wt-hd-dieu-kien-duyet, chưa commit.
Đang làm dở: —
Bước tiếp theo: user xem / báo commit; hỏi user có sửa lỗi Ngày hết hạn lùi 1 ngày không.
Blocked:

## Fix 17/11 — Ngày ký / Ngày hết hạn / Ngày cấp CCCD lùi 1 ngày mỗi lần Lưu (user cho "làm" 17/11)
Gốc (tinker có rollback + Playwright chặn PUT): `DetailContractResource` trả Carbon của cột cast `date:Y-m-d` ⇒ JSON giờ UTC
("2027-10-25T17:00:00Z" cho 26/10; cast format chỉ áp ở toArray) ⇒ form Sửa hiện lệch 1 ngày, Lưu gửi nguyên chuỗi ⇒ cast lưu ngày UTC.
- [x] `DetailContractResource::dateOnly()` — sign_date / effective_date / expiry_date / customer_id_card_date / validity_date trả "Y-m-d".
- [x] `ContractService::normalizeDateInputs()` đầu `update()` — chuỗi ngày có giờ (tab mở từ trước bản vá) đổi về giờ app rồi lấy ngày.
- [x] PHPUnit `ContractDateRoundTripTest` 3/3 (gỡ tạm bản vá ⇒ 3/3 fail, đã trả lại); 10 bộ PHPUnit HĐ xanh.
- [x] Playwright :3061 HĐ 3443: API 2027-10-26 · form 26/10/2027 · 2 lần Lưu nháp PUT 2027-10-26 · DB giữ nguyên. Khôi phục HĐ 3443 từ mysqldump (kèm SET TIME_ZONE).
- [x] e2e: contracts-detail-layout 7/7 + contracts-history 3/3 xanh. contracts-form-422 E422-1 fail VÌ nhánh chưa có fix `8275d6a0c` (chỉ ở gop_db-xuat-hang-cha-con) — không liên quan; contracts-form-layout 12 skip (rehearsal không có báo giá trúng thầu chưa lập HĐ).
- [ ] Dữ liệu cũ đã bị lùi ngày: chưa rà — hỏi user (dev hrm_crm hiện 1 HĐ).
- Ghi thêm cho lỗi "cờ Sửa mẫu in tự bật": lần Lưu 17/11 md5(template) KHÔNG đổi mà vẫn ghi legal_edit_on ⇒ cờ bật không do lời văn đổi (chưa kiểm gốc `resolveTemplateFields`).

### Checkpoint — 2026-11-17 (fix lùi ngày xong, CHƯA commit)
Vừa hoàn thành: fix ngày lùi 1 ngày + fix Lịch sử HĐ (cùng worktree wt-hd-dieu-kien-duyet, chưa commit).
Đang làm dở: —
Bước tiếp theo: hỏi user rà dữ liệu cũ bị lùi ngày; lỗi cờ "Sửa mẫu in" tự bật; đợt 4 Phụ lục.
Blocked:

## Fix 17/11 — Menu "Xem hỗ trợ hạch toán" ở danh sách HĐ (user chốt phương án 1 "mọi trạng thái" + "làm")
Khảo sát ERP: `ContractDatatable` menu "Xem hỗ trợ hạch toán" (preview) khi `Contract::canViewSupportAccounting` = Đang tạo/Chờ duyệt/Chờ hiệu lực + !ẩn giá.
HRM trước: danh sách chỉ có "Duyệt" (is_can_approve); màn xem HĐ nút "Hỗ trợ hạch toán" trừ Đang tạo/Chờ TP duyệt/Không duyệt (ngược ERP).
- [x] BE cờ `is_can_view_support_accounting` = !hide_price && !đang có Duyệt — `ContractResource` + `DetailContractResource` cùng công thức.
- [x] FE danh sách: mục "Xem hỗ trợ hạch toán" (ri-calculator-line) → `/assign/contracts/{id}/support-accounting` (màn đã có vai viewer chỉ xem).
  Màn xem HĐ: `canViewHtht` dùng cờ BE; bỏ 2 hằng thừa STATUS_CHO_DUYET / STATUS_DANG_TAO.
- [x] PHPUnit `ContractViewSupportAccountingFlagTest` 3/3 (8 trạng thái, ẩn giá, Duyệt loại trừ; 2 Resource khớp) + 10 bộ HĐ xanh.
- [x] Playwright :3061: HĐ 3443 (Đang tạo) + 734 (Đang thực hiện): menu danh sách có "Xem hỗ trợ hạch toán" = nút màn xem HĐ; bấm ⇒ màn HTHT chỉ Quay lại;
  API HTHT 200 (Đang tạo = regulation, Đang thực hiện = saved).
- [x] e2e: FLAGS_OFF thêm cờ mới; sửa F8 (tab Lịch sử đọc system-logs). approval-flow + detail-layout + filter + history: chỉ F42, F44 fail — lỗi CÓ SẴN (dưới).

### Ghi nhận ngoài luồng — form Sửa HĐ luôn "còn thay đổi chưa lưu" (F42, F44 fail)
`edit.vue` `detailSnapshot()` có `delivery_batches` (Phase 34) nhưng mốc mixin `unsavedSnapshotSource()` không có ⇒ mở form là `detailChangedUnsaved = true`
(đo Playwright 17/11 HĐ 3443: diff duy nhất `.delivery_batches` null vs []). Hệ quả: luôn hiện "Lưu nháp để cập nhật bảng hàng hoá…", popup Xem bản in luôn câu "chưa lưu".
Không do đợt 17/11 (edit.vue không đổi). Có thể liên quan cảnh báo thoát khi chưa lưu — chưa kiểm.

### Checkpoint — 2026-11-17 (menu Xem HTHT xong, CHƯA commit)
Vừa hoàn thành: menu Xem HTHT + fix lùi ngày + fix Lịch sử (worktree wt-hd-dieu-kien-duyet, chưa commit).
Đang làm dở: —
Bước tiếp theo: hỏi user sửa lỗi form Sửa luôn "chưa lưu" (F42/F44); cờ "Sửa mẫu in" tự bật; rà dữ liệu cũ lùi ngày; đợt 4 Phụ lục.
Blocked:

## Fix 17/11 — Form Sửa HĐ vừa mở đã "chưa lưu" (user cho "làm" 17/11)
Gốc: Phase 34 (`be9c9a7d0`) thêm `delivery_batches` vào `detailSnapshot()` nhưng không vào `unsavedSnapshotSource()` (nguồn mốc của unsavedChangesMixin).
- [x] `edit.vue` `unsavedSnapshotSource()` thêm `delivery_batches: this.deliveryBatchesPayload()` (cùng dạng detailSnapshot). Không đụng mixin dùng chung.
- [x] Playwright :3061 HĐ 3443, chặn mọi lệnh ghi — TRƯỚC: mở form dirty=true, sửa-rồi-trả-lại vẫn dirty, chỉ sửa kế hoạch giao hàng rồi rời màn KHÔNG hỏi;
  SAU: false / false / hiện "Thông tin chưa lưu" + ở lại. Màn Lập: không cảnh báo giả.
- [x] e2e thêm DLV-3 (contracts-delivery-plan). Chạy delivery-plan + approval-flow + payment-schedule + guarantee-execution-base + bgd-reasons + detail-layout + history: 76 passed, 0 failed (F42, F44 xanh lại).

### Checkpoint — 2026-11-17 (fix form "chưa lưu" xong, CHƯA commit)
Vừa hoàn thành: 4 việc 17/11 (Lịch sử, lùi ngày, menu Xem HTHT, form "chưa lưu") — worktree wt-hd-dieu-kien-duyet, chưa commit.
Đang làm dở: —
Bước tiếp theo: user báo commit; cờ "Sửa mẫu in" tự bật; rà dữ liệu cũ lùi ngày hrm_crm; đợt 4 Phụ lục.
Blocked:

## Khảo sát 17/11 — Cờ "Sửa mẫu in" tự bật khi Lưu dù lời văn không đổi (CHỈ ĐỌC, chưa sửa gì)
- [x] Gốc trên HĐ 3443 (tinker, không ghi DB): `resolveTemplateFields` so lời văn gửi lên với `template_original` (không phải lời văn đang lưu).
  Lời văn 3443 cùng 4.144 từ với bản chụp nhưng có thêm `<p style="margin-bottom:8px;margin-top:8px;text-align:justify"></p>` trước "ĐIỀU 1" ⇒
  `normalizeLayout` lệch ⇒ cờ 1 mỗi lần Lưu.
- [x] Dữ liệu 3443 bất thường: lịch sử cuối `legal_edit_on` 08/11 16:09:29 = `updated_at` HĐ, nhưng cờ đang 0 ⇒ bị đặt 0 bằng lệnh ghi thẳng DB
  (khả năng dọn dữ liệu sau e2e 08/11). Đi đúng luồng app thì cờ 0 luôn kèm lời văn = bản chụp hoặc bản đã qua phép so dàn trang ⇒ chưa thấy lỗi code.
- [x] Luật không đồng nhất: `<p></p>` trần = dàn trang (test 08/11), nhưng `<p style="margin/justify"></p>` và `<p style="text-align:justify">&nbsp;</p>` = bật cờ.
  CHƯA đo Enter trên trình soạn thật ra thẻ gì (editor `ENTER_DIV`).
- [x] 18/11 user chọn (1) + "làm": UPDATE `need_legal_approval=1` HĐ 3443 trên `hrm_erp_rbac_rehearsal` (giữ `updated_at`, không thêm lịch sử). Backup dòng: scratchpad session 0d64b5cf `hrm_contracts_3443_backup.sql`. Đọc lại: cờ 1, lịch sử 16 dòng, cuối 3827 `legal_edit_on` ⇒ khớp. Luật so lời văn GIỮ NGUYÊN.

### Checkpoint — 2026-11-17 (wrap up)
Vừa hoàn thành: 4 fix 17/11 (Lịch sử chuẩn, ngày lùi 1 ngày, menu Xem HTHT, form "chưa lưu") + khảo sát cờ "Sửa mẫu in" — worktree wt-hd-dieu-kien-duyet, CHƯA commit.
Đang làm dở: —
Bước tiếp theo: user chọn hướng cho cờ "Sửa mẫu in" (1/2/3); user báo commit; rà dữ liệu cũ lùi ngày hrm_crm (chỉ đọc); đợt 4 Phụ lục.
Blocked:

### Checkpoint — 2026-11-18 (cờ Sửa mẫu in: chọn phương án 1, đã sửa dữ liệu rehearsal)
Vừa hoàn thành: HĐ 3443 rehearsal cờ need_legal_approval 0 → 1 cho khớp lịch sử. Không đụng code.
Đang làm dở: —
Bước tiếp theo: user báo commit 4 fix 17/11 (wt-hd-dieu-kien-duyet); rà dữ liệu cũ lùi ngày hrm_crm (chỉ đọc); đợt 4 Phụ lục.
Blocked:

## Đợt 4 — Phụ lục điều chỉnh điều khoản (mục 13) — BRAINSTORM, chưa design, chưa code
Khảo sát 18/11 (đọc code ERP + đếm DB rehearsal):
- ERP HĐ hãng (`FirmContract`, bảng `firm_contracts`): phụ lục nằm chung bảng theo `type` — PL bổ sung (2, 1.141 dòng), PL giảm (3, 1.067 dòng),
  HĐDA PLBS/PLG (5/6), HĐNT PLBS (9), DHNT PLG (10). Đều là phụ lục HÀNG HOÁ / giá trị, không phải điều khoản.
  Controller `Sale/Firm/FirmContractAnnexesController`, `FirmContractAdditionAnnexesController`; view `resources/views/sale/firm/{annexes,addition_annexes}`.
- ERP phụ lục điều khoản: `ContractTermAnnexController` + `App\Model\Sale\ContractTermAnnex` (bảng `contract_term_annexes`) — chỉ gắn bảng HĐ CŨ `contracts`
  (`Contract::canTermAnnex`: người lập + HĐ Có hiệu lực). Văn bản thuần: `template` (lời văn) + đính kèm bắt buộc khi gửi duyệt + người duyệt/chức vụ tự chọn,
  3 trạng thái Đang tạo/Chờ duyệt/Đã duyệt (Không duyệt ⇒ về Đang tạo, bắt lý do), in bằng `print_data` HĐ + `SO_PHU_LUC`. KHÔNG đổi dữ liệu HĐ.
  Rehearsal: **0 dòng** ⇒ gần như không dùng.
- Điểm đặt ra cho user: phụ lục chỉ là văn bản ⇒ cảnh báo đợt 3 (hết hiệu lực / giao hàng / thu tiền) vẫn chạy theo số cũ; phụ lục sửa số liệu HĐ ⇒ phải lưu bản cũ/mới,
  tính lại cảnh báo, lịch sử — lớn hơn nhiều.
- [ ] Câu hỏi đang chờ user (hỏi mở): khi HĐ đã hiệu lực, khách thường cần phụ lục điều chỉnh những điều khoản gì, và mong hệ thống làm gì sau khi phụ lục được duyệt?
- Liên quan: mục 1 (ghi chú nội bộ mã hàng ở phụ lục), điều kiện V/IX chuyển BGĐ cho phụ lục (design-phase31).

### Checkpoint — 2026-11-18 (wrap up)
Vừa hoàn thành: cờ "Sửa mẫu in" HĐ 3443 rehearsal 0 → 1 (phương án 1, không đụng code); khảo sát ERP cho đợt 4 Phụ lục.
Đang làm dở: brainstorm đợt 4 — chờ user trả lời câu hỏi mở ở trên (đang ở bước hiểu nhu cầu, chưa đưa phương án).
Bước tiếp theo: nghe user mô tả ⇒ đưa 2–3 phương án (văn bản thuần như ERP / phụ lục sửa số liệu HĐ / kết hợp) ⇒ design-phase36 + mockup.
Việc khác còn treo: user báo commit 4 fix 17/11 (wt-hd-dieu-kien-duyet); rà dữ liệu cũ lùi ngày hrm_crm (chỉ đọc); đợt 5 mẫu in (bàn với a Nam).
Blocked: —

## Đợt giảm giá trên HĐ — dữ liệu test (20/11)
- Rehearsal `hrm_erp_rbac_rehearsal` (worktree wt-hd-dieu-kien-duyet, API :8061 / client :3061), tài khoản namdangit, tạo qua UI:
  - BG-2026-00550 (id 551, GG mặt hàng 10/5/0/3% = 6.375.000) → HĐ **10502** `HĐ_TPE_CTV_NV_26_0001_TEST-GG-DONG-550` (Đang tạo).
  - BG-2026-00552 (id 553, GG tổng 10.000.000 phân bổ tự động) → HĐ **10503** `HĐ_TPE_CTV_NV_26_0002_TEST-GG-TONG-552` (Đang tạo).
  - Rác: BG 547/549 (hàng BENY trụ sạc Toyota chưa gắn tính chất ⇒ không lập được HĐ), đang Trúng thầu.
- Đã chạy 1 migration vào rehearsal (user cho phép): `2026_10_26_000001_add_demand_delivery_address_to_quotations_table`. Rehearsal còn 36 migration chờ khác.
- Ghi nhận: `allocated_discount_amount` GG tổng lưu số lẻ (3.729.784,57…), tổng vẫn đúng 10.000.000.
- Ghi nhận: sao chép báo giá không giữ Người liên hệ (phải chọn lại khi gửi duyệt) — lỗi màn báo giá, chưa sửa.
