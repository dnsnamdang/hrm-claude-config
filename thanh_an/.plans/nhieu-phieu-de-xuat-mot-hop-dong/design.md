# Lập nhiều phiếu đề xuất cung ứng cho 1 hợp đồng — Tóm tắt

- **Người phụ trách**: @khoipv
- **Ngày**: 15/09/2026 · **Cập nhật**: 16/09/2026 (đổi luật hiển thị HĐ đã đề xuất đủ — §11 spec)
- **Spec đầy đủ**: [docs/superpowers/specs/2026-09-15-nhieu-phieu-de-xuat-mot-hop-dong-design.md](../../docs/superpowers/specs/2026-09-15-nhieu-phieu-de-xuat-mot-hop-dong-design.md)

## Mục tiêu

Bỏ ràng buộc **1 hợp đồng ↔ 1 phiếu đề xuất cung ứng**. Hợp đồng chưa đề xuất hết số lượng thì
vẫn còn trong màn "Hợp đồng đã kết xuất" và lập tiếp được phiếu mới.

## Vấn đề gốc

Ràng buộc 1-1 chỉ nằm ở 2 chỗ: `SupplyProposalService::assertContractAvailable()` và
`whereNotExists` trong `RenderedContractService::getList()`.

Nhưng **gỡ 2 chỗ đó là chưa đủ**: `sl_con_lai_hd = qty − exported_qty`, mà `exported_qty` là
SL đã **xuất kho**, không phải SL đã **đề xuất**. Không làm gì thêm thì phiếu thứ 2 sẽ prefill
nguyên số lượng cả hợp đồng.

## Các quyết định lớn

| Quyết định | Chốt |
|---|---|
| SL đã đề xuất tính từ đâu | Mọi phiếu chưa xóa mềm, **trừ phiếu chết** (status 7 BGĐ không duyệt, 8 Từ chối xử lý) |
| Lọc theo cột nào | `supply_proposal_products.contract_id` (không dùng `supply_proposals.contract_id` — 1 phiếu có thể chứa hàng nhiều HĐ) |
| Đề xuất vượt SL | **Cho vượt, không chặn, không cảnh báo** |
| Khi nào HĐ coi là "đề xuất đủ" | Khi **mọi dòng hàng** đã đủ (`sl_con_de_xuat <= 0.0005`) |
| HĐ đề xuất đủ thì sao | **16/09/2026**: vẫn ở lại danh sách với badge *Hoàn thành*, chỉ **mất nút lập phiếu** (bản 15/09 là ẩn hẳn khỏi danh sách) |
| Màn lập phiếu | **Không đổi giao diện.** Chỉ khác: prefill điền SL còn được đề xuất, bỏ dòng đã đủ |
| Màn HĐ đã kết xuất | Thêm cột **Tiến độ** và cột **Phiếu đề xuất** (liệt kê mã phiếu bấm được). **16/09/2026**: cột Tiến độ bỏ `x/y (z%)`, đổi sang badge **Chưa lập đề xuất** / **Đang lập đề xuất** / **Hoàn thành**, số liệu đẩy vào tooltip |
| Phiếu không còn hiệu lực (16/09/2026) | **Không hiển thị** ở cột Phiếu đề xuất; HĐ chỉ còn phiếu chết ⇒ badge về *Chưa lập đề xuất* |
| Layout bảng (16/09/2026) | Cột Khách hàng rộng 300px, bật cuộn ngang, cố định 3 cột STT / Mã HĐ / Số HĐ |
| Cách lọc HĐ đã đủ | **Cách A — lọc bằng PHP**, không migration, không cột cờ (xem §7 spec) |
| Thiếu hệ số ĐVT | Coi như chưa đề xuất gì ⇒ HĐ vẫn lập được phiếu — **thà thừa còn hơn chặn nhầm** |
| Migration | **Không.** `supply_proposal_products` đã có `contract_id`, `unit_id`, `quantity` |

## Công thức mới

```
sl_da_de_xuat  = Σ quantity (phiếu sống, status NOT IN (7,8)) theo [contract_id][product_id]
sl_con_de_xuat = max(sl_con_lai_hd − sl_da_de_xuat, 0)
```

Quy đổi ĐVT theo `unitConversionMap()`, phân bổ waterfall khi 1 mã hàng có nhiều dòng HĐ.

## Lưu ý đã nêu với user

Tổng SL của một HĐ là phép cộng giữa nhiều ĐVT khác nhau (Hộp + Lọ + Cái…) nên con số `120/150`
**không có ý nghĩa vật lý**, chỉ là chỉ báo tiến độ tương đối → từ 16/09/2026 con số này nằm trong
**tooltip** kèm chú thích, bảng chỉ hiện badge trạng thái. Luật "đề xuất đủ" thì tính **theo từng
dòng hàng**, chính xác.

## Tác dụng phụ tích cực

Feature trước (bỏ phân công NV cung ứng) sinh rủi ro: A lập phiếu → HĐ biến mất, B không thấy và
không xóa được phiếu của A. Nay phiếu chết (7/8) không tính vào SL đã đề xuất ⇒ **HĐ tự lập được
phiếu trở lại**; và từ 16/09/2026 HĐ không bao giờ biến mất khỏi danh sách nữa, phiếu chết cũng
không còn hiển thị (HĐ trở về đúng trạng thái *Chưa lập đề xuất* như chưa từng có phiếu).
