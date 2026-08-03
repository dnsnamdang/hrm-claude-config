# Nhập tồn đầu cho kho (Opening Stock) — Tóm tắt

**Ngày:** 2026-07-06 · @manhcuong · Spec đầy đủ: `docs/superpowers/specs/2026-07-06-opening-stock-design.md`

## Mục tiêu
Khai báo tồn kho ban đầu khi triển khai hệ thống, bằng cách bổ sung **loại phiếu nhập mới** vào phiếu nhập kho hiện có (`Modules/Warehouse` + `pages/warehouse/receipt`). Ưu tiên làm TRƯỚC Phase 4 Kiểm kê.

**Trạng thái 2026-07-07: CODE HOÀN THÀNH 7/7 task + final review Ready to merge — chưa commit, chờ user test trình duyệt.**

## Quyết định lớn
- **`receipt_type = 5` "Nhập tồn đầu"** — tái dùng toàn bộ form/workflow/màn/permission phiếu nhập (1124-1126), KHÔNG màn riêng, KHÔNG migration, KHÔNG permission mới.
- **Đơn giá nhập tay** (không bắt buộc) như loại "Nhập khác" — ghi nhận giá vốn tham khảo.
- **Chặn cứng khi DUYỆT**: hàng đã có bất kỳ `stock_movements` nào trong kho → 422 kèm danh sách mã (`assertOpeningStock`, mirror `assertReturnRemaining`). Chặn trùng mã trong cùng phiếu.
- **Import Excel vào form** qua `V2BaseImportModal` 4 bước (skill import-excel): 2 route mới `GET receipts/import-template` + `POST receipts/import/validate` (validate BE: mã tồn tại, ĐVT thuộc product_units, SL > 0, trùng mã, hàng đã có movement → lỗi sớm). Bước Import chỉ đổ dòng hợp lệ vào bảng form, KHÔNG ghi DB. Import trùng mã với dòng đã có trên bảng → ghi đè **cả cặp SL+ĐVT** (+ giá/ghi chú) — SL trong file validate theo ĐVT trong file (quyết định final review 2026-07-07).
- Movement khi duyệt: **type 1 nhập** bình thường — thẻ kho/báo cáo/dashboard không sửa gì.
