# Review package — Task 10 (bộ e2e chính thức)

## Danh sách spec hiện có trong tests/meeting
_auth-smoke.spec.ts
meeting-room.api.spec.ts
meeting-room.spec.ts
room-amenity.api.spec.ts

### tests/meeting/meeting-room.spec.ts
```ts
/**
 * E2E UI CHÍNH THỨC — Danh mục "Phòng họp" + "Tiện nghi phòng họp" (Task 10, plan
 * quan-ly-phong-hop). Thay thế 3 spec tạm (đã xoá): `_room-ui.smoke.spec.ts`,
 * `_room-amenity-ui.smoke.spec.ts`, `_menu.smoke.spec.ts`. Giữ lại `_auth-smoke.spec.ts`
 * (hạ tầng đăng nhập worktree, không liên quan UI màn này).
 *
 * Worktree riêng (nhánh feat/quan-ly-phong-hop): Nuxt ở :3001, API ở :8001.
 * Chạy:
 *   cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
 *   BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001 \
 *   npx playwright test tests/meeting --project=chromium --no-deps --workers=1
 *
 * CẤM chờ `networkidle` (app polling nền) — mọi chờ đều bám mốc DOM cụ thể hoặc dùng
 * assertion tự retry (`toHaveText`/`toHaveCount`), KHÔNG dùng `Promise.all([waitForResponse, click()])`.
 *
 * Cấu trúc — 5 nhóm `test.describe`, mỗi nhóm tự `configure({mode:'serial'})` + `test.use(...)`
 * storageState riêng (khớp khuôn `_menu.smoke.spec.ts` cũ):
 *   A. Admin — Danh mục phòng họp            (ca 1-4 của brief)
 *   B. Admin — Khuôn giao diện (Ruling R2)    (ca 7 của brief)
 *   C. Admin — Danh mục tiện nghi phòng họp   (ca 5 của brief)
 *   D. Tài khoản thiếu quyền — gate route     (ca 6 của brief)
 *   E. Bảo mật checkin_qr_token — lớp Resource (ca 8 của brief, cấp/thu hồi quyền tạm qua DB)
 *
 * Dữ liệu test gắn hậu tố `Date.now()` (RUN_SUFFIX), mọi mã bắt đầu `E2EOFF_` — beforeAll cấp
 * file quét dọn rác `E2EOFF_` còn sót (lần chạy trước bị kill giữa chừng), afterAll cấp file quét
 * lại lần nữa làm lưới an toàn cuối cùng (không phụ thuộc happy-path của từng nhóm).
 */
import { test, expect, request, APIRequestContext } from '@playwright/test';
import { execFileSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8001';
const ADMIN_TOKEN_FILE = path.join(__dirname, '..', '..', '.auth', 'api-wt.json');
const NOCOST_STATE_FILE = path.join(__dirname, '..', '..', '.auth', 'user-nocost-wt.json');

const ROOMS_URL = '/api/v1/meeting/rooms';
const AMENITIES_URL = '/api/v1/meeting/room-amenities';

const RUN_SUFFIX = Date.now();
const CODE_ROOM = `E2EOFF_RM_${RUN_SUFFIX}`;
const NAME_ROOM = `Phòng họp E2E chính thức ${RUN_SUFFIX}`;
const AM1_CODE = `E2EOFF_AM1_${RUN_SUFFIX}`;
const AM1_NAME = `Tiện nghi E2E chính thức 1 ${RUN_SUFFIX}`;
const AM2_CODE = `E2EOFF_AM2_${RUN_SUFFIX}`;
const AM2_NAME = `Tiện nghi E2E chính thức 2 ${RUN_SUFFIX}`;
const STANDALONE_AMENITY_CODE = `E2EOFF_AMSTD_${RUN_SUFFIX}`;
const STANDALONE_AMENITY_NAME = `Tiện nghi danh mục E2E chính thức ${RUN_SUFFIX}`;
const CODE_SECURITY = `E2EOFF_SEC_${RUN_SUFFIX}`;

const EXPECTED_COLUMNS = [
  'Mã',
  'Tên phòng',
  'Công ty',
  'Vị trí',
  'Sức chứa',
  'Tiện nghi',
  'Người quản lý',
  'Cần duyệt',
  'Cho công ty khác đặt',
  'Trạng thái',
  'Hành động',
];

// ---------------------------------------------------------------------------
// API context dùng chung CẢ FILE (admin, employee id 34) — setup dữ liệu + dọn rác.
// ---------------------------------------------------------------------------
let api: APIRequestContext;

/** Xóa mọi bản ghi `code` bắt đầu bằng `prefix` trong `resourceUrl`, lặp theo trang tới hết
 *  (khuôn copy từ `meeting-room.api.spec.ts::cleanupLeftoverE2eData`). */
async function deleteByCodePrefix(resourceUrl: string, prefix: string) {
  for (let i = 0; i < 20; i++) {
    const res = await api.get(`${resourceUrl}?keyword=${encodeURIComponent(prefix)}&per_page=100`);
    if (res.status() !== 200) break;
    const body = await res.json();
    const rows = Array.isArray(body.data) ? body.data : (body.data?.data ?? []);
    const ids = (Array.isArray(rows) ? rows : [])
      .filter((r: any) => typeof r.code === 'string' && r.code.startsWith(prefix))
      .map((r: any) => r.id);
    if (ids.length === 0) break;
    for (const id of ids) {
      await api.delete(`${resourceUrl}/${id}`).catch(() => {});
    }
  }
}

test.beforeAll(async () => {
  const adminToken = JSON.parse(fs.readFileSync(ADMIN_TOKEN_FILE, 'utf8')).token;
  api = await request.newContext({
    baseURL: API_BASE,
    extraHTTPHeaders: { Accept: 'application/json', Authorization: `Bearer ${adminToken}` },
  });

  // Dọn rác của LẦN CHẠY TRƯỚC bị kill giữa chừng — phòng trước (FK tới tiện nghi qua pivot),
  // tiện nghi sau.
  await deleteByCodePrefix(ROOMS_URL, 'E2EOFF_');
  await deleteByCodePrefix(AMENITIES_URL, 'E2EOFF_');

  // 2 tiện nghi dùng để gắn vào phòng ở Nhóm A (modal chỉ hiện tiện nghi ĐANG hoạt động).
  const a1 = await api.post(AMENITIES_URL, { data: { code: AM1_CODE, name: AM1_NAME } });
  const a2 = await api.post(AMENITIES_URL, { data: { code: AM2_CODE, name: AM2_NAME } });
  expect(a1.status(), 'tạo tiện nghi setup 1').toBe(200);
  expect(a2.status(), 'tạo tiện nghi setup 2').toBe(200);
});

test.afterAll(async () => {
  // Lưới an toàn cuối cùng — dọn MỌI bản ghi `E2EOFF_%` còn sót, kể cả khi 1 nhóm fail giữa
  // chừng chưa kịp dọn qua UI. Phòng trước (FK), tiện nghi sau.
  await deleteByCodePrefix(ROOMS_URL, 'E2EOFF_');
  await deleteByCodePrefix(AMENITIES_URL, 'E2EOFF_');
  await api?.dispose();
});

// ---------------------------------------------------------------------------
// Helper select2 — copy nguyên văn từ `_room-ui.smoke.spec.ts` (đã kiểm chứng chạy ổn trên
// server dev đơn luồng: retry mở dropdown, gõ lọc tránh phải cuộn, chờ options nạp xong trên DOM).
// ---------------------------------------------------------------------------

/** Chờ ô select (bọc trong 1 element chứa `wrapperText`) có ĐỦ option nạp xong. */
async function waitForSelectOptions(
  page: import('@playwright/test').Page,
  wrapperClass: string,
  wrapperText: string,
  minOptions = 1
) {
  await page.waitForFunction(
    ({ wrapperClass, wrapperText, minOptions }) => {
      const wraps = [...document.querySelectorAll(`#modal-meeting-room ${wrapperClass}`)];
      const wrap = wraps.find((el) => (el.textContent || '').includes(wrapperText));
      const select = wrap ? wrap.querySelector('select') : null;
      return !!select && select.options.length >= minOptions;
    },
    { wrapperClass, wrapperText, minOptions },
    { timeout: 20000 }
  );
}

/** Bấm mở dropdown select2, có RETRY (server dev đơn luồng đôi lúc không mở dropdown ở lần click đầu). */
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

/** Mở dropdown rồi chọn 1 option theo text hiển thị (null = chọn option đầu tiên), có RETRY. */
async function pickSelect2Option(
  page: import('@playwright/test').Page,
  fieldLocator: import('@playwright/test').Locator,
  optionText: string | null
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
      // Thử lại ở vòng sau — KHÔNG nhấn Escape (unsavedModalMixin bắt phím này, hiện popup che
      // toàn màn hình làm mọi click sau đứng hình).
    }
  }
  throw new Error(`Không chọn được option "${optionText}" sau 3 lần thử`);
}

// =============================================================================
// NHÓM A — Admin: Danh mục phòng họp (ca 1-4 của brief)
// =============================================================================
test.describe('A. Admin — Danh mục phòng họp', () => {
  test.describe.configure({ mode: 'serial' });
  test.use({ storageState: '.auth/user-wt.json' });

  test('A1. Màn danh sách render đủ 11 cột, đúng thứ tự (đo DOM)', async ({ page }) => {
    await page.goto('/meeting/rooms');
    const searchBox = page.getByPlaceholder('Tìm theo mã, tên phòng, vị trí');
    await expect(searchBox).toBeVisible({ timeout: 20000 });

    const headers = page.locator('table.data-table thead th');
    await expect(headers).toHaveCount(EXPECTED_COLUMNS.length);
    await expect(headers).toHaveText(EXPECTED_COLUMNS);
  });

  test('A2. Tạo phòng qua modal gắn 2 tiện nghi -> bảng +1 dòng, đúng 2 chip, cột Công ty/Người quản lý hiện TÊN', async ({
    page,
  }) => {
    test.setTimeout(90000); // server dev đơn luồng, form-options có lúc mất vài giây mới về

    await page.goto('/meeting/rooms');
    const searchBox = page.getByPlaceholder('Tìm theo mã, tên phòng, vị trí');
    await expect(searchBox).toBeVisible({ timeout: 20000 });

    const rows = page.locator('table.data-table tbody tr');

    // Baseline PHẢI là 0 dòng dữ liệu thật (lọc theo mã duy nhất của lần chạy này).
    await searchBox.fill(CODE_ROOM);
    await searchBox.press('Enter');
    await expect(page.getByText('Không có dữ liệu phù hợp bộ lọc.')).toBeVisible({ timeout: 15000 });
    await expect(rows).toHaveCount(1, { timeout: 15000 });

    await page.getByRole('button', { name: 'Tạo mới' }).click();
    const modal = page.locator('#modal-meeting-room');
    await expect(modal).toBeVisible();

    await modal.getByPlaceholder('VD: A301').fill(CODE_ROOM);
    await modal.getByPlaceholder('VD: Phòng họp tầng 3').fill(NAME_ROOM);

    // Công ty (bắt buộc) — chọn option đầu tiên, không lệ thuộc công ty cụ thể nào.
    const companyField = modal.locator('.col-md-6.mb-3').filter({ hasText: 'Công ty' });
    await waitForSelectOptions(page, '.col-md-6.mb-3', 'Công ty', 1);
    await pickSelect2Option(page, companyField, null);

    await modal.getByPlaceholder('VD: Tầng 3, tòa nhà A').fill('Tầng 5, tòa nhà E2E chính thức');
    await modal.getByPlaceholder('VD: 10').fill('12');

    // Người quản lý (không bắt buộc, nhưng test cần TÊN hiện ở cột danh sách) — options đọc từ
    // $store.state.employees (đã có sẵn lúc login), chọn option đầu tiên.
    const managerField = modal.locator('.col-md-8.mb-3').filter({ hasText: 'Người quản lý' });
    await waitForSelectOptions(page, '.col-md-8.mb-3', 'Người quản lý', 1);
    await pickSelect2Option(page, managerField, null);

    // Tiện nghi — chọn nhiều, đúng 2 tiện nghi setup ở beforeAll. Dropdown TỰ ĐÓNG sau mỗi lần
    // chọn (khác mặc định select2 multi) -> phải mở lại trước khi chọn tiện nghi thứ 2.
    const amenityField = modal.locator('.col-md-12.mb-3').filter({ hasText: 'Tiện nghi' }).first();
    await waitForSelectOptions(page, '.col-md-12.mb-3', 'Tiện nghi', 2);
    await pickSelect2Option(page, amenityField, AM1_NAME);
    await pickSelect2Option(page, amenityField, AM2_NAME);
    // Đóng dropdown — bấm ra vùng trống trong thân modal.
    await modal.locator('.v2-modal-body').click({ position: { x: 5, y: 5 } });

    // Nút đầu tiên trong footer luôn là "Lưu".
    await modal.locator('.v2-modal-footer button').first().click();
    await expect(modal).toBeHidden();

    // Đo bằng DOM: bảng tăng đúng 1 dòng so với baseline.
    await expect(rows).toHaveCount(1, { timeout: 15000 });
    const row = rows.first();
    await expect(row).toContainText(CODE_ROOM);
    await expect(row).toContainText(NAME_ROOM);

    // Cột Tiện nghi (thứ 6) — đúng 2 chip.
    const chips = row.locator('td:nth-child(6) .room-amenity-chip');
    await expect(chips).toHaveCount(2);

    // Cột Công ty (thứ 3) và Người quản lý (thứ 7) phải hiện TÊN thật — không rỗng, không "—",
    // không phải id số thuần (lỗi từng gặp: FE tự tra tên từ danh sách nhân viên ĐANG làm việc,
    // quản lý đã nghỉ việc hiện "—" — xem meeting-room.api.spec.ts ca 7).
    const companyCell = row.locator('td:nth-child(3)');
    const managerCell = row.locator('td:nth-child(7)');
    const companyText = (await companyCell.textContent())?.trim() || '';
    const managerText = (await managerCell.textContent())?.trim() || '';
    expect(companyText.length, 'cột Công ty không được rỗng').toBeGreaterThan(0);
    expect(companyText, 'cột Công ty không được là dấu gạch trống').not.toBe('—');
    expect(companyText, 'cột Công ty phải là TÊN, không phải id số thuần').not.toMatch(/^\d+$/);
    expect(managerText.length, 'cột Người quản lý không được rỗng').toBeGreaterThan(0);
    expect(managerText, 'cột Người quản lý không được là dấu gạch trống').not.toBe('—');
    expect(managerText, 'cột Người quản lý phải là TÊN, không phải id số thuần').not.toMatch(/^\d+$/);
  });

  test('A3. Khóa phòng -> badge đổi Hoạt động -> Khóa; mở khóa -> đổi lại', async ({ page }) => {
    await page.goto('/meeting/rooms');
    const searchBox = page.getByPlaceholder('Tìm theo mã, tên phòng, vị trí');
    await expect(searchBox).toBeVisible({ timeout: 20000 });

    await searchBox.fill(CODE_ROOM);
    await searchBox.press('Enter');
    const rows = page.locator('table.data-table tbody tr');
    await expect(rows).toHaveCount(1, { timeout: 15000 });
    const row = rows.first();
    await expect(row).toContainText(CODE_ROOM);

    const statusBadge = row.locator('td:nth-child(10) .v2-badge');
    await expect(statusBadge).toHaveText('Hoạt động', { timeout: 15000 });

    // Khóa — popup xác nhận render bằng plugin $confirm(), lọc theo tiêu đề (id sinh ngẫu nhiên).
    await row.getByTitle('Khóa phòng họp').click();
    const lockConfirm = page.locator('.modal-content').filter({ hasText: 'Khóa phòng họp' });
    await expect(lockConfirm).toBeVisible();
    // Phòng vừa tạo chưa có phiếu đặt nào -> đúng nhánh "không có phiếu" của onLock().
    await expect(lockConfirm).toContainText('Bạn chắc chắn muốn khóa phòng họp này?');
    await lockConfirm.locator('.modal-footer button').first().click();
    await expect(statusBadge).toHaveText('Khóa', { timeout: 15000 });

    // Mở khóa
    await row.getByTitle('Mở khóa phòng họp').click();
    const unlockConfirm = page.locator('.modal-content').filter({ hasText: 'Mở khóa phòng họp' });
    await expect(unlockConfirm).toBeVisible();
    await unlockConfirm.locator('.modal-footer button').first().click();
    await expect(statusBadge).toHaveText('Hoạt động', { timeout: 15000 });
  });

  test('A4. Phòng chưa có phiếu đặt thì nút Xóa hiện; xóa xong bảng giảm đúng 1 dòng', async ({ page }) => {
    await page.goto('/meeting/rooms');
    const searchBox = page.getByPlaceholder('Tìm theo mã, tên phòng, vị trí');
    await expect(searchBox).toBeVisible({ timeout: 20000 });

    await searchBox.fill(CODE_ROOM);
    await searchBox.press('Enter');
    const rows = page.locator('table.data-table tbody tr');
    await expect(rows).toHaveCount(1, { timeout: 15000 });
    const row = rows.first();
    await expect(row).toContainText(CODE_ROOM);

    // Phòng chưa từng có phiếu đặt -> is_can_delete = true -> nút Xóa PHẢI hiện (ẩn hẳn, không
    // disable, khi không được phép — quy tắc chung của dự án).
    const deleteBtn = row.getByTitle('Xóa');
    await expect(deleteBtn).toBeVisible();

    await deleteBtn.click();
    const deleteConfirm = page.locator('#confirm-delete-meeting-room');
    await expect(deleteConfirm).toBeVisible();
    await deleteConfirm.locator('.modal-footer button').first().click();

    // Bảng giảm đúng 1 dòng -> trở lại placeholder rỗng.
    await expect(page.getByText('Không có dữ liệu phù hợp bộ lọc.')).toBeVisible({ timeout: 15000 });
    await expect(rows).toHaveCount(1, { timeout: 15000 });
  });
});

// =============================================================================
// NHÓM B — Admin: Khuôn giao diện (Ruling R2 của task-10-brief.md — ca 7 của brief)
// Màn danh mục KHÔNG dùng V2Footer (chỉ có ở màn chi tiết/form) -> đo 2 phép đo có thật:
// (a) footer V2BaseModal luôn nằm trong viewport kể cả khi body modal cuộn
// (b) bảng không đẩy cả trang tràn ngang
// =============================================================================
test.describe('B. Admin — Khuôn giao diện (modal footer + không tràn ngang)', () => {
  test.describe.configure({ mode: 'serial' });
  test.use({ storageState: '.auth/user-wt.json' });

  test('B1. Modal footer nằm trong viewport khi body cuộn; trang không tràn ngang', async ({ page }) => {
    await page.goto('/meeting/rooms');
    const searchBox = page.getByPlaceholder('Tìm theo mã, tên phòng, vị trí');
    await expect(searchBox).toBeVisible({ timeout: 20000 });

    // (b) Bảng (nhiều cột) không đẩy cả trang tràn ngang — bảng có thanh cuộn RIÊNG bên trong.
    const overflow = await page.evaluate(() => document.body.scrollWidth - document.body.clientWidth);
    expect(overflow).toBeLessThanOrEqual(0);

    // (a) Mở modal Tạo mới — footer luôn ghim đáy, nằm trong viewport dù cuộn body modal.
    // ⚠️ Đo DOM thật (Playwright MCP) xác nhận: phần tử THỰC SỰ cuộn là `.v2-modal-body` (class
    // riêng của V2BaseModal); `.modal-body` (class do bootstrap-vue tự thêm qua `body-class`) chỉ
    // là khung bọc ngoài, CSS đã tắt cuộn của nó (xem comment trong V2BaseModal.vue) — cuộn nhầm
    // phần tử này sẽ là no-op và làm ca test vô nghĩa.
    await page.getByRole('button', { name: 'Tạo mới' }).click();
    const modal = page.locator('#modal-meeting-room');
    await expect(modal).toBeVisible();

    await page.locator('.modal.show .v2-modal-body').evaluate((el) => {
      el.scrollTop = el.scrollHeight;
    });
    const footer = await page.locator('.modal.show .modal-footer').boundingBox();
    const viewport = page.viewportSize()!;
    expect(footer).not.toBeNull();
    expect(footer!.y).toBeGreaterThanOrEqual(0);
    expect(footer!.y + footer!.height).toBeLessThanOrEqual(viewport.height);

    // Đóng modal (chưa nhập gì -> không kích hoạt cảnh báo "chưa lưu").
    await modal.locator('.v2-modal-footer button').last().click();
    await expect(modal).toBeHidden();
  });
});

// =============================================================================
// NHÓM C — Admin: Danh mục tiện nghi phòng họp (ca 5 của brief)
// =============================================================================
test.describe('C. Admin — Danh mục tiện nghi phòng họp', () => {
  test.describe.configure({ mode: 'serial' });
  test.use({ storageState: '.auth/user-wt.json' });

  test('C1. Tạo -> khóa -> mở khóa -> xóa tiện nghi, đo DOM từng bước', async ({ page }) => {
    test.setTimeout(60000);
    await page.goto('/meeting/room-amenities');
    const searchBox = page.getByPlaceholder('Tìm theo mã, tên tiện nghi');
    await expect(searchBox).toBeVisible({ timeout: 20000 });

    const rows = page.locator('table.data-table tbody tr');

    await searchBox.fill(STANDALONE_AMENITY_CODE);
    await searchBox.press('Enter');
    await expect(page.getByText('Không có dữ liệu phù hợp bộ lọc.')).toBeVisible({ timeout: 15000 });
    await expect(rows).toHaveCount(1, { timeout: 15000 });

    // Tạo
    await page.getByRole('button', { name: 'Tạo mới' }).click();
    const modal = page.locator('#modal-room-amenity');
    await expect(modal).toBeVisible();
    await modal.getByPlaceholder('VD: WIFI, PROJECTOR').fill(STANDALONE_AMENITY_CODE);
    await modal.getByPlaceholder('VD: Wifi / Máy chiếu / Điều hòa / ...').fill(STANDALONE_AMENITY_NAME);
    await modal.locator('.v2-modal-footer button').first().click();
    await expect(modal).toBeHidden();

    await expect(rows).toHaveCount(1, { timeout: 15000 });
    const row = rows.first();
    await expect(row).toContainText(STANDALONE_AMENITY_CODE);
    await expect(row).toContainText(STANDALONE_AMENITY_NAME);
    const badge = row.locator('.v2-badge');
    await expect(badge).toHaveText('Hoạt động', { timeout: 15000 });

    // Khóa
    await row.getByTitle('Khóa tiện nghi').click();
    const lockConfirm = page.locator('#confirm-toggle-lock-room-amenity');
    await expect(lockConfirm).toBeVisible();
    await lockConfirm.locator('.modal-footer button').first().click();
    await expect(badge).toHaveText('Khóa', { timeout: 15000 });

    // Mở khóa
    await row.getByTitle('Mở khóa tiện nghi').click();
    const unlockConfirm = page.locator('#confirm-toggle-lock-room-amenity');
    await expect(unlockConfirm).toBeVisible();
    await unlockConfirm.locator('.modal-footer button').first().click();
    await expect(badge).toHaveText('Hoạt động', { timeout: 15000 });

    // Xóa
    await row.getByTitle('Xóa').click();
    const deleteConfirm = page.locator('#confirm-delete-room-amenity');
    await expect(deleteConfirm).toBeVisible();
    await deleteConfirm.locator('.modal-footer button').first().click();
    await expect(page.getByText('Không có dữ liệu phù hợp bộ lọc.')).toBeVisible({ timeout: 15000 });
    await expect(rows).toHaveCount(1, { timeout: 15000 });
  });
});

// =============================================================================
// NHÓM D — Tài khoản THIẾU quyền: chứng minh gate route còn sống (ca BẮT BUỘC ở đầu
// task-10-brief.md — "vào được trang ≠ gate còn sống"). Vào thẳng URL, không qua menu.
// =============================================================================
test.describe('D. Tài khoản thiếu quyền — gate route trực tiếp còn sống', () => {
  test.describe.configure({ mode: 'serial' });
  test.use({ storageState: '.auth/user-nocost-wt.json' });

  test('D1. /meeting/rooms bị đẩy khỏi trang VÀ bảng KHÔNG render', async ({ page }) => {
    await page.goto('/meeting/rooms');
    await page.waitForURL(/\/pages\/extras\/404/, { timeout: 15000 });
    expect(page.url()).toContain('/pages/extras/404');

    // Đo DOM: KHÔNG có dấu hiệu nào của màn danh sách phòng họp — không chỉ kiểm URL.
    await expect(page.getByPlaceholder('Tìm theo mã, tên phòng, vị trí')).toHaveCount(0);
    await expect(page.locator('table.data-table tbody tr')).toHaveCount(0);
  });

  test('D2. /meeting/room-amenities bị đẩy khỏi trang VÀ bảng KHÔNG render', async ({ page }) => {
    await page.goto('/meeting/room-amenities');
    await page.waitForURL(/\/pages\/extras\/404/, { timeout: 15000 });
    expect(page.url()).toContain('/pages/extras/404');

    await expect(page.getByPlaceholder('Tìm theo mã, tên tiện nghi')).toHaveCount(0);
    await expect(page.locator('table.data-table tbody tr')).toHaveCount(0);
  });
});

// =============================================================================
// NHÓM E — Bảo mật `checkin_qr_token` ở LỚP RESOURCE (ca BẮT BUỘC, re-review Task 6 — xem đầu
// task-10-brief.md). Route `show` đã gắn checkPermission (lớp 1) NÊN tài khoản nocost (không quyền
// nào cả) bị chặn NGAY Ở LỚP ĐÓ — chưa từng chạm lớp 2 (Resource chỉ trả checkin_qr_token cho ai có
// quyền "Quản lý danh mục phòng họp"). Ca này cấp TẠM quyền "Xem danh mục phòng họp" (id 1575, chỉ
// đủ qua lớp route) cho nhân viên id 25 để buộc request phải chạm lớp 2.
//
// Cách xác định ĐÚNG role để cấp (không đoán): nhân viên 25 có 2 dòng trong `employee_has_roles`
// (role_id=100003 `model_type=App\Employee`, role_id=20 `model_type=Modules\Timesheet\Entities\Employee`)
// — CHỈ dòng thứ 2 khớp model auth thật (`Modules\Timesheet\Entities\Employee`, xem
// task-4b-report.md mục 1) nên middleware CheckPermission (dùng `$employee->getAllPermissions()`)
// CHỈ đọc permission qua role_id=20. Đã xác nhận bằng thực nghiệm trực tiếp (curl) trước khi đưa
// vào spec: cấp id 1575 cho role_id=20/company_id=1 -> GET chi tiết trả 200 và KHÔNG có
// `checkin_qr_token`; xoá dòng đó -> trả lại 403 như cũ.
// =============================================================================
test.describe('E. Bảo mật checkin_qr_token — lớp Resource (cấp/thu hồi quyền tạm qua DB)', () => {
  test.describe.configure({ mode: 'serial' });
  test.use({ storageState: '.auth/user-nocost-wt.json' });

  const WORKTREE_API_REPO = '/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api';
  const PERM_ID_XEM = 1575; // 'Xem danh mục phòng họp'
  const ROLE_ID = 20; // role 'Quản lý báo cơm' — dòng employee_has_roles khớp model auth thật
  const COMPANY_ID = 1;

  function readEnvValue(key: string): string {
    const envContent = fs.readFileSync(path.join(WORKTREE_API_REPO, '.env'), 'utf8');
    const match = envContent.match(new RegExp(`^${key}=(.*)$`, 'm'));
    return match ? match[1].trim() : '';
  }

  /** Chạy 1 câu lệnh mysql CLI, đọc credential từ .env của worktree API tại RUNTIME (không hardcode
   *  mật khẩu vào spec). Thử vài đường dẫn binary phổ biến (PATH lúc chạy playwright có thể bị
   *  ghi đè bởi biến PATH truyền tay khi gọi lệnh test). */
  function runMysql(sql: string): string {
    const dbHost = readEnvValue('DB_HOST') || '127.0.0.1';
    const dbDatabase = readEnvValue('DB_DATABASE') || 'hrm_erp';
    const dbPassword = readEnvValue('DB_PASSWORD');
    const candidates = [
      'mysql',
      '/opt/homebrew/opt/mysql@8.0/bin/mysql',
      '/usr/local/bin/mysql',
      '/usr/local/mysql/bin/mysql',
    ];
    let lastErr: any;
    for (const bin of candidates) {
      try {
        return execFileSync(bin, ['-h', dbHost, '-uroot', dbDatabase, '-N', '-e', sql], {
          env: { ...process.env, MYSQL_PWD: dbPassword },
          encoding: 'utf8',
        });
      } catch (e: any) {
        lastErr = e;
        if (e.code !== 'ENOENT') throw e; // lỗi SQL/kết nối thật -> không nuốt, không thử binary khác
      }
    }
    throw lastErr;
  }

  function countGrantedRows(): number {
    const out = runMysql(
      `SELECT COUNT(*) FROM role_has_permissions WHERE permission_id=${PERM_ID_XEM} AND role_id=${ROLE_ID} AND company_id=${COMPANY_ID};`
    );
    return Number(out.trim());
  }

  let adminApi: APIRequestContext;
  let nocostApi: APIRequestContext;
  let securityRoomId: number;

  test.beforeAll(async () => {
    const adminToken = JSON.parse(fs.readFileSync(ADMIN_TOKEN_FILE, 'utf8')).token;
    adminApi = await request.newContext({
      baseURL: API_BASE,
      extraHTTPHeaders: { Accept: 'application/json', Authorization: `Bearer ${adminToken}` },
    });
    const nocostState = JSON.parse(fs.readFileSync(NOCOST_STATE_FILE, 'utf8'));
    const nocostToken = nocostState.origins[0].localStorage.find((i: any) => i.name === 'access_token').value;
    nocostApi = await request.newContext({
      baseURL: API_BASE,
      extraHTTPHeaders: { Accept: 'application/json', Authorization: `Bearer ${nocostToken}` },
    });

    // Idempotent: xoá trước (phòng lần chạy trước bị kill giữa chừng chưa thu hồi) rồi cấp lại
    // đúng 1 dòng — KHÔNG dùng ON DUPLICATE KEY vì cần biết chắc chắn số dòng sau khi cấp là 1.
    runMysql(
      `DELETE FROM role_has_permissions WHERE permission_id=${PERM_ID_XEM} AND role_id=${ROLE_ID} AND company_id=${COMPANY_ID};`
    );
    runMysql(
      `INSERT INTO role_has_permissions (permission_id, role_id, company_id) VALUES (${PERM_ID_XEM}, ${ROLE_ID}, ${COMPANY_ID});`
    );
    expect(countGrantedRows(), 'phải cấp đúng 1 dòng quyền tạm').toBe(1);

    const created = await adminApi.post(ROOMS_URL, { data: { code: CODE_SECURITY, name: 'P.BaoMatQR', company_id: 1 } });
    expect(created.status()).toBe(200);
    securityRoomId = (await created.json()).data.id;
  });

  test.afterAll(async () => {
    // Thu hồi ĐÚNG dòng vừa cấp, kiểm lại bằng truy vấn — chạy dù ca test pass hay fail, DB dùng
    // chung với phiên khác.
    runMysql(
      `DELETE FROM role_has_permissions WHERE permission_id=${PERM_ID_XEM} AND role_id=${ROLE_ID} AND company_id=${COMPANY_ID};`
    );
    expect(countGrantedRows(), 'phải thu hồi sạch quyền tạm').toBe(0);

    if (securityRoomId) await adminApi.delete(`${ROOMS_URL}/${securityRoomId}`).catch(() => {});
    await adminApi?.dispose();
    await nocostApi?.dispose();
  });

  test('E1. UI: nocost CÓ quyền Xem (tạm) -> vào được /meeting/rooms, bảng render, KHÔNG thấy nút Tạo mới', async ({
    page,
  }) => {
    await page.goto('/meeting/rooms');
    // KHÔNG bị đẩy về 404 (khác Nhóm D — ở đây đã có quyền Xem).
    await expect(page).not.toHaveURL(/pages\/extras\/404/);

    const searchBox = page.getByPlaceholder('Tìm theo mã, tên phòng, vị trí');
    await expect(searchBox).toBeVisible({ timeout: 20000 });
    const rows = page.locator('table.data-table tbody tr');
    await expect(rows.first()).toBeVisible({ timeout: 15000 });

    // Chỉ có quyền XEM (không có quyền QUẢN LÝ) -> nút "Tạo mới" (gate bởi canManage) PHẢI ẨN HẲN.
    await expect(page.getByRole('button', { name: 'Tạo mới' })).toHaveCount(0);
  });

  test('E2. API: GET /meeting/rooms/{id} bằng token nocost -> 200 nhưng KHÔNG có checkin_qr_token', async () => {
    const res = await nocostApi.get(`${ROOMS_URL}/${securityRoomId}`);
    expect(res.status()).toBe(200);
    const text = await res.text();
    expect(text).not.toContain('checkin_qr_token');
  });
});
```

### tests/meeting/meeting-room.api.spec.ts (để đối chiếu ca bảo mật)
```ts
/**
 * E2E API — Danh mục "Phòng họp" (Task 6, plan quan-ly-phong-hop).
 *
 * Worktree riêng (nhánh feat/quan-ly-phong-hop): API ở :8001.
 * Token đọc từ e2e/.auth/api-wt.json (tài khoản CÓ quyền quản lý danh mục, employee id 34).
 * Ca "không quyền" dùng token của e2e/.auth/user-nocost-wt.json (tài khoản id 25).
 *
 * Phủ 7 ca theo brief + fix round 1 (review) của Task 6 và Task 8:
 *   1. mã phòng trùng trong CÙNG công ty thì 422, khác công ty thì cho
 *   2. tạo phòng là có sẵn checkin_qr_token
 *   3. gắn nhiều tiện nghi rồi đọc lại đúng danh sách
 *   4. form-options trả tiện nghi đang hoạt động + cấu hình giờ công ty
 *   5. không quyền quản lý danh mục thì POST trả 403
 *   6. không quyền thì GET chi tiết phòng cũng trả 403, KHÔNG lộ checkin_qr_token
 *   7. (mới, Task 8 fix round 1) tạo phòng có company_id + manager_employee_id -> cả response
 *      POST, GET chi tiết, VÀ GET danh sách đều trả company_name/manager_name đúng
 *
 * Fix round 1 (review, Task 6):
 *   - CRITICAL 1: route `show` phải gắn checkPermission (trước đây chỉ có `auth:api`) +
 *     `checkin_qr_token` chỉ trả cho ai có quyền "Quản lý danh mục phòng họp" — thêm ca 6.
 *   - CRITICAL 2: ca "trùng mã" trước đây `expect(await dup.text()).toContain('code')` luôn
 *     pass vì MỌI response đều có key top-level `"code": <httpStatus>` — sửa thành parse JSON
 *     và assert đúng `body.errors.code` (khuôn thật của `BaseRequest::failedValidation()`).
 *   - IMPORTANT 4: mã test gắn hậu tố `Date.now()` (không dùng literal cố định) + `beforeAll`
 *     dọn rác `E2E_%` còn sót từ lần chạy trước bị kill giữa chừng (afterAll không kịp chạy).
 *
 * Fix round 1 (review, Task 8) — mục "việc BE":
 *   - `MeetingRoomResource`/`DetailMeetingRoomResource` trả thêm `company_name`/`manager_name`
 *     (trước đây FE tự tra tên từ `$store.state.employees`, vốn chỉ chứa nhân viên ĐANG làm việc
 *     — `Employee::getAll(true)` — nên phòng có quản lý đã nghỉ việc hiện "—" dù dữ liệu còn
 *     nguyên trong DB). Ca 7 thêm ở đây khẳng định cả 3 nguồn đọc (POST response, GET chi tiết,
 *     GET danh sách) đều trả đúng, không chỉ riêng response tạo mới.
 */
import { test, expect, request, APIRequestContext } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8001';
const ADMIN_TOKEN_FILE = path.join(__dirname, '..', '..', '.auth', 'api-wt.json');
const NOCOST_STATE_FILE = path.join(__dirname, '..', '..', '.auth', 'user-nocost-wt.json');

const ROOMS_URL = '/api/v1/meeting/rooms';
const AMENITIES_URL = '/api/v1/meeting/room-amenities';

// Hậu tố duy nhất cho mỗi lần chạy — tránh đụng mã còn sót của lần chạy trước.
const RUN_SUFFIX = Date.now();
const CODE_A301 = `E2E_A301_${RUN_SUFFIX}`;
const CODE_QR01 = `E2E_QR01_${RUN_SUFFIX}`;
const CODE_AM1 = `E2E_RM_AM1_${RUN_SUFFIX}`;
const CODE_AM2 = `E2E_RM_AM2_${RUN_SUFFIX}`;
const CODE_AM_ROOM = `E2E_AM_ROOM_${RUN_SUFFIX}`;
const CODE_NOPERM = `E2E_NOPERM_${RUN_SUFFIX}`;
const CODE_NOPERM_GET = `E2E_NOPGET_${RUN_SUFFIX}`;
const CODE_NAMES = `E2E_NAMES_${RUN_SUFFIX}`;

test.describe.configure({ mode: 'serial' });

let api: APIRequestContext;
let noPermApi: APIRequestContext;
const createdRoomIds: number[] = [];
const createdAmenityIds: number[] = [];

/** Xóa mọi bản ghi `code LIKE 'E2E_%'` còn sót (lần chạy trước bị kill giữa chừng, afterAll
 *  không kịp dọn). Dọn cả 2 danh mục — phòng trước (FK tới tiện nghi qua pivot), tiện nghi sau. */
async function cleanupLeftoverE2eData() {
  for (let i = 0; i < 20; i++) {
    const res = await api.get(`${ROOMS_URL}?keyword=E2E_&per_page=100`);
    if (res.status() !== 200) break;
    const body = await res.json();
    const rows = Array.isArray(body.data) ? body.data : (body.data?.data ?? []);
    const leftoverIds = (Array.isArray(rows) ? rows : [])
      .filter((r: any) => typeof r.code === 'string' && r.code.startsWith('E2E_'))
      .map((r: any) => r.id);
    if (leftoverIds.length === 0) break;
    for (const id of leftoverIds) {
      await api.delete(`${ROOMS_URL}/${id}`).catch(() => {});
    }
  }

  for (let i = 0; i < 20; i++) {
    const res = await api.get(`${AMENITIES_URL}?keyword=E2E_&per_page=100`);
    if (res.status() !== 200) break;
    const body = await res.json();
    const rows = Array.isArray(body.data) ? body.data : (body.data?.data ?? []);
    const leftoverIds = (Array.isArray(rows) ? rows : [])
      .filter((r: any) => typeof r.code === 'string' && r.code.startsWith('E2E_'))
      .map((r: any) => r.id);
    if (leftoverIds.length === 0) break;
    for (const id of leftoverIds) {
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

  const nocostState = JSON.parse(fs.readFileSync(NOCOST_STATE_FILE, 'utf8'));
  const nocostToken = nocostState.origins[0].localStorage.find((i: any) => i.name === 'access_token').value;
  noPermApi = await request.newContext({
    baseURL: API_BASE,
    extraHTTPHeaders: { Accept: 'application/json', Authorization: `Bearer ${nocostToken}` },
  });

  await cleanupLeftoverE2eData();
});

test.afterAll(async () => {
  // Dọn dữ liệu test tạo ra — DB dùng chung với phiên khác.
  for (const id of createdRoomIds) {
    await api.delete(`${ROOMS_URL}/${id}`).catch(() => {});
  }
  for (const id of createdAmenityIds) {
    await api.delete(`${AMENITIES_URL}/${id}`).catch(() => {});
  }
  await api?.dispose();
  await noPermApi?.dispose();
});

test('1. mã phòng trùng trong CÙNG công ty thì 422, khác công ty thì cho', async () => {
  const created = await api.post(ROOMS_URL, {
    data: { code: CODE_A301, name: 'P.A301', company_id: 1 },
  });
  expect(created.status()).toBe(200);
  const createdBody = await created.json();
  createdRoomIds.push(createdBody.data.id);

  const dup = await api.post(ROOMS_URL, {
    data: { code: CODE_A301, name: 'Khác', company_id: 1 },
  });
  expect(dup.status()).toBe(422);

  // Khuôn body thật của BaseRequest::failedValidation(): { code: 422, errors: { <field>: <msg> } }.
  // res.text().toContain('code') luôn xanh (mọi response đều có key top-level "code": <httpStatus>)
  // nên PHẢI parse JSON rồi assert đúng field lỗi nằm trong `errors`.
  const dupBody = await dup.json();
  expect(dupBody.errors).toHaveProperty('code');
  expect(typeof dupBody.errors.code).toBe('string');
  expect(dupBody.errors.code.length).toBeGreaterThan(0);

  const other = await api.post(ROOMS_URL, {
    data: { code: CODE_A301, name: 'P.A301 CT2', company_id: 2 },
  });
  expect(other.status()).toBe(200);
  const otherBody = await other.json();
  createdRoomIds.push(otherBody.data.id);
});

test('2. tạo phòng là có sẵn checkin_qr_token', async () => {
  const res = await api.post(ROOMS_URL, {
    data: { code: CODE_QR01, name: 'P.QR', company_id: 1 },
  });
  expect(res.status()).toBe(200);
  const id = (await res.json()).data.id;
  createdRoomIds.push(id);

  const detail = await (await api.get(`${ROOMS_URL}/${id}`)).json();
  expect(detail.data.checkin_qr_token).toMatch(/^[0-9a-f-]{36}$/);
  expect(detail.data.is_can_edit).toBe(true);
  expect(detail.data.is_can_delete).toBe(true);
  expect(detail.data.is_can_lock).toBe(true);
  expect(detail.data.status_text).toBe('Hoạt động');
});

test('3. gắn nhiều tiện nghi rồi đọc lại đúng danh sách', async () => {
  const amenity1 = await api.post(AMENITIES_URL, { data: { code: CODE_AM1, name: 'Máy chiếu E2E rooms' } });
  const amenity2 = await api.post(AMENITIES_URL, { data: { code: CODE_AM2, name: 'Bảng trắng E2E rooms' } });
  expect(amenity1.status()).toBe(200);
  expect(amenity2.status()).toBe(200);
  const amenityId1 = (await amenity1.json()).data.id;
  const amenityId2 = (await amenity2.json()).data.id;
  createdAmenityIds.push(amenityId1, amenityId2);

  const created = await api.post(ROOMS_URL, {
    data: { code: CODE_AM_ROOM, name: 'P.Tiện nghi', company_id: 1, amenity_ids: [amenityId1, amenityId2] },
  });
  expect(created.status()).toBe(200);
  const id = (await created.json()).data.id;
  createdRoomIds.push(id);

  const detail = await (await api.get(`${ROOMS_URL}/${id}`)).json();
  const returnedAmenityIds = (detail.data.amenities || []).map((a: any) => a.id).sort();
  expect(returnedAmenityIds).toEqual([amenityId1, amenityId2].sort());

  // Sửa lại chỉ còn 1 tiện nghi -> sync phải bỏ tiện nghi còn lại
  const updated = await api.post(ROOMS_URL, {
    data: { id, code: CODE_AM_ROOM, name: 'P.Tiện nghi', company_id: 1, amenity_ids: [amenityId1] },
  });
  expect(updated.status()).toBe(200);
  const detailAfterUpdate = await (await api.get(`${ROOMS_URL}/${id}`)).json();
  const returnedAmenityIdsAfterUpdate = (detailAfterUpdate.data.amenities || []).map((a: any) => a.id);
  expect(returnedAmenityIdsAfterUpdate).toEqual([amenityId1]);
});

test('4. form-options trả tiện nghi đang hoạt động + cấu hình giờ công ty', async () => {
  const res = await (await api.get(`${ROOMS_URL}/form-options`)).json();
  expect(res.data.config.open_time).toBeTruthy();
  expect(res.data.config.close_time).toBeTruthy();
  expect(typeof res.data.config.checkin_grace_minutes).toBe('number');
  expect(Array.isArray(res.data.amenities)).toBe(true);
  expect(Array.isArray(res.data.companies)).toBe(true);
  // Tiện nghi trả về đều đang hoạt động (status = 1)
  for (const amenity of res.data.amenities) {
    expect(amenity.status).toBe(1);
  }
});

test('5. không quyền quản lý danh mục thì POST trả 403', async () => {
  const res = await noPermApi.post(ROOMS_URL, {
    data: { code: CODE_NOPERM, name: 'X', company_id: 1 },
  });
  expect(res.status()).toBe(403);
});

test('6. không quyền thì GET chi tiết phòng cũng trả 403, không lộ checkin_qr_token', async () => {
  const created = await api.post(ROOMS_URL, {
    data: { code: CODE_NOPERM_GET, name: 'P.KhongQuyenXem', company_id: 1 },
  });
  expect(created.status()).toBe(200);
  const id = (await created.json()).data.id;
  createdRoomIds.push(id);

  const res = await noPermApi.get(`${ROOMS_URL}/${id}`);
  expect(res.status()).toBe(403);
  const text = await res.text();
  expect(text).not.toContain('checkin_qr_token');
});

test('7. tạo phòng có company_id + manager_employee_id -> company_name/manager_name đúng ở cả 3 nguồn đọc', async () => {
  // employee id 34 = chủ token admin (xem comment đầu file) -> chắc chắn tồn tại + có employee_info.
  const managerId = 34;

  const created = await api.post(ROOMS_URL, {
    data: { code: CODE_NAMES, name: 'P.TenCongTyNguoiQuanLy', company_id: 1, manager_employee_id: managerId },
  });
  expect(created.status()).toBe(200);
  const createdBody = await created.json();
  const id = createdBody.data.id;
  createdRoomIds.push(id);

  // Nguồn 1: response của chính POST (DetailMeetingRoomResource) — FE hiện tên ngay sau khi lưu,
  // không phải load lại trang.
  expect(createdBody.data.company_name).toBeTruthy();
  expect(createdBody.data.manager_name).toBeTruthy();
  expect(createdBody.data.manager_name).not.toBe('UNKNOWN'); // Employee::getFullnameAttribute() fallback khi thiếu info

  // Nguồn 2: GET chi tiết (DetailMeetingRoomResource, route show).
  const detail = await (await api.get(`${ROOMS_URL}/${id}`)).json();
  expect(detail.data.company_name).toBe(createdBody.data.company_name);
  expect(detail.data.manager_name).toBe(createdBody.data.manager_name);

  // Nguồn 3: GET danh sách (MeetingRoomResource, route index) — đây là nơi FE màn `/meeting/rooms`
  // đọc để hiển thị cột Công ty/Người quản lý.
  const list = await (await api.get(`${ROOMS_URL}?keyword=${encodeURIComponent(CODE_NAMES)}`)).json();
  const rows = Array.isArray(list.data) ? list.data : (list.data?.data ?? []);
  const row = rows.find((r: any) => r.code === CODE_NAMES);
  expect(row, 'phải tìm thấy đúng phòng vừa tạo trong danh sách').toBeTruthy();
  expect(row.company_name).toBe(createdBody.data.company_name);
  expect(row.manager_name).toBe(createdBody.data.manager_name);
});
```
