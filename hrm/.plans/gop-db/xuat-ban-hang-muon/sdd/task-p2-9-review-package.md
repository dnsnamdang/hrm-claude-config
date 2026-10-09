# Review package T9 — BASE 7277390bec9eeea36558657bcefeff9afe6da70d .. HEAD 394b5da44f830ee7129d1f7401a3a9f1474b94ee

## git log
394b5da44 feat(finance): thêm API BorrowSellController + 3 Resource + routes cho PXBHM (task P2-9)

## diff --stat
 Modules/Finance/Entities/BorrowSell/BorrowSell.php |  89 ++++++++++++
 .../Http/Controllers/V1/BorrowSellController.php   |  81 +++++++++++
 Modules/Finance/Routes/api.php                     |  31 ++++
 .../Finance/Tests/Feature/BorrowSellApiTest.php    | 160 +++++++++++++++++++++
 .../BorrowSellDetailResource.php                   | 141 ++++++++++++++++++
 .../BorrowSellResource/BorrowSellListResource.php  |  73 ++++++++++
 .../BorrowSellResource/BorrowSellPrintResource.php |  66 +++++++++
 7 files changed, 641 insertions(+)

## diff -U10
diff --git a/Modules/Finance/Entities/BorrowSell/BorrowSell.php b/Modules/Finance/Entities/BorrowSell/BorrowSell.php
index 60054b283..18d7c229a 100644
--- a/Modules/Finance/Entities/BorrowSell/BorrowSell.php
+++ b/Modules/Finance/Entities/BorrowSell/BorrowSell.php
@@ -1,20 +1,30 @@
 <?php
 namespace Modules\Finance\Entities\BorrowSell;
 
 use Illuminate\Database\Eloquent\Model;
+use Illuminate\Http\Request;
 use Modules\Finance\Entities\Concerns\ChecksEmployeePermission;
 use Modules\Finance\Entities\BorrowSellRequest\BorrowSellRequest;
+use Modules\Human\Entities\Employee;
 
 /**
  * Phiếu XUẤT BÁN HÀNG MƯỢN — bảng `borrow_sells` (DB gộp).
  * Phase 2 (HRM): entity map thuần (task P2-1). Port ERP `App\Model\Warehouse\BorrowSell`.
+ *
+ * Task P2-9 (Ruling T9-entity-additions) bổ sung searchByFilter/meta/userCanCreate/is_can_view.
+ *
+ * GOTCHA đã verify (đọc DESCRIBE thật trên DB `erp_hrm_check`, xem task-p2-9-report.md):
+ * bảng `borrow_sells` KHÔNG có cột `company_id`/`department_id` (khác `borrow_sell_requests` —
+ * bảng NÀY có 2 cột đó). Scope 4 cấp quyền trong searchByFilter() do đó KHÔNG lọc trực tiếp trên
+ * `borrow_sells` mà đi qua quan hệ `borrowSellRequest` (`whereHas`) để lấy company_id/department_id
+ * của phiếu YÊU CẦU gốc — mirror đúng ý nghĩa nghiệp vụ "phạm vi công ty/phòng ban của yêu cầu".
  */
 class BorrowSell extends Model
 {
     use ChecksEmployeePermission;
 
     protected $table = 'borrow_sells';
     public $timestamps = true;
     protected $guarded = [];
 
     const PREFIX = 'PXBHM';
@@ -32,27 +42,106 @@ class BorrowSell extends Model
     public function tabs()
     {
         return $this->hasMany(BorrowSellTab::class, 'parent_id');
     }
 
     public function borrowSellRequest()
     {
         return $this->belongsTo(BorrowSellRequest::class, 'borrow_sell_request_id', 'id');
     }
 
+    /** Người lập phiếu — dùng cho creator_name ở Resource (mirror BorrowSellRequest::employee_create). */
+    public function employee_create()
+    {
+        return $this->belongsTo(Employee::class, 'created_by', 'id');
+    }
+
     // ===== Mã phiếu =====
     // Static thuần (không dùng $this) để dùng được cả khi chưa có instance — port
     // ERP `generateCode()` ("PXBHM-".generateCode(5,id)) sang dạng trả chuỗi.
     public static function generateCode(): string
     {
         $nextId = (int) (self::max('id') ?? 0) + 1;
         return self::PREFIX . '-' . str_pad((string) $nextId, 5, '0', STR_PAD_LEFT);
     }
 
     // ===== Gate quyền =====
     // Port ERP `canView()`: Auth::user()->can("Kế toán kho") && status!=3 || created_by==auth->id
     public function canView(): bool
     {
         return (self::currentEmployeeHasPermission(self::PERMISSION_KE_TOAN_KHO) && $this->status != 3)
             || $this->created_by == auth()->id();
     }
+
+    // ===== Danh sách + quyền FE (Task P2-9, Ruling T9-perm) =====
+
+    /**
+     * List scope 4 cấp quyền — TÁI DÙNG NAME hằng của `BorrowSellRequest`
+     * (PERMISSION_VIEW_ALL_COMPANY/_COMPANY/_DEPARTMENT) vì `borrow_sells` không có permission
+     * riêng của nó trong seeder — mirror đúng phạm vi của phiếu YÊU CẦU gốc.
+     *
+     * `borrow_sells` KHÔNG có cột company_id/department_id (đã verify DESCRIBE thật) → scope
+     * company/department đi qua whereHas('borrowSellRequest', ...) thay vì where() trực tiếp.
+     */
+    public static function searchByFilter(Request $request)
+    {
+        $query = self::query()->with(['employee_create', 'borrowSellRequest'])->orderByDesc('id');
+
+        if ($request->filled('code')) {
+            $query->where('code', 'like', '%' . $request->get('code') . '%');
+        }
+        if ($request->filled('status')) {
+            $query->where('status', $request->get('status'));
+        }
+        if ($request->filled('contractable_type')) {
+            $query->where('contractable_type', $request->get('contractable_type'));
+        }
+        if ($request->filled('startDate')) {
+            $query->where('created_at', '>=', $request->get('startDate'));
+        }
+        if ($request->filled('endDate')) {
+            $query->where('created_at', '<=', $request->get('endDate'));
+        }
+
+        // Phân quyền 4 cấp (mirror BorrowSellRequest::searchByFilter nhánh type=all).
+        if (self::currentEmployeeHasPermission(BorrowSellRequest::PERMISSION_VIEW_ALL_COMPANY)) {
+            // không lọc thêm — xem toàn bộ tổng công ty
+        } elseif (self::currentEmployeeHasPermission(BorrowSellRequest::PERMISSION_VIEW_COMPANY)) {
+            $companyId = self::currentCompanyId();
+            $query->whereHas('borrowSellRequest', function ($q) use ($companyId) {
+                $q->where('company_id', $companyId);
+            });
+        } elseif (self::currentEmployeeHasPermission(BorrowSellRequest::PERMISSION_VIEW_DEPARTMENT)) {
+            $departmentIds = self::currentManagedDepartmentIds();
+            $query->whereHas('borrowSellRequest', function ($q) use ($departmentIds) {
+                $q->whereIn('department_id', $departmentIds);
+            });
+        } else {
+            $query->where('created_by', auth()->id());
+        }
+
+        return $query;
+    }
+
+    /** Cờ FE cho màn list (fail-closed mặc định false, mirror BorrowSellRequest::meta). */
+    public static function meta(): array
+    {
+        return [
+            'canViewAllCompany' => self::currentEmployeeHasPermission(BorrowSellRequest::PERMISSION_VIEW_ALL_COMPANY),
+            'canViewCompany' => self::currentEmployeeHasPermission(BorrowSellRequest::PERMISSION_VIEW_COMPANY),
+            'canViewDepartment' => self::currentEmployeeHasPermission(BorrowSellRequest::PERMISSION_VIEW_DEPARTMENT),
+            'is_ke_toan_kho' => self::currentEmployeeHasPermission(self::PERMISSION_KE_TOAN_KHO),
+        ];
+    }
+
+    /** Gate tạo phiếu (Ruling T9-store-gate) — controller store() gọi trước khi vào service. */
+    public static function userCanCreate(): bool
+    {
+        return self::currentEmployeeHasPermission(self::PERMISSION_KE_TOAN_KHO);
+    }
+
+    /** Accessor cho Resource — fail-closed, luôn gọi qua canView() thật. */
+    public function getIsCanViewAttribute(): bool
+    {
+        return $this->canView();
+    }
 }
diff --git a/Modules/Finance/Http/Controllers/V1/BorrowSellController.php b/Modules/Finance/Http/Controllers/V1/BorrowSellController.php
new file mode 100644
index 000000000..bacc1fea6
--- /dev/null
+++ b/Modules/Finance/Http/Controllers/V1/BorrowSellController.php
@@ -0,0 +1,81 @@
+<?php
+
+namespace Modules\Finance\Http\Controllers\V1;
+
+use Illuminate\Http\Request;
+use Modules\Finance\Entities\BorrowSell\BorrowSell;
+use Modules\Finance\Http\Requests\BorrowSell\StoreBorrowSellRequest;
+use Modules\Finance\Services\BorrowSell\BorrowSellService;
+use Modules\Finance\Transformers\BorrowSellResource\BorrowSellListResource;
+use Modules\Finance\Transformers\BorrowSellResource\BorrowSellDetailResource;
+use Modules\Finance\Transformers\BorrowSellResource\BorrowSellPrintResource;
+
+/**
+ * Phiếu XUẤT BÁN HÀNG MƯỢN thực tế (PXBHM) — tầng HTTP MỎNG, chỉ gọi BorrowSellService::store()
+ * (đã port 1-1 nghiệp vụ ở task T7). Controller CHỈ làm 2 việc: gate quyền tường minh (403) +
+ * chuyển đổi Request/Resource — KHÔNG chứa logic nghiệp vụ.
+ *
+ * Quyền (Ruling T9-store-gate): KHÔNG middleware checkPermission trên route (cùng lý do
+ * BorrowSellRequestController — role gán qua ERP model_type='App\Employee' khiến spatie
+ * hasPermissionTo/middleware checkPermission bỏ sót). store() gate 403 tường minh qua
+ * BorrowSell::userCanCreate() TRƯỚC khi gọi service; BorrowSellRequest::canApprove() bên trong
+ * service vẫn giữ nguyên làm defense-in-depth (double check theo đúng ERP).
+ */
+class BorrowSellController extends ApiController
+{
+    private $service;
+
+    public function __construct(BorrowSellService $service)
+    {
+        $this->service = $service;
+    }
+
+    /** Danh sách — searchByFilter TRÊN ENTITY (trả builder) → paginate ở đây. meta() cờ quyền màn. */
+    public function index(Request $request)
+    {
+        $items = BorrowSell::searchByFilter($request)->paginate((int) $request->get('per_page', 20));
+
+        return (new BorrowSellListResource($items))->additional(array_merge([
+            'total' => $items->total(),
+            'lastPage' => $items->lastPage(),
+            'currentPage' => $items->currentPage(),
+            'perPage' => (int) $items->perPage(),
+        ], BorrowSell::meta()));
+    }
+
+    public function store(StoreBorrowSellRequest $request)
+    {
+        if (!BorrowSell::userCanCreate()) {
+            return $this->responseJson('Không đủ quyền!', 403);
+        }
+
+        $m = $this->service->store($request);
+
+        return $this->responseJson('Lập phiếu xuất bán hàng mượn thành công', 200, [
+            'id' => $m->id,
+            'code' => $m->code,
+            'status' => $m->status,
+        ]);
+    }
+
+    public function show($id)
+    {
+        $m = BorrowSell::with(['products.details', 'tabs.products', 'employee_create', 'borrowSellRequest'])
+            ->findOrFail((int) $id);
+        if (!$m->canView()) {
+            return $this->responseJson('Không đủ quyền!', 403);
+        }
+
+        return new BorrowSellDetailResource($m);
+    }
+
+    public function printData($id)
+    {
+        $m = BorrowSell::with(['products', 'employee_create'])->findOrFail((int) $id);
+        if (!$m->canView()) {
+            return $this->responseJson('Không đủ quyền!', 403);
+        }
+
+        return new BorrowSellPrintResource($m);
+    }
+}
diff --git a/Modules/Finance/Routes/api.php b/Modules/Finance/Routes/api.php
index 3b923539f..5ae404ff1 100644
--- a/Modules/Finance/Routes/api.php
+++ b/Modules/Finance/Routes/api.php
@@ -3,20 +3,22 @@
 use Illuminate\Support\Facades\Route;
 use Modules\Finance\Http\Controllers\V1\AccountController;
 use Modules\Finance\Http\Controllers\V1\BillAdjustDeptController;
 use Modules\Finance\Http\Controllers\V1\BillAdjustDeptRequestController;
 use Modules\Finance\Http\Controllers\V1\BillIncomeController;
 use Modules\Finance\Http\Controllers\V1\BillIncomeRequestController;
 use Modules\Finance\Http\Controllers\V1\BillIncomeReportController;
 use Modules\Finance\Http\Controllers\V1\BillPaymentAuthorizationController;
 use Modules\Finance\Http\Controllers\V1\BillPaymentController;
 use Modules\Finance\Http\Controllers\V1\BillPaymentRequestController;
+use Modules\Finance\Http\Controllers\V1\BorrowSellController;
+use Modules\Finance\Http\Controllers\V1\BorrowSellRequestController;
 use Modules\Finance\Http\Controllers\V1\CompanyAccountController;
 use Modules\Finance\Http\Controllers\V1\CostDebtController;
 use Modules\Finance\Http\Controllers\V1\PrepickCancelController;
 use Modules\Finance\Http\Controllers\V1\PrepickCancelRequestController;
 use Modules\Finance\Http\Controllers\V1\PrepickExtendRequestController;
 use Modules\Finance\Http\Controllers\V1\PrepickTransferRequestController;
 use Modules\Finance\Http\Controllers\V1\ProductImportController;
 use Modules\Finance\Http\Controllers\V1\ProductImportDirectTransferController;
 use Modules\Finance\Http\Controllers\V1\ProductImportRequestController;
 use Modules\Finance\Http\Controllers\V1\ProductTransferRequestController;
@@ -732,11 +734,40 @@ Route::group(['prefix' => '/v1/finance', 'middleware' => 'auth:api'], function (
     Route::group(['prefix' => '/prepick-stocks'], function () {
         Route::get('/', [PrepickStockController::class, 'index']);
         Route::get('/meta', [PrepickStockController::class, 'meta']);
         // Tang 2+3 (nhan vien -> khach hang) cua 1 hang hoa, lay trong CUNG mot lan goi.
         Route::get('/details', [PrepickStockController::class, 'details']);
         // So bien dong ton giu cua 1 cap hang hoa x khach hang x cong ty x nhan vien. Sap CU -> MOI.
         Route::get('/logs', [PrepickStockController::class, 'logs']);
         Route::get('/export', [PrepickStockController::class, 'export']);
         Route::get('/print', [PrepickStockController::class, 'print']);
     });
+
+    // Yeu cau xuat ban hang muon (PYCXBHM). KHONG middleware checkPermission — quyen gate qua
+    // canX() tren entity trong Controller (role ERP model_type='App\Employee' → spatie bo sot,
+    // giong ProductImportController). searchByFilter/meta la static tren ENTITY.
+    Route::group(['prefix' => '/borrow-sell-requests'], function () {
+        Route::get('/', [BorrowSellRequestController::class, 'index']);
+        Route::get('/contracts', [BorrowSellRequestController::class, 'contracts']);
+        Route::get('/contracts/{id}/borrow-sell-data', [BorrowSellRequestController::class, 'contractBorrowSellData']);
+        Route::get('/export-requests', [BorrowSellRequestController::class, 'myExportRequests']);
+        Route::post('/', [BorrowSellRequestController::class, 'store']);
+        Route::post('/{id}/deny', [BorrowSellRequestController::class, 'deny']);
+        Route::post('/{id}/manager-approve', [BorrowSellRequestController::class, 'managerApprove']);
+        Route::post('/{id}/switch-board-of-manager', [BorrowSellRequestController::class, 'switchBoardOfManager']);
+        Route::post('/{id}/board-of-manager-approve', [BorrowSellRequestController::class, 'boardOfManagerApprove']);
+        Route::get('/{id}/histories', [BorrowSellRequestController::class, 'histories']);
+        Route::get('/{id}/print-data', [BorrowSellRequestController::class, 'printData']);
+        Route::get('/export-requests/{id}', [BorrowSellRequestController::class, 'exportRequestBorrowSellData']);
+        Route::get('/{id}', [BorrowSellRequestController::class, 'show']); // CUOI CUNG — sau cac route tinh
+    });
+
+    // Xuat ban hang muon THUC TE (PXBHM). KHONG middleware checkPermission (Ruling T9-store-gate,
+    // cung ly do nhom borrow-sell-requests o tren) — quyen gate tuong minh trong controller
+    // (store() qua BorrowSell::userCanCreate(), show()/printData() qua canView()).
+    Route::group(['prefix' => '/borrow-sells'], function () {
+        Route::get('/', [BorrowSellController::class, 'index']);
+        Route::post('/', [BorrowSellController::class, 'store']);
+        Route::get('/{id}/print-data', [BorrowSellController::class, 'printData']);
+        Route::get('/{id}', [BorrowSellController::class, 'show']); // CUOI CUNG — sau cac route tinh
+    });
 });
diff --git a/Modules/Finance/Tests/Feature/BorrowSellApiTest.php b/Modules/Finance/Tests/Feature/BorrowSellApiTest.php
new file mode 100644
index 000000000..2a84e107f
--- /dev/null
+++ b/Modules/Finance/Tests/Feature/BorrowSellApiTest.php
@@ -0,0 +1,160 @@
+<?php
+
+namespace Modules\Finance\Tests\Feature;
+
+use Tests\TestCase;
+use Illuminate\Foundation\Testing\DatabaseTransactions;
+use Illuminate\Support\Facades\DB;
+use Modules\Finance\Entities\BorrowSell\BorrowSell;
+use Modules\Finance\Entities\BorrowSell\BorrowSellProduct;
+use Modules\Finance\Transformers\BorrowSellResource\BorrowSellDetailResource;
+use Modules\Finance\Transformers\BorrowSellResource\BorrowSellPrintResource;
+
+/**
+ * Test cho lớp API PXBHM (Task P2-9 — Controller + 3 Resource + routes).
+ * Test API thật (route + auth JWT + phân quyền + dữ liệu HĐ) rất phức tạp để dựng full ở môi
+ * trường test → ưu tiên các test dựng được và XANH THẬT (không mock quyền/DB giả), phần cần
+ * auth context thật (userCanCreate/searchByFilter theo nhân viên đăng nhập) markTestSkipped khi
+ * dữ liệu/fixture không sẵn có (cùng cách tiếp cận BorrowSellPostingWrServiceTest/BorrowSellStoreTest).
+ *
+ * Dùng lại fixture "HĐ dịch vụ thật trong DB gộp" (wr_service_contracts.id=4) từ
+ * BorrowSellPostingWrServiceTest để dựng 1 BorrowSell KHÔNG lưu DB (id giả 999999003) đủ điều
+ * kiện gọi thẳng BorrowSellPostingService::getDataAccounting() qua Resource.
+ */
+class BorrowSellApiTest extends TestCase
+{
+    use DatabaseTransactions;
+
+    private const WR_CONTRACT_ID = 4;
+
+    /**
+     * XANH THẬT #1 — Route đăng ký đúng, prefix module đúng (/api/v1/finance), không lỗi 500.
+     * Không auth → route đứng sau middleware 'auth:api' của group cha → kỳ vọng 401 (Unauthenticated),
+     * KHÔNG phải 404 (chứng minh route /borrow-sells thực sự được đăng ký trong group đúng prefix).
+     */
+    public function test_index_route_is_registered_under_finance_prefix()
+    {
+        $response = $this->getJson('/api/v1/finance/borrow-sells');
+
+        $response->assertStatus(401);
+    }
+
+    /**
+     * XANH THẬT #2 — BorrowSell::userCanCreate() fail-closed: không auth (guest) → luôn false.
+     * Đây là gate 403 mà controller store() dùng (Ruling T9-store-gate) — test đơn vị hoá, không
+     * cần dựng auth context thật vẫn khoá được regression "lỡ hardcode true".
+     */
+    public function test_user_can_create_is_fail_closed_without_auth()
+    {
+        $this->assertFalse(BorrowSell::userCanCreate());
+    }
+
+    /**
+     * XANH THẬT #3 — BorrowSellDetailResource: khối 'accounting'/'accounting_error' (Ruling
+     * T9-accounting-in-detail) đúng shape khi getDataAccounting() trả ok=true, và 'is_can_view'
+     * lấy từ canView() thật (guest, không phải hardcode true) → guest xem phiếu không phải của
+     * mình (created_by khác) và không có quyền Kế toán kho → is_can_view PHẢI false.
+     */
+    public function test_detail_resource_has_accounting_block_and_fail_closed_is_can_view()
+    {
+        $bs = $this->makeWrServiceBorrowSellFixture();
+        if ($bs === null) {
+            $this->markTestSkipped('Không tìm thấy HĐ dịch vụ fixture (wr_service_contracts.id=' . self::WR_CONTRACT_ID . ') đủ điều kiện HTHT trong DB test.');
+        }
+
+        $resource = (new BorrowSellDetailResource($bs))->toArray(request());
+
+        $this->assertArrayHasKey('accounting', $resource);
+        $this->assertArrayHasKey('accounting_error', $resource);
+        $this->assertIsArray($resource['accounting']);
+        $this->assertNotEmpty($resource['accounting'], 'getDataAccounting() phải trả accounts khi ok=true (fixture hợp lệ)');
+        $this->assertNull($resource['accounting_error']);
+
+        // Fail-closed: guest (không auth) không phải created_by của phiếu → is_can_view=false.
+        $this->assertArrayHasKey('is_can_view', $resource);
+        $this->assertFalse($resource['is_can_view']);
+    }
+
+    /** XANH THẬT #4 — BorrowSellPrintResource: JSON thuần, không tra khóa mẫu in (Ruling T9-print). */
+    public function test_print_resource_shape_is_plain_json()
+    {
+        $bs = $this->makeWrServiceBorrowSellFixture();
+        if ($bs === null) {
+            $this->markTestSkipped('Không tìm thấy HĐ dịch vụ fixture (wr_service_contracts.id=' . self::WR_CONTRACT_ID . ') đủ điều kiện HTHT trong DB test.');
+        }
+
+        $resource = (new BorrowSellPrintResource($bs))->toArray(request());
+
+        $this->assertArrayHasKey('code', $resource);
+        $this->assertArrayHasKey('products', $resource);
+        $this->assertCount(1, $resource['products']);
+        $this->assertSame(1, $resource['products'][0]['stt']);
+    }
+
+    /**
+     * store() không quyền → 403. Cần user auth JWT thật + phân quyền dựng qua migration/seeder —
+     * môi trường test hiện không có helper actingAs employee sẵn có trong module này (khác các
+     * test posting/store thuần đơn vị hoá) → skip, ghi rõ lý do thay vì fake auth không thật.
+     */
+    public function test_store_without_permission_returns_403()
+    {
+        $this->markTestSkipped('Cần user JWT thật gán/không gán quyền "Kế toán kho" trong DB test — '
+            . 'chưa có helper actingAs employee cho module Finance ở test suite này. Gate 403 đã được '
+            . 'khoá bằng test đơn vị hoá userCanCreate() (test_user_can_create_is_fail_closed_without_auth) '
+            . 'và bằng đọc code controller (BorrowSellController::store gọi BorrowSell::userCanCreate() '
+            . 'trước khi vào service, ValidationException của service vẫn rethrow bình thường).');
+    }
+
+    private function makeWrServiceBorrowSellFixture(): ?BorrowSell
+    {
+        $wrExists = DB::table('wr_service_contracts')->where('id', self::WR_CONTRACT_ID)->exists();
+        $saExists = DB::table('wr_support_accounting')
+            ->where('contractable_id', self::WR_CONTRACT_ID)
+            ->where('contractable_type', BorrowSell::CONTRACT_WR_SERVICE)
+            ->exists();
+        if (!$wrExists || !$saExists) {
+            return null;
+        }
+
+        $bs = new BorrowSell([
+            'id' => 999999003,
+            'code' => 'PXBHM-TEST-P2-9',
+            'status' => 1,
+            'type' => 1,
+            'contractable_type' => BorrowSell::CONTRACT_WR_SERVICE,
+            'contractable_id' => self::WR_CONTRACT_ID,
+            'created_by' => 999999, // khác auth guest id → is_can_view phải false
+            'sum_amount_after_extra' => 10000000,
+            'sum_amount_after_extra_vat' => 1000000,
+            'sum_amount_after_extra_after_vat' => 11000000,
+        ]);
+
+        $product = new BorrowSellProduct([
+            'id' => 999999003,
+            'parent_id' => 999999003,
+            'product_id' => 1,
+            'code' => 'SP-TEST-P2-9',
+            'product_name' => 'SP test P2-9',
+            'model_name' => 'Model test',
+            'unit_id' => 1,
+            'unit_name' => 'Cái',
+            'price' => 1000000,
+            'extra_price' => 0,
+            'contract_qty' => 10,
+            'qty' => 10,
+            'unit_coefficient' => 5,
+            'export_price' => 900000,
+            'allocated_price' => 50000,
+            'rebate_price' => 100000,
+            'vat_percent' => 10,
+        ]);
+        $product->setRelation('details', collect());
+
+        $bs->setRelation('products', collect([$product]));
+        $bs->setRelation('tabs', collect());
+        $bs->setRelation('employee_create', null);
+        $bs->setRelation('borrowSellRequest', null);
+
+        return $bs;
+    }
+}
diff --git a/Modules/Finance/Transformers/BorrowSellResource/BorrowSellDetailResource.php b/Modules/Finance/Transformers/BorrowSellResource/BorrowSellDetailResource.php
new file mode 100644
index 000000000..b7ff43ccb
--- /dev/null
+++ b/Modules/Finance/Transformers/BorrowSellResource/BorrowSellDetailResource.php
@@ -0,0 +1,141 @@
+<?php
+
+namespace Modules\Finance\Transformers\BorrowSellResource;
+
+use Carbon\Carbon;
+use Illuminate\Http\Resources\Json\JsonResource;
+use Illuminate\Support\Facades\DB;
+use Modules\Finance\Entities\BorrowSell\BorrowSell;
+use Modules\Finance\Services\BorrowSell\BorrowSellPostingService;
+
+/**
+ * Chi tiết phiếu XUẤT BÁN HÀNG MƯỢN. Mirror `BorrowSellRequestDetailResource` + THÊM tab
+ * "Hạch toán" (Ruling T9-accounting-in-detail) — gọi thẳng BorrowSellPostingService::getDataAccounting
+ * (đã port 1-1 ở T4-6): ok → 'accounting' = accounts, 'accounting_error' = null;
+ * !ok → 'accounting' = [], 'accounting_error' = message lỗi.
+ *
+ * `borrow_sells` KHÔNG lưu snapshot khách hàng như `borrow_sell_requests` (đã verify DESCRIBE) —
+ * lấy qua quan hệ `borrowSellRequest` (yêu cầu gốc, đã có snapshot sẵn ở Phase 1).
+ */
+class BorrowSellDetailResource extends JsonResource
+{
+    private static $statusNames = [1 => 'Đã duyệt'];
+    private static $typeNames = [1 => 'HĐ hãng', 2 => 'HĐ dịch vụ'];
+
+    public function toArray($request): array
+    {
+        $isFirm = $this->contractable_type === BorrowSell::CONTRACT_FIRM;
+        $table = $isFirm ? 'firm_contracts' : 'wr_service_contracts';
+        $contractCode = $this->contractable_id
+            ? optional(DB::table($table)->where('id', $this->contractable_id)->first(['code']))->code
+            : null;
+
+        $bsr = $this->borrowSellRequest;
+
+        [$ok, $accounts, $err] = app(BorrowSellPostingService::class)->getDataAccounting($this->resource);
+
+        return [
+            'id' => $this->id,
+            'code' => $this->code,
+            'type' => $this->type,
+            'type_name' => self::$typeNames[$this->type] ?? null,
+            'status' => $this->status,
+            'status_name' => self::$statusNames[$this->status] ?? null,
+            'note' => $this->note,
+            'bear_the_shipping' => $this->bear_the_shipping,
+
+            'borrow_sell_request_id' => $this->borrow_sell_request_id,
+            'borrow_sell_request_code' => optional($bsr)->code,
+
+            'contractable_id' => $this->contractable_id,
+            'contractable_type' => $this->contractable_type,
+            'contract_type' => $isFirm ? 'firm' : 'wr_service',
+            'contract_code' => $contractCode,
+            'firm_contract_tab_id' => $this->firm_contract_tab_id,
+            'vat_percent' => $this->vat_percent,
+            'export_price' => $this->export_price,
+            'vat_cost_allocated' => $this->vat_cost_allocated,
+            'sum_amount_allocated' => $this->sum_amount_allocated,
+            'sum_amount_allocated_after_vat' => $this->sum_amount_allocated_after_vat,
+            'sum_amount_after_extra' => $this->sum_amount_after_extra,
+            'sum_amount_after_extra_vat' => $this->sum_amount_after_extra_vat,
+            'sum_amount_after_extra_after_vat' => $this->sum_amount_after_extra_after_vat,
+
+            // Snapshot khách hàng — mượn từ yêu cầu gốc (borrow_sells không tự lưu).
+            'customer_id' => optional($bsr)->customer_id,
+            'customer_name' => optional($bsr)->customer_name,
+            'customer_address' => optional($bsr)->customer_address,
+            'customer_mobile' => optional($bsr)->customer_mobile,
+            'customer_contact_name' => optional($bsr)->customer_contact_name,
+            'customer_contact_phone' => optional($bsr)->customer_contact_phone,
+            'contact_address' => optional($bsr)->contact_address,
+            'delivery_place' => optional($bsr)->delivery_place,
+
+            'created_by' => $this->created_by,
+            'creator_name' => optional(optional($this->employee_create)->info)->fullname,
+            'created_at' => self::formatDateTime($this->created_at),
+
+            'products' => $this->products->map(function ($p) {
+                return [
+                    'id' => $p->id,
+                    'product_id' => $p->product_id,
+                    'code' => $p->code,
+                    'product_name' => $p->product_name,
+                    'unit_id' => $p->unit_id,
+                    'unit_name' => $p->unit_name,
+                    'brand_id' => $p->brand_id,
+                    'brand_name' => $p->brand_name,
+                    'model_id' => $p->model_id,
+                    'model_name' => $p->model_name,
+                    'contract_qty' => $p->contract_qty,
+                    'qty' => $p->qty,
+                    'unit_coefficient' => $p->unit_coefficient,
+                    'vat_percent' => $p->vat_percent,
+                    'price' => $p->price,
+                    'extra_price' => $p->extra_price,
+                    'export_price' => $p->export_price,
+                    'allocated_price' => $p->allocated_price,
+                    'rebate_price' => $p->rebate_price,
+                    'details' => $p->relationLoaded('details')
+                        ? $p->details->map(function ($d) {
+                            return [
+                                'id' => $d->id,
+                                'product_export_request_id' => $d->product_export_request_id,
+                                'product_export_request_detail_id' => $d->product_export_request_detail_id,
+                                'product_id' => $d->product_id,
+                                'unit_id' => $d->unit_id,
+                                'qty' => $d->qty,
+                            ];
+                        })->values()
+                        : [],
+                ];
+            })->values(),
+
+            'tabs' => $this->tabs->map(function ($t) {
+                return [
+                    'id' => $t->id,
+                    'firm_contract_id' => $t->firm_contract_id,
+                    'firm_contract_tab_id' => $t->firm_contract_tab_id,
+                    'name' => $t->name,
+                ];
+            })->values(),
+
+            // Ruling T9-accounting-in-detail.
+            'accounting' => $ok ? $accounts : [],
+            'accounting_error' => $ok ? null : $err,
+
+            'is_can_view' => $this->is_can_view,
+        ];
+    }
+
+    private static function formatDateTime($value): ?string
+    {
+        if (empty($value)) {
+            return null;
+        }
+
+        return $value instanceof Carbon
+            ? $value->format('d/m/Y H:i')
+            : Carbon::parse($value)->format('d/m/Y H:i');
+    }
+}
diff --git a/Modules/Finance/Transformers/BorrowSellResource/BorrowSellListResource.php b/Modules/Finance/Transformers/BorrowSellResource/BorrowSellListResource.php
new file mode 100644
index 000000000..3f429ff17
--- /dev/null
+++ b/Modules/Finance/Transformers/BorrowSellResource/BorrowSellListResource.php
@@ -0,0 +1,73 @@
+<?php
+
+namespace Modules\Finance\Transformers\BorrowSellResource;
+
+use Carbon\Carbon;
+use Illuminate\Http\Resources\Json\ResourceCollection;
+use Illuminate\Support\Facades\DB;
+use Modules\Finance\Entities\BorrowSell\BorrowSell;
+
+/**
+ * Danh sách phiếu XUẤT BÁN HÀNG MƯỢN. Mirror `BorrowSellRequestListResource` — batch tra
+ * contract_code theo firm/wr ids (tránh N+1); `status_name`/`type_name` là map tối thiểu vì
+ * BorrowSell chỉ khai const STATUS_DEFAULT=1 (chưa có bộ đủ trạng thái như BorrowSellRequest —
+ * ghi giả định trong report).
+ */
+class BorrowSellListResource extends ResourceCollection
+{
+    private static $statusNames = [1 => 'Đã duyệt'];
+    private static $typeNames = [1 => 'HĐ hãng', 2 => 'HĐ dịch vụ'];
+
+    public function toArray($request): array
+    {
+        $firmIds = [];
+        $wrIds = [];
+        foreach ($this->collection as $it) {
+            if ($it->contractable_type === BorrowSell::CONTRACT_FIRM) {
+                $firmIds[] = $it->contractable_id;
+            } elseif ($it->contractable_type === BorrowSell::CONTRACT_WR_SERVICE) {
+                $wrIds[] = $it->contractable_id;
+            }
+        }
+        $firmCodes = $firmIds ? DB::table('firm_contracts')->whereIn('id', array_unique($firmIds))->pluck('code', 'id') : collect();
+        $wrCodes = $wrIds ? DB::table('wr_service_contracts')->whereIn('id', array_unique($wrIds))->pluck('code', 'id') : collect();
+
+        $result = [];
+        foreach ($this->collection as $item) {
+            $contractCode = $item->contractable_type === BorrowSell::CONTRACT_FIRM
+                ? ($firmCodes[$item->contractable_id] ?? null)
+                : ($wrCodes[$item->contractable_id] ?? null);
+
+            $result[] = [
+                'id' => $item->id,
+                'code' => $item->code,
+                'type' => $item->type,
+                'type_name' => self::$typeNames[$item->type] ?? null,
+                'contractable_type' => $item->contractable_type,
+                'contract_code' => $contractCode,
+                'customer_name' => optional($item->borrowSellRequest)->customer_name,
+                'creator_name' => optional(optional($item->employee_create)->info)->fullname,
+                'status' => $item->status,
+                'status_name' => self::$statusNames[$item->status] ?? null,
+                'sum_amount_after_extra_after_vat' => $item->sum_amount_after_extra_after_vat,
+                'created_at' => self::formatDateTime($item->created_at),
+
+                // Cờ hành động — FE disable nút chứ không ẩn (quy ước dự án).
+                'is_can_view' => $item->is_can_view,
+            ];
+        }
+
+        return $result;
+    }
+
+    private static function formatDateTime($value): ?string
+    {
+        if (empty($value)) {
+            return null;
+        }
+
+        return $value instanceof Carbon
+            ? $value->format('d/m/Y H:i')
+            : Carbon::parse($value)->format('d/m/Y H:i');
+    }
+}
diff --git a/Modules/Finance/Transformers/BorrowSellResource/BorrowSellPrintResource.php b/Modules/Finance/Transformers/BorrowSellResource/BorrowSellPrintResource.php
new file mode 100644
index 000000000..4c275e2bf
--- /dev/null
+++ b/Modules/Finance/Transformers/BorrowSellResource/BorrowSellPrintResource.php
@@ -0,0 +1,66 @@
+<?php
+
+namespace Modules\Finance\Transformers\BorrowSellResource;
+
+use Carbon\Carbon;
+use Illuminate\Http\Resources\Json\JsonResource;
+use Illuminate\Support\Facades\DB;
+use Modules\Finance\Entities\BorrowSell\BorrowSell;
+
+/**
+ * Bản in phiếu XUẤT BÁN HÀNG MƯỢN — JSON thuần cho FE tự render (Ruling T9-print: KHÔNG tra
+ * khóa mẫu in). Mirror `BorrowSellRequestPrintResource`.
+ */
+class BorrowSellPrintResource extends JsonResource
+{
+    public function toArray($request): array
+    {
+        $isFirm = $this->contractable_type === BorrowSell::CONTRACT_FIRM;
+        $table = $isFirm ? 'firm_contracts' : 'wr_service_contracts';
+        $contractCode = $this->contractable_id
+            ? optional(DB::table($table)->where('id', $this->contractable_id)->first(['code']))->code
+            : null;
+
+        $bsr = $this->borrowSellRequest;
+
+        return [
+            'code' => $this->code,
+            'contract_code' => $contractCode,
+            'note' => $this->note,
+            'created_at' => self::formatDateTime($this->created_at),
+            'creator_name' => optional(optional($this->employee_create)->info)->fullname,
+
+            'customer_name' => optional($bsr)->customer_name,
+            'customer_address' => optional($bsr)->customer_address,
+            'customer_mobile' => optional($bsr)->customer_mobile,
+            'customer_contact_name' => optional($bsr)->customer_contact_name,
+            'customer_contact_phone' => optional($bsr)->customer_contact_phone,
+            'contact_address' => optional($bsr)->contact_address,
+            'delivery_place' => optional($bsr)->delivery_place,
+
+            'products' => $this->products->map(function ($p, $i) {
+                return [
+                    'stt' => $i + 1,
+                    'code' => $p->code,
+                    'product_name' => $p->product_name,
+                    'model_name' => $p->model_name,
+                    'unit_name' => $p->unit_name,
+                    'qty' => $p->qty,
+                    'export_price' => $p->export_price,
+                    'thanh_tien' => $p->export_price !== null ? $p->export_price * $p->qty : null,
+                ];
+            })->values(),
+        ];
+    }
+
+    private static function formatDateTime($value): ?string
+    {
+        if (empty($value)) {
+            return null;
+        }
+
+        return $value instanceof Carbon
+            ? $value->format('d/m/Y H:i')
+            : Carbon::parse($value)->format('d/m/Y H:i');
+    }
+}
