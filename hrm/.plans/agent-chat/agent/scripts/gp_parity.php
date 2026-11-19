<?php
require 'vendor/autoload.php'; $app=require 'bootstrap/app.php'; $app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
use Illuminate\Http\Request;
$emp=(int)($argv[1]??13); auth()->onceUsingId($emp); App\Support\RequestCache::flush(); App\Support\Permissions\PermissionChecker::flush();
$co=(int) auth()->user()->current_company_role;
$rep = app(Modules\Assign\Services\Report\SolutionRequestsByDepartmentReportService::class);
$r = $rep->getReportData(new Request(['company_id'=>$co,'per_page'=>1000,'current_page'=>1]));
$byDept=[]; foreach ($r['data'] as $c) foreach ($c['departments'] ?? [] as $d) $byDept[$d['name'] ?? $d['department_name'] ?? '?'] = $d['total_requests'] ?? $d['total'] ?? ($d['count'] ?? null);
$t = (new Modules\Agent\Tools\ThongKeGiaiPhapTool)->run(['doi_tuong'=>'yeu_cau','pham_vi'=>'cong_ty','nhom_theo'=>'phong']);
echo "YC báo cáo tổng=", $r['total_requests'], " · agent tổng=", $t->data['totals']['requests'] ?? $t->outcome, "\n";
$mine=[]; foreach ($t->data['groups'] ?? [] as $g) $mine[$g['label']]=$g['requests'];
echo "phòng báo cáo: ", json_encode($byDept, JSON_UNESCAPED_UNICODE), "\nphòng agent:   ", json_encode($mine, JSON_UNESCAPED_UNICODE), "\n";
$v = app(Modules\Assign\Services\Report\SolutionVersionsReportService::class);
$rows = (new ReflectionMethod($v,'buildQuery'))->getClosure($v)(new Request(['company_id'=>$co]))->get();
$g = (new Modules\Agent\Tools\ThongKeGiaiPhapTool)->run(['doi_tuong'=>'giai_phap','pham_vi'=>'cong_ty']);
echo "GP báo cáo version: số GP=", $rows->pluck('solution_id')->unique()->count(), " giờ dự kiến=", round($rows->sum('estimated_hours'),1), " giờ thực tế=", round($rows->sum('actual_hours'),1),
 " · agent: số GP=", $g->data['totals']['solutions'] ?? $g->outcome, " dự kiến=", $g->data['totals']['planned_hours'] ?? '', " thực tế=", $g->data['totals']['actual_hours'] ?? '', "\n";
