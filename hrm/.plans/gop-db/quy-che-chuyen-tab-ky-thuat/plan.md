# Quy chế – Chuyển tab "Kỹ thuật" & tách "Đơn giá công" — Plan

Xem `design.md` cùng thư mục. Nhánh `gop_db`. Giữ `tabKey = 'kythuat'`, giữ tên tab "Kỹ thuật".

## Phase 1 — BE (hrm-api)
- [x] `RegulationTabRegistry.php`: **dời** entry `work_price` (Đơn giá công) từ tab `kythuat` sang tab
      `giaban` (khối store=company). Giữ y nguyên key/label/unit; cột `companies.work_price` không đổi.
- [x] `kythuat` còn `work_bond` + `contract_rows` — giữ `scope=MIXED, shape=SCALAR`.
- [x] `php -l` sạch.
- [x] Cập nhật 3 test: `RegulationTabRegistryTest` (kythuat còn work_bond+contract_rows + thêm assert
      work_price∈giaban), `RegulationKythuatSubtableTest` (bỏ assert work_price), `RegulationScalarTabsTest`
      (`cron_applies_due` hẹn work_price qua tab `giaban`). **PHPUnit: 6 test / 33 assertions PASS.**

## Phase 2 — FE data.js (hrm-client)
- [x] Group `giaban`: thêm `num('Đơn giá công', 'đồng', 350000)`.
- [x] Group `kythuat`: **bỏ** dòng `num('Đơn giá công', ...)`; **thêm** `subsystem: 'assign'`; đổi `sub` →
      'Công khoán & bảng tính công khoán'. Giữ `name: 'Kỹ thuật'` + `work_bond` + subtable.

## Phase 3 — FE route + menu (hrm-client)
- [x] Tạo `pages/assign/regulation-config/index.vue` (`extends RegulationConfigScreen`, `subsystem:'assign'`).
- [x] `components/menu-sidebar.js` — nhóm "Thiết lập" của `menuItemsAssign`: thêm mục
      `{ label: 'Khai Quy chế – Cấu hình', link: '/assign/regulation-config', isShow: ['Cài đặt cấu hình'] }`.

## Phase 4 — Verify (Playwright MCP, DB erp_hrm_check local, tài khoản DNS Admin)
- [x] `/sale/regulation-config` (Bán hàng): KHÔNG còn tab "Kỹ thuật" (còn Chung, Báo giá–HĐ, Chiết khấu, Tổ chức bán hàng & thị trường, Hàng hóa, Điều khoản).
- [x] `/finance/regulation-config` → tab "Giá bán": field "Đơn giá công" hiển thị = 700.000 (đọc đúng `companies.work_price`), badge 5 field.
- [x] `/assign/regulation-config` (Công việc): 1 tab "Kỹ thuật" — "Công khoán" = 350.000 (đọc `companies.work_bond`) + "Bảng tính công khoán" (subtable `contract_rows` render đủ cột, 1 dòng SL=10).
- [x] Menu "Thiết lập" phân hệ Công việc: có mục "Khai Quy chế – Cấu hình".
- [x] Không tạo dữ liệu test (chỉ điều hướng/đọc) → không cần dọn.

## Checkpoint

**2026-09-23 — Verify PASS (Playwright MCP, DB erp_hrm_check local, DNS Admin).**
- Đường ghi (save) không test-live để tránh mutate DB gộp chung; đã phủ ở tầng service bằng feature test
  `RegulationScalarTabsTest` (work_price áp qua tab `giaban`, work_bond qua `kythuat`).
- Chưa commit — chờ user duyệt (ràng buộc CLAUDE.md: không commit khi chưa có yêu cầu).
- Lưu ý prod: nếu đã có phiên bản hẹn (`regulation_config` versions) chứa work_price dưới tabKey `kythuat`
  chưa áp → rà lại vì BE nay resolve work_price qua tabKey `giaban`.
