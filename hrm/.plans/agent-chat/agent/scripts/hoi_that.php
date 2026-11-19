<?php
require "vendor/autoload.php"; $app=require "bootstrap/app.php"; $app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
use Modules\Agent\Entities\{AgentConversation, AgentTurn, AgentToolCall};
$qs = [[13,'Phòng nào có máy chiếu còn trống trong hôm nay?'],[835,'Phòng họp Lớn hôm nay ai đặt, để làm gì?'],[13,'Ngày mai phòng nào có tivi còn trống buổi chiều?'],[157,'Có phiếu đặt phòng họp nào đang chờ tôi duyệt không?']];
foreach ($qs as [$emp,$q]) {
  App\Support\RequestCache::flush(); App\Support\Permissions\PermissionChecker::flush(); auth()->forgetGuards(); auth()->onceUsingId($emp);
  $cid = (int) auth()->user()->current_company_role;
  $c = AgentConversation::create(['employee_id'=>$emp,'company_id'=>$cid,'title'=>'[thử] '.$q,'created_by'=>$emp]);
  $t = AgentTurn::create(['conversation_id'=>$c->id,'employee_id'=>$emp,'company_id'=>$cid,'question'=>$q,'status'=>AgentTurn::STATUS_QUEUED,'created_by'=>$emp]);
  try {
    app(Modules\Agent\Services\AgentRunner::class)->run($t, function(){});
    $t = $t->fresh();
    echo "=== NV$emp: $q\n";
    foreach (AgentToolCall::where('turn_id',$t->id)->orderBy('id')->get() as $tc) echo "  · {$tc->tool} ".json_encode($tc->input, JSON_UNESCAPED_UNICODE)." → {$tc->outcome} ({$tc->rows})\n";
    echo "  kind={$t->kind} ".round($t->cost_vnd,1)."₫\n  ".str_replace("\n","\n  ",trim($t->answer_text))."\n";
  } finally { AgentToolCall::where('turn_id',$t->id)->delete(); AgentTurn::where('id',$t->id)->delete(); $c->delete(); }
}
