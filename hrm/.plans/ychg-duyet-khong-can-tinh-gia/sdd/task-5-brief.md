# Task 5 — FE nút footer "Duyệt không cần tính giá" (ProductForm.vue)

Repo: `hrm-client` (Nuxt 2.14 / Vue 2 / Bootstrap-Vue, Node 14.21.3). Branch `develop`.
Working dir: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client`.

## Global Constraints
- Chỉ dùng component chuẩn `V2Base*` (V2BaseButton…), KHÔNG `<button>`/`<input>`/`class="btn"` thô cho phần thêm mới (xem skill `button-convention`).
- Badge màu + text do BE trả; FE chỉ hiển thị. Số en-US.
- Dùng Playwright qua `http://127.0.0.1:3000` (KHÔNG localhost) để kiểm.

## Đã có từ BE (Task 3)
- `tempForm` meta trả `can_approve_no_price` (bool).
- Endpoint `POST {ASKING}/{requestId}/temp-products/{productId}/approve-no-price` → trả `{product_id, company_status:9}`.
- `tempStatus` của dòng có thể = 9.

## Files
- Modify: `components/product/form/ProductForm.vue`
  - Footer `mode==='temp-approve'` (~dòng 72-105): cạnh nút "Đồng ý"/"Không duyệt".
  - Nơi load meta tempForm (~dòng 365-374): map `can_approve_no_price`.
  - Vùng handler submit temp (~dòng 427-469).

## Steps

**Step 1 — Thêm nút** trong footer (chỉ chế độ `temp-approve`):
- `V2BaseButton` variant primary, size sm, chữ **"Duyệt không cần tính giá"**.
- `v-if="tempMeta.can_approve_no_price && tempStatus !== 9"` (đã là 9 thì ẩn, giống "Đồng ý" ẩn khi đã 7).
- `:interactable="ready && !saving"` (bám đúng cờ nút "Đồng ý" đang dùng).
- Lề/icon theo convention (vd `mr-2 mb-2`). Thêm icon info (`ri-information-line`) + `b-popover` giải thích ngắn 2 trường hợp (TH1 vật tư giá 0; TH2 hàng tạm lấy báo giá trúng thầu) — bám mẫu info-icon đang dùng ở các nút kế bên (xem skill `info-icon-tooltip`).

**Step 2 — Handler** `tempApproveNoPrice()`:
- Confirm nhẹ (`$confirm` như nút "Đồng ý"): "Duyệt không cần tính giá cho hàng {code}? Hàng sẽ lên 'Đang kinh doanh' khi phiếu được duyệt, bỏ qua hỏi giá và tính giá."
- Gọi `apiPostMethod(tempUrl('/approve-no-price'))` (bám đúng cách `tempSubmit('approve')` build URL: `${ASKING}/${requestId}/temp-products/${productId}${suffix}`).
- Thành công: `markFormSaved()` + điều hướng về chi tiết phiếu (giống luồng approve).
- Trong `loadTempForm`, destructure thêm `can_approve_no_price` vào `tempMeta`.

**Step 3 — Kiểm Playwright** (`http://127.0.0.1:3000`): (HRM chạy local qua skill `run-hrm`; nếu server chưa chạy, nêu trong report thay vì tự dựng nếu không thể.)
- Mở trang quyết định 1 hàng tạm (status 6): xác nhận hiện 3 nút (Đồng ý / Duyệt không cần tính giá / Không duyệt).
- Bấm nút mới → confirm → quay về phiếu; dòng chuyển nhãn + badge "Duyệt không cần tính giá".
- Chụp màn hình, XEM ảnh (ảnh trống = lỗi).

**Step 4 — Tự kiểm convention**: `grep -n '<button \|<input \|class="btn ' components/product/form/ProductForm.vue` cho phần thêm mới phải không dính component thô.

**Step 5 — Commit** (`develop`):
`feat(ychg): third footer action 'Duyệt không cần tính giá' on temp-approve form`
Trailer: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

## Report contract
Full report vào report file. Nêu: các đoạn code thêm, kết quả Playwright (kèm nhận xét ảnh), concerns (nếu server không chạy được thì nói rõ). Trả về CHỈ status + commit + 1-dòng kiểm + concerns. KHÔNG dispatch subagent.
