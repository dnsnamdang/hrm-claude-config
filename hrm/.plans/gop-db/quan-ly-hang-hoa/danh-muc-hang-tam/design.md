# Design Phase 6 — Hàng tạm (quản lý mới trên HRM) — 12/10/2026

> Nguồn: brainstorm với user 12/10/2026 (thay hẳn `ton.md` Q1–Q16 — bản "chép ERP" đã bị user gạt: *"quay lại brainstorm để lên phương án quản lý hàng tạm mới"*).
> Khảo sát: `khao-sat-be-erp.md` · `khao-sat-fe-erp.md` · `khao-sat-hrm.md`.
> 🔧 12/10 sửa: PTKD duyệt **cả phiếu** (không phải nhóm) — mockup phát hiện, khớp Phase 7 Q19.
> ✅ **Mockup `mockup-hang-tam.html` USER DUYỆT 12/10/2026** (kèm §8 + §9 A1–A13). ⛔ Chưa có "làm" — tài liệu này KHÔNG phải lệnh code. Tiếp: plan ⇒ xin "làm" kèm phạm vi.

## 1. Mục đích (user chốt)

Hàng tạm phục vụ 3 việc: **báo giá nhanh** món chưa có trong danh mục · **hỏi giá** · **bổ sung hàng vào danh mục kinh doanh**.
Sale có đủ các trường bắt buộc của phần *Thông tin hàng hoá* khi lập hàng tạm.

## 2. Quyết định đã chốt

| # | Quyết định | Thay cho ERP |
|---|---|---|
| D1 | **Không có bước duyệt hàng tạm riêng** — gộp vào YCHG: PTKD duyệt **phiếu** YCHG (Phase 7 Q19 — duyệt cả phiếu, không theo nhóm) = duyệt hàng tạm | ERP: người có "Duyệt hàng tạm" / phụ trách hãng duyệt từng hàng ⇒ tạo hàng + đặt giá + Đang kinh doanh ngay |
| D2 | **Phương án A**: hàng tạm = hàng hoá thật (`products` + bảng con) ngay khi lưu, trạng thái theo công ty **mới `6` "Hàng tạm"** ở `product_company_coefficients` (dòng của công ty lập YCHG). Không bảng hàng tạm riêng, không migration (cột `status` có sẵn) | ERP: bảng đệm `tmp_products` ⇒ duyệt chép sang `products` |
| D3 | **Mã chính thức sinh ngay khi lưu** (quy tắc §16); huỷ thì mã bỏ, không tái dùng | — |
| D4 | PTKD **không duyệt phiếu / nhóm bị huỷ** ⇒ hàng tạm **giữ status 6**, sale sửa rồi đưa vào YCHG khác; xoá khi không dùng = xoá cứng theo luật 2-C4 | ERP: status 0 Không duyệt, sửa gửi lại |
| D5 | **Ai cũng tạo được** hàng tạm (không quyền riêng — như lập YCHG) | ERP mượn "Thêm báo giá" |
| D6 | **Tái dùng popup có sẵn** `hrm-client/pages/assign/quotations/components/QuotationProductSearchModal.vue` (tab *Tái sử dụng* / *Thêm mới thủ công*), thêm **chế độ YCHG**: hiện + bắt buộc các trường *Thông tin hàng hoá* còn thiếu; BOM / Báo giá giữ nguyên hành vi | — |
| D7 | Dòng tạm BOM / báo giá (`bom_list_products` 74, `quotation_product_prices` 510 — `erp_product_id IS NULL`) **giữ là nháp dự án**; chỉ khi chọn vào YCHG mới sinh mã ⇒ gắn `erp_product_id` cho **mọi dòng cùng gốc** (dòng chọn + dòng báo giá trỏ qua `bom_list_product_id` + dòng cùng mã `HHB…`/`HHBG…`). Không backfill | — |
| D8 | **Màn mới "Hàng tạm"** ở Danh mục dùng chung › Hàng hoá; màn `/assign/product-project` giữ, đổi nhãn **"Hàng tạm dự án"** | ERP: Danh mục hàng tạm + Hàng tạm của tôi + Phiếu YC duyệt hàng tạm |
| D9 | **ERP**: chặn tạo/sửa/duyệt/từ chối/xoá hàng tạm + phiếu YC duyệt hàng tạm (khuôn T7, trang báo link HRM); giữ XEM dữ liệu cũ. **HRM**: gỡ nút "Gửi duyệt hàng tạm" (`TmpProductSyncService` → ERP `sync-from-hrm`) + đường INSERT thẳng `tmp_products` khi duyệt báo giá (`QuotationErpSyncService::createTmpProducts`) | — |
| D10 | Lỗi sẵn có ERP ở luồng hàng tạm (`reject`/`delete` không kiểm quyền, link "Đang phát triển"…): theo chốt chung 12/10 **sửa hết trước prod** — phần lớn tự hết vì route bị chặn; còn lại ghi `viec-con-lai.md` | — |

## 3. Dữ liệu

| Dữ liệu | Nơi lưu | Ghi chú |
|---|---|---|
| Thông tin chung | `products` + bảng con (ĐVT, thuộc tính, ảnh, NCC…) | ghi qua đường tạo hàng hoá HRM sẵn có (2-C1), không đường ghi mới |
| "Là hàng tạm" | `product_company_coefficients(product, công ty YCHG).status = 6` | `ProductCompany::STATUS_TEMP = 6`, nhãn "Hàng tạm", màu xám tím (chốt ở mockup). Công ty khác không có dòng |
| Thuộc YCHG nào | `price_asking_request_products.product_id` | sẵn có |
| Dòng BOM / báo giá đã thành mã nào | `bom_list_products.erp_product_id`, `quotation_product_prices.erp_product_id` | sẵn có |
| Giá | — | sinh ở PTG như mọi hàng (Phase 7) |
| ERP `tmp_products` / `tmp_product_requests` | giữ nguyên, chỉ xem | HRM không ghi thêm |

Vòng đời `pcc.status` của hàng tạm:
```
lưu từ popup chế độ YCHG ─► 6 Hàng tạm ──PTKD duyệt phiếu──► 2 Chờ tính giá ─► 5 Đang tính giá ─► 3 Đang kinh doanh
                               ▲   │ không duyệt phiếu / huỷ nhóm: giữ 6
                               └───┘ sửa ⇒ đưa vào YCHG khác          xoá (2-C4) khi chưa dính chứng từ khác
```

## 4. Luồng

### 4.1 Thêm hàng tạm vào YCHG (sale)
1. Form YCHG (T3, `/sale/price-asking-requests`) — nút **"Thêm hàng tạm"** cạnh chọn hàng ⇒ mở popup D6 chế độ YCHG.
2. Tab *Thêm mới thủ công*: nhập; tab *Tái sử dụng*: chọn dòng tạm BOM / báo giá trong các dự án người lập được xem ⇒ điền sẵn Tên, ĐVT, Thương hiệu, Xuất xứ, Model, TSKT ⇒ nhập nốt phần thiếu.
3. Lưu ⇒ BE (1 transaction): kiểm trùng (tên trong cùng model — cả hàng thật lẫn hàng tạm, như ERP) ⇒ tạo hàng hoá qua đường ghi 2-C1 ⇒ `pcc.status = 6` công ty YCHG ⇒ (nếu từ dòng tạm) gắn `erp_product_id` cho mọi dòng cùng gốc (D7) ⇒ trả `product_id`.
4. Dòng được thêm vào YCHG, gom nhóm Thương hiệu – Hãng như hàng thường (T3). Có thể thêm nhiều hàng tạm vào 1 YCHG.

### 4.2 PTKD duyệt
- Duyệt **phiếu** (T3 `PriceAskingRequestWriter::ptkdApprove`, Q19) ⇒ mọi hàng status 6 trong phiếu ⇒ 2 (cùng transaction) ⇒ XNK / YCTG / PTG / KQ không đổi.
- Trước khi duyệt, PTKD **sửa được** hàng tạm trong phiếu (mở form hàng hoá tab *Thông tin hàng hoá*) — người duyệt hay chỉnh như ERP.
- Không duyệt phiếu / nhóm bị huỷ ⇒ hàng tạm giữ 6.
- Chặn: không duyệt được phiếu nếu hàng tạm trong nhóm đã bị xoá / đổi công ty (kiểm lại ở BE).

### 4.3 Màn "Hàng tạm"
- Danh mục dùng chung › Hàng hoá (rail nhóm Hàng hoá, cạnh 4 màn 2-B). Tái dùng `ProductListPage`, lọc `pcc.status = 6` công ty đang làm việc.
- Cột như "Hàng hoá nhập thông tin" + **YCHG đang chứa** (mã, trạng thái nhóm) + Người tạo.
- Hành động: **Sửa** (người tạo hoặc 1652) · **Xoá** (xoá cứng theo 2-C4, chặn nếu đang nằm trong YCHG chưa đóng) · **Lập YCHG** (hàng chưa thuộc YCHG nào đang mở).
- Không quyền xem riêng (D5 — ai cũng tạo được); phạm vi theo công ty đang làm việc.

### 4.4 Ẩn status 6
Status 6 **không hiện / không chọn được** ở: Kho dữ liệu (và không "Lấy về") · Dữ liệu hàng hoá công ty · Hàng hoá nhập thông tin · Hàng đang kinh doanh · popup chọn hàng chứng từ HRM · popup ERP `SearchController` (rà như 2-D1 đã làm cho 1/2/4) · cron ERP 14:30. Chỉ hiện ở: YCHG, màn Hàng tạm, chi tiết hàng hoá (badge).

### 4.5 ERP + đường cũ
- ERP: `tmp_products` (store / edit / reject / delete / approve / draft) + `tmp_product_requests` (create / store / updateNote) ⇒ `productMovedToHrm` đích mới; danh sách / show / print / export giữ xem. Menu + thẻ dashboard "Hàng tạm cần duyệt" ⇒ HRM màn Hàng tạm. Nút "➕ Hàng tạm" ở báo giá ERP ⇒ trỏ HRM.
- HRM: gỡ banner "Gửi duyệt hàng tạm" (`ProspectiveProjectQuotationsTab.vue:3-27,654-689`) + route `api.php:678-679, 816-821` + `TmpProductSyncService`; gỡ `QuotationErpSyncService::createTmpProducts` (:105-129) khỏi luồng duyệt báo giá.
- Đổi nhãn menu `/assign/product-project` ⇒ "Hàng tạm dự án".

## 5. Kiểm thử
- PHPUnit: tạo hàng tạm (status 6, mã sinh, trùng tên chặn, gắn mọi dòng cùng gốc) · duyệt nhóm 6⇒2 · không duyệt giữ 6 · xoá chặn khi trong YCHG mở · ẩn status 6 ở 4 màn + Kho + lấy về · ERP route chặn.
- e2e (được cấp quyền tạm trên dev local): sale tạo hàng tạm trong YCHG (cả 2 tab) ⇒ PTKD duyệt ⇒ hàng sang Chờ tính giá; dòng BOM/báo giá đổi thành hàng thật; ca không quyền PTKD.
- Playwright đo DOM: popup chế độ YCHG đủ trường bắt buộc, báo lỗi đồng thời; BOM/Báo giá popup không đổi.

## 6. Ngoài phạm vi
Popup thêm nhanh ở báo giá ERP · port `checkDueConfigs` · sửa dữ liệu cũ `products.tmp_product_id` (bẩn 7.057/8.931) · màn "Làm lại báo giá" ERP · chuẩn hoá dòng tạm BOM/báo giá thành bảng chung.

## 7. Rủi ro
| # | Rủi ro | Giảm |
|---|---|---|
| R1 | Sót chỗ đọc `pcc.status` ⇒ hàng tạm lọt vào popup chứng từ / Kho | rà như Phase 7 (mã 5) + test 4 màn + ERP popup |
| R2 | Sửa popup dùng chung làm hỏng BOM / Báo giá | chế độ bằng prop, mặc định = hành vi cũ; e2e BOM/Báo giá chạy lại |
| R3 | Gắn mã cho "mọi dòng cùng gốc" bắt nhầm dòng khác trùng mã HHB do người dùng gõ tay | chỉ gắn dòng `erp_product_id IS NULL` + cùng mã sinh tự động; test |
| R4 | Mã chính thức bị "đốt" bởi hàng tạm huỷ | chấp nhận (D3) |

## 8. Chốt sau mockup (12/10/2026)

| # | Câu (mockup-ghi-chu Q1–Q5) | Chốt |
|---|---|---|
| M-Q1 | Tiểu mục catalog (bắt buộc ở đường tạo 2-C1, thuộc tab Quản trị) — sale có chọn khi lập hàng tạm? | **Không** — hàng tạm + cả luồng tính giá chạy khi chưa có catalog; người có 1655 xếp catalog sau (popup Xây dựng catalog). Luật tạo hàng **nới riêng cho status 6** (bỏ bắt buộc `admin.job_cluster_ids`); popup chế độ YCHG không có ô Tiểu mục |
| M-Q2 | PTKD duyệt nhóm hay phiếu? | **Phiếu** (Phase 7 Q19) — lỗi ghi spec, đã sửa D1/D4/§4.2 |
| M-Q3 | PTKD sửa hàng tạm bằng gì? | **Form hàng hoá đầy đủ** `/master-data/products/{id}/edit` — cần **1652** + đúng công ty; PTKD không có 1652 ⇒ KHÔNG hiện nút Sửa (không để 403). Runbook: nhắc cấp 1652 cho vai trò PTKD |
| M-Q4 | Phiếu Không duyệt có tính là "YCHG đang mở"? | **Không** — hàng tạm được Xoá / Lập YCHG khác ngay; chỉ chặn khi hàng đang trong YCHG Nháp / Chờ PTKD duyệt |
| M-Q5 | Ai được Xoá hàng tạm? | **Người tạo hoặc có 1652** (như Sửa ở màn Hàng tạm); xoá cứng luật 2-C4 |

Điểm UI tự chốt trong mockup (màu "Hàng tạm" `#6D5A9E`, tab Tái sử dụng chọn 1 dòng + "Dùng hàng này", ẩn "Số lượng cần dùng" ở chế độ YCHG, màn Hàng tạm bỏ cột Trạng thái, badge nguồn BOM/Báo giá 2 màu): giữ theo `mockup-ghi-chu.md`.

## 9. Chốt sau mockup lần 2 (12/10/2026) — DUYỆT TỪNG HÀNG TẠM

User: *"Thể hiện rõ button là duyệt, form duyệt kiêm cập nhật thêm thông tin phải tương đồng form tạo hàng hoá"* + chọn **"Duyệt hết hàng tạm mới duyệt được phiếu"**.

| # | Chốt | Ghi chú |
|---|---|---|
| A1 | Mỗi dòng hàng tạm trong YCHG chờ duyệt có nút **"Duyệt"** (có nhãn) ⇒ mở **form duyệt hàng tạm** bố cục như form tạo hàng hoá (tab *Thông tin hàng hoá* 5 tab bước, `ProductForm` chế độ duyệt hàng tạm; không tab Quản trị, không Tiểu mục). Footer: Hủy · Lưu · **Duyệt** (validate đủ, lỗi báo đồng thời) | thay M-Q3 (form đầy đủ qua 1652) |
| A2 | Trạng thái mới **7 "Hàng tạm đã duyệt"** ở `pcc.status` (không migration). Duyệt hàng: 6 ⇒ 7 | tự chốt dữ liệu — user đổi được |
| A3 | **Duyệt phiếu** khoá (disabled + tooltip "Còn N hàng tạm chưa duyệt") khi phiếu còn hàng 6; duyệt phiếu ⇒ mọi hàng 7 ⇒ 2 Chờ tính giá. **Không duyệt phiếu** ⇒ hàng 7 về 6 | BE kiểm lại điều kiện (không tin FE) |
| A4 | Quyền form duyệt + nút "Duyệt" = quyền **PTKD duyệt YCHG (1662)** trong công ty phiếu; không đòi 1652 | gắn với vai duyệt |
| A5 | Vòng đời cập nhật: `6 Hàng tạm ─Duyệt hàng─► 7 Đã duyệt ─Duyệt phiếu─► 2 ─► 5 ─► 3`; Không duyệt phiếu: 7 ⇒ 6; sale sửa hàng 7 ⇒ quay về 6 (phải duyệt lại) | |
| A6 | Ẩn status 6 **và 7** ở mọi nơi như §4.4 | |
| A7 | **"Duyệt" = Đồng ý hoặc Không duyệt** (user 12/10). Form duyệt: Hủy · Lưu · **Không duyệt** (lý do bắt buộc) · **Đồng ý** | |
| A8 | Không duyệt ⇒ status mới **8 "Hàng tạm không duyệt"**; lý do ghi `price_asking_request_approve_histories` (bảng log YCHG có sẵn). Hàng 8 **giữ trong phiếu nhưng không đi tiếp**; phiếu **vẫn duyệt được** với phần còn lại (user chọn) | tự chốt chỗ lưu lý do |
| A9 | Duyệt phiếu chỉ khoá khi còn hàng **6**. Duyệt phiếu: 7 ⇒ 2; 8 giữ 8 (không sang XNK / YCTG, loại khỏi nhóm khi lập YCTG). Không duyệt phiếu: 7 ⇒ 6, 8 giữ 8 | |
| A10 | Hàng 8 hiện ở màn Hàng tạm kèm lý do; sale Sửa ⇒ về 6; Xoá / Lập YCHG khác được | |
| A11 | Ẩn 6 / 7 / 8 ở mọi nơi như §4.4 | thay A6 |
| A12 | **Nhóm Phân loại bắt buộc toàn bộ** cho hàng tạm (popup chế độ YCHG + form duyệt): Tính chất · Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · **Đặc tính**. 3 cấp cây tự suy từ Loại SP (như form thật); Đặc tính hiện KHÔNG bắt buộc ở form hàng hoá ⇒ luật riêng cho đường hàng tạm (BE kiểm). User 12/10: form hàng hoá THƯỜNG cũng sẽ bắt buộc Đặc tính, **tạm bỏ vì dữ liệu cũ chưa có** ⇒ việc sau (xem `viec-con-lai.md` A11) | user 12/10 |
| A13 | Form duyệt hàng tạm có thêm tab cha **"Quản trị hàng hoá"** (user 12/10) — PTKD nhập dữ liệu quản trị của **công ty phiếu** ngay khi duyệt (Chính sách KD, Bảo hành + loại, Tồn tối thiểu, NCC, Catalog). Bắt buộc như tab Quản trị thật, **trừ Tiểu mục catalog không bắt buộc** (M-Q1). Ghi qua đường ghi tab Quản trị sẵn có (2-C2 `admin-data`), gate = 1662 công ty phiếu thay vì 1652. Popup sale không có tab này | tự chốt mức bắt buộc |

## 10. Chốt khi đối chiếu code (12/10/2026 — `diem-cham-code.md`)

| # | Chốt | Nguồn |
|---|---|---|
| C1 | **Xoá hàng tạm**: chưa từng vào YCHG ⇒ xoá cứng (luật 2-C4); đã từng vào YCHG ⇒ **xoá mềm** (`products.status = 0`, như hàng ERP đã xoá), ẩn mọi màn, phiếu cũ giữ dòng tra cứu | user |
| C2 | Hàng tạm đã qua PTKD (2) mà nhóm đóng (không giá / huỷ) ⇒ về **1 Đang nhập thông tin** như hàng thường (giữ luật Phase 7 `closeGroup`) | user |
| C3 | Báo giá trúng thầu có dòng hàng tạm: **lập hợp đồng ERP chỉ khi mọi dòng có mã VÀ mã Đang kinh doanh (3)** ở công ty; banner "Còn N hàng tạm chưa tính giá xong" + link YCHG | user |
| C4 | Lý do Không duyệt từng hàng: `price_asking_request_approve_histories` type `temp_reject`, `note` = "<mã hàng>: <lý do>" (bảng không có `product_id`, không migration) | tự chốt |
| C5 | Dấu vết "hàng sinh từ hàng tạm": log type `temp_created`, `note` = product_id, ghi khi tạo từ popup YCHG — dùng cho màn "Hàng tạm dự án" (giữ dòng BOM/báo giá đã gắn mã, `filterOutNativeErp` không ẩn) và báo cáo | tự chốt |
| C6 | Duyệt phiếu: nhóm mà mọi dòng đều 8 ⇒ đóng nhóm luôn (Huỷ duyệt, lý do "Mọi hàng tạm không được duyệt"), không gửi XNK | tự chốt |
| C7 | Tab Tái sử dụng chế độ YCHG: dòng tạm (`erp_product_id IS NULL`) của các dự án TKT **người lập được xem** (dùng phạm vi xem dự án hiện có của module Assign) | tự chốt |
| C8 | Không thêm quyền mới, không migration, không seeder. Form duyệt gate 1662 (công ty phiếu); tạo hàng tạm không gate quyền (D5) | D5, A4 |

## 11. Xác nhận sau khi làm (13/10/2026)

| # | Nội dung | User |
|---|---|---|
| X1 | PTKD đổi được quyết định Đồng ý ↔ Không duyệt (6/7/8) tới khi bấm Duyệt phiếu; thêm ⓘ giải thích ở 6 nút (Duyệt · Sửa · Duyệt phiếu · Lưu · Đồng ý · Không duyệt) | ✅ giữ như hiện tại + ⓘ (đã làm, client `dc793189e`) |
| X2 | Không đổi Thương hiệu/Hãng SX khi phiếu Chờ PTKD (PTKD: ô khoá; sale: 422). Phiếu Nháp đổi được (tự gom lại nhóm); hàng 8 đổi được. Sai hãng ⇒ PTKD Không duyệt hàng đó ⇒ sale sửa ⇒ đưa vào YCHG khác | ✅ giữ như hiện tại (không làm tự chuyển nhóm) |
| X3 | Câu banner chặn lập HĐ (C3): "Còn N hàng hoá chưa sẵn sàng kinh doanh (hàng tạm chưa tính giá xong / chưa lấy về)" | ✅ 13/10 |
