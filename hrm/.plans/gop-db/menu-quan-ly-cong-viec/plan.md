# Menu hub cho phân hệ Quản lý công việc (assign) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans để thực thi task-by-task. Bước dùng checkbox (`- [ ]`).
>
> Nhánh `gop_db` (client) · @namdangit · Spec: `docs/superpowers/specs/gop-db/2026-08-10-menu-quan-ly-cong-viec-design.md`

**Goal:** Đưa phân hệ Quản lý công việc (`assign`) sang sidebar hub navy+teal như 14 phân hệ mới, giữ nguyên toàn bộ menu nghiệp vụ.

**Architecture:** Kích hoạt chuẩn hub bằng cách thêm `'assign'` vào `HUB_SUBSYSTEMS`; bổ sung khái niệm "nút rail đi thẳng" (nav-link) để giữ 3 màn lẻ cấp 1 vốn bị `deriveHubGroups` bỏ. Thuần FE, không đụng BE/DB/route.

**Tech Stack:** Nuxt 2 (Vue 2), Vuex, SCSS. Không có unit-test framework → verify bằng **dev compile + Playwright 1440px**.

## Global Constraints

- Chỉ đụng 2 file: `components/subsystem-menu/hub.js`, `components/sale/SaleHubSidebar.vue`.
- **KHÔNG** đổi cấu trúc mảng `groups` (giữ search/Yêu thích/Gần đây/đếm số của mọi phân hệ hub).
- **KHÔNG** sửa component V2 chung; mọi style navy+teal đã nằm dưới `.sale-theme`.
- Không commit git khi chưa được yêu cầu.
- Interpolation Vue chuẩn (`{{ }}`) — đây là hrm-client (Nuxt), không phải AngularJS.

---

## Phase 1 — FE sidebar hub cho assign

### Task 1: Thêm nav-link API + bật hub cho assign (`hub.js`)

**Files:**
- Modify: `components/subsystem-menu/hub.js` (mảng `HUB_SUBSYSTEMS` ~dòng 25–42; thêm hàm sau `hubGroupsFor` ~dòng 162)

**Interfaces:**
- Consumes: `HUB_SUBSYSTEMS`, `HAND_WRITTEN`, `isScreenVisible` (đã có trong file).
- Produces:
  - `deriveHubNavLinks(menu): Array<{n, link, icon, isShow}>`
  - `hubNavLinksFor(subsystem, permissions): Array<{n, link, icon, isShow}>`

- [x] **Step 1: Thêm `'assign'` vào `HUB_SUBSYSTEMS`**

Trong block `// Đã chuyển code sang HRM`, thêm dòng `'assign',` (đặt sau `'sale',`):

```js
export const HUB_SUBSYSTEMS = [
    // Đã chuyển code sang HRM
    'sale',
    'assign',
    'master-data',
    'insurance',
    'customer-care',
    'finance',
    // ... (giữ nguyên phần còn lại)
```

- [x] **Step 2: Thêm 2 hàm export ở cuối file** (sau `hubGroupsFor`)

```js
/**
 * Link lẻ cấp 1 của cây menu (có `link`, KHÔNG có `subItems`) — sẽ thành nút rail đi thẳng
 * trong sidebar hub. `deriveHubGroups` cố tình bỏ các mục này; hàm này thu lại để render riêng.
 */
export function deriveHubNavLinks(menu) {
    return (menu || [])
        .filter((item) => !Array.isArray(item.subItems) && item.link && item.link !== '#')
        .map((item) => ({ n: item.label, link: item.link, icon: item.icon, isShow: item.isShow }))
}

/**
 * Nút rail đi thẳng của 1 phân hệ hub.
 * - Bỏ link trùng trang Tổng quan (`/<key>/dashboard`) vì rail đã có nút Tổng quan built-in.
 * - Lọc theo quyền bằng `isScreenVisible` (giống màn/mục khác).
 * - Phân hệ HAND_WRITTEN (sale) tự khai đủ cấu trúc menu → trả [].
 *
 * @param {object} subsystem bản ghi trong SUBSYSTEMS
 * @param {Array} [permissions] $store.state.permissions; bỏ trống → không lọc quyền
 */
export function hubNavLinksFor(subsystem, permissions) {
    if (!subsystem || !HUB_SUBSYSTEMS.includes(subsystem.key)) return []
    if (HAND_WRITTEN[subsystem.key]) return []
    const dashPath = `/${subsystem.key}/dashboard`
    const strip = (p) => String(p || '').split('?')[0].split('#')[0].replace(/\/$/, '')
    let links = deriveHubNavLinks(subsystem.menu).filter((l) => strip(l.link) !== dashPath)
    if (permissions !== undefined) links = links.filter((l) => isScreenVisible(l, permissions))
    return links
}
```

- [x] **Step 3: Kiểm tra dev compile không lỗi**

Server dev đang chạy ở cổng 3000 (hot-reload). Đọc log task dev, xác nhận không có `ERROR`/`Module not found` mới sau khi lưu `hub.js`.

- [x] **Step 4: Commit** — đã commit + push lên `gop_db`

```bash
git add components/subsystem-menu/hub.js
git commit -m "feat(assign): bật chuẩn hub + API nav-link cho màn lẻ cấp 1"
```

---

### Task 2: Render nút rail đi thẳng (`SaleHubSidebar.vue`)

**Files:**
- Modify: `components/sale/SaleHubSidebar.vue` (import ~dòng 129; template rail sau "Tổng quan" ~dòng 36; computed sau `groups()` ~dòng 212; thêm method)

**Interfaces:**
- Consumes: `hubNavLinksFor` (Task 1), `this.subsystem`, `this.$store.state.permissions`, class CSS `.cat.cat-nav`, `.cat-ic`, `.cat-ic-font`, helper `isSvgIcon`, `catColor`, `close`.
- Produces: nút rail `router-link.cat.cat-nav` render giữa "Tổng quan" và `v-for groups`.

- [x] **Step 1: Mở rộng import `hubNavLinksFor`**

Dòng 129 hiện tại:
```js
import { hubGroupsFor } from '@/components/subsystem-menu/hub'
```
Sửa thành:
```js
import { hubGroupsFor, hubNavLinksFor } from '@/components/subsystem-menu/hub'
```

- [x] **Step 2: Thêm computed `navLinks`** (ngay sau computed `groups()` ~dòng 212)

```js
        navLinks() {
            return hubNavLinksFor(this.subsystem, this.$store.state.permissions)
        },
```

- [x] **Step 3: Thêm method `isNavActive`** (trong khối `methods`, cạnh `close`)

```js
        isNavActive(link) {
            const strip = (p) => String(p || '').split('?')[0].split('#')[0].replace(/\/$/, '')
            return strip(this.$route.path) === strip(link)
        },
```

- [x] **Step 4: Render nút rail lẻ** — chèn NGAY SAU router-link "Tổng quan" (đóng ở dòng 36 `</router-link>`), TRƯỚC `<a v-for="(g, i) in groups"` (dòng 37)

```html
                <router-link
                    v-for="(nav, k) in navLinks"
                    :key="'nav-' + k"
                    :to="nav.link"
                    class="cat cat-nav"
                    :class="{ on: isNavActive(nav.link) }"
                    :style="{ '--ic': catColor(k) }"
                    @click.native="close"
                >
                    <svg v-if="isSvgIcon(nav.icon)" class="cat-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" v-html="nav.icon"></svg>
                    <i v-else class="cat-ic cat-ic-font" :class="nav.icon"></i>
                    <span>{{ nav.n }}</span>
                </router-link>
```

- [x] **Step 5: Kiểm tra dev compile không lỗi**

Đọc log dev server (cổng 3000), xác nhận không `ERROR in`/`Module not found` mới sau khi lưu.

- [x] **Step 6: Commit** — đã commit + push lên `gop_db`

```bash
git add components/sale/SaleHubSidebar.vue
git commit -m "feat(assign): render nút rail đi thẳng cho màn lẻ cấp 1 trong sidebar hub"
```

---

### Task 3: Verify bằng Playwright (1440px) + regression

**Files:** không sửa (chỉ kiểm thử).

- [x] **Step 1: Mở `/assign/my-todo`** — xác nhận:
  - Rail navy+teal (`.sale-theme` áp), topbar "QUẢN LÝ CÔNG VIỆC" + logo đúng.
  - Có nút "Tổng quan" + 3 nút lẻ: **Lịch làm việc của tôi**, **Công việc của tôi**, **Cập nhật tiến độ Task**.
  - Nút "Lịch làm việc của tôi" được highlight (`on`) khi đang ở `/assign/my-todo`.
  - Chụp screenshot lưu vào scratchpad.

- [x] **Step 2: Bấm nút lẻ** (vd "Công việc của tôi") → điều hướng thẳng tới `/assign/my-job`, panel không bung, highlight chuyển sang nút đó.

- [x] **Step 3: Bấm 1 nhóm** (vd "Giao việc - Công tác") → panel bay ra, có các màn con bấm được.

- [x] **Step 4: Nhóm ERP** (vd "Hồ sơ công việc") → panel hiện màn xám mờ (chưa có link).

- [x] **Step 5: Regression** — mở `/sale/quotations`: sidebar Bán hàng KHÔNG đổi (vẫn 0 nút lẻ, groups/search/Yêu thích như cũ). Mở thêm 1 phân hệ hub khác (vd `/finance/...`) xác nhận rail bình thường.

- [x] **Step 6: Wrap up** — cập nhật `plan.md` (đánh `[x]`, checkpoint) + `STATUS.md`.

---

## Self-review (đã chạy)

- **Spec coverage:** §3.1→Task 1 Step 1; §3.2→Task 1 Step 2 + Task 2; §3.3→tự động (không cần task); §6 kiểm thử→Task 3. Đủ.
- **Placeholder scan:** không có TBD/TODO; code cụ thể ở mọi step.
- **Type consistency:** `hubNavLinksFor`/`deriveHubNavLinks`, field `{n, link, icon, isShow}`, `navLinks`, `isNavActive` đồng nhất giữa Task 1 và Task 2.

---

## Phase 2 — Áp chuẩn hub cho phân hệ Đào tạo (training)

> Tái dùng nguyên hạ tầng Phase 1. Training dùng `layout: 'default-sidebar'`, menu `menuItemsTraining` toàn mục có `subItems` (trừ "Tổng quan" → `/training/dashboard`, đã có nút built-in) → `hubNavLinksFor` trả `[]`. Chỉ cần bật hub.

### Task 4: Bật hub cho training (`hub.js`)

**Files:** Modify `components/subsystem-menu/hub.js` (mảng `HUB_SUBSYSTEMS`).

- [x] **Step 1: Thêm `'training'` vào `HUB_SUBSYSTEMS`** (block "Đã chuyển code sang HRM", sau `'assign'`).
- [x] **Step 2: Kiểm tra dev compile không lỗi** (log cổng 3000) — không lỗi.
- [x] **Step 3: Verify Playwright 1440** — `/training/courses`: rail navy+teal, topbar "ĐÀO TẠO", 12 nhóm, panel "Khoá học · 9 chức năng" bung đúng, không nút lẻ (đúng, training chỉ có dashboard). Regression assign/sale không đổi.
- [x] **Step 4: Commit** — đã commit + push lên `gop_db`.

---

### Checkpoint — 2026-08-10
Vừa hoàn thành: TOÀN BỘ feature — Phase 1 (assign) + Phase 2 (training). ĐÃ COMMIT + PUSH lên `gop_db`.
- Phase 1 (assign): thêm `'assign'` vào `HUB_SUBSYSTEMS`; hạ tầng nav-link (`deriveHubNavLinks`/`hubNavLinksFor` trong `hub.js`) + render nút rail đi thẳng trong `SaleHubSidebar.vue` cho 3 màn lẻ (my-todo/my-job/tasks daily-report); 6 nhóm ERP xám; verify Playwright 1440 OK.
- Phase 2 (training): thêm `'training'` vào `HUB_SUBSYSTEMS` (không có nút lẻ → chỉ 1 dòng); verify `/training/courses` rail "ĐÀO TẠO" + 12 nhóm, panel bung OK.
- Kèm fix trước đó: import `pages/assign/quotations/_id/index.vue` (`@/components/sale/*` → `@/components/assign/*`).
- Regression: Bán hàng (/sale/dashboard) 0 error, không đổi.
Đang làm dở: (không)
Bước tiếp theo (tùy chọn): (1) dashboard overview kiểu hub cho `/assign/dashboard` + `/training/dashboard`; (2) áp hub cho nhóm `layout: 'default'` (Chấm công/Tính lương/Quyết định/Quản lý cơm/Thông tin nhân sự) — cần thêm việc vì dùng topbar ngang.
Blocked:
