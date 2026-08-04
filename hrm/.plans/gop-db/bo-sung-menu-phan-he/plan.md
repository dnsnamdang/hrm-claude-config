# Plan — Bổ sung menu đầy đủ cho các phân hệ

**Người phụ trách:** @junfoke — 2026-08-01
**Design:** `.plans/bo-sung-menu-phan-he/design.md`
**Spec:** `docs/superpowers/specs/2026-08-01-bo-sung-menu-phan-he-design.md`

Repo đụng tới: **`hrm-client` duy nhất**. Không đụng `hrm-api`, không đổi DB, không đổi quyền.

---

## Phase 0 — Chuẩn bị

- [x] Đọc sheet `Gộp phân hệ ERP-HRM` (857 dòng) + `erp-menu-inventory` (275 dòng)
- [x] Đối chiếu sheet với menu hiện tại → chốt danh sách mục thiếu trên 14 phân hệ
- [x] Resolve 4 route name Laravel → URL thật từ `TanPhatDev/routes/web.php`
- [x] Chốt scope loại trừ với user (Mua hàng/Kho/VC, Danh mục hàng hóa - dịch vụ, Danh sách nhân viên)
- [x] Viết design.md + spec + Phụ lục A

## Phase 1 — Hạ tầng Sidebar (làm trước, mọi phase sau phụ thuộc)

- [x] `Sidebar.vue`: thêm nhánh render `erpPath` → `<a :href="ERP_URL + erpPath" target="_blank"
      rel="noopener">` + icon `ri-external-link-line`, áp dụng cả 3 cấp menu
- [x] `Sidebar.vue`: thêm nhánh render mục pending (không `link`, không `erpPath`) →
      `<a class="menu-item-pending" title="Chức năng chưa được xây dựng">` **không có href**, cả 3 cấp
- [x] `Sidebar.vue`: thêm `ERP_URL: process.env.ERP_URL` + `PENDING_TITLE` vào `data()`
- [x] `Sidebar.vue`: thêm style `.menu-item-pending` + `.menu-external-icon`
- [x] Verify: **không** đụng `isShowMenuParent` / `isShowSubItemMenu` / nhánh `router-link`
- [x] Compile template bằng `vue-template-compiler` — 0 lỗi
- [x] Render thật 3 kiểu item ở cả 3 cấp (`render-sidebar.js`) — 12/12 PASS
- [x] Regression 11 bộ menu đang chạy (`regression-menus.js`) — 11/11 PASS
- [x] Đối chứng: chạy lại regression với `Sidebar.vue` từ `git show HEAD` → **số liệu giống hệt**

## Phase 2 — Ẩn 3 phân hệ Mua hàng / Kho / Vận chuyển

- [x] `components/subsystems.js`: thêm `hidden: true` cho `purchase`, `warehouse`, `transport`
      (giữ nguyên `permissionType` 20/21/22)
- [x] `pages/index.vue :: isShow()`: thêm `if (subsystem.hidden) return false`
- [x] `components/SubsystemSwitcher.vue :: isShow()`: sửa song song
- [x] `components/subsystems.js :: getPermissionSubsystemGroups()`: thêm `&& !s.hidden`
- [x] Verify bằng script nạp registry thật (`check-hidden.js`) — 7/7 PASS: 22 phân hệ còn hiện,
      nhóm SẢN XUẤT - CUNG ỨNG chỉ còn `production`, màn Phân quyền còn 21 khối

## Phase 3 — 9 phân hệ nhỏ (tạo file menu mới)

- [x] `subsystem-menu/admin.js` — Quản trị hệ thống, 15 mục / 5 nhóm (2 mục `erpPath`)
- [x] `subsystem-menu/tax.js` — Thuế TNCN, 5 mục
- [x] `subsystem-menu/recruitment.js` — Tuyển dụng, 6 mục
- [x] `subsystem-menu/kpi.js` — Đánh giá KPI, 5 mục
- [x] `subsystem-menu/legal.js` — Hoạt động pháp lý, 9 mục
- [x] `subsystem-menu/asset.js` — Quản lý tài sản, 4 mục
- [x] `subsystem-menu/iso.js` — Hồ sơ ISO, 6 mục
- [x] `subsystem-menu/operation.js` — Vận hành nghiệp vụ, 2 mục
- [x] `subsystem-menu/production.js` — Quản lý sản xuất, 7 mục / 2 nhóm
- [x] `subsystems.js`: trỏ 9 menu mới, bỏ 9 lời gọi `dashboardOnlyMenu()` tương ứng
- [x] Grep 31 class `ri-*` dùng trong đợt này với `_remixicon.scss` local — tất cả tồn tại

## Phase 4 — Bổ sung vào 3 file menu đã có

- [x] `subsystem-menu/master-data.js` — +7 mục (2 nhóm sẵn có)
- [x] `menu-sidebar.js :: menuItemsAssign` — +18 mục / 6 nhóm mới
- [x] `subsystem-menu/customer-care.js` — tạo mới, 17 mục / 4 nhóm
- [x] `subsystems.js`: trỏ menu `customer-care`

## Phase 5 — 2 phân hệ lớn

- [x] `subsystem-menu/sale.js` — +139 mục / 36 nhóm mới (2 mục `erpPath`)
- [x] `subsystem-menu/finance.js` — +96 mục / 24 nhóm mới (2 mục `erpPath`)
- [x] Sinh code bằng script từ sheet để tránh sai sót gõ tay (`gen-big-menus.py`)

## Phase 6 — Kiểm thử tự động

- [x] `audit-menus.js`: đối chiếu 21 phân hệ với sheet **theo từng phân hệ** — 0 mục thiếu
      ngoài ý muốn (chỉ còn `Danh mục ngân hàng` là chủ ý bỏ, xem §3.2 spec)
- [x] `final-checks.js` — 9/9 PASS: bất biến mỗi link thuộc đúng 1 phân hệ (284 link),
      không item nào vừa `link` vừa `erpPath`, mọi item có label, 19 phân hệ menu dọc đều có
      "Tổng quan" `isShow: true`, render 24 phân hệ không lỗi, đếm đúng số pending + ERP
- [x] Kiểm tra format theo `.prettierrc.json` (nháy đơn, không semicolon, indent 4, ≤120 ký tự)

## Phase 7 — Tái phân bổ 14 màn bị khuất vì ẩn phân hệ

User phát hiện: 4 màn Kiểm kê (trong 7 màn cần link ERP) đang nằm ở phân hệ Kho — vừa bị ẩn
nên không ai thấy. Rà rộng ra toàn bộ `erp-menu-inventory`.

- [x] Đọc màu chữ ô Excel bằng `openpyxl` → 24 dòng chữ đỏ (`FFFF0000`) = "Bỏ" /
      "Không chuyển, chờ logic mới" → loại khỏi diện xét
- [x] Cross-map 251 dòng còn lại với cột `Phân hệ` của sheet gộp (khớp theo route, fallback
      theo tên) → **15 dòng rơi hoàn toàn vào phân hệ đang ẩn**
- [x] Loại 1 dòng đã hiện sẵn ở Bán hàng (bản `?type=all` của BC phân công phòng) → còn **14**
- [x] Resolve 4 route Kiểm kê → URL ERP thật từ `TanPhatDev/routes/web.php`
- [x] `finance.js`: thêm nhóm `Kiểm kê` — 4 màn, cả 4 khai `erpPath` (trả về đúng menu
      `Kế toán > Kiểm kê` của ERP)
- [x] `sale.js`: thêm nhóm `Khởi tạo phiếu yêu cầu` — 10 phiếu (user chốt về Bán hàng, căn cứ
      ghi chú ERP "Chuyển Khởi tạo của KD sang nền tảng HRM")
- [x] Grep icon `ri-clipboard-line` trong `_remixicon.scss` local
- [x] Chạy lại toàn bộ kiểm thử — PASS, số mới: **340 xám mờ + 10 link ERP = 350**

## Phase 8 — Bổ sung 5 màn thiếu khỏi sheet + cập nhật sheet gộp

- [x] Xác định 5 màn có trong `erp-menu-inventory` nhưng thiếu hẳn khỏi sheet gộp
- [x] `sale.js`: nhóm mới `Báo giá` (3 màn) + `Danh sách báo giá (ERP)` vào nhóm SC-BH có sẵn
- [x] `finance.js`: nhóm mới `Kết chuyển cuối kỳ` (1 màn)
- [x] Gắn hậu tố `(ERP)` cho 4 màn báo giá (trùng vai trò với module báo giá HRM ở Dự án TKT)
- [x] **Sao lưu** sheet gộp → `... - truoc-khi-bo-sung-menu-20260801.xlsx`
- [x] Cập nhật sheet: 15 dòng đổi phân hệ + điền 4 dòng giữ chỗ + thêm 1 dòng mới
      (861 → 862 dòng), STT đánh lại, autofilter mở rộng, style/màu giữ nguyên
- [x] Verify sheet sau khi ghi: STT liên tục, 0 khối bị chia cắt, 2 nhóm trùng tên
      "Khởi tạo phiếu yêu cầu" (Quản lý sản xuất / Bán hàng) tách riêng đúng, màu cột Nguồn đúng
- [x] Chạy lại toàn bộ kiểm thử — PASS, số cuối: **345 xám mờ + 10 link ERP = 355**

## Phase 9 — Mua hàng / Kho / Vận chuyển: hiện card, trỏ sang ERP

User đổi yêu cầu: thay vì ẩn hẳn, 3 phân hệ này vẫn hiện ở màn chọn phân hệ, bấm vào thì sang ERP.

- [x] `subsystems.js`: bỏ cờ `hidden`, thay bằng `external: true` + `erpPath` cho 3 phân hệ
- [x] Resolve màn ERP đại diện cho từng phân hệ từ `TanPhatDev/routes/web.php`
      (ERP không có landing riêng — topmenubar chỉ có Danh mục/Khởi tạo/Kinh doanh/Kế toán/CSKH/QTTT)
- [x] `pages/index.vue` + `SubsystemSwitcher.vue`: `openERP()` nhận tham số subsystem để
      ghép `ERP_URL + erpPath`; bỏ nhánh `hidden` trong `isShow()`; 4 chỗ gọi trong template
- [x] `getPermissionSubsystemGroups()`: đổi `!s.hidden` -> `!s.external`
- [x] Verify `check-external.js` — 17/17 PASS: 3 card hiện lại, nhóm SẢN XUẤT - CUNG ỨNG đủ
      4 phân hệ, permissionType 20/21/22 giữ nguyên, màn Phân quyền còn 21 khối, card ERP tổng
      vẫn về trang chủ, `resolveSubsystem` không đổi
- [x] Compile 3 template (`index.vue`, `SubsystemSwitcher.vue`, `Sidebar.vue`) — 0 lỗi

## Phase 10 — CÒN LẠI (chưa làm)

- [ ] **Verify trên browser thật** — chưa chạy. Cần kiểm bằng mắt:
      - mục xám mờ hiển thị đúng độ mờ và không bấm được (kiểm cả hover)
      - mục ERP mở đúng tab mới, icon mũi tên không lệch hàng
      - sidebar dài không vỡ layout: Tài chính (104 mục / 27 nhóm),
        Bán hàng (184 mục / 44 nhóm) — cuộn `simplebar`, nhóm thu gọn mặc định
      - màn chọn phân hệ + dropdown + màn Phân quyền không còn Mua hàng / Kho / Vận chuyển
      - ⚠️ dọn screenshot sau khi xong, KHÔNG dùng wildcard khi xóa file trong thư mục dự án
- [ ] Sửa nhãn `'Quyết định '` thừa dấu cách cuối ở `default-menu/decision.js` (lỗi có sẵn,
      để ngoài phạm vi feature này — gộp vào đợt dọn dẹp sau)
- [ ] Quyết định lại vụ `Danh mục ngân hàng` bị liệt kê ở 2 phân hệ trong sheet
      (hiện chỉ giữ ở Danh mục chung)
- [ ] ⚠️ **Xung đột link `/assign/customers`** — sau commit `564125504 gop database khach hang`,
      mục "Khách hàng" ở `master-data.js` đổi sang `/assign/customers`, trùng với mục
      "Khách hàng" trong nhóm Danh mục của `sale.js`. Vi phạm bất biến *mỗi link chỉ thuộc
      đúng 1 phân hệ*: mở `/assign/customers` giờ luôn hiện sidebar **Danh mục chung**
      (đứng trước trong `SUBSYSTEMS`), không bao giờ ra Bán hàng. Cần bỏ 1 trong 2.

---

## Checkpoint — 2026-08-01

**Vừa hoàn thành:** Phase 0-9. Toàn bộ code đã xong và **kiểm thử tự động PASS hết** bằng cách
render thật template `Sidebar.vue` qua `vue-server-renderer`.

Số liệu chốt: **355 mục menu mới** (345 xám mờ + 10 link ERP) trên 14 phân hệ; 3 phân hệ
Mua hàng / Kho / Vận chuyển đã ẩn; 284 link trong registry, mỗi link thuộc đúng 1 phân hệ.

Phase 7 (tái phân bổ) phát sinh từ câu hỏi của user: ẩn 3 phân hệ làm 14 màn thuộc diện
chuyển sang HRM bị khuất. Đã đưa 4 màn Kiểm kê về Tài chính (kèm link ERP thật) và 10 phiếu
Khởi tạo về Bán hàng. Phase 8 bổ sung nốt 5 màn thiếu khỏi sheet và **cập nhật lại chính
sheet gộp** cho khớp menu (đã sao lưu bản gốc trước khi sửa).

Files: tạo mới 10 file `components/subsystem-menu/*.js`; sửa `Sidebar.vue`, `subsystems.js`,
`menu-sidebar.js`, `master-data.js`, `sale.js`, `finance.js`, `pages/index.vue`,
`SubsystemSwitcher.vue`.

⚠️ **Con số trong bản plan/spec đầu tiên (326) là SAI.** Nó tính bằng cách đối chiếu nhãn trên
toàn hệ thống nên vừa cộng thiếu vừa bỏ sót mục trùng tên giữa 2 phân hệ — chính vì vậy mà sót
mục "Phiếu giao việc" của phân hệ Quản lý công việc. Số thực tế sau cài đặt là **336**, cộng 14 màn tái phân bổ ở Phase 7 thành **350**.
Phụ lục A của spec đã được sinh lại từ code.

**Đang làm dở:** (không)

**Bước tiếp theo:** Phase 10 — verify trên browser thật. Đây là phần **duy nhất** chưa được
kiểm chứng: mọi thứ hiện mới chỉ được xác nhận ở mức render HTML, chưa nhìn bằng mắt trên
trình duyệt (đặc biệt là độ mờ của mục xám mờ và chiều dài sidebar của Bán hàng / Tài chính).

**Blocked:** (không)
