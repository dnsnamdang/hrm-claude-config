# Fix: phiếu hạch toán dịch vụ — dòng "Vật tư lắp đặt" SL=0 (downstream của bug qty clamp)

## Bối cảnh
Tiếp nối [[fix-wr-approve-service-qty-clamp]]. Phiếu hạch toán dịch vụ (`wr_accounting_services`) sinh TỪ phiếu duyệt khi qty service còn = 0 → `wr_accounting_service_items.qty=0` → mọi cột tiền = 0, và **sổ kế toán (account_details)** thiếu doanh thu/VAT của dòng đó.

## Root cause
- `WrAccountingService::store` → `syncServices` lưu item với `qty = service.qty` (của phiếu duyệt, lúc đó = 0 do bug clamp).
- HĐ loại HOP_DONG: `getDataCreateDept()` (nhánh else) sinh sổ bằng **lặp trực tiếp `$this->services` (items)** — dùng `amount_after_extra`, `vat_percent`, `rebate_price`, `discount_price`, `amount_cost_price`. qty=0 → doanh thu/VAT dòng đó = 0 trong sổ.

## Phạm vi
- Quét toàn DB: chỉ **2 item** qty=0 & price>0 → **2 phiếu hạch toán: 746 (duyệt 2023), 747 (duyệt 2101)**.

## Fix (đã chạy trên prod)
Hàm `UpdateDB::fixAndRegenerateAccountingService($id)`:
1. Item qty=0&price>0 → qty=1, recompute amount columns (= per-unit × qty); `amount_cost_price` = giá vốn HĐ (`wr_service_contract_product_services.price`) × qty.
2. Xoá `account_details` cũ của phiếu (invoiceable = WrAccountingService).
3. Chạy lại `getDataCreateDept()` + `AccountDetail::saveAccountDetail()` (login creator để có auth context).

## Tasks
- [x] Viết hàm `fixAndRegenerateAccountingService` trong UpdateDB.php
- [x] Chạy 746 (prod): item#744 amount 0→5,050,000, VAT 363,600; sổ sinh lại 22 bút toán, **cân đối Nợ=Có (lệch 0)**
- [x] Chạy 747 (prod): item#746 amount 0→2,250,000; sổ 22 bút toán, **cân đối Nợ=Có (lệch 0)**
- [ ] User verify màn show 746/747 + đối chiếu sổ kế toán

### Checkpoint — 2026-06-16 (bổ sung: chiết khấu)
Phát hiện thêm: bug qty=0 cũng zero `rebate_price` (Tiền chiết khấu) của dòng vật tư → sổ thiếu chiết khấu (doanh thu thừa). Công thức chuẩn (validate từ dòng đúng): `rebate_price = price_after_extra − price_after_discount`.
- Nâng `fixAndRegenerateAccountingService` thành idempotent + sửa `rebate_price` (cả khi qty đã =1).
- Chạy lại prod: 746 rebate 0→505,000; 747 rebate 0→225,000. Sổ sinh lại, đều **cân đối Nợ=Có (lệch 0)**.
- Dòng "Công tháo lắp" (rebate đã đúng) không bị đụng.

### Checkpoint — 2026-06-15
Vừa hoàn thành: fix 2 phiếu hạch toán (746, 747) trên prod — sửa item + sinh lại sổ, đều cân đối Nợ=Có.
Bước tiếp theo: user reload 2 màn show + đối chiếu kế toán.
Lưu ý: `.env` ERP local trỏ DB prod → tinker chạy thẳng prod. Phòng ngừa tương lai: bug gốc clamp đã fix (FE) nên phiếu hạch toán mới sẽ không còn qty=0.
