# Plan — Xử lý phản hồi QA 7 task PL8 (QLDA)

Nhánh `tpe`. Phụ trách: @cuong61n. Nguồn: Redmine #10789, #10791, #10804, #10814, #10818, #10840, #10841.
Cả 7 task đã chuyển trạng thái "Đang tiến hành" ngày 17/09/2026.

## #10789 — Phân quyền giảm giá  ✅ ĐÃ SỬA (commit 7d95d3c64)
- [x] Toast trùng khi lưu mà không có quyền: bỏ toast ở catch `save()`, để interceptor axios bắn (đối chứng: code cũ 2 toast → code mới 1 toast)
- [x] Khối "Giảm giá tổng đơn hàng" hiện với người không có quyền: ẩn hẳn; báo giá đã có khoản GG thì vẫn hiện chỉ-đọc (0 ô nhập, 0 nút)

## #10841 — Hủy yêu cầu làm giải pháp  ✅ KHÔNG PHẢI SỬA (đã đạt, chỉ cần nghiệm thu lại)
- [x] Người khác bấm hủy → API trả 403 "Chỉ người tạo yêu cầu mới được hủy" (kiểm thật trên local)
- [x] Người tạo hủy → 200, `request_solution_history` ghi `note` = lý do hủy, UI `SystemInfoSection` có hiển thị `log.note`
- [x] FE ẩn nút Hủy theo cờ BE `is_can_cancel` ở cả danh sách, màn chờ tiếp nhận và màn chi tiết

## #10804 — Bảng giá ERP  ✅ ĐÃ SỬA (4/4)
- [x] "Bảng giá thiếu x clear": màn Tạo mới ĐÃ có nút × (kiểm thật); màn Sửa khoá ô theo thiết kế
- [x] Thanh tổng hợp `.pricing-footer` đè menu trái: `left: 0` + `padding-left: 80px` → `left: 220px`
      (+ rule `body[data-sidebar-size='condensed'] → 58px`), theo khuôn `components/TrainingFooter.vue`
- [x] Báo giá dự án con không kế thừa bảng giá: thêm `resolveChildProjectPriceTypeId()` — ưu tiên
      `prospective_projects.price_type_id`, không có thì lấy theo BÁO GIÁ MỚI NHẤT của dự án cha, cuối cùng mới về 1
- [x] Cỡ chữ bảng Chi tiết sản phẩm không đồng đều (12px / 10.24px / 13px) → ép mọi ô nhập về 12px
- [x] Test `test_10804.php` 8/8 PASS (đối chứng code cũ: FAIL đúng ca QA); đo lại trên UI: footer `left=220` trùng mép sidebar, cả dòng còn duy nhất cỡ chữ 12px

## #10814 — Thông tin hệ thống / Lịch sử  ✅ ĐÃ SỬA
- [x] Lịch sử ở BOM / Hạng mục / Báo giá / Task: kiểm code + UI + bản build trên dev → **đã có đủ**
      (`SystemInfoSection` nhúng từ 06/08, BE hỗ trợ 9 entity type, bản build dev 17/09 có `system-logs`).
      QA phản hồi 11/09, khi đó dev nhiều khả năng chưa build lại.
- [x] Đồng bộ action danh sách ↔ chi tiết:
      · Meeting: thiếu **In biên bản** → thêm (bật cờ `print` + mang cụm 2 bước cấu hình/xem trước sang màn chi tiết)
      · BOM: thiếu **Sửa / Sao chép / Xóa** → thêm, kèm `created_by` vào sự kiện `bom-loaded` để tính đúng điều kiện
      · Dự án: thiếu **Tạo giải pháp / Tạo yêu cầu làm giải pháp** → thêm; BE trả thêm 2 cờ
        `is_can_create_request_solution`, `is_form_complete` ở `DetailProspectiveProjectResource`
      · Giải pháp: thiếu **Giao cho Leader / Lưu và duyệt** → thêm theo đúng điều kiện của danh sách
      · YCGP: `menu` chưa hề khai → V2Footer chỉ có "Quay lại"; thêm **Sửa / Xóa** + popup xác nhận xóa
- [x] Test UI nhiều tài khoản: Meeting 151 (Sửa·In·Tạo phiếu công tác khác·Xóa·Quay lại) · BOM 25 với
      người tạo (Sửa·In·Xuất Excel·Sao chép·Xóa·Quay lại) · Dự án 239 (Tạo giải pháp) · Dự án 273
      (Tạo yêu cầu làm giải pháp) · Dự án 274 đã có YCGP → ẩn đúng · YCGP 17 (Sửa·Xóa) ·
      Giải pháp: tài khoản không đủ quyền thì danh sách lẫn chi tiết đều không có nút → khớp nhau

## #10818 — Báo cáo Dự án TKT theo PB–NV KD  ✅ ĐÃ SỬA
Lúc đầu đo nhầm chỗ (khoảng cách ô chọn ↔ panel = 4px, đúng thiết kế) nên tưởng không tái hiện.
Phóng to ảnh QA mới thấy lỗi nằm BÊN TRONG panel: dòng option lòi ra giữa 2 thanh dính.
- [x] **Khe giữa 2 thanh dính**: `.cps-search` để cứng `top: 33px` trong khi `.cps-toolbar` cao thật
      **31.5px** → hở ~1.5px, danh sách cuộn qua khe đó lộ ra và bị cắt ngang (đúng ảnh QA khoanh đỏ).
      Sửa: đo chiều cao thật bằng JS ghi vào biến CSS `--cps-toolbar-h` (không làm tròn) →
      khe = **0** ở cả ô cha và ô con. Áp cùng cách cho `components/CheckboxMultiSelect.vue` (cùng lỗi
      `top: 33px`, dùng ở nhiều bộ lọc khác).
- [x] **Panel bị UI khác đè** (user báo thêm): không phải z-index mà do
      `.advanced-filters { overflow: hidden }` của `V2BaseFilterPanel` CẮT panel khi tràn xuống dưới.
      Thêm `.advanced-filters { overflow: visible }` cho màn báo cáo — giống cách `/assign/customers`
      và `/assign/prospective-projects` đã xử lý trước đó. Kiểm lại: panel nằm TRÊN CÙNG ở cả 3 điểm
      (đầu / giữa / đáy).
- [ ] Gốc rễ: `V2BaseFilterPanel` để `overflow: hidden` nên MỌI màn có dropdown trong bộ lọc đều phải
      tự vá lại — nên sửa 1 lần ở component dùng chung (cần chốt vì đụng animation thu gọn của mọi màn).

## #10840 — Tự sinh mã hàng tạm  ✅ ĐÃ SỬA
Nguyên nhân: `QuotationService::collectProjectTempGoodCodes()` giữ lại mã hàng tạm khi trùng mã trong
CÙNG DỰ ÁN nhưng **không lọc trạng thái**, trong khi màn "Hàng hoá dự án" (`ProductProjectController`)
chỉ lấy BOM tổng hợp ĐÃ DUYỆT + báo giá ĐÃ DUYỆT/TRÚNG THẦU. Hàng tạm mới chỉ nằm ở báo giá NHÁP cũng
bị giữ mã → import file Excel sang báo giá khác cùng dự án ra 2 dòng trùng mã (ca QA: HHBG001222 ở cả
BG-2026-00341 và BG-2026-00342, dự án 465).
- [x] Thêm `b.status = ĐÃ DUYỆT` (BOM) và `q.status IN (ĐÃ DUYỆT, TRÚNG THẦU)` (báo giá) cho khớp đúng
      điều kiện của màn Hàng hoá dự án — chốt với user 17/09/2026
- [x] Bộ test `test_10840.php`: **14/14 PASS**; đối chứng code cũ **5 FAIL**, tái hiện đúng ca QA (A và B trùng mã)
- [x] Test UI thật (tài khoản `quyenhn.kd3`): import file mang mã `HHBG010012` của báo giá nháp cùng dự án
      → báo giá đích sinh mã mới `HHBG010013` đúng quy tắc HHBG + id
- [x] (bổ sung 17/09 theo yêu cầu user) Import xong **KHÔNG hiện mã hàng tạm** trên lưới: mã trong file chỉ
      là "nhãn" để gom nhóm/đối chiếu, mã thật do BE sinh lúc Lưu → thêm helper `displayCode(row)`:
      hàng tạm chưa lưu (chưa có `price_id`) để trống cột Mã, hàng ERP và hàng tạm đã lưu hiện mã như cũ.
      Vẫn GIỮ mã trong payload gửi BE để Rule 1 (giữ mã của hàng hoá dự án) và Rule 3 (gom dòng cùng nhãn) chạy đúng.
      Kiểm UI: sau Import cột Mã trống → Lưu nháp → hiện `HHBG010031` (khớp id dòng 10031);
      kiểm hàm: ERP chưa lưu vẫn hiện mã, hàng tạm đã lưu vẫn hiện mã.

## #10791 — Cập nhật đơn giá theo thời giá  🔶 ĐÃ SỬA PHẦN CHẮC CHẮN
- [x] Popup in tiền kiểu VN (`1.250.000`) → chuẩn quốc tế (`1,250,000`), đúng CLAUDE.md chốt 2026-08-26.
      Sửa thêm 5 chỗ khác trong luồng báo giá / BOM / giải pháp cũng đang dùng `vi-VN` cho SỐ.
- [ ] CHỜ CHỐT: chữ 2 nút. QA ghi "ĐỒNG Ý VÀ TỪ CHỐI"; skill `button-convention` không có chữ "Đồng ý"
      (chuẩn là "Xác nhận") và "Từ chối" thuộc nhóm nút đỏ nguy hiểm — không hợp với thao tác *giữ giá cũ*.
      Đang giữ "Cập nhật giá" / "Giữ giá cũ" vì nói đúng việc sẽ xảy ra.
- [ ] Ngoài phạm vi (KHÔNG tự sửa đại trà): còn ~8 chỗ khác trong phân hệ Giao việc format số kiểu VN
      (settings history, MeetingsTab, meeting/index, children tab, parent quotations tab, 2 file report…)
