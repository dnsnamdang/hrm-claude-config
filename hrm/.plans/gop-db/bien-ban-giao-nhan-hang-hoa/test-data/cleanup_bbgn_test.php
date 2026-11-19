<?php
/**
 * Xoá dữ liệu TEST do seed_bbgn_test.php tạo — CHỈ theo id trong manifest.json.
 * Biên bản giao nhận bạn tự tạo trên các HĐ test (contract_id thuộc manifest) cũng bị xoá kèm dòng hàng / serial / lịch sử,
 * vì HĐ gốc của chúng không còn. Serial đã ghi vào bảng `serials` chung khi "Lưu và duyệt" được liệt kê để bạn tự quyết.
 */
$manifestFile = __DIR__ . '/manifest.json';
if (!file_exists($manifestFile)) {
    echo "Không có manifest.json — không có gì để xoá.\n";
    return;
}
$m = json_decode(file_get_contents($manifestFile), true);
$ids = function ($t) use ($m) {
    return $m[$t] ?? [];
};

DB::beginTransaction();
try {
    // Biên bản tạo trên HĐ test
    $recs = DB::table('handover_acceptance_product_records')
        ->where(function ($q) use ($ids) {
            $q->where(function ($w) use ($ids) {
                $w->where('contract_type', 'App\\Model\\Sale\\Firm\\Contract\\FirmContract')->whereIn('contract_id', $ids('firm_contracts') ?: [0]);
            })->orWhere(function ($w) use ($ids) {
                $w->where('contract_type', 'Modules\\Assign\\Entities\\Contract\\Contract')->whereIn('contract_id', $ids('hrm_contracts') ?: [0]);
            });
        })->get(['id', 'code']);
    $recIds = $recs->pluck('id')->all();
    if ($recIds) {
        $detIds = DB::table('handover_acceptance_product_record_details')->whereIn('parent_id', $recIds)->pluck('id')->all();
        $serials = DB::table('handover_acceptance_product_record_serials')->whereIn('detail_id', $detIds ?: [0])->pluck('serial_number')->all();
        if ($serials) {
            $core = DB::table('serials')->whereIn('serial_number', $serials)->get(['id', 'serial_number']);
            echo 'Serial trong bảng serials chung (KHÔNG tự xoá, xem lại): ' . json_encode($core) . "\n";
        }
        DB::table('handover_acceptance_product_record_serials')->whereIn('detail_id', $detIds ?: [0])->delete();
        DB::table('handover_acceptance_product_record_details')->whereIn('parent_id', $recIds)->delete();
        DB::table('catalog_histories')->where('table_name', 'handover_acceptance_product_records')->whereIn('table_id', $recIds)->delete();
        DB::table('handover_acceptance_product_records')->whereIn('id', $recIds)->delete();
        echo 'Đã xoá biên bản test: ' . $recs->pluck('code')->implode(', ') . "\n";
    }

    // Quyền + vai trò tạm
    foreach ($ids('roles') as $roleId) {
        DB::table('employee_has_roles')->where('role_id', $roleId)->delete();
        DB::table('role_has_permissions')->where('role_id', $roleId)->delete();
        DB::table('roles')->where('id', $roleId)->delete();
    }

    foreach (['product_export_request_details', 'product_export_requests', 'hrm_contract_product_prices', 'hrm_contracts',
        'quotations', 'firm_contract_tab_products', 'firm_contracts'] as $t) {
        $n = $ids($t) ? DB::table($t)->whereIn('id', $ids($t))->delete() : 0;
        echo "$t: xoá $n\n";
    }
    DB::commit();
} catch (\Throwable $e) {
    DB::rollBack();
    echo 'LỖI, đã rollback: ' . $e->getMessage() . "\n";

    return;
}
unlink($manifestFile);
echo "Xong, đã xoá manifest.json\n";
