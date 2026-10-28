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
- [ ] TK ngân hàng Bên A màn Chi tiết thiếu tiền tệ ("VNĐ") so với màn Sửa — API chi tiết không trả `currency_name` của TK; cần thêm ở BE nếu muốn khớp hẳn (chờ user quyết).
- [ ] Dọn DB local khi user báo test xong: role tạm 108470 + 108473 (gắn NV 50) · khôi phục `menu_settings` ẩn (2 bản sao lưu ở scratchpad session 27/10: `menu_hidden_sale_admin_backup.json` 54 mục, `menu_hidden_all_backup.json` 71 mục) · BG-2026-00442 (id 501, test) · xoá cache quyền.
- [ ] E2E chưa kiểm được: Q2/Q3 danh sách (cấp bộ phận / phòng ban) — cần tài khoản test KHÔNG có cờ `company_employees.all_department`.

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
