# Task 7 brief

## Task 7: Command cron + đăng ký scheduler

**Files:**
- Create: `app/Console/Commands/MasterData/ApplyScheduledRegulationsCommand.php`
- Modify: `app/Console/Kernel.php`
- Test: `Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php` (thêm test command)

**Interfaces:**
- Consumes: `RegulationConfigService::applyDueCongnoVersions`.
- Produces: command `regulation-config:apply-scheduled`; đăng ký `dailyAt('00:00')`.

- [ ] **Step 1: Viết test command (failing)**

```php
    /** @test */
    public function command_applies_due_versions()
    {
        $companyId = $this->makeCompanyWithCongno([
            'limit_export_debt_employee' => 200000000, 'adjust_odd_balance' => 50000,
            'overdue_date_max_customer' => 30, 'overdue_date_max_agency' => 45,
            'overdue_date_max_service' => 60, 'warning_due_date' => 7, 'interest_rate' => 1.5,
        ]);
        $svc = app(\Modules\MasterData\Services\RegulationConfigService::class);
        $base = $svc->getCurrentCongnoValues($companyId);
        $v = $svc->createCongnoVersion($companyId, now()->addYear()->toDateString(),
            array_merge($base, ['interest_rate' => 1.9]), 'future', 1);
        $v->effective_date = now()->toDateString();   // kéo về hôm nay, vẫn pending
        $v->saveQuietly();

        $this->artisan('regulation-config:apply-scheduled')->assertExitCode(0);
        $this->assertSame(1.9, (float) \App\Models\Company::find($companyId)->interest_rate);
        $this->assertSame('applied', $v->fresh()->status);
    }
```

- [ ] **Step 2: Chạy test → fail**

Run: `php artisan test --filter=RegulationCongnoVersioningTest::command_applies_due_versions`
Expected: FAIL — command chưa tồn tại.

- [ ] **Step 3: Viết command**

```php
<?php

namespace App\Console\Commands\MasterData;

use Illuminate\Console\Command;
use Modules\MasterData\Services\RegulationConfigService;

class ApplyScheduledRegulationsCommand extends Command
{
    protected $signature = 'regulation-config:apply-scheduled';
    protected $description = 'Áp dụng các phiên bản quy chế/cấu hình đã hẹn tới hạn (effective_date <= hôm nay)';

    public function handle(RegulationConfigService $service): int
    {
        $applied = $service->applyDueCongnoVersions();
        $this->info("Đã áp dụng {$applied} phiên bản Công nợ tới hạn.");
        return 0;
    }
}
```

- [ ] **Step 4: Đăng ký scheduler trong `app/Console/Kernel.php`**

Thêm vào cuối method `schedule(Schedule $schedule)` (theo đúng style các dòng có sẵn):

```php
        $schedule->command('regulation-config:apply-scheduled')
            ->dailyAt('00:00')
            ->timezone('Asia/Ho_Chi_Minh')
            ->withoutOverlapping();
```

- [ ] **Step 5: Verify command đăng ký + chạy**

Run: `php artisan list | grep regulation-config` (thấy command) rồi `php artisan test --filter=RegulationCongnoVersioningTest::command_applies_due_versions`
Expected: command hiện; test PASS.

- [ ] **Step 6: Commit**

```bash
git add app/Console/Commands/MasterData/ApplyScheduledRegulationsCommand.php app/Console/Kernel.php Modules/MasterData/Tests/Feature/RegulationCongnoVersioningTest.php
git commit -m "feat(masterdata): apply-scheduled cron command + daily schedule"
```

---

