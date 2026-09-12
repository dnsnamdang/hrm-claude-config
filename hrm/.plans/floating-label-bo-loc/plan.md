# Plan — Floating label cho ô lọc phân hệ assign

- **Phụ trách:** @dnsnamdang · **Nhánh:** `tpe`
- Design tóm tắt: `.plans/floating-label-bo-loc/design.md`
- Spec đầy đủ: `docs/superpowers/specs/2026-08-31-floating-label-filter-assign-design.md`

---

## Phase 1 — Component dùng chung + màn pilot (XONG)

### FE

- [x] **Task 1** — Prop `height` (String, mặc định `null`) cho `V2BaseSelect` + `V2BaseSelectInModal`;
      `updateHeight()` ưu tiên prop. Bắt buộc vì method này ghi inline `!important`, CSS ngoài
      không đè nổi. Mặc định `null` nên 0 màn nào khác đổi — đã đo `/assign/customers` vẫn 32px.
- [x] **Task 2** — Tạo `components/V2BaseFloatingField.vue`: vỏ thuần, control nằm trong slot,
      3 biến thể (thường / `range` / `tags`), trạng thái `is-float` / `is-focus` / `is-error` /
      `is-disabled`. Dùng lại `V2BaseFieldHint` + từ điển `getFieldHintByLabel` để giữ tooltip ⓘ.
- [x] **Task 3** — `V2BaseFilterPanel`: khai `--panel-bg: #fff` trên `.tp-card`.
      Page: `.filter-grid { row-gap: 18px }` (trước là `mb-2` = 8px, quá hẹp cho nhãn float).
- [x] **Task 4** — Migrate 10 ô page tự render: 7 ô Select2 + 2 ô autocomplete Khách hàng
      (nút `×` chuyển vào slot `suffix`) + gộp "Ngày tạo từ/đến" thành 1 ô `variant="range"`.
      Bỏ 8 placeholder trùng nhãn.
- [x] **Task 5** — Prop `floating` cho `V2BaseCompanyDepartmentFilter` (4 khối: Công ty / Phòng ban /
      Bộ phận / Nhân viên). Regression: `/assign/customers` giữ nguyên 13 nhãn cũ + control 32px.
- [x] **Task 6** — Prop `floating` cho `CheckboxMultiSelect` (ô Ứng dụng). Bọc bằng
      `<component :is>` để không chép đôi ~50 dòng markup.
- [x] **Task 7** — Prop `floating` cho `CascadePairSelect` (2 ô: Loại hình + Lĩnh vực).
- [x] **Task 8** — Bộ e2e `e2e/tests/assign/prospective-projects-filter.spec.ts` — **18/18 xanh**.
- [x] **Task 9** — Cập nhật `.claude/skills/list-page/SKILL.md`: ngoại lệ placeholder + toàn bộ quy
      ước floating label + 4 cái bẫy.

### Chỉnh theo phản hồi nghiệm thu

- [x] **Task 10** — Hiệu ứng + màu viền focus lấy theo ô tìm nhanh: `#1976d2`, không quầng.
      (Đo ra rule `#16a34a` + quầng trong `V2BaseFilterPanel` bị `custom-theme.scss` đè mất.)
- [x] **Task 11** — Sửa viền select đè lên nhãn khi focus: `.ff` thành stacking context riêng
      (`z-index: 0`) + nhãn `z-index: 10000`, thắng `z-index: 9999` của `.select2-container--open`.
- [x] **Task 12** — 3 ô chip (Ứng dụng / Loại hình / Lĩnh vực) bỏ float vĩnh viễn, theo quy tắc
      chung như mọi select; đệm phải 30px → 10px; giấu placeholder riêng khi nhãn còn trong ô.
- [x] **Task 13** — Nhãn nằm TRONG ô để `font-weight: 400`, bay lên viền mới 600.

---

## Phase 2 — Nhân bản 76 màn còn lại (CHƯA LÀM)

Chưa mở. Khi làm, đọc `design.md` §4 (3 quyết định đã đổi) + §5 (4 cái bẫy) trước, và bám khuôn
`pages/assign/prospective-projects/index.vue`.

- [ ] Rà 77 màn assign dùng `V2BaseFilterPanel`, phân loại theo độ phức tạp ô lọc
- [ ] Nhân bản theo nhóm, mỗi nhóm kiểm Playwright trước khi sang nhóm sau
- [ ] Quyết định có áp cho `timesheet/timeworking/shift-history` không (màn duy nhất ngoài assign)
- [ ] Test thủ công zoom 110% / 125% (chưa tự động hoá được)

---

### Checkpoint — 2026-09-02

**Vừa hoàn thành:** Phase 1 đủ 13 task. Màn pilot `/assign/prospective-projects` chạy floating
label cho cả 16 ô; panel lọc **449px → 312px** (−31%), 5 hàng còn 4. e2e **18/18 xanh**.
Code đã nằm trong commit `3b4dc465c` ("fix bao cao cskh + filter styles") trên `tpe`,
working tree sạch — commit này do session khác gom, có lẫn cả file của Phase 13 màn CSKH.

**Đang làm dở:** không có.

**Bước tiếp theo:** user yêu cầu **dừng ở màn thử nghiệm**, mở rộng sau. Khi mở lại → Phase 2.

**Blocked:**
- Chưa chạy lại toàn bộ `e2e/tests/assign` sau 4 task chỉnh nghiệm thu (lần chạy đầy đủ gần nhất:
  98 passed / 5 failed / 1 flaky / 19 did not run — đã truy 5 ca fail đều là dữ liệu + môi trường,
  không phải do thay đổi này, nhưng **chưa chứng minh tuyệt đối** bằng cách hoàn nguyên rồi chạy lại).
- `.claude/skills/list-page/SKILL.md` sửa tại chỗ, theo quy tắc team nên tách PR riêng.
