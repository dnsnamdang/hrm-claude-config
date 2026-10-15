# Xuất bán hàng mượn — port ERP → HRM (nhánh gop_db)

> Placeholder — sẽ fill sau brainstorming. Người phụ trách: @namdangit

## Mục tiêu
Chuyển toàn bộ luồng "xuất bán hàng mượn" từ ERP sang HRM (Module Finance), cho **cả 3 loại hợp đồng**:
FirmContract (HĐ hãng), WrServiceContract (HĐ dịch vụ), và "HĐ mới" (Firm có `hrm_quotation_id` — đi chung nhánh Firm).

## Bối cảnh luồng (4 bước, 2 chứng từ, chỉ bước 1 đụng kho)
1. **Phiếu YC xuất hàng loại "Xuất mượn"** (`ProductExportRequest` type 3, `borrow_status=DA_MUON`) — QUA KHO, hàng rời kho cho khách mượn. (đã có nguồn bên HRM/DB gộp)
2. **Phiếu YC xuất bán hàng mượn** (`BorrowSellRequest`, mã `PYCXBHM`) — KHÔNG qua kho, chỉ yêu cầu + duyệt. ← **Phase 1**
3. **Phiếu xuất bán hàng mượn thực tế** (`BorrowSell`) — KHÔNG qua kho, **sinh hạch toán bán** (5111/5211/5213, 33311, giá vốn 632/1561, công nợ 1311). ← **Phase 2**
4. Hàng mượn không mua → **Nhập bán mượn trả lại** (type 9) — đã port bên HRM.

## Phân phase
- **Phase 1** (đợt này): Phiếu YC xuất bán hàng mượn — list + tạo + chi tiết + in + luồng duyệt (kế toán kho / vượt hạn mức TP→BGD) + từ chối. KHÔNG hạch toán, KHÔNG tồn.
- **Phase 2** (sau): Phiếu xuất bán hàng mượn thực tế + hạch toán bán trên DB gộp.

## Quyết định lớn
_TBD sau brainstorming (phân quyền theo cấp, cách đọc nguồn xuất mượn từ DB gộp, phạm vi duyệt Phase 1)._

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-28-xuat-ban-hang-muon-phase1-design.md`

---

## Phase 3 — Hỗ trợ HĐ HRM `hrm_contracts` (2026-09-07)

⚠️ **Phân biệt "HĐ mới"**: dòng 7 phía trên ("HĐ mới = Firm có `hrm_quotation_id`, đi chung nhánh Firm")
là khái niệm CŨ/KHÁC — HĐ đó vẫn nằm trong bảng `firm_contracts`. Phase 3 nói về **HĐ HRM thật**:
bảng riêng `hrm_contracts`, model `Modules\Assign\Entities\Contract\Contract` (module Assign),
SP ở `hrm_contract_product_prices` — là **nhánh contractable_type thứ 3 hoàn toàn mới**.

**Mục tiêu**: cho borrow-sell (Phase 1 + Phase 2) nhận thêm loại HĐ thứ 3 = HĐ HRM "giao việc",
**port đối xứng nhánh Firm** (hành vi + bút toán giống HĐ hãng; nguồn TK = support_accounting của HĐ HRM).

**Phát hiện then chốt**: phiếu xuất mượn (type 3) contract-agnostic → **phía xuất mượn không đụng gì**;
toàn bộ thay đổi nằm ở borrow-sell.

**3 quyết định (user chốt 2026-09-07)**:
- Q1: port 1:1 nhánh Firm; bút toán giống firm.
- Q2 (**Cách A**): thêm cột `exported_qty` + `returned_qty` vào `hrm_contract_product_prices` (đối xứng firm).
- Q3 (**Cách 1**): nhóm `hrm_contract_groups` = đợt; Phase 1 cho chọn nhóm, khớp trong nhóm đã chọn.

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-xuat-ban-hang-muon-phase3-hrm-contract-design.md`
