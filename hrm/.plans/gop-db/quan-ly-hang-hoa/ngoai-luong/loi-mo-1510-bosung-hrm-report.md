# Report đợt bổ sung 15/10 (HRM) — (a) hrm-api N112 · (b) hrm-client N114 · N116

Repo `wt-chuyen-doi-hang-hoa/{hrm-api,hrm-client}`, nhánh chung `feat/chuyen-doi-hang-hoa`. Không push, không stash.
Soát marker xung đột (`git grep '^<<<<<<<|^>>>>>>>'`) sau merge: 0 ở cả 2 repo. EOL: mọi file LF, `git diff --numstat` chỉ
có dòng sửa chủ ý. Server 8031 / Nuxt 3031 KHÔNG restart (PHP đọc code mới, Nuxt hot reload).

## (a) hrm-api — N112

Nhánh con `feat/cdhh-loi-mo-2-api` (từ `ca4a37802`) ⇒ merge `--no-ff` LOCAL: **`4bdcf760e`**.

| Mã | Commit | Nội dung |
|---|---|---|
| N112 | `954f1bb98` | `AdminData::formValues` coi dòng pcc `status IS NULL` như không có dòng ⇒ lùi thông tin chung của hàng |
| merge | `4bdcf760e` | Merge feat/cdhh-loi-mo-2-api |

- File: `Modules/MasterData/Transformers/Product/AdminData.php` (`formValues`, +4 dòng + comment),
  `Modules/MasterData/Tests/Feature/AdminDataNullStatusTest.php` (+4 ca).
- Luật: đúng N91 / ERP `Product::adminRowFor()` (`$row && $row->status !== null ? $row : null`). Dòng ĐANG DÙNG (status
  khác NULL) của công ty lấy về vẫn đọc nghiêm như Q-A3 (ca chặn hồi quy).
- Hệ quả cần biết: dòng NULL ở công ty chủ, bấm Lưu thì `writeAdmin` (không đổi) ghi đè số đang hiện (= số chung) vào
  dòng đó và đưa dòng vào luồng (status 3) — như trước. Công ty KHÔNG phải chủ có dòng NULL thì `/edit` vẫn 403
  ("chưa lấy về"), nên nhánh "lấy về" chỉ chạm qua form hàng tạm / `sameAsShown`. Dữ liệu dev: 298 dòng NULL, cả 298
  đều trống 4 ô (bảo hành, ĐVT bảo hành, tồn tối thiểu, chính sách) ⇒ trước sửa nhánh lấy về hiện TRỐNG trong khi màn
  chi tiết hiện số chung.

Test (đỏ trước khi sửa, đã đo):
- `form_values_cong_ty_lay_ve_dong_null_status_lui_cot_chung`: `null is identical to 12` ⇒ xanh.
- `form_values_dong_null_status_co_so_van_bo_qua_ca_2_nhanh` (dòng NULL CÓ số 2 năm / tồn 7 / chính sách; nhánh lấy về
  + nhánh chủ): `2 is identical to 12` ⇒ xanh.
- `api_form_sua_bang_man_chi_tiet_voi_dong_null_status` (GET `/edit` so GET chi tiết, chủ Cty 1): form "2 năm" ≠ chi tiết
  "12 tháng" ⇒ xanh (cả 2 "12 tháng", tồn 3).
- `form_values_dong_co_status_lay_ve_van_doc_nghiem_dong`: xanh trước và sau (chặn hồi quy Q-A3).
- `Modules/MasterData/Tests`: **OK 557/557** (5101 assertions) = mốc 553 + 4 ca mới.
- Fixture trong `DatabaseTransactions` (kể cả 1 dòng `business_policies` tạo tạm vì bảng dev rỗng). Sau chạy:
  `business_policies` = 0, dòng pcc NULL-status = 298 (như trước).

## (b) hrm-client — N114 · N116

Nhánh con `feat/cdhh-loi-mo-2-fe` (từ `f211bd195`) ⇒ merge `--no-ff` LOCAL: **`baa5a3563`**.

| Mã | Commit | Nội dung |
|---|---|---|
| N114 | `5e1e0f845` | `ProductForm.focusFirstError()` — 422 ⇒ cuộn + focus ô lỗi đầu tiên (Lưu + Lưu/Đồng ý hàng tạm) |
| N116 | `e1541058f` | `ChooseErpCustomerModal` đổi data `fields` ⇒ `tableFields` |
| merge | `baa5a3563` | Merge feat/cdhh-loi-mo-2-fe |

### N114 — tái hiện trước khi sửa

Đo dòng thời gian (mỗi 100ms) sau khi bấm Lưu với 422 giả lập `galleries.0`, đứng ở bước Thông số, khung 1280×900
(hàng 49017, không ghi DB):

| t (ms) | scrollY | top lỗi đầu | phần tử focus |
|---|---|---|---|
| 200 | 17 | 1351 | DIV |
| 400 | 625 | 743 | DIV |
| ≥ 600 | 699 | 669 (trong khung) | DIV (không đổi tới 2,5s) |

⇒ Ghi nhận thật: mixin `applyServerErrors` ĐÃ cuộn (`scrollToInputError` lúc 100ms); con số y=1368 của L4 đợt 2 là đo
ngay lúc lỗi vừa hiện, trước lượt cuộn. Phần hỏng thật là **không focus** ô nào (`activeElement` = body/DIV ở cả 4 ca),
cộng với helper chung không loại lỗi nằm trong pane `v-show` ẩn và không nhận `.invalid-feedback.d-block` (xem N123).

Sửa: `focusFirstError()` chạy sau `openFirstErrorTab()` (nextTick → rAF → 150ms, tức sau lượt cuộn của mixin nên lượt
này quyết): lấy lỗi đầu tiên CÓ hộp hiển thị trong `this.$el` (`.v2-error, .invalid-feedback.d-block`), nhóm =
`td / .form-group / [class*="col-"]`, không có thì `parentElement` (không lùi cả panel); focus ô nhập đứng NGAY TRƯỚC lỗi
(input/textarea/select, `.select2-selection`, kể cả ô chọn ảnh) — KHÔNG focus nút (lỗi ảnh mà focus nút Xoá ảnh thì
Enter là xoá nhầm). Cuộn `smooth/center` rồi `focus({preventScroll:true})`.

### Số đo trước / sau (Playwright headless, đo DOM, sau 1,8s)

| Ca (422 giả) | Trước: lỗi top / trong khung / focus | Sau: lỗi top / trong khung / focus |
|---|---|---|
| `galleries.0`, đứng ở bước Thông số | 669 / có / `body` | 669 / có / `input.v2-file__input` (top 626, ô Chọn ảnh) |
| `name` + `galleries.0`, đứng ở Nhóm máy | 320 / có / `body` | 320 / có / `input.v2-input` (ô Tên, top 284) |
| `units.0.unit_id`, cuộn sẵn xuống đáy | 486 / có / `body` | 470 / có / `span.select2-selection` (ô ĐVT dòng 1) |
| `admin.guarantee`, đứng ở Thông số | 337 / có / `body` | 337 / có / `input.v2-input` (ô Bảo hành, tab Quản trị) |

Mọi ca tự mở đúng tab/bước chứa lỗi (bước `general` / tab "Quản trị hàng hoá").

### N116

Tái hiện (màn `/customer-care/warranty-repair-requests/create`, mở popup Chọn KH, không lưu):

| Đo | Trước | Sau |
|---|---|---|
| `[Vue warn] computed property "fields" is already defined in data` | 1 | **0** |
| `… already defined as a prop` ở `<BTable>` | 1 | 1 (lỗi chung — N122) |
| số `thead th` / ô dòng 1 / số dòng | 9 / 9 / 10 | 9 / 9 / 10 |
| tiêu đề cột | STT, Mã KH - Tên khách hàng, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP | y hệt |

Nguyên nhân: vee-validate 2 (`Vue.use(VeeValidate)` mặc định `inject: true`, `fieldsBagName: 'fields'`) tự gắn
computed `fields` vào MỌI component ⇒ trùng tên data `fields` của popup. Đổi tên data là hết cảnh báo của popup; không
ai ngoài file đọc `.fields` của popup (đã grep).

### E2E

Spec `e2e/tests/master-data/products-form-loimo-ui.spec.ts` (e2e nằm ngoài git) thêm:
- **L6 (N114)**: 2 lượt 422 giả (`galleries.0`, `admin.guarantee`) từ bước Thông số ⇒ lỗi đầu trong khung nhìn, focus là
  `input` cùng nhóm với lỗi (`v2-file__input` / `v2-input`), không phải nút `icon-btn`; số `product_galleries` của C giữ 1.
- **L7 (N116)**: popup Chọn KH — 9 tiêu đề đúng thứ tự, dòng 1 đủ 9 ô, 0 cảnh báo "already defined in data" (cảnh báo
  BTable chỉ in log, ghi N122).
- Trước sửa (đã gỡ tạm 2 file về HEAD rồi áp lại bản sửa): L6 **fail** (`activeNearError` false hết 10s), L7 **fail**
  (`dataWarn` 1).
- Sau sửa, nhánh con: **7 passed** (0 failed, 0 did not run). Sau merge, nhánh chung: **7 passed** (0 failed, 0 did not run).
  L6 đo trong project (viewport 1280×720): ảnh top 576/bottom 598, Bảo hành top 337.
- Spec liên quan `products-form-ui.spec.ts` (ProductForm): **17 passed, 1 skipped** (E11 skip sẵn), 0 failed, 0 did not run.
- Lệnh: `API_BASE=http://127.0.0.1:8031 BASE_URL=http://127.0.0.1:3031 npx playwright test <spec> --project=chromium
  --no-deps --workers=1` (node 20).
- Fixture `E2ELM` dọn đúng id ở `afterAll` + assert mốc 13 bảng trước = sau (lượt cuối A=75953 B=75951 C=75952, natures
  7237–7238, types 6268–6269, cluster 6403). Soát tay sau chạy: `products` 45.890 / pcc 113.782 (= trước), 0 dòng
  `E2ELM%` ở products / natures. N114/N116 không ghi DB (422 giả bằng `page.route`, popup chỉ mở).
- Script Playwright tái hiện/đo: scratchpad `loimo2/probe-n114.mjs`, `probe-n114-timeline.mjs`, `probe-n116.mjs`,
  `probe-btable.mjs`.

## Lỗi mới (không vá)

- **N122** — Cảnh báo `[Vue warn] The computed property "fields" is already defined as a prop` ở MỌI `<b-table>` toàn app
  (đối chứng: `/rice/category/menu` cũng có). Do vee-validate 2 gắn computed `fields` vào cả BTable (có prop `fields`).
  Thêm nữa 215 component khai data `fields: [` đều dính cảnh báo kiểu N116. Hướng sửa gốc (đụng toàn cục, cần user
  chốt): `Vue.use(VeeValidate, { fieldsBagName: 'veeFields' })` ở `plugins/vee-validate.js` — đã grep, không thấy code
  nào đọc cờ field (`fields.x.dirty/touched/valid…`), nhưng phải chạy lại e2e các màn form trước khi áp.
- **N123** — Helper chung `utils/helpers.js::scrollToInputError` (mixin `formValidateMixin` gọi cho mọi form 422/FE):
  (1) chỉ xét `display` của CHÍNH phần tử lỗi, không loại lỗi nằm trong pane/tab `v-show` đang ẩn ⇒ form nhiều tab có
  thể "cuộn" tới lỗi vô hình (không nhúc nhích); (2) quét `span.text-danger` ⇒ bắt nhầm dấu `*` bắt buộc dạng
  `<span class="text-danger">*</span>` (vd tiêu đề "Catalog kinh doanh" ở `ProductFormCatalogPicker`); (3) không nhận
  `.invalid-feedback.d-block` (memory marker); (4) không focus. Form hàng hoá đã có `focusFirstError` riêng (N114) chạy
  sau nên không bị ảnh hưởng; các form khác chưa soát.
