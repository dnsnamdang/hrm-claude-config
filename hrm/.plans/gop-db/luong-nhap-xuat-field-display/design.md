# Luồng nhập/xuất — chuẩn hóa hiển thị trường (field display) — Design (tóm tắt)

> Nhánh: `gop_db` (hrm-client; hrm-api chỉ khi cần cờ/field hỗ trợ) · Tạo: 2026-10-12 · @namdangit
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-12-luong-nhap-xuat-field-display-design.md`
> Liên quan (không trùng): `dong-bo-form-xuat-nhap` (đồng bộ LAYOUT card). Feature này lo HÀNH VI TRƯỜNG.

## Mục tiêu

Rà soát toàn bộ **8 màn luồng nhập/xuất** (Tạo / Sửa / Xem chi tiết) và chuẩn hóa 3 điểm hiển thị:

- **(a) "Xuất thẳng" luôn là checkbox** ở cả 3 chế độ (tạo, sửa, xem chi tiết). Hiện tại chi tiết
  đang hiện dạng ô text "Có/Không" → đổi về checkbox tick (readonly ở chế độ xem). CHỈ trường
  "Xuất thẳng"; KHÔNG đụng "Cần lắp đặt".
- **(b) Màn chi tiết: bỏ trường "Trạng thái" trong khối THÔNG TIN CHUNG** vì header đã có badge
  trạng thái (`buildStatusTitle`). Áp cho cả 8 màn.
- **(c) Ẩn trường theo loại phiếu**: ẩn một trường KHI VÀ CHỈ KHI nó **(không liên quan tới loại
  phiếu hiện tại theo ERP gốc) VÀ (rỗng)**. Còn lại thì hiện: liên-quan-mà-rỗng → hiện;
  không-liên-quan-mà-có-dữ-liệu → hiện. Áp cho cả 3 chế độ.

## 8 màn ↔ loại phiếu

| Màn HRM | Viết tắt |
| --- | --- |
| `finance/product-export-requests` | YCXH |
| `finance/warehouse-export-requests` | ĐNXK |
| `finance/product-exports` | PXH |
| `finance/product-import-requests` | YCNH |
| `finance/warehouse-import-requests` | ĐNNK |
| `finance/product-imports` | PNK |
| `finance/borrow-sell-requests` | YCXBHM |
| `finance/borrow-sells` | PXBHM |

## Quyết định đã chốt (brainstorming)

1. **Phạm vi**: cả 8 màn (không chỉ YCXH).
2. **Nguồn "liên quan"**: bám đúng ERP gốc — một trường liên quan tới một loại ⟺ ERP hiện trường đó
   cho loại đó.
3. **3 chế độ**: áp (c) cho cả Tạo / Sửa / Xem chi tiết.
4. **Quy tắc ẩn**: chỉ ẩn khi *vừa không liên quan vừa rỗng* (`shouldShowField = isRelevant || !isEmpty`).
5. **Cách làm**: **Cách 2** — helper dùng chung tập trung (`utils/flow-field-visibility.js`) + ma trận
   `fieldRelevance` khai theo từng màn (field × loại phiếu), KHÔNG rải `v-if` tay, KHÔNG để BE quyết
   (vì tạo/sửa đổi loại realtime, chưa có bản ghi → BE không phải nguồn sự thật).

## Trạng thái

- [ ] Spec đầy đủ (gồm ma trận ERP 8 màn) — ĐANG VIẾT
- [ ] User review spec (gate)
- [ ] Plan (writing-plans) — CHƯA mở khóa (chờ duyệt spec)
- [ ] Implement — CHƯA (HARD-GATE brainstorming)
