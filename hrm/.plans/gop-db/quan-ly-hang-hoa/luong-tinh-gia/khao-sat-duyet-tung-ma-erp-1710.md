# Khảo sát 17/10/2026 — ERP cũ có duyệt / loại TỪNG MÃ trong YCHG không?

Câu hỏi user: *"Khi 1 nhóm theo Thương hiệu – Hãng gồm nhiều mã hàng thì người duyệt có được từ chối/duyệt từng mã không?"*
Nguồn: code `origin/gop_db` (ERP prod) + số đo DB `hrm_erp_giacty` (bản sao dữ liệu tới 15/09/2026). Chỉ đọc, không sửa gì.

## 1. ERP cũ — 1 YCHG = 1 Thương hiệu (+ Hãng)
- `PriceAskingRequestController@store/update`: `brand_id` **bắt buộc** trên phần đầu phiếu, `manufacture_id` đi kèm ⇒ mỗi phiếu chính là 1 "nhóm".
- Mọi thao tác duyệt đều ở **cấp cả phiếu**, không nhận danh sách dòng:
  | Thao tác | Hàm (`app/Model/Order/PriceAskingRequest.php`) | Tác động |
  |---|---|---|
  | PTKD duyệt / không duyệt | `approve()` :588 · `reject()` :614 | cả phiếu ⇒ 5 / 8 |
  | XNK duyệt / không có giá | `approveXNK()` :628 · `rejectXNK()` :645 | cả phiếu ⇒ 1 / 9 |
  | XNK huỷ duyệt | `cancelApprove()` :671 | cả phiếu ⇒ 6 |
  Màn xem (`orders/price_asking_requests/show.blade.php:310-338`) chỉ có 5 nút ở chân trang, dòng hàng không có nút / ô tick.

## 2. Chỗ ERP cũ cho LOẠI TỪNG MÃ: ô tick `chosen` ở YCTG (và PTG)
- Form YCTG (`orders/price_calculate_requests/form.blade.php:135-140`): mỗi dòng hàng × ĐVT có ô tick `product.chosen` (mặc định tick, có tick-tất-cả). Bỏ tick ⇒ dòng mờ, không bắt nhập Giá NCC (`required_if:products.*.chosen,true`, `PriceCalculateRequestController:118,185`).
- Form PTG (`orders/price_calculates/form.blade.php:138-143`) cũng có ô tick; `PriceCalculate::approve()` :337/:364 + `updatePriceWithApproval` bỏ qua dòng `!chosen` ⇒ mã bỏ tick **không được ghi giá**.
- Người dùng ô tick YCTG = **XNK** (người lập YCTG); PTG = KT mua hàng.
- Mã bỏ tick không có trạng thái riêng: YCHG vẫn đi tới 4 "Đã tính giá" cho cả phiếu, không thông báo riêng mã nào bị loại.

## 3. Dữ liệu thật đã dùng
| | Phiếu | Phiếu có bỏ tick | Dòng bỏ tick |
|---|---|---|---|
| YCTG | 3.147 | **61** (≈1,9%, 03/02 → 05/09/2026, đều đã Đã tính giá) | 102 — **toàn bộ là bỏ CẢ MÃ** (mọi ĐVT của mã), 0 ca bỏ lẻ 1 ĐVT |
| PTG | 3.120 | 1 | 1 |
⇒ Nghiệp vụ thực tế: XNK thỉnh thoảng loại 1 vài mã khỏi nhóm khi lập YCTG (không hỏi được giá), phần còn lại tính giá bình thường.

## 4. HRM hiện tại (nhánh `feat/chuyen-doi-hang-hoa`)
- YCHG gom nhóm theo Thương hiệu + Hãng trong 1 phiếu; PTKD duyệt cả phiếu; XNK duyệt / Không có giá / Huỷ duyệt **cả nhóm** (`PriceAskingRequestWriter` :415-545).
- Riêng **hàng tạm**: PTKD Đồng ý / Không duyệt từng mã (Phase 6).
- YCTG **đã bỏ ô tick** theo chốt **T4-Q1** (`t4-plan.md:45`): mọi dòng hàng × ĐVT phải có Giá NCC, `chosen`=1 mọi dòng.
- ⇒ HRM **mất** khả năng ERP cũ đang có (61 phiếu): XNK không loại được 1 mã khỏi nhóm; chỉ còn cách đóng cả nhóm.

## 5. Câu hỏi cần user chốt (chưa hỏi)
Có khôi phục khả năng loại từng mã không, và ở bước nào: (a) mở lại ô tick ở YCTG như ERP (đảo T4-Q1); (b) XNK "Không có giá" từng mã ở YCHG (có lý do, thông báo người lập); (c) giữ nguyên.

## 6. Chốt 17/10/2026
- ✅ User chọn **(a) mở lại ô tick "chosen" ở YCTG như ERP** — đảo chốt T4-Q1. Chưa có lệnh code; còn hỏi các điểm chi tiết (mục 7).

## 7. Khảo sát HRM cho phương án (a) — 17/10 (chỉ đọc)
Trạng thái hàng × công ty (`ProductCompany.php:23-36`): 2 Chờ tính giá · 5 Đang tính giá · 3 Đang KD · 1 Nhập thông tin.
- `chosen` hiện chỉ GHI cứng 1 (YCTG `PriceCalculateRequestWriter:195`, PTG `PriceCalculateWriter:380`), không chỗ nào ĐỌC.
- Bắt buộc Giá NCC mọi dòng khi gửi YCTG (`PriceCalculateRequestWriter::validate` :253-261); PTG chép MỌI dòng YCTG (`PriceCalculateService::skeletonRows` :246-262), bắt đủ giá mọi dòng khi gửi (:562).
- ⚠️ Rủi ro chính: mã bỏ tick không vào PTG ⇒ **kẹt ở 2 mãi** (Finalizer chỉ đẩy 2/5→3 cho mã có dòng PTG; nhóm PRICED thì không còn đường 2→1). Ở 2: không vào YCHG mới, không sửa thông tin, không cập nhật giá (423), và chặn báo giá/HĐ ("Còn N hàng hoá chưa sẵn sàng kinh doanh", `QuotationTempGate`). ⇒ BẮT BUỘC có bước chuyển trạng thái riêng cho mã bỏ tick.
- Bỏ tick lẻ 1 ĐVT: `promoteProducts` sẽ đưa mã lên 3 dù thiếu giá ĐVT đó.
- FE: tick thêm vào `PriceInputGoodsTable.vue` (dùng chung YCTG + PTG, comment :2 "không ô tick (T4-Q1)"); form YCTG `components/sale/price-calculate/PriceCalculateRequestForm.vue`, PTG `components/finance/price-calculate/PriceCalculateForm.vue`.
- Test phải sửa: `PriceCalculateRequestApiTest` :152/:188/:204-219, `PriceCalculateApiTest` :304-322. Chưa có e2e YCTG/PTG.

### Câu tồn (hỏi lần lượt)
- D1. Tick theo mã hay theo dòng? ⇒ ✅ 17/10 **THEO MÃ** (1 ô ở dòng ĐVT đầu, dòng "↳ cùng mã" ăn theo)
- D2. Mã bỏ tick chuyển khi nào? ⇒ ✅ 17/10 **KHI NHÓM TÍNH GIÁ XONG** (finalize): 2 ⇒ 1 Nhập thông tin; trước đó giữ 2, KTMH trả YCTG thì XNK tick lại được
- D3. PTG có ô tick không? ⇒ ✅ 17/10 **CÓ, tick ở cả PTG** (KT bỏ được mã; PTG mặc định theo tick YCTG; mã KT bỏ cũng về 1 khi xong — D2)
- D4. Người lập YCHG biết thế nào? ⇒ ✅ 17/10 **Lý do bắt buộc (≤255) khi bỏ tick + nhãn "Không tính giá" kèm lý do ở dòng YCHG + thông báo "đã tính giá" ghi thêm số mã không tính giá**
- D5. Bỏ tick hết? ⇒ ✅ 17/10 **CHẶN — gửi YCTG/PTG phải còn ≥ 1 mã tick** ("Phải chọn ít nhất 1 hàng hoá"); bỏ cả nhóm dùng đường cũ

## 8. Tóm tắt thiết kế (chờ "làm")
1. **YCTG** (XNK): cột tick theo MÃ ở `PriceInputGoodsTable` (ô ở dòng ĐVT đầu, dòng "↳ cùng mã" ăn theo + mờ), mặc định tick. Bỏ tick ⇒ ô lý do bắt buộc ≤255; dòng bỏ tick không bắt Giá NCC. BE: `chosen` + lý do theo mọi dòng của mã; gửi phải ≥1 mã tick; Lưu nháp giữ trạng thái tick.
2. **PTG** (KT): chép chỉ các mã tick ở YCTG (mã XNK đã bỏ không có Giá NCC ⇒ không hiện / không tick lại được); KT bỏ tick thêm được, cùng quy tắc lý do + ≥1 mã; dòng bỏ tick không bắt giá, không gửi duyệt giá, không ghi KQ.
3. **Finalizer** (nhóm PRICED): mã bị bỏ (YCTG hoặc PTG) 2/5 ⇒ 1 Nhập thông tin; mã tick ⇒ 3 như cũ. Xoá PTG / KTMH trả YCTG: giữ đường hiện có (mã vẫn 2, tick lại được).
4. **YCHG show**: dòng mã bị bỏ hiện nhãn "Không tính giá" + lý do (+ người bỏ: XNK/KT). Thông báo "đã tính giá" cho người lập thêm "… (N hàng hoá không tính giá)".
5. **Lưu trữ**: cần cột lý do trên `price_calculate_request_products` + `price_calculate_products` ⇒ 1 migration (chạy vào `hrm_erp_giacty` — có thể phải đưa lệnh cho user chạy).
6. Test: sửa `PriceCalculateRequestApiTest` :152/:188/:204-219, `PriceCalculateApiTest` :304-322; thêm ca bỏ tick (YCTG, PTG), ≥1 mã, finalize 2⇒1, lý do bắt buộc, quyền. Spec e2e YCTG/PTG mới (chạy khi user bảo).

## 9. Kết quả code 17/10/2026 — nhánh `feat/cdhh-tick-bo-ma-yctg` (api `08e988b2e` · client `500a46c4e`), ĐÃ PUSH nhánh con, CHƯA merge nhánh chung
- Migration `2026_10_17_000001_add_unchosen_reason_to_price_calculate_lines` (cột `unchosen_reason` varchar 255 trên `price_calculate_request_products` + `price_calculate_products`) — **ĐÃ CHẠY vào `hrm_erp_giacty`**. Trước deploy: chạy cùng các migration khác.
- BE: `ChosenProducts` (mới, chuẩn hoá tick theo mã + lý do + ≥1 mã) · YCTG writer/service · PTG writer/service (khung PTG chỉ lấy mã tick YCTG; mã bỏ tick không gửi duyệt/áp giá; 2→5 chỉ mã tick; PTG 6 chặn bỏ tick mã còn ĐVT đã duyệt — `MSG_UNCHOSEN_LOCKED`) · Finalizer (chốt chỉ xét dòng tick; KQ chỉ mã tick; `releaseUnchosen` 2/5⇒1; thông báo "(N hàng hoá không tính giá)") · YCHG show `not_priced {reason, by: XNK | Kế toán mua hàng}` khi nhóm Đã tính giá · bản in YCTG/PTG ghi "Không tính giá: lý do" · popup lập PTG đếm mã tick.
- Hàng ĐANG KD hỏi lại giá bị bỏ tick giữ 3 (chỉ 2/5 ⇒ 1).
- FE: cột "Tính giá" sau STT ở `PriceInputGoodsTable` (ô ở dòng ĐVT đầu, mờ 0.45 + gạch tên + ô lý do; chỉ xem ⇒ "Không tính giá: lý do"); tab Chi phí / Tính giá PTG khoá + mờ mã bỏ tick; lỗi chung `err.rows` ở PTG; hộp xác nhận YCTG đếm mã; YCHG chi tiết nhãn "Không tính giá (XNK|Kế toán mua hàng) — lý do" (khuôn dòng hàng tạm không duyệt).
- PHPUnit: YCTG 11/11 (+2 ca), PTG 17/17 (+4 ca: bỏ tick PTG, lý do/≥1 mã, PTG 6, bỏ tick YCTG ⇒ không sang PTG + về 1 + nhãn YCHG + bản in). Liên quan xanh: PriceAskingRequestApi 11, PriceAskingTempProduct 16, GroupBackfill 8, ProductPriceApprovalApi 26, PriceReaderWhitelist 2, PriceReadPoints 9, TempProductApi 15, TempProductScreen 12, ProductPriceScreenApi 32.
- Playwright MCP (3031/8031, e2e_assign; khung form dựng bằng service thật qua tinker + route.fulfill vì e2e không phải XNK nhóm; mọi ghi bị chặn): YCTG nhóm 3997 (7 mã) — cột thứ 2 "Tính giá", 7 ô tick sẵn; bỏ tick ⇒ mờ 0.45 / tên gạch / ô lý do / Giá NCC + Thuế khoá; gửi thiếu lý do ⇒ 8 lỗi (tiền tệ + 6 giá + 1 lý do), mã bỏ tick không bị bắt giá, 0 ghi; bỏ hết ⇒ "Phải chọn ít nhất 1 hàng hoá để tính giá", 0 ghi; giữ 1 mã bỏ ⇒ xác nhận "6 hàng hoá tính giá, 1 hàng hoá không tính giá" ⇒ 1 POST đúng payload. PTG từ YCTG 2874 (8 mã) — bỏ tick ở tab Hàng hoá ⇒ tab Tính giá 6 dòng loại giá mờ, 0 ô mở; thiếu lý do ⇒ đúng 1 lỗi, tự về tab Hàng hoá, 0 ghi; có lý do ⇒ 1 POST `chosen:false` + lý do. Chi tiết YCTG 3163: ô tick khoá + "Không tính giá: …". Chi tiết YCHG 4223: 2 nhãn XNK / Kế toán mua hàng, chữ rgb(185,28,28), tên gạch.
- e2e: `wt-chuyen-doi-hang-hoa/e2e/tests/sale/price-calculate-tick-ui.spec.ts` (K1–K7, không ghi DB) — CHƯA chạy (`--list` biên dịch OK, 3 ca).
