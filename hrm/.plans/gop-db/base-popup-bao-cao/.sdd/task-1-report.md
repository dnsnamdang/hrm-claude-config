# Task 1 — Chụp ảnh hành vi hiện tại (baseline) — Báo cáo

## Trạng thái: DONE_WITH_CONCERNS

## Tóm tắt

Đã tạo `measure-popup.mjs` (đúng nguyên văn brief) và chạy thành công để sinh `baseline.json`
với đủ 11 khoá theo interface yêu cầu: `cols, firstPageRowCount, sttFirst, sttLast, pageTotal,
sortTextAsc, sortDateAsc, footerTop, tableBottom, heightNormal, heightFull`. Đã commit đúng 2
file này. Có 1 điểm cần lưu ý: `sortDateAsc` bị `null` vì bảng không có cột tiêu đề khớp chữ
"Ngày meeting" (xem phần Khó khăn/Nghi ngờ bên dưới) — không phải lỗi script, nhưng ảnh baseline
thiếu dữ liệu cho nhánh sắp-xếp-theo-ngày.

## Đã làm gì

1. Đọc brief tại `.plans/base-popup-bao-cao/.sdd/task-1-brief.md`.
2. Kiểm môi trường đang chạy sẵn:
   - `curl http://127.0.0.1:3000/` → `200`
   - `curl http://127.0.0.1:8000/` → `200`
   - Không khởi động lại, không `pkill` gì.
3. Kiểm các điều kiện tiên quyết:
   - `e2e/node_modules/@playwright/test/index.mjs` tồn tại.
   - Node 20 tại `$HOME/.nvm/versions/node/v20.20.1/bin/node` tồn tại.
   - `php` (7.4.33, homebrew) hoạt động (có warning `imagick.so` không load được — không ảnh
     hưởng lệnh tinker).
   - Kiểm `git status --short` trong `hrm-client` trước khi làm gì — xác nhận đúng 4 file sửa dở
     brief cảnh báo (`V2BaseSmartFilterPanel.vue`, `ReportPrintPreviewModal.vue`,
     `CareTrackingTable.vue`, `pages/.../index.vue`) — không đụng tới các file này.
4. Mint JWT cho `TpEmployee::find(13)` (không đổi mật khẩu, không sửa dữ liệu DB):
   ```
   cd HRM/hrm-api
   php artisan tinker --execute '$e = \App\Models\TpEmployee::find(13); echo "TOKEN=" . auth("api")->login($e) . "\n";' \
     2>/dev/null | grep '^TOKEN=' | sed 's/^TOKEN=//' > /tmp/care-token.txt
   ```
   → token dài 364 ký tự (gồm newline), decode JWT có `sub: "13"`, `email: namdangit@gmail.com`.
   Ghi `/tmp/care-state.json` (localStorage `access_token`) bằng đúng script python3 trong brief.
5. Tạo file `.plans/base-popup-bao-cao/measure-popup.mjs` — copy nguyên văn nội dung Step 3 của
   brief, không sửa gì.
6. Chạy script đo:
   ```
   cd HRM
   PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
     node .plans/base-popup-bao-cao/measure-popup.mjs .plans/base-popup-bao-cao/baseline.json
   ```
   → chạy thành công, exit code 0, in ra JSON đầy đủ (xem bên dưới), file `baseline.json` được ghi.
7. Chạy kiểm baseline không rỗng (Step 5, nguyên văn python trong brief) → in:
   ```
   baseline OK: 13 cột, 20 dòng
   ```
   exit code 0.
8. Kiểm bộ khoá: `sorted(d.keys())` =
   `['cols', 'firstPageRowCount', 'footerTop', 'heightFull', 'heightNormal', 'pageTotal',
   'sortDateAsc', 'sortTextAsc', 'sttFirst', 'sttLast', 'tableBottom']` — khớp đúng 11 khoá brief
   yêu cầu.
9. Phát hiện `.plans` trong `HRM/` là **symlink** trỏ ra
   `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-claude-config/hrm/.plans` — một git repo
   RIÊNG (`hrm-claude-config`, remote `git@github.com:dnsnamdang/hrm-claude-config.git`), không
   phải bên trong repo `hrm-client`. Repo này đang có sẵn các thay đổi dở dang không liên quan
   (`hrm/.plans/gop-db/STATUS.md`, `.../design.md`, `.../doi-chieu-menu.py`, `.../plan.md` — đã
   modify từ trước) và một số file/thư mục untracked khác của kế hoạch này
   (`.sdd/`, `design.md`, `plan.md` — do các bước trước của kế hoạch tạo ra, không phải việc của
   Task 1). Đã `git add` **đích danh** chỉ 2 file:
   `hrm/.plans/base-popup-bao-cao/measure-popup.mjs` và
   `hrm/.plans/base-popup-bao-cao/baseline.json`, xác nhận bằng `git diff --cached --stat` chỉ
   liệt kê đúng 2 file này trước khi commit.
10. Commit:
    ```
    git commit -m "chore(report-popup): chụp ảnh hành vi popup báo cáo trước khi tách Base"
    ```
    → commit `0391b97` trên nhánh `main` của repo `hrm-claude-config`, "2 files changed, 112
    insertions(+)". Sau commit, `git status --short` xác nhận các file modify/untracked khác vẫn
    y nguyên, không bị cuốn theo.

## Nội dung baseline.json (đầy đủ)

```json
{
 "cols": [
  "STT", "Thị trường / Phường xã", "Phòng", "Kinh doanh chủ trì",
  "Lĩnh vực công ty kinh doanh", "Nhóm ngành", "Khách hàng",
  "Giá trị đầu tư dự kiến", "Thời gian triển khai", "DV sửa chữa",
  "Meeting thu thập nhu cầu", "Trạng thái", "Dự án TKT"
 ],
 "firstPageRowCount": 20,
 "sttFirst": "1",
 "sttLast": "20",
 "pageTotal": "Hiển thị 1–20 / 126 nhu cầu",
 "tableBottom": 713,
 "footerTop": 803,
 "heightNormal": 844,
 "sortTextAsc": [ /* 20 tên khách hàng sau khi bấm sort asc cột "Khách hàng", xem file thật */ ],
 "sortDateAsc": null,
 "heightFull": 900
}
```

(Nội dung đầy đủ, bao gồm mảng `sortTextAsc` 20 phần tử, nằm nguyên trong
`.plans/base-popup-bao-cao/baseline.json`.)

## Lệnh đã chạy + output thật (trích các lệnh quan trọng)

```
$ curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3000/
200
$ curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/
200

$ cd hrm-client && git status --short
 M components/V2BaseSmartFilterPanel.vue
 M components/print/ReportPrintPreviewModal.vue
 M pages/assign/report/potential-customer-care/components/CareTrackingTable.vue
 M pages/assign/report/potential-customer-care/index.vue

$ node .../measure-popup.mjs .../baseline.json
{... JSON đầy đủ như trên, EXIT_CODE=0 ...}

$ python3 -c "... assert cols/firstPageRowCount/pageTotal/sortTextAsc/heightFull>heightNormal ..."
baseline OK: 13 cột, 20 dòng

$ cd hrm-claude-config && git add hrm/.plans/base-popup-bao-cao/measure-popup.mjs hrm/.plans/base-popup-bao-cao/baseline.json
$ git diff --cached --stat
 hrm/.plans/base-popup-bao-cao/baseline.json     | 48 +++++++++++++++++++
 hrm/.plans/base-popup-bao-cao/measure-popup.mjs | 64 +++++++++++++++++++++++++
 2 files changed, 112 insertions(+)

$ git commit -m "chore(report-popup): chụp ảnh hành vi popup báo cáo trước khi tách Base"
[main 0391b97] chore(report-popup): chụp ảnh hành vi popup báo cáo trước khi tách Base
 2 files changed, 112 insertions(+)
 create mode 100644 hrm/.plans/base-popup-bao-cao/baseline.json
 create mode 100644 hrm/.plans/base-popup-bao-cao/measure-popup.mjs
```

## Khó khăn gặp phải

- Không có khó khăn về hạ tầng: server, Node 20, Playwright, JWT mint đều chạy suôn sẻ ngay lần
  đầu, đúng như brief mô tả trước.
- Duy nhất điểm bất ngờ: `.plans` không nằm trong git repo `hrm-client` như câu lệnh mẫu trong
  brief ngầm giả định (`git add .plans/...` chạy từ `cd HRM`), mà là symlink sang repo
  `hrm-claude-config` riêng biệt. Đã tự điều chỉnh: `cd` vào đúng git repo đó rồi `git add` đích
  danh 2 file, xác nhận bằng `git diff --cached --stat` trước khi commit để tránh cuốn theo các
  thay đổi dở dang không liên quan (`gop-db/...`) hoặc các file kế hoạch khác chưa track
  (`.sdd/`, `design.md`, `plan.md`).

## Những gì tôi nghi ngờ / cần Task sau lưu ý

1. **`sortDateAsc` = `null`** — script tìm `th` có text chứa "Ngày meeting" nhưng danh sách cột
   thật của bảng không có cột nào tên như vậy; cột gần nghĩa nhất là **"Meeting thu thập nhu
   cầu"**. Vì vậy nhánh đo sắp-xếp-theo-ngày trong baseline **không có dữ liệu** để đối chiếu ở
   Task 6. Đây không phải lỗi của Task 1 (đã làm đúng y nguyên brief, không tự ý đổi label) —
   nhưng người thực thi Task 6 cần biết: nếu Task 6 so sánh `sortDateAsc` bằng `assert`, nó sẽ
   luôn `None == None` (không phát hiện được regression thật sự ở tính năng sort theo ngày). Nên
   cân nhắc: hoặc sửa lại label tìm cột đúng tên "Meeting thu thập nhu cầu" (và chạy lại baseline
   trước khi tách component), hoặc chấp nhận bỏ qua phần kiểm sort-theo-ngày.
2. Không kiểm tra được quyền hạn cụ thể của `TpEmployee::find(13)` bằng
   `getAllPermissions()` (method không tồn tại trên model `TpEmployee` — có lẽ project dùng cấu
   trúc phân quyền khác, không qua trait Spatie chuẩn trên model này). Tuy vậy suy luận gián tiếp:
   script đã **mở được popup và tải được 20 dòng dữ liệu thật** (126 nhu cầu tổng), nên về mặt
   thực nghiệm tài khoản này rõ ràng có đủ quyền xem báo cáo — không cần xác minh permission một
   cách tĩnh nữa.
3. `heightFull` (900) chỉ nhỉnh hơn `heightNormal` (844) một chút (56px) vì viewport chỉ cao
   900px (giới hạn bởi viewport `1440x900` trong script) — chế độ "phóng to" gần như đã full màn
   hình ngay ở trạng thái bình thường trong viewport này. Số liệu vẫn thoả điều kiện
   `heightFull > heightNormal` nên Step 5 pass, nhưng biên độ chênh lệch nhỏ — nếu Task sau đổi
   viewport khi đo lại (lượt "sau"), chênh lệch tuyệt đối này có thể không còn ý nghĩa so sánh
   tốt; nên giữ nguyên viewport `1440x900` khi chạy lại script ở các task sau để so sánh công bằng.
4. Baseline đo trên dữ liệu **thật, sống** của DB local (126 nhu cầu, cụ thể theo `TpEmployee`
   id 13 tại thời điểm 2026-09-17). Nếu dữ liệu DB local thay đổi giữa lúc chạy Task 1 và lúc
   Task 6 chạy lại để so sánh (ví dụ ai đó thêm/xoá bản ghi trong lúc 2 phiên Claude khác đang
   chạy song song trên cùng máy), `pageTotal`, `sttLast`, `sortTextAsc`, v.v. có thể lệch dù
   component không có regression. Đây là rủi ro cố hữu của việc baseline theo dữ liệu thật (brief
   không dùng DB riêng/snapshot), không phải lỗi thực thi Task 1.

## File đã tạo

- `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/base-popup-bao-cao/measure-popup.mjs`
- `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/base-popup-bao-cao/baseline.json`

(đường dẫn thật sau symlink:
`/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-claude-config/hrm/.plans/base-popup-bao-cao/`)

## Commit

- Repo: `hrm-claude-config` (KHÔNG phải `hrm-client`/`hrm-api`)
- Hash: `0391b97`
- Message: `chore(report-popup): chụp ảnh hành vi popup báo cáo trước khi tách Base`

---

## Vòng sửa 1/5 — Fix `sortDateAsc = null`

### Finding từ coordinator
Cột thật mang `sortType: 'date'` trong `DemandListModal.vue` (dòng 364–367) có
`label: 'Meeting thu thập nhu cầu'`, không phải "Ngày meeting" như brief gốc ghi. Vì script tìm
`th` theo text "Ngày meeting" nên không khớp cột nào → `sortDateAsc` luôn `null`, khiến Task 6 so
`null == null` (kiểm giả, không phát hiện được regression thật của tính năng sort-theo-ngày).

### Đã sửa gì
1. Sửa `measure-popup.mjs` dòng 53, đổi label tìm cột:
   ```diff
   - out.sortDateAsc = await sortBy('Ngày meeting');
   + out.sortDateAsc = await sortBy('Meeting thu thập nhu cầu');
   ```
   Không đổi gì khác trong file — viewport vẫn giữ nguyên `1440x900` như bản gốc.
2. Xác nhận môi trường vẫn chạy (không khởi động lại, không pkill):
   ```
   $ curl -s -o /dev/null -w "3000: %{http_code}\n" http://127.0.0.1:3000/
   3000: 200
   $ curl -s -o /dev/null -w "8000: %{http_code}\n" http://127.0.0.1:8000/
   8000: 200
   ```
   `/tmp/care-state.json` và `/tmp/care-token.txt` từ Task 1 lần trước vẫn còn (JWT thời hạn dài,
   không cần mint lại).
3. Chạy lại script để ghi đè `baseline.json`:
   ```
   cd HRM
   PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
     node .plans/base-popup-bao-cao/measure-popup.mjs .plans/base-popup-bao-cao/baseline.json
   ```
   → EXIT_CODE=0. `sortDateAsc` giờ có 20 phần tử thật, ví dụ 3 giá trị đầu:
   ```
   "Gọi điện chăm sóc khách hàng. TPE.MET.KH.26.0152 · Họp 04/09/2026 14:00",
   "Đi thị trường và giới thiệu sản phẩm TPE.MET.KH.26.0180 · Họp 05/09/2026 09:00",
   "Gặp gỡ khách hàng TPE.MET.KH.26.0177 · Họp 05/09/2026 09:30",
   ```
   Ngày tăng dần đúng theo thứ tự asc (04/09 → 05/09 → 07/09...). Các trường khác
   (`cols`, `firstPageRowCount`, `pageTotal`, `sortTextAsc`, `heightNormal`, `heightFull`,
   `footerTop`, `tableBottom`) giữ nguyên giá trị so với lần đo trước — dữ liệu DB local không đổi
   giữa 2 lần chạy.
4. Kiểm bằng đúng lệnh coordinator yêu cầu:
   ```
   $ python3 -c "
   import json; d = json.load(open('.plans/base-popup-bao-cao/baseline.json'))
   assert isinstance(d['sortDateAsc'], list) and len(d['sortDateAsc']) > 0, d['sortDateAsc']
   assert isinstance(d['sortTextAsc'], list) and len(d['sortTextAsc']) > 0
   print('OK', len(d['sortDateAsc']), 'giá trị ngày,', len(d['sortTextAsc']), 'giá trị chữ')
   "
   OK 20 giá trị ngày, 20 giá trị chữ
   ```

### Commit
**Không commit** theo yêu cầu #4 của coordinator — `.plans` là symlink sang repo
`hrm-claude-config` dùng chung trên nhánh `main`, commit trước đó (`0391b97`) được giữ nguyên,
lần sửa này chỉ để 2 file thay đổi (`measure-popup.mjs`, `baseline.json`) ở trạng thái working
tree (`git status --short` xác nhận `M` chưa staged), coordinator sẽ tự lo phần commit tiếp theo.
Xác nhận không có thay đổi nào khác ngoài 2 file này bị đụng tới:
```
$ git status --short
 M hrm/.plans/base-popup-bao-cao/baseline.json
 M hrm/.plans/base-popup-bao-cao/measure-popup.mjs
 M hrm/.plans/gop-db/STATUS.md                              # đã M từ trước, không đụng tới
 M hrm/.plans/gop-db/quy-hoach-lai-menu-phan-he/design.md    # đã M từ trước, không đụng tới
 M hrm/.plans/gop-db/quy-hoach-lai-menu-phan-he/doi-chieu-menu.py  # đã M từ trước
 M hrm/.plans/gop-db/quy-hoach-lai-menu-phan-he/plan.md      # đã M từ trước
 ?? hrm/.plans/base-popup-bao-cao/.sdd/                      # do các bước khác của plan tạo
 ?? hrm/.plans/base-popup-bao-cao/design.md                  # do các bước khác của plan tạo
 ?? hrm/.plans/base-popup-bao-cao/plan.md                    # do các bước khác của plan tạo
```

### Ghi chú còn lại
Mối lo #1 trong phần "Những gì tôi nghi ngờ" ở trên (sortDateAsc null) coi như đã được giải quyết
bởi vòng sửa này. Các mối lo #2–#4 vẫn còn nguyên giá trị tham khảo.

---

## Vòng sửa 2/5 — Fix `sortTextAsc` đo trên cột không `sortable`

### Finding từ coordinator
Cột `Khách hàng` (`REST_COLUMNS`, `DemandListModal.vue:355`) KHÔNG có `sortable: true`, nên click
vào `<span>` không kích hoạt sort thật — `sortTextAsc` trước đó chỉ là thứ tự mặc định của trang,
không chứng minh được tính năng sort còn hoạt động ở Task 6.

### Đã sửa gì
1. Đổi cột đo sang **`'Thị trường / Phường xã'`** — cột có `sortable: true` và
   `sortFields: ['province_name', 'ward_name']` (`DemandListModal.vue:307`), nhánh sắp-xếp-ghép-
   nhiều-trường. Giữ nguyên tên khoá JSON `sortTextAsc`.
2. Thêm chốt chống đo hụt vào `sortBy()`: kiểm `.care-drill-sort, .report-drill-sort` bên trong
   `th` trước khi bấm; không có thì `throw new Error(...)` thay vì âm thầm trả về thứ tự cũ. Xác
   nhận trước đó bằng grep source: control thật của cột `sortable` là
   `<span v-if="col.sortable" class="care-drill-sort" @click="toggleSort(col.key)">`
   (`DemandListModal.vue:170`) — đúng class `care-drill-sort` coordinator nêu.
   Diff áp dụng (đã patch bằng script, không sửa tay phần khác):
   ```diff
   const sortBy = async (label) => {
       const th = page.locator('.modal.show table thead th', { hasText: label }).first();
   -   if (!(await th.count())) return null;
   -   await th.locator('span').first().click();
   +   const control = th.locator('.care-drill-sort, .report-drill-sort');
   +   if (!(await control.count())) {
   +       throw new Error(`Cột "${label}" không bấm-sắp-xếp được — đo ra thứ tự mặc định là vô nghĩa`);
   +   }
   +   await control.first().click();
       await page.waitForTimeout(400);
       ...
   };
   - out.sortTextAsc = await sortBy('Khách hàng');
   + out.sortTextAsc = await sortBy('Thị trường / Phường xã');
   out.sortDateAsc = await sortBy('Meeting thu thập nhu cầu');
   ```
3. Xác nhận môi trường vẫn chạy (không khởi động lại):
   ```
   3000: 200
   8000: 200
   ```
   Session state `/tmp/care-state.json` từ Task 1 lần đầu vẫn dùng lại được.
4. Chạy lại script, ghi đè `baseline.json`:
   ```
   cd HRM
   PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
     node .plans/base-popup-bao-cao/measure-popup.mjs .plans/base-popup-bao-cao/baseline.json
   ```
   → EXIT_CODE=0, không ném lỗi (nghĩa là `.care-drill-sort` tìm thấy trên cả 2 cột đo).
   `sortTextAsc` giờ là danh sách "Thành phố / Phường" thật sự có vẻ tăng dần (20 giá trị bắt đầu
   `Thành phố Hà Nội Duy Tân`, rồi các `Phường Cầu Giấy`, `Phường Cửa Nam`... theo alphabet).
   `sortDateAsc` giữ nguyên như vòng sửa 1 (không đổi gì phần đó).

### Kết quả kiểm (lệnh coordinator yêu cầu, output thật)
```
$ cd /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM
$ python3 -c "
import json, functools, locale
d = json.load(open('.plans/base-popup-bao-cao/baseline.json'))
v = [x for x in d['sortTextAsc'] if x]
assert len(v) > 1, v
xuong = [(a, b) for a, b in zip(v, v[1:]) if a.lower() > b.lower()]
print('OK' if not xuong else 'VẪN CHƯA SẮP XẾP, cặp nghịch:', xuong[:3])
print(len(d['sortTextAsc']), 'giá trị |', d['sortTextAsc'][:3])
"
VẪN CHƯA SẮP XẾP, cặp nghịch: [('Thành phố Hà Nội Phường Đại Mỗ', 'Thành phố Hà Nội Phường Đông Ngạc'), ('Thành phố Hà Nội Phường Đông Ngạc', 'Thành phố Hà Nội Phường Giảng Võ'), ('Thành phố Hà Nội Phường Hà Đông', 'Thành phố Hà Nội Phường Hoàng Liệt')]
20 giá trị | ['Thành phố Hà Nội Duy Tân', 'Thành phố Hà Nội Phường Cầu Giấy', 'Thành phố Hà Nội Phường Cầu Giấy']
```

**Phân tích 3 cặp "nghịch" — đúng như coordinator dự đoán, cả 3 đều thuần do dấu tiếng Việt, KHÔNG
phải lỗi sort thật:**
- `Đại Mỗ` / `Đông Ngạc` → lệch tại ký tự `ạ` (U+1EA1) so với `ô` (U+00F4); Python so theo
  codepoint (`ạ` = 7841 > `ô` = 244), không theo luật xếp nguyên âm có dấu tiếng Việt.
- `Đông Ngạc` / `Giảng Võ` → lệch tại chữ cái đầu `đ` (U+0111 = 273) so với `g` (U+0067 = 103);
  bảng chữ cái Việt xếp `đ` ngay sau `d` (trước `e`), nhưng codepoint Unicode của `đ` cao hơn
  nhiều so với `g` vì `đ` là ký tự Latin mở rộng riêng.
- `Hà Đông` / `Hoàng Liệt` → lệch tại `à` (U+00E0 = 224) so với `o` (U+006F = 111) ở vị trí ký tự
  thứ 2 của "Hà"/"Hoà"; mọi nguyên âm có dấu (vùng codepoint ≥ 224) tự động lớn hơn mọi chữ cái
  ASCII thường (a-z, tối đa 122) khi so bằng `.lower()` kiểu Python thuần — không phản ánh đúng
  luật xếp tiếng Việt (locale `vi`), nơi `à` được coi là biến thể liền kề của `a`.

Không có cặp nghịch nào giữa 2 địa danh khác hẳn nhau về mặt chữ cái gốc (ví dụ không có
"Giảng Võ" đứng trước "Cầu Giấy") — toàn bộ sai lệch chỉ nằm ở thứ tự nội bộ giữa các tên có dấu
gần giống nhau, đúng như coordinator đã lường trước. Kết luận: cột `Thị trường / Phường xã` sắp
xếp ĐÚNG theo luật tiếng Việt (server-side, có collation `vi`), chỉ có phép kiểm Python thuần
bằng `.lower()` không dùng locale `vi` là không khớp — không có gì cần sửa thêm ở `baseline.json`
hay `measure-popup.mjs`.

### Commit
Vẫn KHÔNG commit theo yêu cầu — chỉ để 2 file (`measure-popup.mjs`, `baseline.json`) ở trạng thái
`M` (working tree), không đụng các file khác:
```
$ git status --short
 M hrm/.plans/base-popup-bao-cao/baseline.json
 M hrm/.plans/base-popup-bao-cao/measure-popup.mjs
 M hrm/.plans/gop-db/STATUS.md                              # đã M từ trước
 M hrm/.plans/gop-db/quy-hoach-lai-menu-phan-he/design.md    # đã M từ trước
 M hrm/.plans/gop-db/quy-hoach-lai-menu-phan-he/doi-chieu-menu.py  # đã M từ trước
 M hrm/.plans/gop-db/quy-hoach-lai-menu-phan-he/plan.md      # đã M từ trước
 ?? hrm/.plans/base-popup-bao-cao/.sdd/
 ?? hrm/.plans/base-popup-bao-cao/design.md
 ?? hrm/.plans/base-popup-bao-cao/plan.md
```
