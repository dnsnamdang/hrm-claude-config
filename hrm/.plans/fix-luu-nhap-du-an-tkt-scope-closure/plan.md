# Plan — Fix lỗi 500 khi Lưu nháp dự án TKT (rule dạng mảng chứa Closure)

Người phụ trách: @khoipv
Nhánh: `tpe-develop-assign` (hrm-api)

## Phase 1 — BE

- [x] T1. `ProspectiveProjectRequest::relaxRequiredRules()` bỏ qua phần tử KHÔNG phải string
      (Closure / Rule object) thay vì đưa vào `strpos()`
- [x] T2. Khi bộ luật có phần tử không phải string → trả về DẠNG MẢNG, không `implode('|')`
      (implode sẽ nổ "Object of class Closure could not be converted to string")
- [x] T3. Verify: gọi `rules()` với `status = STATUS_DANG_TAO` cho cả 3 luồng
      (dự án độc lập / dự án con / dự án cha) — không còn ErrorException, `scope_id`
      và `scope_ids.*` vẫn giữ closure chống trùng nhóm ngành

### Checkpoint — 2026-09-12
Vừa hoàn thành: T1–T3. Sửa `relaxRequiredRules()` (hrm-api, nhánh `tpe-develop-assign`):
bỏ qua phần tử không phải string khi lọc, và trả về mảng khi bộ luật có Closure/Rule object.
Đang làm dở: không có.
Bước tiếp theo: user bấm "Lưu nháp" lại trên màn dự án TKT để xác nhận hết 500 (chưa kiểm thử trình duyệt).
Blocked:
