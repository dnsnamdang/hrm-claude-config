# Design (tóm tắt) — Demo "Tạo đơn giao hàng từ HĐ mua"

> Người phụ trách: @khoipv · 06/10/2026
> Spec đầy đủ: `docs/superpowers/specs/2026-10-06-demo-don-giao-hang-design.md`
> Demo: `demos/demo-tao-don-giao-hang.html`

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

## Câu hỏi mở
Hóa đơn khi giao công ty khác Bên A · trả trước một phần · gối đầu đếm theo HĐ hay NCC · áp dụng cho Đơn mua hàng.
