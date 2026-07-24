# Hợp đồng mua (build thật) — Plan

@namdangit — 2026-07-20

Plan chi tiết (code mẫu + verify từng bước): `docs/superpowers/plans/2026-07-20-hop-dong-mua.md`
Spec: `docs/superpowers/specs/2026-07-20-hop-dong-mua-design.md`

## Cách thực thi: subagent-driven (mỗi task 1 subagent + review)

## Phase 1 — BE data layer
- [ ] Task 1: Migrations 4 bảng (purchase_contracts + products + payment_terms + progress)
- [ ] Task 2: Entities 4 (PurchaseContract + Product + PaymentTerm + Progress)

## Phase 2 — BE service/api
- [x] Task 3: StorePurchaseContractRequest + PurchaseContractService
- [ ] Task 4: Transformers (list + detail)
- [ ] Task 5: Controller + Routes + seed 3 quyền

## Phase 3 — FE menu + danh sách
- [ ] Task 6: MenuSupply + index.vue

## Phase 4 — FE form thêm/sửa
- [ ] Task 7: Khung form + Tab Thông tin chung + add/edit
- [ ] Task 8: Tab Hàng hóa + popup chọn hàng
- [ ] Task 9: Tab Mẫu in

## Phase 5 — FE xem/duyệt + E2E
- [ ] Task 10: Trang xem read-only + trang duyệt
- [ ] Task 11: E2E Playwright toàn luồng + kiểm log

## Checkpoint
### Checkpoint — 2026-07-20 (khởi tạo)
Vừa hoàn thành: brainstorming + spec đầy đủ + plan chi tiết + khung .plans/STATUS
Đang làm dở: chuẩn bị chạy Task 1 (migrations)
Bước tiếp theo: subagent code Task 1 → review → Task 2...
Blocked: (không)
