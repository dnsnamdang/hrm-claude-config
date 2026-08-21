# Plan — Mockup màn Chi tiết Báo giá

> Nhánh `gop_db` · @namdangit · Feature nhỏ (mockup tĩnh).
> Design: `design.md` · Spec: `docs/superpowers/specs/gop-db/2026-08-06-mockup-chi-tiet-bao-gia-design.md`

## Phase 0 — Dựng mockup gốc (bám màn thật)

- [x] Task 0.1 — Chụp + trích dữ liệu màn thật `/assign/quotations/80` (BG-2026-00080)
- [x] Task 0.2 — Tạo feature folder + design.md + plan.md + spec
- [x] Task 0.3 — Dựng `chi-tiet-bao-gia-mockup.html`: shell (topbar + sidebar) kế thừa menu-mockup
- [x] Task 0.4 — Khối Thông tin chung (lưới 2 cột) + badge trạng thái + meta người lập
- [x] Task 0.5 — Khối Chi tiết báo giá: bảng 18 cột, nhóm A, section I, item cha–con, dòng TỔNG
- [x] Task 0.6 — Khối Tổng hợp giá trị báo giá + Giảm giá + Điều khoản
- [x] Task 0.7 — Thanh hành động sticky (Quay lại / Lịch sử / Xuất Excel / In)

## Phase 1 — Chỉnh cho bản mockup chuẩn

- [x] Task 1.1 — Nhúng **menu đầy đủ** (10 nhóm + Yêu thích/Gần đây) từ `menu-mockup.html` thành flyout
      bật ra khi click mục sidebar (flat-mode & nav-mode như bản gốc)
- [x] Task 1.2 — Sửa thanh nút (Quay lại/Lịch sử/Xuất Excel/In) thành **fixed bottom** thật
      (trước đó absolute trong vùng cuộn → trôi theo nội dung)

<!-- Mỗi yêu cầu chỉnh UI tiếp theo của user = 1 task ở đây -->

## Phase 6 — Làm mềm nền + đổi màu header bảng

- [x] Task 6.1 — Sidebar: bỏ line chéo/chữ X (rối) → **3 quầng sáng mềm (aurora)** xanh/teal, tối giản.
- [x] Task 6.4 — Line nền sidebar: v1 (3 đường tay) → xấu; v2 (SVG **bó ~44 đường mảnh lệch pha** = ribbon uốn lượn
      kiểu spirograph, stroke gradient sáng giữa mờ 2 đầu; sinh bằng script python). Giống ảnh minimalistic gradient wave.
      `.side-waves` z-index 0 dưới menu. Script sinh: scratchpad/waves.svg.
- [x] Task 6.2 — Topbar: bỏ vệt chéo → **glow mềm toả sau logo** (trái→phải) + teal nhạt mép phải.
- [x] Task 6.3 — Header bảng: bỏ cyan `#20d9ea` (chói). Đã thử deep teal + chữ trắng → **user chọn phương án B**:
      nền teal rất nhạt `#eefafb→#e2f5f6` + chữ teal đậm `#0a7c88` + viền đáy teal `#0a99a7` (nhẹ, tối giản). Áp cả bảng chi tiết + tổng hợp.

## Phase 5 — Bỏ box brand, line nền, icon màu, màu tiêu đề/header (user đề xuất)

- [x] Task 5.1 — Bỏ box "Bán hàng + tagline" ở sidebar (trùng tên phân hệ đã có ở topbar).
- [x] Task 5.2 — Thêm hiệu ứng **line** vào nền gradient: sidebar (2 vệt sáng chéo giao nhau + line mảnh lặp),
      topbar (vệt sáng chéo phải + line mảnh lặp).
- [x] Task 5.3 — **Icon menu mỗi mục 1 màu** (biến `--ic` inline; hover/active vẫn về sky). Bảng màu curated,
      echo badge nhiều màu ở màn chọn phân hệ. → Khuyến nghị: NÊN, tăng nhận diện + đỡ đơn điệu; có thể revert về mono nếu muốn.
- [x] Task 5.4 — Màu user đề xuất: **tiêu đề card `#0a99a7`** (+ icon chip teal), **header bảng `#20d9ea`** (chữ teal đậm).
      Hài hoà nhóm A / dòng TỔNG / hover row / tổng hợp sang tông teal để đồng bộ với header cyan.

## Phase 4 — Cách điệu hiện đại + thu gọn thông tin + phối màu bảng

- [x] Task 4.1 — Topbar hiện đại: glow góc (radial xanh), viền gradient sáng dưới, logo chip phát sáng,
      tiêu đề có divider trái, icon hover bo tròn, user chip pill + avatar tròn.
- [x] Task 4.2 — Sidebar hiện đại: glow đỉnh, **brand banner premium** (gradient xanh + ánh sáng + icon viền),
      nav item dạng **pill**, active có thanh sáng `#6fb2ff` + glow + nền gradient.
- [x] Task 4.3 — Card Thông tin chung **thu gọn được** (nút chevron): khi thu gọn → dải summary 1 hàng
      (KH · Dự án · Hiệu lực · Bảng giá · **Tổng giá trị** nổi bật) → bảng chi tiết đẩy lên trên. Nén padding info khi mở.
- [x] Task 4.4 — Phối màu: header card (nền gradient nhẹ + icon chip xanh + shadow mềm),
      header bảng (gradient xanh-xám + chữ blue-ink + viền đáy), nhóm A (gradient xanh), hover row xanh nhạt `#eaf3fd`.

## Phase 3 — Tối ưu layout / màu / button vùng nội dung

- [x] Task 3.1 — Card Thông tin chung: divider nhẹ (solid mảnh), bỏ dòng trống thừa,
      mã báo giá dạng `code` xanh mono, "Bảng giá: Bán lẻ" → chip info xanh (bỏ màu đỏ nhầm nghĩa lỗi).
- [x] Task 3.2 — Dòng Giảm giá / Điều khoản: gọn thành `.fline` (nhãn muted + chip trung tính "Không có" / "—").
- [x] Task 3.3 — Bảng chi tiết: nhấn cột **Giá bán** & **Thành tiền sau VAT** (đậm/đậm màu),
      dòng **TỔNG** đổi hổ phách → xanh navy nhạt; tổng hợp: dòng V thêm viền trên xanh.
- [x] Task 3.4 — Hệ thống button: `primary` (gradient xanh + shadow, dùng cho In), `outline` (Lịch sử/Xuất Excel),
      `ghost` (Quay lại); hover xanh nhạt nhất quán.

## Phase 2 — Đồng nhất màu theo NỀN màn chọn phân hệ (navy)

> Quyết định: KHÔNG dùng màu nhóm (tím KINH DOANH). Dùng **màu nhận diện NỀN màn chọn phân hệ**:
> navy gradient `#1e57a0→#14417e→#0e2f5f→#0a1c3d` + màu chủ đạo phần mềm `#2E71C3` (sáng `#4C90D9`, glow `#6fb2ff`),
> chữ trên navy `#eaf1fb`/`#b6c8e2`. Nguồn: `layouts/system.vue` + `components/subsystems.js`.

- [x] Task 2.1 — Token màu navy/brand; đổi accent teal → xanh `#2E71C3`. Áp cho: card header icon, link,
      nút In, dòng nhóm/section bảng, dòng tổng, flyout (marker/scat active/tint), sao Yêu thích → vàng `#f2b93b`.
- [x] Task 2.2 — **Topbar navy** (gradient `#0e2f5f→#123c74`), logo chip gradient xanh + icon túi, chữ sáng,
      icon/avatar theo tông; badge "Đang tạo" giữ hổ phách.
- [x] Task 2.3 — **Sidebar navy** (gradient dọc `#123c74→#0a1c3d`), banner nhận diện "Bán hàng · Đơn hàng & báo giá"
      (icon túi trên chip gradient xanh), search kính mờ, item active nền kính + viền trái `#6fb2ff` + chữ trắng.

---

### Checkpoint — 2026-08-06 (Phase 6 — chốt phiên)
Vừa hoàn thành:
- Nền topbar: glow mềm sau logo (bỏ vệt chéo).
- Nền sidebar: bỏ line chéo/chữ X rối → aurora mềm + **bó ~44 đường sóng uốn lượn (ribbon spirograph)** sinh bằng script,
  stroke gradient sáng giữa mờ 2 đầu (giống ảnh minimalistic gradient wave user gửi). Lớp `.side-waves` z-index 0 dưới menu.
- Header bảng: bỏ cyan chói → **phương án B**: nền teal rất nhạt `#eefafb→#e2f5f6` + chữ teal `#0a7c88` + viền đáy teal `#0a99a7`.
- Tiêu đề card teal `#0a99a7` + icon chip teal; icon menu mỗi mục 1 màu; bảng/nhóm/tổng đồng bộ gam teal.
Đang làm dở: —
Bước tiếp theo (khi quay lại): tinh chỉnh bó sóng nếu cần (đậm/nhạt, vị trí thắt, áp motif cho topbar);
hoặc sang hạng mục khác: badge trạng thái từng dòng hàng, micro-animation hover/thu gọn, bản responsive.
Blocked:

> Mockup chạy tại: `http://127.0.0.1:8899/chi-tiet-bao-gia-mockup.html` (server python tạm) hoặc mở thẳng file.
> Toàn bộ là mockup tĩnh — CHƯA áp vào code thật (`hrm-client/pages/assign/quotations/`).

### Checkpoint — 2026-08-06 (Phase 5)
Vừa hoàn thành: Bỏ box brand sidebar; thêm hiệu ứng line nền topbar+sidebar; icon menu mỗi mục 1 màu (--ic);
áp màu user đề xuất (tiêu đề #0a99a7, header bảng #20d9ea) + hài hoà bảng sang teal. Render verify OK.
Đang làm dở: —
Bước tiếp theo: Chờ user duyệt tông teal/cyan + icon nhiều màu (giữ hay tiết chế).
Blocked:

### Checkpoint — 2026-08-06 (Phase 4)
Vừa hoàn thành: Topbar + sidebar cách điệu hiện đại (glow, brand banner premium, active pill phát sáng);
card Thông tin chung thu gọn được (chevron → summary 1 hàng, đẩy bảng lên); phối màu header card/bảng + hover row.
Render verify OK: mở rộng + thu gọn + flyout. JS toggle `#btnCollapse`.
Đang làm dở: —
Bước tiếp theo: Chờ user duyệt → tinh chỉnh tiếp (vd: trạng thái item, responsive, animation micro-interaction).
Blocked:

### Checkpoint — 2026-08-06 (Phase 3)
Vừa hoàn thành: Tối ưu vùng nội dung — card Thông tin chung gọn (code/chip xanh, bỏ đỏ), dòng giảm giá/điều khoản dạng chip,
bảng nhấn cột tiền + dòng TỔNG xanh, hệ thống button primary/outline/ghost. Render verify OK (màn chính + tổng hợp + button).
Đang làm dở: —
Bước tiếp theo: Chờ user duyệt → yêu cầu tinh chỉnh tiếp (vd: header card, trạng thái item, mật độ bảng, responsive…).
Blocked:
