# Design (tóm tắt) — Phiếu đề nghị thanh toán (ERP → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Ngày: 2026-08-14
> **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-08-14-finance-bill-payment-request-design.md`
> Feature tham chiếu: `.plans/gop-db/finance-bill-income-request/` (Đề nghị **thu** tiền — đã xong)

---

## Mục tiêu

Port màn ERP `admin/income-expenditure/bill_payment_requests` sang HRM, phân hệ **Tài chính**,
route `/finance/bill-payment-requests`. Chứng từ đề nghị **chi tiền**, đi qua **luồng duyệt 5 cấp**.

## Scope

**Trong**: danh sách 4 chế độ (Của tôi · Tất cả · Chờ duyệt · Đã duyệt) · tạo/sửa/xóa nháp ·
duyệt 5 cấp · Không duyệt · file đính kèm · in · xuất Excel · thông báo chuông.

**Ngoài**: màn Phiếu chi / Ủy nhiệm chi (dừng ở trạng thái *Chờ tạo phiếu chi*) · loại chi 3/4/10
(0 phiếu) · nhánh "không có hợp đồng" (`has_contract` = 1 ở cả 4.040 phiếu) · bảng phân bổ phiếu
YCXH (0 dòng) · không đụng repo ERP.

## Quyết định lớn (user chốt 2026-08-14)

| # | Quyết định |
| --- | --- |
| 1 | Dùng chung bảng ERP `bill_payment_requests` + `bill_payment_request_details`, không migration |
| 2 | Port 4 loại chi: **1** Chi trả NCC · **2** Chi trả lại KH · **6** Chi thưởng thực hiện HĐ · **12** CP vận chuyển NCC |
| 3 | **Đủ 5 cấp duyệt** (TP → KT công nợ → KT trưởng → BGĐ → Chờ tạo phiếu chi), dừng trước phiếu chi |
| 4 | Nguồn hợp đồng bán `firm_contracts` → **`hrm_contracts`** (loại 2 và 6) |
| 5 | Công nợ giữ nguyên công thức ERP — đọc sổ cái `account_details` (TK 3311 / 1311 / 3351) |
| 6 | File đính kèm **giữ cột `attachments` của ERP**, KHÔNG dùng bảng `files` — ngoại lệ có chủ đích vì 2 cổng dùng chung DB |
| 7 | Popup "Chi tiết chuyến xe" (loại 12) làm **đầy đủ 13 cột** như ERP |
| 8 | Thêm **9 quyền mới id 1153–1161** vào `PermissionsTableSeeder`, **giữ nguyên văn tên ERP** (kể cả 2 chỗ ERP sai chính tả "đề **nghi**"); dùng lại `Kế toán thanh toán` id 1152 |
| 9 | Base UI: danh sách bám `pages/assign/customers/index.vue`, form bám `CustomerForm.vue` |

## Quyết định lớn bổ sung (user chốt 2026-08-18) — đợt sửa UI màn danh sách

| # | Quyết định |
| --- | --- |
| 10 | Cột Hành động **KHÔNG có nút "Xem chi tiết"** — lối vào chi tiết là link ở cột Mã phiếu, nên cột đó bị khoá `locked`, không tắt được ở popup cấu hình cột |
| 11 | Có popup **Cấu hình cột hiển thị** dùng `columnCustomizationMixin`, khoá `finance_bill_payment_requests` **dùng chung cho cả 4 chế độ** (tách khoá theo `mode` thì user phải cấu hình lại 4 lần). BE không cần migration |
| 12 | Lưới có thêm 2 cột **Người / Ngày cập nhật** (mặc định hiện) — kéo theo quan hệ `employee_update()` + 2 field ở `BillPaymentRequestListResource` |
| 13 | **3 cột ngày cùng định dạng `d/m/Y H:i`** (Ngày lập · Ngày nhận · Ngày cập nhật). Giờ:phút là dữ liệu thật, 0/4.051 dòng ở `00:00:00` |
| 14 | Tiêu đề cột `objectName` là **"Khách hàng / Nhà cung cấp"** (không phải "Khách hàng") — nội dung cột đổi theo loại chi, loại 1 và 12 luôn hiện NCC. Dữ liệu và luật `objectName()` **giữ nguyên như ERP** (không đụng quyết định #4 cũ) |
| 15 | Sắp xếp: **bỏ** sort cột Loại chi + Hình thức TT · **thêm** sort cột KH/NCC · cột Trạng thái sort thật (trước đó hỏng) |
| 16 | Việt hoá thông báo Select2 sửa thẳng ở **component dùng chung** `V2BaseSelectRemote.vue` (18 màn), không chắp vá riêng cho màn này |

**Điều tra kèm theo (không phải bug):** gõ tên nhà cung cấp vào ô lọc **Khách hàng** luôn ra 0 kết
quả — bảng `customers` chứa **cả KH lẫn NCC**, phân biệt bằng `is_customer` / `is_supplier`
(bảng `suppliers` có 0 dòng), mà `assign/customers/search` có điều kiện cứng `is_customer = 1`.
Đó là lý do phải đổi tiêu đề cột ở quyết định #14.

**Ràng buộc kỹ thuật phát sinh:** sort cột KH/NCC không map thẳng được sang cột DB nên có nhánh
riêng `BillPaymentRequest::applyObjectNameSort()` dựng lại 5 nhánh của `objectName()` bằng SQL —
**bắt buộc dùng derived table**, không dùng LEFT JOIN thẳng (nổ `created_by` ambiguous) và không
dùng subquery tương quan (14,2s vì `bill_payment_request_details` thiếu index trên
`bill_payment_request_id`). Lý do đầy đủ ghi trong docblock của hàm.

## Tận dụng được từ feature Đề nghị thu tiền

- `Relation::morphMap()` cho **8 class hợp đồng ERP** đã đăng ký sẵn ở `FinanceServiceProvider`
  (còn thiếu 2: `WarehouseImport` 25 dòng + `WarehouseExport` 15 dòng → phải thêm).
- 3 endpoint popup dùng lại nguyên: `search-contracts` (HĐ bán 3 nguồn) ·
  `search-buy-contracts` (HĐ mua 5 nguồn) · `search-suppliers`.
- Component FE: popup Hợp đồng bán / Hợp đồng mua / NCC / Khách hàng.
- Quyền `Kế toán thanh toán` id 1152.
- Bài học: **không** dùng middleware `checkPermission` (spatie bỏ sót role `model_type='App\Employee'`);
  **không** chép khuôn form từ `ProductTransferRequestForm.vue` (class nằm trong `<style>` riêng).

## Khác biệt có chủ đích so với ERP

1. Sinh mã phiếu bọc transaction + `lockForUpdate` (ERP không khóa, 2 cổng cùng sinh mã dễ trùng).
2. Validate chặt hơn: chặn nhảy cóc trạng thái, chặn số tiền duyệt vượt cấp trước, 403 đúng chỗ.
3. **Trần số tiền đề nghị chỉ áp khi công nợ > 0** — vì hợp đồng `hrm_contracts` chưa có dòng
   hạch toán nào nên công nợ = 0; bê nguyên luật ERP thì loại chi 2 sẽ bị cắt về 0 và không dùng được.
4. File đính kèm dùng cột `attachments` của ERP; gỡ file qua `DELETE /{id}/files` với `file_url` và
   **xoá thật object trên S3** (mỗi file có tên ngẫu nhiên riêng nên chỉ thuộc 1 phiếu).
   **Chốt lại cuối 2026-08-15**: giao diện theo khuôn "Import tài liệu kèm biên bản" (bỏ cột Tên tài
   liệu) và **upload NGAY khi chọn file** (`POST /upload-files` → lưu phiếu gửi `attachment_urls[]`),
   thay cho phương án ban đầu gửi kèm multipart trong `store`/`update`. Lý do bắt buộc: `FilePreviewModal`
   xem trước PDF/Word/Excel bằng Google & Office Viewer — 2 dịch vụ này phải tải được file qua URL công
   khai, giữ file ở client thì chỉ xem trước được ảnh. Đổi lại chấp nhận file rác trên S3 nếu user bỏ
   form giữa chừng (màn Biên bản họp cũng vậy), và BE phải chặn `starts_with` prefix S3 của màn.
   Dung lượng file đã lưu lấy qua `GET /{id}/attachment-sizes` (HEAD S3 song song), tách khỏi `show()`
   để màn in / xuất Excel không phải chờ.
5. `POST /{id}/approve` tách riêng khỏi `PUT /{id}` — gộp thì buộc phải nới `canEdit()` cho người
   duyệt, đúng lỗ hổng mà spec 8.3 yêu cầu bịt.
6. Trần số tiền của từng cấp **cắt ở BE** (ERP chỉ cắt ở FE nên gọi thẳng API là lách được).
7. **Bảng chi tiết in/Excel (chốt 2026-08-24)** — bám cấu trúc ERP (tiêu đề 2 dòng · bảng riêng cho
   phiếu ngoại tệ · nhãn `KT trưởng/BGD`, `Số hợp đồng nhập mua` / `Số đơn hàng/Hợp đồng` · dòng
   "Nhà cung cấp:" đầu phiếu), trừ 3 chỗ cố ý lệch:
   - Cột **"Số tiền chi"** chỉ in khi phiếu ở trạng thái **Duyệt phiếu chi** (ERP in luôn, toàn dấu `_`).
   - **Không port 3 nhánh cột đối tượng "code chết" của ERP** (`type_customer_cash()` /
     `type_supplier_cash()` / `type_employee_cash()` xét `isset($data['type_customer'])`… — khoá không
     tồn tại nên luôn `false`). Port vào chỉ sinh cột rỗng. Cột đối tượng duy nhất giữ lại là
     "Nhà cung cấp" ở nhánh loại 1 + `has_contract = 1` + tiền mặt.
   - Dòng **Tổng cộng** gộp theo **số cột mô tả thật**; ERP cắm cứng `colspan = 3` nên lệch 1 ô ở
     loại 2/3 + tiền mặt, và **không in dòng tổng** ở nhánh loại 1 không hợp đồng.

   Toàn bộ cờ bố cục (`is_foreign` · `show_delivery` · `show_supplier` · `contract_label` ·
   `show_money_approve`) do BE tính trong `BillPaymentRequestPrintResource::columns` — màn in FE và
   file Excel **không được tự suy lại**, nếu không 2 đầu ra sẽ lệch cột.

## Rủi ro đã biết

- Phiếu do HRM tạo gắn `hrm_contracts` → mở bên **ERP lỗi "Class not found"** (đã chấp nhận, y hệt
  màn Đề nghị thu tiền).
- Loại chi 2/6 hiển thị công nợ **0** cho hợp đồng HRM tới khi có luồng hạch toán.
- DB gần như không có phiếu ở trạng thái chờ duyệt (status 5: **0 phiếu**) → cần seeder dữ liệu test.

## Số liệu nền (DB `gop_db`, 2026-08-14)

4.040 phiếu · 47.329 dòng chi tiết · 3.432 phiếu có file đính kèm ·
loại chi: 1 → 3.322 · 6 → 429 · 2 → 205 · 12 → 84 · các loại khác 0.


---

## Kết quả triển khai (2026-08-15) — CODE DONE 8/8 phase

| Lớp | Sản phẩm |
| --- | --- |
| BE | 30 file mới + 5 file sửa · **15 route** · 9 quyền id 1153–1161 · 2 seeder (quyền + dữ liệu test) |
| FE | **12 file mới** + 2 file sửa · màn danh sách 4 chế độ · form tạo/sửa · màn chi tiết + duyệt · màn in |

**Bổ sung ngoài plan (có lý do):**
1. `GET /party-banks` — spec 4.5 đòi khối ngân hàng tự điền từ `supplier_banks` + cột ngân hàng của
   `customers`, nhưng không phase nào dựng API cho nó ⇒ thiếu thì khối ngân hàng là ô trống vĩnh viễn.
2. `ContractSearchModal` thêm prop `extraParams` (thuần thêm) để loại chi 2 gửi `only_mine=1`.
3. Bảng chi tiết thêm `approvalMode` + `editableMoneyKey` cho màn duyệt.
4. `reject_comment` thêm vào dữ liệu màn in.

**Đã chứng minh bằng số liệu thật:** công nợ 1.035 dòng lệch 0 · cột tiền theo trạng thái 116 phiếu
lệch 0 · validate 15/15 ca · vòng đời duyệt 5 cấp 6/6 bước + 10/10 ca xấu bị chặn · vòng đời file
thật trên S3 · phạm vi quyền khớp SQL tuyệt đối ở 3 mức quyền.

**Còn lại (không chặn):** toàn bộ FE chưa mở trình duyệt — cần user test tay 6 nhóm việc ghi ở
checkpoint cuối `plan.md`. Dữ liệu sẵn: 8 phiếu `TEST.DNTT-CHI.*`.

---

## Bổ sung 2026-09-03 — Lưu nháp chỉ bắt buộc Loại chi

User báo màn Tạo vẫn chặn ở **Lý do chi** khi bấm *Lưu nháp*. Chốt lại luật của 2 nút:

| Nút | Bắt buộc |
| --- | --- |
| **Lưu nháp** (`status = 1`) | **Chỉ `type` (Loại chi)** |
| **Lưu và gửi duyệt** (`status = 2`) | Nguyên bộ rule cũ theo ma trận loại chi × hình thức TT |

- Thay quyết định 2026-08-22 (khi đó mới nới khối ngân hàng + bảng chi tiết, lý do chi vẫn bắt).
  Nháp giờ chấp nhận cả dòng chi tiết thiếu hợp đồng / số tiền.
- Rule **định dạng** vẫn chạy ở nháp (`numeric` · `gt:0` · `date` · `exists` · `Rule::in` cho
  `contractable_type`) — nới required không mở cửa cho dữ liệu rác vào cột morph / khoá ngoại.
- ⚠️ Bẫy đã xử: `reason` · `type_payment` · `type_money_id` · `exchange_rate` là cột **NOT NULL,
  không default**. Chỉ nới validate mà không đổ mặc định ở
  `BillPaymentRequestService::masterPayload()` (TM · VNĐ · tỷ giá 1 · lý do rỗng) thì lưu nháp trả
  **500** chứ không lưu được.
- Phạm vi sửa: **BE 2 file** (`BillPaymentRequestStoreRequest` — `UpdateRequest` kế thừa nên ăn theo ·
  `BillPaymentRequestService`). **FE không đụng**: `validateForm()` chỉ chạy rule vee-validate về
  định dạng, mọi câu "Bắt buộc nhập" trên form đều là lỗi 422 do BE trả về.
- Chi tiết + bảng kiểm chứng 6 ca: `plan.md` mục "Nới validate LƯU NHÁP" ·
  spec mục 4.5 (khối chú ý đầu mục).
