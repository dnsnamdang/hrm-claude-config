# 1 phiếu đề xuất chỉ bám 1 hợp đồng — DESIGN (tóm tắt)

**Người phụ trách:** @khoipv · **Ngày:** 23/09/2026
**Spec đầy đủ:** `docs/superpowers/specs/2026-09-23-de-xuat-cung-ung-mot-hop-dong-design.md`

## Mục tiêu
Với các loại đề xuất bám hợp đồng bán (1, 4, 5, 6), mỗi phiếu chỉ được lấy hàng của **đúng 1 hợp
đồng**. Hàng ngoài hợp đồng vẫn chọn tự do.

## Quyết định lớn
1. Khóa mềm theo hàng đã chọn, không thêm ô "Hợp đồng" trên form.
2. HĐ khóa = HĐ của dòng hàng trong HĐ đầu tiên của phiếu; nếu phiếu prefill từ màn Kết xuất hợp
   đồng thì lấy luôn HĐ nguồn. Xóa hết hàng trong HĐ → mở lại.
3. Trong 1 lần mở popup cũng khóa: tick dòng HĐ A trước thì dòng HĐ B mờ ngay.
4. `supply_proposals.contract_id` (cấp phiếu) tự suy từ hàng đã chọn lúc lưu — trước đây chỉ có giá
   trị khi phiếu đi từ màn Kết xuất hợp đồng.
5. BE chặn lần cuối ở `store()`/`update()` để phiếu gửi từ API khác vẫn không lách được.

## Rủi ro / nợ
- `add.vue::isFromContract` đang tính theo `formSubmit.contract_id` → KHÔNG được auto-set field này
  ở FE (sẽ khóa nhầm ô Loại đề xuất / Khách hàng); chỉ suy khi build payload.
