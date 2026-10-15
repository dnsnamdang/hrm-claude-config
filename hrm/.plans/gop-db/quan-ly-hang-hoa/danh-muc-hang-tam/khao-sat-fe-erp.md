# Khảo sát FE + quyền — luồng Hàng tạm ERP (12/10/2026)

> Chỉ đọc, không sửa source. Nguồn ERP: worktree `wt-erp-2d1`. Đường dẫn ERP tính từ gốc `wt-erp-2d1/`.
> HRM: `wt-chuyen-doi-hang-hoa/hrm-client` + `hrm-api` (nhánh `feat/chuyen-doi-hang-hoa`).
>
> Viết tắt: **HT** = hàng tạm (`tmp_products`, model `App\Model\Product\TmpProduct`) · **PYC** = Phiếu yêu cầu
> duyệt hàng tạm (`tmp_product_requests`, model `App\Model\Product\TmpProductRequest`, mã `PYCDHT-xxxxx`).

---

## 0. Bức tranh chung

```
Tạo HT ── (a) popup "Thêm nhanh hàng hóa" trong Báo giá thường / màn Tạo PYC  → status 2 Chờ duyệt (+ notify người có quyền Duyệt)
       └─ (b) HRM báo giá dự án trúng thầu "Gửi duyệt hàng tạm" → API sync-from-hrm → status 3 Đang tạo (KHÔNG notify)

HT  Đang tạo(3) ─[người tạo: Lưu]→ 3 · ─[Lưu và gửi duyệt]→ Chờ duyệt(2)
    Chờ duyệt(2) ─[Duyệt]→ Đã duyệt(1)  ⇒ Product::createRecord() tạo HÀNG HOÁ THẬT (19,5% hàng hoá ERP sinh từ đây)
                └─[Không duyệt + Ghi chú duyệt bắt buộc]→ Không duyệt(0) ─[người tạo: Gửi duyệt lại]→ 2
                └─[Xoá]→ -1 (ẩn mềm)
PYC  không có status riêng — TÍNH từ các HT con (TmpProductRequest.php:178-204):
     hết con / con đều 2 → Chờ xử lý(3) · toàn con nháp → Đang tạo(4) · lẫn nháp & đã gửi hoặc có con 0/1 → Đang xử lý(2) · không con nào 2 → Hoàn thành(1)
```

- Hằng số trạng thái HT: `app/Model/Product/TmpProduct.php:11-15` (-1 Xoá · 0 Không duyệt · 1 Đã duyệt · 2 Chờ duyệt · 3 Đang tạo).
- Không có màn "chi tiết HT" thật: `TmpProductsController@show` và `MyTmpProductsController@show` đều `return "Đang phát triển"`
  (`TmpProductsController.php:929-932`, `MyTmpProductsController.php:136-153`). **Mọi lối xem/sửa/duyệt đều đi màn `/{id}/edit`.**

---

## 1. Danh sách màn + popup

| # | Màn / popup | Route (`routes/web.php`) | Controller | View |
|---|---|---|---|---|
| M1 | **Quản lý hàng tạm** (danh sách) | `GET /admin/tmp_products` `tmpProductIndex` :682 | `TmpProductsController@index` :45 | `sale/tmp_products/list.blade.php` |
| M2 | **Duyệt hàng hóa tạm** (xem / sửa nháp / duyệt / từ chối / gửi lại) | `GET /{id}/edit` `tmpProductEdit` :683 (mw `checkDueConfigs`) | `@edit` :211 | `sale/tmp_products/edit.blade.php` + `form.blade.php` (1529 dòng) |
| M3 | **Hàng tạm của tôi** | `GET /admin/my_tmp_products` `myTmpProductIndex` :697 | `MyTmpProductsController@index` :40 | `sale/my_tmp_products/list.blade.php` |
| M3b | Chi tiết HT của tôi | `myTmpProductShow` :698 | `@show` :136 | **"Đang phát triển"** (view `show.blade.php` 478 dòng là code chết) |
| M4 | **Danh sách yêu cầu duyệt hàng tạm** (`?type=all` / `approve` / trần) | `GET /admin/sale/tmp_product_requests` :3637 | `TmpProductRequestController@index` :26 | `sale/tmp_product_requests/index.blade.php` |
| M5 | **Tạo yêu cầu duyệt hàng tạm** | `/create` :3638 → `POST /store` :3640 | `@create` :64, `@store` :93 | `create.blade.php` + `form.blade.php` + `formJs.blade.php` |
| M6 | **Chi tiết yêu cầu duyệt hàng tạm {code}** | `/{id}/show` :3639, `POST /{id}/update-note` :3643 | `@show` :68, `@updateNote` :75 | `show.blade.php` |
| M7 | In PYC | `/{id}/print` :3642 | `@print` :129 | `view('print')` + mẫu `ReportTemplate::YC_DUYET_HANG_TAM` |
| P1 | **Popup "Thêm nhanh hàng hóa"** (tạo HT) | `POST /admin/tmp_products` `tmpProductStore` :681 (mw `checkPermission:Thêm báo giá`) | `@store` :250 | `partials/tmpProduct/createTmpProductForm.blade.php` (587) + `createTmpProductJs.blade.php` (127) |
| P2 | Màn **Làm lại báo giá** (đổi HT đã duyệt → hàng thật trong báo giá) + popup "Chi tiết duyệt hàng tạm" | `quotation.tmpProductChange` :5376 / `…Store` :5377 | `QuotationsController@tmpProductChange` :958 | `quotations/tmp_product_change.blade.php` |
| — | Xuất Excel / CSV / PDF danh sách HT | `/exportExcel|CSV|PDF` :689-691 | `@exportExcel` :171… | xuất `TmpProduct::all()` không lọc; PDF dùng view `products.pdf` + host cứng `localhost:8000` (:205) |

---

## 2. Từng màn

### 2.1 M1 — Quản lý hàng tạm (`sale/tmp_products/list.blade.php`)

- Khuôn ERP cũ: DataTable server-side, **hàng lọc dưới tiêu đề cột** (ô text / select theo cột), nút 🔍 Tìm kiếm + ⟳ Tất cả ở cột Hành động (:175-181); lưu bộ lọc `saveSearch/restoreSearch`.
- Thanh nút trên bảng (:36-39): **Tùy chỉnh cột** (popup kéo-thả + tick ẩn/hiện, "Phục hồi mặc định", lưu `localStorage['tmp-product-columns']` :124/:144) · **Xuất CSV** · **Xuất Excel** · **Xuất PDF**. Không có nút Thêm mới.
- Cột (`defaultColumns` :100-119; ✔ = hiện mặc định):

| Cột | Mặc định | Lọc | Ghi chú render (Controller `searchData` :53-168) |
|---|---|---|---|
| Tên hàng hóa | ✔ | text | |
| Model | ✔ | text (like theo tên model) | "Chưa xác định" nếu model đã xoá |
| Thông số cơ bản | ✔ | — | "- Tên: giá trị đơn vị" mỗi dòng; có Read more/less (:205-228) |
| Nhóm | ✗ | select | |
| Thương hiệu | ✔ | select | |
| Xuất xứ | ✗ | select | |
| Hãng sản xuất | ✗ | select | |
| Định mức công | ✗ | — | |
| Loại sản phẩm | ✗ | select (`PRODUCT_TYPES`) | |
| Ảnh | ✗ | — | thumbnail 50px |
| Người tạo | ✔ | select | "Mã phòng - Họ tên" |
| Ngày tạo | ✗ | — | d/m/Y |
| Trạng thái | ✔ | select (Đã duyệt/Không duyệt/Đang chờ duyệt/Đang tạo) | badge: 0 đỏ "Không duyệt" · 2 xanh dương "Đang chờ duyệt" · 1 xanh lá "Đã duyệt" · 3 **đỏ** "Đang tạo" (:136-146) |
| Người duyệt | ✔ | select | "Mã phòng - Họ tên" |
| Ghi chú duyệt | ✔ | — | `comment` |
| Hệ số / Giá vốn / Giá {loại giá 1} | ✗ | — | lấy đơn vị cơ bản, giá loại đầu tiên (:120-128) |

- Phạm vi dữ liệu (`TmpProduct::searchByFilter` :176-194): có **Xem danh sách hàng tạm** hoặc **Duyệt hàng tạm** ⇒ tất cả; không ⇒ HT thuộc cặp Thương hiệu–Hãng SX mình đang phụ trách (`AssignHistory`, `employee_date_to` null) **hoặc** do mình tạo. Mặc định sắp `created_at DESC`. Không lọc theo công ty.
- Cột Hành động (`searchData` :147-165) — **tất cả đều trỏ M2 `/edit`** trừ Xoá:

| Nút | Điều kiện hiện |
|---|---|
| ✏ "Sửa hàng tạm" (vàng) | `canEdit()`: status 3 **và** là người tạo (`TmpProduct.php:72-74`) |
| 👁 "Xem chi tiết" | `canView()`: quyền **Xem danh sách hàng tạm** (:68-70) |
| ✏ "Duyệt hàng hóa tạm" (xanh) | `canApprove()`: status 2 **và** (quyền **Duyệt hàng tạm** **hoặc** đang phụ trách cặp Thương hiệu–Hãng của HT) (:56-58) |
| ✏ "Sửa và gửi duyệt lại" | status 0 **và** là người tạo |
| 🗑 "Xóa hàng hóa tạm" | `canDelete()` = y hệt `canApprove()` (:64-66) — chỉ xoá được HT **Chờ duyệt** |

- Xoá: link GET `/{id}/delete` **không có lớp `delete` ⇒ không hỏi xác nhận** (partial `confirm` chỉ bắt `a.delete`). BE (:899-927): status 1 ⇒ toast cảnh báo "Không thể xóa hàng tạm đã duyệt!"; còn lại set `status=-1`, notify người tạo "{tên} vừa xóa sản phẩm tạm: **{tên HT}**" (link `myTmpProductShow` — trang chết), redirect về M1 với "Xóa hàng tạm thành công!". ⚠️ HT đã xoá (-1) **không bị loại khỏi danh sách** (searchByFilter không lọc `status != -1`), badge Trạng thái trống.

### 2.2 M2 — Duyệt hàng hóa tạm (`edit.blade.php` + `form.blade.php`)

**Bố cục form** — gần như bản chép form hàng hoá ERP `products/form.blade.php` (diff ~15 chỗ: bỏ cột "Thành phần chính" ở Công thức lắp ráp, card Phụ tùng chỉ cho `accessories`, **bảng giá theo loại giá bị comment** :1049-1143, ô NCC nạp bằng ajax). 2 cột `col-md-9` / `col-md-3`, các card xếp dọc (không tab):

Cột trái (`col-md-9`):

| Card (dòng) | Trường (★ = nhãn bắt buộc) |
|---|---|
| Thông tin hàng hóa (:3-160) | ★Tính chất hàng hóa (select `product_type`) · ★Model (select2 + nút ➕ tạo model nhanh) · Loại hàng hóa (multi `product_cate`; BE store bắt buộc) · ★Tên hàng hóa · Tên hàng thường gọi · Tên tiếng Anh · Barcode · Định mức công lắp đặt · Hệ số công nghệ · Bảo hành (số + Ngày/Tháng/Năm) · Ghi chú |
| Tài liệu kỹ thuật (:162-243) | bảng STT · Danh mục · Tài liệu (nhiều file) · ➕/➖ |
| Thông số cơ bản ★ (:245-350) | Trọng lượng(kg) · Kích thước(cm) · ★Nhóm hàng hóa (đổi nhóm ⇒ nạp thuộc tính `/admin/attributes/byGroup/{id}`) · bảng Tên · Giá trị · Đơn vị · ☑Lưu · ☑In |
| Phụ tùng – Phụ kiện (:352, chỉ khi Tính chất = accessories) | Nhóm máy · ★Máy (bảng Mã máy/Tên máy, nút tìm) |
| Phụ tùng ô tô (:422, chỉ automotive_parts) | ★Hãng xe · Loại xe · Model xe (mỗi ô "Chọn tất cả") · bảng Hãng/Loại/Model/Đời xe |
| Phụ kiện tùy chọn mua thêm (:598) · Vật tư sửa chữa - bảo dưỡng (:665) · Vật tư phục vụ lắp đặt (:713) · Công thức lắp ráp (:779) · Phụ kiện tiêu chuẩn (:841) | bảng hàng hoá (Mã · Tên · Code đặt hàng · ĐVT · Số lượng [· Bảo hành]) + nút tìm hàng |
| Đặc điểm (:857) | CKEditor |
| **Hệ số giá theo công ty** (:872, chỉ khi quyền **Quản lý giá**) | bảng STT · Công ty · Hệ số |
| Khác (:935) | % giảm giá thanh lý |
| **Giá theo đơn vị** (:951, `can_show_price` = quyền **Quản lý giá** hoặc bản ghi chưa có id ⇒ ở M2 luôn cần quyền) | tab mỗi đơn vị (➕ thêm, ✖ xoá); mỗi tab: ★Đơn vị / Đơn vị cơ bản · ★Hệ số quy đổi · ★Giá vốn · Giá mua ngoài · ★Hệ số tính định mức hàng thúc đẩy bán · Định mức đàm phán giá hàng thúc đẩy bán(%) + ☑ Tính theo giá niêm yết. (Bảng Loại giá · Hệ số · Giá công thức · Giá bán · Định mức đàm phán · Ngày hiệu lực đã comment) |

Cột phải (`col-md-3`):

| Card | Trường |
|---|---|
| Nguồn gốc (:1153) | ★Thương hiệu · ★Xuất xứ · ★Hãng sản xuất (đổi ⇒ set `company_id` theo hãng) · Code đặt hàng (multi + "Thêm nhanh" popup `createBarcode`) · Nhà cung cấp (multi) · ★Công ty |
| Đặt hàng (:1263) | Tên khai báo hải quan · HS Code · ★% VAT · Thuế NK (không CO) · Thuế NK (có CO) · Thuế chống bán phá giá (%) · SL tối thiểu nhập mua · ☑Tính thuế BVMT · Hệ số thuế BVMT |
| Kho hàng (:1400) | SL tồn kho tối thiểu |
| Ảnh hàng hóa (:1419) | tab ★Ảnh đại diện / Ảnh mô tả (dropzone) |
| Video (:1487) | bảng Tên · URL |

**Khối duyệt** (`edit.blade.php`):

| Điều kiện (thứ tự if/elseif) | Hiện |
|---|---|
| `canApprove()` (:19, :33) | card **Ghi chú duyệt (\*)** (textarea `comment`) + nút **Duyệt** (xanh lá) + **Không duyệt** (đỏ) |
| status 0 & là người tạo (:47) | nút **Gửi duyệt lại** → `saveDraft(1)` |
| `canEdit()` (status 3 & người tạo) (:56) | nút **Lưu** → `saveDraft(0)` + **Lưu và gửi duyệt** → `saveDraft(1)` |
| còn lại (vd người có quyền Xem, HT đã duyệt) | form vẫn MỞ nhập nhưng không có nút nào — "xem" = form không lưu được |

- Không có nút Quay lại/Huỷ ở M2. Không hỏi xác nhận trước Duyệt / Không duyệt.
- **Duyệt** (`submit()` :137-176 → `POST /{id}/approve`, BE :538-687): validate theo **luật hàng hoá chính thức** `Product::getRules/getTranslate` (không phải luật HT); ghi đè HT bằng dữ liệu người duyệt sửa; tạo hàng thật `Product::createRecord($request, $tmp->id)`; status 1, `approver_id`, `comment`. Thành công ⇒ về M1 + toast "Duyệt hàng hóa tạm thành công!". Lỗi ⇒ "Duyệt hàng tạm thất bại!" + lỗi từng ô; sai trạng thái ⇒ "Không thể duyệt hàng hóa tạm này do trạng thái hàng không đúng!"; không quyền ⇒ "Không có quyền duyệt!". Notify người tạo "… vừa duyệt sản phẩm tạm: **X**" (link `myTmpProductShow` ⇒ trang "Đang phát triển").
- **Không duyệt** (`reject()` :178-209 → `PUT /{id}/reject`, BE :690-742): `comment` bắt buộc ≤255 ("Bắt buộc phải nhập"); status ≠2 ⇒ "Từ chối phê duyệt thất bại!"; OK ⇒ status 0, toast "Từ chối phê duyệt thành công!", về M1. Notify người tạo "… không duyệt sản phẩm tạm: **X**" (link M2). ⚠️ BE reject **không kiểm `canApprove()`** — ai gọi được route cũng từ chối được.
- **Lưu / Lưu và gửi duyệt / Gửi duyệt lại** (`saveDraft(submit)` :211-249 → `POST /{id}/draft`, BE :746-896): chỉ người tạo, status 3 hoặc 0 ("Không thể sửa hàng tạm này!"). Lưu nháp: chỉ bắt Tên ("Vui lòng nhập tên hàng"), toast "Đã lưu nháp!". Gửi duyệt: validate đủ luật hàng hoá, status → 2, nếu từ trạng thái 0 thì xoá `comment` + `approver_id`; toast "Đã gửi duyệt!"; notify quyền **Duyệt hàng tạm** "… vừa gửi duyệt hàng tạm **X**" (link M2). Lỗi: "Gửi duyệt thất bại!" / "Lưu thất bại!". Thành công đều về M1.

### 2.3 M3 — Hàng tạm của tôi (`sale/my_tmp_products/list.blade.php`)

- Lối vào: menu tài khoản (avatar) `layouts/topheader.blade.php:171` — không gate quyền.
- Cùng khuôn M1 (Tùy chỉnh cột, lưu cột). Cột (:95-109): Tên hàng hóa ✔ · Model ✔ · Thông số cơ bản ✔ · Nhóm ✔ · Thương hiệu ✔ · Trạng thái ✔ · Xuất xứ · Hãng SX · Định mức công · Loại SP · Ảnh · Người duyệt ✔ · Ghi chú duyệt ✔.
- Dữ liệu: `created_by = mình` (Controller :46-52). ⚠️ **Hàng lọc vẽ ra nhưng BE bỏ qua mọi tham số lọc**; select Trạng thái thiếu "Đang tạo" (:139); không loại HT đã xoá.
- Hành động: 1 nút ℹ "Chi tiết hàng hóa tạm" → `myTmpProductShow` = **trang chữ "Đang phát triển"**. ⇒ Người tạo muốn sửa nháp / gửi lại phải sang M1.

### 2.4 M4 — Danh sách yêu cầu duyệt hàng tạm (`tmp_product_requests/index.blade.php`)

- Khuôn ERP mới hơn (`new DATATABLE` — bộ lọc phía trên, có lọc thời gian, có nút Thêm mới `create_link`).
- Cột (:43-50): STT · **Số yêu cầu** (link M6) · Người lập · Ngày lập · Trạng thái (badge theo `STATUSES`: Hoàn thành success · Đang xử lý danger · Chờ xử lý danger · Đang tạo secondary) · Hành động (⚙ dropdown: **In**).
- Bộ lọc (:51-61): Số yêu cầu (text) · Tên hàng (text) · Model (select-ajax) · Người tạo (select-ajax) · Từ ngày–Đến ngày; khi `type=all` thêm Công ty / Phòng ban theo 3 quyền phạm vi.
- `type` (Model :69-107):
  - `all` — phạm vi: **Xem YC duyệt hàng tạm theo tổng công ty** (tất cả) > **…theo công ty** (company_id mình) > **…theo phòng ban** (phòng mình quản lý) > còn lại của mình; kèm điều kiện whereHas rối (:88-98).
  - `approve` + quyền **Duyệt hàng tạm** — phiếu thuộc công ty mình (điều kiện `status != 1 OR status != 2` luôn đúng ⇒ thực tế = mọi phiếu có ≥1 HT).
  - trần / không đủ quyền — phiếu của mình.

### 2.5 M5 — Tạo yêu cầu duyệt hàng tạm (`create.blade.php` + `form.blade.php`)

- Card **Thông tin chung**: Ghi chú (input text).
- Card **Chi tiết**: bảng STT · Tên hàng hóa · Model · Thương hiệu · [➕ ở tiêu đề → mở **P1**; ➖ mỗi dòng bỏ khỏi bảng]. Rỗng: "Chưa có hàng hóa".
- Nút: **Gửi** · **Hủy** (về `?type=all`). Không có Lưu nháp.
- Luồng: mỗi lần Lưu P1 ⇒ HT được TẠO NGAY (status 2, notify người duyệt) rồi mới thêm dòng vào bảng (`formJs.blade.php:9-11`). Bấm ➖ chỉ bỏ dòng — **HT đã tạo vẫn tồn tại mồ côi** (không gắn phiếu). Bấm Hủy cũng vậy.
- Gửi (`store` :93-127): bắt `products` ≥1; tạo phiếu (code `PYCDHT-` + 5 số), gán `tmp_product_request_id` cho HT, notify quyền **Duyệt hàng tạm** "… vừa gửi yêu cầu duyệt hàng tạm **{code}**" (link M6). Toast `successResponse()` mặc định, về M4 `?type=all`. Không gate quyền ở route/controller.

### 2.6 M6 — Chi tiết yêu cầu duyệt hàng tạm (`show.blade.php`)

- Xem được: Super Admin · người tạo · quyền **Duyệt hàng tạm** (Model `canView` :163-168); không ⇒ view `not_found`.
- Ghi chú: sửa được + nút **Lưu ghi chú** chỉ khi phiếu **Đang tạo** (4) (:26-35); BE `updateNote` lặp lại điều kiện + ≤1000 ký tự; toast "Cập nhật ghi chú thành công!" / "Chỉ sửa được ghi chú khi phiếu ở trạng thái Đang tạo!".
- Bảng Chi tiết: STT · Tên hàng hóa (**link mở M2 tab mới chỉ khi HT status 2**) · Model · Thương hiệu · Trạng thái (Không duyệt / Đã duyệt / Đang chờ duyệt / Đang tạo) · Ghi chú duyệt. ⇒ người duyệt duyệt TỪNG HT ở M2, không duyệt cả phiếu.
- Nút: **Quay lại** (về `?type=all`). Không có nút In ở màn này (In chỉ ở dropdown M4).

### 2.7 M7 — In PYC

- Mẫu `ReportTemplate::YC_DUYET_HANG_TAM`, biến (`TmpProductRequest.php:212-224`): SO_PHIEU · LOGO · CONG_TY · DIA_CHI_CONG_TY · NGAY_LAP · NGUOI_LAP · PHONG_BAN · GHI_CHU · CHI_TIET (bảng STT · Tên hàng · Model · Thương hiệu · Trạng thái · Ghi chú duyệt, :226-264). Mở trang `print` riêng (không popup xem trước).

### 2.8 P1 — Popup "Thêm nhanh hàng hóa" (`partials/tmpProduct/createTmpProductForm.blade.php`)

- Modal toàn màn (`modal-dialog-full`), tiêu đề **"Thêm nhanh hàng hóa"** (:12), thân cuộn 85vh. Bố cục 9/3 giống M2 nhưng rút gọn:
  - Thông tin hàng hóa: ★Tính chất hàng hóa · **Ngày xóa hàng tạm** (date, BE `after:today`; chỉ có ở popup) · ★Model (+➕) · ★Loại hàng hóa (multi) · ★Tên hàng hóa · Tên tiếng Anh · Ghi chú · Bảo hành · Định mức công lắp đặt.
  - Thông số cơ bản ★: Trọng lượng · Kích thước · ★Nhóm hàng hóa · bảng Tên · Giá trị · Đơn vị · ☑.
  - Đặc điểm (CKEditor).
  - **Giá theo đơn vị**: tab đơn vị; ★Đơn vị cơ bản · ★Hệ số quy đổi · ★Giá vốn · Giá mua ngoài + **bảng giá theo loại giá** (Loại giá ★ · Hệ số · Giá công thức · Giá bán · Định mức đàm phán giá %) — BE bắt buộc ≥1 đơn vị, đúng 1 đơn vị cơ bản ("Chưa có đơn vị cơ bản!" / "Không thể chọn nhiều đơn vị cơ bản!"), mỗi đơn vị ≥1 giá.
  - Cột phải: ★Thương hiệu · ★Xuất xứ (+➕) · ★Hãng sản xuất · Code đặt hàng (+Thêm nhanh) · Nhà cung cấp · ★% VAT (+➕) · Ảnh (★đại diện / mô tả) · Video.
- Nút: **Lưu** · **Hủy** (:567-575).
- Lưu (`createTmpProductJs.blade.php:97-127` → `POST tmpProductStore`): route gate quyền **Thêm báo giá**; trùng tên+model ở `tmp_products` **hoặc** `products` ⇒ "Tên hàng hóa đã tồn tại trên hệ thống"; lỗi ⇒ toast "Tạo hàng hóa thất bại!" + lỗi từng ô. OK ⇒ HT status 2, notify Super Admin + quyền **Duyệt hàng tạm** "{người} vừa tạo sản phẩm tạm: **X**" (link M2) + Redis kênh `tmp_product`; đóng popup, toast "Tạo hàng hóa thành công!", gọi `tmpProductCallback` (thêm dòng vào chứng từ gọi).
- Nơi mở popup:

| Màn | Nút | Callback |
|---|---|---|
| Báo giá thường (`quotations/form.blade.php:182-183`, create/edit) | **➕ Hàng tạm** (đỏ, cạnh nút "Hàng hóa"; ẩn khi báo giá thanh lý) | `form.addTmpProduct()` (`quotations/formJs.blade.php:238`) |
| Tạo PYC (M5) | ➕ ở tiêu đề bảng Chi tiết | `form.addProduct()` |
| Báo giá dự án (`sale/project_quotations/form_template.blade.php:701`) · Báo giá firm (`sale/firm/quotations/formJs.blade.php:428`) | ⚠️ có markup popup / callback nhưng **không include JS và không có nút mở** ⇒ code chết | — |

### 2.9 P2 — Làm lại báo giá (`quotations/tmp_product_change.blade.php`)

- Lối vào: dropdown hành động danh sách báo giá "Làm lại báo giá" khi `has_tmp_product && !child` (`QuotationsController.php:154,199`, `Sale/QuotationAllController.php:130,170`); chỉ người tạo báo giá.
- Bảng Chi tiết: dòng HT chưa duyệt tô class `tmp-not-approved` + title "Hàng tạm chưa được duyệt"; đã duyệt `tmp-approved` + link "Chi tiết duyệt hàng tạm" → popup so sánh 2 dòng **Hàng tạm** vs **Hàng hóa** (Tên · Model · ĐVT · Đơn giá · Ảnh), ô khác nhau tô đỏ (:294-358).
- Lưu: còn HT chưa duyệt ⇒ swal "Lưu thất bại" / "Báo giá vẫn còn hàng tạm chưa được duyệt!" (:396-401).
- **Thuộc luồng Báo giá ERP**, không thuộc danh mục HT — liệt kê để biết phụ thuộc.

---

## 3. Lối vào

### 3.1 Menu ERP (`resources/views/layouts/topmenubar.blade.php`)

| Dòng | Vị trí | Nhãn → đích | Gate |
|---|---|---|---|
| 20 | **Danh mục › Hàng hóa › Quản lý hàng hóa** | Danh mục hàng tạm → M1 | không |
| 326 | **Khởi tạo › Hàng hóa › Hỏi hàng - đặt hàng - Khiếu nại** | Phiếu Yêu cầu duyệt hàng tạm → M4 `?type=all` | không |
| 1530 | **Mua hàng › Hàng tạm - Hỏi giá** | Phiếu yêu cầu duyệt hàng tạm → M4 `?type=approve` | Duyệt hàng tạm |
| 1532 | ↑ cùng nhóm | Danh sách hàng tạm → M1 | không |
| 2228-2229 | **Chờ duyệt › Hàng hóa - dịch vụ - vận chuyển › Duyệt hàng hoá** | Yêu cầu duyệt hàng tạm → M4 `?type=approve` · Danh sách hàng tạm → M1 | Duyệt hàng tạm |
| 2379 | **Chờ duyệt › Mua hàng** | Phiếu yêu cầu duyệt hàng tạm chờ duyệt → M4 `?type=approve` | Duyệt hàng tạm |
| 2381 | ↑ cùng nhóm | "Duyệt hàng tạm" → M4 **trần** (= phiếu của mình — nhãn sai nghĩa) | không |
| `topheader.blade.php:171` | Menu tài khoản | Hàng tạm của tôi → M3 | không |

### 3.2 Dashboard (`HomeController.php:549-575`)

- Ô **"Hàng tạm cần duyệt"** (nhóm `QUAN_LY_HANG_HOA`) → M1, số = HT status 2: quyền **Duyệt hàng tạm** ⇒ đếm tất cả; không ⇒ đếm theo cặp Thương hiệu–Hãng phụ trách. Ẩn khi 0. (Link về M1 nhưng M1 không tự lọc "Đang chờ duyệt".)

### 3.3 Thông báo

| Sự kiện | Người nhận | Nội dung | Link |
|---|---|---|---|
| Tạo HT (P1) `:492-520` | Super Admin + quyền Duyệt hàng tạm | "{A} vừa tạo sản phẩm tạm: **X**" | M2 |
| Gửi duyệt nháp / gửi lại `:877-883` | quyền Duyệt hàng tạm | "{A} vừa gửi duyệt hàng tạm **X**" | M2 |
| Gửi PYC `TmpProductRequest.php:171` | quyền Duyệt hàng tạm | "{A} vừa gửi yêu cầu duyệt hàng tạm **{code}**" | M6 |
| Duyệt `:662-671` | người tạo | "{A} vừa duyệt sản phẩm tạm: **X**" | `myTmpProductShow` ⚠️ trang chết |
| Không duyệt `:728-737` | người tạo | "{A} không duyệt sản phẩm tạm: **X**" | M2 |
| Xoá `:911-920` | người tạo | "{A} vừa xóa sản phẩm tạm: **X**" | `myTmpProductShow` ⚠️ trang chết |
| HRM sync tạo HT nháp (`Services/Sale/TmpProductRequestSyncService.php:71`) | — | **không bắn** | — |

### 3.4 Đường từ HRM (đã có)

- HRM **Dự án TKT › tab Báo giá**: banner "Đồng bộ hàng tạm sang ERP" + nút **Gửi duyệt hàng tạm** (confirm "Gửi duyệt hàng tạm của báo giá trúng thầu sang ERP?") và tự/bấm kéo kết quả (`hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue:3-39, 654-715`).
- BE HRM `Modules/Assign/Services/TmpProductSyncService.php` gọi ERP `POST /api/v1/tmp-product-requests/sync-from-hrm` (tạo PYC + HT status 3) và `/approved-status` (ERP `routes/api.php:74-77`). Người tạo phải **sang ERP M1** bấm "Sửa hàng tạm" để bổ sung rồi "Lưu và gửi duyệt".

---

## 4. So với HRM đã có

### 4.1 Khuôn có sẵn trong hrm-client

| Thứ | Ở đâu | Dùng cho HT? |
|---|---|---|
| Form hàng hoá 2 tab cha × 5 tab bước (Thông tin chung · Thông số kỹ thuật · Mua hàng · Phân loại xe · Nhóm máy + **Quản trị hàng hoá**) | `components/product/form/ProductForm.vue` (+12 component con), API `master-data/products` | ✅ **Nền chính cho M2**: trường của HT ≈ trường hàng hoá ERP; nên dùng lại bằng prop (vd `entity="tmp"` / `api-base`) thay vì chép |
| Màn chi tiết chỉ đọc 5 tab | `components/product/detail/ProductTab*.vue`, `pages/master-data/products/_id/index.vue` | ✅ cho M2 khi không có quyền sửa/duyệt (thay "form mở mà không lưu được" của ERP) và cho M3b |
| Danh sách hàng hoá 4 màn dùng chung | `components/product/ProductListPage.vue` + `utils/product-list-screens.js` | ◐ khuôn bảng/bộ lọc/cấu hình cột cho M1, M3 — cột khác (Trạng thái duyệt, Người tạo, Người duyệt, Ghi chú duyệt) |
| Khuôn phiếu yêu cầu + danh sách theo phạm vi | `pages/sale/price-asking-requests`, `price-calculate-requests` | ✅ cho M4/M5/M6 (bảng dòng hàng + chọn hàng, phân phạm vi tổng công ty/công ty/phòng) |
| Popup chọn hàng có "Thêm hàng tạm" | `pages/assign/quotations/components/QuotationProductSearchModal.vue` (overlay 2 tab) | ⚠️ đây là **hàng tạm DỰ ÁN của HRM** (dòng báo giá `erp_product_id` null), KHÁC `tmp_products` ERP — xem F2 |
| In popup xem trước | skill `print-page` (`ReportPrintPreviewModal`) | ✅ cho M7 |
| Menu | `components/subsystem-menu/sale-hub.js:164` đã có mục trần **'YC duyệt hàng tạm'** (xám); `master-data.js:62-86` nhóm "Hàng hoá" (chưa có mục HT); `menu-sidebar.js:34-35` "Danh sách hàng tạm" = `/assign/product-project` (**hàng tạm dự án** — trùng tên) | gắn link vào đúng các mục này |

### 4.2 Phải dựng mới / lệch khuôn

1. **Trạng thái duyệt + khối duyệt** (Ghi chú duyệt bắt buộc khi Không duyệt, Duyệt / Không duyệt / Lưu / Lưu và gửi duyệt / Gửi duyệt lại) — ProductForm hiện chỉ có 1 nút Lưu (G3). Cần footer theo trạng thái + quyền.
2. **Giá theo đơn vị**: form hàng hoá HRM **không còn giá** (ProductFormUnitsTable chỉ Đơn vị · Đơn vị cơ bản · Hệ số · Quy đổi; giá đã tách sang `finance/product-prices` theo công ty). HT ERP lại bắt buộc Giá vốn + giá theo loại giá khi tạo, và có card "Hệ số giá theo công ty" ⇒ F3.
3. **Phân loại**: HT ERP dùng `product_type` (Tính chất) + `product_cate` + `group_id` (Nhóm hàng → thuộc tính). HRM đã đổi sang cây mới Tính chất → Nhóm chức năng → Nhóm SP → Loại SP (Redmine #11421) ⇒ form HT phải theo cây mới, kéo theo khi duyệt tạo hàng hoá đúng chuẩn HRM ⇒ F4.
4. **Phạm vi theo phụ trách Thương hiệu–Hãng** (`AssignHistory`) — chưa có ở các màn hàng hoá HRM.
5. **Popup tạo HT gọn** (P1) — chưa có bản tương ứng; quyết định có cần không ⇒ F5.
6. **Các màn chứng từ ERP còn gọi P1** (Báo giá thường) — nếu ERP chỉ-đọc sau Phase 6 thì nút "Hàng tạm" ở báo giá ERP phải đi đâu ⇒ F6.

---

## 5. Câu tồn giao diện

| # | Câu hỏi | Đề xuất |
|---|---|---|
| F1 | M2 ERP gộp xem / sửa nháp / duyệt vào 1 form luôn mở. HRM tách **chi tiết chỉ đọc** (`/{id}`) + **form** (`/{id}/edit`) như hàng hoá? | Tách. Chi tiết có nút theo trạng thái: Sửa (người tạo, 3/0) · Duyệt / Không duyệt (người duyệt, 2) · Xoá. Duyệt mở form edit ở chế độ duyệt vì người duyệt hay sửa trước khi duyệt (ERP ghi đè dữ liệu người duyệt) |
| F2 | Đặt tên: HRM đã có "Danh sách hàng tạm" = hàng tạm DỰ ÁN (`/assign/product-project`). Danh mục `tmp_products` gọi là gì để không nhầm? | "Danh mục hàng tạm" (master-data) cho `tmp_products`; đề nghị đổi nhãn mục dự án thành "Hàng tạm dự án" (cần user chốt vì nhãn là menuKey) |
| F3 | Giá trên HT: giữ Giá vốn + giá theo loại giá (bắt buộc như ERP) hay bỏ, để khi duyệt hàng sinh ra đi luồng Tính giá / Cập nhật giá theo công ty? | Bỏ giá khỏi form HT (đồng bộ form hàng hoá HRM); khi duyệt hàng tạo ở trạng thái chưa có giá ⇒ đi luồng giá. Nếu nghiệp vụ cần "giá dự kiến" để báo giá: giữ 1 ô Giá dự kiến chỉ để tham khảo (HRM sync đã gửi `estimated_price`/`quoted_price`) |
| F4 | Form HT theo cây phân loại MỚI của HRM (Loại SP → thuộc tính) hay giữ Nhóm hàng cũ? | Theo cây mới — HT duyệt xong là hàng hoá HRM, dùng cùng `ProductForm` |
| F5 | Có cần popup **"Thêm nhanh hàng tạm"** riêng (P1) ở HRM không, hay tạo HT = mở màn form đầy đủ? | Chỉ cần nếu có chứng từ HRM gọi (xem F6). Nếu cần: popup dùng tab "Thông tin chung" của ProductForm + ô bắt buộc tối thiểu |
| F6 | Lối tạo HT: (a) Báo giá thường ERP nút "➕ Hàng tạm", (b) Tạo PYC M5, (c) HRM dự án sync. Sau Phase 6 giữ lối nào? Báo giá ERP còn tạo HT được không (ERP chỉ-đọc)? | Giữ (c) + thêm nút **Thêm mới** ở danh mục HT HRM; (a) tạm trỏ sang HRM hoặc khoá — cần chốt cùng người quản luồng báo giá |
| F7 | PYC (M4–M7) còn cần không? Thực tế duyệt theo TỪNG HT, phiếu chỉ là nhóm + in; trạng thái phiếu tính từ con | Giữ PYC chỉ làm "gói gửi duyệt" (sync HRM đang tạo PYC); màn chi tiết PYC cho duyệt/không duyệt từng dòng ngay trong bảng để khỏi nhảy tab |
| F8 | Danh sách HT: giữ "Hàng tạm của tôi" thành màn riêng hay là tab/bộ lọc "Của tôi" trên M1? | Gộp: M1 có ô lọc nhanh "Của tôi / Chờ tôi duyệt / Tất cả"; menu tài khoản trỏ M1 `?mine=1` |
| F9 | Trạng thái & màu: ERP "Đang tạo" màu đỏ ở M1 nhưng xám ở M3; HT đã xoá (-1) vẫn hiện | Badge HRM: Đang tạo xám · Chờ duyệt cam · Đã duyệt xanh · Không duyệt đỏ; ẩn -1 |
| F10 | Xoá: ERP xoá không hỏi xác nhận, chỉ người duyệt xoá được HT Chờ duyệt; người tạo không tự xoá được nháp | Có hộp xác nhận; cho người tạo xoá HT Đang tạo/Không duyệt của mình (cần chốt nghiệp vụ) |
| F11 | Dashboard "Hàng tạm cần duyệt" + thông báo: link HRM nào? (2 thông báo ERP đang trỏ trang chết) | Link chi tiết HT HRM; dashboard → M1 lọc sẵn "Chờ tôi duyệt" |
| F12 | Xuất CSV/Excel/PDF ở M1 (xuất toàn bảng không lọc) — có giữ? | Chỉ giữ Xuất Excel theo bộ lọc (skill export-excel) |
| F13 | Phạm vi xem theo phụ trách Thương hiệu–Hãng (`AssignHistory`) + quyền "Xem danh sách hàng tạm" / "Duyệt hàng tạm" — giữ nguyên? Có cần lọc theo công ty không (ERP không lọc)? | Giữ nguyên logic quyền; hỏi thêm về lọc công ty |
| F14 | Màn "Làm lại báo giá" (P2) ở ERP phụ thuộc HT đã duyệt có `product_id` — phạm vi Phase 6 hay luồng báo giá? | Ngoài phạm vi Phase 6; chỉ cần đảm bảo HT duyệt ở HRM vẫn ghi `tmp_product_id` vào hàng hoá như ERP |

---

## 6. Lỗi ERP thấy khi đọc (ghi lại, không vá)

1. `show` của cả 2 controller trả chuỗi "Đang phát triển"; thông báo Duyệt / Xoá + nút ℹ ở M3 trỏ vào đó.
2. M3 vẽ bộ lọc nhưng BE không lọc; thiếu lựa chọn "Đang tạo".
3. Xoá HT không hỏi xác nhận; HT status -1 vẫn hiện ở M1/M3.
4. `reject` không kiểm `canApprove()` (chỉ kiểm status = 2).
5. M5: HT tạo ngay khi Lưu popup — bỏ dòng / Huỷ phiếu để lại HT mồ côi đã notify người duyệt.
6. `searchByFilter` type=approve: điều kiện `status != 1 OR status != 2` luôn đúng.
7. Menu "Chờ duyệt › Mua hàng › Duyệt hàng tạm" (`topmenubar:2381`) trỏ M4 trần = phiếu của mình.
8. Báo giá dự án / firm include markup P1 nhưng không có nút mở + không include JS.
9. Export PDF dùng view `products.pdf` + host cứng `http://localhost:8000`; Export Excel/CSV gọi `$product->employee` (không tìm thấy quan hệ `employee()` trong `TmpProduct`/`BaseProduct`/`BaseModel` ⇒ nhiều khả năng lỗi khi xuất) và xuất cả HT đã xoá.
