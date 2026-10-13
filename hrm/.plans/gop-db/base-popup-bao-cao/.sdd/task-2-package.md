# Review package: dc57d23b1..7faef7daf

## Commits
7faef7daf feat(V2BaseModal): thêm slot header + prop noEnforceFocus cho popup báo cáo

## Files changed
 components/modal/V2BaseModal.vue | 77 ++++++++++++++++++++++------------------
 1 file changed, 43 insertions(+), 34 deletions(-)

## Diff
diff --git a/components/modal/V2BaseModal.vue b/components/modal/V2BaseModal.vue
index e81eae003..5c1dcdaba 100644
--- a/components/modal/V2BaseModal.vue
+++ b/components/modal/V2BaseModal.vue
@@ -8,65 +8,71 @@
            + nút ×.
         2. Thân: vùng cuộn RIÊNG, padding sát `0.5rem` (khuôn popup "Chọn trường xuất CSV") — không
            để popup thừa khoảng trắng như các popup dựng tay trước đây.
         3. Footer: nằm NGOÀI vùng cuộn + `position: sticky` → nội dung dài mấy vẫn thấy nút.
     -->
     <b-modal
         :id="modalId"
         ref="modal"
         :size="size"
         :dialog-class="dialogClass"
+        :no-enforce-focus="noEnforceFocus"
         hide-footer
         content-class="shadow"
         body-class="v2-modal-wrap"
         @show="$emit('show')"
         @shown="$emit('shown')"
         @hide="$emit('hide', $event)"
         @hidden="$emit('hidden')"
     >
         <template #modal-header>
-            <!--
-                KHÔNG dùng `w-100` ở đây: `.modal-header` là flex row chứa khối này + nút ×; khối
-                rộng đúng 100% thì nút × không còn chỗ và bị ĐẨY RA NGOÀI mép popup (đo thật: tràn
-                26px khi dòng mô tả dài). Dùng `flex: 1 1 auto` + `min-width: 0` để khối chiếm hết
-                phần còn lại NHƯNG vẫn co được, nhờ đó `text-overflow: ellipsis` bên trong mới ăn.
-            -->
-            <div class="d-flex align-items-center v2-modal-head-left">
-                <div class="v2-modal-icon mr-2" :style="{ background: iconBackground, color: iconColor }">
-                    <i :class="icon" style="font-size: 16px"></i>
-                </div>
-                <div class="v2-modal-heading">
-                    <h5 class="modal-title mb-0" style="font-size: 14px; font-weight: 800">{{ title }}</h5>
-                    <!--
-                        Dòng mô tả bản ghi: `Khách hàng: 19TPHPVI-262 - NGUYỄN HỮU HỌC`.
-                        Chữ xám nhạt, phần giá trị đậm hơn một chút nhưng KHÔNG in đậm và
-                        TUYỆT ĐỐI không dùng màu đỏ (đỏ chỉ dành cho lỗi validate — CLAUDE.md).
-                    -->
-                    <!--
-                        Dòng mô tả CHỈ 1 DÒNG, dài quá thì cắt bằng "…" — tên bản ghi (tên thiết bị,
-                        tên hàng hóa) hay dài 2-3 dòng, để nguyên thì khối tiêu đề cao gần bằng nửa
-                        popup. Rê chuột vào hiện `title` gốc đầy đủ (Redmine #11164).
-                    -->
-                    <div
-                        v-if="subtitle"
-                        class="mt-1 v2-modal-subtitle"
-                        :title="subtitleFullText"
-                        style="font-size: 11px; color: #6b7280"
-                    >
-                        <template v-if="subtitleLabel">{{ subtitleLabel }}: </template>
-                        <span style="color: #374151">{{ subtitle }}</span>
+            <!-- Popup báo cáo thay header chuẩn bằng dải banner riêng (xem
+                 `components/report/V2BaseReportModal.vue`). Không truyền slot thì render y như cũ
+                 — 30 popup đang dùng không đổi gì. Slot tự vẽ nút đóng nên nhận luôn `close`. -->
+            <slot name="header" :close="close">
+                <!--
+                    KHÔNG dùng `w-100` ở đây: `.modal-header` là flex row chứa khối này + nút ×; khối
+                    rộng đúng 100% thì nút × không còn chỗ và bị ĐẨY RA NGOÀI mép popup (đo thật: tràn
+                    26px khi dòng mô tả dài). Dùng `flex: 1 1 auto` + `min-width: 0` để khối chiếm hết
+                    phần còn lại NHƯNG vẫn co được, nhờ đó `text-overflow: ellipsis` bên trong mới ăn.
+                -->
+                <div class="d-flex align-items-center v2-modal-head-left">
+                    <div class="v2-modal-icon mr-2" :style="{ background: iconBackground, color: iconColor }">
+                        <i :class="icon" style="font-size: 16px"></i>
+                    </div>
+                    <div class="v2-modal-heading">
+                        <h5 class="modal-title mb-0" style="font-size: 14px; font-weight: 800">{{ title }}</h5>
+                        <!--
+                            Dòng mô tả bản ghi: `Khách hàng: 19TPHPVI-262 - NGUYỄN HỮU HỌC`.
+                            Chữ xám nhạt, phần giá trị đậm hơn một chút nhưng KHÔNG in đậm và
+                            TUYỆT ĐỐI không dùng màu đỏ (đỏ chỉ dành cho lỗi validate — CLAUDE.md).
+                        -->
+                        <!--
+                            Dòng mô tả CHỈ 1 DÒNG, dài quá thì cắt bằng "…" — tên bản ghi (tên thiết bị,
+                            tên hàng hóa) hay dài 2-3 dòng, để nguyên thì khối tiêu đề cao gần bằng nửa
+                            popup. Rê chuột vào hiện `title` gốc đầy đủ (Redmine #11164).
+                        -->
+                        <div
+                            v-if="subtitle"
+                            class="mt-1 v2-modal-subtitle"
+                            :title="subtitleFullText"
+                            style="font-size: 11px; color: #6b7280"
+                        >
+                            <template v-if="subtitleLabel">{{ subtitleLabel }}: </template>
+                            <span style="color: #374151">{{ subtitle }}</span>
+                        </div>
                     </div>
                 </div>
-            </div>
-            <button type="button" class="close" @click="close">
-                <span aria-hidden="true">&times;</span>
-            </button>
+                <button type="button" class="close" @click="close">
+                    <span aria-hidden="true">&times;</span>
+                </button>
+            </slot>
         </template>
 
         <!-- CHỈ khối này cuộn. Đừng đặt lại class `modal-body` cho nội dung bên trong: nó kế thừa
              overflow + padding của bootstrap và sinh ra 2 thanh cuộn lồng nhau. -->
         <div class="v2-modal-body" :style="bodyStyle">
             <slot></slot>
         </div>
 
         <div class="modal-footer v2-modal-footer">
             <slot name="footer">
@@ -92,20 +98,23 @@ export default {
         subtitle: { type: String, default: '' },
         /** Nhãn đứng trước dòng mô tả: "Khách hàng", "Vụ việc"… */
         subtitleLabel: { type: String, default: '' },
         icon: { type: String, default: 'ri-file-list-3-line' },
         iconColor: { type: String, default: '#1abc9c' },
         iconBackground: { type: String, default: 'rgba(26, 188, 156, 0.1)' },
         size: { type: String, default: 'lg' },
         dialogClass: { type: String, default: '' },
         /** Chiều cao tối đa vùng cuộn; popup có bảng dài thì nới thêm. */
         maxBodyHeight: { type: String, default: 'calc(100vh - 220px)' },
+        /* Popup có select2/datepicker render dropdown ra ngoài `<body>`: BootstrapVue giành lại
+           focus sẽ đóng dropdown ngay khi vừa mở. Mặc định `false` — 30 popup đang dùng giữ nguyên. */
+        noEnforceFocus: { type: Boolean, default: false },
     },
     computed: {
         /** Nội dung tooltip của dòng mô tả — ghép cả nhãn để rê chuột đọc được trọn câu. */
         subtitleFullText() {
             return this.subtitleLabel ? `${this.subtitleLabel}: ${this.subtitle}` : this.subtitle
         },
         bodyStyle() {
             return { maxHeight: this.maxBodyHeight }
         },
     },
