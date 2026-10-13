# Design — Base dùng chung cho popup báo cáo

- **Người phụ trách**: @dnsnamdang · **Ngày**: 2026-09-17
- **Nhánh**: `gop_db` (client `hrm-client`)
- **Mẫu nguồn (user chốt)**: `pages/assign/report/potential-customer-care/components/DemandListModal.vue`
- **Phương án đã chốt**: tách 2 lớp — component vỏ + mixin máy (phương án C)

## Mục tiêu

Popup drill-down của các màn báo cáo đang mỗi cái một kiểu. Dựng một khuôn dùng chung lấy popup
"Danh sách nhu cầu" của báo cáo CSKH tiềm năng làm mẫu, để popup báo cáo nào cũng có cùng dải
header, cùng cách bấm sắp xếp, cùng chỗ đặt phân trang và hàng nút.

## Hiện trạng (đo 2026-09-17)

`pages/assign/report/` có 21 popup. Chia 3 nhóm:

| Nhóm | Số lượng | Đặc điểm |
|---|---|---|
| Drill-down lớn | 3 | có bảng + bộ lọc + phân trang: `DemandListModal` (1307 dòng), `DevelopmentDrillModal` (1204), `ProjectListModal` (888) |
| Popup bảng nhỏ | 15 | có bảng, không phân trang, 182–528 dòng |
| `PrintOptionsModal` | 3 | không bảng — **ngoài phạm vi** |

`DevelopmentDrillModal` và `ProjectListModal` **đã dựng trên `components/modal/V2BaseModal.vue`**;
riêng mẫu nguồn thì không — nó viết trên nhánh `bao_cao_cskh_tiem_nang` lúc `V2BaseModal` chưa tồn
tại (comment ngay trong file ghi rõ điều đó). Đây chính là chỗ "không theo chuẩn chung" mà user
nhắc, và cũng là nguyên nhân gián tiếp của lỗi stacking context đã sửa 2026-09-17.

### ⚠️ 3 popup dùng 3 chiến lược dữ liệu KHÁC NHAU

Đây là dữ kiện quan trọng nhất của thiết kế — Base ôm nhầm phần này là hỏng cả 3:

| Popup | Lọc | Sắp xếp | Phân trang | Nguồn dữ liệu |
|---|---|---|---|---|
| `DemandListModal` | **server** (`$emit('filter')`, màn cha tải lại) | client | client | cha truyền `rows` |
| `DevelopmentDrillModal` | **client** (`filteredRows`) | client | client | cha truyền `rows` |
| `ProjectListModal` | **server** | server | server | **popup tự gọi `fetchList()`** |

Thứ **giống hệt nhau ở cả 3** chỉ có: bố cục màn hình, schema cột, cách bấm sắp xếp, luật "đổi tập
là về trang 1", và hàng nút In / Xuất Excel / Đóng. Base chỉ được ôm đúng những thứ đó.

## Kiến trúc

### 1. `components/report/V2BaseReportModal.vue` — VỎ (~350 dòng)

Dựng **trên `V2BaseModal`**, KHÔNG fork `b-modal` lần nữa.

Tự lo:

- **Dải header banner** (giữ đúng mẫu nguồn, user chốt): `lead` ("Bạn đang xem kết quả …:") +
  `title` (tên đối tượng, nổi) + dòng `meta` (số bản ghi · tiền · kỳ · "đang lọc trong N").
- **Nút phóng to / thu nhỏ toàn màn hình** + nút ×.
- **Bảng dựng theo schema `columns`**, bọc trong `components/V2BaseTableScroll.vue` — bỏ hẳn phần
  tự chế 2 thanh cuộn đồng bộ (~60 dòng JS) của mẫu nguồn.
- **Header cột bấm để sắp xếp** (mũi tên 3 trạng thái) — phát `sort` ra ngoài, không tự sắp.
- **Dòng rỗng** ("Đang tải…" / "Không có … khớp bộ lọc") với `colspan` đúng số cột.
- **`V2BasePagination`** đặt ngoài vùng cuộn bảng, chỉ render khi có `total-rows`. Vỏ nhận
  `current-page` / `current-page-size` / `total-rows` qua **prop** và phát `page-change` /
  `page-size-change` ra ngoài — nhờ vậy dùng được cho cả popup phân trang client-side (giá trị
  đến từ mixin) lẫn popup phân trang ở BE (giá trị đến từ response).

Slot cho màn: `filters`, `summary`, `back`, `footer`, và **scoped slot `cell-<key>`** cho ô đặc
biệt (link Meeting, Khách hàng + icon lịch sử, Dự án TKT, badge Trạng thái…).

**Không** biết gì về: nghiệp vụ, cách lấy dữ liệu, cách lọc.

#### Thay đổi kèm theo ở `V2BaseModal.vue`

Thêm **slot `header`** (additive): không truyền thì render header chuẩn y như cũ → 30 popup đang
dùng không đổi một pixel nào.

### 2. `utils/mixins/reportDrillListMixin.js` — MÁY (~180 dòng)

Chỉ ôm phần **3 popup giống hệt nhau**:

- **state**: `keyword`, `filters`, `sort { key, dir }`, `page`, `pageSize`, `summaryCollapsed`.
- **sắp xếp client-side**: `sortedRows` — `localeCompare(…, 'vi')` cho chữ, `sortType: 'date'` cho
  ngày, **ô trống luôn xuống cuối ở CẢ HAI chiều** (không thì bấm desc là cụm rỗng nhảy lên đầu).
- **phân trang client-side**: `pageCount`, `safePage` (kẹp biên), `pageOffset`, `pagedRows`.
- **luật chung**: đổi bộ lọc / đổi tập dữ liệu → `page = 1`. Chỉ dựa vào phép kẹp `safePage` là
  chưa đủ: tập mới vẫn nhiều trang thì người dùng bị bỏ lại ở trang 3 của kết quả khác.
- **`resetFilters()`**, **`toggleSort(key)`**.
- **hook `onFilterChange()`**: mixin gọi khi state lọc đổi, **màn tự cài** — emit lên cha
  (`DemandListModal`), gọi API (`ProjectListModal`), hay lọc tại chỗ (`DevelopmentDrillModal`).
- **`applyLocalFilters(rows)`**: hàm **tuỳ chọn**, chỉ popup lọc client-side gọi tới.

Popup server-side (sắp xếp / phân trang ở BE) chỉ lấy vỏ, **không** lấy mixin.

## Hợp đồng schema

```js
columns: [
    {
        key: 'customer',          // khoá cột, cũng là tên scoped slot `cell-customer`
        label: 'Khách hàng',
        field: 'customer_name',   // đường dẫn giá trị mặc định
        width: '220px',           // min-width, tuỳ chọn
        cellClass: 'text-right',  // tuỳ chọn
        sortable: true,           // tuỳ chọn
        sortType: 'text',         // 'text' | 'date'
        sortFields: ['a', 'b'],   // tuỳ chọn — sắp theo nhiều trường ghép
    },
]

filterFields: [
    { key: 'field', param: 'drill_field_id', placeholder: 'Chọn lĩnh vực', options: [] },
]
```

Đúng hai schema mẫu nguồn đang dùng, nên 2 popup kia khớp được mà không phải bẻ dữ liệu.

## Phạm vi đợt này

1. Thêm slot `header` vào `V2BaseModal`.
2. Dựng `V2BaseReportModal` + `reportDrillListMixin`.
3. Chuyển **một mình** `DemandListModal` sang dùng chúng: ước **1307 → ~550 dòng**.
4. Cập nhật e2e của màn.

2 popup lớn còn lại và 15 popup nhỏ chuyển ở đợt sau — Base thiết kế theo cả 3 nhưng chỉ chứng
minh trên 1.

## Hành vi BẮT BUỘC giữ nguyên

Đều là thứ đã trả giá và đang có ca e2e canh:

| Hành vi | Ca |
|---|---|
| Mở lượt sau KHÔNG mang dữ liệu / kích thước của lượt trước | 17 |
| Bảng cuộn trong khung, KHÔNG chạy xuyên hàng nút | 18 |
| Đổi bộ lọc → về trang 1; STT chạy tiếp qua trang | 19 |
| Chip cơ cấu và ô lọc phải khớp nhau (bấm chip thì ô lọc hiện đúng giá trị) | 4 |
| Popup lịch sử meeting mở ĐÈ lên popup nhu cầu, đóng lại popup cũ còn nguyên trang | 20, 21 |
| Phóng to toàn màn hình rồi thu nhỏ | 7 |
| `no-enforce-focus` + `V2BaseSelectInModal` để dropdown select2 không bị popup cắt | 8 |

## Cái giá phải trả

1. **Đổi tiền tố lớp CSS** `care-drill-*` → `report-drill-*` (Base không thể mang tên của riêng
   một màn). **106 chỗ** trong `e2e/tests/assign/potential-customer-care.spec.ts` phải sửa, nhiều
   nhất là `.care-drill-table` (41). Sửa bằng script rồi rà lại. Khi chuyển 2 popup kia sẽ churn
   thêm 19 chỗ (`cmd-drill`) và 15 chỗ (`tkt-drill`) ở 2 spec của chúng.
2. **`V2BaseModal` là component dùng chung của 30 màn** — chỉ thêm slot, không đổi mặc định.

## Kiểm chứng

Playwright, đo **trước / sau khi chuyển trên cùng một popup**, so bằng SỐ lấy từ DOM:

- bộ cột và thứ tự cột;
- số dòng trang 1, STT đầu/cuối, nội dung `.page-total`;
- kết quả sắp xếp 1 cột chữ + 1 cột ngày (so nguyên mảng giá trị);
- toạ độ đáy vùng bảng vs đỉnh hàng nút (lỗi footer trong suốt đã gặp);
- chiều cao popup lúc thường và lúc phóng to.

Rồi chạy lại **toàn bộ 29 ca** của màn.

> ⚠️ Vật cản môi trường đã biết: `hrm-api/database/e2e_provision.php` còn trỏ 5 bảng `hrm_*` đã bị
> `ReconcileEmployeesSeeder` gộp và xoá, nên `api-setup` đổ và mọi spec UI của HRM không chạy
> được. Phần nào không chạy được phải báo rõ, không được nói suông là đã kiểm.

## Ngoài phạm vi

- 3 `PrintOptionsModal` (không có bảng).
- `ReportPrintPreviewModal` (popup xem trước bản in — khuôn riêng, vừa sửa stacking context).
- Đổi giao diện 2 popup lớn còn lại (chuyển đợt sau).


---

## Kết quả thực hiện (18/09/2026)

### Đã dựng

| File | Vai trò |
|---|---|
| `components/report/V2BaseReportModal.vue` (481 dòng) | Vỏ: dải banner, nút phóng to, bảng theo schema `columns`, phân trang, cuộn-về-đầu khi lật trang |
| `utils/mixins/reportDrillListMixin.js` (146 dòng) | Máy: sắp xếp + phân trang client-side + state bộ lọc; lọc là HOOK |
| `components/modal/V2BaseModal.vue` (sửa) | Thêm slot `header` + prop `noEnforceFocus`, mặc định giữ nguyên hành vi cho 30 màn đang dùng |

3 popup đã chuyển, **giữ nguyên 3 chiến lược dữ liệu khác nhau** — đây là lý do kiến trúc tách 2 lớp:

| Popup | Dòng | Lọc | Sắp xếp / phân trang | Dùng |
|---|---|---|---|---|
| `DemandListModal` (CSKH tiềm năng) | 1307 → 871 | server (`$emit('filter')`) | client | vỏ + mixin |
| `DevelopmentDrillModal` (phát triển thị trường) | 1204 → 1050 | client | client | vỏ + mixin |
| `ProjectListModal` (kết quả dự án TKT) | 888 → 916¹ | BE | BE | **chỉ vỏ** |

¹ tăng vì bổ sung nút "Xoá lọc" + dải chip bấm được để lọc nhanh — vốn bị thiếu so với 2 popup kia.

### Quyết định phát sinh trong lúc làm (bổ sung cho mục "Quyết định đã chốt")

1. **`cellClass` do popup truyền vào vỏ phải khai `<style>` KHÔNG scoped.** Thẻ `<td>` do vỏ render
   nên thuộc tính scope của popup không với tới. Lớp nào ≥2 popup dùng chung y hệt thì đưa thẳng vào
   khối `scoped` của vỏ (`.report-drill-table__center`, `.report-drill-table__money`).
2. **Tên state `filters` / `keyword` là CỐ ĐỊNH** nếu dùng cơ chế lọc của mixin; chỉ các KHOÁ bên
   trong `filters` mới do từng popup tự đặt qua `emptyFilters()`.
3. **`resetFilterState()` (im lặng) vs `resetFilters()` (gọi hook)**: mọi đường mở popup / đổi đối
   tượng drill phải dùng bản im lặng — gộp 2 vai làm popup gọi API 2 lần.
4. **Adapter schema cột nằm ở phía popup**, KHÔNG sửa nguồn `columns` của BE (nó còn dùng cho bản in
   và Excel của màn).
5. **Popup phân trang/sắp xếp ở BE thì KHÔNG gắn mixin** — xem `ProjectListModal.vue` làm mẫu.

### Cái giá đã trả (để lần sau không lặp lại)

Baseline chỉ đo toạ độ + số dòng nên **không bắt được** 3 lỗi: mất viền khung bảng, mất chặn chiều
cao 92vh, và mất căn phải/in đậm ô tiền. Bộ đo Phase 2 đã bổ sung `getComputedStyle`, `overflow`,
khoảng cách nút footer. Ngoài ra: đổi tên lớp hàng loạt phải **đối chiếu selector ↔ class thật trong
nguồn** (Phase 1 sót 4 nhóm, Phase 2 sót thêm 9 selector không chứa chuỗi tiền tố).
