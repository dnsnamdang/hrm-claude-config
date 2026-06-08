# Danh mục Kho — Plan

> **Checkpoint 2026-06-05: HOÀN THÀNH** (BE+FE, chạy main chưa commit). BE smoke-test pass (warehouse_type_name, isCanDelete=false). Permission 1103-1104. Còn: user test UI + tạo file mẫu import.

> Subagent-driven, copy Manufacturer + thêm trường. KHÔNG commit.
**Spec:** `docs/superpowers/specs/2026-06-05-warehouse-category-design.md`

## Phase 1 — BE
- [ ] Migration warehouses
- [ ] Entity Warehouse (enum, manager, isCanDelete=false)
- [ ] Request (warehouse_type in:1-4, manager_id)
- [ ] Service (filter type/manager, no contacts, import)
- [ ] Transformers (warehouse_type_name, manager_name)
- [ ] Controller (no delete) + Routes + 2 permission + export

## Phase 2 — FE
- [ ] Menu "Kho"
- [ ] index.vue (no delete, filter loại kho)
- [ ] AddWarehouseModal (loại kho + thủ kho + địa chỉ)

## Phase 3 — Test
