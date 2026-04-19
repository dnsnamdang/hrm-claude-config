Dispatch subagent `superpowers:code-reviewer` với context window riêng để review code vừa implement theo conventions ERP TPE.

## Hướng dẫn

1. Xác định scope review:
   - Đọc `.plans/STATUS.md` → tìm feature đang ở "Đang làm"
   - Đọc `.plans/[feature]/plan.md` + `design.md` → xác định requirements + task vừa hoàn thành
   - Lấy diff:
     - Unstaged: `git diff` trong hrm-api + hrm-client
     - Đã commit: `git log --oneline -10` + `git diff <base>..HEAD`
   - Liệt kê danh sách files thay đổi

2. Dispatch subagent với **subagent_type: `superpowers:code-reviewer`** — prompt bao gồm:

```
## Context
- Project: ERP TPE (Laravel 8 / PHP 7.4 + Nuxt 2 / Vue 2)
- Feature: [tên feature từ STATUS.md]
- Branch API: [branch hiện tại hrm-api]
- Branch Client: [branch hiện tại hrm-client]
- Plan: .plans/[feature]/plan.md
- Design: .plans/[feature]/design.md

## Files thay đổi
[Liệt kê files + số dòng thay đổi]

## Requirements (từ plan.md)
[Task vừa hoàn thành + yêu cầu cụ thể]

## Project-specific checklist (BẮT BUỘC kiểm tra)

### Backend (Laravel 8 / PHP 7.4)
- Không dùng syntax PHP 8+ (named arguments, match expression, union types, nullsafe ?->, str_contains, enum)
- Dùng đúng BaseService, BaseModel, ApiController có sẵn
- Permission dùng spatie/laravel-permission — không tạo middleware riêng
- Query N+1: đã dùng with() eager load chưa?
- Migration có down() rollback không?
- Route trong Modules/[Module]/Routes/api.php — không đặt routes/api.php chung
- Model $fillable đầy đủ cho TẤT CẢ cột mới (đặc biệt quan trọng — đã bị miss trước đây)
- Không sửa hàm dùng chung khi chưa confirm
- Không tự thêm permission theo cấp khi chưa confirm
- Log::error() có context đầy đủ

### Frontend (Nuxt 2 / Vue 2)
- Không dùng Vue 3 syntax (Composition API, <script setup>, defineProps, ref/reactive)
- Dùng V2Base components có sẵn (V2BaseButton, V2BaseBadge, V2BaseFilterPanel...)
- Style: <style lang="scss"> với @import '@/assets/scss/v2-styles.scss'
- API call qua this.$store.dispatch('apiGetMethod'/'apiPostMethod') — KHÔNG dùng this.$axios
- Cascading filter đúng thứ tự: Công ty >> Phòng ban >> Bộ phận

### Chung
- Không hardcode URL — dùng env variable
- Tên biến/hàm nhất quán với pattern có sẵn trong module
- Không commit vendor/, node_modules/, .env

## Output format
Trả về báo cáo:

### Summary
- Tổng files reviewed: X
- Critical: X | Important: X | Minor: X | OK: X

### Critical (fix ngay — bug runtime, bảo mật, mất data)
- [file:line] Mô tả vấn đề → Cách fix

### Important (fix trước merge — vi phạm convention, N+1, thiếu check)
- [file:line] Mô tả vấn đề → Cách fix

### Minor (ghi nhận — code style, naming)
- [file:line] Mô tả vấn đề

### OK (làm đúng convention)
- Liệt kê điểm tốt

### So sánh với plan
- Task nào trong plan đã implement đúng?
- Task nào thiếu hoặc implement khác yêu cầu?
```

3. Sau khi subagent trả kết quả → tóm tắt cho user:
   - Bảng summary: số issue theo mức độ
   - Liệt kê Critical + Important cần fix (kèm file:line)
   - So sánh với plan: đúng/thiếu/khác
   - Hỏi: "Muốn fix ngay hay ghi nhận?"
