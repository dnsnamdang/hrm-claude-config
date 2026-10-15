# Đợt 2-C4 — Tiến độ FE (PHA 2 F1–F3 + E1–E2)

> 08/10/2026 · worktree `wt-chuyen-doi-hang-hoa/hrm-client`, nhánh `feat/p2c4-vong-doi` · commit **`9ca80b35a`** (chưa push/merge).
> Theo `c4-plan.md` (dòng ⚠️: BỎ xoá S3 — V9 = không xoá S3). BE làm song song ở hrm-api (agent khác).

## Đã xong

| Task | Nội dung | File |
|---|---|---|
| F1 | `trading.lifecycle = true`; hằng mới `PRODUCT_COMPANY_SCREEN_STATUS_OPTIONS` (1·2·3·4) cho ô lọc màn công ty — hằng cũ 3 lựa chọn giữ nguyên cho popup catalog; docblock | `utils/product-list-screens.js` |
| F2 | `utils/productLifecycle.js` (mới): `confirmAndRun(vm, kind, product, companyName)` — `$confirm` TRƯỚC lớp tải → `apiDeleteMethod products/{id}` / `apiPutMethod products/{id}/lock|unlock` (payload `{}`) → toast; trả `{ ok, data }` / `{ cancelled }` / `{ status, reload }` (reload khi 404/423). 403/500/504 không toast (interceptor đã toast), 404 "Dữ liệu đã thay đổi, vui lòng tải lại", 422/423 toast nguyên văn `message`. Danh sách: `rowActionsOf` = Sửa → Xóa (danger) → Khóa → Mở khóa theo cờ BE AND quyền 1652; `hasActionsColumn` thêm nhánh `lifecycle`; `runLifecycle` ⇒ bỏ tick + `loadData()` | `utils/productLifecycle.js`, `components/product/ProductListPage.vue` |
| F3 | Chi tiết: `V2Footer menu.delete = canBuild && can_delete` + slot `#custom-actions` Khóa (`warning`, `ri-lock-line`) / Mở khóa (`success`, `ri-lock-unlock-line`); Xóa xong `router.push(backUrl)`, Khóa/Mở khóa tải lại tại chỗ. Form sửa: `onLoadError` 423 ⇒ toast câu BE + `router.replace` chi tiết `?from=` | `pages/master-data/products/_id/index.vue`, `_id/edit.vue` |
| E1 | `products-form-ui`: E4 footer đọc cờ API rồi so `['Sửa','Xóa','Quay lại']`; E12b bỏ `test.skip`, thêm đo menu dòng màn công ty (0 Sửa/Xóa/Khóa, 1 Mở khóa, badge) + footer `['Mở khóa','Quay lại']`. `products-read-ui`: `SCREENS.trading` thêm `Hành động`, docblock 2-C4, 2 ca footer chi tiết so CẢ bộ nút với cờ BE (`expectedFooter`) | e2e |
| E2 | Mới `products-lifecycle.api.spec.ts` (A1–A6, project `api`) + `products-lifecycle-ui.spec.ts` (D1–D3, D5–D11, N1, project `chromium`). `--list` (Node 20) OK: 45 ca / 7 file khi list chung với form-ui + read-ui | e2e |

Kiểm biên dịch: parse template (vue-template-compiler) + script (babel) 5 file — sạch; chạy thử `confirmAndRun` bằng mock (Node) — câu hỏi / đường API / toast / mã trả đúng. CHƯA build Nuxt đầy đủ, CHƯA chạy app, CHƯA chạy e2e.

## Tự chốt khi làm (thuần UI)

- Câu hỏi Xóa (`destroy`) BỎ cụm "ảnh/tài liệu đã tải lên" của T3 vì V9 đổi thành KHÔNG xoá S3 ⇒ dùng câu khảo sát FE: "Xóa hàng hoá <mã>? Hàng hoá và toàn bộ dữ liệu đi kèm bị xóa hẳn, không khôi phục được."
- Popup gỡ (`release`) cũng tiêu đề "Xác nhận xóa" (T3 không nêu tiêu đề riêng); chữ nút "Xóa".
- Nút Sửa ở menu dòng cũng AND quyền 1652 (trước chỉ `can_edit`) — fail-closed, không đổi hành vi khi BE đã tính quyền vào `can_edit`.
- 423 khi bấm Xóa/Khóa ở danh sách / chi tiết ⇒ ngoài toast còn tải lại (cờ trên màn đã cũ).
- `ProductForm` (2-C1) vẫn đặt `loadFailed` cho 423 trước khi `edit.vue` chuyển trang ⇒ khối báo lỗi có thể chớp 1 nhịp; không sửa (plan: form 2-C1/2-C2 không đụng) — đo ở D11.

## Field / route FE dựa vào (đối chiếu BE)

- `DELETE master-data/products/{id}` → `data.mode` (`deleted`|`released`), `data.code`, `data.company_name` (gỡ).
- `PUT master-data/products/{id}/lock` · `/unlock` (body `{}`) → `data.code`.
- Lỗi: `message` ở 422/423 (không đọc `errors`); `GET /{id}/edit` trả 423 + `message` khi khoá.
- List + Detail resource: `can_edit`, `can_delete`, `delete_mode` (`destroy`|`release`), `can_lock`, `can_unlock`, `code`, `company_status`, `status_text`, `status_color`.
- Ô lọc màn công ty gửi `company_status=4` — BE `applyScreen` phải nhận giá trị 4.

## Còn lại (F4 — cần user cho phép ghi DB)

Đo Playwright MCP bảng 4.3 (D1–D11, N1) sau khi BE xong. S1 bỏ (không S3). Chép 2 spec mới + 2 spec sửa về `HRM/e2e/tests/master-data/` khi chốt.

## Rủi ro spec (chưa chạy được)

- A3 chèn 1 dòng `serials` bằng cách tự điền cột NOT NULL không mặc định (đọc `information_schema`) — nếu `serials` có FK khác bắt buộc thì ca đỏ ở bước chèn, sửa giá trị điền.
- D7 bấm ô lọc Trạng thái qua select2 cạnh thẻ `<select>` có option "Ngừng kinh doanh" (mở panel lọc bằng `.filter-toggle-btn` nếu ô chưa dựng).
