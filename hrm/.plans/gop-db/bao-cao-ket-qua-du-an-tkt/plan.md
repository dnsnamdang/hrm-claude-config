# Báo cáo kết quả thực hiện Dự án TKT — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: dùng `superpowers:subagent-driven-development`
> (khuyến nghị) hoặc `superpowers:executing-plans` để thực thi plan này theo từng task.
> Các bước dùng cú pháp checkbox (`- [ ]`) để theo dõi.

**Goal:** Dựng màn báo cáo mới `/assign/report/prospective-project-results` — theo dõi kết quả thực
hiện Dự án TKT trong kỳ (Thành công / Thất bại / Đang triển khai) trên 3 trục cắt: Phòng ban ·
Thị trường · Lĩnh vực Công ty KD.

**Architecture:** Port nguyên kiến trúc màn `potential-customer-care` đang chạy thật (service dựng
cây đệ quy + popup drill-down + bản in + Excel). Tập dự án vào báo cáo xác định bằng **trạng thái tại
đầu kỳ** đọc từ `prospective_project_status_logs` (tính hàng loạt, không N+1); 3 nhóm kết quả suy
thẳng từ `status` tại cuối kỳ. Không đụng màn báo cáo TKT cũ.

**Tech Stack:** PHP 7.4 / Laravel 8 (`Modules/Assign`), MySQL · Nuxt 2.14 / Vue 2 + Bootstrap-Vue 2.15
(`hrm-client`) · Playwright (`HRM/e2e`, chạy bằng Node 20).

**Spec:** `docs/superpowers/specs/gop-db/2026-09-13-bao-cao-ket-qua-du-an-tkt-design.md`
**Design UI + logic gốc:** `.plans/gop-db/bao-cao-ket-qua-du-an-tkt/design.md` + `logic-bao-cao.md`
**Mockup đã duyệt:** `.plans/gop-db/bao-cao-ket-qua-du-an-tkt/bao-cao-ket-qua-du-an-tkt.html`

---

## Global Constraints

Áp cho **MỌI** task, không nhắc lại ở từng task.

- **Nhánh**: nhánh con tách từ `tpe` ở CẢ 2 repo. **KHÔNG** checkout từ `gop_db`.
- **Commit: user mở lại ngày 13/09/2026** ("nếu vướng cứ commit nếu cần"), thay cho quyết định
  "không commit" trước đó trong cùng ngày. Quy tắc hiện hành:
  - **Người triển khai (subagent) chỉ `git add`, KHÔNG tự commit.** Commit do người điều phối tạo
    **sau khi review sạch** — để không có commit nào chưa qua review.
  - Commit **cục bộ trên nhánh feature**. ⛔ **KHÔNG `git push`, KHÔNG merge** — 2 việc đó đưa code
    ra ngoài máy này, phải hỏi user trước.
  - `HRM/e2e/` **không thuộc repo nào** → file test không commit được; vẫn dựa vào snapshot.
- **KHÔNG `git stash`** ở `hrm-api` / `hrm-client` — nhiều session Claude chạy song song, stash nuốt
  việc của session khác. Cần cách ly thì dùng worktree.
- **KHÔNG `pkill -f nuxt` / `pkill -f php`** — kill đúng PID theo cổng.
- **Line ending**: nhiều file `hrm-client` là CRLF. Kiểm `file <path>` trước khi sửa; sửa bằng script
  xong phải `git diff --stat` đối chiếu, số dòng đổi bất thường = đã phá line ending.
- **Định dạng số quốc tế**: `,` hàng nghìn, `.` thập phân. FE `Number(x).toLocaleString('en-US')`;
  BE `number_format($x, $precision)`. **CẤM** `toLocaleString('vi-VN')` cho số và
  `number_format($x, 0, ',', '.')`. Ngày vẫn `dd/mm/yyyy`.
- **Excel**: ô số là **số thật** + `data-format="#,##0"`. Ô không có giá trị để **RỖNG**, không ghi 0.
- **Mọi element form dùng `V2Base*`**; select trong modal dùng `V2BaseSelectInModal`. Tự kiểm:
  `grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/assign/report/prospective-project-results/ | grep -v V2Base`
  phải **RỖNG**.
- **`.text-muted` trong hrm-client là màu ĐỎ** — dùng xám `#6b7280`. Chữ đỏ chỉ dành cho lỗi validate.
- **Badge** dùng `V2BaseBadge`, màu do BE trả. 3 nhóm kết quả: Thành công `#16A34A` · Thất bại
  `#DC2626` · Đang triển khai `#2563EB`. Tiến trình = **pill xám trung tính** kèm số bước.
- **Nút không dùng được thì ẨN HẲN**, không disable.
- **Cờ quyền FE fail-closed**: khởi tạo `false`, chỉ set từ `$store.state.permissions`. **Cấm** gán
  literal `true` (chặn pattern `can[A-Za-z]*\s*=\s*true`).
- **Cấm N+1**: eager load `scope`, `industry`, `closedReason`, nhân viên; batch resolve tỉnh/TP.
  Popup luôn phân trang.
- **Model mới** (nếu có) `extends BaseModel`, `created_by`/`updated_by` trong `$fillable`.
  Luôn `auth()->id()`, **không** `auth()->user()->info->id`.
- **Icon ⓘ**: `ri-information-line` 14px `#94a3b8` + `b-popover custom-class="info-popover"`.
  **Không** `fa-info-circle`, không `title=""`, không `v-b-tooltip`.
- **Chạy e2e phải `--workers=1`** (2 worker tranh 1 Nuxt dev server gây đỏ ngẫu nhiên):
  ```bash
  cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test <spec> --workers=1
  ```
  Cần sẵn API `:8000` và client `:3000`. Bộ test chạy `serial` — **một ca fail làm mọi ca sau in
  "did not run", KHÔNG phải "passed"**. Phải đọc dòng tổng kết.
- **Playwright MCP luôn mở `http://127.0.0.1:3000`**, KHÔNG `localhost:3000` (token nằm trong
  localStorage của origin `127.0.0.1`).
- **Task đụng giao diện BẮT BUỘC verify Playwright, ĐO BẰNG SỐ LẤY TỪ DOM** (toạ độ, bề rộng,
  `getComputedStyle`, số phần tử) — "nhìn có vẻ ổn" không được tính là đã kiểm.

---

## File Structure

### `hrm-api` — `Modules/Assign/`

| File | Trách nhiệm |
|---|---|
| `Database/Migrations/2026_09_13_000001_fix_backfill_prospective_project_status_logs.php` | Vá log cho dự án Thất bại lập trước 18/05/2026 |
| `Services/Report/ProspectiveProjectResultReportService.php` | Toàn bộ tính toán: tập dự án, 3 nhóm kết quả, các chiều, cây, dải tổng hợp, drill, filter-options |
| `Services/Report/ProspectiveProjectResultPrintService.php` | Dựng dữ liệu bản in + letterhead theo `company_id` **ghi trên chứng từ** |
| `Http/Controllers/Api/V1/ProspectiveProjectResultReportController.php` | 6 endpoint, mỏng — không chứa logic |
| `Transformers/ProspectiveProjectResultResource/ProjectRowResource.php` | 1 dòng dự án trong popup |
| `Routes/api.php` | +6 route |
| `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` | +3 quyền 1184–1186 |
| `database/e2e_tkt_result_report_seed.php` | Fixture e2e, idempotent |

### `hrm-client` — `pages/assign/report/prospective-project-results/`

| File | Trách nhiệm |
|---|---|
| `index.vue` | Khung màn: toolbar lọc, gọi API, điều phối 3 khối con |
| `components/ResultSummaryBlocks.vue` | Dải tổng hợp 2 khối × 3 ô con + dòng meta |
| `components/ResultTrackingTable.vue` | Bảng theo dõi 10 cột, cây đa cấp, select chọn cấp |
| `components/ProjectListModal.vue` | Popup danh sách dự án + bộ lọc riêng + chip phân bổ + sắp xếp |
| `components/DrillNum.vue` | Ô số bấm được (copy từ màn CSKH) |
| `components/PrintOptionsModal.vue` | Chọn chế độ in (copy từ màn CSKH) |
| `format.js` | Hàm định dạng số/tiền rút gọn dùng chung 3 component |
| `components/menu-sidebar.js` (sửa) | +1 mục menu |

**Dùng lại, KHÔNG port lại**: `components/print/ReportPrintPreviewModal.vue`,
`utils/print/reportPrintStyle.js`, `utils/mixins/reportPrintPreviewMixin.js`,
`components/V2BaseTableScroll.vue`.

### `HRM/e2e/`

| File | Trách nhiệm |
|---|---|
| `utils/tktResultFixture.ts` | Gọi seed PHP qua khoá thư mục (khuôn `careFixture.ts`) |
| `tests/assign/tkt-result-report.api.spec.ts` | Ca API: tập dự án, 2 đẳng thức, phân quyền fail-closed |
| `tests/assign/tkt-result-report.spec.ts` | Ca UI: đo DOM cây, bỏ cột popup, chọn cấp |

---

# Phase 1 — Nền tảng BE

### Task 1: Migration vá log tiến trình cho dữ liệu cũ

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_09_13_000001_fix_backfill_prospective_project_status_logs.php`
- Đọc tham khảo: `hrm-api/Modules/Assign/Database/Migrations/2026_05_18_000002_backfill_prospective_project_status_logs.php`

**Interfaces:**
- Consumes: bảng `prospective_project_status_logs`, `prospective_projects`
- Produces: dữ liệu log đúng cho dự án status 11 lập trước 18/05/2026 — Task 5 (`statusAtBulk`) dựa vào

- [x] **Bước 1: Đo hiện trạng trước khi sửa (bắt buộc — phải tái hiện được vấn đề)**

```bash
cd HRM/hrm-api && PW=$(grep -m2 "^DB_PASSWORD=" .env | tail -1 | cut -d= -f2-)
mysql -h127.0.0.1 -uroot -p"$PW" hrm_erp -t -e "
SELECT COUNT(*) AS du_an_can_va
FROM prospective_projects p
WHERE p.created_at < '2026-05-18'
  AND p.status = 11
  AND p.closed_at IS NOT NULL
  AND IFNULL(p.is_parent_project,0) = 0
  AND (SELECT COUNT(*) FROM prospective_project_status_logs l
       WHERE l.prospective_project_id = p.id) = 1;"
```

Ghi lại con số. **DB local dự kiến trả 0** (dự án sớm nhất 03/07/2026) — đó là kết quả đúng, không
phải lỗi. Production sẽ > 0.

- [x] **Bước 2: Viết migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;

/**
 * Vá bản backfill 2026_05_18_000002: migration đó sinh ĐÚNG 1 dòng log/dự án với
 * changed_at = created_at và status_to = trạng thái HIỆN TẠI. Dự án lập trước 18/05/2026
 * vì thế bị khai là "đã ở trạng thái cuối ngay từ ngày lập" -> statusAt(S) trả trạng thái
 * đóng -> dự án biến mất khỏi báo cáo kết quả dự án TKT mà không có lỗi nào báo ra.
 *
 * Chỉ vá được nhóm THẤT BẠI (status 11) vì chỉ nhóm này có mốc `closed_at`.
 * Dự án Thành công (9/10/12) không có mốc nào để suy ngược — giới hạn đã ghi ở spec mục 3.4.
 *
 * MỘT CHIỀU: down() để rỗng, KHÔNG truncate bảng log (sẽ xoá cả log thật).
 */
class FixBackfillProspectiveProjectStatusLogs extends Migration
{
    /** Bước đầu sau khi dự án được lưu chính thức */
    const STATUS_THU_THAP_THONG_TIN = 2;
    const STATUS_DONG_DU_AN = 11;
    /** Ngày chạy migration backfill gốc — dữ liệu sau mốc này có log thật, TUYỆT ĐỐI không đụng */
    const BACKFILL_DATE = '2026-05-18';

    public function up()
    {
        DB::table('prospective_projects as p')
            ->select('p.id', 'p.closed_at', 'p.closed_by')
            ->where('p.created_at', '<', self::BACKFILL_DATE)
            ->where('p.status', self::STATUS_DONG_DU_AN)
            ->whereNotNull('p.closed_at')
            ->where(function ($q) {
                $q->whereNull('p.is_parent_project')->orWhere('p.is_parent_project', 0);
            })
            ->orderBy('p.id')
            ->chunk(1000, function ($rows) {
                foreach ($rows as $row) {
                    $logs = DB::table('prospective_project_status_logs')
                        ->where('prospective_project_id', $row->id)
                        ->orderBy('id')
                        ->get();

                    // Chỉ chạm dự án còn nguyên dấu vết backfill: đúng 1 dòng, status_from NULL,
                    // status_to = 11. Idempotent: chạy lần 2 thì dự án đã có 2 dòng -> bỏ qua.
                    if ($logs->count() !== 1) {
                        continue;
                    }
                    $log = $logs->first();
                    if ($log->status_from !== null || (int) $log->status_to !== self::STATUS_DONG_DU_AN) {
                        continue;
                    }

                    DB::table('prospective_project_status_logs')
                        ->where('id', $log->id)
                        ->update(['status_to' => self::STATUS_THU_THAP_THONG_TIN]);

                    DB::table('prospective_project_status_logs')->insert([
                        'prospective_project_id' => $row->id,
                        'status_from' => self::STATUS_THU_THAP_THONG_TIN,
                        'status_to'   => self::STATUS_DONG_DU_AN,
                        'changed_at'  => $row->closed_at,
                        'changed_by'  => $row->closed_by,
                        'created_at'  => now(),
                        'updated_at'  => now(),
                    ]);
                }
            });
    }

    public function down()
    {
        // Một chiều — không khôi phục được trạng thái backfill cũ, và KHÔNG được truncate
        // bảng log vì trong đó có log thật của dự án lập sau 18/05/2026.
    }
}
```

- [x] **Bước 3: Chạy migration**

```bash
cd HRM/hrm-api && php artisan migrate
```
Kỳ vọng: `Migrated: 2026_09_13_000001_fix_backfill_prospective_project_status_logs`

- [x] **Bước 4: Kiểm idempotent — chạy lại không đẻ thêm dòng**

```bash
cd HRM/hrm-api && PW=$(grep -m2 "^DB_PASSWORD=" .env | tail -1 | cut -d= -f2-)
mysql -h127.0.0.1 -uroot -p"$PW" hrm_erp -N -e "SELECT COUNT(*) FROM prospective_project_status_logs;"
php artisan migrate:rollback --step=1 && php artisan migrate
mysql -h127.0.0.1 -uroot -p"$PW" hrm_erp -N -e "SELECT COUNT(*) FROM prospective_project_status_logs;"
```
Kỳ vọng: **2 con số bằng nhau**.

- [x] **Bước 5: Kiểm không đụng dữ liệu có log thật**

```bash
cd HRM/hrm-api && PW=$(grep -m2 "^DB_PASSWORD=" .env | tail -1 | cut -d= -f2-)
mysql -h127.0.0.1 -uroot -p"$PW" hrm_erp -t -e "
SELECT COUNT(*) AS log_cua_du_an_moi
FROM prospective_project_status_logs l
JOIN prospective_projects p ON p.id = l.prospective_project_id
WHERE p.created_at >= '2026-05-18';"
```
So với con số đo trước khi chạy migration — **phải bằng nhau**.

---

### Task 2: Ba quyền mới 1184–1186

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (chèn ngay sau dòng quyền `1183`)

**Interfaces:**
- Produces: 3 tên quyền dùng nguyên văn ở Task 6 (`applyPermissionFilter`) và Task 14 (cờ FE):
  - `Xem báo cáo kết quả dự án TKT theo tổng công ty`
  - `Xem báo cáo kết quả dự án TKT theo công ty`
  - `Xem báo cáo kết quả dự án TKT theo phòng ban`

- [x] **Bước 1: Kiểm id còn trống**

```bash
cd HRM/hrm-api && PW=$(grep -m2 "^DB_PASSWORD=" .env | tail -1 | cut -d= -f2-)
mysql -h127.0.0.1 -uroot -p"$PW" hrm_erp -t -e "SELECT id, name FROM permissions WHERE id BETWEEN 1184 AND 1186;"
grep -n "'id' => 118[0-9]" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
```
Kỳ vọng: query DB **rỗng**, seeder max = 1183.

- [x] **Bước 2: Thêm 3 dòng vào seeder**

```php
        // Báo cáo kết quả thực hiện dự án TKT (feature bao-cao-ket-qua-du-an-tkt).
        // Tách khỏi bộ 1054-1056 "Báo cáo tổng hợp dự án TKT" vì màn này chấm thắng/thua
        // theo từng nhân viên -> phải cấp riêng.
        Permission::create(['id' => 1184, 'guard_name' => 'api', 'name' => 'Xem báo cáo kết quả dự án TKT theo tổng công ty', 'display_name' => 'Xem báo cáo kết quả dự án TKT theo tổng công ty', 'group' => 'Báo cáo kết quả dự án TKT', 'type' => 4]);
        Permission::create(['id' => 1185, 'guard_name' => 'api', 'name' => 'Xem báo cáo kết quả dự án TKT theo công ty', 'display_name' => 'Xem báo cáo kết quả dự án TKT theo công ty', 'group' => 'Báo cáo kết quả dự án TKT', 'type' => 4]);
        Permission::create(['id' => 1186, 'guard_name' => 'api', 'name' => 'Xem báo cáo kết quả dự án TKT theo phòng ban', 'display_name' => 'Xem báo cáo kết quả dự án TKT theo phòng ban', 'group' => 'Báo cáo kết quả dự án TKT', 'type' => 4]);
```

- [x] **Bước 3: Insert thủ công vào DB local (KHÔNG chạy seeder)**

⚠️ `PermissionsTableSeeder` **truncate cả bảng `permissions`** — chạy nó trên DB có dữ liệu sẽ mất
sạch phân quyền hiện tại.

```bash
cd HRM/hrm-api && PW=$(grep -m2 "^DB_PASSWORD=" .env | tail -1 | cut -d= -f2-)
mysql -h127.0.0.1 -uroot -p"$PW" hrm_erp -e "
INSERT INTO permissions (id, guard_name, name, display_name, \`group\`, type, created_at, updated_at) VALUES
 (1184,'api','Xem báo cáo kết quả dự án TKT theo tổng công ty','Xem báo cáo kết quả dự án TKT theo tổng công ty','Báo cáo kết quả dự án TKT',4,NOW(),NOW()),
 (1185,'api','Xem báo cáo kết quả dự án TKT theo công ty','Xem báo cáo kết quả dự án TKT theo công ty','Báo cáo kết quả dự án TKT',4,NOW(),NOW()),
 (1186,'api','Xem báo cáo kết quả dự án TKT theo phòng ban','Xem báo cáo kết quả dự án TKT theo phòng ban','Báo cáo kết quả dự án TKT',4,NOW(),NOW());"
```

- [x] **Bước 4: Gán 1184 cho role của tài khoản e2e**

⚠️ `role_has_permissions` cần `company_id` (mặc định `1`).

```bash
cd HRM/hrm-api && PW=$(grep -m2 "^DB_PASSWORD=" .env | tail -1 | cut -d= -f2-)
mysql -h127.0.0.1 -uroot -p"$PW" hrm_erp -e "
INSERT IGNORE INTO role_has_permissions (permission_id, role_id, company_id)
SELECT 1184, role_id, 1 FROM role_has_permissions WHERE permission_id = 1054 GROUP BY role_id;"
mysql -h127.0.0.1 -uroot -p"$PW" hrm_erp -t -e "SELECT permission_id, role_id, company_id FROM role_has_permissions WHERE permission_id = 1184;"
```
Kỳ vọng: ít nhất 1 dòng.

- [x] **Bước 5: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-api && git add Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026).

⚠️ `PermissionsTableSeeder.php` là file **dùng chung toàn hệ thống**, nhiều feature khác cũng sửa.
Chỉ thêm đúng 3 dòng của mình, không định dạng lại phần còn lại của file.

---

### Task 3: Fixture e2e

**Files:**
- Create: `hrm-api/database/e2e_tkt_result_report_seed.php`
- Create: `HRM/e2e/utils/tktResultFixture.ts`
- Đọc tham khảo: `hrm-api/database/e2e_care_report_seed.php`, `HRM/e2e/utils/careFixture.ts`

**Interfaces:**
- Produces: hàm `seedTktResultFixture(): TktResultFixture` cho Task 17/20. Kiểu:
  ```ts
  export type TktResultFixture = {
    company_id: number;
    period: { from: string; to: string };          // 'YYYY-MM-DD'
    project_ids: {
      won_in_period: number;      // lập trước kỳ, tại S chưa đóng, tại E status 9
      lost_in_period: number;     // lập trước kỳ, tại S chưa đóng, tại E status 11 + closed_reason_id
      open_created_before: number;// lập trước kỳ, tại E status 5
      open_created_in: number;    // lập TRONG kỳ, tại E status 4
      closed_before_period: number;// đã đóng TRƯỚC S  -> PHẢI bị loại
      draft: number;              // status 1          -> PHẢI bị loại
      parent: number;             // is_parent_project -> PHẢI bị loại
    };
    dept: { id: number; part_id: number | null };
    employee_id: number;
    province_id: number;
    scope_id: number;
    industry_id: number;
    noperm_email: string;        // KHÔNG có quyền nào trong 1184-1186
    noperm_password: string;
    // R6 (13/09): tài khoản CHỈ có quyền 1185 (theo công ty) — dùng cho ca test chống leo thang
    // phạm vi. Tài khoản e2e mặc định đã có 1184 (tổng công ty) nên `allowedCompanyIds()` trả null
    // và MỌI company_id đều hợp lệ ⇒ chạy ca đó bằng tài khoản mặc định là PASS mà không kiểm
    // được gì (fail-open im lặng).
    company_only_email: string;
    company_only_password: string;
    other_company_id: number | null;  // công ty KHÁC công ty của tài khoản trên; null nếu DB chỉ có 1 công ty
  };
  ```

- [x] **Bước 1: Viết seed PHP — idempotent, mã có tiền tố `E2E-TKTR-`**

Yêu cầu bắt buộc của seed:
- Mọi dự án mang `code` tiền tố `E2E-TKTR-` để dọn được chính xác và không đụng dữ liệu thật.
- **Tự ghi `prospective_project_status_logs`** cho từng dự án theo đúng mốc thời gian mong muốn —
  KHÔNG dựa vào hook `booted()` (hook ghi `changed_at = now()`, không dựng được quá khứ):
  - `won_in_period`: log `(null → 2, changed_at = S - 40 ngày)`, `(2 → 9, changed_at = S + 5 ngày)`
  - `lost_in_period`: log `(null → 2, S - 30 ngày)`, `(2 → 11, S + 10 ngày)` + `closed_at = S + 10 ngày`
  - `open_created_before`: log `(null → 2, S - 20 ngày)`, `(2 → 5, S + 2 ngày)`
  - `open_created_in`: log `(null → 2, S + 3 ngày)`, `(2 → 4, S + 6 ngày)`
  - `closed_before_period`: log `(null → 2, S - 90 ngày)`, `(2 → 11, S - 10 ngày)` + `closed_at = S - 10 ngày`
  - `draft`: log `(null → 1, S + 1 ngày)`
  - `parent`: `is_parent_project = 1`, log `(null → 2, S + 1 ngày)`
- Tất cả dự án trên gán **cùng** `company_id`, `main_sale_department_id`, `main_sale_employee_id`,
  `scope_id`, `industry_id`, và khách hàng có `province_id` xác định — để ca test cắt được theo mọi chiều.
- Tạo 1 tài khoản **không có quyền nào trong 1184–1186** (`noperm_email` / `noperm_password`), và
  tài khoản đó **không** là `main_sale_employee_id` của bất kỳ dự án fixture nào → dùng cho ca
  fail-closed.
- **R6 (13/09) — tạo THÊM 1 tài khoản chỉ có quyền `1185`** (`company_only_email` /
  `company_only_password`), gán đúng 1 quyền đó, hồ sơ nhân sự thuộc **cùng công ty** với các dự án
  fixture. Seed phải tự `INSERT` quyền 1185 vào role của tài khoản này (`role_has_permissions` cần
  `company_id`) vì Task 2 mới chỉ gán 1184.
  Đồng thời trả `other_company_id` = id một công ty **khác** (lấy công ty đầu tiên trong `companies`
  có id khác công ty của tài khoản). DB chỉ có 1 công ty thì trả `null` — ca test tương ứng sẽ tự bỏ qua.
- In ra `json_encode($fixture)` ở cuối để TS đọc.

⚠️ `e2e_provision.php` từng làm **cả bộ test không chạy** vì thiếu `employee_infos.email` (cột
UNIQUE) — tài khoản mới tạo trong seed này phải có `employee_infos.email`.

- [x] **Bước 2: Viết `tktResultFixture.ts` — copy nguyên cơ chế khoá thư mục**

Copy `HRM/e2e/utils/careFixture.ts`, đổi:
- `LOCK_DIR` → `path.join(__dirname, '..', '.auth', 'tkt-result-seed.lock')`
- file seed → `database/e2e_tkt_result_report_seed.php`
- kiểu trả về → `TktResultFixture` ở trên

Giữ nguyên `fs.mkdirSync` làm khoá nguyên tử và ngưỡng khoá mồ côi 60s.

- [x] **Bước 3: Chạy seed 2 lần, kiểm idempotent**

```bash
cd HRM/hrm-api && php database/e2e_tkt_result_report_seed.php > /tmp/fx1.json
php database/e2e_tkt_result_report_seed.php > /tmp/fx2.json
diff /tmp/fx1.json /tmp/fx2.json && echo "IDEMPOTENT OK"
PW=$(grep -m2 "^DB_PASSWORD=" .env | tail -1 | cut -d= -f2-)
mysql -h127.0.0.1 -uroot -p"$PW" hrm_erp -N -e "SELECT COUNT(*) FROM prospective_projects WHERE code LIKE 'E2E-TKTR-%';"
```
Kỳ vọng: `IDEMPOTENT OK`, số dự án = **7** ở cả 2 lần.

- [x] **Bước 4: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-api && git add database/e2e_tkt_result_report_seed.php
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`**.
⚠️ `HRM/e2e/utils/tktResultFixture.ts` **không thuộc repo nào** — không stage, không cần git.

---

# Phase 2 — BE: service tính toán

### Task 4: Khung service — kỳ báo cáo, tập dự án, phân quyền, 7 chiều

> **Ruling R1 (13/09/2026)** — task này GỘP nội dung của 3 task rời trong bản plan đầu
> (khung service · phân quyền · các chiều). Lý do: cả 3 sửa **cùng một file** và phụ thuộc vòng —
> `getProjects()` gọi thẳng `applyCompanyScope()`, `applyPermissionFilter()`, `applyDimensionFilters()`,
> nên commit riêng phần đầu sẽ để lại code gọi hàm không tồn tại. Không reviewer nào duyệt được
> phần này mà từ chối phần kia. **Thứ tự làm: mục 4.1 → 4.2 → 4.3**, commit một lần ở cuối.
>
> #### 4.1 Kỳ báo cáo + tập dự án

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php`
- Đọc tham khảo: `hrm-api/Modules/Assign/Services/Report/PotentialCustomerCareService.php`

**Interfaces:**
- Consumes: `ProspectiveProject`, `prospective_project_status_logs` (Task 1)
- Produces (Task 5–9 gọi lại):
  - `resolvePeriod(Request $r): array` → `[Carbon $from, Carbon $to]`
  - `statusAtBulk(array $projectIds, Carbon $at): array` → `[projectId => int status]`
  - `getProjects(Request $r): Collection` → tập dự án đã lọc + đã gate quyền

- [x] **Bước 1: Viết ca test API thất bại trước**

Tạo `HRM/e2e/tests/assign/tkt-result-report.api.spec.ts` với ca đầu tiên:

```ts
/**
 * E2E API — Báo cáo kết quả thực hiện Dự án TKT.
 *
 * ⚠️ KHÔNG so tổng tuyệt đối của kỳ: DB test còn fixture của feature khác rơi vào cùng kỳ.
 * Thay vào đó kiểm: (a) từng dự án fixture nằm ĐÚNG nhóm · (b) 2 đẳng thức bất biến luôn đúng
 * · (c) dự án bị loại không lọt vào đâu cả · (d) phân quyền fail-closed.
 */
import { test, expect, request, APIRequestContext } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';
import { seedTktResultFixture, TktResultFixture } from '../../utils/tktResultFixture';

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8000';
const STATE_FILE = path.join(__dirname, '..', '..', '.auth', 'api.json');
const REPORT = '/api/v1/assign/report/prospective-project-results';

test.describe.configure({ mode: 'serial' });

let api: APIRequestContext;
let fx: TktResultFixture;

test.beforeAll(async () => {
  fx = seedTktResultFixture();
  api = await request.newContext({
    baseURL: API_BASE,
    storageState: JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8')),
  });
});

test.afterAll(async () => { await api.dispose(); });

function reportUrl(extra: Record<string, string> = {}) {
  const p = new URLSearchParams({
    period: 'custom',
    from: fx.period.from,
    to: fx.period.to,
    company_id: String(fx.company_id),
    criteria: 'dept',
    ...extra,
  });
  return `${REPORT}?${p.toString()}`;
}

test('1. Tập dự án: 4 dự án hợp lệ vào báo cáo, 3 dự án bị loại', async () => {
  const res = await api.get(reportUrl());
  expect(res.status()).toBe(200);
  const body = await res.json();

  const ids: number[] = body.data.debug_project_ids ?? [];
  expect(ids).toContain(fx.project_ids.won_in_period);
  expect(ids).toContain(fx.project_ids.lost_in_period);
  expect(ids).toContain(fx.project_ids.open_created_before);
  expect(ids).toContain(fx.project_ids.open_created_in);

  expect(ids).not.toContain(fx.project_ids.closed_before_period);
  expect(ids).not.toContain(fx.project_ids.draft);
  expect(ids).not.toContain(fx.project_ids.parent);
});
```

⚠️ `debug_project_ids` chỉ trả khi `config('app.debug')` — **không** để lộ trên production.

- [x] **Bước 2: Chạy test để chắc chắn nó ĐỎ**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test tkt-result-report.api --workers=1
```
Kỳ vọng: **FAIL** — `expect(res.status()).toBe(200)` nhận `404` (route chưa có).

- [x] **Bước 3: Viết `resolvePeriod()`**

```php
/** Kỳ báo cáo. Không có mục "Tất cả": mọi chỉ tiêu đều tính theo kỳ. */
private function resolvePeriod(Request $request): array
{
    $period = $request->get('period', 'this_month');
    $now = Carbon::now();

    switch ($period) {
        case 'last_month':    $from = $now->copy()->subMonthNoOverflow()->startOfMonth();   $to = $now->copy()->subMonthNoOverflow()->endOfMonth();   break;
        case 'this_quarter':  $from = $now->copy()->startOfQuarter();                        $to = $now->copy()->endOfQuarter();                       break;
        case 'last_quarter':  $from = $now->copy()->subQuarterNoOverflow()->startOfQuarter();$to = $now->copy()->subQuarterNoOverflow()->endOfQuarter();break;
        case 'this_year':     $from = $now->copy()->startOfYear();                           $to = $now->copy()->endOfYear();                          break;
        case 'last_year':     $from = $now->copy()->subYearNoOverflow()->startOfYear();      $to = $now->copy()->subYearNoOverflow()->endOfYear();     break;
        case 'custom':
            $from = Carbon::parse($request->get('from'))->startOfDay();
            $to   = Carbon::parse($request->get('to'))->endOfDay();
            // Không tự đảo ngày — trả 422 để user biết mình chọn sai (spec mục 9)
            abort_if($to->lt($from), 422, 'Ngày kết thúc phải sau ngày bắt đầu.');
            break;
        default:              $from = $now->copy()->startOfMonth();                          $to = $now->copy()->endOfMonth();                         break;
    }

    return [$from->startOfDay(), $to->endOfDay()];
}
```

- [x] **Bước 4: Viết `statusAtBulk()` — 1 query, KHÔNG dùng `statusAt()` trong vòng lặp**

```php
/**
 * Trạng thái của từng dự án TẠI thời điểm $at, lấy từ bảng log.
 *
 * ⚠️ KHÔNG gọi ProspectiveProject::statusAt() trong vòng lặp — hàm đó chạy 1 query/dự án.
 * Lấy MAX(id) trong nhóm đã lọc changed_at <= $at là đúng vì log chỉ chèn thêm, id tăng dần
 * theo thời gian ghi. Index sẵn có: idx_pp_status_logs_pp_changed_at.
 *
 * Dự án không có dòng log nào <= $at ⇒ KHÔNG có entry trong mảng trả về
 * (nghĩa là "chưa tồn tại tại thời điểm đó").
 *
 * @return array<int,int> [prospective_project_id => status]
 */
private function statusAtBulk(array $projectIds, Carbon $at): array
{
    if (empty($projectIds)) {
        return [];
    }

    $rows = DB::table('prospective_project_status_logs as l')
        ->joinSub(
            DB::table('prospective_project_status_logs')
                ->selectRaw('prospective_project_id, MAX(id) as mid')
                ->where('changed_at', '<=', $at)
                ->whereIn('prospective_project_id', $projectIds)
                ->groupBy('prospective_project_id'),
            't',
            't.mid',
            '=',
            'l.id'
        )
        ->select('l.prospective_project_id', 'l.status_to')
        ->get();

    $map = [];
    foreach ($rows as $row) {
        $map[(int) $row->prospective_project_id] = (int) $row->status_to;
    }

    return $map;
}
```

- [x] **Bước 5: Viết `getProjects()` — TH1 ∪ TH2, trừ dự án cha và bản nháp**

```php
/** Tiến trình đã ngã ngũ tại một thời điểm (Thành công 9/10/12 + Thất bại 11) */
const CLOSED_STATUSES = [9, 10, 11, 12];
const STATUS_DRAFT = 1;

/** Cache tập dự án theo request — getProjects() bị gọi lại ở summary(), buildTree(), projectList() */
private $projectCache = null;
private $projectCacheRequest = null;

/**
 * Tập dự án của kỳ đang xem, đã áp quyền + bộ lọc, đã gắn sẵn các chiều.
 *
 * TH1 (lập trước kỳ) : created_at <  S  AND  status_at(S) ∉ {9,10,11,12}
 * TH2 (lập trong kỳ) : created_at ∈ [S, E]
 * Loại ra            : is_parent_project = 1  ·  status_at(E) = 1 (Đang tạo)
 *
 * ⚠️ R7 (13/09): TRẠNG THÁI TẠI E PHẢI LẤY TỪ LOG, không phải cột `status` hiện tại. Bộ chọn kỳ
 * có Tháng trước / Quý trước / Năm trước — với kỳ quá khứ, `status` hôm nay đã đi tiếp, dùng nó
 * là gán kết quả của HÔM NAY cho một kỳ đã qua. Sai IM LẶNG: 2 đẳng thức bất biến vẫn đúng.
 */
private function getProjects(Request $request)
{
    if ($this->projectCacheRequest === $request && $this->projectCache !== null) {
        return $this->projectCache;
    }

    [$from, $to] = $this->resolvePeriod($request);

    $query = ProspectiveProject::query()
        ->with(['scope:id,name', 'industry:id,name', 'closedReason:id,name'])
        // Lấy RỘNG hơn kỳ là cố ý: dự án lập từ kỳ trước vẫn phải xét TH1, nên không
        // lọc created_at theo kỳ ngay ở SQL.
        ->where('prospective_projects.created_at', '<=', $to)
        // ⚠️ R7: KHÔNG lọc `status <> 1` ở SQL — bản nháp phải xét theo status_at(E), vì dự án
        // hôm nay đã ở bước 5 vẫn có thể còn là nháp tại cuối một kỳ quá khứ.
        ->where(function ($q) {
            $q->whereNull('prospective_projects.is_parent_project')
              ->orWhere('prospective_projects.is_parent_project', 0);
        });

    $this->applyCompanyScope($query, $request);   // mục 4.2
    $this->applyPermissionFilter($query);         // mục 4.2
    $this->applyDimensionFilters($query, $request); // mục 4.3

    $candidates = $query->select([
        'prospective_projects.id',
        'prospective_projects.code',
        'prospective_projects.name',
        'prospective_projects.status',
        'prospective_projects.created_at',
        'prospective_projects.company_id',
        'prospective_projects.customer_id',
        'prospective_projects.main_sale_department_id',
        'prospective_projects.main_sale_part_id',
        'prospective_projects.main_sale_employee_id',
        'prospective_projects.scope_id',
        'prospective_projects.industry_id',
        'prospective_projects.closed_reason_id',
        'prospective_projects.expected_contract_amount',
    ])->get();

    $ids = $candidates->pluck('id')->all();
    $statusAtStart = $this->statusAtBulk($ids, $from);
    // R7: trạng thái tại CUỐI KỲ cũng lấy từ log, không đọc cột `status` hiện tại
    $statusAtEnd = $this->statusAtBulk($ids, $to);

    $projects = $candidates->filter(function ($p) use ($from, $statusAtStart, $statusAtEnd) {
        // Loại bản nháp theo trạng thái TẠI CUỐI KỲ
        if (($statusAtEnd[(int) $p->id] ?? self::STATUS_DRAFT) === self::STATUS_DRAFT) {
            return false;
        }
        // TH2 — lập trong kỳ
        if ($p->created_at >= $from) {
            return true;
        }
        // TH1 — lập trước kỳ, tại S chưa đóng. Không có log <= S ⇒ chưa tồn tại ⇒ loại.
        if (!array_key_exists((int) $p->id, $statusAtStart)) {
            return false;
        }
        return !in_array($statusAtStart[(int) $p->id], self::CLOSED_STATUSES, true);
    })->values();

    // Đánh dấu "lập trong kỳ" cho chip ở popup và 2 ô của dải tổng hợp,
    // và gắn TRẠNG THÁI TẠI CUỐI KỲ — nguồn DUY NHẤT cho nhóm kết quả, cột Tiến trình và 2 ô lọc.
    foreach ($projects as $p) {
        $p->created_in_period = $p->created_at >= $from;
        $p->status_at_end = (int) ($statusAtEnd[(int) $p->id] ?? $p->status);
    }

    $this->projectCacheRequest = $request;
    $this->projectCache = $projects;

    return $projects;
}
```

#### 4.2 Phân quyền + phạm vi công ty

Đọc tham khảo: `hrm-api/Modules/Assign/Services/Report/PotentialCustomerCareService.php:117-152`
Produces: `applyPermissionFilter($query): void` · `applyCompanyScope($query, Request $r): void` ·
`allowedCompanyIds(): ?array` (`null` = mọi công ty)

- [x] **Bước 1: Viết ca test fail-closed**

```ts
test('4. Phân quyền fail-closed: user không quyền chỉ thấy dự án của mình', async () => {
  const guest = await request.newContext({ baseURL: API_BASE });
  const login = await guest.post('/api/v1/login', {
    data: { email: fx.noperm_email, password: fx.noperm_password },
  });
  expect(login.status()).toBe(200);
  const token = (await login.json()).data.token ?? (await login.json()).access_token;

  const asGuest = await request.newContext({
    baseURL: API_BASE,
    extraHTTPHeaders: { Authorization: `Bearer ${token}` },
  });
  const res = await asGuest.get(reportUrl());
  expect(res.status()).toBe(200);
  const ids: number[] = (await res.json()).data.debug_project_ids ?? [];

  // Tài khoản này không phụ trách dự án fixture nào ⇒ không được thấy dòng nào của fixture
  for (const id of Object.values(fx.project_ids)) {
    expect(ids, `không được thấy dự án ${id}`).not.toContain(id);
  }
  await asGuest.dispose();
  await guest.dispose();
});

test('5. Không leo thang phạm vi: tài khoản chỉ có quyền "theo công ty" bị ép về công ty của mình', async () => {
  // R6 (13/09): PHẢI chạy bằng tài khoản chỉ có quyền 1185. Tài khoản e2e mặc định có 1184
  // (tổng công ty) ⇒ allowedCompanyIds() trả null ⇒ mọi company_id đều hợp lệ ⇒ ca test sẽ
  // PASS mà không kiểm được gì.
  test.skip(!fx.other_company_id, 'DB chỉ có 1 công ty — không dựng được ca leo thang phạm vi');

  const ctx = await request.newContext({ baseURL: API_BASE });
  const login = await ctx.post('/api/v1/login', {
    data: { email: fx.company_only_email, password: fx.company_only_password },
  });
  expect(login.status()).toBe(200);
  const body = await login.json();
  const token = body.data?.token ?? body.access_token;

  const scoped = await request.newContext({
    baseURL: API_BASE,
    extraHTTPHeaders: { Authorization: `Bearer ${token}` },
  });

  // Gửi company_id của công ty KHÁC -> BE phải ép về công ty của tài khoản, không trả dữ liệu lạ
  const res = await scoped.get(reportUrl({ company_id: String(fx.other_company_id) }));
  expect(res.status()).toBe(200);
  const ids: number[] = (await res.json()).data.debug_project_ids ?? [];

  // Dự án fixture thuộc công ty CỦA tài khoản này -> vẫn phải thấy (bị ép về đúng công ty mình),
  // chứ không phải trả rỗng vì đã nghe theo company_id lạ.
  expect(ids).toContain(fx.project_ids.open_created_in);

  await scoped.dispose();
  await ctx.dispose();
});
```

- [x] **Bước 2: Chạy test — kỳ vọng ĐỎ (404)**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test tkt-result-report.api --workers=1
```

- [x] **Bước 3: Viết `applyPermissionFilter()`**

```php
const PERM_ALL_COMPANY = 'Xem báo cáo kết quả dự án TKT theo tổng công ty';
const PERM_COMPANY     = 'Xem báo cáo kết quả dự án TKT theo công ty';
const PERM_DEPARTMENT  = 'Xem báo cáo kết quả dự án TKT theo phòng ban';

/**
 * Gate quyền xem theo cấp — bám khuôn PotentialCustomerCareService::applyPermissionFilter().
 * Route KHÔNG gắn checkPermission vì làm vậy sẽ chặn mất cấp fallback cuối.
 * Không có quyền nào: chỉ thấy dự án MÌNH phụ trách hoặc MÌNH tạo.
 */
private function applyPermissionFilter($query): void
{
    $userId = auth()->id();

    if (isCurrentEmployeeHasPermission(self::PERM_ALL_COMPANY)) {
        return;
    }

    if (isCurrentEmployeeHasPermission(self::PERM_COMPANY)) {
        $companyId = auth()->user()->current_company_role;
        $query->where(function ($q) use ($companyId, $userId) {
            $q->where('prospective_projects.company_id', $companyId)
              ->orWhere('prospective_projects.main_sale_employee_id', $userId);
        });
        return;
    }

    if (isCurrentEmployeeHasPermission(self::PERM_DEPARTMENT)) {
        $query->where(function ($q) use ($userId) {
            $q->whereIn('prospective_projects.main_sale_department_id', listManageDepartmentIds())
              ->orWhereIn('prospective_projects.main_sale_part_id', listManagePartIds())
              ->orWhere('prospective_projects.main_sale_employee_id', $userId);
        });
        return;
    }

    $query->where(function ($q) use ($userId) {
        $q->where('prospective_projects.main_sale_employee_id', $userId)
          ->orWhere('prospective_projects.created_by', $userId);
    });
}
```

- [x] **Bước 4: Viết `allowedCompanyIds()` + `applyCompanyScope()`**

```php
/**
 * Danh sách công ty user được xem. null = mọi công ty (quyền tổng công ty).
 * Dùng cho CẢ filter-options (đổ ô Công ty) lẫn applyCompanyScope.
 */
private function allowedCompanyIds(): ?array
{
    if (isCurrentEmployeeHasPermission(self::PERM_ALL_COMPANY)) {
        return null;
    }

    return array_values(array_filter([(int) auth()->user()->current_company_role]));
}

/**
 * Ô Công ty BẮT BUỘC chọn, không có mục "Tất cả" ⇒ báo cáo luôn nằm trong đúng 1 pháp nhân.
 *
 * ⚠️ KHÔNG tin company_id do FE gửi lên: user có nhiều vai trò có thể gửi công ty ngoài phạm vi.
 * Ngoài phạm vi thì ÉP về công ty hợp lệ đầu danh mục chứ không trả lỗi (tránh màn chết).
 */
private function applyCompanyScope($query, Request $request): void
{
    $requested = (int) $request->get('company_id');
    $allowed = $this->allowedCompanyIds();

    if ($allowed !== null && !in_array($requested, $allowed, true)) {
        $requested = (int) ($allowed[0] ?? 0);
    }

    $query->where('prospective_projects.company_id', $requested);
}
```

> ⏸ **Chưa commit ở đây** — R1: cả Task 4 commit MỘT LẦN ở bước cuối.

#### 4.3 Các chiều dữ liệu + bộ lọc

Đọc tham khảo: `hrm-api/Modules/Assign/Services/Report/MeetingByMarketService.php:214-250`
Produces:
- `attachDimensions(Collection $projects): void` — gắn `dept_id/dept_name`, `part_id/part_name`,
  `emp_id/emp_name`, `province_id/province_name`, `scope_id/scope_name`,
  `industry_id/industry_name`, `customer_id/customer_name` lên từng dự án
- `applyDimensionFilters($query, Request $r): void` · `filterByProvince($projects, Request $r)`

- [x] **Bước 1: Viết `attachDimensions()` — batch, không N+1**

```php
/** Nhãn dùng chung cho mọi chiều khi dự án thiếu dữ liệu. */
const UNKNOWN_LABEL = 'Chưa xác định';

/**
 * Gắn đủ 7 chiều lên từng dự án bằng các truy vấn GOM (1 query/chiều), không N+1.
 *
 * ⚠️ Dự án thiếu dữ liệu ở một chiều vẫn PHẢI lên báo cáo ở nhóm "Chưa xác định" —
 * lọc bỏ sẽ làm dòng TỔNG khác tổng các dòng cấp 0 và 2 đẳng thức bất biến vỡ.
 */
private function attachDimensions($projects): void
{
    $deptIds  = $projects->pluck('main_sale_department_id')->filter()->unique()->values()->all();
    $partIds  = $projects->pluck('main_sale_part_id')->filter()->unique()->values()->all();
    $empIds   = $projects->pluck('main_sale_employee_id')->filter()->unique()->values()->all();
    $custIds  = $projects->pluck('customer_id')->filter()->unique()->values()->all();

    $depts = DB::table('departments')->whereIn('id', $deptIds)->pluck('name', 'id');
    $parts = DB::table('parts')->whereIn('id', $partIds)->pluck('name', 'id');
    $emps  = DB::table('employees')->whereIn('id', $empIds)->pluck('fullname', 'id');
    $customers = $this->resolveCustomerProvinces($custIds);

    foreach ($projects as $p) {
        $p->dept_id   = $p->main_sale_department_id ?: null;
        $p->dept_name = $p->dept_id ? ($depts[$p->dept_id] ?? self::UNKNOWN_LABEL) : self::UNKNOWN_LABEL;

        $p->part_id   = $p->main_sale_part_id ?: null;
        $p->part_name = $p->part_id ? ($parts[$p->part_id] ?? null) : null;

        $p->emp_id    = $p->main_sale_employee_id ?: null;
        $p->emp_name  = $p->emp_id ? ($emps[$p->emp_id] ?? self::UNKNOWN_LABEL) : self::UNKNOWN_LABEL;

        $info = $p->customer_id ? ($customers[$p->customer_id] ?? null) : null;
        $p->customer_name  = $info['fullname'] ?? self::UNKNOWN_LABEL;
        $p->province_id    = $info['province_id'] ?? null;
        $p->province_name  = $info['province_name'] ?? 'Chưa xác định thị trường';

        $p->scope_name    = optional($p->scope)->name ?: self::UNKNOWN_LABEL;
        $p->industry_name = optional($p->industry)->name ?: self::UNKNOWN_LABEL;
        $p->closed_reason_name = optional($p->closedReason)->name;
    }
}

/**
 * Map customer_id => [province_id, province_name, fullname, code].
 * Port khuôn MeetingByMarketService::resolveCustomerProvinces(): khách hàng nằm ở DB ERP
 * (App\Models\TpCustomer, connection mysql2 / env('DB_DATABASE_SECOND')).
 *
 * ⚠️ Chỉ giữ province_id khi resolve được CẢ province_id LẪN province_name. Khách có
 * province_id nhưng mất bản ghi provinces bên ERP mà vẫn giữ id sẽ đẻ ra một nhóm riêng
 * trùng nhãn "Chưa xác định thị trường" nhưng khác id ⇒ không gộp được.
 */
private function resolveCustomerProvinces(array $customerIds): array
{
    if (empty($customerIds)) {
        return [];
    }

    $erpDb = env('DB_DATABASE_SECOND');

    $rows = \App\Models\TpCustomer::query()
        ->leftJoin($erpDb . '.provinces as p', 'p.id', '=', 'customers.province_id')
        ->whereIn('customers.id', $customerIds)
        ->select(['customers.id', 'customers.fullname', 'customers.code', 'customers.province_id', 'p.name as province_name'])
        ->get();

    $map = [];
    foreach ($rows as $row) {
        $hasProvince = $row->province_id && !empty($row->province_name);
        $map[(int) $row->id] = [
            'fullname'      => $row->fullname,
            'code'          => $row->code,
            'province_id'   => $hasProvince ? (int) $row->province_id : null,
            'province_name' => $hasProvince ? $row->province_name : null,
        ];
    }

    return $map;
}
```

- [x] **Bước 2: Viết `applyDimensionFilters()`**

```php
/**
 * Ô lọc của toolbar. Ô "Tiến trình" chỉ nhận 2..12 — id 1 (Đang tạo) không bao giờ lên
 * báo cáo nên để trong danh sách là ô lọc chết luôn ra 0 dòng.
 * Ô "Kết quả" lọc theo 3 NHÓM, không lọc theo tiến trình lẻ.
 */
private function applyDimensionFilters($query, Request $request): void
{
    $map = [
        'department_id' => 'main_sale_department_id',
        'part_id'       => 'main_sale_part_id',
        'employee_id'   => 'main_sale_employee_id',
        'customer_id'   => 'customer_id',
        'scope_id'      => 'scope_id',
        'industry_id'   => 'industry_id',
    ];
    foreach ($map as $param => $column) {
        if ($request->filled($param)) {
            $query->where('prospective_projects.' . $column, (int) $request->get($param));
        }
    }

    // ⚠️ R7: ô lọc `status` (Tiến trình) và `result` (Kết quả) KHÔNG lọc ở SQL nữa — cả hai xét
    // theo TRẠNG THÁI TẠI CUỐI KỲ (`status_at_end`, lấy từ log), không phải cột `status` hiện tại.
    // Lọc ở PHP sau khi gắn status_at_end — xem filterByResult().
    // province_id cũng KHÔNG lọc ở SQL: tỉnh chỉ resolve được sau khi lấy dữ liệu (nằm ở DB ERP).
    // Lọc ở PHP sau attachDimensions() — xem filterByProvince().
}

/**
 * R7: lọc theo Tiến trình / Kết quả TẠI CUỐI KỲ (`status_at_end`), sau khi đã gắn trạng thái từ log.
 * Ô Tiến trình chỉ nhận 2..12 — id 1 (Đang tạo) không bao giờ lên báo cáo nên để trong danh sách
 * là ô lọc chết luôn ra 0 dòng.
 */
private function filterByResult($projects, Request $request)
{
    if ($request->filled('status')) {
        $status = (int) $request->get('status');
        if ($status >= 2 && $status <= 12) {
            $projects = $projects->filter(function ($p) use ($status) {
                return (int) $p->status_at_end === $status;
            })->values();
        }
    }

    if ($request->filled('result')) {
        $wanted = $request->get('result');
        $projects = $projects->filter(function ($p) use ($wanted) {
            return $this->resultGroupOf((int) $p->status_at_end) === $wanted;
        })->values();
    }

    return $projects;
}

/** Lọc thị trường sau khi đã resolve tỉnh (không lọc được ở SQL vì customers nằm ở DB ERP). */
private function filterByProvince($projects, Request $request)
{
    if (!$request->filled('province_id')) {
        return $projects;
    }
    $wanted = (int) $request->get('province_id');

    return $projects->filter(function ($p) use ($wanted) {
        return (int) ($p->province_id ?? 0) === $wanted;
    })->values();
}
```

- [x] **Bước 3: Nối 2 hàm vào `getProjects()`**

Trong `getProjects()`, ngay trước khi cache, chèn:

```php
    $this->attachDimensions($projects);
    $projects = $this->filterByResult($projects, $request);   // R7 — lọc theo status_at_end
    $projects = $this->filterByProvince($projects, $request);
```

- [x] **Bước 6: Kiểm cú pháp + chạy lại test — vẫn đỏ vì chưa có route, nhưng đã có logic**

```bash
cd HRM/hrm-api && php -l Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php
```
Kỳ vọng: `No syntax errors detected`.

Ca e2e vẫn **ĐỎ có chủ đích** (chưa có route) — sẽ xanh ở **Task 9**. Ghi rõ điều này trong report,
đừng cố sửa cho xanh ở đây.

- [x] **Bước 7: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-api && git add Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026). Stage để `git diff HEAD` bắt được cả file mới, phục vụ khâu review.

---

### Task 5: Chấm 3 nhóm kết quả + cột tiền

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php`

**Interfaces:**
- Consumes: `getProjects()` (Task 4)
- Produces:
  - `resultGroupOf(int $status): string` → `'won' | 'lost' | 'open'`
  - `contractAmountFor($project): ?float` → **luôn `null`** ở phase 1
  - `expectedAmountFor($project): ?float`
  - `metricsOf(Collection $projects): array` → khoá `total, open, closed, won, lost, created_before,
    created_in, contract_amount, expected_amount, success_rate` (7 khoá đầu là **số nguyên**;
    `contract_amount`/`expected_amount`/`success_rate` là `float|null`, `null` ⇒ FE hiện `—`)

- [x] **Bước 1: Viết ca test đẳng thức bất biến (thêm vào spec API đã tạo)**

```ts
test('2. Hai đẳng thức bất biến đúng ở mọi dòng, mọi cấp', async () => {
  const res = await api.get(reportUrl());
  const body = await res.json();

  const bad: string[] = [];
  const walk = (node: any, path: string) => {
    const m = node.metrics;
    if (m.total !== m.open + m.closed) bad.push(`${path}: total ${m.total} != open ${m.open} + closed ${m.closed}`);
    if (m.closed !== m.won + m.lost) bad.push(`${path}: closed ${m.closed} != won ${m.won} + lost ${m.lost}`);
    (node.children ?? []).forEach((c: any, i: number) => walk(c, `${path}/${i}`));
  };
  (body.data.tree as any[]).forEach((n, i) => walk(n, `root${i}`));
  walk({ metrics: body.data.total, children: [] }, 'TỔNG');

  expect(bad, bad.join('\n')).toEqual([]);
});

test('3. Nhóm kết quả khớp tiến trình', async () => {
  for (const [group, allowed] of [['won', [9, 10, 12]], ['lost', [11]], ['open', [2, 3, 4, 5, 6, 7, 8]]] as const) {
    const res = await api.get(`${REPORT}/project-list?${new URLSearchParams({
      period: 'custom', from: fx.period.from, to: fx.period.to,
      company_id: String(fx.company_id), criteria: 'dept', metric: group, per_page: '200',
    })}`);
    expect(res.status(), group).toBe(200);
    const rows = (await res.json()).data.rows as any[];
    const wrong = rows.filter((r) => !(allowed as readonly number[]).includes(r.status));
    expect(wrong.map((r) => `${r.code}:${r.status}`), `nhóm ${group}`).toEqual([]);
    expect(rows.some((r) => r.status === 1), `nhóm ${group} không được có tiến trình 1`).toBe(false);
  }
});
```

- [x] **Bước 2: Chạy test — kỳ vọng ĐỎ (404)**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test tkt-result-report.api --workers=1
```

- [x] **Bước 3: Viết 2 hàm tiền**

> **Ruling R8 (13/09)**: `resultGroupOf()` + hằng `STATUSES_WON` / `STATUS_LOST` **đã nằm ở Task 4**
> (nơi `filterByResult()` dùng tới đầu tiên). **KHÔNG khai lại ở đây.** Bản chuẩn trả đúng 3 chuỗi
> `'won'` / `'lost'` / `'open'` — đây là hợp đồng API (tham số `result` và `metric`), đổi tên là
> bộ lọc "Kết quả" chết im lặng.

```php
/**
 * Giá trị HỢP ĐỒNG đã ký của dự án Thành công.
 *
 * ⚠️ TREO (chốt 13/09/2026): KHÔNG dùng hợp đồng ERP — user đang phát triển hợp đồng HRM
 * lập từ báo giá HRM. Phase 1 luôn trả null ⇒ cột "Giá trị HĐ" hiện "—" ở mọi dòng.
 * KHI CÓ NGUỒN: SỬA DUY NHẤT HÀM NÀY, không nơi nào khác đọc giá trị hợp đồng.
 */
private function contractAmountFor($project): ?float
{
    return null;
}

/**
 * Giá trị KỲ VỌNG của dự án Đang triển khai = ô "Giá trị HĐ kỳ vọng" của form dự án.
 *
 * Ô này KHÔNG bắt buộc nhập (đo được 58% dự án có số). Chốt 13/09/2026: khuyết thì ĐỂ TRỐNG,
 * KHÔNG lấy estimated_budget thay thế — 2 số khác bản chất (doanh thu kỳ vọng vs ngân sách chi).
 */
private function expectedAmountFor($project): ?float
{
    $value = $project->expected_contract_amount;

    return ($value === null || (float) $value <= 0) ? null : (float) $value;
}
```

- [x] **Bước 4: Viết `metricsOf()` — nguồn duy nhất của mọi con số**

```php
/**
 * Bộ chỉ tiêu của một tập dự án. Dùng CHUNG cho dòng cây, dòng TỔNG và dải tổng hợp
 * ⇒ 3 nơi không thể lệch nhau.
 *
 * Bất biến (có ca e2e):  total = open + closed  ·  closed = won + lost
 */
private function metricsOf($projects): array
{
    $won = $lost = $open = 0;
    $contract = $expected = 0.0;
    $createdBefore = $createdIn = 0;

    foreach ($projects as $p) {
        switch ($this->resultGroupOf((int) $p->status_at_end)) {   // R7
            case 'won':
                $won++;
                $contract += (float) ($this->contractAmountFor($p) ?? 0);
                break;
            case 'lost':
                $lost++;
                // Dự án thất bại KHÔNG đóng góp vào cột tiền nào (chốt 09/09/2026)
                break;
            default:
                $open++;
                $expected += (float) ($this->expectedAmountFor($p) ?? 0);
                break;
        }
        $p->created_in_period ? $createdIn++ : $createdBefore++;
    }

    $closed = $won + $lost;

    return [
        'total'           => $won + $lost + $open,
        'open'            => $open,
        'closed'          => $closed,
        'won'             => $won,
        'lost'            => $lost,
        'created_before'  => $createdBefore,
        'created_in'      => $createdIn,
        // null (không phải 0) khi chưa có nguồn hợp đồng ⇒ FE hiện "—", Excel để ô rỗng
        'contract_amount' => $contract > 0 ? $contract : null,
        'expected_amount' => $expected > 0 ? $expected : null,
        // Mẫu số 0 ⇒ null ⇒ FE hiện "—", KHÔNG hiện 0,0%
        'success_rate'    => $closed > 0 ? round($won * 100 / $closed, 1) : null,
    ];
}
```

- [x] **Bước 5: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-api && git add Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026). Stage để `git diff HEAD` bắt được cả file mới, phục vụ khâu review.

---

### Task 6: Cây theo dõi đệ quy theo 3 tiêu chí

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php`

**Interfaces:**
- Consumes: `getProjects()`, `metricsOf()`, `attachDimensions()`
- Produces: `buildTree(Collection $projects, string $criteria): array` — mảng node
  `['key','dim','id','name','metrics','children']`

- [x] **Bước 1: Viết bảng khai báo 3 tiêu chí**

```php
/**
 * Cấp của cây theo từng tiêu chí. Khai báo TƯỜNG MINH, không suy bằng cờ nhị phân.
 *
 * - Cấp "Thị trường" nằm DƯỚI Nhân viên ở tiêu chí dept chính là câu trả lời cho
 *   "nhân viên đó làm ở các thị trường nào".
 * - Tiêu chí scope DỪNG ở Phòng ban: câu hỏi quản trị chỉ hỏi "do phòng ban nào phụ trách".
 */
const CRITERIA_DIMS = [
    'dept'   => ['dept', 'part', 'emp', 'province'],
    'market' => ['province', 'dept', 'part', 'emp'],
    'scope'  => ['scope', 'industry', 'dept'],
];

/** Khoá + nhãn của từng chiều trên 1 dự án */
const DIM_FIELDS = [
    'dept'     => ['id' => 'dept_id',     'name' => 'dept_name'],
    'part'     => ['id' => 'part_id',     'name' => 'part_name'],
    'emp'      => ['id' => 'emp_id',      'name' => 'emp_name'],
    'province' => ['id' => 'province_id', 'name' => 'province_name'],
    'scope'    => ['id' => 'scope_id',    'name' => 'scope_name'],
    'industry' => ['id' => 'industry_id', 'name' => 'industry_name'],
    'customer' => ['id' => 'customer_id', 'name' => 'customer_name'],
];
```

- [x] **Bước 2: Viết `buildTree()` đệ quy**

```php
/**
 * Dựng cây theo danh sách cấp của tiêu chí.
 *
 * ⚠️ Cấp BỘ PHẬN tự bỏ qua ở phòng ban không chia bộ phận (part_id rỗng) — nhảy thẳng
 * Phòng ban ▸ Nhân viên, KHÔNG đẻ dòng "Chưa phân bộ phận" rỗng.
 *
 * `key` là tổ hợp lọc AND, dùng làm drill_key của popup: "dept:5+part:9+emp:88".
 */
private function buildTree($projects, string $criteria): array
{
    $dims = self::CRITERIA_DIMS[$criteria] ?? self::CRITERIA_DIMS['dept'];

    return $this->buildLevel($projects, $dims, 0, '');
}

private function buildLevel($projects, array $dims, int $depth, string $parentKey): array
{
    if ($depth >= count($dims)) {
        return [];
    }

    $dim = $dims[$depth];
    $idField = self::DIM_FIELDS[$dim]['id'];
    $nameField = self::DIM_FIELDS[$dim]['name'];

    // Cấp Bộ phận: dự án không thuộc bộ phận nào thì BỎ QUA CẤP, đẩy thẳng xuống cấp sau.
    if ($dim === 'part') {
        $withPart = $projects->filter(function ($p) { return !empty($p->part_id); });
        $withoutPart = $projects->filter(function ($p) { return empty($p->part_id); });

        $nodes = $withPart->isEmpty() ? [] : $this->groupInto($withPart, $dim, $idField, $nameField, $dims, $depth, $parentKey);
        $skipped = $withoutPart->isEmpty() ? [] : $this->buildLevel($withoutPart, $dims, $depth + 1, $parentKey);

        return array_merge($nodes, $skipped);
    }

    return $this->groupInto($projects, $dim, $idField, $nameField, $dims, $depth, $parentKey);
}

private function groupInto($projects, string $dim, string $idField, string $nameField, array $dims, int $depth, string $parentKey): array
{
    $groups = $projects->groupBy(function ($p) use ($idField) {
        return (string) ($p->{$idField} ?? '0');
    });

    $nodes = [];
    foreach ($groups as $id => $items) {
        $key = ($parentKey === '' ? '' : $parentKey . '+') . $dim . ':' . $id;
        $nodes[] = [
            'key'      => $key,
            'dim'      => $dim,
            'id'       => (int) $id,
            'name'     => $items->first()->{$nameField} ?: self::UNKNOWN_LABEL,
            'metrics'  => $this->metricsOf($items),
            'children' => $this->buildLevel($items, $dims, $depth + 1, $key),
        ];
    }

    // Nhóm "Chưa xác định" (id = 0) luôn xuống cuối, còn lại sắp theo tên
    usort($nodes, function ($a, $b) {
        if (($a['id'] === 0) !== ($b['id'] === 0)) {
            return $a['id'] === 0 ? 1 : -1;
        }
        return strcasecmp($a['name'], $b['name']);
    });

    return $nodes;
}
```

- [x] **Bước 3: Viết ca test "dòng cha = tổng dòng con"**

Thêm vào `tkt-result-report.api.spec.ts`:

```ts
test('6. Số dòng cha = tổng dòng con ở 7 cột cộng được, cả 3 tiêu chí', async () => {
  const COLS = ['total', 'open', 'closed', 'won', 'lost', 'created_before', 'created_in'] as const;
  const bad: string[] = [];

  for (const criteria of ['dept', 'market', 'scope']) {
    const res = await api.get(reportUrl({ criteria }));
    expect(res.status(), criteria).toBe(200);
    const body = await res.json();

    const walk = (node: any, path: string) => {
      const kids = node.children ?? [];
      if (kids.length) {
        for (const col of COLS) {
          const sum = kids.reduce((s: number, k: any) => s + (k.metrics[col] ?? 0), 0);
          if ((node.metrics[col] ?? 0) !== sum) {
            bad.push(`${criteria} ${path} ${col}: cha ${node.metrics[col]} != tổng con ${sum}`);
          }
        }
        kids.forEach((k: any, i: number) => walk(k, `${path}/${k.name}`));
      }
    };
    (body.data.tree as any[]).forEach((n) => walk(n, n.name));
  }

  expect(bad, bad.join('\n')).toEqual([]);
});
```

- [x] **Bước 4: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-api && git add Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php
cd ../e2e && git status --short  # e2e không thuộc repo nào — chỉ ghi nhận
cd ../hrm-api && 
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026). Stage để `git diff HEAD` bắt được cả file mới, phục vụ khâu review.

---

### Task 7: Dải tổng hợp + drill (popup) + 4 luật bỏ cột

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php`
- Create: `hrm-api/Modules/Assign/Transformers/ProspectiveProjectResultResource/ProjectRowResource.php`

**Interfaces:**
- Produces:
  - `summary(Request $r): array` — 2 khối × 3 ô + dòng meta
  - `projectList(Request $r): array` — `['rows' => …, 'columns' => […], 'total' => int]`
  - `drillColumns(string $criteria, string $drillKey, Collection $projects): array`

- [x] **Bước 1: Viết `summary()`**

```php
/**
 * Dải tổng hợp: 2 khối, mỗi khối 3 ô con chia HẾT tổng.
 *   Khối 1 bổ dọc theo NGÀY LẬP PHIẾU : lập trước kỳ + lập trong kỳ = tổng
 *   Khối 2 bổ dọc theo KẾT QUẢ tại E  : thành công + thất bại + đang triển khai = tổng
 * Dùng chung metricsOf() với bảng ⇒ dòng TỔNG của bảng luôn khớp dải này (có ca e2e).
 */
public function summary(Request $request): array
{
    $projects = $this->getProjects($request);
    $metrics = $this->metricsOf($projects);
    [$from, $to] = $this->resolvePeriod($request);

    return [
        'period' => ['from' => $from->format('d/m/Y'), 'to' => $to->format('d/m/Y')],
        'blocks' => [
            [
                'title' => 'Dự án TKT trong kỳ',
                'items' => [
                    ['key' => 'total',          'label' => 'Tổng dự án',          'value' => $metrics['total']],
                    ['key' => 'created_before', 'label' => 'Dự án lập trước kỳ',  'value' => $metrics['created_before']],
                    ['key' => 'created_in',     'label' => 'Dự án lập trong kỳ',  'value' => $metrics['created_in']],
                ],
            ],
            [
                'title' => 'Kết quả thực hiện trong kỳ',
                'items' => [
                    ['key' => 'won',  'label' => 'Chuyển đổi thành công',   'value' => $metrics['won']],
                    ['key' => 'lost', 'label' => 'Thất bại',                'value' => $metrics['lost']],
                    ['key' => 'open', 'label' => 'Vẫn tiếp tục triển khai', 'value' => $metrics['open']],
                ],
            ],
        ],
        'meta' => [
            'project_count'  => $metrics['total'],
            // Đếm distinct — đúng chỗ của nó là dải tổng hợp, KHÔNG đưa vào bảng
            // (cột đếm distinct không cộng được theo cấp).
            'customer_count' => $projects->pluck('customer_id')->filter()->unique()->count(),
            // Phase 1 chưa có nguồn hợp đồng ⇒ null ⇒ FE bỏ hẳn đoạn "Giá trị HĐ X tỷ"
            'contract_amount' => $metrics['contract_amount'],
        ],
    ];
}
```

- [x] **Bước 2: Viết `drillColumns()` — 4 luật rút gọn, BE quyết**

```php
/** Bộ cột chiều theo từng tiêu chí, khai báo tường minh (thứ tự = thứ tự cấp) */
const CRITERIA_DRILL_COLS = [
    'dept'   => ['dept', 'part', 'emp', 'province', 'customer'],
    'market' => ['province', 'dept', 'part', 'emp', 'customer'],
    'scope'  => ['scope', 'industry', 'dept', 'part', 'emp', 'customer'],
];

/**
 * Bộ cột của popup sau khi áp 4 luật rút gọn. BE quyết để bảng popup, bản in và Excel
 * dùng CHUNG một nguồn — 3 nơi không thể lệch nhau.
 *
 * Luật 2: bỏ cột của cấp đã cố định (nằm trên drill_key). Popup từ dòng TỔNG không bỏ cột nào.
 * Luật 3: bỏ cột Bộ phận khi KHÔNG dòng nào thuộc bộ phận — xét trên TOÀN BỘ dự án của node,
 *         KHÔNG xét theo bộ lọc trong popup, để cột không nhấp nháy khi lọc.
 */
private function drillColumns(string $criteria, string $drillKey, $projects): array
{
    $fixed = [];
    foreach (array_filter(explode('+', $drillKey)) as $part) {
        [$dim] = explode(':', $part);
        $fixed[] = $dim;
    }

    $cols = self::CRITERIA_DRILL_COLS[$criteria] ?? self::CRITERIA_DRILL_COLS['dept'];
    $cols = array_values(array_diff($cols, $fixed));                         // luật 2

    $hasPart = $projects->contains(function ($p) { return !empty($p->part_id); });
    if (!$hasPart) {
        $cols = array_values(array_diff($cols, ['part']));                   // luật 3
    }

    // 4 cột nhận dạng dự án dồn lên ngay sau STT (chốt 09/09/2026), rồi tới cụm cột chiều,
    // cuối cùng là đuôi cố định.
    // R2 (13/09): khoá cột trả về TRÙNG khoá của ProjectRowResource để FE render thẳng
    // row[col], không cần bảng map thứ 3 giữa BE và FE — chính là chỗ 3 đầu ra
    // (bảng popup / bản in / Excel) hay lệch nhau.
    $cols = array_map(function ($dim) { return $dim . '_name'; }, $cols);

    return array_merge(
        ['code', 'name', 'created_at', 'status_text'],
        $cols,
        ['result_text', 'closed_reason', 'amount']
    );
}
```

- [x] **Bước 3: Viết `projectList()` + Resource**

```php
/** Popup danh sách dự án của 1 lát cắt. Luôn phân trang — không trả cả tập. */
public function projectList(Request $request): array
{
    $projects = $this->getProjects($request);
    $criteria = $request->get('criteria', 'dept');
    $drillKey = (string) $request->get('drill_key', '');

    // Bộ cột xét trên TOÀN BỘ dự án của node (trước khi lọc trong popup) — luật 3
    $nodeProjects = $this->applyDrillKey($projects, $drillKey);
    $columns = $this->drillColumns($criteria, $drillKey, $nodeProjects);

    $rows = $this->applyMetricFilter($nodeProjects, $request->get('metric', 'total'));
    $rows = $this->sortRows($rows, $request->get('sort', 'created_at'), $request->get('sort_dir', 'desc'));

    $perPage = min(max((int) $request->get('per_page', 20), 1), 200);
    $page = max((int) $request->get('page', 1), 1);
    $total = $rows->count();

    return [
        'columns' => $columns,
        'total'   => $total,
        'rows'    => ProjectRowResource::collection($rows->forPage($page, $perPage)->values()),
    ];
}

/** Lọc tập dự án theo tổ hợp drill_key "dept:5+part:9+emp:88" (AND). Key rỗng = dòng TỔNG. */
private function applyDrillKey($projects, string $drillKey)
{
    foreach (array_filter(explode('+', $drillKey)) as $part) {
        [$dim, $id] = array_pad(explode(':', $part), 2, null);
        if (!isset(self::DIM_FIELDS[$dim])) {
            continue;
        }
        $field = self::DIM_FIELDS[$dim]['id'];
        $projects = $projects->filter(function ($p) use ($field, $id) {
            return (int) ($p->{$field} ?? 0) === (int) $id;
        });
    }

    return $projects->values();
}

/** Lọc theo ô số user vừa bấm trên bảng / dải tổng hợp. */
private function applyMetricFilter($projects, string $metric)
{
    switch ($metric) {
        case 'won':  return $projects->filter(function ($p) { return $this->resultGroupOf((int) $p->status_at_end) === 'won';  })->values();
        case 'lost': return $projects->filter(function ($p) { return $this->resultGroupOf((int) $p->status_at_end) === 'lost'; })->values();
        case 'open': return $projects->filter(function ($p) { return $this->resultGroupOf((int) $p->status_at_end) === 'open'; })->values();
        case 'closed': return $projects->filter(function ($p) { return $this->resultGroupOf((int) $p->status_at_end) !== 'open'; })->values();
        case 'created_before': return $projects->filter(function ($p) { return !$p->created_in_period; })->values();
        case 'created_in':     return $projects->filter(function ($p) { return  $p->created_in_period; })->values();
        default: return $projects;
    }
}
```

`ProjectRowResource.php`:

```php
<?php

namespace Modules\Assign\Transformers\ProspectiveProjectResultResource;

use Illuminate\Http\Resources\Json\JsonResource;
use Modules\Assign\Entities\ProspectiveProject;

class ProjectRowResource extends JsonResource
{
    public function toArray($request)
    {
        $group = $this->result_group;   // service gắn sẵn, xem sortRows()

        return [
            'id'            => $this->id,
            'code'          => $this->code,
            'name'          => $this->name,
            'created_at'    => optional($this->created_at)->format('d/m/Y'),
            'created_in_period' => (bool) $this->created_in_period,
            // R7: tiến trình TẠI CUỐI KỲ, không phải tiến trình hôm nay
            'status'        => (int) $this->status_at_end,
            'status_text'   => $this->status_label,
            // Tiến trình hiện pill XÁM TRUNG TÍNH kèm số bước — 11 tiến trình mà tô 11 màu
            // thì bảng loang lổ; màu để dành cho 3 nhóm kết quả.
            'status_color'  => '#6B7280',
            'dept_name'     => $this->dept_name,
            'part_name'     => $this->part_name,
            'emp_name'      => $this->emp_name,
            'province_name' => $this->province_name,
            'scope_name'    => $this->scope_name,
            'industry_name' => $this->industry_name,
            'customer_name' => $this->customer_name,
            'result'        => $group,
            'result_text'   => ['won' => 'Thành công', 'lost' => 'Thất bại', 'open' => 'Đang triển khai'][$group],
            'result_color'  => ['won' => '#16A34A',   'lost' => '#DC2626',  'open' => '#2563EB'][$group],
            // Lý do thất bại CHỈ có giá trị ở dòng Thất bại, còn lại null ⇒ FE hiện "—"
            'closed_reason' => $group === 'lost' ? $this->closed_reason_name : null,
            // null ⇒ FE hiện "—", Excel để ô RỖNG. Dòng Thất bại LUÔN null (chốt 09/09/2026).
            'amount'        => $this->row_amount,
        ];
    }
}
```

- [x] **Bước 4: Viết `sortRows()` — gắn sẵn `result_group`, `row_amount`, `status_label`**

```php
/**
 * Sắp xếp 7 cột. Mặc định "Ngày lập dự án" giảm dần.
 *
 * ⚠️ Dòng THẤT BẠI không có giá trị hiện ra ⇒ khoá sắp xếp cột Giá trị của chúng = 0 để
 * chúng dồn về một đầu, không nằm lẫn giữa các dòng có số theo một giá trị KHÔNG hiện ra.
 */
private function sortRows($projects, string $sort, string $dir)
{
    $statusNames = collect(ProspectiveProject::STATUS)->keyBy('id');

    foreach ($projects as $p) {
        // R7: mọi thứ dưới đây bám TRẠNG THÁI TẠI CUỐI KỲ, không phải tiến trình hôm nay
        $s = (int) $p->status_at_end;
        $group = $this->resultGroupOf($s);
        $p->result_group = $group;
        $p->status_label = $s . ' ' . ($statusNames[$s]['name'] ?? '');
        $p->row_amount = $group === 'won'  ? $this->contractAmountFor($p)
                       : ($group === 'open' ? $this->expectedAmountFor($p) : null);
        $p->sort_amount = (float) ($p->row_amount ?? 0);
    }

    $keys = [
        'dept' => 'dept_name', 'emp' => 'emp_name', 'province' => 'province_name',
        'scope' => 'scope_name', 'created_at' => 'created_at', 'result' => 'result_group',
        'amount' => 'sort_amount',
    ];
    $key = $keys[$sort] ?? 'created_at';

    $sorted = $projects->sortBy($key, SORT_REGULAR, $dir === 'desc');

    return $sorted->values();
}
```

- [x] **Bước 5: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-api && git add Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php Modules/Assign/Transformers/ProspectiveProjectResultResource/
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026). Stage để `git diff HEAD` bắt được cả file mới, phục vụ khâu review.

---

### Task 8: `filterOptions()`

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php`

**Interfaces:**
- Produces: `filterOptions(Request $r): array` với các khoá `companies, departments, parts, employees,
  provinces, customers, scopes, industries, statuses, results`

- [x] **Bước 1: Viết hàm — 1 endpoint duy nhất cho toàn bộ ô lọc**

```php
/**
 * Toàn bộ danh mục của toolbar trong MỘT request (CLAUDE.md: 1 màn càng ít API càng tốt —
 * không bắn 8 API danh mục rời rạc lúc mở màn).
 *
 * Danh mục Phòng ban / Bộ phận / Nhân viên thu hẹp theo CÔNG TY đang chọn.
 * Ô Công ty: quyền tổng công ty thì liệt kê mọi công ty, còn lại chỉ công ty trong hồ sơ.
 */
public function filterOptions(Request $request): array
{
    $allowed = $this->allowedCompanyIds();
    $companyQuery = DB::table('companies')->select('id', 'name')->orderBy('name');
    if ($allowed !== null) {
        $companyQuery->whereIn('id', $allowed);
    }
    $companies = $companyQuery->get();

    $companyId = (int) $request->get('company_id', optional($companies->first())->id);

    $departments = DB::table('departments')->where('company_id', $companyId)
        ->select('id', 'name')->orderBy('name')->get();
    $deptIds = $departments->pluck('id')->all();

    $parts = DB::table('parts')->whereIn('department_id', $deptIds)
        ->select('id', 'name', 'department_id')->orderBy('name')->get();

    // Nhân viên hiển thị theo khuôn CHUẨN: "Tên nhân viên - Mã phòng - Mã nhân viên"
    // (chốt 11/09/2026, áp cho MỌI màn). BE dựng nhãn bằng employeeOptionLabel().
    // ⚠️ employeeOptionLabel() nhận ĐÚNG 1 THAM SỐ là object/array có fullname + department_code
    // + code (app/Helper/FormatHelper.php:1217) — KHÔNG phải 3 tham số rời.
    $employees = DB::table('employees as e')
        ->leftJoin('departments as d', 'd.id', '=', 'e.department_id')
        ->whereIn('e.department_id', $deptIds)
        ->select('e.id', 'e.fullname', 'e.code', 'd.code as department_code')
        ->orderBy('e.fullname')
        ->get()
        ->map(function ($e) {
            return ['id' => $e->id, 'name' => employeeOptionLabel($e)];
        });

    return [
        'companies'   => $companies,
        'departments' => $departments,
        'parts'       => $parts,
        'employees'   => $employees,
        'provinces'   => $this->provinceOptions($companyId),
        'customers'   => $this->customerOptions($companyId),
        'scopes'      => DB::table('scopes')->select('id', 'name')->orderBy('name')->get(),
        'industries'  => DB::table('industries')->select('id', 'name', 'scope_id')->orderBy('name')->get(),
        // Ô Tiến trình chỉ liệt kê 2..12 — id 1 (Đang tạo) không bao giờ lên báo cáo
        'statuses'    => collect(ProspectiveProject::STATUS)
            ->filter(function ($s) { return $s['id'] >= 2; })
            ->map(function ($s) { return ['id' => $s['id'], 'name' => $s['id'] . ' ' . $s['name']]; })
            ->values(),
        'results'     => [
            ['id' => 'won',  'name' => 'Chuyển đổi thành công'],
            ['id' => 'lost', 'name' => 'Thất bại'],
            ['id' => 'open', 'name' => 'Vẫn tiếp tục triển khai'],
        ],
    ];
}
```

⚠️ **KHÔNG viết mới `provinceOptions()`** — đã có sẵn `CustomerController::provinces`
(`Modules/Assign/Routes/api.php:135`, đường dẫn `/assign/customers/provinces`). Gọi lại logic đó
thay vì dựng bản riêng; nếu cần gọi chéo controller thì tách phần thân sang service dùng chung
(**hỏi trước khi sửa hàm dùng chung**, theo CLAUDE.md).

`customerOptions()` dùng **search server-side có `limit`** (khách hàng là danh mục lớn) — KHÔNG
load toàn bộ danh sách vào ô select.

⚠️ **Danh mục bị khoá vẫn phải hiện ở bản ghi đang dùng nó**: mọi danh mục trả về
(`scopes`, `industries`, `departments`, `parts`) phải kèm cờ **`is_locked`**. FE **không phải khai
gì** — `utils/select2LockedOption.js` đã được `V2BaseSelect` gọi sẵn, tự gắn 🔒 và tự ẩn option
khoá mà bản ghi hiện tại không dùng. Thiếu `is_locked` ở BE là mất 🔒 im lặng.

Bảng thật đã kiểm: `companies` · `departments` · `parts` · `employees` · `scopes` · `industries`.

- [x] **Bước 2: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-api && git add Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026). Stage để `git diff HEAD` bắt được cả file mới, phục vụ khâu review.

---

### Task 9: Controller + routes — ca test API 1–6 phải XANH

**Files:**
- Create: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/ProspectiveProjectResultReportController.php`
- Modify: `hrm-api/Modules/Assign/Routes/api.php` (trong cùng `Route::group` với `potential-customer-care`, quanh dòng 992)

**Interfaces:**
- Consumes: toàn bộ public method của service (Task 4–10)
- Produces: 6 endpoint theo spec mục 5

- [x] **Bước 1: Viết controller — mỏng, không chứa logic**

```php
<?php

namespace Modules\Assign\Http\Controllers\Api\V1;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Modules\Assign\Services\Report\ProspectiveProjectResultReportService;

class ProspectiveProjectResultReportController extends Controller
{
    private $service;

    public function __construct(ProspectiveProjectResultReportService $service)
    {
        $this->service = $service;
    }

    public function index(Request $request)
    {
        return response()->json(['data' => $this->service->report($request)]);
    }

    public function filterOptions(Request $request)
    {
        return response()->json(['data' => $this->service->filterOptions($request)]);
    }

    public function projectList(Request $request)
    {
        return response()->json(['data' => $this->service->projectList($request)]);
    }

    // R3 (13/09): 3 stub dưới đây PHẢI có ngay ở task này — route đã khai, không có method
    // thì Laravel nổ 500 khó đọc và bộ e2e của task này không chạy được.
    // Task 10 THAY THẾ cả 3 bằng bản thật.
    public function export(Request $request)            { return response()->json(['message' => 'Chưa triển khai'], 501); }
    public function exportProjectList(Request $request) { return response()->json(['message' => 'Chưa triển khai'], 501); }
    public function printListData(Request $request)     { return response()->json(['message' => 'Chưa triển khai'], 501); }
}
```

Và trong service, `report()` gom 3 mảnh:

```php
public function report(Request $request): array
{
    $projects = $this->getProjects($request);
    $criteria = $request->get('criteria', 'dept');

    $data = [
        'summary' => $this->summary($request),
        'tree'    => $this->buildTree($projects, $criteria),
        'total'   => $this->metricsOf($projects),
    ];

    // Chỉ để ca e2e soi tập dự án — TUYỆT ĐỐI không lộ trên production
    if (config('app.debug')) {
        $data['debug_project_ids'] = $projects->pluck('id')->all();
    }

    return $data;
}
```

- [x] **Bước 2: Thêm 6 route**

```php
        // Báo cáo kết quả thực hiện dự án TKT (feature bao-cao-ket-qua-du-an-tkt).
        // KHÔNG gắn checkPermission: gate 4 cấp nằm trong service để giữ cấp fallback
        // "chỉ thấy dự án mình phụ trách / mình tạo".
        Route::get('/prospective-project-results', [ProspectiveProjectResultReportController::class, 'index']);
        Route::get('/prospective-project-results/filter-options', [ProspectiveProjectResultReportController::class, 'filterOptions']);
        Route::get('/prospective-project-results/project-list', [ProspectiveProjectResultReportController::class, 'projectList']);
        Route::get('/prospective-project-results/export', [ProspectiveProjectResultReportController::class, 'export']);
        Route::get('/prospective-project-results/project-list/export', [ProspectiveProjectResultReportController::class, 'exportProjectList']);
        // Tên `print-list-data` là contract của utils/mixins/reportPrintPreviewMixin.js — ĐỪNG ĐỔI
        Route::get('/prospective-project-results/print-list-data', [ProspectiveProjectResultReportController::class, 'printListData']);
```

⚠️ 3 route cuối (`export`, `project-list/export`, `print-list-data`) làm ở **Task 10** — tạm để
method rỗng trả `501` để route tồn tại mà không gây lỗi 500 khó đọc.

- [x] **Bước 3: Chạy toàn bộ ca API — kỳ vọng 6/6 XANH**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test tkt-result-report.api --workers=1
```
Kỳ vọng: **6 passed**. ⚠️ Bộ test chạy `serial` — **phải đọc dòng tổng kết**, ca sau in
"did not run" nghĩa là ca trước fail chứ không phải pass.

- [x] **Bước 4: Nếu đỏ — sửa theo `systematic-debugging`, KHÔNG sửa mò**

Log BE: `hrm-api/storage/logs/laravel-$(date +%Y-%m-%d).log`

- [x] **Bước 5: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-api && git add Modules/Assign/Http/Controllers/Api/V1/ProspectiveProjectResultReportController.php Modules/Assign/Routes/api.php Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026). Stage để `git diff HEAD` bắt được cả file mới, phục vụ khâu review.

---

### Task 10: Xuất Excel + dữ liệu bản in

**Files:**
- Create: `hrm-api/Modules/Assign/Services/Report/ProspectiveProjectResultPrintService.php`
- Modify: controller (3 method) + service
- Đọc tham khảo: `hrm-api/Modules/Assign/Services/Report/PotentialCustomerCarePrintService.php`,
  trait `Modules/Assign/Services/Concerns/PrintsCompanyLetterhead`

**Interfaces:**
- Produces: `export()` · `exportProjectList()` · `printListData()`

- [x] **Bước 1: Đọc skill trước khi viết**

```bash
cat HRM/.claude/skills/export-excel/SKILL.md
cat HRM/.claude/skills/print-page/SKILL.md
```

- [x] **Bước 2: Viết print service dùng trait letterhead**

⚠️ **Letterhead lấy theo `company_id` GHI TRÊN BÁO CÁO** (ô lọc Công ty), **không** theo người đăng
nhập. Dùng `PrintsCompanyLetterhead::headerUrl()`; thiếu `ERP_URL` thì trả nguyên path chứ **không**
trả chuỗi rỗng.

- [x] **Bước 3: Excel bảng theo dõi — xuất ĐỦ MỌI CẤP**

Bản in / Excel **luôn xuất đủ mọi cấp**, không phụ thuộc cấp đang xem trên màn.

```php
/**
 * Làm phẳng cây để xuất Excel / bản in: ĐỦ MỌI CẤP, kèm STT phân cấp (1, 1.1, 1.1.1)
 * và độ sâu để thụt lề. KHÔNG phụ thuộc `level` đang chọn trên màn.
 */
private function flattenTree(array $nodes, string $prefix = '', int $depth = 0): array
{
    $rows = [];
    $i = 1;
    foreach ($nodes as $node) {
        $stt = $prefix === '' ? (string) $i : $prefix . '.' . $i;
        $rows[] = ['stt' => $stt, 'depth' => $depth, 'name' => $node['name'], 'metrics' => $node['metrics']];
        $rows = array_merge($rows, $this->flattenTree($node['children'], $stt, $depth + 1));
        $i++;
    }

    return $rows;
}
```

⚠️ **Ô số phải là SỐ THẬT + `data-format="#,##0"`**, không đổ chuỗi đã format (Excel báo "number
stored as text", SUM ra 0). Ô `Giá trị HĐ`, kỳ vọng khuyết và mọi dòng Thất bại để **RỖNG**, không ghi 0.

- [x] **Bước 4: Viết ca test export**

```ts
test('7. Excel bảng theo dõi xuất ĐỦ MỌI CẤP, không phụ thuộc cấp trên màn', async () => {
  const res = await api.get(`${REPORT}/export?${new URLSearchParams({
    period: 'custom', from: fx.period.from, to: fx.period.to,
    company_id: String(fx.company_id), criteria: 'dept',
  })}`);
  expect(res.status()).toBe(200);
  expect(res.headers()['content-type']).toContain('excel');
  expect((await res.body()).length).toBeGreaterThan(1000);
});

test('8. Dòng Thất bại không mang giá trị ở mọi đầu ra', async () => {
  const res = await api.get(`${REPORT}/project-list?${new URLSearchParams({
    period: 'custom', from: fx.period.from, to: fx.period.to,
    company_id: String(fx.company_id), criteria: 'dept', metric: 'lost', per_page: '200',
  })}`);
  const rows = (await res.json()).data.rows as any[];
  expect(rows.length).toBeGreaterThan(0);
  expect(rows.every((r) => r.amount === null), 'dòng Thất bại phải có amount = null').toBe(true);
});
```

- [x] **Bước 5: Chạy — kỳ vọng 8/8 xanh**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test tkt-result-report.api --workers=1
```

- [x] **Bước 6: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-api && git add Modules/Assign/
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026). Stage để `git diff HEAD` bắt được cả file mới, phục vụ khâu review.

---

# Phase 3 — FE

### Task 11: Khung màn + toolbar lọc

**Files:**
- Create: `hrm-client/pages/assign/report/prospective-project-results/index.vue`
- Create: `hrm-client/pages/assign/report/prospective-project-results/format.js`
- Modify: `hrm-client/components/menu-sidebar.js` (quanh dòng 250)
- Đọc tham khảo: `hrm-client/pages/assign/report/potential-customer-care/index.vue`

**Interfaces:**
- Consumes: `GET /assign/report/prospective-project-results` + `/filter-options`
- Produces: state `filters`, `summary`, `tree`, `total` cho Task 12–16

- [x] **Bước 1: Đọc skill + màn mẫu trước khi viết**

```bash
cat HRM/.claude/skills/list-page/SKILL.md
sed -n '1,120p' HRM/hrm-client/pages/assign/report/potential-customer-care/index.vue
```

- [x] **Bước 2: Thêm mục menu**

Trong `components/menu-sidebar.js`, ngay sau mục *Dự án TKT theo PB - NV KD*:

```js
            {
                label: 'Kết quả thực hiện dự án TKT',
                link: '/assign/report/prospective-project-results',
            },
```

- [x] **Bước 3: Dựng toolbar — 3 ô khung đứng đầu, cố định**

Thứ tự `Kỳ theo dõi ▸ Công ty ▸ Tiêu chí theo dõi`, rồi các ô sau **xếp đúng thứ tự cấp của tiêu chí
đang xem**:

| Tiêu chí | Thứ tự ô lọc |
|---|---|
| `dept` | Phòng ban · Bộ phận · Nhân viên · Thị trường · Khách hàng · Tiến trình · Kết quả |
| `market` | Thị trường · Phòng ban · Bộ phận · Nhân viên · Khách hàng · Tiến trình · Kết quả |
| `scope` | Lĩnh vực · Nhóm ngành · Phòng ban · Bộ phận · Nhân viên · Khách hàng · Tiến trình · Kết quả |

Yêu cầu bắt buộc:
- **Ô đang ẩn phải XOÁ GIÁ TRỊ** (chống lọc ngầm): *Thị trường* chỉ hiện ở `dept`/`market`;
  *Lĩnh vực* + *Nhóm ngành* chỉ hiện ở `scope`.
- ⚠️ **Nhóm ngành thuộc NHIỀU lĩnh vực** — quan hệ nhiều-nhiều qua pivot `industry_scopes`, đã xác
  nhận trên dữ liệu thật ngày 13/09 (industry 35/38/70 mỗi cái thuộc 2 lĩnh vực). `filter-options`
  trả mỗi nhóm ngành kèm **`scope_ids` (MẢNG)**, KHÔNG phải `scope_id`.
  Khi user chọn *Lĩnh vực*, ô *Nhóm ngành* phải lọc bằng
  `industry.scope_ids.includes(selectedScopeId)`. Dùng `industry.scope_id === selectedScopeId` là
  **ô lọc chết im lặng** — chỉ ra đúng vài nhóm ngành may mắn thuộc 1 lĩnh vực, không báo lỗi gì.
- **Ô Công ty bắt buộc**, không có mục *Tất cả*, mặc định công ty đầu danh mục. Bề rộng **292px**
  (khuôn chung 150px), **bỏ tiền tố "CÔNG TY "** khi hiển thị nhưng `title` giữ **tên đầy đủ**.
- **Xoá lọc** đưa về: công ty đầu danh mục · kỳ *Tháng này* · tiêu chí *Theo Phòng ban* · cấp 0.
  **KHÔNG** đưa ô Công ty về rỗng (mở rộng phạm vi xem bằng 1 cú bấm).
- Placeholder: màn có nhãn floating thì **BỎ placeholder trùng nhãn**; chỉ giữ khi nói thêm
  (`Gõ tối thiểu 2 ký tự`, `dd/mm/yyyy`). **CẤM** `Tất cả`, `Chọn...`, để trống.
- Cờ quyền khởi tạo `false`, chỉ set từ `$store.state.permissions`.

- [x] **Bước 4: Verify Playwright — ĐO BẰNG SỐ**

```
Mở http://127.0.0.1:3000/assign/report/prospective-project-results
```
Đo và ghi lại:
1. `document.documentElement.scrollWidth - clientWidth` = **0** (không cuộn ngang trang).
2. Ô Công ty: `getBoundingClientRect().width` ≈ **292**, và **tên dài nhất hiện đủ** — đo bằng
   `Range.selectNodeContents()`, KHÔNG dùng `scrollWidth` (tooltip `::after` thổi phồng số này).
3. Đổi tiêu chí 3 lần → đọc `[...document.querySelectorAll('.filter-field')].map(e => e.dataset.dim)`
   → đúng thứ tự bảng trên, 3 ô khung luôn đứng đầu.
4. Ô bị ẩn có giá trị = rỗng.

- [x] **Bước 5: Tự kiểm không có HTML thô**

```bash
cd HRM/hrm-client && grep -rn '<input \|<textarea\|<select \|<button \|<label \|class="btn \|class="form-control' pages/assign/report/prospective-project-results/ | grep -v V2Base
```
Kỳ vọng: **RỖNG**.

- [x] **Bước 6: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-client && git add pages/assign/report/prospective-project-results/ components/menu-sidebar.js
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026). Stage để `git diff HEAD` bắt được cả file mới, phục vụ khâu review.

---

### Task 12: Dải tổng hợp

**Files:**
- Create: `hrm-client/pages/assign/report/prospective-project-results/components/ResultSummaryBlocks.vue`
- Đọc tham khảo: `hrm-client/pages/assign/report/potential-customer-care/components/CareSummaryBlocks.vue`

**Interfaces:**
- Consumes: `summary` từ Task 11
- Produces: sự kiện `@drill="{ metric, drillKey, path }"` cho Task 14.
  **Ruling R4 (13/09)**: dải tổng hợp phát **cùng shape** với bảng, với `drillKey: ''` và
  `path: []` — `drillKey` rỗng nghĩa là dòng `TỔNG`, popup không bỏ cột nào (luật 2 của spec).
  Một shape duy nhất để `index.vue` chỉ cần **một** handler, không phân nhánh theo nguồn phát.

- [x] **Bước 1: Dựng 2 khối cùng 1 hàng, mỗi khối 3 ô con xếp ngang**

- Mỗi ô con: số to + tỷ lệ % trên tổng.
- Header khối **không lặp số to**; có nút *Thu gọn* dùng chung khuôn `.rsum-toggle`.
- Dòng meta: `Tổng hợp kỳ dd/mm/yyyy – dd/mm/yyyy · N dự án · M khách hàng`.
  ⚠️ **Phase 1 BỎ đoạn `Giá trị HĐ X tỷ`** vì `meta.contract_amount = null`.
- Mọi số trong dải **bấm được** → mở popup.

- [x] **Bước 2: Verify Playwright — ĐO BẰNG SỐ**

1. `created_before + created_in === total` (đọc từ DOM, không từ API).
2. `won + lost + open === total`.
3. Dải tổng hợp chiếm ≤ **25% chiều cao màn** — đo
   `document.querySelector('.rsum').getBoundingClientRect().height / window.innerHeight`.
4. Dòng meta **không chứa** chuỗi `Giá trị HĐ`.

- [x] **Bước 3: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-client && git add pages/assign/report/prospective-project-results/components/ResultSummaryBlocks.vue
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026). Stage để `git diff HEAD` bắt được cả file mới, phục vụ khâu review.

---

### Task 13: Bảng theo dõi 10 cột + cây + chọn cấp

**Files:**
- Create: `hrm-client/pages/assign/report/prospective-project-results/components/ResultTrackingTable.vue`
- Create: `hrm-client/pages/assign/report/prospective-project-results/components/DrillNum.vue`
- Đọc tham khảo: `potential-customer-care/components/CareTrackingTable.vue` + `DrillNum.vue`

**Interfaces:**
- Consumes: `tree` + `total` từ Task 11
- Produces: `@drill="{ metric, drillKey, path }"` cho Task 14

- [x] **Bước 1: Dựng bảng 10 cột**

`STT · Nội dung theo dõi · Tổng dự án · Đang triển khai · Đóng trong kỳ · Thành công · Thất bại ·
Tỷ lệ thành công · Giá trị HĐ · Giá trị dự kiến`

- Tiêu đề cột **viết hoa chữ đầu** (không `text-transform: uppercase`) + `white-space: nowrap`.
- Đúng **1 dòng `TỔNG`**, nhãn đổi theo tiêu chí (`PHÒNG BAN / BỘ PHẬN / NHÂN VIÊN / THỊ TRƯỜNG`…).
- **Icon ⓘ cạnh 2 cột tiền**: *"Giá trị HĐ cộng trên dự án Thành công · Giá trị dự kiến cộng trên dự
  án Đang triển khai · Dự án Thất bại không ghi nhận giá trị"*.
- **Icon ⓘ cạnh cột `Giá trị HĐ`** thêm dòng: *"Chờ nguồn hợp đồng HRM — hiện chưa ghi nhận"*.
  Mọi ô của cột này hiện `—` (**không** hiện `0`).
- `Tỷ lệ thành công` mẫu số 0 → `—`; cột này **không bấm được** (số dẫn xuất).
- Chữ trong ô **để thường**, không in đậm, kể cả cột tên.

⚠️ **Bẫy đã trả giá ở màn anh em**: `.rsum-tb { min-width: 1280px }` là số cứng của bảng 10 cột —
bảng này đúng 10 cột nên giữ được, nhưng **đừng copy số đó sang bảng khác số cột**.

- [x] **Bước 2: Phân biệt cấp khi bung hết — port nguyên cách đã chốt**

- Nền dòng cha theo **TỪNG CẤP**: `d0 #dceaf4` · `d1 #e9f3f9` · `d2 #f2f8fb`. KHÔNG dùng 1 rule
  `--open` chung.
- **Vạch cấp bên trái ô tên** — nấc 22px, dựng bằng `::before` tuyệt đối (**KHÔNG** `border-left`
  của `td`, border sẽ nằm ở mép ô chứ không đúng chỗ thụt lề): `d0` 3px `#0a7c88` tại `left:2px`;
  `d1/d2/d3` 2px alpha `.55 / .32 / .18` tại `24 / 46 / 68px`.
- Kẻ đậm 2px `#b6d8e0` phía trên mỗi dòng cấp 0.
- ⚠️ Selector phải là `td.rsum-tb__name--dN` — `.rsum-tb td` (0,1,1) sẽ đè `.rsum-tb__name--dN`
  (0,1,0) làm thụt lề không ăn.

- [x] **Bước 3: Select chọn cấp — hiểu theo TÊN CẤP, không theo độ sâu**

Select nằm trong ô tiêu đề cột *Nội dung theo dõi*:
- `dept`: `Chỉ Phòng ban · Đến Bộ phận · Đến Nhân viên · Tất cả cấp (đến Thị trường)`
- `market`: `Chỉ Thị trường · Đến Phòng ban · Đến Bộ phận · Tất cả cấp (đến Nhân viên)`
- `scope`: `Chỉ Lĩnh vực · Đến Nhóm ngành · Tất cả cấp (đến Phòng ban)`

Chỉ bung node có con **thuộc cấp còn trong phạm vi** ⇒ chọn *Đến Bộ phận* thì phòng không chia bộ
phận dừng ở Phòng ban, **không lòi nhân viên ra sớm**. Bấm mũi tên từng dòng vẫn tự do (chỉ đổi
`expanded`, không đụng `level`). Đổi sang tiêu chí ít cấp hơn thì cấp đang chọn **tự kẹp**.

- [x] **Bước 4: Bọc `V2BaseTableScroll` — thanh cuộn ngang cả TRÊN và DƯỚI**

Không chép lại cặp `topScroll`/`tableWrapper`.

- [x] **Bước 5: Verify Playwright — ĐO BẰNG SỐ (bắt buộc)**

1. **2 đẳng thức bất biến trên DOM** ở mọi dòng, cả 3 tiêu chí.
2. **Dòng cha = tổng dòng con** ở 7 cột cộng được (đọc số từ ô bảng, không từ API).
3. **Dòng `TỔNG` = số ở dải tổng hợp** (4 chỉ tiêu).
4. Thụt lề 4 cấp: đo `getComputedStyle(td, '::before').left` = `2 / 24 / 46 / 68` px.
5. Chọn *Đến Bộ phận*: đếm dòng cấp nhân viên = **0** ở phòng không chia bộ phận.
6. Cột `Giá trị HĐ`: mọi ô `textContent.trim() === '—'`, **không ô nào là `0`**.
7. `scrollWidth - clientWidth === 0` ở cả trang.

- [x] **Bước 6: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-client && git add pages/assign/report/prospective-project-results/components/
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026). Stage để `git diff HEAD` bắt được cả file mới, phục vụ khâu review.

---

### Task 14: Popup danh sách dự án

**Files:**
- Create: `hrm-client/pages/assign/report/prospective-project-results/components/ProjectListModal.vue`
- Đọc tham khảo: `potential-customer-care/components/DemandListModal.vue`

**Interfaces:**
- Consumes: `GET /prospective-project-results/project-list` (trả `columns` + `rows` + `total`)
- Produces: mở panel chi tiết dự án khi bấm tên

- [x] **Bước 1: Đọc skill modal trước khi viết**

```bash
cat HRM/.claude/skills/modal-popup/SKILL.md
```
Popup dựng trên `components/modal/V2BaseModal.vue`; select trong modal dùng `V2BaseSelectInModal`.

- [x] **Bước 2: Dựng popup**

- **Bộ cột do BE trả** (`columns`) — FE **không tự suy**, để bảng, bản in và Excel không lệch nhau.
- **Khối tổng hợp MẶC ĐỊNH THU GỌN** — mỗi lần mở đều đặt lại `drillSumCollapsed = true`.
  Ẩn bằng thuộc tính `hidden` trên khối bọc, **KHÔNG** `style.display`.
  Nhãn nút: *"Xem tổng hợp"* khi thu, *"Thu gọn"* khi mở.
- **Tiêu đề nêu rõ đối tượng**: *"Đang xem &lt;chỉ tiêu&gt; theo &lt;Cấp&gt;: &lt;Tên&gt;"*; node sâu
  thì dòng phụ hiện đường dẫn cấp cha. Dòng phụ dùng **chữ XÁM** (`#6b7280` nhãn, `#374151` giá trị),
  **không in đậm, KHÔNG tô đỏ**.
- **Chip phân bổ**: luôn có *Phòng ban* + 2 chiều cơ cấu theo tiêu chí. Dải chip **cuộn ngang**
  (scrollbar mảnh) khi nhiều mục — đây là hành vi của khuôn gốc, không phải chip bị cắt.
- **Sắp xếp 7 cột**, icon = **2 mũi tên ngược chiều** (chưa sắp thì cả 2 mờ `opacity .3`). Mặc định
  *Ngày lập dự án* giảm dần; mở popup mới thì reset.
- Cột **Tên dự án** gắn chip *"Lập trong kỳ"* — **sắc lam**, KHÔNG xanh lá (tránh lẫn badge "Thành công").
- **Phân trang**, mặc định 20 dòng.

- [x] **Bước 3: Verify Playwright — 4 luật bỏ cột (ĐO BẰNG SỐ)**

1. Popup theo **Bộ phận** → không còn cột *Phòng ban* lẫn *Bộ phận*; 2 ô lọc tương ứng ẩn và
   **giá trị rỗng**.
2. Popup của phòng **không chia bộ phận** → mất cột *Bộ phận*.
3. Popup theo **Nhóm ngành** → mất cột *Lĩnh vực* + *Nhóm ngành*, ẩn ô lọc *Lĩnh vực*.
4. Popup từ dòng **TỔNG** → **đủ cột**, không bỏ cột nào.
5. Lọc trong popup **không làm cột Bộ phận nhấp nháy** — đếm số cột trước/sau khi lọc: bằng nhau.
6. Dòng Thất bại: ô *Giá trị* = `—`; ô *Lý do thất bại* có chữ.
7. Dòng Thành công: ô *Giá trị* = `—` (phase 1 chưa có nguồn hợp đồng).

⚠️ **Escape đóng cả modal** — ca test đóng popup phải bấm nút, không gõ Escape.
⚠️ Chờ `.stats-row` là **chờ sai mốc** (danh sách chưa render) — chờ đúng selector của bảng popup.

- [x] **Bước 4: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-client && git add pages/assign/report/prospective-project-results/components/ProjectListModal.vue
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026). Stage để `git diff HEAD` bắt được cả file mới, phục vụ khâu review.

---

### Task 15: Bản in + Xuất Excel trên FE

**Files:**
- Create: `hrm-client/pages/assign/report/prospective-project-results/components/PrintOptionsModal.vue`
- Modify: `index.vue` (2 nút toolbar) + `ProjectListModal.vue` (2 nút footer)
- **Dùng lại**: `components/print/ReportPrintPreviewModal.vue`, `utils/print/reportPrintStyle.js`,
  `utils/mixins/reportPrintPreviewMixin.js`

**Interfaces:**
- Consumes: `/export`, `/project-list/export`, `/print-list-data` (Task 10)

- [x] **Bước 1: Đọc skill in trước khi viết**

```bash
cat HRM/.claude/skills/print-page/SKILL.md
```

- [x] **Bước 2: Nối 4 đầu ra**

| Vị trí | Nút |
|---|---|
| Toolbar | *In báo cáo* · *Xuất Excel* |
| Footer popup | *In danh sách* · *Xuất Excel danh sách* |

Tất cả **bám bộ lọc đang áp dụng**; In/Excel của popup bám **đúng thứ tự đang sắp**.

Yêu cầu bản in (từ skill `print-page`):
- `#content` rộng đúng khổ, padding = lề `@page`, viền `1px #d3d3d3` + bo 5px + bóng nhẹ,
  căn giữa bằng `margin: 0 auto` (**KHÔNG** flex `align-items:center` — sẽ căn giữa cả nút In).
- Nền quanh giấy dùng màu xám `#eee` có sẵn ở `layouts/print.vue`; màn in **KHÔNG** khai
  `background` riêng. `.print-preview` cần `min-height: 100vh` + `display: flow-root`
  (thiếu `flow-root` là hở dải khác màu 16px đầu trang).
- Nút **In** là `V2BaseButton primary size="sm"`, căn phải thẳng mép phải tờ giấy.
- Đầu bản in ghi: kỳ, số dự án, số khách hàng, phân bổ lập trước/trong kỳ, kết quả cuối kỳ và
  **bộ lọc đang áp dụng**. Tên công ty in **tên đầy đủ**, không phải tên đã cắt tiền tố.

- [x] **Bước 3: Verify Playwright — ĐO BẰNG SỐ**

1. Bản in bảng theo dõi: đếm số dòng = **đủ mọi cấp**, kể cả khi trên màn đang ở cấp 0.
2. In/Excel của popup: **5 dòng đầu trùng thứ tự** với bảng đang hiện trên màn.
3. Excel: mở lại bằng script kiểm ô số là **số thật**, ô `Giá trị HĐ` và mọi dòng Thất bại **RỖNG**
   (không phải 0).
   ⚠️ Reader PhpSpreadsheet **cắt sạch khoảng trắng đầu ô** và **ép "1.10" thành số 1.1** — đừng
   dựa vào 2 thứ đó khi so sánh.
4. `.print-preview` không hở dải màu ở đầu trang: đo `getBoundingClientRect().top` của con đầu tiên.

- [x] **Bước 4: Stage file (KHÔNG commit)**

```bash
cd HRM/hrm-client && git add pages/assign/report/prospective-project-results/
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`** — `CLAUDE.md` cấm commit khi chưa được yêu cầu
(chốt 13/09/2026). Stage để `git diff HEAD` bắt được cả file mới, phục vụ khâu review.

---

# Phase 4 — Kiểm chứng toàn màn

### Task 16: Bộ ca e2e UI

**Files:**
- Create: `HRM/e2e/tests/assign/tkt-result-report.spec.ts`
- Đọc tham khảo: `HRM/e2e/tests/assign/potential-customer-care.spec.ts`

**Interfaces:**
- Consumes: `seedTktResultFixture()` (Task 3)

- [x] **Bước 1: Viết 8 ca UI**

1. Mở màn → dòng `TỔNG` khớp dải tổng hợp (4 chỉ tiêu).
2. 2 đẳng thức bất biến trên DOM, cả 3 tiêu chí.
3. Dòng cha = tổng dòng con ở 7 cột cộng được.
4. Đổi tiêu chí → thứ tự ô lọc, nhãn select cấp, ô lọc riêng, chip phân bổ đều đổi đúng bảng khai báo.
5. Chọn cấp *Đến Bộ phận* không lòi dòng Nhân viên của phòng không chia bộ phận.
6. 4 luật bỏ cột của popup.
7. Cột `Giá trị HĐ` mọi ô = `—`, không ô nào là `0`.
8. **Fail-closed**: đăng nhập bằng `fx.noperm_email` → không thấy dự án fixture nào.

- [x] **Bước 2: Chạy TOÀN BỘ bộ test của màn**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test tkt-result-report --workers=1
```
Kỳ vọng: **8 API + 8 UI = 16 passed**.
⚠️ Đọc **dòng tổng kết**, không suy từ việc cuối log không có chữ "failed".

- [x] **Bước 3: Chạy lại toàn bộ e2e của phân hệ Assign — chống hồi quy**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test tests/assign --workers=1
```
⚠️ 4 ca UI của bộ **meeting** đã đỏ sẵn trên nhánh `tpe` từ trước (fixture chủ trì thiếu
`company_employees`) — **không phải lỗi của feature này**, ghi nhận chứ không sửa.

- [x] **Bước 4: Commit (chỉ phần trong repo)**

⚠️ `HRM/e2e/` **không thuộc repo nào** — spec test chỉ nằm trên máy này. Riêng fixture
`hrm-api/database/e2e_tkt_result_report_seed.php` **có** vào repo `hrm-api`.

```bash
cd HRM/hrm-api && git add database/e2e_tkt_result_report_seed.php
```
Chỉ `git add`, **TUYỆT ĐỐI không `git commit`**.

---

### Task 17: Đối chiếu bản Vue với mockup đã duyệt

**Files:** không tạo file mới — đây là task nghiệm thu.

- [x] **Bước 1: Mở song song mockup và bản thật**

```bash
cd HRM/.plans/gop-db/bao-cao-ket-qua-du-an-tkt && python3 -m http.server 8732 --bind 127.0.0.1 &
```
Mockup: `http://127.0.0.1:8732/bao-cao-ket-qua-du-an-tkt.html`
Bản thật: `http://127.0.0.1:3000/assign/report/prospective-project-results`

⚠️ Dùng **cổng mới** để né cache; luôn `127.0.0.1`, không `localhost`.

- [x] **Bước 2: Đối chiếu 8 điểm, ĐO BẰNG SỐ**

| # | Điểm | Cách đo |
|---|---|---|
| 1 | Số cột bảng theo dõi | `document.querySelectorAll('thead th').length` = **10** ở cả 2 |
| 2 | Nhãn cột | so từng chuỗi, viết hoa chữ đầu, `white-space: nowrap` |
| 3 | Thứ tự ô lọc theo 3 tiêu chí | so mảng `dataset.dim` |
| 4 | Nhãn select chọn cấp theo 3 tiêu chí | so từng chuỗi |
| 5 | Thụt lề + vạch cấp | `getComputedStyle(td,'::before').left` = 2/24/46/68 |
| 6 | Nền dòng cha 3 cấp | `#dceaf4 / #e9f3f9 / #f2f8fb` |
| 7 | Icon ⓘ | đếm số icon + so nội dung tooltip từng cái |
| 8 | Không cuộn ngang trang | `scrollWidth - clientWidth === 0` |

- [x] **Bước 3: Ghi kết quả đo vào `plan.md` + chụp ảnh**

Lưu ảnh vào `.plans/gop-db/bao-cao-ket-qua-du-an-tkt/screenshots/2026-XX-XX-*.png`.

- [x] **Bước 4: Lệch chỗ nào thì sửa rồi đo lại**

⚠️ **SKILL THẮNG SPEC khi về hình thức UI.** Mockup lệch quy ước trong `.claude/skills/` thì theo
skill, và **phải confirm với user trước khi code** (nêu rõ: mockup ghi gì · skill quy định gì ·
đề xuất hướng nào). Chốt xong ghi vào `design.md` mục *Quyết định đã chốt*.

---

### Task 18: Tự kiểm cuối + cập nhật tài liệu

- [x] **Bước 1: Chạy 3 lệnh tự kiểm bắt buộc — cả 3 phải RỖNG**

```bash
cd HRM/hrm-client && grep -rnE "(toLocaleString|Intl\.NumberFormat)\(\s*'vi-VN'" pages/assign/report/prospective-project-results components | grep -v "new Date"
cd ../hrm-api && grep -rnE "number_format\([^)]+,\s*'.?',\s*'\.'\)" Modules/Assign/Services/Report/ProspectiveProjectResultReportService.php Modules/Assign/Services/Report/ProspectiveProjectResultPrintService.php
cd ../hrm-client && grep -rnE "can[A-Za-z]*\s*=\s*true" pages/assign/report/prospective-project-results/
```

- [x] **Bước 2: Kiểm line ending không bị phá**

```bash
cd HRM/hrm-client && git diff --stat
cd ../hrm-api && git diff --stat
```
Số dòng thay đổi lớn bất thường (cả file bị đánh dấu đổi) = đã phá line ending → trả lại ngay.

- [x] **Bước 3: Kiểm hiệu năng**

Mở màn, đếm số request API lúc load — **≤ 2** (`/` + `/filter-options`). Đo thời gian đáp
`/prospective-project-results` — **< 2s**. Vượt thì nêu ra và đề xuất gộp/tối ưu, không im lặng cho qua.

- [x] **Bước 4: Kiểm màn *Lịch sử* của dự án TKT sau migration**

Migration Task 1 sửa dữ liệu mà `SystemLogService:285` cũng đọc. Mở
`/assign/prospective-projects/{id}` của 1 dự án Thất bại cũ → mục *Lịch sử* nay hiện **2 mốc** thay
vì 1, và cả 2 mốc đọc xuôi. Không lỗi, không mốc trùng.

- [x] **Bước 5: Viết ghi chú deploy vào `design.md`**

Môi trường khác phải làm **đúng 3 bước** (spec mục 12):
1. `php artisan migrate` — 1 migration vá log.
2. **Insert thủ công** 3 quyền 1184–1186 rồi gán role (`role_has_permissions` cần `company_id`).
   ⚠️ **KHÔNG** chạy `PermissionsTableSeeder` — nó **truncate cả bảng `permissions`**.
3. Deploy code BE + FE. **Không có cron mới.**

- [x] **Bước 6: Cập nhật tài liệu**

1. `.plans/gop-db/bao-cao-ket-qua-du-an-tkt/plan.md` — đánh `[x]`, ghi checkpoint.
2. `.plans/gop-db/STATUS.md` — thêm feature vào mục *Đang làm* kèm trạng thái.
3. `.plans/gop-db/bao-cao-ket-qua-du-an-tkt/design.md` — bổ sung kết quả đo thật + chênh lệch so
   với mockup (nếu có).
4. `.plans/hrm-quotation-to-erp-contract/design.md` — ghi chú hướng lập HĐ ERP từ báo giá HRM
   **đã bị thay bằng hợp đồng HRM** (quyết định 13/09/2026).

---

## Checkpoint

### Checkpoint — 2026-09-13 (lập plan)
Vừa hoàn thành: brainstorming + spec đầy đủ
(`docs/superpowers/specs/gop-db/2026-09-13-bao-cao-ket-qua-du-an-tkt-design.md`, 13 chương) + plan này.
Đang làm dở: chưa động vào code; chưa tách nhánh ở 2 repo.
Bước tiếp theo: tách nhánh con từ `tpe` ở cả `hrm-api` và `hrm-client`, rồi chạy **Task 1**.
Blocked: không có.

**5 quyết định đã chốt (13/09/2026)** — chi tiết ở spec mục 1:
1. Cột `Giá trị`: Thành công → giá trị HĐ · Đang triển khai → kỳ vọng · Thất bại → không hiện, kèm icon ⓘ.
2. Giá trị HĐ **treo** — chờ hợp đồng HRM lập từ báo giá HRM (không dùng HĐ ERP); phase 1 giữ cột,
   hiện `—`, BE tách `contractAmountFor()` trả `null`.
3. Kỳ vọng khuyết (42%) → để trống, không thay bằng `estimated_budget`.
4. Phân quyền: 3 quyền MỚI **1184–1186**, tách khỏi 1054–1056.
5. Nhánh con của `tpe`; tài liệu giữ ở `.plans/gop-db/bao-cao-ket-qua-du-an-tkt/`.

**3 phát hiện khiến plan ngắn hơn dự kiến:**
- 12 bước tiến trình + 3 tên mới **đã có sẵn** trong `ProspectiveProject::STATUS` (bỏ được 1 task).
- Bảng `prospective_project_status_logs` + hook ghi log **đã có sẵn và đáng tin** (Redmine #11426
  đã vá 4 chỗ đổi bước bằng query builder).
- `ProspectiveProject::statusAt()` **đã có sẵn** ở dòng 686, chưa ai dùng — nhưng N+1, service phải
  tự tính hàng loạt.

### Checkpoint — 2026-09-13 (Task 18 — tự kiểm cuối, code XONG)
Vừa hoàn thành: Task 1→18 (toàn bộ 92 bước) — BE + FE + fixture e2e + bộ e2e 21 ca xanh (10 API +
11 UI) + nghiệm thu đối chiếu mockup + tự kiểm cuối (5 lệnh bắt buộc, cả 3 grep RỖNG) + cập nhật
4 tài liệu. **16 commit** trên nhánh `tpe-bao-cao-ket-qua-du-an-tkt` ở 2 repo (7 FE + 9 BE — không
phải 14 như ước tính ban đầu, đếm lại bằng `git log` tại thời điểm chốt). Toàn bộ file thay đổi đều
là **file mới** (không sửa CRLF file cũ) — `git diff --stat` sạch, không có dấu hiệu phá line ending.
Đang làm dở: không — code đã đủ điều kiện review. **CHƯA commit Task 18** (chỉ `git add`, người điều
phối commit sau khi review sạch theo Global Constraints); **CHƯA push, CHƯA merge**.
Bước tiếp theo: người điều phối review sạch → commit Task 18 → merge nhánh con vào `tpe` ở cả
2 repo → deploy theo 3 bước ở mục *Ghi chú deploy* trong `design.md` (đặc biệt: insert thủ công
3 quyền 1184–1186, KHÔNG chạy `PermissionsTableSeeder`).
Blocked: không có.

**Kết quả 5 lệnh tự kiểm (chi tiết đủ ở task-18-report.md):**
1. `vi-VN` ở FE (loại `new Date`) — RỖNG trong phạm vi feature (5 match ở `grep` là do lệnh gốc quét
   luôn thư mục `components/` toàn app; cả 5 file đều KHÔNG nằm trong diff của nhánh này).
2. `number_format($x, 0, ',', '.')` ở BE — RỖNG (2 file service không gọi `number_format` lần nào).
3. Cờ quyền `can*= true` hard-code ở FE — RỖNG.
4. `git diff --stat` 2 repo — toàn bộ 9 file (hrm-client) + 14 file (hrm-api) đều là **file mới**
   (dấu `+`), không CRLF nào bị phá.
5. Hiệu năng lúc mở màn — đúng **2 request** (`filter-options` 354ms + endpoint chính 152ms), cả
   hai đều < 2s.

**Ngoại lệ V2Base đã biết + 1 ngoại lệ mới phát hiện khi soát:** `DrillNum.vue` (`<button>`, đã chấp
nhận từ đầu) + `PrintOptionsModal.vue` (`<button>`/`<label>`/`<input>` radio) — file này **copy gần
như nguyên văn** từ `potential-customer-care/components/PrintOptionsModal.vue` đã chạy thật, lý do
markup thô đã ghi sẵn trong comment đầu file (bootstrap `.custom-control` lệch nửa dòng do thiếu
`.mate-field`; `V2BaseModal` chỉ có trên `gop_db`). Không phải vi phạm mới.

**Phần B — Lịch sử dự án TKT sau migration:** DB local **không tái hiện được** kịch bản dữ liệu cũ
(dự án sớm nhất 03/07/2026, sau mốc backfill 18/05/2026, migration vá 0 bản ghi — đúng như dự đoán).
Ngoài ra phát hiện **1 blocker môi trường KHÔNG liên quan đến feature này**: mọi trang chi tiết dự
án TKT (kể cả mục Lịch sử, `SystemLogService:285`) trả 500 vì bảng `prospective_project_extension_requests`
chưa tồn tại trên DB local (migration `2026_09_11_000003` — của tính năng "gia hạn thời gian triển
khai", Redmine #11153 — chưa chạy). Đã xác minh bằng tinker rằng phần log trạng thái (đối tượng
migration Task 1 xử lý) tự nó hoạt động đúng: dự án 4 log (id=1, thật) và fixture 2 log lập trước
18/05/2026 (id=151) đều đọc xuôi theo `changed_at` DESC, không trùng mốc, không lỗi. **Đề xuất kiểm
đầy đủ trên môi trường có migration `2026_09_11_000003` đã chạy**: mở
`/assign/prospective-projects/{id}` của 1 dự án Thất bại lập trước 18/05/2026, xem mục Lịch sử có
đúng 2 mốc (Tạo dự án + Đóng dự án) và đọc xuôi.

**Đối chiếu Vue thật vs mockup (Task 17, đã port sang `design.md`):** 6/8 điểm khớp tuyệt đối · 2 chỗ
lệch — thứ tự ô lọc (cặp Từ ngày/Đến ngày phải bám ngay sau Kỳ, không đứng sau Công ty/Tiêu chí) và
bề rộng ô Công ty (292px demo → 340px tên công ty thật) — **đã sửa và đo lại khớp**, không còn treo.

**Còn nợ (chi tiết ở `design.md` mục Còn treo + `STATUS.md`):** giá trị hợp đồng (`—` mọi dòng, chờ
hợp đồng HRM từ báo giá HRM) · dự án Thành công lập trước 18/05/2026 không suy được mốc đóng ·
`expected_contract_amount` khuyết 42% · `V2BaseTableScroll.vue` port trùng, merge vào `tpe` sẽ
conflict add/add với `gop_db`/`permiss_manager` (nội dung giống hệt, lấy bản nào cũng được) · SRS +
testcase chưa làm.

---

### Checkpoint — 2026-09-14 (sau review tổng toàn nhánh)

**Vừa hoàn thành:** vòng review tổng toàn nhánh (mô hình + 1 lượt sửa gộp), rồi 1 thay đổi theo yêu
cầu user. Tất cả đã commit, cây làm việc 2 repo sạch.

**Review tổng bắt được 1 lỗi Important mà CẢ 21 CA E2E ĐỀU KHÔNG THẤY** — đáng ghi nhớ nhất của feature:

`buildLevel()` nhánh `$withoutPart` truyền `$parentKey` TRẦN xuống cấp sau, không ghi dấu việc đã bỏ
qua cấp Bộ phận. `applyDrillKey()` chỉ lọc AND trên các chiều CÓ MẶT trong key ⇒ key `dept:5+emp:88`
khớp CẢ dự án có bộ phận lẫn không có bộ phận của nhân viên đó.
Hệ quả: bấm số `1` trên bảng, popup mở ra `3` dự án — 2 cái thừa đã được đếm ở node `part:9` bên trên
nên **bị liệt kê ở 2 popup khác nhau**. Excel + bản in chi tiết sai theo.

⚠️ **Vì sao không ca nào bắt được:** bảng theo dõi VẪN ĐÚNG — 2 đẳng thức bất biến và phép cha = tổng
con đều xanh. Lỗi nằm ở **đường từ bảng sang popup**, mà không ca nào so *"số vừa bấm = `total` của
popup"*. Toàn bộ hệ tự kiểm canh BẢNG, không canh CẦU NỐI.
→ Sửa: gắn `part:0` vào key. Bổ sung **ca 10** so số bấm vs `total` popup ở nhiều cấp × 2 tiêu chí —
ca này chặn cả LỚP lỗi, không chỉ ca cụ thể.
→ DB local có **0 cặp (phòng ban, nhân viên)** kích hoạt được lỗi nên ca 10 tự nó xanh cả trước lẫn
sau khi sửa; đã chứng minh giá trị thật bằng dữ liệu giả `E2E-TMP-*` (đo `bảng=1 / popup=3` khi chưa
sửa, xanh sau khi sửa), rồi xoá sạch.

**3 việc sửa kèm theo review tổng:** 4 nhãn cột popup về đúng mockup (`Tỉnh/TP` → `Thị trường`, còn
bất nhất ngay trong cùng popup vì ô lọc và chip đều gọi là Thị trường) · xoá import thừa · thêm
comment cho 2 `<button>` affordance.

**Thay đổi theo yêu cầu user (14/09):** ô Công ty vẫn BẮT BUỘC chọn, KHÔNG có mục "Tất cả công ty",
nhưng **mặc định đổi từ `companies[0]` sang CÔNG TY CỦA USER ĐĂNG NHẬP**. Trước đó user mở màn ra số
của pháp nhân khác công ty mình, và "Xoá lọc" cũng nhảy sang pháp nhân đó. BE trả `default_company_id`
(clamp qua `clampCompanyId()` có sẵn); ca biên công ty hồ sơ không nằm trong danh sách được phép thì
rơi về công ty đầu danh mục vì ô này bắt buộc, để rỗng là màn chết.
Đo: công ty user = 1, `companies[0]` = 2 (khác nhau nên phép đo có nghĩa) → mở màn ra 1, Xoá lọc về 1.

**Trạng thái cuối:** e2e **22 ca xanh** · `hrm-api` **11 commit** · `hrm-client` **10 commit** ·
nhánh `tpe-bao-cao-ket-qua-du-an-tkt` tách từ đỉnh `tpe` ở cả 2 repo · **chưa push, chưa merge**.

**Đã merge (14/09/2026):** user merge nhánh feature vào `tpe` ở cả 2 repo, **không conflict** —
`hrm-api` `769061693` (merge `tpe-develop-assign` vào trước bằng `8ca563f93`), `hrm-client` `12b6f4f6e`.

**Bước tiếp theo:** `tpe` đang đi trước `origin/tpe` **86 commit** (hrm-api) / **80 commit**
(hrm-client) — **chưa push**. Trước khi push nên chạy lại bộ e2e trên `tpe` sau merge, vì `hrm-api`
có gộp thêm `tpe-develop-assign` (nhánh khác) nên tổ hợp code sau merge chưa từng được kiểm.

**Blocked:** không có.
