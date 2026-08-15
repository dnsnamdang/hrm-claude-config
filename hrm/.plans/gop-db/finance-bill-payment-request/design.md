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
