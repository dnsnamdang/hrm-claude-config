# Fix: Số chứng từ công nợ đầu kỳ → link về danh sách lọc theo phiếu

## Bối cảnh
Báo cáo `admin/accounting/account_details?type=customer`. Số CT loại **DeclareDebtBeginning** (Khai báo công nợ đầu kỳ, vd TPV.CNĐKHĐ.00235) KHÔNG có màn chi tiết → click phải về màn DANH SÁCH và lọc sẵn theo phiếu đó.

## Hiện trạng
- Accessor `AccountDetail::getInvoiceableLinkAttribute` nhánh DeclareDebtBeginning: `route('declareDebtBeginning.index', ['id'=>invoiceable_id])` → mở danh sách nhưng KHÔNG lọc (id không được view dùng).
- `DeclareDebtBeginning::searchByFilter` ĐÃ hỗ trợ `$request->code` (exact). View có ô search cột `code` ("Mã phiếu", id=`#code`).

## Fix
- [x] Accessor: đổi sang `route('declareDebtBeginning.index', ['code'=>$this->invoiceable_code])`.
- [x] View index blade: sau init datatable, `getParam('code')` → nếu có thì `$('#code').val(code)` + `table.ajax.reload()` → lọc đúng phiếu.
- [x] php -l sạch, view:clear. Verify: accessor sinh URL ?code=...; code 598 khớp; đúng 1 phiếu.
- [ ] User reload báo cáo → click số CT DeclareDebtBeginning → mở danh sách lọc đúng phiếu.

## Không làm: các loại phiếu khác giữ nguyên (đa số đã có màn show).

## Bổ sung 2026-07-20 (report type=customer dùng JS getInvoiceLink, KHÔNG dùng accessor)
- [x] Phát hiện: customerIndex.blade.php render số CT bằng JS getInvoiceLink → fix accessor trước KHÔNG tác động report này.
- [x] Sửa JS getInvoiceLink: DeclareDebtBeginning → '/admin/accounting/declare-debt-beginning?code='+encodeURIComponent(code). ServiceAccounting (HTDV) GIỮ NGUYÊN link show (user chốt A - đúng theo canView phân quyền; not_found khi thiếu quyền là đúng).
- [ ] User reload report → click số CT công nợ đầu kỳ → danh sách lọc đúng phiếu.
