<?php
require 'vendor/autoload.php'; $app=require 'bootstrap/app.php'; $app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
foreach (array_slice($argv,1) as $n) { $c="Modules\\Agent\\Tools\\$n"; $d=(new $c)->definition()['description']; echo "== $n (".mb_strlen($d).")\n$d\n"; }
