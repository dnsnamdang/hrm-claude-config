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

## 10831 vòng 2 (2026-08-20) — Hãng: auto-fill + multi (CHỜ USER CHỐT)
- [ ] 10831b — "Hãng" của KH sau chuyển giao chưa auto-fill + KH có nhiều hãng nhưng form chỉ chọn 1
      Data: Customer.customer_vehicle_manufacts = belongsToMany (nhiều hãng, pivot CustomerHasVehicleManufact). HỢP ĐỒNG (contractable) chỉ có 1 cột vehicle_manufact_id — applyCustomerToContract ghi 1 hãng khi duyệt.
      Form hiện: single-select list TẤT CẢ vehicleManufacts, ng-model vehicle_manufact_id, KHÔNG auto-fill khi chọn KH; getCustomerData không eager-load customer_vehicle_manufacts.
      → CHỜ USER quyết cách xử lý multi vs contract single (xem câu hỏi). Sau khi chốt sẽ sửa getCustomerData + applyNewCustomer + form.blade (+ store/show/approve nếu chọn lưu nhiều).

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
