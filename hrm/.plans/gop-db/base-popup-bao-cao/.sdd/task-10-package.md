# Review package: 81bdddd18..01a6fbb28

## Commits
01a6fbb28 refactor(tkt): chuyển ProjectListModal sang V2BaseReportModal (server-side, không mixin)

## Files changed
 .../components/ProjectListModal.vue                | 536 ++++++++++-----------
 1 file changed, 247 insertions(+), 289 deletions(-)

## Diff
diff --git a/pages/assign/report/prospective-project-results/components/ProjectListModal.vue b/pages/assign/report/prospective-project-results/components/ProjectListModal.vue
index 615ebfdd9..1cefb9b6a 100644
--- a/pages/assign/report/prospective-project-results/components/ProjectListModal.vue
+++ b/pages/assign/report/prospective-project-results/components/ProjectListModal.vue
@@ -1,20 +1,28 @@
 <!--
     Popup danh sách dự án — mở khi bấm bất kỳ con số nào trên dải tổng hợp / bảng theo dõi
     (Task 14). Cột do BE quyết (`columns`, khoá TRÙNG khoá row — xem
     `ProjectRowResource::COLUMN_LABELS`) — FE CHỈ map nhãn hiển thị, KHÔNG tự suy/bớt cột, để bảng
     popup / bản in / Excel (Task 15-16) dùng chung 1 nguồn.
 
-    Dựng trên `components/modal/V2BaseModal.vue` theo `.claude/skills/modal-popup/SKILL.md` mục 0
-    (khác khuôn `b-modal` tay của `potential-customer-care/components/DemandListModal.vue` — file
-    đó ghi chú V2BaseModal "không tồn tại trên nhánh này", nhưng nó ĐÃ có ở nhánh
-    `tpe-bao-cao-ket-qua-du-an-tkt` nên bám đúng skill, không copy khuôn `b-modal` tay).
+    Task 10 (base-popup-bao-cao) — chuyển vỏ sang `components/report/V2BaseReportModal.vue`
+    (KHÔNG gắn `utils/mixins/reportDrillListMixin.js`): popup này TỰ GỌI API (`fetchList()`), lọc /
+    sắp xếp / phân trang ĐỀU Ở BE — khác 2 popup còn lại (`DemandListModal.vue`,
+    `DevelopmentDrillModal.vue`) lọc/sắp CLIENT-SIDE trên mảng đã tải sẵn nên dùng được mixin. Vỏ chỉ
+    lo khung popup (banner, bảng + thanh cuộn, phân trang, nút phóng to, cuộn-về-đầu khi lật trang) —
+    dữ liệu, bộ lọc, khối tổng hợp, sắp xếp vẫn do CHÍNH component này quyết định rồi gọi lại
+    `fetchList()`.
+
+    ⚠️ Slot của vỏ có THỨ TỰ CỐ ĐỊNH: `#filters` -> `#back` -> `#summary` -> bảng. Bản trước (dựng
+    trên `V2BaseModal` tay) đặt khối tổng hợp (nút thu gọn + KPI + chip phân bổ) TRƯỚC hàng bộ lọc —
+    sang vỏ dùng chung thì thứ tự bị đảo (bộ lọc lên trước, khối tổng hợp xuống `#summary`), do vỏ
+    quy định cứng, không phải rơi rụng.
 
     Filter dùng CHUNG namespace với màn chính (department_id/part_id/employee_id/province_id/
     customer_id/scope_id/industry_id/status/result) — BẮT BUỘC gửi kèm `baseParams` (bộ lọc hiện
     tại của màn, `index.vue` truyền qua `buildParams()`) vì `getProjects()` ở BE dùng CHÍNH các
     tham số đó để dựng cả cây; popup chỉ THÊM `metric` + `drill_key`, KHÔNG thay thế. Ô lọc của
     popup khởi tạo bằng giá trị đang có trong `baseParams`, user đổi tại chỗ để lọc SÂU HƠN — không
     ảnh hưởng ngược lại màn chính (state cục bộ trong `ownFilters`).
 
     2 luật ẩn ô lọc (đọc theo brief "6 điều dễ làm sai nhất" mục 2):
       Luật 1: dim đã CÓ trong `payload.path` (= dim đã cố định trong `drill_key`) -> ẩn hẳn ô lọc
@@ -28,250 +36,232 @@
     cùng số liệu với ô đã bấm trên bảng theo dõi/dải tổng hợp (`metricsOf()` ở BE), do `index.vue`
     tự dò trong `tree`/`total` (đã có sẵn trong bộ nhớ, KHÔNG gọi thêm API) rồi truyền qua
     `payload.nodeMetrics` khi gọi `open()`.
 
     Chip phân bổ (Task 14b) LẤY TỪ khoá `allocation` do `project-list` trả kèm — tính trên tập ĐÃ
     áp `drill_key` + bộ lọc `metric` (ĐÚNG tập popup đang liệt kê), CHỈ trước phân trang (xem
     `allocationOf()`/`projectList()` ở BE). Ẩn theo CHÍNH `fieldVisibility` bên dưới (computed
     `allocationGroups`) — không viết luật ẩn thứ hai.
 -->
 <template>
-    <V2BaseModal
-        ref="baseModal"
+    <V2BaseReportModal
         modal-id="tkt-project-list-modal"
+        :visible="visible"
+        :loading="loading"
+        lead="Bạn đang xem:"
         :title="modalTitle"
-        subtitle-label="Thuộc"
-        :subtitle="ancestorText"
-        icon="ri-file-list-3-line"
-        size="xl"
-        dialog-class="tkt-drill-dialog"
-        max-body-height="80vh"
+        :meta="ancestorText"
+        :columns="columnDefs"
+        :rows="rows"
+        :start-index="startIndex"
+        :sort="modalSort"
+        :current-page="page"
+        :current-page-size="perPage"
+        :total-rows="total"
+        item-label="dự án"
+        :page-size-options="[20, 50, 100]"
+        empty-text="Không có dự án nào khớp bộ lọc."
+        @sort="onSort"
+        @page-change="onPageChange"
+        @page-size-change="onPageSizeChange"
+        @close="close"
     >
-        <div v-if="hasSummary" class="tkt-drill-sum-toggle">
-            <V2BaseButton tertiary size="xs" @click="summaryCollapsed = !summaryCollapsed">
-                <template #prefix><i class="ri-bar-chart-2-line" style="font-size: 12px"></i></template>
-                {{ summaryCollapsed ? 'Xem tổng hợp' : 'Thu gọn' }}
-            </V2BaseButton>
-        </div>
-
-        <!-- `hidden` (không phải style.display / v-show) — bẫy brief đã nhắc: v-show render ra
-             `style="display:none"` là chuẩn CSS, hoàn toàn hợp lệ, nhưng brief chốt riêng cho popup
-             này phải dùng thuộc tính `hidden` để không có logic ẩn nào khác đè lên bằng inline style. -->
-        <template v-if="hasSummary">
-            <div v-if="nodeMetrics" :hidden="summaryCollapsed" class="tkt-drill-sum">
-                <div class="tkt-drill-sum__item">
-                    <span>Tổng dự án</span><strong>{{ money(nodeMetrics.total) }}</strong>
-                </div>
-                <div class="tkt-drill-sum__item">
-                    <span>Đang triển khai</span><strong>{{ money(nodeMetrics.open) }}</strong>
-                </div>
-                <div class="tkt-drill-sum__item">
-                    <span>Đóng trong kỳ</span><strong>{{ money(nodeMetrics.closed) }}</strong>
-                </div>
-                <div class="tkt-drill-sum__item tkt-drill-sum__item--good">
-                    <span>Thành công</span><strong>{{ money(nodeMetrics.won) }}</strong>
-                </div>
-                <div class="tkt-drill-sum__item tkt-drill-sum__item--bad">
-                    <span>Thất bại</span><strong>{{ money(nodeMetrics.lost) }}</strong>
-                </div>
-                <div class="tkt-drill-sum__item">
-                    <span>Tỷ lệ thành công</span><strong>{{ rateText(nodeMetrics.success_rate) }}</strong>
+        <template #filters>
+            <div class="report-drill-filters">
+                <div v-for="field in visibleFields" :key="field.key" class="report-drill-filters__item">
+                    <V2BaseSelectRemote
+                        v-if="field.remote"
+                        v-model="ownFilters[field.key]"
+                        :fetch-fn="searchCustomers"
+                        :initial-option="selectedCustomerLocal"
+                        :minimum-input-length="2"
+                        :allow-clear="true"
+                        size="sm"
+                        :placeholder="field.placeholder"
+                        @select="onCustomerSelect"
+                    />
+                    <V2BaseSelectInModal
+                        v-else
+                        v-model="ownFilters[field.key]"
+                        :options="fieldOptions(field)"
+                        :allow-clear="true"
+                        size="sm"
+                        :placeholder="field.placeholder"
+                        @change="onFilterChange"
+                    />
                 </div>
+                <span class="report-drill-count">{{ loading ? 'Đang tải…' : `${total} dự án` }}</span>
             </div>
+        </template>
 
-            <!-- Chip phân bổ (Task 14b, design.md mục "Luật POPUP chi tiết" điểm 3): LUÔN Phòng
-                 ban + 2 chiều cơ cấu theo tiêu chí. Ẩn theo ĐÚNG `fieldVisibility` của ô lọc
-                 (`allocationGroups` bên dưới lọc lại bằng chính computed đó) — không viết luật ẩn
-                 thứ hai. Dải chip cuộn ngang trong 1 khối chung (khuôn CSKH `DemandListModal.vue`
-                 `.report-drill-sum` — tên CŨ là `.care-drill-sum`, đã đổi ở Task 3) khi nhiều mục —
-                 KHÔNG phải chip bị cắt. -->
-            <div v-if="allocationGroups.length" :hidden="summaryCollapsed" class="tkt-drill-chipbox">
-                <p class="tkt-drill-chipbox__title">Phân bổ theo cơ cấu</p>
-                <div class="tkt-drill-chips">
-                    <div v-for="group in allocationGroups" :key="group.dim" class="tkt-drill-chips__grp">
-                        <span class="tkt-drill-chips__label">{{ dimLabel(group.dim) }}</span>
-                        <div class="tkt-drill-chips__list">
-                            <span
-                                v-for="item in group.items"
-                                :key="`${group.dim}-${item.id}`"
-                                class="tkt-drill-chip"
-                            >
-                                {{ item.name }}
-                                <b class="tkt-drill-chip__n">{{ money(item.count) }}</b>
-                            </span>
+        <!--
+            Khối tổng hợp (nút thu gọn + KPI + chip phân bổ) — chuyển từ vị trí ĐẦU popup (bản dựng
+            tay trên V2BaseModal) sang slot `#summary` của vỏ, đứng SAU `#filters` (thứ tự do vỏ quy
+            định, xem ghi chú đầu file). `hidden` (không phải style.display / v-show) — bẫy đã nhắc:
+            v-show render ra `style="display:none"` là chuẩn CSS, hoàn toàn hợp lệ, nhưng popup này
+            chốt riêng phải dùng thuộc tính `hidden` để không có logic ẩn nào khác đè lên bằng inline
+            style.
+        -->
+        <template #summary>
+            <div v-if="hasSummary" class="report-drill-sum-toggle">
+                <V2BaseButton tertiary size="xs" @click="summaryCollapsed = !summaryCollapsed">
+                    <template #prefix><i class="ri-bar-chart-2-line" style="font-size: 12px"></i></template>
+                    {{ summaryCollapsed ? 'Xem tổng hợp' : 'Thu gọn' }}
+                </V2BaseButton>
+            </div>
+
+            <template v-if="hasSummary">
+                <div v-if="nodeMetrics" :hidden="summaryCollapsed" class="report-drill-sum">
+                    <div class="report-drill-sum__item">
+                        <span>Tổng dự án</span><strong>{{ money(nodeMetrics.total) }}</strong>
+                    </div>
+                    <div class="report-drill-sum__item">
+                        <span>Đang triển khai</span><strong>{{ money(nodeMetrics.open) }}</strong>
+                    </div>
+                    <div class="report-drill-sum__item">
+                        <span>Đóng trong kỳ</span><strong>{{ money(nodeMetrics.closed) }}</strong>
+                    </div>
+                    <div class="report-drill-sum__item report-drill-sum__item--good">
+                        <span>Thành công</span><strong>{{ money(nodeMetrics.won) }}</strong>
+                    </div>
+                    <div class="report-drill-sum__item report-drill-sum__item--bad">
+                        <span>Thất bại</span><strong>{{ money(nodeMetrics.lost) }}</strong>
+                    </div>
+                    <div class="report-drill-sum__item">
+                        <span>Tỷ lệ thành công</span><strong>{{ rateText(nodeMetrics.success_rate) }}</strong>
+                    </div>
+                </div>
+
+                <!-- Chip phân bổ (Task 14b) — dải chip cuộn ngang trong 1 khối chung (khuôn CSKH
+                     `DemandListModal.vue` `.report-drill-sum` — tên CŨ `.care-drill-sum`) khi nhiều
+                     mục, KHÔNG phải chip bị cắt. -->
+                <div v-if="allocationGroups.length" :hidden="summaryCollapsed" class="report-drill-chipbox">
+                    <p class="report-drill-chipbox__title">Phân bổ theo cơ cấu</p>
+                    <div class="report-drill-chips">
+                        <div v-for="group in allocationGroups" :key="group.dim" class="report-drill-chips__grp">
+                            <span class="report-drill-chips__label">{{ dimLabel(group.dim) }}</span>
+                            <div class="report-drill-chips__list">
+                                <span
+                                    v-for="item in group.items"
+                                    :key="`${group.dim}-${item.id}`"
+                                    class="report-drill-chip"
+                                >
+                                    {{ item.name }}
+                                    <b class="report-drill-chip__n">{{ money(item.count) }}</b>
+                                </span>
+                            </div>
                         </div>
                     </div>
                 </div>
-            </div>
+            </template>
         </template>
 
-        <div class="tkt-drill-filters">
-            <div v-for="field in visibleFields" :key="field.key" class="tkt-drill-filters__item">
-                <V2BaseSelectRemote
-                    v-if="field.remote"
-                    v-model="ownFilters[field.key]"
-                    :fetch-fn="searchCustomers"
-                    :initial-option="selectedCustomerLocal"
-                    :minimum-input-length="2"
-                    :allow-clear="true"
-                    size="sm"
-                    :placeholder="field.placeholder"
-                    @select="onCustomerSelect"
-                />
-                <V2BaseSelectInModal
-                    v-else
-                    v-model="ownFilters[field.key]"
-                    :options="fieldOptions(field)"
-                    :allow-clear="true"
-                    size="sm"
-                    :placeholder="field.placeholder"
-                    @change="onFilterChange"
-                />
-            </div>
-            <span class="tkt-drill-count">{{ loading ? 'Đang tải…' : `${total} dự án` }}</span>
-        </div>
-
-        <V2BaseTableScroll max-height="50vh">
-            <table class="tkt-drill-table">
-                <thead>
-                    <tr>
-                        <th class="tkt-center" style="width: 46px">STT</th>
-                        <th v-for="col in columnDefs" :key="col.key" :class="col.align">
-                            <span v-if="col.sortKey" class="tkt-sort" @click="toggleSort(col)">
-                                {{ col.label }}
-                                <span class="tkt-sort__arrows">
-                                    <i
-                                        class="ri-arrow-up-s-fill"
-                                        :class="{ 'tkt-sort__arrow--active': isSortActive(col, 'asc') }"
-                                    ></i>
-                                    <i
-                                        class="ri-arrow-down-s-fill"
-                                        :class="{ 'tkt-sort__arrow--active': isSortActive(col, 'desc') }"
-                                    ></i>
-                                </span>
-                            </span>
-                            <span v-else>{{ col.label }}</span>
-                        </th>
-                    </tr>
-                </thead>
-                <tbody>
-                    <tr v-for="(row, index) in rows" :key="row.id">
-                        <td class="tkt-center">{{ (page - 1) * perPage + index + 1 }}</td>
-                        <td v-for="col in columnDefs" :key="col.key" :class="col.align">
-                            <template v-if="col.key === 'name'">
-                                <!--
-                                    Thẻ `a` THẬT + href đầy đủ + target="_blank" (khuôn
-                                    `potential-customer-care/components/CustomerMeetingHistoryModal.vue`
-                                    — tên meeting mở tab mới): giữa/Ctrl+click/chuột phải "Mở ở tab
-                                    mới" đều ra đúng kết quả, KHÔNG dùng router.push đổi hẳn tab
-                                    hiện tại — user đang có bộ lọc + popup + vị trí cuộn, điều
-                                    hướng cùng tab là mất hết, quay lại phải lọc lại từ đầu.
-                                -->
-                                <a
-                                    :href="projectUrl(row.id)"
-                                    target="_blank"
-                                    rel="noopener"
-                                    class="tkt-project-link"
-                                    title="Xem chi tiết dự án ở tab mới"
-                                >{{ row.name }}</a>
-                                <span v-if="row.created_in_period" class="tkt-chip-new">Lập trong kỳ</span>
-                            </template>
-                            <template v-else-if="col.key === 'status_text'">
-                                <V2BaseBadge :color="row.status_color">{{ row.status_text }}</V2BaseBadge>
-                            </template>
-                            <template v-else-if="col.key === 'result_text'">
-                                <V2BaseBadge :color="row.result_color">{{ row.result_text }}</V2BaseBadge>
-                            </template>
-                            <template v-else-if="col.key === 'amount'">{{ moneyOrDash(row.amount) }}</template>
-                            <template v-else>{{ textOf(row, col.key) }}</template>
-                        </td>
-                    </tr>
-                    <tr v-if="!loading && !rows.length">
-                        <td :colspan="columnDefs.length + 1" class="tkt-drill-table__empty">
-                            Không có dự án nào khớp bộ lọc.
-                        </td>
-                    </tr>
-                    <tr v-if="loading">
-                        <td :colspan="columnDefs.length + 1" class="tkt-drill-table__empty">Đang tải…</td>
-                    </tr>
-                </tbody>
-            </table>
-        </V2BaseTableScroll>
-
-        <V2BasePagination
-            v-if="!loading"
-            class="tkt-drill-paging"
-            :current-page="page"
-            :current-page-size="perPage"
-            :total-rows="total"
-            item-label="dự án"
-            :page-size-options="[20, 50, 100]"
-            @page-change="onPageChange"
-            @page-size-change="onPageSizeChange"
-        />
+        <!--
+            Ô đặc biệt — 4 cột cần hiển thị khác nguyên văn `row[col.key]`: tên dự án (link + chip
+            "Lập trong kỳ"), 2 badge trạng thái/kết quả, giá trị tiền. Các cột còn lại vẫn đi qua
+            slot để giữ đúng hành vi cũ (dấu `—` khi rỗng — `textOf()`), vỏ chỉ tự render
+            `row[col.field]` NGUYÊN VĂN khi không có slot, không có fallback `—`.
+        -->
+        <template #cell-code="{ row }">{{ textOf(row, 'code') }}</template>
+        <template #cell-name="{ row }">
+            <!--
+                Thẻ `a` THẬT + href đầy đủ + target="_blank" (khuôn
+                `potential-customer-care/components/CustomerMeetingHistoryModal.vue` — tên meeting mở
+                tab mới): giữa/Ctrl+click/chuột phải "Mở ở tab mới" đều ra đúng kết quả, KHÔNG dùng
+                router.push đổi hẳn tab hiện tại — user đang có bộ lọc + popup + vị trí cuộn, điều
+                hướng cùng tab là mất hết, quay lại phải lọc lại từ đầu.
+            -->
+            <a
+                :href="projectUrl(row.id)"
+                target="_blank"
+                rel="noopener"
+                class="report-drill-project-link"
+                title="Xem chi tiết dự án ở tab mới"
+            >{{ row.name }}</a>
+            <span v-if="row.created_in_period" class="report-drill-chip-new">Lập trong kỳ</span>
+        </template>
+        <template #cell-created_at="{ row }">{{ textOf(row, 'created_at') }}</template>
+        <template #cell-status_text="{ row }"><V2BaseBadge :color="row.status_color">{{ row.status_text }}</V2BaseBadge></template>
+        <template #cell-dept_name="{ row }">{{ textOf(row, 'dept_name') }}</template>
+        <template #cell-part_name="{ row }">{{ textOf(row, 'part_name') }}</template>
+        <template #cell-emp_name="{ row }">{{ textOf(row, 'emp_name') }}</template>
+        <template #cell-province_name="{ row }">{{ textOf(row, 'province_name') }}</template>
+        <template #cell-scope_name="{ row }">{{ textOf(row, 'scope_name') }}</template>
+        <template #cell-industry_name="{ row }">{{ textOf(row, 'industry_name') }}</template>
+        <template #cell-customer_name="{ row }">{{ textOf(row, 'customer_name') }}</template>
+        <template #cell-result_text="{ row }"><V2BaseBadge :color="row.result_color">{{ row.result_text }}</V2BaseBadge></template>
+        <template #cell-closed_reason="{ row }">{{ textOf(row, 'closed_reason') }}</template>
+        <template #cell-amount="{ row }">{{ moneyOrDash(row.amount) }}</template>
 
         <!--
             Task 15 — 2 đầu ra của popup, BÁM ĐÚNG bộ lọc riêng (`ownFilters`) + thứ tự đang sắp
             (`sort`) của CHÍNH popup này (`buildExportParams()`), KHÔNG phải bộ lọc màn cha.
             Thứ tự + màu theo `.claude/skills/button-convention/SKILL.md` mục 2b + mục 5 (modal
-            footer: action phụ trước, Đóng luôn cuối) — khác khuôn `b-modal` tay của
-            `potential-customer-care/components/DemandListModal.vue` (Đóng đứng ĐẦU, Xuất Excel
-            tô `primary`): `V2BaseModal` đã có sẵn slot `#footer` nên bám đúng quy tắc chung, không
-            copy nguyên thứ tự/màu của màn mẫu đó.
+            footer: action phụ trước, Đóng luôn cuối).
         -->
         <template #footer>
             <V2BaseButton secondary size="sm" @click="printList">
                 <template #prefix><i class="ri-printer-line" style="font-size: 14px"></i></template>
                 In danh sách
             </V2BaseButton>
             <V2BaseButton secondary status="success" size="sm" @click="exportList">
                 <template #prefix><i class="ri-file-excel-2-line" style="font-size: 14px"></i></template>
                 Xuất Excel danh sách
             </V2BaseButton>
             <V2BaseButton tertiary size="sm" @click="close">
                 <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
                 Đóng
             </V2BaseButton>
         </template>
-    </V2BaseModal>
+    </V2BaseReportModal>
 </template>
 
 <script>
-import V2BaseModal from '@/components/modal/V2BaseModal.vue'
 import V2BaseButton from '@/components/V2BaseButton.vue'
 import V2BaseSelectInModal from '@/components/V2BaseSelectInModal.vue'
 import V2BaseSelectRemote from '@/components/V2BaseSelectRemote.vue'
 import V2BaseBadge from '@/components/V2BaseBadge.vue'
-import V2BaseTableScroll from '@/components/V2BaseTableScroll.vue'
-import V2BasePagination from '@/components/V2BasePagination.vue'
+import V2BaseReportModal from '@/components/report/V2BaseReportModal.vue'
 import { money, percent } from '../format'
 
 const API = 'assign/report/prospective-project-results'
 
-/** Nhãn cột — khoá TRÙNG khoá row của `ProjectRowResource::COLUMN_LABELS` (BE), không lệch nhau. */
+/** Nhãn cột — khoá TRÙNG khoá row của `ProjectRowResource::COLUMN_LABELS` (BE), không lệch nhau.
+    KHÔNG SỬA (chốt Task 10) — `align` dưới đây vẫn là khoá NỘI BỘ cũ, được `ALIGN_CLASS_MAP` map
+    sang `cellClass` của vỏ ở computed `columnDefs`, không đổi trực tiếp trong bảng này. */
 const COLUMN_DEFS = {
     code: { label: 'Mã dự án', align: '' },
     name: { label: 'Tên dự án TKT', align: '' },
     created_at: { label: 'Ngày lập dự án', align: 'tkt-center', sortKey: 'created_at' },
     status_text: { label: 'Tiến trình', align: 'tkt-center' },
     dept_name: { label: 'Phòng ban', align: '', sortKey: 'dept' },
     part_name: { label: 'Bộ phận', align: '' },
     emp_name: { label: 'Nhân viên phụ trách', align: '', sortKey: 'emp' },
     province_name: { label: 'Thị trường', align: '', sortKey: 'province' },
     scope_name: { label: 'Lĩnh vực', align: '', sortKey: 'scope' },
     industry_name: { label: 'Nhóm ngành', align: '' },
     customer_name: { label: 'Khách hàng', align: '' },
     result_text: { label: 'Kết quả', align: 'tkt-center', sortKey: 'result' },
     closed_reason: { label: 'Lý do thất bại', align: '' },
     amount: { label: 'Giá trị', align: 'tkt-right', sortKey: 'amount' },
 }
 
+/** `align` cũ (khoá nội bộ của `COLUMN_DEFS`, không đổi) -> `cellClass` của vỏ. `tkt-center` trỏ
+    thẳng vào `.report-drill-table__center` VỎ ĐÃ CÓ SẴN (khối KHÔNG scoped của
+    `V2BaseReportModal.vue`) — dùng lại, không định nghĩa trùng. `tkt-right` -> `.report-drill-table__money`
+    — cùng tên + cùng nội dung với lớp của `DevelopmentDrillModal.vue`/`DemandListModal.vue` (khuôn
+    adapter cột đã port ở 2 popup trước), định nghĩa KHÔNG scoped ở cuối file — xem comment ở đó. */
+const ALIGN_CLASS_MAP = {
+    'tkt-center': 'report-drill-table__center',
+    'tkt-right': 'report-drill-table__money',
+}
+
 const METRIC_LABELS = {
     total: 'Tổng dự án',
     open: 'Đang triển khai',
     closed: 'Đóng trong kỳ',
     won: 'Thành công',
     lost: 'Thất bại',
     created_before: 'Dự án lập trước kỳ',
     created_in: 'Dự án lập trong kỳ',
 }
 
@@ -326,42 +316,43 @@ const DIM_TO_FILTER_KEY = {
     part: 'part_id',
     emp: 'employee_id',
     province: 'province_id',
     scope: 'scope_id',
     industry: 'industry_id',
 }
 
 export default {
     name: 'ProjectListModal',
     components: {
-        V2BaseModal,
         V2BaseButton,
         V2BaseSelectInModal,
         V2BaseSelectRemote,
         V2BaseBadge,
-        V2BaseTableScroll,
-        V2BasePagination,
+        V2BaseReportModal,
     },
     props: {
         /** Bộ lọc hiện tại của màn chính (`index.vue` -> `buildParams()`): company_id, period,
             from, to, criteria + toàn bộ dimension filter đang có giá trị. */
         baseParams: { type: Object, default: () => ({}) },
         /** Danh mục dùng CHUNG với bộ lọc màn chính — KHÔNG gọi thêm API riêng cho popup. */
         options: { type: Object, default: () => ({}) },
         criteria: { type: String, default: 'dept' },
         /** Nhãn khách hàng đang chọn ở màn chính — mồi `initialOption` khi popup mở đúng khách đó. */
         selectedCustomer: { type: Object, default: null },
         /** Hàm tìm khách hàng — TÁI DÙNG `searchCustomers()` của `index.vue`, không viết lại. */
         searchCustomers: { type: Function, required: true },
     },
     data() {
         return {
+            /** Vỏ (`V2BaseReportModal`) điều khiển show/hide qua prop `visible` — component này TỰ
+                giữ trạng thái (không nhận từ cha, cha vẫn gọi `open()` qua `ref` như trước). */
+            visible: false,
             payload: { metric: 'total', drillKey: '', path: [] },
             /** Metrics của ĐÚNG node vừa bấm — do `index.vue` tự dò rồi truyền vào `open()`. */
             nodeMetrics: null,
             columns: [],
             rows: [],
             /** Chip phân bổ do BE trả kèm `project-list` — [{ dim, items: [{id, name, count}] }],
                 tính trên TOÀN BỘ dự án của node (không đổi khi lật trang). */
             allocation: [],
             total: 0,
             loading: false,
@@ -372,35 +363,58 @@ export default {
             /** Mặc định THU GỌN — đặt lại `true` mỗi lần `open()`, KHÔNG mang trạng thái cũ sang. */
             summaryCollapsed: true,
             ownFilters: this.seedFilters(),
             selectedCustomerLocal: null,
         }
     },
     computed: {
         modalTitle() {
             const metricLabel = METRIC_LABELS[this.payload.metric] || this.payload.metric
             const path = this.payload.path || []
-            if (!path.length) return `Đang xem ${metricLabel} — Tổng số dự án`
+            if (!path.length) return `${metricLabel} — Tổng số dự án`
             const last = path[path.length - 1]
-            return `Đang xem ${metricLabel} theo ${DIM_LABELS[last.dim] || last.dim}: ${last.name}`
+            return `${metricLabel} theo ${DIM_LABELS[last.dim] || last.dim}: ${last.name}`
         },
         /** Dòng phụ (đường dẫn cấp CHA, không lặp lại cấp đã nêu trong title) — chữ xám theo skill. */
         ancestorText() {
             const path = this.payload.path || []
             if (path.length <= 1) return ''
             return path
                 .slice(0, -1)
                 .map((p) => `${DIM_LABELS[p.dim] || p.dim}: ${p.name}`)
                 .join(' · ')
         },
+        /** Adapter cột cho `V2BaseReportModal`: BE trả mảng KHOÁ (`this.columns`), map qua
+            `COLUMN_DEFS` cục bộ như cũ rồi đổi shape sang `{ key, label, sortable, cellClass }` —
+            KHÔNG sửa `COLUMN_DEFS` lẫn dữ liệu BE trả về. */
         columnDefs() {
-            return (this.columns || []).map((key) => ({ key, ...(COLUMN_DEFS[key] || { label: key, align: '' }) }))
+            return (this.columns || []).map((key) => {
+                const def = COLUMN_DEFS[key] || { label: key, align: '' }
+                return {
+                    key,
+                    label: def.label,
+                    field: key,
+                    sortable: !!def.sortKey,
+                    sortKey: def.sortKey,
+                    cellClass: ALIGN_CLASS_MAP[def.align],
+                }
+            })
+        },
+        /** `this.sort` giữ khoá BE (vd `emp`, `dept`) để gửi `buildListParams()` — vỏ so khớp cột
+            đang sắp bằng `col.key` (vd `emp_name`), KHÁC khoá BE, nên phải quy đổi riêng cho prop
+            `sort` truyền xuống vỏ (chỉ ảnh hưởng icon mũi tên hiển thị, không đụng state thật). */
+        modalSort() {
+            const col = this.columnDefs.find((c) => c.sortKey === this.sort.key)
+            return { key: col ? col.key : this.sort.key, dir: this.sort.dir }
+        },
+        startIndex() {
+            return (this.page - 1) * this.perPage
         },
         /** Luật 1: dim đã cố định trong `drill_key` (đọc qua `payload.path`, TRÙNG dims của key). */
         fixedDims() {
             return new Set((this.payload.path || []).map((p) => p.dim))
         },
         effectiveDepartmentId() {
             const fixed = this.fixedValueOf('dept')
             return fixed !== null ? fixed : this.ownFilters.department_id
         },
         effectiveScopeId() {
@@ -514,21 +528,21 @@ export default {
             this.allocation = []
             this.sort = { key: 'created_at', dir: 'desc' }
             this.page = 1
             this.perPage = 20
             this.summaryCollapsed = true
             this.ownFilters = this.seedFilters()
             this.selectedCustomerLocal =
                 this.selectedCustomer && String(this.selectedCustomer.id) === String(this.ownFilters.customer_id)
                     ? this.selectedCustomer
                     : null
-            this.$refs.baseModal.show()
+            this.visible = true
             this.fetchList()
         },
         /** `/assign/prospective-projects/{id}` — mở tab mới khi bấm tên dự án (Fix round 1). */
         projectUrl(id) {
             return `/assign/prospective-projects/${id}`
         },
         buildListParams() {
             const params = { ...this.baseParams }
             DIM_FILTER_KEYS.concat(['customer_id', 'status', 'result']).forEach((key) => {
                 params[key] = this.fieldVisibility[key] ? this.ownFilters[key] : null
@@ -539,20 +553,27 @@ export default {
             params.sort_dir = this.sort.dir
             params.page = this.page
             params.per_page = this.perPage
             Object.keys(params).forEach((key) => {
                 if (params[key] === null || params[key] === undefined || params[key] === '') delete params[key]
             })
             return params
         },
         async fetchList() {
             this.loading = true
+            /* Vỏ (`V2BaseReportModal`) chỉ hiện "Đang tải…" khi `rows.length === 0` (không có ô
+               loading phủ riêng như bản dựng tay cũ, vốn LUÔN chèn thêm 1 dòng "Đang tải…" bên
+               dưới dữ liệu cũ dù bảng đang có dữ liệu). Popup này gọi lại API ở MỌI lần đổi trang/
+               sắp xếp/lọc (không giống 2 popup lọc client-side kia) — phải dọn `rows` trước khi gọi
+               để vỏ hiện đúng trạng thái đang tải, tránh giữ dữ liệu CŨ hiển thị mà không có tín
+               hiệu nào cho biết đang tải trang MỚI. */
+            this.rows = []
             try {
                 const res = await this.$store.dispatch('apiGetMethod', {
                     url: `${API}/project-list`,
                     params: this.buildListParams(),
                 })
                 this.columns = (res.data && res.data.columns) || []
                 this.rows = (res.data && res.data.rows) || []
                 this.allocation = (res.data && res.data.allocation) || []
                 this.total = (res.data && res.data.total) || 0
             } catch (e) {
@@ -566,44 +587,45 @@ export default {
         },
         onFilterChange() {
             this.page = 1
             this.fetchList()
         },
         onCustomerSelect(option) {
             this.ownFilters.customer_id = option && option.id ? option.id : null
             this.selectedCustomerLocal = option && option.id ? { id: option.id, text: option.text } : null
             this.onFilterChange()
         },
-        toggleSort(col) {
-            if (!col.sortKey) return
+        /** `@sort` của vỏ chỉ gửi `col.key` (vd `emp_name`) — quy về `sortKey` BE (vd `emp`) qua
+            `columnDefs` rồi nối vào CHÍNH cơ chế sắp xếp BE sẵn có (gọi lại `fetchList()`), KHÔNG
+            dùng máy sắp xếp client-side của mixin. */
+        onSort({ key }) {
+            const col = this.columnDefs.find((c) => c.key === key)
+            if (!col || !col.sortKey) return
             this.sort =
                 this.sort.key === col.sortKey
                     ? { key: col.sortKey, dir: this.sort.dir === 'asc' ? 'desc' : 'asc' }
                     : { key: col.sortKey, dir: 'asc' }
             this.page = 1
             this.fetchList()
         },
-        isSortActive(col, dir) {
-            return this.sort.key === col.sortKey && this.sort.dir === dir
-        },
         onPageChange(page) {
             this.page = page
             this.fetchList()
         },
         onPageSizeChange(size) {
             this.perPage = size
             this.page = 1
             this.fetchList()
         },
 
         close() {
-            this.$refs.baseModal.close()
+            this.visible = false
         },
 
         /**
          * Task 15 — params dùng CHUNG cho In + Xuất Excel của popup: y hệt `buildListParams()`
          * (bộ lọc riêng `ownFilters` đã áp luật ẩn + `sort`/`sort_dir` ĐANG SẮP trong popup) nhưng
          * bỏ `page`/`per_page` — BE dùng `projectListAll()` (KHÔNG phân trang) cho cả 2 endpoint
          * `print-list-data` (mode=detail) và `project-list/export`, giữ 2 khoá đó không sai gì
          * nhưng thừa, xoá cho params sạch.
          */
         buildExportParams() {
@@ -620,92 +642,83 @@ export default {
         },
 
         /** Nút "Xuất Excel danh sách" — cha chỉ gọi thẳng endpoint tải file. */
         exportList() {
             this.$emit('export', this.buildExportParams())
         },
     },
 }
 </script>
 
-<!-- KHÔNG scoped: `.tkt-drill-dialog` gắn vào `.modal-dialog` render RA NGOÀI cây component
-     (b-modal dùng portal/teleport), scoped attr sẽ không bao giờ khớp. -->
-<style lang="scss">
-.tkt-drill-dialog {
-    max-width: 1200px;
-    width: 95vw;
-}
-</style>
-
 <style lang="scss" scoped>
 $text-main: #1f2937;
 $text-muted: #6b7280;
 $teal-dark: #0e7490;
 
-.tkt-drill-sum-toggle {
+.report-drill-sum-toggle {
     display: flex;
     justify-content: flex-end;
     margin-bottom: 6px;
 }
 
-.tkt-drill-sum {
+.report-drill-sum {
     display: flex;
     flex-wrap: wrap;
     gap: 8px;
     margin-bottom: 10px;
     padding-bottom: 10px;
     border-bottom: 1px dashed #e2e8f0;
 }
-.tkt-drill-sum__item {
+.report-drill-sum__item {
     flex: 1 1 140px;
     padding: 6px 10px;
     border: 1px solid #e6edf3;
     border-radius: 6px;
     background: #f8fafc;
 
     span {
         display: block;
         font-size: 10.5px;
         font-weight: 700;
         color: $text-muted;
     }
     strong {
         font-size: 14px;
         font-weight: 800;
         color: $text-main;
         font-variant-numeric: tabular-nums;
     }
 }
-.tkt-drill-sum__item--good strong {
+.report-drill-sum__item--good strong {
     color: #16a34a;
 }
-.tkt-drill-sum__item--bad strong {
+.report-drill-sum__item--bad strong {
     color: #dc2626;
 }
 
 /* Chip phân bổ (Task 14b) — khuôn cuộn ngang port từ CSKH `DemandListModal.vue` `.report-drill-sum`
-   (tên CŨ là `.care-drill-sum`, đã đổi ở Task 3) — 1 thanh cuộn mảnh DÙNG CHUNG cho mọi hàng, không
-   phải mỗi hàng 1 thanh riêng. */
-.tkt-drill-chipbox {
+   (tên CŨ là `.care-drill-sum`) — 1 thanh cuộn mảnh DÙNG CHUNG cho mọi hàng, không phải mỗi hàng
+   1 thanh riêng. */
+.report-drill-chipbox {
     flex-shrink: 0;
     margin: 0 0 10px;
     padding: 0 0 8px;
     border-bottom: 1px dashed #e2e8f0;
 }
-.tkt-drill-chipbox__title {
+.report-drill-chipbox__title {
     margin: 0 0 5px;
     font-size: 11px;
     font-weight: 800;
     letter-spacing: 0.3px;
     color: $text-main;
 }
-.tkt-drill-chips {
+.report-drill-chips {
     display: flex;
     flex-direction: column;
     gap: 2px;
     margin: 0;
     padding: 0;
     overflow-x: auto;
     overflow-y: hidden;
     scrollbar-width: thin;
     scrollbar-color: #d7e0e8 transparent;
 
@@ -717,174 +730,119 @@ $teal-dark: #0e7490;
         border-radius: 2px;
 
         &:hover {
             background: #b8c6d4;
         }
     }
     &::-webkit-scrollbar-track {
         background: transparent;
     }
 }
-.tkt-drill-chips__grp {
+.report-drill-chips__grp {
     display: flex;
     align-items: baseline;
     gap: 8px;
     width: max-content;
     min-width: 100%;
 }
-.tkt-drill-chips__label {
+.report-drill-chips__label {
     flex-shrink: 0;
     width: 96px;
     font-size: 10px;
     font-weight: 800;
     letter-spacing: 0.4px;
     text-transform: uppercase;
     color: $text-muted;
     /* Ghim nhãn khi cuộn ngang để luôn biết đang xem cơ cấu nào */
     position: sticky;
     left: 0;
     z-index: 1;
     background: #fff;
 }
 /* KHÔNG xuống dòng: 1 cơ cấu = 1 hàng, dài thì cuộn ngang cả khối */
-.tkt-drill-chips__list {
+.report-drill-chips__list {
     display: flex;
     flex-wrap: nowrap;
     gap: 2px;
 }
-.tkt-drill-chip {
+.report-drill-chip {
     flex-shrink: 0;
     white-space: nowrap;
     display: inline-flex;
     align-items: baseline;
     gap: 5px;
     padding: 2px 7px;
     border: 1px solid #e6edf3;
     border-radius: 5px;
     background: #f8fafc;
     font-size: 11.5px;
     color: $text-main;
 }
-.tkt-drill-chip__n {
+.report-drill-chip__n {
     font-weight: 800;
     color: $teal-dark;
     font-variant-numeric: tabular-nums;
 }
 
-.tkt-drill-filters {
+.report-drill-filters {
     display: flex;
     flex-wrap: wrap;
     align-items: center;
     gap: 8px;
     margin-bottom: 10px;
 }
-.tkt-drill-filters__item {
+.report-drill-filters__item {
     flex: 0 0 auto;
     width: 190px;
 }
-.tkt-drill-count {
+.report-drill-count {
     margin-left: auto;
     font-size: 11.5px;
     font-weight: 700;
     color: $text-muted;
 }
 
-.tkt-drill-table {
-    width: 100%;
-    table-layout: auto;
-    border-collapse: collapse;
-    font-size: 12.5px;
-    background: #fff;
-
-    th,
-    td {
-        padding: 7px 9px;
-        border: 1px solid #e2eaf1;
-        vertical-align: middle;
-        white-space: nowrap;
-    }
-
-    thead th {
-        position: sticky;
-        top: 0;
-        z-index: 3;
-        background: linear-gradient(180deg, #f3fdfe, #e2f6f9);
-        border-bottom: 2px solid #20d9ea;
-        color: #0a7c88;
-        font-size: 11.5px;
-        font-weight: 700;
-        text-align: left;
-        white-space: nowrap;
-    }
-
-    tbody tr:hover td {
-        background: #d9eff7;
-    }
-}
-.tkt-center {
-    text-align: center;
-}
-.tkt-right {
-    text-align: right;
-    font-variant-numeric: tabular-nums;
-}
-.tkt-drill-table__empty {
-    text-align: center;
-    color: $text-muted;
-    padding: 22px;
-    white-space: normal;
-}
-
-/* Sort: 2 mũi tên ngược chiều, mặc định cả 2 mờ — chiều đang áp mới tô đậm */
-.tkt-sort {
-    display: inline-flex;
-    align-items: center;
-    cursor: pointer;
-    user-select: none;
-}
-.tkt-sort__arrows {
-    display: inline-flex;
-    flex-direction: column;
-    margin-left: 4px;
-    line-height: 0.6;
-}
-.tkt-sort__arrows i {
-    font-size: 12px;
-    opacity: 0.3;
-    color: #64748b;
-}
-.tkt-sort__arrow--active {
-    opacity: 1 !important;
-    color: $teal-dark !important;
-}
-
 /* Tên dự án — link mở tab mới (Fix round 1). Màu teal chủ đạo của bảng, TUYỆT ĐỐI không
-   `.text-muted`/đỏ — đỏ chỉ dành cho lỗi validate. */
-.tkt-project-link {
+   `.text-muted`/đỏ — đỏ chỉ dành cho lỗi validate. Slot content nên scoped CSS của POPUP với tới
+   bình thường (khác `cellClass`, xem comment cuối file). */
+.report-drill-project-link {
     color: $teal-dark;
     cursor: pointer;
 
     &:hover {
         color: #0a5c73;
         text-decoration: underline;
     }
 }
 
 /* Chip "Lập trong kỳ" — SẮC LAM, khác hẳn badge Thành công (xanh lá) để không lẫn */
-.tkt-chip-new {
+.report-drill-chip-new {
     display: inline-block;
     margin-left: 6px;
     padding: 0 6px;
     border: 1px solid rgba(37, 99, 235, 0.35);
     border-radius: 3px;
     background: rgba(37, 99, 235, 0.08);
     color: #1d4ed8;
     font-size: 10px;
     font-weight: 700;
     line-height: 16px;
     white-space: nowrap;
 }
+</style>
 
-.tkt-drill-paging {
-    margin-top: 4px;
+<!-- KHÔNG scoped: `.report-drill-table__money` gắn vào ô `amount` qua `cellClass` (adapter
+     `columnDefs` ở trên) — `<td>` mang class đó do VỎ (`V2BaseReportModal.vue`) render bằng
+     TEMPLATE CỦA CHÍNH NÓ (`:class="col.cellClass"`), không phải slot content của popup này, nên
+     scoped attr của popup KHÔNG với tới (bài học đã trả giá — xem ghi chú đầu file). Cùng tên +
+     cùng nội dung với `.report-drill-table__money` của `DevelopmentDrillModal.vue`/`DemandListModal.vue`
+     (2 popup trước) — trùng tên CSS global nhưng không xung đột vì thuộc tính giống hệt nhau, cho 3
+     popup báo cáo 1 khuôn "ô tiền" thống nhất. `.report-drill-table__center` (dùng cho created_at/
+     status_text/result_text) KHÔNG cần định nghĩa lại ở đây — vỏ đã có sẵn trong khối KHÔNG scoped
+     của chính nó. -->
+<style>
+.report-drill-table__money {
+    text-align: right;
+    font-weight: 700;
+    font-variant-numeric: tabular-nums;
 }
 </style>
