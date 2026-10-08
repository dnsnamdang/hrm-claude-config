# Báo cáo kết quả CSKH tiềm năng — update theo khuôn

## Đợt 1 — Thêm cấp Bộ phận ở phần III (07/10/2026)

Màn `potential-customer-care`. Phần IV "Theo khách hàng" đã có cấp Bộ phận; phần III "Theo phòng ban / Nhân viên" thì chưa,
và đang lấy phòng trên MEETING (người tạo) trong khi cấp NV là người chủ trì — lệch 30/187 nhu cầu.

User chốt: (1) phần III lấy Phòng ban + Bộ phận theo HỒ SƠ NGƯỜI CHỦ TRÌ; (2) ô lọc Phòng ban đầu báo cáo cũng theo hồ sơ chủ trì
(phân quyền giữ nguyên theo cột meeting).

Đã làm:
- BE `PotentialCustomerCareService::buildSections`: phần III + IV dùng chung `$hostOrgLevels` (hdept ▸ hpart [bỏ cấp nếu phòng
  không chia theo danh mục, "Không thuộc bộ phận" cuối] ▸ emp). Tiêu đề "Theo phòng ban / Bộ phận / Nhân viên". Lọc
  `department_id` = subquery employees ⨝ employee_infos theo host. describeFilters lấy tên `host_department_name`.
- FE: nhãn tiêu chí (index.vue), tooltip phần III/IV (CareTrackingTable), comment DemandListModal (popup phần III khoá `hdept…`
  dùng chung bộ cột / ô lọc với phần IV — không sửa logic).
- PHPUnit: +1 ca phần III trong `PotentialCustomerCareNoPartTest` (4/4 xanh). e2e API: đổi tiêu đề ca 6, +2 ca (cây + ô lọc). Chưa chạy.

MCP (năm 2026): tổng 181 nhu cầu / 107,630,675,520 không đổi; Ô tô 2: 34 → 4, xuất hiện PHÒNG CSKH 30 ▸ BP Bảo hành (đúng
30 nhu cầu lệch); Thương mại 90 ▸ 3 bộ phận; cha = tổng con mọi dòng; lọc phòng 47 chỉ còn đúng phòng đó; popup BP Bảo hành
30 nhu cầu, cột Phòng ban chủ trì / Bộ phận / KD chủ trì, ô lọc PB/BP ẩn.

Ghi lại, chưa sửa: popup mở từ phần I/II + khối tổng hợp vẫn có ô lọc / thống kê chéo "Phòng ban" theo cột MEETING (người tạo).

## Đợt 2 — Thống nhất CẢ báo cáo theo người chủ trì (07/10/2026)

User chốt: mọi chỗ "Phòng ban" của báo cáo theo HỒ SƠ NGƯỜI CHỦ TRÌ. Phân quyền xem vẫn xét `meetings.department_id` / `part_id`.

Đã làm:
- BE `attachOrganisation()`: `department_id/_name` của dòng GHI ĐÈ bằng `host_department_*` → ô lọc / cột / thống kê chéo / options
  "Phòng ban" của popup, bản in, Excel, panel meeting tự cùng nguồn. Bỏ query tên phòng theo người tạo.
- Excel danh sách: bỏ cột "Phòng ban" (người tạo) trùng; thứ tự Phòng ban chủ trì ▸ Bộ phận ▸ KD chủ trì. Bản in: Phòng ban ▸ Bộ phận ▸ KD chủ trì.
- FE `DemandListModal`: popup phần I/II/tổng hợp thêm ô lọc Bộ phận (`drill_host_part_id`, cha = ô Phòng ban; không có bộ phận
  nào thì ẩn ô) + cột Bộ phận; nhãn "Phòng" → "Phòng ban chủ trì".
- PHPUnit +1 (5/5). e2e: UI ca sắp xếp 6→7 cột + thứ tự ô lọc có `hpart`; API +1 ca. Chưa chạy.

MCP (năm 2026): 181/181 dòng popup department = host; thống kê chéo Phòng ban = cây phần III (TM 90 · CSKH 30 · … · Ô tô 2 4);
lọc Phòng 47 ▸ BP lốp = 57 (khớp cây); phòng 55 không chia → ô Bộ phận ẩn; bản in drill hdept:50 30 dòng đúng thứ tự cột;
Excel blade 17 th = 17 td.
