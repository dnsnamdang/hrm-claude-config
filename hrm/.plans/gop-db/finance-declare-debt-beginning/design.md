# Design — Khai báo đầu kỳ công nợ (KH + NCC)

> Phụ trách: @junfoke · Tạo 2026-10-01 · nhánh `develop`
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-01-finance-declare-debt-beginning-design.md`

## Mục tiêu

Port 2 màn ERP `Kế toán > Khai báo đầu kỳ` sang phân hệ Tài chính, dùng chung bảng ERP
`declare_debt_beginning` / `declare_debt_supplier_beginnings` + ghi sổ `account_details` đúng định
dạng ERP (báo cáo công nợ ERP vẫn đọc). Chuyển hẳn sang HRM: entity ghi được, sửa luôn lỗi ERP.

## Phạm vi

- 2 màn theo khuôn 4 trang: danh sách · thêm (chọn đối tượng + bảng nhiều HĐ) · sửa · chi tiết
- Import Excel (giữ cột file mẫu ERP), Xuất Excel (chọn trường), In danh sách (mẫu ERP 466/468)
- Lịch sử thay đổi 2 nơi (popup ở danh sách + khối ở chi tiết) qua bộ dùng chung `catalog_histories`

## Quyết định đã chốt (user 2026-10-01)

| Vấn đề | Chốt |
|---|---|
| Nhánh | `develop` (đã chứa `gop_db`) |
| Lỗi ERP | Sửa luôn |
| Lịch sử | Có — bắt buộc theo quy tắc chung SRS mục 3 + skill entity-history |
| Entity | Chuyển hẳn HRM: `DeclareDebtBeginning` bỏ chỉ-đọc, thêm `DeclareDebtSupplierBeginning` |
| Sửa/Xoá | **Chặn khi đã phát sinh** chứng từ khác (cả 2 màn, chặn ở BE + ẩn nút) |
| Nguồn HĐ màn KH | **Port đủ 8 loại như ERP**, sửa các nhánh lọc lỗi |
| Danh sách tài khoản | **Giữ như ERP**: KH mọi TK lá đang hoạt động · NCC TK lá theo dõi công nợ |
| Kiểu cột `float` bảng NCC | **Không đổi DB** |
| "Đã phát sinh" tính chứng từ nào | **Chỉ chứng từ công nợ**: thu, chi, báo có, UNC, phiếu kế toán (+ phiếu gắn `billable` vào khai báo). Không tính phiếu xuất/nhập hàng (doanh thu trong kỳ) — nếu tính thì khai báo trên HĐ bán bị khoá ngay khi tạo. Hằng `DeclareDebtPostingService::DEBT_DOCUMENT_TYPES` |

Hệ quả dữ liệu thật (01/10): đã khoá 1.519/1.747 khai báo KH và 497/1.141 khai báo NCC (đã có phiếu thu /
phiếu kế toán trừ vào).

## Quyết định kỹ thuật

- Không thêm class vào `morphMap` dùng chung → bảng tra riêng `DeclareDebtContractRegistry`.
- Ghi tên class **ERP** vào `deptable_type` / `invoiceable_type` / `contractable_type`.
- Quyền: dùng lại tên quyền ERP + bản ghi guard `api` trùng tên (id 1591-1598). KH gate cả màn bằng
  `Quản lý công nợ đầu kỳ`; NCC xem tự do (phạm vi theo quyền), thêm/sửa/xoá theo 3 quyền ERP.
- Màn ERP dùng popup; HRM theo khuôn 4 trang (skill erp-to-hrm-screen) — sửa/chi tiết là 1 dòng.
- 2 màn dùng CHUNG lõi BE (`AbstractDeclareDebtService` / `AbstractDeclareDebtController`), lớp con chỉ
  khai phần khác (đối tượng, nguồn HĐ, tài khoản, ngoại tệ, quyền, cột in).
- Mã phiếu: MAX+1 theo tiền tố + khoá dòng cho cả form lẫn import (ERP KH có 2 cách sinh mã → trùng).
- Xuất Excel đi đường `export-rows` + FE dựng file (`DynamicExport` đổ ô số thành chuỗi, sai quy tắc).
- VNĐ (currency id 1) luôn có trong danh sách tiền tệ dù đang khoá (DB local để VNĐ "Khoá").
- Nhà cung cấp chọn được HĐ của NCC khác (giữ tab "NCC khác" của ERP); KH bắt buộc HĐ thuộc đúng KH.
