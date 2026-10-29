#!/bin/bash
# Đối chiếu "Có thể LR" HRM (ProductStockExtraReader) với ERP (App\Product::getJoinStockDetail) cho MỌI hàng có công thức.
# Cả 2 repo phải trỏ cùng DB local_hrm_erp. In: tong=... lech=0 là đạt.
PHP=/opt/homebrew/Cellar/php@7.4/7.4.33_9/bin/php
OUT=$(mktemp)
cd /Users/manhcuong/Desktop/dns/HRM/TanPhatDev && $PHP -d memory_limit=2G artisan tinker --execute='$o=[]; foreach(DB::table("recipe_products")->distinct()->pluck("base_product_id") as $id){ $o[$id]=App\Product::getJoinStockDetail($id)["join_qty"]; } file_put_contents("'$OUT'", json_encode($o));' >/dev/null 2>&1
cd /Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-api && $PHP -d memory_limit=2G artisan tinker --execute='$e=json_decode(file_get_contents("'$OUT'"),true); $h=app(Modules\MasterData\Services\Product\ProductStockExtraReader::class)->joinQty(array_keys($e)); $bad=0; foreach($e as $id=>$q){ if((float)$q!=(float)($h[$id]??-1)) $bad++; } echo "tong=",count($e)," khac0=",count(array_filter($e))," lech=$bad\n";' 2>&1 | tail -1
rm -f $OUT
