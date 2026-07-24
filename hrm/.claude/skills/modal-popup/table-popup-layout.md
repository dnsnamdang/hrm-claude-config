# Popup chứa bảng dữ liệu — công thức đầy đủ

Tham chiếu chi tiết cho mục 5 của `SKILL.md`. File mẫu đang chạy production:
`pages/assign/quotations/components/QuotationProductSearchModal.vue`
(dùng chung `/assign/bom-list/add|edit` + `/assign/quotations/_id/edit`).

---

## 1. Công thức bố cục (copy-paste)

Popup cao **cố định**, mọi khối phụ `flex-shrink: 0`, **CHỈ** khung bảng `flex: 1`.
Mỗi px tiết kiệm ở khối phụ rơi thẳng vào bảng.

```vue
<div v-if="show" class="modal-backdrop-lite">
    <div class="modal-card" style="width: 98vw">
        <div class="modal-head">...</div>
        <div class="modal-body">
            <b-tabs v-model="activeTab" content-class="mt-2" no-key-nav
                    :nav-class="onlyOneTab ? 'd-none' : ''">
                <b-tab title="Hàng hoá">
                    <!-- control lẻ: nhãn NGANG control -->
                    <div class="group-picker-row mb-1">...</div>

                    <V2BaseFilterPanel inlineSearchButtons ...>
                        <template #header-actions>
                            <V2BaseButton primary size="sm" class="btn-compact">Thêm hàng tạm</V2BaseButton>
                        </template>
                        <template #advanced-filters="{ collapsed }">
                            <!-- 1 grid PHẲNG, KHÔNG chia hàng cứng -->
                            <div v-show="!collapsed" class="filter-grid mt-2">
                                <div class="filter-item">...</div>
                                <!-- ...N ô... -->
                            </div>
                        </template>
                    </V2BaseFilterPanel>

                    <div ref="erpTableWrap" class="erp-table-wrap">
                        <table class="table table-bordered table-hover table-sm mb-0 erp-product-table">...</table>
                    </div>

                    <V2BasePagination v-if="!loading" ... />
                </b-tab>
            </b-tabs>
        </div>
        <div class="modal-footer-fixed">...</div>
    </div>
</div>
```

```css
/* ===== 1. Khung: CAO CỐ ĐỊNH ===== */
.modal-backdrop-lite {
    position: fixed;
    inset: 0;
    z-index: 5000;
    background: rgba(0, 0, 0, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 6px;
}
.modal-card {
    background: #fff;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    height: 98vh;      /* BẮT BUỘC có `height`, không chỉ max-height */
    max-height: 98vh;
}
.modal-head,
.modal-footer-fixed {
    flex-shrink: 0;
    padding: 6px 14px;
}

/* ===== 2. Chuỗi flex KHÔNG ĐỨT (b-tabs chèn 3 lớp vào giữa) ===== */
.modal-body {
    padding: 6px 10px;
    flex: 1 1 auto;
    min-height: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;   /* KHÔNG dùng overflow-y:auto — xem "Bẫy" #1 */
}
.modal-body ::v-deep .tabs,
.modal-body ::v-deep .tab-content {
    display: flex;
    flex-direction: column;
    flex: 1 1 auto;
    min-height: 0;
}
.modal-body ::v-deep .tab-content .tab-pane.active {
    display: flex !important;
    flex-direction: column;
    flex: 1 1 auto;
    min-height: 0;
}

/* ===== 3. Bảng: khối DUY NHẤT co giãn ===== */
.erp-table-wrap {
    flex: 1 1 auto;
    min-height: 160px;
    overflow: auto;             /* KHÔNG đặt max-height cứng */
    border: 1px solid #e5e7eb;
    border-radius: 8px;
}

/* ===== 4. Chiều cao DÒNG (mẫu số) ===== */
.erp-product-table td,
.erp-product-table th {
    padding: 3px 6px;
    font-size: 12px;
    vertical-align: middle;
}
.erp-product-table thead th {
    position: sticky;
    top: 0;
    z-index: 2;
    background: #f8fafc;
    white-space: nowrap;
}
/* Cột chữ dài: cắt 2 dòng + tooltip title. KHÔNG clamp = 1 ô mô tả dài 5 dòng
   nuốt chỗ của 3 dòng khác. */
.cell-clamp {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1.35;
    word-break: break-word;
}
/* Ảnh quyết định SÀN chiều cao dòng */
.erp-thumb {
    width: 26px;
    height: 26px;
    object-fit: cover;
    border-radius: 5px;
    vertical-align: middle;
}
/* Cột ngắn: thà scroll ngang còn hơn bóp co làm cao dòng */
.erp-product-table .col-compact {
    min-width: 90px;
    white-space: nowrap;
}

/* ===== 5. Lưới lọc tự lấp đầy ===== */
.filter-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 4px 8px;
}
.filter-item {
    min-width: 0;
}

/* ===== 6. Control lẻ: nhãn ngang (32px thay vì 56px) ===== */
.group-picker-row {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
}
.group-picker-row ::v-deep label {
    margin-bottom: 0;
    font-size: 12px;
    white-space: nowrap;
}
.group-picker-control {
    width: 260px;
    flex: 0 0 auto;
}

/* ===== 7. Nén component dùng chung (chỉ trong popup này) ===== */
::v-deep .tp-card {
    padding: 6px 8px !important;
    margin-bottom: 4px !important;
    box-shadow: none !important;
}
::v-deep .tp-card > .d-flex.mb-2 {
    margin-bottom: 4px !important;
    align-items: center !important;
}
::v-deep .tp-card > .mb-2 {
    margin-bottom: 0 !important;
}
::v-deep .tp-section-title {
    font-size: 12px;
}
::v-deep .nav-tabs .nav-link {
    padding: 4px 12px;
}
::v-deep .tab-content {
    padding: 2px 0;
}
/* V2BasePagination = .row.paging.mt-3 → mt-3 tốn 24px */
::v-deep .row.paging {
    margin-top: 4px !important;
    padding: 0 !important;
}
::v-deep .row.paging .page-total {
    padding: 0 8px !important;
    font-size: 12px;
}
::v-deep .row.paging .pagination {
    margin-bottom: 0 !important;
}
::v-deep .row.paging .pagination-page-size-select {
    height: 28px;
    padding-top: 0;
    padding-bottom: 0;
}
::v-deep .row.paging .page-link {
    padding: 2px 8px;
}
```

---

## 2. Bẫy đã trả giá (đo thật, không suy đoán)

### Bẫy 1 — `overflow-y: auto` ở `.modal-body` = thủ phạm "chỉ thấy 2 dòng"

Body cuộn dọc → mở bộ lọc nâng cao **đẩy bảng trôi khỏi tầm nhìn**, bảng vẫn cao như cũ nhưng user không thấy.
→ `.modal-body { overflow: hidden }`, chỉ `.erp-table-wrap` được cuộn dọc.

### Bẫy 2 — Thiếu `min-height: 0` → `flex: 1` vô hiệu

Flex item mặc định `min-height: auto` = không co dưới kích thước nội dung.
Thiếu ở **bất kỳ mắt xích nào** (`.modal-body`, `.tabs`, `.tab-content`, `.tab-pane.active`) là bảng tràn/không giãn.
Đây là dòng CSS dễ bị xoá nhất khi review vì trông như thừa.

### Bẫy 3 — `max-height` cứng cho bảng

`max-height: 400px` = bảng không bao giờ lớn dù màn còn 600px trống. Dùng `flex: 1 1 auto` + `min-height`.

### Bẫy 4 — `height` vs `max-height` ở card

`max-height: 98vh` đơn độc → card co theo nội dung → không có phần dư để bảng giãn. **Phải** có `height: 98vh`.

### Bẫy 5 — select2 multiple: ép full width đè lên chip

**Triệu chứng**: chọn xong 1 giá trị, ô search nằm **đè lên chip**, UI vỡ khi gõ tìm.
**Căn nguyên**: select2 khởi tạo lúc panel `v-show=false` → `resizeSearch()` đọc width `ul` = 0 → ô search width ~0 → mất placeholder. Hack cũ ép `width:100%; float:none` **mọi lúc** → khi có chip, ô search thành block full-width đè lên chip đang float.
**Cách đúng**: giới hạn hack vào đúng trạng thái rỗng bằng `:only-child` (rỗng → ô search là con DUY NHẤT của `ul`; có chip → `ul` có thêm `__clear` + `__choice` nên rule tự tắt, trả về float mặc định).

```css
.filter-item ::v-deep .select2-selection--multiple {
    min-height: 32px;
    padding-bottom: 2px;
}
.filter-item ::v-deep .select2-selection__rendered > .select2-search--inline:only-child {
    width: 100%;
    float: none;
}
.filter-item ::v-deep .select2-selection__rendered > .select2-search--inline:only-child .select2-search__field {
    width: 100% !important;
    min-width: 120px;
}
```

### Bẫy 6 — Đừng "sửa" z-index select2 trong popup overlay tự dựng

`V2BaseSelectInModal.mounted()` chỉ set `dropdownParent` khi tìm thấy `.modal-content`. Popup overlay tự dựng **không có** `.modal-content` → dropdownParent = null → select2 append vào `<body>`.

**Nhìn code dễ kết luận nhầm là dropdown bị backdrop (z-index 5000) che.** Thực tế **KHÔNG lỗi**: chính `V2BaseSelectInModal.vue` đã set `z-index: 9999 !important` cho container/dropdown → luôn nổi trên backdrop. Đã đo live: `containerZIndex = 9999`, `elementFromPoint` giữa dropdown chạm đúng `.select2-results__option`.
→ **Không cần** thêm class `modal-content` giả, không cần vá z-index.

### Bẫy 7 — Đừng đặt `overflow: auto` lên `.filter-grid`

Vì dropdown append vào `<body>` (Bẫy 6), nó **không** bị grid cắt — nhưng vị trí dropdown được tính 1 lần lúc mở, cuộn grid sẽ làm dropdown lệch khỏi ô. Với `auto-fit`, N ô lọc hiếm khi vượt 2-3 hàng nên **không cần** trần chiều cao. Chỉ cân nhắc nếu đo thật thấy lưới > 3 hàng.

---

## 3. Ngân sách chiều cao (@1920×1080, đo thật)

| Khối | Cao |
|---|---|
| modal-head | ~34px |
| Nhãn ngang (Nhóm hàng) | ~32px |
| Filter panel — thu gọn | ~86px |
| Filter panel — mở nâng cao (18 ô, 9 ô/hàng, 2 hàng) | ~193px |
| Phân trang | ~34px |
| modal-footer-fixed | ~40px |
| **Bảng (phần còn lại)** | **~640-830px** |
| Chiều cao 1 dòng (thumb 26px + padding 3px + clamp 2 dòng) | **~39-40px** |

**Kết quả thật:** nâng cao ĐÓNG **20 dòng**, MỞ **15-17 dòng** (trước khi tối ưu: **2 dòng**).

Số dòng = **chiều cao bảng ÷ chiều cao dòng**. Phải tối ưu **cả tử số và mẫu số** —
chỉ nới popup mà để dòng cao 64-81px thì vẫn ít dòng.

---

## 4. Snippet đo bằng Playwright

```js
// browser_evaluate — đếm số dòng THẤY ĐỦ + soi chỗ lãng phí
() => {
  const card = document.querySelector('.modal-card');
  const wrap = card.querySelector('.erp-table-wrap');
  const body = card.querySelector('.modal-body');
  const rows = Array.from(card.querySelectorAll('.erp-product-table tbody tr'));
  const headH = card.querySelector('.erp-product-table thead').getBoundingClientRect().height;
  const wrapH = wrap.getBoundingClientRect().height;
  let acc = headH, visible = 0;
  for (const r of rows) {
    const h = r.getBoundingClientRect().height;
    if (acc + h <= wrapH) { acc += h; visible++; } else break;
  }
  return {
    visibleRows: visible,
    rowHeights: rows.slice(0, 5).map(r => Math.round(r.getBoundingClientRect().height)),
    tableShareOfPopup: (wrapH / card.getBoundingClientRect().height * 100).toFixed(0) + '%',
    bodyMustNotScroll: body.scrollHeight <= body.clientHeight + 1,  // Bẫy 1+2
    noHorizontalOverflow: document.body.scrollWidth <= window.innerWidth,
  };
}
```
