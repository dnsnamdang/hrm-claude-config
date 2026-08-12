# Plan — Chuyển menu Nhóm giải pháp + Ứng dụng sang Danh mục dùng chung

> @khoipv · nhánh `gop_db` (cả 2 repo) · chỉ đụng `hrm-client`
> Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-08-12-chuyen-menu-nhom-giai-phap-design.md`

## Phase 0 — Khảo sát & chốt yêu cầu

- [x] Kiểm tra nhánh 2 repo (`gop_db` / ancestor) → áp dụng quy tắc `.plans/gop-db/`
- [x] Đọc lại spec đợt `chuyen-menu-nhom-nganh` để dùng chung khuôn
- [x] Khảo sát hiện trạng: `sale-hub.js:197-198`, `sale.js:45-46`, `master-data.js`
- [x] Grep toàn repo tìm nơi khai/khai chéo 2 link (không có khai trùng; 3 link chéo dạng `<a :href>`)
- [x] Đối chiếu 2 icon trong `_remixicon.scss` (`ri-lightbulb-line`, `ri-apps-2-line`)
- [x] Chốt với user: chuyển 2 mục · 2 mục cấp 1 phẳng · chỉ menu
- [x] Viết spec chi tiết + design tóm tắt

## Phase 1 — Sửa menu (FE)

- [x] `components/subsystem-menu/sale-hub.js` — xoá 2 dòng khỏi mục `Dự án - Giải pháp`, để lại ghi chú chuyển đi
- [x] `components/subsystem-menu/sale.js` — xoá 2 entry `SALE_LINK_PERMISSIONS` (code chết)
- [x] `components/subsystem-menu/master-data.js` — thêm 2 mục cấp 1 sau `Nhóm ngành`, giữ nguyên link + tên quyền

## Phase 2 — Verify tự động (không cần trình duyệt) — 21/21 PASS

Cách làm: mini-loader Node (babel transform ES→CJS, tự resolve alias `@/`) **nạp thật**
`subsystems.js` + `hub.js` + 3 file menu rồi gọi đúng hàm production.

- [x] Mỗi link khai đúng 1 phân hệ (5 link kiểm: 2 link mới + industry-groups + project_items + banks)
- [x] `resolveSubsystem()` trả `master-data` cho 2 link mới; `project_items` vẫn `sale`; `/assign/tasks` vẫn `assign`
- [x] `deriveHubNavLinks(masterDataItems)` = Tổng quan | Ngân hàng | Nhóm ngành | **Nhóm giải pháp** | **Ứng dụng**
- [x] `hubNavLinksFor()` lọc quyền: 0 quyền → ẩn cả 2 · 1 quyền → hiện đúng 1 · đủ quyền → hiện cả 2
- [x] Icon khai đúng (`ri-lightbulb-line`, `ri-apps-2-line`), `isShow` đều là mảng 2 tên quyền
- [x] Bán hàng: `Dự án - Giải pháp` còn 4 mục · cây `saleItems` không còn 2 link · `Danh mục chung` vẫn 3 mục

📌 2 lần FAIL đầu đều là **kỳ vọng của test sai**, không phải lỗi code:
(1) mục `Ngân hàng` khai `isShow: true` nên luôn hiện kể cả 0 quyền — phải lọc riêng 2 mục mới khi assert;
(2) `isScreenVisible()` so `p.name` → `permissions` phải truyền mảng **object** `{name}`, không phải mảng chuỗi.

## Phase 4 — "Loại hình hoạt động KH": tách lên cấp 1 rồi HOÀN TÁC (2026-08-12)

Bối cảnh: user yêu cầu "chuyển tiếp menu Loại hình hoạt động kinh doanh khách hàng". Khảo sát cho
thấy màn này (`/assign/customer-scope-groups`) **đã ở phân hệ Danh mục dùng chung từ trước**
(chuyển khỏi Giao việc, xem `menu-sidebar.js:234`), đang nằm trong nhóm cấp 2 `Đối tác`
→ hỏi lại user, chốt tách lên mục cấp 1 phẳng. **Sau đó user đổi ý: giữ ở nhóm `Đối tác`.**

- [x] (đã làm) `master-data.js` — tách mục lên cấp 1 sau `Ứng dụng`, icon `ri-briefcase-line`
- [x] (đã hoàn tác) trả mục về `Đối tác.subItems` đúng vị trí cũ (giữa `Khách hàng` và
      `Lĩnh vực kinh doanh KH`), bỏ icon + comment thừa → `git diff` quanh `customer-scope-groups` **rỗng**
- [x] Verify lại toàn bộ: **29/29 PASS** — rail về đúng 5 mục (Tổng quan | Ngân hàng | Nhóm ngành |
      Nhóm giải pháp | Ứng dụng) · nhóm `Đối tác` đủ 8 mục đúng thứ tự · không còn mục nào cấp 1
      trỏ `/assign/customer-scope-groups`

→ **Chốt cho lần sau: không đề xuất tách mục này lên cấp 1 nữa.**

## Phase 3 — Kiểm tra trên app (user tự bấm khi dùng)

> **KHÔNG chạy Playwright cho feature này** (user chốt 2026-08-12). Phần đảm bảo chất lượng dựa vào
> 29/29 check tự động ở Phase 2 — nạp thật module menu + gọi đúng hàm production. Checklist dưới
> để user rà bằng mắt lúc tiện, không phải cổng nghiệm thu.

- [ ] `/assign/solution-groups`, `/assign/application` → sidebar Danh mục dùng chung, dữ liệu lên bình thường
- [ ] `/sale/dashboard` → `Dự án - Giải pháp` còn 4 mục
- [ ] `/master-data/dashboard` → có 2 mục mới, icon hiện đúng
- [ ] Tài khoản thiếu quyền → 2 mục bị ẩn
- [ ] 3 link chéo (industry-groups → solution-groups/application, solution-groups → application) chạy đúng
- [ ] (Phase 4) Nhóm `Đối tác` vẫn đủ 8 mục như cũ, `Loại hình hoạt động KH` nằm trong đó — xác nhận
      việc hoàn tác không để lại dấu vết

⚠️ Bẫy: tài khoản dev đang đăng nhập có **0 quyền** → mọi màn gated bị `middleware/checkPermission.js`
đẩy về `/pages/extras/404`. Không phải lỗi của đợt này.

---

### Checkpoint — 2026-08-12
Vừa hoàn thành: Phase 0 + Phase 1 (3 file menu) + Phase 2; Phase 4 tách "Loại hình hoạt động KH" lên cấp 1 rồi HOÀN TÁC theo yêu cầu user — 29/29 check tự động PASS
Đang làm dở: không có — code xong
Bước tiếp theo: không còn việc bắt buộc. Không test Playwright (user chốt); user restart
`npm run dev` rồi rà bằng mắt lúc tiện theo checklist Phase 3
Blocked:

### Checkpoint — 2026-08-12 (HOÀN THÀNH)
Vừa hoàn thành: user chốt đóng feature → chuyển sang mục **Hoàn thành** trong
`.plans/gop-db/STATUS.md`.
Đang làm dở: không có.
Bước tiếp theo: không còn việc trong phạm vi feature này. 6 ô checklist Phase 3 vẫn để `[ ]` vì là
phần user tự rà bằng mắt lúc tiện — không tick thay.
Blocked: không có.
