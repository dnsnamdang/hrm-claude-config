# Việc còn lại — feature Chuyển đổi hàng hoá

## 📌 Bản tổng hợp 14/10/2026 (thay cho số đếm cũ bên dưới)
Đã xong & ĐÃ PUSH tới 14/10: Phase 1, 2-A…2-D, 2d cây catalog, Phase 6 hàng tạm, Phase 7 (T1–T7), giá theo công ty G0–G6, bảng C đợt C-a…C-f (N1 N13 N14 N26 N27 N32 N33 N39 N41–N46 N49–N51 N54 N58–N63 N65 N67 N68 N73–N78 N81 N89 + A8), A7 Phase 3 (đóng — đã hấp thụ), Phase 4 (4.1–4.5 + 4.3b), Phase 5.

### 1. Còn phải làm (code) — trước lên prod
| # | Việc | Ghi chú |
|---|---|---|
| A7-2c | ✅ Phase 2c — Biển số · Lái xe ngoài · Danh mục xe · Nhiên liệu + ERP chặn ghi 10 danh mục xe | XONG + ĐÃ PUSH 14/10 (api `8f5990cca`, client `cf5efd2ea`, ERP `ca5fa294de`); checklist deploy gán quyền trong `plan-2c.md` |
| N100 🔴 | Gói bảo dưỡng: `service_has_products.group_id` → id Loại SP theo mapping user cung cấp (migration + chuyển dữ liệu + ERP đọc) | task riêng; CHẶN GO-LIVE |
| A3 | 2-E Excel hàng hoá (Catalog chỉ ghi Tiểu mục) + nghiệm thu "ERP không vỡ" 14 bước | Excel XONG (merge 15/10 api `b38852de0`, client `0469c32a3`, ĐÃ PUSH); nghiệm thu lượt 2: 12 đạt · B2 đạt một phần (iii chỉ đo bằng SQL/API 403) · B3' không đạt ⇒ N111 đã sửa 15/10 (ERP `bfbd794503`, ĐÃ PUSH 15/10) — `excel-nghiem-thu-2e/nghiem-thu.md` |
| ~~N79~~ | ERP `WrServiceQuotation.php:1072,1308` `$service` chưa khai báo | lỗi cũ  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N82~~ | Xuất Excel báo giá KHÔNG theo BOM 400 `$show_children` | lỗi cũ  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N84~~ | Bảng `product_vehicle_model_has_life` thiếu index `product_id` (80k dòng) | cần migration  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N85~~ | Lỗi BE `galleries.N` không có chỗ hiện ở FE | nhỏ  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N86~~ | Ô chọn hàng kèm theo chưa lọc hàng đang khoá ở công ty | nhỏ  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N87~~ | `ProductFormVehicles` "Đang tải…" dùng `.text-muted` (= đỏ) | nhỏ  ✅ sửa 15/10 (ĐÃ PUSH) |
| N88 | e2e `api.setup.ts` ghim `API_REPO` checkout chính | công cụ test |
| ~~N91~~ | HRM `AdminData::source` đọc cả dòng hệ số status NULL (lệch ERP 23 dòng) | nhỏ  ✅ sửa 15/10 (ĐÃ PUSH) |
| N92 | Spec e2e `quotation-unit-select-nocost` gõ cứng giá cũ | spec |
| N94-rest | Catalog `@json` trong `searchProductJs` còn ~70 trang đọc; `sync_products` gọi `availableGroup` không có | dọn sau 4.5 |
| ~~N97~~ | ERP YC đặt hàng NK 2 / TN mới thêm hàng tay lỗi `unit_coefficient` (+ TN mới thiếu create/edit) | lỗi cũ từ 01/2024  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N98~~ | ERP Chi tiết KH (2 KH) lỗi JS khi mở | lỗi cũ, chưa khảo sát  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N99~~ | HRM `ChooseEquipmentTypeModal` không nhận chọn loại | cần kiểm tay  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N129~~ | Popup chọn hàng HRM: lọc Thương hiệu/Hãng SX/Xuất xứ ra 0 hàng + bố cục ô tag + công tắc lệch + đổi nhãn "Gồm hàng ngoài catalog" | ✅ sửa 15/10 (client merge `995dfb554`, ĐÃ PUSH 15/10 (client `41085f380`, ERP `4462d1178b`)) |
| N130 | Popup HRM nuốt lỗi 422 thành "0 hàng" — xem `soat-bang-c.md` (N131 nhãn ERP ✅ 15/10 `0441a83b9d`) | ngoài luồng |
| N137 🔴 | 3 file gop_db đọc giá không theo công ty (Doanh số tiêu chuẩn HĐ, giá bán lẻ YCXH) — sau merge gop_db 15/10 | CHẶN GO-LIVE, user: làm sau |
| N138 · N139 · N140 | Runbook đổi sang `permission:sync` · khoá trùng `attachment_types` · port "xem trước ảnh" vào popup chọn hàng | chờ |
| ~~N132 N134 N135 N136~~ | Popup chọn hàng: panel 280px · cấu hình cột bấm sớm + STT · bảng theo mẫu MISA (1 dòng + tooltip đen, mặc định 20) — HRM + ERP | ✅ ĐÃ PUSH 15/10 (client `41085f380`, ERP `4462d1178b`) |
| N122, N123, N126, N127, N128 + dọn giacty luật giá cũ | Lỗi mới 15/10 (N112 N114 N116 N120 N121 đã sửa; N113 N115 để sau) — xem `soat-bang-c.md` | chờ chốt |
| — | Minor hoãn của 4.4 / 4.5 / 4.3b (ledger `popup-tim-kiem-hang-hoa/progress.md`) | gom 1 đợt dọn |

### 2. Chờ user chốt / để sau (⏸)
| # | Việc |
|---|---|
| N95 | Cột "tồn lắp ráp" trong popup chọn hàng báo giá ERP — có đưa lại không |
| N103 | Gỡ UNIQUE DB `name` (biển số, nhiên liệu, hãng xe) để tạo lại tên đã khoá — Hãng xe 2b trùng tên lộ lỗi SQL — user 14/10: làm sau |
| N101 | Bảo hành hãng ERP (`firm_warranty_*`) có tìm toàn bộ hàng không — user: xử lý sau |
| N104 | Quyền xe 2b lệch id DB (1620–1631) vs seeder (1640–1651) — soát trước deploy |
| N105–N107 | `route:list` hrm-api lỗi sẵn · e2e mẫu in tem Loại SP đỏ · `V2BaseSelectRemote` TypeError khi request lỗi |
| N90 | Báo cáo CSKH + Tổng hợp bán hàng đọc bảo hành cột chung — user tính sau |
| N83 | Gỡ chip select2 nhiều lựa chọn — cần kiểm tay |
| A4 | Popup "Xem hàng hoá Công ty khác" (L6) |
| A5 (N34 N36) | Bỏ hẳn hệ số giá: 2 cron + 3 màn xem giá ERP, Cập nhật giá theo hãng — "chuyển sau" |
| N35 | Hệ số giá đóng băng — chấp nhận tới Phase 8 |
| A6 | 2-bc Báo cáo hàng hoá theo công ty |
| A11 | Bắt buộc Đặc tính ở form hàng thường — chờ dữ liệu cũ |
| N5 | Cron giá về 0 khi hết tồn bỏ sót hàng HRM |
| N64-rest · N80 | Route lịch sử chung chưa gate (chứng từ tài chính) · YC xuất hàng lộ tài chính HĐ — ngoài feature, việc riêng |

### 3. Trước go-live — dữ liệu / nghiệp vụ (không phải code)
| # | Việc |
|---|---|
| B6 🔴 | Nhập cây phân loại (Tính chất › Nhóm CN › Nhóm SP › Loại SP) + quy đổi 45.890 hàng + xếp catalog — dev gần rỗng; popup mới mặc định chỉ hiện hàng đã xếp catalog |
| B5 🔴 | Nhập danh mục Đặc tính (0 dòng) — hàng tạm bắt buộc |
| — 🔴 | Khai cờ "Hàng hoá làm dịch vụ" / "Dùng cho báo giá dịch vụ" trên Tính chất (vật tư theo máy / gói BD / vật tư thay thế đang ra 0 hàng) |
| B1 | Tick cờ phụ tùng ô tô (`is_auto_parts`) cho Tính chất thật |
| B2 | Cty 5/6/8 loại bỏ: mốc tắt tài khoản / chứng từ dở |
| B4 | Dọn 30 phiếu hỏi chéo công ty còn dở ở ERP (T-7 ngày) |
| A9 | Nghiệm thu Phase 1 · 2b · 2d · 48 màn `bang-man-hinh-menu.md` |
| A10 | Dựng dữ liệu thử "lấy về" khi nghiệm thu |
| Deploy | ERP prod khai `HRM_API_BASE_URL` + `config:cache`, giữ `IS_USE_SSO=true`, thử staging có SSO (đường cookie `jwt_token`); chạy runbook `gia-theo-cong-ty/runbook-trien-khai.md`; migration gop_db `2026_10_12_000000_change_exchange_rate…` chưa chạy giacty/hrm_erp; prod đếm lại `quotations`/`contracts` cũ |

---

## (Bản soát 12/10/2026 — giữ để tra)

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
| A1 | Phase 7 T7 — chặn 40 route tính giá ERP, 5 link menu, 3 thẻ dashboard, chạy thử runbook | ✅ 12/10 (ERP `443c812553`, đã lên remote) | `luong-tinh-gia/t7-plan.md` §7–9 |
| A2 | Phase 6 Hàng tạm (phương án mới) | ✅ 13/10 đã push (api 657fa731f, client dc793189e, ERP 396f42dd7c); e2e xanh | `danh-muc-hang-tam/p6-plan.md` |
| A3 | 2-E Excel hàng hoá (Catalog chỉ ghi Tiểu mục) + nghiệm thu ERP 14 bước | 🟡 Excel xong (ĐÃ PUSH 15/10); nghiệm thu 12/14 đạt, N111 đã sửa (ERP `bfbd794503`, ĐÃ PUSH 15/10) | SO-CHOT §2c |
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
