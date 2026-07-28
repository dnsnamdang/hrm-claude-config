# Plan — Hình thức thanh toán (theo đợt / theo đơn) + phân biệt HĐ chính / KPI

**Phụ trách:** @namdangit
**Spec:** `docs/superpowers/specs/2026-07-24-contract-payment-mode-design.md`
**Plan chi tiết (TDD):** `docs/superpowers/plans/2026-07-24-contract-payment-mode.md`

> Đã qua bước writing-plans → task chi tiết (10 task, code + verify đầy đủ) nằm ở plan chi tiết. Dưới đây là khung tổng quát theo Phase.

## Phase 1 — Database (BE)
- [ ] Migration thêm `payment_mode_main` + `payment_mode_kpi` vào `contracts`
- [ ] Migration thêm cột `block` vào `contract_payment_terms` + đổi unique (contract_id, block, term_code)
- [ ] Migration tạo bảng `contract_payment_installments` (index, không FK)
- [ ] Model `ContractPaymentInstallment` + bổ sung hằng block cho `ContractPaymentTerm`

## Phase 2 — Backend logic
- [ ] `StoreContractRequest`: rule cho payment_mode_*, payment_installments.*, payment_terms.*.block
- [ ] `ContractService` store/update: ghi mode + sync terms/installments theo mode từng block + xóa data mode ẩn + xóa block kpi khi has_kpi=0
- [ ] Tính lại `amount` = round(percent × baseTotal_block) ở BE
- [ ] `ContractDetailResource`: trả thêm payment_mode_*, payment_installments, block trong payment_terms

## Phase 3 — Frontend
- [ ] Component `PaymentBlockCard.vue` (header badge/dropdown + body dot/don, bảng đợt + cảnh báo mềm)
- [ ] Sửa `PaymentTermsTab.vue`: thêm prop `block`
- [ ] Sửa `GeneralComponent.vue` tab Điều khoản thanh toán: render 1-2 card + wire mainTotal/kpiTotal + formSubmit
- [ ] Mở rộng cơ chế "lưu sau duyệt" (hasPaymentTermChanges / submitPaymentTermsAfterApprove) cho installments + mode + 2 block

## Phase 4 — Verify
- [ ] BE live-verify (migrate, smoke store/update, kiểm tra sync + xóa mode ẩn)
- [ ] E2E qua UI: HĐ không KPI (1 card), HĐ có KPI (2 card khác mode), đổi mode, tổng % cảnh báo, sửa sau duyệt

---

## Execution ledger (Subagent-Driven)
- [x] Task 1: migration payment_mode → contracts — DONE, review sạch
- [x] Task 2: cột block + đổi unique + bỏ FK — DONE, review sạch (Minor: chưa test runtime down())
- [x] Task 3: bảng contract_payment_installments + model — DONE, review sạch
- [x] Task 4: validate StoreContractRequest — DONE, review sạch
- [x] Task 5: ContractService sync — DONE, review tìm 2 Critical (has_kpi lấy từ request → xóa nhầm data kpi khi lưu-sau-duyệt; modeKpi fallback null). ĐÃ FIX (dùng $contract->has_kpi + fallback 'don') + verify data kpi sống sót
- [x] Task 6: ContractDetailResource trả field mới — DONE, review sạch (v0-snapshot giữ nguyên)
- [x] Task 7: PaymentTermsTab prop block — DONE, tự verify (block+showNote+filter)
- [x] Task 8: PaymentBlockCard.vue — DONE, review APPROVED. Fix Important (sumPercent làm tròn tránh cảnh báo giả) + Minor (step=0.01). Compile OK
  - **Sửa theo phản hồi user 2026-07-24**: bỏ toàn bộ màu (badge-color/border-left/mode-chip), header gọn (chỉ tên khối + tổng giá trị), đổi dropdown mode `b-form-select` → `base-select2` (options {id,text}, `:value`+`@input`, global auto-import). GeneralComponent bỏ prop badge-color, badge đổi sang chữ thường "Hợp đồng chính"/"Hàng KPI". Compile OK.
  - **Sửa input bảng "theo đợt" 2026-07-24**: input trần → base có sẵn. Nội dung + Tỷ lệ % → `base-input-field` (ô % dùng `unit="%"`, `class-input="text-right"`, min/max/step qua $attrs); Thời gian → `base-date-picker` (valueType YYYY-MM-DD khớp pay_date, dùng trần như convention trong table cell). pay_date khởi tạo `null` thay `''`. Handler @input nhận value trực tiếp (base emit value, không phải event.target). Compile OK.
  - **Sửa nút thêm/xóa 2026-07-24**: theo convention module contract — nút thêm `b-button` → `base-add-button` (plus.svg, v-if="!isLocked", kèm label "Thêm đợt thanh toán"); nút xóa `b-button outline-danger ×` → `b-button variant="secondary" class="btn-small"` + `trash.svg`. Compile OK.
- [x] Task 9: GeneralComponent nối 2 card + change tracking — DONE, review Spec ✅ Approved. Base total tính reactive từ groups/group_kpis (formSubmit.total không tồn tại ở màn add). Đã dọn dead import PaymentTermsTab. Compile OK
- [x] Task 10: verify tổng thể — DONE headless: php -l 9 file BE sạch; 3 migration Ran; schema xác nhận (payment_mode_main/kpi, block, bảng contract_payment_installments đủ cột); route updatePaymentTermsAfterApprove tồn tại; 3 component FE compile OK; smoke ContractDetailResource runtime trả đủ payment_mode_*/payment_installments (collection), mode=dot→terms=0 (cleanup mode ẩn chạy đúng). **E2E-UI: giao user tự bấm** (dev server chưa chạy — không tự bật Node 14 client). Checklist ở dưới.
> Lưu ý pre-flight: Task 2 đã vá — phải dropForeign trước dropUnique (FK dùng chung index), bỏ FK theo convention.
> **Fix 2026-07-24 (sót comment)**: bổ sung `->comment()` cho mọi cột trong 3 migration theo `docs/conventions.md` §Migration ("Luôn viết comment cho mỗi trường"). 3 file lint sạch. User đồng ý bỏ 1 HĐ test → đã `migrate:rollback --step=3` (batch 255/256/257) + `migrate` lại. Xác nhận comment đã vào DB thật qua INFORMATION_SCHEMA.COLUMNS (đủ 12 cột nghiệp vụ; id/created_at/updated_at không comment là đúng).

## Checkpoint — 2026-07-24 (Task 9-10 xong)
Vừa hoàn thành: Task 9 (GeneralComponent nối 2 card + change tracking, review Approved) + Task 10 (verify headless toàn bộ BE+FE sạch)
Đang làm dở: Không — 10/10 task code xong
Bước tiếp theo: (1) User bấm E2E checklist qua UI; (2) đã dispatch final whole-branch reviewer
Blocked: E2E qua UI cần user bật dev server (API + Node 14 client)

### Review cuối (whole-branch, opus) — Verdict: READY (có điều kiện)
Không Critical. Đối chiếu đạt: data-loss sync (cleanup chạy cuối, mọi thao tác where('block')), thứ tự total-trước-installments, has_kpi lấy từ $contract, base total BE↔FE khớp, round-trip block, reactivity $set, convention không-FK + không đụng TotalComponent, pay_date trả 'YYYY-MM-DD' thuần.
- **Important #1 (CHỜ user quyết — đụng logic dùng chung)**: bất đối xứng đọc-lại SAU DUYỆT. `ContractDetailResource` đọc `payment_terms`/`payment_terms_note` từ snapshot **v0** (do feature Phụ lục 2026-07-07 thêm), nhưng `payment_installments`/`payment_mode_*` đọc **live**. `updatePaymentTermsAfterApprove` chỉ ghi live, không cập nhật v0 → HĐ đã duyệt sửa điều khoản (mode don) không hiển thị lại (data vẫn trong DB live). Vốn có từ trước feature này; luồng TRƯỚC duyệt hoàn toàn đúng. 3 hướng: (A) để nguyên/tách task riêng [đề xuất]; (B) cho terms/note đọc live — rủi ro làm sai màn Phụ lục in Cũ→Mới; (C) updatePaymentTermsAfterApprove embed lại snapshot v0. → **USER CHỌN (A) 2026-07-24: để nguyên, tách task riêng sau. Không sửa trong feature này.**
- Minor #2: rule `payment_mode_kpi` nullable (spec §7 nói bắt buộc) — GIỮ NGUYÊN, đổi required_if sẽ chặn nhầm submit (FE chỉ emit mode khi chạm dropdown); service đã fallback 'don'.
- Minor #3: luồng phụ lục (`getDataForAnnexPaymentTerms`) chưa mang block/installments — out-of-scope theo spec §10.
- Minor #4: PaymentBlockCard rebuild rows mỗi keystroke — chấp nhận, không mất data.

### E2E checklist (user bấm tay trên màn contract/contract/add)
- [ ] HĐ KHÔNG KPI: tab Điều khoản thanh toán chỉ hiện 1 card "HỢP ĐỒNG CHÍNH"
- [ ] HĐ CÓ KPI (has_kpi=1): hiện 2 card — "HỢP ĐỒNG CHÍNH" (xanh) + "HÀNG KPI" (cam), mỗi card chọn hình thức riêng
- [ ] Đổi "Theo đợt": hiện bảng đợt, thêm/xóa đợt, nhập % → cột Số tiền tự tính theo tổng gốc khối, tổng % ≠ 100 cảnh báo mềm
- [ ] Đổi "Theo đơn": hiện lại bảng 4 điều khoản (100PCT/TIME/VALUE/ROLLING), logic exclusive giữ nguyên
- [ ] Ghi chú chung nằm ngoài 2 card, lưu đúng
- [ ] Lưu HĐ → reload/mở lại: mode + đợt + điều khoản từng khối nạp đúng
- [ ] HĐ đã duyệt: sửa điều khoản/đợt/mode → nút "Lưu" bật (hasPaymentTermChanges), submit updatePaymentTermsAfterApprove OK, data KPI không bị mất
