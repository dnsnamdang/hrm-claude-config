# Design — Meeting: tải danh sách Dự án TKT phân trang (dùng chung web + app)

Phụ trách: @dnsnamdang · Nhánh: **`gop_db`** (cả `hrm-api` + `hrm-client`, chốt 14/10/2026)
Nguồn đề xuất (đã duyệt 14/10): `.plans/app-meeting-mobile/design.md` mục "Đề xuất — tải danh sách Dự án TKT"
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-14-meeting-chon-du-an-tkt-design.md`

## Vấn đề

Ô "Dự án TKT" ở form meeting (`GeneralInfo.vue:1489`) gọi `getForMeeting?per_page=10000`: tải MỌI dự án
trong phạm vi, mỗi dòng kèm full resource (`RESOURCE_EAGER_RELATIONS` + 5 subquery giải pháp), rồi lọc KH /
tìm kiếm ở FE. App di động không dùng được kiểu này.

## Hướng làm — tách CHỌN (nhẹ, phân trang) và LẤY CHI TIẾT (1 dự án)

1. `GET assign/prospective-projects/options-for-meeting` — `search` · `customer_id` · `page` · `per_page` (20, trần 50).
   Trả gọn `id, code, name, customer_id, customer_code, customer_name, status, status_name, status_color, is_parent`.
   Phạm vi GIỮ NGUYÊN `getForMeeting`: `selectableForMeeting()` (tiến trình 2–10) + (người tạo / người làm giải pháp /
   người hỗ trợ) → tách thành scope dùng chung để 2 endpoint không lệch.
2. `GET assign/prospective-projects/options-for-meeting/{id}` — chi tiết 1 dự án (full resource như `getForMeeting`
   đang trả) cùng điều kiện phạm vi; KHÔNG dùng `show` (theo quyền xem dự án → người hỗ trợ bị 403).
   Chỉ web cần (điền tab "Dự án tiền khả thi"); app bỏ GP/HM nên không gọi.
3. Dự án đã gắn: lấy từ chi tiết meeting (`form.projects`), không cần nằm trong danh sách chọn → bỏ `meeting_id` include.
4. Web FE: ô chọn chuyển sang tìm phía server (debounce 300ms + huỷ request cũ, cuộn cuối tải trang kế).
5. `getForMeeting` cũ: giữ tới khi web chuyển xong rồi mới gỡ.

## Quyết định đã chốt

| Ngày | Nội dung |
|---|---|
| 14/10 | Làm trên `gop_db` (không tách nhánh con) |
| 14/10 | Hồ sơ tách riêng thư mục này (không gộp vào `meeting-theo-doi-tuong`) |
| 14/10 | FE web: tạo component MỚI chọn nhiều tìm phía server, KHÔNG sửa `MultiSearchPicker` |
| 14/10 | User cho phép code Phase 1 BE (hrm-api, gop_db, không migration, không chạy DB, không commit) |

