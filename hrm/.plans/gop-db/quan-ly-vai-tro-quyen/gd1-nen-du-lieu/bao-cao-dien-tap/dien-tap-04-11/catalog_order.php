<?php
$files = glob($argv[1].'/app/Support/Permissions/Catalog/*.php'); sort($files, SORT_STRING);
$o = []; $i = 0;
foreach ($files as $f) foreach ((require $f) as $e) $o[$e['code']] = $i++;
echo json_encode($o);
