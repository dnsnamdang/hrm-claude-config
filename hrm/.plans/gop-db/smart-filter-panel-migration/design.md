# Design — Gom bộ lọc về một panel duy nhất

## Mục tiêu
Toàn hệ thống chỉ còn **một** khối bộ lọc: `V2BaseSmartFilterPanel` + nhãn floating,
trông giống hệt màn mẫu `/master-data/product-natures`.

## Hiện trạng trước khi làm (nhánh `gop_db`)
- 56 file dùng `V2BaseFilterPanel` (bản cũ, nhận ô lọc qua slot `#advanced-filters`)
- 101 file dùng `V2BaseSmartFilterPanel`, trong đó **51 file chưa bật `floating`**
- Hai panel khác API hoàn toàn: bản cũ nhận markup qua slot, bản mới nhận **schema `filterFields`**

## Quyết định đã chốt
| Điểm | Chốt |
| --- | --- |
| Panel | `V2BaseSmartFilterPanel` là duy nhất; `V2BaseFilterPanel` **xoá khỏi repo** |
| Nhãn | `floating` bắt buộc ở MỌI màn, kể cả bộ lọc gọn ≤ 3 ô |
| Khoảng cách trên/dưới khối lọc | `pb-2` = 0.5 × `$spacer` (1.5rem) = **12px** — vỏ trang `pt-2`, card `mb-2`, padding trong card do component lo. Màn không tự khai |
| Dấu `*` ô lọc bắt buộc | Thêm `required` vào `floatingProps()` của panel (user duyệt) |
| Select trong modal | Thêm prop `in-modal` cho panel + control → render `V2BaseSelectInModal` (user duyệt) |
| Ô chọn nhiều | Thêm `field.multiple` cho control, panel tự dùng `variant: 'tags'` (user duyệt) |
| Ô gộp Nhóm ngành–Nhóm GP–Ứng dụng | Thêm prop `floating` cho `V2BaseFieldCategoryApplicationFilter` (user duyệt) |
| Cặp "từ – đến" | Gộp về MỘT field `type: 'date-range'` + `resetKeys`; 2 key gửi BE giữ nguyên |
| Nút "Tìm kiếm/Làm mới" tự chế trong slot | Bỏ, dùng nút mặc định của panel. Điều kiện chặn (`canSearch`) chuyển vào `handleSearch()` + toast, vì nút xám bị cấm |
| `show-text` / `hide-text` | Bỏ — panel mới cố định "Tìm kiếm nâng cao" / "Ẩn tìm kiếm nâng cao" |
| Placeholder | Bỏ mọi placeholder trùng nhãn (floating đã nói đủ) và mọi placeholder cấm (`Tất cả`, `Chọn...`) |

## Bẫy đã gặp
- **`.editorconfig` khai `end_of_line=crlf`** trong khi `.gitattributes` bắt LF → chạy `prettier --write`
  trần là cả file thành CRLF. Luôn dùng `npx prettier --end-of-line lf --write`.
- 4 file vốn KHÔNG đạt chuẩn prettier từ trước (`task-manager-by-employees` thụt 2 space) —
  chạy prettier lên là diff phình 1.758 dòng nhiễu. Đã bỏ qua prettier cho 4 file đó.
- Field gộp phải khai **khoá của chính ô** (`created_range`, `date_range`…) trong state ban đầu,
  Vue 2 không reactive với property chưa khai.
- Component tự vẽ nhãn trong slot (`V2BaseCompanyDepartmentFilter`, `CascadePairSelect`,
  `CheckboxMultiSelect`) phải nhận `:floating="true"`, không thì lệch kiểu với phần còn lại.
- Select trong slot phải `height="36px"`: `updateHeight()` ghi inline `!important`.
