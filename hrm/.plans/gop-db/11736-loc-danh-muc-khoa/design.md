# #11736 — Bộ lọc danh mục hiện cả danh mục đã khoá (🔒) — @khoipv

Redmine: http://quanly.dnsmedia.vn/issues/11736 · "[ERP => HRM] Sửa bộ lọc cho toàn bộ màn hình có gắn danh mục"
Nhánh: `develop` (checkout từ `gop_db`) cả 2 repo.

## Yêu cầu
Ở màn danh sách, ô lọc dùng danh mục có trạng thái khoá phải hiện cả danh mục **đang hoạt động** lẫn
**đã khoá** (đánh dấu 🔒, giống ô Công ty / Phòng ban). Danh mục khoá **không còn bản ghi nào liên kết** thì không hiện.

## Quyết định đã chốt (13/11/2026)
- **Phạm vi**: mọi màn port ERP→HRM (user chốt), không chỉ CSKH sau bán.
- **"Bản ghi liên kết"** = bản ghi CỦA CHÍNH MÀN ĐÓ (lọc theo nó phải ra kết quả), không phải dùng ở bất kỳ đâu.
- **Sửa component chung** `V2BaseFilterFieldControl.vue` — user đồng ý: field lọc khai `keepLockedOptions: true`
  thì truyền xuống `V2BaseSelect` (mặc định select ẩn option khoá chưa được chọn).
- Dấu 🔒 giữ đúng chuẩn hiện hành của hệ thống (`withLockedOptionMarker`, đứng trước tên) — giống ô Công ty/Phòng ban.
- Ô lọc **Trạng thái / Nhân viên / hằng số (enum)** không thuộc phạm vi. Ô Công ty/Phòng ban/Bộ phận trong
  `V2BaseCompanyDepartmentFilter` đã có nút hiện cả mục khoá → giữ nguyên.

## Cách làm
- **BE** `app/Support/LockedCatalogOptions::activeOrUsed($query, $usages, $statusCol, $activeValue)`:
  `status = active OR id IN (subquery cột của màn trỏ tới)`. `$usages` = `['bảng','cột', [điều kiện]]` hoặc
  Closure subquery (liên kết gián tiếp). Bảng/cột không tồn tại bị bỏ qua. Trả `is_locked` từng dòng.
- **FE**: field lọc thêm `keepLockedOptions: true`; options giữ nguyên `is_locked` từ BE.
- Endpoint danh mục dùng chung (nhiều màn gọi) KHÔNG được đổi hành vi mặc định — thêm options riêng cho màn
  (endpoint options của màn) hoặc tham số whitelist phía BE, không cho client truyền tên bảng.

Mẫu: `customer-care/device-errors` (Nhóm hàng hóa) + `customer-care/warranty-repair-requests` (Tỉnh/TP).
