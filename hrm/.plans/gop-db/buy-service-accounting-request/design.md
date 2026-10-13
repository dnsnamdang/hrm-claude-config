# Yêu cầu hạch toán mua dịch vụ — Design (tóm tắt)

> @khoipv · nhánh `develop` (con của `gop_db`) · tạo 2026-10-12
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-12-buy-service-accounting-request-design.md`

## Mục tiêu
Port màn ERP "Yêu cầu hạch toán mua dịch vụ" (`buyServiceAccountingRequest`, màn thứ 3 của chuỗi Mua dịch vụ) sang HRM
`/finance/buy-service-accounting-requests`, giống hệt ERP về nghiệp vụ, UI theo chuẩn HRM.

## Quyết định lớn (user chốt 12/10/2026)
- Cả 2 loại: 1 Công nợ bảo hiểm, 2 Dịch vụ thuê ngoài.
- Phân quyền 3 cấp như ERP + quyền "Hạch toán mua dịch vụ" — 4 quyền mới id 1699-1702, `type 23` (Bán hàng).
- Sửa/Xóa: status Đang tạo / Không duyệt + là người tạo; xóa cứng.
- Phân hệ chính Bán hàng (`?type=all`), lối phụ Tài chính, lối chờ duyệt `?type=for-approve` ở Bán hàng › Phê Duyệt.
- Màn HĐ mua DV + Hạch toán mua DV vẫn ở ERP: nút "Hạch toán" mở ERP; trạng thái 3/4 do ERP ghi ngược về chung DB.
- Không migration: dùng nguyên 3 bảng ERP; lịch sử qua `catalog_histories`.
- Khuôn: màn Yêu cầu mua dịch vụ (`Modules/Finance`, `pages/finance/buy-service-requests`).

## Hiện trạng dữ liệu
51 phiếu (toàn loại 2), 64 dòng chi tiết; bảng bảo hiểm rỗng; mẫu in 428/429 có sẵn.

## Lỗi ERP sửa khi port
Thiếu kiểm quyền server, không kiểm SL ≤ còn lại, chờ duyệt không lọc công ty, xóa sót detail_requests, link thông báo
sai, "Đang tạo" đỏ, `''` vào cột số, `summary` tin client. Chi tiết spec mục 8.

## Giới hạn
Ngày duyệt trống (ERP Hạch toán không gán `approved_time`); loại 1 không có dữ liệu thật để đối chiếu.
