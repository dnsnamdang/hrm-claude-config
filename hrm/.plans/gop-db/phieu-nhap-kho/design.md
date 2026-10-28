# Phiếu nhập kho (ERP `warehouse_imports` → HRM) — Design (tóm tắt)

**Người phụ trách:** @junfoke — 2026-10-15

> Nhánh `gop_db` (cả 2 repo đang đứng `develop`, checkout từ `gop_db`) · Redmine #11693 "Chưa chuyển menu Phiếu nhập kho"
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-15-phieu-nhap-kho-design.md`
> Plan: `.plans/gop-db/phieu-nhap-kho/plan.md`

## Mục tiêu

Port màn **Phiếu nhập kho** (mã `PNK-NNNNN`) sang HRM để QA đi hết luồng nhập hàng trong HRM:
**Yêu cầu nhập hàng → Đề nghị nhập kho → Phiếu nhập kho → Phiếu nhập hàng**. Ba tầng kia đã ở HRM; riêng tầng
này menu (`finance.js:153`) và nút "Tạo phiếu nhập kho" ở màn Đề nghị nhập kho vẫn mở sang ERP.

Đây là chứng từ **thủ kho nhập hàng vật lý vào vị trí kho**: tạo từ ĐNNK → chia phiếu đi xếp hàng → nhập kho
(SL + vị trí thực, file, vận chuyển, bốc xếp) → Gửi = **ghi tồn kho** → Kế toán kho Không duyệt hoặc lập
Phiếu nhập hàng (HRM đã có) để hạch toán.

## Phạm vi đề xuất ban đầu (đã thay bằng mục "Đã chốt" — Q1 = port hết)

| Port đợt 1 (luồng chính) | Để lại ERP / đợt sau |
| --- | --- |
| Danh sách (lọc, phạm vi theo quyền, cấu hình cột) + Xuất Excel | In barcode lô hàng (deep-link ERP) |
| Tạo từ ĐNNK (popup chọn ĐNNK, vị trí dự kiến, vận chuyển, bốc xếp) | Tạo phiếu xuất lại / nhập lại (12 phiếu toàn hệ thống) |
| Phiếu đi xếp hàng (chia nhóm, người đi xếp, In mẫu 30) | Phiếu nhập kho chờ báo thừa thiếu + Phiếu báo hàng thừa thiếu (màn riêng) |
| Nhập kho / Sửa → Lưu / Gửi (ghi tồn) · Chi tiết · Không duyệt · Hủy | Luồng tự sinh nhập ghép (8) / nhập tách (10) phía ERP |
| In phiếu nhập kho (mẫu ERP id 46) · Lịch sử thay đổi | |
| Nối nút: ĐNNK → tạo PNK nội bộ; PNK → Tạo phiếu nhập hàng HRM; đổi menu | |

## Quyết định chính (đề xuất)

1. **Module Finance**, BE `/api/v1/finance/warehouse-imports`, FE `pages/finance/warehouse-imports/`. Dùng thẳng
   bảng ERP (0 bảng mới, 0 migration); giữ mã `PNK-` + `generateCode(5, id)` của ERP.
2. **Giữ đủ 2 bước** tạo → xếp hàng → nhập kho như ERP (ERP chặn nhập kho khi chưa xếp xong; phiếu tạo ở HRM phải
   mở tiếp được ở ERP và ngược lại). In phiếu xếp hàng tách khỏi thao tác lưu nhóm.
3. **Ghi tồn vật lý 8 bảng** (`stocks`, `stock_logs`, `stock_of_companies`, `stock_positions`, `stock_position_logs`,
   `stock_position_details`, `stock_position_of_companies`, `stock_position_detail_logs`) **y hệt ERP**
   `WarehouseImport::updateWarehouse()` — `objectable_type` ghi nguyên chuỗi class ERP. HRM **chưa từng** ghi các bảng
   này ⇒ tách service dùng chung `PhysicalStockWriter` (cần user OK — hàm dùng chung, Phiếu xuất kho sẽ dùng lại).
4. **Tạo PNK = duyệt ĐNNK** (ĐNNK → 1, YCNH → 4) như ERP — HRM hiện không có action duyệt ĐNNK riêng, đang dựa vào màn ERP này.
   Hủy PNK gọi lại hàm hủy ĐNNK có sẵn trong `WarehouseImportRequestService`.
5. **Quyền**: 3 quyền mới guard `api` "Xem phiếu nhập kho theo {tổng công ty|công ty|phòng ban}" cuối seeder;
   `Kế toán kho` + thủ kho kho phiếu gate trong Controller bằng trait 2 guard (không middleware `checkPermission`).
6. **Thông báo** qua chuông HRM (`EmployeeInfoService::sendNotification`, precedent D9), bỏ Redis bảng tin ERP.
7. Badge trạng thái theo SRS (nháp xám, chờ duyệt vàng, không duyệt/hủy đỏ, xong xanh) — khác màu đỏ của ERP.

## Trạng thái (cột ERP, giữ nguyên)

3 Đang tạo → 2 Chờ duyệt → 7 Đang hạch toán (lập phiếu nhập hàng) → 1 Đã hạch toán; nhánh 4 Không duyệt →
5 Đã xuất lại → 6 Đã nhập lại; 8 Đã hủy. Tiến trình `step`: 2 Đang đi xếp hàng · 3 Đang nhập kho / Hoàn thành nhập kho.

## Rủi ro lớn nhất

Ghi tồn kho vật lý dùng chung với ERP (sai 1 cột là lệch tồn mọi màn kho) → bắt buộc đối chiếu song song
1 phiếu ERP ↔ 1 phiếu HRM từng dòng 8 bảng trước khi bàn giao QA.

## Đã chốt (user, 2026-10-15)

- **Q1 = Port hết**: luồng chính F1–F10 + In barcode (F11) + Xuất lại / Nhập lại (F12/F13) ngay đợt 1.
  Vẫn để ERP: F14 Phiếu nhập kho chờ báo thừa thiếu, F15 Phiếu báo hàng thừa thiếu (màn riêng).
- **Q6** port luôn tab Vận chuyển + Bốc xếp · **Q12** OK tạo `PhysicalStockWriter` dùng chung.
- **Q8** không cần hỏi hạ tầng: dùng `App\Helper\CmcS3Helper::putFiles(..., 'warehouse_imports')` như Phiếu xuất kho
  (`Assign/ProductExportController:911`) → ERP đọc lại được.
- Q2, Q3, Q7, Q9, Q10, Q11, Q13: theo cột "Đề xuất" spec mục 10. Q4/Q5 bị Q1 thay (port thật, không deep-link).
