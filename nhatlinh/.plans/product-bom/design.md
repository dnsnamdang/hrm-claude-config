# Quản lý BOM (định mức NVL) — Tóm tắt

**Ngày:** 2026-06-05 · @manhcuong · Spec: `docs/superpowers/specs/2026-06-05-product-bom-design.md` · MODULE 1 (DM-02)

## Scope
BOM riêng cho hàng SX (độc lập BomList của Assign). 1 sản phẩm nhiều BOM, 1 mặc định. Dòng NVL tham chiếu products. Có lịch sử (snapshot mỗi lần lưu). Mã `BOM.xxxx`. **Cấm xóa BOM đang mặc định.**

## Quyết định
- 3 bảng: boms, bom_items (NVL từ products + ĐVT + định mức + hao hụt%), bom_histories (snapshot json).
- is_default: set 1 → bỏ default các BOM khác cùng product.
- FE: list + modal xl (chọn sản phẩm + bảng NVL động + checkbox mặc định + lịch sử). Export (bỏ import đợt này).
- 2 permission. NVL = product bất kỳ.
