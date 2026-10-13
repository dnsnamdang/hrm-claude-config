# Plan T4 — Yêu cầu tính giá (YCTG) — 11/10/2026

> Nguồn: `design.md` §1, §2 (YCTG 3·2·5·1·6·4, nhóm 1→7), §4, §5.5 (công thức K12), §6 (T4), §8 · `ton.md` Q2, Q7, Q9, Q11–Q13, D3, D6, D11, T2-C1 ·
> mockup đã duyệt (`sc-yc`, `sc-ycf`; ảnh `anh-mockup/t0-yctg-form.png`, `t0-yctg-chi-tiet-ket-qua.png`) · khảo sát `khao-sat-be-erp.md` §1.2 §2.1 §3.2 §7,
> `khao-sat-fe-erp.md` §1.2 §2 · khuôn T3 (`t3-plan.md` — Access / Writer / Notifier / form dùng chung).
> ✅ **User cho "LÀM" 11/10/2026** — đúng phạm vi mục 4 (không migration/seeder; sửa service YCHG T3; bảng PTG / KQ chỉ đọc).
> Môi trường: worktree `wt-chuyen-doi-hang-hoa`, nhánh con `feat/t4-yctg` từ nhánh chung `feat/chuyen-doi-hang-hoa`; DB dev `hrm_erp_giacty`. Không migration (T2 đủ cột).

## 0. Hiện trạng (đo 11/10)

- Bảng `price_calculate_requests` (code · `currency` = **id `currencies` dạng chuỗi** · exchange_rate double · note · comment (lý do trả) · price_asking_request_id ·
  group_id UNIQUE · approver_id/approved_time · rejected_by/at · status · company/department/part_id NOT NULL · brand_id · manufacture_id · audit).
  Dữ liệu: 3: 6 · 5: 21 · 1: 1 · 4: 3.119. Mã ERP **`PYCTG-` + 5 số** (cuối PYCTG-03163) — mockup ghi `YCTG-`.
- `price_calculate_request_products`: product_id · product_name · code · **unit_id NOT NULL** · unit_name · supplier_price decimal(16,2) · supplier_price_exchange ·
  import_tax · amount_exchange_after_tax · **chosen** (5.240 tick / 102 bỏ tick; 192 phiếu nhiều ĐVT).
- `price_calculate_request_product_costs`: parent_id · price_calculate_request_id · cost_id · cost_name · rate · value decimal(10,2) (ngoại tệ) · value_exchange.
- Danh mục: `costs` type 8 = 7 dòng (56–62, gồm "Thuế nhập khẩu" — D11 giữ) — **chưa có endpoint HRM lọc type 8**; `currencies` 11 dòng (VNĐ 1 …) có
  `GET /finance/currencies/getAll`; `manufacture_costs` (chi phí mặc định theo hãng) **0 dòng**; `products.import_tax` có ở 4.312 hàng.
- T1 `InternalPricePolicyLookup::find(productId, buyerCompanyId)` có sẵn (chưa mở route — T1 để dành T4).
- ERP: YCTG ở menu **Mua hàng › Hàng tạm - Hỏi giá** (cạnh YCHG); HRM `sale-hub.js` chưa có mục YCTG (D10: phân hệ Bán hàng).
- Khuôn T3 dùng lại được: `PriceAskingAccess` (công ty đang làm việc, nháp chỉ người lập), `XnkAssignmentResolver`, `EmployeeLabel`, notifier, `PriceAskingReasonModal`,
  bảng gom nhóm, danh sách cây. Nhánh này KHÔNG có `CreatorInfoLine` / `V2BaseFormCard` / `pickerPagination` (đã ghi ở T3).

## 1. Tự chốt theo design / mockup / khuôn T3 (không hỏi — ghi để duyệt)

| # | Chốt |
|---|---|
| B1 | Mã **`PYCTG-xxxxx`** (nối dãy ERP, `generateCode(5, id)`) |
| B2 | Lập YCTG CHỈ từ nhóm **1 Chờ lập YCTG** của phiếu Đang hỏi giá, người lập = XNK phân công HIỆN HÀNH của nhóm + quyền 1663 (D3). Lối vào: nút "Lập YCTG" ở dòng nhóm (chi tiết YCHG + nút điều hướng ở danh sách YCHG) và nút "Tạo mới" ở danh sách YCTG mở popup **chọn nhóm đang chờ tôi lập** (mockup điểm 8). YCTG đã lập thuộc người lập |
| B3 | Bung dòng = hàng × MỌI ĐVT đã khai (`product_units`) của các hàng trong nhóm (Q9); thuế NK mặc định `products.import_tax`; chi phí mặc định `manufacture_costs` của hãng (hiện rỗng) |
| B4 | Lưu YCTG (nháp hoặc gửi) ⇒ nhóm 1 → **7**; xoá YCTG ⇒ nhóm 7 → 1 (theo mockup `luuYC`). Phần đầu YCHG giữ 10 |
| B5 | Trạng thái YCTG ở T4: **3 Đang tạo · 2 Chờ tính giá · 5 Không duyệt** (1 / 6 / 4 do T5). Gửi từ 3 hoặc 5 ⇒ 2; KTMH **Từ chối** (chữ theo skill, mockup "Không duyệt") 2 ⇒ 5, lý do bắt buộc, `rejected_by/at` |
| B6 | Sửa: người lập, 3 / 5. Nháp (3) chỉ người lập thấy (như YCHG); xem YCTG cần 1663 hoặc 1664 hoặc 1092 (Q11) — không ⇒ ẩn menu, 403, số YCTG ở YCHG là chữ thường |
| B7 | Nhóm đã đóng (4/6/9) ⇒ BE **423** mọi thao tác ghi trên YCTG của nhóm, FE ẩn nút + dòng "Nhóm đã huỷ duyệt" (T2-C1). Đổi trạng thái xung đột ⇒ 409 câu chuẩn (như T3) |
| B8 | Form: Thông tin chung = YCHG (link) · Thương hiệu – Hãng · Người hỏi giá · XNK lập · **Tiền tệ*** · **Tỉ giá*** (VNĐ ⇒ 1, khoá) · Ghi chú; 2 tab **Hàng hoá · Chi phí** (mockup). Lưu nháp chỉ cần Tiền tệ (cột NOT NULL); Lưu và gửi duyệt: mọi dòng có Giá NCC > 0. Định dạng luôn chặn: tỉ giá > 0, giá ≥ 0, thuế 0–100, tỉ lệ chi phí 0–100, đơn giá chi phí ≤ giá NCC, chi phí không trùng trong 1 dòng |
| B9 | **BE tính lại** đơn giá VNĐ, thành tiền sau thuế, thành tiền chi phí (K12) — không lưu số FE gửi như ERP |
| B10 | Thông báo (skill, như T3-Q5): Gửi ⇒ NV có 1664 tại công ty `[YCTG] Chờ duyệt: PYCTG-x. Nhóm: …` · Từ chối ⇒ XNK lập `[YCTG] Yêu cầu làm lại: PYCTG-x. Lý do: …` |
| B11 | Nút KTMH **"Tính giá"** (mở lập PTG) thuộc T5 — T4 chưa hiện; T4 KTMH chỉ có Từ chối |
| B12 | Cột **Chính sách giá nội bộ** (mockup `oChinhSach`): hàng của chính công ty ⇒ "không có giá mua nội bộ"; chưa có chính sách ⇒ badge "Chưa cấu hình"; có ⇒ cách tính + 2 tỷ lệ + giá bán lẻ công ty quản lý, **giá vốn chỉ khi có 1092** (Q12) |

## 2. Tồn — ✅ chốt đủ 11/10/2026 (Quyết định đã chốt)

| # | Câu | Chốt |
|---|---|---|
| T4-Q1 | Ô tick "Cần tính" từng dòng hàng × ĐVT | ✅ **BỎ ô tick** — mọi dòng hàng × ĐVT phải có Giá NCC khi gửi (đúng Q9 / BB2). Nhập giá ĐVT cơ bản ⇒ ĐVT khác tự gợi ý = giá cơ bản × hệ số quy đổi, sửa được. Cột `chosen` ghi 1 cho mọi dòng (PTG / dữ liệu cũ vẫn đọc cột này) |
| T4-Q2 | Phạm vi T4 | ✅ **Xem KQ ở T4, Tạm tính ở T5**: component "Chi tiết kết quả" dùng chung gắn cả YCHG (bù T3 A10) lẫn YCTG, đọc `price_calculate_results*` (3.119 KQ cũ để kiểm); cột Chính sách chỉ hiện cách tính + 2 tỷ lệ + giá tham khảo (B12) |
| T4-Q3 | Xoá YCTG | ✅ **người lập, chỉ 3 Đang tạo (như ERP)**; xoá ⇒ nhóm 7 → 1. YCTG Không duyệt (5) chỉ sửa rồi gửi lại. ⚠️ Hệ quả: nhóm có YCTG 5 không Huỷ duyệt được (Huỷ duyệt cần nhóm chưa có YCTG) — muốn bỏ thì XNK sửa → gửi lại, hoặc chờ T5 |
| T4-Q4 | Menu | ✅ mục **"YC tính giá"** ngay sau "YC hỏi giá" ở Bán hàng › Khởi tạo › Hàng hóa, isShow 1663 / 1664 / 1092 |

## 3. Task (điền sau khi chốt)

### 3.1 BE — `Modules/MasterData` (prefix `master-data/price-calculate-requests`)
- [x] `PriceCalculateRequestAccess` (dùng lại khuôn `PriceAskingAccess`: công ty, nháp, 1663/1664/1092, XNK phân công, nhóm đóng 423).
- [x] `PriceCalculateRequestService` đọc: list (lọc + phân trang + sort) · filter-options · show (dòng, chi phí, chính sách, lịch sử, cờ nút) · nhóm chờ tôi lập · form-options (tiền tệ, chi phí type 8).
- [x] `PriceCalculateRequestWriter`: tạo từ nhóm (bung ĐVT, mặc định thuế / chi phí) · update · gửi · xoá · KTMH từ chối; tính lại số (K12); nhóm 1↔7; log `price_asking_request_approve_histories` (type ERP "Lập yêu cầu tính giá" / thêm "Gửi tính giá", "Không duyệt tính giá").
- [x] `PriceCalculateRequestNotifier` (`[YCTG]`).
- [x] KQ đọc: show YCHG / YCTG trả giá bán mới theo dòng từ `price_calculate_results` → `result_products` → `result_product_prices` (+ ngày áp, người tính giá, số PTG); chỉ giá bán (Q20).
- [x] YCHG: cờ `can_create_calculate` ở nhóm (nút Lập YCTG) + số YCTG là link khi có quyền xem.
- [x] Controller + route; PHPUnit: luồng lập → gửi → từ chối → sửa → gửi lại · bung ĐVT · validate đồng thời · BE tính lại số · nhóm đóng 423 · quyền có / không (1663 không phân công 403, không 1663/1664/1092 ⇒ 403 xem) · nháp người khác 404 · thông báo · MasterData toàn bộ.

### 3.2 FE — hrm-client
- [x] Menu `sale-hub.js` (T4-Q4) · `pages/sale/price-calculate-requests/{index,add,_id/index,_id/edit}.vue` · form dùng chung 2 tab · popup chọn nhóm · popup lý do (dùng lại `PriceAskingReasonModal`).
- [x] YCHG: nút "Lập YCTG" ở dòng nhóm (chi tiết) + nút điều hướng ở danh sách.
- [x] Component "Chi tiết kết quả" dùng chung (T4-Q2): bật/tắt mặc định TẮT, ẩn từng hàng, `?show_result=1` tự bật; gắn YCHG (dưới mã hàng, mỗi ĐVT 1 dòng × 6 loại giá) + YCTG (dưới dòng hàng × ĐVT, ghim khung khi cuộn ngang) — mockup "Sửa tiếp 11/10".
- [x] Playwright MCP đo DOM (1440/1280, tab, công thức, gate theo vai) + spec e2e `tests/sale/price-calculate-request.spec.ts` (chạy khi user cho).

### 3.3 Kết quả (11/10)
- api `50867c9e2` + `694cb7e89`, client `8562cf7f2` trên `feat/t4-yctg` ⇒ merge LOCAL nhánh chung: **api `e94ebec84` · client `23ebfa9d7`** (CHƯA push).
- BE: `PriceCalculateRequest{Access,Service,Writer,Notifier}`, `PriceResultReader`; 10 route `master-data/price-calculate-requests`; YCHG thêm cờ
  `can_create_calculate`, KQ theo nhóm / hàng, `can_view_calculate`; `PriceAskingNotifier` cho kế thừa (`static::PREFIX`).
- FE: `pages/sale/price-calculate-requests/*`, `components/sale/price-calculate/{PriceCalculateRequestForm,PolicyCell,PendingGroupPickerModal}.vue`,
  `components/sale/price-asking/PriceResultDrill.vue` (dùng chung YCHG + YCTG), menu "YC tính giá".
- PHPUnit `PriceCalculateRequestApiTest` 7 ca; MasterData **389/389**.
- Playwright MCP (NV 13 + role tạm 1662/1663/1664/1092 + phân công tạm + 2 hàng tạm mã 1, YCHG tạo qua API — ĐÃ DỌN, `pcc` trả gốc):
  YCHG nhóm Chờ lập YCTG có nút "Lập YCTG" ⇒ form 3 dòng (hàng 2 ĐVT bung đủ), không ô tick · gửi khi trống ⇒ 0 request, 4 lỗi đỏ, tab gắn cờ ·
  chọn USD ⇒ tỉ giá 26,180 · gõ 100 ở "Cái" ⇒ "Bộ/2c" gợi ý 200 · chi phí 10% ⇒ 10 USD = 261,800 · gửi ⇒ 1 POST 200, DB: status 2, số BE tính lại khớp, chosen 1, nhóm 7 ·
  danh sách 1440 bảng 1145 = khung · KTMH Từ chối ⇒ "Không duyệt" + lý do + chỉ nút Sửa, lịch sử 3 dòng · Sửa ⇒ gửi lại ⇒ Chờ tính giá ·
  YCTG cũ PYCTG-03148: "Chi tiết kết quả" tắt mặc định ⇒ bật 2 drill, ghim lề trái 48px, ẩn 1 ⇒ link "Hiện giá mới"; `?show_result=1` tự bật;
  tiêu đề drill nền trong suốt chữ #6b7280 không gạch chân · YCHG cũ PYCHG-04263: dòng nhóm "Giá bán mới áp ngày 12/09/2026 · người tính giá · PTG-03162",
  số YCTG là link, drill trải từ cột Mã hàng tới cuối bảng · KHÔNG quyền (NV 34): mọi endpoint YCTG 403, YCHG `can_view_calculate=false`.
  🐞 Tự bắt khi đo: tên công ty pháp lý quá dài ở cột Chính sách (⇒ mã công ty TPE/TPHP như T1) · dòng người tạo màn Thêm thiếu giờ · tiêu đề drill bị style bảng
  toàn cục ép nền teal (⇒ `!important`) · dấu * hiện ở màn Chi tiết.
  Chưa đo: menu "YC tính giá" ẩn với người không quyền trên giao diện (đã kiểm code tree đọc `isShow` inline).
- e2e `HRM/e2e/tests/sale/price-calculate-request.spec.ts` (P1–P5 + N1) — **CHẠY 11/10: 6/6 passed** (chạy chung với T3: 12 passed, 1.1 phút; afterAll dọn sạch — 0 phiếu thừa, pcc công ty 1 về đủ 28.371 mã 3).

### Checkpoint — 2026-10-11
Vừa hoàn thành: T4 YCTG code BE + FE, kiểm Playwright MCP, merge LOCAL nhánh chung (api `e94ebec84`, client `23ebfa9d7`).
Đang làm dở: không.
Bước tiếp theo: user soát YCTG trên 3031 · chạy e2e T3 + T4 khi user cho · plan T5 PTG (+ Tạm tính, KTMH "Tính giá", refactor ghi giá G4/G5).
Blocked: —

## 4. Phạm vi sẽ xin "làm"

| | |
|---|---|
| Repo / nhánh | hrm-api + hrm-client worktree `wt-chuyen-doi-hang-hoa`, nhánh `feat/t4-yctg` từ nhánh chung; xong merge LOCAL, không push |
| DB | `hrm_erp_giacty`: KHÔNG migration / seeder; chỉ dữ liệu thử khi kiểm rồi dọn |
| Không đụng | ERP, gop_db, G4/G5, bảng PTG / KQ (chỉ đọc nếu T4-Q2 chọn làm drill) |
