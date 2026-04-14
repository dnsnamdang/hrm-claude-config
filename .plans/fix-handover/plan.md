# Plan: Fix Bàn giao công việc

## Trạng thái
- Bắt đầu: 2026-03-31
- Tiến độ: 3/3 task done

## Danh sách task

[x] Task 1: Fix mất ngày bàn giao khi edit — convert DD/MM/YYYY → YYYY-MM-DD trước khi truyền vào HandoverForm
[x] Task 2: Fix checkbox _selected mặc định checked — đổi thành false khi load edit
[x] Task 3: Sinh bộ testcase Excel — 108 TC, 10 section (DS/Tạo-Sửa/Chi tiết/Tiếp nhận/Chờ duyệt/Chờ tiếp nhận/Phân quyền/BR E2E/Notification/Edge), script `generate_testcase.py`, output `Testcase_Ban_Giao_Cong_Viec.xlsx`

## Checkpoint
- 2026-03-31: 2 bug fix done, merge fix_handover → tpe-develop-assign, pushed GitHub

### Checkpoint — 2026-04-14
Vừa hoàn thành: Sinh `Testcase_Ban_Giao_Cong_Viec.xlsx` (108 TC, prefix HDV) + `generate_testcase.py` + spec `docs/superpowers/specs/2026-04-14-handover-testcase-design.md`
Đang làm dở: —
Bước tiếp theo: QA review & chạy test thủ công theo Excel, đánh cột Status (Passed/Failed/Pending/Not Executed)
Blocked: —
