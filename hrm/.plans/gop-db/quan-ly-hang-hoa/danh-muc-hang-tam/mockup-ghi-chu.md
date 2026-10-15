# Ghi chú mockup Phase 6 — Hàng tạm (12/10/2026)

> File: `mockup-hang-tam.html` (tự chứa, chỉ gọi CDN Roboto + Remix Icon 4.3.0). Thanh tab đầu trang chuyển M1–M5; công tắc "Đánh dấu phần MỚI": khung **cam** = phần mới, khung **đỏ** = cần chốt.
> Style **đo bằng getComputedStyle** trên app thật `127.0.0.1:3031` (worktree `wt-chuyen-doi-hang-hoa`): `/sale/price-asking-requests/4280` + `/add` (form YCHG, popup Chọn hàng hoá), `/master-data/products/company` + `/entering` (khuôn danh sách), `/master-data/products/create` (form hàng hoá, lỗi, toast). CSS overlay "Thêm hàng tạm" lấy từ `<style scoped>` của `QuotationProductSearchModal.vue` (mở popup thật cần báo giá đang sửa).
> Kiểm bằng Playwright ở 1440×900 và 1280×800: 0 lỗi console; footer không đè khối cuối; trang không cuộn ngang; mọi hàng form popup đủ 12 cột (100%); tiêu đề cột 1 dòng.
> ⛔ Mockup là tài liệu, không phải lệnh code.

## M1 — Form YCHG (sửa phiếu)

| Phần | Tái dùng (nguồn) | Mới |
|---|---|---|
| Khung trang, Thông tin chung, bảng gom nhóm La Mã, footer Lưu nháp / Lưu và gửi duyệt | `components/sale/price-asking/PriceAskingRequestForm.vue` | — |
| Nút **Thêm hàng tạm** (secondary, đứng trái "Chọn hàng hoá", cách 12px) | khuôn nút "Chọn hàng hoá" | ✔ mở popup M2 chế độ YCHG |
| Badge **Hàng tạm** ở cột Trạng thái hàng | `V2BaseBadge` + `company_status_color` | ✔ `ProductCompany::STATUS_TEMP = 6`, màu `#6D5A9E` |
| Dòng phụ "Lập từ HHB…/HHBG…" dưới tên hàng | khuôn `asking-note` | ✔ chỉ khi hàng tạm sinh từ dòng BOM/báo giá |
| Icon **Sửa hàng tạm** ở cột Hành động | `V2BaseIconButton` | ✔ mở popup M2 chế độ sửa |
| Icon Bỏ khỏi phiếu | có sẵn | tooltip riêng cho hàng tạm: "hàng tạm vẫn giữ ở màn Hàng tạm" |

## M2 — Popup "Thêm hàng tạm"

| Phần | Tái dùng (nguồn) | Mới (chỉ chế độ YCHG) |
|---|---|---|
| Khung overlay, 2 tab, ô tìm, bảng tái sử dụng, Lưu / Lưu và tiếp tục / Đóng, nút ⊕ thêm nhanh Model/Thương hiệu/Xuất xứ | `pages/assign/quotations/components/QuotationProductSearchModal.vue` (:247-420) | prop chế độ, mặc định = hành vi cũ (R2) |
| Tab Tái sử dụng | bảng có sẵn (endpoint `reuseChildren` `only_temp`) | chọn **1 dòng (radio)** + nút **Dùng hàng này** ⇒ sang tab nhập, điền sẵn Tên, ĐVT, Thương hiệu, Xuất xứ, Model, TSKT + dải báo nguồn có "Bỏ điền sẵn"; thêm cột **Dự án** |
| Model | có sẵn (không bắt buộc) | **bắt buộc** |
| Hãng sản xuất 3 · % VAT 3 · Loại sản phẩm 3 · **Đặc tính** 3 / **Tính chất 4 · Nhóm chức năng 4 · Nhóm sản phẩm 4** (3 ô cây chỉ đọc, tự suy từ Loại SP) | nhãn/luật từ `components/product/form/ProductFormGeneral.vue`, `ProductFormPurchase.vue` | ✔ tất cả bắt buộc (nhóm Phân loại đủ 5 ô — xem chốt 12/10 tối); chọn Loại SP tự điền % VAT khi ô trống (luật C10) và xoá lỗi 3 ô cây |
| ~~Tiểu mục catalog kinh doanh~~ | `admin.job_cluster_ids` | **đã bỏ** (chốt Q1: nới luật cho hàng tạm) |
| Số lượng cần dùng | có sẵn | ẩn ở YCHG (YCHG không có số lượng) ⇒ Ghi chú giãn 12 cột |
| Báo lỗi | `V2BaseError` + toast "Vui lòng kiểm tra lại dữ liệu nhập" | Lưu khi trống ⇒ **12 ô đỏ cùng lúc** (BOM giữ 4 ô: Tên, ĐVT, Thương hiệu, Xuất xứ), cuộn tới ô lỗi đầu; lỗi trùng "Đã có hàng hoá cùng Tên, Model, Thương hiệu và Hãng sản xuất." (`checkUniqueName`) |

Danh sách bắt buộc lấy từ `Modules/MasterData/Http/Requests/Product/ProductRequest.php`: `name`, `model_id`, `brand_id`, `manufacture_id`, `origin_id`, `product_type_id`, `vat_percent_tax_rate_id`, `units` (≥1, đúng 1 ĐVT cơ bản ⇒ ĐVT popup thành ĐVT cơ bản hệ số 1) (bỏ `admin.job_cluster_ids` cho hàng tạm — chốt Q1). Popup cũ chỉ bắt Tên, ĐVT, Thương hiệu, Xuất xứ (+ Nhóm hàng ở BOM).

## M3 — Màn "Hàng tạm" (Danh mục dùng chung › Hàng hoá, mục thứ 5 sau "Hàng đang kinh doanh")

| Phần | Tái dùng (nguồn) | Mới |
|---|---|---|
| Bộ lọc, bảng cột ghim, phân trang, nút "Lập yêu cầu hỏi giá" + tick dòng | `components/product/ProductListPage.vue` + `utils/product-list-screens.js` (màn `entering`) | cấu hình màn `temporary`, lọc `pcc.status IN (6, 7, 8)` công ty đang làm việc |
| Cột **YCHG đang chứa** (mã link + badge trạng thái phiếu), **Người tạo** | — | ✔; ô lọc nâng cao "Yêu cầu hỏi giá" (đang nằm / chưa thuộc) |
| Cột **Trạng thái** (Hàng tạm / Hàng tạm đã duyệt / Hàng tạm không duyệt) + **Lý do không duyệt** | — | ✔ (dựng lại cột Trạng thái vì nay có 3 trạng thái) |
| Hàng 8: phiếu không còn giữ hàng ⇒ Xoá / Lập YCHG khác được; sale **Sửa** ⇒ hàng về 6 (toast báo "chờ PTKD duyệt lại") | — | ✔ |
| Hành động dòng: Sửa · Lập YCHG · Xoá (icon trực tiếp, Xoá kiểu danger + hộp xác nhận) | `v2-row-actions` của 4 màn hàng hoá, `utils/productLifecycle.js` | ✔ điều kiện §4.3; tick bị khoá với hàng đang trong YCHG mở |

## M4 — PTKD duyệt YCHG có hàng tạm (bản 12/10 chiều — duyệt TỪNG hàng tạm rồi mới duyệt phiếu)

Trạng thái hàng tạm theo công ty (`pcc.status`): **6 Hàng tạm** (`#6D5A9E`, chưa xử lý) · **7 Hàng tạm đã duyệt** (`#7C3AED`) · **8 Hàng tạm không duyệt** (`#DC2626`) · 2 Chờ tính giá bán. Mọi chỗ ẩn status 6 (§4.4) ẩn luôn 7 và 8.

| Phần | Tái dùng | Mới |
|---|---|---|
| Chi tiết YCHG, footer Duyệt / Từ chối phiếu, popup lý do | `PriceAskingRequestForm.vue`, `PriceAskingReasonModal.vue` | — |
| Cột Hành động (PTKD, phiếu Chờ PTKD duyệt, có hàng tạm): hàng 6 ⇒ nút có nhãn **Duyệt** (primary, `ri-check-line` — button-convention: Duyệt = teal, chỉ điều hướng nên không hỏi xác nhận); hàng 7/8 ⇒ nút **Sửa** (secondary) mở lại form | — | ✔ thay icon sửa cũ (`edit-temp-full`) |
| Dòng hàng 8: chữ mờ + gạch tên, dòng đỏ "Không đi tiếp — lý do: …"; vẫn nằm trong phiếu, vẫn tính vào nhóm | — | ✔ |
| Nút **Duyệt phiếu** `disabled` khi còn hàng 6, tooltip "Còn N hàng tạm chưa duyệt"; hết hàng 6 ⇒ mở (kể cả khi có hàng 8) | — | ✔ |
| Duyệt phiếu ⇒ 7 → Chờ tính giá bán, 8 giữ 8 (nhóm toàn hàng 8 ghi "không gửi XNK"); Từ chối phiếu ⇒ 7 về 6, 8 giữ 8. Phụ đề 2 popup nêu đúng hệ quả này | — | ✔ |
| **Form duyệt hàng tạm** (trang `…/price-asking-requests/{id}/temp-products/{pid}/approve`, tiêu đề "Duyệt hàng tạm: mã") | khuôn `components/product/form/ProductForm.vue` + 5 component bước (`ProductFormGeneral/Specs/Purchase/Vehicles/Machines`), đo ở `/master-data/products/create`: tab cha kiểu segmented, thanh bước số tròn, chấm đỏ ở bước có lỗi | ✔ 2 tab cha **Thông tin hàng hoá** + **Quản trị hàng hoá** (thêm tab Quản trị theo chốt 12/10 khuya — xem cuối file); đầu form: mã + badge trạng thái + "thuộc YCHG PYCHG-04288" + người lập; trường điền sẵn từ hàng tạm |
| Bước "Phân loại xe" | luật G11 của form thật | chỉ hiện khi Loại SP là phụ tùng ô tô (thử: chọn "Phụ tùng ô tô – lọc dầu") ⇒ form thường 4 bước, hàng phụ tùng ô tô 5 bước |
| Footer form: **Lưu** (secondary, lưu giữ trạng thái) · **Đồng ý** (primary ⇒ validate đủ bắt buộc, báo lỗi đồng thời mọi ô + mở bước lỗi đầu ⇒ hộp xác nhận ⇒ 7) · **Không duyệt** (danger ⇒ hộp nhập **lý do bắt buộc** ⇒ 8) · **Hủy** (tertiary, về phiếu) | `V2Footer`, `PriceAskingReasonModal` | ✔ |

Bắt buộc khi Đồng ý (= `ProductRequest` trừ khối admin, **cộng đủ nhóm Phân loại**): Tên, Model, Loại sản phẩm, Đặc tính, Tính chất, Nhóm chức năng, Nhóm sản phẩm, Thương hiệu, Xuất xứ, Hãng sản xuất (bước 1), ĐVT cơ bản (bảng Đơn vị tính), % VAT (bước 3).
Quyền form duyệt: người có quyền **PTKD duyệt YCHG (1662)** của **công ty phiếu** — không cần 1652 (thay chốt Q3 cũ). BE kiểm thêm: hàng còn thuộc phiếu, phiếu đang Chờ PTKD duyệt, hàng đang 6/7/8.

## M5 — Trang báo ERP

Bản sao `wt-erp-2d1/resources/views/errors/moved_to_hrm.blade.php` (HTTP 403, Bootstrap 4.0 beta: `.btn-primary #007bff`). Chỉ thêm 1 nhánh câu mô tả + khoá đích `tmp-products` ⇒ `/master-data/products/temporary` trong `ProductMovedToHrm::TARGETS`. Bảng route bị chặn nằm dưới hộp (ghi chú mockup).

## Điểm thuần UI tự chốt (đã sửa luôn trong mockup)

1. Màu "Hàng tạm" `#6D5A9E` (xám tím): tách hẳn khỏi xám `#64748B` (Đang nhập thông tin) và xanh `#2563EB` (Đang tính giá); badge dùng rgba(màu,.1) như mọi trạng thái.
2. Tái sử dụng ở YCHG chọn 1 dòng + "Dùng hàng này" thay vì tick nhiều + "Thêm N hàng hoá": mỗi hàng tạm YCHG còn phải nhập thêm 4–5 ô nên không thêm hàng loạt được.
3. Nhóm trường mới không có khung/tiêu đề riêng (giao diện phẳng); xếp Hãng SX 3 · Loại SP 6 · % VAT 3 = 12 cột.
4. Badge nguồn BOM/Báo giá dùng V2 badge 2 màu thay badge bootstrap (`badge-primary`/`badge-success` thật cùng ra `#1abc9c`, không phân biệt được).
5. Màn Hàng tạm bỏ cột Trạng thái (mọi dòng đều "Hàng tạm"; duyệt xong hàng rời màn).
6. Nút Thêm hàng tạm đặt TRÁI nút "Chọn hàng hoá", cùng kiểu secondary.

## Câu hỏi nghiệp vụ còn tồn

| # | Câu | Đề xuất ⭐ |
|---|---|---|
| Q1 | `admin.job_cluster_ids` (Tiểu mục catalog kinh doanh) là bắt buộc của đường tạo hàng 2-C1 nhưng thuộc tab **Quản trị**, không phải *Thông tin hàng hoá*. Sale có phải chọn khi lập hàng tạm? | ⭐ Có, như mockup (giữ 1 đường ghi 2-C1, không nới luật). Phương án B: nới cho status 6, PTKD chọn lúc duyệt |
| Q2 | Thiết kế ghi "PTKD duyệt **nhóm**", nhưng app hiện tại PTKD duyệt **cả phiếu** (footer), XNK mới duyệt từng nhóm. Hàng tạm sang mã 2 lúc PTKD duyệt phiếu? | ⭐ Có — mockup M4 làm theo cách này |
| Q3 | PTKD sửa hàng tạm: popup gọn (như mockup) hay mở form hàng hoá đầy đủ (§4.2)? Form đầy đủ cần quyền 1652 + đúng công ty chủ hàng ⇒ PTKD thiếu quyền sẽ 403 | ⭐ Popup gọn, dùng chung với người lập |
| Q4 | Phiếu **Không duyệt** có tính là "YCHG đang mở" không? (quyết định Xoá / Lập YCHG có bị chặn) | ⭐ Không — phiếu Không duyệt thì hàng tạm được Xoá / Lập YCHG khác (D4); mockup làm vậy |
| Q5 | Ai được **Xoá** hàng tạm: người tạo hay chỉ quyền 1652 (như 2-C4)? | ⭐ Như Sửa: người tạo hoặc 1652 |


## Chốt 12/10 (user) — đã sửa mockup
- Q1 ⇒ **Không** chọn Tiểu mục khi lập hàng tạm (nới luật cho status 6; 1655 xếp catalog sau) — đã bỏ ô Tiểu mục khỏi popup M2.
- Q2 ⇒ PTKD duyệt **phiếu** (Phase 7 Q19) — M4 đã đúng.
- ~~Q3 ⇒ PTKD sửa bằng form hàng hoá đầy đủ (cần 1652)~~ — **thay bởi chốt 12/10 chiều** bên dưới.
- Q4 ⇒ phiếu Không duyệt KHÔNG tính là đang mở — M3 đã đúng.
- Q5 ⇒ Xoá: người tạo hoặc 1652 — M3 đã đúng.

## Chốt 12/10 chiều (user) — đã sửa mockup M3, M4
- PTKD **duyệt từng hàng tạm** trong phiếu bằng **form duyệt hàng tạm** (khuôn form tạo hàng hoá, không tab Quản trị / Tiểu mục): **Đồng ý** ⇒ 7 Hàng tạm đã duyệt · **Không duyệt** (lý do bắt buộc) ⇒ 8 Hàng tạm không duyệt · Lưu giữ trạng thái.
- Hàng 8 vẫn nằm trong phiếu (không đi tiếp); Duyệt phiếu chỉ khoá khi còn hàng 6. Duyệt phiếu: 7 ⇒ 2, 8 giữ. Không duyệt phiếu: 7 ⇒ 6, 8 giữ.
- Quyền form duyệt: 1662 (PTKD duyệt YCHG) của công ty phiếu.
- M3: hiện cả 7 và 8 (cột Trạng thái + Lý do không duyệt); sale sửa hàng 8 ⇒ về 6; hàng 8 Xoá / Lập YCHG khác được.

### Điểm tự chốt thêm (UI)
- Màu 7 = `#7C3AED` (cùng họ tím với 6 ⇒ vẫn đọc là "hàng tạm", đậm hơn = đã duyệt); 8 = `#DC2626` nền rgba(.1) như mọi trạng thái đỏ.
- Thứ tự nút footer form theo button-convention §5 (Lưu nháp-kiểu-Lưu đứng đầu, Hủy luôn cuối): **Lưu · Đồng ý · Không duyệt · Hủy** — khác thứ tự user liệt kê ([Hủy][Lưu][Không duyệt][Đồng ý]); đổi lại được nếu user muốn đúng thứ tự đó.
- Nhãn "Đồng ý" / "Không duyệt" theo đúng chữ user (skill khuyên "Duyệt" / "Từ chối"; giữ chữ user để phân biệt với nút Duyệt / Từ chối **phiếu**).
- Đồng ý có hộp xác nhận (button-convention §6c: mọi bước duyệt phải hỏi); nút "Duyệt" ở dòng chỉ điều hướng nên không hỏi.
- Thanh mockup M4: 5 trạng thái xem (Trước duyệt · Đã duyệt hết hàng tạm · Có hàng tạm bị không duyệt · Đã duyệt phiếu · Không duyệt phiếu) + trong form có nút "Xoá trống 5 ô bắt buộc (thử báo lỗi)".

### Kiểm Playwright (1440×900, 1280×800)
Console 0 lỗi, không cuộn ngang. Nút Duyệt phiếu `disabled=true` ("Còn 2…" ⇒ "Còn 1…") khi còn hàng 6, `false` ở "Đã duyệt hết" và "Có hàng không duyệt". Form: Đồng ý khi xoá trống ⇒ 5 ô lỗi + chấm đỏ ở 2 bước; hộp lý do để trống ⇒ 1 lỗi. Duyệt phiếu ⇒ "Đang hỏi giá", hàng 8 vẫn 8. Footer không đè khối cuối; hàng form đủ 12 cột.

## Chốt 12/10 tối (user) — nhóm Phân loại bắt buộc toàn bộ cho hàng tạm
- Ở **popup M2 chế độ YCHG** và **form duyệt hàng tạm M4**: Tính chất · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · Đặc tính đều có `*`.
- 3 ô cây (Tính chất / Nhóm chức năng / Nhóm sản phẩm) vẫn **tự suy từ Loại SP** như form thật (ô chỉ đọc); chưa chọn Loại SP ⇒ báo "Chưa có tính chất / nhóm chức năng / nhóm sản phẩm — chọn Loại sản phẩm". Thực chất BE chỉ cần kiểm Loại SP có đủ đường cây (Loại SP thiếu cha ⇒ chặn).
- ⚠️ **ĐIỂM MỚI của hàng tạm**: **Đặc tính** (`product_characteristic_id`) thành ô **bắt buộc** — form hàng hoá thật (`ProductRequest`) đang để `nullable`. Cần thêm rule riêng cho đường tạo/duyệt hàng tạm, không đổi form hàng hoá thường.
- Chế độ BOM / Báo giá của popup giữ nguyên (không có các ô này, vẫn 4 ô bắt buộc).
- Kiểm Playwright (1440×900, 1280×800, console 0 lỗi, không cuộn ngang): popup YCHG Lưu khi trống ⇒ **12** ô lỗi (gồm `type, charac, nature, fgroup, family`); chọn Loại SP ⇒ 3 ô cây tự điền + hết lỗi; BOM ⇒ 4. Form duyệt: "Xoá trống ô bắt buộc" + Đồng ý ⇒ **9** ô lỗi (`model, type, charac, nature, fgroup, family, manu, units, vat`); 5 nhãn Phân loại đều có `*`; footer không đè khối cuối.


- 12/10 (user): form hàng hoá THƯỜNG cũng sẽ bắt buộc Đặc tính — tạm bỏ vì dữ liệu cũ chưa có (việc sau, `viec-con-lai.md` A11).

## Chốt 12/10 khuya (user) — form duyệt hàng tạm có thêm tab cha "Quản trị hàng hoá"
- Chỉ ở **form duyệt M4** (PTKD nhập luôn lúc duyệt); popup sale M2 **không** có tab này.
- Bố cục + trường bám đúng `components/product/form/ProductFormAdmin.vue` + `ProductFormCatalogPicker.vue`: khối "Quản trị hàng hoá" — Nhà cung cấp 6 (ô tìm + chip gỡ được) · Chính sách kinh doanh 6 / Số lượng tồn kho tối thiểu 3 · Bảo hành 3 · Đơn vị bảo hành 3 (Ngày/Tháng/Năm, mặc định Tháng) · Hệ số công nghệ 3 (ⓘ "Dùng chung mọi công ty, chỉ công ty tạo sửa."); khối "Catalog kinh doanh" — 4 cột tick dây chuyền Lĩnh vực › Chương › Mục › Tiểu mục + bảng nhánh đã chọn (Gỡ). Đầu tab: dải "Dữ liệu của công ty <công ty phiếu>" (khuôn `product-scope-notice`).
- Bắt buộc: như form thật — tab Quản trị thật **không có ô bắt buộc nào ngoài Tiểu mục**; Tiểu mục **không bắt buộc** với hàng tạm (chốt Q1, hint "người có quyền Xây dựng catalog (1655) xếp sau"). ⇒ Lỗi ở tab Quản trị chỉ là lỗi **định dạng** của `ProductRequest::adminRules()`: tồn tối thiểu ≥ 0, bảo hành số nguyên 0–1000, hệ số công nghệ 0–1000.
- Đồng ý khi thiếu/sai ⇒ báo lỗi đồng thời cả 2 tab, chấm đỏ trên tab cha có lỗi (+ chấm trên bước), mở tab/bước lỗi đầu tiên; **Lưu** lưu cả 2 tab. Thanh bước (5 bước) chỉ hiện khi đang ở tab Thông tin, như form thật.
- Kiểm Playwright (1440×900, 1280×800, console 0 lỗi, không cuộn ngang, footer không đè khối cuối ở cả 2 tab): "Xoá trống ô bắt buộc + nhập sai 2 ô Quản trị" rồi Đồng ý ⇒ **11 ô lỗi** (9 tab Thông tin + 2 tab Quản trị), chấm đỏ ở cả 2 tab cha; tab Quản trị 0 dấu `*`, 4 cột catalog, tick dây chuyền ra 1 dòng bảng, thêm NCC ra chip; mọi hàng form đủ 12 cột.

