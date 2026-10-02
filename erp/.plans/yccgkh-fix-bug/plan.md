# Plan: Fix 22 bug module YCCGKH (Phiếu YC chuyển giao khách hàng) — ERP

> Nguồn chính: bản B `d:\CompanyProject\hrm-cursor\TanPhatDev`, nhánh **task_10696**.
> Nguồn bug: Redmine http://quanly.dnsmedia.vn — dự án "Fix Bug - HRM (Nội bộ)".
> Tham khảo mô tả: `d:\CompanyProject\BANGIAO-YCCGKH.md` (mô tả theo bản A — verify code bản B trước khi tin).
> Trạng thái xác minh: đã đọc code bản B controller + index.blade.php ngày 2026-08-19.

## Trạng thái tổng
- Module đã dựng nền đầy đủ (Task 1→10 + "Fix E") trên task_10696.
- Bắt đầu vòng fix 22 bug Redmine: **CHƯA có bug nào trong 22 issue được fix** (đã verify nhóm action danh sách).

## Nhóm A — Màn danh sách + bộ lọc
- [x] 10867 — Sắp xếp lại thứ tự trường bộ lọc (cả DS + DS chờ duyệt) theo 3 hàng tài liệu [CODE XONG]
      · tắt search_by_time, đưa Từ ngày/Đến ngày thành cột date (created_from/created_to) đúng vị trí · search_columns reorder
- [x] 10846 — DS chờ duyệt thiếu bộ lọc Bộ phận [CODE XONG]
      · bật search_by_parts CHỈ cho big_boss/boss (manager đã có sẵn → tránh trùng), KHÔNG sửa lib dùng chung
- [x] 10853 — DS chờ duyệt thiếu Bộ phận + Trạng thái; bỏ `@if(!$isApprove)`; searchDataApprove [CODE XONG]
      · Trạng thái luôn render (bỏ @if) · searchDataApprove: mặc định CHO_DUYET, chỉ khi không chọn Trạng thái (Option 1) · applyFilters đọc created_from/created_to (parse d/m/Y qua normalizeFilterDate)
- [x] 10850 — Ngày lập/Ngày duyệt hiển thị dd/mm/yyyy hh:mm [CODE XONG] · buildDataTable format d/m/Y H:i
- [x] 10849 — Lọc Người lập trả 0 bản ghi [CODE XONG]
      · Gốc: DB có nhân viên trùng tên, route dùng chung trả cả người chưa lập phiếu → chọn nhầm id. Fix: endpoint riêng searchCreators lấy distinct created_by (id luôn khớp). KHÔNG sửa route dùng chung (370 màn).
- [x] 10848 — Combobox Người lập/Người duyệt trùng data [CODE XONG]
      · Cùng gốc 10849: endpoint riêng searchCreators/searchApprovers chỉ trả người thực sự lập/duyệt phiếu (distinct) → hết trùng.
- [x] 10851 — Phiếu "Đang tạo" thiếu action Xóa (Xem/Sửa/Xóa) + popup xác nhận + method destroy [CODE XONG, chờ verify browser]
      · route GET /{id}/delete → destroy · action Xóa (class delete + data-text) · popup "Bạn chắc chắn muốn xóa phiếu?" · Đồng ý→xóa+toast "Xóa phiếu thành công"
- [x] 10852 — Phiếu "Không duyệt": người tạo phải có Sửa + Xóa (hiện chỉ Xem) [CODE XONG, chờ verify browser]
      · action Sửa+Xóa khi Không duyệt & là người tạo · nới guard edit()/update() cho phép KHONG_DUYET · dùng chung destroy · data-text kèm số phiếu · (Xác nhận qua ảnh Redmine 14278: chỉ link màn sửa, KHÔNG đổi hành vi update)
- [x] 10869 — Màu link menu "…chờ duyệt" khác các mục khác → đồng bộ [CODE XONG]
      · topmenubar.blade.php dòng 2148: color #2957A3 → #212121 (khớp item anh em). GHI CHÚ: link trỏ customerHandover.index?type=waiting (có thể nên là customerHandover.all — ngoài scope 10869, cần user xác nhận).

### Checkpoint — 2026-08-19 (4)
Vừa hoàn thành: NHÓM A XONG 9/9 bug (code):
- 10848/10849: endpoint riêng searchCreators/searchApprovers (distinct created_by/approved_by) thay route dùng chung → hết trùng + lọc đúng. Route + url combobox đã trỏ lại. php -l pass.
- 10869: đổi màu link menu #2957A3 → #212121 (topmenubar.blade.php:2148).
Đang làm dở: chưa verify browser. Ghi chú: link menu "…chờ duyệt" trỏ customerHandover.index (có thể nên .all) — hỏi user.
Bước tiếp theo: user verify Nhóm A; hoặc sang Nhóm B (10868/10854/10855/10857).
Blocked: không.

### Checkpoint — 2026-08-19 (5) — VERIFY NHÓM A
Đã dựng server local từ bản B (php artisan serve :8001, DB erp_dev_30_01_26). Seed 5 permission module (id 1042-1046) + gán big_boss/duyệt cho user 13 (namdangit); tạo 4 phiếu TEST- (đã xóa 1 khi test). KHÔNG chạy full seeder (có truncate).
**VERIFY PASS toàn bộ Nhóm A 9/9 qua Playwright:**
- 10850 ngày có giờ; 10867 panel 12 trường đúng 3 hàng; 10846 Bộ phận cả 2 màn; 10853 Trạng thái luôn hiện + Option 1 (mặc định Chờ duyệt, lọc Không duyệt OK); 10851 Đang tạo Xóa (popup→xóa thật) + guard chặn Đã duyệt; 10852 Không duyệt Sửa+Xóa + edit guard vào được; 10848/10849 endpoint riêng trả 1 dòng id=13 khớp created_by; 10869 màu menu #212121.
Lưu ý phát sinh (không phải bug mới, chỉ lộ ở DB chưa seed): applyPermissionScope dùng hasPermissionTo() ném lỗi khi permission chưa tồn tại (blade dùng can() an toàn) — chỉ ảnh hưởng env chưa seed; env thật đã seed nên không lỗi. Chưa sửa (ngoài scope).
Test data/permission còn trên DB local: 3 phiếu TEST- + quyền cho user 13 (chờ user quyết dọn).
Bước tiếp theo: Nhóm B (10868/10854/10855/10857).

## Nhóm B — Màn xem chi tiết  ✅ VERIFY PASS 4/4
- [x] 10868 — Sắp xếp lại cột Lịch sử duyệt (Tài khoản·Nội dung·Hành động·Thời gian, bỏ STT) + viết hoa chữ đầu Hành động [XONG+VERIFY]
      · show.blade reorder thead/tbody + mb_strtoupper chữ đầu action (hiển thị, không đổi data lưu)
- [x] 10854 — Dòng "Gửi duyệt" hiển thị Lý do (reason) ở cột Nội dung [XONG+VERIFY]
      · controller store()+update(): logHistory('gửi duyệt', $handover->reason, ...)
- [x] 10855 — Ẩn action "Hủy duyệt" ở phiếu Đã duyệt (chỉ ẩn UI, giữ BE) [XONG+VERIFY]
      · show.blade comment nút Hủy duyệt (giữ route cancelApprove + JS doCancelApprove)
- [x] 10857 — Khi Duyệt gửi thông báo cho NV tạo phiếu [XONG+VERIFY]
      · approve() sau commit: NotificationHelper::sendNotify(created_by, url show, "<tên duyệt> đã duyệt phiếu YC chuyển giao khách hàng của bạn <mã>"); try/catch
- [x] (BONUS) Fix crash màn chi tiết phiếu Đã duyệt: model cast approved_at => datetime (trước đó $handover->approved_at là string → format() lỗi). Pre-existing, không thuộc 22 bug nhưng chặn xem phiếu Đã duyệt.

### Checkpoint — 2026-08-19 (6) — NHÓM B XONG + VERIFY
Fix + verify Playwright 4/4 Nhóm B (phiếu 2 test: gắn FirmContract 1043, approve OK → notify tạo đúng). Thêm cast approved_at=>datetime (fix crash màn Đã duyệt). php -l pass controller+model+show.blade.
Đã tạo thêm data test: history row phiếu 2, phiếu 2 giờ Đã duyệt (contractable 1043, không đổi dữ liệu HĐ vì new_customer_data rỗng). Notification test cho user 13 (+1).
Tiến độ: Nhóm A 9/9 ✅ · Nhóm B 4/4 ✅ · Nhóm C 0/8 · Nhóm D 0/1.
Bước tiếp theo: Nhóm C (form tạo/sửa: 10831/10833/10834/10835/10836/10837/10832/10838) — nặng, cần đọc form.blade + formJs kỹ.

### Checkpoint — 2026-08-19 (7) — NHÓM D (#10871) XONG CODE
Implement sync KH ERP→HRM (Option A, chỉ quotation). Sửa 3 file: hrm-api (Assign/Routes/api.php +route, QuotationController +erpSyncCustomer), ERP (Controller +syncCustomerToHrm gọi trong approve/cancelApprove). php -l pass cả 3. Verify ERP non-breaking OK (approve thành công dù HRM unreachable, log sync-fail). HRM end-to-end chờ dev-hrm (DB local thiếu bảng quotations). Dọn hrm_quotation_id giả trên contract 1043.
Tiến độ: A 9/9 ✅ · B 4/4 ✅ · D 1/1 ✅(code) · C 0/8.

### Checkpoint — 2026-08-19 (8) — NHÓM C phần lớn
Đối chiếu form bản B (khác UI ảnh QA bản A). Kết quả:
- ĐÃ OK sẵn bản B (verify): 10833, 10834 (field ẩn khi chưa chọn KH — verify DOM), 10837 (60MB).
- FIX (code, chờ verify UI cần contract+KH cá nhân): 10831 (auto-fill grant_date/location: searchCustomer select + setNewCustomer), 10836 (KH cá nhân → contact=chính KH), 10832 (validate size file client-side).
- CẦN QUYẾT ĐỊNH: 10835 (thiếu label Tỉnh/TP + searchbox + nguồn TK contact-vs-customer), 10838 (popup liên hệ logic mới giống báo giá — cần điều tra).
File chạm: controller (searchCustomer select), formJs.blade (setNewCustomer + save validate). Lint OK, form load OK, không JS error.
Tổng: 20/22 xử lý (A9+B4+D1+C6), còn 10835 (phần) + 10838 chờ quyết.

### Checkpoint — 2026-08-19 (9) — NHÓM C xong phần code
- 10835 FIX đúng tài liệu: nguồn STK = customer_accounts, 4 label (gồm Tỉnh/TP), option format chuẩn. searchCustomer eager-load customer_accounts.bank_province; onAccountChange đọc newCustomer.customer_accounts. Form load OK không JS error.
- 10838 điều tra xong: bản B đã show tất cả contact theo customer_id (không cần SĐT) — tốt hơn báo giá. Vế "người tạo/báo giá" mơ hồ → đề nghị BA làm rõ. Chưa code thêm.
TỔNG KẾT ĐỢT: 21/22 xử lý — A9 ✅verify · B4 ✅verify(+bonus cast) · D1 ✅code(ERP verify) · C: 10837/10834/10833 sẵn OK, 10831/10832/10836/10835 FIX(code, chờ verify UI cần contract+KH có data), 10838 phần lớn đạt + vế mở rộng chờ BA.
Verify UI form (10831/10832/10835/10836) + HRM #10871 end-to-end: cần môi trường dev (contract đủ ĐK + KH có TK/contact; DB HRM có bảng quotations).

### Checkpoint — 2026-08-19 (10) — VERIFY NHÓM C FORM PASS
Dựng test data trên KH 87 (cá nhân: grant_date 2019-06-03, grant_location, + 1 TK Vietcombank/CN Nghệ An/tỉnh TP HCM). Verify qua endpoint searchCustomer thật + Angular scope:
- 10831 ✅ grant_date/grant_location auto-fill.
- 10836 ✅ contact = chính KH (name/address/phone).
- 10835 ✅ TK từ customer_accounts, 4 label đủ (gồm Tỉnh/TP resolve bank_province).
- 10832 ✅ file 70MB → errors['files.0'] inline + loading.save=false (chặn submit).
=> Nhóm C: 10831/10832/10835/10836 FIX+VERIFY; 10833/10834/10837 sẵn OK; 10838 phần lớn đạt + vế mở rộng chờ BA.
**TỔNG KẾT: 21/22 fix+verify. Chỉ còn vế mở rộng 10838 chờ BA làm rõ.**
Test data còn trên DB local: phiếu TEST- (3), history phiếu 2, TK TEST123456 + grant_location trên KH 87, quyền module cho user 13. (Chờ user quyết dọn.)

### Checkpoint — 2026-08-19 (11) — 10838 XONG → 22/22
10838 FIX (union CustomerContact + firm_quotations contact, dedup) + VERIFY (KH 87 hiện contact báo giá; KH 13935 dedup 1 lần). Đã xóa BG test TEST-BG-87.
**🎉 22/22 BUG FIX. Verify: A9 + B4 + C8 chạy thực tế OK; D1 (#10871) ERP non-breaking OK (HRM end-to-end chờ dev-hrm).**
Test data local còn: phiếu TEST- (3: id2 Đã duyệt/3/4), history phiếu 2, customer_has_bank_accounts TEST123456 + grant_location trên KH 87, quyền module user 13. Chờ user quyết dọn + wrap up docs.

## Nhóm C — Màn tạo/sửa phiếu
> LƯU Ý: form bản B đã dựng lại (layout 2 cột KH trước/KH mới), KHÁC UI trong ảnh QA (bản A cũ) → nhiều bug đã xử lý sẵn. Verify theo code+app thật.
- [x] 10831 — KH cá nhân thiếu Ngày cấp/Nơi cấp [FIX: searchCustomer select thêm grant_date/grant_location; setNewCustomer auto-fill]. Hãng là select thủ công đã hiện (customers không có cột hãng). Chờ verify UI (cần contract + KH cá nhân có data).
- [x] 10833 — Cột "trước chuyển giao" [ĐÃ OK bản B]: bảng KH trước đã hiện Tên/Mã/Địa chỉ/SĐT/Fax/MST/CCCD/Ngày cấp/Nơi cấp/Người đại diện/Địa chỉ giao hàng/Số TK/Người liên hệ/Hãng. (Số TK chỉ hiện number+bank_name — chấp nhận.)
- [x] 10834 — Chưa chọn KH nhập được Nơi/Ngày cấp [ĐÃ OK bản B + VERIFY]: 2 field trong ng-if="isIndividualNew" → ẩn khi chưa chọn KH (verify: không render).
- [x] 10835 — Tài khoản ngân hàng đúng tài liệu [FIX]: nguồn STK = customer.customer_accounts (bảng customer_has_bank_accounts, "TK của KH") thay vì theo contact; option format "STK - tại NH {bank} chi nhánh {branch} - {account_name}" (native type-to-search); thêm đủ 4 label Tên TK/Ngân hàng/**Tỉnh/TP**/Chi nhánh (Tỉnh/TP resolve qua customer_accounts.bank_province). searchCustomer eager-load customer_accounts.bank_province; onAccountChange đọc từ newCustomer.customer_accounts. LƯU Ý: "searchbox" = type-to-search của native select (không dùng select2 để tránh xung đột AngularJS) — nếu QA cần select2 thì follow-up.
- [x] 10836 — KH cá nhân mục Liên hệ Tên/Địa chỉ/Điện thoại [FIX: setNewCustomer auto-set contact = chính KH khi cá nhân → label Địa chỉ/SĐT liên hệ hiện]. Chờ verify UI.
- [x] 10837 — Max file 50→60MB [ĐÃ OK bản B + VERIFY]: form hint "≤ 60MB" + StoreRequest max:61440.
- [x] 10832 — Upload > giới hạn loading vô tận [FIX: save() validate size client-side ≤60MB → báo lỗi inline dưới File + chặn submit; bản B đã có complete callback tắt loading nên không còn vô tận].
- [x] 10838 — Popup liên hệ [FIX+VERIFY]: searchContact = UNION (distinct) của (1) CustomerContact của KH (đã có, không cần SĐT) + (2) người liên hệ trên firm_quotations của KH (customer_contact_name/phone) — "đã phát sinh báo giá". Dedup theo customer_contact_id + SĐT. Verify: KH 87 (0 CustomerContact) → trả contact từ báo giá (from_quotation=true); KH 13935 (contact ở cả 2 nguồn) → hiện 1 lần không nhân đôi. [Diễn giải do Claude chốt — user duyệt qua kết quả.]

## Nhóm E — Dashboard phê duyệt
- [x] 10827 — Bổ sung box "YC chuyển giao khách hàng" trong group "Quản lý hợp đồng, đơn hàng" trên Dashboard phê duyệt [ĐÃ CÓ SẴN bản B + VERIFY]
      Box đã có từ Task 9: HomeController::approveList() dòng ~2617, group QUAN_LY_HOP_DONG, name "YC chuyển giao khách hàng chờ duyệt", count status=CHO_DUYET (where company_id = user company), link customerHandover.all, chỉ hiện khi can('Duyệt phiếu YC chuyển giao khách hàng'). Verify /admin/approveList: box trả về đúng group + count (0 khi không có phiếu Chờ duyệt → FE ẩn như các box khác; count=1 khi có phiếu Chờ duyệt). LƯU Ý: count chỉ scope theo company_id, chưa scope phòng ban/bộ phận như DS chờ duyệt (searchDataApprove applyPermissionScope) — refinement nếu QA cần khớp count.

## Nhóm D — Liên quan HRM (cần hrm-api/hrm-client)
- [x] 10871 — Duyệt YCCGKH trên ERP cập nhật KH sang báo giá HRM [CODE XONG; ERP verify non-breaking; HRM end-to-end chờ dev]
      Quyết định: Option A (HTTP endpoint hrm-api, chỉ quotation — theo user chốt). Map: contractable.hrm_quotation_id = id báo giá HRM.
      **HRM (hrm-api):** thêm route POST /api/v1/assign/quotations/erp-contract/{id}/sync-customer (nhóm erp-contract public, cùng erpMarkContract) → QuotationController::erpSyncCustomer ghi đè quotations.customer_id/code/name/tax_code/address/contact_name/contact_phone (FE tab Báo giá đọc trực tiếp).
      **ERP (TanPhatDev):** helper syncCustomerToHrm(handover, customerData) — Guzzle POST (connect_timeout 3, timeout 8), try/catch chỉ log. Gọi trong approve() (new_customer_data) sau notify, và cancelApprove() (old_customer_data) sau commit. Bỏ qua khi hrm_quotation_id null.
      Verify: ERP approve THÀNH CÔNG dù HRM sync fail (gắn hrm_quotation_id giả → log "Sync KH sang HRM thất bại" + phiếu vẫn Đã duyệt) → non-breaking OK. KHÔNG test được HRM end-to-end vì DB HRM local hrm_dev_30_01_26 (snapshot cũ) chưa có bảng quotations; route:list hrm-api lỗi do module Decision (env sẵn có). → verify trên dev-hrm (quotation 208 / project 253) sau deploy.

## Checkpoint
### Checkpoint — 2026-08-19
Vừa hoàn thành: Xác định nguồn chính = bản B; đọc controller + index.blade.php bản B; xác minh nhóm action danh sách (10851/10852/10853) đều CHƯA fix; tạo plan tracking.

### Checkpoint — 2026-08-19 (2)
Vừa hoàn thành:
- Lấy ảnh Redmine 10851 (14276), 10852 (14277/14278), 10853 (14279) → chốt spec.
- Fix 10851 + 10852: cột action (Sửa+Xóa cho người tạo khi Đang tạo/Không duyệt), method destroy, route GET /{id}/delete, nới guard edit()/update() cho KHONG_DUYET. php -l pass.
Đang làm dở: chưa verify trên browser (code local bản B chưa deploy lên dev-erp).
Bước tiếp theo: (a) user review/verify 10851+10852; (b) làm 10853 — cần bàn cách thêm bộ lọc Bộ phận (đụng lib DATATABLE dùng chung) trước khi sửa.
Blocked: không (browser đã mở được sau khi retry).

### Checkpoint — 2026-08-19 (3)
Vừa hoàn thành: Điều tra lib DATATABLE (partials/classes/base/Datatable.blade.php) — KHÔNG sửa lib. Gộp fix nhóm bộ lọc 10867+10846+10853+10850:
- index.blade: reorder search_columns theo layout 3 hàng tài liệu; tắt search_by_time → Từ ngày/Đến ngày thành cột date (created_from/created_to); Trạng thái luôn hiện (bỏ @if(!$isApprove)); bật search_by_parts cho big_boss/boss (tránh trùng manager).
- controller: applyFilters đọc created_from/created_to parse d/m/Y (helper normalizeFilterDate); searchDataApprove mặc định CHO_DUYET chỉ khi không chọn Trạng thái (Option 1); buildDataTable format d/m/Y H:i (10850).
- php -l pass. Xác minh bố cục 12 ô cho big_boss khớp tài liệu.
Đang làm dở: chưa verify browser (code local chưa deploy dev-erp).
Bước tiếp theo: user verify nhóm action (10851/10852) + nhóm bộ lọc (10867/10846/10853/10850); sau đó sang nhóm B (10868/10854/10855/10857).
Blocked: không.

## 10831 vòng 8 (2026-09-03) — 2 phản hồi (modal Thêm KH nhanh) — XONG cả 2 nhánh
- [x] K1. Modal #createCustomer/#searchCustomer không scroll → v1 thêm CSS max-height + overflow-y auto cho .modal-body (create/edit.blade). develop_01 `540e194ffe` (develop_01-only — task_10696 modal KH đơn giản).
- [x] K1(v2) — vòng 9 (2026-09-03). QA re-test dev-erp: đã pull + view:clear vẫn không scroll (loại Cá nhân). Soi Playwright LIVE dev-erp (login SSO): CSS v1 deploy ĐÚNG (max-height 1040, overflow-y auto) nhưng đẻ bug mới trên MÀN CAO (~1250px): `.modal-dialog-full{height:90%}=1125` < content 1173 → body chỉ cuộn ~4px, phần dôi đẩy dialog top=-261 → đỉnh form (Khách hàng/Loại hình) chui khỏi mép trên. Màn thấp 850px (local trước) không lộ nên v1 tưởng xong. FIX v2: bỏ cap max-height, `.modal-dialog{height:calc(100vh-20px);margin:10px auto}` + `.modal-content{max-height:100%;display:flex;flex-direction:column}` + header/footer `flex-shrink:0` + body `overflow-y:auto` → body là phần cuộn duy nhất, header ghim đỉnh, footer ghim đáy. develop_01 `bc646115f9` (develop_01-only). Verify Playwright dev-erp(inject) + local(file) @700px & 1250px: dialog_top=10, header/footer luôn hiện, body cuộn hết (498px @700), dialog đứng yên. **dev-erp cần pull `bc646115f9` + view:clear.**
- [x] K2. Tạo KH xong không lấy được CCCD/Ngày cấp/Địa chỉ. ROOT: form tạo KH gửi Ngày cấp/Sinh nhật d/m/Y ("28/08/2026") → CustomersController@store `Carbon::parse` THROW (verify tinker: "Could not parse '28/08/2026'") → store() fail (try/catch) → KH KHÔNG được tạo → không có gì load. FIX: helper parseFlexibleDate (d/m/Y ưu tiên, fallback Y-m-d, rỗng→null) thay Carbon::parse ở grant_date + date_of_birth. Backward-compatible. develop_01 `540e194ffe`, task_10696 `cf890d8dc5`. Verify: 28/08/2026→2026-08-28; 2026-08-28→2026-08-28; rỗng→null.
      Ghi chú: (a) applyNewCustomer đã verify CHẠY ĐÚNG với KH cũ 1730 (CCCD/grant/address load đủ) → không phải lỗi mapping. (b) Địa chỉ trống ở ảnh QA do user CHƯA chọn Tỉnh/Quận/Phường (ảnh: đều "Chọn...") — không phải bug. (c) CustomersController@store là code dùng chung — fix là chống throw, tương thích ngược. (d) Divergence: git handover page local từng thiếu searchCustomerJs/render form tạo KH; đã thêm searchCustomerJs (vòng 7) — dev-erp cần sync git để repro sạch.

## 10831 vòng 7 (2026-08-25) — 4 phản hồi — XONG J1/J3/J4 cả 2 nhánh; J2 chờ deploy
- [x] J1 + J4-tỉnh (dropdown Tỉnh/TP rỗng ở popup KH: bộ lọc + form tạo KH nhanh) — 2 nguyên nhân:
      (a) I3 khai `$scope.provinces=[mảng phẳng]` TRÙNG biến `provinces[nation_id]` của modal chung → đổi tên `contactProvinces`. develop_01 `b9a8c05d7d`, task_10696 `5a733a4b2a`.
      (b) create/edit.blade develop_01 THIẾU include `searchCustomerJs` → submitSearchCustomer/addCustomers/getProvinces/createCustomer không tồn tại → getProvinces không chạy. FIX: thêm include + openSearchCustomer gọi addCustomers() chung. develop_01 `bdd989cf46` (develop_01-only; task_10696 dùng modal KH riêng đơn giản, không có filter tỉnh). Verify :8001: getProvinces nạp 34 tỉnh, dropdown = 35 option. #createCustomer modal nằm trong searchCustomer.blade nên form tạo KH nhanh cũng có getProvinces.
- [x] J3 (Sinh nhật báo "Không hợp lệ" chặn tạo liên hệ): `<input type=date>` AngularJS bind Date object → jQuery serialize chuỗi locale → Laravel `date` fail. FIX toYmd() format Date→'YYYY-MM-DD'. develop_01 `ac8b9ecba4`, task_10696 `e13b61b4c0`.
- [x] J4-sort (sort cột bảng KH không chạy): orderBy('id','desc') hardcode đè request sort → CHỈ default khi request KHÔNG có order (chưa bấm cột); có order → Yajra sắp theo cột. Cùng commit J3.
- [x] J2 (File KH cũ vẫn "Chưa có tệp" dù đã deploy) — XONG. ROOT: đọc SAI cột. Class JS FirmContract getter `documents` (nguồn hiển thị file màn HĐ) = `this.attachments.split(', ')` → file ở cột **`firm_contracts.attachments`**, KHÔNG phải valid_approve_document (vòng 5 đọc sai). Fix parseContractFiles gộp attachments + add_addition_attachments + valid_approve_document. Verify tinker HĐ 6: snapshot files = [S3 url từ attachments]. develop_01 `c8d2be857a`, task_10696 `c9a214ec3f`.
      ⚠️ Divergence: create.blade develop_01 LOCAL không include searchCustomerJs (chỉ modal HTML + Customer class), nhưng dev-erp CÓ (QA thấy modal chạy) → local sau bản deploy. J1/J4-tỉnh sửa theo logic (rename biến) đúng dù local không repro đủ.

## 10831 vòng 6 (2026-08-25) — popup Tìm kiếm KH: sort + tab Cá nhân (làm RIÊNG) — XONG cả 2 nhánh
- [x] Popup Tìm kiếm KH 2 lỗi: (1) không sort KH mới nhất; (2) tab Cá nhân phải nhập SĐT mới hiện.
      Backend chung `Common\SearchController@searchCustomer` dùng 12 màn → LÀM RIÊNG, không đụng chung.
      **develop_01** (dùng modal CHUNG): endpoint riêng `customerHandover.searchCustomerList` (copy logic + orderBy id desc + cá nhân không bắt SĐT) + openSearchCustomer override `ajax.url` của 2 DataTable (#search-customer-table[-personal]) sang endpoint riêng (giữ modal/JS/luồng tạo KH chung). Commit `1d861ecc57`.
      **task_10696** (đã có picker RIÊNG sẵn = endpoint `customerHandover.searchCustomer`): sửa THẲNG method đó — bỏ where('id',-1) khi cá nhân rỗng SĐT + orderBy id desc. Commit `b1a8be3c00`. (không cần searchCustomerList/override)
      Verify :8001 cả 2: Tổ chức sort id desc (38311→); Cá nhân không SĐT ra 27132 bản ghi.

## 10831 vòng 5 (2026-08-25) — 3 fix tiếp — XONG cả 2 nhánh
- [x] File KH-trước rỗng dù HĐ có file: đọc SAI cột. form.documents = valid_approve_document (không phải add_addition_attachments). Fix snapshot GỘP cả 2 cột (helper parseContractFiles). develop_01 `39dd952c09`, task_10696 `64ba21e2e0`. ⚠️ Local không có file để verify → cần check dev-erp.
- [x] Đè chữ "Chưa có tệp": field File (form sectioned develop_01) dùng div trong custom-group (label nổi absolute) → cho container class form-control + min-height. develop_01 `39dd952c09`. (task_10696 File ở cell bảng, không đè.)
- [x] Form Thêm mới liên hệ quá ít field: bổ sung Họ tên/Chức vụ/Sinh nhật/Email/CCCD + SĐT nhiều số (+/-) + TK cá nhân; submitNewContact gửi đủ; thêm $scope.provinces. develop_01 `39dd952c09`, task_10696 `64ba21e2e0`.
- [x] Form Thêm mới "nhỏ chi chít" (user muốn giống form chung): USER chốt giữ modal riêng, bố cục lại. Sắp xếp đúng layout form liên hệ chung: Họ tên(*)/CMT · Email/Chức vụ(*)/Sinh nhật · SĐT(*) nhiều số · Số TK cá nhân/Chủ TK/Ngân hàng · Tỉnh-TP(select)/Chi nhánh. Đổi TK bảng nhiều dòng → 1 TK phẳng (submitNewContact build accounts khi có số TK). develop_01 `f1a3357a6d`, task_10696 `4b7bccb53e`. Verify: 11 field đúng thứ tự, field rộng 353px (col-6). LƯU Ý: KHÔNG dùng lại modal chung searchContact vì backend chung customerSearchContact validate phone required (gốc 10838) — sửa backend chung = đụng nhiều màn, user chọn không đụng.

## 10831 vòng 4 (2026-08-25) — 3 phản hồi tiếp — XONG develop_01 (chờ port task_10696)
- [x] I1 (=H). KH TRƯỚC thêm File đính kèm — commit `aa612c3979`. Snapshot 'files' từ `firm_contracts.add_addition_attachments` (split ", "); before-panel ① thêm mục File đính kèm link (helper getFileName), rỗng="Chưa có tệp". WrService không có cột file → []. Verify HĐ 21 (files=[], getFileName OK).
- [x] I2. KH TRƯỚC Tỉnh/TP tài khoản NH — commit `aa612c3979`. Snapshot account thêm bank_province_name (Province::find từ bank_province_id), cả FirmContract + WrServiceContract. Verify HĐ 21: "Tỉnh Bắc Ninh".
- [x] I3. Popup liên hệ + Thêm mới + cột — commit `f4fcc621b0`. searchContactModal: thanh Tìm (textbox+nút) + nút Thêm mới + form thêm inline (Tên/SĐT/Chức vụ); bảng STT/Tên/SĐT/Chức vụ/Thao tác. formJs: loadContacts/searchContactSubmit (server-side)/toggleAddContact/submitNewContact (POST customerAddContact → reload + tự chọn). Verify KH 100: cột đúng (Chức vụ=Thủ Kho), Tìm "Thăng"→1, form Thêm mới hiện.
  → ĐÃ PORT task_10696 (commit `13c4bbaa2a`): I1/I2 backend snapshot; I1 before-panel table thêm dòng File đính kèm; I2 dòng TK thêm chi nhánh + Tỉnh/TP; I3 modal (copy) + formJs functions. Verify :8001 HĐ 21/KH 100 OK. (F sectioned-specific — không áp form 2 cột task_10696; G task_10696 hiện sẵn 2 dòng MST+CMND.)

## 10831 vòng 3 (2026-08-25) — QA phản hồi 8 điểm (Nguyễn Minh Hằng) trên dev-erp
> ⚠️ dev-erp đang chạy develop_01 CŨ (ảnh QA: "tối đa 10 MB" + "Hãng: Chọn hãng" select) → nhiều điểm ĐÃ fix trong develop_01 chưa deploy. Cần deploy develop_01 mới trước, rồi re-test.
> Test data QA: KH "etek green"/"vesta"/"Toyota Hà Đông"; HĐ HĐDA_TPE_HN_NSHC_26_0006_123 và _0007_123456765432; KH HRM 38336.

- [x] A. Địa chỉ giao hàng KH TRƯỚC không hiện — XONG develop_01 (commit `422ed159f8`). Là panel KH-trước (snapshot). Accessor FirmContract::delivery_place lấy từ firm_quotation/parent → rỗng với HĐ từ báo giá HRM. Snapshot fallback customer_address (khớp màn chi tiết HĐ). (chờ port task_10696)
- [x] B. TK ngân hàng "ngân hàng null chi nhánh hoàn kiếm" — XONG develop_01 (commit `0b282a4514`). CustomerHasBankAccount thêm relation bank()+branch(); getCustomerData eager-load; helper accountBankName/accountBranchName ưu tiên relation fallback cột string; onAccountChange + accountOptionLabel dùng helper. Verify KH 360. (chờ port task_10696)
- [ ] C. Popup Tìm kiếm liên hệ chưa đúng: cần show sẵn data người đó tạo / đã phát sinh báo giá (logic cũ phải nhập SĐT). ĐÃ fix ở 10838 (develop_01 chưa deploy) → verify sau deploy; bổ sung nếu thiếu.
- [ ] D. KH cá nhân: show sẵn data người tạo/đã phát sinh báo giá (không cần tìm SĐT). Liên quan 10836/10838 → verify sau deploy.
- [ ] E. Địa chỉ ngân hàng KH chỉ đúng STK, còn lại sai (= B). Dùng HĐ _0006_123. (NEW — gộp với B)
- [x] F. KH cá nhân chỉ 2 mục — XONG develop_01 (commit `61bb97718a`). Panel KH-sau ẩn section ③ Liên hệ khi isIndividualNew. Verify DN=3 mục/CN=2 mục. (chờ port task_10696)
- [x] G. Mất CMND KH vesta — XONG develop_01 (commit `61bb97718a`). Là panel KH-TRƯỚC (snapshot). FirmContract snapshot customer_tax_code=null → DN bind rỗng. Fix: DN fallback customer_tax_code||customer_identity. (chờ port task_10696)
- [ ] H. KH TRƯỚC: thiếu file đính kèm. User làm rõ: là file ở mục "File đính kèm" trong "Thông tin Báo giá - KH" của chi tiết HĐ. Nguồn = cột `firm_contracts.add_addition_attachments` (chuỗi path S3 nối ", ", parse thành mảng URL, href trực tiếp). CHƯA làm: (1) snapshot thêm 'files' => explode(', ', add_addition_attachments); (2) before-panel thêm mục File đính kèm hiện link. ⚠️ Local không có data để verify; WrServiceContract chưa rõ cột file. CHỜ: xác nhận + verify trên dev-erp.
      ⚠️ DIVERGENCE: panel KH-trước bản deploy dev-erp CÓ sẵn field "File đính kèm: Chưa có tệp" nhưng develop_01 (git) KHÔNG có → xem ghi chú divergence cuối mục.

> ⚠️ DIVERGENCE dev-erp vs git (2026-08-25): bản form YCCGKH trên dev-erp chứa "tối đa 10 MB" + panel KH-trước "File đính kèm" — grep `--all` KHÔNG có ở bản A, bản B, hay github origin/develop_01 (đã fetch). Nghĩa dev-erp CHƯA sync với develop_01 git (deploy bản cũ/ngoài git). User xác nhận mô hình: dev-erp=develop_01, code YCCGKH ở task_10696 merge vào develop_01. → cần deploy develop_01 git mới nhất lên dev-erp để QA thấy fix.

## 10831 vòng 2 (2026-08-20) — Hãng: hiển thị đủ hãng của KH (USER CHỐT: theo logic multi mới)
- [x] 10831b — "Hãng" của KH sau chuyển giao hiển thị ĐỦ hãng của KH (KH nhiều hãng) — XONG cả 2 nhánh
      Đã làm: (a) eager-load customer_vehicle_manufacts (searchCustomer @task_10696 / getCustomerData @develop_01); (b) setNewCustomer/applyNewCustomer set vehicle_manufact_names = join tên hãng + vehicle_manufact_id = hãng ĐẦU (áp HĐ khi duyệt); (c) form.blade đổi single-select (list toàn hệ thống) → input readonly hiện tên các hãng KH; (d) thêm vehicle_manufact_names vào form model init + edit-prefill + store flatKeys.
      Commit: develop_01 `7cc534f7bb`; task_10696 `935d7f9f06`.
      Verify :8001 (develop_01, KH 823 có 4 hãng): ô Hãng = "Hyundai, MG, Nissan, Toyota" readonly, vehicle_manufact_id=121 (hãng đầu). task_10696 cùng logic mapping (verify by parity).
      Ghi chú: cột KH-TRƯỚC vẫn hiện 1 hãng (oldVehicleManufactName) vì lấy từ snapshot HĐ — HĐ chỉ 1 cột, đúng.

  > (Lịch sử phân tích — mô tả gốc trước khi làm)
      Issue 10831 (đọc Redmine): "Không hiển thị Ngày cấp, Nơi cấp, Hãng sau khi chọn KH → Expected: hiển thị đủ TẤT CẢ thông tin KH". = yêu cầu HIỂN THỊ. Ngày/Nơi cấp đã xong (readonly auto-fill). Hãng còn thiếu.
      USER chốt: KH giờ chọn nhiều hãng (Customer.customer_vehicle_manufacts belongsToMany), single cũ là SAI → hiển thị TẤT CẢ hãng của KH, readonly auto-fill (giống Ngày/Nơi cấp), bỏ select thủ công.
      Downstream: HĐ (FirmContract+WrServiceContract) chỉ 1 cột vehicle_manufact_id (migration 2026_02_02) → khi duyệt applyCustomerToContract lấy HÃNG ĐẦU của KH.
      2 nhánh khác cơ chế nạp KH: task_10696 = searchCustomer+setNewCustomer; develop_01 = getCustomerData+applyNewCustomer → sửa riêng từng nhánh.
      Việc: (a) eager-load customer_vehicle_manufacts; (b) set list names + vehicle_manufact_id=hãng đầu khi chọn KH; (c) form.blade đổi select→ô readonly hiện tên các hãng (join ", "); (d) lưu vehicle_manufact_names cho show/print/edit-fallback.

## Đợt QA phản hồi (2026-08-20) — 5 task bị trả lại + xử lý trên develop_01

> Bối cảnh: QA test trên dev-erp = nhánh **develop_01** (form sectioned ①②③, KHÁC form 2 cột của task_10696). Nhiều fix trước làm trên form task_10696 nên KHÔNG hiện trên develop_01. → phải sửa lại từng task trên develop_01, đồng thời giữ task_10696 (→ master) cũng đúng.

- [x] 10848/10849 — Combobox "Người lập"/"Người duyệt" bộ lọc phải hiện FULL nhân viên như các màn sale khác
      Root: fix cũ (searchCreators/searchApprovers trả distinct người đã lập/duyệt) SAI hướng → chỉ hiện vài người. QA muốn giống mọi màn sale (dùng chung `employee.searchEmployeeByKeyword?all_status=1`).
      Fix: index.blade 2 combobox trỏ `employee.searchEmployeeByKeyword?all_status=1`; XÓA 2 route search-creators/search-approvers + 3 method dead searchCreators/searchApprovers/buildPeopleFilterOptions.
      Nhánh: task_10696 commit `83de93521a`; develop_01 merge `a56935c94c` (resolve conflict giữ getCustomerData + 10835, bỏ dead methods).
      Verify :8001: endpoint chung trả 200 NV/trang (id+text "Mã PB - Tên") ✓.

- [x] 10838 — Popup người liên hệ trên develop_01 vẫn "Không có dữ liệu" tới khi nhập SĐT
      Root: form sectioned develop_01 nối nút liên hệ vào modal CHUNG `#searchContact` (customerSearchContact, bắt nhập SĐT) trong khi ĐÃ CÓ modal riêng `#searchHandoverContactModal` + `openSearchContact()` (load ngay qua customerHandover.searchContact) nhưng chưa được include/nối.
      Fix (develop_01, commit `2db914dd8f`): form.blade nút → `openSearchContact()`; create/edit.blade include `partials.searchContactModal` thay modal chung; formJs `setContact` hide đúng `#searchHandoverContactModal` (trước hide nhầm `#searchContact`).
      task_10696 (→ master) ĐÃ đúng sẵn (nút gọi openSearchContact + include modal riêng) — không cần đụng.
      Verify :8001: mở popup KH id=100 → 12 liên hệ hiện ngay không nhập SĐT; click Chọn → điền contact_name/phone + đóng modal ✓.

- [x] 10832 — Tải file > giới hạn: loading vô tận, không báo lỗi, vẫn cho Lưu (develop_01)
      save() develop_01 ĐÃ validate MAX_FILE_SIZE 60MB (return sớm, không bật loading) + complete callback luôn tắt loading → không kẹt. NHƯNG form.blade develop_01 chỉ set class 'error' (viền) + hiện errors['files'] (key chung), KHÔNG hiện text errors['files.N'] → QA không thấy dòng báo lỗi.
      Fix (develop_01 commit `ec9401025e`): thêm span ng-repeat hiện `errors['files.'+$index]` ngay dưới trường File. task_10696 (→ master) ĐÃ có sẵn dòng này (form.blade line 471) — không cần đụng.
      Verify :8001 (develop_01): inject file 70MB → text đỏ "File big.pdf vượt quá 60MB" dưới trường File, loading.save=false, không submit ✓.

- [x] 10837 — Hint file trên develop_01 vẫn "50MB" (yêu cầu 60MB)
      Fix develop_01 (session trước): form.blade hint "tối đa 50 MB" → "tối đa 60 MB".

- [x] 10835 — Tài khoản NH trên develop_01 phải theo DS TK của KH (customer_accounts) + đủ Tỉnh/TP
      Fix develop_01 (session trước): getCustomerData eager-load `customer_accounts.bank_province`; form.blade select TK nguồn `newCustomer.customer_accounts`; formJs onAccountChange đọc customer_accounts + set account_bank_province_name.
      Verify :8001: KH 87 → TK Vietcombank/CN Nghệ An, Tỉnh/TP "Thành phố Hồ Chí Minh" ✓.

- [x] 10834 — Ngày cấp / Nơi cấp vẫn nhập tay được → phải readonly auto-fill từ KH
      Root: 2 ô grant_date/grant_location là thuộc tính KH sau chuyển giao (applyNewCustomer/setNewCustomer auto-fill), nhưng để ng-model editable → user gõ tay "sss".
      Lần 1 (chưa đủ): thêm `ng-disabled="!newCustomer"` — QA phản hồi lại: KHI ĐÃ chọn KH vẫn gõ được (ảnh MST 0100819515 + "sss").
      Lần 2 (chốt): đổi sang `disabled` cứng, giữ ng-model để nhận auto-fill + submit → readonly như các field anh em (Tên/MST/Fax).
      Nhánh: develop_01 `3d7dd20ea9` (lần 1) → `e8c654f615` (lần 2); task_10696 `fb71332cd9` (lần 1) → `27f8995da0` (lần 2).
      Verify :8001 (develop_01): chọn KH 87 → Ngày cấp "2019-06-03" + Nơi cấp "Cục CSQLHC..." auto-fill, disabled=true, model giữ giá trị ✓.

### Checkpoint — 2026-08-20 — XỬ LÝ ĐỢT QA PHẢN HỒI
Vừa hoàn thành: 5 task QA trả lại (10848/10849 combobox, 10838 popup liên hệ, 10837 60MB, 10835 TK theo KH, 10834 chặn nhập) — fix + verify live :8001 trên develop_01; đồng bộ task_10696 nơi cần (combobox, 10834).
Commit develop_01: 83de93521a → a56935c94c → 2db914dd8f → 3d7dd20ea9. task_10696: 83de93521a + fb71332cd9.
Đang làm dở: chưa push develop_01 lên dev-erp.
Bước tiếp theo: user push develop_01 → dev-erp cho QA re-test 5 task này; rà thêm task QA còn phản hồi (nếu có).
Blocked: không.
Lưu ý kiến trúc: form develop_01 (sectioned) ≠ form task_10696 (2 cột) → fix cấp form phải maintain cả 2 nhánh; fix cấp list/combobox dùng chung, merge được.

### Checkpoint — 2026-09-03 — K1(v2) SCROLL MODAL THÊM KH (soi live dev-erp)
Vừa hoàn thành: K1(v2) — root thật của "không scroll" KHÔNG phải deploy. CSS v1 (max-height cap) đã deploy đúng nhưng gây lỗi mới trên màn cao: dialog height:90% < content → đỉnh form chui khỏi mép trên. Sửa sang flex column (body cuộn duy nhất, header/footer ghim). develop_01 `bc646115f9`.
Cách phát hiện: đăng nhập SSO dev-erp bằng Playwright, đo getBoundingClientRect thật (dialog_top=-261) — đây là lần đầu soi trực tiếp dev-erp thay vì đoán "chưa deploy".
Verify: Playwright dev-erp(inject flex) + local(render từ file) ở 700px & 1250px — header ghim đỉnh, footer ghim đáy luôn hiện, body cuộn hết, dialog đứng yên.
Đang làm dở: chưa push. task_10696 KHÔNG cần (modal KH riêng đơn giản, không có #createCustomer/K1).
Bước tiếp theo: user pull `bc646115f9` lên dev-erp + `php artisan view:clear` → QA re-test loại Cá nhân màn cao.
Blocked: không.

- [x] K1(v3) — vòng 10 (2026-09-03). ROOT THẬT, không phải CSS. QA/user: "đổi Loại hình tổ chức xong kéo bị kẹt / tự nhảy lên đầu". v1 (cap max-height) + v2 (flex column) đều KHÔNG trị được.
      Chẩn đoán: trap `scrollTop` setter trên `.modal-body` → stack `select2.min.js:48290` → `jQuery.scrollTop` ép scrollTop về giá trị cũ. `jQuery._data(body,'events')` lộ handler `scroll.select2.select2-<id>` còn sống dù KHÔNG có dropdown nào đang mở → handler MỒ CÔI.
      Cơ chế: select2 mở dropdown → gắn `scroll.select2-<id>` lên scroll-parent (.modal-body) để ghim vị trí dropdown. AngularJS đổi Loại hình tổ chức → huỷ & dựng lại block DOM → select2 mất theo DOM, `close` không chạy → handler ở lại ghim cứng scrollTop. Đổi càng nhiều lần càng nhiều handler.
      Vì sao test tự động không ra (bài học): select2 chỉ gắn handler khi có thao tác CHUỘT THẬT (mở dropdown); synthetic event không kích hoạt → mọi vòng test tự động đều "pass" sai. Phải nhờ user thao tác tay + gắn bẫy (wrap focus/scrollIntoView, trap scrollTop setter, log jQuery._data events) mới bắt được.
      FIX: dọn handler select2 mồ côi trên .modal-body khi không còn `.select2-container--open` — trigger lúc user chạm vùng cuộn (wheel/touchmove/mousedown) + sau mỗi lần đổi select (setTimeout 300ms). Đặt trong create/edit.blade của màn, KHÔNG đụng file dùng chung `searchCustomerJs`. Giữ CSS flex v2.
      develop_01 `5e73b06eec` (develop_01-only). Verify dev-erp + local: tạo handler mồ côi thật → sau fix `jQuery._data` trả `none`, scrollTop hết bị ép về giá trị cũ.

### Checkpoint — 2026-09-03 (2) — K1(v3) ROOT THẬT: select2 orphan handler
Vừa hoàn thành: tìm ra root thật sau 3 vòng (v1 CSS cap → v2 CSS flex → v3 JS orphan handler). Nguyên nhân là handler `scroll.select2-<id>` mồ côi do Angular re-render huỷ select2 giữa chừng, KHÔNG phải layout. develop_01 `5e73b06eec`.
Bài học quy trình (ghi để không lặp): (a) đo `body.scrollTop` nhúc nhích ≠ hết bug — triệu chứng thật là scroll bị GHIM/đỉnh form bị đẩy; (b) synthetic event không kích hoạt select2 → test tự động pass sai, phải nhờ user thao tác tay; (c) khi user báo "vẫn lỗi" 2-3 lần thì dừng vá tiếp, chuyển sang gắn bẫy đo (trap setter/log events) để tìm thủ phạm.
Đang làm dở: chưa push. task_10696 KHÔNG cần (modal KH riêng, không có #createCustomer + select2 trong modal).
Bước tiếp theo: user pull `bc646115f9` (CSS flex) + `5e73b06eec` (orphan fix) lên dev-erp + `php artisan view:clear` → QA test tay: cuộn giữa, đổi Loại hình tổ chức nhiều lần.
Blocked: không.

- [x] K1(v4) — chuyển fix orphan select2 vào FILE DÙNG CHUNG (user duyệt phương án 2, 2026-09-03).
      Lý do: modal `#createCustomer` / `#searchCustomer` (`partials/modals/searchCustomer`) được **57 màn** dùng (opening_contracts, payment_profile, buyDebtBeginning, assembly_requests, service_quotations, warranty_repair_requests, buy_contract2…) → bug ghim scroll tồn tại ở TẤT CẢ, không riêng YCCGKH. Đặt fix ở blade 1 màn chỉ trị 1/57.
      Thay đổi: thêm khối dọn handler `.k1orphan` vào `resources/views/partials/modals/js/searchCustomerJs.blade.php` (cạnh chỗ init select2); gỡ bản đặt riêng trong create/edit.blade YCCGKH để không gắn trùng. `$(document).off('.k1orphan')` trước khi gắn → idempotent khi file include nhiều lần.
      Nhánh: task_10696 `ec511fc7cc` (file dùng chung); develop_01 `2ed8a65613` (cherry-pick) + `2fc4c22219` (gỡ bản riêng). File dùng chung 2 nhánh giống hệt nhau trước khi sửa → không conflict.
      Verify :8001 (develop_01, script load từ file dùng chung): (a) tạo handler mồ côi thật → lăn chuột → `jQuery._data` trả `none`, scroll hết bị ghim ✓; (b) AN TOÀN: khi dropdown ĐANG mở, lăn chuột → handler `scroll.select2` giữ nguyên, dropdown vẫn mở → không phá select2 đang dùng ✓.
      ⚠️ Lưu ý khi bàn giao: đây là sửa FILE DÙNG CHUNG → nên QA thêm vài màn đại diện ngoài YCCGKH (vd service_quotations, warranty_requests, buy_contract2) xem modal Tìm/Thêm KH còn chạy bình thường.
      Ghi chú task_10696: màn YCCGKH của nhánh này dùng modal RIÊNG `#searchHandoverCustomerModal` (chỉ 1 ô tìm + 1 bảng, không select2, không cuộn dài) → không dính bug; commit ở đây là để các màn KHÁC của nhánh cũng được fix. Modal Người liên hệ `#searchHandoverContactModal` (cả 2 nhánh) dùng `<select>` thuần, không select2 → cũng không dính.

### Checkpoint — 2026-09-03 (3) — K1 hoàn tất, fix nằm ở file dùng chung
Vừa hoàn thành: chuyển fix orphan select2 từ blade YCCGKH sang `searchCustomerJs.blade.php` (dùng chung 57 màn) theo quyết định của user. Verify cả tác dụng lẫn tính an toàn trên :8001.
Trạng thái commit: task_10696 `ec511fc7cc`; develop_01 `2ed8a65613` + `2fc4c22219` (+ CSS flex `bc646115f9`).
Đang làm dở: chưa push (theo quy tắc không tự push).
Bước tiếp theo: user pull lên dev-erp + `php artisan view:clear` → QA test tay YCCGKH (cuộn giữa, đổi Loại hình tổ chức nhiều lần) + spot-check vài màn khác dùng modal chung.
Blocked: không.
Việc còn treo (user hỏi, chưa quyết): modal Thêm nhanh KH KHÔNG có khối "Địa chỉ giao hàng" (form KH đầy đủ có — `customerForm.blade.php:1332` + modal `deliveryPlace` + class `DeliveryPlace`). Chưa rõ có phải yêu cầu QA hay không → chờ user quyết có bổ sung vào modal dùng chung không.

## Testcase (2026-09-03)
- [x] Sinh testcase luồng YCCGKH → `testcase.xlsx` (96 TC, P0 58%), generator `gen_testcase.py` dùng `tc_engine.py` của skill.
      Nguồn dữ liệu: đọc code thật (5 quyền trong blade/controller, 5 trạng thái phiếu, guard sửa/xóa theo trạng thái + người lập,
      rule validate trong CustomerHandoverStoreRequest, cột & bộ lọc trong index.blade, nhãn nút Lưu nháp / Lưu & Gửi duyệt / Duyệt / Không duyệt).
      Cấu trúc: 11 TC phân quyền (đủ 5 quyền + không quyền + 4 TC gọi thẳng chức năng bỏ qua giao diện) + 10 section La Mã.
      Bao phủ toàn bộ bug đã fix đợt này: file đính kèm KH cũ, Tỉnh/TP, hãng xe nhiều giá trị, Ngày cấp/Nơi cấp readonly,
      sort KH mới nhất, tab Cá nhân, ngày d/m/Y khi thêm nhanh KH, sinh nhật người liên hệ, cuộn cửa sổ Thêm KH (K1).
- [x] ⚠️ PHÁT HIỆN KHI VIẾT TC — LỆCH GIỚI HẠN DUNG LƯỢNG TỆP → ĐÃ FIX (user chốt: nâng lên 60MB):
      Màn hình ghi "tối đa 60 MB" và chặn tại chỗ khi > 60MB (formJs: MAX_FILE_SIZE = 60*1024*1024),
      nhưng hệ thống phía sau chỉ nhận tối đa 50MB (CustomerHandoverStoreRequest: `files.*` max 51200 KB,
      thông báo "File vượt quá 50MB"). → Tệp 50–60MB qua được kiểm tra trên màn nhưng bị từ chối khi lưu.
      Đã đưa vào TC_08.008 (P0) + ghi ở mục 9 phần mô tả. Hướng xử lý: nâng giới hạn phía sau lên 60MB
      (đúng với yêu cầu 10832/10837) HOẶC hạ ghi chú trên màn xuống 50MB — cần user chốt.

      **Đã xử lý 03/09/2026**: develop_01 `c05ccf25be` — `files.*` max 51200 → 61440 KB, thông báo đổi thành "File vượt quá 60MB". Verify ngưỡng: nhận 40/55/59MB, từ chối 61/70MB — khớp mức chặn của giao diện; máy chủ cho tải lên tới 2G nên không vướng.
      ⚠️ **task_10696 KHÔNG cần sửa — đã để sẵn 61440 từ trước**; chỉ develop_01 bị tụt lại (lệch nhánh).
      Testcase đã cập nhật theo: TC_08.008 đổi kỳ vọng thành tệp 55MB PHẢI lưu được; bổ sung TC_08.009 (P1) kiểm mốc biên 59MB nhận / 61MB chặn; mục 9 BẪY 1 viết lại. Tổng TC: 96 → **97**, P0 58%.
