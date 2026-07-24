# Fix build lỗi v2-styles.scss — thiếu lang="scss" (@khoipv)

## Bối cảnh

`yarn generate` (production build) fail với lỗi `Expected a pseudo-class or pseudo-element` tại `assets/scss/v2-styles.scss:2:5` ở 11 component module Assign.

**Nguyên nhân:** 11 file dùng `<style>` thuần (không có `lang="scss"`) nhưng `@import '@/assets/scss/v2-styles.scss'` → webpack không chạy sass-loader → cú pháp SCSS (comment `//`, nesting `&`) lọt thẳng vào postcss. Dev mode không sao, nhưng khi build production plugin `postcss-minify-selectors` (cssnano) parse selector nghiêm ngặt → gãy.

**Fix:** đổi `<style>` → `<style lang="scss">` tại đúng 11 vị trí, không đụng nội dung style.

## Tasks

- [x] Đổi `<style lang="scss">` — `pages/assign/application/index.vue:1379`
- [x] Đổi `<style lang="scss">` — `pages/assign/form-templates/index.vue:754`
- [x] Đổi `<style lang="scss">` — `pages/assign/solution-groups/index.vue:1065`
- [x] Đổi `<style lang="scss">` — `pages/assign/solutions/components/SolutionForm.vue:686`
- [x] Đổi `<style lang="scss">` — `pages/assign/project_role/index.vue:1262`
- [x] Đổi `<style lang="scss">` — `pages/assign/my-job/components/IssuesTab.vue:474`
- [x] Đổi `<style lang="scss">` — `pages/assign/meeting_type/index.vue:1188`
- [x] Đổi `<style lang="scss">` — `pages/assign/reason_project_failure/index.vue:948`
- [x] Đổi `<style lang="scss">` — `pages/assign/project_items/index.vue:1105`
- [x] Đổi `<style lang="scss">` — `pages/assign/request-solution/components/RequestSolutionForm.vue:695`
- [x] Đổi `<style lang="scss">` — `pages/assign/project_phase/index.vue:1176`
- [x] Grep toàn bộ `pages/components/layouts` xác nhận không còn `<style>` thuần nào import `.scss` (0 match)
- [ ] User chạy lại `yarn generate` / build trên server xác nhận PASS

### Checkpoint — 2026-07-15
Vừa hoàn thành: sửa cả 11 file + grep xác nhận sạch.
Đang làm dở: không.
Bước tiếp theo: user build lại để xác nhận.
Blocked: không.
