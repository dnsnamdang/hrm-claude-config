# Việc còn lại — feature Chuyển đổi hàng hoá (soát 12/10/2026)

> Gom từ `SO-CHOT-VA-TON.md` §2 + `2c-ghi/chot.md` (Việc ngoài luồng N1–N53) + `gia-theo-cong-ty/design.md` (N54–N70)
> + `gia-theo-cong-ty/g2-plan.md` (N71–N75) + plan T1–T7 Phase 7.
> Trạng thái mỗi mục = đã đối chiếu plan/kết quả kiểm của đợt xử lý (cột Căn cứ). Chưa đối chiếu được ⇒ ghi "⬜ còn".
> Ký hiệu: ✅ đã xử lý · ⬜ còn phải làm · ⏸ user chốt để sau · ❌ user bỏ · ❓ cần user chốt có thuộc lần lên prod này không.
> 🔴 Nguyên tắc: feature lên prod MỘT lần; việc ngoài luồng phải xong hết trước khi merge prod (tiền đề 9).

## Thứ tự đề xuất (user đồng ý 12/10)

1. **T7** chặn ERP luồng tính giá + nghiệm thu Phase 7 — plan `luong-tinh-gia/t7-plan.md`, chờ "làm" (phạm vi §5)
2. **Phase 6** Danh mục hàng tạm — chưa mở (user 10/10: chuyển hết sang HRM trong lần này)
3. **Xử lý mục ⬜ ở bảng C** (việc ngoài luồng)
4. **2-E** Excel hàng hoá + nghiệm thu "ERP không vỡ" 14 bước (`hop-dong-tuong-thich-erp.md`)
5. **Popup "Xem hàng hoá Công ty khác"** (L6 hoãn ở 2-C2)

## A. Phase / đợt chức năng

| # | Việc | Trạng thái | Căn cứ |
|---|---|---|---|
| A1 | Phase 7 T7 — chặn 40 route tính giá ERP, 5 link menu, 3 thẻ dashboard, chạy thử runbook | ✅ 12/10 (ERP merge LOCAL `443c812553`, chưa push) | `luong-tinh-gia/t7-plan.md` §7–9 |
| A2 | Phase 6 Hàng tạm (phương án mới) | ✅ 13/10 đã push (api 657fa731f, client dc793189e, ERP 396f42dd7c); e2e xanh | `danh-muc-hang-tam/p6-plan.md` |
| A3 | 2-E Excel hàng hoá (Catalog chỉ ghi Tiểu mục) + nghiệm thu ERP 14 bước | ⬜ chưa mở | SO-CHOT §2c |
| A4 | Popup "Xem hàng hoá Công ty khác" | ⏸ hoãn (L6) — hiện thay bằng nút "Kho dữ liệu" | `2c-ghi/chot.md` L6 |
| A5 | Bỏ hẳn hệ số giá (tiền đề 8) — N34 cron + 3 màn xem giá ERP, N36 Cập nhật giá theo hãng | ⏸ user 09/10 "chuyển sau" | QC-7, QC-10 |
| A6 | 2-bc Báo cáo hàng hoá theo công ty | ⏸ để sau (04/10) | §27 |
| A7 | Phase 2c (3 danh mục xe còn lại) · 3 (phân quyền theo công ty) · 4 (popup tìm hàng dùng chung) · 5 (gỡ 5 danh mục) | ⬜ **THUỘC lần lên prod này** (user chốt 13/10) — **làm SAU bảng C** (user 13/10), chưa mở cả 4 | SO-CHOT §2 |
| A8 | 5 ca e2e "không quyền" đỏ sẵn (spec chèn `roles.company_id`) | ⬜ | G6 |
| A9 | Nghiệm thu: Phase 1 · 2b · 2d · 48 màn `bang-man-hinh-menu.md` | ⬜ chờ user | — |
| A11 | Bắt buộc **Đặc tính** (`product_characteristic_id`) ở form hàng hoá THƯỜNG — tạm bỏ vì dữ liệu cũ chưa có; cần bổ sung Đặc tính cho hàng cũ rồi mới bật bắt buộc (hàng tạm Phase 6 đã bắt buộc ngay) | ⏸ chờ dữ liệu cũ | user 12/10 |
| A10 | Dữ liệu thử "lấy về": DB giacty 0 mã lấy về được (backfill gán cả 4 công ty status 3) | ⬜ cần dựng dữ liệu khi nghiệm thu luồng lấy về | đo 12/10 |

## B. Trước go-live (thao tác dữ liệu, không phải code)

| # | Việc | Trạng thái |
|---|---|---|
| B1 | N10 tick cờ `product_natures.is_auto_parts` cho các Tính chất phụ tùng ô tô thật | ⬜ |
| B2 | N69/N70 Cty 5/6/8 sẽ loại bỏ: tắt cờ duyệt hàng mới Cty 8, mốc tắt tài khoản / chứng từ dở | ⬜ cần user/khách chốt mốc |
| B3 | Runbook triển khai `gia-theo-cong-ty/runbook-trien-khai.md` + bổ sung bước Phase 7 (T7) | ✅ 12/10 Phần 2 (chạy thử đạt) |
| B6 | **Cây phân loại hàng hoá gần như RỖNG** (giacty + hrm_erp, đo 12/10): Tính chất 1 · Nhóm chức năng 0 · Nhóm SP 0 · Loại SP 0 · Đặc tính 0; 0 hàng có `product_type_id` ⇒ HRM KHÔNG tạo được hàng hoá mới nào (thường lẫn tạm) tới khi nghiệp vụ nhập cây (Phase 0 màn đã có). e2e / kiểm tay phải tự dựng cây thử rồi dọn | ⬜ nghiệp vụ — chặn go-live |
| B5 | Danh mục **Đặc tính sản phẩm** (`product_characteristics`) đang **0 dòng** (giacty + hrm_erp, đo 12/10) — hàng tạm Phase 6 BẮT BUỘC Đặc tính ⇒ phải nhập danh mục trước go-live, nếu không không tạo được hàng tạm | ⬜ nghiệp vụ |
| B4 | D1: dọn 30 phiếu hỏi chéo công ty còn dở ở ERP (production phải = 0 trước deploy) | ⬜ nghiệp vụ, T-7 ngày |

## C. Việc ngoài luồng

> 🔎 **Soát lại 13/10** (chỉ đọc) ⇒ `ngoai-luong/soat-bang-c.md`: đóng N31 · N66 · N64 (phần feature); 16 câu chờ user chốt (Q-N61 trước); đề xuất 5 đợt C-a…C-e.

| # | Việc (tóm tắt) | Trạng thái | Căn cứ |
|---|---|---|---|
| N1 | ERP đọc `min_stock_qty`/`guarantee` chung ⇒ đọc theo công ty chứng từ | ⬜ (2-D ton: "để sau, trước merge prod") | `2d/ton.md:29` |
| N2 | Hãng SX ERP ghi đè `company_id` + xoá dòng hàng × công ty | ✅ 2-D1 (bỏ khối ghi) | `d1-plan` |
| N3 | Thương hiệu ERP ghi đè `company_id` | ✅ 2-D1 (gỡ 2 lời gọi) | `2d/ton.md:10` |
| N4 | Chặn `products/*` ERP chừa danh sách trắng | ✅ 2-D1 | `khao-sat-a` |
| N5 | Cron giá về 0 khi hết tồn bỏ sót hàng HRM | ⏸ để sau các chức năng hàng hoá | chot |
| N6 | `sync:crm` không đẩy hàng HRM | ❌ user bỏ | chot |
| N7 | `->group->` null (popup 338 màn) | ✅ 2-D1 M1–M7 | `d1-kiem-p3` |
| N8 | Popup ERP chọn được hàng công ty đã khoá | ✅ 2-D1 | `d1-kiem-p3` K2 |
| N9 | Popup ERP lọc mất hàng HRM (`product_type` NULL) | ✅ 2-D1 | `d1-kiem-p3` |
| N10 | Cờ phụ tùng ô tô | ⬜ → B1 | |
| N11 | `can_retail` | ✅ 2-D1 P1 gỡ | `d1-plan` |
| N12 | Thiếu tài khoản e2e "chỉ xem hàng hoá" | ⬜ | |
| N13 | Form sửa hàng nhiều đời xe chậm | ⬜ | |
| N14 | Tồn nhỏ 2-C1 (định dạng URL, exists không lọc status, S3 mồ côi, composer.lock) | ⬜ | |
| N26 | 59.710 `product_histories` mồ côi / AUTO_INCREMENT | ⬜ | |
| N27 | Lấy về / sửa đồng thời với khoá không `lockForUpdate` | ⬜ | |
| N28 | `products/change` + 3 route `view-import*` không gate | ✅ 2-D1 gỡ route | `d1-plan` |
| N29 | 4 route `approve*Submit` không kiểm quyền | ✅ G6 chặn (sang HRM) | `g6-plan:35` |
| N30 | `manualUpdatePrices` GET ghi giá | ✅ G6 chặn | `g6-plan:35` |
| N31 | Route `productDelete` khai trùng | ✅ hết tác động (soát 13/10: 2 route đều chặn) ~~⬜~~ (2-D1 chỉ trỏ đích, không đổi tên) | `d1-plan:34` |
| N32 | HRM Thuế suất không lan xuống `products`/`groups` | ✅ C-b 13/10 (ERP `42bbe92ae2` + HRM `5d109a505`, ĐÃ PUSH) ~~⬜~~ | |
| N33 | Hàng HRM không có hàng gốc / hàng gốc lỗi thời | ✅ C-b 13/10 (ERP `42bbe92ae2`, ĐÃ PUSH) ~~⬜~~ | |
| N34 | 2 cron giá + 3 màn xem giá ERP | ⏸ → A5 | |
| N35 | Hệ số giá đóng băng | ⏸ user chấp nhận tới Phase 8 | QC-3 |
| N36 | Cập nhật giá theo hãng | ⏸ → A5 | |
| N37 | `getWareHouseImportLot` 500 hàng không nhóm | ✅ 2-D1 M4b | `d1-plan` |
| N38 | Mẫu tem 1–6 | ✅ 2-D1 (tem theo Loại SP) | `d1-kiem-p3` K6 |
| N39 | ERP CLAUDE.md ghi sai Laravel 8 | ⬜ (tài liệu) | |
| N40 | `brands/list` gọi `importExcelAttribute` | ✅ 2-D1 chặn | `d1-plan` |
| N41 | In tem `twoCode=false` in cả mẫu 2 | ⬜ lỗi cũ | |
| N42 | `product_infos/list` còn nút "Thêm mới" | ✅ C-b 13/10 (ERP `42bbe92ae2`, ĐÃ PUSH) ~~⬜~~ | |
| N43 | `BaseProduct.php:76` `->group->` | ⬜ | |
| N44 | `Product::exportExcel` không null-safe | ⬜ | |
| N45 | ERP `ExampleTest` đỏ sẵn | ⬜ | |
| N46 | In tem phiếu nhập chết Angular | ⬜ lỗi cũ gop_db | |
| N47 | Excel Doanh thu theo hàng hoá 500 | ❌ user bỏ qua 13/10 ~~⬜~~ lỗi cũ | |
| N48 | PDF Doanh thu theo hàng hoá 500 | ❌ user bỏ qua 13/10 ~~⬜~~ lỗi cũ | |
| N49 | Báo giá dịch vụ `reading 'cost'` | ⬜ lỗi cũ | |
| N50 | Báo giá mẫu `infdig` | ⬜ lỗi cũ | |
| N51 | Chi tiết hàng ERP `$parse:syntax` | ⬜ lỗi cũ | |
| N52 | `<title>` trang ngừng sử dụng | ✅ ERP `b2f1761789` | chot |
| N53 | Hàng đang nhập thông tin chọn được ở popup ERP | ✅ ERP `b2f1761789` | chot |
| N54 | 3 luật làm tròn giá × hệ số ERP | ✅ C-a 13/10 (ERP `e7e2ea24c5`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜ (hết khi bỏ hệ số — A5)~~ | |
| N55 | Ô lọc Tồn kho màn giá ERP chết | ✅ màn bị chặn ở G6 | |
| N56 | Duyệt hàng loạt ERP sai `price/prices`, `dd($e)` | ✅ màn bị chặn ở G6 | |
| N57 | `manualUpdatePrices` không lọc `flag` | ✅ chặn ở G6 | |
| N58 | Cron 01:00 làm mồ côi cờ chờ duyệt | ✅ C-a 13/10 (ERP `5408c052aa`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N59 | `getProductsAndPrices` cột sắp xếp tự do | ✅ C-a 13/10 (ERP `b373f1f1cc`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N60 | `ProductExportsController:766` truyền nhầm `unit_coefficient` | ✅ C-a 13/10 (ERP `0fd8894a5d`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N61 | `getData` lộ giá vốn cho người không quyền | ✅ C-a 13/10 (ERP `3fcbf36a5c`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜ 🔴 bảo mật giá vốn~~ | |
| N62 | `WrServiceQuotation` lấy giá theo thứ tự | ✅ C-a 13/10 (ERP `e42f297894`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N63 | 2 Job giá không dispatch (code chết) | ✅ C-a 13/10 (ERP `164fb432ff`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N64 | HRM `catalog-histories/{table}/{id}` không gate | ✅ phần hàng hoá/giá (soát 13/10); phần chứng từ tài chính ⇒ Q-N64 ~~⬜~~ | |
| N65 | 13.662 giá hiệu lực quá ngày + cờ mồ côi | ⬜ | |
| N66 | 3 bảng chứng từ không `company_id` gần rỗng | ✅ G3 `DocumentCompany` phủ (soát 13/10) ~~⬜~~ | |
| N67 | 2 nơi ghi cờ duyệt giá công ty | ✅ C-a 13/10 (ERP `51918163e3`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N68 | `firstOrFail` chỗ gọi chưa bắt exception | ✅ C-a 13/10 (ERP `27204dab75`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N76 | 8 danh mục Phase 1 còn lại + bản `pi-*` vẫn ghi được ở ERP ⇒ user 13/10: chặn hết ở ERP, HRM duy nhất (đảo QĐ8 Phase 1) | ✅ C-b 13/10 (ERP `42bbe92ae2`, ĐÃ PUSH) ~~⬜~~ | `ngoai-luong/soat-bang-c.md` |
| N77 🔴 | trang sửa/xem/sao chép chứng từ ERP nhúng `units` đủ 13 cột pcu (giá vốn…) vào JSON trang — **XÁC NHẬN 13/10** (YC đặt hàng tổng #7692 `cost_price` 240.000 trong `@json($object)`); ~25 hàm; sửa tập trung `unitsInfoFor` | ✅ C-a2 13/10 (ERP `8b23629e97` + `60719788f8` `$hidden` ProductUnit; merge + PUSH `3f017e66dd` 13/10) | `ngoai-luong/n77-khao-sat.md` |
| N77-b | màn Chi tiết hàng hoá ERP (`productShow`, quyền Xem hàng hóa) hiện ô Giá vốn + Giá mua | ✅ C-a2 13/10 ẩn 2 ô (`8b23629e97`); đo bố cục sau khi sửa N51 | n77-khao-sat |
| N80 | trang xem YC xuất hàng nhúng tổng giá vốn HỢP ĐỒNG (`cost_price` khối hiệu quả HĐ) | ⏸ user 13/10: ghi riêng STATUS gop-db, làm sau (ngoài hàng hoá) | n77-khao-sat |
| N78 | thẻ "Hàng reset giá" ghi ở cả ERP Quy chế lẫn HRM tab Hàng hóa — cùng loại N67 | ✅ C-b 13/10 (ERP `42bbe92ae2`, ĐÃ PUSH) ~~⬜ user 13/10: HRM duy nhất — đợt C-b~~ | `ngoai-luong/cb-khao-sat.md` |
| N79 | `WrServiceQuotation.php:1072,1308` `$service` chưa khai báo (lỗi cũ, cảnh báo) | ⬜ lỗi cũ | ca-plan §6 |
| N81 | Route ghi `pi-groups` / `pi-brands` / `pi-manufactures` ở ERP còn mở (menu đã ẩn; ghi bảng pi_*, phục vụ form Hàng hoá có sẵn đã chặn) | ✅ 13/10 user "chặn luôn": 21 route (pi-groups đích `stopped-generic`), ERP `42bbe92ae2` ĐÃ PUSH | `ngoai-luong/cb-plan.md` |
| N69–N70 | Cty 5/6/8 loại bỏ | ⬜ → B2 | |
| N71 | Comparator lệch cặp HRM | ✅ G2b | |
| N72 | Backfill 4 ô quản trị NULL | ✅ G2b | |
| N73 | Seeder test nối giá không kẹp công ty | ⬜ | |
| N74 | 4 helper Human đọc `mysql2` (erp2326) | ⬜ (cờ đã gỡ ở G2b — cần kiểm còn đường đọc này không) | |
| N75 | `e2e_provision.php` mã hàng id erp2326 | ⬜ | |

**Đếm (bảng C, 63 dòng):** ✅ 20 · ⬜ 38 (khoảng 15 là lỗi cũ ERP có sẵn trên gop_db) · ⏸ 4 · ❌ 1.
✅ **User chốt 12/10: SỬA HẾT trước khi update prod** — kể cả lỗi cũ ERP có sẵn trên gop_db (N41, N45–N51, N59–N63, N65…).
