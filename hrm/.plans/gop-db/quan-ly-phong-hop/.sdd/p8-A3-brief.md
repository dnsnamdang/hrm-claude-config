# Brief — Phase 8 / lượt A3 (task T118–T120): FE theo kịp "nhiều người phụ trách phòng"

Repo **`hrm-client`** (Nuxt 2 / Vue 2 / Bootstrap-Vue), thư mục
`/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/hrm-client`, nhánh `gop_db`.
**Chỉ sửa `hrm-client`. KHÔNG đụng `hrm-api`** (BE đã xong và đã review).

## Hợp đồng API mới (BE đã chốt, cứ tin và bám theo)

`meeting_rooms.manager_employee_id` (1 người) **đã bị xoá khỏi DB**, thay bằng bảng nối nhiều người.
API phòng họp nay trả:

| Trường | Kiểu | Dùng ở đâu |
|---|---|---|
| `manager_employee_ids` | mảng id | tô lại select nhiều người ở form Sửa |
| `manager_names` | mảng tên | hiện "2 tên đầu + +N" ở bảng |
| `manager_name` | chuỗi ghép `"; "` | chỗ nào chỉ cần 1 dòng text (export, panel phụ) |

Payload **Lưu phòng** nay gửi `manager_employee_ids` (MẢNG id) và **bắt buộc ≥ 1 phần tử** — BE trả
**422** nếu thiếu. Trường cũ `manager_employee_id` không còn được nhận.

## Việc phải làm

### T118 — `pages/meeting/rooms/components/MeetingRoomModal.vue`

1. Ô "Người quản lý" (~dòng 76-86) đổi thành **chọn nhiều người**, **bắt buộc** (dấu `*` trên nhãn,
   lỗi hiện inline dưới ô theo đúng cách các ô khác của form này đang làm).
2. `data.manager_employee_id` (~235) → `data.manager_employee_ids: []`.
3. `loadData()` (~479-486) đọc `detail.manager_employee_ids` + `detail.manager_names`.
4. Payload lưu (~526) gửi `manager_employee_ids: this.data.manager_employee_ids`.
5. **GIỮ NGUYÊN cơ chế vá option cho người đã nghỉ việc** (~277-323): hiện tại nếu người quản lý
   không còn trong `$store.state.employees` thì màn Sửa sẽ hiện select TRỐNG dù dữ liệu vẫn còn, lưu
   lại là **mất người quản lý**. Code cũ vá bằng cách nhét 1 option dựng từ `manager_name` mà API trả
   kèm. Nay phải vá cho **TỪNG người** trong `manager_employee_ids` mà store không có, dùng tên tương
   ứng theo **cùng chỉ số** trong `manager_names`. Đọc kỹ comment ở đoạn đó trước khi sửa — đây là
   bẫy đã dính một lần rồi.
6. Component: dùng đúng component select của dự án (`V2BaseSelectInModal` vì đây là select **trong
   modal**). Đọc một màn khác đang chọn NHIỀU nhân viên để copy đúng cách khai `multiple`, đừng tự
   chế. Nhãn nhân viên phải theo khuôn dùng chung `Tên - Mã phòng - Mã nhân viên`
   (`utils/employeeOptionText.js`) nếu màn này đang dùng khuôn đó — kiểm trước, đừng tự ghép chuỗi.

### T119 — `pages/meeting/rooms/index.vue`

1. Cột "Người quản lý" (~151-152, key `manager_name`): hiện **2 tên đầu + "+N"** khi có nhiều hơn 2,
   thuộc tính `title` chứa **đủ** danh sách tên ngăn bằng `, `. Nguồn dữ liệu: `item.manager_names`
   (mảng); nếu mảng rỗng thì ô để trống, **không in chữ "Chưa có"**.
2. Chữ trong ô để **thường** (`font-weight: 400`), không in đậm — class `.field-line` sẵn có đã đúng.
3. Map import (~1032) `manager_name: String(row.ManagerName || '')` — giữ nguyên tên cột Excel
   `ManagerName`, BE nay hiểu **nhiều tên ngăn bằng dấu `;`**. Nếu màn có dòng mô tả/hướng dẫn cột
   import thì bổ sung ý "nhiều người ngăn bằng dấu `;`".
4. Kiểm cả `{ id: 'manager_name', name: 'Người quản lý' }` (~427) và khai cột (~565) còn khớp không.

### T120 — `pages/meeting/bookings/components/BookingFormModal.vue`

Panel phải (~464-466) và câu gợi ý gửi duyệt (~1925) đang đọc `selectedRoomInfo.manager_name`.
BE **vẫn trả `manager_name`** (nay là chuỗi ghép nhiều tên bằng `"; "`) nên 2 chỗ này có thể đã chạy
đúng. **Kiểm thật rồi mới kết luận** — đọc Resource `BookableMeetingRoomResource.php` bên `hrm-api`
(chỉ ĐỌC, không sửa) để chắc khoá đúng; nếu đã đúng thì ghi rõ trong báo cáo là "không phải sửa", chỉ
chỉnh nhãn nếu đang ghi số ít ("Người phụ trách") mà thực tế có thể nhiều người.

## Ràng buộc bắt buộc

- Mọi element form là `V2Base*`; select trong modal là `V2BaseSelectInModal`. Không viết HTML thô
  (`<input>`, `<select>`, `<button>`, `class="form-control"`).
- Nút trong cùng cụm khai `class="mr-2 mb-2"`, nút cuối cụm `mb-2`.
- **`.text-muted` trong dự án này bị SCSS toàn cục ép thành MÀU ĐỎ** — dòng phụ/ghi chú dùng
  `#6b7280`, đừng dùng `.text-muted`.
- Cờ quyền khởi tạo `false`, không hard-code `true`.
- **KHÔNG `git commit`/`push`/`stash`.** Không đụng `hrm-api`. Không tạo subagent, không tự gọi
  reviewer.
- **KHÔNG tự mở trình duyệt / không dùng Playwright** — việc đo trên trình duyệt thật do người điều
  phối làm sau, và chỉ có 1 trình duyệt dùng chung.

## Cách tự kiểm (ghi kết quả thật vào báo cáo)

1. `grep -rn "manager_employee_id\b" pages components | grep -v manager_employee_ids` → phải RỖNG
   (không còn chỗ nào dùng trường số ít cũ).
2. `grep -rn '<input \|<textarea\|<select \|<button \|class="btn \|class="form-control' pages/meeting/rooms | grep -v V2Base`
   → phải RỖNG (không HTML thô).
3. Đọc lại đoạn vá option người đã nghỉ việc và **giải thích trong báo cáo** bằng lời: với phòng có 2
   người quản lý mà 1 người đã nghỉ, luồng của bạn hiện ra những gì và lưu lại thì gửi đi những id nào.
4. Nếu dự án có lint (`npm run lint` hoặc eslint) thì chạy cho 3 file đã sửa và dán kết quả; không có
   thì nói rõ là không có.

## Báo cáo

Ghi đầy đủ vào `.plans/gop-db/quan-ly-phong-hop/.sdd/p8-A3-report.md`: từng task, kết quả 4 mục tự
kiểm, danh sách file sửa, những chỗ bạn phải tự quyết, và **những gì người điều phối cần đo lại trên
trình duyệt** (liệt kê cụ thể: mở màn nào, bấm gì, đo số gì).
Trả về chat ngắn gọn: trạng thái, file đã sửa, điểm nghi ngờ.
