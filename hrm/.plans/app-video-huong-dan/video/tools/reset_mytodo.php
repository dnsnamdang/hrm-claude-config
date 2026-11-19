// Đưa DB local về trạng thái NGAY SAU prep_mytodo.py (dọn dữ liệu các lượt chạy thử / quay hỏng) — CHỈ dùng DB dev local.
// Chạy: PREP=~/.cache/tpe-video-work/prep_mytodo.json php artisan tinker --execute="$(cat reset_mytodo.php)"
$prep = json_decode(file_get_contents(getenv('PREP')), true);
$since = getenv('SINCE');                       // mốc dựng dữ liệu (Y-m-d H:i:s)
$keep = array_filter($prep['todos']);
$uid = 13;
$info = (int) DB::table('employees')->where('id', $uid)->value('employee_info_id');

// 1) nhắc việc tạo sau mốc (trừ bộ dựng sẵn) + bước con
$extra = DB::table('personal_todos')->where('user_id', $uid)->whereNull('parent_id')->where('created_at', '>=', $since)
    ->whereNotIn('id', $keep)->pluck('id')->all();
DB::table('personal_todos')->whereIn('parent_id', $extra)->delete();
echo 'xoa nhac viec: ', DB::table('personal_todos')->whereIn('id', $extra)->delete(), "\n";
// bước con tạo thêm trong lúc thử trên nhắc việc dựng sẵn
DB::table('personal_todos')->whereIn('parent_id', $keep)->where('created_at', '>=', date('Y-m-d H:i:s', strtotime($since) + 60))->delete();

// 2) liên hệ tạo sau mốc (trừ Chị Lan của bộ dựng sẵn), loại nhắc việc "Khách hàng"
echo 'xoa lien he: ', DB::table('personal_contacts')->where('user_id', $uid)->where('created_at', '>=', $since)
    ->where('name', 'not like', 'Chị Lan%')->delete(), "\n";
echo 'xoa loai: ', DB::table('personal_todo_lists')->where('name', 'Khách hàng')->where('created_at', '>=', $since)->delete(), "\n";

// 3) trạng thái bộ dựng sẵn: Mua VPP còn (chưa xoá được thì báo), Gửi hồ sơ năng lực = xong, các việc khác chưa xong
$mua = DB::table('personal_todos')->where('user_id', $uid)->where('title', 'Mua văn phòng phẩm cho phòng')->exists();
if (!$mua) {   // lượt quay trước đã xoá thật ở bước "Xóa" ⇒ tạo lại y như prep (hạn = ngày sau ngày dựng)
    $tpl = DB::table('personal_todos')->whereIn('id', $keep)->first();
    DB::table('personal_todos')->insert(['user_id' => $uid, 'company_id' => $tpl->company_id, 'list_id' => 2,
        'title' => 'Mua văn phòng phẩm cho phòng', 'due_date' => date('Y-m-d', strtotime($prep['date'] . ' +1 day')),
        'is_completed' => 0, 'sort_order' => 0, 'created_by' => $uid, 'updated_by' => $uid,
        'created_at' => $prep['date'] . ' 00:01:00', 'updated_at' => now()]);
}
echo 'Mua VPP: ', $mua ? 'con' : 'tao lai', "\n";
DB::table('personal_todos')->whereIn('id', $keep)->where('title', '<>', 'Gửi hồ sơ năng lực cho khách')
    ->update(['is_completed' => 0, 'completed_at' => null]);

// 4) meeting dựng sẵn: tôi CHƯA xác nhận
DB::table('meeting_employees')->where('meeting_id', $prep['meeting'])->where('employee_id', $uid)
    ->update(['attendance_status' => 0, 'attendance_note' => null]);

// 5) nhật ký nhắc (để lệnh nhắc / bản tin sáng gửi lại được) + chuông của tôi phát sinh sau mốc
echo 'xoa log nhac: ', DB::table('work_reminder_logs')->where('employee_info_id', $info)->where('created_at', '>=', $since)->delete(), "\n";
echo 'xoa chuong: ', DB::table('notifications')->where('notifiable_id', $info)->where('created_at', '>=', $since)->delete(), "\n";
