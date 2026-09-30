# Thêm 3 loại đề xuất cung ứng theo loại hợp đồng — DESIGN (tóm tắt)

**Người phụ trách:** @khoipv · **Ngày:** 22/09/2026
**Spec đầy đủ:** `docs/superpowers/specs/2026-09-22-de-xuat-cung-ung-theo-loai-hop-dong-design.md`

## Mục tiêu
Tách phiếu đề xuất cung ứng theo loại hợp đồng bán để popup chọn hàng chỉ hiện đúng hàng của
nhóm HĐ tương ứng.

## Scope
- CÓ: 3 loại đề xuất mới (4 đặt/mượn, 5 trao tặng, 6 nguyên tắc), thu hẹp loại 1 còn HĐ
  trong/ngoài thầu, luồng duyệt, popup chọn hàng, prefill từ màn Kết xuất hợp đồng.
- KHÔNG: phiếu xử lý (bộ cột phân bổ theo loại) — làm vòng sau.

## Quyết định lớn
1. Loại 1 "Cung ứng cho KH" chỉ còn HĐ trong thầu (1) + ngoài thầu (2).
2. Popup 3 loại mới = hàng trong HĐ đúng loại **+ toàn bộ danh mục** (giống loại 1).
3. 3 loại mới **phải BGĐ duyệt** → gửi ra trạng thái Chờ BGĐ duyệt; chỉ loại 1 gửi thẳng đi xử lý.
4. Ô Khách hàng của 3 loại mới = **toàn bộ KH đang hoạt động** (giống khách lẻ), không lọc theo HĐ.
5. Màn Kết xuất hợp đồng tự set loại đề xuất theo loại HĐ (BE trả `type` trong prefill).
6. Mapping đi qua helper `SupplyProposal::contractTypes()` vì id 2 bảng không trùng
   (đề xuất 5 ↔ HĐ 3 cho/tặng, đề xuất 6 ↔ HĐ 5 nguyên tắc).

## Rủi ro / nợ
- `SupplyHandling::COLS_BY_TYPE` chưa có bộ cột cho loại 3/4/5/6 → bảng phân bổ PXL trống.
- Stag chưa có HĐ đã duyệt loại đặt/mượn - trao tặng - nguyên tắc → cần tạo data để test tay.
