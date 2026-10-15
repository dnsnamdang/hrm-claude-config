# A3 · Đợt 2-E — Excel hàng hoá + nghiệm thu "ERP không vỡ" — KHẢO SÁT (14/10/2026, chỉ đọc)

> Phạm vi khảo sát: tài liệu `.plans/gop-db/quan-ly-hang-hoa/**` + code HRM worktree `wt-chuyen-doi-hang-hoa`
> (hrm-api `8f5990cca`, hrm-client `cf5efd2ea`, nhánh `feat/chuyen-doi-hang-hoa`) + ERP worktree `wt-erp-2d1`
> (`ca5fa294de`, nhánh `feat/2d1-erp-khong-loi`) + DB `hrm_erp_giacty` (chỉ SELECT).
> KHÔNG sửa code, KHÔNG ghi DB. Mọi câu hỏi tồn ở mục 4 phải được user chốt + nói "làm" (kèm phạm vi mục 5) trước khi code.

---

## 1. Phạm vi Excel 2-E theo tài liệu đã chốt

### 1.1 Những điều ĐÃ CHỐT (có trích dẫn)

| # | Điều đã chốt | Nguồn |
|---|---|---|
| E1 | Đợt 2-E = "Excel (Catalog chỉ ghi Tiểu mục, D1-a) + nghiệm thu 'ERP không vỡ' 14 bước" | `SO-CHOT-VA-TON.md:70`; `viec-con-lai.md:11` (A3 "chưa mở") |
| E2 | **D1-a**: Excel danh sách hàng hoá — cột Catalog **chỉ ghi cấp 4 = Tiểu mục**, KHÔNG ghi đường 4 cấp; hàng nhiều nhánh ⇒ nhiều Tiểu mục trong **1 ô, mỗi cái 1 dòng**. "Cấp 4 Loại hàng hoá" user nói = Tiểu mục, không đổi tên hiển thị | `man-danh-muc-hang-hoa/design.md:3245`; `ton-chot-truoc-code.md:64` |
| E3 | Đây là **XUẤT** Excel. Không có chốt nào về **nhập (import)** Excel hàng hoá | D1 chỉ nói xuất (`ton-chot-truoc-code.md:64`); popup Import Excel trong mockup chỉ thuộc màn *Chính sách giá bán nội bộ* (`mockup-luong-xay-dung-hang-hoa.html:1325`, `design.md:1914-1921`) |
| E4 | Quyền **1654 "Xuất excel danh sách hàng hoá"**: MỌI nút Xuất Excel danh sách hàng hoá trong luồng dùng chung quyền này | `design.md:3181`, `:3201-3202` (id 1654 đã giữ chỗ) |
| E5 | Màn *Kho dữ liệu* và *Hàng đang kinh doanh* không cần quyền để VÀO, nhưng "các nút thao tác check theo quyền của từng nút" ⇒ nút Xuất vẫn cần 1654 | `design.md:3184` (dòng "không cần quyền"), `:3196` |
| E6 | Màn có nút Xuất Excel theo mockup chốt 30/09: **Kho dữ liệu** (`sc-tong`), **Dữ liệu hàng hoá công ty** (`sc-kho`), **Hàng đang kinh doanh** (`sc-l3`). **Hàng hoá nhập thông tin** (`sc-l1`) KHÔNG có nút | mockup `:1176`, `:1242`, `:1116`; `2b-doc/mockup-inventory.md:552` ("chưa rõ cố ý hay sót") |
| E7 | Các đợt 2-B/2-C cố ý KHÔNG làm Xuất Excel, dồn sang 2-E | `2b-doc/plan.md:10`, `:72`; `2c-ghi/c2-khao-sat-fe.md:133` (L11); `2c-ghi/yeu-cau-ghi.md:166`; `2c-ghi/plan.md:14` |
| E8 | **ERP đã GỠ HẾT xuất hàng hoá (13/10)**, user: *"Xuất excel cũng bỏ luôn, tôi sẽ làm bên HRM sau"* — gỡ nút Xuất Excel + popup chọn cột (`exportProduct`), nút "Hàng chưa có công khoán" (`exportExcelNorm`), route `exportExcel/CSV/PDF` | `ngoai-luong/cc-khao-sat.md:30-31`; ERP commit `81eef9f9c2` |
| E9 | Nguyên tắc §35b: không bảo mật thông tin hàng hoá/giá bán, chỉ gate thao tác + **giá vốn** ⇒ file xuất không được lộ giá vốn | `design.md:3170-3172` |
| E10 | Khuôn chung toàn hệ thống: popup "Chọn trường xuất file" (tick sẵn = cột đang hiện), xuất theo đúng bộ lọc, tất cả dòng; > 2s thì FE dựng file + `export-rows` theo trang (trần 5.000/lượt) | skill `list-page` §14b, §14c (`HRM/.claude/skills/list-page/SKILL.md:1360-1500`); `man-danh-muc-hang-hoa/plan.md:705-712` (F1.1–F1.3) |

### 1.2 Những điều CHƯA CHỐT

| # | Điểm mở | Nguồn |
|---|---|---|
| U1 | Màn nào có nút Xuất: mockup có ở 3 màn; *Hàng hoá nhập thông tin* thiếu nút (sót hay cố ý?); màn **Hàng tạm** (Phase 6) có câu Q12 "⭐ Chỉ Xuất Excel theo bộ lọc" nhưng cột Chốt **trống** | `mockup-inventory.md:552`; `danh-muc-hang-tam/ton.md:22` |
| U2 | **Import Excel hàng hoá**: plan cũ (trước §22) có F1.4 "Import: validate trước khi ghi" nhưng không có chốt nghiệp vụ; mockup không có popup import cho hàng hoá | `man-danh-muc-hang-hoa/plan.md:713` |
| U3 | Cột Catalog ở màn **Kho dữ liệu** (mọi công ty): catalog là dữ liệu **theo công ty** (`product_business_catalogs.company_id`); màn Kho hiện KHÔNG có cột catalog. D1 viết "cột Catalog ở màn Kho" nhưng trong mockup id `sc-kho` lại là *Dữ liệu hàng hoá công ty* ⇒ nhập nhằng | `design.md:2705` (§33i-7); `hrm-client/utils/product-list-screens.js` (warehouse không có `catalogs`) |
| U4 | Bộ cột của file: chỉ cột màn danh sách (~25 cột, khuôn registry) hay thêm cột "đủ thông tin" như bộ xuất ERP cũ (45 cột, gồm thông số, thuế, HS code…) mà user đã cho gỡ để "làm bên HRM" | `man-danh-muc-hang-hoa/khao-sat.md:18`; `cc-khao-sat.md:31` |
| U5 | Xuất "**Hàng chưa có công khoán**" (ERP `exportExcelNorm`, kế toán dùng) — đã gỡ ở ERP 13/10 cùng gói "HRM làm lại sau" — có thuộc 2-E không | `cc-khao-sat.md:31`; `2d-erp-khong-loi/khao-sat-c-gia.md:66` (L8) |
| U6 | D1-b / D2 (xuất báo cáo ma trận) — ⏸ thuộc 2-bc Báo cáo theo công ty, **ngoài** 2-E | `design.md:3246`; `viec-con-lai.md` A6 |

---

## 2. Hiện trạng code

### 2.1 HRM (worktree `wt-chuyen-doi-hang-hoa`)

| Hạng mục | Hiện trạng | Ghi chú |
|---|---|---|
| FE 5 màn danh sách (`pages/master-data/products/{warehouse,company,entering,trading,temp}.vue`) | Đều `extends components/product/ProductListPage.vue` (1.318 dòng) + cấu hình `utils/product-list-screens.js` | **0 nút Xuất Excel**, chưa dùng `exportFieldsMixin` / `ExportFieldsModal`; đã có `columnCustomizationMixin` (khoá `products_<slug>`) ⇒ `visibleExportFields` dùng được ngay |
| BE route `Modules/MasterData/Routes/api.php:415-470` | `GET products/{warehouse,company,entering,trading,temp}` + chi tiết + ghi | **Không có** `/export` hay `/export-rows` |
| `app/ExcelExport/ExportColumnRegistry.php` | Có mục cho danh mục phân loại, catalog, model…; **không có mục `products_*`** | khuôn `resolve($screen, $request)` lọc `fields` qua whitelist |
| Dữ liệu catalog | `ProductListResource` trả `catalogs` = `CatalogBranch::many()` ⇒ `[{job_cluster_id, name (= Tiểu mục), path (Lĩnh vực › Chương › Mục › Tiểu mục)}]`, nạp theo **công ty đang làm** (`ProductService.php:331-337`) | D1-a chỉ cần `name` nối `"\n"` — không query thêm |
| Quyền 1654 | **Chưa seed** (seeder `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php:1592` ghi "1654 + 1656 seed ở đợt dùng tới"); id 1654 trống ở `hrm_erp_giacty`, `hrm_erp` và `origin/gop_db` | 1659 cũng trống; 1656/1657/1658 đã có |
| Hạ tầng dựng file | BE `DynamicExport` + `exports.dynamic` (đa số màn); FE `utils/export/listExportFile.js` (429 dòng, ExcelJS, đã `wrapText` ⇒ `\n` xuống dòng trong ô) + khuôn `export-rows` ở 9 màn (vd `Modules/CustomerCare/Routes/api.php:226`) | Mẫu xuất có letterhead gần nhất trong module: `ProductPriceApprovalController@export` (`ProductPriceApprovalExport`) |
| Rủi ro hiệu năng | `ProductListResource` gọi `AdminData::guaranteeText`, `AdminData::minStockQty`, `tradingCompanyNames()` theo **từng dòng** | Xuất 28k dòng qua Resource dễ N+1 ⇒ `export-rows` phải map bằng query gộp, đo trước |

**Số liệu `hrm_erp_giacty` (SELECT 14/10):** `products` 45.890 (status≠0: **28.378**) · `product_company_coefficients` status 3 = 113.484 (= 28.371 × 4 công ty) ⇒ màn *Dữ liệu công ty* / *Đang kinh doanh* của mỗi công ty ≈ **28,4k dòng**, *Kho dữ liệu* ≈ 28,4k · cây catalog: `chapters` 66, `job_groups` (Mục) 107, `job_clusters` (Tiểu mục) **3** · `product_business_catalogs` **21 dòng / 21 hàng / 1 công ty / 1 Tiểu mục**, tối đa **1 nhánh/hàng** ⇒ dữ liệu dev KHÔNG có ca nhiều nhánh, test D1-a phải tự dựng fixture · cây phân loại: Tính chất 1, Loại SP 0, Đặc tính 0, hàng có `product_type_id` 0 (B6/B5 — HRM không tạo được hàng mới nếu không dựng fixture) · `products` mã rỗng 0, mã trùng 0 · `companies.is_new_company=1`: 1 (Cty 8) · `product_approves` 0.

### 2.2 ERP (worktree `wt-erp-2d1`)

| Hạng mục | Hiện trạng |
|---|---|
| Xuất hàng hoá | **Đã gỡ hết** (`81eef9f9c2`, 13/10): nút Xuất Excel + modal chọn cột, nút "Hàng chưa có công khoán", 5 route `products.exportExcel/CSV/PDF/exportExcelNorm/exportProduct`. `routes/web.php:524-568` chỉ còn khối comment cũ. Giữ `download-export-file` (`:48`, dùng chung tồn kho) + class `ProductReportExport/Norm`, `ProductMailJob` (controller cũ còn tham chiếu, không route) |
| Nhập hàng hoá | `importExcel`, `importExcelNew`, `importExcelInstallWork`, `importExcelAttribute` (`routes/web.php:591-594`) chặn bằng `productMovedToHrm:product-list`; 7 route import khác đã gỡ (404) — nghiệm thu K14/K14-g ở `2d-erp-khong-loi/d1-kiem-p3.md` |
| Màn danh sách hàng hoá ERP | `proList` + `searchData` + `productShow` còn sống (chỉ đọc); toolbar chỉ còn "Cập nhật giá (HRM)" · "Thùng rác" · "Tùy chỉnh cột" (`resources/views/products/list.blade.php:37-49`) |
| Duyệt giá / sửa giá ERP | chặn (G6), `approveExportExcel` chặn `productMovedToHrm:price-approve` |
| PHPUnit ERP liên quan | `ProductMovedToHrmRoutesTest`, `G6PriceRoutesMovedToHrmTest`, `PriceFlowRoutesMovedToHrmTest`, `TempProductRoutesMovedToHrmTest`, `ProductPopupCompanyStatusTest`, `G3CompanyPrice*`, `CcOldBugsTest`… (sau merge P4: 178/178) |
| Server | `.env` trỏ `hrm_erp_giacty`, không có `bootstrap/cache/config.php`; cổng 8090 **đang tắt** (8031/3031 đang chạy) |

**Kết luận phần Excel:** 2-E là việc **làm mới hoàn toàn ở HRM** (BE export + FE nút/popup + quyền 1654). ERP **không còn việc** về Excel hàng hoá (đã gỡ); không có gì "đang hỏng" ở ERP về Excel hàng hoá, chỉ còn lỗi cũ ngoài phạm vi N47/N48 (đã ❌ bỏ qua) và N82 (Excel báo giá không BOM — ngoài luồng).

---

## 3. 14 bước nghiệm thu "ERP không vỡ" (`man-danh-muc-hang-hoa/hop-dong-tuong-thich-erp.md:134-165`)

Bối cảnh đã đổi so với lúc viết hợp đồng (21/09): (a) 2-D chặn mọi đường ghi hàng hoá ERP; (b) **giá theo công ty G0–G6** đưa sửa giá + duyệt giá sang HRM (1657/1658), ERP chỉ đọc; (c) Phase 7 luồng tính giá — hàng HRM mới ở **status 1 Đang nhập thông tin**, phải qua YCHG→YCTG→PTG→KQ→duyệt giá mới thành **status 3**; (d) **popup ERP chỉ nhận `pcc.status = 3`** của công ty đang làm (G3 R5, `gia-theo-cong-ty/design.md:312`) và Phase 4 thay ruột popup ERP bằng picker HRM, **mặc định chỉ hàng đã xếp catalog** (`popup-tim-kiem-hang-hoa/design.md:5`); (e) Phase 6 hàng tạm, 2c xe đều đã chặn ERP. 2-D đã rà lại 14 bước một lần (`2d-erp-khong-loi/khao-sat-b-doc.md:245-256`) và chạy bộ K1–K19 (`d1-kiem-p3.md`).

| # | Bước gốc | Còn áp dụng? | Đã nghiệm thu ở đâu | Việc 2-E | Cách kiểm |
|---|---|---|---|---|---|
| 1 | Màn danh sách ERP thấy hàng mới, mã khuôn `XX-YYYY` | ✅ còn (proList sống) | 2-D1 K11 (mã `AOKA-1800QLK`, `:01`) — SQL, chưa mở màn | **làm lại** trên hàng đi hết luồng | Playwright ERP 8090 `admin/products` gõ mã, đếm dòng DOM + SQL mã |
| 2 | Popup tìm hàng ở màn bất kỳ tìm thấy hàng mới (BB-6) | ✅ còn — **nghĩa đổi**: chỉ thấy khi `pcc.status=3` ở công ty đang làm **và** đã xếp catalog (mặc định popup) | 2-D1 K2/K4 trên popup CŨ (đã thay ruột ở P4); P4 có PHPUnit picker 41 ca + ERP 178 | **làm mới**: (i) hàng status 1 KHÔNG hiện, (ii) sau khi thành 3 thì hiện, (iii) công ty khác chưa lấy về không hiện | Playwright ERP: popup ở báo giá + phiếu xuất kho + hợp đồng mua; SQL đối chiếu |
| 3 | Mở màn **Sửa** ERP hiện đủ dữ liệu | ❌ route sửa chặn (2-D) ⇒ **thay bằng màn Chi tiết `productShow`** | 2-D1 K13 (sửa ⇒ 403 + link HRM) | **làm mới** bản thay: chi tiết ERP đủ tab (thông tin, ĐVT, giá công ty, NCC, ảnh, thông số) | Playwright ERP `admin/products/{id}/show`, đếm ô có giá trị, 0 lỗi console (N51 đã sửa) |
| 4 | Lập báo giá / phiếu xuất kho có hàng mới — chọn được, **giá đúng** | ✅ còn | 2-D1 K10 (4 màn, giá 0 vì chưa có luồng giá); G3/G6 `compare` 113.484 cặp 0 lệch (đọc giá ERP = HRM) | **làm mới** ca xuyên suốt: hàng có giá sau duyệt ⇒ ERP báo giá ra đúng giá của công ty chứng từ | Playwright ERP báo giá (không Lưu, hoặc Lưu rồi xoá theo id), so ô giá DOM với `product_unit_prices` |
| 5 | Người tạo / Người cập nhật đúng tên (BB-5) | ✅ còn | 2-D1 K19 (audit observer), `ProductLifecycleService` gán `updated_by` ở xoá/khoá/mở khoá (`:149,248,340`) | gộp vào bước 1/3 | SQL `created_by/updated_by` + DOM cột Người tạo ERP |
| 6 | Sửa giá công ty `is_new_company` ⇒ không đổi ngay, sinh chờ duyệt | ✅ còn — **nay ở HRM** (màn Cập nhật giá bán 1657) | G4/G5 PHPUnit (`ProductPriceScreenApiTest`, `ProductPriceApprovalApiTest`), e2e `product-prices-ui` 6/6, `product-price-approvals-ui` 8/8 (`gia-theo-cong-ty/g6-plan.md:62-63`) | **coi như đã nghiệm thu**; chỉ chạy lại khi user muốn 1 ca xuyên suốt (Cty 8 sắp bị loại — N69) | — / PHPUnit chạy lại |
| 7 | Màn Duyệt giá thấy phiếu | ✅ — **màn duyệt nay ở HRM**; ERP chỉ còn link | G5 e2e; G6 đo menu ERP "Duyệt giá bán (HRM)" đúng href (`g6-plan.md` Q-G6-2) | đã nghiệm thu | — |
| 8 | Duyệt ⇒ giá áp dụng, cờ về 0 | ✅ (HRM) | G5 PHPUnit/e2e | đã nghiệm thu; **phần ERP đọc giá mới** gộp vào bước 4 | — |
| 9 | Công ty không bật duyệt ⇒ giá đổi ngay | ✅ (HRM) | G4 PHPUnit + e2e | đã nghiệm thu | — |
| 10 | Không quyền `Quản lý giá` sửa hàng ⇒ giá giữ nguyên (BB-2) | ✅ — nay: form hàng hoá **không ghi giá** (C2/C3 `design.md:1093-1094`), route giá gate 1657 | `ProductWriteApiTest` (giá ERP đã khai giữ nguyên `:244-250`), G4 ca 403 | đã nghiệm thu; chạy lại PHPUnit | PHPUnit |
| 11 | Đếm 12 bảng trước/sau — chỉ tăng đúng số vừa tạo | ✅ còn — **mở rộng** thêm bảng mới `product_company_units`, `product_business_catalogs`, `product_approves/pap`, `catalog_histories` | 2-D1 K11 (từng id), G6 CHECKSUM 42 bảng | **làm lại** quanh đợt E2E của 2-E | SQL so TỪNG DÒNG (không `GROUP_CONCAT` — memory checksum giả) |
| 12 | `products.code` rỗng = 0 | ✅ | đo 14/10: **0** | chạy lại cuối đợt | SQL |
| 13 | Mã trùng = 0 | ✅ | đo 14/10: **0** | chạy lại cuối đợt | SQL |
| 14 | Tạo đồng thời HRM + ERP cùng hãng+model ⇒ cả 2 lưu, mã khác | ❌ ERP hết đường tạo hàng ⇒ **thay bằng 2 lượt tạo đồng thời ở HRM** (retry `23000 products_code_unique`, `ProductWriteService.php:88-113`) | `ProductCodeGeneratorTest` (hậu tố `:01`, `:02`) — **chưa có ca nào ép đường retry khi va chạm UNIQUE** | **làm mới** | PHPUnit (giả va chạm: chiếm mã giữa generate và save) hoặc 2 request song song |

**Tóm lại:** còn phải làm thật: bước **1, 2, 3', 4, 5, 11, 12, 13, 14'** (một kịch bản xuyên suốt trên 1 hàng HRM đi hết luồng tới status 3). Bước **6–10** đã nghiệm thu ở G4/G5/G6 — chỉ chạy lại PHPUnit làm bằng chứng.

**Điều kiện tiên quyết cho kịch bản xuyên suốt** (rút kinh nghiệm 2-D1 `d1-kiem-p3.md:20-24`):
- Dựng fixture cây phân loại (Tính chất › Nhóm CN › Nhóm SP › Loại SP + Đặc tính) và nhánh catalog có Lĩnh vực qua API HRM — DB dev đang rỗng (B5/B6).
- Đưa hàng tới status 3: chạy đúng luồng Phase 7 (YCHG→YCTG→PTG→KQ→duyệt) **hoặc** dựng tắt bằng SQL — cần user chốt (Q6).
- ERP 8090 trên worktree `wt-erp-2d1`, DB `hrm_erp_giacty`; đăng nhập form `/login` (e2e_assign); ERP đọc quyền theo `App\Employee` ⇒ cần role tạm ERP (memory "local dev được cấp quyền để test", gỡ + xoá cache sau).
- Tránh tạo chứng từ kho thật (phiếu nhập/xuất cần chuỗi duyệt + ghi tồn — 2-D1 đã bỏ P1/P2): kiểm ở form, không Lưu, hoặc Lưu báo giá rồi xoá đúng id.

---

## 4. Câu hỏi tồn cần user chốt (hỏi LẦN LƯỢT từng câu)

| # | Câu | Phương án · hệ quả | Đề xuất |
|---|---|---|---|
| Q1 | **Màn nào có nút Xuất Excel?** | (a) **4 màn**: Kho dữ liệu · Dữ liệu công ty · Đang kinh doanh · Nhập thông tin — thống nhất (skill list-page coi Xuất là bộ bắt buộc), thêm 1 màn so mockup · (b) đúng mockup 3 màn, bỏ Nhập thông tin · (c) 5 màn, thêm Hàng tạm (chốt luôn Q12 Phase 6 còn trống). Chi phí thêm màn gần như 0 vì cả 5 màn dùng chung `ProductListPage` | ⭐ (c) 5 màn — cùng 1 component, 1 endpoint, chỉ khác bộ cột |
| Q2 | **Có làm IMPORT Excel hàng hoá ở 2-E không?** | (a) **Không** — chỉ xuất; tạo/sửa hàng qua form (đúng mockup + D1). Hệ quả: không còn đường nhập hàng loạt (ERP đã chặn 4 import) · (b) Có — phải chốt thêm: tạo mới hay cập nhật, cột nào, sinh mã, catalog, trạng thái theo công ty, quyền ⇒ thành đợt lớn riêng, ảnh hưởng BB-3/BB-4 | ⭐ (a); nếu cần nhập hàng loạt (vd quy đổi cây phân loại B6, xếp catalog) thì mở đợt riêng sau |
| Q3 | **Cột Catalog ở màn Kho dữ liệu** (hàng mọi công ty; catalog là theo công ty) | (a) Kho **không** có cột Catalog (giữ như màn hiện tại); cột chỉ ở Dữ liệu công ty + Đang kinh doanh, ghi Tiểu mục của **công ty đang làm** · (b) Kho có cột Catalog = Tiểu mục của công ty đang làm (hàng công ty khác chưa lấy về ra trống) · (c) Kho ghi Tiểu mục của **mọi** công ty kèm tên công ty — lệch D1-a ("chỉ ghi Tiểu mục") | ⭐ (a) — đúng màn hiện tại, đúng D1-a |
| Q4 | **Bộ cột của file** | (a) = bộ cột khả dụng của từng màn (~22–25 cột, tick sẵn cột đang hiện, khuôn registry) · (b) (a) + nhóm cột "đủ thông tin" như ERP cũ (thông số cơ bản, tên khai HQ, HS code, thuế NK/BVMT, trọng lượng, kích thước, NCC, phụ kiện tiêu chuẩn…) — file dùng tra cứu/đối soát thay bộ 45 cột ERP vừa gỡ; tốn thêm query + đo hiệu năng · Giá: **không** có cột giá ở cả 2 phương án (Q2 2-B ẩn giá; giá vốn gate) | ⭐ (a) ở 2-E; (b) nếu user cần thay thế đúng file ERP cũ thì liệt kê cột cần |
| Q5 | **Xuất "Hàng chưa có công khoán"** (kế toán, ERP gỡ 13/10) có làm trong 2-E? | (a) Không — ghi việc riêng (thuộc nhóm công khoán/giá) · (b) Có — thêm 1 bộ lọc "Chưa có công khoán" (`norm` rỗng) ở màn Dữ liệu công ty, xuất bằng chính nút Xuất · (c) Có — file riêng khuôn ERP | ⭐ (b) — rẻ, không thêm màn; cần user xác nhận định nghĩa "chưa có công khoán" (`products.norm` NULL/0) |
| Q6 | **Kịch bản nghiệm thu xuyên suốt**: đưa hàng HRM mới tới Đang kinh doanh bằng cách nào? | (a) chạy **đúng luồng Phase 7** (YCHG→YCTG→PTG→KQ→duyệt giá) bằng UI/API — chứng minh thật nhất, nhưng dài, nhiều quyền, nhiều bảng phải dọn · (b) tạo hàng qua API HRM rồi **SQL đặt `pcc.status=3` + giá** — nhanh, nhưng bỏ qua đường chuyển trạng thái thật · (c) (b) cho bước 1–5 + dựa vào nghiệm thu Phase 7 (T1–T7) cho đường chuyển trạng thái | ⭐ (c) |
| Q7 | **Chứng từ thật ở bước 4** (báo giá/phiếu xuất kho) trên DB dev | (a) chỉ mở form + chọn hàng + đọc giá, **không Lưu** · (b) Lưu báo giá rồi xoá đúng id · (c) đi hết tới phiếu xuất (dính tồn kho/hạch toán — 2-D1 đã bỏ) | ⭐ (a) + (b) cho báo giá |
| Q8 | **Bước 14 thay thế** | (a) PHPUnit ép va chạm UNIQUE để chạy đường retry · (b) 2 request song song thật trên dev · (c) bỏ bước 14 (ERP không còn tạo hàng; `ProductCodeGeneratorTest` đã phủ hậu tố) | ⭐ (a) |
| Q9 | **Seed quyền 1654** | (a) seeder riêng idempotent khuôn `ProductPricePermissionSeeder` (G6) — không truncate, chạy được trên prod, thêm vào runbook · (b) thêm dòng vào `PermissionsTableSeeder` (truncate cả bảng — KHÔNG chạy cả seeder, memory) + INSERT tay 1 dòng | ⭐ (a) + vẫn thêm dòng vào `PermissionsTableSeeder` để đồng bộ id (giữ chỗ) |

### Điểm tự chốt kỹ thuật (không phải nghiệp vụ — ghi để user biết, không hỏi)

1. **Đường dựng file = FE + `export-rows`** (list-page §14c): ~28,4k dòng × ~20 cột vượt xa ngưỡng 2s của `DynamicExport` (5.365×13 đã 10,8s). BE `GET master-data/products/{screen}/export-rows` trả `{headings, widths, rows, total, page, limit}`, trần 5.000/lượt; FE `exportListFile()` + popup `ExportFieldsModal` + `exportFieldsMixin` (tick sẵn cột đang hiện).
2. **1 endpoint cho cả 5 màn** (`/{screen}/export-rows`, screen ∈ whitelist), dùng lại `ProductService::index($request, $screen)` ⇒ cùng bộ lọc + cùng gate màn (company: 1652|1653; entering: 1652) **và** thêm `checkPermission:Xuất excel danh sách hàng hoá` (1654) theo công ty đang làm (fail-closed, super admin không ngoại lệ). FE ẩn nút khi không có 1654.
3. **Registry**: 1 khoá/màn `products_warehouse`, `products_company`, … (khớp `columnScreenKey`); key cột trùng key `ProductListResource`; trạng thái xuất bằng `status_text` (mixin tự map `company_status`→`_text` không được — khai `exportFieldKeyMap`); cột catalog khoá `catalogs_text` = tên Tiểu mục nối `"\n"` (D1-a), map qua `exportFieldKeyMap: { catalogs: 'catalogs_text' }`.
4. **Không dùng `ProductListResource` cho export**: tránh N+1 (`guaranteeText`, `minStockQty`, `tradingCompanyNames`, quan hệ catalog 4 tầng) — map bằng query gộp theo trang, đo `EXPLAIN` + thời gian mỗi trang (< 2s).
5. Cột số (`vat_percent`, `min_stock_qty`) trả `float` (khai `EXPORT_NUMERIC_COLUMNS`), mã hàng/barcode là chuỗi (skill export-excel §4c/§4d); không cột ảnh (bỏ `avatar` khỏi registry).
6. Không cột giá nào trong registry ⇒ không cần gate giá vốn ở export (nếu Q4 chọn (b) thì vẫn KHÔNG thêm giá).
7. Tên file: `<slug-man>_<mã cty>_<ddmmyyyy>.xlsx`; tiêu đề hàng 2 = tên màn; letterhead công ty đang làm (listExportFile làm sẵn).
8. Test: PHPUnit export-rows (đúng cột theo `fields`, key lạ bị bỏ, catalog nhiều nhánh ra nhiều dòng trong ô, 403 khi thiếu 1654, 403 khi thiếu quyền màn, phân trang + trần limit) + e2e spec mới `products-export-ui.spec.ts` (có quyền / không quyền, đọc file bằng ExcelJS đo ô) + Playwright MCP đo DOM nút/popup/dòng tiến độ.

---

## 5. Đề xuất chia việc

| Task | Nội dung | Repo · nhánh | File chính | DB |
|---|---|---|---|---|
| **T1** | Quyền 1654: seeder idempotent + dòng giữ chỗ trong `PermissionsTableSeeder` + test seeder; runbook thêm bước | hrm-api · `feat/cdhh-2e-excel` từ `feat/chuyen-doi-hang-hoa` | `Modules/MasterData/Database/Seeders/ProductExportPermissionSeeder.php` (mới), `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, `gia-theo-cong-ty/runbook-trien-khai.md` | chạy seeder riêng vào `hrm_erp_giacty` (1 INSERT) — **cần hỏi** |
| **T2** | BE `export-rows` 5 màn + registry + map catalog Tiểu mục + gate 1654 + PHPUnit | hrm-api · cùng nhánh | `Modules/MasterData/Routes/api.php`, `Http/Controllers/V1/Product/ProductController.php` (hoặc `ProductExportController` mới), `Services/Product/ProductExportService.php` (mới), `app/ExcelExport/ExportColumnRegistry.php`, `Tests/Feature/ProductExportApiTest.php` | không ghi (test transaction) |
| **T3** | FE nút Xuất Excel (`secondary status="success"`) + `ExportFieldsModal` + `exportFieldsMixin` + `exportListFile` + dòng tiến độ, gate 1654, 5 màn qua `ProductListPage` + cờ `export` trong `product-list-screens.js` | hrm-client · `feat/cdhh-2e-excel` | `components/product/ProductListPage.vue`, `utils/product-list-screens.js` | — |
| **T4** | Kiểm FE: Playwright MCP (đo nút, popup tick sẵn, file tải về đúng cột/dòng, ô catalog nhiều dòng, không quyền không thấy nút + API 403) + e2e spec mới, chạy `--workers=1` (chỉ khi user yêu cầu chạy bộ) | `HRM/e2e` (ngoài git) | `e2e/tests/master-data/products-export-ui.spec.ts` (mới) | role tạm + fixture catalog nhiều nhánh, gỡ sau |
| **T5** | Nghiệm thu "ERP không vỡ" (bản cập nhật mục 3): fixture phân loại + catalog → hàng HRM → status 3 (theo Q6) → ERP 8090 bước 1/2/3'/4/5 + SQL 11–13 + PHPUnit bước 14' + chạy lại PHPUnit G4/G5 (bước 6–10) + PHPUnit ERP; ghi `excel-nghiem-thu-2e/nghiem-thu.md`; dọn đúng id | ERP `wt-erp-2d1` (chỉ chạy, không sửa) + HRM | (bước 14' PHPUnit ở hrm-api nếu Q8=(a)) | ghi fixture vào `hrm_erp_giacty` rồi xoá đúng id + role tạm ERP — **cần hỏi** |

Thứ tự: T1 → T2 → T3 → T4 → T5 (T5 độc lập với T1–T4, chạy song song được). Merge: nhánh con → nhánh chung `feat/chuyen-doi-hang-hoa` (memory: KHÔNG merge vào gop_db). ERP không có thay đổi code dự kiến.

Việc ngoài luồng phát hiện khi khảo sát (ghi lại, không làm ở 2-E):
- Dữ liệu dev không có hàng nhiều nhánh catalog (21 dòng, 1 Tiểu mục) — không phải lỗi, chỉ cần fixture.
- `ProductListResource` N+1 ở 3 trường theo công ty — ảnh hưởng tốc độ màn danh sách 100 dòng/trang; đo khi làm T2, nếu > 2s thì ghi N mới.

## 6. Chốt của user 14/10
| # | Chốt |
|---|---|
| Q1 | **Cả 5 màn** có nút Xuất (Kho dữ liệu · Dữ liệu công ty · Nhập thông tin · Đang KD · Hàng tạm) — đóng luôn Q12 Phase 6 |
| Q2 | **Không Import** — chỉ xuất |
| Q3 | Kho dữ liệu **không** có cột Catalog; 4 màn còn lại ghi Tiểu mục của công ty đang làm (nhiều nhánh xuống dòng trong ô) |
| Q4 | **Theo cột màn, không có cột giá** |
| Q5 | Xuất "Hàng chưa có công khoán" — **để sau** (ghi N108) |
| Q6 | Đưa hàng HRM tới trạng thái popup ERP thấy được: **"Sẽ tự xử lý bằng form xây dựng catalog đã làm"** ⇒ làm rõ: **Claude làm trong T5** — tạo hàng bằng form HRM, xếp catalog bằng popup Xây dựng catalog thật (Playwright), Đang KD bằng nút sẵn có trên UI; cây phân loại tối thiểu dựng qua API; dọn đúng id. KHÔNG đặt catalog/trạng thái bằng SQL |
| Q7 | Bước 4: **lưu 1 báo giá ERP rồi xoá đúng id**; chứng từ khác chỉ mở form |
| Q8 | Bước 14': **PHPUnit ép trùng mã** (đường retry `products_code_unique`) |
| Q9 | Quyền 1654: **seeder riêng idempotent** (khuôn G6) + dòng giữ chỗ trong `PermissionsTableSeeder`; 1654 trống trên mọi nhánh remote + DB (kiểm 14/10) |
