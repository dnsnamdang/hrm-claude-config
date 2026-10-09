# Sổ Nhật ký chung (S03a-DN) — Phân hệ Kế toán HRM — TÓM TẮT

> Spec đầy đủ: `docs/superpowers/specs/2026-07-18-so-nhat-ky-chung-hrm-design.md`

## Mục tiêu
Màn báo cáo **Sổ Nhật ký chung** trong phân hệ Kế toán HRM, đọc **generic từ `account_details` của ERP** qua connection `mysql2`, 20 chiều, xuất Excel + in mẫu S03a-DN. Làm lại từ bản đã lỡ làm nhầm bên ERP (sẽ gỡ).

## Quyết định lớn
1. **BE Hướng A**: query thẳng `account_details` trên `mysql2` (không HTTP API, không phụ thuộc nhánh ERP).
2. **FE thuần V2Base** (Nuxt2/Vue2); phần đặc thù kế toán custom qua slot.
3. **Dựng khung chung** `Modules/Accounting` (base service + permission + menu) cho cả phân hệ; journal là màn đầu.
4. **Cascade 4 cấp (Cty→PB→BP→NV) + tên dòng đều nguồn ERP `mysql2`** — vì nhân viên HRM↔ERP không map deterministic (chung id cty/PB/BP; employee lệch ~17%).
5. **Phân quyền P1**: 1 quyền `Xem sổ nhật ký chung`, không giới hạn cấp công ty.
6. **UI phụ trợ làm hết** (cấu hình cột kéo-thả — reuse `modal/column-customization-modal.vue`; cài đặt trường lọc; ẩn/hiện lọc).
7. **Số CT chỉ text**, chưa link phiếu gốc.

## Tái dùng base
`V2BaseDataTable`, `V2BaseFilterPanel`, `V2BasePagination`, `V2BaseSelectRemote`, `modal/column-customization-modal.vue`, `V2BaseDatePicker/CurrencyInput/Button/Badge`.

## Phase
0. Scaffold Module Accounting + permission + menu
1. BE: AccountDetailBaseService + GeneralJournalService + AccountingOrgController + GeneralJournalController
2. FE cốt lõi: page + store + filter + cascade + table (20 cột, tổng, badge, lũy kế)
3. FE phụ trợ: cấu hình cột, cài đặt trường lọc, ẩn/hiện lọc
4. In & Excel
5. Verify (ΣNợ=ΣCó thật, cascade, TK cây, lũy kế, hiệu năng, index ERP)
6. Dọn code Sổ NKC bên ERP (nhánh `so_nhat_ky_chung`)

## Nhánh
`tpe-develop-accounting` (cả hrm-api + hrm-client).

## Liên quan
- Memory: `hrm-erp-org-id-mapping`, `erp-so-nhat-ky-chung-branch`
- Bản ERP (sẽ gỡ): `ERP/.plans/so-nhat-ky-chung/`
