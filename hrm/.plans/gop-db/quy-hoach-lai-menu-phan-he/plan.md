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
- [x] **Verify trình duyệt (Playwright, 16/09 chiều — dev server đã chạy):** cả 3 màn render đúng,
      đo bằng DOM:
      - `/payroll/setting/salary-config`: nạp đủ 3 thông số từ DB (1,000,000 · 3 · 24); gõ **2 ký tự
        → đúng 1 POST** `/api/v1/general-regulations/` (debounce 600ms đúng như thiết kế, màn gốc
        bắn 1 request/ký tự); đổi 3→453 rồi trả về 3, reload đọc lại = 3 → lưu thật; modal
        **Lịch sử thay đổi cấu hình** hiện đủ 2 lượt đổi kèm tên người sửa.
      - `/admin/setting/manpower`: radio nạp đúng trạng thái DB; bấm **nhãn** (không phải input ẩn)
        → 1 POST ngay, reload giữ nguyên; đã trả lại trạng thái cũ "Không dùng định biên".
      - `/insurance/setting/insurance-rate`: sidebar BẢO HIỂM › Cấu hình, header 2 tầng 20 ô, 1 dòng
        dữ liệu thật (10/2022 · 21.5 · 10.5 · 32); nút `+` thêm dòng → 11 ô nhập + Save/Huỷ, **chưa
        gọi API**; bảng cuộn ngang trong khung riêng (`scrollWidth 1794 > clientWidth 1250`,
        `document.scrollWidth = 1512 = viewport` → body KHÔNG tràn ngang).
      - Menu ngang Thông tin nhân sự: **0 mục `Cấu hình`, 0 link `/human/settings`** → đã bỏ đúng.
      - Mục chưa có màn xám mờ đúng: `.menu-item-pending` ("Báo cáo thu nhập") `opacity .45`,
        `pointer-events: none`, `cursor: not-allowed`.

**Khác biệt có chủ đích so với màn gốc:** màn Cấu hình tiền lương **gom 600ms** (debounce) trước khi
tự lưu — màn gốc bắn 1 request + 1 toast cho **mỗi ký tự** gõ vào ô số. Hành vi vẫn là tự lưu,
không thêm nút Lưu. Màn định biên (radio) giữ nguyên lưu ngay.

⚠️ BE `GeneralRegulationController::update` dùng `$request->only([...])` + `fill()` nên mỗi màn chỉ
gửi phần của mình, không ghi đè thông số của 2 màn kia.

### Checkpoint — Verify trình duyệt Phase 2b (2026-09-16)

**Vừa hoàn thành:** verify Playwright 3 màn tách + menu Thông tin nhân sự (chi tiết số đo ở task
trên). Dev server chạy lại trên `gop_db` (`hrm-client` HEAD `3b14f7577`, API `1ec59fff6`).

**Đang làm dở:** (không)

**Bước tiếp theo:** verify từng màn con của 5 nhóm menu (mới verify khung + 3 màn mới + 1 dropdown).

**Blocked:** (không)

⚠️ **1 lỗi tìm ra khi verify — KẾ THỪA từ màn gốc, không phải do tách màn:** bấm **Huỷ (X)** ở dòng
vừa thêm bằng nút `+` (màn Tỉ lệ đóng BHXH) chỉ tắt `edit`, **không xoá dòng khỏi bảng** → còn lại 1
dòng rỗng (STT 2, các ô trống) cho tới khi reload. `cancelItem(index)` ở
`pages/insurance/setting/insurance-rate/index.vue:485` và `pages/human/settings/index.vue:581`
**giống hệt nhau** (`this.insurance_configs[index].edit = false`, thiếu `splice` khi là dòng mới).
Không ảnh hưởng dữ liệu (chưa gọi API). Chờ user chốt có sửa trong phạm vi feature này không.

ℹ️ Dữ liệu test đã trả về trạng thái cũ (% thâm niên = 3, định biên = "Không dùng định biên"),
nhưng bảng lịch sử `general_regulations` có thêm **4 dòng audit** do thao tác verify.

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

## Phase 11 — Gộp phân hệ `decision` vào `operation`, đổi tên "Văn bản nội bộ" (2026-09-16, user chốt)

User chốt **đảo quyết định #5 của design.md**: 2 phân hệ "Ban hành văn bản nội bộ" gộp làm 1.
Tên mới: **Văn bản nội bộ** — subtext **Quyết định, Quy chế công ty**.

⚠️ Không xoá thẳng entry `decision` được: đối chiếu tự động 2 cây menu cho thấy `operation` có đủ
TÊN nhưng **0 link** (sheet bôi vàng), toàn bộ **36 link chạy thật nằm ở `decision`** — xoá trước
khi dời link = 36 màn mất đường vào. 31/36 khớp tên thẳng, 3 lệch chữ
(`Xem Quy chế chung` ↔ `/regulations/general`, `Xem Quy chế lương và hỗ trợ` ↔ `/regulations/salary`,
`Báo cáo thanh bảng lương` (sheet gõ nhầm) ↔ `/decision/reports/regulation-salary`), 2 chưa có chỗ
(`Mẫu in`, `/decision/dashboard`).

- [x] `operation-hub.js`: gắn `link` + `isShow` thật cho 36 mục; thêm mục `Mẫu in` vào nhóm Danh mục;
      bỏ `/decision/dashboard` (hub đã có Tổng quan → `/operation/dashboard`). Đếm lại: phân hệ có
      **37 link**, 8 mục còn xám mờ (8 khối nghiệp vụ sheet chưa có chức năng con)
- [x] `operation.js::toLeaf`: truyền tiếp `isShow` / `groups`
- [x] `hub.js::isScreenVisible`: thêm nhánh `groups` (Topbar có, hub chưa) — 4 màn "Quyết định về tổ
      chức" gate bằng `groups: ['Quyết định']`
- [x] `subsystems.js`: bỏ entry `decision` (29 phân hệ còn lại); `operation` đổi `label`/`desc`, nhận
      `slugs: ['operation','decision','regulations']`, `permissionType: 6`, giữ
      `isShowKey: 'is_use_decision'`
- [x] Xoá `components/default-menu/decision.js` (hết tham chiếu, giữ lại là 2 nguồn menu)
- [x] Thêm `layout: 'default-sidebar'` cho **143 page** `/decision/*` + `/regulations/*` +
      `/human/self-notification*` (user chốt: dùng sidebar hub). Bỏ qua **60 màn in** (giữ nguyên
      như cũ) và **108 file trong `components/`** (Nuxt không đọc `layout` ở component), 17 file đã
      có `layout` sẵn. Script chèn theo **EOL của đúng dòng `export default {`** (repo trộn CRLF/LF)
      → `git diff --numstat` đúng **1 dòng thêm / 0 dòng xoá mỗi file**
- [x] Verify (xem Checkpoint bên dưới)

**Căn cứ chọn `permissionType: 6`:** DB `hrm_erp` có **78 quyền `type = 6`** (`quyết định`) và
**0 quyền `type = 18`** (`vận hành nghiệp vụ`) → lấy 18 là mất 78 quyền khỏi màn phân quyền.

### Checkpoint — Phase 11 (2026-09-16)

**Vừa hoàn thành:** gộp `decision` vào `operation` + đổi tên "Văn bản nội bộ".
6 file component (1 xoá) + 143 file page.

**Lỗi đã TÁI HIỆN trước khi sửa** (đúng quy trình): trên `/decision/decision-reward` với layout cũ,
menu ngang render **14 mục cấp 2 xám mờ** (`.menu-item-pending`) và **màn thật ở tầng 3 biến mất**
— chỉ còn 7 link menu. Sau khi đổi layout: topbar biến mất, rail hub hiện **17 mục**, panel khối
"Quản trị hành chính - nhân sự" báo **5 nhóm · 23 chức năng**, mở nhóm "Quyết định về nhân sự" ra
đủ **12 link thật**.

**Đã kiểm (số đo):**
- Registry: 29 phân hệ, không còn key `decision`; `/decision/*`, `/regulations/*`,
  `/human/self-notification` đều `resolveSubsystem` → `operation`; **355 link toàn app, 5 link
  trùng giữa 2 phân hệ đều là ngoại lệ có sẵn** (assign↔presale, sale↔customer-care, sale↔finance),
  không mục nào liên quan quyết định
- Quyền (test cả ca KHÔNG quyền): user rỗng quyền → 4 màn "Quyết định về tổ chức" **ẩn hết**;
  user chỉ có 1 quyền nhóm `Quyết định` → hiện đủ 4; user chỉ có quyền nhóm khác → ẩn hết.
  Nhóm "Báo cáo" không hiện với DNS Admin vì tài khoản **thiếu 2 quyền** "Xem báo cáo thang bảng
  lương theo tổng công ty/công ty" — gate đúng, không phải lỗi
- `doi-chieu-menu.py` (đã sửa MAP: 2 dòng sheet cùng trỏ `operation-hub.js`): **0 mục thiếu / 22
  phân hệ**
- Màn chọn phân hệ: cánh VĂN PHÒNG SỐ còn **8 phân hệ**, chỉ 1 mục "VĂN BẢN NỘI BỘ — Quyết định,
  Quy chế công ty"; `scrollHeight 785 = viewport 785` → **không sinh thanh cuộn**
- Màn Tổng quan phân hệ: tiêu đề "Phân hệ Văn bản nội bộ", 14 thẻ nhóm, thẻ "Quản trị hành chính -
  nhân sự" ghi 23 chức năng
- `/regulations/general` (103 dòng dữ liệu) và `/human/self-notification` (10 dòng) đều render
  sidebar "VĂN BẢN NỘI BỘ", không còn topbar

**Đang làm dở:** (không)

**Bước tiếp theo:** user duyệt; sau đó verify từng màn con của 5 nhóm (việc còn treo từ Phase 6).

**Blocked:** (không)

⚠️ **Còn lại có chủ đích — 60 màn in `/decision/**/print*.vue`:** giữ nguyên `layouts/default.vue`
nên menu ngang trên đó vẫn là 14 mục xám mờ (chỉ ảnh hưởng thanh menu, nội dung tờ in không đổi).
Chuẩn của team từ 2026-08-20 là `layout: 'print'` (không topbar, nền xám) — đổi 60 file này là
việc riêng, **chưa làm vì ngoài phạm vi yêu cầu**, chờ user chốt.

## Phase 12 — Rút gọn tên 10 phân hệ + gộp tiếp `legal` (2026-09-16, user chốt)

- [x] Đổi `label` (và `permissionLabel` khi nhãn cũ trùng tên phân hệ) cho **10 phân hệ**:

      | key | Tên cũ | Tên mới |
      | --- | --- | --- |
      | `kpi` | Đánh giá KPI | **KPI** |
      | `production` | Quản lý sản xuất | **Sản xuất** |
      | `asset` | Quản lý tài sản | **Tài sản** |
      | `safety-5s` | Quản lý an toàn 5S | **An toàn - 5S** |
      | `assign` | Quản lý công việc | **Công việc** |
      | `sale` | Quản lý bán hàng | **Bán hàng** |
      | `iso` | Hoạt động ISO (quản lý quy trình) | **ISO** |
      | `lookup` | Tra cứu - thông báo | **Thông báo** |
      | `presale` | Quản lý CSKH trước khi bán | **CSKH trước bán** |
      | `customer-care` | CRM | **CSKH sau bán** |

      ⚠️ User gõ "CSKH Sau bán" — tôi viết **"CSKH sau bán"** cho đối xứng với "CSKH trước bán"
      (màn chọn phân hệ in hoa hết nên không ảnh hưởng hiển thị). Báo lại để user bác nếu cần.
      `desc` (subtext) của 10 phân hệ **giữ nguyên** vì user không yêu cầu đổi.
      `permissionLabel` chỉ đổi khi nó chép lại tên phân hệ; `assign` giữ `'giao việc'`,
      `iso` giữ `'hồ sơ ISO'`, `sale` giữ `'bán hàng'` (vốn đã khác nhãn).
- [x] **Gộp `legal` ("Hoạt động pháp lý") vào `operation`** → tên chung
      **"Văn bản - Hồ sơ pháp lý"**, subtext **"Quyết định, quy chế, hồ sơ pháp lý"**:
      - `operation-hub.js`: thêm khối **"Hồ sơ pháp lý"** với đủ **9 mục** của `legal.js` (đều CHƯA
        có màn → giữ dạng chuỗi, render xám mờ), đặt ngay sau khối "Quản trị hành chính - nhân sự"
      - `subsystems.js`: bỏ entry `legal`, `operation` nhận
        `slugs: ['operation','decision','regulations','legal']`
      - Xoá `components/subsystem-menu/legal.js`
      - Giữ `permissionType: 6` — DB có **0 quyền type 15** (`legal`) và 0 quyền type 18, nên không
        mất quyền nào
      - `/legal/dashboard` **không còn trong menu** (hub đã có Tổng quan riêng) nhưng vẫn vào được
        qua slug — y như `/decision/dashboard`
- [x] `pages/index.vue`: sửa ghi chú đã lỗi thời ở `nameOf()` (trước ghi "không rút gọn ISO"),
      nay tên ngắn nằm thẳng trong `label` của registry
- [x] `doi-chieu-menu.py`: MAP `'Hoạt động pháp lý'` trỏ sang `operation-hub.js`

### Checkpoint — Phase 12 (2026-09-16)

**Vừa hoàn thành:** 10 đổi tên + gộp `legal`. 4 file sửa, 1 file xoá — **không đụng file page nào**
(`/legal/*` chỉ có 1 màn dashboard và nó đã khai `layout: 'default-sidebar'` sẵn).

**Đã kiểm (số đo):**
- Registry: **28 phân hệ** (từ 29), không còn key `legal`; 11/11 nhãn mới đúng nguyên văn;
  `/legal/dashboard`, `/legal/abc`, `/decision/*` đều resolve → `operation`
- **354 link** toàn app (giảm 1 = `/legal/dashboard` rời menu), vẫn đúng **5 link trùng** là ngoại
  lệ có sẵn
- `doi-chieu-menu.py`: **0 mục thiếu** (9 mục pháp lý khớp trong khối mới)
- Màn chọn phân hệ: 4 cánh hiện đúng tên mới (KPI · TÀI SẢN · ISO · VĂN BẢN - HỒ SƠ PHÁP LÝ ·
  CÔNG VIỆC · AN TOÀN - 5S · SẢN XUẤT · THÔNG BÁO · CSKH TRƯỚC BÁN · BÁN HÀNG · CSKH SAU BÁN);
  cánh VĂN PHÒNG SỐ còn **7 phân hệ**; `scrollHeight 785 = viewport 785`, không cuộn ngang
- `/legal/dashboard`: rail "VĂN BẢN - HỒ SƠ PHÁP LÝ" **18 mục**, mở khối "Hồ sơ pháp lý" ra đủ
  **9 mục, 0 link** (đúng: chưa xây màn)
- `/customer-care/dashboard` → rail "CSKH SAU BÁN"; `/assign/my-todo` → rail "CÔNG VIỆC" (13 khối)

**Đang làm dở:** (không)

**Bước tiếp theo:** vẫn là danh sách treo A/B/C bên dưới.

**Blocked:** (không)

## Phase 13 — Nền đậm hơn + tên/subtext 1 dòng ở màn chọn phân hệ (2026-09-16, user báo)

User: *"độ tương phản kém, text hơi mờ"* + *"tên phân hệ / subtext chỉ nằm trên 1 dòng"*.

**Đo TRƯỚC khi sửa:** `VĂN BẢN - HỒ SƠ PHÁP LÝ` rớt **2 dòng** (cao 28.3px / line-height 14.2px),
subtext `Quyết định, quy chế, hồ sơ pháp lý` cũng **2 dòng**; ô chữ rộng **139px** trong khi nhãn
cần **156px**, subtext cần **158px**. 6 mục khác chỉ thừa đúng 1px — sát mép rớt dòng.

- [x] `layouts/system.vue` — nền đậm thêm 1 nấc: 4 mốc gradient
      `#1e57a0/#14417e/#0e2f5f/#0a1c3d` → `#17457f/#103460/#0a2244/#061428`; **hạ độ mờ 4 vệt
      sáng góc** `0.38/0.34/0.30/0.36` → `0.22/0.20/0.18/0.21` (chính 4 vệt này nằm đúng chỗ 4
      cánh hoa nên làm chữ trong cánh mờ nhất)
- [x] `pages/index.vue` — chữ phụ sáng hơn: `.app__ds` `#c7d6ee` → `#d5e2f5`,
      `.picker__sub` `#b6c8e2` → `#c9d8ef`; kính cánh hoa `6%/3.5%` → `8%/5%`
- [x] `pages/index.vue` — ép 1 dòng, **nới ô chữ 139px → 158px**: padding né mũi lá `96px → 78px`
      (+18), icon `36 → 32` (+4), gap `10 → 8` (+2), padding ngang mục `6 → 4` (+4),
      `letter-spacing` nhãn `0.3 → 0.15px` (-3px cho nhãn dài nhất);
      `.app__nm` + `.app__ds` thêm `white-space: nowrap; overflow: hidden; text-overflow: ellipsis`
      làm chốt chặn (`.app__tx` đã có `min-width: 0` nên ellipsis chạy đúng)

### Checkpoint — Phase 13 (2026-09-16)

**Đo LẠI sau khi sửa (2 file, 0 file page):**
- **23/23 tên + 23/23 subtext nằm đúng 1 dòng**, và **0 mục bị cắt bằng "…"**
  (`scrollWidth <= clientWidth` cho cả 46 phần tử) — tức nới đủ rộng chứ không phải cắt chữ
- Tỉ lệ tương phản (tính theo WCAG, đã cộng lớp kính trắng của cánh + vệt sáng góc tại đúng vị trí
  4 cánh):

  | Cánh | Tên (chữ trắng) | Subtext |
  | --- | --- | --- |
  | NHÂN SỰ | 6.75 → **9.13** | 4.59 → **6.97** |
  | VĂN PHÒNG SỐ | 6.58 → **9.15** | **4.48** → **6.98** |
  | SẢN XUẤT - CUNG ỨNG | 6.88 → **9.27** | 4.68 → **7.08** |
  | KINH DOANH - TÀI CHÍNH | 7.31 → **9.66** | 4.97 → **7.37** |

  Subtext ở cánh VĂN PHÒNG SỐ trước đây **4.48 < 4.5 = TRƯỢT chuẩn AA**, nay 6.98 (AA cần 4.5,
  AAA cần 7.0). Đúng chỗ user kêu mờ.
- Bố cục không vỡ: 4 cánh vẫn `540×348/228`, **0 mục tràn ngang khỏi cánh**,
  `scrollHeight 785 = viewport 785`, không thanh cuộn ngang
- Padding né mũi lá 78px vẫn an toàn: bán kính bo góc trong của lá chỉ 12px, góc ngoài 78px nằm ở
  mép trên (nơi không có mục nào)

**Bước tiếp theo:** danh sách treo A/B/C bên dưới.

ℹ️ Quan sát thêm (CHƯA sửa vì user không yêu cầu): 2 cánh trên còn **110px trống ở đáy**
(`--petal-h: 348px` đặt từ hồi nhãn còn dài, nay nội dung thấp hơn ~16px so với trước). Muốn cánh
ôm sát nội dung như yêu cầu hôm trước thì hạ `--petal-h` của `.p-tl/.p-tr` xuống ~330px.

## Phase 14 — Chữ nét + 4 cánh hoa bằng nhau (2026-09-16, user báo)

User: *"vẫn có cảm giác nhìn text khá mờ, như bị vỡ pixel"* + *"4 cánh hoa cần có kích thước bằng
nhau cho cân đối, chấp nhận khoảng trống"* + *"2 cánh hoa phía trên đang to một cách dư thừa"*.

**Nguyên nhân chữ mờ — ĐO ĐƯỢC, không phải do màu** (Phase 13 đã sửa màu rồi mà vẫn mờ):

| Nguồn | Số đo trước khi sửa |
| --- | --- |
| `.petal` có `animation: float 7s infinite` dịch **cả cánh (kèm chữ)** theo trục Y | `.petal` y = **96.2665px**, `.app__nm` y = **154.2665px** — toạ độ lẻ, **vẽ lại mỗi khung hình** trên layer hợp thành |
| `line-height: 1.18` (số nhân) | ra **14.16px** / **12.39px** — dòng chữ rơi vào toạ độ lẻ |
| `font-size: 10.5px` ở subtext | cỡ chữ **lẻ nửa pixel** |
| `letter-spacing: 0.15px` | giãn chữ lẻ px, glyph lệch lưới điểm ảnh |

- [x] **Bỏ hẳn `animation: float`** khỏi `.petal` (+ xoá `@keyframes float` và 4 `animation-delay`
      không còn dùng). Muốn giữ hiệu ứng thì phải đặt lên lớp KHÔNG chứa chữ (vd `.petal::before`)
- [x] Khai lại số đo chữ bằng **số nguyên**: `.app__nm` `line-height: 15px`, `letter-spacing: 0`;
      `.app__ds` `font-size: 11px`, `line-height: 14px`; bỏ `line-height: 1.18` ở `.app__tx`
- [x] `.app__ds` `font-weight: 400 → 500` — chữ nhạt + mảnh trên nền tối luôn trông nhoè hơn thực tế
- [x] `subsystems.js`: subtext phân hệ Văn bản rút còn **"Quyết định, quy chế, pháp lý"** để vẫn gọn
      1 dòng sau khi cỡ chữ tăng 10.5 → 11px
- [x] **4 cánh cao BẰNG NHAU = 264px** (trước: trên 348 / dưới 228) + `--stage-h` 642 → **594px**
      theo đúng công thức bắt buộc `2 * petal-h + 66`. Chọn 264 vì đo nội dung thật: cánh 7 mục cần
      **254px**, cánh 5 mục 204px, cánh 4 mục 156px → dư 10px ở cánh cao nhất

### Checkpoint — Phase 14 (2026-09-16)

**Đo lại sau khi sửa:**
- 4 cánh **540×264 bằng nhau tuyệt đối**, `animationName: none` cả 4, **0 mục tràn đáy**
- Chỗ trống đáy: cánh 7 mục **26px**, cánh 5 mục 74px, cánh 4 mục 122px — đúng như user chấp nhận
- **0/46 nhãn+subtext xuống dòng, 0 bị cắt "…"**; `.app__nm` 12px/15px/800,
  `.app__ds` 11px/14px/500 — **không còn số đo lẻ nào**
- `--stage-h` 594px, `scrollHeight 785 = viewport 785`, không cuộn ngang

ℹ️ Còn 1 điểm nhỏ **chưa xử lý**: `.stage` lấy `margin-top` theo công thức `(100vh - 58px -
stage-h) * 0.38` nên khối hoa nằm ở toạ độ **y = 114.539px** (lẻ). Đây là lệch **tĩnh** dưới 1px,
khác hẳn kiểu lẻ + động của `float` — muốn triệt để phải làm tròn bằng `round()` của CSS, nhưng
SCSS hiểu `round()` là hàm của nó nên phải escape, rủi ro hơn lợi ích. Nếu user vẫn thấy mờ thì
đây là chỗ tiếp theo.

## Phase 15 — Sắp lại thứ tự phân hệ trong 2 nhóm (2026-09-16, user chốt)

Thứ tự hiển thị của phân hệ trong 1 nhóm = **thứ tự khai báo trong mảng `SUBSYSTEMS`** (màn chọn
phân hệ, popup chuyển phân hệ và màn Phân quyền đều đọc theo) → đổi bằng cách dời khối khai báo,
không thêm trường `order`.

- [x] **VĂN PHÒNG SỐ**: `asset · iso · operation · training · assign · meeting · safety-5s` →
      **`assign · meeting · operation · training · asset · iso · safety-5s`**
      (Công việc · Meeting · Văn bản - Hồ sơ pháp lý · Đào tạo - đánh giá · Tài sản · ISO · An toàn - 5S)
- [x] **KINH DOANH - TÀI CHÍNH**: `lookup · presale · sale · customer-care · finance` →
      **`presale · sale · customer-care · finance · lookup`**
      (CSKH trước bán · Bán hàng · CSKH sau bán · Tài chính · Thông báo).
      `accounting` ẩn (chỉ giữ khối quyền) nên để nguyên cuối nhóm.
- [x] Sửa chú thích đã sai của `lookup` ("đứng đầu nhóm" → nay xếp cuối) + ghi **quy ước thứ tự**
      vào khối chú thích đầu `subsystems.js` cho người sau

### Checkpoint — Phase 15 (2026-09-16)

- Đo DOM màn chọn phân hệ: 2 cánh ra **đúng thứ tự user yêu cầu**, 2 cánh còn lại không đổi
- 4 cánh vẫn **540×264**, **0 nhãn/subtext rớt dòng hay bị cắt**, `scrollHeight 783 = viewport 783`
- ⚠️ Kéo theo: **màn Phân quyền cũng đổi thứ tự khối** (nó cũng đọc thứ tự mảng này) — đúng ý đồ,
  không phải lỗi

## Phase 16 — Duyệt lại TỪNG PHÂN HỆ: (1) CSKH trước bán (2026-09-16, user chốt)

User bắt đầu rà từng phân hệ, đưa danh sách menu mong muốn. 2 quyết định user chốt khi hỏi:
**dời hẳn** (không dùng chung) và **bỏ hết** mục không nằm trong danh sách.

- [x] Dời hẳn **11 mục** về CSKH trước bán:
      - 3 danh mục nền từ `master-data.js`: Nhóm ngành · Nhóm giải pháp · Ứng dụng (giữ nguyên `isShow`)
      - 5 danh mục dự án từ `sale-hub.js`: Hạng mục · Giai đoạn · Vai trò dự án · Phiếu thu thập
        thông tin · Lý do thất bại (nhóm "Dự án - Giải pháp" bên Bán hàng rỗng → bỏ luôn nhóm)
      - 3 báo cáo từ `meeting.js`: meeting theo nhân viên · theo dự án · theo thị trường
- [x] Bỏ khỏi CSKH trước bán: Báo giá · Nhiệm vụ · Vấn đề · "Phát triển KH theo NVKD" ·
      "Tổng hợp GP theo phòng ban" · cả nhóm "Báo cáo thị trường" (14 mục ERP chưa có màn)
- [x] Cấu trúc mới: **Tổng quan · Danh mục (8) · Dự án TKT · Yêu cầu giải pháp · Yêu cầu báo giá ·
      Báo cáo (8)** — 3 mục giữa khai ở CẤP 1 nên sidebar hub render thành **nút rail đi thẳng**
- [x] Sửa 1 nhãn khai SAI so với màn thật: "Dự án TKT theo PB-NV KD" →
      **"Báo cáo vòng đời dự án TKT"** (đúng tiêu đề trong
      `pages/assign/report/prospective-projects/index.vue`)
- [x] `doi-chieu-menu.py`: khai 13 mục lệch vào `BO_QUA` kèm lý do (sheet vẫn để ở phân hệ cũ)
- [x] 17/09: user chốt đưa nhóm **Danh mục xuống DƯỚI Báo cáo** → thứ tự chốt:
      `Tổng quan · Dự án TKT · Yêu cầu giải pháp · Yêu cầu báo giá · Báo cáo · Danh mục`
      (đo rail + thẻ Tổng quan trên trình duyệt: đúng thứ tự, mỗi nhóm vẫn 8 chức năng)

### Checkpoint — Phase 16 (2026-09-16)

- Menu CSKH trước bán ra **đúng 5 khối user liệt kê**, 16 link + 1 Tổng quan, **0 mục thiếu link**
- Rail trên trình duyệt: `Tổng quan · Dự án TKT · Yêu cầu giải pháp · Yêu cầu báo giá · Danh mục ·
  Báo cáo`; thẻ Tổng quan báo **Danh mục 8 chức năng / Báo cáo 8 chức năng**
- Mở màn đã dời (`/assign/project_items`): rail hiện **"CSKH TRƯỚC BÁN"**, bảng có dữ liệu thật
  (2 dòng) → `resolveSubsystem` theo đúng phân hệ mới
- **Link trùng giữa 2 phân hệ giảm 5 → 3** (bỏ Nhiệm vụ/Vấn đề khỏi presale); 3 link còn lại là
  ngoại lệ có sẵn của Bán hàng
- `doi-chieu-menu.py`: **0 mục thiếu / 22 phân hệ** sau khi khai 13 ngoại lệ có lý do

⚠️ **3 màn tạm thời MỒ CÔI** (không còn ở menu của phân hệ nào) do quyết định "bỏ hết":
`/assign/quotations` (Báo giá) · `/assign/report/customer-development` (Phát triển KH theo NVKD) ·
`/assign/report/solutions-work-summary-by-department` (Tổng hợp GP theo phòng ban).
Màn vẫn chạy nếu gõ thẳng URL. Chờ lượt duyệt phân hệ **Bán hàng** / **Công việc** để khai lại —
sheet Bán hàng đang có mục "Báo giá dự án" chưa gắn link, nhiều khả năng `/assign/quotations`
thuộc về đó.

## Phase 17 — Duyệt phân hệ (2): Bán hàng (2026-09-17, user chốt)

- [x] **Menu Báo cáo dựng lại dạng hub cho gọn**: bỏ cấp bọc `"Báo cáo bán hàng"` (mục duy nhất
      trong cả registry còn dùng `subs` = 4 cấp) → 6 nhóm con của nó thành **mục cấp 1** của khối
      Báo cáo, ngang hàng với `Báo cáo công nợ`. Khối Báo cáo: **7 nhóm · 36 chức năng**, giữ
      nguyên toàn bộ màn (tổng phân hệ vẫn **152 màn**).
- [x] **Đưa nhóm Danh mục xuống DƯỚI Phê Duyệt**: thứ tự rail nay là `Bán hàng · Bán dịch vụ ·
      Yêu cầu · Báo cáo · Kế hoạch · Phê Duyệt · Danh mục · Quy chế - Thiết lập`

### Checkpoint — Phase 17 (2026-09-17)

- Rail + thẻ màn Tổng quan: **đúng thứ tự mới**, `Báo cáo (36 chức năng)`, `Danh mục (9)` đứng sau
  `Phê Duyệt (20)`
- Panel Báo cáo: tiêu đề **"7 nhóm · 36 chức năng"**, **0 phần tử `.sub__t--parent`, 0 `.subkids`**
  → hết hẳn kiểu lồng 3 cấp mà Phase 10 phải vá CSS. Panel render 2 cột kiểu hub: 7 chip nhóm kèm
  số đếm bên trái + danh sách màn bên phải; bấm `Báo cáo công nợ` → cột phải đổi đúng **6 màn**
- `doi-chieu-menu.py`: **0 mục thiếu / 22 phân hệ**
- ℹ️ CSS `.sub__t--parent` / `.subkids` trong `SaleHubSidebar.vue` (Phase 10) nay **không còn menu
  nào dùng** — giữ lại phòng khi có menu 4 cấp mới, không xoá.

## Phase 18 — Duyệt phân hệ (3): Công việc (2026-09-17, user chốt)

- [x] **Chuyển nhóm Phê duyệt xuống DƯỚI Báo cáo** — thứ tự rail nay: `Tổng quan · Lịch làm việc
      của tôi · Công việc của tôi · Làm giải pháp · Nhiệm vụ · Tiếp nhận công việc · Phân công công
      việc · Kết quả công việc · Báo cáo · Phê duyệt · Thiết lập`
- [x] **Phê duyệt chuyển sang dạng hub**: 1 nhóm phẳng 12 mục → **5 mục cấp 1 cùng
      `hubGroup: 'Phê duyệt'`** (cơ chế sẵn có của `deriveHubGroups`), rail vẫn 1 nhóm "Phê duyệt"
      nhưng panel ra 5 chip: `Giải pháp - Dự án (2) · Đề xuất (2) · Giao việc (3) · Công tác (3) ·
      Bàn giao - Lắp đặt (2)`. Khai `hubIcon` ở mục đầu để rail giữ icon dấu tích.
- [x] `doi-chieu-menu.py`: dạy script đọc thêm `hubGroup` — tên nhóm hub là tên người dùng NHÌN
      THẤY, không khai `label` nên trước đó script báo thiếu oan mục "Phê duyệt" của sheet

### Checkpoint — Phase 18 (2026-09-17)

**Lỗi bắt được KHI ĐO TRÊN TRÌNH DUYỆT (chia 4 chip là chưa đủ):**
panel vẫn đổ **danh sách phẳng 11 dòng**, `.scat` = 0. Nguyên nhân: `SaleHubSidebar.vue` /
`SaleMenuHub.vue` chỉ bật NAV-MODE (2 cột chip) khi `group.items.length >= NAV_MIN` mà
**`NAV_MIN = 5`**. → tách "Đề xuất - Giao việc" thành 2 chip riêng cho đủ 5, KHÔNG hạ ngưỡng
(hạ ngưỡng sẽ đổi kiểu hiển thị của mọi nhóm 3-4 mục ở tất cả phân hệ).

**Đo lại sau khi sửa:**
- Panel Phê duyệt: `navMode = true`, tiêu đề **"5 nhóm · 11 chức năng"**, 5 chip đúng tên + số đếm;
  bấm chip `Giao việc` → cột phải đổi đúng 3 màn
- **11/12 chức năng** là ĐÚNG: "Gia hạn dự án TKT" bị ẩn vì tài khoản đang đăng nhập **không có**
  `Trưởng phòng duyệt gia hạn dự án TKT` / `Ban giám đốc duyệt gia hạn dự án TKT` (đã đọc
  `$store.state.permissions` để xác nhận) — gate đúng, không mất màn
- Registry: **44 link** của phân hệ Công việc giữ nguyên, hub tổng **57 màn** như trước
- `doi-chieu-menu.py`: **0 mục thiếu / 22 phân hệ**

## Phase 19 — Công việc: tách "Vấn đề" lên cấp 1 + gom nhóm "Bàn giao công việc" (2026-09-17)

- [x] **"Vấn đề" thành mục cấp 1**, đặt ngay dưới nhóm "Nhiệm vụ" → rail render nút đi thẳng
      (`/assign/issues`). Nhóm "Nhiệm vụ" còn 2 màn (Nhiệm vụ · Cập nhật tiến độ task).
- [x] **Nhóm mới "Bàn giao công việc"** đặt ngay dưới "Kết quả công việc", gom 5 màn: `Phiếu bàn
      giao` · `Tạo bàn giao` · `Chờ tiếp nhận bàn giao` (lấy từ nhóm Nhiệm vụ) + `Biên bản bàn giao
      sơ bộ` · `Biên bản bàn giao nghiệm thu` (lấy từ nhóm Kết quả công việc, cả 2 còn bên ERP nên
      chưa có link). "Kết quả công việc" còn 9 màn.
      ⚠️ Màn DUYỆT `Bàn giao công việc` (`/assign/handover/pending`) **giữ ở Phê duyệt › Bàn giao -
      Lắp đặt** vì là màn duyệt, không phải màn tạo/theo dõi — báo user, đổi được nếu muốn.
- [x] Đổi nhãn `Cập nhật tiến độ task` → **`Báo cáo kết quả nhiệm vụ`** (link `/assign/tasks/
      daily-report` giữ nguyên; khai thêm ngoại lệ trong `doi-chieu-menu.py` vì sheet còn tên cũ).
      ℹ️ Tiêu đề TRONG màn vẫn là "Nhập kết quả báo cáo tiến độ" — user mới yêu cầu đổi nhãn menu,
      chưa đổi tiêu đề màn.
- [x] **Sửa `SaleHubSidebar.vue`: rail xếp theo ĐÚNG thứ tự khai trong menu.**
      Template cũ render hết `navLinks` rồi mới tới `groups` → mục lẻ cấp 1 luôn bị đẩy lên đầu
      rail, không thể đặt "Vấn đề" dưới "Nhiệm vụ". Thêm computed `railItems` trộn 2 danh sách,
      khoá sắp xếp là vị trí của `hubGroup || label` trong `subsystem.menu`; mục không tra được
      (hub khai tay) xếp sau, giữ thứ tự cũ.

### Checkpoint — Phase 19 (2026-09-17)

- Rail phân hệ Công việc (đo DOM, kèm cờ `cat-nav`): `Tổng quan → Lịch làm việc của tôi → Công việc
  của tôi → Làm giải pháp → Nhiệm vụ → **Vấn đề** (nav, href=/assign/issues) → Tiếp nhận công việc →
  Phân công công việc → Kết quả công việc → **Bàn giao công việc** → Báo cáo → Phê duyệt → Thiết lập`
- Panel "Bàn giao công việc": **5 chức năng** đúng danh sách; panel "Nhiệm vụ": **2 chức năng**
- Tổng link phân hệ vẫn **44**, tổng màn hub vẫn **57** (56 trong nhóm + 1 nút đi thẳng)
- `doi-chieu-menu.py`: **0 mục thiếu / 22 phân hệ**
- **Kiểm phân hệ khác không vỡ do sửa component dùng chung:** rail Bán hàng và CSKH trước bán giữ
  nguyên thứ tự cũ. Riêng **Tài chính đổi 1 vị trí**: nút "Khai Quy chế – Cấu hình" trước nổi lên
  ngay sau Tổng quan, nay nằm sau nhóm "Tài chính" — **đúng thứ tự khai trong `finance.js`**, tức
  là sửa đúng chứ không phải lỗi.

## Phase 20 — Popup chuyển phân hệ trên topbar: đổi tên nhóm lõi + đổi thứ tự nhóm (2026-09-17)

- [x] `GROUP_CORE`: **'LÕI HỆ THỐNG' → 'QUẢN TRỊ'** (CSS của popup tự viết hoa nên hiển thị
      "QUẢN TRỊ"). Cập nhật luôn các chú thích còn gọi tên cũ ở `subsystems.js`, `admin.js`,
      `master-data.js`.
- [x] `SUBSYSTEM_GROUPS` đổi thứ tự theo user: **Kinh doanh - Tài chính → Văn phòng số → Sản xuất -
      cung ứng → Nhân sự → Quản trị** (ERP vẫn cuối, popup lọc bỏ). Ghi rõ trong chú thích: số
      `1. 2. 3. 4.` ở tên nhóm là SỐ CỦA SHEET, không phải thứ tự hiển thị (nơi hiển thị đều cắt
      tiền tố `^\d+\.\s*`).

### Checkpoint — Phase 20 (2026-09-17)

- Popup topbar (đo DOM): **5 nhóm đúng thứ tự** `KINH DOANH - TÀI CHÍNH (5) · VĂN PHÒNG SỐ (7) ·
  SẢN XUẤT - CUNG ỨNG (4) · NHÂN SỰ (7) · QUẢN TRỊ (3)`
- Màn chọn phân hệ dạng hoa **KHÔNG đổi**: 4 cánh vẫn đúng vị trí cũ (NHÂN SỰ trên-trái, VĂN PHÒNG
  SỐ trên-phải, SẢN XUẤT dưới-trái, KINH DOANH dưới-phải) vì `pages/index.vue` gắn cứng nhóm vào
  cánh qua `QUADS`; nhuỵ vẫn 3 phân hệ lõi; không sinh thanh cuộn (773 = 773)
- ⚠️ 2 màn khác cũng đọc `SUBSYSTEM_GROUPS` nên **đổi thứ tự khối theo**: màn **Phân quyền**
  (`permissionBlocks()`) và màn **Cài đặt phân hệ** (`pages/timesheet/setting/subsystems`) — nhất
  quán với popup, không phải lỗi.

## Phase 21 — Kho / Mua hàng / Vận chuyển: bấm vào đi thẳng sang ERP (2026-09-17)

3 phân hệ này `hidden: true` + `erpGhost: true` (nghiệp vụ ở lại ERP). Trước đây chưa khai link nên
click chỉ hiện toast "Tính năng đang phát triển".

- [x] `subsystems.js`: khai **`erpPath`** (đường dẫn tương đối, tự ghép `ERP_URL`) — KHÔNG dùng
      `erpLink` tuyệt đối để khỏi phải sửa code khi đổi tên miền ERP:

      | Phân hệ | erpPath | Màn bên ERP |
      | --- | --- | --- |
      | Mua hàng | `/admin/orders/root_order_request?_type=all` | Phiếu yêu cầu đặt hàng |
      | Kho | `/admin/warehouse/warehouse_imports/all` | Phiếu nhập kho |
      | Vận chuyển | `/admin/warehouse/delivery_trips/all` | Chuyến xe chở hàng |

      3 đường dẫn lấy từ chính `routes/web.php` của ERP (dò prefix group để ra URI đầy đủ), đối
      chiếu nhãn trong `resources/views/layouts/topmenubar.blade.php`.
- [x] `pages/index.vue`: thêm `erpHrefOf()` — `erpPath` ghép `ERP_URL`, `erpLink` giữ nguyên cho
      trường hợp URL tuyệt đối; dùng chung cho cả `linkOf()` (thẻ `<a href>`, mở tab mới được) lẫn
      `onClick()`. Không khai gì thì vẫn giữ toast cũ.

### Checkpoint — Phase 21 (2026-09-17)

- Đo DOM màn chọn phân hệ: 3 thẻ nay là `<a>` với href thật
  (`http://qttt.tanphat.com/admin/...`), **0/23 thẻ còn thiếu href** (trước đó 3 thẻ này không có)
- ⚠️ `ERP_URL` phía client suy từ `TP_URL` trong `hrm-client/.env`, hiện trỏ **ERP production**
  (`http://qttt.tanphat.com`) vì dòng `ERP_URL=http://127.0.0.1:8001` đang bị comment. Chạy local
  mà muốn sang ERP local thì bỏ comment dòng đó.

### Checkpoint — WRAP UP phiên 17/09/2026

**Vừa hoàn thành trong phiên này (Phase 16 → 21):**
duyệt lại từng phân hệ theo yêu cầu user — CSKH trước bán (dời hẳn 11 mục về, bỏ mục thừa, Danh mục
xuống cuối) · Bán hàng (Báo cáo dựng lại dạng hub 7 nhóm, Danh mục xuống dưới Phê Duyệt) · Công việc
(Phê duyệt xuống dưới Báo cáo + dạng hub 5 chip, "Vấn đề" lên cấp 1, nhóm mới "Bàn giao công việc",
đổi nhãn "Báo cáo kết quả nhiệm vụ") · popup topbar (đổi tên nhóm lõi thành QUẢN TRỊ + đổi thứ tự 5
nhóm) · Kho/Mua hàng/Vận chuyển gắn `erpPath` đi thẳng ERP. Kèm 2 sửa component dùng chung:
`hub.js::isScreenVisible` thêm nhánh `groups`, `SaleHubSidebar.vue` thêm `railItems` (rail xếp theo
đúng thứ tự khai trong menu).

**Số đo chốt phiên:** registry **28 phân hệ · 357 link · 3 link trùng** (đều là ngoại lệ có sẵn);
`doi-chieu-menu.py` **0 mục thiếu / 22 phân hệ**.

**Trạng thái git:** toàn bộ thay đổi đã được commit (working tree sạch). Nhánh đã có thêm commit của
@junfoke: `dc57d23b1 "fix mất màn không có trong sheet"`.

**Đã viết xong tài liệu còn nợ:** `docs/superpowers/specs/gop-db/2026-09-16-quy-hoach-lai-menu-phan-he-design.md`
(spec đầy đủ: mô hình menu, bất biến, 28 phân hệ, 2 lần gộp, 3 phân hệ đã duyệt, ERP ghost, màn chọn
phân hệ, cách kiểm chứng).

**Bước tiếp theo:** duyệt tiếp các phân hệ còn lại (Meeting · Văn bản - Hồ sơ pháp lý · Tài chính ·
CSKH sau bán · nhóm NHÂN SỰ…), rồi quay lại nhóm A của danh sách treo (verify từng màn con + chạy e2e).

**Blocked:** (không)

### Việc còn lại — DANH SÁCH TREO (chốt lại 16/09/2026, làm sau)

Sắp theo mức ưu tiên tôi đề xuất. Mục nào user đã chốt hướng thì ghi rõ ở dòng đó.

**A. Kiểm thử còn nợ**

- [ ] **A1. Verify từng màn con của 5 nhóm menu** — mới verify khung + 3 màn tách + 1 dropdown +
      phân hệ Văn bản nội bộ. Cách làm gợi ý: duyệt 355 link trong registry, vào từng màn đo
      (HTTP 200 · body không rỗng · không lỗi console · mục xám mờ đúng chỗ).
- [ ] **A2. Chạy lại bộ e2e** — Phase 11 đụng 143 file page + 6 file menu mà **chưa chạy ca e2e
      nào**. Nhớ `--workers=1` và không chạy khi có session khác đang thao tác dữ liệu.
- [ ] **A3. Ca KHÔNG quyền trên trình duyệt thật** — mới test ở mức hàm (`hubGroupsFor` với mảng
      quyền rỗng). Nên đăng nhập 1 tài khoản quyền hẹp để xem rail/panel Văn bản nội bộ.

**B. Việc chờ user chốt**

- [ ] **B1. 60 màn in `/decision/**/print*.vue`** — đang giữ `layouts/default.vue` nên thanh menu
      trên đó là 14 mục xám mờ (nội dung tờ in không đổi). Chuẩn team từ 20/08 là `layout: 'print'`
      (bỏ topbar, nền xám `#eee`). Đổi hay để nguyên?
- [ ] **B2. Menu ngang tràn ở màn hẹp (< ~1500px)** với phân hệ nhiều nhóm còn dùng topbar
      (Thông tin NS, Chấm công, Tính lương, Quản lý cơm) — rút gọn nhãn / gom nhóm / chấp nhận?
- [ ] **B3. Lỗi `cancelItem` để lại dòng rỗng** ở màn Tỉ lệ đóng BHXH — code giống hệt màn gốc
      `pages/human/settings/index.vue:581`, nên sửa thì **sửa cả 2 chỗ**. Xem Checkpoint Verify
      Phase 2b.
- [ ] **B4. Màn quyết định phần lớn KHÔNG khai `isShow`** (kế thừa nguyên văn từ `decision.js`:
      "Quyết định tiếp nhận nhân sự", "Quyết định nghỉ hưu"… ) → ai vào phân hệ cũng thấy. Không
      phải lỗi mới của Phase 11, nhưng nếu muốn siết quyền thì đây là chỗ khai.

**C. Nợ tài liệu / dọn dẹp**

- [x] ~~**C1. Spec chi tiết chưa tồn tại**~~ → **ĐÃ VIẾT 17/09/2026**:
      `docs/superpowers/specs/gop-db/2026-09-16-quy-hoach-lai-menu-phan-he-design.md`.
- [ ] **C2. `permissionType: 18`** ("vận hành nghiệp vụ") nay **không phân hệ nào dùng** → khối đó
      biến mất khỏi màn phân quyền. Vô hại vì DB có 0 quyền type 18, nhưng nếu sau này khai quyền
      cho các khối nghiệp vụ mới thì phải quyết dùng lại 18 hay gộp vào 6.
- [ ] **C3. Nút `+` thêm dòng bảng BHXH** là `<i class="fa fa-plus">` (không phải `button`),
      `cursor: auto`, nằm ở cột cuối (x≈1978) nên phải cuộn ngang mới thấy — kế thừa từ màn gốc.
- [ ] **C4. `components/human-components/human-slidebar.vue`** vẫn còn link `/human/employee`
      (slidebar cũ, ngoài registry) → màn Tài khoản nhân viên vào được từ 2 nơi.
- [ ] **C5. `PermissionsTableSeeder` khai TRÙNG quyền tiền tệ** (id 1115/1116 và 1117/1118) →
      chạy seeder trên DB sạch sẽ nổ lỗi trùng khoá. Ghi ở STATUS.md từ 07/08, chưa ai sửa.

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

- ~~Phân hệ dùng topbar chưa có kiểu "xám mờ"~~ → **đã làm ở Phase 2b** (`Topbar.vue` có
  `:disabled="!item.link || item.link === '#'"` + `.menu-item-pending`), verify DOM 16/09.
  (Ghi chú gốc) Phân hệ dùng **topbar** (Thông tin nhân sự, Chấm công, Tính lương, Quản lý cơm, Quyết định)
  render bằng `components/Topbar.vue` — **chưa có kiểu "xám mờ"** cho mục không có `link` như
  `Sidebar.vue`. Mục chưa có màn ở các phân hệ này (Cấu hình tiền lương, Báo cáo thu nhập,
  Tỉ lệ đóng BHXH…) hiện render thành mục bấm không đi đâu. Muốn xám mờ phải sửa `Topbar.vue`
  (component dùng chung → hỏi user trước).

---

## Chỉnh 05/10/2026 — Menu Báo cáo phân hệ CSKH trước bán (@namdangit)

Nhánh `hrm-client` `gop_db-menu-presale-bao-cao` (tách từ `gop_db`, worktree `websites/wt-fix-tkt-linh-vuc`). Chỉ sửa `components/subsystem-menu/presale.js`.

- [x] Nhóm "Báo cáo thị trường" lên ĐẦU rail Báo cáo, "Báo cáo dự án tiền khả thi" xuống sau
- [x] "Báo cáo kế hoạch & kết quả làm việc theo nhân viên" dời sang nhóm Báo cáo thị trường, vị trí đầu (giữ nguyên `isShow` 3 quyền)
- [x] `hubIcon: 'ri-file-chart-line'` dời theo sang nhóm đứng đầu — icon nút rail lấy từ MỤC ĐẦU nhóm (`hub.js`), không dời là icon đổi thành `ri-map-pin-line`
- [x] Kiểm Playwright MCP: panel "2 nhóm · 13 chức năng", thị trường 7 (mục đầu = báo cáo theo NV, href đúng), TKT 6
- [x] E2E mới `e2e/tests/assign/presale-report-menu.spec.ts`: xanh trên 3021, đỏ trên code cũ 3000
- [ ] ⚠️ Khoá ẩn/hiện menu (`menu_settings.menu_key`) theo ĐƯỜNG NHÃN — mục dời nhóm đổi khoá; local 0 dòng, production cần kiểm trước khi deploy
- [ ] Commit + merge về `gop_db` (chờ user)
