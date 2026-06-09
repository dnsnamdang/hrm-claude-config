# Plan — solution-module-end-customer

@manhcuong · Spec: docs/superpowers/specs/2026-06-26-solution-module-end-customer-design.md

## Phase 1 — Backend ✅
- [x] `SolutionModuleService::getDetailWithRelations()`: thêm 8 key (is_intermediary_customer + customer_benefit_id/code/name + customer_benefit_contact_name/role/email/phone) từ $prospectiveProject — php -l sạch

## Phase 2 — Frontend ✅
- [x] `ProjectInfoTab.vue`: thêm card "KHÁCH HÀNG CUỐI" (v-if is_intermediary_customer && customer_benefit_id) ngay dưới "THÔNG TIN KHÁCH HÀNG", 5 dòng

## Phase 3 — Verify ✅
- [x] BE tinker module 1 (project có KH cuối): trả is_intermediary=true, benefit 43239 "50TPHPTA-1190 . CÔNG TY...ĐỖ LÊ VŨ", contact "23423"/SĐT "0912312314" — PASS
- [x] Playwright (login namdangit, /assign/solution-modules/1/manager tab Thông tin): card "KHÁCH HÀNG CUỐI" hiện ngay dưới "THÔNG TIN KHÁCH HÀNG", đủ Mã.Tên + người liên hệ/chức vụ/email/SĐT — PASS
- [x] Case ẩn: tạm set project 7 (của module 1) is_intermediary_customer=0 → BE trả is_intermediary=false → Playwright reload màn manager 1: card "KHÁCH HÀNG CUỐI" BIẾN MẤT (chỉ còn THÔNG TIN KHÁCH HÀNG → YÊU CẦU LÀM GIẢI PHÁP) PASS → ĐÃ khôi phục is_intermediary=1/benefit=43239

## Checkpoint — 2026-06-26
Vừa hoàn thành: BE + FE + verify (tinker + Playwright PASS). CHƯA commit/git.
Bước tiếp theo: xong; user review thêm nếu cần.
Blocked: không.
