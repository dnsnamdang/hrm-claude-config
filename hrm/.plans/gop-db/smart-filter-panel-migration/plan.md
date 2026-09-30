# Plan — Chuyển toàn bộ `V2BaseFilterPanel` → `V2BaseSmartFilterPanel`

Nhánh: `gop_db` (client `worktrees/gop_db-client`, cổng 3002/8003) · Phụ trách: @namdangit

Chuẩn tham chiếu: `http://127.0.0.1:3002/master-data/product-natures`.

## Phase 0 — Chuẩn hoá skill
- [x] `list-page/SKILL.md`: chốt `V2BaseSmartFilterPanel` là panel DUY NHẤT, `V2BaseFilterPanel` đã xoá
- [x] Bổ sung mục khoảng cách trên/dưới khối lọc = `pb-2` (0.5 × `$spacer 1.5rem` = 12px)
- [x] Chốt `floating` BẮT BUỘC ở mọi màn; ghi thêm `in-modal`, `multiple`, `required`

## Phase 1 — Bổ sung component dùng chung (đã xin phép user)
- [x] `V2BaseSmartFilterPanel`: prop `required` truyền xuống `V2BaseFloatingField`
- [x] `V2BaseSmartFilterPanel` + `V2BaseFilterFieldControl`: prop `in-modal` → dùng `V2BaseSelectInModal`
- [x] `V2BaseFilterFieldControl`: `field.multiple` → `extraSettings: { multiple: true }`, panel tự dùng `variant: 'tags'`
- [x] `V2BaseFieldCategoryApplicationFilter`: prop `floating` (opt-in, mặc định false)

## Phase 2 — Chuyển 56 file dùng panel cũ
- [x] Nhóm A — màn danh sách `pages/**/index.vue` (finance 3, timesheet 1, assign 2)
- [x] Nhóm B — màn báo cáo `pages/assign/report/**` (13 file)
- [x] Nhóm C — tab/modal my-job + solutions + solution-modules (28 file)
- [x] Nhóm D — component dùng chung + modal tìm kiếm (9 file)

## Phase 3 — Chuẩn hoá 51 màn đã dùng Smart nhưng chưa chuẩn
- [x] Bật `floating`
- [x] Bỏ placeholder trùng nhãn (cả `filterFields` lẫn slot `#field-*`) và placeholder cấm (`Tất cả`, `Chọn...`)
- [x] `:floating="true"` cho component tự vẽ nhãn trong slot; `height="36px"` cho select trong slot

## Phase 4 — Kiểm tra
- [x] `grep -rn "<V2BaseFilterPanel" pages components` → RỖNG
- [x] Xoá `components/V2BaseFilterPanel.vue`
- [x] 0/101 màn còn thiếu `floating`
- [x] Parse toàn bộ 111 file bằng `vue-template-compiler` + `@babel/parser` → không lỗi
- [x] Không còn component đăng ký thiếu import / import bị xoá nhầm / `this.xxx` không tồn tại
- [x] Prettier + EOL = LF (bỏ qua 4 file vốn đã lệch chuẩn để diff không phình)
- [x] Verify Playwright — 6 màn đại diện, mở từng ô lọc

## Phase 5 — Lỗi phát hiện khi verify (đã sửa)
- [x] Ô chip: nhãn float **đè lên chip hàng đầu 2px** → `.ff--tags.is-float .ff__control { padding-top: 9px }`
- [x] Ô chọn nhiều: **viền đôi** (vỏ `.ff--tags` + viền riêng của select2) → bỏ viền trong
- [x] Ô chọn nhiều: cao **42px** thay vì 36px → ép `min-height: 26px` + đệm khối chip 2px
- [x] 62 ô `type: 'date'`: cao **32px** → selector nặng ký đè rule 32px của `V2BaseDatePicker`
- [x] 9 slot ở 7 màn: `V2BaseSelectRemote` thiếu `height="36px"` → cao 32px lệch hàng
- [x] Bổ sung mục "MỌI Ô LỌC PHẢI CAO ĐÚNG 36px" + đoạn script tự kiểm vào skill `list-page`

## Phase 6 — Gộp cặp ngày ở 30 màn còn lại (user chốt làm luôn)
- [x] 31 cặp "từ ngày – đến ngày" ở 30 màn → 1 ô `type: 'date-range'` + `resetKeys` + `inputCount: 1`
      (`/assign/tasks` có 2 cặp). 2 key gửi BE giữ nguyên, không đụng `loadData()` lẫn BE.
- [x] Khai khoá của ô gộp trong state ban đầu (Vue 2 reactivity)
- [x] `MultiSearchPicker` (ô Tag ở `/assign/tasks`) cao 32px → ép 36px trong `V2BaseFloatingField`
- [x] Verify: 20 màn quét tự động, 0 hàng lệch chiều cao, 0 ô ≠ 36px

## Phase 7 — Lỗi user chỉ ra khi review (đã sửa)
- [x] `device-errors`: 3 slot tự vẽ **nhãn tĩnh** (không floating) + thừa 1 dòng nhãn → bỏ `hideLabel`,
      slot chỉ render control; "Đơn giá bán từ/đến" gộp 1 ô `variant: 'range'`
- [x] Rà TOÀN BỘ: **24 slot ở 13 file** còn vẽ nhãn tĩnh → 13 cặp ngày chuyển hẳn `type: 'date-range'`
      (xoá slot), 7 cặp tiền chuyển `variant: 'range'` (slot chỉ còn 2 ô + dấu →), 4 ô đơn bỏ nhãn tĩnh
- [x] `V2BaseCurrencyInput` cao 32px trong vỏ floating → ép 36px
- [x] Ô tiền trong khoảng "từ – đến" bị **viền lồng nhau** → bỏ viền/đệm riêng như datepicker
- [x] `MultiSearchPicker` (ô Tag) cao 32px → ép 36px
- [x] 3 `V2BaseSelect` ở `product-transfers` thiếu `height="36px"`
- [x] **19 slot gõ tay không bắt Enter** → gắn `@keyup.enter.native` vào đúng hàm search của từng màn
- [x] **9 màn báo cáo không tự tìm khi đổi select** → `handleFilterChange` gọi search cho ô CHỌN
      (ô gõ tay vẫn chờ Enter). `prospective-project-results` có guard tránh gọi 2 lần.
- [x] Skill `list-page`: thêm bảng luật "ô chọn → tìm luôn / ô gõ tay → Enter" + ngoại lệ

## Phase 8 — Bug trên bản deploy (user phát hiện ở hrm-crm.eteksofts.com)
- [x] `warehouse-export-requests`: slot `org` thiếu `:floating="true"` → nhãn tĩnh (sửa 1 file)
- [x] **Khối Công ty–Phòng ban co sập còn 7px trên bản build**: `.d-contents { display: contents }`
      nằm ở `v2-styles.scss`, mà 226 file import file này trong `<style scoped>` → selector bị gắn
      `data-v` của TRANG, không khớp phần tử do PANEL render. Chỉ chạy khi tình cờ có component nào
      đó import không scoped → cùng bản build, màn đúng màn sai.
      Đã chuyển 4 rule `.d-contents` vào `<style>` KHÔNG scoped của `V2BaseSmartFilterPanel`.
      Kiểm chứng: xoá sạch 40 rule `.d-contents` đến từ CSS của trang → ô vẫn 323px.
- [x] BE `CatalogHistoryService.php` thiếu `]],` dòng 483 (entry `meeting_room_settings`) → parse
      error, **mọi màn danh mục bấm Lịch sử đều chết**. Đã vá, `php -l` sạch, quét 4.375 file PHP
      không còn lỗi cú pháp nào khác.

### Bài học về cách kiểm (ghi để không lặp lại)
- Audit chỉ đếm phần tử `.ff` là **SAI** — ô render trong slot bằng nhãn tĩnh không có `.ff` nên bị
  bỏ qua hoàn toàn, báo "0 lỗi" trong khi màn đang hỏng. Phải duyệt **từng cột** của `.form-row`.
- Audit phải phủ cả **3 chế độ**: tìm nhanh · bộ lọc gọn (`.inline-field`) · nâng cao.
- **Đừng dò auto-search bằng regex trên file Vue** — đã cho kết quả sai 3 lần liên tiếp (30 → 150 →
  toàn dương tính giả). Cách đúng: đổi 1 select trên trình duyệt rồi **đếm request**: 0 = không
  auto-search, 1 = đúng, ≥2 = gọi trùng.
- Khi đo phải trừ nhiễu: màn có guard (`canSearch`) không gọi API là ĐÚNG, không phải lỗi.
- **Đo cả CHIỀU RỘNG, không chỉ chiều cao.** Ô co sập 7px vẫn cao đúng 36px → audit chỉ đo cao báo "đạt".
- **Cột `d-contents` có rect = 0** (display: contents) → audit phải lặn vào trong, đừng bỏ qua theo rect.
- **Kiểm trên LOCAL không đủ**: dev-server tách CSS theo trang nên lỗi chỉ lộ trên bản build. Với lỗi
  CSS nghi do scoped, phải mở đúng cổng dev hoặc mô phỏng bằng cách `deleteRule` các rule của trang.
- Muốn "tắt" một rule để thử thì phải `deleteRule`, **đừng gán giá trị khác** — gán sẽ đè luôn rule
  đang muốn kiểm (thứ tự nguồn), cho kết luận sai.

### Checkpoint — 2026-09-21 (sau verify)
Vừa hoàn thành: Phase 0–6. 113 file thay đổi. Panel cũ đã xoá, 0 màn thiếu `floating`,
0 màn còn tách 2 ô ngày, mọi ô lọc cao đúng 36px.
Đang làm dở: không.
Bước tiếp theo: user duyệt rồi commit/push (chưa commit).
Blocked:

### Checkpoint — 2026-09-21
Vừa hoàn thành: toàn bộ Phase 0–4 (trừ verify trình duyệt).
Đang làm dở: không.
Bước tiếp theo: user duyệt → chạy Playwright rà một số màn đại diện (báo cáo, modal, bộ lọc gọn).
Blocked:
