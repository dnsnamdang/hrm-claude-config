<?php

namespace App\Console\Commands\Assign;

use Carbon\Carbon;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;
use Modules\Assign\Entities\Meeting\Meeting;
use Modules\Assign\Entities\Meeting\MeetingInvestmentDemand;
use Modules\Assign\Entities\MeetingType;

/**
 * Sinh dữ liệu DEMO cho màn "Báo cáo kết quả chăm sóc khách hàng tiềm năng" (chạy được trên VPS).
 *
 * ⚠️ 3 ràng buộc an toàn — đọc trước khi sửa:
 *
 * 1. CHỈ ĐỌC dữ liệu khách hàng của ERP. Lệnh này không bao giờ ghi sang kết nối `mysql2`.
 * 2. Mọi bản ghi sinh ra mang tiền tố mã `DEMO-CSKH-`. Đó là thứ DUY NHẤT `--clean` bám vào để
 *    xoá, nhờ vậy không thể chạm tới meeting hay dự án thật. Đổi tiền tố thì `--clean` của bản cũ
 *    sẽ không dọn được dữ liệu đã sinh trước đó.
 * 3. Hỏi xác nhận kèm tên DB đang trỏ tới trước khi ghi. Chạy trong script thì thêm `--force`.
 *
 * Idempotent: upsert theo mã meeting nên chạy lại nhiều lần không nhân đôi dữ liệu.
 */
class SeedCareReportDemoCommand extends Command
{
    /** Tiền tố nhận dạng dữ liệu demo — xem ràng buộc số 2 ở docblock */
    private const PREFIX = 'DEMO-CSKH-';

    /** Số tỉnh/TP lấy khách hàng — mỗi tỉnh là một dòng cha của phần "Theo thị trường" */
    private const PROVINCE_LIMIT = 15;

    /** Số khách hàng mỗi tỉnh, mỗi người một phường/xã khác nhau để mở được cấp 2 của thị trường */
    private const CUSTOMERS_PER_PROVINCE = 3;

    /**
     * 22 nhóm ngành hệ thống (mã `NN.0001`–`NN.0022`, GIỐNG NHAU ở mọi môi trường) xếp vào lĩnh vực.
     *
     * Lý do phải có bảng này: migration tạo lĩnh vực "Khác" rồi gắn TOÀN BỘ nhóm ngành cũ vào đó,
     * nên môi trường nào cũng dồn 22 nhóm ngành về đúng MỘT lĩnh vực (VPS là "Khác", local là
     * "Công nghiệp") -> phần "Theo lĩnh vực" của báo cáo chỉ ra 1 dòng, không soi được cây.
     *
     * ⚠️ Khớp lĩnh vực theo TÊN đã chuẩn hoá, KHÔNG theo mã: mã lĩnh vực mỗi môi trường một kiểu
     * (`LVKDNB.IDUS` ở local vs `LVKDNB.0001` trên VPS). Mã nhóm ngành thì ổn định nên dùng được.
     */
    private const SCOPE_FIELD_MAP = [
        'Công nghiệp'           => ['NN.0001', 'NN.0004', 'NN.0005', 'NN.0018', 'NN.0019', 'NN.0020'],
        'Môi trường'            => ['NN.0013', 'NN.0014', 'NN.0015', 'NN.0016'],
        'Ngành ô tô'            => ['NN.0009', 'NN.0011', 'NN.0012'],
        'Giải pháp quản trị số' => ['NN.0003', 'NN.0008', 'NN.0021', 'NN.0022'],
        'Tiện ích công cộng'    => ['NN.0006', 'NN.0017'],
        'Năng lượng và hạ tầng' => ['NN.0007', 'NN.0010'],
        'Giáo dục đào tạo'      => ['NN.0002'],
    ];

    protected $signature = 'assign:seed-care-demo
        {--months=6 : Số tháng gần nhất để rải ngày họp}
        {--demands=120 : Số nhu cầu muốn sinh (xấp xỉ)}
        {--clean : Xoá sạch dữ liệu demo rồi dừng}
        {--dry-run : Chỉ in dự kiến, không ghi gì}
        {--no-map-scopes : Bỏ qua bước gán nhóm ngành hệ thống vào lĩnh vực}
        {--force : Bỏ qua bước hỏi xác nhận}';

    protected $description = 'Sinh dữ liệu demo cho báo cáo kết quả chăm sóc khách hàng tiềm năng';

    public function handle(): int
    {
        $database = DB::connection()->getDatabaseName();

        if ($this->option('clean')) {
            return $this->clean($database);
        }

        $months = max(1, (int) $this->option('months'));
        $target = max(1, (int) $this->option('demands'));
        $dryRun = (bool) $this->option('dry-run');

        $mapPlan = $this->option('no-map-scopes') ? null : $this->planScopeFieldMapping();

        $source = $this->collectSource($mapPlan);
        if ($source === null) {
            return self::FAILURE;
        }

        // Mỗi meeting sinh 2-4 nhu cầu -> lấy trung bình 3 để suy ra số meeting cần
        $meetingCount = max(1, (int) ceil($target / 3));

        $this->line('');
        $this->info('Dữ liệu demo báo cáo CSKH tiềm năng');
        $this->table(['Mục', 'Giá trị'], [
            ['Cơ sở dữ liệu', $database],
            ['Số tháng rải ngày họp', $months],
            ['Số meeting sẽ tạo', $meetingCount],
            ['Số nhu cầu (xấp xỉ)', $target],
            ['Khách hàng dùng lại (chỉ đọc)', $source['customers']->count()],
            ['Thị trường (tỉnh/TP) phủ được', $source['customers']->pluck('province_id')->unique()->count()],
            ['Người chủ trì', $source['hosts']->count()],
            ['Nhóm ngành phủ được', $source['scopes']->count()],
            ['Nhóm ngành sẽ gán lại lĩnh vực', $mapPlan['count'] ?? 0],
            ['Tiền tố mã bản ghi demo', self::PREFIX],
        ]);

        if ($mapPlan !== null && $mapPlan['note'] !== null) {
            $this->comment($mapPlan['note']);
        }

        if ($dryRun) {
            $this->comment('--dry-run: không ghi gì vào cơ sở dữ liệu.');
            return self::SUCCESS;
        }

        if (!$this->option('force')
            && !$this->confirm(sprintf('Ghi dữ liệu demo vào cơ sở dữ liệu "%s"?', $database), false)) {
            $this->comment('Đã huỷ, không ghi gì.');
            return self::SUCCESS;
        }

        if ($mapPlan !== null && $mapPlan['count'] > 0) {
            $this->applyScopeFieldMapping($mapPlan, $source['hosts']->first());
            // Đọc lại nhóm ngành: bản trong $source được lấy TRƯỚC khi gán nên còn lĩnh vực cũ,
            // dùng tiếp thì nhu cầu demo vẫn ghi tên lĩnh vực "Khác" vào cột denormalize.
            $source['scopes'] = $this->fetchScopes();
        }

        $stats = $this->seed($months, $meetingCount, $source);
        $this->report($stats);

        return self::SUCCESS;
    }

    // ------------------------------------------------------------------ nguồn

    /**
     * Gom nguồn dữ liệu có sẵn. Trả về null (kèm thông báo) nếu môi trường thiếu thứ gì đó,
     * thay vì sinh ra bộ dữ liệu méo mó khiến người xem tưởng báo cáo tính sai.
     */
    private function collectSource(?array $mapPlan): ?array
    {
        $typeId = DB::table('meeting_types')->where('code', MeetingType::CODE_PRODUCT_INTRO)->value('id');
        if (!$typeId) {
            $this->error('Thiếu loại meeting hệ thống "Họp tìm hiểu & Giới thiệu sản phẩm".');
            $this->line('Khắc phục — chạy seeder loại meeting hệ thống rồi chạy lại lệnh này:');
            $this->line('  php artisan db:seed --class="Modules\\Assign\\Database\\Seeders\\SystemMeetingTypesSeeder" --force');
            return null;
        }

        // Chỉ lấy nhóm ngành CÓ lĩnh vực cha, nếu không phần "Theo lĩnh vực" gom hết vào
        // dòng "Chưa xác định lĩnh vực" và bản demo trông như báo cáo hỏng.
        // Bước gán lĩnh vực (nếu chạy) sẽ bổ sung thêm nhóm ngành cho nguồn này, nên đếm cả nó —
        // ngược lại môi trường mới toanh (nhóm ngành chưa gắn lĩnh vực nào) sẽ dừng ngay tại đây
        // dù chính lệnh này biết cách vá.
        $scopes = $this->fetchScopes();
        if (max($scopes->count(), $mapPlan['count'] ?? 0) < 3) {
            $this->error('Cần ít nhất 3 nhóm ngành đang hoạt động có gắn lĩnh vực Công ty kinh doanh.');
            $this->line('Khắc phục: chạy "php artisan migrate" (migration tự tạo lĩnh vực "Khác" và');
            $this->line('gắn cho các nhóm ngành cũ), hoặc vào Danh mục ▸ Nhóm ngành gán lĩnh vực cho từng nhóm.');
            return null;
        }

        // Người chủ trì trải nhiều phòng ban -> phần "Theo phòng ban / Nhân viên" nhiều dòng.
        // Cấp tổ chức nằm ở `employee_infos`, KHÔNG phải `employees`.
        $hosts = DB::table('employees')
            ->join('employee_infos', 'employee_infos.id', '=', 'employees.employee_info_id')
            ->join('departments', 'departments.id', '=', 'employee_infos.department_id')
            ->where('employee_infos.status', 1)
            ->orderBy('employee_infos.department_id')
            ->orderBy('employees.id')
            ->get([
                'employees.id',
                'employee_infos.company_id',
                'employee_infos.department_id',
                'employee_infos.part_id',
            ])
            ->groupBy('department_id')
            // 1 người mỗi phòng ban, lấy tối đa 12 phòng -> bảng có nhiều dòng cha mà không loãng
            ->map(fn($group) => $group->first())
            ->take(12)
            ->values();
        if ($hosts->isEmpty()) {
            $this->error('Không tìm thấy nhân viên đang hoạt động có phòng ban để làm người chủ trì.');
            return null;
        }

        // CHỈ ĐỌC bảng khách hàng của ERP. Lấy mỗi tỉnh vài khách -> phần "Theo thị trường"
        // có nhiều dòng cha thay vì dồn hết vào một tỉnh.
        //
        // ⚠️ Phải LẤY DANH SÁCH TỈNH TRƯỚC rồi mới truy từng tỉnh. Cách gộp một lượt
        // `orderBy(province_id)->limit(N)` rồi nhóm lại chỉ nạp trọn vẹn vài tỉnh đầu tiên (ERP có
        // hơn 43.000 khách hàng), kết quả ra đúng 3 khách của MỘT tỉnh — đã dính thật khi chạy thử.
        $customerTable = env('DB_DATABASE_SECOND') . '.customers';
        $provinceIds = DB::connection('mysql2')
            ->table($customerTable)
            ->whereNotNull('province_id')->where('province_id', '>', 0)
            ->whereNotNull('ward_id')->where('ward_id', '>', 0)
            ->distinct()
            ->orderBy('province_id')
            ->limit(self::PROVINCE_LIMIT)
            ->pluck('province_id');

        // Mỗi tỉnh lấy vài khách MỖI NGƯỜI MỘT PHƯỜNG/XÃ. Lấy thẳng `limit(3)` theo id thì cả 3
        // thường trùng phường/xã -> mở cấp 2 "Tỉnh ▸ Phường/xã" chỉ ra đúng một dòng con.
        $byProvince = [];
        foreach ($provinceIds as $provinceId) {
            $rows = DB::connection('mysql2')
                ->table($customerTable)
                ->where('province_id', $provinceId)
                ->whereNotNull('ward_id')->where('ward_id', '>', 0)
                ->orderBy('id')
                ->limit(self::CUSTOMERS_PER_PROVINCE * 40)
                ->get(['id', 'province_id', 'ward_id'])
                ->unique('ward_id')
                ->take(self::CUSTOMERS_PER_PROVINCE)
                ->values();

            if ($rows->isNotEmpty()) {
                $byProvince[] = $rows;
            }
        }

        // ⚠️ Xếp XEN KẼ theo tỉnh. Meeting chọn khách bằng `$customers[$i % count]`, nên nếu để
        // nguyên thứ tự gom-theo-tỉnh thì 40 meeting chỉ tiêu thụ 40 khách ĐẦU danh sách = 13 tỉnh
        // đầu tiên, các tỉnh cuối không có meeting nào và biến mất khỏi phần "Theo thị trường".
        $customers = collect();
        for ($slot = 0; $slot < self::CUSTOMERS_PER_PROVINCE; $slot++) {
            foreach ($byProvince as $rows) {
                if (isset($rows[$slot])) {
                    $customers->push($rows[$slot]);
                }
            }
        }
        $customers = $customers->values();
        if ($customers->count() < 3) {
            $this->error('Cơ sở dữ liệu ERP không đủ khách hàng có tỉnh và phường/xã.');
            return null;
        }

        return compact('typeId', 'scopes', 'hosts', 'customers');
    }

    // ------------------------------------------------------------------ sinh

    private function seed(int $months, int $meetingCount, array $source): array
    {
        $now = now();
        $periodStart = $now->copy()->startOfMonth();
        $scopes = $source['scopes'];
        $hosts = $source['hosts'];
        $customers = $source['customers'];

        $stats = [
            'meetings' => 0, 'demands' => 0, 'projects' => 0,
            'open' => 0, 'won' => 0, 'lost' => 0,
            'carried' => 0, 'arisen' => 0, 'won_in_period' => 0, 'lost_in_period' => 0,
        ];

        $scopeCursor = 0;

        for ($i = 0; $i < $meetingCount; $i++) {
            // Rải đều ngày họp trong `months` tháng gần nhất, tháng hiện tại nằm ở cuối dải
            $monthOffset = $months - 1 - intdiv($i * $months, $meetingCount);
            $meetAt = $periodStart->copy()->subMonths($monthOffset)->addDays(2 + ($i * 7) % 24);
            if ($meetAt->gt($now)) {
                $meetAt = $now->copy()->subDay();
            }

            $host = $hosts[$i % $hosts->count()];
            $customer = $customers[$i % $customers->count()];
            $code = self::PREFIX . str_pad((string) ($i + 1), 3, '0', STR_PAD_LEFT);

            $meetingId = $this->upsertMeeting($code, $meetAt, (int) $customer->id, $source['typeId'], $host, $now);
            $stats['meetings']++;

            $perMeeting = 2 + ($i % 3);   // 2, 3 hoặc 4 nhu cầu
            $usedScopes = [];

            for ($j = 0; $j < $perMeeting; $j++) {
                // ⚠️ Con trỏ CHẠY LIÊN TỤC, không tính lại từ `$i`. Bản cũ dùng `($i * 4 + $j)` mà
                // mỗi meeting chỉ tiêu thụ 2-4 giá trị -> chỉ chạm 18/24 nhóm ngành, 6 nhóm không
                // bao giờ tới lượt và lĩnh vực cha của chúng hiện thiếu nhóm ngành trên báo cáo.
                $scope = $scopes[$scopeCursor++ % $scopes->count()];
                if (in_array($scope->id, $usedScopes, true)) {
                    continue;   // trùng nhóm ngành trong cùng meeting là vi phạm ràng buộc duy nhất
                }
                $usedScopes[] = $scope->id;

                [$status, $closedAt] = $this->pickLifecycle($i * 4 + $j, $meetAt, $periodStart, $now);
                $amount = 200000000 + ((($i * 7 + $j * 3) % 25) * 200000000);   // 200 triệu → 5 tỷ
                $expectedStart = $meetAt->copy()->addMonths(3 + ($j % 4))->toDateString();

                // Nhu cầu "Không tiếp tục" phải hết hạn ĐÚNG vào ngày đóng, nếu không cron
                // `assign:close-expired-customer-demands` chạy sau sẽ ghi đè ngày đóng khác đi.
                if ($status === MeetingInvestmentDemand::KHONG_TIEP_TUC) {
                    $expectedStart = $closedAt;
                }

                $projectId = null;
                if ($status === MeetingInvestmentDemand::DA_LAP_DU_AN) {
                    $projectId = $this->upsertProject($code . '-' . $scope->id, $customer, $host, $now);
                    $stats['projects']++;
                }

                $this->upsertDemand($meetingId, $scope, $amount, $expectedStart, $status, $closedAt, $projectId, $host, $now);
                $stats['demands']++;

                $key = [
                    MeetingInvestmentDemand::DANG_THEO_DOI => 'open',
                    MeetingInvestmentDemand::DA_LAP_DU_AN => 'won',
                    MeetingInvestmentDemand::KHONG_TIEP_TUC => 'lost',
                ][$status];
                $stats[$key]++;

                if ($meetAt->lt($periodStart) && ($closedAt === null || $closedAt >= $periodStart->toDateString())) {
                    $stats['carried']++;
                } elseif ($meetAt->gte($periodStart)) {
                    $stats['arisen']++;
                }
                if ($closedAt !== null && $closedAt >= $periodStart->toDateString()) {
                    $stats[$status === MeetingInvestmentDemand::DA_LAP_DU_AN
                        ? 'won_in_period' : 'lost_in_period']++;
                }
            }

            $this->syncMeetingScopes($meetingId, $scopes->whereIn('id', $usedScopes), $host, $now);
        }

        return $stats;
    }

    /**
     * Chọn vòng đời cho một nhu cầu: ~50% Đang theo dõi, ~30% Đã lập dự án TKT, ~20% Không tiếp tục.
     *
     * ⚠️ Trạng thái và MỐC ĐÓNG phải quyết định ĐỘC LẬP với nhau. Bản đầu tiên dùng chính chỉ số
     * nhóm để vừa chọn trạng thái vừa quyết định có kéo ngày đóng về kỳ hiện tại hay không —
     * hậu quả là toàn bộ nhu cầu "Không tiếp tục" dồn vào tháng này, ô KPI "Thất bại / tổng nhu cầu
     * đóng" của bản demo vọt lên 64,9% trông như hệ thống tính sai.
     *
     * Nay: nhóm 0-4 đang theo dõi · 5-7 đã lập dự án · 8-9 không tiếp tục; còn việc kéo ngày đóng
     * về kỳ hiện tại xét theo một chỉ số KHÁC, áp dụng cho cả hai loại như nhau, để kỳ Tháng này,
     * Quý này và Năm nay đều có số khác 0 mà tỷ lệ vẫn giữ đúng 30/20.
     */
    private function pickLifecycle(int $seed, Carbon $meetAt, Carbon $periodStart, Carbon $now): array
    {
        $bucket = $seed % 10;

        if ($bucket < 5) {
            return [MeetingInvestmentDemand::DANG_THEO_DOI, null];
        }

        $status = $bucket < 8
            ? MeetingInvestmentDemand::DA_LAP_DU_AN
            : MeetingInvestmentDemand::KHONG_TIEP_TUC;

        $closedAt = $meetAt->copy()->addDays(20 + ($seed % 45));
        if ($closedAt->gt($now)) {
            $closedAt = $now->copy()->subDays($seed % 5);
        }
        // Khoảng 1/3 số nhu cầu bị đóng được kéo về kỳ hiện tại, KHÔNG phân biệt trạng thái
        if ($seed % 3 === 0 && $closedAt->lt($periodStart)) {
            $closedAt = $periodStart->copy()->addDays($seed % max(1, $now->day));
        }

        return [$status, $closedAt->toDateString()];
    }

    private function upsertMeeting(string $code, Carbon $meetAt, int $customerId, int $typeId, $host, Carbon $now): int
    {
        $row = [
            'name' => 'Demo CSKH tiềm năng — ' . $code,
            'meeting_type_id' => $typeId,
            'is_customer_meeting' => 1,
            'mode_id' => 1,
            'location' => 'Dữ liệu demo',
            'status' => Meeting::HOAN_THANH,
            'start_date' => $meetAt->copy()->setTime(9, 0, 0),
            'end_date' => $meetAt->copy()->setTime(11, 0, 0),
            'host_employee_id' => $host->id,
            'customer_id' => $customerId,
            'has_investment_demand' => 1,
            'has_maintenance_demand' => $customerId % 2,
            'conclusion' => 'Biên bản demo phục vụ nghiệm thu báo cáo.',
            'company_id' => $host->company_id,
            'department_id' => $host->department_id,
            'part_id' => $host->part_id,
            'updated_by' => $host->id,
            'updated_at' => $now,
        ];

        $existing = DB::table('meetings')->where('code', $code)->first();
        if ($existing) {
            DB::table('meetings')->where('id', $existing->id)->update($row);
            return (int) $existing->id;
        }

        $row['code'] = $code;
        $row['created_by'] = $host->id;
        $row['created_at'] = $meetAt->copy()->subDays(5);

        return (int) DB::table('meetings')->insertGetId($row);
    }

    private function upsertDemand(int $meetingId, $scope, float $amount, string $expectedStart,
                                  int $status, ?string $closedAt, ?int $projectId, $host, Carbon $now): void
    {
        $row = [
            'internal_business_scope_id' => $scope->internal_business_scope_id,
            'internal_business_scope_name' => $this->internalScopeName($scope->internal_business_scope_id),
            'scope_name' => $scope->name,
            'expected_amount' => $amount,
            'expected_start_date' => $expectedStart,
            'status' => $status,
            'closed_at' => $closedAt,
            'prospective_project_id' => $projectId,
            'position' => 0,
            'updated_by' => $host->id,
            'updated_at' => $now,
        ];

        $existing = DB::table('meeting_investment_demands')
            ->where('meeting_id', $meetingId)->where('scope_id', $scope->id)->first();

        if ($existing) {
            DB::table('meeting_investment_demands')->where('id', $existing->id)->update($row);
            return;
        }

        $row['meeting_id'] = $meetingId;
        $row['scope_id'] = $scope->id;
        $row['created_by'] = $host->id;
        $row['created_at'] = $now;
        DB::table('meeting_investment_demands')->insert($row);
    }

    /** Dự án tiền khả thi demo để cột "Dự án TKT" trong cửa sổ chi tiết có dữ liệu */
    private function upsertProject(string $code, $customer, $host, Carbon $now): int
    {
        $row = [
            'name' => 'Dự án demo từ nhu cầu ' . $code,
            'status' => 1,
            'customer_id' => $customer->id,
            'main_sale_employee_id' => $host->id,
            'main_sale_department_id' => $host->department_id,
            'company_id' => $host->company_id,
            'department_id' => $host->department_id,
            'part_id' => $host->part_id,
            'updated_by' => $host->id,
            'updated_at' => $now,
        ];

        $existing = DB::table('prospective_projects')->where('code', $code)->first();
        if ($existing) {
            DB::table('prospective_projects')->where('id', $existing->id)->update($row);
            return (int) $existing->id;
        }

        $row['code'] = $code;
        $row['created_by'] = $host->id;
        $row['created_at'] = $now;

        return (int) DB::table('prospective_projects')->insertGetId($row);
    }

    /** Lĩnh vực cha của biên bản — giữ biên bản hợp lệ nếu ai đó mở màn Sửa meeting demo */
    private function syncMeetingScopes(int $meetingId, $scopes, $host, Carbon $now): void
    {
        DB::table('meeting_investment_scopes')->where('meeting_id', $meetingId)->delete();

        $internalIds = collect($scopes)->pluck('internal_business_scope_id')->filter()->unique()->values();
        foreach ($internalIds as $position => $internalId) {
            DB::table('meeting_investment_scopes')->insert([
                'meeting_id' => $meetingId,
                'internal_business_scope_id' => $internalId,
                'internal_business_scope_name' => $this->internalScopeName($internalId),
                'position' => $position,
                'created_by' => $host->id,
                'updated_by' => $host->id,
                'created_at' => $now,
                'updated_at' => $now,
            ]);
        }
    }

    /** Memo trong một lần chạy: cùng một lĩnh vực bị hỏi lại hàng trăm lần */
    private function internalScopeName($internalId): string
    {
        static $cache = [];

        if (!$internalId) {
            return '';
        }
        if (!array_key_exists($internalId, $cache)) {
            $cache[$internalId] = (string) DB::table('internal_business_scopes')
                ->where('id', $internalId)->value('name');
        }

        return $cache[$internalId];
    }

    /**
     * Nhóm ngành đang hoạt động và ĐÃ có lĩnh vực cha — nguồn để rải nhu cầu demo.
     *
     * Ưu tiên đúng bộ 22 nhóm ngành HỆ THỐNG (`NN.0001`–`NN.0022`). Lấy hết mọi nhóm ngành trong
     * DB thì demo mỗi môi trường một khác: local còn lẫn nhóm ngành rác của e2e, môi trường khách
     * có thể đã tự thêm nhóm ngành riêng. Chỉ khi môi trường thiếu bộ hệ thống mới lấy tất.
     */
    private function fetchScopes()
    {
        $base = DB::table('scopes')
            ->where('status', 1)
            ->whereNotNull('internal_business_scope_id');

        $codes = array_merge(...array_values(self::SCOPE_FIELD_MAP));
        $system = (clone $base)->whereIn('code', $codes)
            ->orderBy('id')->get(['id', 'name', 'internal_business_scope_id']);

        return $system->count() >= 3
            ? $system
            : $base->orderBy('id')->get(['id', 'name', 'internal_business_scope_id']);
    }

    // ------------------------------------------------------ gán nhóm ngành vào lĩnh vực

    /**
     * Dựng (chưa ghi) kế hoạch gán 22 nhóm ngành hệ thống vào lĩnh vực theo `SCOPE_FIELD_MAP`.
     *
     * ⚠️ CHỐT CHẶN: chỉ gán khi 22 nhóm ngành đó đang dồn về ĐÚNG MỘT lĩnh vực (hoặc chưa có
     * lĩnh vực nào) — dấu hiệu chưa ai phân loại. Nếu chúng đã nằm ở từ 2 lĩnh vực trở lên nghĩa là
     * khách đã tự phân loại, lệnh demo KHÔNG được phép ghi đè danh mục thật của họ.
     *
     * @return array{count:int, note:?string, assignments:array<string, array<int>>}
     */
    private function planScopeFieldMapping(): array
    {
        $codes = array_merge(...array_values(self::SCOPE_FIELD_MAP));
        $scopes = DB::table('scopes')
            ->whereIn('code', $codes)
            ->get(['id', 'code', 'name', 'internal_business_scope_id'])
            ->keyBy('code');

        $empty = ['count' => 0, 'note' => null, 'assignments' => []];

        if ($scopes->isEmpty()) {
            return ['count' => 0, 'assignments' => [],
                'note' => 'Không thấy nhóm ngành hệ thống NN.0001–NN.0022, bỏ qua bước gán lĩnh vực.'];
        }

        $currentFields = $scopes->pluck('internal_business_scope_id')->filter()->unique();
        if ($currentFields->count() > 1) {
            return ['count' => 0, 'assignments' => [],
                'note' => sprintf(
                    'Nhóm ngành hệ thống đã được phân vào %d lĩnh vực — bỏ qua bước gán để không đè danh mục thật.',
                    $currentFields->count()
                )];
        }

        // Khớp lĩnh vực theo tên chuẩn hoá; cái nào chưa có sẽ được tạo ở bước ghi (id = null).
        $existing = DB::table('internal_business_scopes')
            ->get(['id', 'name'])
            ->keyBy(fn($field) => $this->normalizeName($field->name));

        $assignments = [];
        $count = 0;
        foreach (self::SCOPE_FIELD_MAP as $fieldName => $scopeCodes) {
            $fieldId = optional($existing->get($this->normalizeName($fieldName)))->id;

            $scopeIds = [];
            foreach ($scopeCodes as $code) {
                $scope = $scopes->get($code);
                if (!$scope) {
                    continue;   // môi trường thiếu nhóm ngành này -> bỏ qua, không dựng dữ liệu ma
                }
                if ($fieldId !== null && (int) $scope->internal_business_scope_id === (int) $fieldId) {
                    continue;   // đã đúng lĩnh vực rồi, không đếm là thay đổi
                }
                $scopeIds[] = (int) $scope->id;
            }

            if ($scopeIds) {
                $assignments[$fieldName] = $scopeIds;
                $count += count($scopeIds);
            }
        }

        return $count === 0 ? $empty : ['count' => $count, 'note' => null, 'assignments' => $assignments];
    }

    /** Ghi kế hoạch của `planScopeFieldMapping()`: tạo lĩnh vực còn thiếu rồi trỏ nhóm ngành vào. */
    private function applyScopeFieldMapping(array $plan, $host): void
    {
        $now = now();

        foreach ($plan['assignments'] as $fieldName => $scopeIds) {
            $fieldId = $this->resolveFieldId($fieldName, $host, $now);

            DB::table('scopes')->whereIn('id', $scopeIds)->update([
                'internal_business_scope_id' => $fieldId,
                'updated_by' => $host->id,
                'updated_at' => $now,
            ]);

            $this->line(sprintf('  Lĩnh vực "%s" ← %d nhóm ngành', $fieldName, count($scopeIds)));
        }

        $this->info(sprintf('Đã gán %d nhóm ngành vào lĩnh vực.', $plan['count']));
    }

    /** Lấy id lĩnh vực theo tên chuẩn hoá, tạo mới nếu môi trường chưa có */
    private function resolveFieldId(string $fieldName, $host, Carbon $now): int
    {
        $normalized = $this->normalizeName($fieldName);

        $existing = DB::table('internal_business_scopes')
            ->get(['id', 'name'])
            ->first(fn($field) => $this->normalizeName($field->name) === $normalized);
        if ($existing) {
            return (int) $existing->id;
        }

        // `code` là UNIQUE varchar(50) -> dựng từ tên rồi cắt, đụng thì thêm số đuôi.
        $base = 'LVKDNB.' . substr(strtoupper(preg_replace('/[^A-Z0-9]/i', '', Str::ascii($fieldName))), 0, 40);
        $code = $base;
        for ($i = 2; DB::table('internal_business_scopes')->where('code', $code)->exists(); $i++) {
            $code = substr($base, 0, 46) . $i;
        }

        return (int) DB::table('internal_business_scopes')->insertGetId([
            'code' => $code,
            'name' => $fieldName,
            'status' => 1,
            'created_by' => $host->id,
            'updated_by' => $host->id,
            'created_at' => $now,
            'updated_at' => $now,
        ]);
    }

    /** Bỏ dấu + bỏ mọi ký tự không phải chữ/số -> "Giáo dục & Đào tạo" ≡ "Giáo dục đào tạo" */
    private function normalizeName(?string $name): string
    {
        return strtolower(preg_replace('/[^a-z0-9]/i', '', Str::ascii((string) $name)));
    }

    // ------------------------------------------------------------------ dọn

    private function clean(string $database): int
    {
        $meetingIds = DB::table('meetings')->where('code', 'like', self::PREFIX . '%')->pluck('id');
        $projectCount = DB::table('prospective_projects')->where('code', 'like', self::PREFIX . '%')->count();

        $this->line('');
        $this->table(['Mục', 'Giá trị'], [
            ['Cơ sở dữ liệu', $database],
            ['Meeting demo sẽ xoá', $meetingIds->count()],
            ['Dự án tiền khả thi demo sẽ xoá', $projectCount],
        ]);

        if ($meetingIds->isEmpty() && $projectCount === 0) {
            $this->comment('Không có dữ liệu demo nào để xoá.');
            return self::SUCCESS;
        }

        if ($this->option('dry-run')) {
            $this->comment('--dry-run: không xoá gì.');
            return self::SUCCESS;
        }

        if (!$this->option('force')
            && !$this->confirm(sprintf('Xoá toàn bộ dữ liệu demo trong "%s"?', $database), false)) {
            $this->comment('Đã huỷ, không xoá gì.');
            return self::SUCCESS;
        }

        // Gỡ liên kết trước rồi mới xoá dự án, tránh để lại nhu cầu trỏ vào dự án không còn tồn tại
        DB::table('meeting_investment_demands')->whereIn('meeting_id', $meetingIds)->delete();
        DB::table('meeting_investment_scopes')->whereIn('meeting_id', $meetingIds)->delete();
        DB::table('prospective_projects')->where('code', 'like', self::PREFIX . '%')->delete();
        DB::table('meetings')->whereIn('id', $meetingIds)->delete();

        $this->info('Đã xoá sạch dữ liệu demo.');
        $this->comment('Lưu ý: KHÔNG hoàn tác việc gán nhóm ngành vào lĩnh vực — đó là sửa danh mục');
        $this->comment('cho đúng, không phải dữ liệu demo.');

        return self::SUCCESS;
    }

    // ------------------------------------------------------------------ báo cáo

    private function report(array $stats): void
    {
        $periodStart = now()->startOfMonth();

        $this->line('');
        $this->info('Đã sinh xong dữ liệu demo');
        $this->table(['Chỉ tiêu', 'Số nhu cầu'], [
            ['Meeting đã tạo', $stats['meetings']],
            ['Tổng nhu cầu đã tạo', $stats['demands']],
            ['— Đang theo dõi', $stats['open']],
            ['— Đã lập dự án TKT', $stats['won']],
            ['— Không tiếp tục', $stats['lost']],
            ['Dự án tiền khả thi demo', $stats['projects']],
        ]);

        $this->info(sprintf('Đối chiếu với kỳ Tháng này (%s – %s):',
            $periodStart->format('d/m/Y'), now()->endOfMonth()->format('d/m/Y')));
        $this->table(['Ô trên màn báo cáo', 'Số nhu cầu do lệnh này sinh ra'], [
            ['Tổng nhu cầu còn hiệu lực theo dõi', $stats['carried']],
            ['Tổng nhu cầu phát sinh trong kỳ', $stats['arisen']],
            ['Tổng nhu cầu trong kỳ', $stats['carried'] + $stats['arisen']],
            ['— Chuyển đổi thành dự án TKT', $stats['won_in_period']],
            ['— Hết hạn, không tiếp tục', $stats['lost_in_period']],
            ['Tổng nhu cầu bị đóng trong kỳ', $stats['won_in_period'] + $stats['lost_in_period']],
        ]);
        $this->comment('Số trên màn có thể LỚN HƠN nếu cơ sở dữ liệu đã có nhu cầu thật cùng kỳ.');
        $this->comment('Xoá sạch dữ liệu demo: php artisan assign:seed-care-demo --clean');
    }
}
