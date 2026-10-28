# Report T3 + T4 — A3 (2-E) FE Xuất Excel 5 màn hàng hoá — 14/10/2026

**Trạng thái: DONE** (lo ngại nhỏ ở mục 7).

## 1. Commit (chưa push, chưa merge)

| Repo · nhánh | Commit | Nội dung |
|---|---|---|
| hrm-api · `feat/cdhh-2e-excel` | `9096a1cdc` | Ruling Q4 "theo cột màn": bỏ `catalogs_text` khỏi registry `products_entering` + `products_temp` (`app/ExcelExport/ExportColumnRegistry.php`, 2+/3-), sửa assert trong `ProductExportApiTest` (ca `catalog_nhieu_nhanh…` giờ assert KHÔNG có). Còn Catalog: chỉ company + trading. |
| hrm-client · `feat/cdhh-2e-excel` | `a8ca067d8` | T3 — `components/product/ProductListPage.vue` (130+/5-), `utils/product-list-screens.js` (34+/0-) |
| e2e (ngoài git) | — | Mới: `wt-chuyen-doi-hang-hoa/e2e/tests/master-data/products-export-ui.spec.ts` |

PHPUnit `ProductExportApiTest` chạy lại sau khi sửa registry: **OK 9/9 (342 assertion)**.
Toàn file LF, numstat chỉ xoá đúng các dòng đã thay.

## 2. T3 — FE

- Nút **Xuất Excel** (`secondary status="success"`, icon `ri-file-excel-2-line`) ở slot `#actions`, nằm trước nút Cấu hình cột.
  Hiện ở cả 5 màn, gate `hasAPermission('Xuất excel danh sách hàng hoá')` (fail-closed). Không có quyền thì cả nút lẫn
  `ExportFieldsModal` đều không render.
- Theo khuôn chung (wr-quotations): `exportFieldsMixin` + `ExportFieldsModal` (id `export-fields-products-<slug>`) +
  `exportListFile` (tải theo trang 2.000 dòng). Dòng tiến độ `.export-progress` đi qua 3 nấc: "Đang chuẩn bị dữ liệu…" →
  "Đã tải N/T dòng…" → "Đang dựng file N/T dòng…". Khi đang xuất thì nút bị khoá (`interactable`). 403 không toast lần 2.
- Danh sách trường của popup lấy từ `productExportFields(screen)`: Mã hàng + cột của màn theo đúng thứ tự trên bảng, bỏ Ảnh, ánh
  xạ qua `PRODUCT_EXPORT_FIELD_KEY_MAP` (`catalogs→catalogs_text`, `company_status→status_text`,
  `open_requests→open_requests_text`). Nhãn dùng `columnTitles` (temp: "Người tạo"). Khớp 1-1 registry BE.
- Bộ lọc gửi đi = `requestFilters()`: tách ra từ `loadData`, nên dùng đúng `requestKeys` của màn (có 4 ô catalog, không gửi `_model_label`).
  `loadData` cũng dùng chung hàm này, hành vi không đổi.
- Tên file `<exportFileSlug>_<mã cty>_<ddmmyyyy>.xlsx`, ví dụ `hang_dang_kinh_doanh_TPE_14102026.xlsx`. Mã công ty lấy từ
  `state.companies` (`company_roles` của e2e_assign rỗng nên không dùng được). Sheet = tên màn, hàng 1 = tên màn viết hoa.
  Letterhead, viền và wrapText do `listExportFile` lo.

## 3. Playwright MCP — số đo DOM (cổng 3031/8031, e2e_assign, Cty 1)

Trước khi sửa: màn trading không có nút "Xuất Excel" nào (danh sách nút đo được: Cài đặt bộ lọc · Tìm kiếm nâng cao ·
Tìm kiếm · Làm mới · Lập yêu cầu hỏi giá).

| Màn | Bộ lọc thử | Tổng API danh sách | Nút | Trường popup | Tick sẵn = cột đang hiện | Catalog trong popup | Số dòng file | Tên file |
|---|---|---|---|---|---|---|---|---|
| warehouse | `TEWI` | 73 | 1 | 22 | 12 = 12 ✓ | không | 73 | `kho_du_lieu_hang_hoa_TPE_14102026.xlsx` |
| company | `TEWI-AQUA` | 1 | 1 | 22 | 12 = 12 ✓ | có | 1 | `du_lieu_hang_hoa_cong_ty_TPE_…` |
| entering | `TEWI-823219` | 1 | 1 | 21 | 10 = 10 ✓ | không | 1 | `hang_hoa_nhap_thong_tin_TPE_…` |
| trading | `TEWI-AQUA` | 1 | 1 | 22 | 11 = 11 ✓ | có | 1 | `hang_dang_kinh_doanh_TPE_…` |
| temp | `TEWI-828127` | 1 | 1 | 22 | 14 = 14 ✓ | không | 1 | `hang_tam_TPE_…` |

- Nút trading: hộp 101×32 tại (1257, 267), màu chữ `rgb(21,128,61)`.
- Request đúng bộ lọc + thứ tự tick: `…/trading/export-rows?keyword=TEWI-AQUA&sort_desc=true&fields=code,name,model_name,…,catalogs_text,status_text&page=1&limit=2000`.
- **Xuất cả màn trading, không lọc:** 28.369 dòng, 15 trang `export-rows` đều 200, **21,3 s** từ lúc bấm tới lúc có file. File
  2,1 MB, STT liên tục (hàng 3 → 1, hàng 2002 → 2000, hàng 2003 → 2001, dòng cuối → 28369). Dòng tiến độ đo được đủ 3 nấc.
  Sau khi xong, `.export-progress` còn 0 phần tử.
- **Không quyền 1654** (sau khi gỡ role tạm): cả 5 màn `has1654=false`, 0 nút, 0 popup, gọi thẳng `export-rows` ⇒ **403**.
- Console: chỉ có lỗi 404 ảnh `e2e.png` có sẵn từ trước, không liên quan.

## 4. Nội dung file Excel đo được (ExcelJS)

- company / trading, dòng `TEWI-AQUA`: heading `STT, Mã hàng, Tên hàng hoá, Model, Tính chất hàng hoá, Nhóm chức năng, Nhóm sản phẩm,
  Loại sản phẩm, Thương hiệu, Hãng sản xuất, Catalog kinh doanh, [Công ty quản lý,] Trạng thái`. Ô Catalog =
  `"E2EX2E Tiểu mục A\nE2EX2E Tiểu mục B"`, alignment `{vertical: top, wrapText: true}`. Trạng thái "Đang kinh doanh".
- warehouse: không có cột Catalog. Ô "Công ty đang kinh doanh" nhiều công ty, mỗi công ty 1 dòng (`\n`).
- entering: heading 11 cột (không Catalog), trạng thái "Đang nhập thông tin".
- temp: heading 15 cột `…, YCHG đang chứa, Trạng thái, Lý do không duyệt, Người tạo, Ngày tạo`, trạng thái "Hàng tạm".
- Không file nào có cột chứa chữ "giá". Hàng 1 là tiêu đề màn viết hoa; khối ký tên ở cuối.

## 5. e2e `products-export-ui.spec.ts`

6 ca: N1 (không quyền: 5 màn 0 nút, 0 popup, API 403) và 5 ca có quyền. Mỗi ca có quyền kiểm: đúng 1 nút, không
đè nút cấu hình cột, popup có đúng số trường của màn, tick sẵn == cột đang hiện (cùng thứ tự), có/không trường Catalog, không
trường giá, request mang `keyword` của bộ lọc, tên file, sheet, tiêu đề, heading = STT + cột tick, số dòng = `meta.total`, STT
liên tục, ô Catalog `\n` + wrapText, chữ Trạng thái. ExcelJS nạp từ `hrm-client/node_modules`, đổi được bằng env `HRM_CLIENT`
(`HRM/e2e/node_modules` không có exceljs).

Lệnh: `API_BASE=http://127.0.0.1:8031 BASE_URL=http://127.0.0.1:3031 npx playwright test products-export-ui --project=chromium --no-deps --workers=1 --retries=0`
(node 20) ⇒ **`6 passed (1.3m)`**: 0 failed, 0 did not run.

## 6. Dữ liệu thử + role tạm — đã dọn

- Fixture: cây catalog `E2EX2E` (Chương › Mục › Tiểu mục A/B), 2 dòng `product_business_catalogs` cho hàng `TEWI-AQUA`
  (id 3897, Cty 1). Hàng `TEWI-823219` (pcc 12503) và `TEWI-828127` (pcc 12507) được **tạm đổi** `pcc.status` từ 3 sang 1 / 6,
  vì giacty có 0 hàng ở 2 màn này. Cả hai đã trả lại 3. Ở lượt MCP: role 121714, cluster 6086/6087, pbc 6948/6949. Lượt
  spec dùng id mới, chọn động và dọn theo tên/tiền tố.
- Role tạm: lượt MCP `E2E 2E tam - xuat excel MCP` (id 121714), lượt spec `E2E 2E tạm - xuất excel hàng hoá`. Cả hai đã gỡ
  (roles 0 dòng, `role_has_permissions` của 1654 = 0) và đã `cache:clear`.
- Đếm trước/sau: `products` 45.890 → 45.890 · `product_business_catalogs` 21 → 21 · `catalog_histories` 3.541 → 3.541.
  `job_clusters` E2EX2E = 0.

## 7. Lo ngại / ngoài luồng

1. Thời gian xuất cả màn 28k dòng là ~21 s ở dev (15 lượt × ~0,5–1 s HTTP, cộng dựng file ở trình duyệt). Có dòng tiến độ nên user
   không bị treo câm, nhưng lâu hơn số đo service ở t12 (chưa tính HTTP/JWT).
2. Spec đổi tạm `pcc.status` của 2 hàng thật thay vì tạo hàng mới, để khỏi dựng cây phân loại và cả bộ giá. afterAll trả lại
   có điều kiện. Nếu tiến trình bị kill cứng giữa chừng thì phải tự trả 2 dòng pcc về 3. Lượt chạy kế tiếp KHÔNG tự sửa, vì
   query chọn hàng chỉ lấy hàng status 3.
3. `company_roles` của e2e_assign rỗng nên tên file lấy mã công ty từ `state.companies`. Đáng xem ở các màn khác đang dùng
   `currentCompanyName()` (lấy từ `company_roles`), vì có thể đang ra "công ty đang làm việc" thay cho tên thật. Không vá trong đợt này.
4. Brief ghi ExcelJS nằm ở `HRM/e2e/node_modules` nhưng thực tế không có. Spec dùng bản của hrm-client.
