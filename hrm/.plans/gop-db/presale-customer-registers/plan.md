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

## Ngày 23/11/2026 (@junfoke) — phản hồi bổ sung (không có task Redmine)
- [x] 23/11/2026 — Khảo sát yêu cầu bổ sung từ bảng phản hồi chuyển đổi: đăng ký KH theo báo giá + dự án TKT; thời hạn mặc định theo cấu hình, sửa phải duyệt TP → BGĐ; In / Excel / lịch sử; cấu hình "Thông báo hết hạn đăng ký KH" ở tab Báo giá – Hợp đồng; gia hạn qua TP → BGĐ. ERP: đăng ký chỉ sinh từ báo giá, thời hạn 1 số chung (`configs.customer_register_expiry`, 30 ngày), không có sửa/gia hạn/duyệt/lịch sử/cron; bảng `customer_registers` local 2,143 dòng, 11 còn hạn. HRM: màn hiện chỉ xem; tab Báo giá – Hợp đồng đã có ô "Thời gian đăng ký KH"; dự án TKT có luồng gia hạn TP → BGĐ làm khuôn được.
- [x] 23/11/2026 — User chốt **Cách A** (ERP giữ nguyên logic): bảng chung `customer_registers` không đổi cấu trúc; đăng ký đúng thời hạn mặc định ghi thẳng bảng chung (như nút ERP); thời hạn khác mặc định / gia hạn tạo phiếu yêu cầu ở bảng riêng HRM, duyệt xong mới ghi sang bảng chung. Thông báo hết hạn: gửi **người đăng ký**, trước **3 ngày** (ô cấu hình mới cạnh "Thời gian đăng ký KH"), tác vụ hằng ngày gửi chuông + push, bấm mở đúng đăng ký có nút Gia hạn.
- [ ] Đang chờ user chốt phạm vi xem (đề xuất: theo quyền Xem PB / Công ty / Tổng công ty, không quyền chỉ thấy đăng ký của mình; 2 tab Đăng ký KH + Phiếu yêu cầu) → viết design rồi plan. Chưa code.
