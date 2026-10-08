# Đợt 2-C2 — Tiến độ FE (PHA 2 + E1–E2)

> 08/10/2026 · worktree `wt-chuyen-doi-hang-hoa/hrm-client`, nhánh `feat/p2c2-lay-ve` · commit **`3a9eae100`** (chưa push/merge).

## Đã xong

| Task | Nội dung | File |
|---|---|---|
| F1 | Kho dữ liệu: cờ `takeBack`; ô tick chỉ dòng `can_take_back` (tick đầu bảng chỉ tick các dòng đó); trần 100 + toast + `tickRev`; thanh "Đã chọn N · Lấy về công ty · Bỏ chọn"; action dòng `take_back` (icon `ri-download-2-line`); `$confirm` → lớp tải → `POST products/take` → toast taken/skipped (≤ 5 mã + "và x mã khác") → bỏ tick → `loadData()`; cột Hành động + ô tick chỉ khi có 1652; đọc `?usage=unused` lúc khởi tạo (1 lần gán + bỏ lượt watcher ⇒ 1 request) | `utils/product-list-screens.js`, `components/product/ProductListPage.vue`, `pages/master-data/products/warehouse.vue` |
| F2 | Màn Nhập thông tin: nút secondary "Kho dữ liệu" (`ri-database-2-line`) trước Tạo mới, cùng gate `canCreate` | `ProductListPage.vue`, `pages/master-data/products/entering.vue` |
| F3 | Form: `edit_scope` từ `/edit`; `admin` ⇒ tab Quản trị mở trước, dải báo `.product-scope-notice`, tab Thông tin `lockedKeys` (opacity .4, vẫn bấm được) hiện chỉ đọc bằng 5 `ProductTab*` (`GET products/{id}` song song form-options, vùng `.product-form__readonly`), 12 component form 2-C1 không render; Hệ số công nghệ `disabled` (`adminOnly`); Lưu ⇒ `PUT …/admin-data` body `toAdminPayload` = đúng 6 khoá (không `catalogs`, không `tech_coefficient`); lỗi 422 luôn mở tab Quản trị | `ProductForm.vue`, `ProductFormAdmin.vue`, `productFormModel.js`, `ProductParentTabs.vue` |
| F4 | Không sửa — Sửa ở menu dòng + footer chi tiết theo `can_edit` BE | — |
| E1 | `products-read-ui.spec.ts`: bộ cột warehouse thêm `Hành động`; `allowed` warehouse `/Lấy về công ty\|Lấy về/`; đếm nút "Kho dữ liệu" (1 ở entering, 0 màn khác) | e2e |
| E2 | Viết mới `products-take.api.spec.ts` (A1–A7, project `api`) + `products-take-ui.spec.ts` (K0, K1, K3–K7, U1–U5, N1); `--list` OK (Node 20: take-ui 10 ca chromium, take.api 7 ca project api, read-ui 8 ca) | e2e |

Kiểm biên dịch: parse template (vue-template-compiler) + script (babel) 8 file — sạch. CHƯA build Nuxt đầy đủ, CHƯA chạy app.

## Spec e2e đã đổi (bản sao `wt-chuyen-doi-hang-hoa/e2e`, không nằm trong git — chép về `HRM/e2e` khi chốt)

- sửa `tests/master-data/products-read-ui.spec.ts`
- mới `tests/master-data/products-take.api.spec.ts`
- mới `tests/master-data/products-take-ui.spec.ts`
- `products-form-ui.spec.ts` E2: giữ nguyên (không quyền ⇒ vẫn 0 cột Hành động)

## Còn lại (F5 — cần user cho phép ghi DB)

Đo Playwright MCP bảng 3.3 (K1–K7, U1–U6, N1) + K0. Chưa bấm Lấy về / Lưu trên app.

## Ghi chú / ngoài luồng

- `ProductForm.save()` (2-C1) không bật `$safeLoadingStart` (skill button-convention 6b) — giữ nguyên, cả nhánh admin-data cũng theo; note để sửa chung.
- Tên công ty trong câu hỏi xác nhận lấy từ store `company_roles` × `current_company`; toast dùng `company_name` BE trả.
- Mở Kho bằng `?usage=unused`: query nằm lại trên URL; bấm Làm mới tắt công tắc nhưng F5 trang sẽ bật lại (chấp nhận).
