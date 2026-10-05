<?php
/**
 * Task 13, fix round 1, VIỆC 2 — ca đua THẬT ở tầng DB (2 kết nối PDO riêng, KHÔNG qua HTTP).
 *
 * KHÔNG đưa vào repo code (`Modules/Meeting/...`) — chỉ là script chẩn đoán chạy tay 1 lần để lấy
 * bằng chứng, output dán vào `.sdd/task-13-report.md`. Lý do cần script riêng: API đang chạy bằng
 * `php -S` (`artisan serve`), server này xử lý TUẦN TỰ từng request HTTP một, nên ca e2e
 * `Promise.all()` ở `meeting-room-booking.api.spec.ts` (C1) không chứng minh được gì về khoá DB —
 * 2 request bị chính web server xếp hàng trước khi chạm code.
 *
 * Script này mô phỏng ĐÚNG 2 câu SQL mà `MeetingRoomBookingService::assertNoOverlap()` chạy, bằng
 * 2 tiến trình PHP con (`proc_open`), MỖI TIẾN TRÌNH 1 KẾT NỐI PDO RIÊNG — đây là điều kiện đủ để
 * có 2 transaction MySQL thật sự chạy song song, không phụ thuộc PHP built-in server có tuần tự
 * hay không.
 *
 * 3 kịch bản (đối chứng âm + 2 đối chứng dương):
 *   no-mutex-rc    : SET ISOLATION READ COMMITTED, KHÔNG khoá dòng phòng — đúng code TRƯỚC fix
 *                    round 1 (chỉ có SELECT...FOR UPDATE trên tập overlap). Dưới READ COMMITTED,
 *                    MySQL tắt gap lock nên SELECT...FOR UPDATE trên tập RỖNG không khoá được gì.
 *                    Kỳ vọng: CẢ HAI cùng INSERT thành công -> double-booking.
 *   with-mutex-rc  : Vẫn READ COMMITTED, nhưng CÓ khoá mutex dòng phòng trước (đúng code SAU fix
 *                    round 1). Kỳ vọng: chỉ 1 request INSERT, request kia bị chặn bởi overlap.
 *   with-mutex-rr  : Isolation THẬT đang chạy trong môi trường (REPEATABLE READ, đã tự đo bằng
 *                    `SHOW VARIABLES LIKE 'transaction_isolation'`) + có mutex — đối chứng dưới
 *                    đúng cấu hình production hiện tại.
 *
 * Cách chạy (từ máy có PHP 7.4 + pdo_mysql, KHÔNG cần Laravel bootstrap):
 *   /opt/homebrew/opt/php@7.4/bin/php task-13-race-check.php <no-mutex-rc|with-mutex-rc|with-mutex-rr>
 *
 * Script tự: tạo 1 phòng test -> spawn 2 tiến trình con cùng nhắm 1 phòng + 1 khung giờ -> đợi cả
 * 2 xong -> đếm số phiếu thật trong DB -> XÓA SẠCH phòng + phiếu vừa tạo trước khi thoát.
 */

$envPath = '/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api/.env';

function readEnvValue($path, $key)
{
    $content = file_get_contents($path);
    if (preg_match('/^' . preg_quote($key, '/') . '=(.*)$/m', $content, $m)) {
        return trim($m[1]);
    }

    return '';
}

function pdoConnect($envPath)
{
    $host = readEnvValue($envPath, 'DB_HOST') ?: '127.0.0.1';
    $db = readEnvValue($envPath, 'DB_DATABASE') ?: 'hrm_erp';
    $user = readEnvValue($envPath, 'DB_USERNAME') ?: 'root';
    $pass = readEnvValue($envPath, 'DB_PASSWORD');

    return new PDO("mysql:host={$host};dbname={$db};charset=utf8mb4", $user, $pass, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    ]);
}

// ============================= WORKER MODE (chạy trong tiến trình con) =============================
if (isset($argv[1]) && $argv[1] === '--worker') {
    [, , $role, $scenario, $roomId, $startAt, $endAt] = $argv;
    $pdo = pdoConnect($envPath);

    $useReadCommitted = substr($scenario, -3) === '-rc';
    $useMutex = strpos($scenario, 'with-mutex') === 0;

    if ($useReadCommitted) {
        $pdo->exec('SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED');
    }

    $t0 = microtime(true);
    $pdo->beginTransaction();

    if ($useMutex) {
        // VIỆC 1 (fix round 1) — mutex trên chính dòng phòng, y hệt
        // `MeetingRoom::where('id', $roomId)->lockForUpdate()->first()` trong Service.
        $stmt = $pdo->prepare('SELECT id FROM meeting_rooms WHERE id = ? FOR UPDATE');
        $stmt->execute([$roomId]);
        $stmt->fetch();
    }
    $tLockAcquired = microtime(true);

    // Y hệt `assertNoOverlap()`: chỉ so với phiếu Đã duyệt (status=2), khoảng giờ giao nhau.
    $stmt = $pdo->prepare(
        'SELECT id, title FROM meeting_room_bookings
         WHERE meeting_room_id = ? AND status = 2 AND start_at < ? AND end_at > ?
         FOR UPDATE'
    );
    $stmt->execute([$roomId, $endAt, $startAt]);
    $conflict = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($conflict) {
        $pdo->rollBack();
        $t1 = microtime(true);
        fwrite(STDOUT, sprintf(
            "[%s] BLOCKED_BY_OVERLAP conflict_booking_id=%s lock_wait=%.3fs total=%.3fs\n",
            $role,
            $conflict['id'],
            $tLockAcquired - $t0,
            $t1 - $t0
        ));
        exit(0);
    }

    // ⚠️ MẤU CHỐT của ca đua thật — độ trễ TOCTOU (time-of-check-to-time-of-use) đặt NGAY SAU KHI
    // "kiểm tra xong, thấy KHÔNG trùng" nhưng TRƯỚC KHI insert. Đây chính là khe hở mà brief gọi
    // là "SELECT rồi INSERT không khóa": nếu để độ trễ SAU insert (bản nháp đầu của script này đã
    // mắc lỗi này) thì A luôn insert xong gần như ngay lập tức, B chạm phải MỘT DÒNG ĐÃ TỒN TẠI
    // (dù chưa commit) khi quét index -> B luôn bị chặn bởi khóa dòng thông thường của InnoDB bất
    // kể isolation level, không hề chứng minh được gì về gap lock. Đặt độ trễ Ở ĐÂY thì tại thời
    // điểm B chạy overlap-check, A CHƯA insert -> đúng tình huống "2 kết nối cùng thấy trống".
    usleep(700000); // 0.7s

    $code = 'RACE-' . $role . '-' . substr(md5(uniqid('', true)), 0, 8);
    $stmt = $pdo->prepare(
        'INSERT INTO meeting_room_bookings
            (code, meeting_room_id, title, start_at, end_at, status, booked_by_employee_id, source, created_at, updated_at)
         VALUES (?, ?, ?, ?, ?, 2, 34, 1, NOW(), NOW())'
    );
    $stmt->execute([$code, $roomId, "Race check {$role}", $startAt, $endAt]);
    $insertedId = $pdo->lastInsertId();

    $pdo->commit();
    $t1 = microtime(true);
    fwrite(STDOUT, sprintf(
        "[%s] INSERTED booking_id=%s code=%s lock_wait=%.3fs total=%.3fs\n",
        $role,
        $insertedId,
        $code,
        $tLockAcquired - $t0,
        $t1 - $t0
    ));
    exit(0);
}

// ============================= ORCHESTRATOR MODE =============================
$scenario = $argv[1] ?? null;
$validScenarios = ['no-mutex-rc', 'with-mutex-rc', 'with-mutex-rr'];
if (!in_array($scenario, $validScenarios, true)) {
    fwrite(STDERR, 'Usage: php task-13-race-check.php <' . implode('|', $validScenarios) . ">\n");
    exit(1);
}

$pdo = pdoConnect($envPath);

$isolationRow = $pdo->query("SHOW VARIABLES LIKE 'transaction_isolation'")->fetch(PDO::FETCH_ASSOC);
fwrite(STDOUT, "MySQL transaction_isolation hiện tại (session của orchestrator): {$isolationRow['Value']}\n");

$roomCode = 'RACECHK_' . time() . '_' . $scenario;
$pdo->prepare(
    'INSERT INTO meeting_rooms (code, name, company_id, status, require_approval, created_at, updated_at)
     VALUES (?, ?, 1, 1, 0, NOW(), NOW())'
)->execute([$roomCode, 'Race Check Room']);
$roomId = $pdo->lastInsertId();

$startAt = date('Y-m-d H:i:s', strtotime('+30 days 09:00'));
$endAt = date('Y-m-d H:i:s', strtotime('+30 days 10:00'));

fwrite(STDOUT, "=== Scenario: {$scenario} | room_id={$roomId} | start={$startAt} end={$endAt} ===\n");

$scriptPath = __FILE__;
$buildCmd = function ($role) use ($scriptPath, $scenario, $roomId, $startAt, $endAt) {
    return escapeshellcmd(PHP_BINARY) . ' ' . escapeshellarg($scriptPath)
        . ' --worker ' . escapeshellarg($role) . ' ' . escapeshellarg($scenario) . ' '
        . escapeshellarg($roomId) . ' ' . escapeshellarg($startAt) . ' ' . escapeshellarg($endAt);
};

$descriptors = [1 => ['pipe', 'w'], 2 => ['pipe', 'w']];
$procA = proc_open($buildCmd('A'), $descriptors, $pipesA);
usleep(100000); // A đi trước 100ms để đảm bảo A luôn là bên giữ khoá trước (kết quả dễ đọc hơn).
$procB = proc_open($buildCmd('B'), $descriptors, $pipesB);

$outA = stream_get_contents($pipesA[1]);
$errA = stream_get_contents($pipesA[2]);
fclose($pipesA[1]);
fclose($pipesA[2]);
$outB = stream_get_contents($pipesB[1]);
$errB = stream_get_contents($pipesB[2]);
fclose($pipesB[1]);
fclose($pipesB[2]);

proc_close($procA);
proc_close($procB);

echo $outA;
if (trim($errA)) {
    fwrite(STDERR, "[A][stderr] {$errA}\n");
}
echo $outB;
if (trim($errB)) {
    fwrite(STDERR, "[B][stderr] {$errB}\n");
}

$count = (int) $pdo->query("SELECT COUNT(*) FROM meeting_room_bookings WHERE meeting_room_id = {$roomId}")->fetchColumn();
fwrite(STDOUT, "=== KẾT QUẢ: số phiếu trong DB cho room_id={$roomId} = {$count} ===\n");

// Dọn sạch dữ liệu của script — DB dùng chung với phiên khác.
$pdo->exec("DELETE FROM meeting_room_bookings WHERE meeting_room_id = {$roomId}");
$pdo->exec("DELETE FROM meeting_rooms WHERE id = {$roomId}");
fwrite(STDOUT, "=== Đã dọn sạch room_id={$roomId} và các phiếu liên quan ===\n");
