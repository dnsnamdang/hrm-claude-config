# #10238 — [App Chấm công] Duyệt gia hạn/kết thúc phiếu công tác: lỗi truy cập menu, lỗi/thiếu bộ lọc — @cuong61n

Kiểm 19/10/2026 trên simulator (admin, flavor tpeLocal):
- [x] (1) Menu "Phê duyệt" + "Duyệt gia hạn/Kết thúc công tác" không hiện ngay khi vào Chấm công — ĐÃ SỬA từ trước: đăng xuất → đăng nhập → chọn Chấm công → mở menu lần đầu đã có cả 2 ✓
- [x] (2) Phê duyệt → Gia hạn, kết thúc sớm: ô Người tạo đã là SelectInput có "Tìm kiếm" (gõ "Trần Văn T" lọc đúng) ✓. Lọc sai người: nguyên nhân cũ là app gửi employees.id trong khi BE (`ExtendEndSoonRequestCriteria`) đọc created_by là employee_info_id (Tú emp 378 = info của Tráng). Code hiện gửi `filterUser.employeeInfoId` → chọn Trần Văn Tú gửi created_by=360 → toàn phiếu của Tú (API: Tú 42, Tráng 14, khớp DB) ✓
- [x] (3) Giao việc-công tác → Duyệt gia hạn/kết thúc: đã có bộ lọc Tên nhân viên + đủ ô như web (kiểm ở #10251, thêm Người cập nhật)
- [x] Phát hiện thêm cùng màn: "Mã phiếu công tác" trống ở mọi phiếu — cột `extend_end_soon_requests.assign_business_code` rỗng ~97% (local 1648/1692, prod 1792/1844). Sửa BE `ExtendEndSoonRequestTransformer`: rỗng thì lấy mã qua quan hệ phiếu công tác (giống bản xuất Excel). App hiện PCT-13310… ✓
