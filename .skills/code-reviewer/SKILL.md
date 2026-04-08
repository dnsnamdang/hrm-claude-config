# Code Reviewer — ERP TPE

## Mục đích
Review code theo đúng conventions của project ERP TPE (Laravel 8 + Nuxt 2) trước khi merge hoặc sau khi hoàn thành feature.

## Khi nào dùng
- Sau khi hoàn thành 1 feature hoặc fix bug phức tạp
- Trước khi push/merge vào `tpe-develop-assign`
- Khi cần fresh perspective về code vừa viết

## Cách dùng
Dispatch subagent `superpowers:code-reviewer` với context sau:

```
WHAT_WAS_IMPLEMENTED: [mô tả ngắn]
PLAN_OR_REQUIREMENTS: [link tới .plans/[feature]/plan.md]
BASE_SHA: [commit trước khi bắt đầu]
HEAD_SHA: [commit hiện tại]
```

## Checklist review cho project này

### Backend (Laravel 8 / PHP 7.4)
- [ ] Không dùng syntax PHP 8+ (named arguments, match expression, union types, nullsafe operator)
- [ ] Dùng đúng BaseService, BaseModel, ApiController có sẵn
- [ ] Permission dùng spatie/laravel-permission — không tự tạo middleware auth riêng
- [ ] Query có N+1 không? Đã dùng `with()` eager load chưa?
- [ ] Migration có rollback (`down()`) không?
- [ ] Route đặt trong `Modules/[Module]/Routes/api.php`, không đặt trong `routes/api.php` chung
- [ ] Không sửa hàm dùng chung khi chưa được confirm
- [ ] Không tự thêm permission theo cấp khi chưa được confirm
- [ ] Accessor `is_can_delete` phải hỏi điều kiện xóa cụ thể trước khi viết
- [ ] Log lỗi đúng cách: `Log::error()` với context đầy đủ

### Frontend (Nuxt 2 / Vue 2)
- [ ] Không dùng Vue 3 syntax (Composition API, `<script setup>`, `defineProps`)
- [ ] Dùng V2Base components có sẵn (V2BaseButton, V2BaseBadge, V2BaseFilterPanel...)
- [ ] Style import `@import '@/assets/scss/v2-styles.scss';` trong `<style lang="scss">`
- [ ] API call qua `this.$store.dispatch('apiGetMethod', ...)` / `apiPostMethod`
- [ ] Cascading filter đúng thứ tự: Công ty >> Phòng ban >> Bộ phận
- [ ] Không dùng `this.$axios` trực tiếp — dùng qua store actions

### Chung
- [ ] Không commit file trong `vendor/`, `node_modules/`
- [ ] Không hardcode URL, dùng env variable
- [ ] Tên biến/hàm nhất quán với pattern có sẵn trong module

## Mức độ issue
- **Critical**: Bug runtime, lỗ hổng bảo mật, mất data → fix ngay
- **Important**: Vi phạm convention, N+1 query, thiếu permission check → fix trước khi merge
- **Minor**: Code style, naming, comment thiếu → ghi nhận, fix khi rảnh
