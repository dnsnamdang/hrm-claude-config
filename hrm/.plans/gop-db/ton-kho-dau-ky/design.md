# Khai báo tồn kho đầu kỳ (vật lý) ERP → HRM — Design

**Người phụ trách:** @junfoke — 2026-10-20 · Nhánh `feat/chuyen-doi-hang-hoa` (cả 2 repo)
Plan: `.plans/gop-db/ton-kho-dau-ky/plan.md`

## Nguồn ERP

- Menu `Kho › Tồn kho đầu kỳ › Khai báo tồn kho đầu kỳ` (route `beginningStock.index`, 1 chỗ duy nhất).
- `app/Http/Controllers/Warehouse/BeginningStocksController.php`, `app/Model/Warehouse/BeginningStock.php`,
  `app/ExcelImports/BeginningStocksImport.php`, view `resources/views/warehouse/beginning_stocks/{index,create,edit}`,
  class JS `partials/classes/warehouse/BeginningStock*.blade.php`, popup hàng `ProductsController@getData` (`request_type=begin_stock`).
- Route group `checkPermission:Thủ kho`; phạm vi xem 2 quyền "Xem khai báo tồn kho vật lý theo tổng công ty / theo công ty".

## Dữ liệu (gop_db local, đo 20/10/2026)

10.357 dòng `beginning_stocks`, 4 công ty (1: 6.673 · 4: 3.315 · 3: 275 · 2: 94), 10 kho, 9.936 bộ (kho, hàng, công ty);
khai 08–11/2025. Mỗi dòng có đủ 1 lô `warehouse_import_lots` type 2 + `stock_logs`/`stock_position_logs` type 2
(ngày 2025-08-01, đã chỉnh tay) + `stock_position_detail_logs`. Kế toán: 10.098 dòng `beginning_accounting_stocks`.

## Nghiệp vụ ERP

| Phần | Nội dung |
|---|---|
| Danh sách | STT, Tên hàng, Mã hàng, Kho, Vị trí, ĐVT, Số lượng, Người tạo, Ngày tạo, hành động Sửa/Xóa |
| Lọc | Tên hàng (tên hoặc mã), Mã hàng, Kho (kho THƯỜNG + THANH LÝ của công ty), Vị trí (tên), Người tạo |
| Thêm (trang) | Kho + Công ty; chọn hàng (popup) → ĐVT + SL gợi ý = tồn kế toán đầu kỳ; mỗi hàng nhiều vị trí, tổng vị trí = tổng SL; Lưu / Lưu & Thêm |
| Sửa (trang) | Chỉ sửa Số lượng |
| Sửa/Xóa hiện khi | Hàng chưa có giao dịch nào khác tại kho đó của công ty (`Warehouse::checkActive`) |
| Import | ≤200 dòng; cột: Tên hàng, Mã hàng, ĐVT, Mã kho, Mã vị trí, SL, Mã công ty; bắt buộc đã khai tồn kế toán và SL khớp |
| Xuất Excel | <300 dòng tải ngay, ≥300 gửi mail |
| Ghi tồn | mỗi dòng (hàng × vị trí) = 1 `beginning_stocks` + 1 lô type 2 (`TONDAUKHO-{id}-{product}-{unit}`) + 8 bảng tồn vật lý (type 2) + `stocks.accounting_qty` + nối `accounting_stocks.stock_id`. Sửa/Xóa: chỉnh/đảo ngược + dời log tồn đầu phía sau |

## Quyết định (user chốt 20/10/2026)

1. **Quyền riêng** `Khai báo tồn kho đầu kỳ` (guard api, type phân hệ Kho) cho cả màn (xem + thêm/sửa/xoá/import).
   Phạm vi: Super admin xem mọi công ty + ô lọc Công ty; người khác chỉ công ty được thao tác (chính + `company_employees`,
   theo chốt C-a-1 13/10). Bỏ 2 quyền xem ERP (vá lỗ "không quyền nào ⇒ thấy hết").
2. **Sửa lỗi ghi tồn của ERP** ở phía HRM (ERP không đụng):
   - `stock_of_companies` theo **công ty khai báo** (ERP lấy công ty người đăng nhập).
   - Xóa: `stock_position_of_companies` **trừ** (ERP gán đè `qty = change`).
   - Sửa SL: cập nhật cả `stock_of_companies`, `stock_position_of_companies`, log chi tiết (ERP bỏ sót).
   - Kiểm "đã có phiếu xuất" bằng `whereIn` toàn bộ lô tồn đầu (ERP `where(col, array)` chỉ so 1 phần tử).
3. **Thêm tay áp cùng luật Import** (Claude đề xuất, user OK): hàng phải đã khai tồn kế toán đầu kỳ tại kho đó của công ty
   và **tổng SL (quy ĐVT cơ bản) khớp** số kế toán. Sửa SL cũng phải giữ khớp (tổng các vị trí của hàng).
   Trùng: chặn theo (hàng, kho, công ty) — giống Import + popup chọn hàng ERP.
4. **Mở rộng `PhysicalStockWriter`** bằng HÀM MỚI (`importBeginning`, `adjustBeginning`, `removeBeginning`); KHÔNG sửa
   `importLot` / `exportLot` / `exportShortage` ⇒ Phiếu nhập kho, Phiếu tái xuất không đổi hành vi.
5. Ngày log tồn đầu (`stock_logs`, `stock_position_logs`) = mốc ERP `config('beginning_stock')` = `2023-04-01`
   (ERP `AppServiceProvider:160`) — hằng `BeginningStockService::LOG_DATE`. `stock_position_detail_logs` = now (như ERP).
   (Dữ liệu cũ có log ngày 2025-08-01 — đã chỉnh tay trên prod, không theo config.)
6. `objectable_type` ghi nguyên chuỗi class ERP `App\Model\Warehouse\BeginningStock` (ERP morphTo đọc lại).
7. Xuất Excel làm phía FE (convention HRM), bỏ gửi mail. Danh sách kiểm "đã giao dịch" theo lô cả trang (ERP: ~7 truy vấn/dòng).
8. Ô Công ty ở form Thêm chỉ liệt kê công ty được thao tác; ô Kho = kho có kho kế toán của công ty đã chọn (ERP `getByCompany`).
9. **Sửa / Xoá theo NHÓM** (hàng, kho, công ty) — Claude tự chốt để luật khớp kế toán dùng được: popup Sửa liệt kê mọi vị trí
   của nhóm (chia lại SL, tổng phải = SL kế toán); Xoá gỡ cả nhóm (xoá lẻ 1 vị trí làm lệch tổng, mà khai lại bị chặn trùng).
10. SL tồn kế toán = tổng `beginning_accounting_stocks.import_qty` qua kho kế toán của kho vật lý + công ty (khớp 9.935/9.936
    nhóm dữ liệu hiện có). ERP cộng `qty_after` log kế toán — lệch ở 32 nhóm khi 1 tồn có nhiều log.
