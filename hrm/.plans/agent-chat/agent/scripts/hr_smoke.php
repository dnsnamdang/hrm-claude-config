<?php
require 'vendor/autoload.php'; $app=require 'bootstrap/app.php'; $app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
auth()->onceUsingId((int)$argv[1]); $cls = 'Modules\\Agent\\Tools\\'.$argv[2]; $t = new $cls; $in = json_decode($argv[3], true);
$need = $t->permissionNeed($in); if ($need) { echo "DENY: ",$need->reason,"\n"; exit; }
$s=microtime(true); $r = $t->run($in); $d = $r->data;
foreach (['groups','employees','by_department','trips','by_group'] as $k) if (isset($d[$k]) && is_array($d[$k])) $d[$k] = array_slice($d[$k],0,3);
printf("%s %.2fs %s\n  block: %s\n", $r->outcome, microtime(true)-$s, json_encode($d, JSON_UNESCAPED_UNICODE), json_encode(array_slice($r->block['items'] ?? [],0,3), JSON_UNESCAPED_UNICODE));
