# Sao chép hàng hoá — design

Ngày: 24/10/2026 · Nhánh: `feat/sao-chep-hang-hoa` checkout từ `gop_db` (hrm-api + hrm-client — user chốt 24/10) · ERP: không đụng.
Khảo sát nền: [khao-sat.md](khao-sat.md). Hồ sơ cũ liên quan: `2c-ghi/yeu-cau-ghi.md:81-86` (đề xuất), T9 `:257`
(nay đã chốt ở đây), G8 `2c-ghi/chot.md` ("làm sau" — nay làm). Task C4.3 cũ trong `man-danh-muc-hang-hoa/plan.md:577`
("nhân bản server-side") **bỏ**, thay bằng hồ sơ này.

## 1. Mục tiêu

Người làm hàng hoá tạo nhanh một mã mới cùng dòng với mã đang có ở công ty mình (đổi model, đổi quy cách…)
mà không nhập lại hàng chục ô. Bản sao là **hàng mới hoàn toàn của công ty đang làm việc**, đi đúng luồng tạo mới
(Đang nhập thông tin → tính giá / Chuyển KD không tính giá).

Không làm: nhân bản 1 click ở server · sao chép hàng công ty khác chưa lấy về · sao chép hàng Ngừng KD / hàng tạm /
hàng đã xoá · chép giá · cột nguồn `copied_from_id` · sửa gì ở ERP.

## 2. Quyết định đã chốt (user, 24/10/2026)

| # | Câu | Chốt |
|---|---|---|
| S1 | Cách làm | **Form tạo mới điền sẵn** (như ERP). Bấm Lưu đi đúng `POST products` hiện có — mọi luật của đường tạo giữ nguyên |
| S2 | Hàng nguồn | Chỉ hàng **đang có ở công ty mình**: `Product::editableAt(công ty đang làm, pcc.status)` = đúng (hàng active, không Ngừng KD, không hàng tạm, của mình tạo hoặc đã lấy về). Gồm Đang nhập TT · Chờ tính giá · Đang tính giá · Đang KD |
| S3 | Tab Quản trị | **Điền sẵn** (chính sách KD, tồn tối thiểu, bảo hành, NCC, catalog — của công ty đang làm), cho sửa |
| S4 | Tài liệu kỹ thuật | **Chép tệp sang bản mới**: server chép từng tệp S3 của hàng gốc vào thư mục tạm (`tanphat_hrm/tmp`) khi mở form ⇒ form nhận URL tạm như vừa tải lên ⇒ lưu đi đúng luật N14 + `promoteTemporary`. Không nới luật N14 |
| S5 | Ảnh / video | **Dùng chung đường dẫn**. Hàng không có ảnh mô tả nhưng có `avatar` (hàng ERP cũ) ⇒ đưa avatar vào ảnh mô tả của bản sao. Video chép link, bỏ id |
| S6 | Vị trí nút | Menu ⋮ dòng ở 3 màn **Hàng hoá nhập thông tin · Hàng đang kinh doanh · Dữ liệu hàng hoá công ty** + footer **màn chi tiết** hàng hoá |
| S7 | Nguồn gốc | Chỉ ghi **lịch sử**: dòng "Tạo mới" của bản sao kèm ghi chú `Sao chép từ <mã gốc>`. Không thêm cột, không migration |
| S8 | ERP | Giữ nguyên (route copy cũ đã chặn 403 + link sang HRM, nút đã gỡ) |
| S9 | Danh mục đã khoá trên hàng gốc | **Bỏ trống + báo**: giá trị trỏ danh mục khoá (thương hiệu, model, hãng SX, xuất xứ, Loại SP, đặc tính, ĐVT, thuế suất, NCC, chính sách KD, xe/đời xe, ĐVT thuộc tính, loại tài liệu, nhóm máy, tiểu mục catalog nhánh đóng) bị xoá khỏi form + liệt kê trong khối cảnh báo. Hàng MỚI không sinh trên danh mục khoá. Đường tạo tay KHÔNG đổi luật |
| S10 | Chữ trên nút | **"Nhân bản"** theo `button-convention` (cấm "Sao chép"): nút **Nhân bản** (`ri-file-copy-line`), tiêu đề trang **Nhân bản hàng hoá**, dải báo "Đang nhân bản từ …", lịch sử **Nhân bản từ <mã>**, 403 "Không nhân bản được hàng hoá này." — chữ "Sao chép" khác trong tài liệu này hiểu là Nhân bản (user chốt 24/10) |

Cố định theo luồng mới (không hỏi): **không chép giá** (bộ giá rỗng 0 như tạo mới; giá vốn/giá mua 0) · bản sao
pcc 1 + `info_entered_at = now()` ⇒ đủ điều kiện Chuyển KD không tính giá ngay · chủ = công ty đang làm ⇒ không
kế thừa giá theo hãng ở công ty mình · mã sinh mới bằng `ProductCodeGenerator`.

## 3. Thiết kế

### 3.1 BE (hrm-api, `Modules/MasterData`)

**A. `GET products/{id}/copy-data`** — dữ liệu điền sẵn cho form, KHÔNG ghi DB (chỉ chép tệp S3 vào thư mục tạm).
- Route cạnh `GET products/{id}/edit`, middleware `checkPermission:Xây dựng thông tin hàng hoá`.
- Kiểm: `assertCanWrite()` (1652 tại công ty đang làm) · hàng `editableAt(company, pcc.status)` sai ⇒ **403**
  "Không sao chép được hàng hoá này" (gom mọi trường hợp: chưa lấy về, Ngừng KD, hàng tạm, đã xoá).
- Nạp như `edit()` rồi dựng qua `ProductFormResource` với scope `full` (kể cả khi công ty mình chỉ là công ty lấy về
  — bản sao là hàng mới của mình nên form đầy đủ).
- Làm sạch trong BE (một chỗ, FE không phải đoán):
  - bỏ `id`, `code`, `edit_scope`, `pricing_lock_message`, `owner_*`, `has_vehicle_data`…; bỏ `id` của mọi dòng con
    (ĐVT, tài liệu + tệp, ảnh, video, thuộc tính, hàng kèm).
  - **Hàng kèm + máy** (recipe, phụ kiện, phụ kiện lắp đặt, phụ kiện sửa chữa, `machine_ids` tab Nhóm máy): loại dòng mà `checkKitStatus` sẽ chặn
    (hàng đã xoá / hàng tạm / đang khoá tại công ty) — dùng CHUNG điều kiện với `ProductRequest::checkKitStatus`
    (tách hàm, không chép logic). Trả danh sách đã loại ở `dropped_kits: [{group, code, name}]`.
  - **Danh mục khoá (S9)**: gọi `ProductOptionService::formOptions` với `include_ids` = `option_ids` (CÙNG định nghĩa
    `is_locked` mà form dùng để gắn 🔒) ⇒ ô nào đang chọn bản ghi `is_locked` thì xoá (ô đơn ⇒ null, ô nhiều ⇒ bỏ
    phần tử; ĐVT khoá ⇒ để trống `unit_id` của dòng, giữ hệ số). Tiểu mục catalog: `CatalogBranchGuard::closedErrors`
    (cùng luật `checkClusters`). Trả `dropped_locked: [{field_label, name}]`.
  - **Ảnh**: galleries rỗng + có `avatar` hợp lệ (`GALLERY_URL_REGEX` — bỏ `/images/noimage.png`, 125 hàng) ⇒
    galleries = [avatar]. Quá 10 ảnh (3 hàng) ⇒ giữ 10 ảnh đầu + báo. Video không phải URL hợp lệ (2 dòng) ⇒ bỏ + báo.
  - ĐVT sai hệ số (9 hàng) để nguyên — người dùng sửa trên form khi `checkUnits` báo.
  - **Tài liệu kỹ thuật**: mỗi tệp chép S3 ⇒ `tanphat_hrm/tmp/<tên mới>` bằng hàm mới
    `CmcS3Helper::copyToTemporary($url)` (copyObject trong cùng bucket, tên đích mới để không đè). Tệp nguồn không
    còn (404) ⇒ bỏ tệp đó, ghi vào `dropped_files`. Không tách được key (URL ngoài bucket) ⇒ cũng bỏ + báo.
  - `copy_source: {id, code, name}` để FE hiện tiêu đề / gửi lại.
- Trả kèm `option_ids` như `/edit` để ô chọn danh mục khoá vẫn hiện.

**B. `POST products` nhận thêm `copy_from_id`** (nullable, integer). `ProductRequest::rules()` thêm
`copy_from_id => nullable|integer|exists:products,id` NGOÀI `commonRules()` (`TempProductRequest` kế thừa
`commonRules` — hàng tạm không nhận khoá này). Không đưa vào `fillCommon`. `store($data, $status, ?int $copyFromId)` ⇒
`storeWithRetry` truyền tiếp ⇒ `logCreate($id, 'Sao chép từ ' . $code)` (gọi ở `ProductWriteService:117`; đường hàng tạm
không truyền ⇒ không đổi). Không kiểm lại `editableAt` ở đây (chỉ là ghi chú
lịch sử; dữ liệu đã qua đủ luật tạo mới).

**C. Cờ `can_copy`** ở `ProductListResource` + `ProductDetailResource`: `$canBuild && editableAt(company, status)`
(cùng điều kiện `can_edit`, khai riêng để sau này tách được).

### 3.2 FE (hrm-client)

- `pages/master-data/products/create.vue`: đọc `?copy_from=<id>` ⇒ tiêu đề **"Sao chép hàng hoá"**, truyền prop
  `copy-from-id` cho `ProductForm`. Giữ nguyên gate quyền + `dueConfigCreateGuardMixin`.
- `ProductForm.vue` `init()`: nhánh mới khi có `copyFromId` (mode create) ⇒ gọi `copy-data`, đổ vào form như nhánh
  edit (`{...emptyForm(), ...data}`, attributes `checked: true`), `option_ids` ⇒ `loadOptions`. Lỗi 403/404 ⇒ toast
  lỗi BE + quay về `backUrl`. Payload thêm `copy_from_id` (chỉ khi sao chép).
- **Thông báo trên form** (khối cảnh báo đầu form, dùng mẫu thông báo có sẵn của form — tra trước khi viết):
  "Đang sao chép từ <mã> — <tên>. Đổi Tên / Model / Thương hiệu / Hãng sản xuất để không trùng hàng gốc. Giá không
  được sao chép." + liệt kê `dropped_kits` / `dropped_files` nếu có.
- Nút **Sao chép** (`icon ri-file-copy-line`), hiện khi `item.can_copy`:
  - Menu ⋮ dòng `ProductListPage.vue` `rowActionsOf` — sau "Sửa", chỉ ở màn `entering`, `trading`, `company`.
  - Footer màn chi tiết `pages/master-data/products/_id/index.vue` `V2Footer #custom-actions`, theo `button-convention`
    (tra skill trước khi đặt màu/thứ tự).
  - Bấm ⇒ `/master-data/products/create?copy_from=<id>&from=<màn hiện tại>`.
- Lưu xong như tạo mới: sang chi tiết hàng vừa tạo.

## 4. Ca biên

| Ca | Xử lý |
|---|---|
| Không sửa gì, bấm Lưu | 422 trùng Tên × Model × Thương hiệu × Hãng (luật có sẵn), form nhảy tới ô Tên |
| Hàng gốc chưa có Loại SP | ô Loại SP trống, bắt buộc chọn (luật có sẵn) |
| Hàng gốc có dữ liệu xe nhưng Tính chất không phải phụ tùng ô tô | BE tạo mới tự bỏ dữ liệu xe (có sẵn `ProductWriteService:727`) |
| Hàng kèm / máy bị khoá / xoá / tạm | loại khỏi form + báo trong khối cảnh báo |
| Danh mục đang chọn đã khoá | ô để trống + báo; ô bắt buộc (Loại SP, ĐVT cơ bản, thương hiệu…) ⇒ người dùng chọn lại, Lưu báo lỗi nếu quên |
| Ảnh đại diện mặc định / >10 ảnh / video hỏng | bỏ / cắt 10 + báo |
| Tệp tài liệu mất trên S3 | bỏ tệp + báo; không chặn mở form |
| Mở form sao chép rồi huỷ | tệp tạm bị `files:clean-temporary` dọn |
| Mất quyền 1652 / hàng chuyển Ngừng KD giữa chừng | `copy-data` 403; nếu đã mở form thì Lưu vẫn là tạo mới hợp lệ |
| Còn hàng quá hạn | `dueConfig` chặn như tạo mới |
| Người không có quyền | không thấy nút; gõ URL ⇒ 404 trang (gate có sẵn) / API 403 |

## 5. Kiểm thử

- PHPUnit MasterData: `copy-data` (có quyền / không quyền 403 / hàng công ty khác chưa lấy về 403 / Ngừng KD 403 /
  hàng tạm 403 / bỏ id con / loại hàng kèm khoá / avatar ⇒ galleries / tệp chép sang tmp — **mock `CmcS3Helper`**,
  local S3 trỏ bucket PROD) · `store` với `copy_from_id` ghi đúng ghi chú lịch sử · `can_copy` ở list/detail.
- Playwright MCP (bắt buộc trước khi báo xong): nút ở 3 màn + footer chi tiết (đo số nút, có/không quyền), form điền
  sẵn (đếm ô có giá trị, khối cảnh báo, tiêu đề), lưu ra mã mới + lịch sử. Upload/chép S3 giả lập bằng `page.route`.
- Cập nhật spec e2e (chưa chạy trừ khi user yêu cầu): ca có quyền + không quyền.

## 6. Quyết định do Claude tự chốt (soát design 24/10 — user xem lại khi đọc)

- Lọc máy (`machine_ids`) cùng hàng kèm — `checkKitStatus` chặn cả máy (`ProductRequest.php:385`).
- Ảnh đại diện mặc định bỏ qua, >10 ảnh cắt 10, video hỏng bỏ — đều báo trong khối cảnh báo.
- ĐVT sai hệ số không tự sửa (để `checkUnits` báo trên form).
- `copy_from_id` truyền qua tham số `store`, không đặt trong `commonRules`.
- `copy-data` gom mọi trường hợp không được sao chép thành một 403 chung.
- Menu dòng: **Nhân bản đứng SAU Xoá/Khoá** (V2BaseRowActions đưa 3 mục đầu ra ngoài; quy ước Sửa → Xoá/Khoá → ⋮); footer chi tiết:
  nút `secondary` (trắng) cuối slot, trước Quay lại.
- Review 24/10: lọc hết máy ⇒ bỏ luôn **Nhóm máy** (luật "có nhóm máy phải có máy") + báo; **đời xe KHÔNG lọc theo model đang chọn**
  (R20 — giữ đời xe cũ ERP), chỉ bỏ đời xe của model vừa bỏ vì khoá.
- FE: lỗi 403/500/504 do interceptor axios toast sẵn ⇒ form không toast thêm; 404 ⇒ "Không tìm thấy hàng hoá để nhân bản.".
- Để sau (Minor review): id hàng kèm mồ côi; lỗi S3 khác 404 làm 500 cả form; dải cảnh báo chưa nhắc mất dữ liệu xe khi Tính chất
  không phải phụ tùng; copy-data dựng cả form-options chỉ để đọc `is_locked` (nặng). Chi tiết: progress.md.

## 7. Để builder tự quyết

Tên hàm/biến, vị trí tách hàm kiểm hàng kèm, câu chữ thông báo (theo giọng các thông báo có sẵn), tên tệp đích
trong thư mục tạm.
