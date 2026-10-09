# Plan — Công nợ đầu kỳ: lọc Quá hạn + Ngày BGNT

## Phase 1 — BE (model DeclareDebtBeginning)
- [x] 1.1 `searchByFilter()`: thêm lọc `is_overdue` (phân biệt 0 với rỗng) + khoảng `acceptance_handover_from`/`acceptance_handover_to` (whereDate, parse d/m/Y).
- [x] 1.2 `searchByFilterExport()`: thêm 3 điều kiện tương ứng (đồng bộ in/xuất Excel).
- [x] 1.3 Thêm `use Carbon\Carbon;` (chưa import) + `php -l` sạch.

## Phase 2 — FE (index.blade.php)
- [x] 2.1 Thêm 3 ô vào `search_columns`: `is_overdue` (select Có/Không) + `acceptance_handover_from` (date) + `acceptance_handover_to` (date). Xác nhận picker `.date` output `d/m/Y` (app.js:29) khớp BE parse.

## Phase 3 — FE (popup chọn hợp đồng)
- [x] 3.1 Popup "Thêm mới công nợ đầu kỳ" đang dùng `route('searchContract')` + `d.type='declare-debt-beginning'` + ô lọc "Loại hợp đồng" → trả "Không có dữ liệu". Đổi sang `route('searchAllContract')` (mirror pattern các màn khác, vd `BillIncomeReportDetail`): bỏ `d.type`, giữ `d.customer`, bỏ ô select `contract_type`, chỉ giữ ô text `code`.
- [x] 3.2 Đổi field object trả về cho khớp `searchAllContract`: `contract_costable_type` → `contractable_type` (dedup `selectContract` + map submit `$('#form').submit`). `contract_id` vẫn = `obj.id`.
- [x] 3.3 Cột hiển thị popup: STT, `code`, `customer_id`, `payed_cost`, `created_by`, `created_at`.
- [x] Không sửa hàm dùng chung (`searchAllContract`/`SearchContractService`); store BE đã lưu `deptable_type` đa hình (line 118) + `getDeptAbleType` resolve link → FE-only an toàn. Đã xác nhận `update()` không dùng `contract_type` (tìm record theo id) → đổi tên field chỉ ảnh hưởng luồng store item mới.

## Phase 4 — Bugfix In/Xuất Excel không hiển thị dữ liệu (regression do Phase 3)
- [x] 4.1 Root cause: nút In/Xuất Excel dùng `mergeSearchV2` (selector **global** `.search-column [data-column]`). Popup chọn hợp đồng (BaseSearchModal thêm ở Phase 3) render `DatatableSearchModal` cũng có `.search-column [data-column="code"]` → mergeSearchV2 gom nhầm ô `code` (số hợp đồng) của popup, ghi đè `code` (Mã phiếu) của list → `where('code', ...)` khớp chính xác → 0 dòng. List không bị vì `DATATABLE.mergeSearch` **scoped** theo `#table-list_wrapper`.
- [x] 4.2 Fix: 2 handler `.print-button`/`.export-button` thôi dùng `mergeSearchV2`, thay bằng `collectListSearch()` gọi `DATATABLE.mergeSearch(data, {nTable:{id:'table-list'}})` → lấy filter đúng scope bảng chính, In/Xuất === List.
- [x] 4.3 Verify tinker: `searchByFilter` + `printList` controller render đủ dòng (customer=356 → 5 dòng; không lọc → 2190 dòng). Code path đúng; lỗi cũ do param nhiễm từ popup.

## Phase 5 — Điều tra QA #5: "không thấy ghi nhận công nợ đầu kỳ quá hạn vào sổ chi tiết tài khoản"
- [x] 5.1 Trace luồng hạch toán: `DeclareDebtBeginningController::store()` tạo 1 `AccountDetail` (account_id/type_dept/dept_value/customer/contractable). `is_overdue` KHÔNG ảnh hưởng bút toán (chỉ là thuộc tính aging).
- [x] 5.2 Xác định field ngày quyết định hiển thị: `AccountDetail::boot()` (dòng 185-186) set `invoiceable_date_accounting = $invoiceable->debt_calculation_date` cho DeclareDebtBeginning. `debt_calculation_date` lấy từ `Config::getConfig()->debt_calculation_date` (mốc chung toàn hệ thống, local = 2025-08-01), set trong `DeclareDebtBeginning::boot()` dòng 60.
- [x] 5.3 Verify tinker (local dev_erp_2): declare quá hạn id=3312 → AccountDetail id=26021 (acct=2, type=1, money=20000, inv_date_acct=2025-08-01). Bút toán ĐƯỢC ghi. Với kỳ báo cáo sau 2025-08-01 → rơi vào "Số dư đầu kỳ", KHÔNG xuất hiện thành dòng phát sinh trong thân sổ. BGNT (acceptance_handover_date=2026-08-26) KHÔNG được dùng làm ngày hạch toán.
- [x] 5.4 Kết luận: hạch toán đúng (1 bút toán số dư đầu kỳ). "Không thấy" = công nợ đầu kỳ luôn gộp vào Số dư đầu kỳ, không phải dòng phát sinh. Chờ user chốt: (A) chỉ cần nằm trong số dư đầu kỳ là đủ? hay (B) bút toán quá hạn phải lấy ngày BGNT làm ngày hạch toán? → nếu (B) phải sửa hàm dùng chung `AccountDetail::boot()` (hỏi trước khi sửa).
- [ ] 5.5 (chờ quyết định user) Áp fix nếu chọn (B).

## Phase 6 — Báo cáo công nợ theo NV: hiện Ngày nghiệm thu (BGNT) từ công nợ đầu kỳ + số ngày quá hạn
File: `app/Services/SaleReport/CustomerDebtDetailByEmployeeService.php` (báo cáo `admin/sale/reports/customer-debt-detail-by-employee`).
- [x] 6.1 Hiện trạng: view đã có sẵn cột "Ngày nghiệm thu" (`handover_date`) + "Số ngày nợ" (`number_day_of_debt`) + filter. `handover_date` tính bằng CASE (dòng 83+) CHỈ cho FirmContract/WrServiceContract, còn lại NULL → HĐ công nợ đầu kỳ (thường không có phiếu xuất/biên bản) ra trống.
- [x] 6.2 Quyết định (tự chốt): (b) BGNT chỉ dùng khi CASE hệ thống NULL (fallback, không đụng Firm/WrService); dùng chung công thức +6 ngày ân hạn cho "Số ngày nợ"; chỉ lấy declare `is_overdue=1` có `acceptance_handover_date`.
- [x] 6.3 Fix: bọc `COALESCE(<CASE cũ>, <subquery BGNT>)`. Subquery: `SELECT acceptance_handover_date FROM declare_debt_beginning WHERE deptable_id=contractable_id AND deptable_type=contractable_type AND is_overdue=1 AND acceptance_handover_date IS NOT NULL ORDER BY acceptance_handover_date DESC LIMIT 1`. Giữ nguyên `render()` (+6 ngày) và filter `havingRaw` handover_date.
- [x] 6.4 Verify: `php -l` sạch; chạy DB::select SQL ghép (CASE thật + COALESCE) OK; fallback trả đúng BGNT 2026-08-26 cho FirmContract#1128 (declare id=3312). Cột "Ngày nghiệm thu" + "Số ngày nợ" sẽ có giá trị cho dòng công nợ đầu kỳ quá hạn.

## Checkpoint
### Checkpoint — 2026-09-03 (Phase 6 — BGNT vào báo cáo công nợ theo NV)
Vừa hoàn thành: `CustomerDebtDetailByEmployeeService::getData()` — cột `handover_date` bọc `COALESCE(CASE cũ, subquery acceptance_handover_date của declare_debt_beginning is_overdue=1 khớp contractable)`. HĐ công nợ đầu kỳ quá hạn giờ hiện được Ngày nghiệm thu (BGNT) + Số ngày nợ (+6 ngày ân hạn như cũ). Chỉ fallback khi ngày giao nhận trong hệ thống NULL → không ảnh hưởng Firm/WrService.
Đang làm dở: (trống)
Bước tiếp theo: user QA trên trình duyệt (dev-erp) — mở báo cáo, lọc tới HĐ có khai công nợ đầu kỳ quá hạn, xác nhận cột "Ngày nghiệm thu" = ngày BGNT đã khai, "Số ngày nợ" tính đúng; kiểm tra in + xuất Excel cùng dữ liệu.
Blocked: (trống)

### Checkpoint — 2026-09-03
Vừa hoàn thành: toàn bộ Phase 1-2. BE `DeclareDebtBeginning::searchByFilter` + `searchByFilterExport` thêm lọc Quá hạn (is_overdue, phân biệt 0/rỗng) + khoảng Ngày BGNT (acceptance_handover_date), import Carbon, php -l sạch. FE thêm 3 ô lọc.
Đang làm dở: (trống)
Bước tiếp theo: user QA trên trình duyệt — lọc Quá hạn Có/Không, khoảng Ngày BGNT; kiểm tra in + xuất Excel áp cùng bộ lọc.
Blocked: (trống)

### Checkpoint — 2026-09-03 (Phase 3)
Vừa hoàn thành: Phase 3 — popup chọn hợp đồng (Thêm mới công nợ đầu kỳ) chuyển từ `searchContract` (cần chọn Loại hợp đồng → "Không có dữ liệu") sang `searchAllContract` (mirror pattern `BillIncomeReportDetail`). Bỏ ô lọc "Loại hợp đồng", chỉ lọc theo `d.customer` + ô text `code`. Đổi field `contract_costable_type` → `contractable_type` ở dedup `selectContract` + map submit. Cột popup: STT/code/customer_id/payed_cost/created_by/created_at. FE-only, không đụng hàm dùng chung; store BE lưu deptable_type đa hình, `getDeptAbleType` resolve link; `update()` không dùng contract_type nên an toàn.
Đang làm dở: (trống)
Bước tiếp theo: user QA — chọn KH, mở popup "Chọn hợp đồng", xác nhận ra danh sách HĐ của KH (HĐ hãng/đầu kỳ...), chọn → lưu công nợ đầu kỳ thành công; sửa (edit) 1 dòng vẫn lưu được.
Blocked: (trống)

### Checkpoint — 2026-09-03 (Phase 4 — bugfix In/Xuất Excel)
Vừa hoàn thành: Fix In/Xuất Excel không hiển thị dữ liệu. Root cause là regression từ Phase 3: nút In/Xuất dùng `mergeSearchV2` (global `.search-column`), bị popup chọn hợp đồng (mới thêm) làm nhiễm ô `code` → `where('code',...)` khớp chính xác → 0 dòng. Đã đổi 2 handler sang `collectListSearch()` = `DATATABLE.mergeSearch(data,{nTable:{id:'table-list'}})` (scoped bảng chính, In/Xuất === List). Verify tinker: printList render đủ dòng (customer lọc → có; full → 2190).
Đang làm dở: (trống)
Bước tiếp theo: user QA lại trên trình duyệt — mở popup chọn hợp đồng, gõ search trong popup, đóng lại rồi bấm In / Xuất Excel → phải ra đúng dữ liệu như list (không bị rỗng). Kiểm tra cả lọc theo khách hàng.
Blocked: (trống)
