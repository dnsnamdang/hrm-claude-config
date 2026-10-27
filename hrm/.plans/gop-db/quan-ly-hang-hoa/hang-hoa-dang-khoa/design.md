# Hàng hoá đang khoá — design

> Ngày: 22/10/2026 · Phụ trách: @namdangit · Trạng thái: **ĐÃ CODE 22/10 (user "Làm, native")** — chưa commit; ruling lúc làm ở §7.
> Nhánh làm việc: checkout chính `gop_db` (hrm-api, hrm-client, ERP/TanPhatDev) — xem memory *chuyen-doi-hang-hoa-nhanh-chung*.
> DB local: `hrm_erp_21_10_prod` (dump prod 21/10).

## 0. Yêu cầu gốc

> Màn **Hàng hoá đang khoá**: tổng hợp các hàng hoá đang khoá theo công ty đang làm việc của user.
> - Khảo sát màn ERP: Thùng rác.
> - Cho phép khôi phục về trạng thái **Đang kinh doanh** nếu có đầy đủ giá bán, nếu không sẽ khôi phục về trạng thái
>   **Đã nhập thông tin**.

## 1. Khảo sát

### 1.1 ERP — Thùng rác

- Route `GET /products/deleted` (`products.deleted`, quyền web *Sửa hàng hóa*) → `resources/views/products/deleted.blade.php`.
  Datatable gọi `products.searchData` với `type = deleted` ⇒ mọi hàng `products.status = 0`, **không chia công ty**.
- Khôi phục: `GET /products/{id}/restore` (quyền web *Khôi phục hàng hóa*) — chỉ `status = 1`, không xét giá, không đụng
  `deleted_at`. Route này **đã bị chặn ở 2-D1** (`productMovedToHrm:product-show`), ghi chú trong code "Khôi phục đã chuyển
  sang HRM" — nhưng HRM chưa có màn nào làm việc đó.
- Nút "Thùng rác" ở `products/list.blade.php` vẫn mở (route `products.deleted` chưa gắn `productMovedToHrm`).

### 1.2 HRM hiện có

- 5 màn danh sách dùng chung `components/product/ProductListPage.vue`, khác nhau khai ở `utils/product-list-screens.js`;
  BE lọc từng màn ở `ProductService::applyScreen()`.
- Khoá theo công ty = `product_company_coefficients.status = 4` (Ngừng kinh doanh, 2-C4). `ProductLifecycleService::lock()`
  3 → 4, `unlock()` 4 → 3 (không xét giá). Quyền ghi: **Xây dựng thông tin hàng hoá**.
- "Đã nhập thông tin" = `status = 1` + `info_entered_at` NOT NULL (commit `032d2571c`, 21/10).
- `Product` KHÔNG dùng `SoftDeletes` (ERP bỏ qua `deleted_at`; 175 hàng đang bán còn `deleted_at`).

### 1.3 Số liệu `hrm_erp_21_10_prod`

| Đo | Kết quả |
|---|---|
| Dòng `pcc.status = 4` | **0** |
| `products.status = 0` | **17.596** (16.107 có `deleted_at`) — Cty 1: 17.502 · Cty 4: 72 · Cty 9: 21 · `company_id` NULL: 1 |
| Hàng status 0 có dòng trạng thái công ty (≠ NULL) | 0 (chỉ có 298 dòng hệ số cũ `status NULL`) |
| Đủ 6 loại giá > 0 mọi ĐVT (giá công ty chủ) | 503 |
| Chỉ có Bán lẻ > 1 đ | 1.918 |
| Không có Bán lẻ thật (0 / 1 đ) | 15.519 |
| Chưa có Loại SP (`product_type_id` NULL) | 13.509 |
| Trùng Tên + Model với hàng `status = 1` | 185 |
| Trùng mã với hàng `status = 1` | 0 |

## 2. Quyết định đã chốt (22/10/2026)

| # | Câu hỏi | Chốt |
|---|---|---|
| K1 | Màn gồm hàng nào | **Cả 2 nguồn**: (A) Ngừng KD `pcc.status = 4` của công ty đang làm việc · (B) ERP đã xoá `products.status = 0` có `products.company_id` = công ty đang làm việc |
| K2 | "Đủ giá bán" | **Mọi ĐVT có đủ 6 loại giá > 0** tại công ty đang làm việc; Bán lẻ 1 đ = chưa có giá |
| K3 | Thiếu phân loại | Điều kiện về Đang KD = đủ giá **và** đủ phân loại; thiếu ⇒ Đã nhập thông tin |
| 🔄 Đ2 | (23/10/2026, `chuyen-kd-khong-tinh-gia`) | **K2 + K3 chỉ còn áp cho hàng ERP đã xoá.** Hàng khoá theo công ty (Ngừng KD) khôi phục LUÔN về Đang kinh doanh, không xét giá / Loại SP — `ProductRestoreRule::readySql()` |
| K4 | Quyền | Xem: không gate. Khôi phục: **Xây dựng thông tin hàng hoá**. Không quyền mới, không seeder |
| K5 | Hàng loạt | **Từng dòng + tick nhiều dòng**, trần 100 mã/lượt |
| K6 | Trùng Tên + Model | **Cảnh báo, vẫn cho** khôi phục |
| K7 | Các màn khác | **Mọi màn còn lại loại bỏ hàng đang nằm ở màn Hàng hoá đang khoá**; khôi phục chỉ làm ở màn mới ⇒ gỡ nút Mở khoá rải rác |
| K8 | ERP Thùng rác | **Chuyển hướng sang HRM** |

## 3. Thiết kế

### 3.1 Màn danh sách

- Route FE `/master-data/products/locked`, page `pages/master-data/products/locked.vue` `extends ProductListPage`,
  `layout: 'default-sidebar'`, `productScreen: 'locked'`.
- Menu `components/subsystem-menu/master-data.js` › *Hàng hoá, vật tư* › mục **"Hàng hoá đang khoá"** ngay sau
  "Hàng đang kinh doanh", không `isShow` (khai trong `subItems`).
- BE: thêm `SCREEN_LOCKED` vào `ProductService::applyScreen()`:
  - (A) `companyStatusSql = 4`, **hoặc**
  - (B) `products.status = 0 AND products.company_id = :company` AND không có dòng pcc của công ty chủ ở trạng thái
    hàng tạm 6/7/8 (hàng tạm đã xoá mềm vẫn "không còn ở đâu").
- Cột: `CORE_COLUMNS` + `OPTIONAL_COLUMNS` (tắt sẵn) + mới:
  - **Nguồn khoá** — `stopped` "Ngừng kinh doanh" / `erp_deleted` "ERP đã xoá" (badge).
  - **Ngày khoá** — `updated_at` của dòng pcc (A) / của `products` (B).
  - **Khôi phục về** — dự kiến `Đang kinh doanh` / `Đã nhập thông tin` + dòng lý do khi thiếu
    ("Thiếu giá Đại lý cấp 2 (Cái)", "Chưa đủ phân loại"). Tính bằng cùng hàm của luật §3.2.
  - **⚠ trùng** — biểu tượng cạnh tên khi có hàng `status = 1` khác cùng Tên + Model; tooltip nêu mã hàng đó.
- Mặc định hiện: lõi + Nguồn khoá + Ngày khoá + Khôi phục về.
- Ô lọc: Nguồn khoá · Khôi phục về · phân loại · thương hiệu · hãng SX · xuất xứ · model.
- Xuất Excel (quyền *Xuất excel danh sách hàng hoá*) slug `hang_hoa_dang_khoa`, khai registry BE `products_locked`.

### 3.2 Luật khôi phục

Một hàm BE `ProductLifecycleService::restore(array $productIds)` dùng chung cho từng dòng và hàng loạt.

1. `assertCanWrite()` (quyền Xây dựng thông tin hàng hoá) — không quyền ⇒ 403.
2. Tối đa 100 id/lượt (422 nếu vượt). Trong transaction, `lockForUpdate` `products` + dòng pcc như `lock()`.
3. Mỗi hàng phải đang thuộc màn (nguồn A hoặc B của **công ty đang làm việc**); không thì **bỏ qua** + lý do
   ("Hàng không còn ở trạng thái khoá" / "Hàng không thuộc công ty").
4. Đích:
   - **Đủ giá** = mọi ĐVT của hàng có đủ 6 `price_type_id` 1–6 với `price > 0` tại công ty đang làm việc, riêng Bán lẻ
     phải > 1 đ.
   - **Đủ phân loại** = đủ 5 ô phân loại như Phase 6 (`p6-plan.md`): Tính chất · Nhóm chức năng · Nhóm SP suy từ
     Loại SP ⇒ thực tế kiểm **Loại SP** (`product_type_id` còn hiệu lực) **+ Đặc tính**.
   - Cả hai ⇒ **3 Đang kinh doanh**; thiếu ⇒ **1** + `info_entered_at` (giữ mốc cũ; NULL thì gán `now()`) ⇒
     *Đã nhập thông tin*.
5. Nguồn B thêm: `products.status = 1`, `products.deleted_at = NULL`, `updated_by`. Dòng pcc của công ty: chưa có ⇒
   INSERT (coef 1, như G4); có dòng hệ số cũ `status NULL` ⇒ UPDATE (giữ `coefficient`).
6. `history()->logStatus(product, company, từ, đến)`; nguồn B ghi `từ = null` kèm ghi chú "Khôi phục hàng ERP đã xoá".
7. Kết quả: `{trading: [...], entered: [...], skipped: [{id, code, reason}]}` ⇒ toast "X mã về Đang kinh doanh, Y mã về
   Đã nhập thông tin, Z mã bỏ qua" + danh sách lý do.

API: `POST /products/restore` body `{ids: []}` (từng dòng cũng gọi đường này với 1 id).
`PUT /products/{id}/unlock` cũ chuyển sang gọi `restore([$id])` — không còn đường 4 → 3 không xét giá.

FE: cột Hành động + ô tick + thanh "Khôi phục" chỉ dựng khi có quyền (fail-closed như `rowActions`). Hộp xác nhận nêu
đích dự kiến; có hàng ⚠ trùng thì nhắc thêm tên mã trùng. Logic gọi API + toast đặt ở `utils/productLifecycle.js`.

### 3.3 Các màn khác loại bỏ hàng đang khoá

| Màn | Hiện tại | Sau |
|---|---|---|
| Kho dữ liệu | bỏ `products.status = 0` | bỏ thêm hàng có `status = 4` tại công ty đang làm việc |
| Dữ liệu hàng hoá công ty | gồm status 4 | bỏ status 4; bỏ option 4 ở ô lọc Trạng thái |
| Nhập thông tin / Đang KD / Hàng tạm | không chứa | giữ |

- Gỡ nút **Mở khoá** ở menu dòng (Dữ liệu công ty) và footer màn chi tiết; cờ `can_unlock` thay bằng `can_restore`.
  ⚠️ Chỉnh lúc viết plan (22/10, theo HRM CLAUDE.md "hành động ở chi tiết phải khớp danh sách"): footer chi tiết của hàng
  đang khoá hiện nút **Khôi phục** (cùng luật, cùng cờ `can_restore` với dòng ở màn mới) thay vì gỡ trắng.
- Màn chi tiết hàng đang khoá vẫn mở được (link từ màn mới); toast 423 khi sửa đổi câu hướng dẫn sang
  "khôi phục ở màn Hàng hoá đang khoá".
- Nút **Khoá** ở Đang KD giữ nguyên — khoá xong hàng chuyển sang màn mới.

### 3.4 ERP

- `ProductMovedToHrm`: thêm khoá `'product-locked' => '/master-data/products/locked'`.
- `routes/web.php`: route `products.deleted` gắn `productMovedToHrm:product-locked`; nút Thùng rác ở
  `products/list.blade.php` giữ chữ, trỏ `buildHrmUrl('product-locked')`.

## 4. Kiểm thử

- **PHPUnit (hrm-api, MasterData)** — KHÔNG chạy lên DB sẽ đưa lên prod (memory *phpunit-chay-tren-db-env-de-lai-rac*):
  A đủ giá + đủ phân loại ⇒ 3 · A thiếu giá ⇒ 1 + entered · A thiếu phân loại ⇒ 1 · B đủ ⇒ 3 + `products.status 1` +
  `deleted_at NULL` · B có dòng hệ số cũ ⇒ UPDATE giữ coef · B chưa có dòng ⇒ INSERT · Bán lẻ 1 đ = thiếu giá ·
  không quyền ⇒ 403 · công ty khác ⇒ bỏ qua · > 100 id ⇒ 422 · `unlock` cũ đi qua luật mới · màn
  company/warehouse không còn hàng khoá · màn locked không chứa hàng tạm đã xoá.
- **Playwright MCP** (bắt buộc trước khi báo xong): đo DOM số dòng khớp API, cột Khôi phục về + lý do, ⚠ trùng, toast
  hàng loạt, có quyền / không quyền (không có cột Hành động, không ô tick), màn Dữ liệu công ty không còn status 4,
  footer chi tiết không còn Mở khoá; ERP bấm Thùng rác ⇒ sang HRM.
- **e2e**: thêm spec `products-locked` + sửa spec lifecycle cũ (Mở khoá); chỉ chạy khi user yêu cầu, `--workers=1`.

## 5. Phạm vi source (khi có lệnh "làm")

- hrm-api: `ProductService`, `ProductLifecycleService`, controller + route `restore`, `ProductListResource`
  (cột mới), `ExportColumnRegistry`, test.
- hrm-client: `pages/master-data/products/locked.vue`, `utils/product-list-screens.js`, `ProductListPage.vue`
  (cờ restore), `subsystem-menu/master-data.js`, `utils/productLifecycle.js`, footer chi tiết, edit.vue (câu 423).
- ERP: `app/Http/Middleware/ProductMovedToHrm.php`, `routes/web.php`, `resources/views/products/list.blade.php`.
- **Không migration, không seeder, không quyền mới, không ghi DB.**

## 6. Rủi ro / ghi chú

- Công ty 1 sẽ thấy ~17.500 dòng — phân trang server như các màn khác; cột "Khôi phục về" tính theo trang (subquery
  đếm giá trên tập trang hiện tại, không trên cả bảng). Lọc theo "Khôi phục về" cần subquery trên toàn tập ⇒ đo thời
  gian trên `hrm_erp_21_10_prod`; chậm thì cân nhắc bỏ ô lọc này (hỏi lại).
- Hàng `products.company_id` NULL (1 mã) không công ty nào thấy — chấp nhận.
- Nguồn B đổi `products.status` là thay đổi TOÀN CỤC (hàng hiện lại ở popup ERP / công ty khác) — đúng nghĩa khôi
  phục của ERP; chỉ công ty chủ làm được.

## 7. Điều chỉnh lúc làm (22/10/2026 — chi tiết `progress.md`)

- **Đủ phân loại = CHỈ Loại SP** (bỏ Đặc tính): câu K3 user trả lời ghi đúng "Loại SP trống"; DB prod 21/10 có 0/30.279 hàng
  mang Đặc tính ⇒ xét Đặc tính là 100% hàng về Đã nhập thông tin. Số đo sau đổi: 27/17.502 mã ERP đã xoá của Cty 1 đủ điều kiện.
- **Màn Dữ liệu công ty / Nhập thông tin / Đang KD cũng loại `products.status = 0`** (K7) — trước đây hàng ERP đã xoá có
  dòng pcc vẫn hiện ở màn công ty. Prod 21/10: 0 dòng như vậy.
- Footer chi tiết hàng đang khoá: nút **Khôi phục** (cờ `can_restore`, khớp dòng ở màn mới); xong ⇒ về màn đi vào.
- `PUT /products/{id}/unlock` giữ route nhưng đi qua luật Khôi phục (trả `{trading, entered, skipped}`).
- Lịch sử: action `unlock` (nhãn "Mở khóa" có sẵn) + ghi chú "Khôi phục" / "Khôi phục hàng ERP đã xoá" — không sửa
  `CatalogHistoryService` dùng chung.
- Câu 423 `ProductCompany::LOCKED_MESSAGE` đổi thành "Hàng hoá đang khoá, vui lòng khôi phục ở màn Hàng hoá đang khoá trước
  khi cập nhật."
- Hàng về 3 cũng gắn `info_entered_at` nếu chưa có.
