# BBNT — Thêm cột Số HĐ + Công ty thực hiện + lọc

> @khoipv

## Yêu cầu
Màn `contract/acceptance_report` (danh sách BBNT): thêm cột **Số hợp đồng** (`contract.number`) và **Công ty thực hiện** (mã công ty — `contract.main_company.code`), thêm bộ lọc.

## Task
- [x] BE Resource `AcceptanceReportResource`: thêm `contract_number`, `main_company_code`.
- [x] BE Service `index`: eager load `contract.main_company`; thêm lọc `company_id` → `contract.main_company_id`. (lọc `contract_number` đã có sẵn)
- [x] FE `index.vue`: thêm 2 cột (Số HĐ, Công ty TH — mã); thêm bộ lọc Công ty (base-select2, `company_id`, dùng `$store.state.companies`); `initialStateForm` thêm `company_id`.

## Ghi chú
- "lấy mã thôi" → cột Công ty thực hiện chỉ hiển thị `code`.
- Bộ lọc "Số hợp đồng" (contract_number) đã tồn tại từ trước.

### Checkpoint — 2026-07-21
Vừa hoàn thành: 2 cột (Số HĐ = `contract.number`, Công ty TH = `contract.main_company.code`) + bộ lọc Công ty thực hiện (`company_id` → `main_company_id`).
Đang làm dở: chưa chạy nuxt dev xác nhận (Node 14, cần user chạy).
Bước tiếp theo: user mở /contract/acceptance_report kiểm tra 2 cột + lọc công ty.
Blocked:
