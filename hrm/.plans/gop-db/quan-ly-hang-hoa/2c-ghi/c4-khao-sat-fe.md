# Đợt 2-C4 — Khảo sát FE + mockup: Vòng đời (Xóa + Khóa/Mở khóa theo công ty)

> 08/10/2026 · khảo sát CHỈ ĐỌC (không sửa source, không commit, không đụng DB).
> Code: worktree `websites/wt-chuyen-doi-hang-hoa/hrm-client` nhánh `feat/chuyen-doi-hang-hoa` (client `5c2cfb823`, sau merge 2-C2).
> Luật ưu tiên: `chot.md` (G6, G7, G9a, B3, L1–L7) > `design.md` §35b-4 > ERP đang chạy > mockup
> `man-danh-muc-hang-hoa/mockup-luong-xay-dung-hang-hoa.html` (gọi tắt **MK**, số dòng theo file đó).
> Đường dẫn FE tương đối từ `hrm-client/`, BE từ `hrm-api/`, e2e từ `wt-chuyen-doi-hang-hoa/e2e/`.

---

## 0. Kết luận nhanh

| # | Câu | Kết luận |
|---|---|---|
| 1 | Mockup 2-C4 | **Rất mỏng**: chỉ có 2 mục trong menu ⋮ của dòng, **không có `onclick`** — *Xoá* (đỏ) ở màn *Hàng hoá nhập thông tin*; *Khóa* ở *Dữ liệu hàng hoá công ty* + *Hàng đang kinh doanh*. **Không có** Mở khóa, popup xác nhận cho hàng hoá, toast, nút ở footer, thao tác hàng loạt, cũng **không có trạng thái 4 / badge Ngừng kinh doanh** (bộ `ST` chỉ 4 trạng thái 1·2·tính giá·3) |
| 2 | Hiện trạng FE | **Đã có**: badge trạng thái 4 tự hiện (chữ + màu `#DC2626` do BE trả) ở cột Trạng thái của Kho dữ liệu + Dữ liệu công ty, đầu màn chi tiết, lưới popup catalog tab *Hàng trong tiểu mục*; ẩn Sửa khi status 4 (BE `editableAt` + FE theo `can_edit`, e2e E12b). **Chưa có**: action Xóa/Khóa/Mở khóa ở dòng + footer chi tiết, endpoint, cờ `can_delete`/`can_lock`/`can_unlock`, lựa chọn "Ngừng kinh doanh" ở ô lọc Trạng thái màn công ty |
| 3 | Lệch mockup ↔ chốt | 11 điểm — mục 3 |
| 4 | Câu hỏi user | 4 câu nghiệp vụ — mục 6 |

---

## 1. Mockup — Xoá + Khoá

### 1.1 Chỗ xuất hiện

| Phần | Mockup | Nguồn |
|---|---|---|
| Menu ⋮ dòng — màn *Hàng hoá nhập thông tin* (`sc-l1`, kiểu `nhap`) | **Sửa** · **Sao chép** · **Xoá** (`is-danger` → chữ đỏ `#dc2626`, icon thùng rác). Xoá **không gắn hàm** (`item('Xoá', …, '', true)`) | MK 2504–2506, `item()` 2491–2494, CSS `.ra-item.is-danger` 212 |
| Menu ⋮ dòng — các màn còn lại (kiểu `kd`) | **Xem** · **Khóa** (icon ổ khoá) · **In tem barcode** · **Lịch sử**. Khóa **không gắn hàm** | MK 2507–2511 |
| Màn dùng menu `kd` | `oHanhDong()`: *Dữ liệu hàng hoá công ty* (`sc-kho`, kèm nút *Tính giá* ở trạng thái Chờ tính giá/Đang tính giá) và *Hàng đang kinh doanh* (`sc-l3`). Menu Khóa hiện ở **mọi trạng thái** (cả hàng *Đang nhập thông tin* ở `sc-kho`) | MK 2703–2722 |
| Màn *Kho dữ liệu* (`sc-tong`) | **không** menu ⋮ — chỉ nút chữ *Lấy về* / *Xem* ⇒ không có Xoá/Khóa | MK 2705–2713 |
| Footer form (`sc-form`) | *Lưu nháp · Lưu · Quay lại* — **không** Xoá/Khóa. Mockup **không có màn chi tiết riêng** (mã hàng mở thẳng form) | MK 1738–1742 |
| Popup xác nhận | **Không có** cho hàng hoá. Popup *Xác nhận xoá* duy nhất (`#mask-xoa`, §34a đếm trong 13 popup) là của màn Chính sách giá: icon tròn đỏ nền `#fdecec`, tiêu đề *"Bỏ hãng khỏi lưới"*, câu *"Bỏ hãng khỏi lưới là xoá toàn bộ tỷ lệ đã khai cho các công ty mua của hãng này. Bạn chắc chắn?"*, nút đỏ *Bỏ khỏi lưới* + *Đóng* | MK 2243–2259 |
| Toast | Không có toast nào cho xoá/khoá hàng hoá (danh sách mọi `toast(` của MK) | MK 2461 + grep |
| Hàng loạt | Không — thanh chọn chỉ có *Lấy về công ty* (Kho dữ liệu) / *Xếp catalog* (công ty) | MK 1181–1185 |

### 1.2 Badge "Ngừng kinh doanh"

| Phần | Mockup | Nguồn |
|---|---|---|
| Bộ trạng thái | `ST = { nhap #64748B, cho #D97706, dang #2563EB, kd #16A34A }` — **không có 4** | MK 2276–2281 |
| Ô lọc Trạng thái màn công ty | *Đang nhập thông tin · Chờ tính giá bán · Đang tính giá · Đang kinh doanh* — không có *Ngừng kinh doanh* | MK 3516 |
| Bảng sơ đồ luồng (`sc-flow`) | chỉ bảng "Ai được sửa gì" (3 dòng), không nhắc khoá theo công ty | MK 992–998 |

⇒ Toàn bộ 2-C4 phải **dựng theo khuôn hệ thống** (skill `list-page`, `button-convention`, `modal-popup`) + `chot.md`, mockup chỉ cho **vị trí** (Xoá ở Nhập thông tin; Khóa ở Dữ liệu công ty + Đang kinh doanh).

---

## 2. Hiện trạng FE (worktree, `5c2cfb823`)

### 2.1 Danh sách — `components/product/ProductListPage.vue` (1186 dòng) + `utils/product-list-screens.js` (197 dòng)

| Thành phần | Hiện trạng | Chỗ | Cần cho 2-C4 |
|---|---|---|---|
| Cấu hình màn | `warehouse` `rowActions + takeBack`; `company`, `entering` `rowActions: true`; `trading` **không** `rowActions` ⇒ không cột Hành động | `product-list-screens.js:45–158` | `trading` cần cột Hành động (Khóa) — gate quyền 1652 như Kho (mục 4 T2) |
| Cột Hành động | `hasActionsColumn` = `takeBack ? canTakeBack : rowActions` | `ProductListPage.vue:701–703`, cột push `:667–677` | thêm nhánh "chỉ khi có 1652" cho `trading` |
| Action dòng | Kho: `take_back`; màn khác: **chỉ `edit`** theo `item.can_edit` | `:789–797` | thêm `delete` (danger) · `lock` · `unlock` theo cờ BE |
| Xử lý action | `onRowAction(key, item)` — `edit` → `/edit?from`, `take_back` → `takeBack()` | `:799–805` | thêm 3 nhánh |
| Hỏi xác nhận | đã dùng `this.$confirm({ title, message, textAccept })` (2-C2, plugin `plugins/confirm-dialog.js` render `base-confirm-modal`, id ngẫu nhiên `app-confirm-…`) | `:864–905` | dùng lại; Xóa thêm `danger: true` |
| Khuôn gọi API | `$safeLoadingStart/Finish`, 403 không toast (interceptor), lỗi khác toast `errors[0]`/`message` | `:880–903` | chép khuôn |
| Badge Trạng thái | `V2BaseBadge :color="item.status_color"` + chữ `status_text` BE trả; không có ⇒ *Chưa sử dụng* | `:313–316` | ✅ status 4 đã ra đỏ `#DC2626` — không sửa |
| Ô lọc Trạng thái (màn công ty) | `PRODUCT_COMPANY_STATUS_OPTIONS` = 3 lựa chọn 1·2·3 | `:583`, `product-list-screens.js:188–192` | thêm *Ngừng kinh doanh* (4). ⚠️ hằng này **dùng chung** với popup catalog (`ProductCatalogBuilderModal.vue:367, 521–522` tự `push` 4 ở tab *in*, `:724` bỏ 4 khi về tab *add*) ⇒ không sửa thẳng hằng, tách hằng mới cho màn công ty |
| Ô tick màn công ty | `listSelected` giữ dòng đã tick (catalog 1655) | `:155–202` | xoá dòng xong phải `$delete(listSelected, id)` |

Quyền FE: `hasAPermission('Xây dựng thông tin hàng hoá')` (fail-closed, `:687–696`). G6/G7 không thêm quyền ⇒ cùng 1652.

### 2.2 Dữ liệu BE trả (để FE gate)

| Cờ | Có? | Chỗ |
|---|---|---|
| `company_status` / `status_text` / `status_color` (4 ⇒ *Ngừng kinh doanh* `#DC2626`) | ✅ | `ProductListResource.php:56–58`, `ProductDetailResource.php:39–41`, hằng `ProductCompany.php:26–41` |
| `can_edit` (đã loại status 4 + `products.status ≠ 1`) | ✅ | `ProductListResource.php:61`, `Product::editableAt` `Product.php:423–428` |
| `can_delete`, `can_lock`, `can_unlock`, kiểu xoá (xoá cứng / gỡ khỏi công ty) | ❌ | — BE phải thêm cả List + Detail resource |
| Endpoint xoá / khoá / mở khoá hàng hoá | ❌ | route `Modules/MasterData/Routes/api.php:253–292` chỉ có store/take/edit/admin-data/update/show |

BE chặn sửa status 4 đang trả **403** (`ProductWriteService.php:110–115, 128–136`) chứ không phải 423 như G6 ghi — FE `edit.vue:44–49` đưa 403 về trang 404 (ổn, vì lối vào Sửa đã ẩn).

### 2.3 Màn hiển thị trạng thái 4 (theo `ProductService::applyScreen` `:174–205`)

| Màn | Hàng status 4 hiện? | Badge |
|---|---|---|
| Kho dữ liệu | có (cột Trạng thái của công ty mình) | ✅ đỏ |
| Dữ liệu hàng hoá công ty | có (`status IS NOT NULL`) | ✅ đỏ — **chỗ duy nhất có Mở khóa ở danh sách** |
| Hàng hoá nhập thông tin | không (lọc = 1) | — |
| Hàng đang kinh doanh | không (lọc = 3) ⇒ khoá xong **dòng biến mất** khỏi màn | — |
| Cột *Công ty đang kinh doanh* | không tính công ty status 4 (`tradingCompanyNames` lọc = 3, `Product.php:456–460`) | ✅ đúng G6 |
| Chi tiết `_id/index.vue` | badge đầu trang `:11` | ✅ đỏ |
| Popup catalog tab *Hàng trong tiểu mục* | có + lọc được *Ngừng kinh doanh* (B3) | ✅ (`ProductCatalogBuilderModal.vue:271, 395, 521–522`) |

### 2.4 Chi tiết — `pages/master-data/products/_id/index.vue` (206 dòng)

- Footer `V2Footer :menu="{ edit: !!product.can_edit }"` (`:41–45`) ⇒ chưa có Xóa/Khóa.
- `V2Footer` có sẵn `menu.delete` (nút `primary status="danger"` *Xóa*, emit `delete`, `components/V2Footer.vue:125–128`) và slot `#custom-actions` (`:160`, sau Lịch sử) cho Khóa/Mở khóa.
- Docblock `:2–5` còn ghi "Không nút … Sửa" — cập nhật.

### 2.5 Ẩn Sửa khi status 4 (G9a) — ĐÃ CÓ

BE `editableAt` + `assertOwner/assertCanEditAdmin`; FE menu dòng `visible: !!item.can_edit` (`ProductListPage.vue:796`) + footer `can_edit`; e2e `products-form-ui.spec.ts:521–530` (E12b) đặt status 4 bằng SQL ⇒ footer 0 nút Sửa. **Chưa có** ca đo menu dòng ẩn Sửa (E12b chỉ đo footer, tên ca ghi "menu dòng lẫn footer").

### 2.6 Khuôn tham khảo trong repo

| Màn | Dùng được gì | Lưu ý |
|---|---|---|
| `pages/master-data/manufacturers/index.vue:718–740` | bộ action `edit` · `delete` (`danger`, `ri-delete-bin-line`, `visible` theo `is_can_delete`) · `lock/unlock` (`ri-lock-line` / `ri-lock-unlock-line`, **không** `danger`) · `history` | ⚠️ màn này so `Number(status) === 2` (`:522, :838`) — **lỗi bảng ERP khoá bằng 0** (memory); hàng hoá KHÔNG chép kiểu suy khoá/mở từ `status` thô — dùng cờ BE `can_lock`/`can_unlock` |
| cùng file `:161–177, 804–860` | `BaseConfirmModal` id `confirm-delete-manufacturer` / `confirm-toggle-lock-manufacturer`, toast *"Xóa thành công."*, 404 ⇒ *"Dữ liệu đã thay đổi, vui lòng tải lại"* | hàng hoá đã chọn `$confirm` từ 2-C2 ⇒ giữ 1 kiểu trong cùng component (id ngẫu nhiên; e2e bắt `.modal.show` theo tiêu đề như `products-take-ui.spec.ts:106`). Quy ước id `confirm-<việc>-<catalogSlug>` chỉ áp màn danh mục chép khuôn BaseCatalog |
| skill `button-convention:66–68, 85–89, 217, 331–332, 374–377` | Khóa `warning` (cam) · Mở khóa `success` (xanh lá) · Xóa `danger`; trong cột bảng Khóa/Mở khóa **không** `danger`; chữ **Xóa / Khóa / Mở khóa** (dấu kiểu mới); thứ tự Sửa → Xóa → Khóa → ⋮; `textAccept` = đúng chữ nút | |
| skill `list-page:1116–1180` | footer chi tiết = đủ hành động như dòng, **cùng điều kiện**; nút không dùng được thì ẨN; Xóa từ chi tiết ⇒ về danh sách; Khóa/Mở khóa ở dòng ⇒ ở lại cập nhật tại chỗ | |

---

## 3. Lệch mockup ↔ chốt / quy ước

| # | Mockup | Chốt / quy ước | Xử lý |
|---|---|---|---|
| L1 | Không có trạng thái 4 / badge *Ngừng kinh doanh* | **G6**: status 4, badge `#DC2626` | đã có ở BE + FE (mục 2.3) |
| L2 | Không có *Mở khóa* | G6: mở khoá về 3 | thêm action `unlock` theo cờ BE |
| L3 | *Khóa* hiện ở mọi trạng thái (cả *Đang nhập thông tin* ở `sc-kho`) | **G6 mặc định**: chỉ khoá từ 3 → 4 | `visible` theo `can_lock` BE (Q1) |
| L4 | *Khóa* không có ở màn Nhập thông tin; *Xoá* chỉ ở màn Nhập thông tin | §35b-4: xoá khi *Đang nhập thông tin*; G7 gỡ dòng công ty lấy về | Xóa ở **mọi màn có cột Hành động** khi `can_delete` (thực tế: Nhập thông tin + Dữ liệu công ty) — T1 |
| L5 | Không popup xác nhận | skill `modal-popup:247`, `button-convention §6c`: Xóa/Khóa/Mở khóa phải hỏi | `$confirm` — T3 |
| L6 | Chữ "Xoá" (dấu cũ), "Khóa" | skill `button-convention:138, 156–157`: **Xóa · Khóa · Mở khóa** | theo skill |
| L7 | Không có lối ở footer (mockup không có màn chi tiết) | skill `list-page:1116`: footer = đủ hành động như dòng | thêm footer — T4 |
| L8 | Menu ⋮ có *Sao chép*, *In tem barcode*, *Lịch sử*, *Xem* | G8 sao chép làm sau; lịch sử §14b hoãn; in tem chưa có phase; skill bỏ *Xem* | không làm ở 2-C4 |
| L9 | Menu ⋮ kiểu cũ (mọi mục trong menu) | `V2BaseRowActions` tối đa 3 icon inline, thứ tự Sửa → Xóa → Khóa | theo skill |
| L10 | *Hàng đang kinh doanh* có Khóa nhưng màn thật chưa có cột Hành động | read-ui hiện chốt `trading` không cột Hành động | thêm cột khi có 1652 (T2), sửa spec |
| L11 | Một kiểu "Xoá" | **G7**: 2 nghĩa — công ty tạo ⇒ xoá cứng; công ty lấy về ⇒ gỡ dòng của mình | 1 nút *Xóa*, câu hỏi + toast khác nhau theo kiểu BE trả (T3) |

---

## 4. Điểm thuần UI — tự chốt theo khuôn

| # | Điểm | Tự chốt | Căn cứ |
|---|---|---|---|
| T1 | Action dòng | **tự chốt**: `rowActionsOf` màn ≠ Kho trả `[edit (can_edit), delete (danger, ri-delete-bin-line, can_delete), lock (ri-lock-line, can_lock) \| unlock (ri-lock-unlock-line, can_unlock)]`, Khóa/Mở khóa **không** `danger`; mọi cờ ⇒ `visible`, AND thêm quyền FE 1652 (fail-closed). Kho dữ liệu **giữ** chỉ *Lấy về* (mockup `sc-tong` không menu) | skill list-page, button-convention:89, 217 |
| T2 | Cột Hành động ở *Hàng đang kinh doanh* | **tự chốt**: thêm cờ màn (vd `lifecycle: true`) — chỉ dựng cột khi có 1652 (như Kho dữ liệu 2-C2), action duy nhất Khóa | mockup `sc-l3` có Khóa; giữ màn không quyền như 2-B |
| T3 | Popup xác nhận (`$confirm`, hỏi TRƯỚC lớp tải) | **tự chốt**: · Xóa (công ty tạo): tiêu đề *Xác nhận xóa*, `Xóa hàng hoá <mã>? Hàng hoá và toàn bộ dữ liệu đi kèm bị xóa hẳn, không khôi phục được.`, `textAccept 'Xóa'`, `danger: true` · Xóa (công ty lấy về): `Gỡ hàng hoá <mã> khỏi <công ty>? Dữ liệu quản trị và catalog của <công ty> bị xóa; hàng hoá vẫn còn ở <công ty tạo>.`, `textAccept 'Xóa'`, `danger: true` · Khóa: *Xác nhận khóa*, `Khóa hàng hoá <mã> tại <công ty>? Hàng chuyển sang Ngừng kinh doanh, không sửa được tới khi mở khóa.`, `textAccept 'Khóa'` · Mở khóa: *Xác nhận mở khóa*, `Mở khóa hàng hoá <mã> tại <công ty>? Hàng trở lại Đang kinh doanh.`, `textAccept 'Mở khóa'` | button-convention §6c:331–332, 374–377; khuôn `takeBack` `:871–878` |
| T4 | Footer chi tiết | **tự chốt**: `menu.delete = !!product.can_delete` (nút có sẵn của V2Footer) + slot `#custom-actions`: Khóa `primary status="warning"` `ri-lock-line` (`can_lock`), Mở khóa `primary status="success"` `ri-lock-unlock-line` (`can_unlock`); cùng câu hỏi T3. Điều kiện đọc **cùng cờ BE** với dòng | list-page:1116–1158; button-convention:66–68 |
| T5 | Sau khi làm | **tự chốt**: · ở danh sách: toast success, bỏ id khỏi `listSelected`, `loadData()` (ở *Đang kinh doanh* khoá xong dòng biến mất — toast nói rõ trạng thái mới) · Xóa ở chi tiết: toast + `$router.push(backUrl)` (§7.3) · Khóa/Mở khóa ở chi tiết: toast + tải lại `GET products/{id}` tại chỗ (badge đổi, Sửa ẩn/hiện) | list-page §7.2, §7.3 |
| T6 | Toast | **tự chốt**: `Đã xóa hàng hoá <mã>` · `Đã gỡ hàng hoá <mã> khỏi <công ty>` · `Đã khóa hàng hoá <mã> — trạng thái Ngừng kinh doanh` · `Đã mở khóa hàng hoá <mã> — trạng thái Đang kinh doanh`; lỗi 422 ⇒ toast nguyên văn lý do BE (vd *"Hàng có tồn kho!"*), 404 ⇒ *Dữ liệu đã thay đổi, vui lòng tải lại* + `loadData()`; 403 không toast | khuôn manufacturers `:815–824`, 2-C2 `:893–899` |
| T7 | Hàng loạt | **tự chốt**: KHÔNG có — chỉ từng dòng + footer (mockup không có; thanh chọn màn công ty đang dành cho Xếp catalog 1655) | MK 1181–1185 |
| T8 | Ô lọc Trạng thái màn công ty | **tự chốt**: thêm *Ngừng kinh doanh* (4) bằng hằng riêng (`PRODUCT_COMPANY_SCREEN_STATUS_OPTIONS = [...1·2·3, 4]`), không đụng hằng popup catalog | B3 giữ đúng 2 tab popup |
| T9 | Nhãn | **tự chốt**: chữ nút *Xóa / Khóa / Mở khóa*; badge giữ *Ngừng kinh doanh* (BE) | button-convention:138 |

---

## 5. File FE sẽ đụng + ca e2e

### 5.1 File

| File | Mới/Sửa | Nội dung |
|---|---|---|
| `utils/product-list-screens.js` | sửa | `trading`: cờ cột Hành động gate 1652 (T2); hằng lọc Trạng thái có 4 cho màn công ty (T8); docblock |
| `components/product/ProductListPage.vue` | sửa | `rowActionsOf` + `onRowAction` 3 action; `hasActionsColumn` cho `trading`; hàm `deleteProduct / lockProduct / unlockProduct` (`$confirm` → lớp tải → API → toast → bỏ tick → `loadData`); ô lọc dùng hằng mới |
| `pages/master-data/products/_id/index.vue` | sửa | footer `menu.delete` + `#custom-actions` Khóa/Mở khóa; Xóa xong về `backUrl`; Khóa/Mở khóa tải lại chi tiết; docblock |
| *(tuỳ chọn)* `utils/productLifecycle.js` | mới | gom câu hỏi + gọi API + toast dùng chung cho danh sách và chi tiết (tránh 2 nơi lệch chữ) |
| `pages/master-data/products/{company,trading,entering}.vue` | rà | docblock |
| BE (khảo sát BE riêng) | — | FE cần: `DELETE products/{id}`, `products/{id}/lock`, `/unlock` (đặt trước `/{product}`); cờ `can_delete`, `can_lock`, `can_unlock`, `delete_mode` (`destroy`/`detach`) ở **cả** List + Detail resource |

### 5.2 Ca e2e cần thêm (spec mới `tests/master-data/products-lifecycle.api.spec.ts` + `products-lifecycle-ui.spec.ts`)

| # | Ca | Đo |
|---|---|---|
| A1 (API) | công ty tạo xoá hàng *Đang nhập thông tin* chưa ai lấy về ⇒ 200; `products` + mọi bảng con (đơn vị, 6 dòng giá, dòng công ty, catalog, thuộc tính, phụ kiện, `productables` đúng `productable_type`) = 0 dòng; `productables` loại khác của hàng khác không đổi | đếm DB |
| A2 (API) | công ty lấy về "xoá" ⇒ dòng công ty mình: dòng mới sinh bị xoá / dòng hệ số cũ trả `status NULL` giữ `coefficient`; catalog công ty mình = 0; `products` + dòng công ty khác không đổi | so trước/sau |
| A3 (API) | chặn: có tồn kho / đang mượn / là phụ kiện / thành phần bộ / công ty khác đã lấy về / trạng thái ≠ 1 / `products.status = 0` ⇒ 422 đúng lý do, DB không đổi | |
| A4 (API) | khoá 3 → 4 ⇒ 200; khoá status ≠ 3 ⇒ 422; mở khoá 4 → 3; mở khoá ≠ 4 ⇒ 422; hàng công ty chưa dùng ⇒ 403/422; hàng cũ chưa có dòng ⇒ sinh dòng `coefficient 1` status 4 (G6) | DB |
| A5 (API) | sau khoá: `PUT admin-data`, `PUT /{id}`, `GET /edit` ⇒ 403; Dữ liệu công ty `can_edit=false, can_unlock=true`; *Đang kinh doanh* không còn dòng; `trading_company_names` bỏ công ty mình | |
| A6 (API) **không quyền 1652** | role tạm chỉ 1653 + `cache:clear`: xoá / khoá / mở khoá ⇒ 403, DB không đổi; list trả `can_delete/can_lock/can_unlock = false` | |
| U1 | màn Nhập thông tin: hàng `can_delete` có icon Xóa (đỏ — đo `color` `getComputedStyle`), số icon Xóa = số dòng API `can_delete`; Hủy popup ⇒ 0 request DELETE | đếm DOM + request |
| U2 | Xóa ⇒ popup đúng câu (mã + "xóa hẳn"), nút *Xóa* đỏ; Đồng ý ⇒ đúng 1 DELETE, toast đúng chữ, dòng biến mất, tổng giảm 1 | |
| U3 | công ty lấy về: popup câu "Gỡ … khỏi <công ty>", toast "Đã gỡ …" | |
| U4 | *Đang kinh doanh*: icon Khóa; Đồng ý ⇒ 1 request lock, dòng biến mất; sang *Dữ liệu công ty* lọc *Ngừng kinh doanh* ⇒ có dòng, badge đỏ `rgb(220, 38, 38)`, **0** icon Sửa, có icon Mở khóa | đo màu, đếm icon |
| U5 | chi tiết hàng status 4: footer đúng `['Mở khóa', 'Quay lại']` (không Sửa/Xóa/Khóa), Mở khóa màu xanh lá; bấm ⇒ tại chỗ badge *Đang kinh doanh*, footer có Sửa + Khóa | `footerTexts` |
| U6 | chi tiết hàng `can_delete`: footer có *Xóa* (danger); Xóa ⇒ về đúng `from` | URL |
| U7 | khớp dòng = chi tiết: cùng 1 hàng ở 3 trạng thái (1, 3, 4) — tập action ở menu dòng = tập nút footer | so 2 mảng |
| U8 **không quyền 1652** | role tạm 1653: *Dữ liệu công ty* + chi tiết: 0 icon Xóa/Khóa/Mở khóa, footer chỉ *Quay lại*; *Đang kinh doanh* 0 cột Hành động; console không lỗi | đếm DOM |

### 5.3 Spec cũ cần sửa

| Spec | Chỗ | Vì sao |
|---|---|---|
| `products-form-ui.spec.ts` E4 | `:427` `footerTexts === ['Sửa','Quay lại']` | hàng vừa tạo (status 1, chưa ai lấy về) sẽ có `can_delete` ⇒ footer thành `['Sửa','Xóa','Quay lại']` — **sẽ đỏ** |
| `products-form-ui.spec.ts` E12b | `:521–530` | thêm đo menu dòng (màn công ty) ẩn Sửa + có Mở khóa; bỏ `test.skip` (BE đã tắt `can_edit`) |
| `products-read-ui.spec.ts` | `SCREENS.trading` `:27–28` | thêm `'Hành động'` khi tài khoản có 1652 (T2); docblock `:5–16` |
| `products-read-ui.spec.ts` | `:113–136`, `:138–155` | tên ca/ghi chú footer: thêm khả năng Xóa/Khóa (assert hiện chỉ đếm Sửa + Quay lại — không đỏ, nhưng nên chốt thêm footer = cờ BE) |
| `products-take-ui.spec.ts` | rà | Kho không đổi action ⇒ không sửa; nếu ca U* đếm footer chi tiết thì rà lại |
| `products-catalog-popup-ui.spec.ts` | rà | chỉ sửa nếu đụng hằng `PRODUCT_COMPANY_STATUS_OPTIONS` (T8 tránh đụng) |

---

## 6. Câu hỏi cho user (nghiệp vụ chưa chốt)

| # | Câu | Phương án · hệ quả |
|---|---|---|
| Q1 | G6 ghi "mặc định đề xuất, user có thể sửa": **khoá được từ trạng thái nào?** | ⭐ **Chỉ từ *Đang kinh doanh* (3 → 4), mở khoá về 3** — nút Khóa chỉ ở *Dữ liệu công ty* + *Đang kinh doanh*; hàng đang nhập dở muốn bỏ thì dùng Xóa. · Cho khoá cả 1/2 ⇒ phải nhớ trạng thái trước khi khoá để mở về đúng chỗ (thêm cột), và mockup đang hiện Khóa ở mọi trạng thái |
| Q2 | **Công ty lấy về "xoá" (gỡ dòng của mình) được ở trạng thái nào?** §35b-4 chỉ nói xoá khi *Đang nhập thông tin*; G7 không nói trạng thái | ⭐ **Chỉ khi dòng của mình *Đang nhập thông tin* (1)** — đồng nhất với công ty tạo; đã kinh doanh thì dùng Khóa. · Cho gỡ ở mọi trạng thái ⇒ công ty gỡ được hàng đang kinh doanh, mất dữ liệu quản trị + catalog, nhưng chứng từ ERP cũ của công ty vẫn trỏ mã đó |
| Q3 | Nút Xóa **hiện theo cờ đầy đủ** (BE tính đủ 5 điều kiện ERP + "chưa công ty nào lấy về" cho từng dòng) hay **cờ nhẹ** (trạng thái + chủ hàng + quyền, kiểm tồn kho/mượn/phụ kiện/bộ lúc bấm, báo lý do bằng toast)? | ⭐ **Cờ đầy đủ** — đúng luật "nút không dùng được thì ẨN", danh sách và chi tiết khớp; tốn thêm ~4 truy vấn gom theo trang (≤100 dòng). · Cờ nhẹ ⇒ nhanh hơn nhưng có nút Xóa bấm ra lỗi "Hàng có tồn kho!" — trái quy ước ẩn nút |
| Q4 | Công ty **tạo** muốn xoá hàng mà **công ty khác đã lấy về** (§35b-4 cấm) — báo thế nào? | ⭐ **Ẩn nút Xóa** (theo Q3) và để Khóa là lối thay thế khi hàng đã kinh doanh; không hiện lý do riêng. · Muốn hiện lý do ⇒ cần chỗ hiển thị khác (ghi chú ở chi tiết), thêm 1 dòng chữ ở màn chi tiết |
