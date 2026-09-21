# Design (tóm tắt) — Báo cáo nhu cầu mua: trừ SL đã mua theo dòng

**Spec đầy đủ:** `docs/superpowers/specs/2026-09-19-bc-nhu-cau-mua-tru-sl-da-mua-design.md`

## Vấn đề
Màn `supply/reports/purchase-demand` lấy nhu cầu từ `supply_handling_products.alloc_mua`
(phiếu xử lý đã duyệt) và **không bao giờ trừ đi** khi đã lập HĐ mua / đơn mua:
- Đơn mua không ảnh hưởng gì tới báo cáo.
- HĐ mua chỉ gắn thêm cột hiển thị; "SL còn lại HĐ mua" = Σ SL đã ký, không bao giờ giảm.
- Filter "Chỉ mã chưa có HĐ mua" là **boolean theo mã**: mua 1 cái trên nhu cầu 100 cái
  cũng làm mã đó biến mất khỏi danh sách lập HĐ.
- Popup chọn hàng dùng lại chính báo cáo nên lần nào cũng nạp full nhu cầu gốc → dễ mua trùng.

## Giải pháp
Thêm **liên kết cấp dòng** giữa dòng nhu cầu (`supply_handling_products`) và dòng chứng từ mua
qua bảng nối mới `purchase_demand_allocations`.

> Không dùng cột đơn `supply_handling_product_id` trên `purchase_contract_products` vì
> **1 dòng hàng của HĐ mua gộp nhiều dòng nhu cầu** (mảng `purposes[]`) — quan hệ là n-n.

Công thức:
```
Còn cần mua (dòng) = alloc_mua − Σ allocation của chứng từ ĐÃ DUYỆT
Đang chờ duyệt     = Σ allocation của chứng từ Nháp / Chờ duyệt   (KHÔNG trừ, chỉ cảnh báo)
```

## Quyết định lớn
| # | Quyết định |
|---|---|
| 1 | Bảng nối `purchase_demand_allocations`, chỉ index, không khóa ngoại |
| 2 | Chỉ status = 3 (Đã duyệt) mới trừ; 1/2 hiện badge cam "chờ duyệt" |
| 3 | Tính **cả HĐ mua (doc_type 1) và Đơn mua (doc_type 2)** |
| 4 | SL cấp phát lưu theo **ĐVT cơ bản** (`qty_base`) để miễn nhiễm với đổi ĐVT trên chứng từ |
| 5 | Nguồn SL cấp phát = `purposes[].buyQty` (SL người dùng thực sự nhập), không phải `order_qty` cấp dòng |
| 6 | Dòng đã mua đủ: **mặc định ẩn**, có checkbox "Hiện cả dòng đã mua đủ" để tra cứu lại |
| 7 | Dữ liệu cũ backfill best-effort từ JSON `purposes` (map qua handling_id / proposal_id + product_id) |
| 8 | Thiếu hệ số quy đổi ĐVT → **không trừ**, gắn cờ cảnh báo (thà hiện thừa còn hơn ẩn nhầm) |

## Phạm vi không đụng tới
- Không sửa `SupplyProposalService::unitConversionMap()` (hàm dùng chung) — chỉ gọi lại.
- Không đổi luồng duyệt HĐ mua / đơn mua.
- Không đụng cột "SL còn lại HĐ mua" hiện có (giữ nguyên, vẫn chờ module nhập hàng).

## Kết quả (19/09/2026)
Code xong BE + FE, migration đã chạy trên `thanhan_stag_07052026`
(backfill ghi 14 dòng / bỏ qua 0). Báo cáo trừ đúng: 24 dòng nhu cầu → còn **20 dòng cần mua**,
`tong_sl_con_can_mua` 4115 → 1600. Đơn mua Đã duyệt trừ thật, Nháp / Chờ duyệt chỉ hiện nhãn cam.

Phát sinh ngoài thiết kế ban đầu:
- Line payload của báo cáo vốn **không** có `handling_product_id` → đã bổ sung, nếu không FE
  không có khóa để gửi ngược lại khi lập chứng từ.
- Chứng từ cũ có `purchase_*_products.unit_id` NULL: đối chiếu dữ liệu thật thấy `purposes[].qty`
  của các phiếu này ghi theo **ĐVT của chính dòng nhu cầu** → nhận nguyên, không quy đổi.
- Checkbox "Chỉ mã chưa có HĐ mua" **bị bỏ** (tiêu chí đúng bây giờ là "còn cần mua > 0" do BE lọc),
  đổi thành "Chọn mã để lập HĐ / đơn mua".

**Còn lại:** user click-through trên UI · chạy 2 migration trên môi trường thật · build lại client.

## ĐÃ ROLLBACK (19/09/2026)
User yêu cầu back code lại ngay sau khi hoàn thành. Toàn bộ thay đổi đã được gỡ:
migration đã `rollback` (bảng `purchase_demand_allocations` không còn), file mới đã xóa,
các file BE/FE sửa đã trả về bản HEAD (gỡ thủ công ở những file còn thay đổi khác chưa commit).

**Tài liệu này + spec chi tiết giữ nguyên** làm bản thiết kế tham chiếu nếu sau này làm lại.
Hiện trạng thực tế của màn `supply/reports/purchase-demand`: quay lại như mô tả ở mục "Vấn đề" —
**không trừ SL đã mua**.
