# Design — Hình thức thanh toán (theo đợt / theo đơn) + phân biệt HĐ chính / KPI

**Trạng thái:** Đã chốt design, chờ user review spec
**Phụ trách:** @namdangit
**Ngày:** 2026-07-24
**Spec chi tiết:** `docs/superpowers/specs/2026-07-24-contract-payment-mode-design.md`
**Mock:** `demos/demo-lap-hop-dong-mua.html`

---

## Mục tiêu

Tab "Điều khoản thanh toán" (màn `contract/contract/add`) bổ sung **hình thức "theo đợt"** bên cạnh "theo đơn" (bảng 4 điều khoản hiện có). HĐ áp KPI tách thành **2 khối độc lập** (HỢP ĐỒNG CHÍNH / HÀNG KPI), mỗi khối chọn hình thức riêng, phân biệt trực quan bằng badge màu + dropdown riêng.

## Scope

- BE: 3 migration (2 cột `contracts`, 1 cột `contract_payment_terms`, 1 bảng mới `contract_payment_installments`) + 1 model + mở rộng validate/sync trong flow contract + `ContractDetailResource`.
- FE: component mới `PaymentBlockCard.vue` (1 card = 1 khối, chứa cả 2 mode), tái dùng `PaymentTermsTab.vue` cho mode "theo đơn", sửa tab trong `GeneralComponent.vue`.
- Không API riêng, không foreign key.

## Các quyết định lớn

| | |
|---|---|
| Cấu trúc KPI | 2 khối độc lập main / kpi, mỗi khối 1 hình thức riêng |
| Gốc tính tiền theo đợt | main → tổng hàng chính; kpi → total_kpi |
| Tổng % = 100 | Chỉ cảnh báo mềm, không chặn |
| Cột thời gian đợt | Ngày cụ thể (datepicker) |
| Trình bày | 2 card xếp dọc, badge màu + dropdown hình thức riêng |
| HĐ không KPI | Chỉ 1 card HỢP ĐỒNG CHÍNH |
| Lưu trữ | PA A — bảng đợt mới + cột block/mode |
| Đổi mode rồi lưu | Xóa data mode ẩn khi lưu |
| Default HĐ cũ | payment_mode_main='don', terms cũ → block='main' |

## Out of scope

- Mẫu in HĐ nhúng bảng đợt / 2 khối điều khoản.
- Đối soát dòng tiền thực tế theo đợt.
- Phụ lục đổi điều khoản chưa cover installments/mode (xử lý sau).
