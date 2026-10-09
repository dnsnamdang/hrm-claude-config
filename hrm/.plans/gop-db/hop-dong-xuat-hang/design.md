# Xuất hàng HĐ trên HRM — Tóm tắt design

> @dnsnamdang · Module `Assign` + kho ERP (DB gộp) · Nhánh `hop-dong` (con `gop_db`)
> Spec đầy đủ: `docs/superpowers/specs/2026-08-14-hop-dong-xuat-hang-design.md`

## Mục tiêu
Dựng lại luồng **xuất hàng cho HĐ HRM** trên HRM (yêu cầu xuất hàng, đề nghị xuất kho, phiếu xuất hàng), phiếu xuất kho vẫn làm bên ERP. Thêm loại **"xuất sản xuất theo hợp đồng"** để xử lý hàng cha–con: khi hàng cha thiếu tồn thì xuất hàng con (sản xuất) → tự sinh phiếu nhập hàng cha → rồi xuất bán cha.

## Kiến trúc (chốt brainstorm 2026-08-14)
- **Hướng A:** HRM ghi thẳng vào bảng kho ERP (DB gộp), gắn HĐ HRM qua **polymorphic `emplement_contract_id/code/type`** (các bảng request/export ĐÃ có sẵn cột này).
- **2 loại xuất MỚI** (khai trong `ExportModel`, gắn `emplement_contract_type = Modules\Assign\Entities\Contract\Contract`):
  - `XUAT_SAN_XUAT_HOP_DONG = 20` — hàng CON (sản xuất theo HĐ).
  - `XUAT_BAN_HOP_DONG = 21` — hàng CHA (xuất bán HĐ HRM). *(KHÔNG dùng `XUAT_BAN_HD_HANG=14` vì loại 14 gắn `firm_contracts` ERP.)*

## Chuỗi chứng từ (dùng chung mọi loại)
| Bước | Chứng từ | Bảng | Làm ở |
|---|---|---|---|
| 1 | Yêu cầu xuất hàng | `product_export_requests` | HRM |
| 2 | Đề nghị xuất kho | `warehouse_export_requests` | HRM |
| 3 | Phiếu xuất kho | `warehouse_exports` | **ERP** |
| 4 | Phiếu xuất hàng | `product_exports` | HRM |

## Luồng nghiệp vụ (mỗi hàng CHA trên HĐ)
- **Cha đủ tồn** → chạy chuỗi **loại 21** (xuất bán cha thẳng).
- **Cha thiếu tồn** → chạy chuỗi **loại 20** cho hàng CON → **khi Phiếu xuất hàng (loại 20) XONG → HRM tự sinh Phiếu nhập cha** (`product_imports`, loại nhập thẳng, kho `NHAP_XUAT_THANG=2`) → user **tự làm** chuỗi loại 21 xuất bán cha.

## Gap cần xử lý
- `product_imports` CHƯA có `emplement_contract_*` → thêm cột (migration) để gắn phiếu nhập cha với HĐ HRM.
- `warehouse_exports` (ERP) link HĐ qua `warehouse_export_request_id` (không có emplement_contract riêng) — OK, chảy qua request.
- Xác nhận: hằng số "nhập thẳng" (`NHAP_THANG`?), bảng check tồn (accounting_stock / acc_warehouses).

## Phase
- **Phase 1:** Chuỗi xuất bán HĐ HRM (loại 21) đầy đủ 4 chứng từ trên HRM + duyệt + gắn HĐ.
- **Phase 2:** Loại 20 (xuất sản xuất) + rẽ nhánh tồn + auto-sinh phiếu nhập cha.

> Ghi chú: HDSD màn "Yêu cầu xuất hàng" được làm cho màn **ERP** (không phải HRM) — xem `ERP/.plans/`.
