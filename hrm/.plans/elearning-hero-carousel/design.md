# Hero Carousel trang chủ Elearning — Tóm tắt

- **Người phụ trách**: @junfoke
- **Ngày**: 2026-07-15
- **Spec đầy đủ**: `docs/superpowers/specs/2026-07-15-elearning-hero-carousel-design.md`
- **Plan**: `.plans/elearning-hero-carousel/plan.md`

## Mục tiêu

Nửa trái (70%) của `HeroBanner.vue` trang chủ elearning đang cắm cứng ảnh `/TPE_BANNER.jpg` + tiêu đề tĩnh + 2 nút demo chỉ bắn toast. Thay bằng **carousel khoá học tự chuyển slide**, cá nhân hoá theo học viên, mỗi slide dẫn thẳng tới nội dung học.

## Scope

**Trong phạm vi**: chỉ nửa trái 70% của hero. FE elearning thuần.

**Ngoài phạm vi**: backend / API / migration, thêm dependency npm, bố cục 70/30, khối "Hoạt động gần đây", khối "Vinh danh học viên", 4 section giữa, banner do admin cấu hình.

## Quyết định lớn

1. **Nguồn slide**: data store sẵn có — `needToLearn` → `recommendToLearn` → `popularMix`, khử trùng lặp theo `type_id`, tối đa 5 slide. Zero backend.
2. **Hiệu ứng**: fade tự chuyển **6 giây**/slide (theo NN/G ~1s/3 từ), 1 khoá chiếm trọn khung, có dot + mũi tên + nút pause.
3. **Rỗng → fallback banner tĩnh hiện tại**, không cần empty state mới.
4. **Giữ nguyên** khối "Hoạt động gần đây" 30% bên phải.
5. **Tự viết component, không thêm thư viện** — dự án chưa có lib carousel; swiper/embla đều thừa cho fade 1 slide và a11y vẫn phải tự làm.
6. **Accessibility là ràng buộc cứng** (WCAG 2.2.2): hover/focus dừng, nút pause **dính** (không tự chạy lại), tôn trọng `prefers-reduced-motion`, điều hướng bàn phím, ARIA carousel/slide.

## Files

| File | Loại |
|---|---|
| `elearning/src/components/home/HeroCarousel.vue` | Mới |
| `elearning/src/constants/heroSlides.js` | Mới |
| `elearning/src/stores/elearning.js` | Sửa — getter `heroSlides` |
| `elearning/src/components/home/HeroBanner.vue` | Sửa — nửa trái → HeroCarousel, bỏ 2 nút demo |
| `elearning/src/views/home/HomeView.vue` | Sửa — truyền slides, nối `openLearn` |

## Lưu ý merge

Feature `elearning-home-dynamic` (đang chờ user `php artisan migrate`) chạm cùng `stores/elearning.js` + `HomeView.vue` nhưng khác vùng (recent-activities + categories) → không xung đột logic.
