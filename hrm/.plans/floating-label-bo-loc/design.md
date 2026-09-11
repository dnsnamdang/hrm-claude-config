# Floating label cho ô lọc — phân hệ Quản lý công việc (assign)

- **Phụ trách:** @dnsnamdang
- **Nhánh:** `tpe` (client `hrm-client`)
- **Spec chi tiết:** `docs/superpowers/specs/2026-08-31-floating-label-filter-assign-design.md`
- **Nguồn yêu cầu:** `FILTER-FLOATING-LABEL-SPEC.md` + `floating-label-demo_1.html` (user cung cấp)

---

## 1. Mục tiêu

Bỏ hàng nhãn riêng phía trên mỗi ô lọc, chuyển sang **floating label kiểu Material outlined**:
nhãn nằm giữa ô khi rỗng, trượt lên **đè lên viền trên** khi ô có dữ liệu hoặc đang focus.
Mục đích: panel lọc mở ra đang chiếm ~450px, đẩy bảng dữ liệu xuống dưới fold.

**Kết quả đo được trên màn pilot (1920px):**

| | Trước | Sau |
|---|---|---|
| Chiều cao panel lọc mở | **449px** | **312px** (−137px, −31%) |
| Số hàng lưới | 5 | 4 |
| Số ô lọc | 17 | 16 (gộp "Ngày tạo từ/đến" thành 1 ô range) |
| Chiều cao ô | 32px | 36px đồng loạt |

---

## 2. Phạm vi

**Đã làm:**
- Component dùng chung `components/V2BaseFloatingField.vue` (3 biến thể: thường / `range` / `tags`).
- Prop `height` cho `V2BaseSelect` + `V2BaseSelectInModal` (mặc định `null`).
- Prop `floating` opt-in cho 3 component tự render nhãn.
- Migrate **1 màn pilot**: `pages/assign/prospective-projects/index.vue`.
- Bộ e2e `e2e/tests/assign/prospective-projects-filter.spec.ts` — **18/18 xanh**.
- Cập nhật `.claude/skills/list-page/SKILL.md`.

**CHƯA làm (mở rộng sau):**
- 76 màn assign còn lại đang dùng `V2BaseFilterPanel`.
- Màn `timesheet/timeworking/shift-history` (màn duy nhất ngoài assign dùng panel này).
- Ô nhập trong form Tạo/Sửa, modal, màn chi tiết — **cố ý không đụng**, chỉ áp cho panel bộ lọc.
- Hàng chip "Đang lọc" (bước 5 của spec gốc) — ngoài phạm vi đã chốt.

---

## 3. Quyết định đã chốt

| Vấn đề | Chốt | Ghi chú |
|---|---|---|
| Phạm vi | Chỉ ô lọc trong panel bộ lọc | Không đụng form/modal/chi tiết |
| Nhánh + panel | `tpe`, `V2BaseFilterPanel` | `V2BaseSmartFilterPanel` chỉ có trên `gop_db` |
| Nhịp rollout | Pilot 1 màn rồi mới nhân bản | **Dừng ở đây, mở rộng sau** |
| Chiều cao ô | **36px** | Dù `size="sm"` của repo là 32px |
| Màu focus | **`#1976d2`, KHÔNG quầng sáng** | Lấy theo ô tìm nhanh ĐANG HIỂN THỊ, xem §4 |
| Placeholder | **Bỏ hẳn placeholder trùng nhãn** | Ngoại lệ có chủ ý so với skill `list-page` |
| Nhãn ô chip | Theo **quy tắc chung**, không float sẵn | Đổi so với thiết kế ban đầu, xem §4 |
| `font-weight` nhãn | Nằm trong ô = **400**, float = 600 | Trong ô nó đóng vai placeholder |
| 3 component tự render nhãn | Prop `floating` **opt-in, mặc định `false`** | 3 màn ngoài assign không đổi |

---

## 4. Ba quyết định đổi so với thiết kế ban đầu

Đều do **đo trên trình duyệt** mới lộ ra, không phải đọc code:

1. **Màu focus: teal `#0a99a7` → `#1976d2`.** Ban đầu chọn teal theo `.sale-theme`. Nhưng yêu cầu
   sau là "giống ô tìm nhanh", mà đo ra ô tìm nhanh hiển thị **`#1976d2`, không quầng** — khác hẳn
   rule `#16a34a` + quầng viết trong chính `V2BaseFilterPanel`, vì bị
   `assets/scss/custom-theme.scss:120` (`.form-control:focus,:hover { border-color:#1976d2
   !important }`) đè mất.

2. **Ô chip bỏ "float vĩnh viễn".** Thiết kế đầu cho `variant="tags"` treo nhãn sẵn trên viền vì
   "ô cao tự động, không còn chỗ đặt nhãn ở giữa". Sai: lúc RỖNG ô vẫn đúng 36px, mà lúc có chip
   thì `has-value` đã bật nên nhãn bay lên trước khi ô kịp cao lên. Treo sẵn làm 3 ô này hiển thị
   lệch hẳn với 13 ô còn lại. Kéo theo: 2 component chip phải tự truyền `has-value` và **giấu
   placeholder riêng** khi chưa float, không thì chữ chồng lên nhãn.

3. **Đệm phải ô chip 30px → 10px.** Component chip đã tự vẽ mũi tên và chừa chỗ; chừa thêm
   `--ff-pad-r` nữa là mất một khoảng trống to bên phải, thu hẹp vùng hiển thị chip.

---

## 5. Bốn cái bẫy kỹ thuật đã trả giá

Ghi lại để 76 màn nhân bản sau không vấp lại. Chi tiết + số đo ở spec.

1. **Select2 gán `z-index: 9999` cho `.select2-container--open`** → khung select vẽ ĐÈ lên nhãn,
   viền cắt ngang chữ khi mở dropdown. Phải cho `.ff` thành stacking context riêng (`z-index: 0`)
   rồi nâng nhãn lên `z-index: 10000`.

2. **Select2 dời focus sang ô tìm nằm trong `<body>`** → `focusout` bắn ngay lúc dropdown bung ra,
   nhãn rơi về giữa ô. Phải bám class `.select2-container--open` bằng `MutationObserver`, KHÔNG
   bám focus. (Không dùng `dropdownParent` trỏ vào wrapper: panel có transition + `overflow:
   hidden` sẽ cắt mất dropdown.)

3. **`updateHeight()` của `V2BaseSelect` ghi inline `!important`** → CSS ngoài không đè nổi, phải
   thêm prop `height`. Nhưng nó chạy trong `setTimeout(100ms)`, nên mỗi lần options nạp async xong
   là ô nháy 32→36px. Phải thêm rule CSS làm **sàn**, đặc hiệu hơn rule 32px gốc.

4. **`.ff__label` là thẻ `<label>`** → ăn rule toàn cục `label { font-weight: 600 }` của
   `custom-theme.scss`, phải đè tay mới ra chữ thường ở trạng thái nghỉ.

---

## 6. Rủi ro còn lại

- **Chưa test zoom 110% / 125%** — `scale(1.1818)` nhân zoom phân số dễ ra lệch nửa pixel trên
  Chrome Windows (môi trường thật của người dùng). Nếu thấy nhãn rung khi transition thì thêm
  `backface-visibility: hidden` vào `.ff__label`, **chỉ thêm khi thật sự thấy vấn đề**.
- **Panel 312px, spec đặt mục tiêu ≤300px** — thừa 12px. Muốn xuống dưới phải cắt ở chỗ khác
  (padding panel); gap 18px đã sát sàn 16px mà spec cho phép.
- **`.claude/skills/list-page/SKILL.md` đã sửa tại chỗ.** Quy tắc team ghi *"`.claude/skills/` là
  tài sản chung — sửa qua PR"* → phần này nên tách PR riêng.
