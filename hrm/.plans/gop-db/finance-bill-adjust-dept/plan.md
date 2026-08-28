# Plan — Phiếu kế toán (ERP `bill_adjust_dept` → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Bắt đầu: 2026-08-28
> Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-08-28-finance-bill-adjust-dept-design.md`

---

## Phase 1 — Nền BE (entity, morphMap, quyền, route)

- [x] 1.1 Entity `BillAdjustDept` — bảng `bill_adjust_depts`, hằng trạng thái (Đang tạo = **xám**), quan hệ, accessor `is_can_view/is_can_edit/is_can_delete/status_text/status_type`
- [x] 1.2 Entity `BillAdjustDeptDetail` — bảng `bill_adjust_dept_details`, morphTo `contractable` + `objectable`
- [x] 1.3 Sinh mã `<mã cty>.PKT<mm><yy>.<5 số>` bọc transaction + `lockForUpdate`
- [x] 1.4 Bổ sung **4 morphMap** `objectable`: Customer / Supplier / Employee / Department
- [x] 1.5 Thêm **2 quyền guard `api`** vào `PermissionsTableSeeder` (tổng công ty / công ty)
- [x] 1.6 Khai 15 route (route tĩnh đặt TRƯỚC `/{id}`), gắn `checkPermission:Kế toán thanh toán` cho route ghi

## Phase 2 — Đọc: danh sách + chi tiết

- [x] 2.1 `BillAdjustDeptService::search()` — 12 ô lọc + phạm vi quyền 2 cấp + ẩn phiếu *Đang tạo* của người khác
- [x] 2.2 `BillAdjustDeptResource` (danh sách) + `DetailBillAdjustDeptResource` (chi tiết)
- [x] 2.3 `show()` gate bằng `is_can_view`, không qua → 403
- [x] 2.4 Kiểm chứng phạm vi quyền bằng SQL đếm theo 3 nhánh, so với số dòng API trả

## Phase 3 — Ghi: tạo / sửa / xóa (chưa duyệt)

- [x] 3.1 `BillAdjustDeptStoreRequest` + `UpdateRequest`
- [x] 3.2 `BillAdjustDeptWriteService::validateDetails()` — 5 luật theo nhóm định khoản
- [x] 3.3 `syncDetails()` — ghi 38 cột chi tiết + tính `total_amount`
- [x] 3.4 `store()` / `update()` — validate **trước** khi tạo phiếu; chặn nhảy cóc trạng thái
- [x] 3.5 `destroy()` — gate `is_can_delete`, trả trạng thái phiếu nguồn về *Chờ duyệt*
- [x] 3.6 Đính kèm file S3 (nối attachment của đề nghị nguồn khi có)
- [x] 3.7 Test 5 luật validate × ca đúng/sai

## Phase 4 — Ghi sổ cái (phần rủi ro nhất)

- [x] 4.1 `BillAdjustDeptAccountingService::buildEntries()` — **hàm thuần**, không DB / không `auth()`
- [x] 4.2 `persist()` — chỉ insert `account_details` + `account_detail_refs`
- [x] 4.3 3 nhánh `billable_*` (đầu kỳ / ProductExport / BorrowSell) — kiểm null từng bước
- [x] 4.4 `syncAdjustedMoneyBillIncomeReport()` — cộng `money_adjusted` cho dòng Phiếu báo có
- [x] 4.5 `processApproved()` — 5 bước đúng thứ tự ERP, bọc 1 transaction
- [x] 4.6 `BillAdjustDeptNotifyService` — thông báo chuông theo template `[PREFIX] {Nhóm hành động}: {Tên}. {Ghi chú}`
- [x] 4.7 **Unit test `buildEntries()`** với nhóm định khoản lấy từ phiếu ERP thật, so từng dòng sổ cái
- [x] 4.8 Chạy thử vòng đời đầy đủ trên dữ liệu thật, **bọc transaction rồi rollback**

## Phase 5 — Số dư lẻ + 5 cửa vào

- [x] 5.1 `BillAdjustDeptOddBalanceService::check()` — gom nhóm, so `companies.adjust_odd_balance`
- [x] 5.2 Sinh cặp bút toán đề xuất (Nợ 811/Có 1311 · Nợ 1311/Có 711), gắn `cost_debt` `DCSDCNKH`
- [x] 5.3 Cửa vào 2 — nạp từ Phiếu YCĐC, mặc định TK 1311, ẩn cột nhóm định khoản
- [x] 5.4 Cửa vào 3 — nạp từ Hạch toán bổ sung, copy `type`, ẩn cột phiếu YCXH khi `type = 7`
- [x] 5.5 Cửa vào 4 — nạp từ Hạch toán hoa hồng tháng *(màn nguồn chưa port — chỉ deep-link)*
- [x] 5.6 Cửa vào 5 — nạp từ Chi phí giao nhanh + cập nhật cờ đã hạch toán *(màn nguồn chưa port)*
- [x] 5.7 3 endpoint popup: `search-objects` · `search-contracts` (gộp `hrm_contracts` + `firm_contracts` + 6 loại ERP) · `search-export-requests`

## Phase 6 — In & xuất Excel

- [x] 6.1 `BillAdjustDeptPrintService` — letterhead theo **`company_id` trên chứng từ** (khuôn `BillIncomePrintService::headerUrl()`)
- [x] 6.2 `BillAdjustDeptExport` — Excel chi tiết 1 phiếu, ô tiền dạng số + data-format
- [x] 6.3 `BillAdjustDeptListExport` — Excel danh sách, BE trả đủ trường của `ExportFieldsModal`

## Phase 7 — FE màn danh sách

- [x] 7.1 `pages/finance/bill-adjust-depts/index.vue` — 4 mixin, `localStorageKey` + `columnScreenKey` duy nhất
- [x] 7.2 12 ô lọc bằng `V2BaseSmartFilterPanel` + schema `filterFields`
- [x] 7.3 11 cột + căn lề SRS + `V2BaseBadge` qua `utils/statusBadgeVariant.js`
- [x] 7.4 `getRowActions()` — Sửa → Xóa → In → Xuất Excel, gate bằng cờ BE, handler `switch (action)`
- [x] 7.5 Toolbar: Tạo mới → Xuất Excel → Cấu hình cột (không có Import)
- [x] 7.6 Thêm mục menu vào `components/subsystem-menu/`

## Phase 8 — FE form + chi tiết + in

- [x] 8.1 `BillAdjustDeptForm.vue` — dùng chung cho tạo / sửa / chi tiết
- [x] 8.2 Khối thông tin chung + đổi loại tiền → tính lại toàn bộ cột quy đổi
- [x] 8.3 Bảng chi tiết 18 cột, header 2 tầng khi ngoại tệ, nhập Nợ tự xóa Có
- [x] 8.4 3 popup — select trong popup dùng `V2BaseSelectInModal`
- [x] 8.5 Khối tick "số dư lẻ"
- [x] 8.6 `create.vue` · `_id/index.vue` · `_id/edit.vue` (3 file mỏng) + `unsavedChangesMixin`
- [x] 8.7 `_id/print.vue` — khổ ngang, bố cục mẫu ERP id 208
- [x] 8.8 Cờ quyền **fail-closed** — mọi cờ khởi tạo `false`, chỉ set từ `$store.state.permissions` hoặc field BE

## Phase 9 — Kiểm chứng & dọn

- [x] 9.1 Seeder dữ liệu test (khuôn `TEST.DNDCCN.*`) — có phiếu *Đang tạo* để bấm thử sửa/xóa
- [x] 9.2 Chạy 6 lệnh grep tự kiểm của skill `erp-to-hrm-screen` trên cả thư mục feature
- [x] 9.3 Compile sạch toàn bộ file FE (`vue-template-compiler` + babel — repo **không có ESLint config**)
- [x] 9.4 Đối chiếu ngược với ERP: đủ cột / đủ ô lọc / đủ hành động **và điều kiện ẩn hiện**
- [x] 9.5 Bàn giao user mở trình duyệt bấm thật — báo rõ phần chưa kiểm chứng

---

## Checkpoint — 2026-08-28

Vừa hoàn thành: **toàn bộ BE + FE của màn Phiếu kế toán** (Phase 1-9, trừ 9.1 và 9.5).

**Đã kiểm chứng bằng dữ liệu thật:**
- **Ghi sổ cái**: `buildEntries()` chạy trên **150 phiếu ERP ngẫu nhiên / 403 dòng bút toán**,
  so **33 cột** + toàn bộ `account_detail_refs` → **khớp tuyệt đối 150/150**.
  (Vòng đối chiếu đầu bắt được 2 lỗi thật, đã sửa: `optional(null)` trả object nên nhánh dự phòng
  người lập không chạy — 58 dòng lệch `company_id`/`department_id`; và entity hợp đồng của HRM
  không có quan hệ `employee_create` như `App\BaseModel` của ERP nên `created_by` lấy nhầm người
  lập phiếu — 280 dòng lệch.)
- **Phạm vi quyền**: 3 nhánh (tổng công ty / công ty / chỉ phiếu mình lập) + Super admin đối chiếu
  SQL → khớp 6/6 nhân viên thật.
- **Vòng đời**: lưu nháp → sửa → duyệt (ghi 2 bút toán + 2 dòng đối ứng) → chặn sửa/xoá phiếu đã
  duyệt (403). Bọc transaction rồi rollback, 0 dòng sót lại.
- **4/5 luật validate** nhóm định khoản: chặn đúng, ca hợp lệ lưu được. Luật 2 (vượt tiền Phiếu
  báo có) chưa dựng được ca thật.
- **10 endpoint** smoke test qua HTTP kernel: 200 hết. Popup hợp đồng trả đúng 372 hợp đồng
  (368 HĐ bán + 4 nguồn khác) cho khách hàng có dữ liệu.
- **FE**: 9/9 file compile sạch (`vue-template-compiler` + babel); 5 lệnh grep tự kiểm của skill
  `erp-to-hrm-screen` sạch tuyệt đối.

Đang làm dở: không có.

Bước tiếp theo: **9.5** user mở trình duyệt bấm thật. Seeder đã chạy: 5 phiếu `TEST.PKT.0000x`
trạng thái *Đang tạo* gán cho NV #13 (tài khoản dev), mỗi phiếu 1 nhóm định khoản đã cân sẵn nên
mở ra bấm "Lưu và duyệt" được ngay. 0 bút toán nào được ghi vào sổ cái.

Blocked: [để trống]

### Phần CHƯA kiểm chứng được (ghi rõ để không nhầm là đã xong)
| Hạng mục | Lý do |
| --- | --- |
| Nhánh `exportable_*` (phiếu YC xuất hàng) | `exportable_type` NULL ở **33.409/33.409** dòng thật — code chết của ERP |
| Nhánh `is_begin` (số dư đầu kỳ) khi ghi sổ | `is_begin = 1` ở **0/33.409** dòng thật |
| Cửa vào 4 — Hạch toán hoa hồng tháng | bảng nguồn **0 dòng**, màn nguồn chưa port |
| Cửa vào 5 — Chi phí giao nhanh | màn nguồn chưa port; `fast_delivery_employee_id` do service báo cáo ERP tính, HRM chưa có nguồn nên để null |
| Nghiệp vụ số dư lẻ | chưa dựng được hợp đồng có dư lẻ trong ngưỡng để chạy thật |
| Toàn bộ thao tác FE | chưa mở trình duyệt — user tự bấm |


---

## Phase 10 — Kiểm thử Playwright + đối chiếu trực tiếp với ERP (2026-08-28)

Chạy thật trên trình duyệt: HRM `localhost:3000` ↔ ERP `127.0.0.1:8002`, cùng tài khoản, cùng DB.

- [x] 10.1 Đối chiếu **20 bộ lọc** giữa 2 API (không lọc · mã phiếu · mã YCĐC · 3 trạng thái ·
      tài khoản theo số và theo tên · mã hợp đồng · 2 khoảng tiền · ngân hàng · 2 người lập ·
      2 khoảng ngày · 2 NVKD · khách hàng · kết hợp 2 điều kiện) → **20/20 khớp tuyệt đối**
- [x] 10.2 Đối chiếu danh sách trang 1: 11 cột × 10 dòng, tổng số bản ghi
- [x] 10.3 Bấm thật: sort 2 chiều + hủy sort cột cũ · phân trang · ghi nhớ bộ lọc khi quay lại ·
      popup "Cài đặt bộ lọc" · Cấu hình cột
- [x] 10.4 Nút hành động theo trạng thái: phiếu *Đang tạo* có Sửa/Xóa, phiếu *Đã duyệt* ẩn hẳn
- [x] 10.5 Màn chi tiết + màn sửa: nạp đúng dữ liệu, badge đúng màu, cảnh báo "chưa lưu" khi thoát
- [x] 10.6 Bảng định khoản: nhập Nợ tự xóa Có · cột quy đổi tự tính · **Thêm dòng tự điền chênh
      lệch** để nhóm cân · cảnh báo nhóm lệch
- [x] 10.7 3 popup: chọn đối tượng (tìm theo mã/tên, 3 loại KH/NCC/NV, chọn xong **reset sạch 6
      trường hợp đồng**) · chọn hợp đồng (nhánh KH 372 HĐ, nhánh NCC 104 HĐ) · phiếu YC xuất hàng
- [x] 10.8 Cửa vào 2 (từ Phiếu YCĐC): so **từng dòng** với `getDataForBillAdjustDept` của ERP →
      khớp tuyệt đối 3/3 dòng (tài khoản, số tiền, nhóm, đối tượng, hợp đồng, ngày hạch toán)
- [x] 10.9 **Duyệt qua giao diện** trên phiếu TEST → ghi đúng 2 bút toán + 2 dòng đối ứng chéo
      nhau; **đã dọn sạch**, sổ cái về đúng 972.053 dòng / max id 1001536 như trước khi test
- [x] 10.10 Xóa phiếu qua giao diện → phiếu + dòng chi tiết sạch
- [x] 10.11 Bản in: so ảnh chụp với bản in ERP cùng phiếu
- [x] 10.12 Xuất Excel 1 phiếu (có letterhead, ô tiền kiểu SỐ + `#,##0`) và Excel danh sách

### 7 lỗi tìm được và đã sửa

| # | Lỗi | Bằng chứng | Đã sửa |
| --- | --- | --- | --- |
| 1 | Cột **Phòng ban** ở danh sách/Excel lấy phòng ban NGƯỜI LẬP. ERP lấy của **phiếu YCĐC nguồn** — người lập luôn là kế toán nên cột đó thành vô nghĩa | lệch 4/10 dòng trang đầu so ERP | `BillAdjustDeptService::attachRequestDepartment()` |
| 2 | Màn **chi tiết** vẫn render `<input>` ở cột Mã khách + Đơn hàng/Hợp đồng | 2 ô nhập còn sót khi `readonly` | `AccountingDetailTable.vue` tách nhánh `v-if/v-else` |
| 3 | **Popup chọn hợp đồng trả `created_by` = ID**, trong khi cột `contract_created_by` là `varchar` chứa **TÊN** (18.149/18.149 dòng ERP đều là chữ) → NVKD hiện ra con số | ERP `searchAllContract` trả `fullname` | `BillAdjustDeptPickerService::loadCreatorNames()` |
| 4 | **Ô lọc NVKD chết hoàn toàn** — lọc id trên cột chứa tên | ERP: 84 và 25 phiếu · HRM: 0 và 0 | `searchByFilter()` quay về `whereHasMorph` như ERP |
| 5 | **Excel danh sách chỉ ra 2 cột**, mất 9 cột — `buildQueryString()` (util dùng chung) serialize mảng thành `fields=a&fields=b`, PHP chỉ nhận giá trị cuối | file tải về chỉ có STT + Trạng thái | FE gửi chuỗi `a,b,c`; BE `forData()` nhận cả 2 dạng |
| 6 | **Bản in lệch ERP**: thiếu cột NVKD, thừa cột Nhóm, tách đôi cột Tài khoản, thiếu ô ký BAN GIÁM ĐỐC, ghi "Cộng" thay vì "Tổng", dòng ngày sai định dạng, số tiền xuống dòng giữa con số | so ảnh 2 bản in cùng phiếu | `print.vue` dựng lại theo đúng 9 cột + 3 ô ký của ERP |
| 7 | Popup "Chọn trường xuất" không tự đóng sau khi xuất xong | quan sát trực tiếp | `index.vue` gọi `$bvModal.hide()` sau khi tải xong |

### Lỗi của ERP mà HRM sửa (đã chứng minh trên giao diện ERP thật)

| Lỗi ERP | Bằng chứng | HRM |
| --- | --- | --- |
| Ô lọc **"STK ngân hàng"** lọc cột `account_number` — cột KHÔNG TỒN TẠI trên `bill_adjust_dept_details` | ERP trả **HTTP 500** `Unknown column 'account_number'` | lọc đúng cột `bank_account_number` → ra 15 phiếu |
| Xoá phiếu kế toán không trả trạng thái cho Yêu cầu hạch toán bổ sung | đọc code `delete()` :344-366 | trả về *Chờ duyệt* |

### Vẫn CHƯA kiểm chứng được (không đổi so với trước)

Nhánh `exportable_*` và `is_begin` khi ghi sổ (0 dòng dữ liệu thật) · cửa vào Hoa hồng tháng
(bảng nguồn 0 dòng) và Giao nhanh (màn nguồn chưa port) · nghiệp vụ số dư lẻ (chưa dựng được hợp
đồng có dư lẻ trong ngưỡng) · phiếu **ngoại tệ** ở màn tạo/sửa (chưa có phiếu ngoại tệ nháp để bấm).
