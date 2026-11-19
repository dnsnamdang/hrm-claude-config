<?php
// Xoá dữ liệu mẫu phòng họp AGPH
require 'vendor/autoload.php'; $app=require 'bootstrap/app.php'; $app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();
use Illuminate\Support\Facades\DB;
DB::transaction(function () {
  $rooms = DB::table('meeting_rooms')->where('description','AGPH')->pluck('id');
  $b = DB::table('meeting_room_bookings')->whereIn('meeting_room_id',$rooms)->orWhere('code','like','AGPH-%')->pluck('id');
  DB::table('meeting_room_booking_participants')->whereIn('meeting_room_booking_id',$b)->delete();
  $nb = DB::table('meeting_room_bookings')->whereIn('id',$b)->delete();
  DB::table('meeting_room_managers')->whereIn('meeting_room_id',$rooms)->delete();
  DB::table('meeting_room_room_amenity')->whereIn('meeting_room_id',$rooms)->delete();
  $nr = DB::table('meeting_rooms')->whereIn('id',$rooms)->delete();
  $na = DB::table('meeting_room_amenities')->where('note','AGPH')->delete();
  $np = DB::table('meeting_room_purposes')->where('note','AGPH')->delete();
  echo "Đã xoá $nr phòng, $nb phiếu, $na tiện nghi, $np mục đích\n";
});
