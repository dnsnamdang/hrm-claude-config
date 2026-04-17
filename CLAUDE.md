# HRM Project — Hướng dẫn cho AI

## Nguyên tắc chung

- Luôn gợi ý và làm việc bằng tiếng Việt
- Không xử lý commit hay đẩy code lên git
- Không đọc file thư viện hệ thống — tốn token không cần thiết
- Ưu tiên dùng helper có sẵn, tạo helper mới nếu logic dùng lại nhiều nơi
- Khi cần sửa hàm dùng chung → hỏi ý kiến trước khi làm
- FE: Tuân thủ style list của module đang triển khai (mỗi module có thể khác nhau)
- Trước khi làm màn danh sách mới → hỏi có cần phân quyền theo cấp không
- Trước khi viết accessor `is_can_delete` → hỏi điều kiện xóa cụ thể của màn đó

---

## Tech Stack

| | |
|---|---|
| **Backend** | PHP 7.4, Laravel 8 (`^8.65`), MySQL, Redis |
| **Auth** | JWT (`tymon/jwt-auth ^1.0`) + Laravel Sanctum |
| **Permission** | `spatie/laravel-permission ^5.4` |
| **Module** | `nwidart/laravel-modules ^8.2` |
| **Excel** | `maatwebsite/excel ^3.1` |
| **Storage** | AWS S3 |
| **Frontend** | Nuxt 2.14 (Vue 2), Node 14.21.3 |
| **CSS** | Bootstrap 4 + Bootstrap-Vue 2.15 |
| **State** | Vuex 3.5 |
| **HTTP** | @nuxtjs/axios |
| **Date** | dayjs, vue2-datepicker |
| **Editor** | Quill, CKEditor 5 |
| **Chart** | ApexCharts, Highcharts, Chart.js |

---

## Kiến trúc Module

| # | Module | Backend | Frontend |
|---|--------|---------|----------|
| 1 | Hành chính nhân sự | `Modules/Human` | `pages/human` |
| 2 | Chấm công | `Modules/Timesheet` | `pages/timesheet` |
| 3 | Tính lương | `Modules/Payroll` | `pages/payroll` |
| 4 | Đào tạo | `Modules/Tranning` | `pages/tranning` |
| 5 | Giao việc ← đang phát triển | `Modules/Assign` | `pages/assign` |
| 6 | Quyết định | `Modules/Decision` | `pages/decision` |
| 7 | CRM | `Modules/CRM` | `pages/client` |

---

## Tài liệu chi tiết

| Cần gì | Đọc file nào |
|--------|-------------|
| Base classes, V2Base components, API store calls | `docs/shared.md` |
| Pattern CRUD đầy đủ (code mẫu) | `docs/conventions.md` |
| Onboarding dev mới | `docs/onboarding.md` |

---

## Convention Database (toàn project)

- **Cấp tổ chức**: luôn dùng `company_id`, `department_id`, `part_id` — tất cả `unsignedBigInteger nullable`. KHÔNG dùng `branch_id`.
- **Audit**: dùng `$table->timestamps()` (tạo `created_at`, `updated_at`) + thêm thủ công `created_by`, `updated_by` (`unsignedBigInteger nullable`). KHÔNG dùng SoftDeletes cho entity chính (chỉ dùng cho bảng phụ như comment/log nếu thực sự cần).
- **Version solution**: các entity gắn với solution phải có `solution_version_id` NOT NULL. Nếu áp dụng cả cấp module thì thêm `solution_module_id` + `solution_module_version_id` (nullable).
- **File đính kèm**: KHÔNG tạo bảng pivot riêng. Dùng bảng `files` chung với `table='<table_name>'` + `table_id=<entity_id>`. Model khai báo:
  ```php
  public function files() {
      return $this->hasMany(File::class, 'table_id', 'id')
          ->where('table', '<table_name>');
  }
  ```
- **Mã code tự sinh**: pattern `PREFIX-YYYY-NNNNN`, implement `getNextCode()` trên Entity (copy pattern `BomList::getNextCode()`).

**Skills tự động:** Trước khi thực hiện bất kỳ task nào, quét `.claude/skills/` → đọc tên thư mục → nếu task khớp với tên skill thì đọc `SKILL.md` tương ứng và follow hướng dẫn bên trong. Ví dụ: yêu cầu "tạo SRS" → đọc `.claude/skills/srs-documenter/SKILL.md`, yêu cầu "fix bug" → đọc `.claude/skills/bug-fixer/SKILL.md`.

---

## Quản lý session

**Bắt đầu session mới — bắt buộc theo thứ tự:**
1. Đọc `.plans/STATUS.md`
2. Tìm feature đang ở mục "Đang làm"
3. Đọc `.plans/[feature]/design.md` + `plan.md`
4. Báo lại: "Đang làm [feature], checkpoint cuối: [X], task tiếp theo: [Y]"
5. Chờ xác nhận trước khi bắt đầu


**Khi nhận yêu cầu làm tiếp / cập nhật feature đã có — theo thứ tự:**
1. Cập nhật `STATUS.md` → chuyển feature về "Đang làm"
2. Đọc lại toàn bộ `.plans/[feature-name]/` (design.md + plan.md)
3. Kiểm tra branch:
   - Feature đã merge vào nhánh hiện tại → hỏi có tạo branch mới để update không? (cả API và Client)
   - Feature vẫn ở branch riêng → hỏi có chuyển về branch đó để làm tiếp không? (cả API và Client)
4. Yêu cầu nhập spec để brainstorming yêu cầu mới

**Khi nhận yêu cầu "tạo tính năng mới" / "tạo feature" — làm NGAY:**
1. Tạo folder `.plans/[feature-name]/`
2. Tạo file `design.md` (placeholder, sẽ fill sau brainstorming)
3. Tạo file `plan.md` (placeholder, sẽ fill sau khi lên plan)
4. Cập nhật `STATUS.md` → thêm vào "Đang làm"
5. Sau đó mới bắt đầu brainstorming / hỏi yêu cầu

**Khi nhận yêu cầu mới (feature/fix/task) — BẮT BUỘC trước khi code:**
1. Cập nhật `.plans/[feature]/plan.md` với danh sách task cụ thể
2. Đánh `[x]` khi xong mỗi task
3. Kể cả fix bug nhỏ cũng phải có task trong plan.md

**Khi nghe "wrap up" — làm ngay 4 việc theo thứ tự:**
1. Cập nhật `plan.md` — đánh `[x]` task xong, ghi checkpoint
2. Cập nhật `STATUS.md` — trạng thái feature hiện tại
3. Nếu là lần wrap up đầu tiên của feature (design.md còn trống hoặc chỉ có placeholder) → cập nhật `design.md` đầy đủ dựa trên hiểu biết đã tích luỹ trong session (scope, data structure, UI, business rules, API endpoints)
4. Báo ra chat: "Đã cập nhật xong. Bước tiếp theo: [X]"

Không làm gì khác cho đến khi 3 việc này xong.

**Checkpoint format bắt buộc:**
```
### Checkpoint — [timestamp]
Vừa hoàn thành: [task vừa xong]
Đang làm dở: [file + dòng + dừng ở đâu]
Bước tiếp theo: [hành động cụ thể]
Blocked: [để trống nếu không có]
```

**Quy tắc STATUS.md — chỉ cập nhật khi có 1 trong 4 sự kiện:**
1. Tạo feature mới → thêm vào "Đang làm"
2. Nghe "wrap up" → cập nhật Checkpoint
3. Chuyển feature → move giữa các mục
4. Merge xong → move vào "Hoàn thành", giữ tối đa 3 entry

---

## Quy tắc team

- `CLAUDE.md`, `.claude/skills/`, `docs/` là tài sản chung — sửa qua PR, không tự ý sửa
- Mỗi dev KHÔNG tạo CLAUDE.md, .claude/skills/, docs/ riêng
- Mỗi feature trong `.plans/` ghi rõ người phụ trách (`@username`)
- Muốn thêm skill mới → tạo PR với SKILL.md đầy đủ
- Dev mới vào → đọc `docs/onboarding.md` trước

---

## Custom skills

Các skill tùy chỉnh nằm trong `.claude/skills/`.
Trước khi implement bất kỳ pattern lặp lại nào,
kiểm tra `.claude/skills/` xem đã có SKILL.md chưa.
Nếu có → đọc trước khi viết code.

---

## Lưu ý fix bug

Lỗi BE → đọc log tại:
`hrm-api/storage/logs/laravel-[ngày-hôm-nay].log`

---
## Khi làm việc với git
- Repo API nằm ở: /hrm-api
- Repo Client nằm ở: /hrm-client

## Không làm

- Không commit hay push git khi chưa có yêu cầu
- Không đọc file trong `vendor/`, `node_modules/`
- Không tự sửa hàm dùng chung khi chưa được xác nhận
- Không tự quyết định điều kiện `is_can_delete` — phải hỏi
- Không tự thêm phân quyền theo cấp — phải hỏi
