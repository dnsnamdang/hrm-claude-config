# Design (tóm tắt) — Phiếu báo có (ERP → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Ngày: 2026-08-24
> **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-08-24-finance-bill-income-report-design.md`
> Feature soi gương: `.plans/gop-db/finance-bill-income/` (Phiếu thu tiền — đã ghi sổ cái) ·
> `.plans/gop-db/finance-bill-adjust-dept-request/` (Đề nghị điều chỉnh công nợ — đang đọc dữ liệu báo có)

---

## Mục tiêu

Port màn ERP `admin/income-expenditure/bill_income_report` (**Phiếu báo có**) sang HRM, phân hệ
**Tài chính**, route `/finance/bill-income-reports`.

Phiếu báo có là chứng từ kế toán ghi nhận **tiền về tài khoản ngân hàng** theo sao kê: mỗi khoản
tiền về được gắn với khách hàng / hợp đồng / nhà cung cấp, duyệt xong thì **ghi bút toán vào sổ
cái**. Khoản chưa rõ của ai thì gắn "KHÁCH KHÔNG RÕ", sau đó dùng màn *Tổng hợp tiền về ngân hàng*
để chuyển sang **Phiếu yêu cầu điều chỉnh công nợ** (màn HRM đã port) gán lại đúng đối tượng.

Vòng đời chỉ 2 bước: **Đang tạo → Đã duyệt** (không có gửi duyệt / từ chối / hủy).

## Scope

**Trong**: danh sách · tạo/sửa/xóa nháp · duyệt kèm **ghi sổ cái** · chi tiết + cờ "Không báo tiền
về" · 3 loại thu (bán hàng / nhà cung cấp / khác) · màn **Tổng hợp tiền về ngân hàng** + xuất Excel ·
**Import Excel sao kê** · cửa sang màn Điều chỉnh công nợ · **Lịch sử thay đổi** (ERP không có).

**Ngoài**: 2 màn rác `forAccounting` / `approved` bên ERP (trỏ nhầm sang API Phiếu đề nghị thu tiền,
không có mục menu) · không đụng repo ERP · không migration cấu trúc bảng chính · không `mysql2`.

## Quyết định lớn (user chốt 2026-08-24)

| # | Quyết định |
| --- | --- |
| 1 | **Port đầy đủ chức năng ERP** + bổ sung Lịch sử thay đổi |
| 2 | **Có ghi sổ cái** `account_details` + `account_detail_refs` như ERP — dùng lại kiến trúc `BillIncomeAccountingService` (hàm `buildEntries()` thuần, unit-test được) |
| 3 | Hợp đồng bán: **`firm_contracts` → `hrm_contracts`**; giữ `FirmContract` trong morphMap cho 746 dòng cũ |
| 4 | Quyền **giữ đúng tên ERP**, thêm guard `api` vào `PermissionsTableSeeder`: `Quản lý phiếu báo có`, `Xem tất cả phiếu báo có của tổng công ty`, `Xem tất cả phiếu báo có của công ty` |
| 5 | Dùng chung 2 bảng ERP `bill_income_reports` + `bill_income_report_details`, không đổi schema |
| 6 | Lịch sử ghi vào bảng CHUNG `catalog_histories` như 3 phiếu tài chính đã port ⇒ **feature KHÔNG có thay đổi schema nào** (đính chính so với bản spec đầu: bỏ 2 bảng riêng) |

## Khác biệt có chủ đích so với ERP

1. **Tách `POST /{id}/approve`** thay vì cho client gửi `status=2` qua `PUT /{id}` (ERP gộp → buộc
   nới `canEdit()` cho người duyệt).
2. Ngày gửi lên **ISO `Y-m-d`**, không phải `d/m/Y` (luật `date` của Laravel hiểu `m/d/Y` → form
   chết từ ngày 13 hàng tháng).
3. Sinh mã bọc transaction + `lockForUpdate` (2 cổng cùng sinh mã, cột `code` UNIQUE).
4. Validate bổ sung `supplier_id` bắt buộc khi loại thu = NCC (ERP bỏ sót).
5. Badge **"Đang tạo" = XÁM** theo SRS (ERP để đỏ như phiếu bị từ chối).
6. Import Excel trả kết quả **đồng bộ** qua `V2BaseImportModal` (ERP chạy job nền + ghi file log).
7. Thêm Lịch sử thay đổi.

## Hiện trạng dữ liệu (đo trên `gop_db` 2026-08-24)

3.832 phiếu — **tất cả đều Đã duyệt**, 3.714 phiếu loại *Thu bán hàng*, 111 phiếu cũ `type=0`;
**0 phiếu** loại NCC / Thu khác. 10.199 dòng chi tiết, 9.435 dòng không gắn hợp đồng,
`export_requestable_*` **rỗng 100%**.

⇒ Nhánh *Thu nhà cung cấp*, *Thu khác* và *phiếu YCXH* port theo code ERP, **không có dữ liệu thật
để đối chiếu** — vùng rủi ro cần test tay. Không có phiếu *Đang tạo* nào → cần seeder dữ liệu test
cho luồng sửa/xóa/duyệt.

## Rủi ro đã biết

- **Sổ cái dùng chung với ERP**: ghi sai/trùng là lệch số liệu kế toán thật. Bảo vệ bằng idempotent
  theo `invoiceable_id/type` + transaction + unit test `buildEntries()`.
- Import tự duyệt + ghi sổ ngay → sai file là bút toán rác. Chỉ ghi khi dòng hợp lệ.
- Phiếu HRM gắn `hrm_contracts` có thể lỗi *Class not found* khi mở bên ERP (rủi ro đã chấp nhận ở
  3 feature trước).
- `exchange_rate` lưu kiểu **varchar** trong DB — phải ép kiểu khi tính.
