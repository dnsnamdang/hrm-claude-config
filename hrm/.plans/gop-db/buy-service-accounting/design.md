# Hạch toán mua dịch vụ — Design (tóm tắt)

> @khoipv · nhánh `develop` (con của `gop_db`) · tạo 2026-10-12
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-12-buy-service-accounting-design.md`

## Mục tiêu
Port màn ERP "Hạch toán mua dịch vụ" (`buyServiceAccounting`, màn 4/4 chuỗi Mua dịch vụ) sang HRM
`/finance/buy-service-accountings`: lập phiếu từ Yêu cầu hạch toán Chờ duyệt, Lưu và duyệt = ghi sổ `account_details`.

## Quyết định lớn (user chốt 12/10/2026)
- Quyền xem 3 cấp (1703-1705, type 23); lập/sửa/xoá dùng quyền 1702 "Hạch toán mua dịch vụ".
- Sửa/Xoá: Đang tạo + người tạo (như ERP); xoá cứng, yêu cầu nguồn về Chờ duyệt.
- Bút toán giữ y ERP (loại 2 không ghi Mã phí / Vụ việc vào sổ).
- Nút "Hạch toán" ở màn Yêu cầu chuyển sang màn HRM này.
- Không migration; khuôn màn Yêu cầu hạch toán mua dịch vụ.

## Hiện trạng dữ liệu
48 phiếu (loại 2, Đã duyệt), 61 dòng, 149 bút toán; mẫu in 430/431 có sẵn.
