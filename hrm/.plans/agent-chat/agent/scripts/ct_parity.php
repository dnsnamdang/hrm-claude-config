<?php
require 'vendor/autoload.php'; $app=require 'bootstrap/app.php'; $app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
use Modules\Timesheet\Entities\EmployeeInfo; use Carbon\Carbon;
auth()->onceUsingId(13);
[$from,$to,$dept] = [$argv[1],$argv[2],(int)$argv[3]];
$q = EmployeeInfo::where('company_id',1)->where('department_id',$dept)->where(function($q) use ($from){ $q->where('status',1)->orWhereDate('leave_date','>',$from); });
$page = $q->orderBy('id')->paginate($q->count());
$ref = app(Modules\Timesheet\Services\TimesheetSummaryService::class)->getDataTimesheet($page,$from,$to)['data'];
$tool = new Modules\Agent\Tools\ThongKeCongTacTool; $m = new ReflectionMethod($tool,'checkins'); $m->setAccessible(true);
$rows = $m->invoke($tool,'phong',['phong_ban_id'=>$dept],Carbon::parse($from)->startOfDay(),Carbon::parse($to)->endOfDay(),null,'');
$mine=[]; foreach ($rows as $r) $mine[$r->info_id][$r->d]=true;
$diff=0;$tot=0;$totm=0;
foreach ($ref as $r) { $n=0; foreach ($r as $k=>$v) if (is_string($v) && in_array('CT', explode('<br>',$v),true) && $k!=='tong') $n++;
  $b = count($mine[$r['employee_info_id']] ?? []); $tot+=$n; $totm+=$b;
  if ($n!==$b) { $diff++; if($diff<=10) echo "LỆCH {$r['employee_info_id']}: màn=$n tool=$b\n"; } }
echo "NV ".count($ref)." · CT màn=$tot · tool=$totm · lệch $diff\n";
$extra = array_diff(array_keys($mine), array_column($ref,'employee_info_id')); echo "tool có NV ngoài DS màn: ".json_encode(array_values($extra))."\n";
