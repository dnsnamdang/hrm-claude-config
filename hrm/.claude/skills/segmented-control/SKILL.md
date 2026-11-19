---
name: segmented-control
description: Use when cần cho user chọn 1 trong 2–4 lựa chọn ngắn (Phân loại họp, Hình thức, điểm danh, Có/Không, tab con trong 1 khối) ở hrm-client — dùng V2BaseSegmented (nút gạt kiểu iOS), cùng bộ chuyển động với thanh tab V2BaseTabNavigation; và khi sửa/đọc thanh tab chính.
---

# Skill: Nút gạt (segmented control) + Thanh tab kiểu iOS

Chốt 15/10/2026 — `.plans/gop-db/meeting-form-redesign/design.md` (D7) · spec
`docs/superpowers/specs/gop-db/2026-10-15-meeting-form-redesign-design.md` mục 2.1–2.2.

## 1. Khi nào dùng `V2BaseSegmented`

| Tình huống | Dùng |
| --- | --- |
| Chọn 1 trong **2–4** lựa chọn **ngắn** (≤ 3 từ), luôn thấy hết lựa chọn | `V2BaseSegmented` |
| Nhiều lựa chọn / chữ dài / lấy từ danh mục | `V2BaseSelect` (`V2BaseSelectInModal` trong popup) |
| Chọn nhiều | checkbox / select multiple — KHÔNG dùng nút gạt |
| Chuyển các TAB lớn của màn | `V2BaseTabNavigation` (mục 4) |
| Thanh tab / nút công cụ NHỎ trong 1 khối hoặc đầu khung (vd Nhiệm vụ · Meeting · Vấn đề · File ở đầu Nhóm trao đổi) — mỗi mục icon màu + chữ + số đếm, có thể không mục nào chọn | `V2BaseMiniTab` — mẫu **MINITAB** (mục 4b) |

## 2. Cách dùng

```vue
<V2BaseSegmented
    v-model="form.mode_id"
    :options="[
        { value: 1, label: 'Trực tiếp', icon: 'ri-map-pin-user-line' },
        { value: 2, label: 'Online', icon: 'ri-vidicon-line' },
    ]"
/>

<!-- Trong bảng: size sm (24px); mỗi lựa chọn có màu riêng khi được chọn -->
<V2BaseSegmented
    v-model="m.attendance_status"
    size="sm"
    :options="[
        { value: 1, label: 'Có mặt', icon: 'ri-checkbox-circle-line', color: '#16A34A' },
        { value: 2, label: 'Vắng có lý do', icon: 'ri-time-line', color: '#D97706' },
        { value: 3, label: 'Vắng không lý do', icon: 'ri-close-circle-line', color: '#DC2626' },
    ]"
/>
```

| Prop | Ý nghĩa |
| --- | --- |
| `value` / `v-model` | giá trị đang chọn; `null` → không hiện viên chọn (vd chưa điểm danh). So sánh theo chuỗi (`'1'` = `1`) |
| `options` | `[{ value, label, icon?, color? }]` — `color` lấy trong 9 mã màu chuẩn (CLAUDE.md, badge) |
| `size` | `md` = 34px, cao bằng `V2BaseInput` (đặt cạnh ô nhập) · `sm` = 24px (trong bảng) |
| `block` | rộng 100% khung, các lựa chọn chia đều |
| `disabled` | chỉ đọc (màn Chi tiết) — không hover, không đổi |

Emit `input` + `change`. Bàn phím ←/→ đổi lựa chọn (`role="radiogroup"`).

## 3. Thông số (đừng ghi đè ở từng màn)

- Rãnh `rgba(118,118,128,.12)` bo 9px padding 2px; viên chọn trắng, bóng `0 1px 3px rgba(0,0,0,.08)`.
- Chữ thường 500 `#1c1c1e`; chọn 600 `#000`; icon chọn `#059669` (hoặc `color` của option).
- Hover: viên `rgba(255,255,255,.55)` **nở 2px mỗi bên bằng width thật** — TUYỆT ĐỐI không `transform: scale`
  lên chữ (chữ nhoè — user đã bắt lỗi 15/10/2026).
- Đổi lựa chọn: viên giãn phủ đường đi 160ms rồi co về kiểu lò xo `cubic-bezier(.34,1.36,.64,1)`.

## 4. Thanh tab chính `V2BaseTabNavigation` (cùng ngôn ngữ thiết kế)

- Viên thuốc kính mờ: nền `rgba(242,242,247,.78)` + `backdrop-filter: blur(22px) saturate(180%)`, tab 32px, khe 4px.
- Tab chọn: viên `rgba(5,150,105,.12)`, chữ/icon `#059669` đậm 700. Hover: viên TRẮNG sáng nở 2px.
- API không đổi: `tabs` (`{ key, label, icon, count?, hasError? }`), `active-tab`, `@tab-change`; thêm prop `sticky`.
- `count` → số đếm cạnh nhãn; `hasError` → chữ đỏ + icon cảnh báo, viên chọn nhuộm đỏ khi đang mở tab lỗi.
- Nhiều tab tràn ngang: tự cuộn, mũi tên ‹ ›, mờ mép — viên chọn nằm trong vùng cuộn nên tự đi theo.

## 4b. Thanh tab nhỏ `V2BaseMiniTab` (mẫu MINITAB — chốt 10/11/2026, code 11/11/2026)

Spec gốc Phân hệ Công việc §5.1 (MINITAB) · spec GĐ2 §6.1. Dùng đầu tiên ở `pages/assign/workspaces/_id/index.vue`.

```vue
<V2BaseMiniTab
    :tabs="[{ key: 'tasks', label: 'Nhiệm vụ', icon: 'ri-task-line', color: '#2563EB', count: 22 }]"
    :active-tab="panel === 'tasks' ? 'tasks' : null"
    @tab-change="(key) => (panel = key)"
/>
```

- API như `V2BaseTabNavigation`: `tabs` `[{ key, label, icon?, color?, count?, title?, testid? }]`, `active-tab`
  (**null = không mục nào chọn**, viên chọn ẩn), `@tab-change(key)`. `count` null/undefined = không hiện số.
  `testid` mặc định `mtab-<key>`.
- `color` lấy trong **9 mã màu chuẩn** — component có sẵn bộ rgba / `mix()` SCSS cho cả 9 mã (KHÔNG dùng `color-mix()`);
  mã khác vẫn tô icon/số nhưng bóng viên chọn xám.
- Giao diện: rãnh kính trắng mờ bo 12px (padding 3px, viền hairline, `backdrop-filter`), mục cao 32px ⇒ cả cụm 40px;
  icon trong ô tròn 24px nền nhạt cùng màu; mục chọn = viên trắng bóng + bóng màu loại, icon thành ô tròn đặc màu.
- Chuyển động = đúng thông số mục 3: viên chọn + viên hover là 2 lớp nền dưới nút; giãn 160ms `ease-out` → lò xo
  400ms; hover nở 2px bằng width thật; từ không chọn ⇒ viên hiện tại chỗ, bung từ giữa ra; `prefers-reduced-motion`.
- Đặt viên bằng `getBoundingClientRect` (số lẻ), không `offsetLeft/offsetWidth` (làm tròn ⇒ lệch ~0.5px).
- ⚠️ Màu viên chọn gắn bằng `data-c`, KHÔNG `:class` — Vue vá lại cả thuộc tính `class` khi render ⇒ xoá mất lớp
  chuyển động `is-stretch` / `is-grow` / `is-pop` gắn tay. `sync()` bỏ qua lúc đang giãn (ResizeObserver bắn khi chữ
  mục mới đậm lên làm rãnh đổi rộng ⇒ cắt mất pha giãn).
- KHÁC `V2BaseSegmented`: Segmented là ô CHỌN GIÁ TRỊ (`v-model`, luôn có 1 giá trị); MiniTab là ĐIỀU HƯỚNG (mở mục).

## 5. Tự kiểm (Playwright, đo DOM)

- Viên chọn trùng mục đang chọn: `|thumb.left − active.left| < 2.5` và `|thumb.width − active.width| < 2.5` (rời chuột trước khi đo).
- `size="md"` đặt cạnh ô nhập: chiều cao bằng nhau (34px).
- Hover: nền nở đúng 2px mỗi bên, `transform` của chữ = `none`.
- MiniTab: `|thumb.left − active.left| < 0.5` và `|thumb.width − active.width| < 0.5` sau khi đứng yên (≥ 600ms);
  `active-tab` null ⇒ `opacity` viên chọn = 0.
