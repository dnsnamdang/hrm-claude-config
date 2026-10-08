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

## Đợt 3 — Ô lọc Bộ phận + số tiền đầy đủ + ô chọn cấp (user "làm đi" 08/10/2026)

Phạm vi: nhánh `gop_db`, hrm-api `PotentialCustomerCareService` · hrm-client `potential-customer-care/*`. Không migration/seeder/quyền.

- [x] BE: lọc `part_id` theo HỒ SƠ NGƯỜI CHỦ TRÌ (subquery employees ⨝ employee_infos, cùng khuôn ô Phòng ban); dòng mô tả bộ lọc
      (bản in / Excel) thêm "Bộ phận: X".
- [x] FE bộ lọc: bỏ `:disable_part` → ô Bộ phận sau Phòng ban (cascade); nhãn khối "Công ty / Phòng ban / Bộ phận / Nhân viên";
      đổi tiêu chí khác Tất cả/Phòng ban thì xoá cả `part_id`.
- [x] Số tiền đầy đủ chuẩn quốc tế: `format.js` bỏ `billion()` ("41,5 tỷ"), `money()` en-US, `percent()` "5.0%"; bảng
      "Giá trị dự kiến (VND)", khối tổng hợp, popup "Giá trị đầu tư dự kiến (VND)".
- [x] Nút "Ẩn/Hiện chi tiết" → ô chọn cấp `V2BaseSelect xs` trong tiêu đề cột (khuôn report-styles). Bung theo TÊN cấp
      (tiền tố drill_key: field/sector · market/ward · hdept/hpart/emp · customer/…), không theo độ sâu — phòng không chia bộ
      phận không lòi NV ra ở "Đến Bộ phận". Nhãn theo tiêu chí ("Chỉ Phòng ban / Đến Bộ phận / Tất cả cấp (đến Nhân viên)"),
      tiêu chí Tất cả thì "Chỉ cấp 1 … Tất cả cấp". Mặc định "Chỉ cấp 1" (giữ hành vi thu gọn cũ, giống ResultTrackingTable).
- [x] PHPUnit `PotentialCustomerCarePartFilterTest` 2/2 + `PotentialCustomerCareNoPartTest` 5/5.
- [x] e2e `potential-customer-care.spec.ts`: ca 2 viết lại cho ô chọn cấp (+ expectLevelSelectFits), ca 24/27 đổi sang
      selectLevel, ca ô Bộ phận đổi 0 → 1, ca 28 nhãn khối mới, ca 30 mới (lọc Bộ phận = số dòng bộ phận trên cây + định dạng
      tiền/%). Biên dịch được, CHƯA chạy.
- [x] MCP 1366 (năm 2026): bảng 107,630,675,520 / 5.0%; ô chọn cấp cao 26px cùng hàng nhãn, th 1 dòng; Chỉ cấp 1 → 104 dòng,
      Đến cấp 2 → hpart 4 (chỉ TM 3 + CSKH 1), emp 0; Tất cả cấp 435 dòng; lọc BP lốp (27) = 57 · BP Bảo hành (3) = 30 khớp
      cây; ô Bộ phận ra đúng 3 bộ phận của phòng 47; popup cột "(VND)" 10,000,000; khối tổng hợp không tràn.
- [x] Commit + push `gop_db` 08/10/2026 (user yêu cầu "commit và push toàn bộ") — hrm-api + hrm-client.
- [ ] User kiểm.
