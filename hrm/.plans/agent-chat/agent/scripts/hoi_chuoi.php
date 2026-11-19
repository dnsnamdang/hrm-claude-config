<?php
require "vendor/autoload.php"; $app=require "bootstrap/app.php"; $app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
use Modules\Agent\Entities\{AgentConversation, AgentTurn, AgentToolCall};
$emp=13; $qs=['Bảng công tháng 10 của tôi','tháng 9','tôi muốn xem chi tiết công tháng 9','Tôi muốn xem lịch sử chấm công của Ngô Thị Lý trong tháng 9'];
auth()->onceUsingId($emp); $cid=(int) auth()->user()->current_company_role;
$c = AgentConversation::create(['employee_id'=>$emp,'company_id'=>$cid,'title'=>'[thử] chuỗi công','created_by'=>$emp]);
try { foreach ($qs as $q) {
  App\Support\RequestCache::flush(); App\Support\Permissions\PermissionChecker::flush();
  $t = AgentTurn::create(['conversation_id'=>$c->id,'employee_id'=>$emp,'company_id'=>$cid,'question'=>$q,'status'=>AgentTurn::STATUS_QUEUED,'created_by'=>$emp]);
  app(Modules\Agent\Services\AgentRunner::class)->run($t, function(){}); $t=$t->fresh();
  echo "=== $q\n"; foreach (AgentToolCall::where('turn_id',$t->id)->orderBy('id')->get() as $tc) echo "  · {$tc->tool} ".json_encode($tc->input, JSON_UNESCAPED_UNICODE)." → {$tc->outcome} ({$tc->rows})\n";
  echo "  kind={$t->kind} ".round($t->cost_vnd,1)."₫\n  ".str_replace("\n","\n  ",trim($t->answer_text))."\n";
} } finally { $ids=AgentTurn::where('conversation_id',$c->id)->pluck('id'); AgentToolCall::whereIn('turn_id',$ids)->delete(); AgentTurn::whereIn('id',$ids)->delete(); $c->delete(); }
