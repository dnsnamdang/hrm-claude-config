# Fix: Tổng giá trị khen thưởng bị cộng trùng (double-count)

## Bối cảnh
Màn `/decision/decision-reward/{id}/edit`: "Tổng giá trị khen thưởng" không bằng tổng các mode bên dưới.
VD id=4: tổng = 214.000.000 nhưng các mode "Thưởng tiền mặt" chỉ 152.000.000 (dư 62.000.000).

## Nguyên nhân
Watcher trong `DecisionRewardForm.vue` (~dòng 668-685) cộng thêm `baseRewardAmount = reward_value × số lượng`
khi `hasCashRewardMode(reward_title_id) === false`. Hàm này đọc cấu hình mode của DANH MỤC danh hiệu,
không đọc mode thực nhập trong quyết định. Title 5/6/7 trống mode trong danh mục nhưng user đã thêm tay
mode "Thưởng tiền mặt" → cộng trùng. Form Reviewed/Approved đã comment-out block này (chỉ tính theo mode)
nên không lỗi → hành vi đúng = tổng theo mode thực nhập.

## Phase 1 — Fix FE
- [x] Trace nguyên nhân, đối chiếu DB id=4 (152M mode vs 214M total)
- [x] Xác nhận Reviewed/Approved form đã chỉ tính theo mode (comment-out base)
- [x] `DecisionRewardForm.vue`: bỏ cộng `baseRewardAmount` ở watcher → `total_amount = total_reward_mode`
- [ ] Verify trên trình duyệt id=4 (user đang đăng nhập): tổng = 152.000.000, khớp bảng breakdown

## Phase 1b — Rà soát toàn diện (đã làm)
- [x] BE store/update (`DecisionRewardService`) chỉ pass-through total_amount FE → đúng từ sau fix
- [x] Reviewed/Approved form đã modes-only → không lỗi
- [x] Transformer pass-through; không có report/dashboard nào cộng tổng khen thưởng
- [x] Bản in từng QĐ (`/print`) điền template, không tự tính tổng; bản in danh sách + list hiển thị `total_amount` DB (stale với data cũ)
- [x] Audit DB: chỉ QĐ id=3 (170M→152M) và id=4 (214M→152M) bị cộng trùng; id=1 là data rác (22 / 60000, mode value=0)

## Phase 1c — Bug: bấm "Chọn" nhân sự bị crash khi edit
- [x] Nguyên nhân: `addEmployee` dedup theo `item.employee_info.id` nhưng nhân sự load từ DB (edit) không có `employee_info` → `Cannot read properties of undefined (reading 'id')` → chặn thêm
- [x] Fix: đổi dedup sang `item.employee_id === employees[i].employee_id` (giống pattern addDepartment) ở cả 3 form: Form / Reviewed / Approved
- [ ] Verify: edit QĐ đang có nhân sự → thêm 'Bùi Tiến Nam' (id 1407) → thành công, không lỗi console

## Phase 2 — Data cũ (chờ user quyết)
- [ ] (Tùy chọn) Script recalc `total_amount` chi tiết + `decision_rewards.total_amount` cho QĐ id=3, id=4 (và xử lý id=1 rác)

## Checkpoint
### Checkpoint — 2026-06-29
Vừa hoàn thành: trace + xác định nguyên nhân double-count, tạo plan
Đang làm dở: chuẩn bị sửa DecisionRewardForm.vue watcher
Bước tiếp theo: bỏ block baseRewardAmount, verify trên browser
Blocked: chờ user xác nhận có xử lý data cũ không
