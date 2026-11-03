# Biên bản bàn giao nghiệm thu (ERP → HRM) — @khoipv

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-11-03-bien-ban-ban-giao-nghiem-thu-design.md`

## Mục tiêu
Port màn ERP `handoverAcceptanceRecord.index` (Hồ sơ công việc › Biên bản bàn giao nghiệm thu `?type=all`,
Thông báo › BB bàn giao nghiệm thu theo NV `?type=for-business-staff`) sang HRM trọn bộ.

## Quyết định (user chốt 03/11/2026)
- Nguồn hợp đồng: **cả HĐ hãng (`firm_contracts`) lẫn HĐ HRM (`hrm_contracts`)**.
- Phân quyền theo cấp y ERP — 4 quyền mới type 4 (Giao việc), tên nguyên văn ERP (Tạo + 3 Xem theo cấp).
- Nghiệp vụ y ERP kể cả chỗ lạ (Lưu và duyệt không cần quyền duyệt, "Chờ duyệt" không có đường tạo); nháp đổi màu xám.
- Bộ bắt buộc HRM (Xuất Excel, Cấu hình cột, Lịch sử 2 nơi) + **In danh sách + In biên bản** (mẫu HRM tự dựng).

## Phạm vi code
- BE `Modules/CustomerCare`: entity `HandoverAcceptanceRecord` (+Product, +ProductSerial), service list/show/print/delete,
  service nguồn HĐ (popup + điền sẵn + SL theo HĐ 2 nguồn), service lưu + FormRequest, route
  `/v1/customer-care/handover-acceptance-records`, quyền seeder, registry xuất + lịch sử.
- FE `pages/assign/handover-acceptance-records/` (index, create, `_id/index`, `_id/edit`) + `HandoverAcceptanceRecordForm.vue`
  + bảng hàng + popup chọn HĐ; link 2 mục menu có sẵn.

## Rủi ro đã biết
- ERP đọc biên bản gắn HĐ HRM sẽ lỗi (class morph không có bên ERP) — chờ user quyết vá ERP.
- Luồng xuất kho HRM chưa ghi `exported_qty` về dòng HĐ HRM → biên bản HĐ HRM có hàng chưa "Lưu và duyệt" được.
