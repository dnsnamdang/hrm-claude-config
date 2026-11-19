# YCXH — Port đầy đủ các loại từ ERP (tóm tắt)

- Người phụ trách: @namdangit · Nhánh: `gop_db` · Bắt đầu: 2026-10-12
- Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-12-ycxh-port-erp-day-du-design.md`

## Mục tiêu
Phiếu yêu cầu xuất hàng HRM tương đương ERP về trường/cột/popup/nghiệp vụ cho mọi loại; HRM thêm loại 20/21
(HĐ HRM); mọi loại lưu nháp được khi chỉ chọn Loại.

## Lộ trình
1. **Phase 1 — nền tảng**: nháp chỉ cần Loại; chọn/đổi nguồn khi sửa nháp; ẩn 4/15/16/17; hoàn thiện 20/21
   (popup HĐ `can_export` + V2BaseModal, kiểm SL ≤ còn lại, kho bắt buộc, chi tiết hiện kho); bảng nhập tay đủ cột
   (Tồn, ĐVT, Hình ảnh, Xem tồn); loại 99 Ghi nhận chi phí HĐ (+ HĐ HRM); loại 3 hạn mức `max_borrow_date`.
2. Phase 2 — loại 14 đầy đủ, rồi 15
3. Phase 3 — loại 16, 17
4. Phase 4 — loại 4
5. Phase 5 — duyệt TP/BGD (10/11) + các mục chi tiết
6. Phase 6 — chuyển form sang vee-validate

## Quyết định đã chốt
- Q1 5 phase + phase 6 vee-validate; 20/21 giữ và hoàn thiện
- Q2 Nháp được chọn/đổi nguồn ở Sửa, đổi khi có dòng → xác nhận rồi nạp lại
- Q3 Ẩn 4/15/16/17 ở Tạo tới khi phase tương ứng xong
- Q4 Giữ validateForm thủ công + toast tới Phase 6
- Q5 20/21 kho bắt buộc khi gửi (trừ xuất thẳng), chi tiết hiện kho
- Q6 Cột Tồn dùng lại `StockService::getLineStocks`
- Q7 Popup chi phí HĐ loại 99 = nguồn ERP + nhóm HĐ HRM
- Q8 Hướng B: tách dần component (`SourcePicker`, `ManualLinesTable`, `ContractCostModal`), BE 1 controller + 1 service
- Q9 Không cho đổi Loại khi nháp
- Q10 Tồn < SL yêu cầu chỉ cảnh báo
- Q-ERP = A: model ERP mới `App\Model\Hrm\HrmContract` làm đích morph loại 99
- F9 = (a): loại 7 không cho đổi phiếu chuyển khi sửa (giống ERP)

## Rủi ro
- ERP đọc morph `contract_costable` với class HRM → **đã kiểm: crash** (ERP eager-load + đọc `->link`). Chờ user chọn
  Q-ERP: A model ERP `App\Model\Hrm\HrmContract` (khuyến nghị) / B morphMap. Xem plan.md "Spec corrections" R2.
- ~~Gỡ link phiếu chuyển (loại 7) khi đổi nguồn~~ → **ĐÃ CHỐT (a) 2026-10-12**: loại 7 KHÔNG cho đổi phiếu chuyển khi
  sửa (theo ERP — `validateProductTransferRequests` cấm đổi tập phiếu chuyển), nên không có nhánh gỡ link.
- Sửa `QuotationProductSearchModal` (dùng chung) để có ĐVT/ảnh → hỏi trước.

## Đối chiếu Phase 1 (Task 16, 2026-10-12)

Nguồn ERP: `warehouse/product_export_requests/{create,form,formJs}.blade.php`, JS class
`partials/classes/warehouse/ProductExportRequest.blade.php`, `ProductExportRequestsController@store` (:402-560).
Nguồn HRM: `ProductExportRequestForm.vue`, `ManualLinesTable.vue`, các modal, `rulesForType` (:783-927).
20/21 không có ở ERP → đối chiếu với spec §5.2. "Gửi duyệt" = status 2 (ERP loại 3 gửi → 10 = Phase 5).

| Loại | Trường header | Cột bảng hàng | Popup | Ràng buộc gửi duyệt | Lệch | Thuộc phase |
| --- | --- | --- | --- | --- | --- | --- |
| 3 Mượn | Kho xuất*, Ngày cần mượn*, Ngày trả*, Vận chuyển*/Số km (CTVC) — khớp | Bảng nhập tay đủ cột ERP (STT·Tên·Model·Mã·TH·Tồn·YC xuất*·ĐVT·Đơn giá·Thành tiền·Ảnh·Xem tồn) — khớp | Chọn hàng `QuotationProductSearchModal` | kho, ngày mượn ≥ hôm nay, trả > mượn, trả ≤ hôm nay + `max_borrow_date` — khớp | ERP gửi → status 10 (HRM → 2) | Phase 5 (đã ghi) |
| 6 ĐC nội bộ | Kho xuất*, Kho nhập*, Vận chuyển* — khớp | Bảng nhập tay — khớp | Chọn hàng | kho nhập ≠ kho xuất — khớp | **L1** ERP chặn "Kho đã chọn không thuộc Công ty" (kho phải có `accounting_warehouses` cty người lập); HRM không kiểm | Ngoài Phase 1 — controller quyết (cùng gốc L2) |
| 7 ĐC chi nhánh | Gửi đến công ty*, Kiểu nhập kho*, Phiếu YC chuyển hàng*, Vận chuyển*; không kho xuất — khớp | Bảng read-only từ phiếu chuyển: thiếu cột **Tồn** so với ERP (STT·Tên·Model·Mã·TH·Tồn·YC xuất·ĐVT·Đơn giá·Thành tiền) | Chọn phiếu chuyển | cty, kiểu nhập, ≥1 phiếu, cùng người yêu cầu — khớp | L5 thiếu cột Tồn (minor) | Không thuộc Phase 1 (§5.3 chỉ 3/6/12/18/19/99) |
| 12 Hàng gửi | Khách hàng*, Kho xuất*, Vận chuyển*, khối KH — khớp | Bảng nhập tay; ERP cột thứ 6 tên **"Gửi"** và hiện "-" khi chưa chọn KH, HRM ghi "Tồn" (cùng endpoint, cùng `customer_id`) | Chọn KH + chọn hàng | KH, kho — khớp | L4 nhãn cột "Gửi" vs "Tồn" (minor) | Phase 1 (bảng nhập tay) — chưa sửa vì phải đụng Form.vue user đang sửa |
| 14 Bán HĐ hãng | Bản rút gọn (HĐ hãng, VAT, Cần lắp đặt) | Rút gọn | `FirmContractSearchModal` | firm_contract, VAT, need_repair, kho | Thiếu tab/cột/3 kiểm tra | Phase 2 (đã ghi) |
| 18 Sản xuất | Kho xuất*, Vận chuyển* — khớp | Bảng nhập tay — khớp | Chọn hàng | kho (trừ xuất thẳng), vận chuyển — khớp | ERP luôn hiện ô Vận chuyển cho 18 kể cả xuất thẳng (BE ERP không bắt) — HRM ẩn, hợp lý | — |
| 19 Thực hiện HĐ | HĐ/đơn hàng*, khối KH snapshot, Kho xuất*, Vận chuyển* — khớp | Bảng nhập tay — khớp | `EmplementContractSearchModal` (union firm + wr) | emplement_contract_id(+type), kho — khớp | — | — |
| 99 Khác | Ghi nhận chi phí HĐ (không bắt buộc), Kho xuất*, Vận chuyển* — khớp | Bảng nhập tay — khớp | `ContractCostModal` = nguồn ERP + nhóm HĐ HRM (Q7) | kho — khớp; HĐ chi phí phải có thật + cùng cty | ERP đọc `->link` của `App\Model\Hrm\HrmContract` được, nhưng file model ERP đang **untracked** | Phase 1 — controller quyết commit file ERP |
| 20 SX HĐ | HĐ HRM*, Kho xuất* (trừ xuất thẳng), Cần lắp đặt, Vận chuyển* — khớp spec | Dòng con: SL cần·Đã xuất·**Còn lại**·**Tồn kho**·SL xuất — khớp spec | `HrmContractSearchModal` (V2BaseModal, lọc can_export, phân trang) — khớp | can_export, SL ≤ còn lại, kho — khớp; lập được ĐNXK / dữ liệu PXH (DownstreamTest) | Phía ERP: L3 | Phase 1 (ERP hiển thị — controller quyết) |
| 21 Bán HĐ | như 20 | Dòng cha + cột giá/VAT — khớp spec | như 20 | như 20 | Phía ERP: L3 | như 20 |

Lệch chung (mọi loại có kho):
- **L2** Danh sách Kho xuất/Kho nhập: ERP `Warehouse::getByCompany()` = kho có `accounting_warehouses` của **công ty
  người lập**, mọi `type` (BE chặn type 99). HRM `createData` = mọi kho `type IN (1,3)`, `status=1` của **mọi công ty**
  → user thấy và chọn được kho công ty khác. Ngoài phạm vi spec §5, sửa đụng nghiệp vụ đa công ty → controller quyết.
- **L3** ERP đọc phiếu 20/21 do HRM tạo: không crash (`ALL_EXPORT_TYPES` có 20/21/99); nhưng cột "Số hợp đồng" ở danh
  sách ERP trống, chi tiết ERP không hiện HĐ HRM; `emplement_contract()` ERP là belongsTo FirmContract cho mọi
  type ≠ 3 → với 20/21 có thể nạp nhầm HĐ hãng trùng id; màn create/edit ERP dùng `EXPORT_TYPES` không có 20/21
  (mở sửa nháp HRM trên ERP thì ô Loại trống). Không sửa ERP.
- **L6** BE HRM không chặn trùng (SP, ĐVT) như ERP `validateProducts` ("Có hàng hóa bị trùng lặp"); FE đã chặn thêm
  trùng SP khi chọn từ popup → chỉ lọt khi gọi API thẳng. Minor.
- Cố ý khác ERP (không phải lệch): nháp chỉ cần Loại (ERP đòi ≥1 dòng SL > 0 — `can_submit`), Q4/Q10.
