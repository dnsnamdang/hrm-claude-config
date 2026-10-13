# Task 6 — Báo cáo: Đối chiếu baseline + đổi selector e2e

Thư mục làm việc: `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM`
Brief gốc: `.plans/gop-db/base-popup-bao-cao/.sdd/task-6-brief.md` (path trong brief ghi `.plans/base-popup-bao-cao/...` — đã dùng path mới `.plans/gop-db/base-popup-bao-cao/...`)

## Step 1 — So baseline với sau khi chuyển

Input:
- `.plans/gop-db/base-popup-bao-cao/baseline.json` (Task 1)
- `/tmp/after.json` (Task 5, timestamp 17/09 20:25)

Lệnh chạy:
```bash
python3 - <<'PY'
import json
a = json.load(open('.plans/gop-db/base-popup-bao-cao/baseline.json'))
b = json.load(open('/tmp/after.json'))
all_keys = ['cols', 'firstPageRowCount', 'sttFirst', 'sttLast', 'pageTotal',
            'sortTextAsc', 'sortDateAsc', 'tableBottom', 'footerTop',
            'heightNormal', 'heightFull']
...
PY
```

Kết quả — bảng so 11 khoá:

| Khoá | Trước (baseline) | Sau (after) | Khớp? |
|---|---|---|---|
| cols | 13 cột (STT…Dự án TKT) | giống hệt | ✅ |
| firstPageRowCount | 20 | 20 | ✅ |
| sttFirst | "1" | "1" | ✅ |
| sttLast | "20" | "20" | ✅ |
| pageTotal | "Hiển thị 1–20 / 126 nhu cầu" | giống hệt | ✅ |
| sortTextAsc | 20 dòng | giống hệt | ✅ |
| sortDateAsc | 20 dòng | giống hệt | ✅ |
| heightNormal | 844 | 844 | ✅ |
| heightFull | 900 | 900 | ✅ |
| **tableBottom** | **713** | **709** | ❌ lệch 4px |
| **footerTop** | **803** | **787** | ❌ lệch 16px |

**9/11 khớp tuyệt đối, 2 khoá lệch đúng như đã báo trước: `tableBottom` (713→709, lệch 4px) và `footerTop` (803→787, lệch 16px). KHÔNG có khoá thứ ba lệch.**

Bất biến kiểm tra thêm:
- `tableBottom <= footerTop`: `709 <= 787` → **True** (bảng không chạy xuyên hàng nút)
- `heightFull > heightNormal`: `900 > 844` → **True** (nút phóng to còn tác dụng)

Kết luận Step 1: đúng như đã được xác nhận trước — 2 lệch này là hệ quả cố ý của việc bỏ khung footer riêng để dùng `.modal-footer` chuẩn của `V2BaseModal`. Theo chỉ đạo, **KHÔNG sửa `baseline.json`**, không quay lại Task 5.

## Step 2 — Đổi selector trong spec

Lệnh chạy (path đúng: `HRM/e2e`, không phải `HRM/e2e` dưới `cd HRM/e2e` như brief ghi — đã tự chỉnh theo path thực tế của môi trường):
```bash
cd e2e && python3 - <<'PY'
p = 'tests/assign/potential-customer-care.spec.ts'
s = io.open(p, encoding='utf-8', newline='').read()
truoc = s.count('care-drill')
s = s.replace('care-drill', 'report-drill')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('đã đổi', truoc, 'chỗ')
PY
```

Output thật: `đã đổi 110 chỗ`

⚠️ **Lệch với con số kỳ vọng trong brief (106 chỗ) — thực tế 110 chỗ.** Đây không phải lỗi của bước đổi (script chỉ đếm/đổi chuỗi con `care-drill`, tự nhất quán trước/sau); con số 106 trong brief nhiều khả năng là ước tính cũ từ lúc soạn brief, trước khi spec có thêm vài chỗ dùng `care-drill-*`. Đã kiểm `grep -c "care-drill"` sau khi đổi → **0** (không còn sót).

## Step 3 — Rà theo brief + đối chiếu thật với mã nguồn (bổ sung theo yêu cầu)

### 3a. Grep theo regex whitelist của brief

```bash
grep -n "report-drill" tests/assign/potential-customer-care.spec.ts \
  | grep -vE "report-drill-(table|head|sort|count|filters|dialog|content|paging|sum|customer|meeting|footer|wrap|scroll|back|sub)"
```

Output (brief kỳ vọng RỖNG, thực tế ra 3 dòng):
```
66:    const toggle = modal.locator('.report-drill-toggle');
328:    const toggle = modal.locator('.report-drill-toggle');
694:        seenCarry += await modal.locator('.report-drill-carry').count();
```

Regex whitelist của brief thiếu 2 hậu tố `toggle` và `carry` nên báo dương tính giả — **KHÔNG tự động coi đây là lỗi**, chuyển sang bước 3b để đối chiếu thật với mã nguồn thay vì làm theo máy móc chỉ dẫn "trả về `care-drill-*`" của brief.

### 3b. Đối chiếu từng selector `report-drill-*` với class/id THẬT trong mã nguồn (bắt buộc, không có trong brief)

Nguồn đối chiếu:
- `hrm-client/components/report/V2BaseReportModal.vue`
- `hrm-client/pages/assign/report/potential-customer-care/components/DemandListModal.vue`
- `hrm-client/pages/assign/report/potential-customer-care/components/KpiBoxes.vue` (nhận `id-prefix="report-drill"` từ `DemandListModal.vue:120`)

29 selector duy nhất trích từ spec (`grep -oE "report-drill[a-zA-Z0-9_-]*" ... | sort -u`), đối chiếu từng cái:

| Selector | Có trong mã nguồn? | Nơi định nghĩa |
|---|---|---|
| `.report-drill-back`, `__from` | ✅ | `DemandListModal.vue:104,109,794,800` |
| `.report-drill-carry` | ✅ | `DemandListModal.vue:187` (template) + `:837` (style) |
| `.report-drill-content` | ❌ **KHÔNG có** | chỉ xuất hiện trong COMMENT của `V2BaseReportModal.vue:198` giải thích nó **KHÔNG tồn tại làm class riêng** ("bản gốc gắn nó thẳng vào `.report-drill-dialog`"). Class thật để trỏ container là `.report-drill-dialog .modal-content` / `.modal-body`. |
| `.report-drill-count` | ✅ | `DemandListModal.vue:97,684` |
| `.report-drill-customer`, `__name` | ✅ | `DemandListModal.vue:157-158,819` |
| `.report-drill-dialog`, `--full` | ✅ | `V2BaseReportModal.vue:24,140,195-196,207,213,...` |
| `.report-drill-filters__item`, `--search`, `--action` | ✅ | `DemandListModal.vue:54,62,75,638,642,646` |
| `.report-drill-footer` | ❌ **KHÔNG có** | chỉ xuất hiện trong COMMENT của `V2BaseReportModal.vue:268` — "ĐÃ GỠ `.report-drill-footer`" ở "Vòng sửa 3/5". Footer thật bây giờ là `.modal-footer` chuẩn của `V2BaseModal`. |
| `.report-drill-head__btn`, `__object`, `__sub` | ✅ | `V2BaseReportModal.vue:33,36,42,48,346,350,362` |
| `.report-drill-meeting` | ✅ | `DemandListModal.vue:180` (dùng cùng `.report-drill-link`) |
| `.report-drill-project` | ✅ | `DemandListModal.vue:199` (dùng cùng `.report-drill-link`) |
| `.report-drill-scroll-top` | ❌ **KHÔNG có** | 0 kết quả grep trong toàn `hrm-client`. Không phải tên đã đổi — tên này chưa từng tồn tại. Class gần giống duy nhất là `.report-drill-scroll` (không có hậu tố `-top`, `V2BaseReportModal.vue:59,248`). |
| `.report-drill-sort` | ✅ | `V2BaseReportModal.vue:66,429` |
| `.report-drill-sum__chip`, `--on`, `__n` | ✅ | `DemandListModal.vue:137-144,759,778,782` |
| `.report-drill-sumbox` | ✅ | `DemandListModal.vue:125-126,692,698` |
| `.report-drill-table`, `__empty` | ✅ | `V2BaseReportModal.vue:61,383,84,422` |
| `.report-drill-toggle` | ✅ | `DemandListModal.vue:87` (`class="rsum-toggle report-drill-toggle"`) |
| `.report-drill-topscroll` | ❌ **KHÔNG có** | chỉ xuất hiện trong COMMENT của `V2BaseReportModal.vue:381` — "không còn `.report-drill-topscroll` trong file này", đã thay bằng `.v2-table-scroll__top.scrollbar-thin` (khối CSS không-scoped). |
| `.report-drill-wrap` | ✅ | `V2BaseReportModal.vue:60,244(khớp `.report-drill-wrap` qua comment),288,295,299,302,306` |

**Kết luận 3b — quyết định KHÔNG revert `toggle`/`carry`:** `report-drill-toggle` và `report-drill-carry` (bị regex ở brief báo dương tính giả) đối chiếu thật với `DemandListModal.vue` thì **CÓ tồn tại đúng class đó**, không phải lớp riêng của màn bị đổi nhầm. Whitelist của brief chỉ thiếu 2 hậu tố. Theo đúng chỉ đạo "đối chiếu với mã nguồn thật" > làm máy móc theo brief, đã **giữ nguyên `report-drill-toggle`/`report-drill-carry`**, không trả về `care-drill-*`.

### Danh sách selector nghi vấn — dấu hiệu ca test sẽ đỏ (4 class, 8 dòng spec)

Không tìm thấy class ở nơi định nghĩa thật (chỉ còn trong comment cảnh báo "đã gỡ"/"không tồn tại"):

1. **`.report-drill-content`** — dòng spec: 315, 589, 604, 708
2. **`.report-drill-footer`** — dòng spec: 591, 1081
3. **`.report-drill-scroll-top`** — dòng spec: 1049, 1056 (dùng chung locator OR với `.report-drill-topscroll`)
4. **`.report-drill-topscroll`** — dòng spec: 1049, 1056 (cùng 2 dòng với #3)

→ Cả 4 class này đều **không tồn tại trong DOM sau khi Task 5 hoàn tất** (V2BaseReportModal.vue đã cố ý gỡ bỏ wrapper riêng để dùng cấu trúc chuẩn của `V2BaseModal`: `.modal-content`, `.modal-body`, `.modal-footer`, `.v2-table-scroll__top`). Các dòng spec dùng 4 class này (8 dòng, một số dòng dùng cùng lúc 2 class ở #3+#4) nhiều khả năng sẽ FAIL khi chạy — đây là việc của Task 7 (chạy test), task này **chỉ báo, không tự sửa mã nguồn**.

## Step 4 — Kiểm spec vẫn biên dịch

```bash
PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test tests/assign/potential-customer-care.spec.ts --list --no-deps 2>&1 | tail -3
```

Output thật:
```
  [chromium] › assign/potential-customer-care.spec.ts:1602:5 › 28. Bộ lọc chuẩn mới: nhãn floating, ô ngày gộp, popup "Cài đặt bộ lọc" ẩn trường thì xoá giá trị
  [chromium] › assign/potential-customer-care.spec.ts:1686:5 › 29. Popup xem biên bản mở TỪ panel chi tiết phải nằm TRÊN nền mờ của panel
Total: 29 tests in 1 file
```

Khớp đúng kỳ vọng brief: **29 tests**, spec biên dịch bình thường.

## Step 5 — Commit

Kiểm tra `HRM/e2e` có git riêng hay không:
```bash
git -C e2e rev-parse --show-toplevel   # fatal: not a git repository
git -C . rev-parse --show-toplevel     # HRM/ cũng không phải git repo (đến tận filesystem root)
```

**Kết quả: `HRM/e2e` KHÔNG phải git repo (không có `.git` ở chính nó lẫn bất kỳ thư mục cha nào trong `ERP-HRM/`).** `hrm-client` và `hrm-api` mỗi cái có `.git` riêng (`hrm-client` đang ở nhánh `gop_db`), nhưng `e2e/` đứng độc lập, không version-control.

→ **Không thực hiện `git add` / `git commit`** cho file spec. File đã sửa trực tiếp tại `HRM/e2e/tests/assign/potential-customer-care.spec.ts`, chưa có commit nào (không thể có, vì không có repo).

## Việc KHÔNG làm (đúng phạm vi Task 6)

- Không đụng `components/V2BaseSmartFilterPanel.vue`, `components/print/ReportPrintPreviewModal.vue`, `pages/assign/report/potential-customer-care/components/CareTrackingTable.vue`, `pages/assign/report/potential-customer-care/index.vue`
- Không chạy cả bộ test (dành cho Task 7)
- Không sửa `baseline.json`
- Không sửa mã nguồn `hrm-client` để chiều theo 4 class nghi vấn ở trên

---

## Vòng sửa 1/5 — sửa 4 nhóm selector trỏ vào lớp đã gỡ

Coordinator ra ruling: 4 class nghi vấn ở vòng đầu (`report-drill-content`, `report-drill-footer`,
`report-drill-topscroll`, `report-drill-scroll-top`) là **việc của Task 6**, không đẩy sang Task 7.
Ánh xạ theo ruling — nhưng khi áp dụng thực tế, đã **scope thêm `.report-drill-dialog`** cho 2 lớp
Bootstrap chung (`modal-content`, `modal-footer`) thay vì dùng bare/trần, lý do trình bày dưới đây.

### Vì sao không dùng bare `.modal-content` / `.modal-footer` ở mọi chỗ

Cột "Vì sao" của ruling viết: *"Vỏ nay dùng style qua selector hậu duệ `.report-drill-dialog
.modal-content`"* — tự nó đã gợi ý cách scope đúng. Kiểm tra thêm trong chính spec (test 11,
dòng 583-609) phát hiện: khi popup "Xem trước in" (`ReportPrintPreviewModal.vue`, dựng bằng
`<b-modal hide-footer>`) mở ĐÈ lên popup drill-down, cả 2 modal cùng tồn tại trong DOM tại một số
thời điểm. Nếu dùng `page.locator('.modal-content')` TRẦN (không scope), `expect(...).toBeVisible()`
sẽ vỡ **strict mode** (2+ phần tử khớp) ngay khi cả 2 popup cùng có mặt. Nên áp dụng:

- **`.report-drill-content` → `.report-drill-dialog .modal-content`** (không phải bare `.modal-content`)
- **`.report-drill-footer` (dùng qua `page.locator`) → `.report-drill-dialog .modal-footer`**
- **`.report-drill-footer` (dùng qua `modal.locator(...)`, biến `modal` đã scope sẵn bằng `page.locator('.modal.show')`) → `.modal-footer`** (không cần scope lại 2 lần, đúng pattern có sẵn trong file ở dòng 1024/1046/1053)
- **`.report-drill-topscroll` / `.report-drill-scroll-top` (đi cùng nhau dạng OR `'a, b'`) → gộp về 1 selector `.v2-table-scroll__top`**, xoá vế `.report-drill-scroll-top` chết theo đúng chỉ đạo ("gộp lại thành một selector đúng, đừng để lại vế chết")

Xác minh cấu trúc DOM cho phép scope `.report-drill-dialog .modal-content` / `.report-drill-dialog
.modal-footer`:
- `V2BaseReportModal.vue:24` truyền `dialog-class="... report-drill-dialog ..."` xuống `<V2BaseModal>`
- `V2BaseModal.vue:17` truyền tiếp `:dialog-class="dialogClass"` vào `<b-modal>` — bootstrap-vue gắn class này lên `.modal-dialog` (cha trực tiếp của `.modal-content`)
- `V2BaseModal.vue:77` render `<div class="modal-footer v2-modal-footer">` bên trong `.modal-content`

→ Cây DOM thật: `.modal-dialog.report-drill-dialog > .modal-content > (...) .modal-footer.v2-modal-footer`. Selector hậu duệ `.report-drill-dialog .modal-content` và `.report-drill-dialog .modal-footer` khớp đúng cấu trúc này, không suy đoán.

`.v2-table-scroll__top` xác minh tại `V2BaseTableScroll.vue:5` (`<div v-show="overflowing" ref="topScroll" class="v2-table-scroll__top scrollbar-thin">`).

### Lệnh sửa (Python, giữ nguyên LF — file này không phải CRLF, đã kiểm `grep -c $'\r'` = 0)

5 phép thay literal-string, mỗi phép kiểm số lần khớp trước khi ghi:

| Chuỗi cũ | Chuỗi mới | Số chỗ |
|---|---|---|
| `document.querySelector('.report-drill-content .modal-body')` | `document.querySelector('.report-drill-dialog .modal-content .modal-body')` | 1 |
| `page.locator('.report-drill-content')` | `page.locator('.report-drill-dialog .modal-content')` | 3 |
| `page.locator('.report-drill-footer')` | `page.locator('.report-drill-dialog .modal-footer')` | 1 |
| `modal.locator('.report-drill-footer')` | `modal.locator('.modal-footer')` | 1 |
| `modal.locator('.report-drill-scroll-top, .report-drill-topscroll')` | `modal.locator('.v2-table-scroll__top')` | 2 |

Output thật — tất cả 5 phép đều `[OK]` đúng số lượng kỳ vọng, không có phép nào 0 chỗ:
```
[OK] 1 chỗ (kỳ vọng 1): document.querySelector('.report-drill-content .modal-body') -> document.querySelector('.report-drill-dialog .modal-content .modal-body')
[OK] 3 chỗ (kỳ vọng 3): page.locator('.report-drill-content') -> page.locator('.report-drill-dialog .modal-content')
[OK] 1 chỗ (kỳ vọng 1): page.locator('.report-drill-footer') -> page.locator('.report-drill-dialog .modal-footer')
[OK] 1 chỗ (kỳ vọng 1): modal.locator('.report-drill-footer') -> modal.locator('.modal-footer')
[OK] 2 chỗ (kỳ vọng 2): modal.locator('.report-drill-scroll-top, .report-drill-topscroll') -> modal.locator('.v2-table-scroll__top')
```

Dòng spec bị đổi cụ thể: 315, 589, 591, 604, 708, 1049, 1056, 1081.

### Lưu ý phụ phát hiện khi sửa dòng 1049/1056 (không tự sửa, chỉ ghi nhận)

Biến `barOnOpen` (dòng 1049) và `barAfter` (dòng 1056) được tính (`.count()`) nhưng **KHÔNG có
`expect(...)` nào dùng tới 2 biến này ở bất kỳ đâu trong file** — kiểm bằng `grep -n
"barOnOpen\|barAfter"` chỉ ra đúng 2 dòng khai báo, không có dòng assert. Đây là code chết có sẵn
từ TRƯỚC vòng đổi tên này (không phải lỗi do Task 6 gây ra) — nằm ngoài phạm vi "đổi selector" nên
**không tự thêm/sửa assertion**, chỉ ghi nhận để Task 7 hoặc chủ spec quyết định.

### Kết quả đối chiếu lại — selector KHÔNG tìm thấy nơi định nghĩa

```bash
grep -n "report-drill-content\|report-drill-footer\|report-drill-topscroll\|report-drill-scroll-top" \
  tests/assign/potential-customer-care.spec.ts
```
Output: **rỗng** (exit code 1 — không khớp dòng nào). 4 class nghi vấn đã hết sạch khỏi spec.

Danh sách 22 token `report-drill-*` còn lại trong spec (`grep -oE "report-drill[a-zA-Z0-9_-]*" | sort -u`)
— toàn bộ đã đối chiếu lại với `V2BaseReportModal.vue` / `DemandListModal.vue` ở vòng đầu, không có
gì thay đổi: `report-drill-back`, `report-drill-carry`, `report-drill-count`, `report-drill-customer`,
`report-drill-dialog`, `report-drill-dialog--full`, `report-drill-filters__item` (+ `--search`),
`report-drill-head__btn`, `report-drill-head__object`, `report-drill-head__sub`,
`report-drill-meeting`, `report-drill-project`, `report-drill-sort`, `report-drill-sum__chip`
(+ `--on`, `__n`), `report-drill-sumbox`, `report-drill-table` (+ `__empty`), `report-drill-toggle`,
`report-drill-wrap` — tất cả đều khớp đúng class/id thật trong mã nguồn.

**→ Danh sách selector còn nghi vấn sau vòng sửa 1/5: RỖNG.**

### 2 lệnh kiểm bắt buộc

```bash
grep -c "care-drill" tests/assign/potential-customer-care.spec.ts
```
Output: `0`

```bash
PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test tests/assign/potential-customer-care.spec.ts --list --no-deps 2>&1 | tail -3
```
Output:
```
  [chromium] › assign/potential-customer-care.spec.ts:1602:5 › 28. Bộ lọc chuẩn mới: nhãn floating, ô ngày gộp, popup "Cài đặt bộ lọc" ẩn trường thì xoá giá trị
  [chromium] › assign/potential-customer-care.spec.ts:1686:5 › 29. Popup xem biên bản mở TỪ panel chi tiết phải nằm TRÊN nền mờ của panel
Total: 29 tests in 1 file
```

### Commit

`HRM/e2e` vẫn không phải git repo (đã kiểm lại, không đổi so với vòng đầu) → không có commit nào
được tạo. File đã sửa trực tiếp tại
`HRM/e2e/tests/assign/potential-customer-care.spec.ts`.
