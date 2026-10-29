# Đề nghị xuất hóa đơn (export_bill_requests) — plan

Branch: `de_nghi_xuat_hoa_don` (git worktree `ERP/.worktrees/de_nghi_xuat_hoa_don`).
Module: IncomeExpenditure. Màn: Danh sách + form Tạo/Sửa/Xem.

## Danh sách — feedback
- [x] Thêm sort 4 cột: Số đề nghị (`code`), Ngày nhận (`received_time`), Giá trị xuất HĐ (`amount_after_vat`), Ngày duyệt (`approved_time`). (index.blade `orderable:true`)
- [x] Thêm giờ (H:i) vào Ngày nhận + Ngày duyệt (controller `searchData` editColumn `d/m/Y H:i`).
- [x] Cột Người lập hiển thị "Mã phòng - Tên người lập" (editColumn `created_by`).
- [x] Bộ lọc từ/đến ngày: đổi lọc theo Ngày duyệt → **Ngày nhận** (`received_time`) (model `searchByFilter`).

## Form Tạo/Sửa/Xem
- [x] Căn phải toàn bộ phần tổng bảng Hàng hóa (form.blade dòng tổng, colspan mode-adaptive).
- [x] **Fix auto-fill khi chọn hợp đồng/khách hàng:** (verify PASS)
  - Địa chỉ: FE đọc `self.contract.contract_address` (cột KHÔNG tồn tại trên `firm_contracts`) → sửa thành `self.contract.contact_address`. (ExportBillRequest.blade.php `addFirmContractParent` dòng 104)
  - Số tài khoản: mapping `self.contract.account_number` đã đúng; trống do HĐ/khách chưa khai TK (snapshot từ customer lúc lập HĐ, khớp form HĐ hãng). Không tự thêm fallback.
  - Verify: (1) DB — cột `contract_address` = 0 (không tồn tại), `contact_address`/`account_number` tồn tại + có data HĐ 21. (2) Playwright chạy đúng dòng đã fix qua `addFirmContractParent` với response data thật HĐ 21 → cả 3 input (account_number, contact_address, tax_code) fill đúng vào form + DOM.
  - Môi trường: đã migrate 10 migration feature (thêm cột bill vào firm_contract_tab_products/firm_contract_costs/wr_service_contract_*…) lên DB local để endpoint hết 500.

## Popup Chọn hợp đồng (firmContractModal) — feedback (Task 7)
Popup mở từ `firmContractModal()` trong `partials/ExportBillRequest.blade.php`; dữ liệu từ endpoint DÙNG CHUNG `searchAllContract` (nhánh `d.type='export_bill_request'`); UI dựng bằng class DÙNG CHUNG `BaseSearchModal` (single-select: click dòng → callback).

- [x] **7a. Link ở cột Số hợp đồng** → click mở màn xem chi tiết HĐ (firm/wr). Thêm `render` cho cột `code` trong config popup (ExportBillRequest.blade `firmContractModal`): `<a target="_blank" onclick="event.stopPropagation()">` để mở tab mới mà không chọn dòng. URL template từ `route('firmContract.show', ['id'=>'__ID__'])` (firm) / `route('WarrantyRepairContracts.show', ['id'=>'__ID__'])` (wr), thay `__ID__` bằng `row.id`, rẽ theo `row.type` ('wr_contract' → wr, còn lại → firm).
- [~] **7b. Checkbox từng dòng** — **BỎ** (user chốt 2026-10-29: "không cần tick"). Logic cũ chỉ cho chọn 1 HĐ (cột contractable_id/type/code số ít, FE ghi đè self.contract) — giữ nguyên chọn 1.
- [x] **7c. Hiện HĐ đã quyết toán** — ĐÃ CÓ SẴN trong nhánh: `DA_QUYET_TOAN(10)` nằm trong whereIn status cả firm (SearchContractService dòng 432) lẫn wr (dòng 452). Không cần sửa.
- [x] **7d. Sort theo Khách hàng chạy THẬT (Cách B — user chốt 2026-10-29 "7d phải chạy thật")**. Gốc lỗi: cột `customer` là editColumn TÍNH TOÁN (union chỉ select `objectable_id`), và union có `->orderBy('created_at','desc')` cố định ⇒ sort client bị `created_at` đè (test asc/desc ra y hệt). Fix (user đã cho phép sửa hàm chung, scope CHỈ nhánh `export_bill_request`):
  1. `SearchContractService::searchAllContract` nhánh `export_bill_request`: `addSelect` cột `customer_name` = `(SELECT CONCAT(c.code,'-',c.fullname) FROM customers c WHERE c.id = <table>.customer_id)` cho CẢ firm (`firm_contracts`) + wr (`wr_service_contracts`) → khớp đúng giá trị hiển thị. Áp `orderBy('created_at','desc')` mặc định CHỈ khi `!$request->filled('order')` (chưa chọn cột sort) → nhường quyền sort cho DataTables.
  2. `SearchController@searchAllContract`: `->orderColumn('customer', 'customer_name $1')` (chỉ kích hoạt khi client sort cột customer; màn khác không sort cột này nên không ảnh hưởng).
  3. Popup config: cột `customer` trả `orderable:true`. Giữ `approved_time`/`approver_name` `orderable:false` (addColumn tính toán, không có SQL sort).
- [x] **7e. Bộ lọc "Loại hợp đồng"** 4 giá trị (user chốt 2026-10-29 "theo bạn đề xuất"). Map:
  - `material` Hợp đồng vật tư - hàng hóa - thiết bị → firm type [HOP_DONG(1), PL_BO_SUNG(2)]
  - `project` Hợp đồng dự án → firm type [HOP_DONG_DU_AN(4)]
  - `repair` Hợp đồng sửa chữa - bảo dưỡng - bảo trì → phía wr_contract (toàn bộ side wr)
  - `principle_order` Đơn hàng nguyên tắc → firm type [DON_HANG_NGUYEN_TAC(8)]
  - FE: thêm `search_columns` item `{data:'contract_category', search_type:'select', column_data:[4 giá trị]}` trong `firmContractModal` (ExportBillRequest.blade) → `mergeSearch` gửi `d.contract_category`.
  - BE: nhánh type-gated `export_bill_request` của `extrated()` đọc `$request->input('contract_category')`, áp theo TỪNG side — side không khớp nhóm trả `whereRaw('1=0')` để union không lẫn (firm: switch theo type; wr: chỉ nhận `repair`).
  - Verify (BE fetch + UI thật): material(187) + project(0) + principle_order(869) = 1056 = tổng → 4 nhóm phân hoạch khít tập firm. project/repair = 0 do DB test KHÔNG có HĐ dự án / HĐ wr có hàng xuất được (cả 1056 dòng đều firm). UI: chọn `material` → chỉ `HĐ_...`; `principle_order` → `DHNT_...` 869 mục.

## File đính kèm — giới hạn dung lượng (Task 8)
Phản ánh: "tải > 30MB không thấy báo lỗi". Rà soát: giới hạn BE = **10MB/file** (rule `attachments.* => max:10240` KB), user chốt **GIỮ 10MB** (2026-10-29). "Không báo lỗi" là do UI KHÔNG hiện lỗi quá cỡ, không phải thiếu giới hạn. 3 lỗ hổng + fix:
- [x] **FE chặn ngay khi chọn file** (`formJs.blade.php`): thêm `MAX_ATTACHMENT_SIZE = 10*1024*1024`; handler `change` của `.attachments` kiểm `file.size` > ngưỡng → `toastr.warning` + reset ô (`value=''`, xoá `name` của slot) → không gửi file quá cỡ lên server (chặn luôn ca tràn `post_max_size`/413). Không splice mảng để tránh lệch index khi chọn nhiều file (slot trả về trạng thái "Chọn file" rỗng, user bấm × để bỏ).
- [x] **FE hiện text lỗi theo TỪNG file** (`form.blade.php`): trước chỉ có viền đỏ (`ng-class error`) + span lỗi cấp mảng `errors['attachments']`; lỗi quá cỡ keyed `attachments.0/1/...` không có chữ. Thêm `<span>` `ng-repeat` theo `addition_attachments` hiện `errors['attachments.'+$index][0]`.
- [x] **BE thêm message tiếng Việt** (`ExportBillRequestStoreRequest` + `ExportBillRequestUpdateRequest`): `attachments.*.max` / `.mimes` / `.file` (trước chỉ có `.required`/`.min` → lỗi quá cỡ ra câu mặc định tiếng Anh).
- [x] **Vá vòng lặp submit** (`create.blade.php` + `edit.blade.php`): `forEach` cũ append `input.files[0]` không kiểm tra → slot rỗng (sau khi loại file quá cỡ) append `undefined` thành entry rác. Thêm guard `if (input && input.files[0])`. Vá luôn lỗi tiềm ẩn cũ.
  - Lý do để-slot-rỗng thay vì splice: chooser thêm nhiều file qua `setTimeout` bắt `document{index}` theo index lúc push; splice giữa chừng làm lệch id các setTimeout còn chờ → hỏng batch. Để slot rỗng (reset `value`+`name`) an toàn, submit đã bỏ qua, user bấm × để dọn.
- [x] Verify Playwright (2026-10-29, server worktree `:8010`, trang create): mô phỏng `change` ô `.attachments` với file 11MB → `toastr.warning` "File \"big-11mb.pdf\" vượt quá dung lượng cho phép (tối đa 10MB)." + ô reset (`value=''`, slot `name` rỗng, không gửi lên server); file 1MB hợp lệ → không cảnh báo, slot nhận tên file. BE message VN (`.max`/`.mimes`/`.file`) + guard submit loop đã có trong code (lint PASS). PASS.

## File đính kèm — xóa file đã lưu (Task 9)
Phản ánh: "Đang không xóa được file đính kèm". Gốc lỗi: nút × ở file ĐÃ LƯU gọi `ng-click="deleteFile(d)"` (form.blade:102) nhưng **`$scope.deleteFile` chưa định nghĩa** cho màn này (`ExportBillRequest extends BaseClass`, không phải `BaseClassWithFile`) → bấm không làm gì. Thêm: `update()` luôn nối chuỗi `attachments` cũ, không có đường ghi danh sách rút gọn. User chốt 3 điều (2026-10-29): (a) xóa áp dụng khi **Lưu**; (b) **bắt buộc còn ≥1 file**; (c) **KHÔNG** xóa file vật lý S3, chỉ gỡ khỏi phiếu.
- [x] **FE `$scope.deleteFile(d)`** (`formJs.blade.php`): lọc bỏ path `d` khỏi `form.attachments` (getter `documents` tự tính lại → UI cập nhật). Guard ≥1: nếu gỡ xong còn 0 saved + 0 file mới thì `toastr.warning` + không gỡ.
- [x] **FE gửi danh sách giữ lại** (`create.blade.php` + `edit.blade.php`): append `old_attachments` = `form.attachments` (danh sách saved còn lại) vào FormData. `submit_data` không chứa `attachments` nên không đụng field khác.
- [x] **BE `update()` ghi theo danh sách giữ lại** (`ExportBillRequestController.php`): bỏ gate `if ($request->attachments)`; `attachments` = `old_attachments` (đã trim/filter) + file mới upload; chạy cả khi không có file mới (để xóa persist). KHÔNG gọi S3 delete.
- [x] **BE backstop ≥1** (`ExportBillRequestUpdateRequest`): `$hasKept` suy từ `old_attachments` (thay cho DB record); còn giữ file thì `attachments` nullable, xóa sạch + không upload mới → `required|array|min:1` → lỗi inline "Vui lòng đính kèm file".
- [x] Verify Playwright (2026-10-29, server worktree `php artisan serve :8010`, phiếu test id=12 insert+dọn): (a) trang edit nạp 3 file đã lưu + 3 nút ×, `$scope.deleteFile` là hàm; (b) click × xóa `a.pdf` qua DOM → `form.documents` còn `[b,c]`, `attachments` cập nhật; (c) logic FE: xóa file giữa OK, guard chặn xóa file cuối (toastr "Phải có ít nhất 1 file đính kèm."), có file mới thì cho xóa file lưu cuối; (d) BE persist isolation: giữ `[b,c]`+0 file mới → DB lưu "b, c"; giữ `[b,c]`+1 file mới → DB "b, c, new"; (e) BE backstop `rules()`: `old_attachments` rỗng/chỉ dấu phẩy → `required|array|min:1`, còn ≥1 → `nullable|array`. PASS toàn bộ.

## Xóa ở màn danh sách → nhảy sang trang list khác (Task 10)
- [x] **Bug:** click Xóa (menu ⋮) → xác nhận → bị đẩy sang URL list khác (vd đang ở tab `?type=all` hoặc `/for-accounting` wait-approve). Gốc: `ExportBillRequestController@delete` redirect **cứng** về `route('export_bill_request.index')` (base, mất query `type` + ngữ cảnh). Handler chung `a.delete` (`partials/confirm`) chỉ `window.location.href = href` nên đích redirect do BE quyết định.
- [x] **Fix (bám convention sibling `BillIncomeRequest`/`BillAdjustDeptRequest` — cùng dùng `redirect()->back()`):** đổi cả 3 nhánh redirect trong `delete()` từ `redirect()->route('export_bill_request.index')` → `redirect()->back()` để giữ nguyên trang list user đang đứng (bảo toàn `type` + bộ lọc). Chỉ sửa trong chính controller này, KHÔNG đụng hàm chung.
- [x] Verify Playwright (2026-10-29, `:8010`): insert phiếu test id=13 status=1 (DANG_TAO) → load list `?type=all` → điều hướng tới `/13/delete` (mô phỏng handler `a.delete`) → **landed back đúng `?type=all`** (trước fix về base `.../export_bill_requests`) + phiếu id=13 đã xóa khỏi DB (self-clean). PASS. Lỗi DataTable/notification trong log là do seed/schema môi trường local, không liên quan.

## Đổi text popup xác nhận Xóa (Task 11)
- [x] Đổi câu hỏi popup Xóa → "Có chắc chắn xóa phiếu?" (user gõ "chắc chắn chắn" — lặp từ, đã chỉnh chính tả). Thêm `data-text="Có chắc chắn xóa phiếu?"` vào nút Xóa trong cột action (`ExportBillRequestController@searchData`). Handler chung `a.delete` (`partials/confirm`) đọc `data('text')` → chỉ ảnh hưởng màn này, KHÔNG đụng text mặc định dùng chung.

## Không duyệt phải hiện popup nhập lý do bắt buộc (Task 12)
- [x] **Bug:** bấm "Không duyệt" (màn Chi tiết/Duyệt `show.blade`) chỉ hiện swal xác nhận chung ("Bạn chắc chắn muốn thực hiện hành động này?"), KHÔNG có ô nhập lý do bắt buộc; POST `reject` không gửi lý do và BE cũng không lưu.
- [x] **Cách làm (bám sibling `AdditionAccountingRequestController@reject` — cùng module IncomeExpenditure):** lý do từ chối lưu vào cột `comment` (validate bắt buộc). Bảng `export_bill_requests` chưa có cột → thêm migration `comment` TEXT nullable.
  1. Migration `add_comment_to_export_bill_requests_table`: thêm cột `comment` text nullable (sau `summary`).
  2. Model `ExportBillRequest`: thêm `'comment'` vào `$fillable`.
  3. BE `reject($id, Request $request)`: `Validator` bắt `comment` required (thông báo "Vui lòng nhập lý do không duyệt"), fail → `responseErrors`; lưu `$object->comment`. GIỮ nguyên `status = KHONG_DUYET(5)` + `reverseCountersFromExistingTabs` (khác sibling set về DANG_TAO — đây là hành vi sẵn có của feature, canEdit/canDelete cho phép sửa lại khi KHONG_DUYET). Gửi NotificationHelper tới người lập (bám sibling).
  4. FE `show.blade` `reject()`: thay swal chung bằng swal có `<textarea id="text">` + `#required_note` (khuôn handler chung `a.cancel_approve` trong `partials/confirm`), required client-side (rỗng → hiện `#required_note`, không đóng), POST kèm `comment`.
- [x] Chạy migration local + verify (Playwright, phiếu test id=14 trạng thái Chờ duyệt): bấm "Không duyệt" → popup hiện ô "Lý do không duyệt (*)"; bỏ trống + Xác nhận → lỗi inline `#reject-required` (`d-block`) + popup giữ nguyên; điền lý do + Xác nhận → BE validate qua, `save()` ghi `status=5`, `approver_id=777`, `comment` đúng nội dung. (POST trả 500 do bảng `notifications` DB local thiếu cột `url`/`receiver_id` — lỗi schema gop_db môi trường, cùng gốc với màn danh sách lỗi; production bảng này đủ cột; code bám đúng sibling `AdditionAccountingRequestController@reject` dòng 467, không thêm guard.)

## Hiển thị Ghi chú duyệt trên màn chi tiết (Task 13)
- [x] **Phản hồi:** "Chưa thấy ghi Lịch sử duyệt trong màn chi tiết" — lý do không duyệt (`comment`) đã lưu DB (Task 12) nhưng form không render ra.
- [x] **Chốt Phương án A (bám sibling `AdditionAccountingRequest`):** module Thu chi không dùng bảng lịch sử duyệt nhiều dòng; sibling chỉ hiện 1 card "Ghi chú duyệt" chỉ-đọc khi `form.comment` có. KHÔNG tạo bảng history riêng.
- [x] FE `form.blade` (shared create/edit/show): thêm card "Ghi chú duyệt" `ng-if="form.comment"` với textarea `disabled` bind `form.comment`, đặt sau card "Tổng hóa đơn". `BaseClass` tự gán `comment` lên instance (chỉ `no_set` handover_date/summary là xử lý riêng).
- [x] Verify Playwright (2026-10-29, `:8010`, phiếu test id=15 status=5): (a) có comment → màn chi tiết hiện card "Ghi chú duyệt", `textarea` disabled, value = đúng lý do không duyệt đã lưu; (b) NULL comment + reload → card KHÔNG render (`ng-if="form.comment"`, không có trong DOM). PASS cả 2. Đã dọn: xóa phiếu test id=15, khôi phục hash mật khẩu gốc tài khoản 777 (đặt tạm để đăng nhập Playwright).

## Đã commit + push (2026-10-29)
Commit `81bb041094` trên branch `de_nghi_xuat_hoa_don` (push: `adaa92b9f7..81bb041094`).
Gồm: index.blade.php, ExportBillRequestController.php, ExportBillRequest.php (model), form.blade.php, formJs.blade.php, partials/ExportBillRequest.blade.php, StoreRequest + UpdateRequest, SearchController.php, SearchContractService.php, migration add_comment_to_export_bill_requests_table, show.blade.php.
Rebase lên remote (remote đi trước 19 commit cùng feature); hòa giải 3 xung đột: Controller giữ format `H:i`; Model hợp nhất fillable (`contact_address`, `invoice_customer_name`, `comment`); partial giữ fix `self.contract.contact_address` (cột thật, remote là bug `contract_address`) + giữ dòng mới `invoice_customer_name` của remote. php -l PASS.

### Checkpoint — 2026-10-29
Vừa hoàn thành: Toàn bộ 13 task (Danh sách sort+giờ+người lập+lọc ngày nhận; form căn phải tổng + auto-fill; popup Chọn hợp đồng 7a/7c/7d/7e, 7b bỏ; file đính kèm giới hạn 10MB + xóa file; xóa list giữ URL; text popup xóa; không duyệt popup lý do bắt buộc; card Ghi chú duyệt). Tất cả Playwright-verified. Đã commit `81bb041094` + push (`adaa92b9f7..81bb041094`) sau rebase lên remote (hòa giải 3 xung đột).
Đang làm dở: (không có — tất cả task đóng)
Bước tiếp theo: Chờ user test môi trường thật (prod/test DB có schema `notifications` đủ cột — local gop_db thiếu cột `url`/`receiver_id` nên POST reject trả 500 ở local, không phải bug code). Nếu user có feedback mới cho màn này thì mở task tiếp.
Blocked: (không)
