# Spec chi tiết — Fix 22 bug YCCGKH (Phiếu YC chuyển giao khách hàng)

**Ngày:** 2026-08-19 · **Owner:** @junfoke · **Repo:** ERP `hrm-cursor/TanPhatDev` nhánh `task_10696` (+ hrm-api Modules/Assign cho #10871)

## 0. Bối cảnh / bẫy
- **2 bản TanPhatDev:** bản A `d:\CompanyProject\TanPhatDev` (HEAD cf020c8633, hướng cherry-pick, khớp BANGIAO-YCCGKH.md) vs **bản B `d:\CompanyProject\hrm-cursor\TanPhatDev` = NGUỒN CHÍNH** (module dựng lại Task 1→10). Fix chỉ trên bản B, nhánh task_10696.
- Form bản B đã dựng lại (layout 2 cột KH trước/KH mới) KHÁC UI ảnh QA (bản A cũ) → nhiều bug đã xử lý sẵn, phải verify code+app thật.
- Verify: `php artisan serve --host=127.0.0.1 --port=8001` từ bản B, login namdangit@gmail.com/Dnsmedia@2023 (Employee id 13). Seed 5 quyền module (id 1042–1046, guard web) + givePermissionTo user 13 (KHÔNG chạy full PermissionsTableSeeder — có truncate). DB local erp_dev_30_01_26.

## 1. File chạm
**ERP (TanPhatDev):**
- `app/Http/Controllers/Sale/CustomerHandoverRequestController.php` — action column, destroy, guard edit/update, applyFilters (created_from/to + normalizeFilterDate), searchDataApprove, buildDataTable (d/m/Y H:i), searchCreators/searchApprovers/buildPeopleFilterOptions, searchCustomer (select grant_date/location + eager customer_accounts.bank_province), searchContact (union báo giá), approve (notify + sync HRM), cancelApprove (sync HRM), syncCustomerToHrm.
- `app/Model/Sale/CustomerHandoverRequest.php` — cast approved_at=>datetime.
- `routes/web.php` — thêm GET /{id}/delete, /search-creators, /search-approvers.
- `resources/views/sale/customer_handover_requests/index.blade.php` — search_columns reorder + cột date + status luôn hiện + search_by_parts + url combobox mới.
- `.../show.blade.php` — bảng lịch sử duyệt (cột+viết hoa), ẩn nút Hủy duyệt.
- `.../form.blade.php` — khối STK (nguồn customer_accounts + 4 label gồm Tỉnh/TP).
- `.../formJs.blade.php` — setNewCustomer (map grant_date/location, contact cá nhân), save (validate size), onAccountChange (nguồn customer_accounts), field account_bank_province_name.
- `resources/views/layouts/topmenubar.blade.php:2148` — màu #2957A3→#212121.

**HRM (hrm-api):**
- `Modules/Assign/Routes/api.php` — POST /v1/assign/quotations/erp-contract/{id}/sync-customer.
- `Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` — erpSyncCustomer.

## 2. Chi tiết theo bug

### Nhóm A
- **10851/10852 — action + destroy:** cột action buildDataTable: người tạo thấy Sửa+Xóa khi status ∈ {DANG_TAO(1), KHONG_DUYET(4)}; nút Xóa `class="dropdown-item delete" data-text="Bạn chắc chắn muốn xóa phiếu {code}?"` (partials/confirm sẵn có → sweetalert → GET). Method `destroy($id)`: guard người tạo + status ∈ {1,4}, xóa histories()+files()+phiếu trong transaction, redirect back + toast "Xóa phiếu thành công". Route GET /{id}/delete. Nới guard edit()/update() cho KHONG_DUYET.
- **10867/10846/10853/10850 — panel bộ lọc:** index.blade: tắt search_by_time, đưa Từ/Đến ngày thành cột `search_type:'date'` (data-column created_from/created_to) đặt đúng vị trí; bỏ @if(!$isApprove) để Trạng thái luôn hiện; bật `search_by_parts` chỉ khi big_boss||boss (lib render Bộ phận cho manager sẵn → tránh trùng). Controller applyFilters đọc created_from/created_to parse d/m/Y (helper normalizeFilterDate); searchDataApprove default status=CHO_DUYET khi !request->status; buildDataTable format created_at/approved_at = d/m/Y H:i. Layout 12 trường/3 hàng: [Công ty·Phòng ban·Bộ phận·Số phiếu][Từ ngày·Đến ngày·Số HĐ·KH mới][KH cũ·Trạng thái·Người lập·Người duyệt].
- **10848/10849 — combobox Người lập/duyệt:** gốc = DB có nhân viên trùng tên + route dùng chung trả cả người chưa lập phiếu. Fix: endpoint riêng searchCreators/searchApprovers → buildPeopleFilterOptions(column): distinct created_by/approved_by từ chính bảng phiếu (áp applyPermissionScope) → Employee::with('info.department') → {id, text} lọc keyword. url combobox index.blade trỏ route mới. KHÔNG sửa employee.searchEmployeeByKeyword.
- **10869:** topmenubar.blade.php:2148 màu #2957A3→#212121.

### Nhóm B
- **10868:** show.blade bảng lịch sử: cột Tài khoản·Nội dung·Hành động·Thời gian (bỏ STT); Hành động viết hoa chữ đầu qua `mb_strtoupper(mb_substr(...,0,1)).mb_substr(...,1)` (hiển thị, không đổi data).
- **10854:** controller store()+update() logHistory('gửi duyệt', $handover->reason, ...) thay null.
- **10855:** show.blade comment nút Hủy duyệt (@if isDone) — giữ route cancelApprove + JS doCancelApprove.
- **10857:** approve() sau DB::commit(): NotificationHelper::sendNotify(created_by, route show, "{tên duyệt} đã duyệt phiếu YC chuyển giao khách hàng của bạn {code}") trong try/catch.
- **Bonus:** model cast approved_at=>datetime (fix crash format() màn Đã duyệt).

### Nhóm C
- **10831:** searchCustomer select thêm grant_date, grant_location; setNewCustomer map ncd.grant_date/grant_location = customer.*. (Hãng = select thủ công, customers không có cột hãng.)
- **10832:** save() thêm vòng lặp check file.size > 60*1024*1024 → errors['files.'+j] inline + toastr + return (không set loading → không loading vô tận).
- **10833/10834/10837:** đã OK sẵn bản B (KH trước hiển thị đủ; Ngày/Nơi cấp trong ng-if isIndividualNew ẩn khi chưa chọn KH; hint+validate 60MB).
- **10835:** nguồn STK = customer.customer_accounts (bảng customer_has_bank_accounts) thay contact; searchCustomer eager-load 'customer_accounts.bank_province'; form.blade option "STK - tại NH {bank} chi nhánh {branch} - {account_name}" (native type-to-search) + 4 label Tên TK/Ngân hàng/Tỉnh-TP/Chi nhánh; onAccountChange đọc newCustomer.customer_accounts + account_bank_province_name. (Không dùng select2 để tránh xung đột AngularJS.)
- **10836:** setNewCustomer nếu isIndividualNew → contact_name/address/phone = customer.fullname/address/mobile + selectedContact giả để hiện label.
- **10838:** searchContact = union (1) CustomerContact của KH (with customer_contact_accounts, keyword optional) + (2) firm_quotations của KH (customer_contact_name/phone) distinct, loại trùng theo customer_contact_id + SĐT; item báo giá gắn from_quotation=true, id=customer_contact_id (có thể null). [Diễn giải Claude chốt — chờ BA duyệt.]

### Nhóm D — #10871
- **HRM (hrm-api):** route POST /api/v1/assign/quotations/erp-contract/{id}/sync-customer (nhóm erp-contract public, TODO auth như erpMarkContract); QuotationController::erpSyncCustomer($request,$id): Quotation::find($id) (id = báo giá HRM = ERP firm_contract.hrm_quotation_id); ghi đè customer_id/code/name/tax_code/address/contact_name/contact_phone (cột snapshot quotations, FE tab Báo giá đọc trực tiếp).
- **ERP:** syncCustomerToHrm($handover, $customerData): nếu contractable.hrm_quotation_id null → bỏ qua; Guzzle POST (connect_timeout 3, timeout 8), try/catch chỉ log. Gọi trong approve() (new_customer_data, sau notify) + cancelApprove() (old_customer_data, sau commit). Map contact từ $customerData['contact']['name'/'phone'].
- Verify ERP non-breaking OK (approve thành công dù HRM unreachable). HRM end-to-end chờ dev-hrm (DB local thiếu bảng quotations; route:list hrm-api lỗi do module Decision — env sẵn có).

## 3. Hằng số / lưu ý
- Status: DANG_TAO=1, CHO_DUYET=2, DA_DUYET=3, KHONG_DUYET=4, HUY_DUYET=5.
- HRM quotation link: ERP firm_contract.hrm_quotation_id = HRM quotations.id; HRM quotations có erp_firm_contract_id/erp_firm_quotation_id (chiều ngược).
- quotations HRM lưu KH snapshot phẳng (customer_id/code/name/tax_code/address/contact_name/contact_phone), không relation.
- config('app.hrm_url_BE') = URL hrm-api (mặc định 127.0.0.1:8000); ERP gọi HRM qua HTTP (mẫu Customer::syncSimpleData).

## 4. Còn mở
- #10871 verify end-to-end trên dev-hrm.
- 10838 diễn giải chờ BA duyệt.
- 10835 "searchbox" hiện là native type-to-search (nếu QA cần select2 → follow-up).
