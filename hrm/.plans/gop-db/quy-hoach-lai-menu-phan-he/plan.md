# Plan — Quy hoạch lại menu & phân hệ theo sơ đồ 04/09/2026

Tóm tắt: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-09-16-quy-hoach-lai-menu-phan-he-design.md`

## Phase 0 — Khảo sát tài liệu (2026-09-16)

- [x] Tải 5 sheet (CSV cho nội dung, XLSX cho định dạng)
- [x] Đọc màu nền (`FFFF00` = chưa xây dựng) bằng `openpyxl`
- [x] Đọc gạch ngang (`cell.font.strike` = đã bỏ/đã chuyển) — đã kiểm cả rich text, không có ô gạch một phần
- [x] Đối chiếu với registry hiện tại, chốt 8 quyết định (xem design.md)

## Phase 1 — Nhóm QUẢN TRỊ LÕI (2026-09-16)

- [x] `menu.js` / `menuItemsHuman`: tách thành 4 nhóm **Danh mục / Cơ cấu tổ chức / Hồ sơ nhân sự / Báo cáo**
- [x] Đổi tên theo cột Ghi chú: Quản lý hồ sơ nhân sự, Quản lý nhân viên nghỉ việc, Quản lý hồ sơ tự khai,
      Báo cáo thân nhân và người phụ thuộc, Báo cáo tổng hợp phòng ban, Bảng nhân sự và quỹ thu nhập định mức,
      Báo cáo nhiệm vụ theo PB/NV, Danh mục loại hợp đồng lao động
- [x] `admin.js`: thêm nhóm **Cài đặt chung** (Logo web - tiêu đề web, Cấu hình định biên nhân sự),
      **Tài khoản nhân viên** (`/human/employee`, dời từ Thông tin nhân sự), **Danh sách phân quyền**
      (`/human/roles` — hiện KHÔNG nằm trong menu nào), Danh sách người dùng
- [x] `master-data.js`: thêm **Ngân hàng câu hỏi khảo sát** (`/assign/questions`, dời từ Quản lý công việc)
- [x] Verify: script đếm link trùng trong toàn bộ menu = **0/357 link** (`audit_links.js`), `menu.js` import lại bằng Node không lỗi cú pháp

## Phase 2 — Nhóm NHÂN SỰ (2026-09-16)

- [x] Chấm công: thêm nhóm **Danh mục** (3 DM tách khỏi Chấm công / Ca làm việc); nhóm **Cấu hình**
      = 3 màn có sẵn `/timesheet/setting/{general,overtime,holiday}`; **Giao việc - công tác** chỉ còn
      2 phiếu, "Duyệt gia hạn/kết thúc công tác" dời sang Phê duyệt; "Đề nghị tra soát công admin"
      dời từ Phê duyệt về Quản lý đơn; đổi tên Phiếu giao việc trong ngày / Bảng phân ca chi tiết /
      Dữ liệu máy chấm công (vân tay)
- [x] Tính lương: đổi "lương" → "thu nhập" (Công thức thu nhập, Thành phần thu nhập, Mẫu bảng tính
      thu nhập, Dữ liệu tính thu nhập, Bảng chấm công tổng hợp, Thu nhập P3, Bảng tính thu nhập);
      thêm nhóm **Danh mục** (DM phụ cấp dời từ Thông tin nhân sự + DM hỗ trợ chi phí hoạt động dời
      từ Quyết định); thêm **Cấu hình tiền lương** (3 mục, chưa link) + **Báo cáo thu nhập** (vàng)
- [x] Bảo hiểm: thêm **Cấu hình › Tỉ lệ đóng BHXH** (chưa link) + **Báo cáo BHXH** (2 báo cáo định
      mức dời từ Thông tin nhân sự); thêm DM điều kiện hưởng (dời từ Quyết định)
- [x] Quản lý cơm: 3 màn Danh mục đã có sẵn từ trước; đổi tên Bảng đăng ký cơm của nhân viên /
      Đăng ký suất ăn admin / Danh sách thông báo đăng ký ăn cơm / Thiết lập QL cơm
      (4 mục "Thiết lập…" của sheet là 4 **tab trong cùng màn** `/rice/setting` → giữ 1 mục menu)

### Checkpoint — Phase 2 (2026-09-16)

**Vừa hoàn thành:** `components/menu.js` (timesheet + payroll), `components/subsystem-menu/insurance.js`,
`components/default-menu/rice.js`, `components/default-menu/decision.js` (bỏ 2 DM đã chuyển đi),
`components/subsystem-menu/admin.js` (sửa link Danh sách người dùng/phân quyền về
`/timesheet/setting/{employees,roles}` — đúng cụm "Thiết lập" cũ của Chấm công, không phải `/human/roles`).

**Đã kiểm:** import lại toàn bộ file menu bằng Node (không lỗi cú pháp, cây menu đúng);
`audit_links.js` → **0/360 link trùng**; EOL giữ CRLF.

**Bước tiếp theo:** Phase 3 — nhóm VĂN PHÒNG SỐ (tách phân hệ Meeting + An toàn 5S).

**Blocked:** mục "Chờ user chốt" số 1 (màn `/human/settings`).

## Phase 2b — Tách màn Cấu hình + xám mờ menu ngang (2026-09-16, user chốt)

- [x] `components/Topbar.vue`: mục menu **không có `link`** (hoặc `#`) render **xám mờ + không bấm
      được** — lớp `.menu-item-pending` đặt theo đúng cách sidebar phân hệ mới đang làm; áp cho cả
      mục cấp 1 lẫn mục con trong dropdown (dùng `/deep/` vì `<a class="dropdown-item">` do
      bootstrap-vue render). ⚠️ `Topbar.vue` là component dùng chung — user đã đồng ý sửa.
- [x] Tách `/human/settings` thành **3 màn mới**, mỗi màn giữ nguyên chức năng phần của mình
      (bê nguyên markup + method từ màn gốc, cùng API):
      | Màn mới | Phân hệ | Nội dung |
      | --- | --- | --- |
      | `/payroll/setting/salary-config` | Tính lương | Lương cơ bản · % tăng lương thâm niên · chu kỳ xét thâm niên |
      | `/admin/setting/manpower` | Quản trị hệ thống | Dùng / không dùng định biên nhân sự |
      | `/insurance/setting/insurance-rate` | Bảo hiểm | Bảng tỉ lệ đóng BHXH theo mốc ngày (thêm/sửa/xoá dòng) |
- [x] Cả 3 màn giữ nút **Lịch sử thay đổi** — dùng lại `HumanSettingHistoryModal` của màn gốc
      (API `human/settings/histories` trả lịch sử chung, chưa lọc theo nhóm thông số).
- [x] Gắn link vào menu 3 phân hệ; bỏ mục `Cấu hình` khỏi menu Thông tin nhân sự.
- [x] Màn gốc `/human/settings` **giữ file** (không còn trong menu) + ghi chú deprecate ở đầu file,
      vì `HumanSettingHistoryModal` nằm trong thư mục đó và để không gãy bookmark cũ.
- [x] Verify: `vue-template-compiler` compile 4 file .vue → OK; `audit_links.js` → 0/362 link trùng.
- [ ] Verify trình duyệt (chưa có dev server chạy).

**Khác biệt có chủ đích so với màn gốc:** màn Cấu hình tiền lương **gom 600ms** (debounce) trước khi
tự lưu — màn gốc bắn 1 request + 1 toast cho **mỗi ký tự** gõ vào ô số. Hành vi vẫn là tự lưu,
không thêm nút Lưu. Màn định biên (radio) giữ nguyên lưu ngay.

⚠️ BE `GeneralRegulationController::update` dùng `$request->only([...])` + `fill()` nên mỗi màn chỉ
gửi phần của mình, không ghi đè thông số của 2 màn kia.

## Phase 3 — Nhóm VĂN PHÒNG SỐ (2026-09-16)

- [x] Tách phân hệ **Meeting** (`components/subsystem-menu/meeting.js`, `pages/meeting/dashboard`,
      permissionType 26): Danh mục (Loại meeting, Lý do hủy cuộc họp) · Tổng hợp meeting ·
      Quản lý phòng họp (2 mục chưa có màn) · 4 báo cáo
- [x] Tách phân hệ **Quản lý an toàn 5S** (permissionType 27, `dashboardOnlyMenu` — user chốt
      tách khung trước, chức năng sau)
- [x] Đổi nhãn 4 phân hệ: `iso` → *Hoạt động ISO (quản lý quy trình)* · `operation` →
      *Ban hành văn bản nội bộ (Quyết định - quy định - quy chế)* · `decision` →
      *Ban hành văn bản nội bộ* · `training` → *Đào tạo - đánh giá*
- [x] `operation.js`: dựng lại theo sheet — Quy trình - biểu mẫu + **10 nhánh quy chế theo khối
      nghiệp vụ**. KHÔNG khai lại Chờ duyệt / Báo cáo thang bảng lương vì 3 màn đó chạy thật ở
      phân hệ `decision`
- [x] `decision.js`: nhận **Thông báo nội bộ** (2 màn chuyển từ Thông tin nhân sự); đổi nhãn 4
      nhóm theo sheet; bỏ mục rác "Danh mục test" (trùng link với Danh mục loại sự cố)
- [x] `menuItemsAssign`: bỏ khối Meeting (nhóm + 2 danh mục + 3 báo cáo); thêm nhóm **Làm giải
      pháp** (4 màn chuyển từ khối Dự án TKT của hub Bán hàng, đổi tên Hạng mục giải pháp /
      Danh sách hàng tạm); 4 báo cáo hiệu suất - nguồn lực (link thật, chuyển từ hub Bán hàng);
      nhóm Cấu hình → **Thiết lập**
- [x] `menuItemsTraining`: dựng lại theo sheet — Danh mục nhận 2 DM đánh giá năng lực · nhóm
      **Phê duyệt** (4 mục "cần duyệt" gom từ 4 nhóm) · nhóm **Đánh giá năng lực** (5 màn) ·
      **E-learning** (chưa có màn) · Báo cáo gom đủ 11 BC khóa học + 6 BC đánh giá năng lực;
      bỏ 2 nhóm rỗng "Tổng hợp bài thi" / "Xây dựng khung năng lực"
      → làm bằng script cắt-dán NGUYÊN VĂN từng khối (giữ `isShow`), đối chiếu 98 link trước/sau: khớp

## Phase 4 — Nhóm KINH DOANH - TÀI CHÍNH (2026-09-16)

- [x] Tách phân hệ **Quản lý CSKH trước khi bán** (`presale.js`, permissionType 29): Chức năng
      (Dự án, Yêu cầu giải pháp, Yêu cầu tính giá bán, Báo giá + Nhiệm vụ/Vấn đề chưa link) ·
      7 báo cáo dự án tiền khả thi · 14 báo cáo thị trường
- [x] Tách phân hệ **Tra cứu - thông báo** (`lookup.js`, permissionType 28) — chuyển nguyên nhóm
      "Tra cứu - Thông báo" của hub Bán hàng
- [x] Hub Bán hàng: bỏ khối **Dự án TKT** (chia cho presale + Quản lý công việc, riêng
      *Hợp đồng* ở lại nhóm Hợp đồng bán hàng), bỏ 3 nhóm báo cáo đã chuyển đi
- [x] `customer-care` → nhãn **CRM** (3 báo cáo CSKH đã có sẵn trong menu CRM)

## Phase 5 — Nhóm SẢN XUẤT - CUNG ỨNG (2026-09-16)

- [x] `purchase.js` / `warehouse.js` / `transport.js`: khai chức năng cấp 1 theo sheet
      (Đặt hàng · Công nợ NCC · Hãng bảo hành · Bảo hiểm mua hàng / Xuất - nhập · Tồn kho ·
      Kiểm kê / Bảng giá vận chuyển · Tuyến đường · Công thức vận chuyển · Bốc xếp).
      3 phân hệ vẫn `hidden + erpGhost` (nghiệp vụ bên ERP) — chỉ thay `dashboardOnlyMenu`
- [x] Quản lý sản xuất: sheet chỉ có tên phân hệ (bôi vàng), `production.js` hiện có đã đủ → giữ

### Checkpoint — Phase 3-5 (2026-09-16)

**Vừa hoàn thành:** 4 phân hệ mới (Meeting, An toàn 5S, CSKH trước khi bán, Tra cứu - thông báo)
+ 5 đổi nhãn + dựng lại menu Đào tạo / Quản lý công việc / Ban hành VB nội bộ / hub Bán hàng.

**Đã kiểm:** `audit_links.js` → **0/368 link trùng**; dev server webpack compile lại sau mỗi lần
sửa đều "Compiled successfully" (lỗi duy nhất trong log là lúc `subsystems.js` import
`meeting.js` trước khi file được tạo, đã hết ngay sau đó).

**Bước tiếp theo:** verify trình duyệt toàn bộ 5 nhóm.

**Blocked:** (không)

## Phase 6 — Verify trình duyệt + 4 lỗi phát sinh do menu mới (2026-09-16)

Chạy dev server thật (`hrm-api` + `hrm-client` worktree `gop_db`, cổng 8000/3000), đăng nhập
tài khoản DNS Admin, chụp ảnh nghiệm thu vào `D:\CompanyProject\hrmnh-nghiem-thu-menu\`.

- [x] **Màn chọn phân hệ trắng xoá / 404** — `pages/index.vue::iconOf()` gọi
      `require('@/assets/images/undefined')` khi phân hệ không khai `image` → ném lỗi, hỏng
      render CẢ màn. Sửa: bọc try/catch + fallback, và **vẽ 4 icon SVG mới**
      (`icon_meeting.svg`, `icon_safety_5s.svg`, `icon_presale.svg`, `icon_lookup.svg`)
- [x] **Phân hệ "An toàn 5S" bị CẮT MẤT khỏi cánh hoa** — nhóm VĂN PHÒNG SỐ lên 9 phân hệ,
      `.petal` cao cứng 262px + `overflow: hidden` nên mục thứ 9 không hiện. Sửa: `.petal`
      262 → 306px và `--stage-h` 590 → 634px (giữ nguyên độ chồng 2 hàng cánh + vị trí nhụy)
- [x] **Menu ngang phân hệ Tính lương tràn đè lên chuông/avatar** ở màn ~1100px (8 nhóm, nhãn
      dài). Sửa: `white-space: nowrap` cho nhãn + `align-items: center`
- [x] ⚠️ **Thử cho `.topnav-menu-left` cuộn ngang → dropdown bị cắt, bấm nhóm menu không ra gì.**
      Đã hoàn nguyên; ghi chú cảnh báo ngay trong `Topbar.vue` để người sau không lặp lại
- [x] Ảnh nghiệm thu: màn chọn phân hệ (25 phân hệ, 4 nhóm) · phân hệ Meeting · 3 màn cấu hình
      mới có dữ liệu thật · dropdown "Báo cáo" của Tính lương cho thấy mục **"Báo cáo thu nhập"
      xám mờ** đúng như mục chưa có màn ở sidebar

## Phase 7 — Bỏ tên rút gọn ở màn chọn phân hệ (2026-09-16, user bắt lỗi qua ảnh)

- [x] Bỏ hẳn trường `shortLabel` (15 phân hệ) — `pages/index.vue::nameOf()` và
      `SubsystemSwitcher.vue::nameOf()` dùng thẳng `label`
- [x] Sửa 3 nhãn còn lệch sheet: `Bảo hiểm xã hội` → **Bảo hiểm** · `Danh mục` → **Danh mục dùng
      chung** · `Bán hàng` → **Quản lý bán hàng**
- [x] CSS cho tên dài: `.app__nm` bỏ `nowrap` (tên dài nhất 57 ký tự → 3 dòng), `.app` canh
      `flex-start`; nới cánh hoa `.petal` 306 → 360px và `--stage-h` 634 → 688px
- [x] Đo lại: cánh VĂN PHÒNG SỐ (9 phân hệ) mục cuối cách đáy 23px, 3 cánh còn lại 86-170px
- [x] **Sửa lỗi 2 hàng cánh đè lên nhau** (user phát hiện): nới `.petal` mà chỉ nới `--stage-h`
      một nửa → chồng 32px. Công thức đúng: `--stage-h = 2 × chiều cao .petal + 66`
      (66 = khoảng hở dọc của bản gốc) → `--stage-h: 786px`. Đo lại: hở dọc 57px ở tỉ lệ 0.81,
      4 cánh tách rời, viền liền; kiểm cả ở 1920×1080
- [x] **Sửa lỗi di chuột vào cánh hiện mảng sáng hình chữ nhật** (user báo): `.petal` có
      `backdrop-filter: blur(9px)`, thêm `transform` ở `:hover` khiến Chrome tách layer hợp thành
      và cắt vùng backdrop theo hình chữ nhật thay vì theo `border-radius`. Bỏ `transform` khỏi
      `.petal:hover` → hết mảng vuông. User muốn giữ hiệu ứng phóng to nên chốt phương án
      **dùng thuộc tính `scale: 1.012`** (không phải `transform: scale()`) — `scale` riêng không
      dính lỗi backdrop, giống `animation: float` vẫn dùng `translate` riêng mà nền vẫn bo đúng.
      Verify bằng `page.mouse.move` vào giữa CẢ 4 cánh rồi chụp: phóng to như cũ, không mảng vuông
- [x] User chốt: **giữ 2 cánh CÙNG HÀNG cao bằng nhau**
- [x] **Lỗi vẫn còn khi xem full màn** (user báo tiếp): đổi sang thuộc tính `scale` chưa đủ —
      gốc rễ là `backdrop-filter: blur(9px)` trên `.petal`. Đã **bỏ hẳn backdrop-filter**, thay
      bằng nền gradient đục nhẹ (0.06/0.035) và trả `transform: scale(1.012) translateY(-2px)`
      về đúng bản gốc. ⚠️ Chrome của Playwright chạy **render phần mềm** nên KHÔNG tái hiện được
      lỗi này — phải nhờ user xác nhận trên máy thật.
- [x] **Cánh sát nội dung hơn** (user yêu cầu tối ưu diện tích): chiều cao đặt theo TỪNG HÀNG
      qua biến `--petal-h`. Siết 2 lần theo phản hồi user (vẫn còn trống ở đáy): hàng trên
      372 → **348px**, hàng dưới 250 → **228px**, `padding-bottom` của 2 cánh trên 30 → **16px**,
      `--stage-h = 348 + 228 + 66 = 642px`. Đo ở 1920 / 1366 / 1100: cánh đông phân hệ nhất mỗi
      hàng chỉ còn dư đáy **13-20px**, hở giữa 2 hàng cánh 53-66px, không cánh nào bị cắt.
      ℹ️ Cánh ÍT phân hệ trong cùng hàng (Nhân sự 7 mục, Sản xuất 4 mục) vẫn dư 63-94px — hệ quả
      tất yếu của quy tắc "2 cánh cùng hàng cao bằng nhau" mà user đã chốt
- [x] **Viền cánh bị cắt khi phóng to — nguyên nhân THẬT** (user chỉ đúng chỗ: khối `.stage`):
      `.picker` rộng đúng bằng `.stage` (1220px) và có `overflow-x: clip`; cánh nằm sát mép
      trái/phải nên phóng từ tâm là lồi ra ~3px rồi bị cắt thẳng. Sửa bằng `transform-origin`
      = cạnh NGOÀI của từng cánh (`left center` cho 2 cánh trái, `right center` cho 2 cánh phải).
      Đo khi hover: mép cánh trùng khít mép `.picker` (lệch 0px), không còn phần bị cắt
- [x] Rút gọn lại tên **3 phân hệ lõi** ở nhụy theo user: Thông tin nhân sự → "Thông tin NS",
      Danh mục dùng chung → "Danh mục", Quản trị hệ thống → "Quản trị"
      (khôi phục `shortLabel` nhưng CHỈ cho 3 phân hệ lõi)
- [x] **Tên phân hệ ở đầu SIDEBAR cũng phải dùng `shortLabel`** (user báo: đã đổi "Danh mục" mà
      sidebar vẫn hiện "Danh mục dùng chung", tên dài còn tràn đè lên ô tìm kiếm):
      `components/sale/SaleHubSidebar.vue::subsystemName` + `layouts/default-sidebar.vue::applyBrand()`
      đổi sang `shortLabel || label`; `.subsystem-name` giới hạn **2 dòng rồi cắt "…"**
      (`-webkit-line-clamp: 2`) kèm `title` để hover xem tên đầy đủ.
      Đo: "DANH MỤC" 1 dòng; "BAN HÀNH VĂN BẢN NỘI BỘ (QUYẾT ĐỊNH…" 2 dòng, còn cách ô tìm kiếm 22px
- [x] `admin.js`: bỏ 4 nhóm thừa user khoanh đỏ (Cấu hình ERP · Hướng dẫn sử dụng · Log hệ thống ·
      API Key) — khai từ sheet ERP cũ, không có trong sheet QUẢN TRỊ LÕI. Menu còn đúng 3 nhóm:
      Cài đặt chung · Người dùng & phân quyền · Mẫu in

## Phase 8 — Khai đủ menu theo tài liệu cho phân hệ tên dài (2026-09-16, user báo thiếu)

- [x] **`operation.js` khai lại ĐÚNG sheet dòng 25-70** (trước chỉ có 3 nhóm tự đặt tên, user báo
      "tài liệu nhiều lắm mà vào có mấy cái, nhìn lạ"): Danh mục (4) · Thông báo nội bộ (2) ·
      Quản trị hành chính - nhân sự (23 quyết định/hợp đồng/quy chế) · Bán hàng, dịch vụ và xuất
      khẩu (3) · Ban hành theo khối nghiệp vụ khác (8 khối) · Chờ duyệt (2) · Báo cáo (1)
- [x] `iso.js`: bỏ mục "Quản lý an toàn 5S" (đã tách thành phân hệ riêng)
- [x] `safety-5s`: thay `dashboardOnlyMenu` bằng `safety-5s.js` để rail sidebar không rỗng
- [x] `hub.js`: thêm `meeting` · `presale` · `lookup` · `safety-5s` vào `HUB_SUBSYSTEMS`
- [x] Rà 11 phân hệ còn lại (legal · asset · kpi · tax · recruitment · production · purchase ·
      warehouse · transport · meeting · presale · lookup): khớp sheet, không phải sửa.
      kpi/tax/recruitment/production sheet chỉ có TÊN phân hệ (bôi vàng) — menu hiện tại do
      feature cũ tự đặt, giữ nguyên vì không mâu thuẫn tài liệu

- [x] **Lần 2 (user vẫn báo thiếu + gộp sai)**: 8 khối nghiệp vụ phải là 8 NHÓM RAIL RIÊNG (không
      gom vào "Ban hành theo khối nghiệp vụ khác"), và "Quản trị hành chính - nhân sự" phải giữ
      5 nhóm con như tài liệu (không đổ phẳng 23 mục). Menu 3 cấp + có nhóm chưa có chức năng con
      → `deriveHubGroups` suy không ra, phải **khai tay `operation-hub.js`** (như `sale-hub.js`)
      và đăng ký vào `HAND_WRITTEN` của `hub.js`; `operation.js` chỉ còn sinh cây từ hub
      (1 nguồn menu). Rail giờ đủ **16 nhóm**, panel HCNS đúng 5 nhóm × 23 chức năng

⚠️ **2 gotcha sidebar hub**:
1. `deriveHubGroups()` CHỈ nhận mục cấp 1 **có `subItems`** — mục lá cấp 1 biến mất khỏi rail.
2. `filterHubGroups()` LOẠI nhóm không còn màn nào → nhóm khai `items: []` cũng biến mất.
   Khối nghiệp vụ chưa có chức năng con phải khai 1 màn trùng tên khối
   (HubSidebar tự bỏ tiêu đề lặp khi nhóm chỉ có 1 mục trùng tên nhóm).

⚠️ **Link trùng giữa `operation` và `decision`**: phần lớn mục của khối "Quản trị hành chính -
nhân sự" đã có màn chạy thật nhưng màn đó thuộc phân hệ `decision`; mỗi link chỉ được nằm ở 1
phân hệ nên bên `operation` để trống `link` (xám mờ). **Chờ user chốt** có chuyển hẳn các quyết
định HCNS sang phân hệ này không.

## Phase 9 — Đối chiếu TỰ ĐỘNG toàn bộ tài liệu ↔ menu (2026-09-16)

User mất niềm tin vào việc rà bằng mắt ("giờ tôi không tin bạn nói xong nữa") → viết script
**`doi-chieu-menu.py`** (nằm cùng thư mục feature này) đọc `book.xlsx` + mọi file menu của
`hrm-client`, so từng mục tài liệu với nhãn menu (bỏ dấu, bỏ ngoặc, bỏ mục gạch ngang).

Lần chạy đầu: **43 mục lệch / 23 phân hệ**. Đã sửa hết:

- [x] `menuItemsAssign` **dựng lại theo 8 nhóm tài liệu**: Làm giải pháp · Nhiệm vụ · Tiếp nhận
      công việc · Phân công công việc · Kết quả công việc · Phê duyệt · Báo cáo · Thiết lập
      (trước gom lộn xộn thành "Giao việc & Bàn giao", "Giao việc - Công tác", 3 nhóm ERP rời).
      Đối chiếu link trước/sau: **44/44 link giữ nguyên, không mất màn nào**
- [x] Quản lý cơm: nhóm Thiết lập khai đủ **4 mục** (4 tab của cùng màn `/rice/setting`)
- [x] Tính lương: "Cấu hình tiền lương" khai đủ **3 thông số** (cùng trỏ màn mới)
- [x] Tra cứu - thông báo: thêm nhóm 3 mục sheet nêu đích danh (Tổng hợp tiền về · Danh sách
      giữ - mượn - NXT · Báo cáo tồn kho có thể bán)
- [x] Tài chính: thêm 3 mục sheet nêu (Qũy - Thu chi · Báo cáo tài chính · Báo cáo dòng tiền)
- [x] Bán hàng: thêm nhóm "Quản lý hợp đồng dịch vụ" (Phiếu xử lý · Phiếu bảo hành · Hợp đồng
      dịch vụ) + "Quy chế kinh doanh"
- [x] Meeting: thêm báo cáo "Meeting theo khách hàng"
- [x] Sửa nhãn về ĐÚNG NGUYÊN VĂN tài liệu: Hoạt động pháp lý (2), Quản lý tài sản (1),
      Vận chuyển (1), Danh mục dùng chung (1)
- [x] Chạy lại: **0 mục lệch / 23 phân hệ** (6 mục còn lại là sheet gõ nhầm hoặc đã chuyển phân
      hệ — khai trong `BO_QUA` của script kèm lý do)

ℹ️ 5 phân hệ không có trong báo cáo vì sheet chưa liệt kê chức năng nào (chỉ có tên, bôi vàng):
Thuế TNCN · Tuyển dụng · Đánh giá KPI · Quản lý sản xuất · Quản lý an toàn 5S.

## Phase 10 — Phân cấp cha/con trong panel hub (2026-09-16)

- [x] User báo: nhóm "Báo cáo bán hàng (30)" nhìn NGANG HÀNG với 6 nhóm con bên dưới nên tưởng
      trống. Nguyên nhân: `SaleHubSidebar.vue` render nhóm cha và nhóm con bằng **cùng một class
      `.sub__t`**. Sửa: nhóm cha thêm `sub__t--parent` (chữ 13.5px, nền nhạt, viền dưới màu nhấn),
      nhóm con bọc trong `.subkids` — thụt 18px, có đường kẻ dọc nối về cha, chữ nhỏ và nhạt hơn.
      Chỉ ảnh hưởng phân hệ có menu 3 cấp (hiện chỉ Bán hàng)

### Việc còn lại

- Menu ngang vẫn có thể tràn ở màn hẹp (< ~1500px) với phân hệ nhiều nhóm — chờ user chốt:
  rút gọn nhãn, hay gom bớt nhóm, hay chấp nhận.
- Chưa verify từng màn con của 5 nhóm (mới verify khung + 3 màn mới + 1 dropdown).

## Chờ user chốt

- ~~`/human/settings` bị sheet tách làm 3~~ → **user chốt 16/09: TÁCH LUÔN**, đã làm ở Phase 2b.
  (Ghi chú gốc) `/human/settings` bị sheet **tách làm 3** (rà lại khi làm Phase 2 — nhiều hơn dự đoán ban đầu):
  "Dùng định biên nhân sự" → Quản trị hệ thống · "Lương cơ bản / % tăng thâm niên / chu kỳ xét thâm
  niên" → Tính lương › Cấu hình tiền lương · **"Tỉ lệ đóng BHXH" (bảng theo mốc ngày) → Bảo hiểm ›
  Cấu hình**. Một màn không dời vào 3 phân hệ được → tạm giữ nguyên ở Thông tin nhân sự, 3 mục ở
  phân hệ đích khai **không link**. Chờ user chốt: tách màn làm 3 hay để nguyên 1 chỗ.
- ~~Quận/Huyện trong DM địa giới hành chính~~ → **user chốt 16/09: GIỮ**, vì các quốc gia khác
  Việt Nam vẫn còn cấp quận/huyện (sheet chỉ liệt kê theo địa giới VN sau sáp nhập).
- ~~Các mục human sheet không nhắc tới~~ → **user chốt 16/09: GIỮ NGUYÊN** (Cập nhật tình hình
  nhân sự, Danh mục phụ cấp, Lĩnh vực Công ty kinh doanh, Khai Quy chế – Cấu hình).

### Checkpoint — Phase 1 (2026-09-16)

**Vừa hoàn thành:** 4 file `hrm-client` — `components/menu.js` (dựng lại `menuItemsHuman` thành
4 nhóm), `components/subsystem-menu/admin.js` (+2 nhóm: Cài đặt chung, Người dùng & phân quyền),
`components/subsystem-menu/master-data.js` (+Ngân hàng câu hỏi khảo sát),
`components/menu-sidebar.js` (bỏ Ngân hàng câu hỏi khảo sát khỏi Quản lý công việc).

**Đã kiểm:** import `menu.js` bằng Node → cây menu đúng 6 mục cấp 1; `audit_links.js` → 0 link
khai trùng giữa các file menu; `git diff --numstat` gọn (không đổi EOL toàn file).

**Đang làm dở:** (không)

**Bước tiếp theo:** verify trình duyệt; sau đó Phase 2 (nhóm NHÂN SỰ).

**Blocked:** chờ user chốt 3 mục ở "Chờ user chốt".

ℹ️ Ghi chú: `components/human-components/human-slidebar.vue` (slidebar cũ của phân hệ Nhân sự)
vẫn còn link `/human/employee` — không thuộc registry nên không ảnh hưởng `resolveSubsystem`,
nhưng nếu còn dùng thì màn Tài khoản nhân viên vẫn vào được từ 2 nơi.

## Gotcha

- Phân hệ dùng **topbar** (Thông tin nhân sự, Chấm công, Tính lương, Quản lý cơm, Quyết định)
  render bằng `components/Topbar.vue` — **chưa có kiểu "xám mờ"** cho mục không có `link` như
  `Sidebar.vue`. Mục chưa có màn ở các phân hệ này (Cấu hình tiền lương, Báo cáo thu nhập,
  Tỉ lệ đóng BHXH…) hiện render thành mục bấm không đi đâu. Muốn xám mờ phải sửa `Topbar.vue`
  (component dùng chung → hỏi user trước).
