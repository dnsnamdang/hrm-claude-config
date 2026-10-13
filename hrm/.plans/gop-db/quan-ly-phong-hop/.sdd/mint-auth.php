<?php
// mint-auth.php — chạy bằng:
// php artisan tinker --execute="require '/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-phong-hop/.sdd/mint-auth.php';"
//
// Mint JWT cho 2 tài khoản test e2e worktree (Task 4b):
// - id 34 (thuydt.qttt@tanphat.com): CÓ role 18 (Super admin) + current_company_role = 1
//   -> có quyền 'Quản lý danh mục phòng họp' (permission id 1574)
// - id 25 (cannt.kd1@tanphat.com): KHÔNG có role 18, current_company_role = 1
//   -> KHÔNG có quyền 'Quản lý danh mục phòng họp'
//
// CHỈ ĐỌC — không tạo/sửa bản ghi nào trong DB.

$ids = [34, 25];
foreach ($ids as $id) {
    $u = \App\Models\TpEmployee::find($id);
    if (!$u) {
        echo 'MINT_ERROR=' . json_encode(['id' => $id, 'error' => 'not found']) . PHP_EOL;
        continue;
    }
    echo 'MINT=' . json_encode(['id' => $id, 'email' => $u->email, 'token' => \JWTAuth::fromUser($u)]) . PHP_EOL;
}
