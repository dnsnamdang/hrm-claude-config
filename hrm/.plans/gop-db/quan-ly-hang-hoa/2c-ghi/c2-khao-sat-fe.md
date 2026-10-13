# Đợt 2-C2 — Khảo sát FE + mockup: Lấy về + sửa mức Quản trị

> 08/10/2026 · khảo sát CHỈ ĐỌC (không sửa source, không commit; DB `hrm_erp` chỉ `SELECT COUNT`).
> Code: worktree `websites/wt-chuyen-doi-hang-hoa/hrm-client` nhánh `feat/chuyen-doi-hang-hoa` (client `81f38f36d`, sau merge 2-C1).
> Luật ưu tiên: `chot.md` (G1–G11, C1–C12, D1–D4, T6, H1') > ERP đang chạy > mockup
> `man-danh-muc-hang-hoa/mockup-luong-xay-dung-hang-hoa.html` (gọi tắt **MK**, số dòng theo file đó).
> Đường dẫn FE tương đối từ `hrm-client/`, BE từ `hrm-api/`, e2e từ `wt-chuyen-doi-hang-hoa/e2e/`.

---

## 0. Kết luận nhanh

| # | Câu | Kết luận |
|---|---|---|
| 1 | Mockup lấy về | 2 lối: (a) màn **Kho dữ liệu hàng hoá** — nút *Lấy về* từng dòng + tick nhiều → thanh *Đã chọn N hàng hoá* · **Lấy về công ty** · Bỏ chọn; (b) popup **Xem hàng hoá Công ty khác** ở màn *Hàng hoá nhập thông tin* (tick nhiều → **Chọn**). **Không có popup xác nhận**, toast `Đã lấy … về <công ty> — trạng thái Đang nhập thông tin`. Lối (a) ở lại màn, lối (b) nhảy sang *Hàng hoá nhập thông tin* |
| 2 | Mockup form công ty lấy về | mở thẳng tab cha **Quản trị hàng hoá**; dải xám *"Hàng hoá do **X** tạo — chỉ khai được tab **Quản trị hàng hoá**."*; tab cha *Thông tin hàng hoá* mờ (opacity .4), 5 step khoá (không bấm được), mọi ô/nút trong 5 tab con bị disable/ẩn |
| 3 | Hiện trạng FE | Kho dữ liệu (`warehouse`) **chưa có** cột tick, cột Hành động, thanh chọn — chỉ đọc. Hạ tầng tick + thanh chọn **đã có ở màn công ty** (2-C3) nhưng gắn cứng vào `canBuildCatalog` ⇒ phải tổng quát hoá. Form 2-C1 **không có chế độ khoá nào** (`ProductForm.vue` không prop scope; `can_edit` BE chỉ đúng cho công ty tạo) |
| 4 | Lệch mockup ↔ chốt | 13 điểm — mục 3 |
| 5 | Câu hỏi user | 4 câu nghiệp vụ — mục 6 |

---

## 1. Mockup — luồng lấy về

### 1.1 Lối (a) — màn *Kho dữ liệu hàng hoá* (`sc-tong`)

| Phần | Mockup | Nguồn |
|---|---|---|
| Bộ lọc | ô tìm *"Tìm theo mã, tên hàng hoá, model, barcode"* + công tắc **Chỉ hàng công ty chưa dùng** + Tìm kiếm / Làm mới; nâng cao có *Công ty quản lý* + *Tình trạng sử dụng* | MK 1146–1172, `dsTong()` 6790–6803 |
| Toolbar lưới | tiêu đề *Kho dữ liệu hàng hoá* + phụ đề *"Toàn bộ hàng hoá của mọi công ty"*; nút **Xuất Excel** + Cấu hình cột. **Không** nút Lấy về ở toolbar | MK 1174–1184 |
| Cột tick | cột đầu, **mọi dòng** đều có ô tick (cả dòng công ty đã dùng), ô tick đầu bảng chọn cả trang | `veBangDS(man, ds, coTick)` 2786–2821; `veBangTong()` gọi `coTick=true` 6806 |
| Thanh chọn | `.kho-bar` hiện khi ≥1 tick: **"Đã chọn N hàng hoá"** · nút primary **Lấy về công ty** (icon mũi tên xuống khay) · tertiary **Bỏ chọn** | MK 1181–1185, CSS 687–689, `demChonMan()` 6866–6875 |
| Cột Hành động (dòng) | công ty mình **chưa dùng** (`!x.st[CUR]`) ⇒ nút primary có chữ **Lấy về**; đã dùng ⇒ nút tertiary **Xem** (mở form) | `oHanhDong()` 2704–2712 |
| Cột Trạng thái | *Chưa sử dụng* khi công ty chưa dùng; thêm cột *Công ty quản lý* | §33l (design.md), `khoiTaoCot()` 2696–2701 |
| Lấy 1 dòng | **không hỏi xác nhận**; đặt trạng thái *Đang nhập thông tin*; vẽ lại mọi màn; toast ok `Đã lấy <mã> về <công ty> — trạng thái Đang nhập thông tin`; đã dùng ⇒ toast cảnh báo `Hàng hoá này công ty đang dùng rồi`. **Ở lại màn**, dòng đổi sang nút *Xem* | `layHangVe()` 6817–6824 |
| Lấy hàng loạt | **không hỏi**; bỏ qua im lặng các dòng đã dùng, đếm n dòng lấy được; n = 0 ⇒ toast cảnh báo `Các hàng hoá đã chọn đều đang được công ty dùng rồi`; xong toast `Đã lấy <n> hàng hoá về <công ty> — trạng thái Đang nhập thông tin`. **Không trần** số lượng | `layNhieuHangVe()` 6825–6834 |
| Đo §33l | lấy 1 mã: Kho công ty 150 → 151; tick 3 (1 đã lấy) → bar *Đã chọn 2*… | design.md §33l |

### 1.2 Lối (b) — popup *Xem hàng hoá Công ty khác* (màn *Hàng hoá nhập thông tin*)

| Phần | Mockup | Nguồn |
|---|---|---|
| Nút mở | toolbar lưới màn Nhập thông tin, secondary, icon con mắt, đứng trước *Lập yêu cầu tính giá* và *Tạo mới* | MK 1047–1051 |
| Popup | rộng `min(1480px,100%)`; tiêu đề *Xem hàng hoá Công ty khác*; mô tả `Hàng hoá do công ty khác tạo mà <công ty> chưa sử dụng`; nút Cấu hình cột · Phóng to · Đóng ở header | MK 1775–1793, `moPopup()` 3405–3418 |
| Bộ lọc | tiêu đề *Bộ lọc hàng hoá* + Tìm kiếm nâng cao; ô tìm *"Nhập tên, mã hoặc model hàng hoá..."*; nâng cao: *Công ty quản lý hàng hoá* (bỏ công ty mình) + *Loại sản phẩm* | MK 1794–1808, 3409–3416 |
| Lưới | cột tick + bộ cột chung (bỏ STT/Trạng thái/Hành động, thêm *Công ty quản lý*); rỗng: *"Không còn hàng hoá nào của công ty khác để lấy về"* | `veBangPopup()` 3420–3445 |
| Footer | `Chưa chọn hàng hoá nào` / `Đã chọn N hàng hoá` · **Chọn** (primary, ✓) · **Đóng** | MK 1817–1823, `demChon()` 3444–3446 |
| Chọn | 0 tick ⇒ toast `Chưa chọn hàng hoá nào`; có ⇒ đặt *Đang nhập thông tin*, đóng popup, toast `Đã lấy N hàng hoá về <công ty> — trạng thái Đang nhập thông tin`, **chuyển sang màn Hàng hoá nhập thông tin** | `chonHangHoa()` 3447–3457 |
| Chốt | §33m: **GIỮ CẢ HAI** lối (popup + Kho dữ liệu) | design.md §33m |

### 1.3 Form khi công ty lấy về mở sửa (mức `chiQuanTri`, §26c-bis)

| Phần | Mockup | Nguồn |
|---|---|---|
| Xác định mức | `mucQuyenSua()`: hàng của công ty khác ⇒ `chiQuanTri` (mockup KHÔNG xét trạng thái) | MK 3262–3275 |
| Tab mở đầu | thẳng tab cha **Quản trị hàng hoá** (`chaDau = 'qt'`) | MK 3336–3339 |
| Khoá ô | mọi `input/select/textarea` của pane **khác** tab Quản trị ⇒ `disabled`; nút `.v2-btn`, `.ra-btn` trong pane ⇒ **ẩn** (`display:none`); ô chọn nhiều ⇒ class `khoa` | MK 3281–3296, `dongBoKhoaMs()` 3250–3260 |
| Tab Quản trị | **mở hết**, kể cả *Hệ số công nghệ* (mockup chưa biết T6) | MK 3285 (`laTabQuanTri` không khoá gì) |
| Dải báo | `#bao-muon` trên thẻ tab: icon ⓘ + `Hàng hoá do <b>X</b> tạo — chỉ khai được tab <b>Quản trị hàng hoá</b>.`; CSS `.bao-pham-vi` nền `#f5f8fc`, viền `#e3ebf5`, bo 6px, đệm 8px 12px, chữ 12px `#374151` — **xám, không đỏ** (đỏ dành cho lỗi) | MK 1482–1487, 3299–3305, CSS 322–324 |
| Tab cha *Thông tin hàng hoá* | thêm class `khoa` ⇒ `opacity:.4; cursor:default` — **vẫn bấm được** (`doiTabCha` không chặn) | MK 3309–3314, CSS 375–376, 2585–2599 |
| 5 step con | `stepKhoa = true` ⇒ step thêm class `khoa`, `doiTab()` **return sớm** ⇒ chỉ xem được step đang mở (step 1), không sang step 2–5 | MK 2546–2558, 2604–2606 |
| Footer / Lưu | như form thường; Lưu mockup `luuVaChuyen()` chuyển *Chờ tính giá* + toast `…lập Yêu cầu tính giá để đi tiếp` rồi về màn Kho công ty | MK 3348–3356 |

---

## 2. Hiện trạng FE (worktree, `81f38f36d`)

### 2.1 4 màn danh sách = 1 component

| File | Dòng | Ghi chú |
|---|---|---|
| `components/product/ProductListPage.vue` | 1008 | logic chung 4 màn; page chỉ `extends` + `productScreen` |
| `utils/product-list-screens.js` | 190 | cấu hình màn: `warehouse` **không** `rowActions` (`:43–69`); `company`, `entering` có `rowActions: true` (`:72`, `:100`) |
| `pages/master-data/products/{warehouse,company,entering,trading}.vue` | ~14 | `layout: 'default-sidebar'`; warehouse docblock còn ghi "Đợt 2-B CHỈ ĐỌC — không có nút ghi" |

### 2.2 Thành phần đang có trong `ProductListPage.vue`

| Thành phần | Có? | Chỗ | Đánh giá cho 2-C2 |
|---|---|---|---|
| Nút toolbar `#actions` | Tạo mới (`canCreate`, chỉ `entering`, `:114–124`), Xây dựng catalog (`canBuildCatalog`, `:126–135`), Cấu hình cột (`:136–138`) | | thêm nút *Xem hàng hoá Công ty khác* ở `entering` **nếu** làm lối (b) (Q2) |
| Cột tick | ✅ nhưng `v-if="canBuildCatalog"` (`:158–172`); cột `checkbox` chỉ push khi `canBuildCatalog` (`allColumns` `:578–590`) | | phải tổng quát thành `canSelectRows = canBuildCatalog \|\| canTakeBack` và ô tick dòng thêm điều kiện `item.can_take_back` ở Kho dữ liệu |
| Thanh chọn `#left-actions` | ✅ *Đã chọn N hàng hoá* · **Xếp catalog** · **Bỏ chọn** (`:142–156`), CSS `.product-bulk-bar` | | thêm nhánh Kho dữ liệu: *Đã chọn N hàng hoá* · **Lấy về công ty** · **Bỏ chọn** |
| Giữ tick qua trang | ✅ `listSelected` map id→row (`:446–447`), `toggleListRow/toggleListPage` (`:734–746`) — đã chặn `change` phát lại của `V2BaseCheckbox` | | dùng lại; **chưa có trần** — thêm trần 100 theo khuôn `ProductCatalogBuilderModal.vue:371–374, 860–893` (`TICK_CAP`, toast cảnh báo, `tickRev++` dựng lại ô) |
| Cột Hành động | ✅ `V2BaseRowActions` chỉ action `edit` (`:279–284`), cột `actions` push khi `screen.rowActions` (`:628–638`) | | Kho dữ liệu: bật `rowActions` + action `take_back` (`visible: !!item.can_take_back`). Đề xuất chỉ thêm cột khi có quyền 1652 (giữ ca e2e E2 "Kho dữ liệu không cột Hành động" cho người không quyền) |
| Ô Trạng thái | ✅ badge, không có ⇒ *Chưa sử dụng* (`:286–289`) | | sau khi lấy về `loadData()` là đổi badge, không cần sửa |
| Hỏi xác nhận | ❌ màn chưa dùng | | dùng `this.$confirm({ title, message, textAccept })` (`plugins/confirm-dialog.js`, skill `button-convention` §6c) — KHÔNG `b-modal`/`msgBoxConfirm` |
| Quyền FE | `hasAPermission(...)` (`utils/mixins/CheckPermission.js:3`) | | `canTakeBack = screen.slug === 'warehouse' && hasAPermission('Xây dựng thông tin hàng hoá')` (fail-closed) |

Đối chiếu skill `list-page`: cột Hành động dùng `V2BaseRowActions` icon (không nút chữ), **bỏ "Xem"** (mã là link) — `list-page/SKILL.md` "Cột Hành động" §1–2. Mục bắt buộc "Lịch sử" + "Xuất Excel" chưa có ở cả 4 màn (đã gác từ 2-B, Excel thuộc 2-E) — không thuộc 2-C2.

### 2.3 Dữ liệu dòng BE đang trả (`ProductListResource.php`)

- `company_status` / `status_text` / `status_color` (`:28, :55–57`); `owner_company_id/name` (`:69–70`).
- `can_edit` = **công ty tạo** + `products.status = 1` + không Ngừng KD + quyền 1652 (`:59–63`) ⇒ công ty lấy về **không** có Sửa.
- **Chưa có** cờ cho lấy về; **không trả `products.status`** ⇒ FE không tự suy được G9b-2.
- ⇒ FE cần BE trả thêm: `can_take_back` (chưa dùng tại công ty hiện tại + `products.status = 1` + quyền 1652) và `can_edit` mở rộng cho công ty đã lấy về (có dòng công ty, trạng thái ≠ 4).

DB local (`hrm_erp`, 08/10): `products.status` = 0: **17.512** · 1: 28.371 · 2: 1 · 5: 6 ⇒ **17.519 hàng không lấy về được** theo G9b-2. `product_company_coefficients`: 1.105 dòng, **toàn bộ `status` NULL** (2-A không backfill) ⇒ dòng hệ số cũ của công ty khác hiện là "Chưa sử dụng", lấy về = UPDATE dòng đó (plan 2-C2).

### 2.4 Form sửa 2-C1

| File | Dòng | Hiện trạng | Cần cho 2-C2 |
|---|---|---|---|
| `components/product/form/ProductForm.vue` | 255 | 2 tab cha (`:5`), 5 step (`:7`), 5 tab con form (`:17–21`), tab Quản trị (`:23`), footer Lưu (`:26`); **không** prop/biến khoá; mở mặc định tab `info` (`:67`); payload `toPayload(form)` gửi **toàn bộ** form (`:217`) | nhận `edit_scope` (`full` \| `admin`) từ `/edit`; `admin` ⇒ mở tab `admin` trước, dải báo xám, tab cha *Thông tin* khoá/chỉ đọc, gửi payload chỉ phần quản trị |
| `components/product/form/ProductFormAdmin.vue` | 181 | Hệ số công nghệ là ô nhập thường (`:58–65`), hint *"Dùng chung mọi công ty, chỉ công ty tạo sửa."* | `admin` ⇒ ô Hệ số công nghệ `disabled` (T6) |
| `components/product/form/productFormModel.js` | 70 | `toPayload` (`:40–55`), `tabOfField` (`:24–37`) | thêm `toAdminPayload(form)` = `{ admin: {...} }` (không `tech_coefficient`) |
| `components/product/detail/ProductParentTabs.vue` | 181 | props `tabs`, `value`, `errorKeys` — **không** có trạng thái khoá | thêm prop `lockedKeys` (mờ như MK `.mc.khoa`) — nếu chọn cho xem chỉ đọc thì không cần chặn bấm |
| `components/product/detail/ProductStepTabs.vue` | 127 | không khoá | không đổi nếu tab Thông tin chỉ đọc dựng bằng component chi tiết |
| `components/product/detail/ProductTab*.vue` | | 5 tab chi tiết chỉ đọc (2-B) nhận `product` từ `GET products/{id}` | **tái dùng** để hiện tab *Thông tin hàng hoá* chỉ đọc ở mức `admin` (xem T5) |
| `pages/master-data/products/_id/edit.vue` | 63 | gate FE quyền 1652 (`:26–28`); 403/404 ⇒ 404 (`:44–49`); Lưu xong sang chi tiết (`:58–60`) | không đổi luồng; tiêu đề giữ `Sửa hàng hoá: <mã>` |
| `pages/master-data/products/_id/index.vue` | 206 | footer Sửa theo `can_edit` (`:41–45`) | không đổi — chỉ cần BE mở `can_edit` cho công ty lấy về |
| BE `ProductWriteController@edit` | | `assertOwner($model)` (`:35`) ⇒ công ty lấy về mở `/edit` bị chặn | phần BE (khảo sát BE riêng) |
| Route | `Modules/MasterData/Routes/api.php:253–298` | chưa có endpoint lấy về | FE cần `POST master-data/products/take-back` `{ product_ids: [...] }` (≤100) — đặt TRƯỚC `/{product}` |

Không có component dải báo/alert dùng chung (`components/` chỉ có `V2BaseFieldHint`) ⇒ dựng `div` + CSS theo `.bao-pham-vi` của MK (khuôn như `.product-uncatalogued-notice` trong `ProductListPage.vue`).

---

## 3. Lệch mockup ↔ chốt / quy ước

| # | Mockup | Chốt / quy ước | Xử lý |
|---|---|---|---|
| L1 | Lấy hàng loạt **không trần** (`layNhieuHangVe` 6825) | **G9b-1: ≤ 100 mã/lượt** | trần ở FE lúc tick (khuôn 2-C3) + BE 422 |
| L2 | Lấy được **mọi** hàng công ty chưa dùng | **G9b-2: chỉ `products.status = 1`** (17.519 hàng local bị loại) | ẩn nút + ô tick theo `can_take_back`; BE chặn |
| L3 | Lưu form: `luuVaChuyen` đổi sang *Chờ tính giá* + toast `…lập Yêu cầu tính giá để đi tiếp`, về màn Kho công ty (MK 3348–3356) | **H1' + G9b-4**: Lưu không đổi trạng thái; toast bỏ vế tính giá | đã có ở 2-C1: `Đã lưu hàng hoá <mã>` (`ProductForm.vue:223`), sang chi tiết — áp nguyên cho công ty lấy về |
| L4 | Mức `chiQuanTri` mở cả **Hệ số công nghệ** (pane Quản trị không khoá ô nào, MK 3285) | **T6**: cột chung, chỉ công ty tạo sửa | ô `disabled` + giữ hint; BE bỏ qua/422 |
| L5 | `mucQuyenSua` không xét trạng thái | **G9a**: Ngừng KD (4) ẩn Sửa; **D2**: `products.status = 0` không sửa | theo `can_edit` BE |
| L6 | Ô tick hiện ở **mọi dòng**, hàng đã dùng bị bỏ qua im lặng khi lấy hàng loạt | quy ước "nút không dùng được thì ẨN" | chỉ dòng `can_take_back` có ô tick (tự chốt T2) |
| L7 | Nút chữ **Lấy về** / **Xem** trong ô Hành động | skill `list-page`: `V2BaseRowActions` icon, **bỏ Xem** | action `take_back` icon (tự chốt T1); mã là link chi tiết |
| L8 | **Không** hỏi xác nhận | skill `button-convention` §6c: lệnh GHI không hoàn tác ⇒ hỏi | `$confirm` (tự chốt T3) |
| L9 | Step con bị khoá — **không xem được** step 2–5 ở mức `chiQuanTri` (MK 2604–2606) | §35b-3: ai cũng xem được chi tiết | cho xem chỉ đọc mọi step (tự chốt T5) |
| L10 | Popup lối (b) chọn xong nhảy sang màn Nhập thông tin; mockup không có trần | §33m giữ cả 2 lối; G9b áp cho cả 2 lối | Q2 |
| L11 | Toolbar Kho dữ liệu có **Xuất Excel** | Excel thuộc 2-E | không làm ở 2-C2 |
| L12 | Kho dữ liệu hiện mọi hàng kể cả ERP đã xoá | tồn nhỏ `chot.md:57` | Q1 |
| L13 | Popup lối (b) lọc *Loại sản phẩm* | 4 màn thật lọc theo 4 cấp phân loại dây chuyền (`#field-classification`) | nếu làm popup: dùng bộ lọc màn thật (tự chốt T7) |

---

## 4. Điểm thuần UI — tự chốt theo khuôn

| # | Điểm | Tự chốt | Căn cứ |
|---|---|---|---|
| T1 | Nút lấy về từng dòng | **tự chốt**: `V2BaseRowActions` action `{ key: 'take_back', title: 'Lấy về', icon: 'ri-download-2-line', visible: !!item.can_take_back }`; cột Hành động ở Kho dữ liệu chỉ thêm khi có quyền 1652 | skill list-page §1–2; giữ ca E2 2-C1 |
| T2 | Ô tick | **tự chốt**: chỉ dòng `can_take_back` có ô tick; tick đầu bảng chỉ tick các dòng đó của trang; trần 100 — vượt thì toast cảnh báo `Mỗi lượt chỉ lấy về tối đa 100 mã hàng — hãy lấy lượt này rồi chọn tiếp`, ô vừa bấm trả về chưa tick; không có "Chọn tất cả N kết quả lọc" | khuôn 2-C3 `ProductCatalogBuilderModal.vue:371–374, 860–893` |
| T3 | Hỏi xác nhận | **tự chốt**: hỏi cả 1 dòng lẫn hàng loạt, hỏi TRƯỚC lớp tải. 1 dòng: tiêu đề *Xác nhận lấy về*, câu `Lấy hàng hoá <mã> về <công ty đang làm việc>? Hàng sẽ ở trạng thái Đang nhập thông tin.`, `textAccept: 'Lấy về'`. Hàng loạt: `Lấy <N> hàng hoá đã chọn về <công ty>? …`. Không `danger` | skill button-convention §6c (thao tác ghi, chưa có hoàn tác tới 2-C4) |
| T4 | Thanh chọn + sau khi lấy | **tự chốt**: thanh `Đã chọn N hàng hoá` · **Lấy về công ty** (primary, `btn-compact`, `ri-download-2-line`) · **Bỏ chọn** (tertiary) — y khuôn thanh 2-C3. Xong: toast success nguyên văn MK `Đã lấy <mã> về <công ty> — trạng thái Đang nhập thông tin` / `Đã lấy <n> hàng hoá về <công ty> — trạng thái Đang nhập thông tin`; xoá tick; `loadData()`; **ở lại màn** (như MK lối a). BE báo một phần không lấy được (đã có công ty khác trong phiên khác lấy trước…) ⇒ toast cảnh báo nêu số bỏ qua | MK 6817–6834 |
| T5 | Tab *Thông tin hàng hoá* ở mức `admin` | **tự chốt**: mở thẳng tab *Quản trị*; tab cha *Thông tin* mờ (prop `lockedKeys`, opacity như MK) nhưng **bấm được**, hiện **chỉ đọc** bằng 5 component chi tiết `ProductTab*` (gọi thêm `GET products/{id}`), đi được cả 5 step; không có ô nhập nào bật. Không thêm prop `disabled` vào 12 component form (rủi ro hỏng form 2-C1 đã xanh 32 ca) | §35b-3 (xem chi tiết không cần quyền); L9 |
| T6 | Dải báo phạm vi | **tự chốt**: `div` trên thẻ tab, chữ nguyên văn MK `Hàng hoá do <b>{owner_company_name}</b> tạo — chỉ khai được tab <b>Quản trị hàng hoá</b>.`, icon `ri-information-line`, CSS `.bao-pham-vi` (nền `#f5f8fc`, viền `#e3ebf5`, chữ 12px `#374151`) | MK 322–324, 3299–3305 |
| T7 | Popup lối (b) (nếu Q2 = làm) | **tự chốt**: khuôn `modal-popup`/`V2BaseModal`, lưới dùng lại endpoint `warehouse?usage=unused` + 4 ô phân loại + Công ty quản lý; footer `Đã chọn N hàng hoá` · **Lấy về** · Đóng; cùng trần 100 + hỏi xác nhận như T3; xong đóng popup + `loadData()` màn Nhập thông tin (đã đứng sẵn ở màn đó) | §26d, MK 3447–3457 |
| T8 | Payload Lưu ở mức `admin` | **tự chốt**: gửi chỉ `{ admin: {...} }` (không `tech_coefficient`); endpoint cụ thể (PUT chung với request tách nhánh hay route riêng) — theo khảo sát BE | §26c-bis "BE phải chặn" |

---

## 5. File FE sẽ đụng + ca e2e

### 5.1 File

| File | Mới/Sửa | Nội dung |
|---|---|---|
| `utils/product-list-screens.js` | sửa | `warehouse`: `rowActions: true` (+ cờ `takeBack: true`); sửa docblock "chỉ đọc" |
| `components/product/ProductListPage.vue` | sửa | `canTakeBack`; tổng quát cột tick + `#header-checkbox`/`#cell-checkbox` + thanh `#left-actions` theo màn; trần 100; action `take_back` + `$confirm` + `POST take-back` + lớp tải; `allColumns` điều kiện cột `checkbox`/`actions` theo quyền |
| `pages/master-data/products/warehouse.vue` | sửa | docblock (không còn "không có nút ghi") |
| `components/product/form/ProductForm.vue` | sửa | `editScope` từ `/edit`; mở tab admin; dải báo; tab Thông tin chỉ đọc bằng `ProductTab*`; payload admin-only |
| `components/product/form/ProductFormAdmin.vue` | sửa | prop `adminOnly` ⇒ Hệ số công nghệ `disabled` |
| `components/product/form/productFormModel.js` | sửa | `toAdminPayload()` |
| `components/product/detail/ProductParentTabs.vue` | sửa nhỏ | prop `lockedKeys` (mờ) |
| *(nếu Q2 = làm)* `components/product/ProductTakeBackModal.vue` + `ProductListPage.vue` nút *Xem hàng hoá Công ty khác* ở `entering` | mới/sửa | popup lối (b) |
| e2e `tests/master-data/products-take-back.api.spec.ts` | mới | ca A1–A6 |
| e2e `tests/master-data/products-take-back-ui.spec.ts` | mới | ca U1–U9 |
| e2e `tests/master-data/products-read-ui.spec.ts` | sửa | `WRITE_BUTTONS` (`:30`) đang cấm chữ **Lấy về** ở mọi màn ⇒ cho phép ở `warehouse`; bộ cột mặc định `warehouse` (`:19`) thêm *Hành động* khi tài khoản có 1652 |
| e2e `tests/master-data/products-form-ui.spec.ts` | rà | ca E2 "Kho dữ liệu: không cột Hành động" (`:233–245`) vẫn đúng nếu cột chỉ thêm khi có quyền |

### 5.2 Ca e2e

| # | Ca | Đo |
|---|---|---|
| A1 (API) | `POST take-back` 1 mã chưa dùng ⇒ 200, có dòng công ty `status = 1`, `coefficient` mặc định | DB |
| A2 (API) | mã có dòng hệ số cũ `status NULL` ⇒ **UPDATE** (số dòng không tăng, giữ `coefficient`) | đếm dòng |
| A3 (API) | 101 mã ⇒ 422; mã `products.status ≠ 1` ⇒ 422/bỏ qua; mã công ty đã dùng ⇒ không tạo dòng thứ 2 (gọi 2 lần liên tiếp) | |
| A4 (API) | **không quyền 1652** (role tạm chỉ 1653 + `cache:clear`) ⇒ 403, DB không đổi | |
| A5 (API) | công ty lấy về `PUT` kèm `name`/`tech_coefficient`/`units` ⇒ lớp chung KHÔNG đổi (DB so trước/sau), dữ liệu quản trị lưu đúng công ty, trạng thái giữ 1 | |
| A6 (API) | công ty B `GET /edit` hàng của A **chưa lấy về** ⇒ 403; đã lấy về ⇒ 200 `edit_scope = admin` | |
| U1 | có 1652: Kho dữ liệu — dòng `can_take_back` có ô tick + menu *Lấy về*; dòng đã dùng / `status ≠ 1` không có (đếm DOM khớp API) | |
| U2 | Lấy về 1 dòng: popup xác nhận đúng câu (mã + công ty); Hủy ⇒ 0 POST; Đồng ý ⇒ đúng 1 POST, toast đúng chữ, badge dòng → *Đang nhập thông tin*, hàng có ở màn Nhập thông tin | bắt request |
| U3 | Hàng loạt: tick 3 ⇒ thanh *Đã chọn 3 hàng hoá*; Lấy về công ty ⇒ 1 POST `product_ids` 3 phần tử ⇒ thanh ẩn, tick xoá | |
| U4 | Trần: tick đủ 100 (trang 100) sang trang 2 tick thêm ⇒ toast cảnh báo, đếm vẫn 100, ô vừa bấm không tick | |
| U5 | **Không quyền 1652** (role tạm 1653): Kho dữ liệu 0 ô tick, 0 cột Hành động, 0 chữ *Lấy về*; (nếu Q2) màn Nhập thông tin không vào được như hiện nay | đếm DOM |
| U6 | Form công ty lấy về (từ menu Sửa màn Nhập thông tin + footer chi tiết): mở ở tab *Quản trị*, dải xám đúng chữ + tên công ty tạo, tab *Thông tin* mờ (đo `opacity`), sang tab Thông tin: **0** ô nhập bật, đi được 5 step | `getComputedStyle`, đếm `input:not([disabled])` |
| U7 | Form mức admin: Hệ số công nghệ `disabled`; Lưu ⇒ đúng 1 PUT, body **chỉ** có `admin`; toast `Đã lưu hàng hoá <mã>`; trạng thái giữ *Đang nhập thông tin* | body request |
| U8 | Lưu thiếu catalog (nếu Q3 giữ C1) ⇒ chấm đỏ tab Quản trị, không PUT thứ 2 | |
| U9 | Hồi quy công ty tạo: form vẫn mở tab Thông tin, không dải báo, Hệ số công nghệ sửa được | |

---

## 6. Câu hỏi cho user (nghiệp vụ chưa chốt)

| # | Câu | Phương án · hệ quả |
|---|---|---|
| Q1 | Màn *Kho dữ liệu* đang hiện **17.519 hàng `products.status ≠ 1`** (17.512 ERP đã xoá/khoá + 7 hàng status 2/5) với nhãn *Chưa sử dụng* — G9b không cho lấy về các hàng này. Lọc bỏ không? | ⭐ **Lọc bỏ khỏi Kho dữ liệu** (giống popup Xây dựng catalog B5 loại `status = 0`) — người dùng không thấy dòng "Chưa sử dụng" mà không có nút Lấy về; số tổng màn giảm 45.890 → ~28.371. · Giữ nguyên ⇒ có 17.519 dòng "Chưa sử dụng" không lấy được, dễ bị báo là lỗi; cần thêm nhãn riêng (vd *ERP đã ngừng*) |
| Q2 | Popup **Xem hàng hoá Công ty khác** ở màn *Hàng hoá nhập thông tin* (§33m chốt giữ cả 2 lối) — làm trong 2-C2 không? | ⭐ **Làm sau / bỏ** — chỉ làm lối Kho dữ liệu ở 2-C2: ít code, 1 nơi thao tác, e2e gọn; nếu cần lối tắt thì nút ở màn Nhập thông tin chỉ **điều hướng** sang Kho dữ liệu với công tắc *Chỉ hàng công ty chưa dùng* bật sẵn. · Làm popup ⇒ thêm 1 component + 1 bộ ca e2e, 2 nơi phải giữ cùng trần/luật (G9b) |
| Q3 | Luật C1 *"Lưu bắt buộc ≥ 1 Tiểu mục catalog"* có áp cho **công ty lấy về** khi Lưu tab Quản trị không? | ⭐ **Có áp** — đồng nhất với công ty tạo; hàng mới lấy về chưa có catalog nên lần Lưu đầu buộc chọn. · Không áp ⇒ công ty lấy về lưu được NCC/bảo hành mà chưa xếp catalog; hàng không bao giờ lên màn *Hàng đang kinh doanh* (§33e cần catalog) cho tới khi xếp ở popup 2-C3 |
| Q4 | Sau khi lấy về, công ty lấy về **thấy gì khi công ty tạo sửa lớp chung** (tồn 26g-6 nửa còn lại)? Với thiết kế hiện tại (tham chiếu chung 1 mã `products`) thì **thấy ngay**, không có thông báo | ⭐ **Chấp nhận thấy ngay, không thông báo** ở 2-C2 (đúng mô hình tham chiếu đã chốt — chỉ cần xác nhận). · Muốn có thông báo/ghi lịch sử ⇒ phụ thuộc lịch sử hàng hoá (§14b đang hoãn) — để phase sau |
