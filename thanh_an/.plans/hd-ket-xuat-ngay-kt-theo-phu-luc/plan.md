# HĐ đã kết xuất — đánh dấu "Ngày kết thúc" lấy theo phụ lục gia hạn

@khoipv — Bắt đầu 15/10/2026

## Yêu cầu
Cột "Ngày kết thúc" ở màn Cung ứng › HĐ đã kết xuất lấy `contracts.contract_end_time` — cột này bị ghi đè khi
duyệt phụ lục gia hạn thời gian (`ContractAnnexTimeService::approve()`). Thêm ký hiệu cạnh ngày để người dùng
biết ngày đó đang tính theo phụ lục.

## Quyết định
- Có ký hiệu khi: HĐ có phụ lục `annex_type = 'extend_time'`, `status = 3 (Đã duyệt)`, và ngày KT mới của phụ lục
  duyệt gần nhất **trùng** `contracts.contract_end_time` (ngày hiện tại đúng là do phụ lục ghi).
- Ký hiệu: icon nhỏ màu hổ phách cạnh ngày, rê chuột xem: mã + số phụ lục, ngày duyệt, ngày KT gốc (snapshot
  `contract_versions` tại version trước phụ lục gia hạn đầu tiên), số lần gia hạn nếu > 1.
- Lọc / sắp xếp / Excel giữ nguyên (vẫn theo `contracts.contract_end_time`).

## Phase 1 — BE
- [x] `RenderedContractService::getList()`: addSelect thông tin phụ lục gia hạn đã duyệt gần nhất + số lần + ngày gốc
- [x] `RenderedContractResource`: trả `end_time_annex` (null nếu ngày KT không lấy theo phụ lục)

## Phase 2 — FE
- [x] `pages/supply/contract_render/index.vue`: icon + tooltip ở ô `contract_end_time`

## Phase 3 — Verify
- [x] php -l + test tinker (transaction + rollback) với phụ lục gia hạn giả
- [x] Playwright `e2e/tests/supply/hd-ket-xuat-ngay-kt-phu-luc.spec.js` (seed PL giả cho HĐ đầu danh sách, afterAll dọn) — 3/3 pass, đã chạy headed
- [x] e2e: sinh lại ACCESS_TOKEN (user 13), `auth.setup.js` chờ avatar thay vì "Tổng số bản ghi:", config thêm `SLOW_MO`

### Checkpoint — 15/10/2026
Vừa hoàn thành: BE (getList thêm `end_time_annex`, `end_time_annex_count`, `end_time_original`; Resource trả `end_time_annex`) + FE (icon `ri-file-history-line` màu hổ phách + tooltip HTML có escape). Test script (DB local, transaction + rollback) 5/5: chưa PL → null; PL chờ duyệt → null; PL đã duyệt khớp ngày → có ký hiệu + ngày gốc; gia hạn 2 lần → lấy PL mới nhất, count=2, ngày gốc vẫn ngày trước lần 1; ngày KT bị sửa lệch PL → null.
Đang làm dở: —
Bước tiếp theo: user build client + test UI trên dev (DB local chưa có PL gia hạn thật)
Blocked:

### Checkpoint — 15/10/2026 (2)
Vừa hoàn thành: Playwright 3/3 pass (API + UI icon/tooltip + HĐ không gia hạn không có icon), DB đã dọn sạch.
Đang làm dở: —
Bước tiếp theo: user test trên dev với phụ lục gia hạn thật; quyết có ghi chú "(theo PL)" trong Excel không
Blocked:
