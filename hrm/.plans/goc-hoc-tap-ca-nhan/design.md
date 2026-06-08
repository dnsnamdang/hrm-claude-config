# Góc học tập cá nhân + Tìm kiếm global — Design (Tóm tắt)

- **Người phụ trách:** @junfoke
- **Ngày:** 2026-06-05
- **Spec đầy đủ:** `docs/superpowers/specs/2026-06-05-goc-hoc-tap-ca-nhan-design.md`
- **Project:** elearning (Vue 3.5 + Vite 5)

## Mục tiêu
Convert mockup `my_courses.html` thành trang **Góc học tập cá nhân** (`/goc-hoc-tap`, 4 tab) + làm **tìm kiếm global** ở header kiểu f8.edu.vn (popup gợi ý + trang `/tim-kiem`).

## Quyết định lớn
- Dữ liệu: FE-first, tái dùng API có sẵn; list góc học tập dùng **mock** (chưa có endpoint), certificate dùng API thật. Store để sẵn chỗ swap API.
- Đủ **4 tab**: Tổng quan / Tôi cần học / Tôi đang học / Chứng chỉ. Nút **nối sang trang thật**.
- Chart: cài **`apexcharts` + `vue3-apexcharts`** (wrapper hrm-client là Vue 2 — không tái dùng được).
- Tìm kiếm: **popup gợi ý live** (2 nhóm Khóa học + Lộ trình, mỗi nhóm "Xem thêm" → trang list) + **trang `/tim-kiem`** có badge lọc loại nội dung. Elearning chỉ 2 loại nội dung. Không thêm dep cho search (tự viết debounce + click-outside).

## Kiến trúc (Hướng A)
- 1 store `myLearning.js` gom 4 tab + getters derive (overview luôn khớp). Mock ở `constants/myLearningMock.js` (bổ sung `slug`).
- Tab tách component trong `components/my-learning/`, mỗi file < 300 dòng.
- Search: store `search.js` dùng chung cho popup `GlobalSearch.vue` + trang `SearchResultView.vue`.
- Tái dùng: `LearnCard`/`PathCard`/`CardSkeleton`/`EmptyState`, 2 trang browse list (cho "Xem thêm"), route detail/learn/certificate có sẵn.

## Phase
1. **Góc học tập cá nhân** — route + store + mock + 4 tab + ApexCharts + wiring.
2. **Tìm kiếm global** — store + composable + popup + trang /tim-kiem + nối header + seed keyword browse.

Xem chi tiết DB/API/component/edge case trong spec đầy đủ.
