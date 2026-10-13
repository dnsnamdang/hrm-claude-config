# Review package — Task 9 (menu phân hệ Meeting)

## git diff --numstat
11	2	components/subsystem-menu/meeting.js

## git diff
diff --git a/components/subsystem-menu/meeting.js b/components/subsystem-menu/meeting.js
index 5af57690e..9bdb15512 100644
--- a/components/subsystem-menu/meeting.js
+++ b/components/subsystem-menu/meeting.js
@@ -33,6 +33,11 @@ export const meetingItems = [
                 link: '/assign/meeting_cancel_reason',
                 isShow: ['Quản lý danh mục lý do hủy cuộc họp', 'Xem danh mục lý do hủy cuộc họp'],
             },
+            {
+                label: 'Tiện nghi phòng họp',
+                link: '/meeting/room-amenities',
+                isShow: ['Quản lý danh mục tiện nghi phòng họp', 'Xem danh mục tiện nghi phòng họp'],
+            },
         ],
     },
     {
@@ -47,8 +52,12 @@ export const meetingItems = [
         icon: 'ri-door-open-line',
         isMenuCollapsed: false,
         subItems: [
-            // Sheet bôi vàng cả 2 mục = chưa xây dựng, dự kiến làm sau.
-            { label: 'Danh sách phòng họp' },
+            // Sheet bôi vàng: "Đăng ký phòng họp" chưa xây dựng, dự kiến làm sau (Phase 2).
+            {
+                label: 'Danh sách phòng họp',
+                link: '/meeting/rooms',
+                isShow: ['Quản lý danh mục phòng họp', 'Xem danh mục phòng họp'],
+            },
             { label: 'Đăng ký phòng họp' },
         ],
     },

### e2e/tests/meeting/_menu.smoke.spec.ts
```ts
/**
 * SMOKE UI — Menu phân hệ Meeting (Task 9, plan quan-ly-phong-hop).
 * Tạm thời (spec `_`) — verify việc khai `components/subsystem-menu/meeting.js` (Task 9) render đúng
 * và LỚP CHẶN URL TRỰC TIẾP còn sống (registry menu này chính là dữ liệu mà
 * `middleware/checkPermission.js` tra `isShow` để chặn — xem task-9-brief.md).
 *
 * Phân hệ Meeting nằm trong `HUB_SUBSYSTEMS` (components/subsystem-menu/hub.js) -> sidebar KIỂU HUB
 * (component `components/sale/SaleHubSidebar.vue`, class `.sale-cats`/`.misa-detail`), KHÔNG PHẢI
 * cây UBold `#side-menu` cũ. Đã dò DOM thật bằng Playwright trước khi viết spec này (script dump
 * tạm, đã xoá) — panel nhóm mở ra render `.misa-detail .rows .row[data-k]`, mỗi `.row` có `href`
 * nếu màn đã có link, KHÔNG có `href` nếu màn chưa xây dựng (chỉ mở toast "đang phát triển").
 *
 * ⚠️ Đã đo THẬT: panel "Danh mục" của tài khoản admin worktree (.auth/user-wt.json) chỉ hiện
 * ĐÚNG 2 dòng (Loại meeting, Tiện nghi phòng họp) chứ KHÔNG phải 3 — mục "Lý do hủy cuộc họp" bị
 * `isScreenVisible()` lọc mất vì tài khoản admin worktree KHÔNG có quyền "Quản lý/Xem danh mục lý
 * do hủy cuộc họp" (gap quyền có sẵn từ trước, KHÔNG liên quan tới thay đổi của Task 9 — đã kiểm:
 * file `components/subsystem-menu/meeting.js` không đụng tới mục đó). Assertion dưới đây bám
 * đúng số đo THẬT (2), không bám tổng số khai trong file.
 *
 * Worktree riêng (nhánh feat/quan-ly-phong-hop): Nuxt ở :3001, API ở :8001.
 * Chạy: PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" BASE_URL=http://127.0.0.1:3001 \
 *   API_BASE=http://127.0.0.1:8001 npx playwright test tests/meeting/_menu.smoke.spec.ts \
 *   --project=chromium --no-deps --workers=1
 *
 * CẤM chờ `networkidle` (app polling nền) — chờ mốc DOM cụ thể.
 */
import { test, expect } from '@playwright/test';

test.describe.configure({ mode: 'serial' });

/** Bấm 1 nhóm ở rail (`.sale-cats .cat`) theo tên, chờ panel `.misa-detail` bay ra thật. */
async function openRailGroup(page: import('@playwright/test').Page, groupLabel: string) {
  const cat = page.locator('.sale-cats .cat').filter({ hasText: groupLabel }).first();
  await expect(cat).toBeVisible({ timeout: 20000 });
  await cat.click();
  const panel = page.locator('.misa-detail');
  await expect(panel).toBeVisible({ timeout: 10000 });
  await expect(panel.locator('.dhead')).toHaveText(groupLabel);
  return panel;
}

test.describe('Meeting — sidebar hub, admin (đủ quyền)', () => {
  test.use({ storageState: '.auth/user-wt.json' });

  test('Nhóm Quản lý phòng họp: 2 mục, Danh sách phòng họp có link và render bảng thật', async ({ page }) => {
    test.setTimeout(60000);
    await page.goto('/meeting/dashboard');

    const panel = await openRailGroup(page, 'Quản lý phòng họp');
    const rows = panel.locator('.rows .row');
    await expect(rows).toHaveCount(2);

    const roomsRow = rows.filter({ hasText: 'Danh sách phòng họp' });
    await expect(roomsRow).toHaveAttribute('href', '/meeting/rooms');

    // Mục "Đăng ký phòng họp" vẫn PHẢI treo trống (Phase 2 mới điền link) — không có href.
    const registerRow = rows.filter({ hasText: 'Đăng ký phòng họp' });
    await expect(registerRow).toHaveCount(1);
    expect(await registerRow.getAttribute('href')).toBeNull();

    await roomsRow.click();
    await page.waitForURL('**/meeting/rooms', { timeout: 15000 });

    const searchBox = page.getByPlaceholder('Tìm theo mã, tên phòng, vị trí');
    await expect(searchBox).toBeVisible({ timeout: 20000 });
    // Bảng thật sự render ra DOM (>= 1 dòng: dữ liệu thật hoặc dòng placeholder rỗng) — không chỉ URL đổi.
    const tableRows = page.locator('table.data-table tbody tr');
    await expect(tableRows.first()).toBeVisible({ timeout: 15000 });
    expect(await tableRows.count()).toBeGreaterThan(0);
  });

  test('Nhóm Danh mục: Tiện nghi phòng họp có link và render bảng thật', async ({ page }) => {
    test.setTimeout(60000);
    await page.goto('/meeting/dashboard');

    const panel = await openRailGroup(page, 'Danh mục');
    const rows = panel.locator('.rows .row');
    // Đo THẬT = 2 (Loại meeting, Tiện nghi phòng họp) — xem giải thích gap quyền ở đầu file.
    await expect(rows).toHaveCount(2);

    const amenityRow = rows.filter({ hasText: 'Tiện nghi phòng họp' });
    await expect(amenityRow).toHaveAttribute('href', '/meeting/room-amenities');

    await amenityRow.click();
    await page.waitForURL('**/meeting/room-amenities', { timeout: 15000 });

    const searchBox = page.getByPlaceholder('Tìm theo mã, tên tiện nghi');
    await expect(searchBox).toBeVisible({ timeout: 20000 });
    const tableRows = page.locator('table.data-table tbody tr');
    await expect(tableRows.first()).toBeVisible({ timeout: 15000 });
    expect(await tableRows.count()).toBeGreaterThan(0);
  });
});

test.describe('Meeting — vào thẳng URL, tài khoản THIẾU quyền', () => {
  test.use({ storageState: '.auth/user-nocost-wt.json' });

  test('/meeting/rooms bị đẩy khỏi trang, bảng KHÔNG render', async ({ page }) => {
    await page.goto('/meeting/rooms');
    await page.waitForURL(/\/pages\/extras\/404/, { timeout: 15000 });
    expect(page.url()).toContain('/pages/extras/404');

    // Đo DOM: KHÔNG có dấu hiệu nào của màn danh sách phòng họp (gate còn sống, không chỉ URL đổi).
    await expect(page.getByPlaceholder('Tìm theo mã, tên phòng, vị trí')).toHaveCount(0);
    await expect(page.locator('table.data-table')).toHaveCount(0);
  });

  test('/meeting/room-amenities bị đẩy khỏi trang, bảng KHÔNG render', async ({ page }) => {
    await page.goto('/meeting/room-amenities');
    await page.waitForURL(/\/pages\/extras\/404/, { timeout: 15000 });
    expect(page.url()).toContain('/pages/extras/404');

    await expect(page.getByPlaceholder('Tìm theo mã, tên tiện nghi')).toHaveCount(0);
    await expect(page.locator('table.data-table')).toHaveCount(0);
  });
});
```
