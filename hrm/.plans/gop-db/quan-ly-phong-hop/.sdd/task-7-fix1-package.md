# Re-review package — Task 7 fix round 1

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
import CheckPermission from '@/utils/mixins/CheckPermission'

const initialStateForm = {
    page: 1,
    per_page: 10,
    keyword: '',
    status: '',
}

export default {
    layout: 'default-sidebar',
    mixins: [PageTitleMixin, CheckPermission],
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

            // Status options
            statusOptions: [
                { id: 1, name: 'Hoạt động' },
                { id: 2, name: 'Khóa' },
            ],
        }
    },
    computed: {
        // Cờ quyền fail-closed: dùng helper có sẵn `hasAPermission()` (mixin CheckPermission,
        // reactive theo $store.state.permissions) thay vì tự gán 1 lần ở mounted() — CLAUDE.md yêu
        // cầu ưu tiên helper dùng chung. Chỉ gate hiện/ẩn nút (Sửa/Xóa/Khóa/Tạo mới); chặn vào URL
        // trực tiếp do middleware toàn cục `checkPermission.js` (tra registry menu, Task 9) lo, KHÔNG
        // phải việc của page nên không cần `canView` ở đây (đã bỏ, dead code).
        canManage() {
            return this.hasAPermission('Quản lý danh mục tiện nghi phòng họp')
        },
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
 * CẤM chờ `networkidle` (app polling nền) — chờ mốc DOM cụ thể.
 *
 * Fix round 1 (review):
 *   - Bỏ kiểu chờ đua `Promise.all([page.waitForResponse(<regex khớp CẢ GET nền lẫn GET do click
 *     sinh ra>), click()])` — app có polling nền nên response bắt được có thể KHÔNG PHẢI response
 *     của cú click vừa bấm, khiến assertion chạy trước khi UI kịp render (flaky: reviewer chạy lần 1
 *     FAIL ở `expect(badge).toHaveText('Khóa')` dù BE đã khóa đúng — lỗi timing phía test, không
 *     phải BE). Thay bằng `expect(locator).toHaveText(...)/toHaveCount(...)` — các assertion này TỰ
 *     RETRY tới hết timeout, không cần đoán đúng response nào ứng với thao tác nào.
 *   - Dọn dữ liệu KHÔNG PHỤ THUỘC happy path: `beforeAll` quét xóa rác `E2EUI_` còn sót từ lần chạy
 *     trước bị kill giữa chừng (giống `room-amenity.api.spec.ts`); `afterEach` xóa bản ghi mã CODE
 *     của chính lần chạy này dù ca pass hay fail — không còn để rác nằm lại DB dùng chung.
 */
import { test, expect, request, APIRequestContext } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

test.use({ storageState: '.auth/user-wt.json' });

test.describe.configure({ mode: 'serial' });

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8001';
const ADMIN_TOKEN_FILE = path.join(__dirname, '..', '..', '.auth', 'api-wt.json');
const AMENITIES_URL = '/api/v1/meeting/room-amenities';

const RUN_SUFFIX = Date.now();
const CODE = `E2EUI_${RUN_SUFFIX}`;
const NAME = `Tiện nghi E2E UI ${RUN_SUFFIX}`;

let api: APIRequestContext;

/** Xóa mọi bản ghi có `code` bắt đầu bằng `prefix`, lặp theo trang cho tới khi hết (khuôn copy từ
 *  `room-amenity.api.spec.ts::cleanupLeftoverE2eData`). Dùng cho cả dọn rác lần chạy trước (beforeAll,
 *  prefix rộng `E2EUI_`) lẫn dọn bản ghi của chính lần chạy này (afterEach, prefix hẹp = CODE). */
async function deleteByCodePrefix(prefix: string) {
  // eslint-disable-next-line no-constant-condition
  for (let i = 0; i < 20; i++) {
    const res = await api.get(`${AMENITIES_URL}?keyword=${encodeURIComponent(prefix)}&per_page=100`);
    if (res.status() !== 200) break;
    const body = await res.json();
    const rows = Array.isArray(body.data) ? body.data : (body.data?.data ?? []);
    const ids = (Array.isArray(rows) ? rows : [])
      .filter((r: any) => typeof r.code === 'string' && r.code.startsWith(prefix))
      .map((r: any) => r.id);
    if (ids.length === 0) break;
    for (const id of ids) {
      await api.delete(`${AMENITIES_URL}/${id}`).catch(() => {});
    }
  }
}

test.beforeAll(async () => {
  const adminToken = JSON.parse(fs.readFileSync(ADMIN_TOKEN_FILE, 'utf8')).token;
  api = await request.newContext({
    baseURL: API_BASE,
    extraHTTPHeaders: { Accept: 'application/json', Authorization: `Bearer ${adminToken}` },
  });
  await deleteByCodePrefix('E2EUI_');
});

test.afterEach(async () => {
  // Chạy dù ca pass hay fail — bản ghi lần này (nếu có tạo) không được để lại DB dùng chung.
  await deleteByCodePrefix(CODE);
});

test.afterAll(async () => {
  await api?.dispose();
});

test('CRUD tiện nghi phòng họp qua UI: tạo - khóa - mở khóa - xóa', async ({ page }) => {
  // 60s thay vì mặc định 30s: nhiều assertion sau đã nới lên 15s cho máy dev chạy chung nhiều phiên,
  // tổng các bước có thể vượt 30s dưới tải cao dù mỗi bước đơn lẻ vẫn xanh.
  test.setTimeout(60000);
  await page.goto('/meeting/room-amenities');

  // App-shell chờ API `user-profile` (bootstrap permissions/menu) xong mới tắt spinner tải trang —
  // máy dev dùng chung, nhiều phiên cùng chạy có lúc khiến bước bootstrap này chậm hơn 5s mặc định.
  const searchBox = page.getByPlaceholder('Tìm theo mã, tên tiện nghi');
  await expect(searchBox).toBeVisible({ timeout: 20000 });

  const rows = page.locator('table.data-table tbody tr');

  // 0. Lọc theo mã duy nhất của lần chạy này -> baseline PHẢI là 0 dòng dữ liệu thật.
  // Timeout 15s (thay vì mặc định 5s) cho các assertion sau 1 thao tác gọi API: môi trường dev dùng
  // chung có lúc chậm (nhiều phiên/agent cùng chạy) — `expect().toHaveText/toHaveCount` tự poll tới
  // hết timeout nên nới thời gian không làm test kém chặt chẽ, chỉ bớt false-negative do máy chậm.
  await searchBox.fill(CODE);
  await searchBox.press('Enter');
  await expect(page.getByText('Không có dữ liệu phù hợp bộ lọc.')).toBeVisible({ timeout: 15000 });
  await expect(rows).toHaveCount(1, { timeout: 15000 }); // 1 dòng placeholder "Không có dữ liệu..."

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
  // dưới); scope theo modal chứa đúng tiêu đề rồi bấm theo TEXT (không phải accessible-name).
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
  await expect(rows).toHaveCount(1, { timeout: 15000 }); // vẫn chỉ 1 dòng placeholder rỗng — chưa tạo gì

  // Mở lại modal (onHidden() đã reset local data) rồi nhập thật + lưu.
  await page.getByRole('button', { name: 'Tạo mới' }).click();
  await expect(modal).toBeVisible();
  await expect(nameInput).toHaveValue('');

  await modal.getByPlaceholder('VD: WIFI, PROJECTOR').fill(CODE);
  await nameInput.fill(NAME);

  // Nút đầu tiên trong footer luôn là "Lưu" (khuôn footer: Lưu / Lưu và tiếp tục / Đóng) — dùng vị
  // trí thay vì role+name: icon <i> trong slot #prefix của V2BaseButton làm accessible-name không
  // khớp chuỗi "Lưu" thuần (getByRole name:'Lưu', exact:true không bao giờ resolve được).
  await modal.locator('.v2-modal-footer button').first().click();
  await expect(modal).toBeHidden();

  // Đo bằng DOM: bảng phải tăng đúng 1 dòng so với baseline (0 -> 1 bản ghi thật). `toHaveCount` /
  // `toHaveText` tự retry tới hết timeout — không cần đoán đúng response GET nào ứng với thao tác.
  await expect(rows).toHaveCount(1, { timeout: 15000 });
  const firstRow = rows.first();
  await expect(firstRow).toContainText(CODE);
  await expect(firstRow).toContainText(NAME);
  const badge = firstRow.locator('.v2-badge');
  await expect(badge).toHaveText('Hoạt động', { timeout: 15000 });

  // 2. Khóa
  await firstRow.getByTitle('Khóa tiện nghi').click();
  const lockConfirm = page.locator('#confirm-toggle-lock-room-amenity');
  await expect(lockConfirm).toBeVisible();
  // Nút xác nhận (accept) luôn là nút ĐẦU TIÊN trong `.modal-footer` (base-confirm-modal.vue).
  await lockConfirm.locator('.modal-footer button').first().click();
  await expect(badge).toHaveText('Khóa', { timeout: 15000 });

  // 3. Mở khóa
  await firstRow.getByTitle('Mở khóa tiện nghi').click();
  const unlockConfirm = page.locator('#confirm-toggle-lock-room-amenity');
  await expect(unlockConfirm).toBeVisible();
  await unlockConfirm.locator('.modal-footer button').first().click();
  await expect(badge).toHaveText('Hoạt động', { timeout: 15000 });

  // 4. Xóa — dọn sạch dữ liệu test (happy path). `afterEach` ở trên là lưới an toàn nếu ca fail
  // trước bước này.
  await firstRow.getByTitle('Xóa').click();
  const deleteConfirm = page.locator('#confirm-delete-room-amenity');
  await expect(deleteConfirm).toBeVisible();
  await deleteConfirm.locator('.modal-footer button').first().click();
  await expect(page.getByText('Không có dữ liệu phù hợp bộ lọc.')).toBeVisible({ timeout: 15000 });
  await expect(rows).toHaveCount(1, { timeout: 15000 }); // trở lại 1 dòng placeholder rỗng — đã dọn sạch
});
```
