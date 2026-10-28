# Design (tóm tắt) — Demo "Tạo đơn giao hàng từ HĐ mua"

> Người phụ trách: @khoipv · 06/10/2026
> Spec đầy đủ: `docs/superpowers/specs/2026-10-06-demo-don-giao-hang-design.md`
> Demo: `demos/demo-lap-don-mua-hang.html`

## Mục tiêu
Demo HTML (V2Base) màn lập Đơn giao hàng (DGH) — bước sau HĐ mua trong luồng Cung ứng, để chốt nghiệp vụ trước khi build.

## Scope demo
- 4 tab: Thông tin chung · Hàng hóa · Giao nhận & vận chuyển · Điều khoản thanh toán (đã bỏ khung stepper Luồng xử lý + giả lập).
- 3 HĐ mẫu: Thương mại Roche (điều khoản TIME 30 / VALUE 500tr / gối đầu 2), Thương mại Hồng Anh (100% trước giao), Nguyên tắc Hồng Anh (nợ 45 ngày, nợ tối đa 300tr).

## Quyết định lớn
1. **1 HĐ → nhiều đơn giao**, mỗi đơn 1 công ty nhận (có thể ≠ Bên A). Chọn NCC xuất HĐ cho công ty nhận (mặc định) hoặc cho Bên A (→ điều chuyển nội bộ). Công nợ ghi cho công ty đứng tên HĐ.
2. **Chọn hàng theo `purposes[]`** của HĐ mua: 1 dòng popup = 1 mã × 1 phiếu ĐX/PXL (KH, HĐ bán, Cty bán, còn lại). Trên đơn gộp theo mã, nhập SL giao từng phiếu. **Chặn** vượt còn lại (HĐ TM); HĐ NT không giới hạn SL.
3. **3 phương thức giao** (4 tổ hợp): NCC → kho · NCC → KH (nhập-xuất thẳng) · Cty tự lấy → kho / → KH. Mặc định suy từ `delivery_method` HĐ. Về kho: 1 kho / đơn. **Giao thẳng KH: 1 đơn được nhiều KH** — tự nhóm hàng theo KH thành Điểm giao (địa chỉ / người nhận / SĐT / phí VC riêng); hàng nội bộ / ngoài phiếu bị chặn.
4. **Chi phí VC**: NCC chở & công ty chịu → cộng vào tổng thanh toán NCC; công ty tự lấy → **không có chi phí VC** (ẩn khối). Không phân bổ vào giá vốn.
5. **Thanh toán**: Trả trước → Đề nghị thanh toán → Kế toán chi → mới được giao. Công nợ: theo **N ngày** hoặc **gối đầu K đơn** (đã bỏ "kết hợp"); kiểm hạn mức giá trị; vi phạm → BGĐ duyệt vượt hoặc trả đơn nợ cũ nhất.
6. **HĐ mua không bắt buộc** (16/10/2026): không chọn HĐ = đơn mua lẻ — NCC chọn tay (bắt buộc); hàng lấy từ BC tổng hợp nhu cầu mua – tab **Cần đi mua** (1 dòng = 1 mã × 1 PXL, chặn vượt còn cần mua); đơn giá + VAT nhập tay; ẩn khối Thông tin HĐ, NCC chỉ xuất hóa đơn cho công ty nhận; thanh toán nhập tay, mặc định **Trả trước** (công nợ: theo ngày / gối đầu đếm đơn đang nợ của NCC). Chi tiết: spec mục 10.
7. **Bảng hàng hóa theo màn Đơn mua hàng dev** (`ProductsTab.vue`, 16/10/2026): 23 cột (đã bỏ Cty thực hiện mua — cty mua = Công ty nhận hàng), dòng con theo khách hàng → HĐ bán (rowspan); VAT theo danh mục; đơn lẻ nhập đơn giá + CK theo khách; bỏ đổi hàng / đổi ĐVT / bộ lọc. Chi tiết: spec mục 11.
8. **Tab Thông tin chung** (16/10/2026): khối **Thông tin đơn mua** (Mã · Người lập · Ngày lập · HĐ mua · Công ty mua) + khối **Thông tin nhà cung cấp** (Tên · Mã · MST · Người liên hệ · SĐT · Địa chỉ, tự điền). Bỏ Ngày giao dự kiến, Diễn giải, lựa chọn xuất hóa đơn cho Bên A — NCC luôn xuất HĐ, ghi công nợ cho Công ty mua. Bỏ luôn khối Thông tin hợp đồng mua (17/10). Chi tiết spec mục 12.
9. **Popup chọn hàng — hàng HĐ bán chưa đề xuất** (17/10/2026, đơn mua lẻ): theo `GoodsPickerModal.vue` dev — thêm bộ lọc Nguồn + Số HĐ bán, dòng "HĐ · chưa đề xuất" (SL mua tự nhập), cột HĐ bán; bảng hàng hiện nhãn "Chưa đề xuất". Chi tiết spec mục 13.
10. **Tab Điều khoản thanh toán** (17/10/2026): làm lại theo `PaymentTab.vue` dev — Theo đợt (đợt nhập 2 chiều %↔tiền, tổng = 100%) / Theo đơn (4 điều khoản, 100% trước giao loại trừ) + Ghi chú; có HĐ → nạp sẵn Theo đơn từ điều khoản HĐ. Bỏ trả trước/ĐNTT/công nợ gối đầu cũ. Spec mục 14.
11. **Popup chọn hàng theo HĐ mua — thêm hàng HĐ bán chưa đề xuất** (17/10/2026): nhóm cuối bảng gồm mã không có trong HĐ mua (SL + đơn giá/CK tự nhập). Cột Nguồn phân biệt "Trong HĐ mua" / "HĐ bán · chưa đề xuất". Thêm bộ lọc Nguồn, cột SL còn lại HĐ bán và dòng Tổng. Spec mục 15.

## Câu hỏi mở
Hóa đơn khi giao công ty khác Bên A · trả trước một phần · gối đầu đếm theo HĐ hay NCC · áp dụng cho Đơn mua hàng.
