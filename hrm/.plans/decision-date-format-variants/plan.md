# decision-date-format-variants — Plan

Spec: `docs/superpowers/specs/2026-07-14-decision-date-format-variants-design.md`
Plan chi tiết (code từng bước): `docs/superpowers/plans/2026-07-14-decision-date-format-variants.md`

## Phase 1 — Nền tảng
### BE
- [x] T1. Helper.php: thêm `formatDateVICapital` + `formatDateVICapitalInline` + `fillDateVariants(&$result, base, date, legacyFormat)`
- [x] T2. PrintTemplateVariable.php: đánh cờ `is_date` + `expandDateVariables` (tự sinh _CHU/_SO, ẩn gốc) + wire vào buildSubTypeVariables & buildObjectsForGroup

## Phase 2 — Đổ giá trị (value-fill)
### BE
- [x] T3. DecisionService: 3 biến chung (NGAY_QUYET_DINH/NGAY_KY/NGAY_HIEU_LUC)
- [x] T4. Controller "chu": Appoint, Transfer (2 khối), Retirement, IncreaseSeniority
- [x] T5. Controller inline "so": Accept, Renew, Suspend (2 khối), Termination
- [x] T6. EmployeeDiscipline (composite THOI_GIAN_KY_LUAT) + DecisionRegulationSalary
- [x] T7. HĐLĐ: DecisionLaborContract (2 khối, keep + composite) + AppendixLaborContract
- [x] T8. HĐ đào tạo (TrainingContract) + Biên bản (TroubleShooting)

## Phase 3 — Verify
- [x] T9. In thử QĐ chấm dứt HĐLĐ (tinker $result 3 khóa/ngày) + Playwright picker (tùy chọn) + wrap up
- [x] T10 (final review fix). RegulationGeneralController (mẫu Quy chế chung — sót trong inventory) → NGAY_QUYET_DINH qua fillDateVariants

### Checkpoint — 2026-07-14
Vừa hoàn thành: Toàn bộ 9 task + fix final-review (RegulationGeneral). 18 file BE sửa, php -l sạch, tinker verify picker (6 loại mẫu) + value-fill (Decision#689, RegulationGeneral) OK.
Đang làm dở: (không)
Bước tiếp theo: user hard-refresh trình duyệt, mở /decision/category/print_templates/add chọn loại QĐ → xác nhận picker hiện 2 dòng/ngày; soạn mẫu chèn _CHU/_SO + in thử 1 quyết định thật. Không git/migration.
Blocked:
