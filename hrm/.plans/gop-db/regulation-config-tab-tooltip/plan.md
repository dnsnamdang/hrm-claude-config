# Regulation-config — gộp khối banner xanh vào tooltip ⓘ cạnh tên tab

## Bối cảnh
Màn HRM **Khai báo quy chế – cấu hình** (`/sale|finance|assign/regulation-config`) render chung
`components/regulation-config/RegulationConfigScreen.vue` (+ `data.js`).

Mỗi tab (nhóm quy chế) đang hiển thị:
- Tiêu đề `<h2>{{ curGroup.name }}</h2>` + (tuỳ tab) icon ⓘ `V2BaseFieldHint` giải thích **hẹn ngày
  áp dụng** (`henHint`).
- Phụ đề `<p>{{ curGroup.sub }}</p>`.
- **Khối banner xanh** `.hint` (viền trái xanh `--brand`) nằm DƯỚI phụ đề:
  - Tab **thư viện điều khoản** (Điều khoản báo giá / thanh toán): banner = `curGroup.sub`
    → **trùng y hệt phụ đề** (ảnh user gửi 1 & 2).
  - Tab **hoa hồng (grid)** + **lũy tiến (ladder)**: banner = `curGroup.hint` (HTML).
  - Tab có `deptOnly`: banner cảnh báo "chỉ khai ở cấp Phòng ban".

## Yêu cầu user
Bỏ khối banner xanh lặp phụ đề; **đưa nội dung lên cạnh tên tab dưới dạng tooltip ⓘ giống tab
"Chiết khấu & hỗ trợ bán hàng"** (ảnh 3 = `V2BaseFieldHint`, tooltip tối). Áp cho **tất cả các tab**.

## Quyết định đã chốt
- **Dùng `V2BaseFieldHint`** (đúng pattern ảnh 3 user chỉ, và là component đã dùng sẵn cho tooltip
  tiêu đề trên CHÍNH màn này cho `henHint`). KHÔNG dùng `b-popover info-popover` ở đây vì sẽ lệch
  với tooltip `henHint` ngay cạnh → 2 kiểu tooltip trên cùng 1 tiêu đề. (CLAUDE.md: "đã có ≥1 màn/chỗ
  làm đúng → bám theo".)
- Gộp tất cả nội dung giải thích của tab vào **MỘT** tooltip ⓘ cạnh `<h2>`:
  `titleHint = stripHtml(curGroup.hint)` + cảnh báo `deptOnly` + `henHint`, nối bằng dòng trống.
- **Gỡ 4 khối banner `.hint`** trong vùng tab: dòng 217 (deptOnly), 593 (grid), 717 (ladder),
  825-827 (library/sub).
- **GIỮ NGUYÊN** khối `.hint` ở dòng 1077 — nằm trong **modal hẹn ngày áp dụng** (verGroup), là
  hướng dẫn trong popup, không phải banner cạnh tên tab, không trùng phụ đề.
- Phụ đề `<p>{{ curGroup.sub }}</p>` giữ nguyên → tab thư viện vẫn thấy mô tả (chỉ bỏ banner trùng).
- CSS `.hint` giữ lại (vẫn dùng ở modal dòng 1077).

## Tham chiếu khuôn
- Tooltip tiêu đề: `V2BaseFieldHint.vue` + cách dùng sẵn tại `RegulationConfigScreen.vue:137`.
- Nội dung hint hiện có: `data.js` (`hint` ở dòng 359/371/436), cảnh báo deptOnly ở template 217.

## Tasks
- [x] T1. Thêm computed `titleHint` + method `stripHtml` trong `RegulationConfigScreen.vue`.
- [x] T2. Sửa `<h2>`: `V2BaseFieldHint v-if="titleHint" :text="titleHint"` (thay `henHint`).
- [x] T3. Gỡ 4 khối banner `.hint` (deptOnly, grid, ladder, library). GIỮ banner modal hẹn (verGroup).
- [x] T4. Verify Playwright — PASS:
  - Tab **Điều khoản báo giá / thanh toán** (ảnh 1,2): hết banner xanh trùng phụ đề, phụ đề giữ
    nguyên dưới tên tab, bảng hiện ngay. Không có ⓘ (titleHint rỗng vì library chỉ có `sub`).
  - Tab **Quy chế thưởng (grid)**: ⓘ cạnh tên → tooltip = hint nhóm (bỏ `<b>`) + henHint; banner body = 0.
  - Tab **Thưởng lũy tiến (ladder)**: ⓘ cạnh tên → tooltip = hint nhóm + henHint; banner body = 0.
  - Tab **Quy chế khác (deptOnly)**: ⓘ cạnh tên → tooltip = cảnh báo deptOnly + henHint; banner body = 0.
  - Tab **Chiết khấu & hỗ trợ bán hàng** (ảnh 3): ⓘ + henHint giữ nguyên, không đổi.
  - Hover thật: tooltip tối hiện đủ nội dung, đúng khuôn ảnh 3. Console sạch (không lỗi từ component).
- [ ] T5. Báo user, chờ duyệt commit (CHƯA commit/push khi chưa có yêu cầu).

### Checkpoint — 2026-10-28
Vừa hoàn thành: T1-T4 (code + verify Playwright toàn bộ các loại tab trên /sale/regulation-config).
Đang làm dở: không.
Bước tiếp theo: chờ user duyệt để commit/push nhánh develop (gop_db). CHƯA commit.
Blocked: không.
