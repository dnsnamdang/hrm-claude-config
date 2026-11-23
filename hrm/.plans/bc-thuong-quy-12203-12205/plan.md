# BC thưởng theo quý #12203 #12205 — plan

Spec: `design.md` (cùng thư mục). Người làm: @nguyentrancu97 · Nhánh: hrm-api / hrm-client `develop`.

## Tiến độ
- 19/11: UI phân cấp + Tùy chỉnh cột + phân trang theo dòng HĐ như ERP — api `ebb3eaaad` `63001e8e6` · client `36eed0351`.
- 21/11: popup chi tiết + export (đợt Redmine dt 21/11, xem `.plans/redmine-dt-2111/plan.md`) — client `b96a90a8a`, api `c2f34b301`.
- 23/11: Bug 3 (số lệch ERP) rà lại — code đúng, lệch do dev-hrm chưa deploy bản 19/11; không sửa.
- 23/11: **QA phản hồi "tiêu đề vẫn lỗi"** — tiêu đề tràn sang cột bên, icon ⓘ bị che, cột cuối tràn mép bảng.
  - Nguyên nhân: 6 cột tiền cố định `width: 200`, tiêu đề `nowrap` dài tới ~208px (Roboto 800 12px) + ⓘ + padding.
  - Sửa (chỉ `BonusQuarterTable.vue`, không đụng layout chung): `AMOUNT_WIDTHS` theo từng cột 190–270px; tổng min-width 2.179px, cuộn ngang.
  - Kiểm Playwright local (2026 / kỳ 2): mọi `th` không tràn (`scrollWidth <= clientWidth`), ⓘ nằm trong ô, cột cuối gọn.
  - ĐÃ push develop client `35e6f94b0`; Redmine #12205 → "Code xong chờ test". Chưa gop_db.
