# Phase 29 — Xuất hàng cha / con theo HĐ bán HRM (thiết kế 08/11/2026)

Nhánh: `gop_db` (hrm-api + hrm-client). Khảo sát hiện trạng: `plan.md` mục Phase 29.

## 1. Quyết định đã chốt (user 08/11)

| # | Câu hỏi | Chốt |
|---|---|---|
| Q1 | TK kho hàng cha | ~~1561 mọi trường hợp~~ — **user đổi 08/11 (xem mục 1b)** |
| Q2 | Phiếu xuất bán cha tự động hạch toán gì | **Đủ 8 cụm như loại 21** (doanh thu 1311/5111/33311, giảm trừ, giá vốn, thưởng, TNCN, hoa hồng, quỹ rủi ro) |
| Q3 | "Đủ hàng con" | **Đủ bộ nào làm bộ đó**: cộng dồn mọi PXH loại 20 đã hoàn tất của đúng dòng cha, số bộ = floor(min(con đã xuất / định mức con)); bộ mới đủ ⇒ nhập + xuất bán ngay |
| Q4 | Lưu con thuộc dòng cha nào | **Thêm cột dòng HĐ xuyên chuỗi** (chi tiết YCXH → ĐNXK → PXK → PXH) |
| Q5 | Chuỗi phiếu xuất bán cha tự động | **Chỉ sinh Phiếu xuất hàng** loại 21 Hoàn tất, từ kho kế toán nhập/xuất thẳng, gắn dòng cha + phiếu nhập cha nguồn |
| — | Xuất hàng con | Chỉ giá vốn, không 131 (xem 1b về TK) |

### 1b. Hạch toán — user sửa 08/11 (thay Q1)

| Nghiệp vụ | Bút toán | So với code hiện tại |
|---|---|---|
| Xuất hàng con (PXH loại 20) | **Nợ 1541 / Có 1561** — user sửa lại 08/11 (thay chốt 156 cấp 1): phiếu nhập hàng thông thường ghi Nợ 1561 | Giữ (code đã Có 1561) |
| Nhập hàng cha tự động | **Nợ 155 / Có 1541** — TK 155 cấp 1 | Giữ (code đã Nợ 155) |
| Xuất bán hàng cha TỰ ĐỘNG | 8 cụm, giá vốn **Nợ 632 / Có 155** | Mới |
| Xuất bán hàng cha loại 21 LẬP TAY (cha mua sẵn, nằm ở 1561) | 8 cụm, giá vốn **Nợ 632 / Có 1561** (như ERP) | Đổi Có 155 ⇒ Có 1561 |

Danh mục `accounts` (rehearsal): 155 "Thành phẩm" (cấp 1, chưa ghi sổ lần nào), 1551, 156 "Hàng hóa" (cấp 1, 737 dòng sổ), 1561 "Giá mua hàng hóa" (cấp 2, 111.963 dòng).

## 2. Điểm Claude tự chọn — user DUYỆT 08/11

- **Giá vốn 1 lần nhập cha (N bộ mới đủ)** = Σ theo từng con: đơn giá vốn bình quân của con đó (Σ giá vốn đã ghi Nợ 1541 / Σ SL đã xuất, cộng dồn các PXH loại 20 của dòng cha) × SL con dùng cho N bộ. Phần con dư (chưa đủ bộ) **nằm lại 1541**, vào lần nhập sau.
- **Bỏ code tạo phiếu nhập cha theo từng PXH** (`createParentImport` hiện tại); thay bằng hàm tính theo **dòng cha**: số bộ đủ cộng dồn − số bộ đã nhập ⇒ phần mới. Idempotent theo (dòng cha, PXH con nguồn).
- **Thứ tự trong 1 transaction** khi PXH loại 20 hoàn tất: hạch toán con (1541/1561) ⇒ với mỗi dòng cha bị ảnh hưởng: nhập cha (1561/1541, tăng tồn kho thẳng) ⇒ xuất bán cha (PXH loại 21 Hoàn tất, trừ tồn kho thẳng FIFO đúng lớp vừa nhập, 8 cụm). Lỗi ở bất kỳ bước nào (vd HĐ thiếu HTHT, công ty chưa có kho nhập/xuất thẳng) ⇒ rollback cả lần hoàn tất PXH con, báo câu rõ ràng.
- **Giá bán phiếu tự động** lấy từ dòng cha của HĐ (niêm yết + vượt trội, đơn giá sau giảm) như `writeContractLines` loại 21.
- **SL cha đã xuất tự động** được tính vào "đã yêu cầu / đã xuất" của dòng cha ⇒ nút YCXH loại 21 và `hasLinesLeftToRequest` không cho xuất trùng.
- **Cột mới** (nullable, ERP không đọc): `contract_product_id` ở `product_export_request_details`, `warehouse_export_request_details`, `warehouse_export_details` (tên bảng kiểm lại bằng SHOW TABLES trước khi viết migration), `product_export_details`; `product_import_details` + `product_export_details` thêm khoá dòng cha cho phiếu tự động. Mỗi bước tạo phiếu sau chép cột từ dòng phiếu trước.
- **Dữ liệu cũ**: prod chưa có phiếu loại 20/21 của HĐ HRM (khảo sát 21/10) ⇒ không cần chuyển đổi; kiểm lại số phiếu trên prod trước deploy.

## 3. Phạm vi code (dự kiến — hỏi "làm" + phạm vi trước khi code)

- hrm-api: `ProductExportPostingService` (155 ⇒ 1561; nhập cha 1561), `ContractParentImportService` (viết lại theo dòng cha + cộng dồn + floor), service mới sinh PXH loại 21 tự động (dùng lại `postAccounting`), `ProductExportRequestService::writeContractLines` + các bước tạo ĐNXK / PXK / PXH (chép `contract_product_id`), `Contract::hasLinesLeftToRequest`; migration thêm cột (liệt kê từng file trước khi chạy).
- hrm-client: chi tiết PXH / phiếu nhập hiện dòng cha nguồn (nếu cần); màn Chi tiết HĐ — để sau (mục 4 Phase 22).
- Test: PHPUnit cho 3 ca số (1 bộ đủ, 2 bộ đủ qua 2 phiếu, con dư ở 1541), ca 2 dòng cha trùng mã, ca thiếu HTHT rollback; tổng Nợ = Có mỗi phiếu.

## 4. Còn mở

- Hoá đơn VAT / yêu cầu xuất hoá đơn cho phiếu xuất bán cha tự động: theo luồng hoá đơn hiện có của loại 21 (chưa khảo sát).
- Huỷ / hoàn tác PXH loại 20 đã hoàn tất: hiện không có luồng huỷ sau Hoàn tất ⇒ giữ nguyên, không xử lý đảo phiếu cha.

## 5. Khảo sát cấu trúc kho — rủi ro tồn bán được (08/11/2026, chỉ đọc code + DB rehearsal)

**Cấu trúc**
- Kho vật lý `warehouses` → tồn `stocks` (theo kho) + `stock_of_companies` (tồn vật lý theo công ty).
- Kho kế toán `accounting_warehouses`: kho thường gắn kho vật lý (`warehouse_id`); tồn `accounting_stocks` có `stock_id` trỏ dòng `stocks`.
  Rehearsal: 18.409 dòng, 100% có `stock_id`.
- Kho kế toán nhập/xuất thẳng (`is_import_export_direct = 1`): 7 kho (cty 1, 2, 3, 4, 9), `warehouse_id` NULL, KHÔNG gắn kho vật lý;
  6.456 dòng tồn, 100% `stock_id` NULL; đang còn 42 mã hàng tồn ≠ 0 (1.079 đơn vị) từ luồng nhập/xuất thẳng của ERP
  (ERP theo dõi thêm theo nhân viên ở `product_import_direct_details`, 18.487 dòng — HRM nhập cha KHÔNG ghi bảng này).
- Mỗi (kho kế toán, mã hàng) chỉ 1 dòng `accounting_stocks`; giá vốn FIFO tính trên dòng đó (`StockValueFifoService` dựng lại lớp từ log).

**Tồn bán được** = `SellableStockReader` (HRM) = `Product::stockCompanies()` (ERP, app/Product.php:6011): Σ `accounting_stocks.qty`
**`whereNotNull('stock_id')`** (bỏ kho KM) − giữ hàng − tạm giữ − YC xuất dở ⇒ tồn ở kho nhập/xuất thẳng KHÔNG BAO GIỜ vào tồn bán được
(cả ERP lẫn HRM). Tồn vật lý không đụng kho thẳng. `WarehouseExportAccountingService::updateWarehouse`: kho thẳng ⇒ không lọc
`stock_id`, không trừ `stocks.accounting_qty`.

**Đánh giá**
| # | Rủi ro | Mức | Ghi chú |
|---|---|---|---|
| R1 | Nhập cha tự động làm sai tồn bán được | KHÔNG | dòng tồn cha `stock_id` NULL ở kho thẳng ⇒ cả 2 công thức bỏ qua |
| R2 | Code HIỆN TẠI (trước Phase 29): nhập cha xong KHÔNG xuất ⇒ hàng cha nằm mãi ở kho thẳng; người dùng lập YCXH loại 21 tay ⇒ ĐNXK/PXK chọn kho VẬT LÝ ⇒ nếu công ty có tồn thật cùng mã cha thì trừ nhầm tồn bán được thật, kho thẳng giữ số ảo; không có thì không xuất được | CAO nếu đã có PXH loại 20 trên prod | Phase 29 xuất bán cha tự động ngay trong cùng giao dịch ⇒ hết. Kiểm số PXH loại 20 trên prod trước deploy |
| R3 | FIFO trộn lớp: kho thẳng dùng chung với luồng nhập/xuất thẳng ERP ⇒ xuất cha tự động có thể lấy giá vốn của lớp ERP cũ hơn cùng mã (và ngược lại) | TRUNG BÌNH (rehearsal chưa có HĐ HRM cha–con để đo trùng mã) | Tổng giá trị không mất nhưng giá vốn lệch giữa HĐ / luồng |
| R4 | PXK hàng con lập trên ERP không chép cột dòng HĐ | CAO | Chặn ERP lập PXK cho YCXH 20/21 trước prod (Task 7) |
| R5 | Hàng con | KHÔNG | PXK con trừ tồn vật lý + kế toán kho thường cùng lúc, nhất quán |

**Chốt R3 (user 08/11):** mỗi công ty 1 **kho kế toán nhập/xuất thẳng RIÊNG** cho hàng cha lắp từ con theo HĐ HRM (vd "Kho lắp ráp HĐ");
nhập + xuất cha tự động chỉ dùng kho này ⇒ không trộn lớp FIFO với luồng ERP, giá vốn cha = giá nhập. Còn hỏi khi làm: cách nhận biết kho
(cột cờ mới trên `accounting_warehouses` hay cấu hình theo công ty), ai tạo dữ liệu kho trên prod, ERP có cần ẩn kho này khỏi các màn chọn kho thẳng.

**Chốt vượt SL (user 08/11):** giới hạn CHUNG theo dòng cha — SL còn lại = SL HĐ dòng cha − SL đã lập YCXH loại 21 tay (chưa huỷ) − SL cha đã lắp
tự động. YCXH loại 21 và YCXH con loại 20 (quy ra số bộ theo định mức) đều không vượt phần còn lại ⇒ chặn lúc lập / sửa YCXH (422 câu rõ).
Dòng con: vẫn giới hạn theo SL HĐ của chính dòng con như hiện tại.

**Chốt Task 8 (user 08/11):** (1) cột cờ `accounting_warehouses.is_contract_assembly` (migration, bảng dùng chung ERP), mỗi công ty đúng 1 kho bật,
chỉ bật được khi kho là nhập/xuất thẳng; (2) ô tick ở màn danh mục kho kế toán HRM `/warehouse/accounting-warehouses`, kế toán tự tạo kho trên prod —
công ty chưa có kho ⇒ chặn hoàn tất PXH con, câu báo rõ; (3) ẨN kho này ở mọi danh sách chọn kho kế toán của CẢ ERP và HRM (trừ màn danh mục kho
và báo cáo tồn) — chỉ luồng tự động dùng.

**Sửa Task 8 (user 08/11, thay mục (2) ở trên):** kho THEO TỪNG CÔNG TY, mỗi công ty đúng 1 kho, **do phần mềm khởi tạo, tạo sẵn khi deploy**
(không có ô tick, người dùng không tự tạo / bật cờ). Tên "Kho lắp ráp hợp đồng", mã "<mã công ty>-LRHD", nhập/xuất thẳng, cờ `is_contract_assembly = 1`.
Khoá ở cả ERP + HRM: không sửa cờ / xoá / ngừng hoạt động (BE chặn); vẫn hiện ở danh mục kho + báo cáo tồn, ẩn ở mọi danh sách chọn kho.
Claude chọn cách tạo: lệnh artisan idempotent (tạo cho công ty đang hoạt động còn thiếu kho) chạy lúc deploy, chạy lại được khi thêm công ty;
công ty chưa có kho ⇒ chặn hoàn tất PXH con, câu báo "liên hệ quản trị để khởi tạo kho lắp ráp hợp đồng".
