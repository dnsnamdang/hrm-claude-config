<?php

namespace App\Console\Commands\Assign;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

/**
 * Đẩy DANH MỤC + CẤU HÌNH của phân hệ Giao việc (/assign) từ DB chính sang DB đích
 * cấu hình ở connection `mysql_target` (biến env DB_*_TARGET).
 *
 * Phạm vi bám theo menu sidebar của /assign:
 *  - nhóm "Danh mục" (trừ Khách hàng);
 *  - nhóm "Cấu hình": Cấu hình duyệt giá, và Cấu hình chung › tab Quản lý dự án
 *    (Mức độ ưu tiên + Cấu hình hạn).
 *
 * Cách ghi: MIRROR 1:1 — xoá sạch bảng ở đích rồi chèn lại nguyên vẹn từ nguồn
 * (giữ nguyên id để không lệch tham chiếu). Bản ghi chỉ có ở đích sẽ bị xoá.
 * Toàn bộ nằm trong 1 transaction: lỗi ở bất kỳ bảng nào cũng rollback sạch, đích giữ nguyên.
 * Ngoại lệ duy nhất là `general_regulations` — xem ghi chú ở hằng GENERAL_REGULATION_TABLE.
 *
 * KHÔNG bao gồm: bảng `customers`, các bảng *_snapshots, và các bảng log/lịch sử thay đổi
 * cấu hình (`bom_price_approval_config_logs`, `priority_level_history`,
 * `assign_deadline_config_history`) — log trỏ user_id của cổng nguồn, sang đích sẽ hiển thị sai người.
 */
class SyncAssignCatalogsCommand extends Command
{
    protected $signature = 'assign:sync-catalogs
                            {--tables= : Chỉ đẩy các bảng này, cách nhau bởi dấu phẩy}
                            {--dry-run : Chỉ in số liệu, không ghi gì vào DB đích}
                            {--force : Bỏ qua bước hỏi xác nhận}
                            {--chunk=500 : Số dòng mỗi lần insert}';

    protected $description = 'Đẩy danh mục + cấu hình phân hệ Giao việc từ DB chính sang DB đích (connection mysql_target)';

    /** Connection đích. */
    private const TARGET = 'mysql_target';

    /**
     * Danh sách bảng danh mục, xếp theo thứ tự phụ thuộc CHA → CON.
     * Insert theo đúng thứ tự này, truncate theo thứ tự NGƯỢC LẠI.
     *
     * Mỗi phần tử: 'tên bảng' => 'màn hình tương ứng'
     */
    private const TABLES = [
        // Nhóm ngành
        'scopes'                      => 'Nhóm ngành',
        // Nhóm giải pháp
        'industries'                  => 'Nhóm giải pháp',
        // Ứng dụng
        'applications'                => 'Ứng dụng',
        // Loại hình hoạt động KH
        'customer_scope_groups'       => 'Loại hình hoạt động KH',
        // Lĩnh vực kinh doanh KH
        'customer_scopes'             => 'Lĩnh vực kinh doanh KH',
        // Bảng nối
        'customer_scope_group_members' => 'Loại hình hoạt động KH (bảng nối)',
        'industry_scopes'             => 'Nhóm giải pháp × Nhóm ngành (bảng nối)',
        'application_industries'      => 'Ứng dụng × Nhóm giải pháp (bảng nối)',
        'application_scopes'          => 'Ứng dụng × Nhóm ngành (bảng nối)',
        'application_customer_scopes' => 'Ứng dụng × Lĩnh vực KH (bảng nối)',
        // Danh mục đơn
        'project_items'               => 'Hạng mục dự án',
        'project_phases'              => 'Giai đoạn dự án',
        'project_phase_items'         => 'Giai đoạn dự án (hạng mục con)',
        'project_roles'               => 'Vai trò dự án',
        'meeting_types'               => 'Loại meeting',
        'reason_project_failures'     => 'Lý do thất bại',
        'attachment_types'            => 'Loại tài liệu',
        'discount_types'              => 'Loại giảm giá',
        // Ngân hàng câu hỏi khảo sát — phải đi TRƯỚC nhóm form_*,
        // vì form_groups.survey_question_id và form_questions.survey_question_id trỏ sang đây.
        'survey_questions'            => 'Ngân hàng câu hỏi khảo sát',
        'survey_question_answers'     => 'Ngân hàng câu hỏi khảo sát (đáp án)',
        'survey_question_relations'   => 'Ngân hàng câu hỏi khảo sát (quan hệ cha-con)',
        // Phiếu thu thập thông tin
        'form_templates'              => 'Phiếu thu thập thông tin',
        'form_sections'               => 'Phiếu thu thập thông tin (phần)',
        'form_groups'                 => 'Phiếu thu thập thông tin (nhóm câu hỏi)',
        'form_questions'              => 'Phiếu thu thập thông tin (câu hỏi)',
        'form_question_options'       => 'Phiếu thu thập thông tin (đáp án)',
        // Nhóm menu Cấu hình
        'bom_price_approval_configs'  => 'Cấu hình duyệt giá',
        'priority_levels'             => 'Cấu hình chung › Quản lý dự án › Mức độ ưu tiên',
    ];

    /**
     * Cấu hình chung › Quản lý dự án › Cấu hình hạn KHÔNG có bảng riêng — nó ghi ké vào
     * `general_regulations`, là bảng Quy định chung của phân hệ Chấm công (base_salary,
     * timekeeping_max_distance, min_days_for_insurance…). Mirror cả bảng sẽ ghi đè cấu hình
     * lương/chấm công của cổng đích, nên bảng này xử lý riêng: chỉ UPDATE đúng các cột dưới đây,
     * khớp dòng theo `company_id`.
     */
    private const GENERAL_REGULATION_TABLE = 'general_regulations';

    private const GENERAL_REGULATION_COLUMNS = [
        'task_due_days',
        'issue_due_days',
        'meeting_due_days',
        'solution_due_days',
        'category_late_task_threshold',
        'people_late_task_threshold',
        'meeting_report_lock_days',
        'meeting_report_warning_hours',
    ];

    /** Cột audit sẽ bị ghi đè bằng id nhân viên tra theo email trên DB đích. */
    private const AUDIT_COLUMNS = ['created_by', 'updated_by'];

    public function handle()
    {
        $tables = $this->resolveTables();
        if ($tables === null) {
            return 1;
        }

        if (!$this->assertTargetUsable()) {
            return 1;
        }

        $mirrorTables = $this->mirrorTables($tables);
        $withGeneralRegulation = $this->wantsGeneralRegulation($tables);

        $stats = $this->collectStats($mirrorTables);
        $this->printPlan($stats);
        $this->warnOrphanRisk($mirrorTables);

        if ($withGeneralRegulation) {
            $this->printGeneralRegulationPlan();
        }

        if ($this->option('dry-run')) {
            $this->info('--dry-run: không ghi gì vào DB đích.');
            return 0;
        }

        // Tra id nhân viên TRƯỚC khi hỏi xác nhận, để user thấy trước sẽ ghi created_by bằng gì.
        $auditId = $this->resolveAuditEmployeeId();

        if (!$this->confirmToProceed()) {
            $this->warn('Đã huỷ.');
            return 1;
        }

        $exit = $this->sync($mirrorTables, $auditId, $withGeneralRegulation);
        if ($exit !== 0) {
            return $exit;
        }

        $this->line('');
        $this->info('Đẩy danh mục + cấu hình Giao việc sang DB đích xong.');

        return 0;
    }

    /**
     * Chốt danh sách bảng cần đẩy (theo --tables nếu có), giữ nguyên thứ tự phụ thuộc.
     */
    private function resolveTables(): ?array
    {
        $all = array_keys(self::TABLES);
        $valid = array_merge($all, [self::GENERAL_REGULATION_TABLE]);
        $only = $this->option('tables');
        if (!$only) {
            return $valid;
        }

        $requested = array_filter(array_map('trim', explode(',', $only)));
        $unknown = array_diff($requested, $valid);
        if (!empty($unknown)) {
            $this->error('Bảng không nằm trong danh mục Giao việc: ' . implode(', ', $unknown));
            $this->line('Các bảng hợp lệ: ' . implode(', ', $valid));
            return null;
        }

        // Giữ nguyên thứ tự phụ thuộc, không theo thứ tự user gõ.
        return array_values(array_intersect($valid, $requested));
    }

    /**
     * `general_regulations` không mirror mà update cột — tách ra khỏi danh sách mirror.
     */
    private function wantsGeneralRegulation(array $tables): bool
    {
        return in_array(self::GENERAL_REGULATION_TABLE, $tables, true);
    }

    private function mirrorTables(array $tables): array
    {
        return array_values(array_diff($tables, [self::GENERAL_REGULATION_TABLE]));
    }

    /**
     * Chặn 2 tình huống nguy hiểm: không kết nối được đích, hoặc đích trỏ trúng chính DB nguồn.
     */
    private function assertTargetUsable(): bool
    {
        $target = config('database.connections.' . self::TARGET);
        if (empty($target['database'])) {
            $this->error('Chưa cấu hình DB_DATABASE_TARGET trong .env — không biết đẩy đi đâu.');
            return false;
        }

        try {
            DB::connection(self::TARGET)->select('SELECT 1');
        } catch (\Throwable $e) {
            $this->error('Không kết nối được DB đích: ' . $e->getMessage());
            return false;
        }

        $source = config('database.connections.' . config('database.default'));
        $sameHost = (string) ($source['host'] ?? '') === (string) ($target['host'] ?? '')
            && (string) ($source['port'] ?? '') === (string) ($target['port'] ?? '');
        if ($sameHost && (string) ($source['database'] ?? '') === (string) $target['database']) {
            $this->error('DB đích đang trỏ trúng DB nguồn (' . $target['database'] . ') — dừng để tránh tự xoá dữ liệu.');
            return false;
        }

        return true;
    }

    /**
     * Đếm số dòng 2 bên + phát hiện cột lệch schema.
     */
    private function collectStats(array $tables): array
    {
        $stats = [];
        foreach ($tables as $table) {
            $sourceExists = Schema::hasTable($table);
            $targetExists = Schema::connection(self::TARGET)->hasTable($table);

            $sourceColumns = $sourceExists ? Schema::getColumnListing($table) : [];
            $targetColumns = $targetExists ? Schema::connection(self::TARGET)->getColumnListing($table) : [];

            $stats[$table] = [
                'label'         => self::TABLES[$table],
                'source_exists' => $sourceExists,
                'target_exists' => $targetExists,
                'source_count'  => $sourceExists ? DB::table($table)->count() : 0,
                'target_count'  => $targetExists ? DB::connection(self::TARGET)->table($table)->count() : 0,
                'shared'        => array_values(array_intersect($sourceColumns, $targetColumns)),
                'missing'       => array_values(array_diff($sourceColumns, $targetColumns)),
                'extra'         => array_values(array_diff($targetColumns, $sourceColumns)),
            ];
        }

        return $stats;
    }

    private function printPlan(array $stats): void
    {
        $this->line('');
        $this->info('DB nguồn : ' . config('database.connections.' . config('database.default') . '.database'));
        $this->info('DB đích  : ' . config('database.connections.' . self::TARGET . '.database')
            . ' @ ' . config('database.connections.' . self::TARGET . '.host'));
        $this->line('');

        $rows = [];
        foreach ($stats as $table => $s) {
            $note = '';
            if (!$s['source_exists']) {
                $note = 'BỎ QUA — không có ở nguồn';
            } elseif (!$s['target_exists']) {
                $note = 'BỎ QUA — không có ở đích';
            } elseif ($s['missing'] || $s['extra']) {
                $note = 'schema lệch';
            }

            $rows[] = [
                $table,
                $s['label'],
                $s['target_count'],
                $s['source_count'],
                $note,
            ];
        }

        $this->table(['Bảng', 'Màn hình', 'Đích (sẽ xoá)', 'Nguồn (sẽ ghi)', 'Ghi chú'], $rows);

        foreach ($stats as $table => $s) {
            if ($s['source_exists'] && $s['target_exists'] && ($s['missing'] || $s['extra'])) {
                if ($s['missing']) {
                    $this->warn("[$table] cột có ở nguồn nhưng thiếu ở đích (sẽ không copy): " . implode(', ', $s['missing']));
                }
                if ($s['extra']) {
                    $this->warn("[$table] cột chỉ có ở đích (sẽ nhận giá trị mặc định): " . implode(', ', $s['extra']));
                }
            }
        }
    }

    /**
     * Cảnh báo bản ghi danh mục chỉ tồn tại ở đích: sau khi mirror sẽ biến mất,
     * dữ liệu nghiệp vụ ở đích đang trỏ vào chúng sẽ thành mồ côi.
     */
    private function warnOrphanRisk(array $tables): void
    {
        $references = [
            'discount_types'  => ['quotation_discounts' => 'discount_type_id'],
            'form_questions'  => ['form_question_options' => 'form_question_id'],
        ];

        foreach ($tables as $table) {
            if (!isset($references[$table])) {
                continue;
            }
            if (!Schema::connection(self::TARGET)->hasTable($table) || !Schema::hasTable($table)) {
                continue;
            }

            $sourceIds = DB::table($table)->pluck('id')->all();
            $goneIds = DB::connection(self::TARGET)->table($table)
                ->when(!empty($sourceIds), fn($q) => $q->whereNotIn('id', $sourceIds))
                ->pluck('id')->all();

            if (empty($goneIds)) {
                continue;
            }

            foreach ($references[$table] as $refTable => $refColumn) {
                if (!Schema::connection(self::TARGET)->hasTable($refTable)) {
                    continue;
                }
                $usedIds = DB::connection(self::TARGET)->table($refTable)
                    ->whereIn($refColumn, $goneIds)
                    ->distinct()
                    ->pluck($refColumn)
                    ->all();

                if (!empty($usedIds)) {
                    $this->warn("[$table] id sẽ bị xoá nhưng đang được $refTable.$refColumn tham chiếu ở đích: "
                        . implode(', ', $usedIds));
                }
            }
        }
    }

    private function confirmToProceed(): bool
    {
        if ($this->option('force')) {
            return true;
        }

        $this->line('');
        $this->warn('Toàn bộ dữ liệu các bảng trên ở DB ĐÍCH sẽ bị XOÁ SẠCH rồi ghi lại từ DB nguồn.');

        return $this->confirm('Xác nhận chạy?', false);
    }

    /**
     * Tra id nhân viên trên DB ĐÍCH theo email cấu hình, dùng làm created_by/updated_by.
     */
    private function resolveAuditEmployeeId(): ?int
    {
        $email = config('database.sync_catalog_audit_email');
        if (!$email) {
            $this->warn('Chưa đặt SYNC_CATALOG_AUDIT_EMAIL — created_by/updated_by sẽ để NULL.');
            return null;
        }

        if (!Schema::connection(self::TARGET)->hasTable('employees')) {
            $this->warn('DB đích không có bảng employees — created_by/updated_by sẽ để NULL.');
            return null;
        }

        $id = DB::connection(self::TARGET)->table('employees')->where('email', $email)->value('id');
        if (!$id) {
            $this->warn("Không tìm thấy nhân viên có email $email ở DB đích — created_by/updated_by sẽ để NULL.");
            return null;
        }

        $this->info("created_by/updated_by = $id ($email, tra trên DB đích).");

        return (int) $id;
    }

    /**
     * Truncate ngược thứ tự phụ thuộc rồi insert xuôi.
     * Không bọc DB::transaction vì TRUNCATE là DDL — MySQL implicit-commit sẽ làm hỏng transaction.
     */
    private function sync(array $tables, ?int $auditId, bool $withGeneralRegulation): int
    {
        $target = DB::connection(self::TARGET);
        $chunk = max(1, (int) $this->option('chunk'));

        // Chỉ xử lý bảng tồn tại ở CẢ 2 bên.
        $tables = array_values(array_filter(
            $tables,
            fn($t) => Schema::hasTable($t) && Schema::connection(self::TARGET)->hasTable($t)
        ));

        if (empty($tables) && !$withGeneralRegulation) {
            $this->error('Không có bảng nào tồn tại ở cả 2 DB.');
            return 1;
        }

        $target->statement('SET FOREIGN_KEY_CHECKS = 0');

        $written = [];

        try {
            // Dùng DELETE (DML) chứ KHÔNG dùng TRUNCATE (DDL) để cả lượt đẩy nằm gọn trong 1
            // transaction — lỗi ở bảng bất kỳ thì rollback sạch, đích giữ nguyên dữ liệu cũ.
            // TRUNCATE gây implicit-commit, hỏng đúng tính chất này. Các bảng đều nhỏ nên DELETE
            // không phải vấn đề hiệu năng; id vẫn ghi tường minh nên không cần reset AUTO_INCREMENT.
            $target->transaction(function () use ($target, $tables, $chunk, $auditId, $withGeneralRegulation, &$written) {
                foreach (array_reverse($tables) as $table) {
                    $target->table($table)->delete();
                }

                foreach ($tables as $table) {
                    $written[] = $this->copyTable($target, $table, $chunk, $auditId);
                }

                if ($withGeneralRegulation) {
                    $this->syncGeneralRegulation($auditId);
                }
            });
        } catch (\Throwable $e) {
            $this->error('Lỗi khi đẩy dữ liệu: ' . $e->getMessage());
            $this->warn('Đã rollback — dữ liệu ở DB đích giữ nguyên như trước khi chạy.');
            return 1;
        } finally {
            $target->statement('SET FOREIGN_KEY_CHECKS = 1');
        }

        // Reset con trỏ AUTO_INCREMENT về max(id)+1 — chạy SAU khi transaction đã commit,
        // vì ALTER TABLE là DDL (implicit-commit) nên không thể nằm trong transaction.
        $this->resetAutoIncrement($target, $tables);

        $this->line('');
        $this->table(['Bảng', 'Màn hình', 'Số dòng đã ghi'], $written);

        return 0;
    }

    /**
     * Đưa AUTO_INCREMENT của bảng ở đích về max(id)+1 (bảng rỗng thì về 1), để id không nhảy
     * theo dấu vết của dữ liệu vừa bị xoá.
     */
    private function resetAutoIncrement($target, array $tables): void
    {
        $database = config('database.connections.' . self::TARGET . '.database');

        foreach ($tables as $table) {
            $hasAutoIncrement = DB::connection(self::TARGET)
                ->table('information_schema.COLUMNS')
                ->where('TABLE_SCHEMA', $database)
                ->where('TABLE_NAME', $table)
                ->where('EXTRA', 'auto_increment')
                ->exists();

            if (!$hasAutoIncrement) {
                continue;
            }

            $next = (int) $target->table($table)->max('id') + 1;

            try {
                $target->statement("ALTER TABLE `$table` AUTO_INCREMENT = $next");
            } catch (\Throwable $e) {
                $this->warn("  [$table] không reset được AUTO_INCREMENT: " . $e->getMessage());
            }
        }
    }

    /**
     * Copy 1 bảng từ nguồn sang đích theo chunk. Trả về 1 dòng cho bảng tổng kết.
     */
    private function copyTable($target, string $table, int $chunk, ?int $auditId): array
    {
        $targetColumns = Schema::connection(self::TARGET)->getColumnListing($table);
        $columns = array_values(array_intersect(Schema::getColumnListing($table), $targetColumns));

        // Chỉ ghi đè cột audit khi thực sự có id nhân viên. Nếu không tra được ($auditId = null)
        // thì cột NOT NULL phải GIỮ NGUYÊN giá trị nguồn — ghi NULL vào cột NOT NULL sẽ làm
        // insert chết giữa chừng, mà lúc đó bảng ở đích đã bị xoá.
        $auditColumns = [];
        foreach (array_intersect(self::AUDIT_COLUMNS, $columns) as $column) {
            if ($auditId !== null || $this->isNullableAtTarget($table, $column)) {
                $auditColumns[] = $column;
            }
        }

        $skippedAudit = array_diff(array_intersect(self::AUDIT_COLUMNS, $columns), $auditColumns);
        if (!empty($skippedAudit)) {
            $this->warn("  [$table] giữ nguyên giá trị nguồn cho cột NOT NULL: " . implode(', ', $skippedAudit));
        }

        $count = 0;
        DB::table($table)->select($columns)->orderBy('id')
            ->chunk($chunk, function ($rows) use ($target, $table, $auditColumns, $auditId, &$count) {
                $payload = [];
                foreach ($rows as $row) {
                    $data = (array) $row;
                    foreach ($auditColumns as $column) {
                        $data[$column] = $auditId;
                    }
                    $payload[] = $data;
                }
                $target->table($table)->insert($payload);
                $count += count($payload);
            });

        $this->line("  ✔ $table: $count dòng");

        return [$table, self::TABLES[$table], $count];
    }

    /**
     * Cột ở DB ĐÍCH có cho phép NULL không (đọc information_schema của chính DB đích).
     */
    private function isNullableAtTarget(string $table, string $column): bool
    {
        $database = config('database.connections.' . self::TARGET . '.database');

        $value = DB::connection(self::TARGET)
            ->table('information_schema.COLUMNS')
            ->where('TABLE_SCHEMA', $database)
            ->where('TABLE_NAME', $table)
            ->where('COLUMN_NAME', $column)
            ->value('IS_NULLABLE');

        return strtoupper((string) $value) === 'YES';
    }

    /**
     * Xem trước phần Cấu hình hạn: đối chiếu theo company_id, chỉ ra công ty nào không khớp.
     */
    private function printGeneralRegulationPlan(): void
    {
        $this->line('');
        $this->info('Cấu hình chung › Quản lý dự án › Cấu hình hạn (' . self::GENERAL_REGULATION_TABLE . ')');
        $this->line('  Chỉ UPDATE các cột: ' . implode(', ', self::GENERAL_REGULATION_COLUMNS));
        $this->line('  Khớp dòng theo company_id — KHÔNG truncate, không đụng cấu hình lương/chấm công ở đích.');

        if (!Schema::hasTable(self::GENERAL_REGULATION_TABLE)
            || !Schema::connection(self::TARGET)->hasTable(self::GENERAL_REGULATION_TABLE)) {
            $this->warn('  BỎ QUA — bảng không tồn tại ở một trong hai DB.');
            return;
        }

        $missing = array_diff($this->generalRegulationCompanyIds(null), $this->generalRegulationCompanyIds(self::TARGET));

        $this->line('  Công ty ở nguồn: ' . count($this->generalRegulationCompanyIds(null))
            . ' · ở đích: ' . count($this->generalRegulationCompanyIds(self::TARGET)));

        if (!empty($missing)) {
            $this->warn('  Công ty có ở nguồn nhưng đích chưa có dòng Quy định chung (sẽ BỎ QUA, không tự tạo): '
                . implode(', ', $missing));
        }
    }

    /**
     * @param string|null $connection null = DB nguồn (connection mặc định)
     */
    private function generalRegulationCompanyIds(?string $connection): array
    {
        $query = $connection === null
            ? DB::table(self::GENERAL_REGULATION_TABLE)
            : DB::connection($connection)->table(self::GENERAL_REGULATION_TABLE);

        return $query->whereNotNull('company_id')->pluck('company_id')->all();
    }

    /**
     * Đồng bộ Cấu hình hạn: chỉ UPDATE các cột khai trong GENERAL_REGULATION_COLUMNS,
     * khớp dòng theo company_id. Không INSERT dòng mới — tạo dòng Quy định chung thiếu các cột
     * lương/chấm công sẽ làm hỏng phân hệ Chấm công ở cổng đích.
     */
    private function syncGeneralRegulation(?int $auditId): void
    {
        $table = self::GENERAL_REGULATION_TABLE;

        if (!Schema::hasTable($table) || !Schema::connection(self::TARGET)->hasTable($table)) {
            $this->warn("[$table] bỏ qua — bảng không tồn tại ở một trong hai DB.");
            return;
        }

        $columns = array_values(array_intersect(
            self::GENERAL_REGULATION_COLUMNS,
            array_intersect(Schema::getColumnListing($table), Schema::connection(self::TARGET)->getColumnListing($table))
        ));

        if (empty($columns)) {
            $this->warn("[$table] bỏ qua — không cột nào của Cấu hình hạn có ở cả 2 DB.");
            return;
        }

        $hasUpdatedBy = in_array('updated_by', Schema::connection(self::TARGET)->getColumnListing($table), true);

        $updated = 0;
        $skipped = [];

        foreach (DB::table($table)->whereNotNull('company_id')->get() as $row) {
            $data = [];
            foreach ($columns as $column) {
                $data[$column] = $row->{$column};
            }
            if ($hasUpdatedBy) {
                $data['updated_by'] = $auditId;
            }

            $targetRow = DB::connection(self::TARGET)->table($table)->where('company_id', $row->company_id);

            // Phải kiểm tra tồn tại trước: update() trả 0 cả khi dòng có sẵn nhưng giá trị đã trùng.
            if (!$targetRow->exists()) {
                $skipped[] = $row->company_id;
                continue;
            }

            $targetRow->update($data);
            $updated++;
        }

        $this->line('');
        $this->line("  ✔ $table: cập nhật Cấu hình hạn cho $updated công ty (" . count($columns) . ' cột)');
        if (!empty($skipped)) {
            $this->warn('  Bỏ qua company_id không có dòng Quy định chung ở đích: ' . implode(', ', $skipped));
        }
    }
}
