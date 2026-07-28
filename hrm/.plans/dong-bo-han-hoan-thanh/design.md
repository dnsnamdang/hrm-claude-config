# dong-bo-han-hoan-thanh — Tóm tắt

**Owner**: @junfoke · **Ngày**: 2026-07-24 · Spec chi tiết: `docs/superpowers/specs/2026-07-24-dong-bo-han-hoan-thanh-design.md`

## Mục tiêu
Dẹp "mỗi màn tính hạn hoàn thành một kiểu". Một cơ chế tính hạn thống nhất qua **1 helper duy nhất**; mọi điểm đọc gọi cùng hàm. Làm rõ UI cấu hình theo mô hình **"hạn mặc định + hạn riêng ghi đè cho NV mới"**.

## Quyết định chính (v2 — DYNAMIC)
- **Dynamic (tính khi đọc)**, KHÔNG freeze: hạn = `enrolled_at + số ngày config hiện tại`, tính lại mỗi lần đọc. Đổi config dời hạn cả người đã tham gia.
- **Giữ 2 hạn**, đánh dấu cohort onboarding bằng **cột cờ `is_onboarding`** trên `subject_enrollments` (thay cho `due_date`). `due_date` cũ để dormant.
- **Công thức đọc**:
  - Khoá: `days = (is_onboarding && must_finish>0) ? must_finish : complete_within_days`; `deadline = enrolled + days` (days≤0/null → null).
  - Lộ trình: `deadline = enrolled + complete_within_days`.
- **Quy ước mới**: onboarding must_finish trống/0 = dùng hạn mặc định (cũ = không giới hạn). Nới validate `required`→`nullable`.
- **Enroll không tính/ghi hạn nữa**; chỉ luồng onboarding set `is_onboarding=1` (bỏ ghi due_date).
- **Backfill 1 lần**: `is_onboarding=1 WHERE due_date IS NOT NULL` (user ra lệnh mới chạy).
- Gỡ vá tay FE `myLearning.js:56-61`.

## Phạm vi module
`Modules/Training` (migration + Entity + luồng B + validate + backfill + FE hrm-client) + `Modules/Elearning` (branch `tpe-develop-elearning`: DeadlineHelper + mọi điểm đọc + HallOfFame) + FE elearning.

## Ngoài phạm vi
Không có luồng gán tay/import/auto theo phòng ban ("bắt buộc" chỉ là nhãn). Không làm nút "gia hạn hàng loạt" (dynamic đã tự propagate). Không drop cột due_date.
