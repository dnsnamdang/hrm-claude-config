<?php

namespace App\Console\Commands\GopDb;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Modules\Timesheet\Database\Seeders\GopDb\MergeProdSeeder;
use ReflectionClass;

/**
 * CỔNG NGHIỆM THU cho việc GỘP DB (ERP + HRM).
 *
 * CHỈ ĐỌC — không có một câu lệnh ghi nào. Chạy bao nhiêu lần cũng được, trên PROD cũng an toàn.
 *
 * Dùng ở 2 thời điểm:
 *   --mode=pre   TRƯỚC khi gộp  : cảnh báo cái gì SẮP mất, cái gì SẮP trỏ nhầm (cần --erp + --hrm)
 *   --mode=post  SAU khi gộp    : đo cái gì ĐÃ hỏng (cần --merged; có --erp/--hrm thì đối chiếu thêm)
 *   --mode=auto  (mặc định)     : tự chọn theo schema được truyền vào
 *
 * Ví dụ:
 *   php artisan gopdb:health-check --erp=dev_erp --hrm=hrm_prod_local --mode=pre
 *   php artisan gopdb:health-check --merged=local_hrm_erp --erp=dev_erp --hrm=hrm_prod_local
 *
 * Exit code: 0 = sạch · 1 = có phát hiện mức CHẶN (không được cut-over) · 2 = sai tham số.
 *
 * Danh sách bảng KEEP_HRM / SHARE / TACH KHÔNG chép tay — đọc thẳng từ MergeProdSeeder bằng
 * Reflection để 2 nơi không bao giờ lệch nhau.
 */
class HealthCheckCommand extends Command
{
    protected $signature = 'gopdb:health-check
        {--erp= : schema ERP gốc (vd dev_erp)}
        {--hrm= : schema HRM gốc (vd hrm_prod_local)}
        {--merged= : schema bản đã gộp (vd local_hrm_erp); bỏ trống = connection hiện tại}
        {--mode=auto : pre | post | auto}
        {--offset=100000 : OFFSET mà ReconcileAuthSeeder dùng để dời id roles/permissions của ERP}
        {--full : in đầy đủ, không cắt bớt danh sách dài}';

    protected $description = 'Cổng nghiệm thu GỘP DB ERP+HRM — chỉ đọc, đo FK mồ côi / role trỏ nhầm / bảng bị mất / lệch row-count';

    /** @var int số phát hiện mức CHẶN */
    private $blockers = 0;
    /** @var int số phát hiện mức CẢNH BÁO */
    private $warnings = 0;

    /** Bảng pivot auth — sau khi gộp thực sự chứa dòng của cả 2 hệ, guard 'api' ở đây là hợp lệ. */
    private const AUTH_PIVOT_TABLES = [
        'role_has_permissions',
        'employee_has_roles',
        'employee_has_permissions',
        'company_roles',
        'role_permission_history',
    ];

    public function handle(): int
    {
        $erp    = $this->option('erp');
        $hrm    = $this->option('hrm');
        $merged = $this->option('merged') ?: DB::connection()->getDatabaseName();
        $mode   = $this->option('mode');

        foreach (array_filter(['--erp' => $erp, '--hrm' => $hrm, '--merged' => $merged]) as $flag => $s) {
            if (!$this->schemaExists($s)) {
                $this->error("Schema '$s' ($flag) không tồn tại trên server này.");
                return 2;
            }
        }

        if ($mode === 'auto') {
            $mode = ($erp && $hrm && !$this->option('merged')) ? 'pre' : 'post';
        }
        if ($mode === 'pre' && (!$erp || !$hrm)) {
            $this->error('mode=pre cần cả --erp và --hrm.');
            return 2;
        }

        $this->line('');
        $this->line('<options=bold>═══ CỔNG NGHIỆM THU GỘP DB ═══</>');
        $this->line("  chế độ : <fg=cyan>$mode</>  (chỉ đọc, không ghi gì)");
        $this->line('  ERP    : ' . ($erp ?: '(không truyền)'));
        $this->line('  HRM    : ' . ($hrm ?: '(không truyền)'));
        $this->line('  GỘP    : ' . ($mode === 'post' ? $merged : '(chưa có)'));

        $plan = $this->readMergePlan();

        if ($mode === 'pre') {
            $this->checkPreDuplicates($erp, $hrm, $plan);
            $this->checkPreDroppedTables($erp, $hrm, $plan);
            $this->checkPreShareIdMeaning($erp, $hrm, $plan);
            $this->checkPreRoleRefs($erp);
            $this->checkPreForeignKeys($erp, $hrm);
            $this->checkPreTruncate($erp, $hrm, $plan);
        } else {
            $this->checkPostForeignKeys($merged, $erp, $hrm);
            $this->checkPostRoleRefs($merged);
            $this->checkPostDroppedTables($merged, $erp, $plan);
            $this->checkPostRowCounts($merged, $erp, $hrm);
        }

        return $this->summary();
    }

    // ───────────────────────── PRE ─────────────────────────

    /** Bảng trùng tên giữa 2 schema — nền của mọi rủi ro còn lại. */
    private function checkPreDuplicates(string $erp, string $hrm, array $plan): void
    {
        $dups = $this->duplicateTables($erp, $hrm);
        $this->section('1. Bảng TRÙNG TÊN giữa ERP và HRM', count($dups) . ' bảng');

        $known = array_merge($plan['KEEP_HRM'], $plan['SHARE'], $plan['TACH'], $plan['LOG_DROP'], ['migrations']);
        $unhandled = array_values(array_diff($dups, $known));

        if ($unhandled) {
            $this->blocker(count($unhandled) . ' bảng trùng tên KHÔNG nằm trong nhóm nào của MergeProdSeeder');
            $this->line('     Nhánh else của seeder sẽ BỎ QUA (skip) chúng → dữ liệu HRM ở lại schema cũ, mất khi drop schema:');
            $this->listOut($unhandled);
        } else {
            $this->ok('Mọi bảng trùng tên đều đã được phân nhóm xử lý');
        }
    }

    /** KEEP_HRM: seeder DROP bảng ERP rồi thay bằng bản HRM → ERP mất trắng. */
    private function checkPreDroppedTables(string $erp, string $hrm, array $plan): void
    {
        $this->section('2. Bảng ERP sẽ bị DROP và thay bằng bản HRM (nhóm KEEP_HRM)', '');

        $rows = [];
        $totalLost = 0;
        foreach ($plan['KEEP_HRM'] as $t) {
            if (!$this->tableExists($erp, $t)) {
                continue;
            }
            $e = $this->rows($erp, $t);
            $h = $this->tableExists($hrm, $t) ? $this->rows($hrm, $t) : 0;
            $totalLost += $e;
            $rows[] = [$t, number_format($e), number_format($h), $e > 0 ? 'MẤT TRẮNG' : '-'];
        }

        if (!$rows) {
            $this->ok('Không có bảng nào trong nhóm KEEP_HRM tồn tại ở ERP');
            return;
        }
        $this->table(['Bảng ERP', 'Dòng ERP (mất)', 'Dòng HRM (thay vào)', ''], $rows);

        if ($totalLost > 0) {
            $this->blocker(number_format($totalLost) . ' dòng dữ liệu ERP sẽ bị xoá vĩnh viễn, không có bản sao');
            $this->line('     Cách xử lý: đổi DROP thành RENAME sang `erp_<tên bảng>`, hoặc chuyển bảng đó sang nhóm TACH (hrm_*).');
        }
    }

    /** SHARE + FILL_SHARED_HRM: UPDATE ... ON e.id=h.id — chỉ đúng nếu id 2 bên CÙNG NGHĨA. */
    private function checkPreShareIdMeaning(string $erp, string $hrm, array $plan): void
    {
        $this->section('3. Nhóm SHARE — id hai bên có cùng nghĩa không?', 'ghép bằng e.id = h.id');

        $rows = [];
        foreach ($plan['SHARE'] as $t) {
            if (!$this->tableExists($erp, $t) || !$this->tableExists($hrm, $t)) {
                continue;
            }
            $col = $this->labelColumn($erp, $t, $hrm);
            if (!$col) {
                $rows[] = [$t, '-', '-', '-', 'không có cột tên để đối chiếu'];
                continue;
            }
            $r = DB::selectOne(
                "SELECT COUNT(*) tong, SUM(e.`$col` <=> h.`$col`) khop, SUM(NOT (e.`$col` <=> h.`$col`)) lech
                   FROM `$erp`.`$t` e JOIN `$hrm`.`$t` h ON h.id = e.id"
            );
            $lech = (int) ($r->lech ?? 0);
            if ($lech > 0) {
                $this->warnings++;
            }
            $rows[] = [$t, $col, number_format((int) $r->tong), number_format((int) ($r->khop ?? 0)), $lech > 0 ? "⚠ $lech" : '0'];
        }
        $this->table(['Bảng', 'Cột đối chiếu', 'id trùng', 'khớp', 'LỆCH'], $rows);
        $this->line('     Dòng LỆCH = cùng id nhưng là hai bản ghi KHÁC NHAU → UPDATE sẽ ghi đè chéo, âm thầm.');
    }

    /**
     * Mọi nơi trỏ tới roles/permissions ở ERP. ReconcileAuthSeeder dời id ERP +OFFSET
     * nhưng chỉ remap 4 bảng — chỗ nào ngoài 4 bảng đó sẽ mồ côi hoặc trỏ nhầm.
     */
    private function checkPreRoleRefs(?string $erp): void
    {
        if (!$erp) {
            return;
        }
        $this->section('4. Nơi trỏ tới roles/permissions ở ERP (phải remap khi dời id)', '');

        $remapped = ['role_has_permissions', 'company_roles', 'employee_has_roles', 'employee_has_permissions'];
        $refs = $this->roleRefColumns($erp);

        $rows = [];
        $missing = 0;
        foreach ($refs as [$t, $c, $src]) {
            $n = $this->rowsWhereRef($erp, $t, $c);
            $done = in_array($t, $remapped, true);
            if (!$done && $n > 0) {
                $missing += $n;
            }
            if ($n === 0 && $done) {
                continue;
            }
            $rows[] = [$t, $c, $src, number_format($n), $done ? 'có remap' : ($n > 0 ? '⚠ KHÔNG remap' : '-')];
        }
        $this->table(['Bảng', 'Cột', 'Phát hiện qua', 'Dòng có giá trị', 'Seeder xử lý?'], $rows);

        if ($missing > 0) {
            $this->blocker(number_format($missing) . ' dòng trỏ tới roles/permissions nằm NGOÀI 4 bảng seeder remap');
            $this->line('     Sau khi dời id, số dòng này sẽ mồ côi hoặc trỏ nhầm sang vai trò của hệ còn lại.');
            $this->line('     Cách xử lý: remap theo danh sách sinh từ information_schema như bảng trên, không liệt kê tay.');
        } else {
            $this->ok('Mọi nơi trỏ tới roles/permissions đều nằm trong phạm vi seeder remap');
        }

        $this->checkPreIdCollision($erp);
    }

    /** Dải id roles/permissions 2 bên chồng nhau tới đâu — quyết định "mồ côi" hay "trỏ nhầm". */
    private function checkPreIdCollision(string $erp): void
    {
        $hrm = $this->option('hrm');
        if (!$hrm) {
            return;
        }
        $rows = [];
        foreach (['roles', 'permissions'] as $t) {
            if (!$this->tableExists($erp, $t) || !$this->tableExists($hrm, $t)) {
                continue;
            }
            $e = DB::selectOne("SELECT COUNT(*) n, MIN(id) mi, MAX(id) ma FROM `$erp`.`$t`");
            $h = DB::selectOne("SELECT COUNT(*) n, MIN(id) mi, MAX(id) ma FROM `$hrm`.`$t`");
            $overlap = DB::selectOne("SELECT COUNT(*) n FROM `$erp`.`$t` e JOIN `$hrm`.`$t` h ON h.id = e.id");
            $rows[] = [$t, "{$e->n} (id {$e->mi}–{$e->ma})", "{$h->n} (id {$h->mi}–{$h->ma})", (int) $overlap->n];
            if ((int) $overlap->n > 0) {
                $this->warnings++;
            }
        }
        $this->table(['Bảng', 'ERP', 'HRM', 'id CHỒNG NHAU'], $rows);
        $this->line('     id chồng nhau > 0 → dòng không được remap sẽ trỏ sang một vai trò CÓ THẬT nhưng SAI');
        $this->line('     (nguy hiểm hơn mồ côi, vì không có gì báo lỗi).');
    }

    /** Đếm FK trước khi gộp, để so với sau khi gộp. */
    private function checkPreForeignKeys(string $erp, string $hrm): void
    {
        $this->section('5. Ràng buộc FOREIGN KEY hiện có (mốc để đối chiếu sau khi gộp)', '');
        $this->table(
            ['Schema', 'Số FK', 'Số bảng có FK'],
            [
                [$erp, number_format($this->fkCount($erp)), $this->fkTableCount($erp)],
                [$hrm, number_format($this->fkCount($hrm)), $this->fkTableCount($hrm)],
            ]
        );
        $this->line('     GHI LẠI 2 con số này. Sau khi gộp chạy lại --mode=post để đối chiếu.');
    }

    private function checkPreTruncate(string $erp, string $hrm, array $plan): void
    {
        if (!$plan['EMPTY_AFTER_TACH']) {
            return;
        }
        $this->section('6. Bảng sẽ bị TRUNCATE sau khi tách', '');
        $rows = [];
        foreach ($plan['EMPTY_AFTER_TACH'] as $t) {
            $e = $this->tableExists($erp, $t) ? $this->rows($erp, $t) : 0;
            $h = $this->tableExists($hrm, $t) ? $this->rows($hrm, $t) : 0;
            $rows[] = [$t, number_format($e), number_format($h), number_format($e + $h)];
            if ($e + $h > 0) {
                $this->warnings++;
            }
        }
        $this->table(['Bảng', 'Dòng ERP', 'Dòng HRM', 'TỔNG SẼ MẤT'], $rows);
        $this->line('     Nếu là chủ ý thì archive sang bảng riêng trước khi TRUNCATE.');
    }

    // ───────────────────────── POST ─────────────────────────

    private function checkPostForeignKeys(string $merged, ?string $erp, ?string $hrm): void
    {
        $this->section('1. Ràng buộc FOREIGN KEY sau khi gộp', '');
        $now = $this->fkCount($merged);
        $rows = [[$merged . ' (đã gộp)', number_format($now), $this->fkTableCount($merged)]];

        $before = 0;
        foreach (array_filter([$erp, $hrm]) as $s) {
            $c = $this->fkCount($s);
            $before += $c;
            $rows[] = [$s . ' (gốc)', number_format($c), $this->fkTableCount($s)];
        }
        $this->table(['Schema', 'Số FK', 'Số bảng có FK'], $rows);

        if ($before > 0 && $now < $before) {
            $mat = $before - $now;
            $pct = round($mat * 100 / $before, 1);
            $this->blocker("Mất $pct% ràng buộc FK (" . number_format($mat) . ' FK)');
            $this->line('     Hệ quả: không còn gì chặn dữ liệu mồ côi, và mất ON DELETE/UPDATE CASCADE mà code có thể đang dựa vào.');
        } elseif ($before > 0) {
            $this->ok('Số FK không giảm so với 2 schema gốc');
        }
    }

    /**
     * Đo hậu quả thật: dòng nào mồ côi, dòng nào trỏ nhầm sang guard của hệ kia.
     *
     * ⚠️ Chỉ bảng THUẦN ERP mới tính "trỏ nhầm". Bảng pivot dùng chung sau khi gộp
     * (`role_has_permissions`, `employee_has_roles`, `company_roles`…) chứa cả dòng của HRM,
     * nên dòng guard `api` ở đó là HỢP LỆ — tính vào sẽ thành báo động giả.
     * Phân loại cần cả --erp và --hrm; thiếu thì cột đó ghi "cần rà tay".
     */
    private function checkPostRoleRefs(string $merged): void
    {
        $erp = $this->option('erp');
        $hrm = $this->option('hrm');
        $canClassify = $erp && $hrm;

        $this->section(
            '2. Dòng trỏ tới roles/permissions — mồ côi & trỏ nhầm',
            $canClassify ? 'chỉ bảng thuần ERP mới tính trỏ nhầm' : 'thiếu --erp/--hrm nên không phân loại được'
        );

        $hasGuard = $this->columnExists($merged, 'roles', 'guard_name');
        $rows = [];
        $totWrong = $totOrphan = 0;
        $unclassified = 0;

        // ⚠️ Sau khi gộp, FK của ERP có thể đã mất -> roleRefColumns($merged) sẽ KHÔNG còn thấy
        // các cột như `approver_role_id` / `deputy_role` (tên không phải role_id, chỉ nhận ra nhờ FK).
        // Nên gộp thêm danh sách lấy từ SCHEMA GỐC, nơi FK còn nguyên.
        $refs = $this->roleRefColumns($merged);
        foreach (array_filter([$erp, $hrm]) as $src) {
            foreach ($this->roleRefColumns($src) as $r) {
                $refs[] = $r;
            }
        }
        $refs = array_values(array_reduce($refs, function ($acc, $r) {
            $acc[strtolower($r[0]) . '.' . strtolower($r[1])] = $r;
            return $acc;
        }, []));
        ksort($refs);

        foreach ($refs as [$t, $c, $src]) {
            $target = str_contains($c, 'permission') ? 'permissions' : 'roles';
            if (!$this->tableExists($merged, $target) || !$this->tableExists($merged, $t) || !$this->columnExists($merged, $t, $c)) {
                continue;
            }
            $guardSel = $hasGuard ? "SUM(r.guard_name = 'api') api" : 'NULL api';
            $r = DB::selectOne(
                "SELECT COUNT(*) tong, $guardSel, SUM(r.id IS NULL) mocoi
                   FROM `$merged`.`$t` s LEFT JOIN `$merged`.`$target` r ON r.id = s.`$c`
                  WHERE s.`$c` IS NOT NULL AND s.`$c` <> 0"
            );
            $tong = (int) $r->tong;
            if ($tong === 0) {
                continue;
            }
            $api = (int) ($r->api ?? 0);
            $mocoi = (int) ($r->mocoi ?? 0);
            $totOrphan += $mocoi;

            // Phân loại 3 mức. KHÔNG tuyên bố "hợp lệ" khi không chứng minh được:
            //  - pivot auth  : bảng thực sự trộn 2 hệ sau khi gộp -> dòng guard 'api' là của HRM, hợp lệ
            //  - thuần ERP   : cột chỉ ERP có -> guard 'api' chắc chắn là trỏ nhầm (CHẶN)
            //  - còn lại     : cột tồn tại ở cả 2 schema nhưng dữ liệu trong bản gộp có thể chỉ đến
            //                  từ một bên (vd `companies` lấy nền ERP) -> KHÔNG kết luận tự động,
            //                  đẩy sang "cần rà tay" thay vì gắn nhãn hợp lệ.
            $isAuthPivot = in_array($t, self::AUTH_PIVOT_TABLES, true);
            $erpOnlyCol = $canClassify
                ? ($this->columnExists($erp, $t, $c) && !$this->columnExists($hrm, $t, $c))
                : null;

            if ($isAuthPivot) {
                $loai = 'pivot auth (trộn 2 hệ)';
                $nhamCell = $api > 0 ? "$api (hợp lệ)" : '0';
            } elseif ($erpOnlyCol === true) {
                $loai = 'thuần ERP';
                $totWrong += $api;
                $nhamCell = $api > 0 ? "⚠ $api" : '0';
            } else {
                $loai = $canClassify ? 'cột có ở cả 2 hệ' : '?';
                $nhamCell = $api > 0 ? "⚠ $api — RÀ TAY" : '0';
                $unclassified += $api;
            }

            $rows[] = [$t, $c, $loai, number_format($tong), $nhamCell, $mocoi > 0 ? "⚠ $mocoi" : '0'];
        }

        if (!$rows) {
            $this->ok('Không tìm thấy bảng nào trỏ tới roles/permissions');
            return;
        }
        $this->table(['Bảng', 'Cột', 'Loại bảng', 'Dòng có giá trị', "TRỎ NHẦM (guard 'api')", 'MỒ CÔI'], $rows);

        if ($totWrong > 0) {
            $this->blocker(number_format($totWrong) . " dòng ở bảng THUẦN ERP đang trỏ sang vai trò của HRM (guard 'api')");
            $this->line('     Đây là vai trò CÓ THẬT nhưng SAI — không có exception, không có log, DB cũng không chặn.');
        }
        if ($unclassified > 0) {
            $this->warnings++;
            $this->line('  <fg=yellow>⚠ RÀ TAY</> ' . number_format($unclassified) . " dòng guard 'api' nằm ở cột có mặt trong CẢ HAI hệ — không tự kết luận được.");
            $this->line('     Phải mở từng dòng đối chiếu tên vai trò xem có đúng nghiệp vụ không.');
            $this->line("     VD đã gặp: `companies`.`deputy_role` — cả 8 công ty trỏ sang vai trò HRM, đáng lẽ phải là 'Tổng giám đốc' / 'Giám đốc công ty'.");
        }
        if ($totOrphan > 0) {
            $this->blocker(number_format($totOrphan) . ' dòng MỒ CÔI (trỏ tới id không còn tồn tại)');
        }
        if ($totWrong === 0 && $totOrphan === 0 && $unclassified === 0) {
            $this->ok('Không có dòng nào trỏ nhầm hoặc mồ côi');
        }
    }

    private function checkPostDroppedTables(string $merged, ?string $erp, array $plan): void
    {
        if (!$erp) {
            return;
        }
        $this->section('3. Bảng ERP thuộc nhóm KEEP_HRM — còn dữ liệu không?', '');

        $rows = [];
        $lost = 0;
        foreach ($plan['KEEP_HRM'] as $t) {
            if (!$this->tableExists($erp, $t)) {
                continue;
            }
            $e = $this->rows($erp, $t);
            $g = $this->tableExists($merged, $t) ? $this->rows($merged, $t) : null;
            if ($e === 0) {
                continue;
            }
            $keptBackup = $this->tableExists($merged, 'erp_' . $t);
            if ($g !== null && $g < $e && !$keptBackup) {
                $lost += ($e - $g);
            }
            $rows[] = [
                $t,
                number_format($e),
                $g === null ? '(không còn bảng)' : number_format($g),
                $keptBackup ? 'có erp_' . $t : ($g !== null && $g < $e ? '⚠ KHÔNG có bản sao' : '-'),
            ];
        }
        if (!$rows) {
            $this->ok('Không có bảng KEEP_HRM nào có dữ liệu ở ERP');
            return;
        }
        $this->table(['Bảng', 'Dòng ở ERP gốc', 'Dòng ở bản gộp', 'Bản sao'], $rows);
        if ($lost > 0) {
            $this->blocker(number_format($lost) . ' dòng dữ liệu ERP đã mất, không có bản sao để khôi phục');
        }
    }

    /** So row-count từng bảng — bắt trường hợp bản gộp dựng từ snapshot cũ. */
    private function checkPostRowCounts(string $merged, ?string $erp, ?string $hrm): void
    {
        if (!$erp) {
            return;
        }
        $this->section('4. Bảng ở bản gộp có ÍT dòng hơn ERP gốc', 'dấu hiệu snapshot cũ / mất dòng');

        $plan = $this->readMergePlan();
        $skip = array_flip(array_merge($plan['KEEP_HRM'], $plan['LOG_DROP'], $plan['EMPTY_AFTER_TACH'], ['migrations']));

        $rows = [];
        foreach ($this->tablesOf($erp) as $t) {
            if (isset($skip[$t]) || !$this->tableExists($merged, $t)) {
                continue;
            }
            $e = $this->rows($erp, $t);
            if ($e === 0) {
                continue;
            }
            $g = $this->rows($merged, $t);
            if ($g >= $e) {
                continue;
            }
            $rows[] = [$t, number_format($e), number_format($g), number_format($g - $e), round(($e - $g) * 100 / $e, 1) . '%'];
        }

        if (!$rows) {
            $this->ok('Không bảng nào ít dòng hơn ERP gốc');
            return;
        }
        usort($rows, fn ($a, $b) => (int) str_replace(',', '', $a[3]) <=> (int) str_replace(',', '', $b[3]));
        $show = $this->option('full') ? $rows : array_slice($rows, 0, 25);
        $this->table(['Bảng', 'ERP gốc', 'Bản gộp', 'Chênh', '%'], $show);
        if (count($rows) > count($show)) {
            $this->line('     … và ' . (count($rows) - count($show)) . ' bảng nữa (dùng --full để xem hết).');
        }
        $this->warn('  ⚠ ' . count($rows) . ' bảng ít dòng hơn ERP gốc — nếu ERP vẫn đang chạy thì bản gộp là snapshot cũ, KHÔNG bê lên PROD được.');
        $this->warnings++;
    }

    // ───────────────────────── tra cứu ─────────────────────────

    /** Đọc 3 nhóm bảng thẳng từ MergeProdSeeder — 1 nguồn sự thật duy nhất. */
    private function readMergePlan(): array
    {
        $default = ['KEEP_HRM' => [], 'SHARE' => [], 'TACH' => [], 'EMPTY_AFTER_TACH' => [], 'LOG_DROP' => []];
        try {
            $props = (new ReflectionClass(MergeProdSeeder::class))->getDefaultProperties();
        } catch (\Throwable $e) {
            $this->warn('  ⚠ Không đọc được MergeProdSeeder (' . $e->getMessage() . ') — bỏ qua các mục dựa trên danh sách nhóm.');
            return $default;
        }
        foreach (array_keys($default) as $k) {
            if (isset($props[$k]) && is_array($props[$k])) {
                $default[$k] = $props[$k];
            }
        }
        return $default;
    }

    /**
     * Mọi cột trỏ tới roles/permissions: lấy CẢ hai nguồn — FK khai báo, và cột đặt tên
     * role_id/permission_id nhưng không khai FK (loại này seeder dễ bỏ sót nhất).
     */
    private function roleRefColumns(string $schema): array
    {
        $out = [];
        $fk = DB::select(
            "SELECT table_name t, column_name c FROM information_schema.key_column_usage
              WHERE table_schema = ? AND referenced_table_name IN ('roles','permissions')",
            [$schema]
        );
        foreach ($fk as $r) {
            $out[strtolower($r->t) . '.' . strtolower($r->c)] = [$r->t, $r->c, 'FK'];
        }
        $named = DB::select(
            "SELECT table_name t, column_name c FROM information_schema.columns
              WHERE table_schema = ? AND column_name IN ('role_id','permission_id')",
            [$schema]
        );
        foreach ($named as $r) {
            $k = strtolower($r->t) . '.' . strtolower($r->c);
            if (!isset($out[$k])) {
                $out[$k] = [$r->t, $r->c, 'tên cột'];
            }
        }
        ksort($out);
        return array_values($out);
    }

    private function duplicateTables(string $a, string $b): array
    {
        $r = DB::select(
            "SELECT x.table_name t FROM information_schema.tables x
               JOIN information_schema.tables y ON y.table_name = x.table_name AND y.table_schema = ?
              WHERE x.table_schema = ? AND x.table_type = 'BASE TABLE'
              ORDER BY x.table_name",
            [$b, $a]
        );
        return array_map(fn ($x) => $x->t, $r);
    }

    private function tablesOf(string $schema): array
    {
        $r = DB::select(
            "SELECT table_name t FROM information_schema.tables WHERE table_schema = ? AND table_type = 'BASE TABLE' ORDER BY table_name",
            [$schema]
        );
        return array_map(fn ($x) => $x->t, $r);
    }

    /** Cột dùng để kiểm 2 bản ghi cùng id có phải cùng một thứ không. */
    private function labelColumn(string $schema, string $table, string $other): ?string
    {
        foreach (['name', 'fullname', 'code', 'title', 'email'] as $c) {
            if ($this->columnExists($schema, $table, $c) && $this->columnExists($other, $table, $c)) {
                return $c;
            }
        }
        return null;
    }

    private function schemaExists(string $s): bool
    {
        return (bool) DB::select('SELECT 1 FROM information_schema.schemata WHERE schema_name = ? LIMIT 1', [$s]);
    }

    private function tableExists(string $schema, string $t): bool
    {
        return (bool) DB::select('SELECT 1 FROM information_schema.tables WHERE table_schema = ? AND table_name = ? LIMIT 1', [$schema, $t]);
    }

    private function columnExists(string $schema, string $t, string $c): bool
    {
        return (bool) DB::select(
            'SELECT 1 FROM information_schema.columns WHERE table_schema = ? AND table_name = ? AND column_name = ? LIMIT 1',
            [$schema, $t, $c]
        );
    }

    private function rows(string $schema, string $t): int
    {
        return (int) DB::selectOne("SELECT COUNT(*) n FROM `$schema`.`$t`")->n;
    }

    private function rowsWhereRef(string $schema, string $t, string $c): int
    {
        return (int) DB::selectOne("SELECT COUNT(*) n FROM `$schema`.`$t` WHERE `$c` IS NOT NULL AND `$c` <> 0")->n;
    }

    private function fkCount(string $schema): int
    {
        return (int) DB::selectOne(
            'SELECT COUNT(*) n FROM information_schema.key_column_usage WHERE table_schema = ? AND referenced_table_name IS NOT NULL',
            [$schema]
        )->n;
    }

    private function fkTableCount(string $schema): int
    {
        return (int) DB::selectOne(
            'SELECT COUNT(DISTINCT table_name) n FROM information_schema.key_column_usage WHERE table_schema = ? AND referenced_table_name IS NOT NULL',
            [$schema]
        )->n;
    }

    // ───────────────────────── in ấn ─────────────────────────

    private function section(string $title, string $note): void
    {
        $this->line('');
        $this->line("<options=bold;fg=cyan>── $title</>" . ($note !== '' ? " <fg=gray>($note)</>" : ''));
    }

    private function listOut(array $items): void
    {
        $show = $this->option('full') ? $items : array_slice($items, 0, 20);
        foreach (array_chunk($show, 4) as $chunk) {
            $this->line('       ' . implode(', ', $chunk));
        }
        if (count($items) > count($show)) {
            $this->line('       … và ' . (count($items) - count($show)) . ' bảng nữa (--full để xem hết)');
        }
    }

    private function blocker(string $msg): void
    {
        $this->blockers++;
        $this->line("  <fg=red;options=bold>✖ CHẶN</> $msg");
    }

    private function ok(string $msg): void
    {
        $this->line("  <fg=green>✔</> $msg");
    }

    private function summary(): int
    {
        $this->line('');
        $this->line('<options=bold>═══ KẾT LUẬN ═══</>');
        if ($this->blockers > 0) {
            $this->line("  <fg=red;options=bold>{$this->blockers} phát hiện mức CHẶN</> — KHÔNG được cut-over cho tới khi xử lý xong.");
        } else {
            $this->line('  <fg=green;options=bold>Không có phát hiện mức chặn.</>');
        }
        if ($this->warnings > 0) {
            $this->line("  <fg=yellow>{$this->warnings} cảnh báo</> — đọc kỹ từng mục ở trên trước khi quyết định.");
        }
        $this->line('');
        return $this->blockers > 0 ? 1 : 0;
    }
}
