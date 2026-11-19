---
name: app-list-page
description: Quy chuẩn màn DANH SÁCH của TPE_APP (bám skill web list-page) — hàng tìm + nút lọc (ListFilterBar), bảng lọc chung showFilterSheet (chip / khoảng ngày / trang con chọn 1-nhiều / phạm vi Công ty→Phòng ban→Bộ phận / ô gõ), chip tiêu chí đang bật, nhóm theo hạn, thẻ, badge trạng thái, rỗng, đang tải, kéo tải lại, màn chọn (picker). Dùng khi làm / sửa màn danh sách, khi thêm tiêu chí lọc, khi bộ lọc mỗi màn một kiểu, khi "Làm mới" không xoá lọc.
---

# Màn danh sách — TPE_APP

Ví dụ tham khảo (không phải chuẩn — chuẩn là quy tắc dưới): **Phiếu giao việc** (bộ lọc đầy đủ, phạm vi), **Việc của tôi** (`ui/my_todo/my_todo_list_view.dart` — nhóm
theo hạn, lọc chip chọn 1). Đọc `app-components` mục 3 để biết widget.

## 1. Bố cục

```
PrimaryAppBar (☰/‹ · tiêu đề · chuông)          ← không nút lọc / ➕ trên header
ListFilterBar  [🔍 Tìm theo …        ] [⚙ 2]     ← dải trắng ngay dưới header
               (chip tiêu chí đang bật có ✕)   (dòng "Tổng 128 phiếu" / "24 / 128 phiếu · Xóa lọc")
RefreshIndicator → ListView (thẻ / nhóm)         ← kéo xuống = tải lại
```

- Placeholder ô tìm nói đúng trường BE lọc: "Tìm theo mã phiếu", "Tìm theo tên công việc" — không "Tìm kiếm".
- **KHÔNG hàng chip lọc nhanh** dưới ô tìm (`quickChips`) — bỏ ở 17 màn 29/10/2026 để đồng bộ: mọi tiêu chí,
  kể cả Trạng thái / Loại, nằm trong bảng lọc. KHÔNG nút ↻ / pill lọc riêng cạnh ô tìm.
- Tạo mới không đặt ở màn danh sách nếu phân hệ có nút giữa "Tạo mới" (`app-module-shell` mục 2).

## 2. Bảng lọc chung (`showFilterSheet`)

Khai tiêu chí 1 lần ở `List<FilterField> get _fields`, giữ giá trị trong `FilterValues _values`:

```dart
final v = await showFilterSheet(context, fields: _fields, initial: _values, onCount: _count, unit: 'phiếu', openField: field);
if (v != null && mounted) _apply(v);          // _apply: setState(_values = v) + gọi lại API
```

- **Tiêu chí = ĐÚNG bộ lọc màn web tương ứng** — không tự thêm / bớt, không đổi UI web (user chốt 26/10/2026).
- Loại trường: `FilterChipsField` (ít lựa chọn) · `FilterDateRangeField` · `FilterPickerField` (nhiều lựa chọn,
  trang con trượt ngang) · `FilterTextField` (BE lọc LIKE) · `advanced: true` → gập vào "Thêm tiêu chí".
- **Chọn 1** (`multi: false`): không ô tick, bấm dòng là chọn + quay lại, không footer Bỏ chọn/Xong; dòng có giá
  trị hiện ✕ để xoá nhanh. **Chọn nhiều** mới có ô tick + "ĐÃ CHỌN" + footer.
- Dòng trường chọn nhiều + chip tiêu chí ngoài danh sách hiện **TÊN** mục đã chọn ("Bản vẽ, Lắp đặt +1"), không
  ghi "3 mục" (user chốt 30/10/2026: chọn xong phải thấy đã chọn những gì).
- **Phạm vi Công ty → Phòng ban → Bộ phận** theo QUYỀN xem của màn (API `filter-options` riêng của màn), lọc
  tầng bằng `FilterPickerSection.parentKey` + `FilterSheetOption.parentId`; chỉ 1 công ty → ẩn nhóm Công ty.
- Footer: **"Làm mới"** (xoá mọi lựa chọn trong bảng) + **"Xem N <đơn vị>"** (đếm thử qua `onCount`).
- **Đọc giá trị theo kiểu:** 1 trường có thể là chip hoặc trang con tuỳ số lựa chọn (Trạng thái, Loại đào tạo)
  → `FilterValues.chips()` / `picked()` đã trả rỗng khi sai kiểu; màn đọc thử cả 2 kiểu được, KHÔNG tự ép
  `as Set` / `as List` (từng làm "Làm mới → Xem kết quả" không xoá lọc, 29/10/2026).
- Thanh lọc: `activeCount: _values.activeCount(fields)` (badge số), `activeChips: filterActiveChips(...)`
  (chip có ✕, bấm chip mở đúng trường), `onClearFilter: active > 0 ? () => _apply(FilterValues()) : null`.
- Giá trị mặc định của web (vd Trạng thái "Chưa xong") áp ngầm khi trường trống, không ép hiện chip.
- `FilterView` / `showFilterPanel` (ngăn kéo cũ) — chuyển dần khi sửa màn, không dùng ở màn mới.
- **"Cài đặt bộ lọc" đồng bộ web** (user chốt 30/10/2026): CHỈ làm cho màn mà web đã có cài đặt bộ lọc
  (`V2BaseSmartFilterPanel table="<x>"`) — web chưa có thì app cũng không có. Hiện có: Nhiệm vụ (`tasks`), Vấn đề
  (`issues`), Danh sách meeting (`meetings`; Lịch meeting của tôi không). App khai trường **cùng `key`, cùng nhãn,
  cùng thứ tự** `filterFields` web, không `advanced`; đọc / lưu qua `FilterLayoutStore.load('<x>')` /
  `FilterLayoutStore.save('<x>', l, leadingKeys: [kOrgField])` (custom_view/filter_layout_store.dart) và truyền
  `showFilterSheet(layout: …, onSaveLayout: …)` → bảng lọc chỉ hiện trường đang bật theo thứ tự, KHÔNG "Thêm tiêu
  chí", nút ⚙ "Cài đặt bộ lọc" mở trang tick + kéo sắp xếp, lưu `POST human/filter-customizations {table, config:
  [{key,isVisible}]}` (sửa ở app thì web thấy và ngược lại). Trường bị tắt thì giá trị lọc của nó bị xoá.
  Web tách 2 ô ngày (`from_date` / `to_date`) mà app gộp 1 ô khoảng ngày → ô app mang key ô đầu, lúc lưu ghi ô sau
  liền kề cùng trạng thái (mẫu `meeting_list_filter.dart` `_saveLayout`).
- **Lọc nhanh theo vai trò** (web có nút icon cạnh dòng Tổng: tôi làm / giao / theo dõi / duyệt KQ) → app để ở
  `WorkTotalLine(roles:, activeRole:, onRole:)` như web, KHÔNG nhét vào bảng lọc; bật thì có dòng "Đang lọc: … ✕".
  ⚠️ Dòng Tổng + nút vai trò phải hiện **cả khi danh sách rỗng** (tách `_totalLine()`, vẽ ở nhánh rỗng lẫn nhánh
  có dữ liệu) — để ở phần tử đầu ListView có dữ liệu thì lọc ra 0 dòng là mất luôn nút, không bỏ lọc được (lỗi thật 31/10/2026).
- Đổi lọc liên tục: màn giữ số lượt tải (`_seq`), bỏ kết quả lượt cũ về muộn (kẻo số Tổng lệch nút đang bật).

## 3. Nội dung danh sách

- **Dòng tổng** (user chốt 06/11/2026): `ListResultLine` tự trình bày "Tổng **128** phiếu" (chưa lọc) / "**24** / 128 phiếu"
  (đang lọc) — số đậm màu chữ chính, chữ xám. Màn chỉ truyền `resultText: '128 phiếu'` hoặc `'24 / 128 phiếu'`
  (số theo `en_US`), KHÔNG tự ghép chữ "Tổng" hay tự tô đậm.
- **Khoảng cách dòng tổng → thẻ đầu = 10** (user chốt 06/11/2026, khuôn màn Nhiệm vụ): `ListFilterBar(resultText:)` đã
  có lề dưới 10 → danh sách bên dưới để lề TRÊN = 0 (`EdgeInsets.fromLTRB(16, 0, 16, 16)`). Khai thêm lề trên 8 / 12 / 16
  là khoảng hở 18–26, nhìn rộng hơn các màn khác (đã sửa đồng loạt 18 màn ngày 06/11/2026).
- **Thẻ:** `AppCard` hoặc thẻ chuyên (`WorkItemCard`, `MeetingCard`). Dòng đầu: loại (chip màu loại) · vai trò ·
  badge trạng thái bên phải; tên đậm 14; các dòng meta có icon 13–14 xám (thời gian, địa điểm, bước…).
- **Badge trạng thái:** `StatusBadge` chữ + màu **do BE trả** (`status_text` / `status_color`), không map số →
  chữ / màu ở app. Màu chỉ trong 9 màu chuẩn web (xanh lá hoàn thành, xanh dương đang làm, cam chờ duyệt…).
- **Nhóm theo hạn** (Việc của tôi): Quá hạn → Hôm nay → Ngày mai → Tuần này → Tuần sau → Sau đó → Không hạn;
  Quá hạn LÊN ĐẦU; mặc định chỉ mở "Hôm nay"; tiêu đề nhóm chữ hoa màu nhóm + số đếm; nhóm rỗng ẩn (trừ 4 nhóm đầu).
  ⚠️ 1 việc nằm được ở 2 nhóm (Hôm nay/Ngày mai **và** Tuần này) → key thẻ PHẢI kèm nhóm (`ValueKey('<nhóm>-<loại>-<id>')`);
  key trùng thì mở cả 2 nhóm rồi đóng/mở/tick là ListView vỡ, bản release đứng hình cả tab (lỗi thật 31/10/2026).
- Việc nhiều ngày: hạn = hạn chót / giờ về (không phải ngày bắt đầu); thẻ ghi "Đi dd/MM → về dd/MM" và
  "Đang diễn ra, còn n ngày" (xanh) khi đang chạy — không tính quá hạn.
- Tìm phía app (lọc trên dữ liệu đã tải) chỉ khi API trả trọn; danh mục lớn → tìm phía máy chủ có phân trang
  (`MeetingSearchList`), debounce gõ phím.

## 4. Trạng thái màn

- Đang tải lần đầu: `ContentSkeleton(cards: 4)`; tải thêm cuối danh sách: `ListFooterSkeleton`.
- **Rỗng:** `AppEmptyWidget(filtered: <đang tìm / lọc>)` → "Không có dữ liệu." / "Không có dữ liệu phù hợp."
  (MỌI màn giống nhau, user chốt 28/10/2026). KHÔNG nút "Xóa bộ lọc" / "Tải lại" ở màn rỗng; vẫn bọc
  `ListView(physics: AlwaysScrollableScrollPhysics())` để kéo tải lại được.
- Lỗi tải: `AppEmptyWidget(title: <câu lỗi BE>)` (title chỉ dành cho trạng thái khác rỗng).
- Sau khi màn con đổi dữ liệu (tick, lưu, xoá) → danh sách tự tải lại (nghe `ValueNotifier` chung hoặc
  `push(...).then(reload)`), không bắt user kéo.

## 5. Màn chọn (picker) — 1 khuôn chung (user chốt 06/11/2026)

Bản vẽ: board "PK · Màn chọn — khuôn chung" trong `meeting-mobile_v2.pen` (PK-01 → PK-04).

- **Dòng chọn = `AppPickTile`** (`custom_view/app_pick_tile.dart`) ở MỌI màn chọn: danh sách PHẲNG trên nền
  trắng, kẻ dưới mảnh, tên 15 + dòng phụ xám 12.5. Mục đang chọn chữ đậm màu phân hệ + ✓. KHÔNG thẻ / khối gom
  nhóm, KHÔNG avatar, KHÔNG dấu › (› = mở sang màn khác). Không chọn được → `enabled: false` (mờ) + `note:` lý do (cam).
- **≤ 8 mục, không cần tìm** → `showAppPickSheet(context, title:, items: [AppPickItem(value, title, subtitle:)],
  isSelected:, clearValue:, message:)` (PK-03: thanh kéo · tiêu đề + ✕ · các dòng). KHÔNG tự dựng
  `showModalBottomSheet` + `ListTile` cho bảng chọn.
- **> 8 mục / danh mục đã tải** → `pickWorkOption` (tự chọn bảng trượt hay trang theo số mục).
- **Tìm máy chủ** (nhân sự, khách hàng, dự án, hợp đồng) → trang toàn màn `MeetingSearchList(flat: true)` +
  `CommonScaffold(backgroundColor: Colors.white)` + `PrimaryAppBar(showNotificationBell: false)` (header ‹, không ✕,
  không chuông, không nút Hủy đáy). Không dòng "KẾT QUẢ · n".
- **Ô không bắt buộc đang có giá trị** → dòng "Bỏ chọn" (`AppPickClearTile`) đầu danh sách
  (vd `pickEmployee(selectedId:, allowClear: true)` → trả `kPickEmployeeCleared`).
- **Chọn nhiều** (PK-04) → `AppPickTile(multi: true)` (vòng tròn bên phải) + thanh đáy `[Hủy | Xác nhận (n)]`;
  trang con chọn nhiều của bảng lọc cũng dùng vòng tròn.
- Mẫu: `pickEmployee()`, `CustomerPickerPage`, `MeetingCustomerPickerPage`, `MeetingProjectPickerPage` (chọn nhiều),
  `MeetingContractPickerPage`, `MeetingEmployeePickerPage`, `pickWorkOption`.
- Nhân viên: `Tên` + dòng phụ `chức danh · phòng ban · mã` (web: `Tên - Mã phòng - Mã NV`).

## Checklist

- [ ] `ListFilterBar` ngay dưới header, placeholder đúng trường; không quickChips / ↻
- [ ] Tiêu chí lọc khớp web; chọn 1 không ô tick; phạm vi theo quyền + lọc tầng
- [ ] "Làm mới" → "Xem kết quả" xoá hết lọc thật (đã bấm thử)
- [ ] Badge chữ + màu từ BE; rỗng dùng `AppEmptyWidget(filtered:)`; kéo tải lại được
- [ ] Đổi dữ liệu ở màn con → danh sách tự cập nhật
