# Review package — Task P2-2 (BASE c562527 → HEAD 1c103ca)

## git log --oneline
```
1c103cae5 feat(finance): thêm entity ActivityHasDeliveryTrip (Phase 2 hạch toán chuyến xe)
```
## git diff --stat
```
 .../Entities/Delivery/ActivityHasDeliveryTrip.php  | 26 ++++++++++++++++++++++
 .../Unit/ActivityHasDeliveryTripEntityTest.php     | 23 +++++++++++++++++++
 2 files changed, 49 insertions(+)
```
## git diff -U10
```diff
diff --git a/Modules/Finance/Entities/Delivery/ActivityHasDeliveryTrip.php b/Modules/Finance/Entities/Delivery/ActivityHasDeliveryTrip.php
new file mode 100644
index 000000000..2fa10f497
--- /dev/null
+++ b/Modules/Finance/Entities/Delivery/ActivityHasDeliveryTrip.php
@@ -0,0 +1,26 @@
+<?php
+
+namespace Modules\Finance\Entities\Delivery;
+
+use Illuminate\Database\Eloquent\Model;
+
+/**
+ * Nối 1 lượt xuất/nhập kho (`warehouse_export`/`warehouse_import`) với 1 chuyến xe giao hàng
+ * (`delivery_trips`) của ERP — dùng cho hạch toán chuyến xe giao hàng (Phase 2, T6).
+ *
+ * @property int   $warehouse_export_id
+ * @property int   $warehouse_import_id
+ * @property int   $delivery_trip_id
+ * @property float $total_cost_transition
+ */
+class ActivityHasDeliveryTrip extends Model
+{
+    protected $table = 'activity_has_delivery_trips';
+
+    protected $guarded = [];
+
+    public function trip()
+    {
+        return $this->belongsTo(DeliveryTrip::class, 'delivery_trip_id', 'id');
+    }
+}
diff --git a/Modules/Finance/Tests/Unit/ActivityHasDeliveryTripEntityTest.php b/Modules/Finance/Tests/Unit/ActivityHasDeliveryTripEntityTest.php
new file mode 100644
index 000000000..489f3e2d0
--- /dev/null
+++ b/Modules/Finance/Tests/Unit/ActivityHasDeliveryTripEntityTest.php
@@ -0,0 +1,23 @@
+<?php
+
+namespace Modules\Finance\Tests\Unit;
+
+use Tests\TestCase;
+use Modules\Finance\Entities\Delivery\ActivityHasDeliveryTrip;
+use Modules\Finance\Entities\Delivery\DeliveryTrip;
+
+class ActivityHasDeliveryTripEntityTest extends TestCase
+{
+    public function test_table_name_is_activity_has_delivery_trips()
+    {
+        $this->assertEquals('activity_has_delivery_trips', (new ActivityHasDeliveryTrip())->getTable());
+    }
+
+    public function test_trip_relation_points_to_delivery_trip()
+    {
+        $rel = (new ActivityHasDeliveryTrip())->trip();
+        $this->assertInstanceOf(\Illuminate\Database\Eloquent\Relations\BelongsTo::class, $rel);
+        $this->assertInstanceOf(DeliveryTrip::class, $rel->getRelated());
+        $this->assertEquals('delivery_trip_id', $rel->getForeignKeyName());
+    }
+}
```
