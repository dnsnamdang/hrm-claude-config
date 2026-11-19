# Quyết định định biên — đơ khi chọn nhiều phòng ban (@cuong61n)

## Phase 1 — Tối ưu màn Tạo/Sửa
### FE
- [x] Chọn phòng ban: chỉ tải định biên phòng MỚI thêm, song song, ghi theo id (bỏ vòng tải lại toàn bộ N phòng mỗi lần chọn)
- [x] Danh mục rank_groups / ranks / titles / missions tải 1 lần ở FormComponent, truyền props xuống từng tab (freeze)
- [x] Modal phân công nhiệm vụ nhóm: bỏ watch deep `department` (gõ 1 ký tự gọi API), chỉ tải khi mở modal
### BE
- [x] getManpowerDepartment eager load cây quan hệ + gom RankGroup (8 phòng: 698 → 169 query, kết quả giống hệt)

- [x] Fix hồi quy phát hiện khi test: option phòng BE trả sẵn `list_rank_groups: []` → nhận diện phòng mới bằng object option, không bằng list_rank_groups
- [x] Modal nhiệm vụ: chặn gọi trùng khi mở lại lúc request chưa về
- [x] Playwright local (3002→8003): Tạo mới 8 phòng, gõ/thêm/bỏ phòng, modal, Lưu (POST 200), Chi tiết, Sửa (PUT 200) — bản ghi test decision_id=713 / manpower_planning id=4 trên DB local
- [x] FE-4: chỉ dựng bảng của tab đã mở (renderedDepartmentIds, mở rồi giữ); Lưu thì kiểm dữ liệu thô tab chưa mở, tab lỗi được dựng + chuyển tới để vee-validate báo đỏ
- [x] Fix: màn Sửa/Chi tiết tab đầu rỗng khi vào (watch department_id immediate)
- [x] Playwright 10 phòng: main thread bị chặn 6,5s (8 phòng) → 2–3s rải thành các nhịp 110–330ms; validate tab chưa mở OK; Chi tiết/Sửa OK (PUT 200)
- [x] Dropdown Phòng ban "bị đè" — kiểm lại: KHÔNG lỗi, chỉ là bẫy click của Playwright

### Checkpoint — 2026-10-20
Vừa hoàn thành: Phase 1 + FE-4 trên gop_db, test Playwright local (chưa commit)
Đang làm dở:
Bước tiếp theo: user test tay rồi commit; còn mở: tối ưu `master-data/ranks` (1.141 query/lần, model Rank/Competency dùng chung — cần hỏi)
Blocked:

- [x] Fix 28/10/2026 (PROD id 10): màn Sửa dropdown Phòng ban rỗng — mounted nạp options theo type_decision_id, không xoá phòng đã chọn (FormDecisionComponent.vue). Playwright local OK: loại 1 + loại 2, thêm phòng + Lưu PUT 200, Chi tiết/Thêm mới không gọi thừa
