use Carbon\Carbon;
$ids = json_decode(file_get_contents('/private/tmp/claude-501/-Users-dnsnamdang-Documents-DNSMEDIA-websites-ERP-HRM/c664740e-ee08-48db-85f6-0fe41e29686c/scratchpad/seed_ids.json'), true);
[$R1, $R2, $R3] = $ids['rooms']; $B = $ids['bookings'];
$now = Carbon::now()->second(0); $today = Carbon::today(); $tmr = Carbon::tomorrow();
$t = function ($c) { return $c->format('Y-m-d H:i:s'); };
$at = function ($day, $hm) { return $day->copy()->setTimeFromTimeString($hm); };
DB::transaction(function () use ($B, $now, $today, $tmr, $t, $at, $R1, $R2, $R3, &$meetingIds) {
  $bk = function ($k, $from, $to, $st, $extra = []) use ($B, $t) {
    DB::table('meeting_room_bookings')->where('id', $B[$k])->update(array_merge(['start_at' => $t($from), 'end_at' => $t($to), 'status' => $st], $extra));
  };
  $ok = ['approved_at' => $t(Carbon::now()), 'approved_by' => 13];
  $bk('B1', $now->copy()->subMinutes(30), $now->copy()->addMinutes(60), 2, $ok + ['checkin_at' => $t($now->copy()->subMinutes(25)), 'service_status' => 2, 'service_handled_by' => 13, 'service_handled_at' => $t($now->copy()->subMinutes(40))]);
  $bk('B2', $now->copy()->addMinutes(10), $now->copy()->addMinutes(100), 2, $ok + ['service_status' => 1]);
  $bk('B3', $at($tmr, '09:00'), $at($tmr, '10:00'), 1, ['approved_at' => null, 'approved_by' => null]);
  $bk('B4', $at($today->copy()->subDay(), '08:30'), $at($today->copy()->subDay(), '09:30'), 5, $ok + ['checkin_at' => $t($at($today->copy()->subDay(), '08:28')), 'checkout_at' => $t($at($today->copy()->subDay(), '09:25'))]);
  $bk('B5', $at($today->copy()->addDays(5), '15:00'), $at($today->copy()->addDays(5), '16:00'), 4, ['cancel_reason' => 'Lùi lịch sang tuần sau', 'cancelled_at' => $t(Carbon::now()), 'cancelled_by' => 13]);
  $bk('B6', $at($tmr, '14:00'), $at($tmr, '15:00'), 1, ['approved_at' => null, 'approved_by' => null, 'service_status' => 1]);
  $bk('B7', $at($today->copy()->addDays(2), '10:00'), $at($today->copy()->addDays(2), '11:00'), 1, ['approved_at' => null, 'approved_by' => null]);
  $bk('B8', $at($today, '16:00'), $at($today, '17:00'), 2, $ok + ['service_status' => 1]);

  $tpl = (array) DB::table('meetings')->where('id', 2301)->first();
  $cust = array_intersect_key($tpl, array_flip(['customer_id', 'customer_name', 'customer_code', 'province_id', 'province_name', 'customer_contact_id', 'customer_contact_name', 'customer_contact_phone', 'customer_contact_role']));
  $noCust = array_fill_keys(array_keys($cust), null);
  $room = function ($id) { $r = DB::table('meeting_rooms')->find($id); return ['meeting_room_id' => $id, 'location' => $r->name . ' - ' . $r->location]; };
  $M = [ // key, name, host, status, start, end, customer?, room/booking, extra
    ['M1', 'TA Họp triển khai app phòng họp', 13, 2, $now->copy()->subMinutes(30), $now->copy()->addMinutes(60), false, ['B1', $R1], []],
    ['M2', 'TA Họp kế hoạch tháng 11', 13, 1, $at($tmr, '09:00'), $at($tmr, '10:00'), false, ['B3', $R3], []],
    ['M3', 'TA Tiếp đoàn khách Kính Nổi', 13, 2, $now->copy()->addMinutes(10), $now->copy()->addMinutes(100), true, ['B2', $R2], []],
    ['M4', 'TA Khảo sát dây chuyền hàn (chờ biên bản)', 13, 2, $at($today->copy()->subDay(), '14:00'), $at($today->copy()->subDay(), '15:30'), true, null, []],
    ['M5', 'TA Họp giao ban tuần', 13, 3, $at($today->copy()->subDay(), '08:30'), $at($today->copy()->subDay(), '09:30'), false, ['B4', $R1], ['completed_at' => $t($at($today->copy()->subDay(), '09:35')), 'conclusion' => 'Đã chốt kế hoạch tuần.']],
    ['M6', 'TA Họp chiến lược Q1/2027 (nháp)', 13, 0, $at($today->copy()->addDays(7), '09:00'), $at($today->copy()->addDays(7), '11:00'), false, null, []],
    ['M7', 'TA Họp tổng kết quý (đã huỷ)', 13, 4, $at($today->copy()->addDays(5), '15:00'), $at($today->copy()->addDays(5), '16:00'), false, ['B5', $R1], ['cancel_reason' => 'Lùi lịch sang tuần sau', 'cancelled_at' => $t(Carbon::now()), 'cancelled_by' => 13]],
    ['M8', 'TA Đào tạo sản phẩm mới', 484, 2, $at($tmr, '14:00'), $at($tmr, '15:00'), false, ['B6', $R2], []],
    ['M9', 'TA Họp online với đối tác Nhật', 484, 1, $at($today->copy()->addDays(3), '15:00'), $at($today->copy()->addDays(3), '16:00'), true, null, ['mode_id' => 2, 'online_link' => 'https://meet.google.com/abc-defg-hij', 'location' => null]],
    ['M10', 'TA Giới thiệu vật liệu hàn mới', 484, 3, $at($today->copy()->subDays(2), '10:00'), $at($today->copy()->subDays(2), '11:30'), true, null, ['completed_at' => $t($at($today->copy()->subDays(2), '11:40')), 'conclusion' => 'Khách quan tâm, gửi báo giá trong tuần.']],
    ['M11', 'TA Họp phòng Kinh doanh 1 (chờ biên bản)', 484, 2, $at($today->copy()->subDays(2), '15:00'), $at($today->copy()->subDays(2), '16:00'), false, null, []],
  ];
  $meetingIds = [];
  $i = 0;
  foreach ($M as [$k, $name, $host, $st, $s, $e, $isCust, $rb, $extra]) {
    $i++;
    $row = array_merge($tpl, $isCust ? $cust : $noCust, [
      'code' => sprintf('TA.MET.26.%03d', $i), 'name' => $name, 'status' => $st, 'start_date' => $t($s), 'end_date' => $t($e),
      'host_employee_id' => $host, 'created_by' => $host, 'updated_by' => $host, 'department_id' => $host == 13 ? 111 : $tpl['department_id'],
      'is_customer_meeting' => $isCust ? 1 : 0, 'meeting_type_id' => $isCust ? 14 : 2, 'mode_id' => 1, 'online_link' => null,
      'meeting_room_id' => null, 'location' => $isCust ? $tpl['location'] : 'Văn phòng Tân Phát', 'note' => null,
      'completed_at' => null, 'conclusion' => null, 'cancel_reason' => null, 'cancelled_at' => null, 'cancelled_by' => null,
      'report_deadline_notified_at' => null, 'auto_cancelled_at' => null, 'start_reminded_at' => null,
      'created_at' => $t(Carbon::now()), 'updated_at' => $t(Carbon::now()),
    ], $rb ? $room($rb[1]) : [], $extra);
    unset($row['id']);
    $mid = DB::table('meetings')->insertGetId($row);
    $meetingIds[$k] = $mid;
    if ($rb) DB::table('meeting_room_bookings')->where('id', $B[$rb[0]])->update(['meeting_id' => $mid, 'host_employee_id' => $host]);
    $att = $st == 3 ? 1 : 0;
    $mem = [[13, 'DNS Admin', 'Quản trị hệ thống', null], [484, 'Ngô Xuân Cường', 'Chuyên viên Kinh doanh', '0912018418']];
    if ($host == 484) $mem = array_reverse($mem);
    $o = 0;
    foreach ($mem as [$eid, $n, $r, $p]) DB::table('meeting_employees')->insert(['meeting_id' => $mid, 'employee_id' => $eid, 'name' => $n, 'role' => $r, 'phone' => $p, 'type' => '1', 'attendance_status' => $att, 'sort_order' => ++$o, 'created_at' => $t(Carbon::now()), 'updated_at' => $t(Carbon::now())]);
    if ($isCust) DB::table('meeting_employees')->insert(['meeting_id' => $mid, 'employee_id' => null, 'name' => $tpl['customer_contact_name'], 'role' => $tpl['customer_contact_role'], 'phone' => $tpl['customer_contact_phone'], 'type' => '2', 'attendance_status' => $att, 'sort_order' => 1, 'created_at' => $t(Carbon::now()), 'updated_at' => $t(Carbon::now())]);
  }
});
$ids['meetings'] = $meetingIds;
file_put_contents('/private/tmp/claude-501/-Users-dnsnamdang-Documents-DNSMEDIA-websites-ERP-HRM/c664740e-ee08-48db-85f6-0fe41e29686c/scratchpad/seed_ids.json', json_encode($ids));
echo "OK ", json_encode($meetingIds), "\n";
