# Report đợt 2 (hrm-client) — lỗi mở 15/10: N85 · N86 (FE) · N87 · N99

Repo: `wt-chuyen-doi-hang-hoa/hrm-client`. Nhánh con `feat/cdhh-loi-mo-fe` (từ `feat/chuyen-doi-hang-hoa` @ `0469c32a3`)
⇒ merge `--no-ff` LOCAL về `feat/chuyen-doi-hang-hoa`: **`f211bd195`**. Không push, không stash. Soát marker xung đột
(`git grep '^<<<<<<<|^>>>>>>>'`): 0. EOL: cả 7 file LF, `git diff --numstat` chỉ có dòng sửa chủ ý (không dòng xoá thừa).
Nuxt 3031 KHÔNG restart (hot reload); sau merge chạy lại cả spec mới trên nhánh chung: 5/5 xanh ⇒ trang vẫn chạy.

## Commit

| Mã | Commit | Nội dung |
|---|---|---|
| N87 | `ef01a8f20` | 7 chỗ `.text-muted` trong `components/product/form` → class scoped `.pf-muted` (`#6b7280`) |
| N86 | `ce0752430` | `ProductItemPickerModal` gửi `exclude_locked=1`; ghi chú vì sao lượt nạp ĐVT ở `ProductFormItemsTable` KHÔNG gửi |
| N85 | `c3f24e9ad` | `ProductFormGallery` computed `galleryError` gom `galleries` + `galleries.0..N-1` |
| merge | `f211bd195` | Merge feat/cdhh-loi-mo-fe |

## Quyết định cần biết

- **N87 — class xám:** repo KHÔNG có class xám toàn cục dùng được. Đo trong app: `.text-muted` = `rgb(220, 53, 69)`
  (đỏ), `.text-secondary` = `rgb(255, 255, 255)` (theme đặt `$secondary: $white`), `.text-hint` / `.text-gray` /
  `.v2-empty-row` chỉ là class scoped của từng màn (ngoài màn đó ra `rgb(17,17,17)`). Màu xám chuẩn của khối hàng hoá là
  `#6b7280` (đếm 42 lần trong `components/V2Base*` + `components/product`, ví dụ `.v2-hint` ở ProductPriceTable,
  `.product-readonly-table__empty`) ⇒ dùng đúng màu đó qua class scoped `.pf-muted` ở từng file, không đặt màu mới.
- **N86 — lệch so với hợp đồng đợt 1:** hợp đồng ghi 2 chỗ `ProductItemPickerModal.vue:103` và `ProductFormItemsTable.vue:125`.
  Nhưng `:125` là `hydrateUnits()` — nạp danh sách ĐVT cho dòng **đã gắn** (không phải nguồn chọn mới). Truyền
  `exclude_locked` ở đó thì hàng gắn trước rồi mới khoá bị BE bỏ khỏi kết quả ⇒ ô ĐVT tụt còn mỗi ĐVT đang lưu, trái
  với luật "dòng đã gắn trước giữ" của chính hợp đồng. Vì vậy CHỈ truyền ở `ProductItemPickerModal` — đây là nguồn chọn
  mới duy nhất của cả 4 bảng hàng kèm theo (Công thức lắp ráp / Phụ kiện mua thêm / Vật tư lắp đặt / Vật tư SC-BD) **và**
  tab Nhóm máy (BE `checkKitStatus` cũng chặn `machine_ids` khoá ⇒ đồng bộ). Ca e2e L3 chốt hành vi này. Nếu user muốn
  đúng nguyên văn hợp đồng (lọc cả lượt nạp ĐVT) thì thêm 1 dòng `q.set('exclude_locked', 1)` ở `hydrateUnits` và sửa L3.
- Ô lọc "Dùng cho máy" (`picker/ProductPickerAdvancedFilters.vue`) không đụng — đã đo request.

## Bảng số đo trước / sau (Playwright headless, viewport 1280, đo từ DOM)

| Mã | Đo | Trước sửa | Sau sửa |
|---|---|---|---|
| N87 | `getComputedStyle.color` "(tối đa 10 ảnh…)" | rgb(220, 53, 69) | rgb(107, 114, 128) |
| N87 | "Ảnh đại diện hiện tại — …" | rgb(220, 53, 69) | rgb(107, 114, 128) |
| N87 | "Chưa có video nào." | rgb(220, 53, 69) | rgb(107, 114, 128) |
| N87 | "Chưa có tài liệu kỹ thuật nào." | rgb(220, 53, 69) | rgb(107, 114, 128) |
| N87 | "Đơn vị đã lưu bị khoá" | rgb(220, 53, 69) | rgb(107, 114, 128) |
| N87 | "Đang tải danh mục xe..." (giữ `vehicle-options` bằng `page.route`) | rgb(220, 53, 69) | rgb(107, 114, 128) |
| N87 | "Đã chọn: 0" (footer popup Chọn hàng hoá) | rgb(220, 53, 69) | rgb(107, 114, 128) |
| N87 | số `.product-form .text-muted` | 5 | 0 |
| N86 | query `item-search` từ popup (Công thức lắp ráp / Vật tư lắp đặt) | `?keyword=…&exclude_id=…` | `?keyword=…&exclude_id=…&exclude_locked=1` |
| N86 | mã hàng khoá B trong API / bảng popup | có / có | không / không |
| N86 | hàng thường C (đối chứng) trong bảng | có | có |
| N86 | lượt nạp ĐVT dòng đã gắn B — query / số ĐVT | `?keyword=B` / 2 | `?keyword=B` / 2 (giữ nguyên, cố ý) |
| N86 | ô "Dùng cho máy" — query / B có ra | `?keyword=B&limit=50` / có | `?keyword=B&limit=50` / có |
| N85 | 422 giả lập `{'galleries.0': [...]}` — số `.product-gallery .v2-error` có chữ | 0 | 1 ("Ảnh 1: đường dẫn ảnh không hợp lệ.", chữ rgb(220, 53, 69)) |
| N85 | chấm đỏ bước "Thông tin chung" + tự mở bước đó | có (lỗi không thấy đâu) | có + lỗi hiện ở khối Hình ảnh |

## E2E

- Spec MỚI `e2e/tests/master-data/products-form-loimo-ui.spec.ts` (L1–L5: N87 màu 7 chỗ · N86 tham số + ẩn hàng khoá ·
  N86 dòng đã gắn giữ đủ ĐVT · N85 lỗi galleries.N · N86 ô lọc Máy không truyền). Fixture tiền tố `E2ELM` riêng
  (không đụng `E2EC1S` của spec khác). Thêm export `cleanupProductsByIds(ids)` vào `e2e/utils/productFixture.ts`
  (`cleanupProducts()` gọi lại nó — hành vi cũ không đổi).
- Trước sửa (tái hiện): L1 fail (7/7 đỏ), L2 fail (không tham số, B hiện), L4 fail (0 lỗi), L3 pass (mốc).
- Sau sửa, nhánh con: **5 passed** (0 failed, 0 did not run). Sau merge, nhánh chung: **5 passed** (0 failed, 0 did not run).
- Spec cũ liên quan `products-form-ui.spec.ts` (đổi popup chọn hàng + khối ảnh): **17 passed, 1 skipped** (E11 skip sẵn
  theo đầu file), 0 failed, 0 did not run.
- Lệnh: `API_BASE=http://127.0.0.1:8031 BASE_URL=http://127.0.0.1:3031 npx playwright test <spec> --project=chromium --no-deps --workers=1` (node 20).

## Fixture đã dọn (`hrm_erp_giacty`)

Mỗi lượt chạy tạo: 2 `product_natures` / `product_function_groups` / `product_families` / `product_types`, 1 `chapters` /
`job_groups` / `job_clusters`, 3 hàng qua `POST products` (A loại phụ tùng ô tô + ảnh đại diện + phụ kiện B; B 2 ĐVT,
`pcc.status = 4` ở Cty 1; C + 1 dòng `product_galleries`). Id ghi ra log (lượt cuối: A=75343 B=75341 C=75342, natures
7050–7051, types 6095–6096, cluster 6269), xoá ĐÚNG theo id ở `afterAll`; `afterAll` so mốc 13 bảng (products, pcc,
product_units, unit_prices, company_units, galleries, has_accessories, business_catalogs, histories, product_types,
natures, job_clusters, chapters) trước = sau — khớp ở mọi lượt. Soát cuối: 0 dòng `E2ELM%` ở products / natures / types /
job_clusters / chapters / galleries; 0 dòng `E2EC1S%`. N85 dùng 422 giả lập bằng `page.route` ⇒ không ghi DB.

## N99 — kết luận: KHÔNG tái hiện, không sửa

Đường thật: `/customer-care/warranty-repair-requests/create` → chọn KH qua popup (65TPHXAN, không lưu phiếu) →
"Thêm trang thiết bị của khách hàng" → bấm `.select2-selection` bằng chuột → bấm `.select2-results__option` bằng chuột.

| Loại chọn | Nút Chọn trước | dropdown trong `.modal-content` | Sau chọn: ô hiển thị / `select.value` / nút Chọn | Bấm Chọn |
|---|---|---|---|---|
| Thiết bị Tân Phát CC | disabled, aria-disabled=true | có | "Thiết bị Tân Phát CC" / `1` / bật | popup chọn loại đóng, `#add-old-equipment` mở |
| Thiết bị mua NCC khác (mở lại lần 2) | disabled (đã reset) | có | "Thiết bị mua NCC khác" / `2` / bật | popup đóng, `#add-external-equipment` mở |

⇒ select2 phát `change` đúng, `v-model` nhận, luồng 2 bước chạy đúng cả 2 nhánh. Báo lỗi trước là dương tính giả của
script (đổi `<select>` ẩn không phát change jQuery). Đóng N99. Script: scratchpad `loimo-fe/probe-n99.mjs`.

## Lỗi mới (không vá)

- **N114** — `ProductForm.vue` `save()` (~dòng 517): lỗi 422 từ BE chỉ `openFirstErrorTab()`, KHÔNG cuộn tới lỗi (đường lỗi
  FE thì có `scrollToInputError`). Đo ở L4: lỗi ảnh nằm y=1368 trong viewport cao 900 ⇒ người dùng thấy toast/chấm đỏ
  nhưng phải tự cuộn tìm. Áp mọi lỗi BE của form hàng hoá, không riêng ảnh.
- **N115** — Form tạo yêu cầu KTSC-BH: chọn KH xong, bảng thiết bị gọi `GET assign/customers/{id}/equipment` ⇒ **403** với
  tài khoản e2e_assign (console "Error loading equipment"). Route `customer-info` của màn đã cố ý né gate "Xem khách
  hàng" nhưng danh sách thiết bị thì không ⇒ nghi người tạo phiếu thiếu quyền Xem KH sẽ thấy bảng thiết bị trống im lặng
  (cùng họ memory "tự điền KH 403 im lặng"). Chưa khảo sát quyền — có thể chỉ do tài khoản test.
- **N116** — `components/modals/ChooseErpCustomerModal.vue`: console `[Vue warn] The computed property "fields" is already
  defined in data` (+ "already defined as a prop" ở BTable). Vô hại hiển thị nhưng bẩn console mọi màn dùng popup chọn KH.
