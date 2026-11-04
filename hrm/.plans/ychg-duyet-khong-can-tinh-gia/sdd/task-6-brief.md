# Task 6 — FE nhận diện trạng thái `9` trên phiếu YCHG (Cha + Con)

Repo: `hrm-client` (Nuxt 2.14 / Vue 2 / Bootstrap-Vue, Node 14.21.3). Branch `develop`.
Working dir: `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-client`.

## Global Constraints
- Chỉ dùng component chuẩn `V2Base*` cho phần thêm mới (xem skill `button-convention`). KHÔNG `<button>`/`<input>`/`class="btn"` thô.
- Badge màu + text do BE trả (`company_status_text` / `company_status_color`); FE CHỈ hiển thị, KHÔNG hardcode nhãn/màu status 9. Số en-US.
- Dùng Playwright qua `http://127.0.0.1:3000` (KHÔNG localhost) để kiểm.

## Đã có từ BE (Task 1/3)
- `row.company_status` có thể = `9`; `row.company_status_text` = "Duyệt không cần tính giá"; `row.company_status_color` = `#7C3AED`.
- Dòng `9` reopen được (gate nhận 9) → bấm "Sửa" mở lại trang quyết định; đổi ý Đồng ý ↔ Duyệt không cần tính giá ↔ Không duyệt.
- Nút Duyệt phiếu bật khi 100% dòng (Cha + Con) đã rời `6` (status 9 tính là "đã quyết định").

## Files
- Modify: `components/sale/price-asking/PriceAskingRequestForm.vue`
  - Nút/nhãn dòng Cha (~254-269).
  - Mirror dòng Con (~309-325).
  - `openTempApprove` / readonly guard (~754-758).
- Kiểm bằng Playwright.

## Steps

**Step 1 — Nhãn nút + badge (Cha và Con)**:
- Nhánh `v-else` (`Number(row.company_status) !== 6`) đã hiện "Sửa" cho 7/8 → `9` TỰ rơi vào "Sửa". **XÁC NHẬN** không cần đổi logic điều kiện nút (đọc kỹ v-if/v-else, nếu có check cứng `=== 7 || === 8` thì PHẢI thêm 9; nếu chỉ `!== 6` thì OK — ghi rõ bạn thấy gì).
- Badge trạng thái dòng phải dùng `company_status_text`/`company_status_color` BE (không map cứng). Nếu badge đang map cứng theo id status ở FE (switch/object), PHẢI thêm nhánh 9 HOẶC tốt hơn là đọc text/color BE. Ghi rõ cơ chế badge hiện tại trong report.
- Làm Y HỆT cho dòng Con (`child.company_status`, ~309-325).

**Step 2 — Tooltip nút "Sửa"** (~267, ~323): câu mô tả hiện nhắc "Đồng ý ↔ Không duyệt" → bổ sung lựa chọn thứ 3, ví dụ "Mở lại form để đổi quyết định: Đồng ý ↔ Duyệt không cần tính giá ↔ Không duyệt". Chữ xám, KHÔNG tô đỏ.

**Step 3 — `openTempApprove` / readonly guard** (~754-758): hàm điều hướng dùng chung — `9` KHÔNG cần nhánh riêng. XÁC NHẬN dòng `9` vẫn mở lại form được (readonly guard nếu có chỉ nên chặn status 8 ở chế độ readonly; xác nhận `9` KHÔNG bị chặn nhầm). Nếu guard có liệt kê cứng status cho phép mở → thêm 9. Ghi rõ.

**Step 4 — Kiểm Playwright** (`http://127.0.0.1:3000`): (HRM chạy local qua skill `run-hrm`; nếu server chưa chạy, nêu rõ trong report thay vì tự dựng nếu không thể.)
- Mở phiếu YCHG ở "Chờ PTKD duyệt" có ≥1 dòng đã set `9` (có thể set qua endpoint Task 3 hoặc qua nút Task 5):
  - Badge dòng hiển thị đúng chữ "Duyệt không cần tính giá" + màu tím `#7C3AED`.
  - Nút "Sửa" của dòng `9` mở lại được trang quyết định.
  - **Nút "Duyệt" phiếu SÁNG** khi mọi dòng Cha + Con đã rời `6` (gồm dòng `9`).
- Chụp màn hình, XEM ảnh (ảnh trống = lỗi).

**Step 5 — Tự kiểm convention**: `grep -rn '<button \|<input \|class="btn ' components/sale/price-asking/PriceAskingRequestForm.vue | grep -v V2Base` cho phần thêm mới phải rỗng.

**Step 6 — Commit** (`develop`):
`feat(ychg): recognize status 9 (approved-no-price) on request detail for parent + children`
Trailer: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

## Report contract
Full report vào report file. Nêu: cơ chế badge/nút hiện tại (map cứng hay đọc BE), các đoạn code sửa, kết quả enable nút Duyệt phiếu, kết quả Playwright (kèm nhận xét ảnh), concerns (nếu server không chạy được thì nói rõ). Trả về CHỈ status + commit + 1-dòng kiểm + concerns. KHÔNG dispatch subagent.
