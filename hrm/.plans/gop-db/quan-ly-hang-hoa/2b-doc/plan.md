# Đợt 2-B — Đọc: 4 màn danh sách + form chỉ xem — plan

> 04/10/2026 · @namdangit · khảo sát + chốt: `khao-sat.md` (Q1–Q4) · mockup: `mockup-inventory.md` ·
> code nhánh cũ: `tai-su-dung-nhanh-cu.md`.
> ✅ User cho phép code (04/10/2026). Nhánh `feat/p2b-doc` (api + client) từ `feat/chuyen-doi-hang-hoa`.

## 0. Ranh giới

- CHỈ ĐỌC. Mọi nút [GHI] (Tạo mới · Sửa · Sao chép · Xoá · Lấy về · Xây dựng catalog · Xếp vào tiểu mục) → 2-C.
  Tính giá / Lập yêu cầu tính giá → phase Tính giá. Xuất Excel → 2-E. Các nút này **không hiện** ở 2-B
  (quy tắc HRM: nút không dùng được thì ẩn hẳn).
- **Không có giá** ở bất kỳ màn/form/API nào (Q2).
- Trạng thái theo công ty: đọc `product_company_coefficients.status`; hàng cũ chưa có dòng ⇒ **suy ra lúc đọc** (Q1):
  `products.status = 1` ∧ `products.company_id = công ty xét` ⇒ *Đang kinh doanh*. Gom vào 1 scope, có `@TODO-BACKFILL` để gỡ.
- Công ty hiện tại: `employee_infos.company_role`, lùi về `company_id` (§23c).
- Không `mysql2`, model mới `extends BaseModel`, không đụng `gop_db` (merge về `feat/chuyen-doi-hang-hoa`).

## 1. Phạm vi xin phép

| | |
|---|---|
| Repo · nhánh | `hrm-api` + `hrm-client`, nhánh `feat/p2b-doc` từ `feat/chuyen-doi-hang-hoa` (cả 2 repo) |
| BE | 1 migration (2 cột phân loại) · Entity `Product` + bảng con (port nhánh cũ, sửa theo `tai-su-dung-nhanh-cu.md`) · `ProductService` / `ProductOptionService` / controller / Resource · route `Modules/MasterData/Routes/api.php` · 2 quyền 1652–1653 trong `PermissionsTableSeeder.php` · PHPUnit |
| FE | menu `components/subsystem-menu/master-data.js` (nhóm *Hàng hoá*) · 4 page danh sách + 1 page chi tiết dưới `pages/master-data/products/` · 1 spec e2e |
| DB local `hrm_erp` | chạy 1 migration (`--path`) + INSERT 2 quyền 1652/1653 — **hỏi riêng trước khi chạy**, KHÔNG chạy cả seeder |

## 2. Task

### BE (hrm-api)

- [x] **B1. Migration** `add_classification_to_products_table`: `product_type_id`, `product_characteristic_id` (bigint unsigned NULL, index, không FK). Guard `hasColumn` (DB local đã có từ nhánh cũ).
- [x] **B2. Entity** `Modules/MasterData/Entities/Product/Product.php` + bảng con cần cho form (ĐVT, thuộc tính, NCC, phụ kiện/định mức `base_product_id`, `productables` theo `productable_type`, ảnh/tài liệu/video, đời xe). Lấy từ nhánh cũ: giữ docblock bẫy (không SoftDeletes · không `morphedByMany` · khoá `code`); `extends BaseModel`; bỏ `ProductCompanyCoefficient` (dùng `ProductCompany` 2-A); `ProductSupplier` thêm `company_id`.
  Scope `scopeWithCompanyStatus($q, $companyId)`: left join `product_company_coefficients` theo công ty, trả `company_status = COALESCE(pcc.status, CASE WHEN products.status = 1 AND products.company_id = ? THEN 3 END)`.
- [x] **B3. Quyền** 1652 *Xây dựng thông tin hàng hoá* · 1653 *Xem dữ liệu hàng hoá công ty* (guard `api`, group *Hàng hoá*); kiểm `uniq -d` + tên không trùng-bỏ-dấu với quyền `web`.
- [x] **B4. API** (prefix `master-data/products`):
  | Endpoint | Màn | Gate | Lọc cốt lõi |
  |---|---|---|---|
  | `GET /warehouse` | Kho dữ liệu | đăng nhập | mọi hàng; cột *Công ty đang kinh doanh* = các công ty có `company_status` = 3; công tắc "Chỉ hàng công ty chưa dùng" = không có dòng/suy ra cho công ty mình |
  | `GET /company` | Dữ liệu hàng hoá công ty | 1652 \| 1653 | `company_status IS NOT NULL` của công ty mình; 4 ô catalog + "Chưa xếp catalog" |
  | `GET /entering` | Hàng hoá nhập thông tin | 1652 | `company_status = 1` |
  | `GET /trading` | Hàng đang kinh doanh | đăng nhập | `company_status = 3`; trả kèm `uncatalogued_count` cho dòng nhắc cam |
  | `GET /{id}` | Form chỉ đọc | đăng nhập (§35b-3) | không trả trường giá; trả `company_status` + catalog của công ty mình |
  | `GET /form-options` · `GET /filter-options` | ô lọc + form | đăng nhập | gom 1 request; `include_ids` + `is_locked` |
  Phân trang, `select` đúng cột, eager load, không N+1 (đo số query trong test). Resource trả `status_text` + `status_color` (bảng 9 màu chuẩn).
- [x] **B5. PHPUnit** `ProductReadApiTest`: mỗi màn lọc đúng (gồm hàng suy ra trạng thái + hàng có dòng thật) · 403 khi thiếu quyền ở `/company` `/entering` (có quyền + không quyền) · không response nào chứa khoá giá (`price`, `cost`, `*_price`) · `/trading` đếm `uncatalogued_count` đúng · số query cố định khi tăng số dòng.

### FE (hrm-client)

- [x] **F1. Menu** nhóm *Hàng hoá* (`subItems`, không `children`) 4 mục, gate theo quyền màn; đếm link trên hub bằng DOM.
- [x] **F2. 4 page danh sách** theo `list-page` skill (`V2BaseDataTable` slot `#cell-<key>`, `SmartFilterPanel`, cấu hình cột, badge `V2BaseBadge` màu do BE): cột/lọc theo `mockup-inventory.md` trừ cột giá và nút [GHI]; bấm Mã mở chi tiết.
- [x] **F3. Page chi tiết** `pages/master-data/products/_id/index.vue`: 2 tầng tab theo mockup, mọi ô `V2Base*` + `disabled`, không nút lưu, `V2Footer` chỉ "Quay lại" về màn đi vào; tiêu đề `Chi tiết hàng hoá: <mã>`.
- [x] **F4. Kiểm Playwright MCP** (đo DOM: số cột, số dòng, badge, footer không đè bảng, không còn chữ "Giá") + spec e2e `e2e/tests/master-data/products-read.*.spec.ts` (có quyền + không quyền). Không tự chạy cả bộ e2e trừ khi user yêu cầu.

## 3. Điểm UI tự chốt theo khuôn (ghi lại, không hỏi)

- Menu: nhóm *Hàng hoá* trong Danh mục chung, trên *Phân loại hàng hóa*.
- 16 điểm mơ hồ mockup (mục 7 `mockup-inventory.md`): bám chốt mới nhất (C5 — Đang kinh doanh không đòi catalog; *Công ty quản lý* = công ty tạo hàng); bỏ các ô lọc mockup chưa nối dữ liệu nếu không có nguồn thật — liệt kê lúc báo xong.

## Nhật ký kiểm (04/10/2026)

| Kiểm | Kết quả |
|---|---|
| PHPUnit `ProductReadApiTest` | **OK 8 tests, 77 assertions** (lọc 4 màn · suy ra trạng thái · catalog 4 cấp + công tắc · 403 đủ ca có/không quyền · không khoá giá · ảnh ERP · số query không đổi 5↔50 dòng) |
| Hồi quy | `ProductCompanyFoundationTest` 5/5 · `BusinessCatalogTreeTest` 12/12 |
| Thời gian API thật (45.890 hàng) | 0,21–0,54 s mọi endpoint; `form-options` 183 KB |
| DB local | INSERT quyền 1652/1653 + gán role 18 (company 1), `cache:clear` — user cho phép 04/10. Migration phân loại KHÔNG chạy (DB đã có cột + đã ghi nhận tên file từ nhánh cũ) |
| Playwright MCP (lead tự đo) | warehouse 14 cột/20 dòng · company 14/20 · entering 12 cột, trạng thái rỗng "Không có hàng hoá nào" · trading 13/20, nhắc cam "Có 27,370 …", badge rgb(22,163,74) · 0 cột chứa "Giá" · bảng 1042 < phân trang 1062 (không đè) · chi tiết: 0 ô sửa được, 7 tab, footer chỉ "Quay lại", không chữ giá · console chỉ 404 ảnh avatar topbar của user e2e |
| e2e (user cho chạy 04/10) | `products-read.api.spec.ts` **4/4 passed** · `products-read-ui.spec.ts` **6/6 passed** (`--no-deps --workers=1 --retries=0`); lượt đầu 1 ca đỏ do lỗi SPEC (`.container-fluid` khớp 2 phần tử ở màn chi tiết — strict mode), sửa sang `body` rồi chạy lại cả file |
| Bẫy gặp | (1) Test đổi người đăng nhập giữa ca: guard + singleton JWT giữ user cũ ⇒ phải `forgetGuards()` + `forgetInstance('tymon.jwt*')`. (2) Ảnh hàng hoá ERP: 167 `/images/noimage.png` + vài `/uploads/...` là đường tương đối ⇒ helper `ErpAsset::url()` |

### Lệch mockup đã tự chốt (UI, theo skill)
- Không cột Hành động/nút "Xem" (skill cấm "Xem"; mã hàng là link mở chi tiết). Không nút Xuất Excel (đợt 2-E).
- 4 ô catalog + công tắc "Chỉ hàng chưa xếp catalog" là dải riêng dưới panel lọc (panel chung không có slot hàng luôn hiện; sửa component chung phải hỏi).
- Bỏ ô lọc "Công ty tạo hàng hoá" (trùng nghĩa Công ty quản lý), "Bảo hành", "Có giá bán"; Trạng thái màn công ty 3 lựa chọn (chưa có "Đang tính giá").
- Thứ tự cột STT · Mã · Ảnh (skill ghim cặp STT+Mã); "Ngày sửa" → "Ngày cập nhật"; ô rỗng để trống.
- Chi tiết: Nhà cung cấp ở tab Quản trị (theo mockup); 🔄 04/10 user đính chính: Hệ số công nghệ ≠ hệ số giá ⇒ ĐÃ THÊM ô *Hệ số công nghệ* (`products.tech_coefficient`) vào tab Quản trị, hàng 4+4+4 (đo: hàng 3905 hiện 1.5, disabled); bỏ dải "chỉ khai được tab Quản trị" (mô tả quyền sửa, đợt này chỉ đọc).

### Checkpoint — 2026-10-04
Vừa hoàn thành: B1–B5, F1–F4; commit api `40d3e9028` · client `e9d46129b`, fast-forward vào nhánh chung `feat/chuyen-doi-hang-hoa` + push (04/10). e2e nằm ngoài 2 repo (chỉ lưu máy).
Đang làm dở: không.
⏳ Tồn cho 2-C: Hệ số công nghệ nằm ở tab Quản trị (dữ liệu THEO CÔNG TY) nhưng đang là cột CHUNG `products.tech_coefficient`, không có trong 4 cột §24b ⇒ khi làm ghi phải chốt: theo công ty (thêm cột vào `product_company_coefficients`) hay giữ chung (chỉ công ty tạo sửa).
Bước tiếp theo: mở đợt 2-C (Ghi) — khảo sát + plan, gồm tồn Hệ số công nghệ theo công ty hay chung.
Blocked:
