# Đề xuất PR — cập nhật CLAUDE.md + skill sau đợt đồng bộ form xuất nhập

> ĐÃ ÁP DỤNG 2026-10-10 theo yêu cầu user (sửa thẳng CLAUDE.md L51 + skill `erp-to-hrm-screen`
> checklist "Bố cục"). File này giữ lại làm bản ghi nội dung.

## 1. `HRM/CLAUDE.md` — mục "Nguyên tắc chung"

Dòng hiện tại (L51):

> **Khối NHÓM trong màn form/chi tiết dùng `components/V2BaseFormSection.vue`** (card + tiêu đề + slot
> `#actions` …) — KHÔNG tự dựng `<div class="card"><div class="card-header">…` cho từng màn. …

Thêm ngay sau câu "Khuôn gốc: mục "Địa chỉ giao hàng" màn `/assign/customers/{id}`.":

> **Ngoại lệ — nhóm kho / xuất nhập** (8 luồng YCXH, ĐNXK, PXH, YCNH, ĐNNK, PNK, PXBHM, YCXBHM + PXG)
> dùng `components/V2BaseFormCard.vue` (khuôn chi tiết PXG-02188): tiêu đề IN HOA xám không icon,
> slot `#meta` = `CreatorInfoLine` (mã + người lập), thân là lưới `col-md-4` `V2BaseLabel` +
> `V2BaseInput disabled size="sm"`, ô áp dụng mà rỗng hiện ô xám rỗng (không `—`), trạng thái là
> `V2BaseBadge :color="status_color"` do BE trả. Màn mới trong nhóm này bám `V2BaseFormCard`,
> KHÔNG dùng `V2BaseFormSection` / `.form-card` / `kv-grid`.

## 2. Skill `erp-to-hrm-screen` — checklist L455–457

Dòng hiện tại:

> - [ ] Bố cục: … khối form bám khuôn của màn cùng nhóm (`.form-card` hay `V2BaseFormSection`) — đo
>       `getBoundingClientRect` cạnh màn mẫu (#11356, #11540)

Đề xuất sửa thành:

> - [ ] Bố cục: … khối form bám khuôn của màn cùng nhóm — nhóm kho / xuất nhập dùng **`V2BaseFormCard`**
>       (khuôn PXG-02188, xem đoạn mẫu K1 dưới), nhóm khác `V2BaseFormSection` — đo `getBoundingClientRect`
>       cạnh màn mẫu (#11356, #11540). Màn nhóm kho tự kiểm bằng grep, phải RỖNG (trừ ruột bảng):
>       `grep -nE "ri-[a-z0-9-]+(-line|-fill)?\"></i>|kv-grid|c-section|section-header|card-header|subpanel|status-pill|text-muted|'—'|>—<"`

Đoạn mẫu K1 (đưa vào skill ngay dưới checklist):

```vue
<V2BaseFormCard>
    <template #title>{{ data.type_name || 'Phiếu nhập hàng' }}</template>
    <template #meta>
        <CreatorInfoLine :name="data.creator_name" :created-at="data.created_at" />
    </template>
    <div class="form-row">
        <div class="col-md-4 mb-2">
            <V2BaseLabel>Trạng thái</V2BaseLabel>
            <div><V2BaseBadge :color="data.status_color">{{ data.status_text }}</V2BaseBadge></div>
        </div>
        <div class="col-md-4 mb-2">
            <V2BaseLabel>Kho nhập</V2BaseLabel>
            <V2BaseInput :value="data.warehouse_name || ''" disabled size="sm" />
        </div>
        <div class="col-12 mb-2">
            <V2BaseLabel>Ghi chú</V2BaseLabel>
            <V2BaseTextarea :value="data.note || ''" :rows="2" disabled />
        </div>
    </div>
</V2BaseFormCard>

<!-- Bảng: card bọc bảng, không đệm thân -->
<V2BaseFormCard title="Chi tiết" no-body-padding>
    <V2BaseTableScroll>…</V2BaseTableScroll>
</V2BaseFormCard>
```

Số đo chuẩn (PXG-02188, viewport 1440): head cao 37px, chữ tiêu đề 12px/700 `#374151` IN HOA
letter-spacing 0.24px, nền head `#f9fafb`, padding head `8px 14px`, thân `14px`, viền `1px #e5e7eb`,
bo 8px, cách card dưới 24px, ô nhập cao 32px, nhãn 12px/600 `#0f172a`.
