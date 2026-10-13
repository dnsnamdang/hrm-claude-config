## git status
 M Modules/Meeting/Entities/MeetingRoom.php
 M Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php
 M Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php
 M Modules/Meeting/Services/MeetingRoomBookingService.php
 M Modules/Meeting/Services/MeetingRoomService.php
 M Modules/Meeting/Transformers/MeetingRoom/BookableMeetingRoomResource.php
 M Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php
 M Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php
 M Modules/Meeting/Transformers/MeetingRoomBooking/DetailMeetingRoomBookingResource.php
 M Modules/Meeting/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php
 M app/Services/CatalogHistoryService.php
?? Modules/Meeting/Database/Migrations/2026_09_23_000001_create_meeting_room_managers_table.php
?? tests/Feature/MeetingRoomManagersTest.php

## diff --stat
 Modules/Meeting/Entities/MeetingRoom.php           | 116 +++++++++++++++--
 .../Controllers/Api/V1/MeetingRoomController.php   |  15 ++-
 .../Requests/MeetingRoom/MeetingRoomRequest.php    |  11 +-
 .../Meeting/Services/MeetingRoomBookingService.php |  33 ++---
 Modules/Meeting/Services/MeetingRoomService.php    | 144 ++++++++++++++++-----
 .../MeetingRoom/BookableMeetingRoomResource.php    |  13 +-
 .../MeetingRoom/DetailMeetingRoomResource.php      |  10 +-
 .../MeetingRoom/MeetingRoomResource.php            |  18 ++-
 .../DetailMeetingRoomBookingResource.php           |  12 +-
 .../MeetingRoomBookingResource.php                 |   7 +-
 app/Services/CatalogHistoryService.php             |  14 +-
 11 files changed, 310 insertions(+), 83 deletions(-)

## diff -U10 (toàn bộ Phase 8 khối A: A1 + A2 + fix vòng 1)
diff --git a/Modules/Meeting/Entities/MeetingRoom.php b/Modules/Meeting/Entities/MeetingRoom.php
index 612dc54c6..d149a56a4 100644
--- a/Modules/Meeting/Entities/MeetingRoom.php
+++ b/Modules/Meeting/Entities/MeetingRoom.php
@@ -7,25 +7,29 @@ use Illuminate\Support\Str;
 
 class MeetingRoom extends BaseModel
 {
     const STATUS_ACTIVE = 1;
     const STATUS_INACTIVE = 2;
 
     protected $table = 'meeting_rooms';
 
     protected $fillable = [
         'name', 'company_id', 'allow_cross_company',
-        'location', 'capacity', 'manager_employee_id', 'require_approval',
+        'location', 'capacity', 'require_approval',
         'open_time', 'close_time', 'checkin_grace_minutes', 'checkin_qr_token',
         'description', 'status', 'created_by', 'updated_by',
     ];
 
+    /** Đệm `managerIds()`/`managerNames()` trong 1 request — xem 2 hàm bên dưới. */
+    protected $managerIdsCache;
+    protected $managerNamesCache;
+
     /**
      * Sinh sẵn token QR ngay khi tạo phòng (phase 5 dùng để check-in bằng cách quét mã dán
      * trước cửa). Sinh ở đây thay vì lúc cần: thêm sau đồng nghĩa phải in và dán lại QR ngoài đời.
      */
     protected static function booted()
     {
         static::creating(function (self $room) {
             if (empty($room->checkin_qr_token)) {
                 $room->checkin_qr_token = (string) Str::uuid();
             }
@@ -70,33 +74,123 @@ class MeetingRoom extends BaseModel
     /**
      * Fix round 1 (review) — Resource cần `company_name` hiển thị ở màn danh sách/chi tiết.
      * Cùng nguồn `Modules\Human\Entities\Company` đang dùng ở `MeetingRoomService::formOptions()`.
      */
     public function company()
     {
         return $this->belongsTo(\Modules\Human\Entities\Company::class, 'company_id', 'id');
     }
 
     /**
-     * Fix round 1 (review) — Resource cần `manager_name`. `manager_employee_id` trỏ tới
-     * `employees.id` (khớp cách FE chọn nhân viên qua `$store.state.employees`, nạp từ
-     * `Employee::getAll()`), KHÔNG phải `employee_infos.id`.
+     * Phase 8 lượt A1 (T110) — 1 phòng nay có NHIỀU người phụ trách, thay cho quan hệ `manager()`
+     * (`belongsTo` qua cột `manager_employee_id`, đã DROP ở migration
+     * `2026_09_23_000001_create_meeting_room_managers_table`). Bảng nối `meeting_room_managers`
+     * trỏ `employee_id` -> `Modules\Timesheet\Entities\Employee` (KHÔNG phải `employee_infos.id`),
+     * giữ đúng nguồn nhân viên mà `manager()` cũ đang dùng — xem `managerNames()` bên dưới về vì
+     * sao KHÔNG lọc theo nhân viên đang làm việc.
+     *
+     * ⚠️ `->with('info')` NGAY TẠI ĐỊNH NGHĨA quan hệ (không phải ở nơi gọi): `managerNames()`
+     * đọc `Employee::fullname`, accessor này lazy-load `$employee->info` nếu chưa có — thiếu dòng
+     * này thì phòng có N người phụ trách sẽ ra N query `employee_infos` mỗi lần gọi
+     * `managerNames()` mà không hiện ở bất kỳ chỗ nào ngoài `DB::enableQueryLog()` (đã đo bằng
+     * tinker 23/09/2026, xem p8-A1-report.md mục tự kiểm).
+     */
+    public function managers()
+    {
+        // Fix vòng 1 (lượt A2, reviewer phát hiện ở lượt A1) — `orderBy` TƯỜNG MINH theo khoá pivot:
+        // docblock cũ của `managerNames()` khẳng định "đi theo thứ tự khoá pivot" khi KHÔNG khai
+        // `orderBy` gì, nhưng MySQL không đảm bảo thứ tự trả về khi thiếu ORDER BY (chỉ là hành vi
+        // ngẫu nhiên hay gặp của InnoDB, không phải hợp đồng SQL) — khai rõ để hết phụ thuộc "may
+        // rủi", và để BEFORE/AFTER snapshot của `MeetingRoomService::roomSnapshot()` luôn ra cùng
+        // thứ tự khi tập người phụ trách không đổi.
+        return $this->belongsToMany(
+            \Modules\Timesheet\Entities\Employee::class,
+            'meeting_room_managers',
+            'meeting_room_id',
+            'employee_id'
+        )->withTimestamps()->with('info')->orderBy('meeting_room_managers.id');
+    }
+
+    /**
+     * Fix vòng 1 (lượt A2) — bẫy CACHE reviewer lượt A1 phát hiện: `managerIds()`/`managerNames()`
+     * đệm vào `$managerIdsCache`/`$managerNamesCache`, VÀ Eloquent tự đánh dấu quan hệ `managers`
+     * "đã nạp" (`relationLoaded('managers')` = true) ngay sau lần đọc đầu tiên. Gọi thẳng
+     * `$room->managers()->sync($ids)` từ NƠI KHÁC đổi pivot thật trong DB nhưng KHÔNG xoá cả 2 lớp
+     * cache trên — đọc `managerIds()`/`managerNames()` LẦN NỮA trên CÙNG object sau `sync()` vẫn ra
+     * danh sách CŨ mà không có lỗi/cảnh báo nào. LUÔN gọi `sync()` qua hàm NÀY (không tự viết
+     * `$room->managers()->sync(...)` ở service khác) để cache được xoá đúng lúc.
      *
-     * ⚠️ Cố tình KHÔNG dùng `Employee::getAll(true)` (chỉ lấy nhân viên ĐANG làm việc) ở đây —
-     * đây là quan hệ Eloquent đọc trực tiếp bằng khoá ngoại, phải trả đúng người quản lý đã lưu dù
-     * người đó đã nghỉ việc, nếu không `manager_name` cho phòng có quản lý đã nghỉ sẽ lại rỗng y
-     * hệt lỗi mà lần sửa này đang vá (FE trước đây tra theo state.employees, vốn lọc
-     * `onlyActive = true`, nên bỏ sót đúng trường hợp này).
+     * @return array kết quả `sync()` gốc (['attached' => [...], 'detached' => [...], 'updated' => [...]])
      */
-    public function manager()
+    public function syncManagers(array $employeeIds): array
     {
-        return $this->belongsTo(\Modules\Timesheet\Entities\Employee::class, 'manager_employee_id', 'id');
+        $result = $this->managers()->sync($employeeIds);
+
+        $this->unsetRelation('managers');
+        $this->managerIdsCache = null;
+        $this->managerNamesCache = null;
+
+        return $result;
+    }
+
+    /**
+     * Mảng `employee_id` của TẤT CẢ người phụ trách phòng. Đệm vào thuộc tính protected để gọi
+     * nhiều lần trong 1 request (Resource + các hàm khác) không query lại — dùng CHUNG
+     * `loadedManagers()` với `managerNames()` nên dù gọi cả 2 hàm mà quan hệ CHƯA eager load, chỉ
+     * bắn đúng 1 query (`load()` đánh dấu quan hệ đã nạp trên chính model, khác với
+     * `managers()->get()` — cái đó lấy Collection mới mỗi lần, không đánh dấu gì cả).
+     *
+     * @return array
+     */
+    public function managerIds(): array
+    {
+        if ($this->managerIdsCache !== null) {
+            return $this->managerIdsCache;
+        }
+
+        return $this->managerIdsCache = $this->loadedManagers()->pluck('id')->all();
+    }
+
+    /**
+     * Mảng tên người phụ trách, ĐÚNG THỨ TỰ `managers` (thứ tự `meeting_room_managers.id` tăng
+     * dần — `orderBy('meeting_room_managers.id')` khai TƯỜNG MINH ngay ở `managers()`, fix vòng 1
+     * lượt A2: MySQL không đảm bảo thứ tự khi thiếu ORDER BY, không thể dựa vào "mặc định").
+     *
+     * Tên nhân viên lấy đúng cách `manager()` cũ đang lấy (accessor `Employee::getFullnameAttribute()`
+     * — đọc qua `employee_infos.fullname`, trả `"UNKNOWN"` nếu nhân viên chưa gắn `info`), KHÔNG
+     * dùng `Employee::getAll(true)` (chỉ nhân viên đang làm việc) vì đây là quan hệ đọc trực tiếp
+     * bằng khoá ngoại, phải trả đúng người đã lưu dù người đó đã nghỉ việc.
+     *
+     * @return array
+     */
+    public function managerNames(): array
+    {
+        if ($this->managerNamesCache !== null) {
+            return $this->managerNamesCache;
+        }
+
+        return $this->managerNamesCache = $this->loadedManagers()->pluck('fullname')->all();
+    }
+
+    /**
+     * Nếu quan hệ `managers` đã được eager load (`->with('managers')`) thì đọc thẳng, không bắn
+     * thêm query. Chưa có -> `load()` (KHÔNG dùng `managers()->get()`): `load()` ghi kết quả vào
+     * quan hệ đã nạp của CHÍNH model này, nên `managerIds()` và `managerNames()` gọi nối tiếp
+     * nhau (kể cả không cùng đệm) vẫn dùng chung đúng 1 query.
+     */
+    private function loadedManagers()
+    {
+        if (!$this->relationLoaded('managers')) {
+            $this->load('managers');
+        }
+
+        return $this->managers;
     }
 
     public function effectiveOpenTime($companyOpenTime)
     {
         return self::resolveConfig($this->open_time, $companyOpenTime, '07:00:00');
     }
 
     public function effectiveCloseTime($companyCloseTime)
     {
         return self::resolveConfig($this->close_time, $companyCloseTime, '20:00:00');
diff --git a/Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php b/Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php
index e4a7afd18..a71fe7340 100644
--- a/Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php
+++ b/Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php
@@ -188,23 +188,26 @@ class MeetingRoomController extends ApiController
         } catch (Exception $e) {
             Log::error($e);
 
             return $this->responseJson($e->getMessage(), Response::HTTP_BAD_REQUEST);
         }
     }
 
     public function show(MeetingRoom $meetingRoom)
     {
         // Fix round 1 IMPORTANT 3 + fix round 1 mục "việc BE": kèm employee_create/employee_update.info
-        // tránh N+1 khi Resource đọc employee_create_name/employee_update_name; company/manager.info
-        // tránh N+1 khi Resource đọc company_name/manager_name (xem MeetingRoomService::index()).
-        $meetingRoom->load(['amenities', 'employee_create.info', 'employee_update.info', 'company', 'manager.info']);
+        // tránh N+1 khi Resource đọc employee_create_name/employee_update_name; company/managers
+        // tránh N+1 khi Resource đọc company_name/manager_names (xem MeetingRoomService::index()).
+        // Phase 8 lượt A1 (T111 — sửa kèm dù ngoài danh sách file T109-T113, xem báo cáo mục
+        // "Deviation": `manager.info` -> `managers` bắt buộc, nếu không quan hệ `manager()` đã bị
+        // xoá ở T110 làm `RelationNotFoundException` ngay khi gọi endpoint show().
+        $meetingRoom->load(['amenities', 'employee_create.info', 'employee_update.info', 'company', 'managers']);
 
         return $this->responseJson('success', Response::HTTP_OK, new DetailMeetingRoomResource($meetingRoom));
     }
 
     /**
      * Xóa 1 phòng họp. Chặn khi phòng đã có phiếu đặt (dù mới/đã hủy) — xóa mất phòng thì
      * lịch sử phiếu mồ côi `meeting_room_id`; trường hợp này chỉ được Khóa.
      */
     public function destroy(MeetingRoom $meetingRoom)
     {
@@ -315,22 +318,24 @@ class MeetingRoomController extends ApiController
     /**
      * ================= XUẤT / IMPORT EXCEL (Task 45) =================
      *
      * Xuất dùng bộ DÙNG CHUNG `ExportColumnRegistry` + `DynamicExport` (skill list-page mục 14b):
      * cột do popup "Chọn trường xuất file" của FE quyết, BE chỉ resolve whitelist — KHÔNG viết
      * class `*Export` + blade cứng cột cho riêng màn này.
      */
     public function export(Request $request)
     {
         try {
+            // Phase 8 lượt A1 (T111 — sửa kèm, xem báo cáo mục "Deviation"): `manager.info` ->
+            // `managers`, cùng lý do như `show()`.
             $rows = $this->meetingRoomService->index($request)
-                ->with(['amenities', 'employee_create.info', 'employee_update.info', 'company', 'manager.info'])
+                ->with(['amenities', 'employee_create.info', 'employee_update.info', 'company', 'managers'])
                 ->get();
             $data = MeetingRoomResource::collection($rows)->resolve();
             $columns = ExportColumnRegistry::resolve('meeting_rooms', $request);
 
             return Excel::download(
                 (new DynamicExport())->forData($data)->withColumns($columns)->withTitle('Danh sách phòng họp'),
                 'danh_sach_phong_hop.xlsx'
             );
         } catch (Exception $e) {
             Log::error($e);
@@ -412,21 +417,21 @@ class MeetingRoomController extends ApiController
     {
         // ⚠️ Dòng mẫu CỐ TÌNH để trống "Tiện nghi" và "Người quản lý": 2 cột này phải khớp dữ liệu
         // CÓ THẬT trong hệ thống (tên tiện nghi trong danh mục, tên nhân viên), điền ví dụ bịa vào
         // thì người dùng tải mẫu về bấm Validate là thấy 2 dòng đỏ ngay — đã đo thật trên màn.
         // Cách nhập ghi luôn ở TIÊU ĐỀ cột để không cần dòng ví dụ.
         $headers = [
             'Tên phòng *',
             'Vị trí',
             'Sức chứa',
             'Tiện nghi (ngăn bởi dấu phẩy)',
-            'Người quản lý (tên nhân viên)',
+            'Người quản lý (tên nhân viên, bắt buộc >= 1, nhiều người ngăn bởi dấu ;) *',
             'Cần duyệt',
             'Cho công ty khác đặt',
             'Trạng thái',
         ];
         $samples = [
             ['Phòng họp tầng 3', 'Tầng 3, tòa nhà A', 10, '', '', 'Không', 'Không', 'Hoạt động'],
             ['Phòng họp nhỏ', 'Tầng 1', 6, '', '', 'Có', 'Không', 'Hoạt động'],
         ];
         $widths = ['A' => 32, 'B' => 28, 'C' => 12, 'D' => 34, 'E' => 30, 'F' => 14, 'G' => 22, 'H' => 14];
 
diff --git a/Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php b/Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php
index f57f6f818..c62af7ded 100644
--- a/Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php
+++ b/Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php
@@ -12,20 +12,28 @@ use Modules\Training\Http\Requests\BaseRequest;
  * ⚠️ Quyết định user 19/09/2026: form KHÔNG còn ô chọn Công ty — **công ty nào tạo thì
  * phòng thuộc công ty đó**. `company_id` KHÔNG nhận từ payload nữa (client gửi lên cũng bị bỏ
  * qua ở service): lúc tạo do `BaseModel::creating()` điền theo người đăng nhập, lúc sửa giữ
  * nguyên giá trị đang có.
  *
  * Task 44 — bỏ hẳn trường Mã. `name` chỉ unique TRONG CÙNG công ty: khác công ty được trùng tên (VD 2 chi nhánh cùng có
  * phòng "A301"). Công ty để so trùng vì thế phải TỰ SUY RA (sửa: công ty của chính phòng đó;
  * tạo mới: công ty người đăng nhập) — KHÔNG đọc `$this->input('company_id')` như bản trước,
  * nếu không client bịa `company_id` là né được ràng buộc trùng mã.
  * `ignore($id)` để sửa phòng không tự đụng chính nó.
+ *
+ * Phase 8 lượt A1 (T112) — `manager_employee_id` (1 người) đổi thành `manager_employee_ids`
+ * (mảng, >= 1 người). `exists:employees,id` tra đúng bảng `employees` thật của hệ thống (kiểm
+ * bằng `Modules\Timesheet\Entities\Employee::$table` trước khi viết, KHÔNG đoán).
+ *
+ * ⚠️ CHỈ khai `rules()` — KHÔNG khai `messages()` cho các rule phổ biến (`required`/`array`/
+ * `min`/`integer`/`exists`…): câu lỗi tiếng Việt đã có sẵn ở `resources/lang/vi/validation.php`
+ * (CLAUDE.md, mục "KHÔNG tự viết lại message validate cho rule phổ biến").
  */
 class MeetingRoomRequest extends BaseRequest
 {
     /**
      * Get the validation rules that apply to the request.
      *
      * @return array
      */
     public function rules()
     {
@@ -39,21 +47,22 @@ class MeetingRoomRequest extends BaseRequest
             // (trùng tên trong CÙNG công ty thì chặn, khác công ty vẫn được trùng).
             'name' => [
                 'required', 'string', 'max:255',
                 Rule::unique('meeting_rooms', 'name')
                     ->where(fn ($q) => $q->where('company_id', $companyId))
                     ->ignore($id),
             ],
             'allow_cross_company' => ['nullable', 'boolean'],
             'location' => ['nullable', 'string', 'max:255'],
             'capacity' => ['nullable', 'integer', 'min:1'],
-            'manager_employee_id' => ['nullable', 'integer'],
+            'manager_employee_ids' => ['required', 'array', 'min:1'],
+            'manager_employee_ids.*' => ['integer', 'exists:employees,id'],
             'require_approval' => ['nullable', 'boolean'],
             'open_time' => ['nullable', 'date_format:H:i:s'],
             'close_time' => ['nullable', 'date_format:H:i:s', 'after:open_time'],
             'checkin_grace_minutes' => ['nullable', 'integer', 'min:0', 'max:120'],
             'description' => ['nullable', 'string'],
             'amenity_ids' => ['nullable', 'array'],
             'amenity_ids.*' => ['integer', 'exists:meeting_room_amenities,id'],
         ];
     }
 
diff --git a/Modules/Meeting/Services/MeetingRoomBookingService.php b/Modules/Meeting/Services/MeetingRoomBookingService.php
index c1aea9314..9bd748077 100644
--- a/Modules/Meeting/Services/MeetingRoomBookingService.php
+++ b/Modules/Meeting/Services/MeetingRoomBookingService.php
@@ -151,76 +151,78 @@ class MeetingRoomBookingService extends BaseService
             return $query->orderBy($allowedSortFields[$sortBy], $direction);
         }
 
         // Mặc định: phiếu sắp diễn ra / mới nhất lên trước.
         return $query->orderBy('start_at', 'desc');
     }
 
     /**
      * Task 14, Bước 6 (spec 10 / plan Task 12 bước 4) — "luật nhìn thấy phiếu". Không có quyền
      * *Xem tất cả phiếu đặt phòng họp* thì chỉ thấy phiếu MÌNH ĐẶT, MÌNH ĐƯỢC MỜI (participants),
-     * HOẶC phiếu của PHÒNG MÌNH QUẢN LÝ (`meeting_rooms.manager_employee_id`) — thiếu vế cuối là
+     * HOẶC phiếu của PHÒNG MÌNH QUẢN LÝ (`meeting_room_managers`, nhiều người — Phase 8) — thiếu vế cuối là
      * quản lý phòng không thấy phiếu cần chính mình duyệt (đã bắt gặp trong review Phase 1, xem
      * "ERP approval_inbox registry push gotcha" — luôn cộng đủ mọi nguồn nhìn thấy, đừng chỉ đọc
      * 1 nguồn rồi tưởng đủ).
      */
     private function applyVisibilityScope($query)
     {
         if (isCurrentEmployeeHasPermission('Xem tất cả phiếu đặt phòng họp')) {
             return;
         }
 
         $employeeId = auth()->id();
         $query->where(function ($q) use ($employeeId) {
             $q->where('booked_by_employee_id', $employeeId)
                 ->orWhereHas('participants', function ($p) use ($employeeId) {
                     $p->where('employee_id', $employeeId);
                 })
                 ->orWhereHas('room', function ($r) use ($employeeId) {
-                    $r->where('manager_employee_id', $employeeId);
+                    $r->whereHas('managers', function ($q) use ($employeeId) {
+                        $q->where('employee_id', $employeeId);
+                    });
                 });
         });
     }
 
     /**
      * Cùng luật `applyVisibilityScope()` nhưng cho 1 bản ghi đơn (GET detail) — KHÔNG dùng query
      * builder vì bản ghi đã load rồi, đọc thẳng thuộc tính cho rẻ hơn 1 query thừa.
      */
     private function canView(MeetingRoomBooking $booking)
     {
         if (isCurrentEmployeeHasPermission('Xem tất cả phiếu đặt phòng họp')) {
             return true;
         }
 
         $employeeId = (int) auth()->id();
         if ((int) $booking->booked_by_employee_id === $employeeId) {
             return true;
         }
 
         $room = $booking->room ?? MeetingRoom::find($booking->meeting_room_id);
-        if ($room && $room->manager_employee_id && (int) $room->manager_employee_id === $employeeId) {
+        if ($room && in_array($employeeId, $room->managerIds(), true)) {
             return true;
         }
 
         return $booking->participants()->where('employee_id', $employeeId)->exists();
     }
 
     /**
      * GET chi tiết — eager load đủ để tránh N+1 (participants + phòng + người tạo/cập nhật).
      * Bước 6 — gate luật nhìn thấy phiếu NGAY ĐẦU HÀM, trước khi trả bất kỳ dữ liệu nào.
      */
     public function loadDetail(MeetingRoomBooking $booking)
     {
         // `meeting.*`: popup Xem phiếu sinh từ cuộc họp hiện Loại meeting / Khách hàng / Chủ trì
         // + danh sách thành phần dự họp (Task 56) — eager load để không bắn 5 query lẻ.
         $booking->load([
-            'room.amenities', 'room.manager.info', 'purpose',
+            'room.amenities', 'room.managers.info', 'purpose',
             'meeting.meeting_type', 'meeting.host.info', 'meeting.company_members', 'meeting.customer_members',
             'participants.employee.info', 'employee_create.info', 'employee_update.info',
         ]);
 
         if (!$this->canView($booking)) {
             throw new \Exception('Bạn không có quyền xem phiếu này', 403);
         }
 
         return $this->attachDisplayNames($booking);
     }
@@ -352,21 +354,21 @@ class MeetingRoomBookingService extends BaseService
             $meeting->meeting_room_id = $request->meeting_room_id;
             $meeting->save();
 
             $booking = app(MeetingRoomBookingSyncService::class)->currentBooking($meeting);
 
             if (!$booking) {
                 throw new \Exception('Không tạo được phiếu đặt phòng cho cuộc họp này', 400);
             }
 
             $booking->load([
-                'room.amenities', 'room.manager.info', 'purpose',
+                'room.amenities', 'room.managers.info', 'purpose',
                 'participants.employee.info', 'employee_create.info', 'employee_update.info',
             ]);
 
             return $this->attachDisplayNames($booking);
         });
     }
 
     public function store(Request $request)
     {
         return DB::transaction(function () use ($request) {
@@ -415,21 +417,21 @@ class MeetingRoomBookingService extends BaseService
             // không có bước Chờ duyệt nào để gửi).
             if ((int) $status === MeetingRoomBooking::STATUS_CHO_DUYET) {
                 $this->notifyPendingApproval($booking, $room);
             } else {
                 $this->notifyApproved($booking);
             }
 
             $booking->warnings = $warnings;
 
             $booking->load([
-                'room.amenities', 'room.manager.info', 'purpose',
+                'room.amenities', 'room.managers.info', 'purpose',
                 'participants.employee.info', 'employee_create.info', 'employee_update.info',
             ]);
 
             return $this->attachDisplayNames($booking);
         });
     }
 
     /**
      * Task 13, Bước 6 — sửa phiếu.
      * - Khóa (423) kiểm NGAY ĐẦU HÀM, trước cả validate nghiệp vụ (quy ước CLAUDE.md bản ghi khóa).
@@ -549,21 +551,21 @@ class MeetingRoomBookingService extends BaseService
             // gộp thêm "Chờ duyệt" ở đây dù đôi khi status quay lại Chờ duyệt phía trên, vì đó
             // không nằm trong 5 sự kiện định nghĩa hoàn thành của Task 15 (chỉ Tạo phiếu MỚI mới
             // sinh "Chờ duyệt", không phải mọi lần phiếu chuyển VỀ Chờ duyệt).
             if ($timeOrRoomChanged) {
                 $this->notifyScheduleChanged($booking, $room);
             }
 
             $booking->warnings = $warnings;
 
             $booking->load([
-                'room.amenities', 'room.manager.info', 'purpose',
+                'room.amenities', 'room.managers.info', 'purpose',
                 'participants.employee.info', 'employee_create.info', 'employee_update.info',
             ]);
 
             return $this->attachDisplayNames($booking);
         });
     }
 
     /**
      * Task 14, Bước 1-2 — Duyệt (spec 5.3) + tự động Từ chối mọi phiếu Chờ duyệt CÙNG PHÒNG giao
      * giờ (spec 5.2 vế "duyệt phiếu nào phiếu đó thắng"). TOÀN BỘ trong 1 transaction có khóa —
@@ -642,21 +644,21 @@ class MeetingRoomBookingService extends BaseService
 
                 // Task 15, Bước 3 (spec mục 7) — "Từ chối" cho người đặt CŨNG áp dụng khi tự động
                 // từ chối (không chỉ từ chối thủ công), đúng chữ nghĩa task-15-brief.
                 $this->notifyRejected($conflict, $conflict->reject_reason);
             }
 
             // Task 15, Bước 3 — "Đã duyệt" cho người đặt + participants khi duyệt thủ công.
             $this->notifyApproved($booking);
 
             $booking->load([
-                'room.amenities', 'room.manager.info', 'purpose',
+                'room.amenities', 'room.managers.info', 'purpose',
                 'participants.employee.info', 'employee_create.info', 'employee_update.info',
             ]);
 
             return $this->attachDisplayNames($booking);
         });
     }
 
     /**
      * Task 14, Bước 5 — Từ chối (spec 5.3). Từ chối ≠ Hủy (spec 5.5): trạng thái + màu riêng,
      * `is_auto_rejected` LUÔN = 0 ở đây (chỉ auto-reject của `approve()` mới set = 1).
@@ -686,21 +688,21 @@ class MeetingRoomBookingService extends BaseService
             $booking->is_auto_rejected = 0;
             $booking->reject_reason = $reason;
             $booking->save();
 
             $this->logCatalogStatus($booking, 'reject', 'Chờ duyệt', 'Từ chối', $reason);
 
             // Task 15, Bước 3 (spec mục 7) — "Từ chối" thủ công cho người đặt.
             $this->notifyRejected($booking, $reason);
 
             $booking->load([
-                'room.amenities', 'room.manager.info', 'purpose',
+                'room.amenities', 'room.managers.info', 'purpose',
                 'participants.employee.info', 'employee_create.info', 'employee_update.info',
             ]);
 
             return $this->attachDisplayNames($booking);
         });
     }
 
     /**
      * Task 14, Bước 3-4 — Hủy (spec 5.5).
      *
@@ -746,42 +748,42 @@ class MeetingRoomBookingService extends BaseService
             $booking->cancelled_at = Carbon::now();
             $booking->cancel_reason = $reason;
             $booking->save();
 
             $this->logCatalogStatus($booking, 'cancel', $oldStatusText, 'Đã hủy', $reason);
 
             // Task 15, Bước 3 (spec mục 7) — "Hủy" cho người đặt + participants.
             $this->notifyCancelled($booking, $reason);
 
             $booking->load([
-                'room.amenities', 'room.manager.info', 'purpose',
+                'room.amenities', 'room.managers.info', 'purpose',
                 'participants.employee.info', 'employee_create.info', 'employee_update.info',
             ]);
 
             return $this->attachDisplayNames($booking);
         });
     }
 
     /**
-     * Spec 5.3: "Người duyệt = quản lý phòng (`manager_employee_id`) HOẶC người có quyền
+     * Spec 5.3: "Người duyệt = quản lý phòng (`room->managerIds()`, nhiều người — Phase 8) HOẶC người có quyền
      * *Duyệt phiếu đặt phòng họp*". Dùng chung cho approve/reject/cancel (spec 5.5 cũng liệt
      * đúng 2 vế này + người đặt).
      *
      * ⚠️ CỐ TÌNH KHÔNG gắn `checkPermission:Duyệt phiếu đặt phòng họp` ở tầng route cho
      * approve/reject (xem `Routes/api.php`): route middleware chỉ kiểm ĐƯỢC quyền tĩnh của
      * role, không kiểm được "có phải quản lý CỦA ĐÚNG PHÒNG này không" — 1 phòng cụ thể. Gắn
      * cứng middleware đó sẽ CHẶN LUÔN quản lý phòng không có quyền 1580 (trường hợp bình thường,
      * xem F1/F2 của task-13-report + G4/I3 của task-14), trái spec 5.3. Gate thật nằm ở ĐÂY.
      */
     private function canActOnApprovalByRoom(MeetingRoom $room)
     {
-        $isRoomManager = $room->manager_employee_id && (int) $room->manager_employee_id === (int) auth()->id();
+        $isRoomManager = in_array((int) auth()->id(), $room->managerIds(), true);
 
         return $isRoomManager || isCurrentEmployeeHasPermission('Duyệt phiếu đặt phòng họp');
     }
 
     /**
      * ⚠️ 8 hàm dưới đây đổi từ `private` → `public` ở Phase 4 (19/09/2026) để
      * `MeetingRoomBookingSyncService` (đồng bộ phiếu từ cuộc họp) **dùng lại nguyên văn**, KHÔNG chép
      * lại luật sang service khác: luật chống trùng (mutex `lockForUpdate` trên dòng phòng), luật 5.1,
      * sinh mã chống trùng và 3 loại thông báo phải nằm ĐÚNG 1 CHỖ — chép ra là sớm muộn 2 bản
      * lệch nhau mà không ai biết. Thân hàm giữ nguyên, chỉ đổi tầm nhìn.
@@ -1049,21 +1051,21 @@ class MeetingRoomBookingService extends BaseService
             $booking->has_approve_permission = $hasApprovePermission;
         }
 
         return $bookings;
     }
 
     // ============================================================================================
     // Task 15 (plan quan-ly-phong-hop) — 5 loại thông báo nghiệp vụ (spec mục 7, prefix [DPH]).
     // Đọc task-15-brief.md — BẪY 1: `EmployeeInfoService::sendNotification()`/`sendToAllNotification()`
     // nhận `employee_info_id`, KHÔNG phải `employees.id`. Bảng phòng họp lưu TOÀN BỘ theo
-    // `employees.id` (`booked_by_employee_id`, `host_employee_id`, `manager_employee_id`,
+    // `employees.id` (`booked_by_employee_id`, `host_employee_id`, `meeting_room_managers.employee_id`,
     // `meeting_room_booking_participants.employee_id`) — MỌI nơi gửi thông báo bắt buộc đi qua
     // ĐÚNG 1 helper `mapEmployeeIdsToEmployeeInfoIds()` bên dưới, không tự map lẻ ở từng chỗ.
     // ============================================================================================
 
     const NOTIFICATION_PREFIX = '[DPH]';
 
     /**
      * BẪY 1 — helper DUY NHẤT map `employees.id` -> `employees.employee_info_id`. Đã đo trên DB
      * gộp: chỉ 2/1099 nhân viên có `id == employee_info_id`, truyền thẳng `employees.id` vào
      * `EmployeeInfoService::sendNotification()`/`sendToAllNotification()` là thông báo bay sang
@@ -1183,26 +1185,27 @@ class MeetingRoomBookingService extends BaseService
         } catch (\Throwable $e) {
             Log::error('MeetingRoomBooking: gửi thông báo "' . $action . '" thất bại cho phiếu #' . $booking->id, [
                 'exception' => $e,
             ]);
         }
     }
 
     /** Sự kiện 1/5 (spec mục 7) — Tạo phiếu cần duyệt -> quản lý phòng, nhóm "Chờ duyệt". */
     public function notifyPendingApproval(MeetingRoomBooking $booking, MeetingRoom $room)
     {
-        if (!$room->manager_employee_id) {
+        $managerIds = $room->managerIds();
+        if (empty($managerIds)) {
             return;
         }
 
         $this->sendBookingNotification(
-            [$room->manager_employee_id],
+            $managerIds,
             'Chờ duyệt',
             $booking,
             $this->roomTimeNote($booking, $room, false),
             'meeting_room_booking_pending'
         );
     }
 
     /**
      * Sự kiện 2/5 (spec mục 7) — Duyệt (thủ công HOẶC tạo thẳng ở phòng không cần duyệt) ->
      * người đặt + participants, nhóm "Đã duyệt".
diff --git a/Modules/Meeting/Services/MeetingRoomService.php b/Modules/Meeting/Services/MeetingRoomService.php
index ede7b4146..ab17acc10 100644
--- a/Modules/Meeting/Services/MeetingRoomService.php
+++ b/Modules/Meeting/Services/MeetingRoomService.php
@@ -37,25 +37,25 @@ class MeetingRoomService extends BaseService
     public function __construct(MeetingRoomBookingService $meetingRoomBookingService)
     {
         $this->meetingRoomBookingService = $meetingRoomBookingService;
     }
 
     public function index(Request $request)
     {
         // ⚠️ N+1 (review Task 3 + fix round 1 IMPORTANT 3 + fix round 1 mục "việc BE"):
         // `amenities` tránh N+1 khi Resource đọc quan hệ tiện nghi; `employee_create.info` /
         // `employee_update.info` tránh N+1 khi Resource đọc `employee_create_name` /
-        // `employee_update_name`; `company` / `manager.info` tránh N+1 khi Resource đọc
-        // `company_name` / `manager_name` (mới thêm — trước đây FE tự tra tên từ
-        // $store.state.employees, bỏ sót quản lý đã nghỉ việc).
+        // `employee_update_name`; `company` / `managers` tránh N+1 khi Resource đọc
+        // `company_name` / `manager_names` (Phase 8 lượt A1, T111 — trước đây 1 quan hệ
+        // `manager.info`, nay `managers` vì 1 phòng có NHIỀU người phụ trách).
         $query = MeetingRoom::query()->select('meeting_rooms.*')
-            ->with(['amenities', 'employee_create.info', 'employee_update.info', 'company', 'manager.info']);
+            ->with(['amenities', 'employee_create.info', 'employee_update.info', 'company', 'managers']);
 
         if (isset($request->keyword)) {
             $escapedKeyword = escapeLikeKeyword($request->keyword);
             if ($escapedKeyword !== '') {
                 // Task 44 — bỏ hẳn trường Mã: tìm nhanh nay theo TÊN + VỊ TRÍ (đúng những gì
                 // người dùng nhìn thấy trên bảng).
                 $query->where(function ($q) use ($escapedKeyword) {
                     $q->where('name', 'like', '%' . $escapedKeyword . '%')
                         ->orWhere('location', 'like', '%' . $escapedKeyword . '%');
                 });
@@ -121,21 +121,23 @@ class MeetingRoomService extends BaseService
      */
     public function bookableForCurrentEmployee(Request $request)
     {
         $bookerCompanyId = optional(auth()->user()->info)->company_id;
 
         $query = MeetingRoom::query()->select('meeting_rooms.*')
             // Tránh N+1 khi Resource đọc tiện nghi + tên người quản lý của TỪNG phòng
             // (Task 55 — panel "Thông tin phòng" của popup đặt phòng).
             // `company` thêm ở Task 69 (tên công ty làm dòng phụ của select phòng) — eager load
             // để không N+1 khi Resource đọc tên công ty của TỪNG phòng.
-            ->with(['amenities', 'manager.info', 'company'])
+            // Phase 8 lượt A1 (T111): `manager.info` -> `managers` (1 phòng nay nhiều người phụ
+            // trách; quan hệ `manager()` đã bị xoá ở T110).
+            ->with(['amenities', 'managers', 'company'])
             ->where('status', MeetingRoom::STATUS_ACTIVE);
 
         if (isset($request->keyword)) {
             $escapedKeyword = escapeLikeKeyword($request->keyword);
             if ($escapedKeyword !== '') {
                 // Task 44 — bỏ hẳn trường Mã: tìm nhanh nay theo TÊN + VỊ TRÍ (đúng những gì
                 // người dùng nhìn thấy trên bảng).
                 $query->where(function ($q) use ($escapedKeyword) {
                     $q->where('name', 'like', '%' . $escapedKeyword . '%')
                         ->orWhere('location', 'like', '%' . $escapedKeyword . '%');
@@ -670,29 +672,39 @@ class MeetingRoomService extends BaseService
             'close_time' => MeetingRoom::resolveConfig(null, optional($regulation)->meeting_room_close_time, '20:00:00'),
         ];
     }
 
     protected function catalogTable(): string
     {
         return 'meeting_rooms';
     }
 
     /**
-     * ⚠️ KHÔNG khai `amenities` ở đây: `catalogSnapshot()` đọc `$model->{$column}`, mà
-     * `$room->amenities` là quan hệ (Collection) chứ không phải cột. Tiện nghi được ghép vào
-     * snapshot ở `roomSnapshot()` bên dưới dưới dạng chuỗi tên.
+     * ⚠️ KHÔNG khai `amenities` (cũng KHÔNG khai `managers` — Phase 8) ở đây: `catalogSnapshot()`
+     * đọc `$model->{$column}`, mà cả hai đều là QUAN HỆ (Collection), không phải cột thật. Cả 2
+     * được ghép vào snapshot ở `roomSnapshot()` bên dưới dưới dạng chuỗi tên (khoá ảo).
+     */
+    /**
+     * Phase 8 lượt A1 (T111) — bỏ `manager_employee_id` khỏi cột theo dõi lịch sử: cột đã bị
+     * DROP ở migration `2026_09_23_000001_create_meeting_room_managers_table` (T109), đọc
+     * `$model->manager_employee_id` sau khi drop chỉ ra `null` chứ không lỗi, nên nếu để lại
+     * trong mảng này lịch sử sẽ âm thầm ghi "Người quản lý phòng: ... -> (trống)" ở MỌI lần sửa.
+     *
+     * Phase 8 lượt A2 (T117) — nhóm phụ trách (bảng `meeting_room_managers`, nhiều người) NAY ĐÃ
+     * vào lịch sử qua khoá ảo `managers` ở `roomSnapshot()` bên dưới + nhãn đăng ký trong
+     * `App\Services\CatalogHistoryService::TABLES['meeting_rooms']['columns']['managers']`.
      */
     protected function catalogColumns(): array
     {
         return [
             'name', 'company_id', 'allow_cross_company', 'location', 'capacity',
-            'manager_employee_id', 'require_approval', 'open_time', 'close_time',
+            'require_approval', 'open_time', 'close_time',
             'checkin_grace_minutes', 'description', 'status',
         ];
     }
 
     /**
      * Đổi giá trị thô sang giá trị HIỂN THỊ để log TỰ CHỨA (skill entity-history §3): đọc lại
      * lịch sử 1 năm sau vẫn thấy đúng tên công ty / người quản lý tại thời điểm đó, kể cả khi
      * công ty đổi tên hoặc nhân viên đã nghỉ việc (lúc đó tra id ra rỗng).
      */
     protected function catalogDisplay(string $column, $value)
@@ -706,48 +718,57 @@ class MeetingRoomService extends BaseService
         }
 
         if ($column === 'allow_cross_company' || $column === 'require_approval') {
             return $value ? 'Có' : 'Không';
         }
 
         if ($column === 'company_id') {
             return optional(Company::find($value))->name ?: $value;
         }
 
-        if ($column === 'manager_employee_id') {
-            // ⚠️ `Employee::fullname` (accessor trên Employee) trả NULL — tên thật nằm ở
-            // `employee_infos.fullname`. Dùng nhầm thì lịch sử ghi "(trống)" mà KHÔNG có lỗi nào
-            // báo ra (đã đo bằng tinker 19/09/2026). Không tra được tên thì giữ nguyên id để còn
-            // lần ra người, đừng nuốt thành null.
-            $employee = \Modules\Human\Entities\Employee::with('info')->find($value);
-
-            return optional(optional($employee)->info)->fullname ?: $value;
-        }
+        // `manager_employee_id` (case cũ, 1 người phụ trách) đã bị xoá cùng với cột ở T109/T111.
+        // Nhóm phụ trách (nhiều người, Phase 8) KHÔNG qua hàm này: khoá ảo `managers` được dựng
+        // thẳng thành chuỗi tên ở `roomSnapshot()` (giống `amenities`), không phải cột thật nên
+        // `catalogSnapshot()`/`catalogDisplay()` không bao giờ thấy khoá này.
 
         return $value;
     }
 
     /**
-     * Snapshot ĐẦY ĐỦ của 1 phòng = các cột theo dõi + danh sách TIỆN NGHI.
+     * Snapshot ĐẦY ĐỦ của 1 phòng = các cột theo dõi + danh sách TIỆN NGHI + danh sách NGƯỜI PHỤ
+     * TRÁCH.
      *
      * Tiện nghi nằm ở bảng pivot nên không thể để `catalogSnapshot()` tự đọc; ghép vào đây dưới
      * khoá ảo `amenities` (đã khai nhãn trong `CatalogHistoryService::TABLES`). Sắp xếp theo id
      * để 2 lần chụp cùng dữ liệu luôn ra cùng chuỗi — nếu không, đổi thứ tự sync là log báo
      * "đã thay đổi" trong khi thực tế không đổi gì.
+     *
+     * Phase 8 (T117, lượt A2) — nhóm phụ trách (`meeting_room_managers`, nhiều người) trước đây
+     * CHƯA vào lịch sử (bàn giao của A1, xem docblock `catalogColumns()`). Thêm khoá ảo `managers`
+     * cùng khuôn `amenities`: KHÔNG dùng `$room->managerNames()` (đệm ở `$managerNamesCache` +
+     * dựa vào `relationLoaded('managers')` của chính model — gọi lần 2 SAU KHI `sync()` đã đổi
+     * pivot vẫn trả kết quả CŨ, vì quan hệ coi như "đã nạp" từ lần gọi snapshot TRƯỚC, không tự
+     * query lại) mà PHẢI gọi thẳng `$room->managers()` (query mới mỗi lần, không qua cache) —
+     * đúng lý do `roomSnapshot()` này tồn tại thay vì đọc field cache sẵn trên Entity.
      */
     private function roomSnapshot(MeetingRoom $room): array
     {
         $snapshot = $this->catalogSnapshot($room);
         $snapshot['amenities'] = $room->amenities()
             ->orderBy('meeting_room_amenities.id')
             ->pluck('meeting_room_amenities.name')
             ->implode(', ');
+        $snapshot['managers'] = $room->managers()
+            ->orderBy('employees.id')
+            ->get()
+            ->pluck('fullname')
+            ->implode(', ');
 
         return $snapshot;
     }
 
     /**
      * Khóa / Mở khóa — ĐỂ Ở SERVICE (trước đây controller tự đổi `status` rồi `save()`), vì đổi
      * trạng thái cũng phải ghi lịch sử mà bộ ghi log nằm ở service.
      */
     public function lock(MeetingRoom $room)
     {
@@ -789,51 +810,58 @@ class MeetingRoomService extends BaseService
                 }
             }
 
             // Quyết định user 19/09/2026: form KHÔNG còn ô Công ty — **công ty nào tạo thì phòng
             // thuộc công ty đó**. `company_id` KHÔNG lấy từ payload (client gửi lên cũng bỏ qua):
             // lúc tạo do `BaseModel::creating()` tự điền theo người đăng nhập, lúc sửa giữ nguyên.
             // `department_id`/`part_id` đã bị DROP khỏi bảng (migration 2026_09_19_000001) nên
             // hook `BaseModel` cũng không còn chỗ để tự điền nhầm đơn vị của người tạo.
             $data = $request->only([
                 'name', 'allow_cross_company',
-                'location', 'capacity', 'manager_employee_id', 'require_approval',
+                'location', 'capacity', 'require_approval',
                 'open_time', 'close_time', 'checkin_grace_minutes', 'description',
             ]);
 
             // Snapshot TRƯỚC khi đổi dữ liệu (kể cả pivot tiện nghi), nếu không diff luôn rỗng.
             $before = $id ? $this->roomSnapshot($room) : null;
 
             if ($id) {
                 $room->update($data);
             } else {
                 $data['status'] = MeetingRoom::STATUS_ACTIVE;
                 $room = MeetingRoom::create($data);
             }
 
             $room->amenities()->sync($request->input('amenity_ids', []));
 
+            // Phase 8 lượt A1 (T111) — nhóm phụ trách: đồng bộ TRONG transaction đang có của cả
+            // tạo mới lẫn sửa (KHÔNG mở transaction thứ hai lồng nhau). `MeetingRoomRequest`
+            // (T112) đã bắt `manager_employee_ids` là mảng bắt buộc >= 1 phần tử.
+            // Fix vòng 1 (lượt A2) — gọi `syncManagers()` (không tự `managers()->sync()`) để
+            // Entity tự xoá cache `managerIds()`/`managerNames()` + quan hệ đã nạp ngay sau đồng bộ.
+            $room->syncManagers($request->input('manager_employee_ids', []));
+
             // Ghi lịch sử SAU khi sync pivot để thay đổi tiện nghi cũng vào log. Dùng thẳng
             // `CatalogHistoryService` thay cho `logCatalogUpdate()` của trait: hàm của trait tự
             // dựng `$after` từ `catalogColumns()` nên sẽ THIẾU khoá ảo `amenities`, khiến mọi
             // lần sửa đều báo "Tiện nghi: ... -> (trống)".
             $after = $this->roomSnapshot($room);
             if ($id) {
                 app(CatalogHistoryService::class)->logUpdate($this->catalogTable(), $room->id, $before, $after);
             } else {
                 app(CatalogHistoryService::class)->log($this->catalogTable(), $room->id, 'create', [], $after);
             }
 
-            // `company` / `manager.info` để DetailMeetingRoomResource đọc `company_name` /
-            // `manager_name` ngay sau khi lưu mà không phải lazy-load (fix round 1, đồng bộ
-            // với eager load trong index()).
-            return $room->load(['amenities', 'company', 'manager.info']);
+            // `company` / `managers` để DetailMeetingRoomResource đọc `company_name` /
+            // `manager_names` ngay sau khi lưu mà không phải lazy-load (fix round 1, đồng bộ
+            // với eager load trong index(); Phase 8 lượt A1 T111 đổi `manager.info` -> `managers`).
+            return $room->load(['amenities', 'company', 'managers']);
         });
     }
 
     /**
      * Fix đợt review tổng, mục A.1: `delete()` trần để lại pivot mồ côi vĩnh viễn ở
      * `meeting_room_room_amenity` (không có FK ON DELETE CASCADE trước fix mục A.3) — 78 dòng đã
      * đo được trong DB trước khi sửa. `detach()` TRƯỚC khi xóa phòng, cùng 1 transaction với
      * lệnh xóa (controller đã bọc `DB::transaction` quanh lời gọi hàm này).
      *
      * Bẫy 3 (review Phase 1, task-11-brief): `MeetingRoomController::destroy()` kiểm
@@ -968,22 +996,25 @@ class MeetingRoomService extends BaseService
             $raw = isset($item[$field]) ? trim((string) $item[$field]) : '';
             if ($raw !== '' && $this->mapYesNoToValue($raw) === null) {
                 $errors[] = $label . ' không hợp lệ (chỉ nhận: Có hoặc Không)';
             }
         }
 
         if ($this->mapStatusToValue(isset($item['status']) ? (string) $item['status'] : '') === null) {
             $errors[] = 'Trạng thái không hợp lệ (chỉ nhận đúng: Hoạt động hoặc Khóa)';
         }
 
-        $managerName = isset($item['manager_name']) ? trim((string) $item['manager_name']) : '';
-        if ($managerName !== '' && $this->resolveManagerId($managerName, $managerError) === null) {
+        // Phase 8 (T116, lượt A2) — phòng nay bắt buộc >= 1 người phụ trách (chốt ở lượt A1), cột
+        // "Người quản lý" nhận NHIỀU tên ngăn bằng `;`. Không còn `!== ''` để bỏ qua như trước: rỗng
+        // giờ CŨNG là lỗi dòng (không phải optional nữa).
+        $managerNameRaw = isset($item['manager_name']) ? (string) $item['manager_name'] : '';
+        if ($this->resolveManagerIds($managerNameRaw, $managerError) === null) {
             $errors[] = $managerError;
         }
 
         $amenityNames = isset($item['amenity_names']) ? trim((string) $item['amenity_names']) : '';
         if ($amenityNames !== '') {
             // Chỉ cần biết tên nào KHÔNG có trong danh mục (tham chiếu $missing), id lấy ở bước ghi.
             $this->resolveAmenityIds($amenityNames, $missing);
             if (!empty($missing)) {
                 $errors[] = 'Tiện nghi không có trong danh mục: ' . implode(', ', $missing);
             }
@@ -1018,70 +1049,115 @@ class MeetingRoomService extends BaseService
                 $key = $this->normalizeName($name);
                 if ($existingByName->has($key)) {
                     throw new \Exception('Tên phòng đã tồn tại trong công ty này');
                 }
 
                 $status = $this->mapStatusToValue(isset($item['status']) ? (string) $item['status'] : '');
                 if ($status === null) {
                     throw new \Exception('Trạng thái không hợp lệ (chỉ nhận: Hoạt động hoặc Khóa)');
                 }
 
-                $managerId = null;
-                $managerName = trim((string) ($item['manager_name'] ?? ''));
-                if ($managerName !== '') {
-                    $managerId = $this->resolveManagerId($managerName, $managerError);
-                    if ($managerId === null) {
-                        throw new \Exception($managerError);
-                    }
+                // Phase 8 (T116, lượt A2) — nhiều người phụ trách ngăn bằng `;`, bắt buộc >= 1
+                // (khớp validateRoomRow ở trên, cùng nguồn lỗi `resolveManagerIds()`).
+                $managerNameRaw = (string) ($item['manager_name'] ?? '');
+                $managerIds = $this->resolveManagerIds($managerNameRaw, $managerError);
+                if ($managerIds === null) {
+                    throw new \Exception($managerError);
                 }
 
                 $amenityIds = [];
                 $amenityNames = trim((string) ($item['amenity_names'] ?? ''));
                 if ($amenityNames !== '') {
                     $amenityIds = $this->resolveAmenityIds($amenityNames, $missing);
                     if (!empty($missing)) {
                         throw new \Exception('Tiện nghi không có trong danh mục: ' . implode(', ', $missing));
                     }
                 }
 
                 $capacityRaw = trim((string) ($item['capacity'] ?? ''));
 
                 // `company_id` KHÔNG truyền: hook `BaseModel::creating()` gán theo người đăng nhập
                 // (cùng luật với tạo tay ở màn danh mục).
                 $room = MeetingRoom::create([
                     'name' => $name,
                     'location' => trim((string) ($item['location'] ?? '')) ?: null,
                     'capacity' => $capacityRaw === '' ? null : (int) $capacityRaw,
-                    'manager_employee_id' => $managerId,
                     'require_approval' => $this->mapYesNoToValue((string) ($item['require_approval'] ?? '')) ?? 0,
                     'allow_cross_company' => $this->mapYesNoToValue((string) ($item['allow_cross_company'] ?? '')) ?? 0,
                     'status' => $status,
                 ]);
 
+                // BS-3 (lượt A2) — TRƯỚC đây gán thẳng `manager_employee_id` trong mảng `create()`
+                // ở trên: cột đã bị drop ở A1 nên KHÔNG còn trong `$fillable`, Eloquent ÂM THẦM BỎ
+                // QUA key lạ (không throw MassAssignmentException ở Laravel 8 mặc định) -> import
+                // xong phòng KHÔNG CÓ ai phụ trách, dù cột "Người quản lý" trong Excel có giá trị.
+                // Đổi sang `syncManagers()` (fix vòng 1 — không tự `managers()->sync()`, xem
+                // docblock trên Entity) sau `create()`, đúng khuôn `amenities()->sync()` ngay dưới.
+                $room->syncManagers($managerIds);
+
                 if (!empty($amenityIds)) {
                     $room->amenities()->sync($amenityIds);
                 }
 
                 // Import cũng là một lần TẠO -> phải có vết trong Lịch sử như tạo tay.
                 $this->logCatalogCreate($room);
 
                 $existingByName->put($key, $room);
                 $success++;
             } catch (\Exception $e) {
                 $failed++;
                 $errors[] = ['row' => $index + 2, 'message' => $e->getMessage()];
             }
         }
 
         return ['total' => $total, 'success' => $success, 'failed' => $failed, 'errors' => $errors];
     }
 
+    /**
+     * Phase 8 (T116, lượt A2) — "Tên A; Tên B" -> [id, id]. Phòng bắt buộc >= 1 người phụ trách
+     * (chốt ở lượt A1): rỗng sau khi tách/trim/bỏ phần tử rỗng thì trả `null` + lý do. Dừng ở tên
+     * ĐẦU TIÊN không khớp (khớp khuôn báo lỗi hiện có của file: 1 lỗi rõ ràng cho dòng đó, không
+     * gộp nhiều lỗi cùng ô — xem `resolveManagerId()`/`resolveAmenityIds()` bên dưới).
+     *
+     * @return int[]|null
+     */
+    private function resolveManagerIds(string $rawNames, ?string &$error = null): ?array
+    {
+        $error = null;
+
+        $names = array_values(array_filter(
+            array_map('trim', explode(';', $rawNames)),
+            function ($name) {
+                return $name !== '';
+            }
+        ));
+
+        if (empty($names)) {
+            $error = 'Phòng phải có ít nhất 1 người phụ trách';
+
+            return null;
+        }
+
+        $ids = [];
+        foreach ($names as $name) {
+            $id = $this->resolveManagerId($name, $managerError);
+            if ($id === null) {
+                $error = $managerError;
+
+                return null;
+            }
+            $ids[] = $id;
+        }
+
+        return array_values(array_unique($ids));
+    }
+
     /** Tên nhân viên -> id. Không thấy hoặc trùng nhiều người thì trả null + gán lý do vào $error. */
     private function resolveManagerId(string $managerName, ?string &$error = null): ?int
     {
         $error = null;
         $matches = \Modules\Human\Entities\Employee::query()
             ->whereHas('info', function ($q) use ($managerName) {
                 $q->whereRaw('LOWER(TRIM(fullname)) = ?', [mb_strtolower(trim($managerName), 'UTF-8')]);
             })
             ->pluck('id');
 
diff --git a/Modules/Meeting/Transformers/MeetingRoom/BookableMeetingRoomResource.php b/Modules/Meeting/Transformers/MeetingRoom/BookableMeetingRoomResource.php
index 41dca8707..a56efe301 100644
--- a/Modules/Meeting/Transformers/MeetingRoom/BookableMeetingRoomResource.php
+++ b/Modules/Meeting/Transformers/MeetingRoom/BookableMeetingRoomResource.php
@@ -1,21 +1,21 @@
 <?php
 
 namespace Modules\Meeting\Transformers\MeetingRoom;
 
 use Modules\Human\Transformers\ApiResource;
 
 /**
  * Task 17 fix round 1 (plan quan-ly-phong-hop) — payload GỌN cho `GET meeting/rooms/bookable`,
  * dùng trong modal đặt phòng (`BookingFormModal.vue`). Endpoint này KHÔNG gắn `checkPermission`
  * (mọi nhân viên đặt phòng được — quyết định #8), nên Resource CHỈ trả field modal thật sự cần để
- * chọn/lọc phòng — KHÔNG trả `manager_employee_id` thô và ĐẶC BIỆT
+ * chọn/lọc phòng — KHÔNG trả id thô của người phụ trách và ĐẶC BIỆT
  * KHÔNG trả `checkin_qr_token` (credential check-in QR, Phase 5 — đã bịt ở
  * `DetailMeetingRoomResource` CRITICAL 1, endpoint mới này không được mở lại cửa sau).
  */
 class BookableMeetingRoomResource extends ApiResource
 {
     public function toArray($request): array
     {
         return [
             'id' => $this->id,
             'name' => $this->name,
@@ -42,22 +42,29 @@ class BookableMeetingRoomResource extends ApiResource
             'allow_outside_hours' => (bool) $this->allow_outside_hours,
             // Task 76 — chỉ có khi gọi `GET meeting/rooms/availability` (endpoint `bookable` không
             // biết khung giờ nên để null, FE tự hiểu là "chưa xét"):
             //   free | pending | busy  + thông tin phiếu đang chạm giờ + cờ ngoài giờ mở cửa.
             'availability' => $this->availability,
             'conflict' => $this->conflict,
             'outside_hours' => $this->outside_hours === null ? null : (bool) $this->outside_hours,
             // Task 77 — chỉ có khi phòng `busy`: khe trống GẦN NHẤT trong ngày, dài đúng bằng thời
             // lượng đang định đặt (`['start' => 'HH:mm', 'end' => 'HH:mm']`). Hết chỗ trong ngày -> null.
             'next_free_slot' => $this->next_free_slot,
-            // `Employee::fullname` (accessor) trả NULL — tên thật nằm ở `employee_infos.fullname`.
-            'manager_name' => optional(optional($this->manager)->info)->fullname,
+            // Phase 8 (BS-2, lượt A2) — quan hệ `manager()` (1 người) bị xoá ở A1, `manager_name`
+            // trước đây luôn ra `null`. Fix vòng 1 (chốt tên khoá, xem `p8-A2-report.md` mục
+            // "Fix vòng 1" #1): GIỮ NGUYÊN tên khoá `manager_name` (không đổi sang biến thể khác) —
+            // đúng khoá mà `MeetingRoomResource`/`DetailMeetingRoomResource` cùng trả, VÀ tình cờ
+            // khớp lại đúng khoá FE `BookingFormModal.vue` (~dòng 464, ~1925) đang đọc
+            // (`selectedRoomInfo.manager_name`) — sửa xong không cần đợi lượt FE nữa. Ghép bằng
+            // `"; "` (khớp dấu `resolveManagerIds()` dùng để TÁCH tên lúc import). KHÔNG trả id thô
+            // của người phụ trách (giữ đúng chủ ý cũ của file).
+            'manager_name' => implode('; ', $this->managerNames()),
             'description' => $this->description,
             'amenities' => $this->whenLoaded('amenities', function () {
                 return $this->amenities->map(function ($amenity) {
                     return [
                         'id' => $amenity->id,
                         'name' => $amenity->name,
                     ];
                 });
             }),
         ];
diff --git a/Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php b/Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php
index 39d80b706..7068ad63e 100644
--- a/Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php
+++ b/Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php
@@ -23,22 +23,28 @@ class DetailMeetingRoomResource extends ApiResource
         return [
             'id' => $this->id,
             'name' => $this->name,
             'company_id' => $this->company_id,
             // Fix round 1 (review, đồng bộ với MeetingRoomResource) — tránh FE tự tra tên qua
             // $store.state.employees (chỉ có nhân viên đang làm việc, bỏ sót quản lý đã nghỉ).
             'company_name' => optional($this->company)->name,
             'allow_cross_company' => (bool) $this->allow_cross_company,
             'location' => $this->location,
             'capacity' => $this->capacity,
-            'manager_employee_id' => $this->manager_employee_id,
-            'manager_name' => optional($this->manager)->fullname,
+            // Phase 8 lượt A1 (T113) + lượt A2 fix vòng 1 (chốt tên khoá, xem `p8-A2-report.md`
+            // mục "Fix vòng 1" #1 — ĐỒNG BỘ Y HỆT `MeetingRoomResource`, đọc comment đầy đủ ở đó)
+            // — 3 khoá CỐ ĐỊNH: `manager_employee_ids` (mảng id), `manager_names` (mảng tên) và
+            // `manager_name` (chuỗi ghép `"; "`, KHÔNG BAO GIỜ trả `null`) — khoá ghép phẩy riêng
+            // cho UI của lượt A1 đã BỎ HẲN.
+            'manager_employee_ids' => $this->managerIds(),
+            'manager_names' => $this->managerNames(),
+            'manager_name' => implode('; ', $this->managerNames()),
             'require_approval' => (bool) $this->require_approval,
             'open_time' => $this->open_time,
             'close_time' => $this->close_time,
             'checkin_grace_minutes' => $this->checkin_grace_minutes,
             'checkin_qr_token' => $this->when(
                 isCurrentEmployeeHasPermission('Khai báo phòng họp'),
                 $this->checkin_qr_token
             ),
             'description' => $this->description,
             'status' => $this->status,
diff --git a/Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php b/Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php
index 064c584f6..aaa6a08a0 100644
--- a/Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php
+++ b/Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php
@@ -25,22 +25,36 @@ class MeetingRoomResource extends ApiResource
             'id' => $this->id,
             'name' => $this->name,
             'company_id' => $this->company_id,
             // Fix round 1 (review) — FE trước đây tự tra tên công ty/người quản lý từ
             // $store.state.employees (chỉ chứa nhân viên ĐANG làm việc) nên phòng có quản lý đã
             // nghỉ việc hiện "—" dù dữ liệu còn nguyên. BE trả sẵn tên, tránh sai dữ liệu âm thầm.
             'company_name' => optional($this->company)->name,
             'allow_cross_company' => (bool) $this->allow_cross_company,
             'location' => $this->location,
             'capacity' => $this->capacity,
-            'manager_employee_id' => $this->manager_employee_id,
-            'manager_name' => optional($this->manager)->fullname,
+            // Phase 8 lượt A1 (T113) + lượt A2 fix vòng 1 (chốt tên khoá, xem `p8-A2-report.md`
+            // mục "Fix vòng 1" #1) — 1 phòng nay NHIỀU người phụ trách: `manager_employee_id`
+            // (1 người) đổi thành 3 khoá CỐ ĐỊNH, KHÔNG được thêm biến thể mới:
+            //   - `manager_employee_ids` (mảng id) — FE dùng để tô lại select nhiều người.
+            //   - `manager_names` (mảng tên, cùng thứ tự `manager_employee_ids`) — FE dùng để tự
+            //     dựng "2 tên + +N" hoặc render danh sách.
+            //   - `manager_name` (chuỗi ghép bằng `"; "`, KHÔNG BAO GIỜ trả `null`, rỗng thì `''`)
+            //     — dùng cho cột bảng/Excel; `"; "` khớp đúng dấu mà `resolveManagerIds()` (import)
+            //     dùng để TÁCH tên, nên 1 file Excel xuất ra re-import lại được thẳng.
+            // Lượt A1 từng đặt thêm 1 khoá ghép bằng dấu phẩy cho riêng UI — đã BỎ HẲN ở fix vòng 1
+            // vì 2 khoá cùng nghĩa dễ khiến FE/export mỗi chỗ đọc 1 kiểu; chỉ còn 3 khoá cố định ở
+            // trên. Nguồn tên GIỮ NGUYÊN như `manager()` cũ (`Employee::fullname`, xem
+            // `MeetingRoom::managerNames()`).
+            'manager_employee_ids' => $this->managerIds(),
+            'manager_names' => $this->managerNames(),
+            'manager_name' => implode('; ', $this->managerNames()),
             'require_approval' => (bool) $this->require_approval,
             'open_time' => $this->open_time,
             'close_time' => $this->close_time,
             'checkin_grace_minutes' => $this->checkin_grace_minutes,
             'status' => $this->status,
             'status_text' => $this->status == MeetingRoom::STATUS_ACTIVE ? 'Hoạt động' : 'Khóa',
             // Task 45 — 3 khoá dạng CHUỖI phục vụ file Xuất Excel (`ExportColumnRegistry`):
             // `DynamicExport` đổ thẳng giá trị vào ô nên cột nào cũng phải là scalar; `amenities`
             // là MẢNG object và 2 cờ kia là boolean -> vào ô Excel sẽ ra "Array"/"1".
             'amenity_names' => $this->whenLoaded('amenities', function () {
diff --git a/Modules/Meeting/Transformers/MeetingRoomBooking/DetailMeetingRoomBookingResource.php b/Modules/Meeting/Transformers/MeetingRoomBooking/DetailMeetingRoomBookingResource.php
index 27477e081..8a119a29f 100644
--- a/Modules/Meeting/Transformers/MeetingRoomBooking/DetailMeetingRoomBookingResource.php
+++ b/Modules/Meeting/Transformers/MeetingRoomBooking/DetailMeetingRoomBookingResource.php
@@ -8,22 +8,25 @@ use Modules\Meeting\Entities\MeetingRoomBooking;
 
 /**
  * Plan quan-ly-phong-hop, Task 13 — chi tiết 1 phiếu đặt phòng (popup Xem/Sửa, và cũng dùng làm
  * response của tạo mới/cập nhật để FE có ngay cờ hành động + `warnings` mà không phải gọi lại).
  */
 class DetailMeetingRoomBookingResource extends ApiResource
 {
     public function toArray($request): array
     {
         $isOwner = (int) $this->booked_by_employee_id === (int) auth()->id();
-        $isRoomManager = optional($this->room)->manager_employee_id
-            && (int) $this->room->manager_employee_id === (int) auth()->id();
+        // Phase 8 — phòng nay có NHIỀU người phụ trách (`meeting_room_managers`). Phòng chưa load
+        // thì `optional($this->room)->managerIds()` gọi trên `null` -> `optional()` trả `null` ->
+        // `in_array(..., null)` sẽ lỗi TypeError, nên phải chốt mảng rỗng bằng `?: []` (đúng yêu
+        // cầu "phòng chưa load thì phải ra false").
+        $isRoomManager = in_array((int) auth()->id(), optional($this->room)->managerIds() ?: [], true);
         // Fix round 2 (review) VIỆC 2 — xem comment đầy đủ ở `MeetingRoomBookingResource` (khuôn
         // giống hệt): đọc cờ đã tính sẵn 1 lần ở `attachDisplayNames()`, KHÔNG tự gọi
         // `isCurrentEmployeeHasPermission()` ở Resource (Detail chỉ render 1 dòng/request nên
         // không phải N+1 nghiêm trọng như list, nhưng đồng bộ 1 nguồn duy nhất để 2 Resource không
         // lệch cách tính).
         $hasApprovePermission = (bool) ($this->has_approve_permission ?? false);
         $canActOnApproval = $isRoomManager || $hasApprovePermission;
 
         return [
             'id' => $this->id,
@@ -36,21 +39,24 @@ class DetailMeetingRoomBookingResource extends ApiResource
             // `meeting/rooms/bookable` (không có ô nào để chọn) nên phải kèm sẵn ở đây, nếu không
             // panel trống trơn đúng lúc người duyệt cần biết phòng đó sức chứa bao nhiêu.
             'room' => $this->room ? [
                 'id' => $this->room->id,
                 'name' => $this->room->name,
                 'capacity' => $this->room->capacity,
                 'location' => $this->room->location,
                 'open_time' => $this->room->open_time,
                 'close_time' => $this->room->close_time,
                 'require_approval' => (bool) $this->room->require_approval,
-                'manager_name' => optional(optional($this->room->manager)->info)->fullname,
+                // Phase 8 — quan hệ `manager()` (1 người) đã bị xoá ở lượt A1, đổi sang danh sách
+                // nhiều người phụ trách. Không có FE nào đang đọc khoá này (đã grep
+                // `hrm-client/pages/meeting`), nhưng sửa để tránh mãi mãi ra rỗng im lặng.
+                'manager_name' => implode(', ', $this->room->managerNames()),
                 'amenities' => $this->room->relationLoaded('amenities')
                     ? $this->room->amenities->map(function ($amenity) {
                         return ['id' => $amenity->id, 'name' => $amenity->name];
                     })
                     : [],
             ] : null,
             'start_at' => MeetingRoomBookingResource::isoDateTime($this->start_at),
             'start_at_text' => MeetingRoomBookingResource::readableDateTime($this->start_at),
             'end_at' => MeetingRoomBookingResource::isoDateTime($this->end_at),
             'end_at_text' => MeetingRoomBookingResource::readableDateTime($this->end_at),
diff --git a/Modules/Meeting/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php b/Modules/Meeting/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php
index 93f2bd257..3e5e21a85 100644
--- a/Modules/Meeting/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php
+++ b/Modules/Meeting/Transformers/MeetingRoomBooking/MeetingRoomBookingResource.php
@@ -14,22 +14,25 @@ use Modules\Meeting\Entities\MeetingRoomBooking;
  * - Thời gian trả ISO-8601 CÓ OFFSET (`+07:00`) kèm `*_text` cho người đọc.
  * - Trạng thái trả đủ `status` + `status_text` + `status_color`, client không tự map.
  *
  * List GỌN — KHÔNG nhồi participants (spec 6.4 "Payload list gọn"), chỉ Detail resource mới có.
  */
 class MeetingRoomBookingResource extends ApiResource
 {
     public function toArray($request): array
     {
         $isOwner = (int) $this->booked_by_employee_id === (int) auth()->id();
-        $isRoomManager = optional($this->room)->manager_employee_id
-            && (int) $this->room->manager_employee_id === (int) auth()->id();
+        // Phase 8 — phòng nay có NHIỀU người phụ trách (`meeting_room_managers`). Phòng chưa load
+        // thì `optional($this->room)->managerIds()` gọi trên `null` -> `optional()` trả `null` ->
+        // `in_array(..., null)` sẽ lỗi TypeError, nên phải chốt mảng rỗng bằng `?: []` (đúng yêu
+        // cầu "phòng chưa load thì phải ra false").
+        $isRoomManager = in_array((int) auth()->id(), optional($this->room)->managerIds() ?: [], true);
         // Fix round 2 (review) VIỆC 2 — KHÔNG tự gọi `isCurrentEmployeeHasPermission()` ở đây nữa
         // (N+1 thật: helper đó không cache, chạy lại vài query cho TỪNG DÒNG khi render list).
         // `MeetingRoomBookingService::attachDisplayNames()` PHẢI tính sẵn 1 lần cho cả lô rồi gán
         // vào từng model TRƯỚC khi tới Resource — mọi call site hiện tại (index/show/store/update)
         // đã làm đúng việc này. Fallback `false` (KHÔNG gọi lại hàm) nếu lỡ thiếu bước gán, để một
         // path mới quên gọi `attachDisplayNames()` chỉ mất cờ (fail-closed, an toàn) thay vì âm
         // thầm tái sinh N+1.
         $hasApprovePermission = (bool) ($this->has_approve_permission ?? false);
         $canActOnApproval = $isRoomManager || $hasApprovePermission;
 
diff --git a/app/Services/CatalogHistoryService.php b/app/Services/CatalogHistoryService.php
index d40cd1400..80eeaaa61 100644
--- a/app/Services/CatalogHistoryService.php
+++ b/app/Services/CatalogHistoryService.php
@@ -431,30 +431,34 @@ class CatalogHistoryService
         ]],
         'type_accounts' => ['label' => 'loại tài khoản', 'columns' => [
             'code' => 'Mã loại tài khoản', 'name' => 'Tên loại tài khoản', 'note' => 'Ghi chú',
             'status' => 'Trạng thái',
         ]],
         'product_transfer_requests' => ['label' => 'phiếu yêu cầu chuyển hàng', 'columns' => [
             'code' => 'Mã yêu cầu', 'approver_id' => 'Người tiếp nhận', 'status' => 'Trạng thái',
             'note' => 'Ghi chú',
         ]],
         // ---- Meeting · Quản lý phòng họp ----
-        // `company_id` / `manager_employee_id` được `MeetingRoomService::catalogDisplay()` đổi
-        // sang TÊN trước khi ghi, nên log tự chứa (đọc lại được kể cả khi công ty/nhân viên đổi
-        // tên hoặc nghỉ việc). `amenities` là khoá ẢO: giá trị do service tự dựng (danh sách tên
-        // tiện nghi của phòng, nối bằng dấu phẩy) — bảng `meeting_rooms` KHÔNG có cột này.
+        // `company_id` được `MeetingRoomService::catalogDisplay()` đổi sang TÊN trước khi ghi, nên
+        // log tự chứa (đọc lại được kể cả khi công ty đổi tên). `amenities` VÀ `managers` đều là
+        // khoá ẢO: giá trị do service tự dựng (danh sách tên, nối bằng dấu phẩy) ở
+        // `MeetingRoomService::roomSnapshot()` — bảng `meeting_rooms` KHÔNG có 2 cột này.
         // Task 44 (19/09/2026) — 2 danh mục đã BỎ cột `code`, nên bỏ khỏi đây luôn; tiện nghi
         // thêm `note` (Ghi chú). Phiếu đặt phòng (`meeting_room_bookings`) bổ sung ở Task 46.
+        // Phase 8 lượt A2 (T117) — 1 phòng nay NHIỀU người phụ trách (bảng `meeting_room_managers`,
+        // cột cũ `manager_employee_id` đã bị DROP ở lượt A1): đổi khoá `manager_employee_id` ->
+        // `managers`, nhãn giữ nguyên "Người quản lý phòng". Giá trị là DANH SÁCH TÊN ngăn bằng
+        // ", " (KHÔNG in id trần — xem `roomSnapshot()`).
         'meeting_rooms' => ['label' => 'phòng họp', 'columns' => [
             'name' => 'Tên phòng họp', 'company_id' => 'Công ty quản lý',
             'allow_cross_company' => 'Cho công ty khác đặt', 'location' => 'Vị trí',
-            'capacity' => 'Sức chứa', 'manager_employee_id' => 'Người quản lý phòng',
+            'capacity' => 'Sức chứa', 'managers' => 'Người quản lý phòng',
             'require_approval' => 'Yêu cầu duyệt', 'open_time' => 'Giờ mở cửa',
             'close_time' => 'Giờ đóng cửa', 'checkin_grace_minutes' => 'Ân hạn check-in (phút)',
             'description' => 'Mô tả', 'amenities' => 'Tiện nghi', 'status' => 'Trạng thái',
         ]],
         'meeting_room_amenities' => ['label' => 'tiện nghi phòng họp', 'columns' => [
             'name' => 'Tên tiện nghi', 'icon' => 'Biểu tượng',
             'sort_order' => 'Thứ tự hiển thị', 'note' => 'Ghi chú', 'status' => 'Trạng thái',
         ]],
         // Task 46 — PHIẾU đặt phòng. Không phải danh mục nhưng dùng chung bảng `catalog_histories`
         // + popup `CatalogHistoryModal` (skill entity-history §5.1: không viết bảng log riêng cho

## FILE MỚI: migration
```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

/**
 * Phase 8, lượt A1 (T109) — đổi phòng họp từ 1 người phụ trách (`meeting_rooms.manager_employee_id`)
 * sang NHIỀU người phụ trách, chuẩn bị cho tính năng "yêu cầu dịch vụ" gửi cho cả NHÓM phụ trách
 * phòng thay vì 1 người.
 *
 * Backfill NGAY TRONG migration này (không tách migration riêng): mỗi phòng đang có
 * `manager_employee_id` khác NULL -> 1 dòng trong bảng nối, rồi mới drop cột cũ — tại thời điểm
 * drop, dữ liệu người phụ trách cũ đã có trong `meeting_room_managers`, không mất thông tin.
 *
 * `down()` đổ ngược người phụ trách có `meeting_room_managers.id` NHỎ NHẤT của mỗi phòng (tức
 * người được thêm đầu tiên / đầu danh sách) — chấp nhận mất thông tin "người thứ 2 trở đi" khi
 * rollback, vì cột cũ vốn chỉ chứa được 1 người.
 */
class CreateMeetingRoomManagersTable extends Migration
{
    public function up()
    {
        Schema::create('meeting_room_managers', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedBigInteger('meeting_room_id');
            $table->unsignedBigInteger('employee_id')->index();
            $table->timestamps();

            $table->foreign('meeting_room_id', 'mr_managers_room_fk')
                ->references('id')->on('meeting_rooms')->onDelete('cascade');
            $table->unique(['meeting_room_id', 'employee_id'], 'mr_managers_room_employee_unique');
        });

        // Backfill: mỗi phòng có manager_employee_id khác NULL -> 1 dòng trong bảng nối.
        $now = now();
        $rooms = DB::table('meeting_rooms')
            ->whereNotNull('manager_employee_id')
            ->select('id', 'manager_employee_id')
            ->get();

        $rows = $rooms->map(function ($room) use ($now) {
            return [
                'meeting_room_id' => $room->id,
                'employee_id' => $room->manager_employee_id,
                'created_at' => $now,
                'updated_at' => $now,
            ];
        })->all();

        if (!empty($rows)) {
            DB::table('meeting_room_managers')->insert($rows);
        }

        Schema::table('meeting_rooms', function (Blueprint $table) {
            $table->dropColumn('manager_employee_id');
        });
    }

    public function down()
    {
        Schema::table('meeting_rooms', function (Blueprint $table) {
            if (!Schema::hasColumn('meeting_rooms', 'manager_employee_id')) {
                $table->unsignedBigInteger('manager_employee_id')->nullable()->after('capacity');
            }
        });

        // Đổ ngược người phụ trách có id (meeting_room_managers.id) NHỎ NHẤT của mỗi phòng.
        $firstManagerByRoom = DB::table('meeting_room_managers')
            ->selectRaw('meeting_room_id, MIN(id) as first_id')
            ->groupBy('meeting_room_id')
            ->get();

        foreach ($firstManagerByRoom as $row) {
            $manager = DB::table('meeting_room_managers')->find($row->first_id);
            if ($manager) {
                DB::table('meeting_rooms')
                    ->where('id', $row->meeting_room_id)
                    ->update(['manager_employee_id' => $manager->employee_id]);
            }
        }

        Schema::dropIfExists('meeting_room_managers');
    }
}
```

## FILE MỚI: test
```php
<?php

namespace Tests\Feature;

use App\Models\TpEmployee;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Notification;
use Modules\Meeting\Entities\MeetingRoom;
use Modules\Meeting\Entities\MeetingRoomBooking;
use Modules\Meeting\Services\MeetingRoomBookingService;
use Modules\Meeting\Services\MeetingRoomService;
use Modules\Timesheet\Entities\EmployeeInfo;
use Modules\Timesheet\Notifications\BaseNotification;
use Tests\TestCase;

/**
 * Phase 8, lượt A2 (T114-T117 + BS-1/BS-2/BS-3) — bằng chứng 4 điều bắt buộc theo brief
 * `.sdd/p8-A2-brief.md` mục "Cách tự kiểm" #3: phòng họp nay có NHIỀU người phụ trách
 * (`meeting_room_managers`), thay cho cột `manager_employee_id` (1 người) đã bị DROP ở lượt A1.
 *
 * Actor dùng cố định trong file này (đã kiểm bằng tinker TRƯỚC khi viết test — xem báo cáo A2 mục
 * tự kiểm #3 — để tránh sai lầm chọn nhầm nhân viên có sẵn quyền "Xem tất cả"/"Duyệt phiếu đặt
 * phòng họp" khiến ca "người ngoài bị chặn" xanh giả):
 *   - employee 24, 25 (company_id=1, KHÔNG có 2 quyền trên) = 2 người phụ trách phòng test.
 *   - employee 27 (company_id=1, KHÔNG phải quản lý phòng) = người đặt phiếu.
 *   - employee 28 (company_id=1, KHÔNG có 2 quyền trên, KHÔNG phải quản lý/người đặt) = "người
 *     ngoài nhóm".
 * ⚠️ KHÔNG dùng employee 34 (dùng khắp `MeetingRoomBookingRaceTest`) hay 13 (quản lý 2 phòng thật
 * của DB local) cho vai "người ngoài"/"quản lý cô lập": cả 2 đều CÓ SẴN quyền "Duyệt phiếu đặt
 * phòng họp" + "Xem tất cả phiếu đặt phòng họp" theo role hiện tại của DB local, dùng nhầm sẽ khiến
 * ca "bị chặn"/"không thấy phiếu" xanh giả (đi qua nhánh permission thay vì nhánh đang kiểm).
 *
 * Không dùng RefreshDatabase (khớp `MeetingRoomBookingRaceTest` — TestCase gốc không có
 * transaction/rollback tự động): tự dọn dữ liệu test ở tearDown().
 */
class MeetingRoomManagersTest extends TestCase
{
    private const MANAGER_A_ID = 24;
    private const MANAGER_B_ID = 25;
    private const BOOKER_ID = 27;
    private const OUTSIDER_ID = 28;
    /** Riêng cho ca cache (fix vòng 1 #3) — không trộn với 4 actor trên để tránh nhiễu ý nghĩa. */
    private const CACHE_TEST_MANAGER_ID = 30;

    /** @var int[] */
    private $roomIdsToCleanup = [];

    /** @var int[] */
    private $bookingIdsToCleanup = [];

    protected function tearDown(): void
    {
        foreach ($this->bookingIdsToCleanup as $bookingId) {
            DB::table('meeting_room_bookings')->where('id', $bookingId)->delete();
        }
        foreach ($this->roomIdsToCleanup as $roomId) {
            DB::table('meeting_room_managers')->where('meeting_room_id', $roomId)->delete();
            // Ca import (BS-3, fix vòng 1 #2) gọi `logCatalogCreate()` thật -> ghi 1 dòng
            // `catalog_histories`. Dọn theo đúng `table_name`/`table_id` để không để rác vĩnh viễn.
            DB::table('catalog_histories')->where('table_name', 'meeting_rooms')->where('table_id', $roomId)->delete();
            DB::table('meeting_rooms')->where('id', $roomId)->delete();
        }
        $this->bookingIdsToCleanup = [];
        $this->roomIdsToCleanup = [];

        parent::tearDown();
    }

    /** @param int[] $managerIds */
    private function createTestRoom(string $suffix, array $managerIds, bool $requireApproval = true): int
    {
        // ⚠️ `meeting_rooms` KHÔNG còn cột `code` (Task 44, 19/09/2026 — migration
        // `2026_09_19_000002_drop_code_add_note_meeting_room_catalogs`), khác `meeting_room_bookings`
        // vẫn còn `code`. Test đối chứng khác (`MeetingRoomBookingRaceTest`) vẫn chèn `code` vào
        // `meeting_rooms` nên lỗi "Unknown column 'code'" — đó LÀ baseline đỏ có sẵn, không đụng vào.
        $roomId = DB::table('meeting_rooms')->insertGetId([
            'name' => 'PHPUnit Managers Room ' . $suffix . '_' . time() . '_' . mt_rand(1000, 9999),
            'company_id' => 1,
            'status' => MeetingRoom::STATUS_ACTIVE,
            'require_approval' => $requireApproval ? 1 : 0,
            'created_at' => now(),
            'updated_at' => now(),
        ]);
        $this->roomIdsToCleanup[] = $roomId;

        foreach ($managerIds as $employeeId) {
            DB::table('meeting_room_managers')->insert([
                'meeting_room_id' => $roomId,
                'employee_id' => $employeeId,
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }

        return $roomId;
    }

    private function createTestBooking(int $roomId, string $suffix, \DateTimeInterface $startAt, \DateTimeInterface $endAt, int $status, int $bookedBy = self::BOOKER_ID): int
    {
        $bookingId = DB::table('meeting_room_bookings')->insertGetId([
            'code' => 'PHPUNIT_MGRS_' . $suffix . '_' . time() . '_' . mt_rand(1000, 9999),
            'meeting_room_id' => $roomId,
            'title' => 'PHPUnit Managers Booking ' . $suffix,
            'start_at' => $startAt,
            'end_at' => $endAt,
            'status' => $status,
            'booked_by_employee_id' => $bookedBy,
            'company_id' => 1,
            'source' => MeetingRoomBooking::SOURCE_TU_DAT,
            'created_at' => now(),
            'updated_at' => now(),
        ]);
        $this->bookingIdsToCleanup[] = $bookingId;

        return $bookingId;
    }

    /**
     * Điều 1/4 — phòng có 2 người phụ trách -> CẢ 2 đều duyệt được phiếu (2 phiếu riêng, mỗi
     * người duyệt 1 phiếu, để không ai "duyệt hộ" người kia che lấp kết quả).
     */
    public function test_ca_hai_nguoi_phu_trach_deu_duyet_duoc_phieu()
    {
        $roomId = $this->createTestRoom('APPROVE', [self::MANAGER_A_ID, self::MANAGER_B_ID]);

        $booking1Id = $this->createTestBooking(
            $roomId,
            'A',
            now()->addDays(120)->setTime(9, 0),
            now()->addDays(120)->setTime(10, 0),
            MeetingRoomBooking::STATUS_CHO_DUYET
        );
        $booking2Id = $this->createTestBooking(
            $roomId,
            'B',
            now()->addDays(120)->setTime(11, 0),
            now()->addDays(120)->setTime(12, 0),
            MeetingRoomBooking::STATUS_CHO_DUYET
        );

        $service = app(MeetingRoomBookingService::class);

        $this->actingAs(TpEmployee::find(self::MANAGER_A_ID), 'api');
        $service->approve(MeetingRoomBooking::findOrFail($booking1Id));
        $this->assertSame(
            MeetingRoomBooking::STATUS_DA_DUYET,
            (int) MeetingRoomBooking::find($booking1Id)->status,
            'Người phụ trách A phải duyệt được phiếu 1'
        );

        $this->actingAs(TpEmployee::find(self::MANAGER_B_ID), 'api');
        $service->approve(MeetingRoomBooking::findOrFail($booking2Id));
        $this->assertSame(
            MeetingRoomBooking::STATUS_DA_DUYET,
            (int) MeetingRoomBooking::find($booking2Id)->status,
            'Người phụ trách B (người phụ trách THỨ HAI của CÙNG phòng) cũng phải duyệt được phiếu 2'
        );
    }

    /** Điều 2/4 — người NGOÀI nhóm phụ trách gọi duyệt -> bị chặn 403, phiếu giữ nguyên trạng thái. */
    public function test_nguoi_ngoai_nhom_phu_trach_bi_chan_khi_duyet()
    {
        $roomId = $this->createTestRoom('BLOCK', [self::MANAGER_A_ID, self::MANAGER_B_ID]);
        $bookingId = $this->createTestBooking(
            $roomId,
            'OUT',
            now()->addDays(121)->setTime(9, 0),
            now()->addDays(121)->setTime(10, 0),
            MeetingRoomBooking::STATUS_CHO_DUYET
        );

        $service = app(MeetingRoomBookingService::class);
        $this->actingAs(TpEmployee::find(self::OUTSIDER_ID), 'api');

        $caught = null;
        try {
            $service->approve(MeetingRoomBooking::findOrFail($bookingId));
        } catch (\Exception $e) {
            $caught = $e;
        }

        $this->assertNotNull($caught, 'approve() PHẢI ném exception khi người gọi không phải quản lý phòng và không có quyền Duyệt');
        $this->assertSame(403, $caught->getCode(), 'Đúng mã lỗi 403 (permission), không phải lỗi khác. Message: ' . $caught->getMessage());
        $this->assertSame(
            MeetingRoomBooking::STATUS_CHO_DUYET,
            (int) MeetingRoomBooking::find($bookingId)->status,
            'Phiếu PHẢI giữ nguyên "Chờ duyệt" — không được duyệt lọt'
        );
    }

    /** Điều 3/4 — applyVisibilityScope() (qua index()) trả phiếu của phòng mình phụ trách cho CẢ 2 người; người ngoài không thấy. */
    public function test_apply_visibility_scope_tra_phieu_cho_ca_hai_nguoi_phu_trach()
    {
        $roomId = $this->createTestRoom('SCOPE', [self::MANAGER_A_ID, self::MANAGER_B_ID]);
        // Người ĐẶT là employee 27 — KHÔNG phải quản lý phòng — để phép đo chỉ phản ánh đúng vế
        // "phiếu của phòng mình quản lý", không lẫn với vế "phiếu mình tự đặt".
        $bookingId = $this->createTestBooking(
            $roomId,
            'SCOPE',
            now()->addDays(122)->setTime(9, 0),
            now()->addDays(122)->setTime(10, 0),
            MeetingRoomBooking::STATUS_CHO_DUYET
        );

        $service = app(MeetingRoomBookingService::class);
        $request = Request::create('/', 'GET', ['meeting_room_id' => $roomId]);

        $this->actingAs(TpEmployee::find(self::MANAGER_A_ID), 'api');
        $idsForA = $service->index($request)->get()->pluck('id')->all();
        $this->assertContains($bookingId, $idsForA, 'Người phụ trách A phải thấy phiếu của phòng mình quản lý dù không tự đặt phiếu đó');

        $this->actingAs(TpEmployee::find(self::MANAGER_B_ID), 'api');
        $idsForB = $service->index($request)->get()->pluck('id')->all();
        $this->assertContains($bookingId, $idsForB, 'Người phụ trách B (người phụ trách THỨ HAI) cũng phải thấy phiếu này');

        $this->actingAs(TpEmployee::find(self::OUTSIDER_ID), 'api');
        $idsForOutsider = $service->index($request)->get()->pluck('id')->all();
        $this->assertNotContains($bookingId, $idsForOutsider, 'Người NGOÀI nhóm phụ trách (không đặt, không mời, không có quyền Xem tất cả) KHÔNG được thấy phiếu này');
    }

    /** Điều 4/4 — thông báo "Chờ duyệt" khi tạo phiếu bắn cho ĐỦ 2 người phụ trách (chỉ đếm số người nhận, không kiểm nội dung). */
    public function test_thong_bao_cho_duyet_ban_cho_du_hai_nguoi_phu_trach()
    {
        Notification::fake();

        $roomId = $this->createTestRoom('NOTIFY', [self::MANAGER_A_ID, self::MANAGER_B_ID]);
        $bookingId = $this->createTestBooking(
            $roomId,
            'NOTIFY',
            now()->addDays(123)->setTime(9, 0),
            now()->addDays(123)->setTime(10, 0),
            MeetingRoomBooking::STATUS_CHO_DUYET
        );

        $room = MeetingRoom::findOrFail($roomId);
        $booking = MeetingRoomBooking::findOrFail($bookingId);

        // `sendBookingNotification()` (gọi bên trong `notifyPendingApproval()`) đọc
        // `auth()->user()->employee_info_id` làm người gửi khi không được truyền `$sender` — đúng
        // luồng thật (được gọi từ `store()` lúc booker đang đăng nhập). Không actingAs() thì
        // `auth()->user()` là null, lỗi bị NUỐT bởi try/catch trong `sendBookingNotification()`
        // (bẫy đã ghi ngay trong comment của hàm đó) -> gửi 0 người mà không báo lỗi nào.
        $this->actingAs(TpEmployee::find(self::BOOKER_ID), 'api');

        $service = app(MeetingRoomBookingService::class);
        $service->notifyPendingApproval($booking, $room);

        $managerA = TpEmployee::find(self::MANAGER_A_ID);
        $managerB = TpEmployee::find(self::MANAGER_B_ID);
        $recipientA = EmployeeInfo::find($managerA->employee_info_id);
        $recipientB = EmployeeInfo::find($managerB->employee_info_id);

        $this->assertNotNull($recipientA, 'Cần employee_info của quản lý A tồn tại để so khớp người nhận');
        $this->assertNotNull($recipientB, 'Cần employee_info của quản lý B tồn tại để so khớp người nhận');

        // Đếm SỐ NGƯỜI NHẬN — đúng yêu cầu brief "không assert nội dung".
        Notification::assertSentTimes(BaseNotification::class, 2);
        Notification::assertSentTo([$recipientA, $recipientB], BaseNotification::class);
    }

    /**
     * Fix vòng 1 #2 (BS-3) — import 1 dòng có NHIỀU tên ngăn bằng `;` -> tạo đúng số dòng
     * `meeting_room_managers` tương ứng. Dùng tên THẬT của employee 24/25 (`resolveManagerId()`
     * khớp theo `fullname`, không phải id) — đã xác nhận fullname 2 người này bằng tinker trước khi
     * viết test (24 = "Nguyễn Đức Tuân", 25 = "Nguyễn Thị Cần").
     */
    public function test_import_phong_hop_hai_ten_ngan_boi_cham_phay_tao_dung_hai_dong_quan_ly()
    {
        $this->actingAs(TpEmployee::find(self::BOOKER_ID), 'api');

        $roomName = 'PHPUnit Import Room MGRS_' . time() . '_' . mt_rand(1000, 9999);
        $result = app(MeetingRoomService::class)->importRows([
            [
                'name' => $roomName,
                'location' => '',
                'capacity' => '',
                'manager_name' => 'Nguyễn Đức Tuân; Nguyễn Thị Cần',
                'require_approval' => 'Không',
                'allow_cross_company' => 'Không',
                'status' => 'Hoạt động',
            ],
        ]);

        $this->assertSame(
            1,
            $result['success'],
            'Dòng có 2 tên phụ trách hợp lệ phải import THÀNH CÔNG. Lỗi trả về: '
            . json_encode($result['errors'], JSON_UNESCAPED_UNICODE)
        );
        $this->assertSame(0, $result['failed']);

        $room = MeetingRoom::where('name', $roomName)->first();
        $this->assertNotNull($room, 'Phòng phải được tạo ra sau import');
        $this->roomIdsToCleanup[] = $room->id;

        $managerIds = DB::table('meeting_room_managers')
            ->where('meeting_room_id', $room->id)
            ->pluck('employee_id')
            ->sort()
            ->values()
            ->all();

        $this->assertSame(
            [self::MANAGER_A_ID, self::MANAGER_B_ID],
            $managerIds,
            'File import 1 dòng có 2 tên ngăn bằng ";" PHẢI tạo ra ĐÚNG 2 dòng meeting_room_managers — '
            . 'đây chính là bẫy Eloquent ÂM THẦM BỎ QUA cột manager_employee_id đã drop (BS-3), giờ phải '
            . 'chốt bằng test chứ không dựa vào đọc code.'
        );
    }

    /**
     * Fix vòng 1 #2 (BS-3) — dòng import THIẾU hẳn người phụ trách -> phải báo LỖI DÒNG, không được
     * tạo ra phòng không ai phụ trách (phòng bắt buộc >= 1 người phụ trách, chốt từ lượt A1).
     */
    public function test_import_phong_hop_thieu_nguoi_phu_trach_bao_loi_dong_khong_tao_phong()
    {
        $this->actingAs(TpEmployee::find(self::BOOKER_ID), 'api');

        $roomName = 'PHPUnit Import Room NOMGR_' . time() . '_' . mt_rand(1000, 9999);
        $result = app(MeetingRoomService::class)->importRows([
            [
                'name' => $roomName,
                'location' => '',
                'capacity' => '',
                'manager_name' => '',
                'require_approval' => 'Không',
                'allow_cross_company' => 'Không',
                'status' => 'Hoạt động',
            ],
        ]);

        $this->assertSame(0, $result['success'], 'Dòng thiếu người phụ trách PHẢI thất bại, không được import');
        $this->assertSame(1, $result['failed']);
        $this->assertCount(1, $result['errors']);
        $this->assertSame(2, $result['errors'][0]['row'], 'Dòng dữ liệu đầu tiên = dòng 2 của Excel (dòng 1 là tiêu đề)');
        $this->assertStringContainsString(
            'người phụ trách',
            mb_strtolower($result['errors'][0]['message']),
            'Message lỗi phải nói rõ lý do là thiếu người phụ trách. Message thật: ' . $result['errors'][0]['message']
        );

        $room = MeetingRoom::where('name', $roomName)->first();
        $this->assertNull(
            $room,
            'TUYỆT ĐỐI không được tạo phòng khi dòng import lỗi — đúng bẫy Eloquent từng ÂM THẦM BỎ QUA '
            . 'key `manager_employee_id` lạ (cột đã drop) mà không báo lỗi nào (BS-3).'
        );
    }

    /**
     * Fix vòng 1 #3 — bẫy cache reviewer lượt A1 phát hiện: `MeetingRoom::managerIds()`/
     * `managerNames()` đệm vào thuộc tính riêng + dựa vào quan hệ `managers` "đã nạp" của Eloquent;
     * `sync()` đổi pivot thật trong DB nhưng không tự xoá 2 lớp cache đó. Chứng minh:
     * đọc `managerIds()` -> `syncManagers([id khác])` -> đọc lại TRÊN CÙNG OBJECT -> phải ra danh
     * sách MỚI (không phải danh sách cũ còn kẹt trong cache).
     */
    public function test_managerIds_khong_con_stale_cache_sau_khi_syncManagers()
    {
        $roomId = $this->createTestRoom('CACHE', [self::MANAGER_A_ID, self::MANAGER_B_ID]);

        $room = MeetingRoom::findOrFail($roomId);

        $before = $room->managerIds();
        sort($before);
        $this->assertSame(
            [self::MANAGER_A_ID, self::MANAGER_B_ID],
            $before,
            'Trước khi sync: managerIds() phải ra đúng 2 người phụ trách ban đầu'
        );
        // Gọi thêm managerNames() để chắc chắn CẢ HAI cache ($managerIdsCache lẫn quan hệ
        // `managers` đã nạp qua `relationLoaded()`) đều đã được "mồi" trước khi sync — đúng kịch
        // bản thật gây bug (Resource gọi managerIds() rồi managerNames() trước khi service sync()).
        $room->managerNames();

        $room->syncManagers([self::CACHE_TEST_MANAGER_ID]);

        $after = $room->managerIds();
        $this->assertSame(
            [self::CACHE_TEST_MANAGER_ID],
            $after,
            'SAU khi syncManagers() trên CÙNG object: managerIds() phải ra danh sách MỚI ngay lập '
            . 'tức, không được ra danh sách CŨ ([24,25]) do cache/quan hệ đã nạp không được xoá — '
            . 'đây chính là bẫy reviewer lượt A1 phát hiện.'
        );

        $afterNames = $room->managerNames();
        $this->assertCount(1, $afterNames, 'managerNames() cũng phải hết stale, ra đúng 1 tên (người mới)');
    }
}
```
