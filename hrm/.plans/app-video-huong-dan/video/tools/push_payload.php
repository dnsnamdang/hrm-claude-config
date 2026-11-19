// Dựng gói APNs cho `xcrun simctl push` từ dòng `notifications` mới nhất của 1 nhân viên — đúng title/body như
// Modules/Timesheet/Jobs/SendNotification::formatNotificationData (NotificationMeta::push) + khoá data như FCM thật.
// Chạy: EMP=13 TYPE_LIKE='work_reminder.%' OUT=/path/x.apns php artisan tinker --execute="$(cat push_payload.php)"
$emp = (int) (getenv('EMP') ?: 13);
$like = getenv('TYPE_LIKE') ?: '%';
$info = (int) DB::table('employees')->where('id', $emp)->value('employee_info_id');
$infoIds = [$info];
$n = DB::table('notifications')->whereIn('notifiable_id', $infoIds)
    ->where('data', 'like', '%"type":"' . str_replace('%', '', $like) . '%')
    ->orderByDesc('created_at')->first();
if (!$n) { echo "KHONG_CO_THONG_BAO\n"; return; }
$data = json_decode($n->data, true);
$push = \App\Support\NotificationMeta::push(\App\Support\NotificationMeta::stripSender($data));
$badge = \App\Support\NotificationBadge::unreadCount($info, $n->id);
$apns = [
    'aps' => ['alert' => ['title' => $push['title'], 'body' => $push['body']], 'sound' => 'default', 'badge' => $badge],
    'gcm.message_id' => 'video-' . substr($n->id, 0, 8),
    'employee_info_id' => (string) $n->notifiable_id,
    'created' => (string) $n->created_at,
    'type' => (string) ($data['type'] ?? ''),
    'id' => (string) ($data['id'] ?? ''),
    'notification_id' => (string) $n->id,
];
file_put_contents(getenv('OUT') ?: '/tmp/x.apns', json_encode($apns, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
echo "OK ", $n->created_at, " | ", $push['title'], " | ", $push['body'], "\n";
