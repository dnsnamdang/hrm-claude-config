# Phase 7 — Luồng Tính giá: tồn cần chốt trước khi design

> Mở 10/10/2026. Nguồn: `khao-sat-be-erp.md`, `khao-sat-fe-erp.md` (ERP `wt-erp-2d1` @ `feat/2d1-erp-khong-loi`, DB `hrm_erp_giacty`)
> + design `man-danh-muc-hang-hoa/design.md` §29, §33o–§33s, §34, §35c (C1/C3/C4 gác tới 2-tg).
> Tiền đề: feature lên production MỘT lần, không cờ/đường lui; giá RIÊNG theo công ty (G0–G6 đã xong).

## 0. Đã chốt từ trước — KHÔNG hỏi lại

| # | Chốt | Nguồn |
|---|---|---|
| K1 | MỌI hàng (tự tạo + lấy về) đều tính giá bằng chứng từ; form hàng hoá không còn tab Giá bán | §29a-1, §29g |
| K2 | Ô giá mua để trống, người tính giá tự nhập; chính sách nội bộ chỉ tham khảo | §29a-2 |
| K3 | Hiện song song 2 tỉ lệ Nhập khẩu nguyên lô / Tồn kho | §29a-3 |
| K4 | Giữ ô hàng nhập khẩu: tiền tệ · tỉ giá · thuế NK · tab Chi phí | §29a-5 |
| K5 | Yêu cầu gom nhóm cha–con theo Thương hiệu – Hãng SX, STT La Mã / 1-2-3 | §33o, §33r |
| K6 | Yêu cầu ↔ Phiếu = 1–n (một phiếu mỗi nhóm hãng); yêu cầu "Đã tính giá" khi đủ nhóm duyệt | §33p |
| K7 | Chỉ người phụ trách được phân công mới lập phiếu của nhóm (gate BE); đổi người = Bàn giao công việc sẵn có | §33q |
| K8 | Trạng thái hàng: Lưu & gửi YC ⇒ Chờ tính giá bán · Lưu PTG ⇒ Đang tính giá · duyệt ⇒ Đang kinh doanh | §26, §29c |
| K9 | Mockup chốt 30/09 (`mockup-luong-xay-dung-hang-hoa.html`: `sc-yc`, `sc-ycf`, `sc-pt`, `sc-ptf` + popup Chọn yêu cầu / Tạm tính) | §34 |
| K10 | Quyền chỉ gate GHI + GIÁ VỐN; đọc thông tin hàng/giá bán mở | §35b |
| K11 | 2 cron ERP (01:00 áp giá hiệu lực, 14:30) giữ ở ERP | QC-10 |
| K12 | Công thức (khớp dữ liệu thật + nhánh hiện tại): Giá nhập kho = giá NCC × tỉ giá × (1+thuế NK) + Σ chi phí (% tính trên đơn giá CHƯA thuế) + chi phí khác; giá bán = làm tròn trăm(hệ số × giá nhập kho); TMĐT = Bán lẻ × `configs.coefficient_ecommerce_price`. Phần giá bán đã có ở `hrm-client/utils/productPriceModel.js` | khảo sát FE §2 |

## 1. Dữ kiện mới phát hiện khi khảo sát (10/10)

- Phân công người phụ trách: `assign_histories` dòng `employee_date_to IS NULL`, theo **(thương hiệu × hãng × công ty)**,
  `buy_employee_id` = người mua hàng (Phòng XNK). 837 cặp hãng có người mua; 30 cặp có 2 người (mỗi công ty một người); chỉ công ty 1 và 4 có phân công.
  Màn khai báo là *Phân công nhân viên phụ trách* ở ERP (`AssignEmployeeController`, phiếu `assign_employee_ballots` có duyệt). §33q đề xuất bảng mới
  `assign_employee_manufactures` UNIQUE — **không cần**: dùng nguồn sẵn có.
- ERP: duyệt PTG ghi giá thẳng (8/8 công ty `is_company_price=0`, `product_approves` = 0), ghi vào công ty quản lý hàng (`@TODO-PHASE7`), có ghi đè `products.note`.
- HRM có sẵn quyền 1092 *Xem giá vốn hàng hoá*, 1657 *Cập nhật giá bán hàng hoá*, 1658 *Duyệt giá bán hàng hoá*. Id ERP 1003/1006/144 trùng id HRM ⇒ quyền mới phải cấp id mới.
- ERP chặn bằng middleware, GIỮ tên route (topmenubar 5 link + 3 thẻ dashboard gọi `route()`).
- Lỗi cũ ERP (ghi vào danh sách ngoài luồng, không vá trong đợt): xoá PTG không kiểm quyền; lộ giá vốn ở show YCHG/KQ; in PTG/KQ hỏng; PTKD duyệt 500; lưu PTG lần đầu duyệt luôn YCTG; lọc trạng thái PTG sai bộ; `is_foreign` luôn đúng.

## 2. Tồn — hỏi lần lượt (✅ chốt đủ Q1–Q18 ngày 10/10/2026)

| # | Câu | Đề xuất | Chốt |
|---|---|---|---|
| Q1 | Phạm vi chứng từ: HRM làm những chứng từ nào? (C1) | Chỉ YCTG + PTG như mockup | ✅ 10/10 **GIỮ ĐỦ 4 chứng từ** (YCHG → YCTG → PTG → KQ) ⇒ vẽ thêm mockup YCHG + KQ |
| Q1a | YCHG nối vào luồng thế nào | 2 cửa vào YCTG | ✅ 10/10 **MỌI YCTG đều qua YCHG** — kể cả hàng mới ở màn Nhập thông tin (nút đổi thành *Lập yêu cầu hỏi giá*) ⇒ sửa mockup đã chốt |
| Q1b | Cấu trúc YCHG | YCHG gom nhóm, tách YCTG | ✅ 10/10 **YCHG gom nhóm Thương hiệu–Hãng** (dời §33o lên YCHG); PTKD duyệt cả phiếu; mỗi nhóm tới người mua phụ trách hãng (XNK) duyệt + lập YCTG riêng. **1 YCHG – n YCTG (mỗi nhóm 1), 1 YCTG – 1 PTG**; YCHG xong khi đủ nhóm. K5/K6 dời từ YCTG lên YCHG |
| Q2 | Phân vai YCTG / PTG (thay C3) | Như ERP | ✅ 10/10 **NHƯ ERP**: XNK phụ trách hãng lập YCTG (giá NCC, tiền tệ, tỉ giá, thuế NK, chi phí) · **Kế toán mua hàng duyệt / trả YCTG** · KTMH lập PTG (kế thừa số YCTG, nhập hệ số/giá bán, xem Chính sách nội bộ) rồi duyệt. Mockup PTG chia phần nhập liệu sang YCTG. K7 đổi: người phụ trách lập **YCTG** (không phải PTG). Q7 (tiền tệ ở phiếu) ⇒ tiền tệ/tỉ giá ở **YCTG** |
| Q3 | Người tiếp nhận nhóm tra theo công ty nào | Công ty nhận hỏi giá | ✅ 10/10, **sửa theo Q4**: bỏ ô *Gửi tới công ty*; XNK = phân công hiệu lực (`assign_histories`, `buy_employee_id`) của (thương hiệu × hãng × **công ty phiếu**); KTMH cũng thuộc công ty phiếu. **Nhóm chưa phân công ⇒ CHẶN gửi YCHG**, báo tên hãng. Công ty 2/3/8 chưa có phân công ⇒ phải tự khai |
| Q4 | Duyệt PTG ghi giá cho công ty nào | Công ty người hỏi | ✅ 10/10 user: *"Không có việc tính giá hộ: cả luồng hỏi giá ⇒ YCTG ⇒ tính giá ⇒ duyệt giá (nếu bật) luôn theo 1 công ty ⇒ giá tính + duyệt xong lưu giá công ty đó, không ảnh hưởng công ty khác"*. Bỏ `@TODO-PHASE7`; form PTG nạp giá hiện hành + quy chế duyệt theo công ty phiếu |
| Q5 | PTG đi qua Duyệt giá bán (G5)? | Theo quy chế công ty | ✅ 10/10 **theo quy chế công ty như G5**: bật duyệt ⇒ giá vào màn Duyệt giá bán; hàng sang Đang kinh doanh, YCHG/YCTG sang Đã tính giá, KQ sinh ra **chỉ khi giá được duyệt**; bị từ chối ⇒ PTG mở lại cho sửa. Tắt ⇒ áp ngay |
| Q6 | Hệ số giá | Theo G4 | ✅ 10/10 **theo G4/ERP** — dùng chung `productPriceModel.js` (sửa Bán lẻ lan, vẫn sửa riêng được) |
| Q7 | Tiền tệ + tỉ giá đặt ở đâu | — | ✅ theo Q2: ở **YCTG** (XNK nhập), PTG kế thừa |
| Q8 | Lập PTG từ đâu | — | ✅ theo Q2 (1 YCTG – 1 PTG như ERP): KTMH lập từ YCTG **đã duyệt** của công ty mình (nút trên dòng YCTG + nút *Tạo phiếu tính giá* mở popup chọn YCTG đã duyệt) |
| Q9 | ĐVT | Tự nạp mọi ĐVT | ✅ 10/10 **YCHG chọn hàng, không chọn ĐVT**; YCTG/PTG tự bung đủ mọi ĐVT đã khai ⇒ duyệt xong đủ giá (BB2) |
| Q10 | Ghi đè `products.note`? | Không | ✅ 10/10 **KHÔNG ghi đè** — ghi chú chỉ ở dòng PTG/KQ |
| Q11 | Quyền | Gọn 3 quyền + phân công | ✅ 10/10 Lập YCHG **không cần quyền** · (1) **PTKD duyệt yêu cầu hỏi giá** · (2) **XNK xử lý yêu cầu hỏi giá** (duyệt nhóm + lập YCTG, kèm là người phụ trách hãng) · (3) **Tính giá bán hàng hoá** (duyệt/trả YCTG, lập + duyệt PTG). Xét trong công ty phiếu. **Bỏ 12 quyền phạm vi**: YCHG/KQ ai trong công ty cũng xem; YCTG/PTG chỉ người có (2), (3) hoặc 1092. Id mới (kiểm `uniq -d` + DB) |
| Q12 | Giá vốn công ty quản lý ở khối Chính sách / Tạm tính | Chỉ 1092 | ✅ 10/10 **chỉ người có 1092**; BE trả null, FE "—"; giá mua suy ra từ giá vốn cũng ẩn; giá bán luôn hiện |
| Q13 | Chụp chính sách lúc tính giá (C4) | Có | ✅ 10/10 **có chụp** vào dòng PTG |
| Q14 | Màn Chính sách giá bán nội bộ (§28, 1656) | Làm trong Phase 7 | ✅ 10/10 **làm trong Phase 7**, trước YCHG/PTG |
| Q15 | YCHG chọn hàng trạng thái nào | Cả mới lẫn đang KD | ✅ 10/10 **Đang nhập thông tin + Đang kinh doanh** của công ty mình. Hàng mới chuyển trạng thái theo K8; hàng đang KD giữ trạng thái, chỉ đổi giá khi duyệt. G4 vẫn dùng sửa giá nhanh |
| Q16 | Thông báo | Theo mốc ERP, lọc công ty phiếu | ✅ 10/10 gửi YCHG→PTKD · PTKD duyệt→XNK từng nhóm · từ chối→người lập · gửi YCTG→quyền Tính giá bán · KTMH trả→XNK · giá được áp→người lập YCHG (link KQ) + XNK · đủ nhóm→người lập YCHG. **Chỉ trong công ty phiếu** |
| Q17 | Bản in | In YCHG + YCTG | ✅ 10/10 **IN CẢ 4 chứng từ** (PTG/KQ thiết kế mẫu mới) — khuôn popup xem trước (skill print-page) |
| Q18 | Dữ liệu + ERP sau chuyển | Dùng lại bảng cũ | ✅ 10/10 **dùng lại 15 bảng + thêm bảng nhóm hãng YCHG + cột mới**; phiếu cũ hiện ở HRM như phiếu 1 nhóm. ERP chặn **toàn bộ** 4 chứng từ (kể cả xem) bằng middleware, chuyển link HRM, giữ tên route |

| Q19 | PTKD duyệt YCHG kiểm theo gì | — | ✅ 11/10 **giữ như ERP**: chỉ theo quyền *PTKD duyệt yêu cầu hỏi giá* (ERP `canApprove()` không đọc `brand_employee_id`); duyệt **cả phiếu**, không theo nhóm/phân công. Dữ liệu thật: ~43% phiếu do người không phụ trách hãng duyệt. **Phạm vi: duyệt MỌI phiếu trong công ty phiếu** (giữ Q11, không khôi phục 4 quyền phạm vi xem) |
| Q20 | Kết quả tính giá trả về đâu | Cách A | ✅ 11/10 **cách A (như ERP)**: KHÔNG có màn/menu KQ riêng; giá bán mới hiện ngay dưới nhóm đã tính giá trong YCHG + nút In kết quả; thông báo / link "xem giá bán mới" từ PTG đều về đúng nhóm trong YCHG. Vẫn ghi `price_calculate_results` (bản chụp lúc áp + bản in). Chỉ giá bán — không đưa giá NCC/chi phí ra YCHG (ERP đang lộ) |

## 3. Hệ quả cho bước sau

> ✅ T0 mockup dựng 11/10/2026 — `mockup-luong-tinh-gia.html`, xem `mockup-ghi-chu.md` (8 điểm tự chốt chờ user soát).

- **Mockup phải sửa** (bản chốt 30/09 không còn đúng): thêm màn YCHG (danh sách + form gom nhóm + duyệt PTKD/XNK theo nhóm) và KQ;
  nút ở màn Nhập thông tin đổi thành *Lập yêu cầu hỏi giá*; YCTG thành phiếu của 1 nhóm do XNK nhập giá NCC/thuế/chi phí + bước KTMH duyệt/trả;
  PTG kế thừa số YCTG, chỉ còn hệ số/giá bán + khối Chính sách; bỏ chọn ĐVT; vị trí menu 4 chứng từ + màn Chính sách (§28).
- Thứ tự đợt con dự kiến: T0 mockup · T1 Chính sách giá nội bộ · T2 nền CSDL (bảng nhóm, cột mới) + quyền · T3 YCHG · T4 YCTG · T5 PTG + ghi giá qua G5 + KQ · T6 bản in 4 chứng từ · T7 chặn ERP + nghiệm thu.
- Lỗi cũ ERP (mục 1) không vá: ERP bị chặn toàn bộ 4 chứng từ ⇒ tự hết.

## 4. Tồn vòng design (11/10/2026) — nguồn `khao-sat-hrm.md`, `khao-sat-csdl-chan-erp.md`

Kỹ thuật tự quyết (không hỏi): bảng mới `price_asking_request_groups` + `group_id` ở dòng YCHG/YCTG/log · `unit_id` dòng YCHG nullable (trống = mọi ĐVT) ·
mã trạng thái MỚI không đè mã cũ (YCHG 10; YCTG 5/6; PTG 5/6; nhóm dùng lại số YCHG cùng nghĩa) · UNIQUE 1 YCTG–1 PTG, 1 PTG–1 KQ (kiểm trùng trước) ·
cột chụp chính sách ở dòng PTG, giá vốn chụp chỉ trả khi có 1092 · `product_approves.price_calculate_id` để G5 báo ngược PTG ·
refactor lớp ghi giá G4/G5 nhận công ty + cho hàng trạng thái 1/2 (chạy lại 332 PHPUnit + e2e giá) · ERP: mở rộng `ProductMovedToHrm`, 41 route giữ tên, 5 link menu, gỡ `PriceCalculate.*` khỏi miễn audit; cron 01:00 không sửa.

| # | Câu | Đề xuất | Chốt |
|---|---|---|---|
| D1 | 30 phiếu dở hỏi chéo công ty | Dọn ở ERP | ✅ 11/10 **dọn ở ERP trước go-live**; runbook SQL kiểm còn 0 phiếu chéo dở mới deploy |
| D2 | Phiếu cũ | Backfill + đóng dở cũ | ✅ 11/10 **backfill 1 phiếu = 1 nhóm** (runbook) · phiếu dở trước 01/06/2026 đóng hàng loạt (lý do "chuyển hệ thống") · dở gần đây xử lý tiếp ở HRM · nháp giữ |
| D3 | XNK của nhóm | Tra phân công hiện hành | ✅ 11/10 **tra phân công hiện hành** (như ERP) cho nhóm chưa có YCTG; YCTG đã lập thuộc người lập, đổi người qua Bàn giao công việc; vẫn lưu tên người lúc gửi để tra cứu |
| D4 | "Đang tính giá" hàng × công ty | Thêm mã 5 | ✅ 11/10 **thêm `pcc.status = 5` Đang tính giá**; rà mọi chỗ đọc trạng thái (lọc 4 màn hàng hoá, hằng số, popup lấy về, cron ERP 14:30) xử mã 5 như mã 2 |
| D5 | G5 duyệt từng phần | Theo từng dòng | ✅ 11/10 **theo từng dòng**: dòng duyệt áp ngay; hàng sang Đang KD khi mọi ĐVT duyệt; có dòng từ chối ⇒ PTG "Giá bị từ chối", CHỈ mở lại dòng bị từ chối (dòng đã duyệt khoá); PTG Đã duyệt + kết quả khi mọi dòng duyệt |
| D6 | G4 vs PTG chờ duyệt | G4 chặn | ✅ 11/10 **G4 chặn dòng (hàng × ĐVT) đang có giá PTG chờ duyệt** ("Giá đang chờ duyệt ở PTG-xxxx"); chiều ngược: PTG không gửi duyệt dòng đang có yêu cầu G4 chờ duyệt; hàng chỉ nằm trong YCHG/PTG chưa gửi duyệt thì G4 vẫn sửa |
| D7 | Nhóm đã đóng | Không gửi lại | ✅ 11/10 **không** — nhóm đóng là kết thúc, hỏi lại thì lập YCHG mới |
| D8 | Prefix thông báo | [YCHG] [YCTG] [PTG] | ✅ 11/10 **[YCHG] [YCTG] [PTG]**; "giá đã áp" gửi người hỏi dùng [YCHG], link về nhóm trong YCHG |
| D9 | Id quyền | 1662–1664 + 1656 | ✅ 11/10 **type 8 Tài chính**: 1662 PTKD duyệt yêu cầu hỏi giá · 1663 XNK xử lý yêu cầu hỏi giá · 1664 Tính giá bán hàng hoá + seed 1656; seeder riêng idempotent; kiểm lại id trống ngay trước merge |
| D10 | Menu | — | ✅ 11/10 user: **YCHG ⇒ phân hệ Bán hàng · YCTG ⇒ phân hệ Bán hàng · PTG ⇒ phân hệ Tài chính**. (Màn Chính sách giá nội bộ + tên trùng Presale chưa nói ⇒ tạm giữ đề xuất: Chính sách ở Danh mục > Hàng hoá; giữ tên "Yêu cầu tính giá") |
| D11 | Dòng chi phí "Thuế nhập khẩu" | Ẩn | ✅ 11/10 **giữ như ERP** (vẫn cho chọn) |
| D12 | 3 thẻ dashboard ERP | Bỏ | ✅ 11/10 **bỏ** |
| D13 | §28 Chính sách: cấu trúc + tồn §28f | — | ✅ 11/10 cấu trúc (tự quyết theo mockup): bảng cha (công ty bán × hãng, cách tính) + bảng con (công ty mua, 2 %), tuỳ chọn "hệ số chung / theo công ty" lưu theo công ty bán; quyền 1656 |
| D13a | Giới hạn % | 0–100, cho 0 | ✅ 11/10 **0 ≤ % ≤ 100**, cho 0, tối đa 2 số lẻ |
| D13b | Popup chọn hãng | Mọi hãng | ✅ 11/10 **mọi hãng** (1.071), hiện số mã hàng của công ty bán, hãng 0 mã hiện xám "chưa có hàng" |
| D13c | Bỏ công ty mua / bỏ hãng | Xoá, giữ lịch sử | ✅ 11/10 **xoá cấu hình, lịch sử ghi "Xoá" kèm tỷ lệ cũ**; PTG đã lập giữ số chụp |
| P2 | Lưu hãng chưa khai công ty mua nào (ca 3M) | — | ✅ 11/10 user: **CÓ CHẶN** — đã chọn 1 hãng thì phải nhập đủ các thông tin; hiển thị dấu bắt buộc (*) ở các cột thông tin. ✅ 11/10 user xác nhận: "đủ" = **≥ 1 công ty mua có đủ 2 tỷ lệ** (giữ D13c — công ty để trống cả 2 ô = không có chính sách); chỉ chặn ca 0 công ty (3M). Dấu * ở cột Cách tính + 2 cột tỷ lệ. ✅ CODE 11/10 (user cho "làm") — nhánh `feat/t1b-chan-hang-rong`, xem `t1-plan.md` mục "T1b" |
| P1 | Hãng đã lưu: xoá khỏi lưới? | Có nút xoá | ✅ 11/10 user: **dùng KHOÁ (xoá mềm)** — hãng đã lưu có Khoá / Mở khoá (status cha 1 hoạt động · 2 khoá), không xoá cứng; ghi lịch sử nhóm *Thay đổi trạng thái*. Bỏ 1 công ty mua vẫn = xoá trắng 2 ô rồi Lưu (D13c). Tự chốt: chính sách hãng đang khoá coi như không có ⇒ khối Chính sách ở YCTG/PTG hiện "Chưa cấu hình" |
| D13d | Vị trí màn Chính sách | — | ~~menu "Cấu hình" dạng hub (mẫu Meeting)~~ ⇒ 🔄 **11/10 user đổi: Bán hàng › Quy chế - Thiết lập › Quy chế kinh doanh**, trang riêng rộng toàn khung `/sale/internal-price-policies` (hub làm panel co hẹp) |

| T2-C1 | close-stale: YCTG/PTG nháp của nhóm bị đóng | — | ✅ 11/10 user: **đóng nhóm, giữ chứng từ** (không xoá, không thêm trạng thái Huỷ). Ràng buộc T4/T5: nhóm đóng ⇒ BE 423 mọi thao tác ghi YCTG/PTG của nhóm, FE ẩn nút, hiện "Nhóm đã huỷ duyệt", chỉ xem |
