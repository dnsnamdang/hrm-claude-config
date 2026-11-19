<?php
require "vendor/autoload.php"; $app=require "bootstrap/app.php"; $app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
$nos = array_map('intval', explode(',', $argv[1]));
$all = json_decode(file_get_contents(module_path('Agent','Tests/fixtures/eval/questions.json')), true);
$cmd = app(Modules\Agent\Console\AgentEvalCommand::class);
$cfg = app(Modules\Agent\Services\AgentModelResolver::class)->current(); // runOne cần cấu hình model từ 15/11 (chọn model)
$m = new ReflectionMethod($cmd, 'runOne'); $m->setAccessible(true);
echo (config('agent.fake') ? 'GIẢ' : 'THẬT').' · '.config('agent.model')."\n";
$ok = $kok = 0; $cost = 0;
foreach ($nos as $no) {
  $r = $m->invoke($cmd, $no, $all[$no-1], $cfg);
  $ok += $r['tool_ok']; $kok += $r['kind_ok']; $cost += $r['cost'];
  printf("#%d %s%s %s→%s [%s] %.1f₫ %s\n", $no, $r['tool_ok']?'✓':'✗', $r['kind_ok']?'✓':'✗', $r['expect_kind'], $r['kind'], implode(',', $r['tools']), $r['cost'], mb_substr($r['question'],0,60));
}
printf("Công cụ %d/%d · kind %d/%d · tổng %.0f₫ (%.2f₫/câu)\n", $ok, count($nos), $kok, count($nos), $cost, $cost/count($nos));
