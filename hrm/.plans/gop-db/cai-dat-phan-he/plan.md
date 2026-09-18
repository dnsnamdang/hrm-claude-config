### Checkpoint — 2026-09-17 (Đã test kỹ trên local)
Vừa hoàn thành: test thật `HideErpMenusMenuSettingSeeder` trên stack local (BE 8006 + FE 3006,
DB `local_hrm_erp`), 2 tài khoản: `namdangit@gmail.com` (thuộc "Nhân sự xem đầy đủ") và
`anhbear023@gmail.com` (nhân viên thường).

🔴 **Lỗi phát hiện khi test UI — đã sửa**: mục "Tổng quan" (`/<phân hệ>/dashboard`) của 7 phân hệ
được giữ (sale, presale, meeting, insurance, admin, master-data, operation) là mục MỚI nên bị ẩn
theo quy tắc → bấm vào phân hệ ở trang chọn phân hệ rơi thẳng vào "Tính năng đang phát triển",
phân hệ hiện mà không vào được. Đã thêm quy tắc: CỬA VÀO phân hệ luôn giữ hiện.
Danh sách rút từ 73 → **66 khoá** (10 phân hệ + 56 mục).

Kết quả test sau khi sửa:
- 282/282 màn đang dùng của `tpe`: KHÔNG màn nào bị seeder chặn
- 13/13 cửa vào phân hệ được giữ: vào được (trước khi sửa: 7 cái chết)
- 11 đường dẫn phải chặn (finance/production/kpi/asset/iso/safety-5s/tax/recruitment/
  customer-care/lookup + `setting/subsystems`): chặn đúng, ra `/feature-unavailable?reason=hidden`
- 5 màn ngoại lệ user chốt: vào được
- UI tài khoản thường: 10 phân hệ hiện dạng "Tính năng đang phát triển" (xám, mất link);
  `/assign/quotations` (màn cũ) vào bình thường; `/assign/contracts` (mục port ERP) bị chặn
- Tài khoản "xem đầy đủ": vào được `/timesheet/setting/subsystems` dù mục đã ẩn (lối thoát OK)
- Màn cấu hình: "Đang bật 381/888 mục", Tài chính 0/133, CSKH sau bán 0/27, Bán hàng 14/198
- **Bấm Lưu trên UI: 66/66 khoá seeder còn nguyên** → khoá seeder khớp chính xác khoá FE sinh ra
- Chạy seeder lần 2: "Đã ẩn thêm 0 menu; 66 khoá đã có sẵn" (idempotent); dòng admin tự tick
  trước đó (`human::Báo cáo`) không bị đè

Đang làm dở: chưa commit/push; DB local vẫn đang giữ dữ liệu seeder để user tự xem
Bước tiếp theo: user xem lại rồi quyết commit + chạy trên server
Blocked: không có

### Checkpoint — 2026-09-17 (Seeder ẩn menu chưa mở)
Vừa hoàn thành: `database/seeders/HideErpMenusMenuSettingSeeder.php` — ẩn sẵn menu chưa mở cho
người dùng, để bản gộp DB nhìn giống bản `tpe` đang chạy. 73 khoá: 10 phân hệ (tax, recruitment,
kpi, asset, iso, safety-5s, production, customer-care, finance, lookup) + 63 mục menu mới.
Danh sách KHÔNG gõ tay: bundle `components/subsystems.js` của cả 2 nhánh bằng esbuild rồi đối
chiếu, khoá sinh bằng chính `buildMenuKey()` của FE (đã kiểm: 73/73 khớp registry, 0 trùng, 0 khoá
vượt 191 ký tự).
⚠️ Điểm phải cẩn thận: `gop_db` xếp lại menu nên **91 màn đang dùng của `tpe`** (quyết định, bảo
hiểm, dự án TKT, báo giá, khách hàng…) nay nằm trong phân hệ MỚI `operation` / `presale` /
`master-data` / `sale` / `insurance` / `meeting` / `admin` → KHÔNG được ẩn cả phân hệ, chỉ ẩn từng
mục mới bên trong.
Quyết định của user: giữ hiện 5 màn cũ bị đổi chỗ (phân quyền, quy định chung/làm thêm/nghỉ, cài
đặt); ẩn mục "Cài đặt phân hệ".
Đang làm dở: chưa chạy seeder trên server nào
Bước tiếp theo: chạy `php artisan db:seed --class=HideErpMenusMenuSettingSeeder` rồi mở lại màn
`/timesheet/setting/subsystems` kiểm tra tick
Blocked: không có

# Plan — Cài đặt phân hệ

**Nhánh:** `gop_db` (worktree `worktrees/gop_db-api` + `worktrees/gop_db-client`) · cổng dev 3002 / 8003
**Design:** `design.md` · **Spec:** `docs/superpowers/specs/gop-db/2026-09-14-cai-dat-phan-he-design.md`

## Phase 1 — Backend: lưu trữ & API

### BE
- [x] Migration `create_menu_settings_table`: `menu_key` (191, unique), `is_visible`, `created_by`, `updated_by`, timestamps
- [x] Model `App\Models\MenuSetting extends BaseModel` + `$fillable`
- [x] Service `MenuSettingService`: `index()` trả `hidden_keys`; `store()` ghi đè toàn bộ trong transaction (`query()->delete()` + insert, KHÔNG `truncate()`)
- [x] `store()` ghi bản sao 3 key `master_settings` (`use_erp`/`use_decision`/`use_rice`) cho logic nghiệp vụ BE
- [x] `index()` đọc 100% từ `menu_settings` — KHÔNG đọc ngược `master_settings` (đổi theo yêu cầu user 2026-09-14)
- [x] Controller `MenuSettingController` + Request validate `hidden_keys` (mảng, phần tử ≤ 191, ≤ 2000 phần tử)
- [x] Route `/v1/menu-settings`: `GET` (auth:api), `PUT` (auth:api + `checkPermission:Quản lý phân quyền`)
- [x] Test tay bằng tinker/curl: GET rỗng → `[]`; PUT 3 key → GET trả đúng; PUT lại → dọn key cũ

## Phase 2 — FE: lớp lọc dùng chung

### FE
- [x] `utils/menuVisibility.js`: `buildMenuKey` (`node.menuKey ?? đường dẫn nhãn ĐẦY ĐỦ`, cắt 191 ký tự bằng hậu tố băm), `buildLabelPathKey`, `filterMenuTree`, `filterHubGroupsByVisibility`, `filterHubNavLinks`, `isSubsystemHidden`, `isSubsystemVisible`
- [x] `store/actions.js :: nuxtClientInit` nạp `/api/v1/menu-settings` → `state.menuHiddenKeys` (lỗi API ⇒ `[]` = hiện hết, ghi rõ lý do fail-open)
- [x] `store/state.js` khai `menuHiddenKeys: []`
- [x] ~~Cắm lọc `Topbar.vue`~~ → **không phải sửa**: `layouts/default.vue` truyền menu đã lọc qua prop
- [x] Cắm lọc: `training-components/Sidebar.vue :: filterMenuItems/isShowMenuParent/isShowSubItemMenu`
- [x] Cắm lọc: `subsystem-menu/hub.js :: hubGroupsFor + hubNavLinksFor` (thêm tham số `hiddenKeys`)
- [x] Đóng dấu `menuKey` tại NGUỒN: `deriveHubGroups`/`deriveHubNavLinks` (hub suy từ cây) và `sale.js :: buildSaleTree`/`toLeaf`/`itemScreens` (cây suy từ hub) — để 2 bề mặt của cùng phân hệ dùng chung khoá
- [x] `subsystems.js`: `getSubsystemMenu(path, hiddenKeys)` + `getVisibleMenu(subsystem, hiddenKeys)`
- [x] Đo va chạm khoá trên toàn bộ 24 phân hệ: sidebar cây 829 khoá / **0 va chạm**, sidebar hub 662 khoá / **0 va chạm**
- [x] Cắm lọc: `pages/index.vue :: isShow` + `SubsystemSwitcher.vue :: isShow`
- [x] Kiểm: chưa cấu hình gì thì menu 24 phân hệ không đổi so với trước (so ảnh)

## Phase 3 — FE: màn cấu hình

### FE
- [x] Mục "Cài đặt phân hệ" trong `components/SettingSlidebar.vue`, gate `hasAPermission('Quản lý phân quyền')`
- [x] `pages/timesheet/setting/subsystems/index.vue`: `layout: 'setting'`, gate quyền ở đầu màn
- [x] Cây cấu hình: 5 nhóm → phân hệ (accordion, mặc định thu gọn) → menu nhiều cấp; đọc thẳng registry
- [x] Checkbox tri-state (indeterminate) cho cấp cha; tick cha KHÔNG đụng key con
- [x] Bỏ phân hệ `hidden: true`; giữ phân hệ `external` (1 tick, không menu con)
- [x] Nhãn phụ "chưa có màn" màu `#6b7280` cho mục placeholder (KHÔNG dùng `.text-muted`)
- [x] Ô tìm kiếm lọc theo nhãn + tự mở nhánh khớp; nút Mở rộng/Thu gọn tất cả; đếm "Đang hiện x/y mục"
- [x] Nút Lưu trong `V2Footer` + `unsavedChangesMixin` + `markFormSaved()`
- [x] Lưu xong: nạp lại `menuHiddenKeys` (menu đổi ngay, không F5), toast, ở lại màn

## Phase 4 — Dọn màn Cài đặt cũ & chặn URL

> ⚠️ **Phải lên cùng đợt với Phase 2-3.** Đồng bộ là một chiều (màn mới → `master_settings`);
> để sót 3 checkbox cũ thì tick ở màn Cài đặt sẽ làm menu lệch với nghiệp vụ
> (`use_rice = 0` nhưng menu Quản lý cơm vẫn hiện → vào màn bị đá 404).

### FE
- [x] Gỡ 3 checkbox ERP / Quyết định / Cơm khỏi `pages/timesheet/setting/setting-master/index.vue` (giữ "Sử dụng CRM")
- [x] `middleware/menu-visibility.js`: bỏ qua `/timesheet/setting/*`, `/login`, `/pages/*`, `/feature-unavailable`, `/client`; khớp prefix dài nhất; redirect `/feature-unavailable`
- [x] Đăng ký middleware trong `nuxt.config.js` (sau `checkPermission`)

### BE
- [x] Giữ nguyên `MasterSettingService::TRACKED_FIELDS` (lịch sử cũ vẫn đọc được nhãn)

## Phase 5 — UI + Kiểm thử tự động

### FE (UI pass 2 — sau khi user phản hồi "nhìn xấu")
- [x] Dựng lại bố cục **2 cột** (trái: 22 phân hệ + badge `x/y`; phải: cây menu của phân hệ đang chọn)
- [x] Khung nền cho vùng cây + giới hạn 860px; hàng hover; đường dẫn hướng nét đứt theo cấp
- [x] Badge đếm căn phải, chip "chưa có màn", dải cảnh báo cam khi tắt cả phân hệ
- [x] Làm mờ các mục con khi bị cha/phân hệ ẩn (trước đó vẫn xanh như đang bật)
- [x] **Sửa lệch mũi tên ▸ và ô tick**: rule toàn cục `input:not(:placeholder-shown) + label` (floating label,
      `assets/scss/custom-theme.scss`) đẩy nhãn lên 10px -> huỷ bằng `transform: none !important` TRONG
      `<style scoped>`; đo lại: mũi tên/ô tick/chữ cùng tâm 331.8px
- [x] Kiểm không rò sang màn khác: quét 6 màn, các màn khác giữ nguyên transform toàn cục
      (-9.59/-17.5/-21.19/-37.59px), chỉ màn mới là `none`; `git status` không có file SCSS/CSS nào bị sửa

## Phase 5b — Kiểm thử (chạy khi user yêu cầu)

- [x] **Bộ test tự động `.plans/gop-db/cai-dat-phan-he/e2e_test.py`** (Playwright Python) — 60 kịch bản,
      5 tài khoản khác quyền, chạy `/opt/homebrew/bin/python3 .plans/gop-db/cai-dat-phan-he/e2e_test.py`
- [x] Kết quả lần chạy 2026-09-14: **60/60 PASS**
- [x] 8 kịch bản ở mục 9 của spec (menu nguyên trạng · ẩn mục lẻ cây · ẩn mục hub · ẩn cả phân hệ · `use_rice` đồng bộ · không quyền · chồng với quyền · API lỗi)
- [x] Kiểm CRLF: `git diff --stat` không phình bất thường ở các file cũ đã sửa

### Checkpoint — 2026-09-14 (XONG Phase 1-5, đã test thật)
Vừa hoàn thành: **toàn bộ chức năng + test tay bằng Playwright trên cổng 3002/8003.**

Phase 4: gỡ 3 checkbox ERP/Quyết định/Cơm khỏi màn Cài đặt (giữ "Sử dụng CRM");
`middleware/menu-visibility.js` + đăng ký trong `nuxt.config.js` (sau `checkPermission`);
`pages/feature-unavailable.vue` nhận `?reason=hidden` để nói đúng lý do ("Chức năng đang được ẩn"),
thay vì thông báo nâng cấp phiên bản của luồng bản quyền.

**3 lỗi phát hiện khi test và đã sửa:**
1. Gọi `markFormSaved()` trong `mounted` ⇒ cờ `unsavedIgnore` bật vĩnh viễn ⇒ **cảnh báo chưa lưu
   không bao giờ hiện**. Sửa: `markFormPristine()` sau khi nạp; sau khi lưu thì `unsavedIgnore = false`
   + `markFormPristine()` (màn này ở lại sau khi lưu nên không dùng `markFormSaved()`).
2. Tắt cả phân hệ nhưng bộ đếm vẫn ghi `14/14 mục` ⇒ sửa `countVisible()` trả 0 khi phân hệ bị ẩn.
3. Tìm kiếm lọc đúng nhưng kết quả nằm trong nhánh thu gọn nên **không nhìn thấy gì** ⇒ thêm
   `effectiveExpandedMap`: đang tìm thì mở hết nhánh còn lại, xoá từ khoá thì về đúng trạng thái cũ.

**Kết quả test** (16 kịch bản, xem mục 9 spec + phần bổ sung):
menu nguyên vẹn khi chưa cấu hình · ẩn mục lẻ (topbar mất `/timesheet/timesheet_details`, mục cùng
nhóm còn nguyên) · ẩn cả nhóm (mất "Báo cáo") · ẩn phân hệ (mất card ở màn chọn phân hệ) ·
phân hệ hub Tài chính: "Quản lý tiền" 7→6 chức năng, mất ở cả rail lẫn lưới Tổng quan ·
chặn URL mục lẻ + route con `/finance/bill-incomes/123` → `/feature-unavailable?reason=hidden` ·
`use_rice` đồng bộ 0/1 · chống tự khoá (tắt cả phân hệ Chấm công vẫn vào được màn cấu hình) ·
bật lại cha giữ nguyên tick con (35/41) · tri-state đúng · bộ đếm 848 → 833 → 806 ·
cảnh báo chưa lưu (Thoát/Ở lại) · tài khoản KHÔNG có quyền: sidebar ẩn mục, URL → 404, API PUT → 403 ·
màn Cài đặt chỉ còn "Sử dụng CRM". DB đã trả về sạch (0 dòng, 3 cờ cũ = 1).
CRLF giữ nguyên ở toàn bộ 8 file cũ đã sửa.
Đang làm dở: không có
Bước tiếp theo: user nghiệm thu; chưa commit (theo quy tắc dự án)
Blocked: không còn

### Checkpoint — 2026-09-14 (Phase 3 xong)
Vừa hoàn thành: **Phase 3 — màn cấu hình**. `pages/timesheet/setting/subsystems/index.vue`
(layout `setting`, gate `Quản lý phân quyền`, cây 5 nhóm → phân hệ → menu nhiều cấp, accordion mặc
định thu gọn, ô tìm kiếm + bôi vàng phần khớp, Mở rộng/Thu gọn tất cả, đếm "Đang hiện x/y mục",
checkbox tri-state, nhãn phụ "chưa có màn", `V2Footer` + `unsavedChangesMixin`) và component đệ quy
`components/setting/subsystem/MenuVisibilityNode.vue`; thêm mục "Cài đặt phân hệ" vào `SettingSlidebar.vue`.
Dev server 3002 biên dịch được route mới (HTTP 200). **CHƯA test trên trình duyệt.**
Đang làm dở: không có
Bước tiếp theo: test tay màn mới (chờ user duyệt) rồi làm Phase 4 — gỡ 3 checkbox cũ + middleware chặn URL
Blocked: chưa test gate quyền `Quản lý phân quyền` (cần tài khoản không có quyền đó)

### Checkpoint — 2026-09-14 (Phase 2 xong)
Vừa hoàn thành: **Phase 2 — lớp lọc FE**. `utils/menuVisibility.js` + `menuHiddenKeys` trong store
(nạp ở `nuxtClientInit`, lỗi API ⇒ hiện hết) + cắm lọc vào `layouts/default.vue`, `Sidebar.vue`,
`hub.js`, `SaleHubSidebar.vue`, `SubsystemHubOverview.vue`, `pages/index.vue`, `SubsystemSwitcher.vue`.
⚠️ Phát hiện & đã xử lý: khoá rút gọn ban đầu gây **19 va chạm thật** (vd `/assign/assign_business`
có 4 mục khác nhau; `sale::Kế hoạch::Theo nhân viên` có 3 mục) → đổi sang đường dẫn nhãn ĐẦY ĐỦ +
đóng dấu `menuKey` tại nguồn cho 2 bề mặt của Bán hàng. Đo lại: 0 va chạm ở cả 2 bề mặt.
Kiểm bằng script bundle registry thật: chưa cấu hình gì thì menu nguyên vẹn (41/132/252/22 mục);
ẩn mục lẻ / ẩn nhóm / ẩn phân hệ / ẩn nút rail đều đúng; ẩn 1 màn của Bán hàng mất ở CẢ hub lẫn cây.
Dev server 3002 vẫn trả HTTP 200. CRLF giữ nguyên (`git diff --stat` không phình).
Đang làm dở: không có
Bước tiếp theo: Phase 3 — màn `/timesheet/setting/subsystems`
Blocked: chưa test gate quyền `Quản lý phân quyền` (cần tài khoản không có quyền đó)

### Checkpoint — 2026-09-14 (Phase 1 xong)
Vừa hoàn thành: **Phase 1 — Backend đầy đủ**. Migration đã chạy trên `local_hrm_erp`
(`menu_settings`, 0 dòng = hiện hết). Model/Service/Request/Controller/Route xong, đã test thật
qua HTTP trên cổng 8003: GET không token → 401; GET → `{"hidden_keys":[]}`; PUT ghi đè + dọn key cũ;
PUT thiếu `hidden_keys` → 400 kèm message tiếng Việt; lưu/bỏ tick phân hệ `rice`/`decision` đồng bộ
đúng `master_settings.use_rice` / `use_decision`; `created_by`/`updated_by` ghi đúng id nhân viên.
DB đã trả về trạng thái ban đầu (3 cờ cũ = 1, bảng mới rỗng).
Đang làm dở: không có
Bước tiếp theo: Phase 2 — `utils/menuVisibility.js` + nạp `menuHiddenKeys` vào store + cắm lọc 6 bề mặt
Blocked: chưa test gate quyền `Quản lý phân quyền` bằng tài khoản KHÔNG có quyền (cần user cấp tài khoản
hoặc cho phép đổi mật khẩu 1 tài khoản local) — middleware đã gắn đúng alias `checkPermission`
