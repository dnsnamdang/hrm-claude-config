<?php
/**
 * Dữ liệu TEST local cho màn Biên bản giao nhận hàng hóa — đứng tên namdangit (employee 13), công ty 1.
 * Chạy: php artisan tinker --execute='require "<đường dẫn file này>";'
 * Xoá:  php artisan tinker --execute='require "<thư mục>/cleanup_bbgn_test.php";'
 *
 * CHỈ THÊM dòng mới (nhân bản từ dữ liệu có sẵn), không sửa dòng nào đang có. Mọi id thêm ghi vào manifest.json
 * để cleanup xoá đúng theo id.
 *   - 2 HĐ hãng (nhân bản fc 24823: 6 hàng xuất đủ; fc 24813: 16 hàng, mới xuất 7) + phiếu YCXH đã hạch toán (type 14)
 *   - 1 HĐ HRM (nhân bản hrm_contracts 1) + 7 dòng hàng + phiếu YCXH loại 21 đã hạch toán (xuất 1 phần)
 *   - Vai trò tạm "TEST BBGN" công ty 1 + quyền customer_care.bien_ban_giao_nhan.view mức Tổng công ty, gán cho employee 13
 */
$manifestFile = __DIR__ . '/manifest.json';
if (file_exists($manifestFile)) {
    echo "Đã có manifest.json — chạy cleanup trước khi seed lại.\n";
    return;
}

$ME = 13;
$COMPANY = 1;
$now = now()->format('Y-m-d H:i:s');
$tag = 'TEST-BBGN';
$m = [];
$add = function ($table, $id) use (&$m) {
    $m[$table][] = (int) $id;
};
$clone = function ($table, $id, array $over) use ($add) {
    $row = (array) DB::table($table)->where('id', $id)->first();
    if (!$row) {
        throw new RuntimeException("Không thấy $table#$id");
    }
    unset($row['id']);
    $newId = DB::table($table)->insertGetId(array_merge($row, $over));
    $add($table, $newId);

    return $newId;
};

DB::beginTransaction();
try {
    // ---------------------------------------------------------------- HĐ hãng
    $firmSources = [
        ['fc' => 24823, 'ex' => 35525, 'suffix' => '01'],
        ['fc' => 24813, 'ex' => 35516, 'suffix' => '02'],
    ];
    foreach ($firmSources as $src) {
        $code = "HĐ_{$tag}_HANG_{$src['suffix']}";
        $fcId = $clone('firm_contracts', $src['fc'], [
            'code' => $code, 'created_by' => $ME, 'company_id' => $COMPANY, 'status' => 3,
            'customer_contact_name' => 'Nguyễn Văn Nhận (test)', 'customer_contact_phone' => '0900000001',
            'created_at' => $now, 'updated_at' => $now,
        ]);
        foreach (DB::table('firm_contract_tab_products')->where('firm_contract_id', $src['fc'])->pluck('id') as $tp) {
            $orig = DB::table('firm_contract_tab_products')->where('id', $tp)->value('root_firm_contract_id');
            $clone('firm_contract_tab_products', $tp, [
                'firm_contract_id' => $fcId,
                'root_firm_contract_id' => $orig ? $fcId : null,
            ]);
        }
        $exId = $clone('product_export_requests', $src['ex'], [
            'code' => "YCXH-{$tag}-HANG-{$src['suffix']}", 'firm_contract_id' => $fcId, 'company_id' => $COMPANY,
            'status' => 5, 'type' => 14, 'need_repair' => 0,
        ]);
        foreach (DB::table('product_export_request_details')->where('parent_id', $src['ex'])->pluck('id') as $d) {
            $clone('product_export_request_details', $d, ['parent_id' => $exId]);
        }
        echo "HĐ hãng $code (id $fcId), YCXH id $exId\n";
    }

    // ---------------------------------------------------------------- HĐ HRM
    $hrmCode = "HĐ-{$tag}-HRM-01";
    // hrm_contracts.quotation_id NOT NULL + UNIQUE → báo giá test riêng (không gắn vào báo giá thật)
    $qId = $clone('quotations', 36, [
        'code' => "BG-{$tag}-01", 'customer_id' => DB::table('hrm_contracts')->where('id', 1)->value('customer_id'),
        'created_by' => $ME, 'company_id' => $COMPANY, 'created_at' => $now, 'updated_at' => $now,
    ]);
    $hcId = $clone('hrm_contracts', 1, [
        'code' => $hrmCode, 'created_by' => $ME, 'company_id' => $COMPANY, 'status' => 6,
        'quotation_id' => $qId, 'code_input' => $hrmCode, 'signed_file_name' => null, 'signed_file_path' => null,
        'description' => 'HĐ test màn Biên bản giao nhận hàng hóa (seed_bbgn_test.php) — xoá bằng cleanup_bbgn_test.php',
        'customer_contact_name' => 'Trần Thị Nhận (test)', 'customer_contact_phone' => '0900000002',
        'created_at' => $now, 'updated_at' => $now,
    ]);
    // Hàng lấy theo phiếu xuất 35525 (6 hàng) + 1 máy hàn bắt buộc serial (27869) để thử Nhập seri
    $lines = DB::table('product_export_request_details')->where('parent_id', 35525)->where('need_export', 1)
        ->get(['product_id', 'unit_id', 'unit_name', 'product_name', 'code'])->map(function ($r) {
            return (array) $r;
        })->all();
    $weld = DB::table('product_export_request_details')->where('product_id', 27869)->whereNotNull('unit_id')
        ->orderByDesc('id')->first(['product_id', 'unit_id', 'unit_name', 'product_name', 'code']);
    if ($weld) {
        $lines[] = (array) $weld;
    }
    $exHrm = $clone('product_export_requests', 35525, [
        'code' => "YCXH-{$tag}-HRM-01", 'type' => 21, 'status' => 5, 'need_repair' => 0, 'company_id' => $COMPANY,
        'firm_contract_id' => null, 'wr_service_contract_id' => null,
        'emplement_contract_id' => $hcId, 'emplement_contract_type' => 'Modules\\Assign\\Entities\\Contract\\Contract',
    ]);
    $tplDetail = (array) DB::table('product_export_request_details')->where('parent_id', 35525)->where('need_export', 1)->first();
    unset($tplDetail['id']);
    foreach ($lines as $i => $l) {
        $contractQty = 10;
        $exported = $i % 2 === 0 ? 10 : 4; // xen kẽ xuất đủ / xuất 1 phần
        $cpp = DB::table('hrm_contract_product_prices')->insertGetId([
            'contract_id' => $hcId, 'parent_id' => null, 'erp_product_id' => $l['product_id'], 'unit_id' => $l['unit_id'],
            'name' => $l['product_name'], 'code' => $l['code'], 'qty_needed' => $contractQty, 'sort_order' => $i + 1,
            'created_by' => $ME, 'created_at' => $now, 'updated_at' => $now,
        ]);
        $add('hrm_contract_product_prices', $cpp);
        $det = DB::table('product_export_request_details')->insertGetId(array_merge($tplDetail, [
            'parent_id' => $exHrm, 'product_id' => $l['product_id'], 'unit_id' => $l['unit_id'],
            'product_name' => $l['product_name'], 'code' => $l['code'], 'unit_name' => $l['unit_name'],
            'firm_contract_tab_product_id' => null,
            'qty' => $exported, 'exported_qty' => $exported, 'need_export' => 1,
        ]));
        $add('product_export_request_details', $det);
    }
    echo "HĐ HRM $hrmCode (id $hcId), YCXH loại 21 id $exHrm, " . count($lines) . " hàng\n";

    // ---------------------------------------------------------------- Quyền xem (vai trò tạm công ty 1)
    $roleId = DB::table('roles')->insertGetId([
        'name' => 'TEST BBGN - Xem biên bản giao nhận', 'guard_name' => 'api', 'status' => 1, 'company_id' => $COMPANY,
        'created_by' => $ME, 'created_at' => $now, 'updated_at' => $now,
    ]);
    $add('roles', $roleId);
    $permId = DB::table('permissions')->where('code', 'customer_care.bien_ban_giao_nhan.view')->value('id');
    DB::table('role_has_permissions')->insert(['role_id' => $roleId, 'permission_id' => $permId, 'company_id' => $COMPANY, 'scope' => 4]);
    DB::table('employee_has_roles')->insert([
        'role_id' => $roleId, 'employee_id' => $ME, 'company_id' => $COMPANY, 'position' => 0,
        'model_type' => 'Modules\\Timesheet\\Entities\\Employee',
    ]);
    echo "Vai trò tạm id $roleId + quyền xem (mức Tổng công ty) cho employee $ME\n";

    DB::commit();
} catch (\Throwable $e) {
    DB::rollBack();
    echo 'LỖI, đã rollback: ' . $e->getMessage() . "\n";

    return;
}

file_put_contents($manifestFile, json_encode($m, JSON_PRETTY_PRINT));
echo "Đã ghi manifest.json\n";
