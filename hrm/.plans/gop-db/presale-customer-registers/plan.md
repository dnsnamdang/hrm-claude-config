# Plan — Danh sách đăng ký khách hàng toàn công ty

> @junfoke · 2026-10-08 · nhánh `develop` · Design: `.plans/gop-db/presale-customer-registers/design.md`

- [x] BE service + controller + resource + route (gate quyền 1526) + cột xuất Excel
- [x] FE màn danh sách chuẩn (lọc, tìm nhanh, sắp xếp, cấu hình cột, Xuất Excel) + menu presale
- [x] Đối chiếu ERP `CustomerRegister::searchByFilter`: không lọc 2.071 dòng; tên KH 284; số báo giá 1.278; NV 65 → 333;
      NV 84 + hết hạn 36; + số báo giá 14 — khớp md5 (không lọc: cùng tập dòng, 1 cặp trùng giờ đổi chỗ vì HRM thêm `id`)
- [x] Không quyền → API 403. Playwright (quyền cấp tạm rồi gỡ): lọc Thời hạn, Người đăng ký, Số báo giá + Enter,
      tìm nhanh, Làm mới, sắp xếp, chuyển trang, Xuất Excel (đọc lại file 2.071 dòng)

## Checkpoint — 2026-10-08

- **Vừa hoàn thành:** cả màn, CHƯA commit (nhánh `develop`).
- **Bước tiếp theo:** admin gán quyền 1526 cho vai trò cần xem (hiện chưa vai trò nào có).
- **Blocked:** không.
