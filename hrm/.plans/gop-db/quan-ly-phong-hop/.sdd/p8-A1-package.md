## git status
 M Modules/Meeting/Entities/MeetingRoom.php
 M Modules/Meeting/Http/Controllers/Api/V1/MeetingRoomController.php
 M Modules/Meeting/Http/Requests/MeetingRoom/MeetingRoomRequest.php
 M Modules/Meeting/Services/MeetingRoomService.php
 M Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php
 M Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php
?? Modules/Meeting/Database/Migrations/2026_09_23_000001_create_meeting_room_managers_table.php

## diff --stat
 Modules/Meeting/Entities/MeetingRoom.php           | 87 +++++++++++++++++++---
 .../Controllers/Api/V1/MeetingRoomController.php   | 13 +++-
 .../Requests/MeetingRoom/MeetingRoomRequest.php    | 11 ++-
 Modules/Meeting/Services/MeetingRoomService.php    | 52 ++++++++-----
 .../MeetingRoom/DetailMeetingRoomResource.php      | 10 ++-
 .../MeetingRoom/MeetingRoomResource.php            | 10 ++-
 6 files changed, 143 insertions(+), 40 deletions(-)

## diff -U10
diff --git a/Modules/Meeting/Entities/MeetingRoom.php b/Modules/Meeting/Entities/MeetingRoom.php
index 612dc54c6..13b42779f 100644
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
@@ -70,33 +74,94 @@ class MeetingRoom extends BaseModel
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
+        return $this->belongsToMany(
+            \Modules\Timesheet\Entities\Employee::class,
+            'meeting_room_managers',
+            'meeting_room_id',
+            'employee_id'
+        )->withTimestamps()->with('info');
+    }
+
+    /**
+     * Mảng `employee_id` của TẤT CẢ người phụ trách phòng. Đệm vào thuộc tính protected để gọi
+     * nhiều lần trong 1 request (Resource + các hàm khác) không query lại — dùng CHUNG
+     * `loadedManagers()` với `managerNames()` nên dù gọi cả 2 hàm mà quan hệ CHƯA eager load, chỉ
+     * bắn đúng 1 query (`load()` đánh dấu quan hệ đã nạp trên chính model, khác với
+     * `managers()->get()` — cái đó lấy Collection mới mỗi lần, không đánh dấu gì cả).
      *
-     * ⚠️ Cố tình KHÔNG dùng `Employee::getAll(true)` (chỉ lấy nhân viên ĐANG làm việc) ở đây —
-     * đây là quan hệ Eloquent đọc trực tiếp bằng khoá ngoại, phải trả đúng người quản lý đã lưu dù
-     * người đó đã nghỉ việc, nếu không `manager_name` cho phòng có quản lý đã nghỉ sẽ lại rỗng y
-     * hệt lỗi mà lần sửa này đang vá (FE trước đây tra theo state.employees, vốn lọc
-     * `onlyActive = true`, nên bỏ sót đúng trường hợp này).
+     * @return array
      */
-    public function manager()
+    public function managerIds(): array
     {
-        return $this->belongsTo(\Modules\Timesheet\Entities\Employee::class, 'manager_employee_id', 'id');
+        if ($this->managerIdsCache !== null) {
+            return $this->managerIdsCache;
+        }
+
+        return $this->managerIdsCache = $this->loadedManagers()->pluck('id')->all();
+    }
+
+    /**
+     * Mảng tên người phụ trách, ĐÚNG THỨ TỰ `managers` (thứ tự `meeting_room_managers.id` tăng
+     * dần — mặc định của `belongsToMany` không `orderBy` gì thêm nên đi theo thứ tự khoá pivot).
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
index e4a7afd18..5b0fd999e 100644
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
 
diff --git a/Modules/Meeting/Services/MeetingRoomService.php b/Modules/Meeting/Services/MeetingRoomService.php
index ede7b4146..68a35d945 100644
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
@@ -674,25 +676,37 @@ class MeetingRoomService extends BaseService
     protected function catalogTable(): string
     {
         return 'meeting_rooms';
     }
 
     /**
      * ⚠️ KHÔNG khai `amenities` ở đây: `catalogSnapshot()` đọc `$model->{$column}`, mà
      * `$room->amenities` là quan hệ (Collection) chứ không phải cột. Tiện nghi được ghép vào
      * snapshot ở `roomSnapshot()` bên dưới dưới dạng chuỗi tên.
      */
+    /**
+     * Phase 8 lượt A1 (T111) — bỏ `manager_employee_id` khỏi cột theo dõi lịch sử: cột đã bị
+     * DROP ở migration `2026_09_23_000001_create_meeting_room_managers_table` (T109), đọc
+     * `$model->manager_employee_id` sau khi drop chỉ ra `null` chứ không lỗi, nên nếu để lại
+     * trong mảng này lịch sử sẽ âm thầm ghi "Người quản lý phòng: ... -> (trống)" ở MỌI lần sửa.
+     *
+     * ⚠️ Bàn giao cho lượt sau: nhóm phụ trách (bảng `meeting_room_managers`, nhiều người) HIỆN
+     * CHƯA được ghi vào lịch sử thay đổi — cần thêm khoá ảo (kiểu `amenities` ở `roomSnapshot()`
+     * dưới đây) VÀ đăng ký nhãn hiển thị trong `App\Services\CatalogHistoryService::TABLES`
+     * (file đó nằm ngoài phạm vi lượt này). Trước khi làm việc đó, sửa/xem lịch sử phòng họp sẽ
+     * KHÔNG thấy thay đổi nhóm phụ trách.
+     */
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
@@ -706,29 +720,22 @@ class MeetingRoomService extends BaseService
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
+        // `manager_employee_id` (case cũ, 1 người phụ trách) đã bị xoá cùng với cột ở T109/T111 —
+        // xem docblock `catalogColumns()` phía trên về việc nhóm phụ trách CHƯA có trong lịch sử.
 
         return $value;
     }
 
     /**
      * Snapshot ĐẦY ĐỦ của 1 phòng = các cột theo dõi + danh sách TIỆN NGHI.
      *
      * Tiện nghi nằm ở bảng pivot nên không thể để `catalogSnapshot()` tự đọc; ghép vào đây dưới
      * khoá ảo `amenities` (đã khai nhãn trong `CatalogHistoryService::TABLES`). Sắp xếp theo id
      * để 2 lần chụp cùng dữ liệu luôn ra cùng chuỗi — nếu không, đổi thứ tự sync là log báo
@@ -789,51 +796,56 @@ class MeetingRoomService extends BaseService
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
+            $room->managers()->sync($request->input('manager_employee_ids', []));
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
diff --git a/Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php b/Modules/Meeting/Transformers/MeetingRoom/DetailMeetingRoomResource.php
index 39d80b706..3c6915650 100644
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
+            // Phase 8 lượt A1 (T113) — 1 phòng nay NHIỀU người phụ trách: `manager_employee_id`
+            // (1 người) đổi thành `manager_employee_ids` (mảng id) + `manager_names` (mảng tên,
+            // cùng thứ tự) + `manager_name_text` (chuỗi ghép hiển thị, KHÔNG BAO GIỜ trả `null`).
+            // Nguồn tên GIỮ NGUYÊN như `manager()` cũ (`Employee::fullname`, xem
+            // `MeetingRoom::managerNames()`).
+            'manager_employee_ids' => $this->managerIds(),
+            'manager_names' => $this->managerNames(),
+            'manager_name_text' => implode(', ', $this->managerNames()),
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
index 064c584f6..3ad46f50b 100644
--- a/Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php
+++ b/Modules/Meeting/Transformers/MeetingRoom/MeetingRoomResource.php
@@ -25,22 +25,28 @@ class MeetingRoomResource extends ApiResource
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
+            // Phase 8 lượt A1 (T113) — 1 phòng nay NHIỀU người phụ trách: `manager_employee_id`
+            // (1 người) đổi thành `manager_employee_ids` (mảng id) + `manager_names` (mảng tên,
+            // cùng thứ tự) + `manager_name_text` (chuỗi ghép hiển thị, KHÔNG BAO GIỜ trả `null`).
+            // Nguồn tên GIỮ NGUYÊN như `manager()` cũ (`Employee::fullname`, xem
+            // `MeetingRoom::managerNames()`).
+            'manager_employee_ids' => $this->managerIds(),
+            'manager_names' => $this->managerNames(),
+            'manager_name_text' => implode(', ', $this->managerNames()),
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

## FILE MỚI (untracked): Modules/Meeting/Database/Migrations/2026_09_23_000001_create_meeting_room_managers_table.php
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
