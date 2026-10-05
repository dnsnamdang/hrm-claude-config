# Review package — Task 8 (FE màn danh sách phòng họp)

## git status (worktree client)
 M components/modal/V2BaseModal.vue
?? pages/meeting/room-amenities/
?? pages/meeting/rooms/

### pages/meeting/rooms/index.vue
```vue
<template>
    <div class="v2-styles min-vh-100 d-flex justify-content-center pt-2">
        <div class="container-fluid">
            <!-- Plan quan-ly-phong-hop, Task 8 — bộ lọc dùng V2BaseSmartFilterPanel (khác Task 7 dùng
                 V2BaseFilterPanel) vì màn này có 4 trường lọc nâng cao, cần nhãn floating gọn cho
                 chế độ "Tìm kiếm nâng cao" (brief yêu cầu riêng, không phải khuôn chung của phân hệ). -->
            <V2BaseSmartFilterPanel
                table="meeting_rooms"
                :filter-fields="filterFields"
                :filters="filters"
                :collapsed="filterCollapsed"
                :quickSearchValue="filters.keyword"
                quickSearchPlaceholder="Tìm theo mã, tên phòng, vị trí"
                :floating="true"
                @toggle-panel="toggleFilterPanel"
                @quick-search-change="handleQuickSearchChange"
                @filter-change="handleFilterChange"
                @search="handleSearch"
                @reset="handleReset"
            >
                <!-- Tiện nghi: chọn nhiều, không có type dựng sẵn trong V2BaseFilterFieldControl nên
                     tự render qua slot (giống mẫu `field-tags` của pages/assign/tasks/index.vue) -->
                <template #field-amenity_ids>
                    <V2BaseSelectInModal
                        v-model="filters.amenity_ids"
                        :options="amenityOptions"
                        :extraSettings="{ multiple: true }"
                        placeholder="Chọn tiện nghi"
                        size="sm"
                        :allowClear="true"
                    />
                </template>
            </V2BaseSmartFilterPanel>

            <!-- DATA TABLE -->
            <V2BaseDataTable
                :data="tableData"
                :columns="tableColumns"
                :pagination="pagination"
                :loading="loading"
                :title="title"
                rowKey="id"
                itemLabel="phòng họp"
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

                <!-- Custom company column -->
                <template #cell-company_name="{ item }">
                    <span class="field-line">{{ companyName(item) }}</span>
                </template>

                <!-- Custom location column -->
                <template #cell-location="{ item }">
                    <span class="field-line">{{ item.location || '—' }}</span>
                </template>

                <!-- Custom capacity column -->
                <template #cell-capacity="{ item }">
                    {{ item.capacity != null && item.capacity !== '' ? Number(item.capacity).toLocaleString('en-US') : '—' }}
                </template>

                <!-- Custom amenities column (chip) -->
                <template #cell-amenities="{ item }">
                    <div v-if="item.amenities && item.amenities.length" class="room-amenity-chips">
                        <span v-for="amenity in item.amenities" :key="amenity.id" class="room-amenity-chip">
                            <i v-if="amenity.icon" :class="amenity.icon"></i>
                            {{ amenity.name }}
                        </span>
                    </div>
                    <span v-else style="color: #6b7280">—</span>
                </template>

                <!-- Custom manager column -->
                <template #cell-manager_name="{ item }">
                    <span class="field-line">{{ managerName(item) }}</span>
                </template>

                <!-- Custom require_approval column -->
                <template #cell-require_approval="{ item }">
                    <V2BaseBadge :variant="item.require_approval ? 'brand' : 'muted'">
                        {{ item.require_approval ? 'Có' : 'Không' }}
                    </V2BaseBadge>
                </template>

                <!-- Custom allow_cross_company column -->
                <template #cell-allow_cross_company="{ item }">
                    <V2BaseBadge :variant="item.allow_cross_company ? 'brand' : 'muted'">
                        {{ item.allow_cross_company ? 'Có' : 'Không' }}
                    </V2BaseBadge>
                </template>

                <!-- Custom status column -->
                <template #cell-status="{ item }">
                    <V2BaseBadge :variant="item.status == 2 ? 'required' : 'brand'">
                        {{ item.status == 2 ? 'Khóa' : 'Hoạt động' }}
                    </V2BaseBadge>
                </template>

                <!-- Custom actions column -->
                <template #cell-actions="{ item }">
                    <div class="d-flex align-items-center justify-content-center" style="gap: 8px">
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
                        <!-- Khóa: có kiểm bookings sắp tới trước khi hỏi xác nhận (onLock) — Mở khóa
                             không cần kiểm, hỏi thẳng. -->
                        <V2BaseIconButton
                            v-if="canManage && (item.status == 2 || item.is_can_lock)"
                            size="sm"
                            :title="item.status == 2 ? 'Mở khóa phòng họp' : 'Khóa phòng họp'"
                            @click="() => onToggleLock(item)"
                        >
                            <i :class="item.status == 2 ? 'ri-lock-unlock-line' : 'ri-lock-line'"></i>
                        </V2BaseIconButton>
                        <!-- Ẩn hẳn (không dùng interactable+disabledTitle) khi phòng đã có phiếu đặt -->
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
            id="confirm-delete-meeting-room"
            title="Xác nhận xóa"
            :message="deleteConfirmMessage"
            text-close="Hủy"
            text-accept="Xóa"
            danger
            accept-icon="ri-delete-bin-line"
            @event="handleConfirmDeleteItem"
        />

        <!-- Meeting Room Modal -->
        <MeetingRoomModal
            ref="meetingRoomModal"
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
import V2BaseSmartFilterPanel from '@/components/V2BaseSmartFilterPanel.vue'
import V2BaseSelectInModal from '@/components/V2BaseSelectInModal.vue'
import V2BaseDataTable from '@/components/V2BaseDataTable.vue'
import V2BaseTitleSubInfo from '@/components/V2BaseTitleSubInfo.vue'
import V2BaseBadge from '@/components/V2BaseBadge.vue'
import BaseConfirmModal from '@/components/modal/base-confirm-modal.vue'
import MeetingRoomModal from '@/pages/meeting/rooms/components/MeetingRoomModal.vue'
import { buildQuery } from '@/utils/url-action'
import { employeeFullName } from '@/utils/employeeOptionText'
import PageTitleMixin from '@/utils/mixins/PageTitleMixin'

const initialStateForm = {
    page: 1,
    per_page: 10,
    keyword: '',
    company_id: '',
    capacity_from: '',
    amenity_ids: [],
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
        V2BaseSmartFilterPanel,
        V2BaseSelectInModal,
        V2BaseDataTable,
        V2BaseTitleSubInfo,
        V2BaseBadge,
        BaseConfirmModal,
        MeetingRoomModal,
    },
    data() {
        return {
            loading: false,
            title: 'Danh mục phòng họp',
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

            // Tuỳ chọn bộ lọc — tiện nghi lấy qua form-options (không có API riêng danh sách tiện
            // nghi active, dùng chung endpoint dựng form). Công ty đọc thẳng $store.state.companies
            // (đã có sẵn từ user-profile lúc đăng nhập), không cần gọi thêm API.
            amenityOptions: [],

            // Items for actions
            itemToDelete: null,
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
            return 'Danh mục phòng họp'
        },
        companyOptions() {
            return (this.$store.state.companies || []).map((c) => ({ id: c.id, name: c.name }))
        },
        filterFields() {
            return [
                {
                    key: 'company_id',
                    label: 'Công ty',
                    type: 'select',
                    options: this.companyOptions,
                    col: 3,
                    resetKeys: ['company_id'],
                },
                {
                    key: 'capacity_from',
                    label: 'Sức chứa tối thiểu',
                    type: 'number',
                    col: 3,
                    resetKeys: ['capacity_from'],
                },
                {
                    key: 'amenity_ids',
                    label: 'Tiện nghi',
                    variant: 'tags',
                    col: 3,
                    resetKeys: ['amenity_ids'],
                    inputCount: 1,
                },
                {
                    key: 'status',
                    label: 'Trạng thái',
                    type: 'select',
                    options: this.statusOptions,
                    col: 3,
                    resetKeys: ['status'],
                },
            ]
        },
        tableColumns() {
            return [
                {
                    key: 'code',
                    title: 'Mã',
                    width: '110px',
                    minWidth: '100px',
                    align: 'left',
                },
                {
                    key: 'name',
                    title: 'Tên phòng',
                    minWidth: '160px',
                    cellClass: 'text-wrap',
                    align: 'left',
                },
                {
                    key: 'company_name',
                    title: 'Công ty',
                    minWidth: '140px',
                    align: 'left',
                },
                {
                    key: 'location',
                    title: 'Vị trí',
                    minWidth: '120px',
                    align: 'left',
                },
                {
                    key: 'capacity',
                    title: 'Sức chứa',
                    width: '90px',
                    align: 'center',
                },
                {
                    key: 'amenities',
                    title: 'Tiện nghi',
                    minWidth: '200px',
                    align: 'left',
                },
                {
                    key: 'manager_name',
                    title: 'Người quản lý',
                    minWidth: '160px',
                    align: 'left',
                },
                {
                    key: 'require_approval',
                    title: 'Cần duyệt',
                    width: '90px',
                    align: 'center',
                },
                {
                    key: 'allow_cross_company',
                    title: 'Cho công ty khác đặt',
                    width: '130px',
                    align: 'center',
                },
                {
                    key: 'status',
                    title: 'Trạng thái',
                    width: '100px',
                    align: 'left',
                },
                {
                    key: 'actions',
                    title: 'Hành động',
                    width: '150px',
                    align: 'center',
                },
            ]
        },

        deleteConfirmMessage() {
            if (!this.itemToDelete) return ''
            return `Bạn có chắc muốn xóa phòng họp '${this.itemToDelete.name}'?`
        },
    },
    async mounted() {
        // Cờ quyền fail-closed: khởi tạo false ở data(), chỉ bật từ $store.state.permissions —
        // TUYỆT ĐỐI không gán literal true (CLAUDE.md, lỗ hổng fail-open).
        // ⚠️ state.permissions là mảng OBJECT { id, name, ... }, KHÔNG phải mảng string —
        // .includes('<tên quyền>') luôn false (phát hiện Task 7). Phải so theo p.name.
        const perms = this.$store.state.permissions || []
        this.canManage = perms.some((p) => p.name === 'Quản lý danh mục phòng họp')
        this.canView = this.canManage || perms.some((p) => p.name === 'Xem danh mục phòng họp')

        await Promise.all([this.loadData(), this.loadAmenityOptions()])

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
        // Lookup hiển thị — Resource chỉ trả company_id/manager_employee_id (không có
        // company_name/manager_name), tự map từ state đã có sẵn (không thêm API).
        companyName(item) {
            const company = (this.$store.state.companies || []).find((c) => Number(c.id) === Number(item.company_id))
            return company ? company.name : '—'
        },
        managerName(item) {
            if (!item.manager_employee_id) return '—'
            const employee = (this.$store.state.employees || []).find(
                (e) => Number(e.id) === Number(item.manager_employee_id)
            )
            return employee ? employeeFullName(employee) : '—'
        },

        async loadAmenityOptions() {
            try {
                const body = await this.$store.dispatch('apiGetMethod', 'meeting/rooms/form-options')
                const options = body.data || {}
                this.amenityOptions = (options.amenities || []).map((a) => ({ id: a.id, name: a.name }))
            } catch (error) {
                console.error('Error loading amenity options:', error)
            }
        },

        // Data loading
        async loadData() {
            try {
                this.loading = true

                this.filters.page = this.pagination.currentPage
                this.filters.per_page = this.pagination.pageSize

                const { data, meta } = await this.$store.dispatch(
                    'apiGetMethod',
                    `meeting/rooms${buildQuery(this.filters)}`
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

        handleFilterChange({ key, value }) {
            this.filters[key] = value
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
            this.$refs.meetingRoomModal?.resetModal()
            this.$bvModal.show('modal-meeting-room')
        },

        async viewItem(item) {
            this.selectedItem = item
            this.isShow = true
            let loadOk = true
            if (item?.id) {
                loadOk = await this.$refs.meetingRoomModal?.loadData(item.id)
            }
            if (loadOk !== false) {
                this.$bvModal.show('modal-meeting-room')
            }
        },

        async editItem(item) {
            this.selectedItem = item
            this.isShow = false
            let loadOk = true
            if (item?.id) {
                loadOk = await this.$refs.meetingRoomModal?.loadData(item.id)
            }
            if (loadOk !== false) {
                this.$bvModal.show('modal-meeting-room')
            }
        },

        // Khóa phòng: kiểm phiếu sắp tới trước, nội dung cảnh báo ghi rõ số phiếu (yêu cầu riêng
        // của Task 8, brief bước 4).
        async onLock(room) {
            try {
                const { data } = await this.$store.dispatch(
                    'apiGetMethod',
                    `meeting/rooms/${room.id}/upcoming-bookings`
                )
                const message =
                    data.count > 0
                        ? `Phòng còn ${Number(data.count).toLocaleString(
                              'en-US'
                          )} phiếu đặt sắp tới. Khóa phòng sẽ gửi thông báo cho người đặt để đổi phòng. Bạn chắc chắn khóa?`
                        : 'Bạn chắc chắn muốn khóa phòng họp này?'

                const ok = await this.$confirm({
                    title: 'Khóa phòng họp',
                    message,
                    textAccept: 'Khóa',
                    danger: true,
                    acceptIcon: 'ri-lock-line',
                })
                if (!ok) return

                await this.$store.dispatch('apiGet', `meeting/rooms/${room.id}/lock`)
                this.$toasted?.global?.success?.({ message: 'Khóa phòng họp thành công' })
                await this.loadData()
            } catch (error) {
                console.error('Error locking room:', error)
                const status = Number(error?.response?.status)
                if (status === 403) return

                const errorMessage =
                    status === 404
                        ? 'Dữ liệu đã thay đổi, vui lòng tải lại'
                        : error?.response?.data?.message || 'Khóa phòng họp thất bại'
                this.$toasted?.global?.error?.({ message: errorMessage })
            }
        },

        async onUnlock(room) {
            try {
                const ok = await this.$confirm({
                    title: 'Mở khóa phòng họp',
                    message: 'Bạn có chắc muốn mở khóa phòng họp này?',
                    textAccept: 'Mở khóa',
                    acceptIcon: 'ri-lock-unlock-line',
                })
                if (!ok) return

                await this.$store.dispatch('apiGet', `meeting/rooms/${room.id}/unlock`)
                this.$toasted?.global?.success?.({ message: 'Mở khóa phòng họp thành công' })
                await this.loadData()
            } catch (error) {
                console.error('Error unlocking room:', error)
                const status = Number(error?.response?.status)
                if (status === 403) return

                const errorMessage = error?.response?.data?.message || 'Mở khóa phòng họp thất bại'
                this.$toasted?.global?.error?.({ message: errorMessage })
            }
        },

        async onToggleLock(room) {
            if (room.status == 2) {
                await this.onUnlock(room)
            } else {
                await this.onLock(room)
            }
        },

        async deleteItem(item) {
            try {
                await this.$store.dispatch('apiDelete', `meeting/rooms/${item.id}`)
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
            this.$bvModal.show('confirm-delete-meeting-room')
        },

        async handleConfirmDeleteItem() {
            if (!this.itemToDelete) return

            await this.deleteItem(this.itemToDelete)
            this.itemToDelete = null
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
            this.$bvModal.hide('modal-meeting-room')
        },
    },
}
</script>
<style lang="scss">
@import '@/assets/scss/v2-styles.scss';

.room-amenity-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
}

.room-amenity-chip {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 8px;
    border-radius: 999px;
    background: #f0fdfa;
    border: 1px solid #ccfbf1;
    color: #0f766e;
    font-size: 11px;
    white-space: nowrap;
}
</style>
```

### pages/meeting/rooms/components/MeetingRoomModal.vue
```vue
<template>
    <!--
        Plan quan-ly-phong-hop, Task 8 — popup Thêm / Sửa / Xem phòng họp.
        Khuôn copy từ `pages/meeting/room-amenities/components/RoomAmenityModal.vue` (Task 7),
        thêm nhóm Công ty/Vị trí/Sức chứa/Người quản lý + Tiện nghi (chọn nhiều) + 2 cờ cài đặt.
        `form-options` chỉ gọi 1 lần MỖI LẦN MỞ modal (hook @show = onModalShow), KHÔNG gọi ở
        mounted() — brief Task 8 bước 3.
    -->
    <V2BaseModal
        ref="modal"
        modal-id="modal-meeting-room"
        :title="modalTitle"
        icon="ri-door-open-line"
        size="lg"
        @show="onModalShow"
        @shown="onUnsavedModalShown"
        @hide="onUnsavedModalHide"
        @hidden="onHidden"
    >
        <V2BaseFormSection title="Thông tin chung">
            <div class="form-row">
                <div class="col-md-4 mb-3">
                    <V2BaseLabel required>Mã phòng</V2BaseLabel>
                    <V2BaseInput
                        v-model="data.code"
                        placeholder="VD: A301"
                        size="sm"
                        maxlength="50"
                        :disabled="isShow"
                        :invalid="!!error.code"
                    />
                    <V2BaseError v-if="error.code" :message="error.code" size="sm" class="mb-0 mt-1" />
                </div>

                <div class="col-md-8 mb-3">
                    <V2BaseLabel required>Tên phòng</V2BaseLabel>
                    <V2BaseInput
                        v-model="data.name"
                        placeholder="VD: Phòng họp tầng 3"
                        size="sm"
                        maxlength="255"
                        :disabled="isShow"
                        :invalid="!!error.name"
                    />
                    <V2BaseError v-if="error.name" :message="error.name" size="sm" class="mb-0 mt-1" />
                </div>
            </div>

            <div class="form-row">
                <div class="col-md-6 mb-3">
                    <V2BaseLabel required>Công ty</V2BaseLabel>
                    <V2BaseSelectInModal
                        v-model="data.company_id"
                        :options="companyOptions"
                        placeholder="Chọn công ty"
                        size="sm"
                        :disabled="isShow"
                        :allowClear="false"
                        :invalid="!!error.company_id"
                    />
                    <V2BaseError v-if="error.company_id" :message="error.company_id" size="sm" class="mb-0 mt-1" />
                </div>

                <div class="col-md-6 mb-3">
                    <V2BaseLabel>Vị trí</V2BaseLabel>
                    <V2BaseInput
                        v-model="data.location"
                        placeholder="VD: Tầng 3, tòa nhà A"
                        size="sm"
                        maxlength="255"
                        :disabled="isShow"
                        :invalid="!!error.location"
                    />
                    <V2BaseError v-if="error.location" :message="error.location" size="sm" class="mb-0 mt-1" />
                </div>
            </div>

            <div class="form-row">
                <div class="col-md-4 mb-3">
                    <V2BaseLabel>Sức chứa</V2BaseLabel>
                    <V2BaseInput
                        v-model="data.capacity"
                        type="number"
                        min="0"
                        placeholder="VD: 10"
                        size="sm"
                        :disabled="isShow"
                        :invalid="!!error.capacity"
                    />
                    <V2BaseError v-if="error.capacity" :message="error.capacity" size="sm" class="mb-0 mt-1" />
                </div>

                <div class="col-md-8 mb-3">
                    <V2BaseLabel>Người quản lý</V2BaseLabel>
                    <V2BaseSelectInModal
                        v-model="data.manager_employee_id"
                        :options="employeeOptions"
                        placeholder="Chọn người quản lý"
                        size="sm"
                        :disabled="isShow"
                        :allowClear="true"
                        :invalid="!!error.manager_employee_id"
                    />
                    <V2BaseError
                        v-if="error.manager_employee_id"
                        :message="error.manager_employee_id"
                        size="sm"
                        class="mb-0 mt-1"
                    />
                </div>
            </div>
        </V2BaseFormSection>

        <V2BaseFormSection title="Tiện nghi & cài đặt đặt phòng" class="mt-3">
            <div class="form-row">
                <div class="col-md-12 mb-3">
                    <V2BaseLabel>Tiện nghi</V2BaseLabel>
                    <V2BaseSelectInModal
                        v-model="data.amenity_ids"
                        :options="amenityOptions"
                        :extraSettings="{ multiple: true }"
                        placeholder="Chọn tiện nghi phòng họp"
                        size="sm"
                        :disabled="isShow"
                        :allowClear="true"
                    />
                    <V2BaseError v-if="error.amenity_ids" :message="error.amenity_ids" size="sm" class="mb-0 mt-1" />
                </div>
            </div>

            <div class="form-row">
                <div class="col-md-6 mb-1">
                    <div class="d-flex align-items-center" style="gap: 8px">
                        <V2BaseCheckbox v-model="data.require_approval" :disabled="isShow" />
                        <span class="mb-0" style="cursor: pointer" @click="toggleRequireApproval">
                            Cần duyệt trước khi đặt
                        </span>
                    </div>
                </div>

                <div class="col-md-6 mb-1">
                    <div class="d-flex align-items-center" style="gap: 8px">
                        <V2BaseCheckbox v-model="data.allow_cross_company" :disabled="isShow" />
                        <span class="mb-0" style="cursor: pointer" @click="toggleAllowCrossCompany">
                            Cho công ty khác đặt
                        </span>
                    </div>
                </div>
            </div>
        </V2BaseFormSection>

        <V2BaseFormSection title="Mô tả" class="mt-3">
            <div class="form-row">
                <div class="col-md-12 mb-1">
                    <V2BaseTextarea
                        v-model="data.description"
                        placeholder="Ghi chú thêm về phòng họp"
                        size="sm"
                        :disabled="isShow"
                        style="min-height: 72px; resize: vertical"
                    />
                    <V2BaseError v-if="error.description" :message="error.description" size="sm" class="mb-0 mt-1" />
                </div>
            </div>
        </V2BaseFormSection>

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
import V2BaseCheckbox from '@/components/V2BaseCheckbox.vue'
import V2BaseTextarea from '@/components/V2BaseTextarea.vue'
import V2BaseError from '@/components/V2BaseError.vue'
import V2BaseButton from '@/components/V2BaseButton.vue'
import V2BaseFormSection from '@/components/V2BaseFormSection.vue'
import unsavedModalMixin from '@/utils/mixins/unsavedModalMixin'
import { employeeOptionText } from '@/utils/employeeOptionText'

const emptyData = () => ({
    code: '',
    name: '',
    company_id: null,
    location: '',
    capacity: '',
    manager_employee_id: null,
    amenity_ids: [],
    require_approval: false,
    allow_cross_company: false,
    description: '',
})

export default {
    components: {
        V2BaseModal,
        V2BaseInput,
        V2BaseLabel,
        V2BaseSelectInModal,
        V2BaseCheckbox,
        V2BaseTextarea,
        V2BaseError,
        V2BaseButton,
        V2BaseFormSection,
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
            // form-options: tiện nghi + công ty — nạp 1 lần MỖI LẦN modal mở (xem onModalShow).
            amenityOptions: [],
            companyOptions: [],
        }
    },
    computed: {
        modalTitle() {
            if (this.isShow) return 'Xem phòng họp'
            return this.id ? 'Sửa phòng họp' : 'Thêm phòng họp'
        },
        // Nhân viên đã có sẵn trong $store.state.employees (nạp lúc đăng nhập, xem
        // store/actions.js) — không cần gọi thêm API riêng cho ô "Người quản lý".
        // Nhãn theo khuôn chuẩn `utils/employeeOptionText.js`.
        employeeOptions() {
            return (this.$store.state.employees || []).map((employee) => ({
                id: employee.id,
                name: employeeOptionText(employee),
            }))
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

        async onModalShow() {
            if (!this.id) {
                this.resetLocalData()
            }
            // 1 request duy nhất, gọi ở đây (lúc modal MỞ), KHÔNG gọi ở mounted() — brief Task 8
            // bước 3: tránh gọi lại API mỗi lần component modal được dựng lên nhưng chưa mở.
            await this.loadFormOptions()
        },

        async loadFormOptions() {
            try {
                const body = await this.$store.dispatch('apiGetMethod', 'meeting/rooms/form-options')
                const options = body.data || {}
                this.amenityOptions = (options.amenities || []).map((amenity) => ({
                    id: amenity.id,
                    name: amenity.name,
                }))
                this.companyOptions = (options.companies || []).map((company) => ({
                    id: company.id,
                    name: company.name,
                }))
            } catch (error) {
                console.error('Error loading form options:', error)
                this.$toasted?.global?.error?.({ message: 'Lỗi khi tải dữ liệu dựng form' })
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

        toggleRequireApproval() {
            if (this.isShow) return
            this.data.require_approval = !this.data.require_approval
        },

        toggleAllowCrossCompany() {
            if (this.isShow) return
            this.data.allow_cross_company = !this.data.allow_cross_company
        },

        async loadData(id) {
            try {
                const response = await this.$store.dispatch('apiGet', `meeting/rooms/${id}`)
                const detail = response.data.data
                this.data = {
                    code: detail.code || '',
                    name: detail.name || '',
                    company_id: detail.company_id ?? null,
                    location: detail.location || '',
                    capacity: detail.capacity ?? '',
                    manager_employee_id: detail.manager_employee_id ?? null,
                    amenity_ids: (detail.amenities || []).map((amenity) => amenity.id),
                    require_approval: !!detail.require_approval,
                    allow_cross_company: !!detail.allow_cross_company,
                    description: detail.description || '',
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
                    company_id: this.data.company_id,
                    location: (this.data.location || '').trim(),
                    capacity: this.data.capacity === '' || this.data.capacity === null ? null : Number(this.data.capacity),
                    manager_employee_id: this.data.manager_employee_id || null,
                    amenity_ids: this.data.amenity_ids || [],
                    require_approval: !!this.data.require_approval,
                    allow_cross_company: !!this.data.allow_cross_company,
                    description: (this.data.description || '').trim(),
                }
                if (this.id) payload.id = this.id

                await this.$store.dispatch('apiPostMethod', { url: 'meeting/rooms', payload })

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
                console.error('Error saving meeting room:', error)
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
```

### e2e/tests/meeting/_room-ui.smoke.spec.ts
```ts
/**
 * SMOKE UI — Danh mục "Phòng họp" (Task 8, plan quan-ly-phong-hop).
 * Tạm thời (Task 10 sẽ viết bộ e2e chính thức) — chỉ verify khuôn UI chạy được thật trên browser:
 * mở màn -> tạo 1 phòng gắn 2 tiện nghi qua modal -> khóa -> xóa, đo bằng số/text lấy từ DOM.
 *
 * Worktree riêng (nhánh feat/quan-ly-phong-hop): Nuxt ở :3001, API ở :8001.
 * Chạy: PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" BASE_URL=http://127.0.0.1:3001 \
 *   API_BASE=http://127.0.0.1:8001 npx playwright test _room-ui.smoke --project=chromium --no-deps --workers=1
 *
 * Môi trường này KHÔNG có sẵn tiện nghi phòng họp nào (đã kiểm: GET meeting/room-amenities trả
 * data rỗng) -> phải tự tạo 2 tiện nghi qua API trong beforeAll rồi mới gắn được vào form, dọn
 * lại ở afterAll.
 *
 * CẤM chờ `networkidle` (app polling nền) — chờ response GET list / mốc DOM cụ thể.
 */
import { test, expect, request, APIRequestContext } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

test.use({ storageState: '.auth/user-wt.json' });

test.describe.configure({ mode: 'serial' });

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8001';
const ADMIN_TOKEN_FILE = path.join(__dirname, '..', '..', '.auth', 'api-wt.json');

const RUN_SUFFIX = Date.now();
const CODE = `E2EUI_RM_${RUN_SUFFIX}`;
const NAME = `Phòng họp E2E UI ${RUN_SUFFIX}`;
const AM1_CODE = `E2EUI_AM1_${RUN_SUFFIX}`;
const AM1_NAME = `Tiện nghi E2E UI 1 ${RUN_SUFFIX}`;
const AM2_CODE = `E2EUI_AM2_${RUN_SUFFIX}`;
const AM2_NAME = `Tiện nghi E2E UI 2 ${RUN_SUFFIX}`;

const ROOMS_LIST_GET_RE = /\/api\/v1\/meeting\/rooms(\?|$)/;

let api: APIRequestContext;
const amenityIds: number[] = [];

test.beforeAll(async () => {
  const token = JSON.parse(fs.readFileSync(ADMIN_TOKEN_FILE, 'utf8')).token;
  api = await request.newContext({
    baseURL: API_BASE,
    extraHTTPHeaders: { Accept: 'application/json', Authorization: `Bearer ${token}` },
  });

  // Setup dữ liệu: tạo 2 tiện nghi active để có option gắn vào phòng trong modal.
  for (const [code, name] of [
    [AM1_CODE, AM1_NAME],
    [AM2_CODE, AM2_NAME],
  ]) {
    const res = await api.post('/api/v1/meeting/room-amenities', { data: { code, name } });
    expect(res.status(), `tạo tiện nghi setup ${code}`).toBe(200);
    const body = await res.json();
    amenityIds.push(body.data.id);
  }
});

test.afterAll(async () => {
  // Ca UI đã tự xóa phòng test trong bước cuối — ở đây chỉ cần dọn 2 tiện nghi setup.
  for (const id of amenityIds) {
    await api.delete(`/api/v1/meeting/room-amenities/${id}`).catch(() => {});
  }
  await api.dispose();
});

/**
 * Chờ ô select (bọc trong 1 element chứa `wrapperText`) có ĐỦ option nạp xong.
 *
 * KHÔNG đủ nếu chỉ chờ response GET `form-options`: server dev (`artisan serve`, đơn luồng) xử lý
 * chậm khi có nhiều request xếp hàng — đã đo thực tế response về sau 2-6s dù network log báo 200
 * gần như ngay. Đợi thẳng DOM (`<select>.options.length`) mới là mốc đúng, không đoán thời gian.
 */
async function waitForSelectOptions(page: import('@playwright/test').Page, wrapperClass: string, wrapperText: string, minOptions = 1) {
  await page.waitForFunction(
    ({ wrapperClass, wrapperText, minOptions }) => {
      const wraps = [...document.querySelectorAll(`#modal-meeting-room ${wrapperClass}`)];
      const wrap = wraps.find((el) => (el.textContent || '').includes(wrapperText));
      const select = wrap ? wrap.querySelector('select') : null;
      return !!select && select.options.length >= minOptions;
    },
    { wrapperClass, wrapperText, minOptions },
    { timeout: 20000 },
  );
}

/**
 * Bấm mở dropdown select2, có RETRY — đã đo thấy đôi lúc 1 cú click không làm dropdown mở (server
 * dev đơn luồng làm event loop / render bận), khiến bước chọn option sau đó timeout. Thử lại vài
 * lần thay vì tăng timeout suông cho 1 click.
 */
async function openSelect2(page: import('@playwright/test').Page, fieldLocator: import('@playwright/test').Locator) {
  for (let attempt = 0; attempt < 5; attempt++) {
    await fieldLocator.locator('.select2-selection').click();
    try {
      await page.locator('.select2-container--open').first().waitFor({ state: 'visible', timeout: 3000 });
      return;
    } catch (e) {
      // thử lại
    }
  }
  throw new Error('select2 dropdown không mở được sau 5 lần thử');
}

/**
 * Mở dropdown rồi chọn 1 option theo text hiển thị, có RETRY toàn bộ thao tác mở+chọn.
 *
 * Gõ vào ô tìm kiếm của dropdown để LỌC danh sách còn đúng 1-2 dòng trước khi click — môi trường
 * này có dữ liệu tiện nghi cũ (đợt debug trước) lẫn trong danh mục, danh sách dài/phải cuộn làm
 * click theo text không ổn định. Gõ lọc tránh hẳn việc phải cuộn hay đoán vị trí.
 */
async function pickSelect2Option(
  page: import('@playwright/test').Page,
  fieldLocator: import('@playwright/test').Locator,
  optionText: string | null,
) {
  for (let attempt = 0; attempt < 3; attempt++) {
    await openSelect2(page, fieldLocator);
    if (optionText) {
      const searchField = page.locator('.select2-container--open .select2-search__field').first();
      await searchField.fill(optionText);
    }
    const option = optionText
      ? page.locator('.select2-container--open li.select2-results__option', { hasText: optionText }).first()
      : page.locator('.select2-container--open li.select2-results__option:not(.select2-results__message)').first();
    try {
      await option.click({ timeout: 5000 });
      return;
    } catch (e) {
      // Thử lại bằng cách mở lại dropdown ở vòng sau — TUYỆT ĐỐI không nhấn Escape ở đây: modal
      // dùng unsavedModalMixin bắt phím Escape để hỏi "Thông tin chưa lưu", popup đó che kín màn
      // hình và làm mọi click sau đứng hình (đã đo trúng lỗi này).
    }
  }
  throw new Error(`Không chọn được option "${optionText}" sau 3 lần thử`);
}

test('CRUD phòng họp qua UI: tạo kèm 2 tiện nghi - khóa - xóa', async ({ page }) => {
  test.setTimeout(90000); // server dev đơn luồng, form-options có lúc mất vài giây mới về

  await page.goto('/meeting/rooms');

  const searchBox = page.getByPlaceholder('Tìm theo mã, tên phòng, vị trí');
  // Server dev đơn luồng — lần vào màn đầu tiên có lúc chậm hơn 5s mặc định.
  await expect(searchBox).toBeVisible({ timeout: 20000 });

  const rows = page.locator('table.data-table tbody tr');

  // 0. Lọc theo mã duy nhất của lần chạy này -> baseline PHẢI là 0 dòng dữ liệu thật.
  await searchBox.fill(CODE);
  await Promise.all([
    page.waitForResponse((res) => ROOMS_LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    searchBox.press('Enter'),
  ]);
  await expect(page.getByText('Không có dữ liệu phù hợp bộ lọc.')).toBeVisible();
  await expect(rows).toHaveCount(1); // 1 dòng placeholder "Không có dữ liệu..."

  // 1. Tạo mới qua modal — @show gọi form-options (công ty + tiện nghi) 1 lần.
  await page.getByRole('button', { name: 'Tạo mới' }).click();
  const modal = page.locator('#modal-meeting-room');
  await expect(modal).toBeVisible();

  await modal.getByPlaceholder('VD: A301').fill(CODE);
  await modal.getByPlaceholder('VD: Phòng họp tầng 3').fill(NAME);

  // Công ty (bắt buộc) — chọn option đầu tiên, không lệ thuộc công ty cụ thể nào. Chờ options nạp
  // xong TRÊN DOM (không đoán theo thời gian network) rồi mới click.
  const companyField = modal.locator('.col-md-6.mb-3').filter({ hasText: 'Công ty' });
  await waitForSelectOptions(page, '.col-md-6.mb-3', 'Công ty', 1);
  await pickSelect2Option(page, companyField, null);

  await modal.getByPlaceholder('VD: Tầng 3, tòa nhà A').fill('Tầng 5, tòa nhà E2E');
  await modal.getByPlaceholder('VD: 10').fill('12');

  // Tiện nghi — chọn nhiều, chọn đúng 2 tiện nghi vừa setup ở beforeAll (khớp theo TÊN, không lệ
  // thuộc dữ liệu có sẵn trong môi trường). ⚠️ Đã đo: dropdown TỰ ĐÓNG sau mỗi lần chọn (khác hành
  // vi mặc định select2 multi) -> phải mở lại dropdown trước khi chọn tiện nghi thứ 2.
  const amenityField = modal.locator('.col-md-12.mb-3').filter({ hasText: 'Tiện nghi' }).first();
  await waitForSelectOptions(page, '.col-md-12.mb-3', 'Tiện nghi', 2);
  await pickSelect2Option(page, amenityField, AM1_NAME);
  await pickSelect2Option(page, amenityField, AM2_NAME);
  // Đóng dropdown — bấm ra vùng trống trong thân modal.
  await modal.locator('.v2-modal-body').click({ position: { x: 5, y: 5 } });

  // Lưu — nút đầu tiên trong footer luôn là "Lưu" (khuôn footer: Lưu / Lưu và tiếp tục / Đóng).
  await Promise.all([
    page.waitForResponse((res) => ROOMS_LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    modal.locator('.v2-modal-footer button').first().click(),
  ]);
  await expect(modal).toBeHidden();

  // Đo bằng DOM: bảng phải tăng đúng 1 dòng so với baseline (0 -> 1 bản ghi thật)
  await expect(rows).toHaveCount(1);
  const row = rows.first();
  await expect(row).toContainText(CODE);
  await expect(row).toContainText(NAME);

  // Đo số chip tiện nghi trên dòng vừa tạo — cột "Tiện nghi" là cột thứ 6 (Mã, Tên phòng, Công ty,
  // Vị trí, Sức chứa, Tiện nghi, ...).
  const chips = row.locator('td:nth-child(6) .room-amenity-chip');
  await expect(chips).toHaveCount(2);

  // Badge trạng thái là cột thứ 10 (... Cần duyệt, Cho công ty khác đặt, Trạng thái, Hành động) —
  // dòng còn có 2 badge Có/Không khác nên KHÔNG dùng `.v2-badge` chung chung.
  const statusBadge = row.locator('td:nth-child(10) .v2-badge');
  await expect(statusBadge).toHaveText('Hoạt động');

  // 2. Khóa — popup xác nhận render bằng plugin $confirm() (base-confirm-modal.vue, id ngẫu nhiên
  // sinh lúc runtime) -> lọc theo tiêu đề thay vì id cố định.
  await row.getByTitle('Khóa phòng họp').click();
  const lockConfirm = page.locator('.modal-content').filter({ hasText: 'Khóa phòng họp' });
  await expect(lockConfirm).toBeVisible();
  // Phòng vừa tạo chưa có phiếu đặt nào -> đúng nhánh "không có phiếu" của onLock().
  await expect(lockConfirm).toContainText('Bạn chắc chắn muốn khóa phòng họp này?');
  await Promise.all([
    page.waitForResponse((res) => ROOMS_LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    lockConfirm.locator('.modal-footer button').first().click(),
  ]);
  await expect(statusBadge).toHaveText('Khóa');

  // 3. Xóa — dọn sạch dữ liệu test (phòng đã khóa nhưng chưa từng có phiếu đặt -> vẫn is_can_delete)
  await row.getByTitle('Xóa').click();
  const deleteConfirm = page.locator('#confirm-delete-meeting-room');
  await expect(deleteConfirm).toBeVisible();
  await Promise.all([
    page.waitForResponse((res) => ROOMS_LIST_GET_RE.test(res.url()) && res.request().method() === 'GET'),
    deleteConfirm.locator('.modal-footer button').first().click(),
  ]);
  await expect(page.getByText('Không có dữ liệu phù hợp bộ lọc.')).toBeVisible();
  await expect(rows).toHaveCount(1); // trở lại 1 dòng placeholder rỗng — đã dọn sạch
});
```
