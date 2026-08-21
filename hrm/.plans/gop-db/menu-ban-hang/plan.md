# Plan — Menu Bán hàng kiểu MISA (master-detail) vào HRM

> ✅ **FEATURE DONE (2026-08-05)** — user chốt hoàn thành. Đã verify Playwright trên app thật. Tồn admin: báo @junfoke + merge về `gop_db`, dọn `SaleMenuHub.vue`/`pages/sale/menu`.

> Áp dụng CHỈ cho phân hệ Bán hàng (`sale`), KHÔNG ảnh hưởng menu phân hệ khác.
> Design: `design.md` · Mockup style đã duyệt: `menu-mockup.html` · Cấu trúc: artifact.

## Quyết định đã chốt (2026-08-04)
- **Màu accent = màu nhóm phân hệ**: Bán hàng thuộc "Kinh doanh–Tài chính" → **tím `#6B54B8` / `#8F76D3`**.
- **Phê Duyệt giữ 3 cấp** (không lên 4 cấp). Chỉ "Báo cáo bán hàng" là 4 cấp.

## Phase 0 — Kiến trúc tích hợp ✅
- [x] Khảo sát: sale dùng `layout:'default-sidebar'` → render menu qua `training-components/SidebarMenu.vue` (DÙNG CHUNG nhiều phân hệ) + `training-components/Sidebar.vue` (rail trái).
- [x] Chốt: **KHÔNG sửa SidebarMenu/Sidebar chung**. Tạo **component MenuHub + layout riêng** cho Bán hàng. MenuHub = trang landing của phân hệ; click màn → điều hướng tới màn.
- [ ] Giữ `saleItems` cho `resolveSubsystem`/`findSubsystemByLink` (map route→phân hệ) — hub đọc data riêng nhưng link màn phải khớp.

## Phase 1 — Data model: cây menu Bán hàng (tối đa 4 cấp)
- [ ] Định nghĩa cấu trúc mới cho menu Bán hàng: nhóm (cấp1) → mục (cấp2) → [nhóm con (cấp3)] → màn.
      Mỗi node: `label`, `icon`; màn leaf giữ `link`/`erpGhost`/`isShow` như hiện tại.
- [ ] Chuyển dữ liệu từ bảng đã chốt (10 nhóm) + full báo cáo (Báo cáo bán hàng 4 cấp) vào file dữ liệu (giữ/format lại `sale.js` hoặc tách `sale-menu.js`).
- [ ] Bỏ đúng các mục đã chốt (Báo giá mẫu, Nha khoa, Quản lý giá-CTKM, Khách hàng…).

## Phase 2 — Component MenuHub (master-detail thích ứng)
- [ ] Dựng `SaleMenuHub.vue`: cột cấp1 + vùng nội dung.
- [ ] **Thích ứng:** nhóm ≥5 cấp2 → cột cấp2 (master-detail); nhóm <5 → hiện thẳng section+lưới.
- [ ] Render 4 cấp (nhóm con cấp3 = section header, màn cấp4 = lưới 2 cột) — theo mockup.
- [ ] Style theo mockup: cột trắng (cấp1) / cột tint (cấp2) / header teal + marker (cấp3) / hàng mục lưới (cấp4); phân biệt rõ cấp. Responsive.

## Phase 3 — Tính năng: Tìm kiếm / Yêu thích / Gần đây (BỎ ghim, Ẩn/hiện)
- [ ] **Tìm kiếm**: input lọc màn theo tên trên toàn menu, hiện kết quả kèm đường dẫn nhóm.
- [ ] **Yêu thích**: sao ⭐ toggle trên màn; lưu `localStorage` (key theo user + phân hệ); mục "Yêu thích" đầu cột cấp1.
- [ ] **Gần đây**: khi mở màn → đẩy vào danh sách gần đây (localStorage, giới hạn ~10–15); mục/tab "Gần đây".
- [ ] KHÔNG làm: tính năng ghim riêng, nút Ẩn/hiện mục.

## Phase 4 — Icon cho nhóm/mục
- [ ] Chọn icon phù hợp cho 10 nhóm cấp1 + các mục cấp2 chính (users, briefcase, package, file-text, bar-chart, calendar, list, check, settings…).
- [ ] Dùng **inline SVG** (tránh xung đột codepoint Remix Icon — xem feature redesign-man-chon-phan-he). Có thể gom vào data model hoặc map riêng.

## Phase 5 — Điều hướng màn
- [ ] Màn có `link` (route HRM) → `router.push`.
- [ ] Màn `erpGhost`/chưa có link → toast "Tính năng đang phát triển" (hoặc mở ERP nếu có `erpLink`) — tái dùng cơ chế hiện có.
- [ ] Ghi nhận "Gần đây" khi điều hướng.

## Phase 6 — Tích hợp vào phân hệ Bán hàng
- [ ] Gắn MenuHub làm landing/menu của phân hệ Bán hàng (route + layout riêng), KHÔNG đổi phân hệ khác.
- [ ] Kiểm tra topbar/switcher chuyển phân hệ vẫn hoạt động; các phân hệ khác giữ Sidebar tree cũ.

## Phase 7 — Kiểm thử
- [ ] Chạy hrm-client (Node 14): vào Bán hàng thấy MenuHub đúng style/cấu trúc 4 cấp.
- [ ] Test Tìm kiếm / Yêu thích / Gần đây.
- [ ] Test điều hướng màn (link HRM + màn ERP/toast).
- [ ] **Regression: menu các phân hệ khác KHÔNG đổi** (Sidebar tree cũ nguyên vẹn).

## Chờ chốt trước/khi code
- Màu accent (teal vs tím hệ thống) · nhóm nào lên 4 cấp ngoài Báo cáo bán hàng · route landing Bán hàng.

## Phase 8 — Đồng bộ TREE màn con theo cấu trúc HUB mới (Option B) — 2026-08-04
> Vấn đề user báo: chỉ `/sale/dashboard` hiện menu mới (hub); màn con (`/assign/...`, layout `default-sidebar`) vẫn hiện **tree cũ** = `saleItems` (30 nhóm phẳng).
> User chọn **Option B**: hiện tree theo cấu trúc HUB mới (10 nhóm) trên MỌI màn Bán hàng.

Kiến trúc đã xác định:
- Màn con Bán hàng khai `layout: 'default-sidebar'` → `Sidebar.vue` chung → `resolveSubsystem(route).menu` = `saleItems` (sale.js).
- `resolveSubsystem`: `/assign/customers` map về **master-data** (khai trước, cùng độ dài) → bỏ khỏi sale KHÔNG mất. `/assign/report/*` (8) CHỈ ở sale → BẮT BUỘC giữ.

Cách làm (KHÔNG sửa `Sidebar.vue` chung — chỉ đổi data):
- [x] `sale-hub.js`: gắn 8 `link` `/assign/report/*` vào screens của item "Báo cáo Dự án TKT" (đúng thứ tự 1:1); gắn 2 `erpPath` vào screens ERP của "Thông báo". → hub cũng bấm được. Cập nhật comment đầu file.
- [x] `sale.js`: rebuild `saleItems` = `buildSaleTree(saleHubGroups)`:
      - group→node cấp1 (icon class ri-*/fas theo nhóm `GROUP_ICON`, đã dùng trong saleItems cũ nên render OK);
      - nhóm 1 item không có `subs` → promote screens thẳng lên cấp2 (bỏ node "Chức năng" thừa);
      - item có `subs` (Báo cáo bán hàng 4 cấp) → flatten screens vào cấp3 (tree chỉ render 3 cấp);
      - leaf: `{label, link|erpPath, isShow}`; `isShow` lấy từ `SALE_LINK_PERMISSIONS` (map link→mảng quyền, copy từ saleItems cũ).
      - prepend leaf "Tổng quan" → `/sale/dashboard` (quay về hub).
- [x] Giữ `menu: saleItems` ở registry (subsystems.js KHÔNG đổi) → resolveSubsystem/findSubsystemByLink vẫn đủ link.
- [x] Verify transform bằng Node ESM: 11 mục cấp1, maxDepth=3, 30 link + 2 erpPath (đủ, trừ customers), icon đủ 10 nhóm, gate quyền còn.

---
### Checkpoint — 2026-08-04 (Phase 8 — đồng bộ tree màn con, chờ user test Node 14)
Vừa hoàn thành:
- `sale-hub.js`: gắn 8 report link `/assign/report/*` + 2 erpPath ERP vào data hub (hub cũng bấm được).
- `sale.js`: viết lại — `saleItems` giờ SINH từ `saleHubGroups` qua `buildSaleTree()` (cùng nguồn với hub). Có `GROUP_ICON` (10 nhóm), `SALE_LINK_PERMISSIONS` (giữ gate quyền), promote nhóm 1-item, flatten cấp4→cấp3.
- Verify Node: 30 real link + 2 erpPath khớp bản cũ (trừ `/assign/customers` — đã map về master-data nên bỏ không mất). resolveSubsystem không đổi vì đủ link.
- KHÔNG sửa `Sidebar.vue`/`subsystems.js`/`SaleMenuHub.vue`.

Đang làm dở: (không)
Bước tiếp theo (cần user chạy Node 14):
- Vào 1 màn con Bán hàng (vd `/assign/prospective-projects`) → sidebar tree giờ hiện đúng 10 nhóm mới + "Tổng quan" (không còn 30 nhóm cũ).
- Bấm "Tổng quan" → về hub `/sale/dashboard`. Bấm màn có link (Dự án, Báo cáo…) → điều hướng đúng, tree active đúng mục.
- Regression: sidebar các phân hệ KHÁC (assign, finance, human…) KHÔNG đổi.
Blocked: Môi trường phiên Node 12 → chưa chạy Nuxt dev; verify bằng transform + static analysis.

⚠️ Cần user OK: tree cấp3 (danh mục) KHÔNG lọc theo quyền (Sidebar.vue chỉ eval mảng quyền ở cấp1/2) → hiện với mọi user, BE vẫn enforce 403. Hub vốn cũng không lọc quyền. Nếu cần lọc quyền cấp3 phải sửa `Sidebar.vue` (component chung) — hỏi trước.

⚠️ Behavior change đã biết (consistent với hub đã duyệt): tree cấp3 KHÔNG lọc theo quyền (Sidebar.vue chỉ eval mảng quyền ở cấp1/cấp2) → danh mục ở cấp3 hiện với mọi user (BE vẫn enforce 403). Hub vốn cũng không lọc quyền. Cần user OK.

## Phase 9 — MISA-style sidebar màn con (rail nhóm cha + panel menu con bay ra) — 2026-08-04
> Sau khi verify Playwright: tree UBold thường ở màn con KHÔNG đạt. Mục tiêu **đồng nhất toàn bộ menu phân hệ Bán hàng** = mọi màn con phải có menu kiểu HUB/MISA giống trang Tổng quan.
> Logic MISA: sidebar hiện **nhóm cha** → click nhóm cha → hiện **menu con** (panel master-detail bay ra) → chọn menu con → màn hiện **nội dung**, panel đóng.

- [x] `components/sale/SaleHubSidebar.vue`: cột `cats` (10 nhóm cha, icon+chữ, marker viền trái tím) trong `.left-side-menu` + panel `detail` **rộng 680px** bay ra khi click nhóm → tái dùng ĐÚNG logic render `SaleMenuHub` (lưới 2 cột, section header marker, **nav-mode** cột con cho nhóm ≥5 mục). Chọn màn link → `router.push` + đóng; erpPath → mở tab ERP; chưa có → toast. Chung localStorage `sale_hub_fav`/`sale_hub_recent`. Có Tìm kiếm/Yêu thích/Gần đây. ESC/backdrop đóng.
- [x] `layouts/default-sidebar.vue` (GATE): `isSaleSubsystem = resolveSubsystem(route).key==='sale'` → render `SaleHubSidebar` thay `SideBar`; ép bỏ condensed cho sale. Phân hệ khác GIỮ NGUYÊN `SideBar`.
- [x] Offset: rail dùng width theme (content/topbar tự căn); flyout `position:fixed` left=railW, top=topbarH (đo runtime) + backdrop click-đóng.
- [x] Test Playwright THẬT (app chạy Node 12, heap 8GB): cột cats hiện đúng mockup; click "Bán hàng" (nav-mode) → cột con + lưới 2 cột; click "Dự án TKT" (flat) → section CHỨC NĂNG 8 màn; click "Quản lý giải pháp" → điều hướng `/assign/solutions` + panel đóng + rail giữ. Regression: `.sale-cats` không rò rỉ route ngoài sale.

---
### Checkpoint — 2026-08-04 (Phase 9 — MISA sidebar màn con, ĐÃ VERIFY app thật)
Vừa hoàn thành:
- `SaleHubSidebar.vue` (cột cats nhóm cha + panel detail rộng master-detail, bám mockup `menu-mockup.html`) + gate ở `default-sidebar.vue`.
- Verify Playwright trên app thật (127.0.0.1:3000, Node 12 heap 8GB): luồng MISA đủ — click nhóm cha → menu con (nav-mode/flat theo mockup) → chọn màn → nội dung + panel đóng. Ảnh: `misa-1-default/2-flyout/3-flat` ở thư mục ERP-HRM/.
- Regression: sale-cats không xuất hiện ngoài phân hệ Bán hàng.

⚠️ Dev server hiện do Claude khởi động nền (PID cũ, heap 8GB). Nếu user tự quản → kill `pkill -f nuxt` rồi tự chạy `NODE_OPTIONS=--max-old-space-size=8192 yarn dev`.
Blocked: (không).
Polish tuỳ chọn: màu accent (đang tím theo nhóm KD-TC; mockup gốc teal) · panel có thể auto chọn nhóm đang đứng.

### Checkpoint bổ sung — 2026-08-04 (thêm "Tổng quan" + đồng nhất màn Tổng quan)
- Rail `SaleHubSidebar`: thêm mục cấp 1 **"Tổng quan"** (router-link `/sale/dashboard`, icon lưới) ngay trên "Dự án TKT", active khi ở dashboard & chưa mở panel. Thêm listener `$root 'sale-hub:open-group'` để trang overview bấm mở panel.
- `pages/sale/dashboard/index.vue`: đổi từ full-page hub (`SaleMenuHub`, layout `subsystem`, ẩn tree) → **layout `default-sidebar`** ⇒ dùng CHUNG rail MISA như màn con (SIDEBAR ĐỒNG NHẤT). Nội dung = trang overview mới: hero + lưới 10 thẻ nhóm (bấm → `$root.$emit('sale-hub:open-group', i)` mở panel qua rail) + Gần đây + Yêu thích (chung localStorage). Bỏ `body.sale-hub-page`.
- Verify Playwright: `/sale/dashboard` giờ có rail giống hệt màn con; "Tổng quan" active; bấm thẻ "Báo cáo" → panel nav-mode (5 nhóm/60 chức năng, Báo cáo bán hàng 30) mở đúng. Ảnh `misa-6-tongquan-new.png`, `misa-7-ovw-card-flyout.png`.
- `SaleMenuHub.vue` giờ KHÔNG còn dùng (rail thay thế) — giữ file, có thể dọn sau.

### Checkpoint bổ sung — 2026-08-04 (polish panel)
- Panel `.misa-detail` rộng **680→880px** + tên màn cho **xuống dòng** (`white-space:normal; overflow-wrap:anywhere`) thay vì cắt `...` → menu Báo cáo 4 cấp hiện đủ (6 section cấp 3 + màn cấp 4).
- Fix nội dung panel **sát viền trái** (Yêu thích/Gần đây/menu con): gộp padding vào `.misa-detail > div:not(.dtop):not(.navwrap){padding:14px 26px 32px}`, bỏ `.sub` padding riêng.
- Fix **trống dọc**: `.rows` là grid + `flex:1` → `align-content` mặc định của grid = stretch kéo hàng cao 578px; ép `align-content:start` + `.row{align-self:start; margin:0}` (chống đụng Bootstrap `.row`). Verify Playwright OK.
- Panel nới thêm **880→1180px** (`max-width: calc(100vw - 232px)`) → nhóm Báo cáo tiêu đề dài ("Báo cáo thị trường" 14 mục, "So sánh thực hiện KH PTTT theo thời gian chi tiết theo tỉnh TP"…) hiện gọn 1 dòng trong lưới 2 cột. Verify Playwright OK.

### Checkpoint bổ sung — 2026-08-04 (fix thu gọn sidebar condensed)
- Lỗi user báo: thu gọn sidebar (`data-sidebar-size=condensed`, theme ép `.left-side-menu` = **58px** theo `$leftbar-width-condensed` config default) làm rail vỡ style (icon+chữ+search tràn) + panel không co về mép 58px.
- Fix: (1) CSS `body[data-sidebar-size='condensed'] .sale-cats{...}` → ẩn chữ/search/arrow, chỉ còn icon căn giữa; logo thêm icon bag (`.cats-brand-ic`) để condensed vẫn thấy. (2) `MutationObserver` theo dõi `data-sidebar-size`/`class` trên body → gọi `measure()` (+ lần nữa sau 320ms để qua transition) đưa `railW` về 58 ⇒ panel `left`=58 bám mép. (3) Đồng bộ `$parent.isMenuCondensed=false` khi mounted → nút thu gọn bấm 1 lần là ăn (trước bị lệch state phải bấm 2 lần).
- Hover-expand của theme chỉ nhắm `#sidebar-menu > ul > li` (menu cũ) nên KHÔNG áp rail mới → không cần override.
- Verify Playwright: condensed rail chỉ icon (logo/Yêu thích/Gần đây/10 nhóm), panel `left`=58 bám mép, toggle 1-click. State giữ khi chuyển màn con (layout không remount).

### Checkpoint bổ sung — 2026-08-04 (panel trượt mượt khi thu gọn/mở)
- Trước: đo `left` 2 mốc (0ms + 320ms) → panel NHẢY 1 bước sau khi sidebar đã settle.
- Fix: `trackRail()` dùng `requestAnimationFrame` lặp ~32 frame → mỗi frame `measure()` đọc rail width hiện tại (đang animate) và cập nhật `pos.left` ⇒ panel bám KHÍT mép rail theo từng frame, trượt cùng nhịp sidebar. KHÔNG dùng CSS `transition: left` (sẽ gây trễ → hở khoảng giữa rail và panel).
- Verify Playwright (đo interval khi toggle): `flyLeft === railW` ở mọi mốc (207/207 → 91/91 → 58/58) → không nhảy, không hở, mượt.

---
### Checkpoint — 2026-08-04 (wrap up)
Vừa hoàn thành:
- Toàn bộ Phase 1–9 + polish: menu MISA đồng nhất (rail cats + panel detail 1180px) trên mọi màn Bán hàng; trang Tổng quan overview dùng chung rail + mục "Tổng quan" đầu rail; thu gọn sidebar (icon 58px, panel bám mép, trượt mượt rAF, toggle 1-click); panel hiện đủ menu 4 cấp, padding/căn trên đã fix.
- Fix build: resolve 2 conflict git merge (`pages/index.vue` — user; `components/subsystems.js` — Claude, comment-only). Quét toàn repo sạch marker, build lại OK (HTTP 200 index+sale), không OOM.
- Tất cả verify bằng Playwright trên app thật (127.0.0.1:3000, Node 12 heap 8GB).

Đang làm dở: (không)

Bước tiếp theo:
- User review UI cuối trên trình duyệt (hard refresh) toàn luồng: rail + panel nhóm cha/con, Tổng quan overview, Tìm kiếm/Yêu thích/Gần đây, thu gọn/mở, regression phân hệ khác.
- Nếu OK → báo @junfoke + merge nhánh `menu_phan_he_2026` về `gop_db` (cả API nếu có — thực tế feature này chỉ đụng hrm-client).
- Polish tuỳ chọn (nếu user muốn): màu accent tím↔teal · độ rộng panel · dọn `SaleMenuHub.vue` + `pages/sale/menu/` không còn dùng.

Blocked: (không) — build sạch, app chạy được.

**File đã đụng session này (hrm-client):**
- `components/subsystem-menu/sale-hub.js` (gắn report link + erpPath, comment)
- `components/subsystem-menu/sale.js` (rewrite → `buildSaleTree` sinh `saleItems`)
- `components/sale/SaleHubSidebar.vue` (MỚI — rail + panel MISA + condensed + rAF)
- `pages/sale/dashboard/index.vue` (rewrite → trang overview, layout default-sidebar)
- `layouts/default-sidebar.vue` (gate render SaleHubSidebar cho sale)
- `components/subsystems.js` (CHỈ resolve conflict comment, không đổi logic)

---
### Checkpoint — 2026-08-04 (code xong lần 1)
Vừa hoàn thành (Phase 1–6, chưa chạy app test — môi trường Node 12):
- **Data** `components/subsystem-menu/sale-hub.js`: cây 10 nhóm, tối đa 4 cấp (Báo cáo bán hàng 4 cấp), icon nhóm inline SVG, link màn HRM (Dự án TKT/Danh mục/Phê duyệt TKT/Cấu hình) khớp `saleItems`.
- **Component** `components/sale/SaleMenuHub.vue`: master-detail thích ứng (≥5 mục cấp2 → cột dọc; <5 → flat), render 4 cấp; accent **tím theo nhóm** (`SUBSYSTEM_GROUP_META[GROUP_BUSINESS]`); Tìm kiếm + Yêu thích (localStorage) + Gần đây (localStorage); BỎ ghim/ẩn-hiện. Click màn: có link → `router.push`, không → toast "đang phát triển".
- **Trang** `pages/sale/menu/index.vue` (route `/sale/menu`): render hub, layout `default-sidebar`, ẩn rail tree `.left-side-menu` bằng CSS gắn `body.sale-hub-page` (giữ topbar+switcher). KHÔNG sửa component dùng chung.
- **Registry**: sale `home: '/sale/menu'`.

Đang làm dở: (không)
Bước tiếp theo (Phase 7 — cần user chạy Node 14):
- Vào Bán hàng → kiểm hub hiển thị, ẩn tree đúng (selector `.left-side-menu` có thể cần chỉnh theo markup thật), 4 cấp Báo cáo bán hàng, thích ứng nav/flat.
- Test Tìm kiếm / Yêu thích / Gần đây; click màn HRM (Dự án TKT/Danh mục) điều hướng đúng; màn ERP → toast.
- Regression: menu các phân hệ KHÁC không đổi.
- Bổ sung icon cấp 2 (nếu muốn) — hiện mới có icon cấp 1.
Blocked: Môi trường phiên Node 12 → chưa chạy Nuxt dev để verify.

---
### Checkpoint — 2026-08-04 (đã chạy app thật + fix layout)
Vừa hoàn thành:
- Hub chạy được trong app thật tại `/sale/dashboard` (layout `subsystem`, ẩn tree qua `body.sale-hub-page`).
- Fix topbar lệch: `.navbar-custom{left:0}` khi ở hub (trước đó còn offset 58px của sidebar condensed).
- #2 fix: thống kê "X nhóm · Y chức năng" đưa lên **cùng dòng** tiêu đề nhóm (`.dtop` bọc dhead+dsub, 4 chỗ).
- Verify bằng Playwright: hub render đúng, accent tím, master-detail cấp2→cấp3, tree ẩn, topbar full-width.

Đang làm dở / còn mở:
- **#3** (chờ user chốt hướng): màn con `/assign/...` vẫn hiện **rail icon menu cũ** vì dùng layout riêng. Đề xuất: ẩn tree trên MỌI màn thuộc phân hệ Bán hàng (khi `resolveSubsystem==sale`) → chỉ topbar+nội dung, quay lại bằng topbar. Cần user xác nhận vì đụng layout dùng chung (chỉ áp khi context=sale, không ảnh hưởng phân hệ khác).
- **#1** (chờ user cung cấp URL): "Trang tổng quan bị menu che kín" — chưa tái hiện được, cần URL/screenshot cụ thể.
- Bổ sung icon cấp 2 (hiện mới có icon cấp 1) — tuỳ chọn.

Bước tiếp theo: user trả lời #3 (OK ẩn tree toàn phân hệ Bán hàng?) + #1 (URL trang tổng quan lỗi) → làm tiếp.
Blocked: (không) — app chạy được, verify bằng Playwright ổn.

---

## Phase 10 — Redesign gradient wave nền sidebar (2026-08-07, nhánh `update_sidebar_menu`)

> User: "Sửa lại cách thể hiện gradient wave line ở background của sidebar → đẹp + hiện đại hơn".
> Chốt: (1) Sửa ở **mockup HTML trước** (`.plans/gop-db/mockup-chi-tiet-bao-gia/chi-tiet-bao-gia-mockup.html`); (2) Phong cách **flow lines phát sáng**.
> Hiện trạng: `.side-waves` = bó ~44 polyline gãy khúc (opacity .11–.18, stroke .6, cùng 1 gradient teal) → nhìn răng cưa, tĩnh.

- [x] ~~v1 flow lines (6 bezier + comet)~~ — user chê xấu, bỏ.
- [x] **v2 ribbon blend** (theo ảnh tham khảo wavy-line user gửi): 38 đường mảnh (0.5px) bó theo 1 dải, khoảng cách co giãn dọc (`H(y)=hmax·sin`) → thắt eo/xòe như dải lụa xoắn; centerline drift (`C(y)`); gradient dọc cyan→sky→tím→hồng, mờ 2 đầu; sway 34s; `prefers-reduced-motion`. Sinh bằng script Python splice vào mockup. ✅
- [x] CSS `.side-flow` + keyframes `ribbonsway`. ✅
- [x] Verify Playwright (127.0.0.1:8899): render OK (38 path), **0 lỗi console**, screenshot `sidebar-ribbon1.png` — bám sát ảnh tham khảo. ✅
- [x] **v2 tinh chỉnh theo feedback**: giảm còn ~2.4 eo (`wh` 0.0197→0.0085, liền mạch), mảnh hơn (stroke 0.5→0.35), chìm hơn (opacity 0.6→0.4 + gradient nhạt), dạt phải (`midX` 116→134) để text sạch. N=34, step=5 (mượt hơn). Screenshot `sidebar-ribbon2.png`. ✅
- [ ] User duyệt concept → (đợt sau) port sang `SaleHubSidebar.vue` thật.

## Phase 11 — Nội dung Chi tiết báo giá gọn hơn (mockup, 2026-08-07)

> Mục tiêu: giảm chiều cao khối Thông tin chung → đẩy bảng Chi tiết báo giá lên trên, dễ nhìn.

- [x] Font tổng thể nhỏ gọn: body 13→12px, padding card/hàng thu lại, table.grid 12.5→12px. ✅
- [x] Thông tin chung: lưới ô 2 cột, **label+value cùng 1 dòng** (bỏ stacked) → giảm chiều cao; field dài (Dự án/Địa chỉ) span full-width. ✅
- [x] Giảm giá: bỏ callout riêng → **chip gọn `% Giảm giá: Không áp dụng`** đặt cạnh tiêu đề khối "Chi tiết báo giá" (`.disc-chip`). ✅
- [x] Verify Playwright: bảng Chi tiết hiện trọn ngay màn đầu, **0 lỗi console**, screenshot `content2.png`. ✅
- [x] Bỏ `full` ở Địa chỉ → ghép cùng hàng với "Giao hàng (ngày)" (chỉ Dự án còn full-width) → thấp thêm 1 hàng. Screenshot `content3-info.png`. ✅

## Phase 12 — Panel flyout menu: rộng hơn + icon ngữ cảnh (mockup, 2026-08-07)

- [x] Mở rộng `.flyout` 720→**1180px** → menu Báo cáo (nav-mode: subcats 224px + subdetail) hiện đủ 2 cột, không cắt chữ. ✅
- [x] Bộ icon theo ngữ cảnh (`ICONS` + `ICON_RULES` khớp keyword): báo cáo→chart, hợp đồng→contract, báo giá→tag, đơn hàng/bán hàng→cart, kế hoạch→calendar, chỉ tiêu→target, khách hàng/CSKH→users, thị trường→trending, công nợ→coins, duyệt→check, thiết lập→settings, bảo hành→tool, vật tư→box, yêu cầu→inbox, tra cứu→search, thông báo→bell, dự án→project. Áp cho leaf row (`pickIcon`) + cột subcats (`scatIcon`). ✅
- [x] Reorder rule: đưa 'báo cáo' xuống fallback → nhóm con "Báo cáo X" nhận icon theo lĩnh vực (thị trường↗/CSKH👥/bán hàng🛒/công nợ🪙/dự án📁). Screenshot `menu-baocao2.png`, **0 lỗi console**. ✅
- [x] **Feedback**: leaf item KHÔNG cần icon riêng mỗi cái → dùng **1 icon file-text chung** (`LEAFIC`); giữ icon đa dạng ở cấp 2 (`scatIcon`). ✅
- [x] Nền panel `.flyout`: hiệu ứng background nhẹ (radial glow brand góc trên-phải + teal góc dưới-trái + linear gradient dọc mờ). Screenshot `menu-baocao3.png`, **0 lỗi console**. ✅

## Phase 13 — PORT style "chốt" vào code THẬT (2026-08-07, nhánh `update_sidebar_menu`)

> User: "áp dụng style vừa chốt cho: sidebar, Topbar, header bảng, Tiêu đề card vào phân hệ bán hàng".
> Cũng hiện thực hoá feature `update-style-ban-hang` (dùng chung file `assets/scss/sale-theme.scss`).
> ⚠️ Gate `.sale-theme` hiện = `HUB_SUBSYSTEMS` (user đã sửa `isSaleSubsystem`) → style áp cho NHÓM phân hệ hub, không chỉ sale. Cần hỏi user có siết riêng sale không.
> Cách: TẤT CẢ override trong `assets/scss/sale-theme.scss` dưới `.sale-theme`, KHÔNG sửa V2/theme chung. Verify Playwright trên dev server thật (localhost:3000).

- [x] Khảo sát điểm override thật (Explore): card=`section.tp-card`, tiêu đề=`.tp-section-title`(+ vài `h5.mb-0`), bảng=`table.data-table` (không phải b-table), topbar=`.navbar-custom` (SidebarMenu.vue), rail=`.sale-cats` (SaleHubSidebar.vue). ✅
- [x] **Sidebar**: rail navy (gradient #123c74→#0a1c3d) + ribbon (background-image data-URI SVG ~46KB, 28 đường) + đảo token chữ sáng (`--ink/--muted/--hov/--line`), active pill sky `#6fb2ff` (!important vì `--acc` inline). ✅
- [x] **Topbar** `.navbar-custom`: nền navy + chữ/icon sáng (`.topbar-page-title`, svg). ✅
- [x] **Header bảng** `.data-table thead th` (+ b-table + generic): nền teal gradient `#eefafb→#e2f5f6`, chữ `#0a7c88`, viền dưới `#0a99a7`. ✅
- [x] **Tiêu đề card** `.tp-section-title` (+ `h5.mb-0` trong tp-card): teal `#0a99a7` + thanh accent `::before`. ✅
- [x] Verify Playwright app thật: `/sale/dashboard` (sidebar+topbar) + `/sale/quotations` (bảng+card). Screenshot `real-sale-dashboard.png`, `real-sale-list2.png`. Lỗi console duy nhất = 404 API (data, không phải CSS). ✅
- [x] **Chốt scope: giữ cho cả 14 phân hệ hub** (sale, master-data, insurance, customer-care, finance, admin, asset, iso, kpi, legal, operation, production, recruitment, tax). Không siết riêng sale.
- [x] **Fix nền trắng logo-box**: `.logo-box` (khu icon+tên phân hệ) có `background:#fff` từ theme UBold đè lên nền navy → thêm `.sale-theme .sale-cats .logo-box{ background:transparent!important; border-bottom-color:rgba(255,255,255,.10) }`. Verify `logo-fixed.png`, 0 lỗi console. ✅
- [x] **Fix logo icon đỏ**: `.cats-brand-ic` là `<img>` asset màu → tô trắng bằng `filter: brightness(0) invert(1)`. Verify `logo-white.png`. ✅
- [x] **Tối ưu ribbon**: data-URI 46.7KB → **14.7KB** (giảm ~68%): số nguyên, implicit lineto comma-separated, N=24 step=12. Vẫn đẹp, verify. ✅
- [x] **Verify đa màn**: theme áp cho hub subsystems khác (Tài chính `/finance/dashboard` navy+ribbon+logo trắng ✓). Header bảng `.data-table` teal + card title teal xác nhận lại trên `/sale/quotations` (th color #0a7c88, border #0a99a7, title #0a99a7). ✅
- [x] **Phát hiện scope**: các màn `assign_business`/`settings` (mà Explore trích) thuộc **module Giao việc**, KHÔNG phải hub → topbar trắng, không áp theme (đúng, ngoài 14 phân hệ hub). ✅
- [ ] Tồn nhẹ: chưa tìm được màn hub dùng `b-table` để test live (sale dùng `.data-table`); selector b-table đã thêm phòng hờ. Contrast icon topbar khi nhiều nút — theo dõi.

## Phase 14 — Polish bổ sung sidebar/topbar/panel (2026-08-07)

> User: (1) box tên phân hệ nổi bật hơn; (2) icon phân hệ ấn tượng hơn; (3) topbar thêm gradient+waveline; (4) áp style panel menu mới vào menu các phân hệ.

- [x] **#1 Box tên phân hệ nổi bật**: `.logo-box` gradient sáng (sky/cyan) + viền + shadow + đường sky glow `::after`; `.subsystem-name` bold + letter-spacing + text-shadow. (sale-theme.scss) ✅
- [x] **#2 Icon phân hệ ấn tượng**: `.cats-brand-ic` (img) tô trắng + `drop-shadow` glow sky + phóng 27px. ✅
- [x] **#3 Topbar gradient + waveline**: `.navbar-custom` thêm layer wave ngang (data-URI SVG ~4KB, 14 đường, gradient sky→cyan) + radial glow góc phải, đồng nhất sidebar. ✅
- [x] **#4 Panel menu**: (a) nền gradient `.misa-detail` (sale-theme.scss); (b) **icon ngữ cảnh cấp 2** `.scat` — port `SCAT_ICONS`+`SCAT_RULES`+`scatIcon()` vào `SaleHubSidebar.vue` (dùng chung 14 hub); leaf 1 icon + panel 1180px vốn đã có. ✅
- [x] Verify Playwright: `stageA.png` (box+icon+topbar), `real-panel-icons.png` (cấp 2 có icon: Dự án TKT/thị trường/CSKH/bán hàng/công nợ). **0 lỗi console**. ✅
- [x] **Fix #1 logo-box "rơi xuống"**: rail có `padding-top:60px` (chừa topbar) → logo-box ở y=60 lộ dải navy trống. Kéo lên đỉnh bằng `margin-top:-60px; height:60px` → top=0, căn tầm topbar. Verify `fix3.png`. ✅
- [x] **Fix #2 topbar**: bỏ waveline (không hợp) → **gradient navy + ánh sáng** (2 radial bloom sky/cyan + linear sáng dần sang phải + inset top highlight). ✅
- [x] **Fix #3 panel accent xanh**: `--acc: #6B54B8` (tím) set inline trên rail → override `.sale-theme .misa-detail { --acc:#2E71C3; --acc2:#4C90D9 }` → active scat/marker panel = xanh brand, đồng bộ sidebar. ✅
- [x] **Wave line mép dưới topbar**: `.navbar-custom::after` = SVG wave sáng (2 đường, gradient sky→cyan, ~1KB) + `drop-shadow` glow, `background-size:100% 12px`. ⚠️ Bỏ `position:relative` (làm co topbar fixed → lệch); `fixed` đã đủ non-static cho `::after`. ✅
- [x] **Màu icon menu theo mockup**: palette `CAT_COLORS` (10 màu port từ mockup) cycle theo index nhóm → `:style="{'--ic':catColor(i)}"` trên group cat; inline `--ic` cho fav(#f2b93b)/recent(#86d0ff)/Tổng quan(#7aa7dd); CSS `.cat .cat-ic{color:var(--ic,muted)}`, active vẫn sky. Áp cho cả 14 hub. Verify `fix-final.png`. ✅

## Phase 15 — Style form báo giá + header bảng #20d9ea (2026-08-07)

> User: (1) áp style màn báo giá vào form tạo/sửa/xem chi tiết; (2) header bảng dùng #20d9ea.
> Phát hiện: form báo giá (`pages/sale/quotations/create.vue`, `_id/edit.vue`, `_id/index.vue`) là sale route → ĐÃ có `.sale-theme` + đã dùng card/tiêu đề teal riêng. Điểm thiếu duy nhất = header bảng sản phẩm/summary đang trong suốt.

- [x] Header bảng đổi teal → **#20d9ea** (gradient `#20d9ea→#12c3d6`, chữ `#063b43`, viền `#0b93a6`) trong `sale-theme.scss`. ✅
- [x] Mở rộng selector phủ bảng form: `.quotation-edit-table` (tạo/sửa), `.quotation-view-table` (xem), `.summary-table`, `.breakdown-summary-table`, `.info-table` + generic `.table thead th` + `.data-table` (list). ✅
- [x] Verify Playwright màn **Tạo** (`/sale/quotations/create`): header bảng sản phẩm cyan #20d9ea, form khớp mockup (info grid + tiêu đề teal). Screenshot `form-header-cyan.png`. ✅
- [x] **Xem chi tiết verify LIVE** (`/sale/quotations/80` = BG-2026-00080): header bảng `quotation-view-table` cyan #20d9ea ✓, info grid + tiêu đề teal ✓, sidebar/topbar/wave ✓. Screenshot `detail-80.png`, **0 lỗi console**. (Sửa dùng cùng `quotation-edit-table` như Tạo đã verify.)

## Phase 16 — Fix lỗi "không tìm được báo giá" (alias route BE, 2026-08-07)

> User báo `/sale/quotations/1` lỗi "không tìm được báo giá". Điều tra: KHÔNG do style (phiên này chỉ sửa `sale-theme.scss` + `SaleHubSidebar.vue`, không đụng API/route/pages).
> Nguyên nhân: **lệch route FE↔BE**. FE gọi `sale/quotations/*` (commit `2f1f5818d` Tri Lee 05/08 — dời phân hệ Bán hàng sang /sale) nhưng BE (cả `gop_db` lẫn `menu_phan_he_2026`) chỉ có `assign/quotations`, chưa từng có `sale/quotations` → mọi màn báo giá 404. (BE local vừa `checkout gop_db → menu_phan_he_2026`.)

- [x] Thêm **alias route** ở `hrm-api/Modules/Assign/Routes/api.php`: gói toàn bộ route nhóm quotations (dòng 449-517) thành closure `$quotationRoutes`, đăng ký **2 prefix**: `/assign/quotations` (cũ) + `/sale/quotations` (FE mới). 1 nguồn định nghĩa, không lệch. ✅
- [x] `php -l` OK; `route:clear` (không có cache); `route:list` không chạy được CLI (PermissionHelper cần auth — không liên quan). ✅
- [x] Verify browser: list `/sale/quotations` tải 20 dòng (hết 404/toast), detail `/sale/quotations/80` tải data thật. ✅
- [ ] ⚠️ Đây là **fix nhanh cho BE local** (nhánh `menu_phan_he_2026`, chưa commit). Migration đúng bài (dời route quotations sang `Modules/Sale` prefix `/v1/sale`) thuộc chủ backend/@junfoke. Các endpoint `sale/*` KHÁC (nếu FE gọi) có thể còn 404 — xử lý tương tự khi gặp.

## Phase 17 — Header bg + Thông tin chung theo mockup (2026-08-07)

> User: (1) header bảng style background theo mockup; (2) Thông tin chung áp sắp xếp + style theo mockup.

- [x] **Header bảng** đổi từ cyan đậm → **gradient nhẹ kiểu mockup** `linear-gradient(180deg,#eafcfe,#d2f4f9)` + chữ teal `#0a7c88` + viền accent **#20d9ea**. (sale-theme.scss) ✅
- [x] **Thông tin chung (.info-table)**: style lưới ô theo mockup — nhãn `<th>` nền `#f7f9fc` xám nhạt + gridline mảnh `#eef1f6` + bo góc 10px + compact 6px/14px. Phủ cả Tạo/Sửa/Xem (đều dùng `.info-table`). ✅
- [x] Verify: `detail-styled.png` (xem chi tiết BG-2026-00080) + `create-styled.png` (tạo, input trong lưới không vỡ). **0 lỗi CSS**. ✅
- [x] **Header th `white-space: nowrap`**: tiêu đề cột không xuống dòng ("Giá nhập (VNĐ)", "Thành tiền nhập"…) — bảng có scroll ngang sẵn. Verify `header-nowrap.png`. ✅
- [x] **Ô "Loại tiền tệ" 1 dòng**: `_id/index.vue` — "Bảng giá: …" đổi từ `<div>` (block, xuống dòng) → `<span class="ml-2">` inline → "VNĐ  Bảng giá: Bán lẻ" cùng dòng, hàng đều. Verify `currency-oneline.png`. ✅
- [x] **Chip Bảng giá / Giảm giá theo mockup**: thêm `.sale-chip` (`.info` xanh brand, `.disc` cam) vào `sale-theme.scss`; markup `_id/index.vue`: "Bảng giá: Bán lẻ" → chip xanh, "Giảm giá: Không có" → chip cam "**%** Không áp dụng" (icon %). Verify `chips.png`. ✅
- [x] **Chuyển Giảm giá lên header card "Chi tiết báo giá"** (như mockup): bỏ toolbar Giảm giá riêng, chèn vào `.products-title` cạnh tiêu đề (nút "Ẩn cột chi tiết" vẫn ml-auto phải). Verify `discount-header.png`. ✅
- [ ] Note "sắp xếp": KHÔNG reorder field vì màn thật có thêm field (YCBG/BOM/Giải pháp/Hạng mục cho báo giá không trực tiếp) mà mockup lược bỏ — reorder theo mockup sẽ mất field. Layout thật đã 2 cột compact. Nếu user muốn đổi cặp field cụ thể → làm riêng.

---

### Checkpoint — 2026-08-08 (wrap up — port style Bán hàng vào code thật)
Vừa hoàn thành (Phase 10–17):
- **Mockup** (chi-tiet-bao-gia-mockup.html): ribbon lụa sidebar, nội dung gọn, panel menu (icon cấp 2 + nền + wave/màu).
- **Code THẬT** áp cho **14 phân hệ hub** qua `.sale-theme` (không đụng V2 chung): sidebar navy+ribbon+box tên nổi bật+icon phân hệ glow+**màu icon menu theo mockup**; topbar navy gradient + **wave line mép dưới**; header bảng **#20d9ea** (gradient nhẹ + viền + nowrap); tiêu đề card teal; panel menu (icon ngữ cảnh cấp 2 + nền gradient + accent XANH đồng bộ).
- **Form báo giá** (tạo/sửa/xem): Thông tin chung style lưới ô + "Loại tiền tệ" 1 dòng + **chip Bảng giá (xanh) / Giảm giá (cam)** theo mockup + **Giảm giá đưa lên header card "Chi tiết báo giá"**.
- **Fix 404 báo giá**: alias route BE `sale/quotations` (`Modules/Assign/Routes/api.php`).

File đã đụng (đều CHƯA commit):
- hrm-client: `assets/scss/sale-theme.scss`, `components/sale/SaleHubSidebar.vue`, `pages/sale/quotations/_id/index.vue`
- hrm-api: `Modules/Assign/Routes/api.php` (alias route, nhánh `menu_phan_he_2026`)

Đang làm dở: (không)
Bước tiếp theo:
- User review tổng thể trên trình duyệt (14 phân hệ hub + form báo giá). Nếu OK → báo @junfoke + commit/merge về `gop_db` (client) và xử lý migration route `sale/*` đúng bài (BE).
- Tùy chọn: (a) reorder cặp field Thông tin chung theo mockup nếu muốn; (b) tối ưu/verify thêm màn dùng b-table; (c) dọn mockup nếu không cần.
Blocked: (không) — app chạy được, mọi thay đổi đã verify Playwright, 0 lỗi CSS.
