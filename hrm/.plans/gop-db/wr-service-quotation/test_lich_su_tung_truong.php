<?php
$base='/Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-api';
require $base.'/vendor/autoload.php';
$app=require_once $base.'/bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

use Illuminate\Support\Facades\DB;
use Modules\CustomerCare\Entities\WrServiceQuotation\WrServiceQuotation;
use Modules\CustomerCare\Services\WrServiceQuotationService;
use App\Services\CatalogHistoryService;

$ID = 3785;
$m = WrServiceQuotation::find($ID);
Auth::setUser(App\Models\TpEmployee::find($m->created_by ?: 13));
$svc = app(WrServiceQuotationService::class);

function payloadOf($id) {
    $m = WrServiceQuotation::find($id);
    $m->load(['productRepairs.chooseProductItems','productRepairs.chooseServices',
              'productWarrantys.chooseProductItems','productWarrantys.chooseServices',
              'extendProducts.services.products','costs']);
    $mk = function($p) {
        $r = $p->toArray();
        $r['choose_product_items'] = $p->chooseProductItems->map(function($i){ return $i->toArray(); })->all();
        $r['choose_services'] = $p->chooseServices->map(function($s){ return $s->toArray(); })->all();
        return $r;
    };
    return [
        'code' => $m->code, 'customer_id' => $m->customer_id, 'customer_name' => $m->customer_name,
        'customer_contact_name' => $m->customer_contact_name,
        'customer_contact_phones' => $m->customer_contact_phones,
        'delivery_place' => $m->delivery_place, 'quotation_term' => $m->quotation_term,
        'note' => $m->note, 'footer' => $m->footer, 'status' => $m->status,
        'product_repairs' => $m->productRepairs->map($mk)->all(),
        'product_warrantys' => $m->productWarrantys->map($mk)->all(),
        'extend_products' => $m->extendProducts->map(function($d){
            $r = $d->toArray();
            $r['services'] = $d->services->map(function($s){
                $x = $s->toArray();
                $x['products'] = $s->products->map(function($i){ return $i->toArray(); })->all();
                return $x;
            })->all();
            return $r;
        })->all(),
        'costs' => $m->costs->map(function($c){ return $c->toArray(); })->all(),
    ];
}

function logText($id) {
    $out = app(CatalogHistoryService::class)->getLogs('wr_service_quotations', $id);
    if (!$out) return '(khong co log)';
    $log = $out[0];
    $lines = [];
    foreach ($log['changes'] as $c) {
        foreach (['added','removed'] as $g) {
            foreach (($c[$g.'_rows'] ?? []) as $r) {
                $lines[] = $c[$g.'_label'].': '.$r['name'].($r['detail'] ? ' — '.$r['detail'] : '');
            }
        }
        foreach (($c['changed'] ?? []) as $ch) {
            foreach ($ch['fields'] as $f) {
                $lines[] = $c['changed_label'].': '.$ch['name'].': '.$f['field'].': '.$f['old'].' -> '.$f['new'];
            }
        }
        if (empty($c['added_rows']) && empty($c['removed_rows']) && empty($c['changed'])) {
            $lines[] = $c['field'].': '.mb_substr((string)$c['old'],0,25).' -> '.mb_substr((string)$c['new'],0,25);
        }
    }
    return implode(' || ', $lines) ?: '(khong ghi gi)';
}

$cases = [
    // ---- bảng chính ----
    ['CHINH customer_contact_name', function(&$d){ $d['customer_contact_name'] = 'NGUOI LH TEST'; }],
    ['CHINH customer_contact_phones', function(&$d){ $d['customer_contact_phones'] = '0900000000'; }],
    ['CHINH delivery_place', function(&$d){ $d['delivery_place'] = 'DIA CHI TEST'; }],
    ['CHINH note', function(&$d){ $d['note'] = 'GHI CHU TEST'; }],
    // ---- dòng thiết bị ----
    ['THIETBI serial', function(&$d){ $d['product_repairs'][0]['serial'] = 'SR-TEST'; }],
    ['THIETBI so BBBGNT', function(&$d){ $d['product_repairs'][0]['handover_acceptance_record_code'] = 'BB-TEST'; }],
    ['THIETBI so luong cong', function(&$d){ $d['product_repairs'][0]['engineering_work_qty'] = 7; }],
    ['THIETBI don gia cong', function(&$d){ $d['product_repairs'][0]['sell_engineering_work'] = 123456; }],
    ['THIETBI chiet khau', function(&$d){ $d['product_repairs'][0]['discount_cost'] = 999; }],
    ['THIETBI vat', function(&$d){ $d['product_repairs'][0]['vat_percent'] = 10; }],
    ['THIETBI xoa 1 dong', function(&$d){ array_pop($d['product_repairs']); }],
    // ---- vật tư của thiết bị ----
    ['VATTU so luong', function(&$d){ $d['product_repairs'][0]['choose_product_items'][0]['quantity'] = 9; }],
    ['VATTU don gia ban', function(&$d){ $d['product_repairs'][0]['choose_product_items'][0]['sell_price'] = 777; }],
    ['VATTU chiet khau', function(&$d){ $d['product_repairs'][0]['choose_product_items'][0]['discount_cost'] = 55; }],
    ['VATTU vat', function(&$d){ $d['product_repairs'][0]['choose_product_items'][0]['vat_percent'] = 5; }],
    ['VATTU thoi gian co vat tu', function(&$d){ $d['product_repairs'][0]['choose_product_items'][0]['time_to_has'] = 42; }],
    ['VATTU ghi chu', function(&$d){ $d['product_repairs'][0]['choose_product_items'][0]['note'] = 'note vat tu'; }],
    ['VATTU DVT', function(&$d){ $d['product_repairs'][0]['choose_product_items'][0]['unit_name'] = 'Bo'; }],
    ['VATTU them moi', function(&$d){
        $x = $d['product_repairs'][0]['choose_product_items'][0];
        $x['id']=null; $x['product_id']=4503; $x['product_name']='VAT TU MOI'; $d['product_repairs'][0]['choose_product_items'][]=$x; }],
    ['VATTU xoa', function(&$d){ $d['product_repairs'][0]['choose_product_items'] = []; }],
    // ---- dịch vụ của thiết bị ----
    ['DICHVU so luong', function(&$d){ $d['product_repairs'][0]['choose_services'][0]['quantity'] = 4; }],
    ['DICHVU don gia ban', function(&$d){ $d['product_repairs'][0]['choose_services'][0]['sell_price'] = 888; }],
    ['DICHVU thoi gian co vat tu', function(&$d){ $d['product_repairs'][0]['choose_services'][0]['time_to_has'] = 11; }],
    ['DICHVU ghi chu', function(&$d){ $d['product_repairs'][0]['choose_services'][0]['note'] = 'note dv'; }],
    ['DICHVU xoa', function(&$d){ $d['product_repairs'][0]['choose_services'] = []; }],
    // ---- thiết bị bảo dưỡng ----
    ['BAODUONG serial', function(&$d){ $d['extend_products'][0]['serial'] = 'SR-BD'; $d['extend_products'][0]['serial_id']=null; $d['extend_products'][0]['add_serial']=1; }],
    ['BAODUONG xoa thiet bi', function(&$d){ $d['extend_products'] = []; }],
    // ---- gói bảo dưỡng ----
    ['GOI so luong', function(&$d){ $d['extend_products'][0]['services'][0]['quantity'] = 3; }],
    ['GOI don gia', function(&$d){ $d['extend_products'][0]['services'][0]['price'] = 555; }],
    ['GOI chiet khau', function(&$d){ $d['extend_products'][0]['services'][0]['discount_cost'] = 66; }],
    ['GOI ghi chu', function(&$d){ $d['extend_products'][0]['services'][0]['note'] = 'note goi'; }],
    ['GOI xoa', function(&$d){ $d['extend_products'][0]['services'] = []; }],
    // ---- vật tư của gói ----
    ['VTGOI so luong', function(&$d){ foreach ($d['extend_products'][0]['services'] as $i=>$s) { if ($s['products']) { $d['extend_products'][0]['services'][$i]['products'][0]['qty'] = 8; break; } } }],
    ['VTGOI don gia', function(&$d){ foreach ($d['extend_products'][0]['services'] as $i=>$s) { if ($s['products']) { $d['extend_products'][0]['services'][$i]['products'][0]['price'] = 321; break; } } }],
    ['VTGOI ghi chu', function(&$d){ foreach ($d['extend_products'][0]['services'] as $i=>$s) { if ($s['products']) { $d['extend_products'][0]['services'][$i]['products'][0]['note'] = 'note vt goi'; break; } } }],
    ['VTGOI xoa', function(&$d){ foreach ($d['extend_products'][0]['services'] as $i=>$s) { if ($s['products']) { $d['extend_products'][0]['services'][$i]['products'] = []; break; } } }],
    // ---- chi phí khác ----
    ['CHIPHI gia tri', function(&$d){ $d['costs'][0]['price'] = 24680; }],
    ['CHIPHI bao hanh', function(&$d){ $d['costs'][0]['warranty_price'] = 111; }],
    ['CHIPHI mien phi', function(&$d){ $d['costs'][0]['free_price'] = 222; }],
    ['CHIPHI khong mien phi', function(&$d){ $d['costs'][0]['not_free_price'] = 333; }],
    ['CHIPHI cho SC-BD', function(&$d){ $d['costs'][0]['repair_price'] = 444; }],
    ['CHIPHI KH phai tra', function(&$d){ $d['costs'][0]['total_price'] = 555; }],
    ['CHIPHI ghi chu', function(&$d){ $d['costs'][0]['note'] = 'note chi phi'; }],
    ['CHIPHI xoa 1 khoan', function(&$d){ array_pop($d['costs']); }],
    // ---- thêm dòng mới ----
    ['THIETBI them moi', function(&$d){
        $x = $d['product_repairs'][0]; $x['id']=null; $x['product_id']=4503; $x['product_name']='THIET BI MOI';
        $x['choose_product_items']=[]; $x['choose_services']=[]; $d['product_repairs'][]=$x; }],
    ['DICHVU them moi', function(&$d){
        $x = $d['product_repairs'][0]['choose_services'][0]; $x['id']=null; $x['cost_id']=99999; $x['cost_name']='DICH VU MOI';
        $d['product_repairs'][0]['choose_services'][]=$x; }],
    ['CHIPHI them moi', function(&$d){
        $x = $d['costs'][0]; $x['id']=null; $x['cost_id']=1; $d['costs'][]=$x; }],
    ['GOI them moi', function(&$d){
        $x = $d['extend_products'][0]['services'][0]; $x['id']=null; $x['service_id']=99999; $x['service_name']='GOI MOI';
        $x['products']=[]; $d['extend_products'][0]['services'][]=$x; }],
    ['VTGOI them moi', function(&$d){
        foreach ($d['extend_products'][0]['services'] as $i=>$s) { if ($s['products']) {
            $x = $s['products'][0]; $x['id']=null; $x['product_id']=4503;
            $d['extend_products'][0]['services'][$i]['products'][]=$x; break; } } }],
    ['BAODUONG them thiet bi', function(&$d){
        $x = $d['extend_products'][0]; $x['id']=null; $x['product_id']=4503; $x['product_name']='TB BAO DUONG MOI';
        $x['services']=[]; $d['extend_products'][]=$x; }],
    // ---- cột chính còn lại ----
    ['CHINH code', function(&$d){ $d['code'] = 'MA-TEST-001'; }],
    ['CHINH footer', function(&$d){ $d['footer'] = '<div>Ghi chu moi</div>'; }],
    ['CHINH quotation_term', function(&$d){ $d['quotation_term'] = 99; }],
    ['CHINH customer_name', function(&$d){ $d['customer_name'] = 'KHACH TEST'; }],
    // ---- đổi NHIỀU trường trong 1 lần lưu -> 1 dòng log, nhiều khoá ----
    ['DOI NHIEU TRUONG 1 LUC', function(&$d){
        $d['note'] = 'n1';
        $d['product_repairs'][0]['serial'] = 'S1';
        $d['product_repairs'][0]['choose_product_items'][0]['quantity'] = 3;
        $d['costs'][0]['price'] = 111; }],
    // ---- không đổi gì ----
    ['KHONG DOI GI', function(&$d){ }],
    ['LUU LAI 2 LAN LIEN TIEP (lan 2 phai khong co log)', function(&$d){ }],
];

foreach ($cases as [$ten, $sua]) {
    DB::beginTransaction();
    try {
        $data = payloadOf($ID);
        $sua($data);
        $model = WrServiceQuotation::find($ID);
        $maxLog = (int) DB::table('catalog_histories')->max('id');
        $svc->update($model, $data);
        $soLog = DB::table('catalog_histories')->where('id','>',$maxLog)->count();
        $txt = $soLog ? logText($ID) : '(KHONG GHI LOG)';
        printf("%-30s | log=%d | %s\n", $ten, $soLog, mb_substr($txt, 0, 190));
    } catch (\Throwable $e) {
        printf("%-30s | LOI: %s\n", $ten, mb_substr($e->getMessage(), 0, 120));
    }
    DB::rollBack();
}
