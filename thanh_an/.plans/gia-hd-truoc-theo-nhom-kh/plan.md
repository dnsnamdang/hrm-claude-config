# Giá bán HĐ trước — lọc theo nhóm khách hàng — @khoipv

Bắt đầu: 26/10/2026

## Yêu cầu
- KH thuộc **khối bệnh viện** (nhóm `BV` công lập + `TN` tư nhân, gộp chung) → đúng KH trước, không có thì lấy HĐ gần nhất của **KH khối BV khác cùng tỉnh**.
- KH **Công ty TM / Khách lẻ, HKD / chưa gán nhóm / nhóm khác** → **chỉ** lấy giá HĐ trước của đúng KH đó (bỏ fallback tỉnh).
- Nhóm lấy theo **danh mục KH hiện tại** (`category_customers.customer_group_id` → `customer_groups.code`), không dùng snapshot `contracts.customer_group_name`.

## Phase 1 — BE
- [x] `CustomerGroup::HOSPITAL_CODES = ['BV', 'TN']`
- [x] `ProductPriceService::getPreviousContractPrices()` — chỉ fallback tỉnh khi KH thuộc khối BV
- [x] `queryPricesByProvince()` — join `category_customers` + `customer_groups`, chỉ lấy HĐ của KH khối BV
- [x] Verify tinker: KH BV, KH TM, KH KL, KH không nhóm

## Phase 2 — FE
- Không cần sửa (FE chỉ gọi API + quy đổi ĐVT)

### Checkpoint — 26/10/2026
Vừa hoàn thành: Phase 1 BE — `CustomerGroup::HOSPITAL_CODES`, `ProductPriceService` chỉ fallback tỉnh khi KH thuộc khối BV + chỉ lấy HĐ của KH khối BV. Verify tinker trên `thanhan_stag_07052026` 4/4 PASS (BV 1808/SP 9 → giá HD-114/2026 nguồn tỉnh; TM 1847/SP 9 → rỗng; BV 3214/SP 2371 chỉ có HĐ của KH khác nhóm → rỗng; TM 1819/SP 2371 → giá HĐ chính mình HD-069/2026).
Đang làm dở: —
Bước tiếp theo: User test UI (báo giá / gói thầu / HĐ) — chỉ sửa BE, không cần build client. Giá đã lưu ở `price_pre_contract` của chứng từ cũ không tự tính lại.
Blocked:
