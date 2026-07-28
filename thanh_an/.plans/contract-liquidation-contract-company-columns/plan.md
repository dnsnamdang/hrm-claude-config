# Thanh lý HĐ — Thêm cột Số HĐ + Công ty thực hiện + lọc

> @khoipv

## Yêu cầu
Màn `contract/contract_liquidation` (danh sách biên bản thanh lý): thêm cột **Số hợp đồng** (`contract.number`) và **Công ty thực hiện** (mã công ty — `contract.main_company.code`), thêm bộ lọc cho 2 thông tin này.

## Task
- [x] BE Resource `ContractLiquidationResource`: thêm `contract_number`, `main_company_code`.
- [x] BE Service `index`: eager load `contract.main_company`; thêm lọc `contract_number` → `contract.number`, `company_id` → `contract.main_company_id`.
- [x] FE `index.vue`: thêm 2 cột (Số HĐ, Công ty TH — mã); thêm bộ lọc Số HĐ (base-input-field) + Công ty (base-select2, `company_id`, dùng `$store.state.companies`); `initialStateForm` thêm `contract_number`, `company_id`.

## Ghi chú
- "lấy mã th cty thôi" → cột Công ty thực hiện chỉ hiển thị `code`.
- Làm nhất quán với feature `acceptance-report-contract-company-columns` (BBNT đã làm y hệt).
- "Giá trị HĐ" đối chiếu = `summary.total_contract` (Giá trị HĐ gồm phụ lục — đúng con số hiển thị trên màn).

### Checkpoint — 2026-07-27
Vừa hoàn thành: BE (Resource + Service) và FE (2 cột + 2 bộ lọc).
Đang làm dở: chưa chạy nuxt dev xác nhận (Node 14, cần user chạy).
Bước tiếp theo: user mở /contract/contract_liquidation kiểm tra 2 cột + 2 bộ lọc.
Blocked:
