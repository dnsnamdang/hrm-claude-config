# Đợt 2-C — GHI hàng hoá: yêu cầu, quyền, tái sử dụng, tồn chặn

> 04/10/2026 · khảo sát chỉ đọc (tài liệu `.plans`, `git show`, đọc schema DB local `hrm_erp`, đọc code ERP `TanPhatDev`).
> **Chưa đụng source, chưa ghi DB.** Đây là đầu vào để lập `plan.md` của 2-C, không phải plan.
> Nguồn: sổ chốt `../SO-CHOT-VA-TON.md` · `../man-danh-muc-hang-hoa/design.md` (§16, §23c, §24, §26, §30g, §33, §35, §36) ·
> `../2b-doc/mockup-inventory.md` · mockup `../man-danh-muc-hang-hoa/mockup-luong-xay-dung-hang-hoa.html` ·
> `../2a-nen-csdl/khao-sat.md` (K1–K4) · `../2b-doc/khao-sat.md` + `plan.md` (Q1–Q4).
> Nhánh đích: con của `feat/chuyen-doi-hang-hoa` (api `40d3e9028`). ⛔ không merge `gop_db`.

---

## 0. Tóm tắt một màn hình

| Nhóm | Kết luận |
|---|---|
| Phạm vi 2-C (sổ chốt §2c) | Tạo/sửa form 2 tầng tab · sinh mã · Lưu nháp/Lưu · sao chép · xoá · lấy về (từng dòng + hàng loạt, 2 lối) · popup Xây dựng catalog + "Xếp vào tiểu mục…" · nút tạm "Chuyển kinh doanh" · seed 1655 |
| Ngoài 2-C | Excel (2-E, quyền 1654) · Yêu cầu/Phiếu tính giá + Chính sách giá nội bộ (phase Tính giá, 1656) · Báo cáo theo công ty · Lịch sử (§14b hoãn) · In tem barcode · giá (Phase 8) · backfill A3 |
| Đi 1 → 2 khi chưa có luồng tính giá | **ĐÃ CÓ ĐÁP ÁN**: bấm **Lưu** (không phải Lưu nháp) trên form ⇒ *Chờ tính giá* (§26a "Bấm Lưu ở bước 1", mockup `luuVaChuyen`, H1 "vẫn đủ bước Đang nhập thông tin → Chờ tính giá"). 2 → 3 bằng nút tạm **Chuyển kinh doanh** (H1) |
| Quyền | 1652 + 1653 đã seed (2-B). **1654/1655 CHƯA seed** trên nhánh chung; id 1652–1659 trống trên `origin/gop_db`, 2 nhánh báo cáo, `gop_db_sua_chua` |
| Khoá/Mở khoá | **Chưa từng chốt** — mockup có mục "Khóa" ở menu ⋮ (không handler); ERP **không có** khoá hàng hoá (status 0 = đã xoá) ⇒ tồn T5 |
| Tồn chặn lập plan | **11 câu** ở mục 4 — nặng nhất: Lưu nháp vướng 6 cột NOT NULL + mã UNIQUE (T1), `products.status` của hàng HRM tạo (T2), sửa hàng cũ chưa có dòng trạng thái (T3), ghi kép cột chung cho ERP (T4) |
| Phụ thuộc 2-D | Hàng HRM tạo có `group_id = NULL` ⇒ popup ERP 338 màn **nổ** (`->group->name`) ⇒ 2-C chỉ chạy được trên DB local/không có ERP dùng thật cho tới khi xong 2-D |

---

## 1. Danh sách tính năng GHI và luật

### 1.0 Khái niệm dùng chung

- **Công ty hiện tại** = `employee_infos.company_role ?: company_id` (§23c) — dùng helper đã có từ 2-B (`current_company_role`).
  ⚠️ Hook `creating` của `BaseModel` tự gán `company_id = info->company_id` (KHÔNG phải `company_role`) ⇒ mọi đường tạo
  `products` / `product_company_coefficients` / `product_suppliers` / `product_business_catalogs` phải **gán tay** `company_id`.
- **Công ty tạo (chủ)** = `products.company_id`. **Công ty lấy về** = có dòng `product_company_coefficients` (`status` NOT NULL) mà không phải chủ.
- **Trạng thái theo công ty** (`ProductCompany`): 1 Đang nhập thông tin · 2 Chờ tính giá · 3 Đang kinh doanh. (*Đang tính giá* chưa có hằng — thuộc phase Tính giá.)
  Hàng cũ chưa có dòng ⇒ 2-B **suy ra** *Đang kinh doanh* cho công ty tạo (`@TODO-BACKFILL`) — ảnh hưởng đường ghi, xem T3.
- Dòng HRM sinh ở `product_company_coefficients` **bắt buộc `coefficient = 1`** (K2; hằng `ProductCompany::NEUTRAL_COEFFICIENT`).
- `product_suppliers.company_id` NOT NULL DEFAULT 1 (K3) ⇒ HRM ghi phải kẹp `company_id` công ty hiện tại.
- **Lịch sử: KHÔNG ghi** (§14b xác nhận, plan cũ Task C4 ghi rõ). Hệ quả chấp nhận: sửa từ HRM không để lại vết nào.
- **Không có giá** ở bất kỳ request/response nào (2-B Q2, §20). Ghi `product_units` phải **giữ nguyên** `cost_price`/`buy_price` (§20 — không gán 0/null).

### 1.1 Tạo mới (màn *Hàng hoá nhập thông tin* → nút **Tạo mới**)

| Mục | Luật | Nguồn |
|---|---|---|
| Ai | quyền **1652** (FE ẩn nút + BE `checkPermission`) | §35b |
| Công ty | `products.company_id` = công ty hiện tại; ô *Công ty quản lý* chỉ đọc, hiện công ty chủ (mockup sai: hiện công ty đang làm việc — inventory §7-4) | §36c, §23c |
| Mã | **không nhận từ client**; `ProductCodeGenerator` sinh **một lần ở đường tạo**; form không có ô Mã/Trạng thái; tiêu đề màn sửa ghép mã `Sửa hàng hoá: <mã>` | §16, §36b |
| Dòng theo công ty | sinh 1 dòng `product_company_coefficients` (công ty chủ, `coefficient=1`, `status` = 1 khi Lưu nháp / 2 khi Lưu) + 4 cột quản trị | A1, K2 |
| Footer | **Lưu nháp** (tertiary) · **Lưu** (primary) · **Quay lại** | inventory §5.1 |
| Lưu nháp | mockup: chỉ đòi **Tên**; giữ *Đang nhập thông tin*; không validate catalog. ⚠️ Vướng DB — xem **T1** | inventory §5.9 |
| Lưu | đủ bắt buộc + **≥ 1 nhánh catalog** (C5-a, §33f); chuyển *Chờ tính giá*; báo lỗi đồng thời mọi ô; thiếu catalog ⇒ nhảy tab *Quản trị hàng hoá*, chấm đỏ tab cha, viền đỏ cột Tiểu mục, câu *"Phải xếp hàng hoá vào ít nhất 1 Tiểu mục…"* | §33f, §33v, mockup `luuVaChuyen` |
| Toast Lưu | mockup: *"…chuyển sang Chờ tính giá bán, lập Yêu cầu tính giá để đi tiếp"* — 2-C **không có** Yêu cầu tính giá ⇒ đổi câu (tự chốt UI) | §35b-2 |

**Trường theo tab** (inventory §5.2–5.7; bắt buộc `*` theo mockup):

| Tab | Trường ghi | Bảng |
|---|---|---|
| Thông tin chung | Tên* · Model* (+ thêm nhanh) · Tên thường gọi · Tên tiếng Anh · Barcode · Ghi chú · **Loại sản phẩm*** (3 cấp cha tự điền, chỉ đọc) · Đặc tính sản phẩm · Thương hiệu · Xuất xứ · Hãng SX · Code đặt hàng (+) · bảng **ĐVT** (Đơn vị*, đúng 1 đơn vị cơ bản, hệ số*) · Tài liệu kỹ thuật · Ảnh (≤10) · Video | `products`, `product_units`, `product_tech_attachments`, `product_galleries`, `product_videos` |
| Thông số kỹ thuật | Trọng lượng · Kích thước · Định mức công lắp đặt (vẫn cột lớp chung — §36a/§36c) · bảng thuộc tính (giá trị, đơn vị, bắt buộc, in tem) · Phụ kiện tiêu chuẩn · Đặc điểm (rich text) · 4 bảng hàng con: Công thức lắp ráp (SL, thành phần chính) · Phụ kiện mua thêm · Vật tư lắp đặt · Vật tư sửa chữa | `products`, `attribute_products`, `recipe_products`, `product_has_accessories`, `product_has_install_accessories`, `product_has_repair_accessories` |
| Mua hàng | Tên khai báo hải quan · HS Code · SL tối thiểu nhập mua · **% VAT*** · Thuế NK không CO · Thuế NK có CO · Thuế chống bán phá giá · Hệ số thuế BVMT (không bắt buộc; F7: BE tự suy `need_environment_tax`; 1 ≤ hệ số ≤ 999.999). **Bỏ** % giảm giá thanh lý (F8) | `products` |
| Phân loại xe | Hãng xe* (mockup) · Loại xe · Model xe · "Áp dụng tất cả đời xe" · bảng Đời xe theo từng model. ⚠️ §15/C3c.1 chốt **bỏ bắt buộc** Hãng xe — mockup còn `*` (mâu thuẫn, xem T11). Chỉ hiện khi Loại sản phẩm bật cờ (§18b) | `productables` (kẹp `productable_type`), `product_vehicle_model_has_life` |
| Nhóm máy | Nhóm máy (chọn nhiều) → bảng **Máy*** (chỉ hiện khi ≥1 nhóm) — quay về khuôn ERP (F1–F5) | `productables` loại `App\Model\Product\Group` / `App\Product` (bẫy: 32.366 dòng ERP đang đọc) |
| **Quản trị hàng hoá** (tab cha) | Nhà cung cấp (chọn nhiều) · Chính sách kinh doanh · SL tồn kho tối thiểu · Bảo hành · Đơn vị bảo hành · **Hệ số công nghệ** (xem T6) · catalog 4 cột → bảng nhánh (chỉ lưu Tiểu mục, chặn trùng) | `product_company_coefficients` (4 cột), `product_suppliers` (+company_id), `product_business_catalogs`, `products.tech_coefficient` |

### 1.2 Sửa — 2 mức, BE chặn (§26c-bis, §23c/§23d)

| Trường hợp | Sửa được | BE xử lý |
|---|---|---|
| Công ty hiện tại = `products.company_id` | **toàn bộ** tab | — |
| Công ty hiện tại **đã lấy về** (có dòng `status` NOT NULL) | **chỉ tab Quản trị hàng hoá** (4 cột + NCC của công ty mình + catalog của công ty mình) | trường lớp chung gửi lên ⇒ **403** (§23d: "gửi company_id khác ⇒ 403, không bỏ qua im lặng") |
| Công ty chưa dùng mã này | không gì | 403 |
| Vai Tính giá | (phase sau) | — |

- Đề xuất kỹ thuật: tách **2 endpoint** — `PUT /products/{id}` (lớp chung, chỉ chủ) và `PUT /products/{id}/company-data` (tab Quản trị, chủ hoặc công ty đã lấy về). Một endpoint "lọc bớt field" dễ thủng hơn và khó test 403.
- FE (mockup `datVaiForm`): hàng công ty khác ⇒ form mở thẳng tab *Quản trị hàng hoá*, tab cha *Thông tin hàng hoá* mờ + 5 step khoá, ẩn hẳn nút thêm/xoá dòng, hiện dải *"Hàng hoá do <Công ty tạo> tạo — chỉ khai được tab Quản trị hàng hoá."*
- `code` không nhận ở đường sửa; `Product::boot()` đã ném lỗi nếu `code` dirty.
- **C2: sửa hàng *Đang kinh doanh* (chung hay quản trị) KHÔNG lùi trạng thái.** Mockup `luuVaChuyen` đặt `st='cho'` cho MỌI lần Lưu khi sửa — **sai với C2** ⇒ luật đúng: Lưu chỉ đổi 1 → 2; trạng thái 2/3 giữ nguyên. Lưu nháp chỉ có nghĩa ở trạng thái 1 ⇒ đề xuất ẩn Lưu nháp khi trạng thái ≠ 1 (tự chốt UI).
- C5-a: lưu tab Quản trị (tạo lẫn sửa) phải ≥ 1 nhánh — kể cả hàng cũ chưa có catalog.
- Lối vào sửa: menu ⋮ màn *Nhập thông tin* có **Sửa**; các màn khác có **Xem** (mockup "Xem" mở cùng form sửa). Hàng trạng thái 2/3 sửa từ đâu — xem T10.

### 1.3 Sao chép (menu ⋮ màn *Hàng hoá nhập thông tin*)

- Quyền 1652. Bản sao là **bản ghi MỚI ⇒ sinh mã mới** (§16 hệ quả C4); trạng thái *Đang nhập thông tin* cho công ty hiện tại; chủ = công ty hiện tại.
- ERP làm: `GET /{id}/copy` mở **form tạo mới điền sẵn** từ `getDataForEdit` (ĐVT, thuộc tính, nhóm máy, 4 loại `productables` xe, phụ kiện…; giá gán 1), người dùng bấm lưu mới tạo (`ProductsController:1084`). ⇒ đề xuất HRM theo đúng cách đó: FE mở `/products/create?copy_from=<id>`, không có endpoint clone phía server.
- Rule trùng tên (tên × model × thương hiệu × hãng SX) ⇒ bản sao lưu ngay sẽ **lỗi trùng tên** nếu không đổi gì — đúng ERP.
- Mockup **không có handler** cho Sao chép. Chưa chốt: chép những gì (tab Quản trị? catalog? tệp/ảnh dùng chung đường dẫn hay nhân bản?), sao chép hàng do công ty khác tạo có được không ⇒ **T9**.

### 1.4 Xoá (§35b-4)

| Ca | Điều kiện | Hành động |
|---|---|---|
| Hàng **do công ty mình tạo** | trạng thái của công ty mình = *Đang nhập thông tin* · **chưa công ty nào khác lấy về** · **chưa phát sinh chứng từ** | xoá hàng hoá |
| Hàng **công ty khác đã lấy về** | (đề xuất: trạng thái của mình = *Đang nhập thông tin*, vì nút Xoá chỉ có ở màn này) | **gỡ dòng của công ty mình** ở `product_company_coefficients` (+ NCC, catalog của công ty mình); không đụng `products` |

- Quyền 1652, không thêm quyền. Nút **ẩn hẳn** khi không đủ điều kiện (quy tắc HRM) + BE kiểm lại.
- Popup xác nhận: mockup chỉ có popup xoá của màn Chính sách giá (`#mask-xoa`, khuôn `base-confirm-modal`) ⇒ dùng khuôn đó, id `confirm-<việc>-<slug>`.
- ERP `canDelete()` (`app/Product.php:7215`): khác công ty · còn tồn kho (`stocks.accounting_qty > 0`) · đang mượn chưa trả · nằm trong phụ kiện · nằm trong công thức ghép bộ. ERP xoá = **mềm** (`status = 0` + `deleted_at`, có màn khôi phục).
- Chưa chốt: định nghĩa "chứng từ", xoá cứng hay mềm, gỡ dòng có hệ số cũ ⇒ **T8**.

### 1.5 Lấy hàng công ty khác về (A2 tham chiếu, §26d, §33l, §33m)

| Lối | Vị trí | Ghi |
|---|---|---|
| 1 | Màn **Kho dữ liệu hàng hoá**: nút **Lấy về** từng dòng (dòng công ty mình chưa dùng) + tick → thanh xanh *"Đã chọn N"* → **Lấy về công ty** | 2 lối **giữ cả hai** (§33m) |
| 2 | Màn **Hàng hoá nhập thông tin** → nút **Xem hàng hoá Công ty khác** → popup (chọn nhiều, bộ lọc công ty quản lý + phân loại + Dùng cho nhóm máy/máy (F4), phóng to, cấu hình cột) → **Chọn** | |

- Quyền **1652** cả FE lẫn BE (§35b). Kết quả: dòng (hàng × công ty hiện tại) `status = 1`, `coefficient = 1`; toast *"Đã lấy <mã> về <cty> — trạng thái Đang nhập thông tin"* / *"Đã lấy N hàng hoá…"*; mã công ty đã dùng ⇒ bỏ qua, báo *"…đang dùng rồi"*.
- "Chưa dùng" xét theo **công ty đang đăng nhập** (§26g-4); hàng đã có dòng trạng thái hoặc **được suy ra** *Đang kinh doanh* (hàng cũ của chính công ty mình) ⇒ không lấy được.
- 🔴 **Bẫy UNIQUE(product_id, company_id)**: 1.100 dòng hệ số cũ của Cty 2/3/4 có `status = NULL`. Lấy về hàng đã có dòng hệ số cũ ⇒ phải **UPDATE** dòng sẵn có (đặt `status = 1`, GIỮ `coefficient` cũ), không INSERT (nổ 1062) và không ghi đè `coefficient = 1`.
- Giới hạn lượt: **tài liệu KHÔNG có trần cho Lấy về** — trần 100 mã/lượt của §33j là của **popup Xây dựng catalog**. Đề xuất dùng chung trần 100 cho lấy hàng loạt (xem T11).
- Hệ quả đã chấp nhận (K2): popup ERP của công ty lấy về hiện giá **làm tròn nghìn**. 2-D phải chặn route lưu Hãng SX ERP (`Sale/ManufacturesController:274` xoá-ghi lại dòng của mọi hàng status 1 thuộc hãng ⇒ mất trạng thái).
- Hàng `products.status = 0` (ERP đã xoá, 17.512 mã) có nên lấy về được không — chưa ghi ⇒ đề xuất chặn (T11).

### 1.6 Popup **Xây dựng catalog kinh doanh** (§33c/d/j/k, §36f, A6, C5)

- Mở từ màn **Dữ liệu hàng hoá công ty**: nút **Xây dựng catalog** (toolbar) + tick dòng → **Xếp vào tiểu mục…** (mang sẵn mã đã tick, vào thẳng tab *Thêm*). **Không** có ở màn *Hàng đang kinh doanh* (§33e).
- Quyền **1655 Xây dựng catalog kinh doanh** — không có thì **ẩn nút**, BE gate endpoint (§33a, §35b). Vào màn cần 1652 | 1653.
- Phạm vi: **chỉ công ty đang đăng nhập**; nguồn = **toàn bộ hàng hoá của công ty, mọi trạng thái** (gồm hàng lấy về).
- Trái: cây 4 cấp (Lĩnh vực › Chương › Mục › Tiểu mục), số hàng theo nhánh (cộng giỏ chờ), tìm trong cây, mở/thu toàn bộ + từng lĩnh vực, lĩnh vực khoá 🔒; chỉ nhánh có gốc mới (H3).
- Phải: tab 1 **Hàng trong tiểu mục (N)** (tick → **Gỡ khỏi tiểu mục**, đỏ) · tab 2 **Thêm hàng vào tiểu mục**; bảng 12 cột (☐ · STT · Ảnh · Mã · Tên · Model · Loại SP · Thương hiệu · ĐVT · **Thông số cơ bản** (tóm tắt + nút ⋯, eager load) · Trạng thái · Catalog đang xếp); bấm Mã/Tên cũng tick; phân trang 20/50/100; tìm nâng cao 8 ô (đã bỏ *Công ty quản lý*), mặc định ẩn; phóng toàn màn hình.
- Chọn nhanh: tick · **"Chọn tất cả N kết quả lọc"** · **Dán danh sách mã** (báo đã tick x/y · z không trong danh sách lọc · t không tồn tại). **Trần 100 mã / lượt**, chặn ngay lúc tick (§33j-2) ⇒ FE gửi danh sách id (≤100), không cần `assign-by-filter` (§33i-6 hết hiệu lực).
- Giỏ chờ `+N / −M` + **Hoàn tác** (cả lượt gần nhất) + **Lưu một lần**; đóng khi còn giỏ ⇒ popup *Thông tin chưa lưu*.
- Ghi: `product_business_catalogs` (`product_id, company_id, job_cluster_id`, UNIQUE 3 cột, chỉ Tiểu mục).
- Gỡ nhánh cuối: **được** — C5 bỏ điều kiện catalog ở màn kinh doanh nên hàng không rời màn nào. Hệ quả: lần sau lưu tab Quản trị sẽ bị C5-a chặn tới khi xếp lại (cố ý).
- Lưu ý: catalog ghi được từ **2 cửa với 2 quyền khác nhau**: popup (1655) và tab Quản trị của form (1652).

### 1.7 Nút tạm **Chuyển kinh doanh** (H1)

- Luật: chưa có luồng Tính giá ⇒ người có **1652** bấm để chuyển **Chờ tính giá → Đang kinh doanh** (của công ty hiện tại). Giá bán vẫn khai/duyệt ở ERP như hiện nay. Khi có phase Tính giá ⇒ gỡ nút, thay bằng *Lưu & duyệt giá bán* trên phiếu.
- Chưa ghi: nút đặt ở đâu (đề xuất: màn *Dữ liệu hàng hoá công ty*, đúng chỗ nút **Tính giá** của mockup §33m — chỉ hiện ở dòng trạng thái 2; có thao tác hàng loạt không), có cần xác nhận không ⇒ T10. ⚠️ "Giá vẫn khai bên ERP" mâu thuẫn với việc 2-D chặn route tạo/sửa hàng hoá ERP ⇒ **T7**.

### 1.8 Chuyển trạng thái (tổng hợp)

```
(chưa dùng) ──Tạo mới: Lưu nháp──▶ 1 Đang nhập thông tin ──Lưu (đủ bắt buộc + ≥1 catalog)──▶ 2 Chờ tính giá
(chưa dùng) ──Tạo mới: Lưu──────────────────────────────────────────────────────────────▶ 2 Chờ tính giá
(chưa dùng, hàng công ty khác) ──Lấy về──▶ 1
2 ──Chuyển kinh doanh (H1, 1652)──▶ 3 Đang kinh doanh
1 ──Xoá──▶ (xoá hàng / gỡ dòng công ty mình)
```
- **Không có chiều lùi** (C2): sửa ở 2/3 giữ nguyên; không có thao tác 3 → 1/2. *Đang tính giá* chưa dùng.
- Mỗi công ty một trạng thái riêng cho cùng mã (§26a).

### 1.9 Khoá / Mở khoá — CHƯA CHỐT

- Mockup: mục **Khóa** ở menu ⋮ kiểu `kd` (mọi màn trừ *Nhập thông tin*), **không có handler**, không có "Mở khoá".
- Tài liệu chốt (§26, §33, §35a–h): **không nhắc** khoá hàng hoá. Plan cũ Task C4.1 (21/09) khoá = đổi `products.status` — **trước mô hình trạng thái theo công ty**, không còn đúng.
- ERP không có khoá hàng hoá: `status = 0` + `deleted_at` là **xoá** (có màn khôi phục); popup tìm hàng ERP lọc `status = 1`.
⇒ **T5**.

### 1.10 Ẩn ở 2-C

In tem barcode · Lịch sử (§14b) · Lập yêu cầu tính giá · Tính giá · Xuất Excel (2-E) — nút không dùng được thì ẩn hẳn.

---

## 2. Quyền theo thao tác

| Thao tác | Quyền | FE | BE |
|---|---|---|---|
| Tạo mới, Lưu nháp, Lưu, Sửa (cả 2 mức), Sao chép, Xoá | **1652** Xây dựng thông tin hàng hoá | ẩn nút | `checkPermission` + kiểm công ty |
| Lấy về (từng dòng, hàng loạt, popup Công ty khác) | **1652** (chỉ quyền này — §35b) | ẩn nút | có |
| Chuyển kinh doanh (H1) | **1652** | ẩn nút | có |
| Popup Xây dựng catalog, Xếp vào tiểu mục… | **1655** Xây dựng catalog kinh doanh | ẩn nút | có |
| Catalog trong tab Quản trị của form | 1652 (thuộc thao tác sửa) | | |
| Xuất Excel | 1654 — **đợt 2-E** | | |
| Chính sách giá nội bộ | 1656 — phase Tính giá | | |
| Khoá/Mở khoá | chưa chốt (đề xuất 1652) | | |
| Đọc chi tiết / Kho dữ liệu / Hàng đang KD | không cần quyền (§35b-3) | | |

Hiện trạng seeder `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` trên `feat/chuyen-doi-hang-hoa`:
- **1652, 1653 đã có** (dòng 1582–1583, group *Hàng hoá*, guard `api`, type 9) + đã INSERT vào DB local (2-B).
- **1654, 1655, 1656 CHƯA có** — comment dòng 1581 *"1654–1656 seed ở đợt dùng tới"*.
- Kiểm 04/10: id 1652–1659 **không** xuất hiện trên `origin/gop_db`, `gop_db-bao-cao-ke-hoach-lam-viec`, `gop_db-bao-cao-nhu-cau-dich-vu`, `origin/gop_db_sua_chua` ⇒ 1655 còn trống. Kiểm lại ngay trước khi seed (`uniq -d`), INSERT riêng 1 dòng vào DB local (không chạy cả seeder — memory *PermissionsTableSeeder truncate*), `role_has_permissions.company_id = 1`, xoá cache spatie.
- Super admin không có ngoại lệ. Test bắt buộc cả ca **có** và **không** quyền cho mỗi endpoint ghi + ca 2 token 2 công ty ghi chéo bị 403 (§23d).

---

## 3. Tái sử dụng từ nhánh cũ `feat/p1-danh-muc-hang-hoa` (đóng băng, E1)

| File (nhánh cũ) | Kết luận | Phải sửa |
|---|---|---|
| `Modules/MasterData/Services/Product/ProductCodeGenerator.php` (184 dòng; 869a3bb2d, a5c438d56) | **Lấy nguyên** | Không. Đã có: khuôn `<mã hãng>-<code đặt hàng ?: model>`, cắt 32, hậu tố `:01–:99`, bảng bỏ dấu cố định (né bẫy `iconv` khác máy), ném `RuntimeException` khi thiếu nguồn, docblock "CHỈ GỌI Ở ĐƯỜNG TẠO MỚI". Bổ sung ở Service: bắt lỗi 1062 trên `products_code_unique` (UNIQUE có thật trong DB) ⇒ sinh lại, tối đa vài lần (C1.4 cũ dời sang C2) |
| `Modules/MasterData/Tests/Feature/ProductCodeGeneratorTest.php` (9 ca) | **Lấy nguyên** | 2 ca khoá mã (`test_khong_duoc_doi_ma…`, `test_van_sua_duoc…`) dựa vào `Product::boot()` — nhánh chung đã có hook này. Test ghi DB thật, dọn theo token `PCGT` (không `RefreshDatabase`) |
| `Product::boot()` chặn đổi `code` | **Đã có** trên nhánh chung | — |
| `Modules/MasterData/Http/Requests/Product/ProductRequest.php` (220 dòng; b833d7677 đã gỡ khối giá) | **Lấy khung, sửa nhiều** | xem bảng dưới |
| Store/update/copy/delete service | **Không tồn tại** ở nhánh cũ (`ProductService` chỉ có `index/show`; 9/15 route cũ trỏ method chưa viết) | Viết mới |
| Plan cũ Task C2/C3/C3c/C3b/C4 (`man-danh-muc-hang-hoa/plan.md:442–584`) | Tham khảo luật | C3c (ghi `productables` xoá+chèn **theo từng `productable_type`**, không `sync()`, test bất biến đếm 2 loại không quản) **còn đúng**; C3 nhánh duyệt giá BB-1 **bỏ** (§20); C4.1 khoá theo `products.status` **lỗi thời** (T5); C3b `attributes-by-type` dùng được; `bulk-delete` chưa có trong yêu cầu mới |

**Sửa `ProductRequest`** (đối chiếu ERP `Product::getRules` `app/Product.php:279` + schema `hrm_erp`):

| Rule cũ | Việc |
|---|---|
| `company_id` required từ request | **Bỏ** — server gán công ty hiện tại (`company_role`) |
| `company_coefficients.*` | **Bỏ** — hệ số giá sẽ bỏ (K0), HRM chỉ ghi `coefficient = 1` |
| `rate_liquidation` | Bản cuối **không còn** rule này (tài liệu 2-B ghi có — đã kiểm lại); nhưng `Product::$fillable` nhánh chung **còn** `rate_liquidation` ⇒ bỏ khỏi fillable hoặc chắc chắn không `fill($request->all())` (F8: không ghi, không xoá 1.251 giá trị cũ) |
| `need_environment_tax` / `environment_tax_coefficient` | **Thêm**: hệ số `nullable|numeric|min:1|max:999.999`; cờ **BE tự suy** (F7). ⚠️ `environment_tax_coefficient` là **NOT NULL DEFAULT 1.00** ⇒ khi trống phải ghi cờ 0 + hệ số 1.00, FE đọc lại hiện **trống khi cờ 0** |
| VAT / thuế | **Thêm** `vat_percent_tax_rate_id` **required** (mockup `*`), `import_tax_tax_rate_id` / `import_tax_has_co_tax_rate_id` / `antidump_duty_tax_rate_id` nullable `exists:tax_rates`; BE suy `vat_percent` / `import_tax` / … từ `TaxRate.tax_rate` như ERP (`ProductsController:1866–1869`). Rule cũ nhận thẳng số % — sai khuôn ERP |
| `model_id` `required_without:barcode_id` | Mockup: **Model `*`** (ERP store cũng `required`) ⇒ đổi `required` |
| `name` unique (model × brand × manufacture) | Giữ khuôn ERP **store**; ERP **update** có thêm `origin_id` — chốt dùng 1 khuôn cho cả 2 đường |
| `avatar` required | ERP bắt buộc, mockup *Hình ảnh* không `*`, cột nullable ⇒ hỏi (T1) |
| `tech_coefficient` `min:1` (ERP cũng vậy) | 🔴 **11.156 hàng đang = 0** ⇒ mở hàng cũ bấm Lưu là **lỗi validate dù không sửa ô** ⇒ nới `min:0` hoặc chỉ kiểm khi dirty |
| `guarantee`, `min_stock_qty`, `business_policy_id` | Chuyển sang request của tab Quản trị (ghi `product_company_coefficients`); thêm `guarantee_type in:ngay,thang,nam` |
| `suppliers.*` | Giữ; ghi kèm `company_id` công ty hiện tại, chỉ thay dòng **của công ty mình** |
| `vehicle_*_ids` | Giữ (không `required_if` — §15) + thêm đời xe theo model (bảng bộ ba) |
| Nhóm máy | **Thêm** `group_ids_use` + danh sách máy (F3 — dữ liệu ERP dùng tiếp nguyên trạng) |
| Catalog | **Thêm** `job_cluster_ids` `required|array|min:1` khi **Lưu** (không khi Lưu nháp), `distinct`, `exists` + chỉ Tiểu mục thuộc nhánh gốc mới (H3) |
| `product_type_id` required | Giữ (mockup *Loại sản phẩm* `*`; cột đã có từ 2-B Q3) |
| Lưu nháp | **Tách bộ rule riêng** — chỉ những gì DB bắt buộc (xem T1) |

---

## 4. Tồn CHẶN lập plan — hỏi lần lượt từng câu

> Mỗi câu kèm phương án + hệ quả; ⭐ = đề xuất. Chưa trả lời hết thì không mở code (memory *hoi-het-ton-truoc-khi-code*).

**T1. Lưu nháp chỉ cần Tên — nhưng `products` có 6 cột NOT NULL không default + mã UNIQUE.**
Đo `hrm_erp`: NOT NULL không default = `code` (UNIQUE `products_code_unique`), `name`, `status`, `brand_id`, `manufacture_id`, `origin_id`, `created_by`. Mã cần Hãng SX + (Code đặt hàng | Model) và **chỉ sinh một lần** (§16).
- ⭐ (a) Lưu nháp bắt buộc **Tên + Thương hiệu + Hãng SX + Xuất xứ + Model** (đủ để insert + sinh mã ngay) — đơn giản, mã sinh đúng 1 lần; nháp "nặng" hơn mockup.
- (b) Lưu nháp sinh **mã tạm** rồi sinh mã thật lúc Lưu — vi phạm "sinh một lần" + phải nới hook `boot()`.
- (c) Nháp lưu ở bảng riêng (JSON) tới lần Lưu đầu — đổi CSDL (ngoại lệ Tiền đề 1), hàng nháp không hiện ở màn danh sách theo `products`.
Kèm: `avatar` bắt buộc như ERP (§17) hay không bắt buộc như mockup?

**T2. `products.status` của hàng HRM tạo.** ERP (popup 338 màn, báo giá…) chỉ nhìn `products.status = 1`, không biết trạng thái theo công ty.
- (a) Ghi `1` ngay khi tạo — hàng đang nhập dở **hiện ở ERP** để bán; cộng `group_id = NULL` là popup ERP nổ cho tới khi xong 2-D.
- ⭐ (b) Ghi `2` (`Product::CHO_DUYET`) khi tạo, đổi `1` khi **công ty đầu tiên** sang *Đang kinh doanh* (nút H1) — ERP không thấy hàng chưa xong; cần kiểm màn *Duyệt giá* ERP có liệt kê `status = 2` không.
- (c) Giữ 1 nhưng chặn bằng cờ khác — đổi CSDL.

**T3. Sửa hàng CŨ chưa có dòng trạng thái (2-B suy ra *Đang kinh doanh*, K1 không backfill).** Lưu tab Quản trị buộc phải **sinh dòng** `product_company_coefficients` cho công ty tạo; dòng `coefficient = 1` làm popup ERP **làm tròn nghìn** giá của hàng đó (8.904 hàng status 1 có giá lẻ nghìn — khảo sát 2-A §2). K2 mới chấp nhận cho *tạo mới / lấy về*.
- (a) Sinh dòng `status = 3`, `coefficient = 1`, chép sẵn 3 giá trị chung (`min_stock_qty`, `guarantee`, `guarantee_type`) — mở rộng K2 sang hàng cũ; giá ERP đổi dần theo từng lần sửa, im lặng.
- (b) Hàng cũ **chỉ sửa được lớp chung**, tab Quản trị khoá tới khi phase giá backfill/gỡ hệ số — không đổi giá ERP; người dùng không xếp catalog trong form được (vẫn dùng popup 1655).
- (c) Sinh dòng với `coefficient = NULL` — giá ERP = 0 (khảo sát 2-A) ⇒ loại.

**T4. 3 cột quản trị chung (`min_stock_qty` 29 file ERP, `guarantee`/`guarantee_type` 86 file) — ERP vẫn đọc trên `products`.** §24b: chuyển sang theo công ty, xoá cột chung **sau cùng**.
- ⭐ (a) Công ty **chủ** ghi **kép** (`products.*` + dòng công ty); công ty lấy về chỉ ghi dòng của mình — ERP vẫn đúng cho công ty chủ tới lúc cắt.
- (b) Chỉ ghi dòng công ty — ERP thấy số cũ đứng yên (bảo hành sai trên chứng từ — 23 bảng chép `guarantee_type`, sổ chốt §5-7).

**T5. Khoá / Mở khoá hàng hoá** (mockup có "Khóa", chưa từng chốt).
- ⭐ (a) **Không làm ở Phase 2**, ẩn mục Khóa — ERP không có khoá hàng hoá; thay bằng Xoá cho hàng nháp.
- (b) Khoá **theo công ty**: thêm trạng thái 4 *Ngừng kinh doanh* trên dòng công ty (rời màn *Đang kinh doanh*, popup Phase 4 không thấy) + Mở khoá về 3 — cần thêm hằng/badge, đụng C2 (có phải "lùi"?).
- (c) Khoá **toàn cục** `products.status = 0` (chỉ công ty chủ) — trùng nghĩa *xoá mềm* ERP, ảnh hưởng mọi công ty đang bán.

**T6. Hệ số công nghệ (`products.tech_coefficient`, cột CHUNG, ERP chép sang phiếu phân công lắp đặt `AssemblyRequestController:550`)** — nằm ở tab *Quản trị* (dữ liệu "riêng công ty", tooltip §36n) nhưng **không** thuộc 4 cột §24b.
- (a) Theo công ty: thêm cột `product_company_coefficients.tech_coefficient` (đổi CSDL) — ERP vẫn đọc cột chung ⇒ phải ghi kép như T4 hoặc sửa ERP.
- ⭐ (b) Giữ chung, **chỉ công ty chủ sửa**; với công ty lấy về ô này khoá trong tab Quản trị — không đổi CSDL; tab có 1 ô lệch nghĩa "riêng công ty".
- (c) Giữ chung và **dời ô sang tab Thông số kỹ thuật** — sửa mockup đã chốt, sửa tooltip §36n.

**T7. H1 "giá vẫn khai/duyệt bên ERP" vs 2-D chặn route tạo/sửa hàng hoá ERP (QĐ13).** Hàng HRM tạo có `product_units` nhưng **0 dòng `product_unit_prices`** (ERP luôn có 6 dòng/ĐVT, 264.646 dòng).
- Cần chốt: giá của hàng HRM tạo khai ở **màn nào của ERP** (màn giá theo ĐVT / cập nhật nhanh giá — `sua-erp-de-khong-loi.md` §1.3 có 3 hàm `update/update2/update3`) và 2-D **phải chừa** route đó.
- HRM có phải sinh sẵn **6 dòng giá rỗng/ĐVT** để màn giá ERP không lỗi? (⭐ kiểm ERP trước khi chốt.)

**T8. Xoá — 3 điểm chưa có chữ.**
- "Chưa phát sinh chứng từ" = (⭐) đúng 5 điều kiện ERP `canDelete()` + "chưa công ty khác lấy về", hay quét toàn bộ 171 bảng FK trỏ `products`?
- Xoá hàng của mình: ⭐ **mềm** như ERP (`status = 0` + `deleted_at`, giữ mã) + xoá dòng công ty/NCC/catalog của mình · hay xoá cứng (hàng nháp chưa ai dùng)?
- Gỡ hàng lấy về khi dòng đó **có sẵn hệ số cũ** từ trước (1.100 dòng): xoá dòng là **mất hệ số giá cũ** ⇒ ⭐ đặt `status = NULL` + xoá 4 cột quản trị thay vì xoá dòng.

**T9. Sao chép chép những gì?** ⭐ như ERP: mở form tạo điền sẵn toàn bộ lớp chung (ĐVT không giá, thuộc tính, 4 bảng hàng con, xe, nhóm máy, mô tả) — **không** chép tab Quản trị/catalog, **không** chép tệp/ảnh (hoặc dùng chung đường dẫn?). Có cho sao chép hàng **do công ty khác tạo** (đang ở màn Nhập thông tin của mình sau khi lấy về) thành hàng của mình không?

**T10. Lối sửa + vị trí nút H1.** (a) Hàng trạng thái 2/3: menu ⋮ chỉ có **Xem** — mở form **sửa được** (C2 ngụ ý sửa được hàng đang KD) hay chỉ đọc + nút Sửa riêng? (b) Nút *Chuyển kinh doanh*: ⭐ màn *Dữ liệu hàng hoá công ty*, dòng trạng thái 2 (chỗ nút *Tính giá* §33m), có thêm thao tác hàng loạt không, có popup xác nhận không?

**T11. Câu nhỏ (đề xuất tự chốt nếu user không phản đối).**
- Trần **100 mã/lượt** cho *Lấy về* hàng loạt (tài liệu chỉ có trần cho catalog).
- Không cho lấy về hàng `products.status ≠ 1` (ERP đã xoá/chờ duyệt).
- Tab Phân loại xe: Hãng xe **không bắt buộc** (§15, C3c.1) — mockup còn dấu `*` ⇒ theo §15.
- Lưu nháp ẩn khi trạng thái ≠ 1; toast Lưu bỏ vế "lập Yêu cầu tính giá".

---

## 5. Bẫy phải mang theo khi code

- `productables` gánh 5 loại — mọi xoá/chèn kẹp `productable_type`; không `sync()`, không `morphedByMany()`. Tab Nhóm máy nay **HRM ghi** cả 2 loại `Group`/`App\Product` mà plan cũ coi là "không quản" ⇒ test bất biến phải đổi: loại nào không thuộc tab đang lưu thì số dòng không đổi.
- `products` không `SoftDeletes` (175 hàng status 1 còn `deleted_at`).
- UNIQUE `(product_id, company_id)` + 1.100 dòng hệ số cũ `status NULL` ⇒ upsert, không insert mù (mục 1.5).
- Hook `BaseModel::creating` gán `company_id = info->company_id` ⇒ gán tay `company_role`.
- `getChanges()` rỗng ở đường INSERT — test riêng đường tạo và đường sửa.
- `group_id = NULL` trên hàng mới ⇒ popup ERP nổ tới khi xong 2-D; `product_type` (chuỗi) NULL ⇒ hàng "biến mất" ở 4 chỗ lọc ERP.
- `environment_tax_coefficient` NOT NULL DEFAULT 1.00; `tech_coefficient` 11.156 hàng = 0 vs rule `min:1`.
- Ghi ĐVT không đụng `cost_price`/`buy_price`.
- Catalog: chỉ Tiểu mục thuộc nhánh có `chapters.internal_business_scope_id` (H3) — dữ liệu cũ 65/106/2 ẩn, không được chọn.
- Đo xong FE bằng Playwright (DOM), e2e có quyền + không quyền; không tự chạy cả bộ e2e.

---

## 6. Đề xuất chia 2-C (mỗi đợt nhánh con từ `feat/chuyen-doi-hang-hoa`, xin "làm" riêng)

| Đợt | Nội dung | Phụ thuộc tồn |
|---|---|---|
| **2-C1 Tạo + sửa (chủ)** | `ProductCodeGenerator` + test · `ProductRequest` (bộ Lưu nháp / bộ Lưu) · `POST /products` + `PUT /products/{id}` lớp chung (5 tab con) · ghi dòng công ty + tab Quản trị cho **công ty chủ** · Lưu nháp/Lưu, 1 → 2 · page `create` + `_id/edit` 2 tầng tab · PHPUnit (tạo, sửa, khoá mã, 403 công ty khác, có/không 1652, bất biến `productables`, không đụng giá) | T1, T2, T3, T4, T6, T11 |
| **2-C2 Lấy về + sửa mức Quản trị** | `POST /products/take` (1 hoặc nhiều id, ≤100) ở Kho dữ liệu + popup *Xem hàng hoá Công ty khác* · `PUT /products/{id}/company-data` cho công ty lấy về (403 nếu gửi lớp chung) · form chế độ `chiQuanTri` | T11; nền từ 2-C1 |
| **2-C3 Catalog** | seed **1655** · endpoint cây + danh sách hàng công ty cho popup (eager load thông số) · `POST` gán/gỡ theo lô (≤100) · popup Xây dựng catalog + *Xếp vào tiểu mục…* | không tồn chặn (độc lập 2-C1, chỉ cần màn công ty 2-B) — **làm song song hoặc đầu tiên được** |
| **2-C4 Vòng đời** | Xoá (2 ca) · Sao chép (form điền sẵn) · nút **Chuyển kinh doanh** (H1) · (Khoá nếu T5 chọn b/c) | T5, T7, T8, T9, T10 |

Thứ tự đề xuất: **2-C3 → 2-C1 → 2-C2 → 2-C4** (2-C3 không vướng câu nào và cho người dùng xếp catalog cho hàng cũ trước khi form bắt buộc catalog). Nếu gộp một nhánh: ~4 endpoint nhóm + 2 page form/popup lớn — quá rộng để nghiệm thu một lượt.
