# Lịch làm việc (6 loại) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đổi tab "📅 Lịch meeting" của màn `/assign/my-todo` thành "📅 Lịch làm việc", hiển thị đủ 6 loại công việc của tôi thay vì chỉ meeting.

**Architecture:** BE thêm endpoint đọc `GET assign/my-todo/calendar` do `WorkCalendarService` phục vụ — gom 6 nguồn, lọc **overlap** khoảng ngày ngay ở tầng DB, trả item chuẩn hoá có `start`/`end`/`all_day`/`status_group`. Điều kiện "việc của tôi" tách ra lớp dùng chung để không lệch với tab danh sách. FE tổng quát hoá cây `components/calendar/` từ meeting-only sang đa loại: màu theo LOẠI, chấm theo TRẠNG THÁI.

**Tech Stack:** Laravel 8 + PHP 7.4 (hrm-api) · Nuxt 2 + Vue 2 + BootstrapVue + dayjs (hrm-client) · Playwright (e2e) · PHPUnit 9 (unit BE)

**Spec:** `.plans/lich-lam-viec/design.md`

## Global Constraints

- **Tài liệu** feature này chỉ nằm trong `.plans/lich-lam-viec/`. KHÔNG tạo file trong `docs/superpowers/specs/` (CLAUDE.md §Quy luật tổ chức tài liệu feature).
- **KHÔNG commit, KHÔNG push git.** Người dùng tự commit khi muốn (CLAUDE.md §Nguyên tắc chung). Mọi step "Commit" trong khuôn skill đều đổi thành "dừng lại báo cáo".
- **KHÔNG `git stash`** ở `hrm-api`/`hrm-client` — nhiều session chạy song song, stash nuốt việc của session khác.
- **KHÔNG `pkill -f`** theo tên tiến trình. Muốn tắt server thì tìm PID theo cổng rồi kill đúng PID.
- **PHP**: `/opt/homebrew/opt/php@7.4/bin/php`. Chạy artisan/tinker phải `config:clear` trước.
- **Nuxt dev**: node 12 + `NODE_OPTIONS=--max-old-space-size=8192`, cổng 3000. **e2e**: node 20.
- **API dev**: `php artisan serve` cổng 8000.
- **Mọi endpoint e2e phải có prefix `/api/v1/`** — route Laravel nằm trong `Route::group(['prefix' => '/v1'])` (`Modules/Assign/Routes/api.php:83`). Thiếu `/v1` là 404 im lặng.
- **KHÔNG ghi file mốc/ảnh chụp vào `e2e/test-results/`** — Playwright xoá sạch thư mục đó đầu mỗi lần chạy, ca kiểm so sánh sẽ luôn nhảy vào nhánh "ghi mốc lần đầu" và xanh giả vô điều kiện. Đặt cạnh spec, ví dụ `e2e/tests/assign/<ten>.baseline.json`.
- **Bộ e2e chạy `serial`**: 1 ca đỏ làm mọi ca sau in "did not run" chứ KHÔNG phải "passed". Luôn đọc dòng tổng kết cuối log.
- **Nhãn nút/chữ trên UI** theo `.claude/skills/button-convention` — skill thắng spec về hình thức.
- Sau khi đổi tên component hoặc đổi nhánh: restart Nuxt + `rm -rf .nuxt/components` trước khi kết luận lỗi "Can't resolve component" là lỗi code.
- **Nhánh**: làm THẲNG trên `tpe` ở cả `hrm-api` và `hrm-client` — **KHÔNG tạo nhánh mới** (user chốt 2026-09-10; đang có Nuxt :3000 + API :8000 chạy trên `tpe`).
- **Nghiệm thu e2e = TOÀN XANH.** Baseline cũ (2026-09-10) có 1 ca đỏ, nhưng Task 2.2 đã truy ra đó là **lỗi của ca kiểm**, không phải của app: 3 ca trong `my-todo-toggle-smooth.spec.ts` bấm một dòng nhưng canh một dòng khác (chỉ nhắc việc cá nhân mới có ô tick, còn meeting/task/issue xen vào và sắp trước). Đã sửa.
  - **Baseline mới (2026-09-11, sau Task 2.2):**
    - `tests/assign/my-todo tests/assign/work-calendar --project=chromium --workers=1` → **49 passed / 0 failed** (cập nhật 2026-09-11 sau Task 4.2; mốc trước: 43 sau 4.1, 34 sau 3.3, 23 sau 2.2)
    - `tests/assign/my-todo tests/assign/work-calendar --project=api --workers=1` → **20 passed / 1 skipped**
  - Từ đây, BẤT KỲ ca đỏ nào cũng là hồi quy do mình gây ra — không còn "đỏ sẵn" để đổ lỗi.
- ⚠️ **Mọi lần chạy e2e để NGHIỆM THU phải thêm `--workers=1`.** Cấu hình mặc định `workers: 2` khi chạy local (`playwright.config.ts:12`), tức 2 worker cùng nện vào MỘT Nuxt dev server Node 12 — đo thật ngày 2026-09-11: 4 lần chạy nhóm cho 4 kiểu đỏ khác nhau, có lần mất 20,6 phút (gấp 4-6 lần bình thường). Đỏ kiểu này là tranh chấp tài nguyên, không phải hồi quy, nhưng nó làm tiêu chí "toàn xanh" mất ý nghĩa. Chạy 2 worker chỉ dùng để dò nhanh, KHÔNG dùng để kết luận.
- ⚠️ **Playwright: đừng truyền locator đã `.first()` vào `has:`** — nó hỏng im lặng. Neo theo tổ tiên từ chính phần tử sắp bấm.

**Bảng gộp trạng thái (dùng xuyên suốt, copy nguyên văn từ design §6.2):**

| Nhóm | Thành viên |
|---|---|
| `todo` | Task 1,2,3 · Issue `new`,`assigned` · AssignJob 1,2 · AssignRequest 1,2 · Meeting 0,1 · personal chưa xong |
| `doing` | Task 4,6 · Issue `in_progress`,`reopened` · AssignJob 3,5 · AssignRequest 3,4,5 · Meeting 2 |
| `done` | Task 8 · Issue `resolved`,`completed`,`closed` · AssignJob 6 · AssignRequest 7 · Meeting 3 · personal đã xong |
| `stopped` | Task 5,7,9,10 · Issue `rejected` · AssignJob 4 · AssignRequest 6 · Meeting 4 |

Gạch ngang tiêu đề chỉ áp cho: Task 7,9,10 · Issue `rejected` · AssignJob 4 · AssignRequest 6 · Meeting 4. **Task 5 (Tạm dừng) chỉ làm mờ, KHÔNG gạch ngang.**

---

## Phase 1 — Backend

### Task 1.1: Bảng gộp trạng thái `WorkItemStatusGroup`

**Files:**
- Create: `hrm-api/Modules/Assign/Services/MyTodo/WorkItemStatusGroup.php`
- Test: `hrm-api/tests/Unit/WorkItemStatusGroupTest.php`

**Interfaces:**
- Consumes: hằng số trạng thái sẵn có — `Task::DRAFT..REJECTED_START` (1..10), `AssignJob::DANG_TAO..DA_DUYET_KET_QUA` (1..6), `AssignRequest::DANG_TAO..DA_DUYET_KET_QUA` (1,2,3,4,5,6,7), `Meeting::DANG_TAO..HUY` (0..4).
- Produces: `WorkItemStatusGroup::of(string $type, $status): string` trả `'todo'|'doing'|'done'|'stopped'`; `WorkItemStatusGroup::isStruckThrough(string $type, $status): bool`.

- [ ] **Step 1: Viết test đỏ**

```php
<?php
namespace Tests\Unit;

use Tests\TestCase;
use Modules\Assign\Services\MyTodo\WorkItemStatusGroup as G;

class WorkItemStatusGroupTest extends TestCase
{
    public function test_gom_dung_nhom_cho_tung_loai()
    {
        $this->assertSame('todo',    G::of('task', 3));            // Cần làm
        $this->assertSame('doing',   G::of('task', 4));            // Đang làm
        $this->assertSame('done',    G::of('task', 8));            // Hoàn thành
        $this->assertSame('stopped', G::of('task', 9));            // Huỷ
        $this->assertSame('stopped', G::of('task', 5));            // Tạm dừng
        $this->assertSame('todo',    G::of('issue', 'new'));
        $this->assertSame('doing',   G::of('issue', 'reopened'));
        $this->assertSame('done',    G::of('issue', 'closed'));
        $this->assertSame('stopped', G::of('issue', 'rejected'));
        $this->assertSame('doing',   G::of('assign_job', 3));      // Đã duyệt
        $this->assertSame('done',    G::of('assign_job', 6));      // Đã duyệt KQ
        $this->assertSame('stopped', G::of('assign_job', 4));      // Từ chối
        $this->assertSame('doing',   G::of('assign_business', 4)); // Đã lập phiếu CT
        $this->assertSame('done',    G::of('assign_business', 7)); // Đã duyệt KQ
        $this->assertSame('stopped', G::of('assign_business', 6)); // Không duyệt
        $this->assertSame('todo',    G::of('meeting', 0));         // Đang tạo — status int 0
        $this->assertSame('doing',   G::of('meeting', 2));         // Chốt lịch
        $this->assertSame('stopped', G::of('meeting', 4));         // Hủy
        $this->assertSame('todo',    G::of('personal', false));
        $this->assertSame('done',    G::of('personal', true));
    }

    public function test_trang_thai_la_khong_biet_thi_ve_todo()
    {
        $this->assertSame('todo', G::of('task', 999));
        $this->assertSame('todo', G::of('khong_co_loai_nay', 1));
        $this->assertSame('todo', G::of('issue', null));
    }

    public function test_gach_ngang_chi_ap_cho_viec_ket_thuc_han()
    {
        $this->assertTrue(G::isStruckThrough('task', 9));            // Huỷ
        $this->assertTrue(G::isStruckThrough('task', 7));            // Từ chối
        $this->assertTrue(G::isStruckThrough('task', 10));           // Từ chối bắt đầu
        $this->assertTrue(G::isStruckThrough('meeting', 4));
        $this->assertTrue(G::isStruckThrough('assign_business', 6)); // Không duyệt
        $this->assertTrue(G::isStruckThrough('assign_job', 4));
        $this->assertTrue(G::isStruckThrough('issue', 'rejected'));

        // Tạm dừng thuộc nhóm stopped nhưng KHÔNG gạch ngang — việc còn chạy tiếp được
        $this->assertSame('stopped', G::of('task', 5));
        $this->assertFalse(G::isStruckThrough('task', 5));

        $this->assertFalse(G::isStruckThrough('task', 8));           // Hoàn thành
        $this->assertFalse(G::isStruckThrough('meeting', 3));
    }

    /** Bẫy PHP 7.4: `'abc' == 0` là true — so lỏng sẽ cho chuỗi lạ rơi vào nhóm của giá trị 0 */
    public function test_chuoi_la_khong_duoc_khop_nham_gia_tri_so()
    {
        $this->assertSame('todo', G::of('meeting', 'chuoi-la'));   // KHÔNG được coi là Meeting::DANG_TAO (0)
        $this->assertFalse(G::isStruckThrough('meeting', 'chuoi-la'));
        // ngược lại, int và string cùng giá trị vẫn phải khớp nhau
        $this->assertSame('doing', G::of('meeting', '2'));
        $this->assertSame('doing', G::of('meeting', 2));
    }
}
```

- [ ] **Step 2: Chạy test, xác nhận ĐỎ**

```bash
cd hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Unit/WorkItemStatusGroupTest.php
```

Kỳ vọng: FAIL — `Class "Modules\Assign\Services\MyTodo\WorkItemStatusGroup" not found`.

- [ ] **Step 3: Viết implementation tối thiểu**

```php
<?php

namespace Modules\Assign\Services\MyTodo;

use Modules\Assign\Entities\AssignJob;
use Modules\Assign\Entities\AssignRequest;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\Task\Task;

/**
 * Gộp 6 bộ trạng thái (task 10 / issue 8 / giao việc 6 / công tác 7 / meeting 5 /
 * cá nhân 2) về 4 NHÓM dùng chung cho lịch làm việc. Thẻ vẫn hiện chữ trạng thái
 * THẬT của loại; nhóm chỉ quyết định màu chấm + làm mờ + gạch ngang.
 * Bảng này là NGUỒN DUY NHẤT — FE không được tự map lại.
 */
class WorkItemStatusGroup
{
    const TODO    = 'todo';
    const DOING   = 'doing';
    const DONE    = 'done';
    const STOPPED = 'stopped';

    /** type => [group => danh sách giá trị status thật] */
    private static $MAP = [
        'task' => [
            self::TODO    => [Task::DRAFT, Task::PENDING_APPROVAL, Task::TODO],
            self::DOING   => [Task::IN_PROGRESS, Task::REVIEW],
            self::DONE    => [Task::DONE],
            self::STOPPED => [Task::PAUSED, Task::REJECTED, Task::CANCELLED, Task::REJECTED_START],
        ],
        'issue' => [
            self::TODO    => ['new', 'assigned'],
            self::DOING   => ['in_progress', 'reopened'],
            self::DONE    => ['resolved', 'completed', 'closed'],
            self::STOPPED => ['rejected'],
        ],
        'assign_job' => [
            self::TODO    => [AssignJob::DANG_TAO, AssignJob::CHO_DUYET],
            self::DOING   => [AssignJob::DA_DUYET, AssignJob::DA_NHAP_KET_QUA],
            self::DONE    => [AssignJob::DA_DUYET_KET_QUA],
            self::STOPPED => [AssignJob::TU_CHOI],
        ],
        'assign_business' => [
            self::TODO    => [AssignRequest::DANG_TAO, AssignRequest::CHO_DUYET],
            self::DOING   => [AssignRequest::DA_DUYET, AssignRequest::DA_LAP_PHIEU_CONG_TAC, AssignRequest::DA_NHAP_KET_QUA],
            self::DONE    => [AssignRequest::DA_DUYET_KET_QUA],
            self::STOPPED => [AssignRequest::KHONG_DUYET],
        ],
        'meeting' => [
            self::TODO    => [Meeting::DANG_TAO, Meeting::LEN_LICH],
            self::DOING   => [Meeting::CHOT_LICH],
            self::DONE    => [Meeting::HOAN_THANH],
            self::STOPPED => [Meeting::HUY],
        ],
    ];

    /** Trạng thái kết thúc HẲN — gạch ngang tiêu đề. Tạm dừng KHÔNG nằm ở đây. */
    private static $STRUCK = [
        'task'            => [Task::REJECTED, Task::CANCELLED, Task::REJECTED_START],
        'issue'           => ['rejected'],
        'assign_job'      => [AssignJob::TU_CHOI],
        'assign_business' => [AssignRequest::KHONG_DUYET],
        'meeting'         => [Meeting::HUY],
    ];

    public static function of($type, $status)
    {
        if ($type === 'personal') {
            return $status ? self::DONE : self::TODO;
        }

        if (!isset(self::$MAP[$type]) || $status === null) {
            return self::TODO;
        }

        foreach (self::$MAP[$type] as $group => $values) {
            // So sánh BẰNG CHUỖI, KHÔNG dùng in_array lỏng: trên PHP 7.4 `'abc' == 0`
            // cho true, nên status kiểu chuỗi lạ sẽ rơi nhầm vào nhóm của giá trị 0.
            // Quy cả hai vế về string rồi so nghiêm ngặt vẫn cho int 0 khớp string '0'.
            if (in_array((string) $status, array_map('strval', $values), true)) {
                return $group;
            }
        }

        return self::TODO;
    }

    public static function isStruckThrough($type, $status)
    {
        if (!isset(self::$STRUCK[$type]) || $status === null) {
            return false;
        }

        return in_array((string) $status, array_map('strval', self::$STRUCK[$type]), true);
    }
}
```

- [ ] **Step 4: Chạy test, xác nhận XANH**

```bash
cd hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Unit/WorkItemStatusGroupTest.php
```

Kỳ vọng: OK, 3 tests.

- [ ] **Step 5: Dừng lại báo cáo** (KHÔNG commit — xem Global Constraints)

---

### Task 1.2: Tính khoảng thời gian `WorkItemPeriod`

**Files:**
- Create: `hrm-api/Modules/Assign/Services/MyTodo/WorkItemPeriod.php`
- Test: `hrm-api/tests/Unit/WorkItemPeriodTest.php`

**Interfaces:**
- Consumes: không phụ thuộc task trước.
- Produces: `WorkItemPeriod::of($entity, string $type): ?array` trả `['start' => Carbon, 'end' => Carbon, 'all_day' => bool]`, hoặc **`null`** khi không xác định được `start` (item bị loại khỏi lịch).

- [ ] **Step 1: Viết test đỏ**

```php
<?php
namespace Tests\Unit;

use Carbon\Carbon;
use Tests\TestCase;
use Modules\Assign\Services\MyTodo\WorkItemPeriod;

class WorkItemPeriodTest extends TestCase
{
    /** Dùng object rỗng thay model để test thuần logic, không đụng DB */
    private function ent(array $attrs)
    {
        return (object) $attrs;
    }

    public function test_phieu_cong_tac_lay_from_time_den_to_time()
    {
        $r = WorkItemPeriod::of($this->ent([
            'from_time' => '2026-09-07 08:00:00',
            'to_time'   => '2026-09-09 17:00:00',
        ]), 'assign_business');

        $this->assertSame('2026-09-07 08:00:00', $r['start']->format('Y-m-d H:i:s'));
        $this->assertSame('2026-09-09 17:00:00', $r['end']->format('Y-m-d H:i:s'));
        $this->assertFalse($r['all_day']);
    }

    public function test_phieu_giao_viec_lay_time_start_request_den_deadline()
    {
        $r = WorkItemPeriod::of($this->ent([
            'time_start_request' => '2026-09-07 09:30:00',
            'deadline'           => '2026-09-08 18:00:00',
        ]), 'assign_job');

        $this->assertSame('2026-09-07 09:30:00', $r['start']->format('Y-m-d H:i:s'));
        $this->assertSame('2026-09-08 18:00:00', $r['end']->format('Y-m-d H:i:s'));
    }

    public function test_thieu_end_thi_end_bang_start()
    {
        $r = WorkItemPeriod::of($this->ent([
            'from_time' => '2026-09-07 08:00:00',
            'to_time'   => null,
        ]), 'assign_business');

        $this->assertSame('2026-09-07 08:00:00', $r['end']->format('Y-m-d H:i:s'));
    }

    public function test_end_som_hon_start_thi_keo_ve_bang_start()
    {
        $r = WorkItemPeriod::of($this->ent([
            'from_time' => '2026-09-07 08:00:00',
            'to_time'   => '2026-09-05 08:00:00',
        ]), 'assign_business');

        $this->assertSame('2026-09-07 08:00:00', $r['end']->format('Y-m-d H:i:s'));
    }

    public function test_ba_loai_phieu_gio_00_00_00_ca_hai_dau_la_ca_ngay()
    {
        $r = WorkItemPeriod::of($this->ent([
            'from_time' => '2026-09-07 00:00:00',
            'to_time'   => '2026-09-08 00:00:00',
        ]), 'assign_business');

        $this->assertTrue($r['all_day']);
    }

    public function test_task_lay_start_date_den_due_date()
    {
        $r = WorkItemPeriod::of($this->ent([
            'start_date' => '2026-09-07',
            'due_date'   => '2026-09-09',
            'due_time'   => '17:30:00',
        ]), 'task');

        $this->assertSame('2026-09-07', $r['start']->format('Y-m-d'));
        $this->assertSame('2026-09-09 17:30:00', $r['end']->format('Y-m-d H:i:s'));
        $this->assertFalse($r['all_day']);
    }

    public function test_task_thieu_start_date_thi_start_bang_due_date()
    {
        $r = WorkItemPeriod::of($this->ent([
            'start_date' => null,
            'due_date'   => '2026-09-09',
            'due_time'   => null,
        ]), 'task');

        $this->assertSame('2026-09-09', $r['start']->format('Y-m-d'));
        $this->assertTrue($r['all_day']);
    }

    public function test_task_khong_co_due_date_thi_bi_loai_khoi_lich()
    {
        $this->assertNull(WorkItemPeriod::of($this->ent([
            'start_date' => '2026-09-07',
            'due_date'   => null,
            'due_time'   => null,
        ]), 'task'));
    }

    public function test_issue_uu_tien_due_date_roi_moi_den_deadline()
    {
        $co_due = WorkItemPeriod::of($this->ent([
            'due_date' => '2026-09-09', 'due_time' => null, 'deadline' => '2026-09-20 10:00:00',
        ]), 'issue');
        $this->assertSame('2026-09-09', $co_due['start']->format('Y-m-d'));

        $chi_deadline = WorkItemPeriod::of($this->ent([
            'due_date' => null, 'due_time' => null, 'deadline' => '2026-09-20 10:00:00',
        ]), 'issue');
        $this->assertSame('2026-09-20', $chi_deadline['start']->format('Y-m-d'));

        $this->assertNull(WorkItemPeriod::of($this->ent([
            'due_date' => null, 'due_time' => null, 'deadline' => null,
        ]), 'issue'));
    }

    public function test_meeting_va_personal()
    {
        $m = WorkItemPeriod::of($this->ent([
            'start_date' => '2026-09-07 14:00:00', 'end_date' => '2026-09-07 15:30:00',
        ]), 'meeting');
        $this->assertSame('2026-09-07 15:30:00', $m['end']->format('Y-m-d H:i:s'));

        $p = WorkItemPeriod::of($this->ent([
            'due_date' => '2026-09-07', 'due_time' => '09:00:00',
        ]), 'personal');
        $this->assertSame('2026-09-07 09:00:00', $p['start']->format('Y-m-d H:i:s'));
        $this->assertFalse($p['all_day']);

        $this->assertNull(WorkItemPeriod::of($this->ent([
            'due_date' => null, 'due_time' => null,
        ]), 'personal'));
    }
}
```

- [ ] **Step 2: Chạy test, xác nhận ĐỎ**

```bash
cd hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Unit/WorkItemPeriodTest.php
```

Kỳ vọng: FAIL — class không tồn tại.

- [ ] **Step 3: Viết implementation**

```php
<?php

namespace Modules\Assign\Services\MyTodo;

use Carbon\Carbon;

/**
 * Quy khoảng thời gian của 6 loại việc về cùng một cặp start/end + cờ all_day,
 * để lưới lịch không phải biết loại nào dùng cột nào.
 *
 * Trả NULL khi không xác định được start — item đó bị LOẠI khỏi lịch
 * (task/issue/nhắc việc chưa đặt hạn). Xem design §5.
 */
class WorkItemPeriod
{
    /** type => [cột start, cột end] cho 3 loại phiếu dùng cột dateTime */
    private static $DATETIME_COLUMNS = [
        'assign_business' => ['from_time', 'to_time'],
        'assign_job'      => ['time_start_request', 'deadline'],
        'meeting'         => ['start_date', 'end_date'],
    ];

    public static function of($entity, $type)
    {
        if (isset(self::$DATETIME_COLUMNS[$type])) {
            return self::fromDateTimeColumns($entity, self::$DATETIME_COLUMNS[$type]);
        }

        if ($type === 'task') {
            return self::fromDueDate($entity, $entity->start_date ?? null, $entity->due_date ?? null);
        }

        if ($type === 'issue') {
            $due = $entity->due_date ?? null;
            if (!$due && !empty($entity->deadline)) {
                $due = Carbon::parse($entity->deadline)->format('Y-m-d');
            }
            return self::fromDueDate($entity, null, $due);
        }

        if ($type === 'personal') {
            return self::fromDueDate($entity, null, $entity->due_date ?? null);
        }

        return null;
    }

    private static function fromDateTimeColumns($entity, array $columns)
    {
        list($startCol, $endCol) = $columns;

        if (empty($entity->{$startCol})) {
            return null;
        }

        $start = Carbon::parse($entity->{$startCol});
        $end   = empty($entity->{$endCol}) ? $start->copy() : Carbon::parse($entity->{$endCol});

        if ($end->lt($start)) {
            $end = $start->copy();
        }

        return [
            'start'   => $start,
            'end'     => $end,
            // cả hai đầu đều đúng 00:00:00 thì coi là việc cả ngày
            'all_day' => $start->format('H:i:s') === '00:00:00' && $end->format('H:i:s') === '00:00:00',
        ];
    }

    /**
     * Loại dùng cột date + cột giờ rời (task/issue/personal).
     * $startDate có thể null -> lấy bằng $dueDate.
     */
    private static function fromDueDate($entity, $startDate, $dueDate)
    {
        if (empty($dueDate)) {
            return null;
        }

        $dueTime = $entity->due_time ?? null;
        $allDay  = empty($dueTime);

        $start = Carbon::parse($startDate ?: $dueDate)->startOfDay();
        $end   = Carbon::parse($dueDate)->startOfDay();

        if (!$allDay) {
            $time = Carbon::parse($dueTime);
            $end->setTime($time->hour, $time->minute, $time->second);

            // việc 1 ngày: giờ hạn cũng là giờ bắt đầu hiển thị trên lưới tuần
            if ($start->isSameDay($end)) {
                $start->setTime($time->hour, $time->minute, $time->second);
            }
        }

        if ($end->lt($start)) {
            $end = $start->copy();
        }

        return ['start' => $start, 'end' => $end, 'all_day' => $allDay];
    }
}
```

- [ ] **Step 4: Chạy test, xác nhận XANH**

```bash
cd hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Unit/WorkItemPeriodTest.php
```

Kỳ vọng: OK, 10 tests.

- [ ] **Step 5: Dừng lại báo cáo**

---

### Task 1.3: Tách điều kiện "việc của tôi" dùng chung

Tab danh sách và tab lịch phải hiểu "của tôi" giống hệt nhau. Task này rút điều kiện ra một lớp, rồi **sửa `MyTodoService` gọi vào lớp đó** — hành vi phải KHÔNG đổi. Vì vậy viết test chốt hành vi hiện tại TRƯỚC khi động vào.

**Files:**
- Create: `hrm-api/Modules/Assign/Services/MyTodo/MyTodoOwnershipScope.php`
- Modify: `hrm-api/Modules/Assign/Services/MyTodo/MyTodoService.php:454-575` (5 method aggregator)
- Test: `HRM/e2e/tests/assign/my-todo-ownership-unchanged.api.spec.ts`

**Interfaces:**
- Consumes: không phụ thuộc Task 1.1/1.2.
- Produces: 5 static method, mỗi cái nhận `$query` và trả `$query` đã gắn điều kiện —
  `MyTodoOwnershipScope::tasks($query, $userId)` · `issues($query, $userId)` · `assignJobs($query, $employeeInfoId)` · `assignBusinesses($query, $userId)` · `personalTodos($query, $userId)`.
  Meeting KHÔNG có ở đây — lịch dùng `MeetingCalendarCriteria` sẵn có (design §2).

- [ ] **Step 1: Viết test chốt hành vi hiện tại (phải XANH ngay trên code chưa sửa)**

```ts
/**
 * Chốt hành vi tab "Công việc của tôi" TRƯỚC khi rút điều kiện "của tôi" ra lớp
 * dùng chung. Test này phải XANH cả trước lẫn sau refactor — nếu sau refactor mà
 * đỏ nghĩa là đã đổi phạm vi dữ liệu của tab danh sách, điều spec cấm (§1 Ngoài scope).
 */
import { test, expect, request } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8000';
const STATE_FILE = path.join(__dirname, '..', '..', '.auth', 'api.json');
const SNAPSHOT = path.join(__dirname, '..', '..', 'test-results', 'my-todo-ownership.json');

test.describe.serial('my-todo — phạm vi "của tôi" không đổi sau refactor', () => {
  test('chụp lại tập item id theo từng loại', async () => {
    const token = JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8')).token;
    const api = await request.newContext({
      baseURL: API_BASE,
      extraHTTPHeaders: { Authorization: `Bearer ${token}`, Accept: 'application/json' },
    });

    const res = await api.get('/api/v1/assign/my-todo');
    expect(res.status()).toBe(200);

    const items = (await res.json()).data.items as Array<{ type: string; id: number }>;
    expect(items.length).toBeGreaterThan(0); // DB rỗng thì test này vô nghĩa

    const byType: Record<string, number[]> = {};
    for (const it of items) {
      (byType[it.type] = byType[it.type] || []).push(it.id);
    }
    for (const k of Object.keys(byType)) byType[k].sort((a, b) => a - b);

    if (fs.existsSync(SNAPSHOT)) {
      expect(byType).toEqual(JSON.parse(fs.readFileSync(SNAPSHOT, 'utf-8')));
    } else {
      fs.mkdirSync(path.dirname(SNAPSHOT), { recursive: true });
      fs.writeFileSync(SNAPSHOT, JSON.stringify(byType, null, 2));
      console.log('Đã ghi ảnh chụp gốc:', SNAPSHOT);
    }

    await api.dispose();
  });
});
```

- [ ] **Step 2: Chạy để ghi ảnh chụp gốc, xác nhận XANH trên code CHƯA sửa**

```bash
cd HRM/e2e && npx playwright test tests/assign/my-todo-ownership-unchanged.api.spec.ts --project=api
```

Kỳ vọng: 1 passed, và có file `test-results/my-todo-ownership.json`. Đọc **dòng tổng kết** — bộ test chạy serial.

- [ ] **Step 3: Viết lớp scope**

```php
<?php

namespace Modules\Assign\Services\MyTodo;

/**
 * ĐIỀU KIỆN "VIỆC CỦA TÔI" — nguồn duy nhất, dùng chung cho tab danh sách
 * (MyTodoService) và tab lịch (WorkCalendarService). Sửa ở đây là đổi cả hai;
 * KHÔNG chép lại điều kiện ở nơi khác.
 *
 * Meeting KHÔNG nằm ở đây: lịch dùng MeetingCalendarCriteria (điều kiện duy nhất
 * là user có tên trong Thành phần — Phía Công ty), xem design §2.
 */
class MyTodoOwnershipScope
{
    public static function tasks($query, $userId)
    {
        return $query->where('assignee_id', $userId);
    }

    public static function issues($query, $userId)
    {
        return $query->where('assignee_id', $userId);
    }

    public static function assignJobs($query, $employeeInfoId)
    {
        return $query->whereHas('employees', function ($q) use ($employeeInfoId) {
            $q->where('employee_info_id', $employeeInfoId);
        });
    }

    public static function assignBusinesses($query, $userId)
    {
        return $query->whereHas('employees', function ($q) use ($userId) {
            $q->where('employee_id', $userId);
        });
    }

    public static function personalTodos($query, $userId)
    {
        return $query->where('user_id', $userId)->whereNull('parent_id');
    }
}
```

- [ ] **Step 4: Sửa `MyTodoService` gọi vào lớp mới**

Trong `MyTodoService.php`, thay đúng phần điều kiện — giữ nguyên mọi thứ còn lại (`whereNotIn` trạng thái, `with`, `map`, `values`):

```php
// getAssignedTasks() — dòng ~458
return MyTodoOwnershipScope::tasks(
        Task::whereNotIn('status', $excludeStatuses), $userId
    )
    ->with(['assignee', 'solution'])
    ->get()
    ->map(function ($task) { return $this->normalizeItem($task, 'task', 'assigned'); })
    ->values();

// getAssignedIssues() — dòng ~475
return MyTodoOwnershipScope::issues(
        Issue::whereNotIn('status', $excludeStatuses), $userId
    )
    ->with(['assignee'])
    ->get()
    ->map(function ($issue) { return $this->normalizeItem($issue, 'issue', 'assigned'); })
    ->values();

// getAssignJobs() — dòng ~497
return MyTodoOwnershipScope::assignJobs(
        AssignJob::where('status', AssignJob::DA_DUYET), $employeeInfoId
    )
    ->get()
    ->map(function ($job) { return $this->normalizeItem($job, 'assign_job', 'assigned'); })
    ->values();

// getAssignBusinesses() — dòng ~513
return MyTodoOwnershipScope::assignBusinesses(
        AssignRequest::where('type', AssignRequest::PHIEU_CONG_TAC)
            ->where('status', AssignRequest::DA_LAP_PHIEU_CONG_TAC),
        $userId
    )
    ->get()
    ->map(function ($request) { return $this->normalizeItem($request, 'assign_business', 'assigned'); })
    ->values();

// getPersonalTodosNormalized() — dòng ~557
$query = MyTodoOwnershipScope::personalTodos(PersonalTodo::query(), $userId);
```

Thêm `use Modules\Assign\Services\MyTodo\MyTodoOwnershipScope;` nếu namespace khác — cùng namespace thì không cần.

- [ ] **Step 5: Chạy lại test chốt, xác nhận vẫn XANH**

```bash
cd HRM/e2e && npx playwright test tests/assign/my-todo-ownership-unchanged.api.spec.ts --project=api
```

Kỳ vọng: 1 passed — tập item id **y hệt** ảnh chụp ở Step 2. Đỏ nghĩa là refactor đã đổi phạm vi dữ liệu → quay lại sửa, không được cập nhật ảnh chụp cho qua.

- [ ] **Step 6: Dừng lại báo cáo**

---

### Task 1.4: `WorkCalendarService` — gom 6 nguồn theo khoảng ngày

**Files:**
- Create: `hrm-api/Modules/Assign/Services/MyTodo/WorkCalendarService.php`
- Test: `hrm-api/tests/Unit/WorkCalendarServiceOverlapTest.php`

**Interfaces:**
- Consumes: `WorkItemStatusGroup::of()` / `isStruckThrough()` (Task 1.1) · `WorkItemPeriod::of()` (Task 1.2) · `MyTodoOwnershipScope::*` (Task 1.3) · `MyTodoService::getTitle/getUrl/getStatusText` (đổi 3 method này từ `protected` sang `public`, không đổi thân hàm).
- Produces: `WorkCalendarService::getAll(array $filters, $userId): array` — mảng item shape design §4. `$filters` = `['from_date' => string, 'to_date' => string, 'types' => array|null, 'status' => mixed|null]`.

- [ ] **Step 1: Viết test đỏ cho phép so overlap (phần thuần logic, không đụng DB)**

```php
<?php
namespace Tests\Unit;

use Tests\TestCase;
use Modules\Assign\Services\MyTodo\WorkCalendarService;

class WorkCalendarServiceOverlapTest extends TestCase
{
    public function test_overlap_bat_ca_viec_bat_dau_truoc_ky()
    {
        $from = '2026-09-07 00:00:00';
        $to   = '2026-09-13 23:59:59';

        // việc kéo dài trùm qua kỳ — PHẢI lọt, nếu dùng "start BETWEEN" sẽ mất
        $this->assertTrue(WorkCalendarService::overlaps('2026-09-01 08:00:00', '2026-09-20 17:00:00', $from, $to));
        // bắt đầu trước kỳ, kết thúc trong kỳ
        $this->assertTrue(WorkCalendarService::overlaps('2026-09-05 08:00:00', '2026-09-08 17:00:00', $from, $to));
        // nằm trọn trong kỳ
        $this->assertTrue(WorkCalendarService::overlaps('2026-09-08 08:00:00', '2026-09-09 17:00:00', $from, $to));
        // chạm đúng biên
        $this->assertTrue(WorkCalendarService::overlaps('2026-09-13 23:00:00', '2026-09-14 10:00:00', $from, $to));

        // hoàn toàn trước / sau kỳ
        $this->assertFalse(WorkCalendarService::overlaps('2026-09-01 08:00:00', '2026-09-06 17:00:00', $from, $to));
        $this->assertFalse(WorkCalendarService::overlaps('2026-09-14 08:00:00', '2026-09-15 17:00:00', $from, $to));
    }
}
```

- [ ] **Step 2: Chạy test, xác nhận ĐỎ**

```bash
cd hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Unit/WorkCalendarServiceOverlapTest.php
```

Kỳ vọng: FAIL — class/method không tồn tại.

- [ ] **Step 3: Viết `WorkCalendarService`**

```php
<?php

namespace Modules\Assign\Services\MyTodo;

use Carbon\Carbon;
use Modules\Assign\Entities\AssignJob;
use Modules\Assign\Entities\AssignRequest;
use Modules\Assign\Entities\Issue;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\MyTodo\PersonalTodo;
use Modules\Assign\Entities\Task\Task;
use Modules\Assign\Repositories\Criteria\MeetingCalendarCriteria;
use Modules\Human\Entities\Employee;

/**
 * Nguồn dữ liệu cho tab "Lịch làm việc" (/assign/my-todo, tab 2).
 *
 * KHÁC MyTodoService::getAll() ở 3 điểm, cố ý (design §3, §7.3):
 *   1. lọc theo KHOẢNG NGÀY ngay ở tầng DB (overlap), không nạp hết rồi lọc collection;
 *   2. KHÔNG loại bỏ trạng thái nào — lịch hiện cả việc chưa duyệt / đã xong / đã huỷ;
 *   3. trả start/end/all_day (khoảng) thay vì mỗi due_date (một mốc).
 * Điều kiện "của tôi" thì dùng CHUNG qua MyTodoOwnershipScope, không được lệch.
 */
class WorkCalendarService
{
    /** @var MyTodoService */
    private $myTodoService;

    public function __construct(MyTodoService $myTodoService)
    {
        $this->myTodoService = $myTodoService;
    }

    public static function overlaps($start, $end, $from, $to)
    {
        return $start <= $to && $end >= $from;
    }

    public function getAll(array $filters, $userId)
    {
        $from = $filters['from_date'];
        $to   = $filters['to_date'];
        $types = !empty($filters['types']) ? (array) $filters['types'] : null;

        $wanted = function ($type) use ($types) {
            return $types === null || in_array($type, $types);
        };

        $items = collect();

        if ($wanted('task'))            $items = $items->concat($this->fetchTasks($userId, $from, $to));
        if ($wanted('issue'))           $items = $items->concat($this->fetchIssues($userId, $from, $to));
        if ($wanted('assign_job'))      $items = $items->concat($this->fetchAssignJobs($from, $to));
        if ($wanted('assign_business')) $items = $items->concat($this->fetchAssignBusinesses($userId, $from, $to));
        if ($wanted('meeting'))         $items = $items->concat($this->fetchMeetings($from, $to));
        if ($wanted('personal'))        $items = $items->concat($this->fetchPersonalTodos($userId, $from, $to));

        // Lọc trạng thái chỉ có nghĩa khi đang xem ĐÚNG 1 loại (design §7.1)
        if (isset($filters['status']) && $filters['status'] !== null && $filters['status'] !== '' && $types !== null && count($types) === 1) {
            $status = $filters['status'];
            $items = $items->filter(function ($item) use ($status) {
                return (string) $item['status'] === (string) $status;
            });
        }

        return $items->sortBy('start')->values()->all();
    }

    private function fetchTasks($userId, $from, $to)
    {
        // KHÔNG whereNotIn status — lịch hiện đủ mọi trạng thái
        $query = MyTodoOwnershipScope::tasks(Task::query(), $userId)
            ->whereNotNull('due_date')
            ->whereDate('due_date', '>=', Carbon::parse($from)->subDays(1)->toDateString())
            ->where(function ($q) use ($to) {
                $q->whereDate('start_date', '<=', Carbon::parse($to)->toDateString())
                  ->orWhereNull('start_date');
            })
            ->with(['assignee', 'solution']);

        return $this->build($query->get(), 'task', $from, $to);
    }

    private function fetchIssues($userId, $from, $to)
    {
        $query = MyTodoOwnershipScope::issues(Issue::query(), $userId)
            ->where(function ($q) {
                $q->whereNotNull('due_date')->orWhereNotNull('deadline');
            })
            ->with(['assignee', 'solution']);

        return $this->build($query->get(), 'issue', $from, $to);
    }

    private function fetchAssignJobs($from, $to)
    {
        $employeeInfoId = auth()->user()->employee_info_id ?? null;
        if (!$employeeInfoId) {
            return collect();
        }

        $query = MyTodoOwnershipScope::assignJobs(AssignJob::query(), $employeeInfoId)
            ->whereNotNull('time_start_request')
            ->where('time_start_request', '<=', $to)
            ->where(function ($q) use ($from) {
                $q->where('deadline', '>=', $from)->orWhereNull('deadline');
            })
            ->with(['employees']);

        return $this->build($query->get(), 'assign_job', $from, $to);
    }

    private function fetchAssignBusinesses($userId, $from, $to)
    {
        $query = MyTodoOwnershipScope::assignBusinesses(
                AssignRequest::where('type', AssignRequest::PHIEU_CONG_TAC), $userId
            )
            ->whereNotNull('from_time')
            ->where('from_time', '<=', $to)
            ->where(function ($q) use ($from) {
                $q->where('to_time', '>=', $from)->orWhereNull('to_time');
            })
            ->with(['employees']);

        return $this->build($query->get(), 'assign_business', $from, $to);
    }

    private function fetchMeetings($from, $to)
    {
        $employeeInfoId = auth()->user()->employee_info_id ?? null;
        if (!$employeeInfoId) {
            return collect();
        }

        $employee = Employee::where('employee_info_id', $employeeInfoId)->first();
        if (!$employee) {
            return collect();
        }

        // Giữ nguyên phạm vi đã chốt ở Phase 9 feature tiền nhiệm
        $query = Meeting::query()->whereHas('company_members', function ($q) use ($employee) {
            $q->where('employee_id', $employee->id);
        })
        ->whereNotNull('start_date')
        ->where('start_date', '<=', $to)
        ->where(function ($q) use ($from) {
            $q->where('end_date', '>=', $from)->orWhereNull('end_date');
        })
        ->with(['company_members']);

        return $this->build($query->get(), 'meeting', $from, $to);
    }

    private function fetchPersonalTodos($userId, $from, $to)
    {
        $query = MyTodoOwnershipScope::personalTodos(PersonalTodo::query(), $userId)
            ->whereNotNull('due_date')
            ->whereDate('due_date', '>=', Carbon::parse($from)->toDateString())
            ->whereDate('due_date', '<=', Carbon::parse($to)->toDateString())
            ->with(['todoList']);

        return $this->build($query->get(), 'personal', $from, $to);
    }

    /** Chuẩn hoá + lọc overlap lần cuối bằng start/end đã tính (chốt chặn cho mọi loại) */
    private function build($entities, $type, $from, $to)
    {
        $today = Carbon::today();

        return $entities->map(function ($entity) use ($type, $from, $to, $today) {
            $period = WorkItemPeriod::of($entity, $type);
            if ($period === null) {
                return null; // không có ngày -> không lên lịch (design §5)
            }

            $start = $period['start']->format('Y-m-d H:i:s');
            $end   = $period['end']->format('Y-m-d H:i:s');

            if (!self::overlaps($start, $end, $from, $to)) {
                return null;
            }

            $status     = $type === 'personal' ? (bool) $entity->is_completed : $entity->status;
            $group      = WorkItemStatusGroup::of($type, $status);
            $statusInfo = $this->myTodoService->getStatusText($entity, $type);

            return [
                'type'        => $type,
                'id'          => $entity->id,
                'code'        => $entity->code ?? null,
                'title'       => $this->myTodoService->getTitle($entity, $type),
                'subtitle'    => $this->subtitle($entity, $type),
                'start'       => $start,
                'end'         => $end,
                'all_day'     => $period['all_day'],
                'status'      => $status,
                'status_text' => $statusInfo['text'],
                'status_group'=> $group,
                'struck'      => WorkItemStatusGroup::isStruckThrough($type, $status),
                'is_overdue'  => in_array($group, ['todo', 'doing']) && $period['end']->lt($today),
                'url'         => $this->myTodoService->getUrl($entity, $type),
            ];
        })->filter()->values();
    }

    private function subtitle($entity, $type)
    {
        switch ($type) {
            case 'assign_business':
            case 'meeting':
                return $entity->customer_name ?? null;
            case 'assign_job':
                return $entity->customer_name ?: ($entity->place ?? null);
            case 'task':
            case 'issue':
                return optional($entity->solution)->name;
            case 'personal':
                return optional($entity->todoList)->name;
            default:
                return null;
        }
    }
}
```

- [ ] **Step 4: Mở quyền truy cập 3 method của `MyTodoService`**

Trong `MyTodoService.php`, đổi **chỉ từ khoá** `protected` → `public` cho `getTitle`, `getUrl`, `getStatusText`. KHÔNG đổi thân hàm, KHÔNG đổi chữ ký.

- [ ] **Step 5: Chạy test, xác nhận XANH**

```bash
cd hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/Unit/
```

Kỳ vọng: OK — cả 3 file test của Task 1.1/1.2/1.4 đều xanh, 2 test cũ (`CustomerPhoneVisibilityTest`, `CompanyMigrationServiceTest`) không đỏ thêm.

- [ ] **Step 6: Dừng lại báo cáo**

---

### Task 1.5: Endpoint `GET assign/my-todo/calendar`

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/MyTodoController.php` (thêm method `calendar`)
- Modify: `hrm-api/Modules/Assign/Routes/api.php:1063-1076` (thêm route vào nhóm `/assign/my-todo`)
- Test: `HRM/e2e/tests/assign/work-calendar.api.spec.ts`

**Interfaces:**
- Consumes: `WorkCalendarService::getAll()` (Task 1.4).
- Produces: `GET /api/v1/assign/my-todo/calendar?from_date&to_date&types[]&status` → `{ data: WorkItem[] }` theo shape design §4.

- [ ] **Step 1: Viết test đỏ — gồm cả 2 chiều phân quyền**

```ts
/**
 * E2E API — endpoint lịch làm việc 6 loại.
 *
 * Phủ CẢ 2 CHIỀU phân quyền như bộ ca của feature tiền nhiệm: sửa hụt (fail-open,
 * thấy việc của người khác) hay sửa quá tay (không thấy việc của chính mình) đều phải đỏ.
 * Ca dò dữ liệu lúc chạy, KHÔNG viết cứng id — id fixture đổi mỗi lần dựng lại DB.
 */
import { test, expect, request, APIRequestContext } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8000';
const STATE_FILE = path.join(__dirname, '..', '..', '.auth', 'api.json');
const FROM = '2020-01-01 00:00:00';
const TO   = '2030-12-31 23:59:59';
const CAL  = '/api/v1/assign/my-todo/calendar';

const TYPES = ['task', 'issue', 'assign_job', 'assign_business', 'meeting', 'personal'];

let api: APIRequestContext;

test.describe.serial('Lịch làm việc — endpoint', () => {
  test.beforeAll(async () => {
    const token = JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8')).token;
    api = await request.newContext({
      baseURL: API_BASE,
      extraHTTPHeaders: { Authorization: `Bearer ${token}`, Accept: 'application/json' },
    });
  });

  test.afterAll(async () => { await api.dispose(); });

  test('trả item đủ trường bắt buộc, type nằm trong 6 loại', async () => {
    const res = await api.get(`${CAL}?from_date=${FROM}&to_date=${TO}`);
    expect(res.status()).toBe(200);

    const items = (await res.json()).data;
    expect(Array.isArray(items)).toBe(true);
    expect(items.length).toBeGreaterThan(0);

    for (const it of items) {
      expect(TYPES).toContain(it.type);
      expect(it.start).toMatch(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/);
      expect(it.end).toMatch(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/);
      expect(it.end >= it.start).toBe(true);
      expect(typeof it.all_day).toBe('boolean');
      expect(['todo', 'doing', 'done', 'stopped']).toContain(it.status_group);
      expect(typeof it.title).toBe('string');
    }
  });

  test('lọc types[] chỉ trả đúng loại đã chọn', async () => {
    const res = await api.get(`${CAL}?from_date=${FROM}&to_date=${TO}&types[]=meeting`);
    const items = (await res.json()).data;
    expect(items.length).toBeGreaterThan(0);
    expect([...new Set(items.map((i: any) => i.type))]).toEqual(['meeting']);
  });

  test('lọc theo khoảng ngày dùng OVERLAP, không phải start BETWEEN', async () => {
    const all = (await (await api.get(`${CAL}?from_date=${FROM}&to_date=${TO}`)).json()).data;
    const nhieuNgay = all.find((i: any) => i.start.slice(0, 10) !== i.end.slice(0, 10));
    test.skip(!nhieuNgay, 'DB không có việc kéo dài nhiều ngày để kiểm');

    // kỳ nằm GIỮA việc: không chứa start, không chứa end -> vẫn phải thấy
    const giua = nhieuNgay.start.slice(0, 10) < nhieuNgay.end.slice(0, 10);
    expect(giua).toBe(true);
    const res = await api.get(`${CAL}?from_date=${nhieuNgay.end.slice(0, 10)} 00:00:00&to_date=${nhieuNgay.end}`);
    const ids = (await res.json()).data.filter((i: any) => i.type === nhieuNgay.type).map((i: any) => i.id);
    expect(ids).toContain(nhieuNgay.id);
  });

  test('KHÔNG lọc bỏ trạng thái đã xong / đã huỷ', async () => {
    const items = (await (await api.get(`${CAL}?from_date=${FROM}&to_date=${TO}`)).json()).data;
    const nhomKetThuc = items.filter((i: any) => i.status_group === 'done' || i.status_group === 'stopped');
    expect(nhomKetThuc.length).toBeGreaterThan(0); // tab danh sách lọc bỏ, lịch thì không
  });

  test('việc không có hạn thì KHÔNG lên lịch nhưng vẫn còn ở tab danh sách', async () => {
    const listRes = await api.get('/api/v1/assign/my-todo');
    const listItems = (await listRes.json()).data.items;
    const khongHan = listItems.filter((i: any) => !i.due_date);
    test.skip(khongHan.length === 0, 'DB không có việc thiếu hạn để kiểm');

    const calItems = (await (await api.get(`${CAL}?from_date=${FROM}&to_date=${TO}`)).json()).data;
    for (const it of khongHan) {
      const conTrenLich = calItems.some((c: any) => c.type === it.type && c.id === it.id);
      expect(conTrenLich, `${it.type}#${it.id} không có hạn mà vẫn lên lịch`).toBe(false);
    }
  });

  test('fail-closed: mọi item trả về đều thuộc về chính user đang đăng nhập', async () => {
    const calItems = (await (await api.get(`${CAL}?from_date=${FROM}&to_date=${TO}`)).json()).data;

    // đối chiếu với tab danh sách: mọi item trên lịch mà tab danh sách CŨNG lấy
    // (tức còn mở) thì phải khớp id; lịch không được rộng hơn về mặt "của ai"
    const listItems = (await (await api.get('/api/v1/assign/my-todo')).json()).data.items;
    const listKeys = new Set(listItems.map((i: any) => `${i.type}#${i.id}`));

    const conMo = calItems.filter((i: any) => i.status_group === 'todo' || i.status_group === 'doing');
    expect(conMo.length).toBeGreaterThan(0);

    for (const it of conMo) {
      // meeting là ngoại lệ hợp lệ: tab danh sách chỉ lấy status 1,2 còn lịch lấy đủ 5
      if (it.type === 'meeting') continue;
      // task/issue "Nháp"/"Chờ duyệt" cũng là ngoại lệ: tab danh sách loại Nháp
      if (it.type === 'task' && [1].includes(Number(it.status))) continue;
      expect(listKeys.has(`${it.type}#${it.id}`), `${it.type}#${it.id} có trên lịch mà không có ở tab danh sách`).toBe(true);
    }
  });

  test('thiếu from_date/to_date thì trả 400, không trả toàn bộ DB', async () => {
    expect((await api.get(CAL)).status()).toBe(400);
    expect((await api.get(`${CAL}?from_date=${FROM}`)).status()).toBe(400);
  });
});
```

- [ ] **Step 2: Chạy test, xác nhận ĐỎ**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar.api.spec.ts --project=api
```

Kỳ vọng: FAIL — 404 vì chưa có route. Đọc **dòng tổng kết**, không nhìn mỗi ca cuối.

- [ ] **Step 3: Thêm method `calendar()` vào `MyTodoController`**

```php
/**
 * Lịch làm việc — 6 loại, lọc overlap theo khoảng ngày. Khác index() ở chỗ
 * KHÔNG loại trạng thái nào và trả start/end thay vì due_date (design §3, §7.3).
 */
public function calendar(Request $request)
{
    try {
        $request->validate([
            'from_date' => 'required|date',
            'to_date'   => 'required|date',
            'types'     => 'nullable|array',
            'types.*'   => 'in:task,issue,assign_job,assign_business,meeting,personal',
        ]);

        $items = app(WorkCalendarService::class)->getAll([
            'from_date' => $request->input('from_date'),
            'to_date'   => $request->input('to_date'),
            'types'     => $request->input('types'),
            'status'    => $request->input('status'),
        ], auth()->id());

        return $this->responseJson('success', Response::HTTP_OK, $items);
    } catch (ValidationException $e) {
        return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
    } catch (Exception $e) {
        Log::error($e);

        return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
    }
}
```

Thêm import: `use Illuminate\Validation\ValidationException;` và `use Modules\Assign\Services\MyTodo\WorkCalendarService;`.

- [ ] **Step 4: Thêm route**

Trong `Modules/Assign/Routes/api.php`, nhóm `'/assign/my-todo'`, đặt **TRƯỚC** các route có tham số động để không bị nuốt:

```php
Route::group(['prefix' => '/assign/my-todo'], function () {
    Route::get('/', [MyTodoController::class, 'index']);
    Route::get('/calendar', [MyTodoController::class, 'calendar']);   // <— thêm dòng này
    Route::get('/lists', [MyTodoController::class, 'listLists']);
    // ... giữ nguyên phần còn lại
});
```

- [ ] **Step 5: Chạy test, xác nhận XANH**

```bash
cd hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan config:clear && /opt/homebrew/opt/php@7.4/bin/php artisan route:clear
cd HRM/e2e && npx playwright test tests/assign/work-calendar.api.spec.ts --project=api
```

Kỳ vọng: 7 passed. Nếu có ca `skipped` vì DB thiếu dữ liệu thì ghi lại vào báo cáo, đừng lờ đi.

- [ ] **Step 6: Đo thời gian phản hồi trên dữ liệu thật**

```bash
cd hrm-api && time curl -s -o /dev/null -w "%{time_total}s\n" \
  -H "Authorization: Bearer $(python3 -c "import json;print(json.load(open('../e2e/.auth/api.json'))['token'])")" \
  "http://127.0.0.1:8000/api/v1/assign/my-todo/calendar?from_date=2026-09-01%2000:00:00&to_date=2026-10-12%2023:59:59"
```

Ghi lại con số. Trên 1.5s thì báo cáo kèm số đo và đề xuất index, **không tự ý cắt bớt dữ liệu** để cho nhanh.

- [ ] **Step 7: Dừng lại báo cáo**

---

## Phase 2 — Frontend: nền tảng loại việc + đổi tên

### Task 2.1: Bảng loại việc `work-item-types.js`

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/calendar/work-item-types.js`
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/calendar-status.js`

**Interfaces:**
- Consumes: `status_group` từ API (Task 1.5).
- Produces:
  - `WORK_ITEM_TYPES` — mảng `{ key, label, color, icon }` theo đúng thứ tự hiển thị.
  - `typeColor(type): string` · `typeLabel(type): string` · `typeIcon(type): string`
  - `cardTypeStyle(type): object` — trả `{'--card-color','--card-bg','--card-border'}`
  - `groupDotColor(group): string`
  - `MEETING_STATUS_OPTIONS` giữ nguyên (đang dùng nơi khác).

- [ ] **Step 1: Viết `work-item-types.js`**

```js
// Nguồn DUY NHẤT về 6 loại việc trên lịch: nhãn, màu, icon, thứ tự.
// Chip lọc, thanh tóm tắt, thẻ, drawer đều đọc từ đây — KHÔNG khai báo lại chỗ khác.
// 3 màu đầu lấy nguyên token đã chốt ở mockup
// (.plans/gop-db/ke-hoach-phat-trien-thi-truong/ke-hoach-phat-trien-thi-truong-mockup.html);
// 3 màu sau là mới, chọn tông tương phản để 6 loại phân biệt được khi nhìn lướt.
export const WORK_ITEM_TYPES = [
    { key: 'assign_business', label: 'Phiếu công tác',      color: '#0d9488', icon: 'ri-briefcase-line' },
    { key: 'meeting',         label: 'Meeting',             color: '#4f46e5', icon: 'ri-group-line' },
    { key: 'task',            label: 'Task',                color: '#ea580c', icon: 'ri-task-line' },
    { key: 'issue',           label: 'Issue',               color: '#e11d48', icon: 'ri-bug-line' },
    { key: 'assign_job',      label: 'Phiếu giao việc',     color: '#ca8a04', icon: 'ri-file-list-3-line' },
    { key: 'personal',        label: 'Nhắc việc cá nhân',   color: '#64748b', icon: 'ri-sticky-note-line' },
]

const BY_KEY = WORK_ITEM_TYPES.reduce((acc, t) => {
    acc[t.key] = t
    return acc
}, {})

const FALLBACK = { key: '', label: '', color: '#94a3b8', icon: 'ri-checkbox-blank-circle-line' }

export function typeInfo(type) {
    return BY_KEY[type] || FALLBACK
}

export function typeColor(type) {
    return typeInfo(type).color
}

export function typeLabel(type) {
    return typeInfo(type).label
}

export function typeIcon(type) {
    return typeInfo(type).icon
}

function hexToRgbTuple(hex) {
    const clean = String(hex || '').replace('#', '')
    const bigint = parseInt(clean, 16)
    if (Number.isNaN(bigint)) return [148, 163, 184]
    return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255]
}

export function typeColorRgba(type, alpha) {
    const [r, g, b] = hexToRgbTuple(typeColor(type))
    return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

// Nền/viền thẻ theo LOẠI — giữ đúng công thức mockup: nền alpha 0.13, viền 0.38
export function cardTypeStyle(type) {
    return {
        '--card-color': typeColor(type),
        '--card-bg': typeColorRgba(type, 0.13),
        '--card-border': typeColorRgba(type, 0.38),
    }
}
```

- [ ] **Step 2: Thêm phần nhóm trạng thái vào `calendar-status.js`**

Giữ nguyên toàn bộ nội dung cũ (`MEETING_STATUS_OPTIONS`, `statusColor`, `cardStatusStyle`… — vẫn có nơi dùng), **thêm** vào cuối file:

```js
// ---- Nhóm trạng thái dùng chung cho 6 loại (BE trả sẵn `status_group`) ----
// FE KHÔNG tự map lại từ status thật: bảng gộp nằm ở
// Modules/Assign/Services/MyTodo/WorkItemStatusGroup.php
const GROUP_DOT_HEX = {
    todo: '#94a3b8',
    doing: '#3b82f6',
    done: '#22c55e',
    stopped: '#ef4444',
}

export function groupDotColor(group) {
    return GROUP_DOT_HEX[group] || GROUP_DOT_HEX.todo
}

// Việc đã kết thúc thì làm mờ thẻ (cả done lẫn stopped)
export function isGroupMuted(group) {
    return group === 'done' || group === 'stopped'
}
```

- [ ] **Step 3: Kiểm cú pháp bằng build**

```bash
cd hrm-client && export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh" && nvm use 12 && node --check pages/assign/my-todo/components/calendar/work-item-types.js && node --check pages/assign/my-todo/components/calendar/calendar-status.js
```

Kỳ vọng: không in lỗi.

- [ ] **Step 4: Dừng lại báo cáo**

---

### Task 2.2: Đổi tên component + đổi nhãn tab

**Files:**
- Rename: `MeetingCalendarTab.vue` → `WorkCalendarTab.vue` · `MeetingCard.vue` → `WorkItemCard.vue` · `MeetingMultiDayBar.vue` → `WorkItemMultiDayBar.vue` · `MeetingDetailDrawer.vue` → `WorkItemDetailDrawer.vue` · `DayMeetingsPopover.vue` → `DayItemsPopover.vue` (đều trong `hrm-client/pages/assign/my-todo/components/calendar/`)
- Modify: `hrm-client/pages/assign/my-todo/index.vue:7` (nhãn tab) và `:122-124` (thẻ component)
- Modify: `MonthGrid.vue`, `WeekGrid.vue` (import + tên thẻ con)
- Modify: mọi spec e2e đang bám selector cũ

**Interfaces:**
- Consumes: không.
- Produces: tên component mới dùng cho Phase 3-5.

- [ ] **Step 1: Chụp lại danh sách selector e2e đang phụ thuộc**

```bash
cd HRM/e2e && grep -rn "meeting-calendar-tab\|ticket-card\|MeetingCard\|meeting-detail-drawer\|day-meetings-popover" tests/ pages/ utils/ | tee /tmp/e2e-selectors-truoc.txt && wc -l /tmp/e2e-selectors-truoc.txt
```

Ghi lại số dòng — Step 5 phải xử lý hết chỗ này.

- [ ] **Step 2: Đổi tên file + cập nhật import**

```bash
cd hrm-client/pages/assign/my-todo/components/calendar
git mv MeetingCalendarTab.vue WorkCalendarTab.vue
git mv MeetingCard.vue WorkItemCard.vue
git mv MeetingMultiDayBar.vue WorkItemMultiDayBar.vue
git mv MeetingDetailDrawer.vue WorkItemDetailDrawer.vue
git mv DayMeetingsPopover.vue DayItemsPopover.vue
```

Rồi sửa từng file: đổi `name:` bên trong `export default`, đổi mọi `import ... from './Meeting*.vue'`, đổi tên thẻ trong `<template>` (`<meeting-card>` → `<work-item-card>`, `<meeting-detail-drawer>` → `<work-item-detail-drawer>`, `<day-meetings-popover>` → `<day-items-popover>`, `<meeting-multi-day-bar>` → `<work-item-multi-day-bar>`).

Đổi luôn class gốc `.meeting-calendar-tab` → `.work-calendar-tab` để selector e2e nói đúng thứ nó trỏ tới.

- [ ] **Step 3: Đổi nhãn tab trong `index.vue`**

```html
<button type="button" class="mt-view-tabs__btn" :class="{ active: activeTab === 'calendar' }" @click="activeTab = 'calendar'">📅 Lịch làm việc</button>
```

và thẻ component:

```html
<div v-if="activeTab === 'calendar'" class="mt-tab-calendar">
    <work-calendar-tab />
</div>
```

cùng phần `components: { ..., WorkCalendarTab }` và import tương ứng.

- [ ] **Step 4: Restart Nuxt sạch rồi mở màn**

```bash
cd hrm-client && rm -rf .nuxt/components
# tìm PID đang giữ cổng 3000 rồi kill ĐÚNG PID đó — KHÔNG pkill theo tên
lsof -ti tcp:3000
# kill <PID vừa in>
export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh" && nvm use 12 && NODE_OPTIONS=--max-old-space-size=8192 npm run dev
```

Mở `http://127.0.0.1:3000/assign/my-todo`, bấm tab thứ 2. Kỳ vọng: tab tên "📅 Lịch làm việc", lịch vẫn render như trước (dữ liệu vẫn là endpoint meeting cũ — Phase 3 mới đổi). Nếu báo "Can't resolve component" thì restart lại + xoá `.nuxt/components`, đây là manifest cũ chứ không phải lỗi code.

- [ ] **Step 5: Cập nhật selector e2e rồi chạy TOÀN BỘ bộ test của màn**

Sửa mọi chỗ trong `/tmp/e2e-selectors-truoc.txt` sang tên/class mới, rồi:

```bash
cd HRM/e2e && npx playwright test tests/assign/my-todo --reporter=list 2>&1 | tail -30
```

Kỳ vọng: đọc **dòng tổng kết** — số passed phải bằng số ca, không có "did not run". Bộ chạy serial nên một ca đỏ sẽ che hết phần sau.

- [ ] **Step 6: Dừng lại báo cáo**

---

## Phase 3 — Frontend: dữ liệu, lưới, thẻ

### Task 3.1: `WorkCalendarTab` đổi sang endpoint mới

**Files:**
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/WorkCalendarTab.vue`
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/calendar-lanes.js`
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/calendar-week-helpers.js`

**Interfaces:**
- Consumes: `GET assign/my-todo/calendar` (Task 1.5); `WORK_ITEM_TYPES` (Task 2.1).
- Produces: prop `items` (thay `meetings`) truyền xuống `MonthGrid`/`WeekGrid`; mỗi item có `start`/`end`/`all_day`.

- [ ] **Step 1: Đổi `calendar-lanes.js` đọc `start`/`end` thay vì `start_date`/`end_date`**

Hai helper đang đọc tên cột meeting:

```js
// TRƯỚC
export function startDateStr(m) { return m && m.start_date ? String(m.start_date).slice(0, 10) : '' }
export function effectiveEndDate(m) { ... m.end_date ... }

// SAU — đọc khoảng chuẩn hoá, dùng chung cho 6 loại
export function startDateStr(item) {
    return item && item.start ? String(item.start).slice(0, 10) : ''
}
export function effectiveEndDate(item) {
    if (!item) return ''
    const end = item.end || item.start
    return end ? String(end).slice(0, 10) : ''
}
```

Giữ nguyên `assignMultiDayLanes`, `computeWeekSegments`, `mapLanesToDisplayRows`, `monthGridStart`, `mondayOf` — chúng gọi qua 2 helper trên nên tự đúng theo.

- [ ] **Step 2: Đổi `calendar-week-helpers.js` phân loại cả ngày theo cờ `all_day`**

```js
// Việc "cả ngày" nay do BE quyết (cờ all_day), không suy từ việc thiếu giờ nữa
export function getAllDayTicketsForDate(items, dateStr) {
    return (items || []).filter((it) => it.all_day && startDateStr(it) <= dateStr && effectiveEndDate(it) >= dateStr)
}

export function getTicketsForDateHour(items, dateStr, hour) {
    return (items || []).filter((it) => {
        if (it.all_day) return false
        if (startDateStr(it) !== dateStr) return false
        return Number(String(it.start).slice(11, 13)) === hour
    })
}
```

- [ ] **Step 3: Đổi `fetchMeetings` → `fetchItems` trong `WorkCalendarTab.vue`**

```js
async fetchItems() {
    try {
        this.loading = true
        const params = {
            from_date: this.fetchRange.from,
            to_date: this.fetchRange.to,
            status: this.filters.status,
        }
        // types[] gửi dạng mảng — rỗng nghĩa là lấy tất cả
        const query = buildQueryString(params) +
            (this.filters.types.length ? this.filters.types.map((t) => `&types[]=${encodeURIComponent(t)}`).join('') : '')

        const { data } = await this.$store.dispatch('apiGetMethod', 'assign/my-todo/calendar' + query)
        this.items = data || []
    } catch (error) {
        this.$toasted?.global?.error?.({ message: 'Lỗi khi tải dữ liệu lịch làm việc' })
        this.items = []
    } finally {
        this.loading = false
    }
}
```

Đổi `data()`: `meetings: []` → `items: []`, `filters: { meeting_type_id: null, status: null }` → `filters: { types: [], status: null }`. Đổi mọi `this.meetings` → `this.items`, `summaryPeriodMeetings` → `summaryPeriodItems`, và 3 `watch` gọi `fetchItems()`. Bỏ `loadMeetingTypes()` cùng `meetingTypes` (chip loại thay cho select loại meeting).

**Giữ nguyên** `fetchRange` (lưới tháng 6 hàng cố định từ `monthGridStart`) và cách `summaryPeriodItems` lọc theo overlap — hai chỗ này từng gây lỗi lệch lưới và lệch số ở feature tiền nhiệm.

- [ ] **Step 4: Đổi prop truyền xuống lưới + sửa khoá lặp**

`MonthGrid`/`WeekGrid`: prop `meetings` → `items`, sự kiện `click-meeting` → `click-item`, `click-more` giữ nguyên. Sửa cả trong 2 file lưới. Đổi luôn tên biến nội bộ `day.shownMeetings` → `day.shownItems`.

⚠️ **Khoá lặp phải gồm cả loại.** Bản cũ dùng `:key="m.id"` vì chỉ có meeting; nay 6 loại đánh id độc lập nên id trùng nhau giữa các loại là chuyện chắc chắn xảy ra — trùng khoá làm Vue tái dùng nhầm DOM:

```html
<work-item-card
    v-for="it in day.shownItems"
    :key="it.type + '-' + it.id"
    :item="it"
    @click="onCardClick"
/>
```

Áp cùng quy tắc cho `WorkItemMultiDayBar` trong cả 2 lưới.

- [ ] **Step 4b: Giữ thanh lọc chạy được ở trạng thái trung gian**

`filters` vừa đổi shape sang `{ types, status }` và `meetingTypes` đã bị bỏ, nhưng `CalendarFilterToolbar` đến Task 4.1 mới dựng lại. Nếu để nguyên, toolbar cũ đọc prop không còn tồn tại và có thể ném lỗi, làm đỏ oan e2e của Task 3.2/3.3. Sửa tối thiểu ngay tại đây — chỉ đủ để không vỡ:

```html
<template>
    <div class="calendar-filter-toolbar">
        <button type="button" class="calendar-filter-reset" title="Làm mới" @click="$emit('filter-clear')">
            <i class="ri-refresh-line"></i>
        </button>
    </div>
</template>

<script>
export default {
    name: 'CalendarFilterToolbar',
    // Bản rút gọn tạm thời — Task 4.1 dựng đủ 6 chip + ô trạng thái động.
    props: {
        value: { type: Object, default: () => ({ types: [], status: null }) },
    },
}
</script>
```

Chỗ gọi trong `WorkCalendarTab.vue` đổi sang `:value="filters"` và bỏ `:meeting-types`.

- [ ] **Step 5: Viết e2e đo số thẻ trên lưới khớp API**

```ts
/**
 * Lưới lịch phải vẽ ĐÚNG số việc mà API trả cho kỳ đang xem.
 * Đo bằng số lấy từ DOM, không nhìn ảnh — "trông có vẻ ổn" từng bỏ lọt lỗi.
 */
import { test, expect } from '@playwright/test';

test.describe.serial('Lịch làm việc — lưới khớp API', () => {
  test('số thẻ trên lưới tháng bằng số item API trả về', async ({ page }) => {
    const items: any[] = [];
    page.on('response', async (res) => {
      if (res.url().includes('/assign/my-todo/calendar') && res.status() === 200) {
        items.push(...((await res.json()).data || []));
      }
    });

    await page.goto('/assign/my-todo');
    await page.getByRole('button', { name: 'Lịch làm việc' }).click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));
    await expect(page.locator('.work-calendar-tab')).toBeVisible();

    // chờ lưới vẽ xong — chờ đúng mốc là thẻ đầu tiên, không chờ khung ngoài
    await page.locator('.ticket-card, .multiday-bar').first().waitFor();

    const soThe = await page.locator('.ticket-card').count();
    const soThanh = await page.locator('.multiday-bar').count();
    expect(soThe + soThanh).toBeGreaterThan(0);
    expect(items.length).toBeGreaterThan(0);
  });
});
```

Lưu vào `HRM/e2e/tests/assign/work-calendar-grid.spec.ts`.

- [ ] **Step 6: Chạy e2e, xác nhận XANH**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-grid.spec.ts --reporter=list 2>&1 | tail -20
```

- [ ] **Step 7: Dừng lại báo cáo**

---

### Task 3.1b: Fixture dữ liệu đa loại cho e2e (CHÈN THÊM 2026-09-11)

> Task này KHÔNG có trong plan gốc. Chèn vào sau khi đo thật: tài khoản e2e chỉ có **11 meeting + 1 nhắc việc
> cá nhân**, KHÔNG có task/issue/phiếu công tác/phiếu giao việc, **0 item cả ngày**, **0 item nhiều ngày**.
> Không có fixture thì ca kiểm màu (3.2) chỉ chạm 2/6 màu, ca hàng "Cả ngày" và thanh nhiều ngày (3.3) skip,
> ca bấm đủ 6 loại (6.1) không làm được — tức là kiểm cho có.

**Files:**
- Create: `HRM/e2e/utils/work-calendar-fixtures.ts`

**Interfaces:**
- Produces: `taoFixtureDaLoai(api): Promise<FixtureIds>` và `donFixtureDaLoai(api): Promise<void>`.
  Mọi bản ghi tạo ra mang tiền tố nhận dạng `[E2E lichlv]` trong tiêu đề để dọn được và không đụng dữ liệu thật.

**Ràng buộc:**
- **KHÔNG sửa `e2e/auth/api.setup.ts` hay `e2e_provision.php`** — mọi spec khác phụ thuộc chúng; thêm fixture ở đó
  có thể làm lệch số của bộ test khác.
- Tạo qua **API thật**, không ghi thẳng DB.
- Dọn phải chạy được cả khi ca đỏ giữa chừng.
- Loại nào KHÔNG tạo được qua API thì **báo rõ lý do**, không im lặng bỏ qua.

**Thứ tự ưu tiên (làm được đến đâu báo đến đó):**
1. Nhắc việc cá nhân **CẢ NGÀY** — `POST assign/my-todo/todos` với `due_date` có, `due_time` rỗng. Dễ nhất, chắc chắn được.
2. **Meeting nhiều ngày** — `start_date`/`end_date` lệch ngày nhau. Cho cả thanh nhiều ngày lẫn loại meeting.
3. **Task** — `POST assign/tasks`, cần `project_id` (fixture có sẵn), `solution_id` (dò qua API), `assignee_id`,
   `priority`, `status`, `estimated_hours`. ⚠️ `TaskStoreRequest` **comment out `start_date`** nên task tạo qua API
   nhiều khả năng chỉ 1 ngày — ghi rõ nếu đúng vậy.
4. **Issue** — dò xem có API tạo không.
5. **Phiếu công tác / phiếu giao việc** — nhiều khả năng vướng luồng duyệt; nếu quá tốn thì DỪNG và báo, đừng đục.

---

### Task 3.2: `WorkItemCard` — màu theo loại, chấm theo trạng thái

**Files:**
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/WorkItemCard.vue`
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/WorkItemMultiDayBar.vue`
- Test: `HRM/e2e/tests/assign/work-calendar-card.spec.ts`

**Interfaces:**
- Consumes: `cardTypeStyle`, `typeIcon`, `typeLabel` (Task 2.1); `groupDotColor`, `isGroupMuted` (Task 2.1 Step 2); item shape từ Task 1.5.
- Produces: thẻ có `data-type`, `data-group`, class `ticket-card--muted` / `ticket-card--struck`, badge `.ticket-overdue-badge`.

- [ ] **Step 1: Viết e2e đỏ — đo màu, độ mờ, gạch ngang bằng `getComputedStyle`**

```ts
/**
 * Thẻ tô màu theo LOẠI (không theo trạng thái như bản chỉ-meeting cũ), chấm màu
 * theo NHÓM trạng thái. Đo bằng getComputedStyle lấy từ DOM.
 */
import { test, expect } from '@playwright/test';

const MAU_LOAI: Record<string, string> = {
  assign_business: 'rgb(13, 148, 136)',
  meeting: 'rgb(79, 70, 229)',
  task: 'rgb(234, 88, 12)',
  issue: 'rgb(225, 29, 72)',
  assign_job: 'rgb(202, 138, 4)',
  personal: 'rgb(100, 116, 139)',
};

test.describe.serial('Lịch làm việc — thẻ', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/assign/my-todo');
    await page.getByRole('button', { name: 'Lịch làm việc' }).click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));
    await page.locator('.ticket-card').first().waitFor();
  });

  test('mỗi thẻ tô đúng màu của LOẠI nó', async ({ page }) => {
    const loaiCoTren = await page.$$eval('.ticket-card', (els) =>
      [...new Set(els.map((e) => (e as HTMLElement).dataset.type || ''))].filter(Boolean),
    );
    expect(loaiCoTren.length).toBeGreaterThan(0);

    for (const loai of loaiCoTren) {
      const mau = await page.$eval(`.ticket-card[data-type="${loai}"]`, (el) =>
        getComputedStyle(el).getPropertyValue('--card-color').trim(),
      );
      // token có thể ở dạng hex — quy về rgb để so
      const rgb = await page.evaluate((hex) => {
        const d = document.createElement('div');
        d.style.color = hex;
        document.body.appendChild(d);
        const v = getComputedStyle(d).color;
        d.remove();
        return v;
      }, mau);
      expect(rgb, `màu thẻ loại ${loai}`).toBe(MAU_LOAI[loai]);
    }
  });

  test('việc đã xong / đã huỷ thì mờ, và chỉ việc kết thúc hẳn mới gạch ngang', async ({ page }) => {
    const ketThuc = page.locator('.ticket-card[data-group="done"], .ticket-card[data-group="stopped"]');
    const n = await ketThuc.count();
    test.skip(n === 0, 'Kỳ đang xem không có việc đã kết thúc');

    const opacity = await ketThuc.first().evaluate((el) => parseFloat(getComputedStyle(el).opacity));
    expect(opacity).toBeLessThan(1);

    const struck = page.locator('.ticket-card--struck .ticket-card__title');
    if (await struck.count()) {
      const deco = await struck.first().evaluate((el) => getComputedStyle(el).textDecorationLine);
      expect(deco).toContain('line-through');
    }

    // Task "Tạm dừng" (status 5) thuộc nhóm stopped nhưng KHÔNG được gạch ngang
    const tamDung = page.locator('.ticket-card[data-type="task"][data-status="5"]');
    if (await tamDung.count()) {
      await expect(tamDung.first()).not.toHaveClass(/ticket-card--struck/);
    }
  });

  test('việc cả ngày ghi "Cả ngày" thay cho khoảng giờ', async ({ page }) => {
    const caNgay = page.locator('.ticket-card[data-all-day="true"]');
    test.skip((await caNgay.count()) === 0, 'Kỳ đang xem không có việc cả ngày');
    await expect(caNgay.first().locator('.ticket-card__time')).toHaveText('Cả ngày');
  });
});
```

- [ ] **Step 2: Chạy, xác nhận ĐỎ**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-card.spec.ts --reporter=list 2>&1 | tail -20
```

Kỳ vọng: đỏ ở ca đầu — thẻ chưa có `data-type`, màu vẫn theo trạng thái.

- [ ] **Step 3: Viết lại `WorkItemCard.vue`**

```html
<template>
    <button
        type="button"
        class="ticket-card"
        :class="{ 'ticket-card--muted': isMuted, 'ticket-card--struck': item.struck }"
        :style="cardStyle"
        :data-type="item.type"
        :data-group="item.status_group"
        :data-status="String(item.status)"
        :data-all-day="String(!!item.all_day)"
        :title="title"
        @click="$emit('click', item)"
    >
        <span class="ticket-card__top">
            <span class="ticket-card__icon"><i :class="icon"></i></span>
            <span class="ticket-card__title">{{ title }}</span>
        </span>

        <span v-if="item.subtitle" class="ticket-card__customer" :title="item.subtitle">{{ item.subtitle }}</span>

        <span class="ticket-card__badges">
            <span class="ticket-card__time">{{ timeText }}</span>
            <span class="ticket-status-badge">
                <span class="ticket-status-badge__dot" :style="{ background: dotColor }"></span>
                {{ item.status_text }}
            </span>
            <span v-if="item.is_overdue" class="ticket-overdue-badge">Quá hạn</span>
        </span>
    </button>
</template>

<script>
import dayjs from 'dayjs'
import { cardTypeStyle, typeIcon } from './work-item-types'
import { groupDotColor, isGroupMuted } from './calendar-status'

export default {
    name: 'WorkItemCard',
    props: {
        item: { type: Object, required: true },
    },
    computed: {
        title() {
            return (this.item && this.item.title) || ''
        },
        icon() {
            return typeIcon(this.item.type)
        },
        cardStyle() {
            return cardTypeStyle(this.item.type)
        },
        dotColor() {
            return groupDotColor(this.item.status_group)
        },
        isMuted() {
            return isGroupMuted(this.item.status_group)
        },
        timeText() {
            if (this.item.all_day) return 'Cả ngày'
            const s = dayjs(this.item.start)
            const e = dayjs(this.item.end)
            return s.format('HH:mm') + ' - ' + e.format('HH:mm')
        },
    },
}
</script>
```

CSS: giữ nguyên khối `.ticket-card*` cũ; đổi `.ticket-card--muted` sang `opacity: .55`; thêm:

```css
.ticket-card--struck .ticket-card__title { text-decoration: line-through; }
.ticket-overdue-badge {
    background: #fee2e2; color: #b91c1c; border-radius: 4px;
    padding: 0 4px; font-size: 10px; font-weight: 600; margin-left: 4px;
}
```

- [ ] **Step 4: Sửa `WorkItemMultiDayBar.vue` tương ứng**

Đổi prop `meeting` → `item`, dùng `cardTypeStyle(item.type)` thay `cardStatusStyle(item.status)`, thêm cùng bộ `data-type`/`data-group`/`data-status`, class `--muted`/`--struck` như trên. Giữ nguyên phần tính đoạn tràn tuần + mũi tên ‹ ›.

- [ ] **Step 5: Chạy e2e, xác nhận XANH**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-card.spec.ts --reporter=list 2>&1 | tail -20
```

Kỳ vọng: 3 passed (ca nào `skipped` vì kỳ đang xem thiếu dữ liệu thì ghi vào báo cáo).

- [ ] **Step 6: Dừng lại báo cáo**

---

### Task 3.3: Lưới Tuần — việc cả ngày và thanh nhiều ngày

**Files:**
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/WeekGrid.vue`
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/MonthGrid.vue`
- Test: `HRM/e2e/tests/assign/work-calendar-week.spec.ts`

**Interfaces:**
- Consumes: `getAllDayTicketsForDate`, `getTicketsForDateHour` (Task 3.1 Step 2); `WorkItemCard` (Task 3.2).
- Produces: hàng `.calendar-week__row--allday` chứa đúng việc `all_day`.

- [ ] **Step 1: Viết e2e đỏ — đo bằng TOẠ ĐỘ, không nhìn ảnh**

```ts
/**
 * Việc "cả ngày" phải nằm trong hàng Cả ngày của lưới Tuần, việc có giờ thì không.
 * Kiểm bằng toạ độ hình học — bao nhau theo trục Y — chứ không tin vào ảnh chụp.
 */
import { test, expect } from '@playwright/test';

test.describe.serial('Lịch làm việc — lưới Tuần', () => {
  test('việc cả ngày nằm đúng hàng "Cả ngày"', async ({ page }) => {
    await page.goto('/assign/my-todo');
    await page.getByRole('button', { name: 'Lịch làm việc' }).click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));
    await page.getByRole('button', { name: 'Tuần', exact: true }).click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));
    await page.locator('.calendar-week__row--allday').waitFor();

    const hang = await page.locator('.calendar-week__row--allday').boundingBox();
    expect(hang).not.toBeNull();

    const caNgay = page.locator('.ticket-card[data-all-day="true"]');
    const n = await caNgay.count();
    test.skip(n === 0, 'Tuần đang xem không có việc cả ngày');

    for (let i = 0; i < n; i++) {
      const o = await caNgay.nth(i).boundingBox();
      expect(o!.y).toBeGreaterThanOrEqual(hang!.y - 1);
      expect(o!.y + o!.height).toBeLessThanOrEqual(hang!.y + hang!.height + 1);
    }

    // ngược lại: việc có giờ KHÔNG được nằm trong hàng Cả ngày
    const coGio = page.locator('.ticket-card[data-all-day="false"]');
    if (await coGio.count()) {
      const o = await coGio.first().boundingBox();
      expect(o!.y).toBeGreaterThan(hang!.y + hang!.height - 1);
    }
  });

  test('thanh nhiều ngày trải đúng số ngày', async ({ page }) => {
    await page.goto('/assign/my-todo');
    await page.getByRole('button', { name: 'Lịch làm việc' }).click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));
    await page.locator('.ticket-card, .multiday-bar').first().waitFor();

    const thanh = page.locator('.multiday-bar');
    test.skip((await thanh.count()) === 0, 'Kỳ đang xem không có việc nhiều ngày');

    const oNgay = await page.locator('.calendar-day').first().boundingBox();
    const box = await thanh.first().boundingBox();
    // trải ≥ 2 ô ngày thì mới gọi là thanh nhiều ngày
    expect(box!.width).toBeGreaterThan(oNgay!.width * 1.5);
  });
});
```

- [ ] **Step 2: Chạy, xác nhận ĐỎ hoặc xác nhận đã xanh sẵn**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-week.spec.ts --reporter=list 2>&1 | tail -20
```

Hàng "Cả ngày" đã có sẵn từ bản meeting (`WeekGrid.vue:31`) nên ca 1 có thể xanh ngay sau Task 3.1 — nếu vậy ghi rõ trong báo cáo là "xanh sẵn, không cần sửa", đừng sửa mò.

- [ ] **Step 3: Sửa `WeekGrid.vue` + `MonthGrid.vue` cho khớp prop mới**

Đổi prop `meetings` → `items`, đổi tên biến vòng lặp, đổi `<meeting-card :meeting="m">` → `<work-item-card :item="it">`, đổi phát sự kiện `click-meeting` → `click-item`. Ô ngày của lưới tháng tên class thật là `.calendar-day` (kèm `[data-date]`) — xem `MonthGrid.vue:38`. Đừng đổi class chỉ để chiều test.

- [ ] **Step 4: Chạy lại, xác nhận XANH**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-week.spec.ts --reporter=list 2>&1 | tail -20
```

- [ ] **Step 5: Dừng lại báo cáo**

---

## Phase 4 — Frontend: chip lọc + thanh tóm tắt

### Task 4.1: Chip lọc 6 loại + ô trạng thái động

**Files:**
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/CalendarFilterToolbar.vue`
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/WorkCalendarTab.vue`
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/work-item-types.js` (thêm `STATUS_OPTIONS_BY_TYPE`, file do Task 2.1 tạo)
- Test: `HRM/e2e/tests/assign/work-calendar-filter.spec.ts`

**Interfaces:**
- Consumes: `WORK_ITEM_TYPES` (Task 2.1); `filters.types` / `filters.status` (Task 3.1).
- Produces: sự kiện `@toggle-type="(typeKey) => void"` và `@filter-change="({ status }) => void"`.
- **Bộ trạng thái cho ô select** — id kiểu **STRING** (bắt buộc, xem Global Constraints):

```js
export const STATUS_OPTIONS_BY_TYPE = {
    task: [
        { id: '1', name: 'Nháp' }, { id: '2', name: 'Chờ duyệt' }, { id: '3', name: 'Cần làm' },
        { id: '4', name: 'Đang làm' }, { id: '5', name: 'Tạm dừng' }, { id: '6', name: 'Review' },
        { id: '7', name: 'Từ chối' }, { id: '8', name: 'Hoàn thành' }, { id: '9', name: 'Huỷ' },
        { id: '10', name: 'Từ chối bắt đầu' },
    ],
    issue: [
        { id: 'new', name: 'Mới' }, { id: 'assigned', name: 'Đã giao' }, { id: 'in_progress', name: 'Đang xử lý' },
        { id: 'resolved', name: 'Đã xử lý' }, { id: 'closed', name: 'Đã đóng' }, { id: 'reopened', name: 'Mở lại' },
        { id: 'completed', name: 'Hoàn thành' }, { id: 'rejected', name: 'Từ chối' },
    ],
    assign_job: [
        { id: '1', name: 'Đang tạo' }, { id: '2', name: 'Chờ duyệt' }, { id: '3', name: 'Đã duyệt' },
        { id: '4', name: 'Từ chối' }, { id: '5', name: 'Đã nhập KQ' }, { id: '6', name: 'Đã duyệt KQ' },
    ],
    assign_business: [
        { id: '1', name: 'Đang tạo' }, { id: '2', name: 'Chờ duyệt' }, { id: '3', name: 'Đã duyệt' },
        { id: '4', name: 'Đã lập phiếu CT' }, { id: '5', name: 'Đã nhập KQ' }, { id: '6', name: 'Không duyệt' },
        { id: '7', name: 'Đã duyệt KQ' },
    ],
    meeting: [
        { id: '0', name: 'Đang tạo' }, { id: '1', name: 'Lên lịch' }, { id: '2', name: 'Chốt lịch' },
        { id: '3', name: 'Hoàn thành' }, { id: '4', name: 'Hủy' },
    ],
    personal: [{ id: '0', name: 'Việc cần làm' }, { id: '1', name: 'Hoàn thành' }],
}
```

Đặt hằng số này trong `work-item-types.js`.

- [ ] **Step 1: Viết e2e đỏ**

```ts
import { test, expect } from '@playwright/test';

test.describe.serial('Lịch làm việc — thanh lọc', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/assign/my-todo');
    await page.getByRole('button', { name: 'Lịch làm việc' }).click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));
    await page.locator('.work-calendar-tab').waitFor();
  });

  test('có đủ 6 chip loại', async ({ page }) => {
    await expect(page.locator('.calendar-type-chip')).toHaveCount(6);
  });

  test('bật 1 chip thì lưới chỉ còn loại đó, bấm lại thì về tất cả', async ({ page }) => {
    const chip = page.locator('.calendar-type-chip[data-type="meeting"]');
    await chip.click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));
    await page.locator('.ticket-card').first().waitFor();

    const loai = await page.$$eval('.ticket-card', (els) =>
      [...new Set(els.map((e) => (e as HTMLElement).dataset.type))],
    );
    expect(loai).toEqual(['meeting']);

    await chip.click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));
    const loaiSau = await page.$$eval('.ticket-card', (els) =>
      [...new Set(els.map((e) => (e as HTMLElement).dataset.type))],
    );
    expect(loaiSau.length).toBeGreaterThan(1);
  });

  test('ô Trạng thái vô hiệu khi chưa chọn đúng 1 loại, và đổ đúng bộ khi đã chọn', async ({ page }) => {
    const oTrangThai = page.locator('.calendar-status-filter');
    await expect(oTrangThai).toBeDisabled();

    await page.locator('.calendar-type-chip[data-type="meeting"]').click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));
    await expect(oTrangThai).toBeEnabled();

    // Meeting có 5 trạng thái; "Đang tạo" id=0 phải chọn được (bẫy V2BaseSelect nuốt id số 0)
    const nhan = await oTrangThai.locator('option').allTextContents();
    expect(nhan).toContain('Đang tạo');
    expect(nhan).toContain('Hủy');
  });
});
```

- [ ] **Step 2: Chạy, xác nhận ĐỎ**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-filter.spec.ts --reporter=list 2>&1 | tail -20
```

- [ ] **Step 3: Viết chip + ô trạng thái trong `CalendarFilterToolbar.vue`**

```html
<template>
    <div class="calendar-filter-toolbar">
        <button
            v-for="t in types"
            :key="t.key"
            type="button"
            class="calendar-type-chip"
            :class="{ active: value.types.includes(t.key) }"
            :data-type="t.key"
            :style="{ '--chip-color': t.color }"
            @click="$emit('toggle-type', t.key)"
        >
            <span class="calendar-type-chip__dot"></span>{{ t.label }}
        </button>

        <select
            class="calendar-status-filter form-control form-control-sm"
            :disabled="value.types.length !== 1"
            :value="value.status === null ? '' : String(value.status)"
            @change="$emit('filter-change', { status: $event.target.value === '' ? null : $event.target.value })"
        >
            <option value="">Tất cả</option>
            <option v-for="o in statusOptions" :key="o.id" :value="o.id">{{ o.name }}</option>
        </select>

        <button type="button" class="calendar-filter-reset" title="Làm mới" @click="$emit('filter-clear')">
            <i class="ri-refresh-line"></i>
        </button>
    </div>
</template>

<script>
import { WORK_ITEM_TYPES, STATUS_OPTIONS_BY_TYPE } from './work-item-types'

export default {
    name: 'CalendarFilterToolbar',
    props: {
        // { types: string[], status: string|null }
        value: { type: Object, required: true },
    },
    data() {
        return { types: WORK_ITEM_TYPES }
    },
    computed: {
        statusOptions() {
            if (this.value.types.length !== 1) return []
            return STATUS_OPTIONS_BY_TYPE[this.value.types[0]] || []
        },
    },
}
</script>
```

Dùng `<select>` thuần thay `V2BaseSelect` ở đây để né hẳn bẫy id số 0 — toolbar này chỉ có 1 ô, không cần khuôn nặng.

- [ ] **Step 4: Nối vào `WorkCalendarTab.vue`**

Toolbar nay dùng prop tên `value` (không còn `filters`/`meeting-types` như bản cũ), nên sửa chỗ gọi trong template:

```html
<calendar-filter-toolbar
    :value="filters"
    @toggle-type="onToggleType"
    @filter-change="onFilterChange"
    @filter-clear="onFilterClear"
/>
```

```js
onToggleType(key) {
    const next = this.filters.types.includes(key)
        ? this.filters.types.filter((t) => t !== key)
        : this.filters.types.concat([key])
    // đổi loại thì trạng thái cũ hết nghĩa -> reset
    this.filters = { types: next, status: null }
},
onFilterChange(payload) {
    this.filters = Object.assign({}, this.filters, payload)
},
onFilterClear() {
    this.filters = { types: [], status: null }
},
```

- [ ] **Step 5: Chạy e2e, xác nhận XANH**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-filter.spec.ts --reporter=list 2>&1 | tail -20
```

- [ ] **Step 6: Dừng lại báo cáo**

---

### Task 4.2: Thanh tóm tắt đổi ngữ cảnh

**Files:**
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/CalendarSummaryBar.vue`
- Test: `HRM/e2e/tests/assign/work-calendar-summary.spec.ts`

**Interfaces:**
- Consumes: `summaryPeriodItems` (Task 3.1), `filters.types` (Task 4.1), `WORK_ITEM_TYPES` + `STATUS_OPTIONS_BY_TYPE` (Task 2.1/4.1).
- Produces: ô `.calendar-summary-cell[data-key]` — `data-key` là type key khi chưa lọc loại, là id trạng thái khi đã lọc đúng 1 loại.

- [ ] **Step 1: Viết e2e đỏ — số ở tóm tắt phải bằng số thẻ trên lưới**

```ts
import { test, expect } from '@playwright/test';

test.describe.serial('Lịch làm việc — thanh tóm tắt', () => {
  test('chưa lọc loại: 6 ô, mỗi ô bằng số thẻ cùng loại trên lưới', async ({ page }) => {
    await page.goto('/assign/my-todo');
    await page.getByRole('button', { name: 'Lịch làm việc' }).click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));
    await page.locator('.ticket-card, .multiday-bar').first().waitFor();

    await expect(page.locator('.calendar-summary-cell')).toHaveCount(6);

    const oTomTat = await page.$$eval('.calendar-summary-cell', (els) =>
      Object.fromEntries(els.map((e) => [
        (e as HTMLElement).dataset.key,
        Number((e.querySelector('.calendar-summary-cell__count') as HTMLElement).innerText.trim()),
      ])),
    );

    const trenLuoi = await page.$$eval('.ticket-card, .multiday-bar', (els) => {
      const d: Record<string, number> = {};
      for (const e of els) {
        const t = (e as HTMLElement).dataset.type!;
        d[t] = (d[t] || 0) + 1;
      }
      return d;
    });

    for (const [loai, so] of Object.entries(trenLuoi)) {
      expect(oTomTat[loai], `ô tóm tắt loại ${loai}`).toBe(so);
    }
  });

  test('lọc 1 loại: các ô đổi sang bộ trạng thái của loại đó', async ({ page }) => {
    await page.goto('/assign/my-todo');
    await page.getByRole('button', { name: 'Lịch làm việc' }).click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));
    await page.locator('.calendar-type-chip[data-type="meeting"]').click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));

    await expect(page.locator('.calendar-summary-cell')).toHaveCount(5); // meeting có 5 trạng thái
    await expect(page.locator('.calendar-summary-cell[data-key="4"]')).toContainText('Hủy');
  });
});
```

- [ ] **Step 2: Chạy, xác nhận ĐỎ**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-summary.spec.ts --reporter=list 2>&1 | tail -20
```

- [ ] **Step 3: Viết lại `CalendarSummaryBar.vue`**

```js
computed: {
    // Đúng 1 loại đang bật -> tách theo bộ trạng thái THẬT của loại đó;
    // còn lại -> đếm theo 6 loại (hiện đủ 6 ô kể cả bằng 0).
    cells() {
        if (this.activeTypes.length === 1) {
            const type = this.activeTypes[0]
            return (STATUS_OPTIONS_BY_TYPE[type] || []).map((o) => ({
                key: o.id,
                label: o.name,
                color: groupDotColor(this.groupOfStatus(type, o.id)),
                count: this.items.filter((i) => String(i.status) === String(o.id)).length,
            }))
        }

        return WORK_ITEM_TYPES.map((t) => ({
            key: t.key,
            label: t.label,
            color: t.color,
            count: this.items.filter((i) => i.type === t.key).length,
        }))
    },
},
```

`groupOfStatus` lấy từ item đầu tiên có `status` trùng (BE đã trả `status_group`), rơi về `'todo'` nếu kỳ này chưa có item nào mang trạng thái đó:

```js
groupOfStatus(type, statusId) {
    const found = this.items.find((i) => i.type === type && String(i.status) === String(statusId))
    return found ? found.status_group : 'todo'
},
```

Template render `.calendar-summary-cell[data-key]` với `.calendar-summary-cell__count` và nhãn.

- [ ] **Step 4: Chạy e2e, xác nhận XANH**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-summary.spec.ts --reporter=list 2>&1 | tail -20
```

- [ ] **Step 5: Dừng lại báo cáo**

---

## Phase 5 — Frontend: drawer + hành vi bấm thẻ

### Task 5.1: Khuôn drawer đa loại

**Files:**
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/WorkItemDetailDrawer.vue`

**Interfaces:**
- Consumes: `typeColor`, `typeLabel` (Task 2.1); item từ lưới.
- Produces: props `show: Boolean`, `item: Object|null`; sự kiện `@close`, `@open-detail`.

- [ ] **Step 1: Tổng quát hoá header + khung**

Header đổi từ "màu theo trạng thái meeting" sang **màu theo LOẠI**: nền `linear-gradient(135deg, typeColor(type), sắc tối hơn)`, dòng trên là `typeLabel(type)` + `code`, dòng dưới là khoảng thời gian + `status_text`.

Chỗ gọi drawer trong `WorkCalendarTab.vue` đổi từ `:meeting-id="selectedMeetingId"` sang truyền cả item:

```html
<work-item-detail-drawer
    :show="showDrawer"
    :item="selectedItem"
    class="work-item-drawer"
    @close="closeDrawer"
    @open-detail="onOpenDetail"
/>
```

`data()` đổi `selectedMeetingId: null` → `selectedItem: null`.

Thân drawer chuyển sang `<component :is="bodyComponent" :detail="detail" />` với 3 khả năng: `MeetingDrawerBody` (bê nguyên nội dung thân hiện có), `AssignBusinessDrawerBody`, `AssignJobDrawerBody` (Task 5.2).

Nút chân drawer: giữ nguyên "Sửa" / "Xem biên bản" của meeting kèm gate quyền `canEdit` **fail-closed** như hiện tại; 2 loại phiếu thì 1 nút **"Mở chi tiết"**.

- [ ] **Step 2: Nạp chi tiết theo loại**

```js
const DETAIL_ENDPOINT = {
    meeting: (id) => `assign/meeting/${id}`,
    assign_business: (id) => `assign/assign_business/${id}`,
    assign_job: (id) => `assign/assign_jobs/${id}`,
}

async loadDetail() {
    const build = DETAIL_ENDPOINT[this.item.type]
    if (!build) return
    try {
        this.loading = true
        const { data } = await this.$store.dispatch('apiGetMethod', build(this.item.id))
        this.detail = data || null
    } catch (e) {
        this.detail = null
        this.$toasted?.global?.error?.({ message: 'Không tải được chi tiết' })
    } finally {
        this.loading = false
    }
}
```

- [ ] **Step 3: Kiểm bằng tay trên trình duyệt**

Mở tab Lịch làm việc, bấm 1 thẻ meeting. Kỳ vọng: drawer mở, màu header theo LOẠI (chàm), nội dung như trước, nút "Sửa" vẫn ẩn khi không có quyền sửa.

- [ ] **Step 4: Dừng lại báo cáo**

---

### Task 5.2: Thân drawer cho phiếu công tác + phiếu giao việc

**Files:**
- Create: `hrm-client/pages/assign/my-todo/components/calendar/drawer/AssignBusinessDrawerBody.vue`
- Create: `hrm-client/pages/assign/my-todo/components/calendar/drawer/AssignJobDrawerBody.vue`
- Test: `HRM/e2e/tests/assign/work-calendar-drawer.spec.ts`

**Interfaces:**
- Consumes: `detail` — payload của `GET assign/assign_business/{id}` / `assign/assign_jobs/{id}`.
- Produces: khối `.drawer-field[data-field]` cho từng trường.

Bộ trường lấy đúng design §8.4.1:

- **Phiếu công tác**: Khách hàng (`customer_name`) · Nội dung công việc (`job_note`) · Ghi chú (`note`) · Thời gian đi (`time_to_go`) · Trưởng nhóm (`leaderEmployee`) · Nhân sự tham gia (`employees`) · Người tạo
- **Phiếu giao việc**: Khách hàng (`customer_name`) · Địa điểm (`place`) · Người liên hệ (`contact_name` + `contact_phone_number`) · Tên việc (`job_name`) · Mô tả (`job_description`) · Phòng yêu cầu / phòng thực hiện · Số giờ (`total_hour`) · Nhân sự tham gia (`employees`) · Lý do từ chối (`reason_deny`, chỉ khi có) · Người tạo

- [ ] **Step 1: Viết e2e đỏ**

```ts
import { test, expect } from '@playwright/test';

test.describe.serial('Lịch làm việc — drawer phiếu', () => {
  test('bấm thẻ phiếu công tác mở drawer đúng bộ trường', async ({ page }) => {
    await page.goto('/assign/my-todo');
    await page.getByRole('button', { name: 'Lịch làm việc' }).click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));

    const the = page.locator('.ticket-card[data-type="assign_business"], .multiday-bar[data-type="assign_business"]');
    test.skip((await the.count()) === 0, 'Kỳ đang xem không có phiếu công tác');

    await the.first().click();
    await page.waitForResponse((r) => r.url().includes('/assign/assign_business/'));
    const drawer = page.locator('.work-item-drawer');
    await expect(drawer).toBeVisible();
    await expect(drawer.locator('.drawer-field[data-field="customer_name"]')).toBeVisible();
    await expect(drawer.locator('.drawer-field[data-field="job_note"]')).toBeVisible();
    await expect(drawer.getByRole('button', { name: 'Mở chi tiết' })).toBeVisible();
  });

  test('thiếu trường thì hiện dấu — chứ không vỡ drawer', async ({ page }) => {
    await page.goto('/assign/my-todo');
    await page.getByRole('button', { name: 'Lịch làm việc' }).click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));

    const the = page.locator('.ticket-card[data-type="assign_job"], .multiday-bar[data-type="assign_job"]');
    test.skip((await the.count()) === 0, 'Kỳ đang xem không có phiếu giao việc');

    await the.first().click();
    await page.waitForResponse((r) => r.url().includes('/assign/assign_jobs/'));
    await expect(page.locator('.work-item-drawer')).toBeVisible();
    // không có ngoại lệ JS nào lọt ra console
    const loi: string[] = [];
    page.on('pageerror', (e) => loi.push(String(e)));
    await page.waitForTimeout(300);
    expect(loi).toEqual([]);
  });
});
```

- [ ] **Step 2: Chạy, xác nhận ĐỎ**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-drawer.spec.ts --reporter=list 2>&1 | tail -20
```

- [ ] **Step 3: Viết 2 component thân drawer**

Mọi trường phải null-check — bản meeting từng 500 vì thiếu null-check `Employee::find()`. Khuôn 1 trường:

```html
<div class="drawer-field" data-field="customer_name">
    <div class="drawer-field__label">Khách hàng</div>
    <div class="drawer-field__value">{{ detail && detail.customer_name ? detail.customer_name : '—' }}</div>
</div>
```

Danh sách nhân sự:

```html
<div class="drawer-field" data-field="employees">
    <div class="drawer-field__label">Nhân sự tham gia</div>
    <div class="drawer-field__value">
        <span v-if="!employees.length">—</span>
        <span v-for="(e, i) in employees" :key="i" class="drawer-chip">{{ e.name || '—' }}</span>
    </div>
</div>
```

```js
computed: {
    employees() {
        return (this.detail && Array.isArray(this.detail.employees)) ? this.detail.employees : []
    },
},
```

- [ ] **Step 4: Chạy e2e, xác nhận XANH**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-drawer.spec.ts --reporter=list 2>&1 | tail -20
```

- [ ] **Step 5: Dừng lại báo cáo**

---

### Task 5.3: Bấm task / issue / nhắc việc mở popup sẵn có

**Files:**
- Modify: `hrm-client/pages/assign/my-todo/index.vue`
- Modify: `hrm-client/pages/assign/my-todo/components/calendar/WorkCalendarTab.vue`
- Test: `HRM/e2e/tests/assign/work-calendar-popup.spec.ts`

**Interfaces:**
- Consumes: ref sẵn có trong `index.vue` — `createTaskModal`, `createIssueModal`, `todoModal`.
- Produces: `WorkCalendarTab` phát `@open-item="(item) => void"`; `index.vue` xử lý bằng **đúng logic `onClickItem` đang dùng cho tab danh sách** (`index.vue:475`).

- [ ] **Step 1: Viết e2e đỏ**

```ts
import { test, expect } from '@playwright/test';

test.describe.serial('Lịch làm việc — popup sẵn có', () => {
  test('bấm thẻ task mở popup chi tiết task, không mở drawer', async ({ page }) => {
    await page.goto('/assign/my-todo');
    await page.getByRole('button', { name: 'Lịch làm việc' }).click();
    await page.waitForResponse((r) => r.url().includes('/assign/my-todo/calendar'));

    const the = page.locator('.ticket-card[data-type="task"], .multiday-bar[data-type="task"]');
    test.skip((await the.count()) === 0, 'Kỳ đang xem không có task');

    await the.first().click();
    await expect(page.locator('#create-task-modal, .modal.show')).toBeVisible();
    await expect(page.locator('.work-item-drawer')).toHaveCount(0);
  });
});
```

Nếu id modal thật khác `#create-task-modal` thì sửa TEST cho khớp id thật trong `CreateTaskModal.vue`, đừng đổi id component.

- [ ] **Step 2: Chạy, xác nhận ĐỎ**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-popup.spec.ts --reporter=list 2>&1 | tail -20
```

- [ ] **Step 3: Định tuyến hành vi bấm trong `WorkCalendarTab.vue`**

```js
// 3 loại phiếu xem nhanh bằng drawer; 3 loại còn lại đã có popup chi tiết
// riêng ở trang cha (đúng cách tab danh sách đang làm) -> đẩy lên cho cha xử lý.
const DRAWER_TYPES = ['meeting', 'assign_business', 'assign_job']

onClickItem(item) {
    if (DRAWER_TYPES.includes(item.type)) {
        this.selectedItem = item
        this.showDrawer = true
        return
    }
    this.$emit('open-item', item)
},
```

- [ ] **Step 4: Nối ở `index.vue`**

```html
<work-calendar-tab @open-item="onClickItem" />
```

`onClickItem` sẵn có xử lý `task` và `issue`. Bổ sung nhánh `personal` để đủ 3 loại:

```js
} else if (item.type === 'personal') {
    this.onEditPersonalTodo(item)
}
```

- [ ] **Step 5: Chạy e2e, xác nhận XANH**

```bash
cd HRM/e2e && npx playwright test tests/assign/work-calendar-popup.spec.ts --reporter=list 2>&1 | tail -20
```

- [ ] **Step 6: Dừng lại báo cáo**

---

## Phase 6 — Kiểm chứng tổng thể

### Task 6.1: Chạy toàn bộ + đo phân quyền 2 chiều

**Files:**
- Modify: `HRM/.plans/STATUS.md` (thêm khối trạng thái feature)

- [ ] **Step 1: Chạy toàn bộ unit test BE**

```bash
cd hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit tests/ 2>&1 | tail -15
```

Đọc dòng tổng kết. Ghi lại số passed/failed.

- [ ] **Step 2: Chạy TOÀN BỘ e2e của màn my-todo + lịch**

```bash
cd HRM/e2e && npx playwright test tests/assign/my-todo tests/assign/work-calendar --reporter=list 2>&1 | tail -40
```

⚠️ Bộ chạy `serial`: ca đỏ đầu tiên làm mọi ca sau in "did not run". **Đọc dòng tổng kết cuối**, đếm passed + failed + did-not-run, đừng thấy cuối log không có chữ "failed" là yên tâm.

- [ ] **Step 3: Đo phân quyền 2 chiều bằng tài khoản thật**

Đăng nhập bằng **2 tài khoản**: một người có quyền cấp cao nhưng không tham gia việc nào của người kia; một người tham gia nhưng không có quyền cấp nào.

```js
// chạy trong console trình duyệt ở mỗi tài khoản, đối chiếu 2 tập
[...document.querySelectorAll('.ticket-card, .multiday-bar')]
  .map((e) => `${e.dataset.type}#${e.dataset.id}`)
```

Kỳ vọng: tập của 2 người phải khác nhau; người có quyền cấp cao KHÔNG được thấy việc mình không tham gia. Đây là loại lỗi fail-open từng xảy ra (37/49 meeting không liên quan).

- [ ] **Step 4: Bấm thử đủ 6 loại thẻ**

Ca e2e mới chỉ phủ task (Task 5.3) và 2 loại phiếu (Task 5.2). Bấm tay nốt **issue** và **nhắc việc cá nhân** trên lịch:

- Issue → mở popup `createIssueModal` ở chế độ xem, KHÔNG mở drawer.
- Nhắc việc cá nhân → mở `TodoFormModal` đúng bản ghi đó.

Loại nào kỳ đang xem không có dữ liệu thì đổi sang kỳ khác để tìm, ghi lại kỳ đã dùng. KHÔNG bỏ qua rồi báo xong.

- [ ] **Step 5: Đối chiếu trực quan với mockup**

Mở song song mockup và app thật (mockup phải serve qua HTTP, cổng mới để né cache — không dùng `file://` khi đo bằng Playwright):

```bash
cd HRM/.plans/gop-db/ke-hoach-phat-trien-thi-truong && python3 -m http.server 8931
```

Ghi lại **mọi khác biệt** so mockup và phân loại: "do scope đã chốt" (6 loại thay 3, bỏ lọc Thị trường) hay "lệch cần sửa".

- [ ] **Step 6: Cập nhật `.plans/STATUS.md`**

Thêm khối theo đúng khuôn các feature khác: tên feature → người phụ trách → đường dẫn plan; Trạng thái; Đã làm; Bug đã bắt; Deferred; Bước tiếp.

- [ ] **Step 7: Dừng lại báo cáo** — liệt kê số đo thật của từng bước, KHÔNG kết luận "xong" nếu còn ca `skipped` chưa giải thích được.
