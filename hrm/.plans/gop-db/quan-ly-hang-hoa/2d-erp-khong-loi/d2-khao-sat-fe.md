# Đợt 2-D2 — Khảo sát FE: màn "Cập nhật giá hàng hoá" + "Duyệt giá" (09/10/2026)

> Khảo sát CHỈ ĐỌC: không sửa source, không ghi DB, không checkout/stash, không bật/tắt server.
> **ERP:** worktree `websites/wt-erp-2d1` (nhánh `feat/2d1-erp-khong-loi`, `b2f1761789`). **HRM:** worktree
> `websites/wt-chuyen-doi-hang-hoa/hrm-client` (nhánh `feat/chuyen-doi-hang-hoa`, `9b05f7b42`) + `.../e2e`.
> Đọc trước: `khao-sat-c-gia.md` (§1 L1/L5, §2.5 HĐ1–HĐ10, §4.2), `ton.md` mục C (QC-0…QC-10), `../SO-CHOT-VA-TON.md` §1 + §6,
> `../2c-ghi/chot.md`. Không đo được DB local lần này (mysql CLI từ chối đăng nhập bằng `.env` của worktree) ⇒ các số đếm
> (hàng có công thức lắp ráp, ĐVT có lý do sửa giá…) để lúc lập plan.

---

## 0. Tóm tắt — những điều khảo sát C chưa thấy

1. 🔴 **Duyệt giá không phải màn độc lập: nó là một NHÁNH của chính `updatePrice`.** Khi công ty tạo hàng bật
   `companies.is_company_price` (+ `is_all_brand` / `brand_ids`), nút Lưu ở màn Cập nhật giá **không ghi giá** mà ghi vào
   `*_wait_approve` + bật cờ 1 + sinh `product_approves`/`product_approve_prices` + bắn thông báo cho người có quyền
   *Duyệt giá hàng hoá* (`ProductsController.php:2647-2663`, `:2745-2785`, `:2910-3040`). ⇒ Port Duyệt giá = port cả
   nhánh "gửi duyệt" của màn Cập nhật giá + bộ lọc "Chờ duyệt giá / Không duyệt" + badge trên từng ô. Hai màn phải làm
   cùng một đợt và dùng chung model FE.
2. 🔴 **Duyệt/Không duyệt ở ERP đổi luôn `products.status`** (Duyệt → 1 `HOAT_DONG`, Không duyệt → 5 `KHONG_DUYET`;
   `ProductApprovesController.php:259, :299, :388, :438`). Ở HRM, trạng thái "Đang kinh doanh" của hàng cũ được **suy ra từ
   `products.status = 1`** (`hrm-api/.../Entities/Product/Product.php:368-391`) ⇒ một lần "Không duyệt" là hàng **biến mất khỏi
   màn Hàng đang kinh doanh** của HRM. Phải hỏi (F2).
3. 🔴 **Ô "Hãng cần duyệt" ở Quy chế HRM trỏ nhầm bảng.** ERP lưu `companies.brand_ids` là **id Hãng SX** (màn quy chế ERP nạp
   `Manufacture::getForSelect()` vào `$scope.brands` — `common/companies/regulation.blade.php:704`; `updatePrice` so với
   `product->manufacture_id` `:2655-2660`), còn HRM `RegulationTabRegistry.php:388-392` khai `'options' => 'brands'` và
   `RegulationConfigService.php:551-552` đọc **bảng `brands` (Thương hiệu)**. Ai cấu hình ở HRM là ghi id thương hiệu vào cột
   id hãng ⇒ điều kiện gửi duyệt sai im lặng. Cùng lỗi ở `new_brand_ids`. (F3)
4. **Thao tác nhập trong ERP nhiều "phép tính ngầm" hơn khảo sát C ghi** (mục 1.4): sửa **Giá bán lẻ** là ghi đè giá/hệ
   số/ĐMGG của **cả 4 loại giá 2–5** (`ProductUnit.blade.php:111-148`); sửa hệ số là tính lại giá = `round(hệ số × giá vốn / 100) × 100`;
   giá hiệu lực tính `hệ số × giá vốn` **không làm tròn**; TMĐT không thêm được giá hiệu lực.
5. **ERP KHÔNG hiển thị công khoán (`norm`) và ĐMGG thanh lý (`liquidation_sale_max_percent`) trên màn này** — chỉ gửi lại
   nguyên giá trị cũ (`ProductWithPrice.blade.php:64-75`). Khảo sát C §4.2 liệt kê cột "ĐMGG thanh lý" và HĐ5 ghi cột này ⇒
   tự chốt: **không hiện, BE không đụng** (đúng ERP: giá trị không đổi). Công khoán: QC-8 chốt "chỉ hiển thị" ⇒ hiện dạng chữ
   dưới mã hàng (ERP không có, là phần thêm theo QC-8).
6. **Bulk "Duyệt" của ERP hỏng** — FE gửi khoá `price` (`products_approve/partials/ProductApproved.blade.php:51`) nhưng BE đọc
   `prices` (`ProductApprovesController.php:448`) ⇒ duyệt hàng loạt đặt hệ số + ĐMGG = 0, giá hiệu lực = 0, bỏ qua mọi sửa của
   người duyệt; còn giá hiện hành lấy `$price->price` (giá CŨ, `:473`) chứ không phải giá đề xuất. Chưa ai dính vì
   `product_approves` chưa từng có dòng. Port: sửa theo nghĩa đúng (tự chốt, không hỏi).
7. **Khuôn HRM:** không có component bảng nhập tại chỗ có rowspan để dùng lại; `V2BaseDataTable` không hỗ trợ rowspan.
   Khuôn gần nhất = bảng viết tay `v2-table v2-form-table` trong `V2BaseTableScroll` (`components/product/form/ProductFormUnitsTable.vue`).
   Lịch sử dùng `V2BaseModal` + `SystemInfoSection` có `endpoint-base` (`components/modal/SettingHistoryModal.vue`).
   Popup lý do dùng `$confirm({ showInput })` (`components/modal/base-confirm-modal.vue:40-43, :92-93`).
8. **Menu:** phân hệ `master-data` là hub; nhóm "Hàng hoá" (`components/subsystem-menu/master-data.js:59-86`) đang 4 mục ⇒ thêm 2
   mục thành 6 (≥ NAV_MIN 5, không vỡ panel). Lối phụ cho "Hàng hoá chờ duyệt giá" ở Bán hàng → Phê duyệt (`sale-hub.js:253-279`).
9. **Đề xuất làm mockup HTML trước** (1 file, 2 màn + 3 popup) — bảng rowspan + sticky là đúng vùng bẫy §6 đã trả giá.

---

## A. Màn ERP "Cập nhật nhanh giá hàng hoá" (`products/editPrices`)

Nguồn: view `resources/views/products/editPrices.blade.php` (678 dòng) · lớp JS `resources/views/partials/classes/sale/`
`ProductWithPrice.blade.php` (79) → `ProductUnit.blade.php` (203) → `ProductPrice.blade.php` (310) → `ProductExpectedPrice.blade.php` (188)
· BE `app/Http/Controllers/ProductsController.php` `editPrices` :2296 · `getProductsAndPrices` :2313-2546 · `updatePrice` :2550-~3085.
Lối vào: menu Kế toán → Quản lý giá - CTKM → Giá bán → "Cập nhật giá nhanh" (`topmenubar.blade.php:932`); thông báo "Không duyệt" trỏ
`editPrices?status=2` (`ProductApprovesController.php:333, :398`).

### A.1 Bộ lọc (thẻ "Bộ lọc" thu gọn được, `editPrices.blade.php:72-181`)

| Ô | Kiểu | Dòng | BE | Ghi chú port |
|---|---|---|---|---|
| Tên hàng hóa | text | :82-83 | `p.name LIKE` | gộp vào ô tìm nhanh HRM |
| Mã hàng hoá | text | :105-106 | `p.code LIKE` | gộp ô tìm nhanh |
| Model | text | :111-112 | `pm.name LIKE` (INNER JOIN `product_models` ⇒ hàng không model **bị loại**) | gộp ô tìm nhanh; BE dùng LEFT JOIN (hàng HRM có thể thiếu model? — kiểm lúc plan) |
| Tồn kho (Còn/Hết) | select | :116-124 | **chết** — BE đã comment `:2499-2501` | F8 |
| Trạng thái (Tất cả / Chờ duyệt giá / Không duyệt) | select | :128-134 | `status=1` ⇒ có cờ `=1` ở ĐVT/giá/giá hiệu lực; `=2` ⇒ cờ `=2` (`:2419-2475`) | giữ — đi cùng Duyệt giá |
| Thương hiệu | select2 | :137-142 | `p.brand_id` | giữ |
| Tính chất hàng hoá (enum cũ `product_type`) | select2 | :145-150 | `p.product_type` | **thay** bằng cây phân loại mới (Tính chất → … → Loại SP) như `ProductListPage.vue:20-33` |
| Loại hàng hoá (`product_cate` cũ) | select2 | :153-158 | `p.product_cate LIKE` | **bỏ** (cây cũ) — thay bằng cây mới ở dòng trên |
| Hãng sản xuất | select2 (mọi hãng) | :161-168 | hãng khác công ty ⇒ trả `success=false` "Hãng sản xuất này không thuộc quyền quản lý của bạn!" (`:2476-2484`) | HRM: chỉ liệt kê hãng của công ty đang làm (QC-4) |
| Nút Lọc / làm mới | — | :170-179 | — | khuôn SmartFilterPanel |

Mặc định: không lọc, sắp `p.name DESC` (`:2523`), sắp được theo Mã, Model (`:193-205`). Phạm vi: `p.status IN (1,2,5)` (`:2526`);
**không** lọc theo công ty — danh sách hiện mọi hàng, chặn ở lúc Lưu (F1). Không quyền *Cập nhật nhanh giá hàng hóa* ⇒ trả rỗng
"Không có quyền!" (`:2510-2515`). Phân trang `per_page = 20` cố định, `uib-pagination` (`:377-380`, `:466`).

### A.2 Bảng — mỗi hàng là 1 khối, ĐVT chọn bằng select trong khối

Tiêu đề **2 tầng** (`:187-225`): tầng 1 các cột rowspan=2 + nhóm "Giá" colspan=7; tầng 2 là 7 cột con. `thead` sticky top
(`:9-14`) + 3 cột đầu dính trái (`head-col-1/2/3` left 0/250/365px, `:15-33`).

| Cột | rowspan | Ô | Dòng |
|---|---|---|---|
| Tên hàng hóa | khối | chữ + nút ✎ "Thêm lý do sửa giá" mở ô nhập `current_unit.reason_edit_price` (blur thì ẩn) + link "Xem công thức lắp ráp" (khi có `recipe_products`) + chữ đỏ "Ghi chú không duyệt: …" (`approve_comment`) | :234-244 |
| Đơn vị | khối | **select ĐVT** của hàng (nhãn `Tên (xHệ số)`), đổi ĐVT ⇒ đổi khối giá đang hiện + gọi lại tồn kho | :245-254 |
| Mã hàng hóa | khối | chữ + nút ✎ đỏ "Ghi chú cho hàng hoá" mở ô nhập `products.note` | :255-266 |
| Model · Hãng SX · Loại HH · Tính chất | khối | chữ | :267-270 |
| Tồn kho | khối | số (gọi riêng `warehouseInfo.stockOfProducts` sau khi tải danh sách, chia hệ số ĐVT) | :271, :509-530, :595-602 |
| Giá vốn | khối | **ô nhập** `current_unit.cost_price` + badge "Đang chờ duyệt"/"Không duyệt" theo `flag_price_wait_approve` | :272-279 |
| (7 ô giá của dòng đầu khối) | — | `<td colspan=7 class="p-0">` trống — dòng đầu khối KHÔNG có giá | :280 |
| Hành động | khối | 1 nút 💾 Lưu (spinner khi đang lưu) | :281-286 |
| **Loại** | 1 + số giá hiệu lực | tên loại giá + link "Thêm giá hiệu lực" (chỉ khi chưa có và **không phải loại 6**) | :289-296 |
| Giá hiện tại | 1 | số `price_old` (giá thật trong DB, bỏ qua giá chờ duyệt) | :297 |
| Hệ số | 1 | ô số step 0.1; loại 6 khoá trừ khi tick "Chỉnh sửa" | :298-309 |
| Giá công thức | 1 | **chỉ đọc** = giá vốn × hệ số (loại 6 làm tròn nghìn) | :310 |
| Giá mới | 1 | ô nhập; loại 6 khoá trừ khi tick "Chỉnh sửa" | :311-322 |
| ĐMGG | 1 | ô số step 1; loại 6 khoá trừ khi tick "Chỉnh sửa" | :323-334 |
| Ngày hiệu lực | 1 | chữ xanh "Đang áp dụng" | :335 |
| *(dòng giá hiệu lực, 0–1 / loại)* | — | `-` · hệ số · giá công thức · giá · ĐMGG · ô ngày `dd/mm/yyyy` + nút ✕ xoá; loại 6 khoá hết | :337-371 |

rowspan khối = `1 + Σ(1 + số giá hiệu lực)` trên 6 loại giá (`ProductWithPrice.blade.php:39-48`; loại giá `ProductPrice.blade.php:250-252`).
Khối luôn đủ **6 loại giá**: thiếu loại nào FE tự thêm dòng rỗng (`syncPrices` `ProductWithPrice.blade.php:56-63`; loại 5 chèn
vị trí 2 `ProductUnit.blade.php:98-105`) — khớp HĐ1 (ERP BE cũng tự sinh `:2724-2727`).

**Popup "Xem công thức lắp ráp"** (`:387-445`): bảng STT · Mã hàng · Tên hàng · Code đặt hàng · ĐVT · Số lượng, chỉ đọc, nút Đóng.

### A.3 Lưu — theo TỪNG KHỐI (hàng × ĐVT đang chọn), không có lưu toàn trang

- Nút 💾 gửi `POST /admin/products/{id}/updatePrice` với `submit_data` (`ProductWithPrice.blade.php:64-75`):
  `unit_id` (ĐVT đang chọn) · `norm` (giá trị cũ, không có ô sửa) · `note` · `cost_price` · `note_edit_price` (không có ô nhập ở màn này
  ⇒ luôn rỗng/giữ) · `reason_edit_price` · `liquidation_sale_max_percent` (giá trị cũ, không có ô) · `prices[6]` (mỗi loại:
  `price_type_id, coefficient, sale_max_percent, price, 3 cờ is_manual_*_online, expected_prices[≤1]{id, coefficient,
  sale_max_percent, price, effect_date}`).
- Sửa xong ĐVT A rồi đổi sang ĐVT B: giá trị đã sửa ở A **nằm lại trong bộ nhớ, không lưu** — chỉ ĐVT đang hiện được gửi.
- Thành công: `toastr.success` "Sản phẩm đã được cập nhật giá mới" (hoặc "Yêu cầu duyệt giá hàng hoá đã được gữi!" khi nhánh duyệt),
  khối nạp lại từ `data_with_prices` BE trả (`:3129-3135` ⇒ `editPrices.blade.php:640-642`).
- Lỗi: `response.errors` gắn theo khoá `prices.{i}.coefficient` / `prices.{i}.expected_prices.{j}.price`… dưới từng ô, toast vàng
  "Cập nhật thất bại!" (`:644-645`). Lỗi nghiệp vụ (hãng khác công ty, `canEdit()` sai) trả `success=false` + message, không có `errors`.
- Validate BE (`:2552-2610`): giá vốn bắt buộc, 0 ≤ x ≤ 999.999.999.999 (min 0 báo "Bắt buộc phải nhập"); hệ số bắt buộc,
  0 ≤ x < 100; giá bắt buộc 0…12 chữ số; ĐMGG 0…100; giá hiệu lực tối đa 1/loại, giá + hệ số (≤ 99) bắt buộc, ngày bắt buộc +
  **sau hôm nay**; `norm`/`liquidation` 0 ≤ x < 1000. **FE ERP không validate gì** ngoài kẹp ĐMGG 0–100 (`ProductPrice.blade.php:217-226`).

### A.4 Phép tính FE (port nguyên văn — đây là hợp đồng hành vi)

| # | Khi | Thì | Nguồn |
|---|---|---|---|
| T1 | Sửa **hệ số** loại X (≠ 6 hoặc 6 đang tick sửa tay) | Giá mới X = `round(hệ số × giá vốn / 100) × 100` (làm tròn **trăm**) | `ProductPrice.blade.php:197-204` |
| T2 | Sửa **giá mới / hệ số / ĐMGG của loại 1 (bán lẻ)** | Ghi đè **cùng trường** của **mọi loại 2–5** = giá trị loại 1 (bỏ qua loại 6) | `ProductUnit.blade.php:111-118`, gọi từ `ProductPrice:179-181, :203, :225` |
| T3 | Loại 1 đổi và loại 6 **không** tick sửa tay | TMĐT giá = `round(giá bán lẻ × configs.coefficient_ecommerce_price)` (= 1,3), hệ số = hệ số bán lẻ × 1,3, ĐMGG = 0 | `ProductUnit:119-147`, `ProductPrice:95-104, :162-172, :184-195` |
| T4 | Tick "Chỉnh sửa" của loại 6 | Mở ô tương ứng; nếu ô đang trống thì điền sẵn giá trị công thức. Bỏ tick ĐMGG ⇒ ĐMGG về 0 | `ProductPrice:24-72` |
| T5 | Hiển thị loại 6 khi không tick | luôn hiện giá trị CÔNG THỨC (không phải DB) — lưu lại sẽ ghi đè giá TMĐT cũ lệch công thức | `ProductPrice:106-160` (mode `update`: chỉ cờ tick quyết định) |
| T6 | Giá công thức | `giá vốn × hệ số`; loại 6 làm tròn **nghìn** | `ProductPrice:228-248` |
| T7 | Sửa hệ số giá **hiệu lực** | giá hiệu lực = `hệ số × giá vốn` (**không** làm tròn — lệch T1) | `ProductExpectedPrice:87-94` |
| T8 | Giá hiệu lực loại 6 | không thêm được (ẩn link :291), mọi ô khoá; BE tự tính từ giá hiệu lực bán lẻ cùng vị trí | `editPrices:340-363`, BE `:2796-2812` |
| T9 | Sửa **giá vốn** | KHÔNG tự tính lại giá (code comment sẵn) — chỉ "Giá công thức" đổi theo | `ProductUnit:66-71` |
| T10 | ĐMGG nhập ngoài 0–100 | kẹp về 0/100 (ERP) | `ProductPrice:217-226` — HRM **báo đỏ, không kẹp** (skill select-and-input-state 4b) |
| T11 | Số tiền | hiện `toLocaleString('en')`, nhập chuỗi có dấu phẩy ⇒ `parseNumberString` | `ProductPrice:13, :171`, `ProductUnit:62-64` |

Badge "Đang chờ duyệt" (cờ 1, vàng) / "Không duyệt" (cờ 2, đỏ) dưới ô giá vốn, hệ số, giá, ĐMGG, giá hiệu lực. Ô hiện giá **chờ duyệt**
(nếu cờ ≠ 0) thay cho giá thật (BE `CASE flag` `:2350-2378`), riêng "Giá hiện tại" luôn là giá thật.

### A.5 Nhánh gửi duyệt (khi công ty tạo hàng bật duyệt giá) — `updatePrice`

- Điều kiện `is_approve` (`:2647-2663`): `companies` của `products.company_id ?? công ty người dùng` có `is_company_price = 1` và
  (`is_all_brand = 1` hoặc `manufacture_id ∈ brand_ids`). **Hiện cả 8 công ty = 0** ⇒ nhánh này chưa từng chạy (`product_approves` rỗng).
- Bật: giá/hệ số/ĐMGG ghi vào `*_wait_approve`, cờ = 1 chỉ cho trường **thực sự đổi** (`:2745-2785`); giá hiệu lực ghi
  `*_wait_approve` + `flag = 1` (`:2830-2860`); giá vốn đổi ⇒ `product_units.price_wait_approve` + cờ 1 (`:2873-2882`); upsert
  `product_approves` theo (hàng, ĐVT) + `product_approve_prices` (`:2913-3120`); thông báo cho mọi người có *Duyệt giá hàng hoá*
  tại công ty đó: "Bạn có yêu cầu duyệt giá hàng hoá từ <tên>" → link màn duyệt (`:3029-3033`).
- Gửi lại khi đang chờ: ghi đè đề xuất cũ (cập nhật dòng `product_approve_prices`, xoá dòng giá hiệu lực cũ của phiếu).

---

## B. Màn ERP "Danh sách hàng hóa chờ duyệt giá bán" (`products/approvePrices`)

Nguồn: `resources/views/products_approve/list.blade.php` (727) + `partials/ProductApproved*.blade.php`, `ProductDatas.blade.php`, export
`products_approve/exports/export.blade.php`; BE `ProductApprovesController.php` (562). Menu: "Danh sách hàng hóa chờ duyệt giá bán"
(`topmenubar.blade.php:2225`, nhóm Chờ duyệt). Quyền màn `Duyệt giá hàng hoá` (`routes/web.php:587`); 4 route ghi + export **không gate** (N29).

| Phần | Nội dung | Dòng |
|---|---|---|
| Bộ lọc | Tính chất HH (enum cũ) · Loại HH (`product_cate` cũ) · Hãng SX · **Người cập nhật** (mọi NV) · Tên · Mã · Model | `list.blade.php:63-133` |
| Nút toolbar | Lọc · làm mới · **Xuất excel** (mở tab mới, toàn bộ theo lọc) · **Duyệt** (hàng loạt) · **Không duyệt** (hàng loạt) | :136-155 |
| Cột (khối rowspan = 1 + số dòng giá) | STT · ☐ (tick tất cả ở tiêu đề) · Tên (+ "Lý do sửa giá: …" xanh) · ĐVT · Model · Mã (link chi tiết ERP + 2 nút **Duyệt** / **Không duyệt** + "Ghi chú hàng hoá") · Loại HH · Tính chất · Ghi chú (`note_edit_price`) · Giá vốn (đề xuất) | :165-237 |
| Dòng giá (mỗi loại giá đổi + mỗi giá hiệu lực đổi) | Loại giá · Giá cũ · **Hệ số (ô nhập)** · **Giá mới (ô nhập)** + chênh lệch ±(xanh/đỏ) · ĐMGG cũ · **ĐMGG mới (ô nhập)** + chênh lệch · Ngày hiệu lực (hoặc "Đang áp dụng") · Người cập nhật (`mã phòng - tên`) · Thời gian (`dd/mm/yyyy HH:mm`) | :239-270 |
| Phép tính | đổi hệ số ⇒ giá = `round(hệ số × giá vốn / 100) × 100` (`ProductApprovedPrice.blade.php:24-26`); ĐMGG kẹp 0–100 | |
| Duyệt 1 dòng | **không hỏi xác nhận**; gửi giá đã sửa; BE: ghi giá + giá hiệu lực (ngày đã qua ⇒ dời về **mai**), cờ 0, giá vốn + `unit_coefficient` từ phiếu, `approve_comment = ''`, **`products.status = 1`**, xoá phiếu, ghi version/history; toast "Thao tác thành công!" | :581-620; BE :188-274 |
| Không duyệt 1 dòng | popup swal: "Danh sách mã hàng hoá không duyệt: X" + **Ghi chú (\*) bắt buộc**; BE: cờ 1 → 2 ở giá/ĐVT/giá hiệu lực, `approve_comment` + `approve_time`, **`products.status = 5`**, xoá phiếu; thông báo cho người cập nhật "Không duyệt yêu cầu duyệt giá của mã hàng X từ Y" → `editPrices?status=2` | :506-579; BE :352-412 |
| Hàng loạt | phải tick ≥ 1 (toast "Vui lòng chọn hàng hoá để duyệt/không duyệt"); Không duyệt dùng chung 1 ghi chú; lọc `pa.company_id` = công ty người dùng (bản 1 dòng thì KHÔNG kiểm — `:199-201`, `:362-364` comment) | :363-504; BE :276-350, :414-507 |
| Phạm vi | `pa.company_id = công ty người dùng`, sắp `updated_at DESC`, 20/trang | BE :137-186 |
| Xuất Excel | `danh_sach_hang_cho_duyet_gia_ban.xlsx`, có letterhead công ty; cột như bảng (bỏ Loại HH/Tính chất/Ghi chú) | BE :514-560; export :19-38 |

Lỗi ERP cần biết khi port (không mang sang): bulk Duyệt sai khoá `price`/`prices` (mục 0.6); `dd($e)` trong catch (`:270, :503`);
`changeAllProductCompleted` là getter nhưng gọi như hàm (`ProductDatas.blade.php:21`, `list.blade.php:170`); ghi đè
`product_units.unit_coefficient` từ phiếu (`:254, :490`) — trái HĐ2/C7 ⇒ HRM **không** ghi hệ số ĐVT.

---

## C. Khuôn HRM sẵn có

### C.1 Page + bố cục
- Màn danh sách hàng hoá: `components/product/ProductListPage.vue` (1.218 dòng) + 4 page vỏ `pages/master-data/products/{warehouse,company,entering,trading}.vue`
  (`extends` + `layout: 'default-sidebar'` + `productScreen`) — `trading.vue:9-13`. Màn giá **không** `extends` component này (bảng khác hẳn),
  nhưng lấy lại: `V2BaseSmartFilterPanel` + slot cây phân loại 4 cấp `#field-classification` (`ProductListPage.vue:4-58`), ô Model tìm từ máy chủ
  `V2BaseSelectRemote` (`:36-46`), mixin `PageTitleMixin`, `filterStateMixin`, (`columnCustomizationMixin` không dùng — bảng nhập không cấu hình cột).
- Bảng nhập tại chỗ: **không có component dùng lại được**. Khuôn: `<V2BaseTableScroll>` + `<table class="table table-bordered table-sm mb-0 v2-table v2-form-table">`
  với ô `V2BaseInput` / `V2BaseSelect` / `V2BaseError` (`components/product/form/ProductFormUnitsTable.vue:10-80`). Phân trang tách rời: `V2BasePagination.vue`.
  `pages/customer-care/service-price-config/index.vue` **không** phải bảng (form 2 ô) ⇒ không dùng được.
- ⚠️ Vue 2 một gốc: khối nhiều `<tr>` không tách được thành component — dùng `<template v-for>` trong `<tbody>`; tách component ở
  mức **cả bảng** và **ô** (ô tiền, ô hệ số kèm badge), không ở mức "khối hàng".
- Ô số: `utils/number-input.js` `sanitizeNumberEvent` (`:value` + `@input.native`, KHÔNG `v-model`); tiền dùng `V2BaseCurrencyInput`; ngày `V2BaseDatePicker`.
- Popup xác nhận / lý do: `$confirm({ title, message, textAccept, danger, showInput, inputLabel })` (`plugins/confirm-dialog.js` →
  `components/modal/base-confirm-modal.vue:40-43, :92-93`). KHÔNG chép `components/assign/quotation/QuotationRejectModal.vue` (b-modal thô).
- Lịch sử: `components/modal/SettingHistoryModal.vue` (vỏ `V2BaseModal` + `components/assign/SystemInfoSection.vue` với `endpoint-base`) — màn giá
  chỉ cần 1 vỏ mỏng đổi `endpoint-base` (hoặc thêm adapter BE `setting-histories/product_price/{id}` để dùng thẳng). Hàng hoá HRM hiện **chưa có lịch sử nào**.
- Cảnh báo chưa lưu: `utils/mixins/unsavedChangesMixin.js` (page có form) — override `unsavedSnapshotSource()` = các khối đã sửa.
  Mixin không chặn đổi trang/lọc trong cùng route ⇒ tự hỏi `$confirm` trước khi đổi trang/lọc/ĐVT khi còn khối bẩn.
- Lỗi + nhảy tới lỗi: `utils/scrollToFirstError.js`; marker `.v2-error` (memory: jump-to-error chỉ nhận `.v2-error`).

### C.2 API/store
- Gọi API qua `this.$store.dispatch('apiGetMethod' | 'apiPostMethod' | 'apiPutMethod' | 'apiDeleteMethod', …)` (vd `ProductListPage.vue:971-1010`,
  `utils/productLifecycle.js:58-61`). Tiền tố hàng hoá `master-data/products`. Không có service/api module riêng — gọi thẳng trong page.
- Tên công ty đang làm: `currentCompanyName(store)` (`utils/productLifecycle.js:23-27`) — dùng cho câu hỏi xác nhận.

### C.3 Menu hub
- `components/subsystem-menu/master-data.js:59-86` nhóm **"Hàng hoá"** (`subItems`, KHÔNG `children`), mục `{ label, link, isShow: [tên quyền…] }`.
  Phân hệ `master-data` là hub (`components/subsystem-menu/hub.js:32`) ⇒ page phải `layout: 'default-sidebar'` (memory topbar 2 cấp vs hub 3 cấp).
- Lối phụ: `sale-hub.js:253-279` nhóm **Phê Duyệt** (khuôn `{ n, link, isShow }`) — bê nguyên `isShow`.
- `lookup.js:47` có sẵn mục trống "Hàng sắp tăng giá" (màn L3 vẫn ở ERP — N34) ⇒ không đụng.
- Không đổi nhãn mục cũ (nhãn là `menuKey`).

### C.4 Quyền FE ở màn hàng hoá hiện có
- Mixin `utils/mixins/CheckPermission.js:3` `hasAPermission(name)` đọc `$store.state.permissions` (đã lọc theo công ty đang làm).
- Gate fail-closed theo computed: `canBuildCatalog`, `canBuildProduct`, `canCreate`, `canTakeBack` (`ProductListPage.vue:685-703`); nút từng dòng theo
  **cờ BE** (`can_delete`, `can_lock`… — `utils/productLifecycle.js` docblock) chứ không suy từ trạng thái thô.
- Menu: `isShow: ['Xây dựng thông tin hàng hoá', 'Xem dữ liệu hàng hoá công ty']`. Super admin không bypass.
- ⇒ Màn giá: menu + page gate bằng quyền mới "Cập nhật giá hàng hoá"; ô khoá/nút Lưu từng khối theo cờ BE `can_edit_price` + `lock_reason`.
  Màn duyệt: gate "Duyệt giá hàng hoá" (quyền HRM mới, guard `api`).

### C.5 e2e
- Spec hàng hoá ở `e2e/tests/master-data/products-*.{api,ui}.spec.ts`; fixture chung `e2e/utils/productFixture.ts` (tiền tố `E2EC1S`, `createFixtures`,
  `cleanupProductFixtures`, `loginToken`, tài khoản không quyền `e2e_cmd_noperm@test.local`, `COMPANY_ID = 1`). Mẫu ca có quyền / không quyền /
  khác công ty + role tạm + `flushApiPermissionCache()`: `products-lifecycle-ui.spec.ts:1-80, :404-466`.
- Quy ước: `mode: 'serial'`, `--workers=1`, `--no-deps`, viewport 1280, không `networkidle`, chờ request theo **ĐƯỜNG**, lọc nút V2BaseButton
  bằng chuỗi đã chuẩn hoá khoảng trắng, worktree truyền `API_BASE`/`BASE_URL`/`API_REPO`.

---

## D. Đề xuất HRM

### D.1 Màn 1 — "Cập nhật giá hàng hoá" `/master-data/product-prices`

```
[Bộ lọc ▾  Tìm mã / tên / model…                                    ] [Lọc] [↺]
  Tính chất ▾ | Nhóm CN ▾ | Nhóm SP ▾ | Loại SP ▾ | Hãng SX (cty mình) ▾ | Thương hiệu ▾ | Trạng thái duyệt ▾
Cập nhật giá hàng hoá · 1.234 hàng hoá                      (không có nút toolbar)
┌──────────────┬───────┬────────────┬──────┬──────┬───────┬──────────┬─────────┬──────────┬──────┬──────────┬──────────┬─────┬────────────┬──────┐
│ Tên hàng hoá │ ĐVT   │ Mã         │Model │Hãng  │Tồn kho│ Giá vốn  │Loại giá │Giá h.tại │Hệ số │Giá c.thức│ Giá mới  │ĐMGG │Hiệu lực    │      │  ← 1 tầng, nowrap
├──────────────┼───────┼────────────┼──────┼──────┼───────┼──────────┼─────────┼──────────┼──────┼──────────┼──────────┼─────┼────────────┼──────┤
│ Máy nén khí  │[Cái▾] │ TPE.00123  │ AB-1 │ ABAC │   12  │[1,000,000]│ Bán lẻ  │1,250,000 │[1.3] │1,300,000 │[1,300,000]│[5] │Đang áp dụng│ 💾   │
│ ✎ Lý do sửa  │       │ Công khoán:│      │      │       │ ⏳Chờ duyệt│ +Thêm giá hiệu lực                                         │ 🕘   │
│ 📐 Công thức │       │  2         │      │      │       │          │  └ –    │          │[1.4] │1,400,000 │[1,400,000]│[5] │[12/10/2026]✕│     │
│ ⚠ Không duyệt:│      │ Ghi chú HH │      │      │       │          │ Bán buôn│ …        │      │          │          │     │            │      │
│  "…"         │       │ (chỉ đọc)  │      │      │       │          │ … (đủ 6 loại; TMĐT có 3 công tắc "Sửa tay")                     │      │
├──────────────┼───────┼────────────┼──────┼──────┼───────┼──────────┼─────────┼────────────────────────────────────────────────────────┼──────┤
│ Hàng X  [Đang nhập thông tin]  — mọi ô khoá (nền #f1f5f9), không nút Lưu, ⓘ "Nhập giá sau khi có luồng Tính giá"              │      │
└──────────────┴───────┴────────────┴──────┴──────┴───────┴──────────┴─────────┴──────────┴──────┴──────────┴──────────┴─────┴────────────┴──────┘
                                                                                      « ‹ 1 2 3 › »  20 / trang
```

Tự chốt (thuần UI / theo khuôn — ghi đầu file mockup):
- Tiêu đề **1 tầng** (bỏ nhóm "Giá" colspan) để né bẫy `th rowspan=2 + sticky` (§6). Tiêu đề dính trên + 2 cột Tên/ĐVT dính trái; bảng có
  **vùng cuộn riêng** đo tại chỗ + nghe `resize` (không `calc(100vh - N)` ghim cứng; `.content-page overflow:hidden` giết sticky).
  `table-layout: fixed` thì cộng tổng bề rộng rồi ghim `table.style.width`.
- Bỏ dòng đầu khối trống 7 ô của ERP: dòng 1 của khối = loại giá Bán lẻ (rowspan các cột hàng = số dòng giá).
- Cột Hành động cuối: 💾 Lưu (icon-button primary, có lớp tải + chống bấm 2 lần) + 🕘 Lịch sử giá. Lưu từng khối như ERP.
- Ô "Lý do sửa giá" mở inline như ERP (V2BaseInput); công khoán + ghi chú hàng hoá **chỉ đọc** (QC-8). ĐMGG thanh lý không hiện.
- Badge cờ duyệt dùng `V2BaseBadge` (vàng "Chờ duyệt", đỏ "Không duyệt").
- Validate: FE chặn đúng rule BE (bắt buộc, khoảng giá trị, ngày hiệu lực > hôm nay, ≤ 1 giá hiệu lực/loại) — báo đồng thời mọi ô của khối,
  lỗi 422 gắn theo `prices.{i}…` (form-validate 3b/3d); ĐMGG ngoài 0–100 **báo đỏ** (không kẹp như ERP).
- Đổi ĐVT / đổi trang / đổi lọc khi khối đang bẩn ⇒ `$confirm` "Thông tin chưa lưu". Rời route ⇒ `unsavedChangesMixin`.
- Tồn kho nạp sau danh sách (request thứ 2), ô hiện "…" khi đang tải — giữ nhịp như ERP để danh sách không chậm.
- Popup "Công thức lắp ráp": `V2BaseModal` chỉ đọc, giữ như ERP (1–1).

### D.2 Màn 2 — "Hàng hoá chờ duyệt giá" `/master-data/product-price-approvals`

```
[Bộ lọc ▾ Tìm mã / tên / model]  Cây phân loại 4 cấp | Hãng SX | Người cập nhật      [Lọc] [↺]
Hàng hoá chờ duyệt giá · 8 yêu cầu                                    [Xuất Excel]
 (khi tick ≥1) Đã chọn 3 yêu cầu  [✓ Duyệt] [✕ Không duyệt] [Bỏ chọn]
┌──┬──┬───────────────┬────┬────────────┬──────────┬─────────┬─────────┬──────┬───────────┬────────┬─────────┬──────────┬───────────┬──────────────┬────────┐
│☐ │# │ Tên hàng hoá  │ĐVT │ Mã         │ Giá vốn  │Loại giá │ Giá cũ  │Hệ số │ Giá mới   │ĐMGG cũ │ĐMGG mới │Hiệu lực  │Người cập n│ Thời gian    │        │
├──┼──┼───────────────┼────┼────────────┼──────────┼─────────┼─────────┼──────┼───────────┼────────┼─────────┼──────────┼───────────┼──────────────┼────────┤
│☐ │1 │ Máy nén khí   │Cái │ TPE.00123  │1,000,000 │ Bán lẻ  │1,250,000│[1.3] │[1,300,000]│  5%    │ [5]     │Đang áp d.│KD1 - An   │09/10/26 10:20│ ✓  ✕   │
│  │  │ Lý do: tăng giá│    │ (link CT)  │(cũ 950k) │         │         │      │ +50,000   │        │ +0%     │          │           │              │ 🕘     │
│  │  │               │    │            │          │ └ Bán lẻ│  —      │[1.4] │[1,400,000]│        │ [5]     │12/10/2026│           │              │        │
└──┴──┴───────────────┴────┴────────────┴──────────┴─────────┴─────────┴──────┴───────────┴────────┴─────────┴──────────┴───────────┴──────────────┴────────┘
```

- Duyệt (dòng / hàng loạt): `$confirm` gọi tên mã + hệ quả ("Giá mới áp dụng ngay; giá hiệu lực đã qua ngày sẽ dời về ngày mai"), không `danger`.
- Không duyệt: `$confirm({ danger, showInput, inputLabel: 'Lý do không duyệt' })` bắt buộc — đủ là 1 lần hỏi (button-convention 6c).
- Người duyệt sửa được hệ số/giá/ĐMGG trước khi duyệt (1–1 ERP), chênh lệch ± màu xanh/đỏ. Giá cũ hiển thị cho cả giá vốn (ERP không có — tự chốt thêm
  chữ phụ "cũ …" để người duyệt so; nếu không muốn thì bỏ ở mockup).
- Xuất Excel theo bộ lọc (khuôn skill export-excel). Thông báo chuông theo `notification-convention` (gửi duyệt → người có quyền duyệt; không duyệt → người cập nhật).

### D.3 File FE dự kiến (hrm-client) — chỉ để ước lượng, chưa phải phạm vi xin "làm"

| Tạo / sửa | File | Nội dung |
|---|---|---|
| tạo | `pages/master-data/product-prices/index.vue` | page màn 1 (`layout: 'default-sidebar'`, mixins PageTitle + filterState + unsavedChanges + CheckPermission) |
| tạo | `pages/master-data/product-price-approvals/index.vue` | page màn 2 |
| tạo | `components/product/price/ProductPriceTable.vue` | bảng nhập tại chỗ rowspan (khối = `<template v-for>`), sticky, đo vùng cuộn |
| tạo | `components/product/price/ProductPriceApprovalTable.vue` | bảng duyệt rowspan + ô tick |
| tạo | `components/product/price/PriceCell.vue` (hoặc 2 ô: tiền / hệ số) | ô nhập + badge cờ duyệt + `V2BaseError` |
| tạo | `utils/productPriceModel.js` | port T1–T11 thành hàm thuần (dựng khối từ API, tính TMĐT, lan bán lẻ → 2–5, giá công thức, payload lưu, payload duyệt) — 1 nơi cho cả 2 màn |
| tạo | `components/product/price/ProductPriceHistoryModal.vue` | vỏ `V2BaseModal` + `SystemInfoSection` (hoặc dùng thẳng `SettingHistoryModal` nếu BE làm adapter) |
| tạo | `components/product/price/ProductRecipeModal.vue` | popup công thức lắp ráp (chỉ đọc) |
| sửa | `components/subsystem-menu/master-data.js` | +2 `subItems` vào nhóm "Hàng hoá" (`isShow` quyền mới) |
| sửa | `components/subsystem-menu/sale-hub.js` | +1 lối phụ "Hàng hoá chờ duyệt giá" ở Phê Duyệt (nếu F5 chọn) |
| sửa (F3) | `pages/sale/regulation-config/…` (FE chỉ ăn `options` BE) | không đổi FE nếu BE đổi `options` sang Hãng SX |

### D.4 Ca e2e chính (`e2e/tests/master-data/product-prices{.api,-ui}.spec.ts`, `product-price-approvals-ui.spec.ts`)

Fixture: mở rộng `utils/productFixture.ts` — hàng E2EC1S của Cty 1 có hãng SX Cty 1, 2 ĐVT, ĐVT phụ **thiếu dòng loại 5**; 1 hàng hãng SX Cty khác; 1 hàng "Đang nhập thông tin"
(HRM tạo); bật/tắt `companies.is_company_price` cho Cty 1 trong `beforeAll/afterAll` (khôi phục giá trị cũ). Role tạm "chỉ Cập nhật giá" / "chỉ Duyệt giá" + `flushApiPermissionCache()`.

| # | Ca | Chốt bằng |
|---|---|---|
| P1 | Có quyền: vào màn từ menu hub, khối đủ 6 loại giá (cả ĐVT thiếu loại 5) | đếm dòng giá = 6, rowspan ô Tên = 6 + số giá hiệu lực |
| P2 | Sửa hệ số Bán lẻ ⇒ giá mới làm tròn trăm; loại 2–5 bằng bán lẻ; TMĐT = round(×1,3) khi không tick | đọc `value` ô |
| P3 | Tick "Sửa tay" TMĐT mở ô; bỏ tick ĐMGG về 0 | `disabled` + giá trị |
| P4 | Thêm 1 giá hiệu lực (ngày mai) + Lưu ⇒ đúng 1 request lưu, toast, khối nạp lại; SQL: 6 dòng giá, `product_expected_prices` 1 dòng status 2 | request theo ĐƯỜNG + SQL |
| P5 | Lưu với nhiều ô sai cùng lúc (giá vốn trống, hệ số 100, ngày hôm nay) ⇒ hiện đủ lỗi mọi ô, 0 request, cuộn tới ô đầu | đếm `.v2-error` |
| P6 | Hàng "Đang nhập thông tin": mọi ô khoá, không nút Lưu; gọi API trực tiếp ⇒ BE chặn | DOM + API 4xx |
| P7 | Khác công ty (hãng SX Cty khác): theo F1 — không hiện / ô khoá; API ép lưu ⇒ 403 | DOM + API |
| P8 | Không quyền: menu không có mục, mở URL ⇒ không có bảng, toast/403, console sạch | DOM + console |
| P9 | Sửa rồi đổi trang / bấm menu khác ⇒ popup "Thông tin chưa lưu"; Ở lại giữ giá trị | modal + value |
| P10 | Lịch sử giá: sau P4 mở popup ⇒ dòng mới nhất "Thay đổi thông tin", cũ đỏ → mới xanh, bộ lọc 3 nhóm | DOM |
| A1 | Bật duyệt giá Cty 1 ⇒ Lưu ⇒ toast "Yêu cầu duyệt giá…", badge Chờ duyệt, SQL `product_approves` 1 dòng, giá thật KHÔNG đổi, 1 thông báo | SQL + DOM |
| A2 | Màn duyệt: sửa giá mới ⇒ chênh lệch ±; Duyệt ⇒ popup gọi tên mã; Đồng ý ⇒ giá thật = giá đã sửa, phiếu biến mất | SQL |
| A3 | Không duyệt: popup bắt buộc lý do (trống ⇒ báo lỗi, 0 request); có lý do ⇒ cờ 2, màn giá hiện "Không duyệt" + "Ghi chú không duyệt: …"; thông báo người cập nhật | SQL + DOM |
| A4 | Duyệt hàng loạt 2 phiếu có sửa ⇒ giá sửa được áp (chốt lỗi ERP 0.6 không tái diễn) | SQL |
| A5 | Không quyền Duyệt giá: không menu, URL ⇒ chặn; API approve ⇒ 403; phiếu công ty khác ⇒ 403 | API |

### D.5 Điểm đo DOM bắt buộc khi kiểm Playwright (memory e2e-ui-phai-kiem-khuon-giao-dien)
1. `thead tr` = 1; mọi `th` cùng `offsetHeight` (nowrap — tiêu đề 1 dòng).
2. Khối: `rowSpan` của ô Tên = số `tr` của khối; số khối = số hàng API trả.
3. Sticky: cuộn ngang 600px ⇒ `getBoundingClientRect().left` của ô Tên không đổi; cuộn dọc ⇒ `thead` bottom ≤ top dòng dữ liệu đầu tiên đang hiện
   (không đè), `z-index` ô dính > ô thường.
4. Chỉ **1** vùng cuộn dọc (đếm phần tử `scrollHeight > clientHeight` có `overflow-y` auto/scroll); trang không cao hơn khung nhìn.
5. Ô khoá: `getComputedStyle` nền `rgb(241, 245, 249)`, chữ `rgb(71, 85, 105)`, `disabled` thật (Playwright `fill` thất bại).
6. Định dạng số: giá có dấu ngăn nghìn đúng `formatNumber` của HRM; giá công thức TMĐT tròn nghìn.
7. Mỗi lần Lưu đúng 1 request ĐƯỜNG lưu; bấm 2 lần nhanh vẫn 1 request.
8. Badge chờ duyệt / không duyệt: màu nền `rgba(màu, .1)` theo `V2BaseBadge`.
9. Footer phân trang không đè bảng (toạ độ đáy bảng ≤ đỉnh phân trang).
10. Console không lỗi JS ở cả ca có quyền và không quyền.

---

## E. Có cần mockup HTML trước khi code?

**Có — đề xuất 1 file** `2d-erp-khong-loi/mockup-gia.html` (không tính source, làm không cần xin "làm"): màn Cập nhật giá (3–4 khối mẫu: hàng thường 2 ĐVT,
có giá hiệu lực, có cờ chờ duyệt/không duyệt, hàng Đang nhập thông tin khoá) + màn Duyệt giá + 3 popup (Lịch sử giá, Không duyệt có lý do, Công thức lắp ráp),
JS tính T1–T11 chạy thật để user thử nhập. Lý do: (1) bảng rowspan + sticky + vùng cuộn là đúng chỗ §6 ghi 4 bẫy đã trả giá — chốt trên mockup rẻ hơn sửa
trên Nuxt; (2) bố cục tiêu đề 1 tầng, chỗ đặt Lý do sửa giá / công khoán / badge là lệch ERP, cần user nhìn; (3) màn duyệt đổi từ ERP khá nhiều.
Bắt buộc: serve HTTP + đo `getComputedStyle` từ app V2 đang chạy (primary `#1abc9c`, badge `rgba(màu,.1)`, ô khoá `#f1f5f9`), không chép CSS mockup khác;
điểm lệch thuần UI tự chốt + ghi comment đầu file; viewport 1280.

---

## F. Tồn cần hỏi user (hỏi LẦN LƯỢT; điểm thuần UI đã tự chốt ở D)

| # | Câu | ⭐ Đề xuất | Hệ quả từng đáp án |
|---|---|---|---|
| **F1** | Màn Cập nhật giá hiện **những hàng nào**? ERP hiện mọi hàng (status 1/2/5) rồi mới chặn lúc Lưu | ⭐ Chỉ hàng công ty đang làm **được sửa giá** (hãng SX + công ty tạo = công ty đang làm, QC-4); hàng "Đang nhập thông tin" của công ty mình vẫn hiện nhưng khoá + nhãn lý do | ⭐: danh sách gọn, không có nút chết; người Cty 2–8 thấy ít hàng (bảng chung đa số do Cty 1). Hiện tất cả (ERP): xem được giá mọi hàng (giá bán không bảo mật) nhưng phần lớn dòng khoá, phân trang dài; giá vốn hàng công ty khác lộ ra trên màn |
| **F2** | Duyệt / Không duyệt có đổi `products.status` như ERP (Duyệt → 1, Không duyệt → 5) không? | ⭐ **Không đổi** — chỉ ghi cờ chờ duyệt trên giá/ĐVT | ⭐: trạng thái hàng HRM không bị phá. Giữ như ERP: một lần Không duyệt làm hàng cũ **mất khỏi "Hàng đang kinh doanh"** HRM (luật suy ra cần `status = 1`) và Duyệt lật hàng status 2/5 về 1, lách luồng Tính giá |
| **F3** | Ô "Hãng cần duyệt" ở *Khai Quy chế – Cấu hình* HRM đang nạp bảng **Thương hiệu** trong khi cột lưu id **Hãng SX** (cả `brand_ids` lẫn `new_brand_ids`). Sửa trong 2-D2? | ⭐ **Sửa trong 2-D2** (đổi nguồn lựa chọn sang Hãng SX, kiểm dữ liệu đã lưu) vì Duyệt giá đọc trực tiếp cột này | Sửa: điều kiện gửi duyệt đúng. Để ngoài luồng (note N-mới): ai bật duyệt giá theo hãng ở HRM là sai im lặng; chỉ an toàn khi chọn "Tất cả các hãng" |
| **F4** | Hàng **Ngừng kinh doanh (4)** và **Chờ tính giá (2)** tại công ty tạo: cho sửa giá không? (QC-5 mới chốt cho "Đang nhập thông tin") | ⭐ **Khoá cả 2** — 4: luật bản ghi đã khoá (như tab Quản trị trả 423); 2: chờ luồng Tính giá Phase 7 | Khoá: nhất quán G6/QC-5; công ty khác đang bán hàng đó (bảng chung) không được chỉnh giá qua công ty tạo tới khi mở khoá. Cho sửa 4: tiện cho công ty khác nhưng sửa được bản ghi đang khoá |
| **F5** | Đặt menu ở đâu? (sheet quy hoạch chưa có dòng cho 2 màn này; ERP đặt ở Kế toán → Quản lý giá, mà `finance.js:25` ghi sheet đã xếp nhóm đó sang phân hệ khác) | ⭐ **Danh mục dùng chung → Hàng hoá**: "Cập nhật giá hàng hoá" + "Hàng hoá chờ duyệt giá"; thêm lối phụ "Hàng hoá chờ duyệt giá" ở **Bán hàng → Phê Duyệt** | ⭐: cạnh 4 màn hàng hoá, người duyệt tìm được ở nhóm chờ duyệt quen thuộc. Đặt ở Tài chính (như ERP Kế toán): đúng thói quen kế toán nhưng trái chú thích sheet; cần thêm nhóm rail mới |
| **F6** | **Lịch sử giá** (QC-9) — theo dõi gì, xem ở đâu? | ⭐ Theo **hàng hoá** (mọi ĐVT, tên ĐVT trong dòng): giá vốn, 6 loại × (giá, hệ số, ĐMGG, cờ sửa tay TMĐT), giá hiệu lực thêm/sửa/xoá, lý do sửa giá; nhóm "Thay đổi trạng thái" cho Gửi duyệt / Duyệt / Không duyệt (kèm lý do). Ai vào được màn giá thì xem. Chỉ popup ở màn giá + màn duyệt; **chưa** thêm khối vào chi tiết hàng hoá (hàng hoá chưa có lịch sử) | ⭐: đủ vết, 1 nơi. Thêm cả khối ở chi tiết hàng hoá (skill entity-history đòi 2 nơi): đúng skill nhưng chi tiết hàng hoá sẽ có "Lịch sử giá" trong khi thông tin hàng chưa có lịch sử — lệch; làm thì cần quyền xem (chi tiết mở cho mọi người, lộ lịch sử giá vốn) |
| **F7** | **Xuất Excel**: màn Duyệt giá có (ERP); màn Cập nhật giá không có ở ERP nhưng skill coi Xuất Excel là bộ bắt buộc của HRM. Quyền xuất? | ⭐ Duyệt giá: có, gate **quyền màn + 1654** *Xuất excel danh sách hàng hoá* (§35b "mọi nút xuất trong luồng"); Cập nhật giá: **không** làm ở 2-D2 | ⭐: bám §35b, đợt gọn. Thêm xuất ở màn giá: +1 export BE (khối 6 loại giá × ĐVT, file lớn) |
| **F8** | Ô lọc **"Còn tồn / Hết tồn"** (ERP có ô nhưng BE đã tắt — lọc không chạy) | ⭐ **Bỏ** ở 2-D2 | Bỏ: đúng hành vi thật của ERP. Làm cho chạy: phải join tồn kho kế toán trong truy vấn danh sách (chậm, cần định nghĩa tồn theo kho nào/công ty nào) |

Không hỏi (tự chốt, ghi plan): tiêu đề 1 tầng; Lưu từng khối; lý do sửa giá giữ ô nhập; `note_edit_price` không có ô (ERP cũng không); ĐMGG thanh lý không hiện/không ghi;
công khoán + ghi chú hàng hoá chỉ đọc (QC-8); ĐMGG ngoài khoảng báo đỏ thay vì kẹp; bulk Duyệt sửa theo nghĩa đúng; HRM không ghi `unit_coefficient` khi duyệt; kiểm công
ty ở cả duyệt 1 dòng; popup công thức lắp ráp giữ 1–1; người duyệt sửa được giá trước khi duyệt (1–1 ERP).

Việc ngoài luồng mới phát hiện (đề xuất ghi vào `2c-ghi/chot.md`): **N-a** Quy chế HRM "Hãng cần duyệt" nạp nhầm bảng Thương hiệu (nếu F3 không sửa trong 2-D2);
**N-b** ERP bulk Duyệt giá sai khoá `price`/`prices` + `dd($e)` (mất khi chặn ERP ở 2-D2b, chỉ ghi nhận).
