# HRM Project — Hướng dẫn cho AI

## Scope thư mục

> **Thư mục gốc của dự án HRM là `HRM/`** (chứa file CLAUDE.md này).
> Tất cả đường dẫn tương đối trong file này (`.plans/`, `docs/`, `.claude/`, `hrm-api/`, `hrm-client/`, `Modules/`, `pages/`) đều tính từ thư mục `HRM/`, KHÔNG phải từ thư mục cha `ERP-HRM/`.
> Khi tạo file, đọc file, hay thao tác git — luôn thực hiện bên trong `HRM/`.

---

## Nguyên tắc chung

- Luôn gợi ý và làm việc bằng tiếng Việt
- Không xử lý commit hay đẩy code lên git
- Không đọc file thư viện hệ thống — tốn token không cần thiết
- Ưu tiên dùng helper có sẵn, tạo helper mới nếu logic dùng lại nhiều nơi
- Khi cần sửa hàm dùng chung → hỏi ý kiến trước khi làm
- **BẮT BUỘC rà project trước khi làm bất kỳ UI/logic nào — không tự phát minh kiểu mới.** Trước khi code 1 thành phần (icon, tooltip, popup, badge/chip, bảng, filter, upload, phân trang, xác nhận xoá, kéo thả, biểu đồ, export…) phải **grep xem trong project đã có chỗ nào làm chưa, kể cả ở phân hệ/chức năng khác**, rồi **copy đúng pattern đó** hoặc tách ra component dùng chung. Mỗi màn tự làm một kiểu là lỗi, không phải "tuỳ ý thiết kế".
  - Cách rà: grep theo class/tên component đặc trưng (vd `custom-class="info-popover"`, `V2Base`, `draggable`, `BaseConfirmModal`), và quét `.claude/skills/` xem đã có SKILL.md quy định chưa.
  - Đã có ≥1 màn làm đúng → **bám theo màn đó**, ghi rõ trong plan.md: "copy pattern từ `<file:dòng>`".
  - Chưa có ở đâu → tự thiết kế, nhưng phải **tách thành component/util dùng chung** ngay từ lần đầu và bổ sung SKILL.md để lần sau không lệch.
  - Phát hiện project đang có **nhiều kiểu khác nhau** cho cùng 1 thứ → nêu ra cho user chọn kiểu chuẩn, KHÔNG tự chọn rồi làm tiếp, cũng KHÔNG tự sửa đại trà các màn cũ.
- **Icon Info (chữ "i") + tooltip mô tả**: dùng `ri-information-line` 14px màu `#94a3b8` + `b-popover` với `custom-class="info-popover"`. KHÔNG dùng `fa-info-circle`, không tự vẽ vòng tròn chữ `i`, không dùng `title=""` thuần, không dùng `v-b-tooltip`. Chi tiết + trường hợp icon nằm trong dropdown select2: `.claude/skills/info-icon-tooltip/SKILL.md`
- FE: Tuân thủ style list của module đang triển khai (mỗi module có thể khác nhau)
- FE: Select trong modal/popup BẮT BUỘC dùng `V2BaseSelectInModal` thay cho `V2BaseSelect` (chi tiết xem `.claude/skills/modal-popup/SKILL.md`)
- Trước khi làm màn danh sách mới → hỏi có cần phân quyền theo cấp không
- Trước khi viết accessor `is_can_delete` → hỏi điều kiện xóa cụ thể của màn đó
- Mọi form có validate: BE phải rethrow `ValidationException` (không catch chung `Exception`), FE phải hiện lỗi inline tại từng input required (viền đỏ `is-invalid` + text lỗi `invalid-feedback`), dùng flag `touched` để chỉ hiện sau lần submit đầu (áp dụng cho màn cũ)
- **Màn MỚI: validate realtime bằng `vee-validate` gắn trên component `V2Base*`** — chỉ trường **Tên** mới gắn `required` ở FE (vì Lưu nháp không được chặn các trường khác), required còn lại do BE quyết theo `status` rồi trả 422 → FE map vào `formError`. Chi tiết: `.claude/skills/form-validate/SKILL.md`
- **Cờ phân quyền phải fail-closed (KHÔNG BAO GIỜ hard-code `= true`)**: mọi cờ quyền FE (`canViewCostPrice`, `canEdit`, `canDelete`, `can_view_*`,…) BẮT BUỘC khởi tạo mặc định `false` và chỉ set từ `$store.state.permissions` (quyền thật) hoặc field BE trả về. TUYỆT ĐỐI không gán literal `true` cho cờ quyền (kể cả ở màn tạo mới / khi "chưa có data") — đây là lỗ hổng fail-open làm lộ dữ liệu nhạy cảm (vd giá vốn). Nếu màn tạo mới cần hiện dữ liệu do user tự nhập, dùng cờ nghiệp vụ riêng (vd `hasUserCreatedProducts`), KHÔNG bật cờ quyền. BE: mọi endpoint trả dữ liệu nhạy cảm (giá vốn/cost, lương…) phải gate bằng `isCurrentEmployeeHasPermission('<Tên quyền>')` trước khi trả, trả `null` nếu không quyền — không dựa vào FE ẩn (defense-in-depth). Khi review: chặn pattern `can[A-Za-z]*\s*=\s*true`.
- **Mọi popup XÁC NHẬN dùng đúng 1 component `components/modal/base-confirm-modal.vue`** (Xóa, Khóa/Mở khóa, Duyệt/Từ chối, Hủy, thoát khi chưa lưu…). Gọi từ code ngoài template thì dùng `await this.$confirm({...})` — plugin render chính component đó. TUYỆT ĐỐI không tạo confirm riêng cho từng màn và không dùng `$bvModal.msgBoxConfirm()`. Chi tiết: `.claude/skills/modal-popup/SKILL.md` mục 3a
- **Mọi màn form (Tạo mới/Sửa) phải cảnh báo khi thoát lúc chưa lưu** — dùng mixin có sẵn `@/utils/mixins/unsavedChangesMixin`, gọi `markFormSaved()` sau khi lưu thành công; KHÔNG tự viết `beforeRouteLeave` riêng. Chi tiết: `.claude/skills/unsaved-changes/SKILL.md`
- **Mọi thông báo nghiệp vụ (chuông/push/socket) theo template `[PREFIX] {Nhóm hành động}: {Tên đối tượng}. {Ghi chú}`** — tên đối tượng ≤ 50 ký tự và in đậm, tổng ≤ 120 ký tự, deep-link bắt buộc kèm ID. Chi tiết + bảng prefix/nhóm hành động: `.claude/skills/notification-convention/SKILL.md` (đọc trước khi code phần có thông báo)
- **Bản ghi ĐÃ KHOÁ thì KHÔNG cho sửa/xoá nữa — chặn ở BE, không chỉ ẩn nút ở FE** (áp cho mọi màn, mọi module: danh mục, khách hàng, phiếu, dự án…). Muốn sửa thì phải Mở khoá trước.
  - **BE (bắt buộc, là chốt chặn thật)**: mọi endpoint `update` / `destroy` / thao tác đổi dữ liệu phải kiểm tra trạng thái khoá NGAY ĐẦU HÀM, trước cả validate nghiệp vụ → trả `423 LOCKED` kèm message rõ ("Bản ghi đang bị khoá, vui lòng mở khoá trước khi cập nhật."). Đặt điều kiện trong 1 accessor/method của Entity (vd `isLocked()` / `isCanEdit()`) rồi dùng lại, KHÔNG rải `if ($x->status == ...)` khắp controller.
    - ⚠️ **Controller nhận `FormRequest` thì `if` ở đầu hàm KHÔNG chạy trước validate** — Laravel validate ngay lúc resolve tham số, payload thiếu trường sẽ trả `422` và guard không bao giờ tới lượt. Trường hợp này phải đặt guard ở **middleware route** (khuôn `CheckCustomerNotLocked` / `CheckServiceNotLocked`, alias `customerNotLocked` / `serviceNotLocked`), KHÔNG gắn cho route mở khoá và route chỉ đọc.
    - **Chặn update thì phải có lối MỞ KHOÁ** — màn nào chưa có thao tác mở khoá thì bổ sung endpoint + nút, nếu không bản ghi bị khoá sẽ kẹt vĩnh viễn.
  - **FE**: ẩn (KHÔNG disable) nút Sửa, Xoá và mọi nút thao tác đổi dữ liệu khi `is_locked` / `is_can_edit = false`; vào màn Sửa bằng URL trực tiếp thì chuyển về màn Chi tiết. FE chỉ là lớp trải nghiệm — **không được coi là đã chặn**.
  - **Ngoại lệ duy nhất là thao tác Mở khoá** (và các thao tác chỉ đọc: xem, in, export, xem lịch sử).
  - **Ẩn nút phải làm ĐỦ CẢ 2 NƠI**: dòng ở màn danh sách VÀ footer màn chi tiết (xem gạch đầu dòng dưới).
  - Thao tác Khoá/Mở khoá vẫn phải ghi lịch sử (nhóm "Thay đổi trạng thái" — xem `.claude/skills/entity-history/SKILL.md`).
- **Badge trạng thái dùng component chung `V2BaseBadge`**, KHÔNG tự khai `<span class="status-pill">` / class badge riêng cho từng màn (`variant`: `brand` = hoạt động, `required` = khoá/từ chối, `muted` = nháp). Text lấy từ `status_text` BE trả về, không tự map số → chữ ở FE. Khuôn: `pages/customer-care/device-errors/index.vue`. Chi tiết: `.claude/skills/list-page/SKILL.md` mục 3c
- **Nút KHÔNG DÙNG ĐƯỢC thì ẨN HẲN — không hiện rồi disable.** Áp cho MỌI lý do: không có quyền, **và cả** chưa đủ điều kiện nghiệp vụ (đã phát sinh chứng từ, sai trạng thái, đã khoá…). Điều kiện phải nằm trong `visible` / `v-if`, KHÔNG dùng `interactable` + `disabledTitle` để hiện nút xám. Áp cho cả cột Hành động ở màn danh sách lẫn footer màn chi tiết (nút ẩn ở danh sách thì phải ẩn ở chi tiết). Cần cho user biết vì sao không thao tác được thì ghi ở chỗ khác (cột Trạng thái, ghi chú trong form), không giữ nút xám trên giao diện.
- **Màn chi tiết/form: nút BẮT BUỘC đặt trong `V2Footer`**, không tự dựng khối `<div class="d-flex justify-content-end">` + loạt `V2BaseButton`. Hành động không có sẵn trong `V2Footer.menu`, hoặc cần variant/màu khác với mặc định của component, thì đưa vào slot `#custom-actions`. `V2Footer` tự render "Quay lại" ở cuối — đừng tự thêm. Chi tiết: `.claude/skills/list-page/SKILL.md` mục 7.2
- **Tiêu đề màn chi tiết chỉ ghép mã khi bản ghi CÓ mã**: `Chi tiết <đối tượng>: <mã>`. Bảng không có cột mã → để tiêu đề TRẦN, **không lấy tên thay thế** (tên dài làm tiêu đề/tab lê thê mà không giúp định danh).
- **Hành động ở màn CHI TIẾT phải khớp màn DANH SÁCH của đúng bản ghi đó** — giống cả danh sách hành động lẫn **điều kiện hiện/ẩn**. Với cùng 1 bản ghi, số nút ở 2 màn phải bằng nhau (chi tiết chỉ được thiếu "Xem" vì đang ở màn xem, và "Lịch sử" nếu đã có mục Lịch sử nhúng sẵn trong form). Nút ẩn ngoài danh sách mà chi tiết vẫn hiện là SAI. Sai hay gặp: danh sách gate `perm.edit && isActive`, chi tiết chỉ gate `perm.edit`. Điều kiện nên đọc từ cùng 1 nguồn (cờ BE `is_can_edit`/`is_can_delete` hoặc computed dùng chung). **Sửa điều kiện của 1 hành động thì phải kiểm cả 2 nơi trước khi báo xong.** Chi tiết + cách tự kiểm: `.claude/skills/list-page/SKILL.md` mục 7.2
- **Danh mục bị khoá / ngừng hoạt động vẫn phải hiện ở bản ghi đang dùng nó** (nghiệp vụ xuyên suốt MỌI màn, mọi module): dropdown/select lấy từ danh mục (giai đoạn dự án, loại hình, lĩnh vực, nguồn khách hàng, phòng ban, chức danh…) mặc định chỉ liệt kê bản ghi còn hoạt động (`is_active = 1` / chưa khoá), NHƯNG khi mở màn Sửa/Chi tiết của đối tượng đã chọn giá trị nay bị khoá thì giá trị đó BẮT BUỘC vẫn là 1 option và hiển thị đúng tên — không được để select trống, không tự đổi sang giá trị khác, không mất dữ liệu khi lưu lại.
  - **BE**: API danh mục nhận thêm id đang dùng (vd `include_ids` / `current_id`) → `where('is_active', 1)->orWhereIn('id', $includeIds)`. Nếu không sửa được API danh mục thì Resource của đối tượng phải trả kèm object danh mục đang chọn (id + name) để FE merge.
  - **FE**: sau khi load options, nếu `form.xxx_id` có giá trị mà không có trong options → push object đang chọn (lấy từ data detail) vào mảng options. Hiển thị **đúng tên gốc**, KHÔNG thêm hậu tố kiểu `(đã khoá)` vào text.
  - **Đánh dấu bằng 🔒 — TỰ ĐỘNG**: BE trả cờ `is_locked`, FE **không phải khai gì**: `utils/select2LockedOption.js` đã được `V2BaseSelect` + `V2BaseSelectInModal` gọi sẵn, tự gắn `🔒 ` trước tên option **chỉ trong danh sách chọn** (chip/giá trị đã chọn giữ tên gốc). KHÔNG nối chữ vào `name`, KHÔNG tự viết `templateResult` ở từng màn. Chi tiết: `.claude/skills/list-page/SKILL.md` mục 11.
  - Áp dụng cả cho filter màn danh sách (giá trị đang lọc/đã lưu), cột hiển thị trong bảng và màn in/export.
- **Code phải TỐI ƯU HIỆU NĂNG, không phải "chạy được là xong"** — mọi màn/API viết ra đều phải cân nhắc số request, số query, khối lượng dữ liệu trả về. Cụ thể:
  - **FE: 1 màn = càng ít API càng tốt.** Không bắn hàng loạt API rời rạc lúc mở màn — gom danh mục dùng chung vào 1 endpoint tổng hợp (vd `GET .../form-options`) hoặc trả kèm trong API detail. TUYỆT ĐỐI không gọi API trong vòng lặp / trong `v-for` (mỗi dòng 1 request).
  - **Lazy load**: danh mục chỉ dùng ở tab/modal/select chưa mở → chỉ gọi khi mở, không gọi ở `mounted`. Select danh mục lớn (khách hàng, nhân viên, hàng hoá…) dùng search server-side có `limit`, KHÔNG load toàn bộ danh sách.
  - **Cache & huỷ request**: danh mục ít thay đổi (phòng ban, chức danh, đơn vị tính…) lưu Vuex/localStorage, không gọi lại mỗi lần vào màn. Ô tìm kiếm gõ liên tục → debounce ≥ 300ms + cancel request cũ.
  - **BE: cấm N+1 query** — luôn `with()` / `load()` eager load quan hệ dùng trong Resource; đếm/tổng hợp bằng `withCount` / `selectRaw`, không loop `->count()` từng dòng.
  - **Luôn phân trang**, không trả cả bảng. KHÔNG dùng `per_page` khổng lồ (5000…) — có endpoint `search?limit=` thì dùng. Chỉ `select` cột thực sự cần, không `SELECT *` rồi map.
  - **Index DB**: cột dùng `where` / `join` / `order by` thường xuyên phải có index; thêm bảng mới hoặc filter mới → kiểm tra index trước khi bàn giao.
  - Xử lý nặng (export, tính lương, tổng hợp báo cáo) → queue/job hoặc chunk, không chạy đồng bộ trong request.
  - Khi review/bàn giao: 1 màn gọi > 5 API lúc load, hoặc 1 request > 2s → phải nêu ra và đề xuất phương án gộp/tối ưu, không im lặng cho qua.
- `.claude`, `.plans`, `docs`, `CLAUDE.md` là symlink sang `hrm-claude-config/` — ghi file vào các path này bình thường, KHÔNG cần hỏi xác nhận

---

## Tech Stack

|                |                                               |
| -------------- | --------------------------------------------- |
| **Backend**    | PHP 7.4, Laravel 8 (`^8.65`), MySQL, Redis    |
| **Auth**       | JWT (`tymon/jwt-auth ^1.0`) + Laravel Sanctum |
| **Permission** | `spatie/laravel-permission ^5.4`              |
| **Module**     | `nwidart/laravel-modules ^8.2`                |
| **Excel**      | `maatwebsite/excel ^3.1`                      |
| **Storage**    | AWS S3                                        |
| **Frontend**   | Nuxt 2.14 (Vue 2), Node 14.21.3               |
| **CSS**        | Bootstrap 4 + Bootstrap-Vue 2.15              |
| **State**      | Vuex 3.5                                      |
| **HTTP**       | @nuxtjs/axios                                 |
| **Date**       | dayjs, vue2-datepicker                        |
| **Editor**     | Quill, CKEditor 5                             |
| **Chart**      | ApexCharts, Highcharts, Chart.js              |

---

## Kiến trúc Module

| #   | Module                      | Backend             | Frontend          |
| --- | --------------------------- | ------------------- | ----------------- |
| 1   | Hành chính nhân sự          | `Modules/Human`     | `pages/human`     |
| 2   | Chấm công                   | `Modules/Timesheet` | `pages/timesheet` |
| 3   | Tính lương                  | `Modules/Payroll`   | `pages/payroll`   |
| 4   | Đào tạo                     | `Modules/Training`  | `pages/training`  |
| 5   | Giao việc ← đang phát triển | `Modules/Assign`    | `pages/assign`    |
| 6   | Quyết định                  | `Modules/Decision`  | `pages/decision`  |
| 7   | CRM                         | `Modules/CRM`       | `pages/client`    |

---

## Tài liệu chi tiết

| Cần gì                                           | Đọc file nào                                |
| ------------------------------------------------ | ------------------------------------------- |
| Base classes, V2Base components, API store calls | `docs/shared.md`                            |
| Pattern CRUD đầy đủ (code mẫu)                   | `docs/conventions.md`                       |
| Onboarding dev mới                               | `docs/onboarding.md`                        |
| Design + Plan của từng feature                   | `.plans/[feature]/` (xem quy luật bên dưới) |

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
- **Permission**: Khi thêm/sửa/đổi tên/xóa permission → sửa trực tiếp trong file `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`. KHÔNG tạo migration riêng cho permission.
- **Middleware checkPermission**: Khi có quyền tương ứng trong `PermissionsTableSeeder`, các route thao tác dữ liệu (store, update, destroy, approve, toggle,...) phải gắn middleware `checkPermission:TênQuyền`. Route xem (index, show) chỉ gắn nếu có quyền xem riêng. Cú pháp: `->middleware('checkPermission:Tên quyền')`, nhiều quyền dùng `|`: `->middleware('checkPermission:Quyền A|Quyền B')`. Không gắn middleware nếu chưa có quyền tương ứng trong seeder.

**Skills tự động:** Trước khi thực hiện bất kỳ task nào, quét `.claude/skills/` → đọc tên thư mục → nếu task khớp với tên skill thì đọc `SKILL.md` tương ứng và follow hướng dẫn bên trong. Ví dụ: yêu cầu "tạo SRS" → đọc `.claude/skills/srs-documenter/SKILL.md`, yêu cầu "fix bug" → đọc `.claude/skills/bug-fixer/SKILL.md`.

---

## Quy luật tổ chức tài liệu feature

Tất cả tài liệu của 1 feature nằm trong `.plans/[feature]/`. KHÔNG tạo file trong `docs/superpowers/specs/`.

**Feature nhỏ (1-2 phase):**

```
.plans/[feature]/
├── design.md          ← design duy nhất
├── plan.md            ← plan duy nhất
├── SRS - <Tên màn hình>.docx ← SRS (tạo khi được yêu cầu, CHỈ 1 file .docx)
└── testcase.xlsx      ← Test case Excel (tạo khi được yêu cầu)
```

**Feature lớn (3+ phase):**

```
.plans/[feature]/
├── design.md          ← tóm tắt tổng thể feature (scope, hiện trạng, quyết định chung)
├── design-phase{N}.md ← design chi tiết cho từng phase lớn
├── plan.md            ← TẤT CẢ tasks (append phase mới vào cuối, trước checkpoint)
├── SRS - <Tên màn hình>.docx ← SRS (tạo khi được yêu cầu, CHỈ 1 file .docx)
├── testcase.xlsx      ← Test case Excel (tạo khi được yêu cầu)
└── (các file phụ: testcase, script...)
```

**Quy tắc:**

- `design.md`: tóm tắt chung, KHÔNG chứa spec chi tiết từng phase
- `design-phase{N}.md`: spec đầy đủ (DB, BE, FE, edge cases) — tạo khi phase có nhiều thay đổi
- `plan.md`: 1 file duy nhất chứa tất cả phase, append liên tục
- SRS: **CHỈ 1 file `.docx`** đặt tên `SRS - <Tên màn hình>.docx`, lưu cùng folder feature. Bám **form chuẩn của team** (`.claude/skills/srs-documenter/assets/SRS_MAU.docx`) — biểu đồ Use Case phải là **ảnh thật**; mục Layout màn hình của **mỗi chức năng** ghi đường dẫn vào màn **VÀ kèm ảnh chụp thật** của chức năng đó (đổi 2026-08-13 — trước kia chốt bỏ ảnh, nay đưa lại theo bản mẫu). Bắt buộc đọc `.claude/skills/srs-documenter/SKILL.md` trước khi viết. (`srs.html` là format CŨ, chỉ còn ở feature sinh trước 2026-08-07, không tạo mới)
- Testcase: chỉ Excel (`testcase.xlsx`) — lưu cùng folder feature
- KHÔNG tạo `plan-phase{N}.md` riêng (đã có convention cũ nhưng không tiếp tục)

---

## ⚠️ Phần GỘP DATABASE — nhánh `gop_db` (bắt buộc cả team)

### 0. Cách nhận biết — NHÌN VÀO NHÁNH GIT, không đoán theo tên feature

**Bước bắt buộc trước mọi task đụng tới code:** kiểm tra nhánh đang đứng ở repo đang sửa.

```bash
git branch --show-current                              # nhánh hiện tại
git merge-base --is-ancestor gop_db HEAD && echo GOPDB # nhánh có checkout ra từ gop_db không
```

- Đang ở **`gop_db`**, hoặc nhánh **checkout ra từ `gop_db`** (lệnh trên in `GOPDB`) → **áp dụng toàn bộ mục 1-3 dưới đây**: tài liệu vào `.plans/gop-db/`, spec vào `docs/superpowers/specs/gop-db/`
- Đang ở nhánh khác (`tpe`, `tpe-develop-assign`, `main`…) → làm theo quy luật thường ở mục trên, tài liệu để `.plans/[feature]/`
- Nhánh không suy ra được (worktree lạ, detached HEAD) → **hỏi** trước khi tạo folder tài liệu, đừng đoán

### 1. Tài liệu — thêm 1 cấp `gop-db/`

```
.plans/gop-db/
├── STATUS.md                    ← STATUS RIÊNG của phần gộp DB (Đang làm / Tạm dừng / Hoàn thành)
├── design.md                    ← NỀN TẢNG chung của việc gộp DB (đọc TRƯỚC khi làm bất kỳ feature nào)
├── [feature-a]/design.md + plan.md
├── [feature-b]/design.md + plan.md
└── ...
docs/superpowers/specs/gop-db/YYYY-MM-DD-<feature>-design.md   ← spec chi tiết (cũng thêm 1 cấp gop-db/)
```

- Code đang làm trên nhánh `gop_db` (hoặc nhánh con của nó) → **KHÔNG** tạo folder ở `.plans/[feature]/` mà tạo ở **`.plans/gop-db/[feature]/`**, kể cả khi tên feature nghe không liên quan gì tới database (VD: `finance-account-catalog`)
- Ngược lại, nhánh khác → vẫn để ở `.plans/[feature]/` như cũ
- **STATUS riêng**: mọi cập nhật trạng thái (tạo feature mới, `wrap up`, chuyển mục, merge xong) ghi vào **`.plans/gop-db/STATUS.md`**, KHÔNG ghi vào `.plans/STATUS.md`. File gốc chỉ giữ 1 khối con trỏ sang đây
- Đầu session, nếu đang đứng trên nhánh `gop_db` → đọc **`.plans/gop-db/STATUS.md`** thay cho `.plans/STATUS.md`
- Cấu trúc bên trong mỗi feature giữ nguyên quy luật ở mục trên (design.md / plan.md / srs / testcase)

### 2. Code — luôn đứng trên nhánh `gop_db`

- Code của phần này **chỉ làm trên nhánh `gop_db`**, hoặc nhánh con **checkout ra từ `gop_db`** (KHÔNG checkout từ `tpe`, `tpe-develop-assign`, `main`)
- Xong việc → merge/PR **về lại `gop_db`**, không merge thẳng sang nhánh khác
- Trước khi code: kiểm tra nhánh hiện tại ở CẢ 2 repo (`git branch --show-current`); đứng sai nhánh thì `Modules/Finance`, `components/subsystems.js`, `pages/finance`… sẽ không tồn tại
- Mỗi người tự chọn cách làm việc trên nhánh này (checkout thẳng hay dùng git worktree riêng) — không bắt buộc theo ai. Nếu dùng worktree: worktree KHÔNG có `.plans/`, `.claude/`, `docs/`, `CLAUDE.md` (là symlink ra ngoài repo) → **tài liệu luôn ghi về `HRM/.plans/gop-db/`**, worktree chỉ chứa code

### 3. Ràng buộc thường trực trên nhánh `gop_db`

- **KHÔNG dùng `DB_CONNECTION_SECOND` / connection `mysql2`** cho bất kỳ tính năng mới nào, kể cả ghép tiền tố tên bảng bằng `env('DB_DATABASE_SECOND')` trong constructor model — `mysql2` đang trỏ DB ERP CŨ, id lệch
- Bảng trùng tên: **ưu tiên bản ERP**; bản HRM đã đổi tên thành `hrm_*` (24 bảng). Model con không khai `$table` sẽ đọc nhầm bảng ERP
- Trước khi làm bất kỳ feature nào trong nhóm này → **đọc `.plans/gop-db/design.md`** (7 gotcha khi port màn ERP → HRM)

---

## Quản lý session

**Bắt đầu session mới — bắt buộc theo thứ tự:**

1. Đọc `.plans/STATUS.md` — nếu đang đứng trên nhánh `gop_db` (hoặc nhánh con của nó) thì đọc `.plans/gop-db/STATUS.md`
2. Tìm feature đang ở mục "Đang làm"
3. Đọc `.plans/[feature]/design.md` + `plan.md` (nhánh `gop_db` → `.plans/gop-db/[feature]/`)
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
2. Tạo file `.plans/[feature-name]/design.md` (placeholder, sẽ fill sau brainstorming)
3. Tạo file `.plans/[feature-name]/plan.md` (placeholder, sẽ fill sau khi lên plan)
4. Tạo file `docs/superpowers/specs/YYYY-MM-DD-<feature-name>-design.md` (placeholder, sẽ fill sau brainstorming)
5. Cập nhật `STATUS.md` → thêm vào "Đang làm" (kèm link tới spec chi tiết)
6. Sau đó mới bắt đầu brainstorming / hỏi yêu cầu

**Phân biệt 3 tài liệu của 1 feature:**

- `.plans/[feature]/design.md` — **TÓM TẮT** (1-2 trang): mục tiêu, scope, các quyết định lớn, link sang spec chi tiết
- `.plans/[feature]/plan.md` — task **TỔNG QUÁT** theo Phase → BE/FE (định dạng progress-manager)
- `docs/superpowers/specs/YYYY-MM-DD-<feature>-design.md` — **SPEC ĐẦY ĐỦ**: schema DB, migration script, API contract, validation rule, business rule chi tiết, edge case, downstream impact, UX chi tiết
- Khi brainstorming: fill `docs/superpowers/specs/...` trước (chi tiết) → tóm tắt vào `.plans/[feature]/design.md`
- Khi `wrap up` lần đầu: cả 2 file design phải đầy đủ

**Khi nhận yêu cầu mới (feature/fix/task) — BẮT BUỘC trước khi code:**

1. Cập nhật `.plans/[feature]/plan.md` với danh sách task cụ thể
2. Đánh `[x]` khi xong mỗi task
3. Kể cả fix bug nhỏ cũng phải có task trong plan.md

**Khi nghe "wrap up" — làm ngay 4 việc theo thứ tự:**

1. Cập nhật `plan.md` — đánh `[x]` task xong, ghi checkpoint
2. Cập nhật `STATUS.md` — trạng thái feature hiện tại
3. Nếu là lần wrap up đầu tiên của feature (design.md còn trống hoặc chỉ có placeholder) → cập nhật `.plans/[feature]/design.md` (tóm tắt) VÀ `docs/superpowers/specs/YYYY-MM-DD-<feature>-design.md` (chi tiết đầy đủ) dựa trên hiểu biết đã tích luỹ trong session (scope, data structure, UI, business rules, API endpoints, edge case, downstream impact)
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

**Skill bắt buộc đọc theo ngữ cảnh:**

| Khi làm gì                                          | Đọc skill nào                                |
| --------------------------------------------------- | -------------------------------------------- |
| Tạo/sửa button (nút bấm) trên FE hrm-client         | `.claude/skills/button-convention/SKILL.md`  |
| Tạo/sửa modal, popup, dialog trên FE hrm-client     | `.claude/skills/modal-popup/SKILL.md`        |
| Tạo màn danh sách mới ở hrm-client                  | `.claude/skills/list-page/SKILL.md` (nếu có) |
| Làm code trong project **elearning** (Vue 3 + Vite) | `.claude/skills/elearning-base/SKILL.md`     |
| Validate, error, toast trong elearning              | `.claude/skills/elearning-validate/SKILL.md` |
| Auth, SSO, profile, avatar trong elearning          | `.claude/skills/elearning-auth/SKILL.md`     |
| Viết tài liệu HDSD / hướng dẫn sử dụng màn hình     | `.claude/skills/hdsd-documenter/SKILL.md`    |
| Lịch sử thay đổi / audit log (BE ghi log + UI)      | `.claude/skills/entity-history/SKILL.md`     |
| Viết tài liệu SRS / đặc tả yêu cầu màn hình         | `.claude/skills/srs-documenter/SKILL.md`     |
| Viết tài liệu test case cho màn hình                | `.claude/skills/testcase-documenter/SKILL.md` |
| Bắn/sửa thông báo nghiệp vụ (chuông, push, socket)  | `.claude/skills/notification-convention/SKILL.md` |
| Tạo/sửa màn form (add/edit, modal nhập liệu)        | `.claude/skills/unsaved-changes/SKILL.md`    |
| Validate form ở màn mới (realtime, required, lỗi)   | `.claude/skills/form-validate/SKILL.md`      |
| Icon Info (chữ "i") + tooltip/popover mô tả         | `.claude/skills/info-icon-tooltip/SKILL.md`  |

→ Gặp ngữ cảnh trên → **đọc SKILL.md trước khi viết code**, không cần user nhắc.

**Nguyên tắc viết tài liệu hướng dẫn (HDSD):** Phải CỰC KỲ CHI TIẾT, click-by-click tới từng hành động nhỏ. Liệt kê nút thôi là CHƯA ĐỦ — mỗi nút Tạo mới/Sửa/Duyệt/Nhập kết quả/Xóa… phải mô tả form mở ra, **từng trường nhập (bắt buộc + giá trị mặc định/điền sẵn)**, cách lưu, kết quả. Ảnh **chụp thật** từ hệ thống (Playwright MCP). Theo `.claude/skills/hdsd-documenter/SKILL.md`.

---

## Lưu ý fix bug

Lỗi BE → đọc log tại:
`hrm-api/storage/logs/laravel-[ngày-hôm-nay].log`

---

## Khi làm việc với git
- Repo API nằm ở: /hrm-api
- Repo Client nằm ở: /hrm-client

---

## ⚠️ Line ending — GIỮ NGUYÊN CRLF

Nhiều file trong `hrm-client` (và một số file `hrm-api`) đang dùng **CRLF (`\r\n`)**. Khi sửa code **KHÔNG được đổi line ending của file** — đổi cả file sang LF làm diff phình lên hàng nghìn dòng giả, che mất thay đổi thật và gây conflict vô nghĩa khi merge.

- **Kiểm tra trước khi sửa** file lạ: `file <path>` (thấy `with CRLF line terminators`) hoặc `grep -c $'\r' <path>`
- File đang CRLF → dòng **mới thêm vào cũng phải kết thúc bằng `\r\n`**, KHÔNG trộn 2 kiểu trong 1 file
- **Nguy hiểm nhất là sửa hàng loạt bằng script** (Python `open().write()`, `sed -i`, `awk`, prettier/eslint `--fix`): mặc định ghi ra LF → nuốt sạch `\r` toàn file. Dùng Python thì mở `newline=''` cho cả đọc lẫn ghi
- Sau khi sửa bằng script, **luôn chạy `git diff --stat` kiểm tra**: số dòng thay đổi lớn bất thường (cả file bị đánh dấu đổi) = đã phá line ending → trả lại ngay, không commit đè
- KHÔNG tự ý thêm `.gitattributes`, đổi `core.autocrlf`, hay "chuẩn hoá toàn bộ repo về LF" — muốn làm phải hỏi trước

## Không làm

- Không commit hay push git khi chưa có yêu cầu
- Không đọc file trong `vendor/`, `node_modules/`
- Không tự sửa hàm dùng chung khi chưa được xác nhận
- Không tự quyết định điều kiện `is_can_delete` — phải hỏi
- Không tự thêm phân quyền theo cấp — phải hỏi

---


