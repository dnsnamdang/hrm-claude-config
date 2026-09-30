<?php
/**
 * Redmine #10840 — mã hàng tạm khi lưu/import báo giá.
 *
 * Luật sau khi sửa: mã hàng tạm CHỈ được giữ khi hàng đó đã có trên màn "Hàng hoá dự án"
 * của CÙNG dự án — tức nguồn là BOM tổng hợp ĐÃ DUYỆT hoặc báo giá tự lập ĐÃ DUYỆT/TRÚNG THẦU.
 * Nguồn còn nháp, hoặc khác dự án → sinh mã HHBG mới theo id.
 *
 * Chạy: php test_10840.php   (từ worktree hrm-api)
 */
$root = '/Users/manhcuong/Desktop/dns/HRM/worktrees/tpe-api';
require $root . '/vendor/autoload.php';
$app = require $root . '/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Http\Kernel::class);
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Http\Request;
use Modules\Assign\Entities\Quotation;
use Modules\Assign\Entities\BomList;

const TAG = 'TST10840';

$pass = 0; $fail = 0; $msgs = [];
function ok($cond, $name, $extra = '') {
    global $pass, $fail, $msgs;
    if ($cond) { $pass++; echo "  ✓ $name\n"; }
    else { $fail++; $msgs[] = $name . ($extra ? " | $extra" : ''); echo "  ✗ $name" . ($extra ? " | $extra" : '') . "\n"; }
}

function api($method, $uri, $payload, $employeeId) {
    global $kernel, $app;
    $tok = \Tymon\JWTAuth\Facades\JWTAuth::fromUser(\App\Models\TpEmployee::find($employeeId));
    \Illuminate\Support\Facades\Auth::forgetGuards();
    $req = Request::create($uri, $method, [], [], [], [
        'CONTENT_TYPE' => 'application/json',
        'HTTP_ACCEPT' => 'application/json',
        'HTTP_AUTHORIZATION' => 'Bearer ' . $tok,
    ], json_encode($payload));
    $app->instance('request', $req);
    // JWTAuth giữ request/token của lần gọi trước trong cùng tiến trình -> lần sau đổi tài khoản
    // vẫn chạy bằng user cũ (đã dính: emp2 lưu báo giá của chính mình bị "Chỉ người tạo mới sửa được").
    \Tymon\JWTAuth\Facades\JWTAuth::setRequest($req);
    \Tymon\JWTAuth\Facades\JWTAuth::unsetToken();
    // JWTGuard cache user của request trước trong cùng tiến trình -> ép đúng user của lượt này,
    // nếu không thì đổi tài khoản vẫn chạy bằng người cũ (đã dính: 422 "Chỉ người tạo mới sửa được").
    \Illuminate\Support\Facades\Auth::guard('api')->setUser(\App\Models\TpEmployee::find($employeeId));
    $res = $kernel->handle($req);
    \Illuminate\Support\Facades\Auth::forgetGuards();
    return [$res->getStatusCode(), json_decode($res->getContent(), true)];
}

// ---------------- dọn fixture cũ ----------------
function cleanup() {
    $qIds = DB::table('quotations')->where('code', 'like', TAG . '%')->pluck('id');
    if ($qIds->count()) {
        DB::table('quotation_product_prices')->whereIn('quotation_id', $qIds)->delete();
        DB::table('quotation_service_items')->whereIn('quotation_id', $qIds)->delete();
        DB::table('quotation_groups')->whereIn('quotation_id', $qIds)->delete();
        DB::table('quotations')->whereIn('id', $qIds)->delete();
    }
    $bIds = DB::table('bom_lists')->where('code', 'like', TAG . '%')->pluck('id');
    if ($bIds->count()) {
        DB::table('bom_list_products')->whereIn('bom_list_id', $bIds)->delete();
        DB::table('bom_lists')->whereIn('id', $bIds)->delete();
    }
    DB::table('prospective_projects')->where('name', 'like', TAG . '%')->delete();
}
cleanup();

// ---------------- fixture ----------------
$now = now();
$duAnA = DB::table('prospective_projects')->insertGetId([
    'name' => TAG . ' - Du an A', 'code' => TAG . '-DA-A', 'company_id' => 1,
    'created_at' => $now, 'updated_at' => $now,
]);
$duAnB = DB::table('prospective_projects')->insertGetId([
    'name' => TAG . ' - Du an B', 'code' => TAG . '-DA-B', 'company_id' => 1,
    'created_at' => $now, 'updated_at' => $now,
]);

/** Tạo báo giá tự lập trong dự án, theo trạng thái cho trước */
function mkQuotation($code, $projectId, $status, $employeeId) {
    $now = now();
    return DB::table('quotations')->insertGetId([
        'code' => $code, 'project_id' => $projectId, 'type' => Quotation::TYPE_SELF_BUILT,
        'bom_list_id' => null, 'is_summary' => 0, 'status' => $status,
        'company_id' => 1, 'price_type_id' => 1, 'exchange_rate' => 1,
        'created_by' => $employeeId, 'updated_by' => $employeeId,
        'created_at' => $now, 'updated_at' => $now,
    ]);
}

/** Thêm 1 dòng hàng tạm ĐÃ CÓ MÃ vào báo giá (mô phỏng dữ liệu nguồn của file Excel export) */
function mkTempRow($quotationId, $code, $name) {
    $now = now();
    return DB::table('quotation_product_prices')->insertGetId([
        'quotation_id' => $quotationId, 'code' => $code, 'name' => $name,
        'erp_product_id' => null, 'qty_needed' => 1, 'estimated_price' => 1000, 'quoted_price' => 1500,
        'created_at' => $now, 'updated_at' => $now,
    ]);
}

/** Payload lưu báo giá: 1 dòng hàng tạm MỚI mang mã lấy từ file Excel */
function payloadImport($code, $name) {
    return [
        'products' => [[
            'code' => $code, 'name' => $name, 'erp_product_id' => null,
            'qty_needed' => 1, 'estimated_price' => 1000, 'quoted_price' => 1500, 'vat_percent' => 8,
        ]],
    ];
}

function maSauKhiLuu($quotationId, $name) {
    return DB::table('quotation_product_prices')->where('quotation_id', $quotationId)->where('name', $name)->value('code');
}

// tài khoản test: người tạo báo giá + 1 người khác (quyền khác)
$emp1 = 34;    // Đào Thị Thúy
$emp2 = 101;   // Nguyễn Văn Thắng
foreach ([$emp1, $emp2] as $e) {
    // password_changed_at lùi về quá khứ: token tạo bằng fromUser() có iat = bây giờ,
    // trùng giây với thời điểm đổi mật khẩu thì middleware coi là phiên hết hạn (401).
    DB::table('employees')->where('id', $e)->update(['password' => Hash::make('Test@12345'), 'password_changed_at' => now()->subDay(), 'token_version' => 1]);
}

echo "Dự án A=$duAnA | Dự án B=$duAnB | tài khoản: $emp1, $emp2\n";

// ============ TC1: nguồn là báo giá NHÁP cùng dự án -> PHẢI sinh mã mới ============
echo "\nTC1 — Import mã hàng tạm lấy từ báo giá NHÁP cùng dự án\n";
$qNhap = mkQuotation(TAG . '-NHAP', $duAnA, Quotation::STATUS_DANG_TAO, $emp1);
$rowNhap = mkTempRow($qNhap, 'HHBG' . str_pad($qNhap, 6, '0', STR_PAD_LEFT), TAG . ' hang nhap');
$maNguon = DB::table('quotation_product_prices')->where('id', $rowNhap)->value('code');

$qDich1 = mkQuotation(TAG . '-DICH1', $duAnA, Quotation::STATUS_DANG_TAO, $emp1);
list($code, $body) = api('PUT', "/api/v1/assign/quotations/$qDich1", payloadImport($maNguon, TAG . ' hang dich 1'), $emp1);
$ma1 = maSauKhiLuu($qDich1, TAG . ' hang dich 1');
ok($code === 200, 'Lưu báo giá đích thành công', "code=$code");
ok($ma1 !== $maNguon, 'Sinh mã MỚI, không dùng lại mã của báo giá nháp', "nguồn=$maNguon | mới=$ma1");
ok($ma1 === 'HHBG' . str_pad(DB::table('quotation_product_prices')->where('quotation_id', $qDich1)->value('id'), 6, '0', STR_PAD_LEFT),
    'Mã mới đúng quy tắc HHBG + id của chính dòng', (string) $ma1);

// ============ TC2: nguồn là báo giá ĐÃ DUYỆT cùng dự án -> GIỮ mã ============
echo "\nTC2 — Import mã lấy từ báo giá ĐÃ DUYỆT cùng dự án (đã có trên màn Hàng hoá dự án)\n";
$qDuyet = mkQuotation(TAG . '-DUYET', $duAnA, Quotation::STATUS_DA_DUYET, $emp1);
mkTempRow($qDuyet, 'HHBG' . str_pad($qDuyet, 6, '0', STR_PAD_LEFT), TAG . ' hang duyet');
$maDuyet = DB::table('quotation_product_prices')->where('quotation_id', $qDuyet)->value('code');

$qDich2 = mkQuotation(TAG . '-DICH2', $duAnA, Quotation::STATUS_DANG_TAO, $emp1);
list($code) = api('PUT', "/api/v1/assign/quotations/$qDich2", payloadImport($maDuyet, TAG . ' hang dich 2'), $emp1);
$ma2 = maSauKhiLuu($qDich2, TAG . ' hang dich 2');
ok($ma2 === $maDuyet, 'GIỮ nguyên mã (BOM ↔ báo giá cùng dự án dùng chung mã)', "nguồn=$maDuyet | sau lưu=$ma2");

// ============ TC3: nguồn là báo giá TRÚNG THẦU cùng dự án -> GIỮ mã ============
echo "\nTC3 — Import mã lấy từ báo giá TRÚNG THẦU cùng dự án\n";
$qTrung = mkQuotation(TAG . '-TRUNG', $duAnA, Quotation::STATUS_TRUNG_THAU, $emp1);
mkTempRow($qTrung, 'HHBG' . str_pad($qTrung, 6, '0', STR_PAD_LEFT), TAG . ' hang trung thau');
$maTrung = DB::table('quotation_product_prices')->where('quotation_id', $qTrung)->value('code');

$qDich3 = mkQuotation(TAG . '-DICH3', $duAnA, Quotation::STATUS_DANG_TAO, $emp1);
api('PUT', "/api/v1/assign/quotations/$qDich3", payloadImport($maTrung, TAG . ' hang dich 3'), $emp1);
$ma3 = maSauKhiLuu($qDich3, TAG . ' hang dich 3');
ok($ma3 === $maTrung, 'GIỮ nguyên mã', "nguồn=$maTrung | sau lưu=$ma3");

// ============ TC4: nguồn là BOM tổng hợp ĐÃ DUYỆT cùng dự án -> GIỮ mã ============
echo "\nTC4 — Import mã lấy từ BOM tổng hợp ĐÃ DUYỆT cùng dự án\n";
$now = now();
$bomDuyet = DB::table('bom_lists')->insertGetId([
    'code' => TAG . '-BOM-DUYET', 'bom_list_type' => BomList::TYPE_AGGREGATE, 'status' => BomList::STATUS_DA_DUYET,
    'prospective_project_id' => $duAnA, 'company_id' => 1, 'created_by' => $emp1, 'updated_by' => $emp1,
    'created_at' => $now, 'updated_at' => $now,
]);
$maBom = 'HHBOMTEST01';
DB::table('bom_list_products')->insert([
    'bom_list_id' => $bomDuyet, 'code' => $maBom, 'name' => TAG . ' hang bom duyet',
    'erp_product_id' => null, 'qty_needed' => 1, 'created_at' => $now, 'updated_at' => $now,
]);
$qDich4 = mkQuotation(TAG . '-DICH4', $duAnA, Quotation::STATUS_DANG_TAO, $emp1);
api('PUT', "/api/v1/assign/quotations/$qDich4", payloadImport($maBom, TAG . ' hang dich 4'), $emp1);
$ma4 = maSauKhiLuu($qDich4, TAG . ' hang dich 4');
ok($ma4 === $maBom, 'GIỮ nguyên mã của BOM đã duyệt', "nguồn=$maBom | sau lưu=$ma4");

// ============ TC5: nguồn là BOM tổng hợp CHƯA DUYỆT -> sinh mã mới ============
echo "\nTC5 — Import mã lấy từ BOM tổng hợp CHƯA DUYỆT cùng dự án\n";
$bomNhap = DB::table('bom_lists')->insertGetId([
    'code' => TAG . '-BOM-NHAP', 'bom_list_type' => BomList::TYPE_AGGREGATE, 'status' => 1,
    'prospective_project_id' => $duAnA, 'company_id' => 1, 'created_by' => $emp1, 'updated_by' => $emp1,
    'created_at' => $now, 'updated_at' => $now,
]);
$maBomNhap = 'HHBOMNHAP01';
DB::table('bom_list_products')->insert([
    'bom_list_id' => $bomNhap, 'code' => $maBomNhap, 'name' => TAG . ' hang bom nhap',
    'erp_product_id' => null, 'qty_needed' => 1, 'created_at' => $now, 'updated_at' => $now,
]);
$qDich5 = mkQuotation(TAG . '-DICH5', $duAnA, Quotation::STATUS_DANG_TAO, $emp1);
api('PUT', "/api/v1/assign/quotations/$qDich5", payloadImport($maBomNhap, TAG . ' hang dich 5'), $emp1);
$ma5 = maSauKhiLuu($qDich5, TAG . ' hang dich 5');
ok($ma5 !== $maBomNhap && strpos((string) $ma5, 'HHBG') === 0, 'Sinh mã HHBG mới', "nguồn=$maBomNhap | sau lưu=$ma5");

// ============ TC6: KHÁC dự án (nguồn đã duyệt) -> vẫn sinh mã mới ============
echo "\nTC6 — Import mã của báo giá ĐÃ DUYỆT nhưng thuộc DỰ ÁN KHÁC\n";
$qDich6 = mkQuotation(TAG . '-DICH6', $duAnB, Quotation::STATUS_DANG_TAO, $emp1);
api('PUT', "/api/v1/assign/quotations/$qDich6", payloadImport($maDuyet, TAG . ' hang dich 6'), $emp1);
$ma6 = maSauKhiLuu($qDich6, TAG . ' hang dich 6');
ok($ma6 !== $maDuyet, 'Khác dự án -> sinh mã mới', "nguồn=$maDuyet | sau lưu=$ma6");

// ============ TC7: 2 báo giá nháp cùng dự án, cùng file -> 2 mã KHÁC NHAU (ca QA báo) ============
echo "\nTC7 — Ca QA: 2 báo giá nháp cùng dự án import cùng 1 file\n";
$qA = mkQuotation(TAG . '-QA-A', $duAnA, Quotation::STATUS_DANG_TAO, $emp1);
$qB = mkQuotation(TAG . '-QA-B', $duAnA, Quotation::STATUS_DANG_TAO, $emp2);
// Bước 1: emp1 tạo hàng tạm ở báo giá nháp A -> hệ thống sinh mã M
api('PUT', "/api/v1/assign/quotations/$qA", payloadImport('', TAG . ' hang QA'), $emp1);
$maA = maSauKhiLuu($qA, TAG . ' hang QA');
echo "    (mã sinh ở báo giá A: $maA)\n";
// Bước 2: export A ra Excel rồi import sang báo giá nháp B (cùng dự án) -> file mang đúng mã M
list($codeB, $bodyB) = api('PUT', "/api/v1/assign/quotations/$qB", payloadImport($maA, TAG . ' hang QA'), $emp2);
$maB = maSauKhiLuu($qB, TAG . ' hang QA');
echo "    (emp2 lưu báo giá của chính mình: HTTP $codeB" . ($codeB !== 200 ? ' — ' . json_encode($bodyB, JSON_UNESCAPED_UNICODE) : '') . ")\n";
ok($maA !== $maB, '2 báo giá ra 2 mã KHÁC NHAU (trước fix: trùng nhau)', "A=$maA | B=$maB");
ok($maB !== $maA, 'Không dùng lại mã ghi trong file Excel (mã của báo giá A)', "A=$maA | B=$maB");
ok(strpos((string) $maB, 'HHBG') === 0, 'Tài khoản khác (emp2) cũng sinh mã đúng quy tắc', (string) $maB);

// ============ TC8: nhiều dòng cùng "nhãn" mã trong 1 lượt -> dùng CHUNG 1 mã (Rule 3 giữ nguyên) ============
echo "\nTC8 — Nhiều dòng cùng nhãn mã trong cùng 1 lượt lưu (Rule 3 không bị phá)\n";
$qGom = mkQuotation(TAG . '-GOM', $duAnA, Quotation::STATUS_DANG_TAO, $emp1);
api('PUT', "/api/v1/assign/quotations/$qGom", ['products' => [
    ['code' => 'NHAN-GOM', 'name' => TAG . ' gom 1', 'erp_product_id' => null, 'qty_needed' => 1, 'estimated_price' => 100, 'quoted_price' => 200],
    ['code' => 'NHAN-GOM', 'name' => TAG . ' gom 2', 'erp_product_id' => null, 'qty_needed' => 2, 'estimated_price' => 100, 'quoted_price' => 200],
]], $emp1);
$maGom = DB::table('quotation_product_prices')->where('quotation_id', $qGom)->pluck('code')->unique()->values();
ok($maGom->count() === 1, '2 dòng cùng nhãn -> CHUNG 1 mã', $maGom->toJson());
ok(strpos((string) $maGom->first(), 'HHBG') === 0, 'Mã chung là mã HHBG tự sinh', (string) $maGom->first());

// ============ TC9: hàng ERP không bị đụng ============
echo "\nTC9 — Dòng hàng ERP giữ nguyên mã master data\n";
$erp = DB::table('quotation_product_prices')->whereNotNull('erp_product_id')->first();
if ($erp) {
    $qErp = mkQuotation(TAG . '-ERP', $duAnA, Quotation::STATUS_DANG_TAO, $emp1);
    api('PUT', "/api/v1/assign/quotations/$qErp", ['products' => [[
        'code' => $erp->code, 'name' => TAG . ' hang erp', 'erp_product_id' => $erp->erp_product_id,
        'qty_needed' => 1, 'estimated_price' => 0, 'quoted_price' => 0,
    ]]], $emp1);
    $maErp = maSauKhiLuu($qErp, TAG . ' hang erp');
    ok($maErp === $erp->code, 'Hàng ERP giữ nguyên mã, không sinh HHBG', "gốc={$erp->code} | sau lưu=$maErp");
} else {
    echo "  (bỏ qua: local không có dòng hàng ERP mẫu)\n";
}

// ---------------- tổng kết + dọn ----------------
echo "\n==============================\nPASS: $pass | FAIL: $fail\n";
foreach ($msgs as $m) echo " - $m\n";
cleanup();
$left = DB::table('quotations')->where('code', 'like', TAG . '%')->count()
    + DB::table('bom_lists')->where('code', 'like', TAG . '%')->count()
    + DB::table('prospective_projects')->where('name', 'like', TAG . '%')->count();
echo "Đã dọn fixture, còn sót: $left\n";
exit($fail > 0 ? 1 : 0);
