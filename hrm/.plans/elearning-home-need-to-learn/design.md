# Design — Section "Bạn cần học" (trang chủ elearning) lấy data thật

Phụ trách: @khoipv
Ngày: 2026-06-04
Liên quan: [[elearning-learning-path-visibility]] (cùng quy tắc visibility)

## Mục tiêu
Section "Bạn cần học" ở trang chủ elearning (`http://localhost:3001/`) hiện đang dùng
mock data. Chuyển sang lấy **khóa học (Subject) + lộ trình (LearningPath)** thật từ BE,
trộn chung, áp quy tắc hiển thị theo loại user.

## Scope
- CÓ: section "Bạn cần học" trên `HomeView.vue` + endpoint BE mới + mở rộng `LearnCard`.
- KHÔNG (ngoài phạm vi): các section khác (Khuyến nghị, Phổ biến, Nội dung mới, Vinh danh,
  Danh mục) vẫn giữ mock; không đụng màn list `/lo-trinh-hoc-tap`, `/khoa-hoc`.

## Quyết định chốt
1. Section là **danh mục chung** (khóa + lộ trình), KHÔNG lọc theo "bắt buộc".
2. Hiển thị **tối đa 4 mục**, sắp theo **mới cập nhật trước** (`updated_at` desc).
3. Lấy data qua **1 endpoint home riêng** (BE trộn + sort + cắt sẵn).
4. Render dùng chung **`LearnCard`**, mở rộng để nhận `type='path'`.

## Quy tắc visibility
| Loại user | Khóa học (Subject) | Lộ trình (LearningPath) |
|-----------|--------------------|--------------------------|
| Khách (guest + learner elearning) | `status=HOAT_DONG(1)` AND `is_public=1` | `status=ACTIVE(2)` AND `is_public=1` |
| Nhân viên HRM (employee, SSO) | `status=HOAT_DONG(1)` | `status=ACTIVE(2)` |

- Nhận diện employee: `$request->attributes->get('user_type') === 'employee'` (set bởi
  middleware `elearning.auth.optional`).
- Subject status: `HOAT_DONG=1`, `KHOA=2`, `STATUS_DRAFT=3`.
- LearningPath status: `STATUS_DRAFT=1`, `STATUS_ACTIVE=2`, `STATUS_LOCKED=3`.

## Backend
### Route
`Modules/Elearning/Routes/api.php`:
```php
Route::get('public/home-content', [PublicBrowseController::class, 'homeContent'])
    ->middleware('elearning.auth.optional');
```

### Controller `PublicBrowseController@homeContent`
- `$isHrmEmployee = $request->attributes->get('user_type') === 'employee';`
- Query Subject: `where('status', Subject::HOAT_DONG)->when(!$isHrmEmployee, is_public=1)`
  → eager-load lessons để tính `minutes`, `orderByDesc('updated_at')`, `limit(4)`.
- Query LearningPath: `where('status', LearningPath::STATUS_ACTIVE)->when(!$isHrmEmployee, is_public=1)`
  → withCount khóa học, `orderByDesc('updated_at')`, `limit(4)`.
- Map cả hai về mảng learn-item chung → merge → sort `updated_at` desc → `slice(0,4)`.
- Trả `responseJson('Thành công', 200, ['items' => $items])`.
- try/catch + `Log::error` theo chuẩn controller.

### Shape "learn item"
```jsonc
{
  "id": 12,
  "type": "course" | "path",      // course=khóa học, path=lộ trình
  "title": "...",                  // name
  "desc": "...",                   // description
  "thumb": "https://...",          // banner_url
  "minutes": 190,                  // tổng thời lượng (path: tổng các khóa)
  "slug": "...",
  "vote": { "stars": 0, "count": 0 },
  "courses_count": 5,              // chỉ path; course = null/0
  "updated_at": "2026-06-01T..."
}
```

## Frontend
### `stores/elearning.js`
- `state.needToLearn = []`.
- `fetchHomeData()`: `await api.get('/api/v1/elearning/public/home-content')`, gán
  `this.needToLearn = res.data?.items || []`. Giữ mock cho các section khác.
- Bỏ getter `needToLearn` lọc mock theo `isMandatory` (chuyển thành state).

### `HomeView.vue`
- Section "Bạn cần học" loop `store.needToLearn`, dùng `LearnCard`, bỏ `:show-deadline`.
- `openLearn(item)` điều hướng theo `type`:
  - `course` → route `subject-detail` (params `slug`).
  - `path` → route `learning-path-detail` (params `slug`).
- Cập nhật `subtitle` section: bỏ chữ "bắt buộc" (vd "Khóa học và lộ trình dành cho bạn").

### `components/base/LearnCard.vue`
- `kindLabel`: `course`→'Khoá học', `path`→'Lộ trình', (`subject`→'Môn học' giữ nguyên).
- `kindIcon` / `kindPillClass`: thêm nhánh `path` (icon `ri-road-map-line`, màu khác).

## Edge cases
- Không token / token hỏng → guest → chỉ public.
- Section rỗng → ẩn section (v-if độ dài > 0) hoặc empty state nhẹ.
- `minutes` null → `0 phút`; `vote.count = 0` → "Chưa có đánh giá".
- Nếu một loại không có mục nào → vẫn trộn loại còn lại (không lỗi).

## Downstream / lưu ý
- Endpoint list `public/subjects` hiện vẫn ép `is_public=1` cho mọi user — KHÔNG đổi trong
  feature này. Nếu sau muốn nhất quán (employee xem khóa nội bộ ở màn list) thì tách task riêng.
- FE `services/api.js` đã tự đính kèm Bearer token nên employee được nhận diện đúng.
