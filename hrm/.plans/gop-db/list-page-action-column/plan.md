# Plan — Chuẩn cột Hành động màn danh sách (màn mẫu: khách hàng)

## Phase 1 — Component + màn mẫu

### FE

- [x] Tạo `components/V2BaseRowActions.vue` — tối đa 3 nút, dư thì 2 nút chính + menu "⋮" dọc; menu appendChild ra body + position fixed để không bị bảng cắt
- [x] `pages/assign/customers/index.vue`: bỏ cụm nút trong ô "Mã KH - Tên KH", tên KH thành link chi tiết (`linkUrl` của `V2BaseTitleSubInfo`)
- [x] Bỏ nút Khóa/Mở khóa khỏi ô Trạng thái, ô chỉ còn badge
- [x] Đổi khoá cột `status` → `customerStatus`, dời xuống cuối `allColumns` (ngay trước cột Hành động)
- [x] Thêm `actionsColumn` chốt cuối bảng, không đưa vào modal Cấu hình cột
- [x] Viết lại `getRowActions`: Sửa + Khóa/Mở khóa (chính), Quản lý + Lịch sử (menu ⋮); bỏ hành động Xem
- [x] `handleRowAction` nhận thêm `lock` / `unlock`; gỡ `viewCustomer` và style `.action-icon-btn` không dùng nữa
- [x] Chuẩn hoá căn lề cột: STT + Trạng thái + Hành động center (kèm width cố định), quy tắc chung ghi ở design.md
- [x] Ghi quy tắc vào skill chung `.claude/skills/list-page/SKILL.md` (mục "Cột Hành động") + xuất Excel tra cứu `quy-tac-can-le-cot.xlsx` (3 sheet)
- [x] Cột "Mã - Tên": đổi header (bỏ "Mã KH - Tên khách hàng"), bật sticky 2 cột đầu theo khuôn assign/prospective-projects
- [x] Tinh chỉnh độ rộng: STT 48px, cột Mã - Tên minWidth 300px
- [x] `V2BaseTitleSubInfo`: title dạng link đổi sang xanh brand #1abc9c (bỏ `color: #111 !important`) — user chốt áp dụng toàn bộ
- [x] Rà soát theo skill button-convention: nút Cấu hình cột đổi sang V2BaseIconButton; icon xuất file tách theo định dạng (CSV/Excel/PDF); Quản lý đổi ri-settings-3-line → ri-folder-user-line; đồng bộ 2 skill (bảng icon + thứ tự nút cột hành động, bỏ nút Xem)
- [x] Bổ sung mục 4 "Chuẩn text trên nút" vào skill button-convention (quy tắc chữ + bảng text chuẩn 25 hành động + cột KHÔNG dùng); đồng bộ tên hành động trong bảng icon về dấu kiểu mới
- [x] Màn KH: đổi nút "Import" → "Import Excel"
- [x] `V2BaseDataTable`: dòng đếm bỏ đuôi tên đối tượng → `Hiển thị 1–10 / 17542`; ghi quy tắc vào skill list-page
- [x] Bỏ prop `title`/`subtitle` của V2BaseFilterPanel ở màn KH → dùng mặc định "Bộ lọc danh sách"; ghi quy tắc vào skill list-page
- [x] Đổi kiểu link title sang khuôn "mã phiếu" của mockup-report.html (navy + dashed underline + ↗, hover teal)
- [x] Bỏ viền/quầng xanh khi focus ô nhập: sửa 10 component base + rule chung trong v2-styles.scss; ghi vào skill list-page
- [x] Bỏ nền đỏ khi hover nút × của select (V2BaseSelect + V2BaseSelectInModal) → nền xám nhạt; ghi vào skill
- [x] Thêm 2 cột bắt buộc Người tạo + Ngày tạo (BE: subquery creatorNameSql không đụng COUNT, Resource đổi formatDateTime → formatDate; FE: 2 cột hiện mặc định trước Trạng thái); ghi quy tắc vào skill
- [x] Tăng tốc vào màn: spinner bật ngay, chỉ 1 request chặn trước danh sách, hoãn 5 request options + request cấu hình bộ lọc đến khi mở panel
- [x] Đổi bộ cột mặc định còn 6 cột (8 cột nghiệp vụ chuyển isVisible: false); ghi quy tắc vào skill
- [x] Bỏ await getFields: danh sách bắn ngay lúc vào màn, cấu hình cột chạy song song + nạp lại 1 lần nếu bật cột cần cờ; thêm loadSeq chống response trễ
- [x] CustomerForm (chi tiết/sửa/quản lý KH): gộp loadCustomer + loadAgentEmployees vào cùng lô Promise.all với 7 request danh mục; tách ensureSelectedAgentOption chống race ghi đè NV phụ trách
- [x] Màn chi tiết KH: tiêu đề "Chi tiết khách hàng: <mã>" (form emit `loaded`), footer đủ hành động Sửa · Lịch sử · Quản lý · Khóa/Mở khóa; BE trả thêm `status` ở CustomerDetailResource
- [x] FIX màn chi tiết trắng trơn: `$nuxt.$loading` chưa sẵn sàng khi loadCustomer chạy ngay đầu mounted → đổi 7 chỗ sang `$safeLoadingStart/$safeLoadingFinish`; verify bằng Playwright (footer đủ 5 nút, tiêu đề kèm mã)
- [x] Bỏ nút Lịch sử ở footer màn chi tiết (đã có mục Lịch sử trong form); gỡ luôn modal + state thừa
- [x] FIX nút "Tìm kiếm nâng cao" phải bấm nhiều lần: bỏ hoãn loadConfig + bỏ v-if="configLoaded" trong V2BaseSmartFilterPanel (transition đo chiều cao khi nội dung rỗng)
- [x] Đồng bộ chip select multiple (V2BaseSelect) về khuôn `.csp-chip` xanh dương 11px/bo 5px, bỏ override của size sm; verify Playwright 3 chip khớp nhau
- [x] Chip select: đưa dấu × ra sau chữ (flex row-reverse) + làm mảnh (bỏ khung tròn 16x16, 13px/opacity .6) cho khớp `.csp-chip`
- [x] Port 2 logic từ prospective-projects sang màn KH: (1) `unsavedChangesMixin` ở add.vue + _id/edit.vue (override unsavedSnapshotSource trỏ vào CustomerForm, CustomerForm emit `saved` trước khi điều hướng); (2) `filterStateMixin` ở index.vue (key `assign_customers`, guard `_restoringFilters` chống gọi API 2 lần)
- [x] Verify Playwright: sửa → Quay lại hiện popup, Ở lại giữ dữ liệu, không sửa → thoát thẳng, beforeunload chặn F5; lọc → vào chi tiết → quay lại giữ nguyên lọc; sang màn khác thì xoá lọc
- [x] Màn KH chuyển sang `columnCustomizationMixin`: cột locked (STT, Mã - Tên, Hành động) hiện xám trong popup; thêm `pinnedColumns` ghim cột locked cho popup + bảng cùng thứ tự (Hành động chốt cuối)
- [x] Chạy migration `create_user_column_settings_table` (bảng mới của cấu hình cột, 34 dòng dữ liệu cũ được bê sang) — API detail hết lỗi 400
- [x] Tách cột "Mã - Tên" thành 2 cột: Mã KH (link, class chung `.v2-cell-link`) + Tên khách hàng (chữ thường); bỏ mũi tên ↗ ở V2BaseTitleSubInfo; BE map sort `customerCode`/`customerName`
- [x] Fix `.v2-cell-link` bị `.field-line` đè màu (đổi selector `a.v2-cell-link`); verify Playwright mã ra navy #28539d, không mũi tên
- [x] Bỏ khoá cột Tên khách hàng (cho ẩn/hiện + kéo thả, bỏ sticky); verify popup: chỉ STT · Mã KH · Hành động bị khoá
- [x] BE `applyRelevanceOrder()`: sắp kết quả ô text theo độ khớp (LEAST của 3 nhóm trường, tie-break LOCATE → CHAR_LENGTH → id DESC); bỏ qua khi user đã sort cột / từ khoá < 2 ký tự; đảo ưu tiên khi từ khoá toàn số. Verify tinker + browser
- [x] FIX 2 lỗi xếp độ khớp: (1) thêm bậc "khớp đúng dấu" (COLLATE utf8mb4_0900_as_ci) — HỮU lên trước HƯU; (2) LOCATE=0 khi khác dấu bị coi là gần đầu nhất → quy về 9999
- [x] Redmine #11067 ý 1: popup Tuỳ chỉnh cột theo skill modal-popup (header icon tròn + footer tự viết có icon Lưu/Đóng) + footer sticky, chỉ danh sách cuộn (verify 1920x1080 & 1366x768)
- [x] Redmine #11067 ý 2: popup Lịch sử chọn filter là lọc luôn (deep watcher), bỏ nút Tìm kiếm
- [x] Redmine #11067 ý 3: endpoint `system-logs/{type}/{id}/filter-options` trả đủ 5 loại hành động + NV cùng công ty người tạo, format "MÃ PHÒNG - Tên NV"; FE lọc theo actor_id
- [x] Redmine #11067 ý 4: Excel wrapText cho vùng dữ liệu (cột dài tự xuống dòng, dòng tự giãn)
- [x] FIX popup Tuỳ chỉnh cột có 2 thanh cuộn dọc: tắt overflow ở .modal-body của b-modal (body-class) + bỏ class modal-body ở div trong; verify còn đúng 1 thanh, footer luôn hiện ở 2 viewport
- [x] SỬA LẠI ĐÚNG CHỖ ý 2+3: "Xem chi tiết - Lịch sử" là `SystemInfoSection` (màn chi tiết), không phải CustomerHistoryModal (popup màn danh sách) — lượt trước sửa nhầm component nên user không thấy đổi. Đã áp auto-lọc + options từ API + format mã phòng cho CẢ HAI; BE chỉ trả options cho type=customer, FE fallback logic cũ để 9 màn khác dùng chung SystemInfoSection không đổi hành vi
- [x] Chuẩn hoá màu ô KHOÁ toàn hệ thống: 1 rule chung trong v2-styles.scss (#f1f5f9 / #475569 / #e2e8f0, bỏ opacity), gỡ màu riêng ở V2BaseSelect/DatePicker/CodeInput/CurrencyInput/csp-control + fix selector nặng ký của select multiple; verify 6/6 ô cùng 1 kiểu
- [x] Chip trong ô khoá về XÁM đồng nhất (select2 + csp-chip): nền #e2e8f0 đậm hơn nền ô, chữ #475569, viền #cbd5e1, ẩn nút ×
- [x] Chip "Loại hình : Lĩnh vực" hết chữ xanh khi khoá (phủ cả thẻ con .csp-chip-group); chặn mở dropdown khi readonly ở toggleGroupDropdown/toggleScopeDropdown
- [x] Danh mục bị khoá: BE customerGroups lọc status=1 + include_ids giữ giá trị đang chọn, trả cờ is_locked; FE gắn ICON ổ khoá (bỏ hậu tố "(đã khoá)") qua helper lockedAwareSelectSettings; cập nhật CLAUDE.md
- [x] Rút gọn cách đánh dấu danh mục khoá: emoji 🔒 qua templateResult (bỏ jQuery + CSS icon), chỉ hiện trong danh sách option, chip giữ tên gốc
- [x] Đưa cơ chế đánh dấu danh mục khoá thành DÙNG CHUNG: `utils/select2LockedOption.js` + gọi sẵn trong V2BaseSelect & V2BaseSelectInModal (màn không phải khai gì); gỡ helper riêng ở CustomerForm; ghi quy tắc vào skill list-page mục 11 + CLAUDE.md
- [x] Chống lỗi FE-mới/BE-cũ ở phần Lịch sử: performerKey lùi dần actor_id → actor_code → actor_name, actorText lùi actor_dept_code → actor_code; verify bằng cách giả lập BE cũ (dropdown vẫn có giá trị, lọc vẫn đúng)
- [x] Chuẩn hoá popup xác nhận: sửa base-confirm-modal theo skill (header icon tròn + footer V2BaseButton có icon + prop danger/acceptIcon), thêm plugin `$confirm()` render chính component đó, chuyển unsavedChangesMixin từ $bvModal.msgBoxConfirm sang $confirm; ghi quy tắc vào CLAUDE.md + skill modal-popup mục 3a
- [x] Đa dạng màu button theo phản hồi tester: Import CAM (thao tác ghi) / cả 3 nút Xuất CÙNG xanh lá (cùng bản chất chỉ đọc, phân biệt bằng icon+chữ); dùng prop `status` có sẵn, không sửa component; ghi bảng màu đầy đủ vào skill button-convention mục 2b
- [x] Xuất file Excel quy tắc button `quy-tac-mau-button.xlsx` (4 sheet: màu có swatch thật · icon · text chuẩn · thứ tự nút)
- [x] Đổi quy tắc thời gian: Ngày tạo/Ngày cập nhật hiện NGÀY + GIỜ PHÚT (d/m/Y H:i, bỏ giây), nới cột 140px; bổ sung bảng quy tắc "định dạng thời gian theo cách nhập trên UI" vào skill
- [x] Nút Khóa/Mở khóa đổi màu theo trạng thái (Khóa=cam, Mở khóa=xanh lá), bỏ đỏ; cột hành động bỏ `danger` cho Khóa — đỏ chỉ dành cho Xóa; ghi quy tắc vào skill button-convention
- [ ] User verify bằng mắt `/assign/customers` (bấm tên vào chi tiết, chuột phải Sửa/Quản lý mở tab mới, menu ⋮ không bị bảng cắt khi ở dòng cuối)

### Checkpoint — 2026-08-12

Vừa hoàn thành: toàn bộ code Phase 1, dev server 3002 compile OK (HTTP 200).
Đang làm dở: không.
Bước tiếp theo: user verify UI; sau đó nhân bản quy ước sang các màn danh sách khác.
Blocked:
