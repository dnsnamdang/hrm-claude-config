# Giá 0 = chưa tính giá + cảnh báo chọn hàng ở Báo giá — Plan

**Design:** `design.md` (cùng folder) · @namdangit · nhánh `gop_db` (checkout chính, 3 repo) · không migration/seeder

## Phase 1 — Cho nhập giá bán 0
### BE (hrm-api)
- [x] `PriceCalculateWriter`: giá bán 5 loại `positive=false` (giá NCC + tỷ giá giữ > 0)
- [x] `OwnerPriceFloor::violations`: giá B = 0 (cả giá hiệu lực) bỏ qua sàn — 1 nguồn cho PTG / Cập nhật giá / Duyệt giá
- [x] Test: `PriceCalculateApiTest::gia_ban_0_duoc_luu_va_duyet_ke_ca_duoi_san_gia_ncc_0_van_bi_chan`,
      `OwnerPriceFloorApiTest::b_nhap_gia_0_chua_tinh_gia_thi_bo_qua_san` + `duyet_gia_0_thi_bo_qua_san` — **CHƯA CHẠY** (chờ user cho chạy phpunit trên DB nào)
### FE (hrm-client)
- [x] `PriceCalculateForm.vue` validate: giá bán chỉ chặn âm ("Không hợp lệ")

## Phase 2 — Cảnh báo chọn hàng chưa tính giá (≤ 1 đ / chưa có giá)
- [x] BE `ProductPickerService` rows: `has_price` = giá > 1 đ (nhãn "Chưa có giá" khớp điều kiện)
- [x] HRM `QuotationProductSearchModal`: prop `warnUnpriced` + overlay trong popup (z 5000, $confirm sẽ bị che); bật ở `assign/quotations/_id/edit.vue`
- [x] HRM `WrQuotationForm.vue` (Báo giá DV CSKH): override `fetchLineInfo('product')` ⇒ `$confirm`
- [x] ERP `searchProductQuotationJs`: `sqKeepUnpricedIfConfirmed` (swal) trong `cfg.onPick`, bật bằng `$scope.warnUnpricedProduct = true` ở 4 formJs (firm / dự án / DV bán / DV CSKH)
- [x] e2e mới `HRM/e2e/tests/master-data/quotation-unpriced-warning-ui.spec.ts` (ép giá bằng page.route) — **chưa chạy**

## Kiểm Playwright MCP (23/10, local hrm_erp_21_10_prod)
- [x] HRM Báo giá BG-2026-00404: nhãn "Chưa có giá" mã 1 đ/0 đ; bấm tên 1 đ ⇒ overlay nằm trên (elementFromPoint), Không ⇒ 0 hàng; có giá ⇒ thêm thẳng; tick 3 (1 đ, 0 đ, 91tr) ⇒ hỏi liệt kê 2 mã, Không ⇒ chỉ thêm 829009; Vẫn chọn ⇒ thêm
- [x] HRM Báo giá DV CSKH 12736 (màn đang ẩn bởi Cài đặt phân hệ — bỏ ẩn tạm trong phiên trình duyệt): như trên qua $confirm
- [x] ERP firm (cổng 8097): bấm tên / tick nhiều / Không / Vẫn chọn / có giá đúng; dự án, DV bán, DV CSKH: cờ bật + swal hiện; thanh lý: không hỏi
- [x] PTG FE: `validate(true)` giá bán 0 không lỗi, âm "Không hợp lệ", giá NCC 0 "Phải lớn hơn 0" (không có PTG sửa được ⇒ chạy hàm trên dòng phiếu 215, không gửi)
- [ ] Báo giá thường ERP `/admin/quotations/create` không dựng được ở local — chỉ xác nhận bằng code (không bật cờ)

### Checkpoint — 23/10/2026
Vừa hoàn thành: code 3 repo + kiểm MCP; commit + push gop_db 23/10 (hrm-api 3230e9bef, hrm-client 54df9cda2, ERP 0b81c0b30a)
Đang làm dở: —
Bước tiếp theo: chạy 3 test PHPUnit mới (user tự chạy bằng `!` — auto mode chặn ghi DB dùng chung) + e2e quotation-unpriced-warning-ui
Blocked: e2e bị đá về login (tài khoản e2e_assign id 2071 không dùng được trên hrm_erp_21_10_prod) — cần user cho ghi đè e2e/.auth/user.json bằng token NV 76
