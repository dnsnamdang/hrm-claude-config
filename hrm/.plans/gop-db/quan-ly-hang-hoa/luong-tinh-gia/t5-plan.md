# Plan T5 — Phiếu tính giá (PTG) + ghi giá qua G4/G5 + Kết quả — 11/10/2026

> Nguồn: `design.md` §1, §2 (PTG 3·5·6·1, dòng `approval_status`, YCTG 1·6·4, nhóm 7→4, `pcc` 2·5→3), §4, §5 (refactor ghi giá), §6 (T5), §8 ·
> `ton.md` Q2, Q4–Q6, Q8–Q10, Q12, Q13, Q16, Q20, D4–D6, D8, T2-C1 · mockup đã duyệt (`sc-pt`, `sc-ptf`, `khoiChoDuyetGia`, `luuPT`, `apGia`;
> ảnh `anh-mockup/t0-ptg-tinh-gia.png`) · khảo sát `khao-sat-be-erp.md` §1.3 §3.3 §4 §7, `khao-sat-fe-erp.md` §1.3 §2 §4.4–4.6,
> `khao-sat-hrm.md` §1 · khuôn T3/T4 (`t3-plan.md`, `t4-plan.md`).
> ✅ **User cho "LÀM" 11/10/2026** — đúng phạm vi mục 4 (không migration/seeder; refactor G4/G5; e2e chỉ chạy khi user cho).
> Môi trường: worktree `wt-chuyen-doi-hang-hoa`, nhánh con `feat/t5-ptg` từ nhánh chung `feat/chuyen-doi-hang-hoa`; DB dev `hrm_erp_giacty`.

## 0. Hiện trạng (đo 11/10)

- **CSDL đủ từ T2** — T5 KHÔNG migration: `price_calculates` UNIQUE(request) (M6) · `price_calculate_products` + 8 cột chụp chính sách + `approval_status/comment/decided_at` (M7) ·
  `price_calculate_results` UNIQUE(calc) (M8) · `product_approves.price_calculate_id` + index (M9). Entity + hằng trạng thái đã có
  (`PriceCalculate::STATUS_*` 1/3/5/6, `PriceCalculateProduct::APPROVAL_*`, `PriceCalculateRequest::STATUS_*` 1/6/4, `ProductCompany::STATUS_PRICING` 5).
- Dữ liệu giacty: PTG 3.120 (1: 3.119 · 3: 1 — PTG-00215 nháp của PYCTG-00177 st 1); mã ERP **`PTG-` + 5 số**, cuối **PTG-03178**. `product_approves` = 0.
  `price_calculate_products` 4.908 dòng (5 có `other_cost`, 32 có `note`); giá hiệu lực PTG 4.192. **Cả 8 công ty `is_company_price = 0`** ⇒ nhánh duyệt chỉ kiểm được bằng dữ liệu thử.
- G4 `ProductPriceUpdateService` (463 dòng): `update()` gắn công ty đang làm + chỉ `pcc.status = 3`; ghi giá ở 4 hàm **private** `writePrices` / `writeExpected` /
  `writeCompanyUnit` / `dropPendingApprovals`; `resolvePrices()` public; `ecomCoefficient()`. G5 `ProductPriceApprovalSubmitter::submit()` public, nhận công ty tường minh.
  G5 `ProductPriceApprovalService::applyApprove/applyReject` xoá cứng `pa` + `pap`, chỉ chuyển trạng thái khi công ty = công ty quản lý (`markOwnerTrading`, docblock "chốt ở Phase 7").
- T4 có sẵn: `PriceCalculateRequest{Access,Service,Writer,Notifier}`, `PriceResultReader` (đọc mọi KQ của YCTG), `PolicyCell.vue`, `PriceResultDrill.vue`,
  form YCTG 766 dòng (2 tab Hàng hoá / Chi phí viết liền trong file).
- FE: `utils/productPriceModel.js` (`Calc` setCoef / spread / ecom / toggleManual / setExpCoef / addExpected, `validateUnit`, `buildPayload`) — dùng thẳng cho tab Tính giá.
  Menu `components/subsystem-menu/finance.js:444` `{ label: 'Phiếu tính giá' }` chưa link. Trang finance khai `layout: 'default-sidebar'`.

## 1. Tự chốt theo design / mockup / khuôn T3–T4 (không hỏi — ghi để duyệt)

| # | Chốt |
|---|---|
| C1 | Mã **`PTG-xxxxx`** nối dãy ERP (`generateCode(5, id)`, như B1 T4). BE module `Modules/MasterData` (như T3/T4), prefix `master-data/price-calculates`; FE `/finance/price-calculates` (D10 — phân hệ Tài chính), gắn link mục 'Phiếu tính giá' `finance.js:444`, isShow 1663 / 1664 / 1092 |
| C2 | **Lập PTG CHỈ từ YCTG 2 Chờ tính giá** của công ty đang làm, người có 1664. 2 lối vào: nút **Tính giá** (primary, điều hướng) ở chi tiết YCTG + dòng YCTG ở danh sách (B11 T4); nút **Tạo mới** ở danh sách PTG mở popup chọn YCTG Chờ tính giá (mockup điểm 8). Mở form KHÔNG đổi trạng thái gì — chỉ khi lưu. UNIQUE 1 YCTG – 1 PTG ⇒ lập trùng ⇒ 409 |
| C3 | PTG kế thừa YCTG: tiền tệ (khoá), tỉ giá, mọi dòng hàng × ĐVT, giá NCC, thuế NK, chi phí — sửa được ở PTG như ERP (T5-Q1), YCTG không đổi |
| C4 | Tab **Tính giá** theo mockup: mỗi (hàng × ĐVT) 1 khối rowspan — Đơn giá VNĐ · Thành tiền sau thuế · Tổng chi phí · **Chi phí khác** (nhập) · **Giá nhập kho** · 6 loại giá (Hệ số · Giá công thức · Giá bán · ĐMGG · Ngày hiệu lực + nút **Giá hiệu lực**, ≤ 1 giá hiệu lực/loại, ngày > hôm nay — như ERP/G4). Sửa Bán lẻ lan 4 loại (G4 T2), TMĐT = Bán lẻ × hệ số TMĐT công ty phiếu (khoá). Dùng `Calc` của `productPriceModel.js` (Q6). Mở PTG mới: hệ số nạp từ giá hiện hành của **công ty phiếu** (Q4), chưa có ⇒ để trống |
| C5 | Mã hàng ở tab Tính giá: + khối Chính sách bản gọn (`PolicyCell` T4) + nút **Tạm tính** (popup: cách tính · 2 tỷ lệ · 6 giá bán công ty quản lý · giá mua suy ra, tròn trăm, "chỉ tham khảo"; giá vốn công ty quản lý + giá mua suy từ giá vốn **chỉ khi có 1092** — BE trả null, FE "—", Q12) + ô **Ghi chú dòng** (`price_calculate_products.note`, KHÔNG ghi `products.note` — Q10). Hàng của chính công ty phiếu ⇒ "không có giá mua nội bộ", không nút Tạm tính |
| C6 | **BE tính lại** đơn giá VNĐ, sau thuế, chi phí, giá nhập kho (K12), TMĐT; giá bán = số user nhập (FE gợi ý tròn trăm từ hệ số — không ép lại ở BE, chỉ kiểm > 0 và ≤ `MONEY_MAX`) |
| C7 | Nút (skill button-convention, có popup xác nhận nêu tên phiếu + hệ quả): **Lưu nháp** (secondary) · **Lưu và duyệt** khi công ty tắt quy chế / **Lưu và gửi duyệt** khi bật (primary). Dòng nhắc ở chân form: "Lưu và duyệt sẽ áp giá ngay cho <công ty>" / "… gửi giá sang màn Duyệt giá bán" (mockup). Thao tác xong về danh sách PTG |
| C8 | Validate báo đồng thời. **Lưu nháp**: chỉ rule định dạng (tỉ giá > 0, giá ≥ 0, thuế 0–100, chi phí 0–100 %, chi phí khác ≥ 0, hệ số 0–99,99, ĐMGG 0–100, ngày hiệu lực > hôm nay). **Lưu và duyệt / gửi duyệt**: thêm bắt buộc giá NCC > 0 mọi dòng + đủ giá bán 5 loại (TMĐT tự tính) mọi dòng. Lỗi dưới từng ô + gắn cờ tab |
| C9 | Quyền xem / sửa (Q11, như B6 T4): xem PTG cần 1663 / 1664 / 1092; nháp (3) chỉ người lập thấy; sửa = **người lập** + 1664, trạng thái **3** (mọi dòng) hoặc **6** (chỉ dòng bị từ chối — D5). Nhóm đã đóng (4/6/9) ⇒ 423 mọi thao tác ghi, FE ẩn nút + "Nhóm đã huỷ duyệt" (T2-C1). Xung đột trạng thái ⇒ 409 câu chuẩn |
| C10 | Chụp chính sách (Q13) **mỗi lần lưu** khi PTG còn sửa được (3/6); PTG 5/1 hiện số chụp. `policy_owner_cost_price` chỉ trả khi có 1092 |
| C11 | **Lõi ghi giá dùng chung** `ProductPriceWriter` (mới, `Services/ProductPrice/`): chuyển nguyên 4 hàm private của G4 sang (public) + `apply(productId, unitId, companyId, resolved, cost, reason, by)` = `ensureUnitSet` → khoá `pcu` → write* → `dropPendingApprovals`, KHÔNG kiểm trạng thái hàng. G4 `update()` gọi lại `ProductPriceWriter` — giữ nguyên chữ ký + hành vi + câu báo |
| C12 | **Lưu và duyệt — tắt quy chế**: từng dòng `apply()` cho **công ty phiếu** ⇒ chép giá vào dòng PTG ⇒ chuyển hàng §2.3 (hàng mới 2·5 → 3 khi MỌI ĐVT đã áp; hàng 3 giữ) ⇒ PTG 1, YCTG 4, nhóm 4 + `priced_at`, sinh KQ, YCHG 4/9 nếu mọi nhóm đóng, lịch sử, thông báo — 1 transaction, thông báo sau commit |
| C13 | **Lưu và gửi duyệt — bật quy chế** (`approvalRule/needsApproval` của công ty phiếu × hãng): từng dòng `submitter->submit()` kèm `price_calculate_id` ⇒ dòng `approval_status = 1`, PTG 5, YCTG 6; hàng mới giữ 5. `submit()` trả `approve_id = null` (giá đề nghị = giá đang chạy) ⇒ coi dòng đó **đã duyệt ngay** (approval_status 2). Mọi dòng như vậy ⇒ đi luôn nhánh C12 |
| C14 | **G5 báo ngược** (sửa `applyApprove/applyReject`, trước khi xoá `pa`): `pa.price_calculate_id` ⇒ ghi `approval_status/comment/decided_at` lên dòng PTG (tra theo PTG × hàng × ĐVT); duyệt ⇒ chép **giá thực áp** (gồm giá người duyệt G5 sửa) vào dòng PTG + chuyển hàng khi đủ ĐVT. Sau vòng duyệt, mỗi PTG chạm tới (khoá dòng PTG): còn dòng 1 ⇒ giữ 5 · mọi dòng 2 ⇒ C12 phần sau (PTG 1, YCTG 4, nhóm 4, KQ, YCHG) · không còn 1 mà có 3 ⇒ PTG **6**, YCTG về **1**. Bổ sung nhánh G5 cho công ty KHÔNG quản lý hàng: `pcc` 2·5 → 3 khi đủ ĐVT (docblock "chốt Phase 7"). ✅ **User xác nhận 11/10** (sau khi giải thích; gồm cả "giá thực áp" ghi vào dòng PTG + KQ, giá đề nghị chỉ còn ở lịch sử G5) |
| C15 | **Chặn chéo** (D6): G4 `update()` gặp `pa` mở có `price_calculate_id` ⇒ 423 "Giá đang chờ duyệt ở PTG-xxxxx". PTG gửi duyệt / áp gặp `pa` mở KHÔNG có `price_calculate_id` (của G4) ⇒ 422 tại dòng đó "Đang có yêu cầu duyệt giá ở màn Cập nhật giá bán"; gặp `pa` của **PTG khác** ⇒ 422 "Giá đang chờ duyệt ở PTG-xxxxx" (không cho PTG sau đè `pa` PTG trước — BB6 sẽ làm PTG trước treo). Tắt quy chế mà còn sót `pa` G4 ⇒ PTG cũng chặn dòng đó. Không chặn: hàng chỉ ở YCHG / YCTG / PTG nháp; tắt quy chế ⇒ ai lưu sau thắng. 1 dòng bị chặn ⇒ **cả PTG không gửi được** (không gửi lẻ từng dòng). ✅ **User xác nhận 11/10** (gồm ca PTG ↔ PTG và chặn cả phiếu) |
| C16 | PTG 6 gửi lại: chỉ dòng `approval_status = 3` mở sửa + gửi lại (dòng 2 khoá, giữ giá đã áp — D5); cột "Kết quả duyệt" + lý do từ chối ở từng dòng; banner đầu form như mockup |
| C17 | Lưu nháp lần đầu: YCTG 2 → **1**, hàng mới 2 → **5** (§2.3). PTG 6 ⇒ YCTG 1; PTG 5 ⇒ YCTG 6 (theo mockup `g5TuChoi`: YCTG về "Đang tính giá") |
| C18 | Thông báo (skill, 14 nhóm hành động — D8): gửi duyệt ⇒ **1 thông báo gộp / PTG** cho người có 1658 tại công ty `[GIA] Chờ duyệt: PTG-x. n dòng giá` (thay vì mỗi dòng 1 cái); `pa` của PTG thì G5 KHÔNG báo từng dòng — thay bằng mức PTG: `[PTG] Từ chối: PTG-x. Lý do: …` (người lập PTG) · `[PTG] Đã duyệt: PTG-x.` (người lập PTG). Giá áp: `[YCHG] Đã duyệt: PYCHG-x. Nhóm …: đã có giá bán mới` (người lập YCHG + XNK lập YCTG, link nhóm + `show_result=1`); nhóm cuối xong gộp luôn "Đã tính giá xong n/n nhóm" (không gửi 2 cái) |
| C19 | KQ (Q20): 1 KQ / PTG, sinh khi PTG → 1, chép giá đã áp từ dòng PTG (+ giá hiệu lực, ghi chú dòng nếu có cột — không thì bỏ). Drill YCHG / YCTG của T4 tự hiện, không sửa `PriceResultReader` |
| C20 | Danh sách PTG (mockup `veBangPT`): STT · Số phiếu · YCTG · YCHG · Thương hiệu – Hãng · Số mã hàng · Người lập · Ngày lập · Trạng thái (`V2BaseBadge`, BE trả chữ + màu) · Hành động (Sửa khi 3/6 · Xoá khi 3 · Xem · Xem giá bán mới khi 1). Lọc: tìm nhanh (số PTG / YCTG / YCHG / mã hàng), trạng thái, thương hiệu, hãng, người lập, ngày lập. Khuôn `pages/finance/product-prices` |
| C21 | YCTG (sửa T4): nút **Tính giá** (C2) + số PTG là link ở chi tiết / danh sách khi có quyền xem; nút "Xem phiếu tính giá" ở chi tiết YCTG 1/6/4. In ⇒ T6 (T5 chưa có nút In) |

## 2. Tồn — hỏi lần lượt (chưa chốt)

| # | Câu | Đề xuất | Chốt |
|---|---|---|---|
| T5-Q1 | Ở PTG, KTMH có được sửa số XNK đã nhập (tỉ giá, giá NCC, thuế NK, chi phí)? | — | ✅ 11/10 user: **"khảo sát logic ERP ⇒ làm theo"**. ERP (`wt-erp-2d1` `orders/price_calculates/form.blade.php`, `PriceCalculateController@store/update`, `PriceCalculate::syncProducts`): tiền tệ **khoá** (lấy YCTG) · **sửa được**: tỉ giá, giá NCC, thuế NK, chi phí (thêm / xoá / sửa tỉ lệ + đơn giá), chi phí khác, ghi chú dòng, hệ số / giá / ĐMGG / giá hiệu lực · lưu chỉ vào bảng PTG, **YCTG giữ nguyên số XNK** ⇒ làm theo: PTG có bản số riêng, BE tính lại từ số PTG. Riêng ô tick "Cần tính" ERP có ở PTG nhưng **không làm** — giữ T4-Q1 / Q9 (mọi dòng hàng × ĐVT đều tính giá). Hệ quả code: tách 2 tab Hàng hoá / Chi phí của `PriceCalculateRequestForm.vue` thành component dùng chung YCTG + PTG |
| T5-Q2 | Xoá PTG Đang tạo? (ERP: `canDelete` = false nhưng route xoá không kiểm — lỗi) | — | ✅ 11/10 user: **cho xoá PTG Đang tạo, trả trạng thái YCTG**. Người lập + 1664, chỉ PTG **3** (PTG 5/6/1 không xoá — đã sinh yêu cầu duyệt / đã áp giá). Xoá ⇒ YCTG 1 → **2 Chờ tính giá** (KTMH lập lại hoặc Từ chối trả XNK được), hàng mới 5 → **2 Chờ tính giá bán** (hàng không còn trong PTG nào khác), xoá cứng dòng / chi phí / giá / giá hiệu lực của PTG, log lịch sử "Xoá phiếu tính giá", popup xác nhận nêu số phiếu + hệ quả, nhóm đóng ⇒ 423. Nút Xoá ở danh sách + chi tiết (cùng điều kiện) |

## 3. Task (điền đủ sau khi chốt tồn)

### 3.1 BE — refactor giá (`Services/ProductPrice/`)
- [x] `ProductPriceWriter` (C11) + G4 `update()` gọi lại; chạy PHPUnit MasterData toàn bộ (389) — phải xanh nguyên trạng trước khi đụng tiếp.
- [x] G5: hook PTG trong `applyApprove/applyReject` (C14) + nhánh công ty không quản lý hàng + bỏ thông báo từng dòng cho `pa` của PTG (C18).
- [x] Chặn chéo G4 ↔ PTG (C15).

### 3.2 BE — PTG (`Services/PriceCalculation/`, prefix `master-data/price-calculates`)
- [x] `PriceCalculateAccess` (công ty, nháp, 1663/1664/1092, người lập, nhóm đóng 423).
- [x] `PriceCalculateService` đọc: list · filter-options · show (dòng, chi phí, giá bán 6 loại + hiệu lực, chính sách chụp / hiện hành, kết quả duyệt dòng, cờ nút, lịch sử) · YCTG chờ tính giá (popup) · form-options (hệ số TMĐT công ty phiếu, quy chế bật/tắt, giá hiện hành để nạp hệ số) · Tạm tính (`InternalPricePolicyLookup` T1, gate 1092 phần giá vốn).
- [x] `PriceCalculateWriter`: tạo từ YCTG · update (3 / 6 chỉ dòng bị từ chối) · Lưu và duyệt (C12) · Lưu và gửi duyệt (C13) · chốt PTG sau G5 (C14) · sinh KQ (C19) · chụp chính sách (C10) · chuyển YCTG / nhóm / YCHG / `pcc` (C17) · log `price_asking_request_approve_histories` (Lập phiếu tính giá / Duyệt tính giá / Gửi duyệt giá / Giá bị từ chối).
- [x] `PriceCalculateNotifier` (`[PTG]`) + mở rộng `PriceAskingNotifier` (giá áp / xong).
- [x] YCTG: cờ `can_calculate` + `price_calculate` (id, code, link khi có quyền).
- [x] Xoá PTG 3 (T5-Q2: YCTG 1→2, hàng 5→2, PTG 5/6/1 ⇒ 409, người khác 403).
- [x] Controller + route + PHPUnit: tắt quy chế áp ngay (giá đúng công ty phiếu, công ty khác KHÔNG đổi, `pcu.cost_price` = giá nhập kho, hàng 2→5→3, YCTG/nhóm/YCHG, KQ) · bật quy chế (pa có `price_calculate_id`, PTG 5, duyệt từng dòng, từ chối 1 dòng ⇒ 6 ⇒ sửa dòng đó ⇒ gửi lại ⇒ 1, giá người duyệt sửa vào KQ) · `submit` trả null ⇒ duyệt ngay · chặn chéo 2 chiều + PTG–PTG · BE tính lại số · validate đồng thời · quyền có / không (1664, 1092 giá vốn null, người khác sửa 403, nháp người khác 404) · nhóm đóng 423 · lập trùng 409 · thông báo · MasterData toàn bộ.

### 3.3 FE — hrm-client
- [x] Menu `finance.js:444` · `pages/finance/price-calculates/{index,add,_id/index,_id/edit}.vue` (`layout: 'default-sidebar'`).
- [x] `components/finance/price-calculate/`: form 3 tab (tách tab Hàng hoá / Chi phí của `PriceCalculateRequestForm.vue` thành component dùng chung YCTG + PTG — T5-Q1; kiểm hồi quy form YCTG) · bảng Tính giá (dùng `Calc`, bọc `V2BaseTableScroll`) · popup chọn YCTG · popup Tạm tính · banner Chờ duyệt / Bị từ chối · cột kết quả duyệt dòng.
- [x] YCTG: nút Tính giá + link PTG (C21).
- [x] Playwright MCP đo DOM (1440 / 1280; công thức; lan Bán lẻ; TMĐT; validate đồng thời; tắt quy chế; bật quy chế bằng dữ liệu thử + màn Duyệt giá bán thật; gate theo vai; 1092) + spec e2e `tests/finance/price-calculate.spec.ts` (chạy khi user cho).

### 3.4 Hồi quy bắt buộc (R1)
- [x] PHPUnit MasterData toàn bộ (gồm 332 ca giá G4/G5) sau MỖI bước refactor — 389/389 sau C11, 396/396 sau hook G5 + PTG (api `e88f58d1a`, `00bead939`).
- [x] e2e giá G4 / G5 — ⚠️ KHÔNG có spec e2e riêng cho G4/G5 (plan ghi nhầm `product-price*.spec.ts`); hồi quy G4/G5 phủ bằng PHPUnit MasterData 396/396.

### 3.5 Kết quả (11/10)
- api `e88f58d1a` (C11) + `00bead939` (PTG BE), client `a45f0e029` trên `feat/t5-ptg` ⇒ merge LOCAL nhánh chung: **api `9e738e18f` · client `7bd5aa626`** (CHƯA push; api +21, client +19 so origin).
- BE: `ProductPriceWriter` (lõi ghi giá tách từ G4); `PriceCalculate{Access,Service,Writer,Finalizer,Notifier}`; 7 route `master-data/price-calculates`;
  G5 Submitter nhận `price_calculate_id`, Approve/Reject báo ngược dòng PTG + settle; G4 423 khi dòng chờ duyệt ở PTG; YCTG `can_calculate` + `calculate`;
  `PriceAskingNotifier::groupPriced`, `ProductPriceNotifier::submittedFromCalculate`. Danh sách trắng `price-readers.txt` + 4 file.
- FE: `pages/finance/price-calculates/*`, `components/finance/price-calculate/{PriceCalculateForm,PriceSellTable,RequestPickerModal,PolicyEstimateModal}.vue`;
  tách `components/sale/price-calculate/{PriceInputGoodsTable,PriceInputCostsTable}.vue` + `price-input-table.css` + `utils/mixins/priceInputRowsMixin.js` (form YCTG dùng lại);
  menu Tài chính › Giá bán › Phiếu tính giá; YCTG: nút Tính giá / Xem phiếu tính giá (chi tiết + danh sách).
- PHPUnit `PriceCalculateApiTest` 7 ca; MasterData **396/396**.
- Playwright MCP (NV 13 + role tạm 1092/1658/1662/1663/1664 + phân công tạm + 2 hàng tạm, YCHG/YCTG tạo qua API — **ĐÃ DỌN**, quy chế công ty 1 trả gốc 0/0/NULL):
  danh sách 1440 bảng 1145 = khung (sau khi thu cột), 1280 cuộn trong khung, trang không tràn · YCTG Chờ tính giá có "Tính giá" ⇒ form, tab Tính giá mặc định, giá nhập kho 3,010,700 ·
  Lưu và duyệt khi trống ⇒ 20 lỗi đồng thời, tab gắn cờ, 0 POST · hệ số Bán lẻ 1.5 ⇒ 4,516,100 lan 4 loại, TMĐT 5,870,930 · sửa tay ĐL1 + chi phí khác 100,000 ⇒ công thức 4,666,100, ĐL1 giữ ·
  Lưu và duyệt ⇒ DB PTG 1 / YCTG 4 / nhóm 4 / YCHG 4, 2 hàng sang 3, giá công ty 1 đúng, công ty khác 0 dòng, giá vốn = giá nhập kho, KQ 1, chụp chính sách 3/3 ·
  chi tiết chỉ "Xem giá bán mới" ⇒ YCHG drill "Giá bán mới áp ngày … PTG-03240" · bật quy chế: nút "Lưu và gửi duyệt", hệ số nạp từ giá đang áp dụng; G5 thấy 3 yêu cầu;
  duyệt (sửa giá 4,400,000) + từ chối + duyệt ⇒ PTG "Giá bị từ chối", banner lý do, chỉ khối bị từ chối mở (17 ô), tỉ giá khoá, dòng đã duyệt hiện giá thực áp; gửi lại + duyệt ⇒ Đã duyệt, KQ 4,400,000 / 35,735,700 ·
  Lưu nháp ⇒ YCTG chỉ còn "Xem phiếu tính giá"; Xoá ⇒ popup nêu số phiếu, YCTG về Chờ tính giá + hiện lại Tính giá / Từ chối · Tạm tính (hàng công ty 4, chính sách tạm theo giá bán 10% / 5%) đúng số ·
  KHÔNG quyền: menu không còn link PTG, vào thẳng URL ⇒ 403 ⇒ trang 404 · hồi quy form YCTG (2 bảng dùng chung, Chi tiết kết quả, tab Chi phí) đạt. Ảnh `anh-mockup/t5-ptg-*.png`.
  🐞 Tự bắt khi đo: bảng danh sách tràn ngang 1440 · STT / tên lặp ở dòng ĐVT thứ 2 · lỗi đỏ không tắt ở ô được Bán lẻ lan sang · nút chân form thừa `mr-2` (V2Footer đã `gap: 5px`).
- e2e: viết `HRM/e2e/tests/finance/price-calculate.spec.ts` (P1–P6 + N1, hàng tạm tạo bằng SQL — không đụng giá hàng thật); sửa selector `.yctg-table` ⇒ `.price-input-table`
  ở `tests/sale/price-calculate-request.spec.ts` (do tách bảng dùng chung). `--list` biên dịch đạt 13 ca. **CHẠY 11/10 (user cho): T5 + T4 13/13 passed** (1.3 phút, worktree 3031/8031, `--no-deps --workers=1`); afterAll dọn sạch (0 hàng / thương hiệu / PTG / yêu cầu duyệt thừa, quy chế công ty 1 về 0/0/NULL).
- ⚠️ Lúc gỡ role tạm có gọi `Cache::flush()` trên môi trường dev (xoá cache Laravel của DB giacty / Redis dev — chỉ cache, tự dựng lại).

### Checkpoint — 2026-10-11 (T5)
Vừa hoàn thành: T5 PTG BE + FE, PHPUnit 396/396, Playwright MCP đủ luồng tắt / bật quy chế, merge LOCAL nhánh chung (api `9e738e18f`, client `7bd5aa626`).
Đang làm dở: không. Dữ liệu thử đã dọn; server 8031 / 3031 đang chạy.
Bước tiếp theo: user soát PTG trên 3031 · push khi user báo · plan T6 Bản in 4 chứng từ. (e2e T5 + T4 13/13 đã chạy 11/10.)
Blocked: —

## 4. Phạm vi sẽ xin "làm"

| | |
|---|---|
| Repo / nhánh | hrm-api + hrm-client worktree `wt-chuyen-doi-hang-hoa`, nhánh `feat/t5-ptg` từ nhánh chung; xong merge LOCAL, không push |
| DB | `hrm_erp_giacty`: KHÔNG migration / seeder; chỉ dữ liệu thử khi kiểm (bật `is_company_price` tạm 1 công ty, role / phân công tạm) rồi dọn, trả nguyên |
| Đụng code đã nghiệm thu | G4 `ProductPriceUpdateService` (tách lõi ghi), G5 `ProductPriceApprovalService` + `ProductPriceApprovalSubmitter` (hook PTG, nhánh công ty không quản lý, thông báo), T4 YCTG (nút + link), `finance.js` |
| Không đụng | ERP, gop_db, bản in (T6) |
