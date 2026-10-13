# Review package — Task 7 (FE màn danh mục tiện nghi)

## git status (worktree client)
 M components/modal/V2BaseModal.vue
?? pages/meeting/room-amenities/
?? pages/meeting/rooms/

## diff component dùng chung (đã được user duyệt giữ lại)
diff --git a/components/modal/V2BaseModal.vue b/components/modal/V2BaseModal.vue
index 5c1dcdaba..dd1f3f5f5 100644
--- a/components/modal/V2BaseModal.vue
+++ b/components/modal/V2BaseModal.vue
@@ -125,6 +125,14 @@ export default {
         close() {
             this.$bvModal.hide(this.modalId)
         },
+        // Alias của close() — `utils/mixins/unsavedModalMixin.js` gọi `this.$refs[ref].hide()`
+        // sau khi user xác nhận "Thoát" (khuôn cũ dùng <b-modal ref="modal"> nên có sẵn .hide()
+        // gốc của BootstrapVue). V2BaseModal bọc b-modal nên thiếu method này — bổ sung thêm (không
+        // đổi hành vi show()/close() hiện có) để modal MỚI dựng trên V2BaseModal dùng được mixin
+        // cảnh báo "chưa lưu" theo đúng quy định CLAUDE.md, không phải tự viết beforeRouteLeave riêng.
+        hide() {
+            this.close()
+        },
     },
 }
 </script>

### pages/meeting/room-amenities/index.vue
```vue
<template>
    <div class="v2-styles min-vh-100 d-flex justify-content-center pt-2">
        <div class="container-fluid">
            <!-- FILTER PANEL -->
            <V2BaseFilterPanel
                title="Bộ lọc danh sách tiện nghi phòng họp"
                subtitle="Bạn có thể chọn tìm kiếm nâng cao để lọc nhiều thông tin hơn"
                :collapsed="filterCollapsed"
                :quickSearchValue="filters.keyword"
                quickSearchPlaceholder="Tìm theo mã, tên tiện nghi"
                :filters="filters"
                @toggle-panel="toggleFilterPanel"
                @quick-search-change="handleQuickSearchChange"
                @search="handleSearch"
                @reset="handleReset"
            >
                <template #advanced-filters="{ collapsed: slotCollapsed }">
                    <div v-show="!slotCollapsed" class="advanced-filters">
                        <div class="form-row">
                            <div class="col-md-4 mb-2">
                                <V2BaseLabel>Trạng thái</V2BaseLabel>
                                <V2BaseSelect
                                    v-model="filters.status"
                                    :options="statusOptions"
                                    :allowClear="true"
                                    placeholder="Chọn trạng thái"
                                />
                            </div>
                        </div>
                    </div>
                </template>
            </V2BaseFilterPanel>

            <!-- DATA TABLE -->
            <V2BaseDataTable
                :data="tableData"
                :columns="tableColumns"
                :pagination="pagination"
                :loading="loading"
                :title="title"
                rowKey="id"
                itemLabel="tiện nghi"
                emptyText="Không có dữ liệu phù hợp bộ lọc."
                @page-change="handlePageChange"
                @page-size-change="handlePageSizeChange"
            >
                <template #actions>
                    <V2BaseButton v-if="canManage" primary size="sm" class="mb-2" @click="createItem">
                        <template #prefix>
                            <i class="ri-add-line" style="font-size: 13px"></i>
                        </template>
                        Tạo mới
                    </V2BaseButton>
                </template>

                <!-- Custom code column -->
                <template #cell-code="{ item }">
                    <span class="field-line">{{ item.code }}</span>
                </template>

                <!-- Custom name column -->
                <template #cell-name="{ item }">
                    <V2BaseTitleSubInfo :title="item.name" titleClass="field-line" :titleBold="false">
                    </V2BaseTitleSubInfo>
                </template>

                <!-- Custom icon column -->
                <template #cell-icon="{ item }">
                    <div v-if="item.icon" class="room-amenity-icon-cell">
                        <i :class="item.icon"></i>
                    </div>
                    <span v-else style="color: #6b7280">—</span>
                </template>

                <!-- Custom sort_order column -->
                <template #cell-sort_order="{ item }">
                    {{ Number(item.sort_order || 0).toLocaleString('en-US') }}
                </template>

                <!-- Custom status column -->
                <template #cell-status="{ item }">
                    <div class="d-flex align-items-center" style="gap: 10px">
                        <V2BaseBadge :variant="item.status == 2 ? 'required' : 'brand'">
                            {{ item.status == 2 ? 'Khóa' : 'Hoạt động' }}
                        </V2BaseBadge>
                        <V2BaseIconButton
                            v-if="canManage && (item.status == 2 || item.is_can_lock)"
                            size="sm"
                            :title="item.status == 2 ? 'Mở khóa tiện nghi' : 'Khóa tiện nghi'"
                            @click="() => confirmToggleLock(item)"
                        >
                            <i :class="item.status == 2 ? 'ri-lock-unlock-line' : 'ri-lock-line'"></i>
                        </V2BaseIconButton>
                    </div>
                </template>

                <!-- Custom updated column -->
                <template #cell-updated_by_name="{ item }">
                    <V2BaseTitleSubInfo
                        :title="item.updated_by_name || '—'"
                        titleClass="field-line"
                        :titleBold="false"
                        :subs="item.updated_at ? [item.updated_at] : []"
                    ></V2BaseTitleSubInfo>
                </template>

                <!-- Custom actions column -->
                <template #cell-actions="{ item }">
                    <div class="d-flex align-items-center" style="gap: 8px">
                        <V2BaseIconButton size="sm" title="Xem" @click="() => viewItem(item)">
                            <i class="ri-eye-line"></i>
                        </V2BaseIconButton>
                        <V2BaseIconButton
                            v-if="canManage && item.is_can_edit"
                            size="sm"
                            title="Sửa"
                            @click="() => editItem(item)"
                        >
                            <i class="ri-edit-line"></i>
                        </V2BaseIconButton>
                        <V2BaseIconButton
                            v-if="canManage && item.is_can_delete"
                            size="sm"
                            danger
                            title="Xóa"
                            @click="() => confirmDeleteItem(item)"
                        >
                            <i class="ri-delete-bin-6-line"></i>
                        </V2BaseIconButton>
                    </div>
                </template>
            </V2BaseDataTable>
        </div>

        <!-- Xác nhận xóa — thao tác phá huỷ dữ liệu nên bật `danger` (nút đỏ + icon cảnh báo) -->
        <BaseConfirmModal
            id="confirm-delete-room-amenity"
            title="Xác nhận xóa"
            :message="deleteConfirmMessage"
            text-close="Hủy"
            text-accept="Xóa"
            danger
            accept-icon="ri-delete-bin-line"
            @event="handleConfirmDeleteItem"
        />

        <!-- Xác nhận khóa / mở khóa — Khóa là thao tác hạn chế (danger), Mở khóa là khôi phục -->
        <BaseConfirmModal
            id="confirm-toggle-lock-room-amenity"
            :title="lockConfirmTitle"
            :message="lockConfirmMessage"
            text-close="Hủy"
            :text-accept="lockConfirmAction"
            :danger="isLockAction"
            :accept-icon="isLockAction ? 'ri-lock-line' : 'ri-lock-unlock-line'"
            @event="handleConfirmToggleLock"
        />

        <!-- Room Amenity Modal -->
        <RoomAmenityModal
            ref="roomAmenityModal"
            :id="selectedItem ? selectedItem.id : null"
            :isShow="isShow"
            @event="eventHandler"
            @closeModal="handleCloseModal"
        />
    </div>
</template>
<script>
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseIconButton from '@/components/V2BaseIconButton.vue'
import V2BaseFilterPanel from '@/components/V2BaseFilterPanel.vue'
import V2BaseDataTable from '@/components/V2BaseDataTable.vue'
import V2BaseLabel from '@/components/V2BaseLabel.vue'
import V2BaseSelect from '@/components/V2BaseSelect.vue'
import V2BaseTitleSubInfo from '@/components/V2BaseTitleSubInfo.vue'
import V2BaseBadge from '@/components/V2BaseBadge.vue'
import BaseConfirmModal from '@/components/modal/base-confirm-modal.vue'
import RoomAmenityModal from '@/pages/meeting/room-amenities/components/RoomAmenityModal.vue'
import { buildQueryString } from '@/utils/url-action'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'

const initialStateForm = {
    page: 1,
    per_page: 10,
    keyword: '',
    status: '',
}

export default {
    layout: 'default-sidebar',
    mixins: [PageTitleMixin],
    head() {
        return {
            title: `${this.title}`,
        }
    },
    components: {
        V2BaseButton,
        V2BaseIconButton,
        V2BaseFilterPanel,
        V2BaseDataTable,
        V2BaseLabel,
        V2BaseSelect,
        V2BaseTitleSubInfo,
        V2BaseBadge,
        BaseConfirmModal,
        RoomAmenityModal,
    },
    data() {
        return {
            loading: false,
            title: 'Danh mục tiện nghi phòng họp',
            tableData: [],
            pagination: {
                currentPage: 1,
                pageSize: 10,
                total: 0,
                totalPages: 1,
                from: 0,
                to: 0,
            },

            filterCollapsed: true,
            filters: { ...initialStateForm },

            // Items for actions
            itemToDelete: null,
            itemToLock: null,
            selectedItem: null,
            isShow: false,

            // Filter watching
            ignoredFields: ['keyword'],
            oldFilters: {},

            // Permission — fail-closed: mặc định false, chỉ bật từ $store.state.permissions.
            canManage: false,
            canView: false,

            // Status options
            statusOptions: [
                { id: 1, name: 'Hoạt động' },
                { id: 2, name: 'Khóa' },
            ],
        }
    },
    computed: {
        pageTitle() {
            return 'Danh mục tiện nghi phòng họp'
        },
        tableColumns() {
            return [
                {
                    key: 'code',
                    title: 'Mã',
                    width: '140px',
                    minWidth: '120px',
                    align: 'left',
                },
                {
                    key: 'name',
                    title: 'Tên tiện nghi',
                    maxWidth: '400px',
                    cellClass: 'text-wrap',
                    align: 'left',
                },
                {
                    key: 'icon',
                    title: 'Icon',
                    width: '80px',
                    align: 'center',
                },
                {
                    key: 'sort_order',
                    title: 'Thứ tự',
                    width: '100px',
                    align: 'center',
                },
                {
                    key: 'status',
                    title: 'Trạng thái',
                    align: 'left',
                },
                {
                    key: 'updated_by_name',
                    title: 'Người cập nhật',
                    align: 'left',
                },
                {
                    key: 'actions',
                    title: 'Hành động',
                    align: 'center',
                },
            ]
        },

        deleteConfirmMessage() {
            if (!this.itemToDelete) return ''
            return `Bạn có chắc muốn xóa tiện nghi phòng họp '${this.itemToDelete.name}'?`
        },

        lockConfirmTitle() {
            if (!this.itemToLock) return ''
            return this.itemToLock.status == 2 ? 'Xác nhận mở khóa' : 'Xác nhận khóa'
        },

        lockConfirmMessage() {
            if (!this.itemToLock) return ''
            const action = this.itemToLock.status == 2 ? 'mở khóa' : 'khóa'
            return `Bạn có chắc muốn ${action} tiện nghi phòng họp '${this.itemToLock.name}'?`
        },

        lockConfirmAction() {
            if (!this.itemToLock) return ''
            return this.itemToLock.status == 2 ? 'Mở khóa' : 'Khóa'
        },

        /** Đang KHÓA (hạn chế) -> nút đỏ; Mở khóa là khôi phục -> không tô đỏ */
        isLockAction() {
            return !!this.itemToLock && this.itemToLock.status != 2
        },
    },
    async mounted() {
        // Cờ quyền fail-closed: khởi tạo false ở data(), chỉ bật từ $store.state.permissions —
        // TUYỆT ĐỐI không gán literal true (CLAUDE.md, lỗ hổng fail-open).
        // ⚠️ state.permissions là mảng OBJECT { id, name, ... } (API user-profile trả nguyên
        // Eloquent collection Permission), KHÔNG phải mảng string — .includes('<tên quyền>') luôn
        // false. Phải so theo p.name, đúng khuôn `utils/mixins/CheckPermission.js::hasAPermission()`.
        const perms = this.$store.state.permissions || []
        this.canManage = perms.some((p) => p.name === 'Quản lý danh mục tiện nghi phòng họp')
        this.canView = this.canManage || perms.some((p) => p.name === 'Xem danh mục tiện nghi phòng họp')

        await this.loadData()

        if (this.$route.query.message) {
            this.$toasted.global.success({
                message: this.$route.query.message,
            })
        }
    },
    watch: {
        filters: {
            handler(newVal) {
                const shouldCallApi = !this.ignoredFields.some((field) => newVal[field] !== this.oldFilters[field])

                if (shouldCallApi) {
                    this.loadData()
                }

                this.oldFilters = JSON.parse(JSON.stringify(this.filters))
            },
            deep: true,
        },
    },
    methods: {
        // Data loading
        async loadData() {
            try {
                this.loading = true

                this.filters.page = this.pagination.currentPage
                this.filters.per_page = this.pagination.pageSize

                const { data, meta } = await this.$store.dispatch(
                    'apiGetMethod',
                    `meeting/room-amenities${buildQueryString(this.filters)}`
                )

                this.tableData = data
                this.pagination.currentPage = meta.current_page
                this.pagination.pageSize = meta.per_page
                this.pagination.total = meta.total
                this.pagination.totalPages = meta.last_page
                this.pagination.from = meta.from
                this.pagination.to = meta.to
            } catch (error) {
                console.error('Error loading data:', error)
                if (error?.response?.status !== 403) {
                    this.$toasted?.global?.error?.({ message: 'Lỗi khi tải dữ liệu' })
                }
            } finally {
                this.loading = false
            }
        },

        // Filter handlers
        toggleFilterPanel() {
            this.filterCollapsed = !this.filterCollapsed
        },

        handleQuickSearchChange(value) {
            this.filters.keyword = value
        },

        async handleSearch() {
            this.pagination.currentPage = 1
            this.filters.page = 1
            this.oldFilters = JSON.parse(JSON.stringify(this.filters))
            await this.loadData()
        },

        async handleReset() {
            this.filters = { ...initialStateForm }
            this.pagination.currentPage = 1
            this.oldFilters = JSON.parse(JSON.stringify(this.filters))
            await this.loadData()
        },

        async handlePageChange(page) {
            this.pagination.currentPage = page
            this.filters.page = page
            await this.loadData()
        },

        async handlePageSizeChange(pageSize) {
            this.pagination.pageSize = pageSize
            this.filters.per_page = pageSize
            this.pagination.currentPage = 1
            this.filters.page = 1
            await this.loadData()
        },

        // CRUD operations
        createItem() {
            this.selectedItem = null
            this.isShow = false
            this.$refs.roomAmenityModal?.resetModal()
            this.$bvModal.show('modal-room-amenity')
        },

        async viewItem(item) {
            this.selectedItem = item
            this.isShow = true
            let loadOk = true
            if (item?.id) {
                loadOk = await this.$refs.roomAmenityModal?.loadData(item.id)
            }
            if (loadOk !== false) {
                this.$bvModal.show('modal-room-amenity')
            }
        },

        async editItem(item) {
            this.selectedItem = item
            this.isShow = false
            let loadOk = true
            if (item?.id) {
                loadOk = await this.$refs.roomAmenityModal?.loadData(item.id)
            }
            if (loadOk !== false) {
                this.$bvModal.show('modal-room-amenity')
            }
        },

        async toggleLock(item) {
            try {
                const action = item.status == 1 ? 'lock' : 'unlock'
                await this.$store.dispatch('apiGet', `meeting/room-amenities/${item.id}/${action}`)
                const actionText = action === 'lock' ? 'Khóa' : 'Mở khóa'
                this.$toasted?.global?.success?.({
                    message: `${actionText} thành công`,
                })
                await this.loadData()
            } catch (error) {
                console.error('Error toggling lock:', error)
                const status = Number(error?.response?.status)
                if (status === 403) return

                const errorMessage =
                    status === 404
                        ? 'Dữ liệu đã thay đổi, vui lòng tải lại'
                        : error?.response?.data?.message || 'Lỗi khi thay đổi trạng thái khóa'
                this.$toasted?.global?.error?.({ message: errorMessage })
            }
        },

        async deleteItem(item) {
            try {
                await this.$store.dispatch('apiDelete', `meeting/room-amenities/${item.id}`)
                this.$toasted?.global?.success?.({ message: 'Xóa thành công' })
                await this.loadData()
            } catch (error) {
                console.error('Error deleting item:', error)
                const status = Number(error?.response?.status)
                if (status === 403) return

                const errorMessage =
                    status === 404
                        ? 'Dữ liệu đã thay đổi, vui lòng tải lại'
                        : error?.response?.data?.message || 'Xóa thất bại'
                this.$toasted?.global?.error?.({ message: errorMessage })
            }
        },

        // Confirm modals
        confirmDeleteItem(item) {
            this.itemToDelete = item
            this.$bvModal.show('confirm-delete-room-amenity')
        },

        async handleConfirmDeleteItem() {
            if (!this.itemToDelete) return

            await this.deleteItem(this.itemToDelete)
            this.itemToDelete = null
        },

        confirmToggleLock(item) {
            this.itemToLock = item
            this.$bvModal.show('confirm-toggle-lock-room-amenity')
        },

        async handleConfirmToggleLock() {
            if (!this.itemToLock) return

            await this.toggleLock(this.itemToLock)
            this.itemToLock = null
        },

        // Event handler for modal
        async eventHandler() {
            this.selectedItem = null
            this.isShow = false
            await this.loadData()
        },

        handleCloseModal() {
            this.selectedItem = null
            this.isShow = false
            this.$bvModal.hide('modal-room-amenity')
        },
    },
}
</script>
<style lang="scss">
@import '@/assets/scss/v2-styles.scss';

.room-amenity-icon-cell {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 6px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    color: #1abc9c;
    font-size: 14px;
}
</style>
```

### pages/meeting/room-amenities/components/RoomAmenityModal.vue
```vue
<template>
    <!--
        Plan quan-ly-phong-hop, Task 7 — popup Thêm / Sửa / Xem tiện nghi phòng họp.
        Dựng trên V2BaseModal (khuôn popup dùng chung) — khuôn copy từ
        `components/modal/meeting-cancel-reason-modal.vue`, thêm 2 ô Mã + Icon/Thứ tự, bỏ ô
        Trạng thái (trạng thái đổi qua nút Khóa/Mở khóa ở màn danh sách, không sửa trong modal).
    -->
    <V2BaseModal
        ref="modal"
        modal-id="modal-room-amenity"
        :title="modalTitle"
        icon="ri-list-check-2"
        size="lg"
        @show="onModalShow"
        @shown="onUnsavedModalShown"
        @hide="onUnsavedModalHide"
        @hidden="onHidden"
    >
        <div class="form-row">
            <div class="col-md-4 mb-3">
                <V2BaseLabel required>Mã tiện nghi</V2BaseLabel>
                <V2BaseInput
                    v-model="data.code"
                    placeholder="VD: WIFI, PROJECTOR"
                    size="sm"
                    maxlength="50"
                    :disabled="isShow"
                    :invalid="!!error.code"
                />
                <V2BaseError v-if="error.code" :message="error.code" size="sm" class="mb-0 mt-1" />
            </div>

            <div class="col-md-8 mb-3">
                <V2BaseLabel required>Tên tiện nghi</V2BaseLabel>
                <V2BaseInput
                    v-model="data.name"
                    placeholder="VD: Wifi / Máy chiếu / Điều hòa / ..."
                    size="sm"
                    maxlength="255"
                    :disabled="isShow"
                    :invalid="!!error.name"
                />
                <V2BaseError v-if="error.name" :message="error.name" size="sm" class="mb-0 mt-1" />
            </div>
        </div>

        <div class="form-row">
            <div class="col-md-8 mb-1">
                <V2BaseLabel>Icon</V2BaseLabel>
                <div class="d-flex align-items-center" style="gap: 8px">
                    <div class="room-amenity-icon-preview">
                        <i :class="data.icon || 'ri-question-line'"></i>
                    </div>
                    <div style="flex: 1 1 auto; min-width: 0">
                        <V2BaseSelectInModal
                            v-model="data.icon"
                            :options="iconOptions"
                            placeholder="Chọn icon"
                            size="sm"
                            :disabled="isShow"
                            :allowClear="true"
                        />
                    </div>
                </div>
                <V2BaseError v-if="error.icon" :message="error.icon" size="sm" class="mb-0 mt-1" />
            </div>

            <div class="col-md-4 mb-1">
                <V2BaseLabel>Thứ tự</V2BaseLabel>
                <V2BaseInput
                    v-model="data.sort_order"
                    type="number"
                    min="0"
                    placeholder="0"
                    size="sm"
                    :disabled="isShow"
                    :invalid="!!error.sort_order"
                />
                <V2BaseError v-if="error.sort_order" :message="error.sort_order" size="sm" class="mb-0 mt-1" />
            </div>
        </div>

        <V2BaseError v-if="formError" :message="formError" size="sm" class="mb-0 mt-2" />

        <template #footer>
            <V2BaseButton v-if="!isShow" primary size="sm" :interactable="!isSubmitSave" @click="submitSave(false)">
                <template #prefix><i class="ri-save-3-line" style="font-size: 15px"></i></template>
                Lưu
            </V2BaseButton>
            <V2BaseButton
                v-if="!id && !isShow"
                secondary
                size="sm"
                :interactable="!isSubmitSave"
                @click="submitSave(true)"
            >
                <template #prefix><i class="ri-save-3-line" style="font-size: 15px"></i></template>
                Lưu và tiếp tục
            </V2BaseButton>
            <V2BaseButton tertiary size="sm" @click="closeModal">
                <template #prefix><i class="fas fa-arrow-left" style="margin-right: 3px"></i></template>
                Đóng
            </V2BaseButton>
        </template>
    </V2BaseModal>
</template>

<script>
import V2BaseModal from '@/components/modal/V2BaseModal.vue'
import V2BaseInput from '@/components/V2BaseInput.vue'
import V2BaseLabel from '@/components/V2BaseLabel.vue'
import V2BaseSelectInModal from '@/components/V2BaseSelectInModal.vue'
import V2BaseError from '@/components/V2BaseError.vue'
import V2BaseButton from '@/components/V2BaseButton.vue'
import unsavedModalMixin from '@/utils/mixins/unsavedModalMixin'

const emptyData = () => ({
    code: '',
    name: '',
    icon: '',
    sort_order: 0,
})

export default {
    components: {
        V2BaseModal,
        V2BaseInput,
        V2BaseLabel,
        V2BaseSelectInModal,
        V2BaseError,
        V2BaseButton,
    },
    mixins: [unsavedModalMixin],
    props: {
        id: { type: Number, default: null },
        isShow: { type: Boolean, default: false },
    },
    data() {
        return {
            data: emptyData(),
            error: {},
            formError: '',
            isSubmitSave: false,
            // Danh sách icon cố định (Remix Icon có sẵn trong hrm-client) — chưa có màn nào ở
            // project làm icon-picker nên tự chọn bộ icon phổ biến cho tiện nghi phòng họp.
            iconOptions: [
                { id: 'ri-wifi-line', name: 'Wifi' },
                { id: 'ri-tv-2-line', name: 'Màn hình / TV' },
                { id: 'ri-projector-line', name: 'Máy chiếu' },
                { id: 'ri-mic-line', name: 'Micro' },
                { id: 'ri-speaker-line', name: 'Loa' },
                { id: 'ri-volume-up-line', name: 'Âm thanh' },
                { id: 'ri-temp-cold-line', name: 'Điều hòa' },
                { id: 'ri-lightbulb-line', name: 'Đèn chiếu sáng' },
                { id: 'ri-printer-line', name: 'Máy in' },
                { id: 'ri-computer-line', name: 'Máy tính' },
                { id: 'ri-webcam-line', name: 'Webcam' },
                { id: 'ri-phone-line', name: 'Điện thoại hội nghị' },
                { id: 'ri-cup-line', name: 'Nước uống' },
                { id: 'ri-plug-line', name: 'Ổ cắm điện' },
                { id: 'ri-camera-line', name: 'Camera an ninh' },
                { id: 'ri-table-line', name: 'Bàn họp' },
                { id: 'ri-wheelchair-line', name: 'Hỗ trợ người khuyết tật' },
            ],
        }
    },
    computed: {
        modalTitle() {
            if (this.isShow) return 'Xem tiện nghi phòng họp'
            return this.id ? 'Sửa tiện nghi phòng họp' : 'Thêm tiện nghi phòng họp'
        },
    },
    watch: {
        id: {
            handler(newId) {
                if (!newId) {
                    this.data = emptyData()
                    this.error = {}
                    this.formError = ''
                }
            },
            immediate: false,
        },
    },
    methods: {
        // Cảnh báo "chưa lưu" (utils/mixins/unsavedModalMixin.js) theo dõi this.data,
        // modal ref="modal" khớp mặc định unsavedModalRef() nhưng vẫn khai rõ cho dễ đọc.
        unsavedSnapshotSource() {
            return this.data
        },
        unsavedModalRef() {
            return 'modal'
        },

        onModalShow() {
            if (!this.id) {
                this.resetLocalData()
            }
        },

        resetLocalData() {
            this.data = emptyData()
            this.error = {}
            this.formError = ''
        },

        resetModal() {
            this.error = {}
            this.formError = ''
            if (!this.id) {
                this.resetLocalData()
            }
        },

        async loadData(id) {
            try {
                const response = await this.$store.dispatch('apiGet', `meeting/room-amenities/${id}`)
                const detail = response.data.data
                this.data = {
                    code: detail.code || '',
                    name: detail.name || '',
                    icon: detail.icon || '',
                    sort_order: detail.sort_order ?? 0,
                }
                // Modal show() gọi TRƯỚC khi load xong -> @shown đã chốt mốc trên form rỗng.
                // Chốt lại ở đây để dữ liệu detail vừa nạp không bị tính nhầm là user vừa sửa.
                this.$nextTick(() => this.markFormPristine())
                return true
            } catch (error) {
                console.error('Error loading data:', error)
                const status = Number(error?.response?.status)
                let errorMessage = 'Lỗi khi tải dữ liệu'

                if (status === 403) return false
                if (status === 404) errorMessage = 'Dữ liệu đã thay đổi, vui lòng tải lại'
                else if (error?.response?.data?.message) errorMessage = error.response.data.message

                this.$toasted?.global?.error?.({ message: errorMessage })
                return false
            }
        },

        closeModal() {
            this.$refs.modal?.close()
        },

        /** V2BaseModal phát `hidden` sau khi popup đóng hẳn — dọn state ở đây, không cần setTimeout */
        onHidden() {
            this.resetLocalData()
            this.$emit('closeModal')
        },

        async submitSave(continueAfterSave = false) {
            if (this.isSubmitSave) return
            this.isSubmitSave = true
            this.error = {}
            this.formError = ''

            try {
                const payload = {
                    code: (this.data.code || '').trim(),
                    name: (this.data.name || '').trim(),
                    icon: this.data.icon || '',
                    sort_order:
                        this.data.sort_order === '' || this.data.sort_order === null
                            ? 0
                            : Number(this.data.sort_order),
                }
                if (this.id) payload.id = this.id

                await this.$store.dispatch('apiPostMethod', { url: 'meeting/room-amenities', payload })

                const message = this.id ? 'Cập nhật thành công' : 'Thêm mới thành công'
                this.$toasted?.global?.success?.({ message })
                this.markFormSaved()
                this.$emit('event')

                if (continueAfterSave) {
                    this.resetModal()
                    this.$nextTick(() => this.markFormPristine())
                } else {
                    this.closeModal()
                }
            } catch (error) {
                console.error('Error saving room amenity:', error)
                const status = Number(error?.response?.status)
                if (status === 403) return

                const payload = error?.response?.data
                if (status === 422 && payload?.errors) {
                    this.error = payload.errors
                    this.formError = 'Bạn chưa nhập đầy đủ thông tin'
                } else if (status === 404) {
                    this.formError = 'Dữ liệu đã thay đổi, vui lòng tải lại'
                    this.$toasted?.global?.error?.({ message: this.formError })
                } else {
                    this.formError = payload?.message || (this.id ? 'Cập nhật thất bại' : 'Thêm mới thất bại')
                    this.$toasted?.global?.error?.({ message: this.formError })
                }
            } finally {
                this.isSubmitSave = false
            }
        },
    },
}
</script>

<style lang="scss" scoped>
.room-amenity-icon-preview {
    flex: 0 0 auto;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    background: #f8fafc;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #1abc9c;
    font-size: 16px;
}
</style>
```

### e2e/tests/meeting/_room-amenity-ui.smoke.spec.ts
```ts
/**
 * SMOKE UI — Danh mục "Tiện nghi phòng họp" (Task 7, plan quan-ly-phong-hop).
 * Tạm thời (Task 10 sẽ viết bộ e2e chính thức) — chỉ verify khuôn UI chạy được thật trên browser:
 * mở màn -> tạo 1 bản ghi qua modal -> khóa -> mở khóa -> xóa, đo bằng số/text lấy từ DOM.
 *
 * Worktree riêng (nhánh feat/quan-ly-phong-hop): Nuxt ở :3001, API ở :8001.
 * Chạy: PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" BASE_URL=http://127.0.0.1:3001 \
 *   API_BASE=http://127.0.0.1:8001 npx playwright test _room-amenity-ui.smoke --project=chromium --no-deps --workers=1
 *
 * CẤM chờ `networkidle` (app polling nền) — chờ response GET list / mốc DOM cụ thể.
 */
import { test, expect } from '@playwright/test';

test.use({ storageState: '.auth/user-wt.json' });

test.describe.configure({ mode: 'serial' });

const RUN_SUFFIX = Date.now();
const CODE = `E2EUI_${RUN_SUFFIX}`;
const NAME = `Tiện nghi E2E UI ${RUN_SUFFIX}`;

const LIST_GET_RE = /\/api\/v1\/meeting\/room-amenities(\?|$)/;

test('CRUD tiện nghi phòng họp qua UI: tạo - khóa - mở khóa - xóa', async ({ page }) => {
  await page.goto('/meeting/room-amenities');

  const searchBox = page.getByPlaceholder('Tìm theo mã, tên tiện nghi');
  await expect(searchBox).toBeVisible();

  const rows = page.locator('table.data-table tbody tr');

  // 0. Lọc theo mã duy nhất của lần chạy này -> baseline PHẢI là 0 dòng dữ liệu thật.
  await searchBox.fill(CODE);
  await Promise.all([
    page.waitForResponse((res) => LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    searchBox.press('Enter'),
  ]);
  await expect(page.getByText('Không có dữ liệu phù hợp bộ lọc.')).toBeVisible();
  const baselineCount = await rows.count();
  expect(baselineCount).toBe(1); // 1 dòng placeholder "Không có dữ liệu..."

  // 1. Tạo mới qua modal
  await page.getByRole('button', { name: 'Tạo mới' }).click();
  const modal = page.locator('#modal-room-amenity');
  await expect(modal).toBeVisible();

  // 1a. Cảnh báo "chưa lưu" (unsavedModalMixin + V2BaseModal.hide() alias) — gõ dở tên rồi bấm X,
  // phải hiện popup xác nhận; chọn "Ở lại" thì modal + dữ liệu vẫn còn nguyên.
  // Dùng pressSequentially (gõ phím THẬT, có keydown) thay vì fill(): mixin bắt "user vừa sửa" bằng
  // listener keydown/pointerdown ở document trong cửa sổ 500ms — fill() set value thẳng, không phát
  // sự kiện phím nên mixin không thấy đây là thao tác của user (baseline tự dời, không báo bẩn).
  const nameInput = modal.getByPlaceholder('VD: Wifi / Máy chiếu / Điều hòa / ...');
  await nameInput.click();
  await nameInput.pressSequentially('Nháp chưa lưu', { delay: 20 });
  // Popup xác nhận render bằng plugin $confirm() (base-confirm-modal.vue) — nút "Thoát"/"Ở lại"
  // cũng dính icon trong slot #prefix nên getByRole(name, exact) không resolve được (như "Lưu" ở
  // trên); scope theo modal chứa đúng tiêu đề rồi bấm theo TEXT (không phải accessible-name).
  await modal.locator('button.close').click();
  const unsavedModalBox = page.locator('.modal-content').filter({ hasText: 'Thông tin chưa lưu' });
  const unsavedConfirm = page.getByText('Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?');
  await expect(unsavedConfirm).toBeVisible();
  await unsavedModalBox.getByText('Ở lại', { exact: true }).click();
  await expect(unsavedConfirm).toBeHidden();
  await expect(modal).toBeVisible();
  await expect(nameInput).toHaveValue('Nháp chưa lưu');

  // Bấm X lần nữa, lần này chọn "Thoát" -> modal đóng thật, KHÔNG tạo bản ghi nào (baseline vẫn 0).
  await modal.locator('button.close').click();
  await expect(unsavedConfirm).toBeVisible();
  await unsavedModalBox.getByText('Thoát', { exact: true }).click();
  await expect(modal).toBeHidden();
  await expect(rows).toHaveCount(1); // vẫn chỉ 1 dòng placeholder rỗng — chưa tạo gì

  // Mở lại modal (onHidden() đã reset local data) rồi nhập thật + lưu.
  await page.getByRole('button', { name: 'Tạo mới' }).click();
  await expect(modal).toBeVisible();
  await expect(nameInput).toHaveValue('');

  await modal.getByPlaceholder('VD: WIFI, PROJECTOR').fill(CODE);
  await nameInput.fill(NAME);

  // Nút đầu tiên trong footer luôn là "Lưu" (khuôn footer: Lưu / Lưu và tiếp tục / Đóng) — dùng vị
  // trí thay vì role+name: icon <i> trong slot #prefix của V2BaseButton làm accessible-name không
  // khớp chuỗi "Lưu" thuần (getByRole name:'Lưu', exact:true không bao giờ resolve được).
  await Promise.all([
    page.waitForResponse((res) => LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    modal.locator('.v2-modal-footer button').first().click(),
  ]);
  await expect(modal).toBeHidden();

  // Đo bằng DOM: bảng phải tăng đúng 1 dòng so với baseline (0 -> 1 bản ghi thật)
  await expect(rows).toHaveCount(1);
  const firstRow = rows.first();
  await expect(firstRow).toContainText(CODE);
  await expect(firstRow).toContainText(NAME);
  const badge = firstRow.locator('.v2-badge');
  await expect(badge).toHaveText('Hoạt động');

  // 2. Khóa
  await firstRow.getByTitle('Khóa tiện nghi').click();
  const lockConfirm = page.locator('#confirm-toggle-lock-room-amenity');
  await expect(lockConfirm).toBeVisible();
  // Nút xác nhận (accept) luôn là nút ĐẦU TIÊN trong `.modal-footer` (base-confirm-modal.vue).
  await Promise.all([
    page.waitForResponse((res) => LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    lockConfirm.locator('.modal-footer button').first().click(),
  ]);
  await expect(badge).toHaveText('Khóa');

  // 3. Mở khóa
  await firstRow.getByTitle('Mở khóa tiện nghi').click();
  const unlockConfirm = page.locator('#confirm-toggle-lock-room-amenity');
  await expect(unlockConfirm).toBeVisible();
  await Promise.all([
    page.waitForResponse((res) => LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    unlockConfirm.locator('.modal-footer button').first().click(),
  ]);
  await expect(badge).toHaveText('Hoạt động');

  // 4. Xóa — dọn sạch dữ liệu test
  await firstRow.getByTitle('Xóa').click();
  const deleteConfirm = page.locator('#confirm-delete-room-amenity');
  await expect(deleteConfirm).toBeVisible();
  await Promise.all([
    page.waitForResponse((res) => LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    deleteConfirm.locator('.modal-footer button').first().click(),
  ]);
  await expect(page.getByText('Không có dữ liệu phù hợp bộ lọc.')).toBeVisible();
  await expect(rows).toHaveCount(1); // trở lại 1 dòng placeholder rỗng — đã dọn sạch
});
```
