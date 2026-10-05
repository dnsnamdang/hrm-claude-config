# Review package: b85478388..81bdddd18

## Commits
81bdddd18 refactor(cmd): chuyển popup drill báo cáo phát triển thị trường sang V2BaseReportModal + mixin

## Files changed
 .../components/DevelopmentDrillModal.vue           | 781 +++++++++------------
 1 file changed, 315 insertions(+), 466 deletions(-)

## Diff
diff --git a/pages/assign/report/customer-market-development/components/DevelopmentDrillModal.vue b/pages/assign/report/customer-market-development/components/DevelopmentDrillModal.vue
index da85d3aec..a2f30251d 100644
--- a/pages/assign/report/customer-market-development/components/DevelopmentDrillModal.vue
+++ b/pages/assign/report/customer-market-development/components/DevelopmentDrillModal.vue
@@ -10,217 +10,209 @@
        BỎ cột Trạng thái (mọi dòng đều "Huỷ") và BỎ 2 cột nhu cầu (nhu cầu chỉ ghi nhận được ở
        meeting Hoàn thành nên ở đây luôn rỗng).
     3. KH mới — là danh sách KHÁCH HÀNG, không phải meeting:
        `STT · Khách hàng · Thị trường · Phòng ban · Bộ phận · Người tạo KH · Ngày tạo KH`
 
     2 luật bỏ cột dùng chung cho cả 3 biến thể:
       · cấp đã bị node CỐ ĐỊNH thì bỏ luôn cột đó (mọi dòng mang đúng 1 giá trị, cột chỉ lặp lại
         điều tiêu đề popup đã nói);
       · bỏ cột Bộ phận khi KHÔNG dòng nào thuộc bộ phận.
     Hệ quả: popup mở theo Khách hàng mất cột Khách hàng -> chip "KH mới" NHẢY SANG cột Tên meeting.
+
+    Dựng TRÊN `components/report/V2BaseReportModal.vue` (vỏ dùng chung cho popup báo cáo) +
+    `utils/mixins/reportDrillListMixin.js` (máy sắp xếp + phân trang tại chỗ) — cùng khuôn với
+    `pages/assign/report/potential-customer-care/components/DemandListModal.vue` (popup gốc). Khác
+    biệt DUY NHẤT với popup gốc: popup này lọc CLIENT-SIDE trên mảng `rows` đã tải sẵn (không gọi lại
+    API). `applyLocalFilters()` của mixin không hợp ở đây — nó so `row[param]` thẳng, còn ô lọc khai
+    theo id khác tên field thật (`market` ứng với `province_id`…) — nên GIỮ hàm lọc riêng
+    `filteredRows`, chỉ đổi tên state `ownFilters` -> `filters` để dùng chung
+    `resetFilters()`/`resetFilterState()`/`hasActiveFilter` của mixin.
+
+    Khung popup, dải banner đầu, bảng + thanh cuộn, phân trang, nút phóng to, cuộn-về-đầu khi lật
+    trang đều do vỏ lo — component này chỉ còn giữ phần NGHIỆP VỤ RIÊNG: bộ lọc, khối KPI/phân bổ,
+    thứ tự + nội dung cột, và các ô bảng cần hiển thị đặc biệt.
 -->
 <template>
-    <V2BaseModal
-        ref="baseModal"
+    <V2BaseReportModal
         modal-id="cmd-drill-modal"
-        :title="modalTitle"
-        subtitle-label="Thuộc"
-        :subtitle="crumb"
-        icon="ri-file-list-3-line"
-        size="xl"
-        dialog-class="cmd-drill-dialog"
-        max-body-height="70vh"
-        @hidden="$emit('close')"
+        :visible="visible"
+        :loading="loading"
+        lead="Bạn đang xem phát triển thị trường:"
+        :title="drillTitle"
+        :meta="metaText"
+        :columns="baseColumns"
+        :rows="pagedRows"
+        :start-index="pageOffset"
+        :sort="sort"
+        :current-page="safePage"
+        :current-page-size="pageSize"
+        :total-rows="filteredRows.length"
+        :item-label="unit"
+        :empty-text="`Không có ${unit} nào khớp bộ lọc.`"
+        @sort="({ key }) => toggleSort(key)"
+        @page-change="onPageChange"
+        @page-size-change="onPageSizeChange"
+        @close="$emit('close')"
     >
         <!--
             Bộ lọc riêng của popup (luật 1 trong design.md):
               · đang xem theo đối tượng A thì BỎ ô lọc theo A (mọi chiều nằm trên `path` của node);
               · cố định Khách hàng thì ẩn luôn ô Thị trường (1 KH chỉ thuộc 1 thị trường);
               · popup "KH mới" không liệt kê meeting nên bỏ 2 ô Loại meeting / Trạng thái.
-            Ô bị ẩn PHẢI xoá giá trị (watcher `visibleFields`) — nếu không sẽ lọc ngầm.
+            Ô bị ẩn PHẢI xoá giá trị — mọi đường đổi `path`/`metric` đi qua `resetState()` nên tự dọn.
             Select trong modal dùng V2BaseSelectInModal để dropdown không bị popup cắt.
         -->
-        <div class="cmd-drill-filters">
-            <V2BaseInput v-model="keyword" class="cmd-drill-search" :placeholder="`Tìm trong ${rows.length} ${unit}…`" size="sm" />
-
-            <V2BaseSelectInModal
-                v-for="field in visibleFields"
-                :key="field.id"
-                v-model="ownFilters[field.id]"
-                class="cmd-drill-filter"
-                :options="optionsOf(field.id)"
-                :placeholder="field.placeholder"
-                :allowClear="true"
-                size="sm"
-            />
-
-            <V2BaseButton v-if="hasActiveFilter" tertiary size="xs" @click="resetFilters">
-                <template #prefix><i class="ri-refresh-line" style="font-size: 13px"></i></template>
-                Xoá lọc
-            </V2BaseButton>
-
-            <span class="cmd-drill-count">{{ filteredRows.length }} / {{ rows.length }} {{ unit }}</span>
-        </div>
+        <template #filters>
+            <div class="report-drill-filters">
+                <V2BaseInput
+                    v-model="keyword"
+                    class="report-drill-search"
+                    :placeholder="`Tìm trong ${rows.length} ${unit}…`"
+                    size="sm"
+                    @input="onFilterChange"
+                />
+
+                <V2BaseSelectInModal
+                    v-for="field in visibleFields"
+                    :key="field.id"
+                    v-model="filters[field.id]"
+                    class="report-drill-filter"
+                    :options="optionsOf(field.id)"
+                    :placeholder="field.placeholder"
+                    :allowClear="true"
+                    size="sm"
+                    @change="onFilterChange"
+                />
+
+                <V2BaseButton v-if="hasActiveFilter" tertiary size="xs" @click="resetFilters">
+                    <template #prefix><i class="ri-refresh-line" style="font-size: 13px"></i></template>
+                    Xoá lọc
+                </V2BaseButton>
+
+                <span class="report-drill-count">{{ filteredRows.length }} / {{ rows.length }} {{ unit }}</span>
+            </div>
+        </template>
 
         <!--
             Khối tổng hợp của popup (luật 0 + luật 3 trong design.md) — MẶC ĐỊNH THU GỌN để mở popup
-            ra là thấy ngay danh sách. Nút thu gọn dùng chung khuôn `.rsum-toggle` với khối tổng hợp
-            của màn chính. `v-if` (không phải `v-show`): thu gọn thì khỏi dựng, khỏi tính.
+            ra là thấy ngay danh sách. `summaryCollapsed` nay là data CỦA MIXIN (dùng chung với 2
+            popup kia). `v-if` (không phải `v-show`): thu gọn thì khỏi dựng, khỏi tính.
         -->
-        <div class="cmd-sumhead" :class="{ 'cmd-sumhead--collapsed': sumCollapsed }">
-            <span class="cmd-sumhead__label">Tổng hợp danh sách đang xem</span>
-            <button
-                type="button"
-                class="rsum-toggle"
-                :class="{ 'rsum-toggle--collapsed': sumCollapsed }"
-                :title="`${sumCollapsed ? 'Xem' : 'Thu gọn'} khối tổng hợp`"
-                @click="sumCollapsed = !sumCollapsed"
-            >
-                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
-                    <polyline points="6 9 12 15 18 9"></polyline>
-                </svg>
-                {{ sumCollapsed ? 'Xem tổng hợp' : 'Thu gọn' }}
-            </button>
-        </div>
-
-        <div v-if="!sumCollapsed" class="cmd-sumwrap">
-            <!-- 3 hộp KPI — popup "KH mới" bỏ hẳn vì cả 3 đều tính trên meeting -->
-            <section v-if="!isNewMetric" class="cmd-sumbox">
-                <div class="cmd-kpis">
-                    <div v-for="kpi in kpis" :key="kpi.key" class="cmd-kpi" :class="`cmd-kpi--${kpi.tone}`">
-                        <span class="cmd-kpi__label">
-                            {{ kpi.label }}<InfoTip :head="kpi.tip.head" :lines="kpi.tip.lines" />
-                        </span>
-                        <span class="cmd-kpi__value">{{ kpi.value }}<em>{{ kpi.sub }}</em></span>
-                        <!-- Ô KPI chỉ có SỐ (KH mới) vẫn giữ thanh nền ẩn để 3 hộp cao bằng nhau -->
-                        <span class="cmd-kpi__track" :style="{ visibility: kpi.percent === null ? 'hidden' : 'visible' }">
-                            <span class="cmd-kpi__fill" :style="{ width: `${kpi.percent || 0}%` }"></span>
-                        </span>
-                    </div>
-                </div>
-            </section>
-
-            <!-- Dải chip phân bổ: CHỈ Thị trường + Phòng ban, ẩn theo đúng luật ẩn của ô lọc -->
-            <section v-if="allocations.length" class="cmd-sumbox">
-                <h4 class="cmd-sumbox__title">Phân bổ {{ unit }} theo cơ cấu</h4>
-                <div class="cmd-sum">
-                    <div v-for="group in allocations" :key="group.dim" class="cmd-sum__grp">
-                        <span class="cmd-sum__label">{{ group.label }}</span>
-                        <span class="cmd-sum__chips">
-                            <button
-                                v-for="chip in group.chips"
-                                :key="chip.id"
-                                type="button"
-                                class="cmd-sum__chip"
-                                :class="{ 'cmd-sum__chip--on': String(ownFilters[group.dim]) === String(chip.id) }"
-                                title="Lọc nhanh theo mục này"
-                                @click="toggleChip(group.dim, chip.id)"
-                            >
-                                <span class="cmd-sum__chip__name">{{ chip.name }}</span>
-                                <span class="cmd-sum__chip__n">{{ chip.count }}</span>
-                                <span class="cmd-sum__chip__pct">{{ chip.percent }}%</span>
-                            </button>
-                        </span>
+        <template #summary>
+            <div class="report-drill-sumhead" :class="{ 'report-drill-sumhead--collapsed': summaryCollapsed }">
+                <span class="report-drill-sumhead__label">Tổng hợp danh sách đang xem</span>
+                <button
+                    type="button"
+                    class="rsum-toggle"
+                    :class="{ 'rsum-toggle--collapsed': summaryCollapsed }"
+                    :title="`${summaryCollapsed ? 'Xem' : 'Thu gọn'} khối tổng hợp`"
+                    @click="summaryCollapsed = !summaryCollapsed"
+                >
+                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
+                        <polyline points="6 9 12 15 18 9"></polyline>
+                    </svg>
+                    {{ summaryCollapsed ? 'Xem tổng hợp' : 'Thu gọn' }}
+                </button>
+            </div>
+
+            <div v-if="!summaryCollapsed" class="report-drill-sumwrap">
+                <!-- 3 hộp KPI — popup "KH mới" bỏ hẳn vì cả 3 đều tính trên meeting -->
+                <section v-if="!isNewMetric" class="report-drill-sumbox">
+                    <div class="report-drill-kpis">
+                        <div v-for="kpi in kpis" :key="kpi.key" class="report-drill-kpi" :class="`report-drill-kpi--${kpi.tone}`">
+                            <span class="report-drill-kpi__label">
+                                {{ kpi.label }}<InfoTip :head="kpi.tip.head" :lines="kpi.tip.lines" />
+                            </span>
+                            <span class="report-drill-kpi__value">{{ kpi.value }}<em>{{ kpi.sub }}</em></span>
+                            <!-- Ô KPI chỉ có SỐ (KH mới) vẫn giữ thanh nền ẩn để 3 hộp cao bằng nhau -->
+                            <span class="report-drill-kpi__track" :style="{ visibility: kpi.percent === null ? 'hidden' : 'visible' }">
+                                <span class="report-drill-kpi__fill" :style="{ width: `${kpi.percent || 0}%` }"></span>
+                            </span>
+                        </div>
                     </div>
-                </div>
-            </section>
-        </div>
-
-        <!-- Bảng tràn ngang -> BẮT BUỘC bọc V2BaseTableScroll để có thanh cuộn ở CẢ TRÊN VÀ DƯỚI
-             (quy tắc chung của hrm-client; trước đây tự bọc 1 div overflow nên chỉ có thanh dưới,
-             bảng rộng 2047px trong khung 1108px mà người dùng phải mò tới đáy mới cuộn được). -->
-        <!-- Chiều cao bảng = trần body (70vh) TRỪ hàng bộ lọc + thanh cuộn ngang phía trên, để CHỈ
-             bảng cuộn dọc. Đo thật: để 60vh thì body tràn 40px -> 2 thanh cuộn lồng nhau (đúng bẫy
-             "2 thanh cuộn dọc" của skill modal-popup mục 3b). -->
-        <V2BaseTableScroll :max-height="tableMaxHeight">
-            <table class="cmd-drill-table">
-                <colgroup>
-                    <col v-for="column in columns" :key="`col-${column.id}`" :style="{ width: column.width ? `${column.width}px` : 'auto' }" />
-                </colgroup>
-                <thead>
-                    <tr>
-                        <th
-                            v-for="column in columns"
-                            :key="column.id"
-                            :class="{ 'cmd-sortable': column.sortable }"
-                            @click="column.sortable && sortBy(column.id)"
-                        >
-                            {{ column.label }}
-                            <span v-if="column.sortable" class="cmd-sort" :class="sortClass(column.id)">
-                                <i class="ri-arrow-up-s-line"></i><i class="ri-arrow-down-s-line"></i>
+                </section>
+
+                <!-- Dải chip phân bổ: CHỈ Thị trường + Phòng ban, ẩn theo đúng luật ẩn của ô lọc -->
+                <section v-if="allocations.length" class="report-drill-sumbox">
+                    <h4 class="report-drill-sumbox__title">Phân bổ {{ unit }} theo cơ cấu</h4>
+                    <div class="report-drill-sum">
+                        <div v-for="group in allocations" :key="group.dim" class="report-drill-sum__grp">
+                            <span class="report-drill-sum__label">{{ group.label }}</span>
+                            <span class="report-drill-sum__chips">
+                                <button
+                                    v-for="chip in group.chips"
+                                    :key="chip.id"
+                                    type="button"
+                                    class="report-drill-sum__chip"
+                                    :class="{ 'report-drill-sum__chip--on': String(filters[group.dim]) === String(chip.id) }"
+                                    title="Lọc nhanh theo mục này"
+                                    @click="toggleChip(group.dim, chip.id)"
+                                >
+                                    <span class="report-drill-sum__chip__name">{{ chip.name }}</span>
+                                    <span class="report-drill-sum__chip__n">{{ chip.count }}</span>
+                                    <span class="report-drill-sum__chip__pct">{{ chip.percent }}%</span>
+                                </button>
                             </span>
-                        </th>
-                    </tr>
-                </thead>
-                <tbody>
-                    <tr v-for="(row, index) in pagedRows" :key="row.id">
-                        <td v-for="column in columns" :key="`${row.id}-${column.id}`" :class="column.cellClass">
-                            <!-- Lý do huỷ: 2 dòng — lý do từ danh mục + ghi chú nhập tay -->
-                            <template v-if="column.id === 'cancel'">
-                                <div class="cmd-cancel__reason">{{ row.cancel_reason_name || '—' }}</div>
-                                <div v-if="row.cancel_note" class="cmd-cancel__note">{{ row.cancel_note }}</div>
-                            </template>
-                            <template v-else-if="column.id === 'name'">
-                                <span class="cmd-clamp" :title="row.name">{{ row.name }}</span>
-                                <span v-if="chipOnName && row.is_new_customer === false && isNewCustomer(row)" class="cmd-newchip">KH mới</span>
-                            </template>
-                            <template v-else-if="column.id === 'customer'">
-                                <span class="cmd-clamp" :title="row.customer_name">{{ row.customer_name }}</span>
-                                <span v-if="!isNewMetric && isNewCustomer(row)" class="cmd-newchip">KH mới</span>
-                            </template>
-                            <template v-else>{{ cellText(row, column, pageOffset + index) }}</template>
-                        </td>
-                    </tr>
-                    <tr v-if="!pagedRows.length">
-                        <td class="cmd-drill-empty" :colspan="columns.length">Không có {{ unit }} nào khớp bộ lọc.</td>
-                    </tr>
-                </tbody>
-            </table>
-        </V2BaseTableScroll>
-
-        <!-- Phân trang trên tập ĐÃ LỌC + ĐÃ SẮP. In / Xuất Excel vẫn lấy TOÀN BỘ tập đó, không
-             phải mỗi trang đang xem. -->
-        <V2BasePagination
-            :current-page="safePage"
-            :current-page-size="pageSize"
-            :total-rows="filteredRows.length"
-            :item-label="unit"
-            :page-size-options="[20, 50, 100]"
-            @page-change="page = $event"
-            @page-size-change="onPageSizeChange"
-        />
+                        </div>
+                    </div>
+                </section>
+            </div>
+        </template>
+
+        <!-- Ô đặc biệt: bê nguyên nội dung từng cột cần hiển thị khác `row[col.field]` mặc định.
+             4 cột (market/dept/host/status) không cần slot — vỏ tự lấy đúng `row[col.field]` qua
+             adapter `baseColumns()` vì cellText() trả về NGUYÊN VĂN field đó, không định dạng gì. -->
+        <template #cell-name="{ row }">
+            <span class="report-drill-clamp" :title="row.name">{{ row.name }}</span>
+            <span v-if="chipOnName && row.is_new_customer === false && isNewCustomer(row)" class="report-drill-newchip">KH mới</span>
+        </template>
+        <template #cell-customer="{ row }">
+            <span class="report-drill-clamp" :title="row.customer_name">{{ row.customer_name }}</span>
+            <span v-if="!isNewMetric && isNewCustomer(row)" class="report-drill-newchip">KH mới</span>
+        </template>
+        <!-- Lý do huỷ: 2 dòng — lý do từ danh mục + ghi chú nhập tay -->
+        <template #cell-cancel="{ row }">
+            <div class="report-drill-cancel__reason">{{ row.cancel_reason_name || '—' }}</div>
+            <div v-if="row.cancel_note" class="report-drill-cancel__note">{{ row.cancel_note }}</div>
+        </template>
+        <template #cell-part="{ row, column, index }">{{ cellText(row, column, index) }}</template>
+        <template #cell-cus_created="{ row, column, index }">{{ cellText(row, column, index) }}</template>
+        <template #cell-date="{ row, column, index }">{{ cellText(row, column, index) }}</template>
+        <template #cell-created="{ row, column, index }">{{ cellText(row, column, index) }}</template>
+        <template #cell-type="{ row, column, index }">{{ cellText(row, column, index) }}</template>
+        <template #cell-demand_names="{ row, column, index }">{{ cellText(row, column, index) }}</template>
+        <template #cell-investment="{ row, column, index }">{{ cellText(row, column, index) }}</template>
 
         <!-- Thứ tự + màu theo skill button-convention (modal footer: action phụ trước, Đóng cuối) -->
         <template #footer>
             <V2BaseButton secondary size="sm" @click="printList">
                 <template #prefix><i class="ri-printer-line" style="font-size: 14px"></i></template>
                 In danh sách
             </V2BaseButton>
             <V2BaseButton secondary status="success" size="sm" @click="exportExcel">
                 <template #prefix><i class="ri-file-excel-2-line" style="font-size: 14px"></i></template>
                 Xuất Excel danh sách
             </V2BaseButton>
-            <V2BaseButton tertiary size="sm" @click="close">
+            <V2BaseButton tertiary size="sm" @click="$emit('close')">
                 <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
                 Đóng
             </V2BaseButton>
         </template>
-    </V2BaseModal>
+    </V2BaseReportModal>
 </template>
 
 <script>
 import V2BaseInput from '@/components/V2BaseInput.vue'
 import V2BaseButton from '@/components/V2BaseButton.vue'
-import V2BaseModal from '@/components/modal/V2BaseModal.vue'
-import V2BaseTableScroll from '@/components/V2BaseTableScroll.vue'
 import V2BaseSelectInModal from '@/components/V2BaseSelectInModal.vue'
-import V2BasePagination from '@/components/V2BasePagination.vue'
+import V2BaseReportModal from '@/components/report/V2BaseReportModal.vue'
+import reportDrillListMixin from '@/utils/mixins/reportDrillListMixin'
 import InfoTip from './InfoTip.vue'
 
 const METRIC_LABEL = {
     plan: 'Kế hoạch meeting',
     completed: 'Meeting hoàn thành',
     cancelled: 'Meeting bị huỷ',
     new: 'Khách hàng mới tạo trong kỳ',
     demand: 'Nhu cầu đầu tư thu thập',
     pre: 'Meeting lập trước kỳ',
     inp: 'Meeting lập trong kỳ',
@@ -243,99 +235,101 @@ const FILTER_FIELDS = [
 /**
  * 2 chiều được phân bổ bằng chip (luật 3): Thị trường + Phòng ban. KHÔNG có Loại meeting / Trạng
  * thái (không phải "cơ cấu") và KHÔNG có Nhân viên / Khách hàng (số lượng lớn, chip vụn).
  * `dim` trùng id ô lọc nên bấm chip là bật/tắt đúng ô lọc đó.
  */
 const ALLOC_DIMS = [
     { dim: 'market', label: 'Thị trường', idOf: (r) => r.province_id, nameOf: (r) => r.province_name },
     { dim: 'dept', label: 'Phòng ban', idOf: (r) => r.department_id, nameOf: (r) => r.department_name },
 ]
 
-/**
- * Dưới ngưỡng này (≈ 6 dòng) thì bảng không đáng để có vùng cuộn riêng nữa — nhường cho cả thân
- * popup cuộn, xem `syncTableHeight()`.
- */
-const MIN_TABLE_HEIGHT = 180
-
 /** Trạng thái meeting — dùng cho 2 ô KPI tỷ lệ (đồng bộ Meeting::HOAN_THANH / Meeting::HUY ở BE) */
 const STATUS_COMPLETED = 3
 const STATUS_CANCELLED = 4
 
 const DIM_LABEL = {
     market: 'Thị trường',
     customer: 'Khách hàng',
     dept: 'Phòng ban',
     part: 'Bộ phận',
     host: 'Nhân viên',
 }
 
+/**
+ * `cellClass` cũ (`cmd-*`) -> lớp mới: `report-drill-table__center` đã có sẵn trong `V2BaseReportModal`
+ * (khối KHÔNG scoped của vỏ) nên dùng thẳng, không định nghĩa lại; `report-drill-table__money` là
+ * lớp NGHIỆP VỤ riêng của popup này, định nghĩa KHÔNG scoped ở cuối file — xem comment ở đó.
+ */
+const CELL_CLASS_MAP = { 'cmd-center': 'report-drill-table__center', 'cmd-money': 'report-drill-table__money' }
+
+/**
+ * 4 cột hiển thị NGUYÊN VĂN field của row, không định dạng/giá trị mặc định gì (`cellText()` trả về
+ * đúng field này) -> để vỏ tự render qua `row[col.field]`, khỏi cần slot riêng. Cột nào cần định
+ * dạng (ngày, tiền) hoặc giá trị mặc định (`—`) vẫn đi qua slot `#cell-<id>` gọi `cellText()`.
+ */
+const FIELD_MAP = { market: 'province_name', dept: 'department_name', host: 'host_name', status: 'status_name' }
+
 export default {
     name: 'DevelopmentDrillModal',
-    components: { V2BaseInput, V2BaseButton, V2BaseModal, V2BaseTableScroll, V2BaseSelectInModal, V2BasePagination, InfoTip },
+    components: { V2BaseInput, V2BaseButton, V2BaseSelectInModal, V2BaseReportModal, InfoTip },
+    mixins: [reportDrillListMixin],
     props: {
         visible: { type: Boolean, default: false },
         loading: { type: Boolean, default: false },
         rows: { type: Array, default: () => [] },
         metric: { type: String, default: 'plan' },
         /** Đường dẫn cấp của node đang xem — dùng để đặt tiêu đề và BỎ CỘT của cấp đã cố định */
         path: { type: Array, default: () => [] },
         /** Khoá node đang xem — gửi kèm khi in để BE lọc đúng nhánh */
         nodeKey: { type: String, default: 'ALL' },
         newCustomerIds: { type: Array, default: () => [] },
         /**
          * Bộ chỉ tiêu CỦA NHÁNH đang xem (dòng TỔNG thì là `total` của báo cáo). Chỉ dùng cho ô KPI
          * "KH mới tạo trong kỳ": khách hàng mới KHÔNG gắn với meeting nào nên không suy ra được từ
          * danh sách đang xem, và cũng không đổi khi lọc trong popup.
          */
         nodeMetrics: { type: Object, default: null },
     },
-    data() {
-        return {
-            keyword: '',
-            // Khối tổng hợp MẶC ĐỊNH THU GỌN — mở popup ra là thấy ngay danh sách (luật 0)
-            sumCollapsed: true,
-            // Trần chiều cao vùng cuộn của bảng — ĐO THẬT trong syncTableHeight()
-            tableMaxHeight: 'calc(70vh - 132px)',
-            page: 1,
-            pageSize: 20,
-            sort: { column: 'date', dir: 'asc' },
-            ownFilters: { market: null, customer: null, dept: null, part: null, host: null, type: null, status: null },
-        }
-    },
     computed: {
         isNewMetric() {
             return this.metric === 'new'
         },
         unit() {
             return this.isNewMetric ? 'khách hàng' : 'meeting'
         },
         metricLabel() {
             return METRIC_LABEL[this.metric] || 'danh sách'
         },
-        /** Tiêu đề popup — chỉ tiêu + đối tượng đang xem, kèm số dòng */
-        modalTitle() {
-            return `${this.metricLabel}${this.nodeLabel} · ${this.rows.length} ${this.unit}`
-        },
         nodeLabel() {
             if (!this.path.length) return ' — toàn bộ báo cáo'
             const last = this.path[this.path.length - 1]
 
             return ` theo ${DIM_LABEL[last.dim] || ''}: ${last.name}`
         },
+        /** "Đối tượng" đang xem cho dải banner của vỏ — chỉ tiêu + đối tượng, KHÔNG kèm số dòng */
+        drillTitle() {
+            return `${this.metricLabel}${this.nodeLabel}`
+        },
         crumb() {
             if (this.path.length < 2) return ''
 
             return this.path
                 .slice(0, -1)
                 .map((item) => `${DIM_LABEL[item.dim] || ''}: ${item.name}`)
                 .join(' › ')
         },
+        /** Dòng phụ đề của dải banner — breadcrumb (nếu có) + số dòng của TOÀN NHÁNH (chưa lọc) */
+        metaText() {
+            const count = `${this.rows.length} ${this.unit}`
+
+            return this.crumb ? `Thuộc: ${this.crumb} · ${count}` : count
+        },
         /** Các chiều đã bị node cố định -> bỏ luôn cột tương ứng */
         fixedDims() {
             return this.path.map((item) => item.dim)
         },
         /**
          * Ô lọc nào được hiện. Chiều nằm trên `path` đã cố định rồi nên lọc lại theo chính nó là
          * thừa; khách hàng cố định thì thị trường cũng chỉ còn đúng 1 giá trị.
          */
         visibleFields() {
             const fixed = this.fixedDims
@@ -441,41 +435,72 @@ export default {
 
                     const chips = Array.from(counts.values())
                         .sort((a, b) => b.count - a.count)
                         .slice(0, 12)
                         .map((chip) => ({ ...chip, percent: Math.round((chip.count * 100) / rows.length) }))
 
                     return { dim: dim.dim, label: dim.label, chips }
                 })
                 .filter((group) => group.chips.length)
         },
-        pageCount() {
-            return Math.max(1, Math.ceil(this.filteredRows.length / this.pageSize))
-        },
-        /** Trang thực dùng, KẸP trong [1, pageCount]: lọc hẹp lại mà giữ `page` cũ là ra trang trắng */
-        safePage() {
-            return Math.min(Math.max(1, this.page), this.pageCount)
-        },
-        pageOffset() {
-            return (this.safePage - 1) * this.pageSize
-        },
-        /** Dòng của TRANG đang xem. KPI, dải chip, In, Xuất Excel vẫn dùng `filteredRows` (toàn tập) */
-        pagedRows() {
-            return this.filteredRows.slice(this.pageOffset, this.pageOffset + this.pageSize)
+        /**
+         * Lọc CLIENT-SIDE trên tập THÔ (`rows`, chưa sắp). `applyLocalFilters()` của mixin không hợp
+         * ở đây — nó so `row[param]` trực tiếp, còn ô lọc khai theo id khác tên field thật (`market`
+         * ứng với `province_id`…) — giữ nguyên hàm lọc riêng, chỉ đổi `ownFilters` -> `filters`
+         * (mixin) để dùng chung `resetFilters()`/`resetFilterState()`/`hasActiveFilter`.
+         */
+        filteredRows() {
+            const keyword = this.keyword.trim().toLowerCase()
+
+            return this.rows.filter((row) => {
+                for (const field of FILTER_FIELDS) {
+                    const picked = this.filters[field.id]
+                    if (picked != null && String(field.valueOf(row)) !== String(picked)) return false
+                }
+
+                if (!keyword) return true
+                const haystack = `${row.name || ''} ${row.customer_name || ''} ${row.host_name || ''} ${row.demand_names || ''}`
+
+                return haystack.toLowerCase().indexOf(keyword) !== -1
+            })
         },
-        hasActiveFilter() {
-            return this.keyword.trim() !== '' || Object.keys(this.ownFilters).some((key) => this.ownFilters[key] != null)
+        /**
+         * ĐÈ LÊN `sortedRows` của mixin: bản gốc của mixin sắp thẳng `this.rows` (tập THÔ, chưa lọc)
+         * — popup này lọc client-side nên phải sắp trên `filteredRows`. `pageCount`/`safePage`/
+         * `pageOffset`/`pagedRows` của mixin đều đọc qua `this.sortedRows` (không đọc `this.rows`
+         * trực tiếp) nên override đúng 1 computed này là đủ, không phải viết lại cả chuỗi phân trang.
+         */
+        sortedRows() {
+            const rows = this.filteredRows
+            const key = this.sort.key
+            if (!key) return rows
+
+            const dir = this.sort.dir === 'desc' ? -1 : 1
+
+            return rows.slice().sort((a, b) => {
+                const va = this.sortValue(a, key)
+                const vb = this.sortValue(b, key)
+                let result = typeof va === 'string' ? va.localeCompare(vb, 'vi') : va - vb
+                if (!result) result = String(a.code || '').localeCompare(String(b.code || ''))
+
+                return result * dir
+            })
         },
         /** Cột Khách hàng bị bỏ -> chip "KH mới" nhảy sang ô Tên meeting */
         chipOnName() {
             return !this.columns.some((column) => column.id === 'customer')
         },
+        /**
+         * NGUỒN GỐC của bộ cột — vẫn dùng cho bản in + Xuất Excel của màn, KHÔNG SỬA cấu trúc/logic
+         * ở đây (chốt Task 9). Khoá `id` + `width` số + `cellClass` kiểu cũ (`cmd-*`) được adapter
+         * `baseColumns()` bên dưới map lại cho `V2BaseReportModal`.
+         */
         columns() {
             const fixed = this.fixedDims.slice()
 
             // Bỏ cột Bộ phận khi KHÔNG dòng nào thuộc bộ phận (phần lớn phòng ban không chia bộ phận)
             if (!this.rows.some((row) => row.part_id)) fixed.push('part')
 
             const dims = [
                 { id: 'customer', label: 'Khách hàng', width: 210 },
                 { id: 'market', label: 'Thị trường', width: 130 },
                 { id: 'dept', label: 'Phòng ban', width: 150, sortable: true },
@@ -510,240 +535,130 @@ export default {
                 stt,
                 { id: 'name', label: 'Tên meeting', width: 250 },
                 { id: 'date', label: 'Ngày họp', width: 128, cellClass: 'cmd-center', sortable: true },
                 { id: 'created', label: 'Ngày tạo meeting', width: 154, cellClass: 'cmd-center', sortable: true },
                 { id: 'type', label: 'Loại meeting', width: 178 },
                 { id: 'status', label: 'Trạng thái', width: 116 },
                 ...dims,
                 ...money,
             ]
         },
-        filteredRows() {
-            const keyword = this.keyword.trim().toLowerCase()
-
-            const rows = this.rows.filter((row) => {
-                for (const field of FILTER_FIELDS) {
-                    const picked = this.ownFilters[field.id]
-                    if (picked != null && String(field.valueOf(row)) !== String(picked)) return false
-                }
-
-                if (!keyword) return true
-                const haystack = `${row.name || ''} ${row.customer_name || ''} ${row.host_name || ''} ${row.demand_names || ''}`
-
-                return haystack.toLowerCase().indexOf(keyword) !== -1
-            })
-
-            const column = this.sort.column
-            const dir = this.sort.dir === 'desc' ? -1 : 1
-
-            return rows.slice().sort((a, b) => {
-                const va = this.sortValue(a, column)
-                const vb = this.sortValue(b, column)
-                let result = typeof va === 'string' ? va.localeCompare(vb, 'vi') : va - vb
-                if (!result) result = String(a.code || '').localeCompare(String(b.code || ''))
-
-                return result * dir
-            })
+        /**
+         * Adapter cột cho `V2BaseReportModal`: `columns()` ở trên khai khoá `id` + `width` số — vỏ
+         * cần khoá `key` (+ `id` giữ lại để `cellText()` trong slot dùng nguyên hàm cũ) + `width`
+         * dạng chuỗi `px`. Bỏ cột `stt`: vỏ tự vẽ cột STT + đánh số theo `start-index`, giữ lại sẽ
+         * ra 2 cột STT.
+         */
+        baseColumns() {
+            return this.columns
+                .filter((column) => column.id !== 'stt')
+                .map((column) => ({
+                    key: column.id,
+                    id: column.id,
+                    field: FIELD_MAP[column.id],
+                    label: column.label,
+                    width: column.width ? `${column.width}px` : undefined,
+                    sortable: column.sortable,
+                    cellClass: CELL_CLASS_MAP[column.cellClass] || column.cellClass,
+                }))
         },
     },
     watch: {
-        // Đóng/mở khối tổng hợp là đổi hẳn ngân sách chiều cao -> đo lại ngay
-        sumCollapsed() {
-            this.syncTableHeight()
-        },
-        // Số dải chip đổi (1 hay 2 cơ cấu) cũng làm khối tổng hợp cao/thấp khác nhau
-        'allocations.length'() {
-            this.syncTableHeight()
-        },
-        // Lọc còn 0 dòng thì thanh phân trang tự ẩn -> ngân sách chiều cao đổi theo
-        'filteredRows.length'() {
-            this.syncTableHeight()
-        },
-        // Lọc lại (ô lọc, ô tìm, chip) -> luôn về trang 1
-        keyword() {
-            this.page = 1
-        },
-        ownFilters: {
-            deep: true,
-            handler() {
-                this.page = 1
-            },
-        },
-        // Mở popup mới luôn reset trạng thái — không mang bộ lọc / mốc sắp xếp của popup trước sang
+        // Mở popup mới luôn reset trạng thái — không mang bộ lọc / mốc sắp xếp của popup trước sang.
+        // Vỏ (`V2BaseReportModal`) tự lo việc show/hide + trả kích thước về bình thường.
         visible(value) {
-            if (value) {
-                this.resetState()
-                this.$nextTick(() => {
-                    if (this.$refs.baseModal) this.$refs.baseModal.show()
-                    // Chờ popup dựng xong (b-modal render qua portal + có transition) rồi mới đo
-                    setTimeout(this.syncTableHeight, 350)
-                })
-            } else if (this.$refs.baseModal) {
-                this.$refs.baseModal.close()
-            }
+            if (value) this.resetState()
         },
         /*
          * Đổi node / chỉ tiêu mà popup ĐANG mở thì `visible` không đổi -> watcher trên không chạy và
          * popup giữ nguyên bộ lọc + khối tổng hợp của lần xem trước. Màn hiện tại chưa có lối đi đó
          * (bấm số nào cũng phải đóng popup trước), nhưng để hở thì thêm 1 lối vào là sai âm thầm.
          */
         nodeKey() {
             if (this.visible) this.resetState()
         },
         metric() {
             if (this.visible) this.resetState()
         },
     },
-    mounted() {
-        window.addEventListener('resize', this.syncTableHeight)
-    },
-    beforeDestroy() {
-        window.removeEventListener('resize', this.syncTableHeight)
-    },
     methods: {
+        emptyFilters() {
+            return { market: null, customer: null, dept: null, part: null, host: null, type: null, status: null }
+        },
         /** Trạng thái đầu của MỖI lần mở popup: chưa lọc, khối tổng hợp thu gọn, sắp theo mốc mặc định */
         resetState() {
-            this.resetFilters()
-            this.sumCollapsed = true
-            this.page = 1
-            this.sort = { column: this.isNewMetric ? 'cus_created' : 'date', dir: 'asc' }
+            // Dọn IM LẶNG (`resetFilterState()`), KHÔNG gọi `resetFilters()`: popup lọc client-side
+            // nên không có API để tải lại, nhưng vẫn giữ đúng quy ước "mở popup mới = dọn ngầm" của
+            // 2 popup dùng chung vỏ kia (tránh lẫn lộn nếu sau này popup có thêm phần lọc server).
+            this.resetFilterState()
+            this.summaryCollapsed = true
+            this.sort = { key: this.isNewMetric ? 'cus_created' : 'date', dir: 'asc' }
         },
-        /** Đổi số dòng/trang thì về trang 1 — giữ trang cũ sẽ nhảy tới chỗ khác hẳn */
-        onPageSizeChange(size) {
-            this.pageSize = Number(size)
+        /** Lọc CLIENT-SIDE: đổi ô lọc/tìm kiếm chỉ cần về trang 1, không có API để gọi lại. */
+        onFilterChange() {
             this.page = 1
         },
-        /**
-         * ĐO THẬT ngân sách chiều cao rồi đặt trần cho vùng cuộn của bảng, để trong popup luôn
-         * CHỈ CÓ 1 THANH CUỘN DỌC (bẫy mục 3b skill modal-popup).
-         *
-         * Không dùng hằng số `calc(70vh - Xpx)`: khối tổng hợp đóng/mở, số dải chip 1 hay 2, popup
-         * "KH mới" không có hộp KPI… mỗi trường hợp một chiều cao. Đo thật trước khi làm việc này
-         * đã thấy body tràn 9px lúc thu gọn và 21px lúc mở rộng.
-         *
-         * Mốc là `max-height` của body (70vh), KHÔNG phải chiều cao hiện tại của nó — lấy chiều cao
-         * hiện tại thì mỗi lần chạy bảng lại co thêm một ít.
-         */
-        syncTableHeight() {
-            /*
-             * `$nextTick` KHÔNG đủ: gọi từ watcher thì callback chạy TRƯỚC lượt vẽ lại, đo ra số của
-             * trạng thái CŨ (đo thật: bấm Thu gọn lại ra đúng trần của lúc đang mở). Phải chờ thêm
-             * 1 khung hình để DOM mới thực sự có mặt.
-             */
-            this.$nextTick(() => window.requestAnimationFrame(() => {
-                const body = document.querySelector('.cmd-drill-dialog .v2-modal-body')
-                if (!body) return
-
-                const wrap = body.querySelector('.v2-table-scroll')
-                const scroller = body.querySelector('.v2-table-scroll__body')
-                if (!wrap || !scroller) return
-
-                const style = getComputedStyle(body)
-                const limit = parseFloat(style.maxHeight) || body.clientHeight
-                let used = parseFloat(style.paddingTop) + parseFloat(style.paddingBottom)
-
-                Array.from(body.children).forEach((child) => {
-                    const box = getComputedStyle(child)
-                    const margin = parseFloat(box.marginTop) + parseFloat(box.marginBottom)
-
-                    // Riêng khối bảng: chỉ tính phần NGOÀI vùng cuộn (thanh cuộn ngang phía trên)
-                    used += child === wrap ? wrap.offsetHeight - scroller.offsetHeight + margin : child.offsetHeight + margin
-                })
-
-                const budget = Math.floor(limit - used)
-
-                /*
-                 * Chỗ còn lại quá hẹp (màn hình thấp + mở khối tổng hợp + có thanh phân trang) thì
-                 * KHÔNG ép trần cho bảng nữa mà trả `0` -> `V2BaseTableScroll` bỏ luôn `overflow-y`,
-                 * cả thân popup thành MỘT vùng cuộn duy nhất. Ép trần trong trường hợp này là đẻ ra
-                 * đúng cái lỗi 2 thanh cuộn lồng nhau (đo ở khổ 1280×720: chỉ còn 137px cho bảng).
-                 */
-                this.tableMaxHeight = budget >= MIN_TABLE_HEIGHT ? `${budget}px` : 0
-
-                // Đo 1 lượt vẫn có thể hụt (thanh phân trang xuống dòng ở màn hẹp, khối tổng hợp
-                // chưa xong layout…) -> đo lại, còn tràn bao nhiêu thì trừ tiếp bấy nhiêu.
-                // Đo thật ở khổ 1280×720: lượt đầu hụt 43px, đúng bằng phần tràn.
-                this.$nextTick(() => window.requestAnimationFrame(() => this.trimTableOverflow(2)))
-            }))
-        },
-        /** Vòng sửa của `syncTableHeight` — CHỈ thu hẹp, tối đa `remaining` lượt để không lặp vô hạn */
-        trimTableOverflow(remaining) {
-            if (remaining <= 0) return
-
-            const body = document.querySelector('.cmd-drill-dialog .v2-modal-body')
-            if (!body) return
-
-            const overflow = body.scrollHeight - body.clientHeight
-            const current = parseFloat(this.tableMaxHeight)
-            if (overflow <= 0 || !current) return
-
-            const budget = Math.floor(current - overflow)
-            this.tableMaxHeight = budget >= MIN_TABLE_HEIGHT ? `${budget}px` : 0
-            this.$nextTick(() => window.requestAnimationFrame(() => this.trimTableOverflow(remaining - 1)))
-        },
         /**
          * Tuỳ chọn của mỗi ô lọc lấy từ CHÍNH tập dòng đang xem (distinct), không gọi danh mục đầy
          * đủ: người dùng chỉ cần lọc sâu hơn trong tập này, hiện giá trị không có dòng nào là bẫy.
          */
         optionsOf(fieldId) {
             const field = FILTER_FIELDS.find((item) => item.id === fieldId)
             const seen = new Map()
 
             this.rows.forEach((row) => {
                 const id = field.valueOf(row)
                 const name = field.labelOf(row)
                 if (id == null || id === '' || !name) return
                 if (!seen.has(String(id))) seen.set(String(id), { id, name })
             })
 
             return Array.from(seen.values()).sort((a, b) => String(a.name).localeCompare(String(b.name), 'vi'))
         },
-        resetFilters() {
-            this.keyword = ''
-            Object.keys(this.ownFilters).forEach((key) => { this.ownFilters[key] = null })
-        },
-        /** Bấm chip = bật/tắt ô lọc của chính chiều đó (bấm lại chip đang bật thì bỏ lọc) */
+        /**
+         * Bấm chip = bật/tắt ô lọc của chính chiều đó (bấm lại chip đang bật thì bỏ lọc). Đây là
+         * mutate THẲNG vào `filters`, không đi qua `@change` của select -> phải tự gọi
+         * `onFilterChange()`, nếu không trang không về 1 khi lọc bằng chip.
+         */
         toggleChip(dim, id) {
-            this.ownFilters[dim] = String(this.ownFilters[dim]) === String(id) ? null : id
+            this.filters[dim] = String(this.filters[dim]) === String(id) ? null : id
+            this.onFilterChange()
         },
         /** Tỷ lệ — 1 chữ số thập phân, chuẩn số quốc tế của hệ thống (`14.3%`) */
         rate(part, total) {
             if (!total) return '—'
 
             return `${((part * 100) / total).toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`
         },
         /** Bề rộng thanh nền của ô KPI, đơn vị % — chặn trần 100 để không tràn khỏi hộp */
         share(part, total) {
             return total ? Math.min(100, Math.round((part * 100) / total)) : 0
         },
-        close() {
-            this.$refs.baseModal && this.$refs.baseModal.close()
-        },
         /**
          * Tham số cho bản in danh sách: node đang xem + chỉ tiêu + BỘ LỌC RIÊNG của popup.
          * Bộ lọc popup đổi về đúng tên tham số của màn chính (cùng chiều, popup chỉ lọc sâu hơn)
          * nên BE `getDrillRows()` dùng lại nguyên bộ lọc, không phải viết nhánh riêng.
          */
         printList() {
             const map = {
                 market: 'province_id',
                 customer: 'customer_id',
                 dept: 'department_id',
                 part: 'part_id',
                 host: 'employee_id',
                 type: 'meeting_type_id',
                 status: 'status',
             }
             const params = { key: this.nodeKey, metric: this.metric }
 
             Object.keys(map).forEach((key) => {
-                if (this.ownFilters[key] != null) params[map[key]] = this.ownFilters[key]
+                if (this.filters[key] != null) params[map[key]] = this.filters[key]
             })
 
             this.$emit('print', params)
         },
         isNewCustomer(row) {
             return this.newCustomerIds.indexOf(row.customer_id) !== -1
         },
         sortValue(row, column) {
             switch (column) {
                 case 'date':
@@ -752,32 +667,20 @@ export default {
                 case 'cus_created':
                     return row.created_at ? new Date(row.created_at).getTime() : 0
                 case 'dept':
                     return row.department_name || ''
                 case 'host':
                     return row.host_name || ''
                 default:
                     return 0
             }
         },
-        sortBy(column) {
-            this.sort = this.sort.column === column
-                ? { column, dir: this.sort.dir === 'asc' ? 'desc' : 'asc' }
-                : { column, dir: 'asc' }
-            // Sắp lại là đổi hẳn thứ tự -> trang 3 của thứ tự cũ không còn ý nghĩa
-            this.page = 1
-        },
-        sortClass(column) {
-            if (this.sort.column !== column) return ''
-
-            return this.sort.dir === 'desc' ? 'cmd-sort--desc' : 'cmd-sort--asc'
-        },
         cellText(row, column, index) {
             switch (column.id) {
                 case 'stt':
                     return index + 1
                 case 'customer':
                     return row.customer_name
                 case 'market':
                     return row.province_name
                 case 'dept':
                     return row.department_name
@@ -809,25 +712,26 @@ export default {
             return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}/${d.getFullYear()}`
         },
         dateTime(value) {
             if (!value) return '—'
             const d = new Date(value)
 
             return `${this.date(value)} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
         },
         /**
          * Xuất Excel danh sách đang xem — dựng file .xls dạng HTML table ngay ở FE vì đây là tập
-         * đã lọc/sắp trên màn, gọi lại server sẽ ra thứ tự khác.
+         * đã lọc/SẮP trên màn (`sortedRows`, không phải `filteredRows` — export phải khớp đúng thứ
+         * tự người dùng đang nhìn thấy), gọi lại server sẽ ra thứ tự khác.
          */
         exportExcel() {
             const head = this.columns.map((column) => `<th>${column.label}</th>`).join('')
-            const body = this.filteredRows
+            const body = this.sortedRows
                 .map((row, index) => {
                     const cells = this.columns
                         .map((column) => {
                             if (column.id === 'cancel') {
                                 const note = row.cancel_note ? ` — ${row.cancel_note}` : ''
 
                                 return `<td>${(row.cancel_reason_name || '')}${note}</td>`
                             }
 
                             return `<td>${this.cellText(row, column, index)}</td>`
@@ -845,67 +749,58 @@ export default {
             link.download = this.isNewMetric ? 'Danh-sach-khach-hang-moi.xls' : 'Chi-tiet-meeting.xls'
             document.body.appendChild(link)
             link.click()
             document.body.removeChild(link)
             setTimeout(() => URL.revokeObjectURL(link.href), 1000)
         },
     },
 }
 </script>
 
-<!-- KHÔNG scoped: `.cmd-drill-dialog` gắn vào `.modal-dialog` render RA NGOÀI cây component
-     (b-modal dùng portal) nên scoped attr không bao giờ khớp. -->
-<style lang="scss">
-.cmd-drill-dialog {
-    max-width: 1400px;
-    width: 96vw;
-}
-</style>
-
 <style lang="scss" scoped>
 $teal-dark: #0e7490;
 $text-muted: #6b7280;
 
-.cmd-drill-filters {
+.report-drill-filters {
     display: flex;
     align-items: center;
     flex-wrap: wrap;
     gap: 6px;
     margin-bottom: 6px;
 }
-.cmd-drill-search {
+.report-drill-search {
     width: 220px;
 }
-.cmd-drill-filter {
+.report-drill-filter {
     width: 168px;
 }
-.cmd-drill-count {
+.report-drill-count {
     margin-left: auto;
     font-size: 11.5px;
     color: $text-muted;
 }
 
 /* ---------- Khối tổng hợp trong popup (port từ mockup đã duyệt) ---------- */
 
 /* Dòng đầu: nhãn + nút thu gọn. Thu gọn thì BỎ luôn viền dưới, nếu không 2 gạch sát nhau */
-.cmd-sumhead {
+.report-drill-sumhead {
     display: flex;
     align-items: center;
     gap: 10px;
     padding: 0 0 6px;
     border-bottom: 1px solid #e3e8ef;
 }
-.cmd-sumhead--collapsed {
+.report-drill-sumhead--collapsed {
     padding-bottom: 3px;
     border-bottom: 0;
 }
-.cmd-sumhead__label {
+.report-drill-sumhead__label {
     font-size: 11px;
     font-weight: 800;
     letter-spacing: 0.3px;
     color: $text-muted;
 }
 
 /* Nút thu gọn: CÙNG khuôn với `.rsum-toggle` của khối tổng hợp màn chính */
 .rsum-toggle {
     margin-left: auto;
     display: inline-flex;
@@ -929,276 +824,230 @@ $text-muted: #6b7280;
     svg {
         width: 12px;
         height: 12px;
         transition: transform 0.15s ease;
     }
 }
 .rsum-toggle--collapsed svg {
     transform: rotate(-90deg);
 }
 
-.cmd-sumbox {
+.report-drill-sumbox {
     padding: 6px 0 7px;
     border-bottom: 1px solid #e3e8ef;
 }
-.cmd-sumbox__title {
+.report-drill-sumbox__title {
     margin: 0 0 5px;
     font-size: 11px;
     font-weight: 800;
     letter-spacing: 0.3px;
     color: #1f2937;
 }
 
 /* 3 hộp KPI — khuôn `.rsum-kpi` của mockup, thu nhỏ lại cho vừa popup */
-.cmd-kpis {
+.report-drill-kpis {
     display: grid;
     grid-template-columns: repeat(3, minmax(0, 1fr));
     gap: 8px;
 }
-.cmd-kpi {
+.report-drill-kpi {
     padding: 6px 10px 7px;
     border: 1px solid #e6edf3;
     border-left: 3px solid $teal-dark;
     border-radius: 6px;
     background: #fbfdfe;
 }
-.cmd-kpi--good {
+.report-drill-kpi--good {
     border-color: rgba(34, 197, 94, 0.3);
     border-left-color: #22c55e;
     background: linear-gradient(135deg, #f4fdf7, #fdfffe);
 }
-.cmd-kpi--bad {
+.report-drill-kpi--bad {
     border-color: rgba(245, 158, 11, 0.35);
     border-left-color: #f59e0b;
     background: linear-gradient(135deg, #fff9ee, #fffdf8);
 }
-.cmd-kpi__label {
+.report-drill-kpi__label {
     display: flex;
     align-items: center;
     gap: 4px;
     font-size: 10px;
     font-weight: 700;
     line-height: 1.3;
     color: $text-muted;
 }
-.cmd-kpi__value {
+.report-drill-kpi__value {
     display: flex;
     align-items: baseline;
     gap: 5px;
     font-size: 18px;
     font-weight: 800;
     line-height: 1.3;
     color: $teal-dark;
     font-variant-numeric: tabular-nums;
 
     em {
         font-style: normal;
         font-size: 10.5px;
         font-weight: 700;
         color: $text-muted;
     }
 }
-.cmd-kpi--good .cmd-kpi__value {
+.report-drill-kpi--good .report-drill-kpi__value {
     color: #15803d;
 }
-.cmd-kpi--bad .cmd-kpi__value {
+.report-drill-kpi--bad .report-drill-kpi__value {
     color: #b45309;
 }
-.cmd-kpi__track {
+.report-drill-kpi__track {
     display: block;
     height: 4px;
     margin-top: 2px;
     border-radius: 3px;
     background: #e8eef4;
     overflow: hidden;
 }
-.cmd-kpi__fill {
+.report-drill-kpi__fill {
     display: block;
     height: 100%;
     border-radius: 3px;
     background: $teal-dark;
 }
-.cmd-kpi--good .cmd-kpi__fill {
+.report-drill-kpi--good .report-drill-kpi__fill {
     background: #22c55e;
 }
-.cmd-kpi--bad .cmd-kpi__fill {
+.report-drill-kpi--bad .report-drill-kpi__fill {
     background: #f59e0b;
 }
 
 /* Dải chip: MỖI cơ cấu gói gọn 1 HÀNG, dài thì cuộn NGANG cả khối (không xuống dòng thành bãi chữ) */
-.cmd-sum {
+.report-drill-sum {
     display: flex;
     flex-direction: column;
     gap: 2px;
     overflow-x: auto;
     overflow-y: hidden;
     scrollbar-width: thin;
     scrollbar-color: #d7e0e8 transparent;
 
     &::-webkit-scrollbar {
         height: 4px;
     }
     &::-webkit-scrollbar-thumb {
         background: #d7e0e8;
         border-radius: 2px;
     }
     &::-webkit-scrollbar-track {
         background: transparent;
     }
 }
-.cmd-sum__grp {
+.report-drill-sum__grp {
     display: flex;
     align-items: baseline;
     gap: 8px;
     width: max-content;
     min-width: 100%;
 }
 /* Ghim nhãn khi cuộn ngang để luôn biết đang xem cơ cấu nào */
-.cmd-sum__label {
+.report-drill-sum__label {
     flex-shrink: 0;
     width: 84px;
     position: sticky;
     left: 0;
     z-index: 1;
     background: #fff;
     font-size: 10px;
     font-weight: 800;
     letter-spacing: 0.4px;
     text-transform: uppercase;
     color: $text-muted;
 }
-.cmd-sum__chips {
+.report-drill-sum__chips {
     display: flex;
     flex-wrap: nowrap;
     gap: 4px;
 }
-.cmd-sum__chip {
+.report-drill-sum__chip {
     display: inline-flex;
     align-items: baseline;
     flex-shrink: 0;
     gap: 5px;
     padding: 2px 7px;
     border: 1px solid transparent;
     border-radius: 5px;
     background: none;
     font: inherit;
     font-size: 11.5px;
     color: #1f2937;
     white-space: nowrap;
     cursor: pointer;
     transition: background 0.12s ease;
 
     &:hover {
         background: #eef6fa;
     }
 }
-.cmd-sum__chip--on {
+.report-drill-sum__chip--on {
     border-color: #06b6d4;
     background: #e2f5fa;
 }
 /* Tên để chữ THƯỜNG cho đỡ rối — điểm nhấn dồn vào con số */
-.cmd-sum__chip__name {
+.report-drill-sum__chip__name {
     font-weight: 400;
 }
-.cmd-sum__chip__n {
+.report-drill-sum__chip__n {
     font-weight: 800;
     color: $teal-dark;
     font-variant-numeric: tabular-nums;
 }
-.cmd-sum__chip__pct {
+.report-drill-sum__chip__pct {
     font-size: 10.5px;
     color: #94a3b8;
     font-variant-numeric: tabular-nums;
 }
 
-.cmd-drill-table {
-    width: 100%;
-    border-collapse: collapse;
-    font-size: 12px;
-    background: #fff;
-    table-layout: fixed;
-
-    th,
-    td {
-        border: 1px solid #e2e8f0;
-        padding: 4px 8px;
-        vertical-align: middle;
-        overflow-wrap: anywhere;
-    }
-
-    thead th {
-        position: sticky;
-        top: 0;
-        background: #eef7fa;
-        font-weight: 700;
-        white-space: nowrap;
-        z-index: 1;
-    }
-
-    tbody tr:hover td {
-        background: #ddf0f7;
-    }
-}
-
 /* Cột chữ dài: cắt 2 dòng + tooltip xem đủ, giữ dòng thấp cho thấy được nhiều bản ghi */
-.cmd-clamp {
+.report-drill-clamp {
     display: -webkit-box;
     -webkit-line-clamp: 2;
     -webkit-box-orient: vertical;
     overflow: hidden;
 }
 
-.cmd-sortable {
-    cursor: pointer;
-}
-.cmd-sort {
-    display: inline-flex;
-    flex-direction: column;
-    line-height: 6px;
-    margin-left: 2px;
-    opacity: 0.3;
-
-    i {
-        font-size: 11px;
-    }
-}
-.cmd-sort--asc,
-.cmd-sort--desc {
-    opacity: 1;
-}
-
-.cmd-center {
-    text-align: center;
-}
-.cmd-money {
-    text-align: right;
-    font-weight: 700;
-}
-.cmd-drill-empty {
-    text-align: center;
-    padding: 22px;
-    color: $text-muted;
-}
-
 /* Ô Lý do huỷ 2 dòng */
-.cmd-cancel__reason {
+.report-drill-cancel__reason {
     font-weight: 600;
 }
-.cmd-cancel__note {
+.report-drill-cancel__note {
     margin-top: 2px;
     font-size: 11px;
     line-height: 1.4;
     color: $text-muted;
 }
 
-.cmd-newchip {
+.report-drill-newchip {
     display: inline-flex;
     align-items: center;
     padding: 1px 7px 2px;
     border-radius: 999px;
     border: 1px solid rgba(34, 197, 94, 0.45);
     background: rgba(34, 197, 94, 0.1);
     color: #15803d;
     font-size: 10.5px;
     font-weight: 700;
 }
 </style>
+
+<!-- KHÔNG scoped: cột "Giá trị dự kiến (đ)" (`report-drill-table__money`, map từ `cmd-money` cũ qua
+     `CELL_CLASS_MAP`) được VỎ `V2BaseReportModal` render — nó lặp `columns` rồi gắn
+     `:class="col.cellClass"` vào `<td>` bằng TEMPLATE CỦA CHÍNH NÓ, xem
+     `components/report/V2BaseReportModal.vue`. Để rule này trong khối scoped ở trên thì nó lặng lẽ
+     KHÔNG áp dụng (`<td>` mang `data-v-xxx` của VỎ, không phải của file này). Cùng tên + cùng nội
+     dung với `.report-drill-table__money` của `DemandListModal.vue` (popup gốc) — trùng tên CSS
+     global 2 file không xung đột vì thuộc tính giống hệt nhau. -->
+<style>
+.report-drill-table__money {
+    text-align: right;
+    font-weight: 700;
+    font-variant-numeric: tabular-nums;
+}
+</style>
