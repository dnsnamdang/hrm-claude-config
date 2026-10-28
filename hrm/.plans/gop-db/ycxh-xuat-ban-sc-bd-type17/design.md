# YCXH loại 17 — Xuất bán SC-BD (XUAT_BD_SC) — Design

**Trạng thái:** ĐÃ CHỐT THIẾT KẾ (2026-10-19). Loại thứ 3/3 đợt này (15 → 4 → 17). Chờ user review spec → writing-plans.

**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-10-19-ycxh-xuat-ban-sc-bd-type17-design.md`

**Định danh:** `ProductExportRequest::XUAT_BD_SC = 17`. Nguồn: HĐ dịch vụ SC-BH, `wr_service_contract_items.type = 1` (type=0 là loại 16 Xuất bán bảo hành). Loại 17 CÓ delivery + CÓ hạch toán.

**Nguyên tắc tối thượng (kế thừa cả đợt):** "làm đúng ERP, không tự bổ sung gì cả" — mirror ERP 1:1, kể cả chỗ ERP chưa nhất quán.

## Phạm vi (user chốt "1 đúng, 2 ok")
- **TRONG:** Tạo/Sửa/Xem YCXH 17 → 2 nhánh chứng từ (xuất thẳng→PXH; không thẳng→ĐNXK→PXK→PXH) → finalize ghi `exported_qty` → **hạch toán đầy đủ gồm HTHT** → modal chọn HĐ SC-BH + FE.
- **NGOÀI:** loại 16, trả hàng bán cho phiếu 17, báo cáo/biên bản downstream.

## 7 vùng port
1. Entity `CREATABLE_TYPE_IDS` += 17.
2. `createFromRequest` nhánh 17: guard `canProductExport`, snapshot KH, đọc nguồn SC-BH, cho trùng dòng product-unit, trần `root−exported−exporting`.
3. Endpoint nguồn `/wr-service-contracts` + `/{id}/data-for-export` (route tĩnh trước `/{id}`) + rules store/update.
4. Snapshot khách hàng từ `wr_service_contracts`.
5. Finalize ghi `exported_qty` (atomic increment) trên item + objectable + YCXHDetail — CẢ 2 đường.
6. Hạch toán nhánh 17 (`ProductExportPostingService`): doanh thu 1311/5111/33311, **chiết khấu 5211/33311/1311 (mới vs 21)**, giảm trừ 5213/33311/1311, giá vốn 1561/632, khối HTHT 1-percent **viết INLINE** (KHÔNG reuse `SupportAccountingTrait` — xem dưới).
7. show/editData nhánh 17 + FE modal + `HAS_DELIVERY += 17`.

## Quyết định đã chốt sau khảo sát (2026-10-19) — ĐẢO CHIỀU, cần user xác nhận ở review plan
- **KHÔNG reuse engine HTHT loại 21, viết INLINE.** Khảo sát chứng minh trait loại 21 làm tròn (`round`), lọc công ty phòng, dùng 2 percent — ERP type 17 thì KHÔNG (1 percent, không round, không lọc). Cả hai ĐỀU CÓ quỹ rủi ro (ERP `:739-745`) và type 17 CÓ THÊM cụm chiết khấu. Reuse = ghi SAI số → vi phạm "làm đúng ERP". Nên bỏ hẳn interface `SupportAccountable` / không chạm `SupportAccountingTrait`. An toàn hơn bản cũ. (§6.1 spec)
- **work_id verified:** DTHH=15, GGHH=16, TTHHD=12, TNST=13, TNSQ=14, RRP=6, CKHH=20 (bảng `works` trên `erp_hrm_check`).
- Task đầu vẫn verify field `WrSupportAccounting` HRM đủ cho engine (có thể là blocker thật).

## Bất nhất ERP chép nguyên trạng (KHÔNG sửa)
- `getExportingQty` lọc `service_contract_id` còn accessor dùng `wr_service_contract_id`.
- Modal chọn HĐ chỉ liệt `HOP_DONG` còn `canProductExport` cho cả `PL_BO_SUNG`/`BAO_HANH`.
