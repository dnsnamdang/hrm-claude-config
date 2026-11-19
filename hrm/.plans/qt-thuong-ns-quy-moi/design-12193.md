# #12193 — Chi tiết quyết toán thưởng NS quý: hiện dung lượng tệp đính kèm

## Vấn đề
Mục "Tệp đính kèm" ở màn chi tiết/sửa quyết toán thưởng NS quý để trống cột Dung lượng.
Cột `attachments` của phiếu chỉ lưu URL (S3), không lưu byte → FE không có số để hiện.

## Cách sửa (copy pattern Quyết toán thưởng NĂM)
- BE `BillProductivitySettlementQuarterController::attachmentSizes($id)` — route
  `GET finance/bill-productivity-settlement-quarters/{id}/attachment-sizes`, kiểm `canView()` (403 nếu không),
  trả map `{url: byte}` qua `PositionInventoryResultAttachmentService::sizes()` (HEAD lên S3).
- FE `SettlementQuarterForm.vue`: truyền `:sizes-url` cho `V2BaseAttachmentSection` (component tự gọi + hiện cột Dung lượng).
  Phiếu tạo mới (chưa có id) → rỗng, không gọi.

## Kiểm
- curl API trả đúng 69,618 byte cho tệp S3 test; FE cột Dung lượng hiện `68 KB`.
- Dữ liệu test gắn tạm vào phiếu local id 19 đã trả về NULL.
