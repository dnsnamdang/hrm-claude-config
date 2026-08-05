# SDD ledger — plan: .plans/gop-db/customer-care-services-catalog/plan.md

BASE hrm-api: c40d72555 · BASE hrm-client: 5d7fb71b9 · Nhánh: gop_db (cả 2 repo)
Chế độ: KHÔNG commit (quy tắc dự án) — review theo working-tree diff + file mới.
Workspace briefs/reports: C:\Users\Admin\AppData\Local\Temp\claude\D--laragon-www-hrm\9ea64a9a-e77b-41e3-b93a-b536c804758b\scratchpad\sdd\

Task 1.1: complete (5 entity Entities/Service/, review clean — Approved)
Task 1.1: minor (deferred): bảng `products` có deleted_at nhưng ErpProduct không SoftDeletes → Task 1.3 searchProducts phải lọc whereNull('deleted_at'); Service::products() có thể trả hàng đã xóa mềm (giống TpProduct sẵn có).
Task 1.1: ghi chú cho 1.3: BaseModel tự set created_by/updated_by (creating) + updated_by (saving) + company_id CHỈ KHI RỖNG → luôn truyền company_id tường minh (form required nên an toàn); LogsActivity ghi activity_log.

Task 1.2: complete (ServiceRequest.php, review clean — Approved)
Task 1.2: minor (deferred): json_decode malformed → [] âm thầm (rule nullable) — FE phải gửi JSON.stringify chuẩn; attributes() hiện chưa message nào dùng :attribute.
Task 1.2: ràng buộc cho 1.5: route param BẮT BUỘC đặt tên {service} (Request đọc $this->route('service')).

Task 1.3: complete (ServiceService.php, review clean — Approved)
Task 1.3: minor (deferred): thứ tự chuỗi attachments khi update = cũ trước mới sau (ERP ngược lại) — không mất data, chỉ đổi thứ tự hiển thị.
Task 1.3: lệch có chủ đích ĐÃ verify: searchProducts lọc status != 0 (ERP thật, products.status ∈ {0,1,2,5}); groups không có deleted_at; dataForEdit dùng attributesToArray.
Task 1.3: ràng buộc cho 1.5: store/update PHẢI bọc DB::transaction (saveServiceMaintain ghi trước throw sau); destroy cũng nên bọc.

Task 1.4: fix round 1/5 (1 addressed, 0 open — format giá export đổi sang khớp ERP formatCurrency 1,400,000)
Task 1.4: complete (ServiceListResource + ServiceExport + exports/services.blade.php, review clean sau fix)
Task 1.4: quyết định: BỎ ServiceDetailResource — controller trả thẳng array dataForEdit; created_by_name tự build từ quan hệ camelCase đã eager-load (tránh N+1 do accessor BaseModel dùng quan hệ snake_case).
Task 1.4: minor (deferred): employeeDisplayName trùng logic Cost::employeeDisplayName — nếu xuất hiện bản sao thứ 3 thì rút helper chung.

Task 1.5: complete (ServiceController + 10 routes + buildPrintData/buildPrintNote + clearNull sẵn có, review Approved; smoke round 2 sau fix quyền: case 5/7/11 PASS qua HTTP thật)
Task 1.5: minor (deferred): ServiceController::printData gọi clearNull($html) thừa (fillReport đã tự gọi) — dead code, dọn ở final review.
Task 1.5: DATA FIX quan trọng (đã chạy local, PHẢI chạy lại khi deploy): (1) UPDATE permissions SET type=24 WHERE id IN (101023,101024,101025); (2) mirror employee_has_roles role 100062/100097 từ model_type App\Employee sang Modules\Timesheet\Entities\Employee (15 dòng, giữ employee_id/position/company_id) — vì CheckPermission HRM resolve theo model_type HRM; (3) INSERT IGNORE role_has_permissions (101023,18),(101024,18),(101025,18) — Super admin HRM cần gán tường minh (ERP Super Admin đi qua bypass riêng nên bảng quyền không có; user báo mất nút Thêm mới 2026-08-04). Phát hiện thêm: DB local KHÔNG có quyền CSKH 1115-1120 của 2 feature trước (chỉ insert trên máy @junfoke).

Task 2.1: complete (pages/customer-care/services/index.vue + menu customer-care.js, review Approved; browser verify thật 207 bản ghi/lọc/sort/popover/export/gate quyền)
Task 2.1: minor (deferred): message confirm xóa thêm tên gói so với câu chữ brief (khớp style costs) — chấp nhận.
Task 2.1: BUG HỆ THỐNG phát hiện (KHÔNG sửa — file dùng chung): V2BaseSelect.vue:59 `opt.id || opt.value || opt.code` làm rớt option id=0 → workaround cục bộ id '0' chuỗi; cần báo team sửa gốc (costs/index.vue khả năng dính tương tự).
Task 2.1: ghi chú cho 3.1/4.1: tài khoản dev trên browser KHÔNG có 3 quyền gói bảo dưỡng → verify form phải sinh JWT employee 461 (role 100062) qua tinker rồi inject vào browser storage.

Task 3.1: review round 1 = Needs fixes: F1+F2 CRITICAL key_word shape {text} (đọc → [object Object], ghi sai shape hỏng màn báo giá DV ERP; 88/207 gói dính); F3 Important (xóa hết dòng khi sửa = no-op im lặng — hành vi ERP nguyên trạng); F4/F5 Important (thiếu evidence đính kèm + chưa test trên gói gốc ERP → dồn sang Task 4.1); M1-M5 minor.
Task 3.1: parked — F3 xóa hết dòng khi sửa là no-op — ruling: GIỮ NGUYÊN, ERP hành xử y hệt (BE `if empty return` là port nguyên trạng đã ghi spec); sẽ nêu cho user trong tổng kết, nếu muốn chặn/cảnh báo thì làm sau.
Task 3.1: minor (deferred): M3 hydrate ghi chú theo vị trí cột (0 gói lệch hiện tại — nên match level_id về sau); M4 lỗi BE maintains.{i>0}/companies.* không có ô hiển thị (toast chung); M5 quantity=0 được chấp nhận (BE cũng chỉ numeric).
Task 3.1: fix round 1/5 (5 addressed, 0 open — F1/F2 key_word shape {text} 2 chiều + M1a sanitize @input.native + M1b guard keystroke + M2 Math.round; verify gói ERP id=2 chip 'Dao tiện', DB 0 dòng hỏng)
Task 3.1: complete (5 file pages/customer-care/services/**, review clean sau fix round 1; F3 parked với ruling giữ nguyên hành vi ERP)
Task 3.1: ghi chú: FE ghi key_word LUÔN xuất shape {text} — gói nào từng lưu mảng chuỗi thuần sẽ tự chuẩn hoá sau lần lưu đầu qua HRM (hướng đúng, ERP đọc .text).
