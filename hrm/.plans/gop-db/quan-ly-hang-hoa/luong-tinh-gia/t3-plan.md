# Plan T3 — Yêu cầu hỏi giá (YCHG) — 11/10/2026

> Nguồn: `design.md` §1, §2, §4, §6–§8, §12 (T3) · `ton.md` Q1–Q20, D3, D7, D8, D10 · mockup đã duyệt (`sc-hg`, `sc-hgf`; ảnh `anh-mockup/t0-hg-*.png`)
> · khảo sát ERP `khao-sat-be-erp.md` §1.1/§3.1, `khao-sat-fe-erp.md` §1.1, `khao-sat-hrm.md` §3/§4.
> ✅ **User cho "LÀM" 11/10/2026** — đúng phạm vi mục 4 (không migration/seeder; sửa thêm lệnh close-stale `--by`).
> Môi trường: worktree `wt-chuyen-doi-hang-hoa`, nhánh con `feat/t3-ychg` từ nhánh chung `feat/chuyen-doi-hang-hoa`; DB dev `hrm_erp_giacty`. **Không migration** (T2 đã đủ bảng).

## 0. Hiện trạng (đo 11/10)

- Chưa có route / controller / page YCHG ở cả 2 repo ⇒ dựng mới.
- Model T2 `Modules/MasterData/Entities/PriceCalculation/`: `PriceAskingRequest` (hằng 1–10, `STATUS_TEXT/COLOR`, `scopeAsking`), `PriceAskingRequestGroup` (5/1/7/4/9/6, `CLOSED_STATUSES`, `isClosed()`), `PriceAskingRequestProduct` (`parent_id`, `group_id`, unit NULL = mọi ĐVT), `PriceAskingRequestApproveHistory` (`type` chuỗi). Đều `extends Model` + `$guarded` ⇒ service tự gán company/created_by/updated_by.
- Mã phiếu: ERP `"PYCHG-" . generateCode(5, $id)` sau khi lưu ⇒ HRM dùng `generateCode()` (`app/Helper/FormatHelper.php:98`), cùng công thức để nối tiếp dãy cũ.
- XNK phân công: `Services/PriceCalculation/XnkAssignmentResolver::resolve(brand, manufacture, company)` (T2) — null = chưa phân công.
- Khuôn T1 (mới nhất): route `Modules/MasterData/Routes/api.php` prefix `/v1/master-data`, controller mỏng `ApiController`, validate trong service (báo đồng thời), gate `checkPermission:`.
- Quyền theo công ty: `isCurrentEmployeeHasPermission` chỉ xét công ty đang làm việc. Phiếu luôn thuộc công ty đang làm việc của người lập (Q4) và danh sách lọc theo công ty đang làm việc ⇒ thao tác chỉ được trên phiếu của công ty đang làm việc (phiếu công ty khác ⇒ 403) ⇒ dùng thẳng `isCurrentEmployeeHasPermission`.
- Thông báo: chép khuôn `ProductPriceNotifier` (`approverInfoIds($companyId)` theo quyền tại công ty, `send()` nuốt lỗi, gửi sau commit).
- FE: màn hàng hoá dùng chung `components/product/ProductListPage.vue` (toolbar `#actions` L113-152; tick dòng chỉ bật ở company/warehouse — `canSelectRows` L711). Popup chọn hàng có sẵn `components/product/form/ProductItemPickerModal.vue` (`open({multiple, excludeIds})`, `@pick`) — cần lọc theo trạng thái công ty 1/3. Bảng nhóm La Mã: khuôn `pages/assign/handover/components/HandoverItemsTable.vue` (`toRoman`). Danh sách bung dòng con: khuôn `pages/finance/borrow-stocks/index.vue` (`V2BaseDataTable` slot `row-expand`). Menu: `sale-hub.js:165` `'YC hỏi giá'` chưa link (giữ nhãn — là menuKey).

## 1. Tự chốt theo design/ERP (không hỏi — ghi để duyệt)

| # | Chốt |
|---|---|
| A1 | Chọn hàng: hàng có `pcc.status` ∈ {1, 3} tại công ty đang làm việc (Q15). Hàng 2/5 (đã trong YCHG khác) không chọn được. Hàng 3 đang nằm trong YCHG mở khác ⇒ **cảnh báo** "đang có người hỏi giá ở PYCHG-…" (như ERP), không chặn |
| A2 | Gom nhóm theo (thương hiệu × hãng) của hàng, tính lại mỗi lần Lưu ở trạng thái 3/8; nhóm sắp theo tên; STT La Mã / 1-2-3 |
| A3 | Gửi: kiểm mọi nhóm có XNK phân công (resolver) — thiếu ⇒ 422 nêu tên từng hãng, không lưu gì; ≥ 1 hàng. Ghi `xnk_employee_id` lúc gửi (tra cứu); phiếu 3/8 ⇒ 2, `received_time`; hàng mới 1 ⇒ 2 |
| A4 | PTKD Duyệt (ghi chú tuỳ chọn) ⇒ phiếu 10, mọi nhóm ⇒ 5. PTKD Từ chối (lý do bắt buộc) ⇒ 8, hàng mới 2 ⇒ 1, nhóm giữ NULL |
| A5 | XNK (1663 + là XNK phân công HIỆN HÀNH của nhóm — D3): Duyệt nhóm (ghi chú tuỳ chọn) 5 ⇒ 1 · Không có giá (lý do bắt buộc) 5 ⇒ 9 · Huỷ duyệt (lý do bắt buộc) 1 ⇒ 6 khi nhóm chưa có YCTG. Nhóm đóng 9/6 ⇒ hàng mới của nhóm 2 ⇒ 1 |
| A6 | Mọi nhóm đóng ⇒ phiếu 4 nếu có nhóm 4, không thì 9 (T3 chỉ sinh ra 9; nhánh 4 để T5) |
| A7 | Thao tác chuyển trạng thái khoá dòng phiếu (`lockForUpdate`) + kiểm lại trạng thái trong transaction ⇒ 2 người bấm cùng lúc chỉ 1 người thành công, người sau nhận **409** "Trạng thái đã bị thay đổi. Vui lòng load lại trang" (câu chuẩn QA #11549) |
| A8 | Danh sách: phiếu công ty đang làm việc; 3 / 8 của người khác ẩn (Q-mockup 7); lọc trạng thái phần đầu "Đang hỏi giá" = `IN (1,5,7,10)` |
| A9 | Lịch sử duyệt ghi `price_asking_request_approve_histories` (type: Gửi yêu cầu · PTKD duyệt · PTKD từ chối · XNK duyệt · Không có giá · Huỷ duyệt), log nhóm có `group_id` |
| A10 | Nút "Lập YCTG" ở nhóm 1 thuộc T4 — T3 chưa hiện. Drill kết quả (T5), In (T6) chưa làm |
| A11 | YCHG không cần quyền để lập / xem (Q11); route ghi gate `checkPermission` cho 1662 / 1663; lập-sửa-xoá chỉ kiểm người lập trong service |

## 2. Tồn — ✅ chốt đủ 11/10/2026 (Quyết định đã chốt)

| # | Câu | Chốt |
|---|---|---|
| T3-Q1 | Chữ nút lệch skill | ✅ **theo skill**: form Lưu nháp · Lưu và gửi duyệt; PTKD Duyệt · Từ chối (danger, lý do bắt buộc); XNK Duyệt · Không có giá (danger, lý do bắt buộc) · Huỷ duyệt (danger, lý do bắt buộc) |
| T3-Q2 | Nút trên dòng nhóm ở danh sách | ✅ **danh sách chỉ điều hướng**: dòng nhóm hiện XNK + trạng thái + "Chờ … duyệt"; người có việc thấy 1 nút icon "Xử lý" ⇒ mở chi tiết, cuộn tới nhóm. Duyệt / Không có giá / Huỷ duyệt nằm ở dòng nhóm trong màn chi tiết. (T4: "Lập YCTG" là điều hướng ⇒ được ở danh sách) |
| T3-Q3 | Nút "Lập yêu cầu hỏi giá" ở màn hàng | ✅ **tick hàng rồi nạp sẵn**: bật tick dòng ở màn Nhập thông tin + Đang KD; có tick ⇒ form nạp sẵn (đã gom nhóm), không tick ⇒ form trống; hàng 2/5 bị loại kèm câu báo. Nới `canSelectRows` của `ProductListPage` ⇒ kiểm lại màn Dữ liệu công ty + Kho |
| T3-Q4 | Sửa / Xoá | ✅ **người lập, trạng thái 3 Đang tạo hoặc 8 Không duyệt**; xoá phiếu 8 không đổi trạng thái hàng; còn lại ẩn nút + BE 409 |
| T3-Q5 | Thông báo | ✅ **theo skill**: Gửi ⇒ 1662 `[YCHG] Chờ duyệt: PYCHG-x. Người lập: …` · PTKD duyệt ⇒ XNK từng nhóm `[YCHG] Chờ duyệt: PYCHG-x. Nhóm: …` · PTKD từ chối ⇒ người lập `Từ chối … Lý do` · XNK không có giá ⇒ người lập `Từ chối … Nhóm … không có giá: …` · Huỷ duyệt ⇒ người lập `Hủy … Nhóm … Lý do`. Không báo khi XNK duyệt |
| T3-Q6 | close-stale production | ✅ **thêm `--by=<id>` bắt buộc khi chạy thật** (dry-run không cần) ⇒ ghi log `created_by`, nhóm `closed_by`/`updated_by`; runbook `--by=13`; làm gộp trong nhánh T3 (+ 1 ca PHPUnit) |

## 3. Task (điền sau khi chốt tồn)

### 3.1 BE — `Modules/MasterData` (prefix `master-data/price-asking-requests`)
- [x] Service `PriceCalculation/PriceAskingRequestService`: list (lọc + phân trang + bung nhóm) · show (nhóm, hàng × ĐVT đã khai, trạng thái hàng, giá bán lẻ hiện hành, cảnh báo, lịch sử, cờ quyền từng nút) · product-options (A1) · store / update (A2, lưu nháp / lưu và gửi) · delete · send (A3) · ptkdApprove / ptkdReject (A4) · xnkApprove / xnkNoPrice / xnkCancel (A5, A6) · `getNextCode`.
- [x] Đổi `pcc.status` hàng mới theo §2.3 (hàm riêng trong service, chỉ hàng có `pcc.status` 1/2).
- [x] `PriceAskingNotifier` (prefix `[YCHG]`) theo T3-Q5.
- [x] T3-Q6: `price-asking:close-stale` thêm `--by` (bắt buộc khi chạy thật) + PHPUnit; cập nhật runbook.
- [x] Controller + route (static trước `/{id}`, `->where('id','[0-9]+')`).
- [x] PHPUnit Feature: luồng đủ (gửi → PTKD duyệt → XNK duyệt/không giá/huỷ → phiếu 9) · chặn nhóm chưa phân công (nêu tên hãng) · validate đồng thời · quyền: có / không 1662, 1663, XNK không phân công 403, phiếu công ty khác 403 · người khác không thấy nháp · đổi `pcc.status` · gửi 2 lần đồng thời · thông báo đúng người nhận · chạy lại MasterData toàn bộ.

### 3.2 FE — hrm-client
- [x] Menu: `sale-hub.js:165` gắn link `/sale/price-asking-requests` (giữ nhãn).
- [x] `pages/sale/price-asking-requests/index.vue` — danh sách theo mockup (`V2BaseDataTable` + `row-expand` dòng nhóm), bộ lọc (Số phiếu · Mã/tên hàng · Thương hiệu · Hãng · Trạng thái · Người lập · PTKD duyệt · XNK tiếp nhận), `layout: 'default-sidebar'`.
- [x] `add.vue` / `_id/edit.vue` / `_id/index.vue` — form + chi tiết: thông tin chung, bảng nhóm La Mã, popup chọn hàng, cảnh báo, khối Ghi chú duyệt & lịch sử, `V2Footer` (unsaved mixin, validate đồng thời, xong quay về danh sách), popup lý do (`V2BaseModal`) cho Từ chối / Không có giá / Huỷ duyệt, xác nhận `$confirm`.
- [x] Nút "Lập yêu cầu hỏi giá" ở màn Nhập thông tin + Đang kinh doanh, tick dòng nạp sẵn (T3-Q3) — kiểm hồi quy tick dòng màn Dữ liệu công ty + Kho.
- [x] Playwright MCP đo DOM (gate theo vai, bố cục 1440/1280, không tràn ngang, khoảng cách nút 12px, badge màu) + viết spec e2e `e2e/tests/sale/price-asking-request{.api,}.spec.ts` (có/không quyền) — chạy khi user yêu cầu.

### 3.3 Kết quả BE (11/10)
- api `aca153974` trên `feat/t3-ychg`: 6 lớp `Services/PriceCalculation/` (Access · ProductReader · RequestService · RequestWriter · Notifier · EmployeeLabel) + controller + 11 route; lệnh close-stale `--by`.
- PHPUnit `PriceAskingRequestApiTest` 9/9 + backfill 8/8; MasterData **382/382**.
- Tự chốt khi code: phiếu công ty khác / nháp người khác ⇒ **404** (không lộ, khuôn T1); PTKD duyệt mà phân công XNK đã gỡ sau khi gửi ⇒ 422 nêu tên nhóm (không chép lỗi 500 ERP); gửi lại phiếu 8 xoá approver/comment ở phần đầu (log giữ); hàng thiếu thương hiệu / hãng không vào được YCHG (cột nhóm NOT NULL — DB hiện 0 hàng thiếu).

### 3.4 Kết quả FE + kiểm (11/10)
- client `32e681df0` (+ api `c28efc64a`, `872ed5898`) trên `feat/t3-ychg` ⇒ merge LOCAL nhánh chung: **api `731db49f1` · client `92bc61723`** (CHƯA push).
- File: `components/sale/price-asking/{PriceAskingRequestForm,PriceAskingProductPickerModal,PriceAskingReasonModal}.vue`,
  `pages/sale/price-asking-requests/{index,add,_id/index,_id/edit}.vue`, `ProductListPage.vue` + `product-list-screens.js` (cờ `priceAsking`), `sale-hub.js`.
- Bám màn: danh sách cây ⇐ `pages/finance/prepick-stocks/index.vue` · trang vỏ / chi tiết ⇐ `pages/finance/bill-adjust-depts` · popup chọn ⇐
  `ProductItemPickerModal.vue` · popup lý do ⇐ `meeting-cancel-reason-modal.vue` (V2BaseModal) · khối ⇐ `V2BaseFormSection`
  (`CreatorInfoLine` / `V2BaseFormCard` / `utils/pickerPagination.js` KHÔNG có trên nhánh này lẫn gop_db ⇒ dòng người tạo ở slot #actions, hằng 10/20/50/100 khai tại chỗ).
- Tự chốt khi code: nút toolbar danh sách = **"Tạo mới"** (skill), nút ở màn hàng hoá giữ **"Lập yêu cầu hỏi giá"** (thao tác nghiệp vụ, T3-Q3);
  không có "Lưu và tiếp tục"; xung đột trạng thái ⇒ **409** câu chuẩn; danh sách mặc định 10 dòng, sắp ngày tạo giảm dần, sort Số phiếu / Ngày tạo / PTKD duyệt;
  tìm nhanh chỉ số phiếu + mã / tên hàng (Người tạo / PTKD / XNK là ô chọn nâng cao); popup chọn hàng phân trang BE (`exclude_ids`).
- Playwright MCP (Nuxt 3031 + API 8031, NV 13 + role tạm 1662/1663 + phân công tạm + 3 hàng tạm mã 1 — ĐÃ DỌN, `pcc` trả status + updated_at gốc):
  tick 3 hàng ⇒ form nạp sẵn 2 nhóm · nhóm thiếu XNK: gửi ⇒ 0 request, lỗi đỏ `rgb(220,53,69)` · bỏ hàng ⇒ popup xác nhận ⇒ 1 POST, về danh sách, hàng ⇒ 2 ·
  PTKD Duyệt (popup ghi chú) ⇒ nhóm Chờ XNK duyệt · XNK Duyệt ⇒ Chờ lập YCTG · Huỷ duyệt trống lý do ⇒ "Bắt buộc phải nhập" ⇒ có lý do ⇒ phiếu 9, nhóm 6, hàng về 1, log 4 dòng ·
  Lưu nháp không hàng ⇒ lỗi, 0 request · popup chọn hàng → Lưu nháp → Sửa → Xoá (confirm) đạt · danh sách 1440: bảng 1139 = khung 1139 (đã thu cột), dòng nhóm nền #ecfdf3 cả ô ghim ·
  1280: bảng cuộn trong khung, trang không tràn · màn Đang KD có tick + nút · KHÔNG quyền (NV 34): nháp người khác 404, không trong danh sách, cờ nút false, /approve 403.
  Console chỉ lỗi `e2e.png` 404 có sẵn + cảnh báo HMR.
  🐞 Tự bắt khi đo: cột ngày hiện `Y-m-d H:i:s` (BE đổi sang `d/m/Y H:i`) · ô Công ty trống (store chỉ có id ⇒ thêm `GET form-options`) ·
  2 nút XNK trên dòng nhóm cách 20px (⇒ cụm `gap 12px`, CHƯA đo lại sau khi sửa — ca e2e P3 chốt 12px) · footer thừa `mr-2` (V2Footer tự gap 5px).
- e2e `HRM/e2e/tests/sale/price-asking-request.spec.ts` (P1–P5 + N1) — **CHẠY 11/10: 6/6 passed** (worktree 3031/8031, `--no-deps --workers=1`, afterAll dọn sạch).
- PHPUnit MasterData **382/382** sau mọi sửa BE.

### Checkpoint — 2026-10-11
Vừa hoàn thành: T3 YCHG code xong BE + FE, kiểm Playwright MCP, merge LOCAL nhánh chung (api `731db49f1`, client `92bc61723`).
Đang làm dở: không.
Bước tiếp theo: user soát màn YCHG (giacty, 3031) · chạy e2e khi user cho · plan T4 YCTG.
Blocked: —

## 4. Phạm vi sẽ xin "làm"

| | |
|---|---|
| Repo / nhánh | hrm-api + hrm-client worktree `wt-chuyen-doi-hang-hoa`, nhánh `feat/t3-ychg` từ nhánh chung; xong merge LOCAL về nhánh chung, không push |
| DB | `hrm_erp_giacty`: KHÔNG migration / seeder; chỉ dữ liệu thử khi kiểm (role tạm `T1_UAT_NAMDANG` giữ nguyên) |
| Không đụng | ERP, gop_db, G4/G5, bảng YCTG/PTG |
