# Báo cáo kế hoạch làm việc của nhân viên — Mockup UI

File mockup: **`bao-cao-ke-hoach-lam-viec-nhan-vien.html`** (standalone, không phụ thuộc thư viện ngoài).

## Mục tiêu

Theo dõi **khối lượng công việc** của các Phòng ban / Bộ phận / Nhân viên theo thời gian, gom từ
**5 nguồn** đang nằm rải rác ở 5 màn danh sách khác nhau: Lịch meeting, Công việc (task),
Vấn đề (issue), Phiếu giao công tác, Phiếu giao việc tại Công ty.

Câu hỏi màn này trả lời: *ai đang ôm nhiều việc, ai đang rảnh, phần việc đó xong tới đâu.*

## Bối cảnh

- **Style tham khảo**: `../../bao-cao-phat-trien-thi-truong-khach-hang/bao-cao-phat-trien-thi-truong-khach-hang.html`.
  Port **NGUYÊN KHỐI** `<style>` của màn đó (design tokens navy + teal, `.market-toolbar`, `.rsum-*`,
  `.minutes-modal`, `.ticket-drawer`, `#print-area`); phần riêng của màn này nằm ở **CUỐI** khối style
  dưới nhãn *"BỔ SUNG RIÊNG MÀN KẾ HOẠCH LÀM VIỆC"*.
- Đã có 2 báo cáo họ hàng, màn này **KHÔNG** thay thế cái nào:
  - `/assign/report/meeting-by-employees` — chỉ meeting.
  - `/assign/report/task-manager-by-employees` — chỉ task, dạng Gantt phân bổ nguồn lực theo giờ.
  Màn mới là góc nhìn **tổng khối lượng đa nguồn**, đếm đầu việc chứ không đếm giờ.

## Cấu trúc cây theo dõi

```
Phòng ban ▸ Bộ phận (chỉ khi phòng CÓ chia bộ phận) ▸ Nhân viên
```

- Phòng không chia bộ phận thì nhảy thẳng **Phòng ban ▸ Nhân viên** — KHÔNG đẻ dòng
  "Chưa phân bộ phận" rỗng (luật đã chốt ở màn phát triển thị trường).
- **Công ty là Ô LỌC, không phải cấp cây.**
- Bảng có đúng **1 dòng `TỔNG`** trên cùng, mang tổng cả kỳ.

## Bộ cột bảng theo dõi (10 cột)

`STT · Nội dung theo dõi · Meeting · Task · Issue · P. công tác · P. giao việc · Tổng · Đã HT · Tỷ lệ HT`

- `Tổng` = cộng ngang 5 cột loại. `Tỷ lệ HT` = `Đã HT / Tổng`.
- Tiêu đề cột **viết hoa chữ đầu** (bỏ `text-transform: uppercase`) và **KHÔNG xuống dòng**
  (`white-space: nowrap`) — áp cho **CẢ bảng theo dõi chính LẪN bảng trong popup**, dùng chung bộ
  thông số (`none` / `12px` / `letter-spacing: 0`) để 2 bảng không lệch nhau.
- Mọi số trong ô là **link** mở popup chi tiết.

## Định nghĩa 5 nguồn (bám dữ liệu thật trong repo)

| Cột | Bảng | Khoảng thời gian (overlap) | Người được tính | "Đã HT" | "Quá hạn" |
|---|---|---|---|---|---|
| Meeting | `meetings` | ngày họp (1 điểm) | chủ trì + mọi thành viên dự (`meeting_employees`) | status `3` Hoàn thành | ngày họp đã qua mà chưa hoàn thành |
| Task | `tasks` | `start_date` → `due_date` | `assignee_id` (= chủ trì) | status `8` Done | `due_date` < TODAY, chưa HT, chưa huỷ |
| Issue | `issues` | `detected_at` → `due_date` | `assignee_id` (= chủ trì) | status ∈ {`resolved`, `completed`, `closed`} | `due_date` < TODAY, chưa HT, chưa huỷ |
| P. công tác | `assign_business` | `from_time` → `to_time` | mọi NV trong đoàn (`assign_business_employees`); trưởng nhóm = chủ trì | status ∈ {`7`,`8`,`9`} (đã duyệt kết quả trở đi) | `to_time` đã qua mà chưa duyệt kết quả |
| P. giao việc | `assign_jobs` | `time_start_request` → `deadline` | NV thực hiện; người lập = chủ trì | status `6` Đã duyệt kết quả | `deadline` < TODAY, chưa HT, chưa huỷ |

**Luật TÌNH TRẠNG dùng CHUNG cho cả 5 loại** (hàm `bucketOf`), không viết riêng từng loại:
`huỷ/từ chối` → `hoàn thành` → `quá hạn` (ngày kết thúc đã qua mà chưa xong) → `đang thực hiện`.
Nhóm Huỷ/Từ chối: Meeting `4` · Task `7`,`9`,`10` · Issue `rejected` · P.công tác `6` · P.giao việc `4`.

Bảng mã trạng thái gốc (đọc từ Entity, để lần sau không phải tra lại):

- `Meeting`: `0` Đang tạo · `1` Lên lịch · `2` Chốt lịch · `3` Hoàn thành · `4` Huỷ
- `Task`: `1` Nháp · `2` Chờ duyệt · `3` Todo · `4` Đang làm · `5` Tạm dừng · `6` Review · `7` Từ chối · `8` Done · `9` Huỷ · `10` Từ chối bắt đầu
- `Issue`: `new` · `assigned` · `in_progress` · `resolved` · `closed` · `reopened` · `completed` · `rejected`
- `AssignJob`: `1` Đang tạo · `2` Chờ duyệt · `3` Đã duyệt · `4` Từ chối · `5` Đã nhập kết quả · `6` Đã duyệt kết quả
- `AssignBusiness`: `1` Đang tạo · `2` Chờ duyệt · `3` Đã duyệt · `5` Chờ duyệt kết quả · `6` Không duyệt · `7` Đã duyệt kết quả · `8`/`9` hồ sơ thanh toán

## Quyết định đã chốt (2026-09-07)

1. **Mốc thời gian = GIAO NHAU với kỳ (overlap)**, không phải ngày tạo cũng không phải ngày bắt đầu.
   Bản ghi nào có khoảng thời gian chạm vào kỳ đều được tính.
   - ⚠️ Hệ quả: 1 bản ghi kéo dài qua nhiều kỳ **bị đếm ở mọi kỳ nó chạm** ⇒ cộng 12 tháng > số cả năm.
     Phải có chú thích ngay dưới bảng, không để user tưởng lệch số.
   - Trong CÙNG 1 lần chạy báo cáo thì vẫn cộng dồn theo cấp bình thường: dòng cha = tổng dòng con.
2. **Gán khối lượng cho MỌI người tham gia**, không chỉ người chủ trì.
   - Đếm theo cặp `(bản ghi × người)` ⇒ dòng phòng ban vẫn = tổng dòng con.
   - 1 meeting có 3 người dự thì toàn công ty đếm 3 — đúng nghĩa "khối lượng thời gian NV bỏ ra",
     KHÔNG phải "số chứng từ".
   - Popup chi tiết có cột **Vai trò** (`Chủ trì` / `Tham gia`); checkbox **"Chỉ tính việc chủ trì"**
     đổi góc nhìn của **cả bảng chính** sang cách đếm 1 bản ghi = 1 người.
3. **Nháp và Huỷ/Từ chối ĐỀU TÍNH vào Tổng.** Không lọc bỏ trạng thái nào.
   - Hệ quả: `Đang thực hiện` **không** còn là `Tổng − HT − Quá hạn` (sẽ nuốt luôn phần huỷ).
     Phải tách thành **4 nhóm chia hết Tổng**: `Đã hoàn thành` + `Đang thực hiện` + `Quá hạn` + `Huỷ/Từ chối`.
   - Bản đã huỷ/từ chối **KHÔNG** bị tính là quá hạn (đã dừng thì không còn hạn để trễ).
   - Nhóm Huỷ/Từ chối: Meeting `4` · Task `7`,`9`,`10` · Issue `rejected` · P.công tác `6` · P.giao việc `4`.
4. **Không có ô "Bình quân/người"** — user yêu cầu bỏ (2026-09-07). Khối "Khối lượng trong kỳ" còn 2 ô.
5. **Công ty là ô lọc, KHÔNG phải cấp cây.** Cây bắt đầu từ Phòng ban.

## Dải tổng hợp

Giữ khuôn **2 khối nằm CÙNG 1 HÀNG, ô con xếp NGANG** của màn phát triển thị trường (đã nén tối đa).
**KHÔNG có khối KPI.** Header khối không mang số to (số đã nằm ở ô con, tránh lặp).

| Khối | Ô con |
|---|---|
| Khối lượng trong kỳ | Tổng đầu việc · Nhân viên có việc |
| Trạng thái xử lý | Đã hoàn thành · Đang thực hiện · Quá hạn · Huỷ/Từ chối |

- 4 ô của khối 2 **chia hết** Tổng đầu việc của khối 1 → tự kiểm được, lệch là biết sai.
- ❌ KHÔNG dùng bản lưới text phẳng kiểu `.type-summary-bar__grid` — user đã chê xấu ở màn trước.
  Giữ ngôn ngữ hộp bo góc / viền trái màu / số to.
- **Dòng meta "Tổng hợp kỳ …" tô cơ cấu 5 loại theo MÀU CHỦ ĐỀ từng loại** (chốt 2026-09-07):
  chấm tròn + tên + số cùng màu, dùng ĐÚNG `WORK_TYPES[].color` — cùng bộ màu với chip "Loại công
  việc" trên thanh lọc và với 5 cột số của bảng, để mắt nối được 3 chỗ với nhau. Hai số đầu dòng
  (`đầu việc`, `nhân viên`) không thuộc loại nào nên giữ màu chữ chính; dấu `·` ngăn cách nằm
  NGOÀI span màu để không bị nhuộm theo loại.
  - ⚠️ Vì vậy phải tách **2 hàm**: `typeBreakdown()` trả CHỮ THUẦN cho `data-tip` (thuộc tính HTML,
    nhét thẻ vào là hỏng tooltip) và cho bản in; `typeBreakdownHtml()` trả HTML có màu, CHỈ dùng ở
    dòng meta hiển thị trên màn.

## Bộ lọc

- **Kỳ**: Tháng này / Quý này / Năm nay / Tuỳ chọn + Từ ngày – Đến ngày. Không có "Tất cả"
  (mọi chỉ tiêu đều tính theo kỳ).
- **Tổ chức (cascade)**: Công ty ▸ Phòng ban ▸ Bộ phận ▸ Nhân viên.
- **Loại công việc** — ô **CHỌN NHIỀU** (chốt 2026-09-07, thay cụm 5 chip toggle của bản đầu), mặc
  định tick hết 5. Bỏ tick loại nào thì **ẩn luôn cột đó** và trừ khỏi `Tổng` / `Đã HT` / dải tổng
  hợp / dòng meta.
  - **KHÔNG dùng `<select multiple>` thuần**: nó bung thành hộp cao nhiều dòng, phá bố cục 1 hàng
    của thanh lọc và không giữ được chấm màu theo loại. Dựng dropdown checkbox bám ĐÚNG thông số
    `.calendar-filter-select` bên cạnh (cao 30px · viền 1px `#cbd5e1` · bo 6px · chữ 12px) để
    không lộ ra là thành phần tự chế.
  - Nhãn trong ô co theo số loại đang chọn: `Tất cả loại` (đủ 5) · ghi thẳng tên khi chọn 1–2 loại
    (lúc đó user cần biết chắc đang xem loại nào) · `Đã chọn N loại` khi 3–4. Luôn kèm chấm màu của
    các loại đang bật.
  - Dòng "Tất cả loại" ở đầu panel dùng trạng thái **indeterminate** khi chọn một phần.
  - Mỗi dòng có **số đầu việc của loại đó theo bộ lọc hiện tại** (bỏ qua chính ô này) → biết trước
    bỏ tick thì mất bao nhiêu.
  - Chưa chọn loại nào → viền ô đỏ + bảng báo *"Chưa bật loại công việc nào…"*.
  - ⚠️ **Panel phải TĨNH khi tick**: chỉ cập nhật nhãn + trạng thái checkbox + số, KHÔNG dựng lại
    `innerHTML`. Dựng lại sẽ thay mới toàn bộ checkbox → mất focus bàn phím và huỷ tham chiếu phần
    tử đang thao tác (cùng lý do khuôn gốc ghi chú *"bộ lọc trong popup để TĨNH, không dựng lại"*).
    Chỉ dựng panel lúc khởi tạo và lúc bấm Xoá lọc.
- **Trạng thái**: Tất cả / Đã hoàn thành / Đang thực hiện / Quá hạn / Huỷ – Từ chối.
- ☑ **Chỉ tính việc chủ trì** — đổi cách đếm của cả màn (xem quyết định 2).
- ☑ **Chỉ hiện NV có việc** — ẩn dòng nhân viên có Tổng = 0 (mặc định BẬT).

## Thanh tiêu đề (đồng bộ mẫu 2026-09-08)

2 nút **In báo cáo · Xuất Excel** dồn về **góc phải thanh tiêu đề navy** (`.topbar__actions`,
`margin-left: auto`), không còn nằm ở toolbar lọc.

- Khuôn gọn: cao **26px**, chữ 12px, nền trong suốt + viền trắng mờ cho hợp nền navy. Nút
  *Xuất Excel* giữ sắc xanh lá để phân biệt với nút *In*.
- **Thanh tiêu đề KHÔNG cao thêm** (vẫn 42px) vì nút thấp hơn khoảng trống sẵn có.
- Toolbar chỉ còn cụm lọc: **118 → 68px**, kéo cả trang lên **51px** (bảng theo dõi từ y=359 lên
  y=308).

## Chọn cấp xem (đồng bộ mẫu 2026-09-08)

Nút *"Ẩn / Hiện chi tiết"* trong ô tiêu đề cột "Nội dung theo dõi" **đã bỏ** — nó chỉ có 2 nấc
(thu hết / bung hết 49 dòng), user cần dừng được ở giữa. Thay bằng **select chọn cấp** đúng chỗ đó:

`Chỉ Phòng ban` · `Đến Bộ phận` · `Tất cả cấp (đến Nhân viên)`

- **Hiểu theo TÊN CẤP, không theo độ sâu** (`applyLevel` xét `dim` của CON): chọn *Đến Bộ phận* thì
  chỉ 4 phòng CÓ bộ phận bung thêm 1 cấp, 6 phòng không chia dừng ở Phòng ban — **không lòi nhân
  viên ra sớm**. Tính theo độ sâu là "cấp 2" sẽ lẫn bộ phận với nhân viên.
- *Tất cả cấp* = cấp sâu nhất nên gộp làm 1 mục, không tách 2 mục trùng nhau.
- Bấm mũi tên từng dòng vẫn tự do — chỉ đổi `state.expanded`, **không** đụng `state.level`, nên
  select giữ nguyên lựa chọn gần nhất.
- Nút *Xoá lọc* đưa cấp về mặc định (`Chỉ Phòng ban`).
- Bản in / Excel **luôn xuất đủ mọi cấp**, không phụ thuộc cấp đang xem trên màn.

## Phân biệt cấp khi bung hết bảng (đồng bộ mẫu 2026-09-08)

Bung *Tất cả cấp* là 49 dòng. Nếu để `.rsum-tb__row--open td` làm **1 rule chung** thì mọi cấp cha
nhận CHUNG một nền, xoá sạch phân tầng màu theo độ sâu. Cách xử lý:

- **Tách nền dòng cha theo TỪNG CẤP**: `d0 #dceaf4` · `d1 #e9f3f9` · `d2 #f2f8fb` (đậm → nhạt).
- **Vạch cấp bên trái ô tên** — nấc thang 22px, đậm → nhạt: `d0` 3px `#0a7c88` tại `left:2px`;
  `d1/d2/d3` 2px với alpha `.55 / .32 / .18` tại `24 / 46 / 68px`. Dựng bằng `::before` tuyệt đối
  chứ KHÔNG dùng `border-left` của `td` — border sẽ nằm ở mép ô, không nằm đúng chỗ thụt lề.
- **Kẻ đậm 2px `#b6d8e0` phía trên mỗi dòng cấp 0** để cắt khối phòng ban.
- Luật `:hover` vẫn thắng nền mới (cụ thể hơn + khai báo sau).

## Luật POPUP chi tiết

Bám nguyên luật đã chốt ở màn phát triển thị trường:

0. **Khối tổng hợp trong popup MẶC ĐỊNH THU GỌN** (đồng bộ mẫu 2026-09-08): 2 khối *KPI* +
   *Phân bổ đầu việc theo cơ cấu* nằm trong `#drill-sumwrap`, phía trên là `.drill-sumhead` mang
   nút thu gọn dùng **chung khuôn `.rsum-toggle`** với khối tổng hợp của màn chính. Mở popup ra là
   thấy ngay danh sách đầu việc (đo được bảng bắt đầu ở y=268 thay vì y=438 — sớm hơn 170px); bấm
   *Xem tổng hợp* mới dựng nội dung 2 khối.
   - `openDrill()` đặt lại `state.drillSumCollapsed = true` **mỗi lần mở**, không mang trạng thái
     từ popup trước sang.
   - Ẩn bằng thuộc tính `hidden` trên lớp bọc, **KHÔNG** dùng `style.display` — `renderDrillSummary`
     có logic tự ẩn khối phân bổ khi không còn chiều nào, đặt display ở đây sẽ đè lên nó.
   - `#drill-sumwrap { display: contents }` để 2 khối con vẫn là flex-item trực tiếp của body popup.
   - Thu gọn thì **xoá luôn nội dung cũ** (`#drill-kpis` / `#drill-summary`): mở popup A có bung
     khối, đóng rồi mở popup B thì DOM ẩn vẫn đang giữ số của A.
   - Nhãn nút: **"Xem tổng hợp"** khi đang thu, **"Thu gọn"** khi đang mở.

1. **Chiều nào đã BỊ CỐ ĐỊNH thì bỏ CẢ CỘT, CẢ Ô LỌC, CẢ CHIP** (chốt 2026-09-07 — bản đầu chỉ bỏ
   ô lọc mà giữ cột, khiến cột lặp đúng 1 giá trị trên mọi dòng, vừa vô nghĩa vừa đẩy cột có ích ra
   ngoài khung). Cấp đã cố định VẪN dùng để thu hẹp cascade của cấp dưới.

   4 nguồn cố định — gom hết trong `drillHiddenDims()`:

   | Nguồn | Ví dụ | Bỏ cột + ô lọc |
   |---|---|---|
   | `path` của node đã bấm | bấm số ở dòng nhân viên | Phòng ban · Bộ phận · Nhân viên |
   | metric là 1 trong 5 **loại** | bấm số ở cột `Meeting` | Loại |
   | metric là 1 trong 4 **trạng thái** | bấm số ở cột `Đã HT` | Trạng thái |
   | cờ "Chỉ tính việc chủ trì" đang bật | — | Vai trò |

   Thêm 2 luật phụ cùng tinh thần:
   - Metric là `task` / `issue` → bỏ cột **Vai trò**: 2 loại này trong DB chỉ có ĐÚNG 1
     `assignee_id`, không có người tham gia nên vai trò luôn là "Chủ trì".
   - Đã cố định 1 phòng ban **không chia bộ phận** → bỏ cột **Bộ phận** (nếu không, cột chỉ toàn
     dấu `—`) — cùng luật với bảng chính.

   ⚠️ **Chỉ ẩn theo CHIỀU BỊ CỐ ĐỊNH, KHÔNG ẩn theo dữ liệu.** Một cột tình cờ chỉ có 1 giá trị vì
   dữ liệu (12 phiếu công tác của phòng đó đều đã hoàn thành) thì vẫn phải giữ — ẩn theo dữ liệu
   làm cột nhảy ra nhảy vào mỗi lần user đổi bộ lọc.

   Hệ quả kỹ thuật: **số cột thay đổi theo từng popup (7 → 12 cột)** nên `min-width` của bảng phải
   khai INLINE theo tổng colgroup hiện tại (`drillTableWidth()`), KHÔNG để số cứng trong CSS. In và
   Xuất Excel của popup cũng phải lấy `drillColumns(key)`, không dùng hằng `DRILL_COLUMNS`.
2. **Tiêu đề nêu rõ đối tượng**: *"Đang xem &lt;chỉ tiêu&gt; theo &lt;Cấp&gt;: &lt;Tên&gt;"*.
   Node nằm sâu thì dòng phụ hiện đường dẫn cấp cha (`Phòng ban: … › Bộ phận: …`), chữ XÁM `#6b7280`,
   không in đậm, **không tô đỏ**.
3. **Chip phân bổ**: Loại công việc + Phòng ban. Ẩn theo cùng luật ẩn của bộ lọc.
4. **Bộ cột (11 cột, thứ tự đã dựng)**: `STT · Loại · Phòng ban · Bộ phận · Nhân viên · Vai trò ·
   Mã/Số phiếu · Tên công việc · Bắt đầu · Kết thúc/Hạn · Trạng thái`.
   - **CHỈ CÓ 1 CỘT TRẠNG THÁI** (chốt 2026-09-07): bỏ cột trạng thái gốc của chứng từ
     (*Hoàn thành · Chờ duyệt · Đã duyệt kết quả…*), cột 4 nhóm theo dõi đổi tên từ "Tình trạng"
     thành **"Trạng thái"**. Popup là màn ĐỌC NHANH, 2 cột trạng thái cạnh nhau gây rối.
     Trạng thái gốc vẫn xem được trong **drawer chi tiết**, ở ô tên là **"Trạng thái chứng từ"**
     để không trùng tên với ô "Trạng thái" (4 nhóm) ngay cạnh.
   - Nhờ bớt 1 cột, tổng colgroup còn **1.362px < 1.366px** khung cuộn ⇒ **popup đầy đủ nhất cũng
     KHÔNG phải cuộn ngang nữa**.
   - Các chiều theo dõi dồn lên ngay sau `Loại`, đúng thứ tự cấp của cây.
   - Cột `Phòng ban` là phòng của **người được tính**, không phải phòng của người chủ trì —
     nên popup theo Kinh doanh 1 vẫn hiện được meeting do phòng khác chủ trì mà NV KD1 có dự.
   - Đây là bộ cột ĐẦY ĐỦ, dùng khi không cố định chiều nào (popup từ dòng `TỔNG` hoặc từ dải tổng
     hợp). Popup cố định càng sâu thì càng ít cột — xem luật 1.
   - `Trạng thái` = 1 trong 4 nhóm (Đã HT / Đang thực hiện / Quá hạn / Huỷ – Từ chối), có badge màu.
   - **MỌI ô thời gian đều NGÀY + GIỜ** (`26/09/2026 17:00`), không trừ loại nào — áp cho cột
     Bắt đầu, cột Kết thúc/Hạn ở popup và cả ô Ngày họp / Bắt đầu / Kết thúc trong drawer
     (chốt 2026-09-07, bản trước còn để Task chỉ có ngày).
   - ⚠️ **NỢ BACKEND**: `tasks.start_date` trong DB là kiểu `date` thuần — bảng `tasks` có
     `due_time` cho hạn hoàn thành nhưng **KHÔNG có `start_time`**. Muốn giờ bắt đầu của Task
     đúng như mockup thì phải **bổ sung cột `start_time` cho bảng `tasks`**, nếu không BE chỉ
     trả về được `00:00`. 4 loại còn lại đã có giờ thật trong DB: meeting (giờ họp) ·
     `issues.detected_at` · `assign_business.from_time` · `assign_jobs.time_start_request`.
   - Khoá sắp xếp của 2 cột này phải **cộng cả giờ**, không chỉ ngày — nếu không, các việc cùng
     ngày sẽ hoà nhau rồi rơi về so theo mã phiếu, nhìn như sắp xếp sai.
5. **3 KPI trong popup**: Tỷ lệ hoàn thành · Tỷ lệ quá hạn · **Tỷ lệ việc chủ trì**.
   KPI thứ 3 KHÔNG dùng "bình quân đầu việc / NV" — user đã chốt bỏ mọi chỉ số bình quân, và
   ở popup mở theo 1 nhân viên thì mẫu số luôn bằng 1 nên chỉ số đó vô nghĩa.
6. **Sắp xếp được ở 7 cột**: Loại · Phòng ban · Bộ phận · Nhân viên · Bắt đầu · Kết thúc/Hạn ·
   Trạng thái (= 4 nhóm). **Icon sort là 2 MŨI TÊN chồng nhau** (đồng bộ mẫu 2026-09-08): cả 2
   luôn hiện mờ `opacity .3` để biết cột nào sắp được kể cả khi chưa bấm, chiều ĐANG áp mới tô đậm.
   Bản cũ 1 mũi tên xoay 180° không cho biết điều đó. (bấm tiêu đề: tăng → giảm; mở popup mới reset về Bắt đầu tăng dần — cột đang sắp có
   thể vừa bị ẩn ở popup khác). **In + Xuất Excel bám đúng thứ tự đang sắp.**
   - **Trạng thái** sắp theo đúng thứ tự khai báo `BUCKETS`: *Đã hoàn thành → Đang thực hiện →
     Quá hạn → Huỷ/Từ chối*, tức theo mức độ cần để mắt tới.
   - **Bộ phận**: nhân viên chưa gán bộ phận (`—`) đẩy xuống CUỐI khi tăng dần, không lẫn vào giữa.
7. **Hàng tiêu đề để CHỮ THƯỜNG** như bảng theo dõi chính (`text-transform: none`, `12px`,
   `letter-spacing: 0`). Khuôn gốc để `uppercase` cho `.drill-table thead th` → phải ghi đè.

## Data demo

- Mốc **`TODAY = 26/09/2026`** — cùng mốc với màn phát triển thị trường, đặt gần cuối kỳ mặc định
  (tháng này) để có đủ việc đã xong / đang làm / quá hạn mà vẫn còn việc chưa tới hạn.
- Sinh cố định bằng **LCG có hạt giống** (KHÔNG `Math.random`) → demo không nhảy số giữa 2 lần mở.
- Danh mục tổ chức **copy nguyên** từ `bao-cao-phat-trien-thi-truong-khach-hang.html` bản
  2026-09-08 (chốt 2026-09-08 — trước đó dùng bộ "Kinh doanh 1…10 / 30 nhân viên" cũ):
  **2 công ty · 10 phòng ban · 2 bộ phận · 43 nhân viên**, tên phòng ban là tên thật của Tân Phát.
  - **CHỈ 1/10 phòng có bộ phận** (`PHÒNG KINH DOANH THƯƠNG MẠI` → 2 BP) — 9 phòng còn lại nhảy
    thẳng Phòng ban ▸ Nhân viên. Vẫn minh hoạ đủ luật *"cấp Bộ phận chỉ hiện với phòng có chia"*,
    thậm chí rõ hơn bộ cũ (4/10 phòng có bộ phận).
  - Bỏ trường `markets` của mẫu — màn này không theo dõi theo thị trường.
- **6 NHÂN VIÊN CHƯA CÓ VIỆC TRONG KỲ** (thêm 2026-09-08 — trước đó mọi NV đều có việc nên ô
  *"Chỉ hiện NV có việc"* bật hay tắt đều như nhau, không thử được):
  - Chọn 6 người **NGAY TRONG danh mục 43 người**, không đẻ thêm người ngoài danh mục:
    `e3` Bùi Hữu Hanh · `e7` Nguyễn Thành Công · `e19` Lương Văn Đạo (thuộc phòng CÓ bộ phận) ·
    `e24` Phạm Phi Tình · `e31` Nguyễn Ngọc Long · `e43` Nguyễn Quốc Lãm.
  - Họ **KHÔNG** nằm trong `ACTIVE_EMPLOYEES` — pool mà bộ sinh chứng từ chính bốc ra.
  - Có **lô chứng từ riêng 5 phiếu/người**, toàn bộ nằm gọn **01/07 – 22/08/2026** (kết thúc TRƯỚC
    kỳ mặc định). Nhờ vậy ở kỳ 09/2026 họ hiện 0 đầu việc, nhưng đổi kỳ sang *Năm nay* thì vẫn có
    việc — **không phải nhân viên ma**. Lô này sinh SAU cùng nên không làm lệch chuỗi ngẫu nhiên.

- Sinh **2.560 chứng từ** trải 150 ngày từ 01/07/2026 (620 meeting · 880 task · 360 issue ·
  300 phiếu công tác · 400 phiếu giao việc), phẳng hoá thành các cặp (chứng từ × người).
- Tổng danh mục: **43 nhân viên** (37 có việc + 6 rảnh trong kỳ).
- Kỳ mặc định 09/2026 ra **1.040 đầu việc**: Meeting 283 · Task 269 · Issue 108 · P.công tác 190 ·
  P.giao việc 190; trạng thái: hoàn thành 530 (51,0%) · đang thực hiện 266 · quá hạn 174 · huỷ 70.

## Ngoài phạm vi (giai đoạn này)

- Chưa port sang Vue (`pages/assign/report/...`), chưa có API BE, chưa responsive.
- Chưa gắn phân quyền theo cấp — mockup hiện toàn bộ cây.

## Gotcha đã gặp khi dựng (đừng vấp lại)

1. **`.rsum-blk__money` để `nowrap`** — nhồi cơ cấu 5 loại vào meta của khối rộng 300px làm nó
   tràn **94px** ra ngoài, bóp cột tiêu đề còn 28px và chữ đè lên nhau. Meta của khối phải NGẮN.
2. **TUYỆT ĐỐI không đặt `overflow: hidden` lên `.rsum-blk__title` / `.rsum-blk__label`** để cắt
   ellipsis: bên trong có icon ⓘ mà tooltip là `::after` định vị absolute rộng 246px → tooltip bị
   cắt mất khi hover. Chỉ cắt ở `.rsum-blk__money` (không chứa tooltip).
3. **Cùng lý do, `scrollWidth > clientWidth` KHÔNG dùng được để kiểm chữ có bị cắt hay không** ở
   các phần tử chứa icon ⓘ — tooltip absolute luôn thổi phồng `scrollWidth`. Muốn đo đúng thì
   dùng `Range.selectNodeContents(textNode).getBoundingClientRect().width`.
4. **Khối 1 của dải tổng hợp cần đúng `flex: 0 0 404px`** — đo được cả header lẫn hàng 2 ô con đều
   cần 382px + padding 20px. Để 300px thì cả tiêu đề lẫn 2 ô con đều bị bóp.
5. **Meeting KHÔNG có % tiến độ** — kết quả của nó là biên bản. Drawer phải đổi ô "Tiến độ" thành
   "Biên bản họp" khi `type = meeting`.
   Drawer của meeting cũng đổi ô thứ 2 từ "Giờ họp" thành **"Kết thúc"** — khi ô "Ngày họp" đã
   mang cả giờ thì để "Giờ họp" bên cạnh là lặp. Dòng đồng hồ ở header rút gọn khi việc gọn trong
   1 ngày: `01/09/2026 15:00 – 17:00` thay vì viết đủ ngày 2 lần.
6. Khi tự kiểm bằng Playwright: `.rsum-tb__toggle-all` là nút TOGGLE — gọi 2 lần là thu lại. Phải
   kiểm class `--open` trước khi bấm, nếu không phép đo ra kết quả ngược.
7. **Khuôn gốc khai `.drill-table { width: 100%; min-width: 1740px; table-layout: auto }`** — số
   cứng đo cho bảng **14 cột** của màn phát triển thị trường. Bảng màn này chỉ 12 cột nên:
   - `min-width: 1740px` ép bảng giãn ra và **nới đều mọi cột thêm ~11%**, đẩy cột Kết thúc/Hạn
     văng khỏi khung cuộn;
   - `table-layout` mặc định (auto) khiến `<colgroup>` chỉ là GỢI Ý → **sửa bề rộng cột trong
     `DCOL` hoàn toàn vô tác dụng**, đo mấy lần vẫn ra đúng 1.740px.
   Phải khai lại CẢ HAI trong khối style riêng: `#drill-table-host .drill-table { table-layout:
   fixed; min-width: <tổng colgroup> }`. Kèm `overflow-wrap: anywhere` cho ô (fixed layout mặc
   định để chữ tràn ra ngoài ô) và `white-space: nowrap` cho `.drill-table__center` để chuỗi
   `26/09/2026 17:00` không bị bẻ đôi.
   → **Port mockup mới thì luôn rà lại `min-width` cứng của bảng, đừng để nguyên số của màn cũ.**

## Đã tự kiểm bằng Playwright (26/09/2026 demo, viewport 1600×900)

- Console **0 lỗi**.
- **Dòng cha = tổng dòng con: 0 sai lệch / 12 dòng cha × 7 cột số**; dòng `TỔNG` = tổng 10 phòng ban.
- 4 nhóm trạng thái **chia hết** tổng: 530 + 266 + 174 + 70 = 1.040.
- Cấp Bộ phận **chỉ hiện ở đúng 1 phòng có chia bộ phận** (`PHÒNG KINH DOANH THƯƠNG MẠI`); 9 phòng
  còn lại nhảy thẳng xuống nhân viên; **không có** dòng "Chưa phân bộ phận". Thụt lề 3 cấp đo được
  30 / 52 / 74px.
- Tắt loại Issue → cột biến mất, Tổng 1.040 → 932 (đúng 1.040 − 108).
- Bật "Chỉ tính việc chủ trì" → 1.040 → 659; chú thích dưới bảng đổi chữ theo.
- Tắt "Chỉ hiện NV có việc" → 37 → 43 dòng nhân viên, 6 dòng Tổng = 0.
- Popup mở theo nhân viên: ẩn đúng 3 ô lọc Phòng ban / Bộ phận / Nhân viên, chip chỉ còn "Loại công
  việc", tiêu đề + đường dẫn cấp cha đúng, số dòng khớp số trên bảng (28 = 28).
- Sắp xếp cột Kết thúc/Hạn tăng → giảm đều đúng thứ tự; **974 cặp dòng cùng ngày đều xếp đúng
  theo GIỜ**.
> Các con số **1.027** ở những gạch đầu dòng dưới đây là của lượt đo TRƯỚC khi đổi sang danh mục
> Tân Phát (bộ cũ 30 nhân viên). Kết luận về LUẬT vẫn nguyên giá trị, chỉ khác quy mô; số hiện tại
> là **1.040 đầu việc / 43 nhân viên**.

- **2.054/2.054 ô** (1.027 dòng × 2 cột) đúng dạng `dd/mm/yyyy HH:MM` ở cả 5 loại; **0 ô bị cắt
  chữ**, 1.027/1.027 ô nằm gọn 1 dòng; bảng popup 1.569px, cặp cột Bắt đầu – Kết thúc cùng nằm
  trong khung 1.366px (chỉ 2 cột chót phải cuộn).
- Drawer cả 5 loại đều ngày-giờ ở cả 2 ô lẫn dòng đồng hồ header; bản in chi tiết 1.027/1.027 dòng
  đúng dạng.
- Thêm trường giờ **KHÔNG làm lệch số liệu cũ** (vẫn 279/269/108/184/187 · 1.027 · 521 · 50,7%) —
  nhờ tính bằng công thức theo số thứ tự thay vì gọi `demoRnd()`.
- Bản in chế độ chi tiết: 1.027/1.027 dòng có giờ kết thúc.
- Ô "Loại công việc" khớp từng thông số với ô select bên cạnh (30px · 1px `#cbd5e1` · 6px · 12px);
  panel nổi đúng trên dải tổng hợp; thanh lọc vẫn 2 hàng. Kiểm đủ các nhánh: chọn 1 loại (nhãn
  `Meeting`, tổng 279, bảng 6 cột, "Tất cả" indeterminate) · 2 loại (`Meeting, P. công tác`, tổng
  463 = 279+184) · 3 loại (`Đã chọn 3 loại`) · 0 loại (viền đỏ, tổng 0, bảng 5 cột) · "Tất cả loại"
  bật/tắt · Esc và bấm ra ngoài đều đóng panel · Xoá lọc về đủ 5.
  **Tick không thay mới phần tử checkbox** (so sánh tham chiếu node trước/sau: cùng một node).
- Dòng meta: 5 loại tô đúng `WORK_TYPES[].color`, **khớp 100% với màu chip trên thanh lọc VÀ màu ô
  số trong bảng** (đo `getComputedStyle` cả 3 nơi); tắt 1 loại thì chip màu tương ứng biến mất;
  thu gọn khối tổng hợp vẫn giữ màu. Tooltip (`data-tip`) và bản in **không lẫn thẻ HTML**.
- **Nút In / Xuất Excel trên thanh tiêu đề** (2026-09-08): 2 nút cao đúng 26px, nằm gọn trong thanh
  42px (thanh **không cao thêm**), dồn sát mép phải; toolbar còn 68px, bảng theo dõi lên y=308.
  Cả 2 nút vẫn chạy: In mở popup chọn chế độ rồi ra 50 dòng đủ 3 cấp, Xuất Excel tạo đúng file
  `Bao-cao-ke-hoach-lam-viec-nhan-vien.xls` kèm toast *"1040 đầu việc"*.
- **Danh mục Tân Phát + nhân viên không có việc** (2026-09-08): 10 phòng ban đúng tên thật, đúng
  1 phòng có bộ phận (`PHÒNG KINH DOANH THƯƠNG MẠI`); *Đến Bộ phận* ra 12 dòng (10 phòng + 2 BP),
  *Tất cả cấp* ra 50 dòng. Dải tổng hợp ghi **37 / 43 NV**; bỏ tick *Chỉ hiện NV có việc* →
  **43 dòng nhân viên, đúng 6 dòng Tổng = 0** (đúng 6 người đã chọn). Đổi kỳ sang *Năm nay* thì cả
  6 đều có việc. Tên phòng dài nhất (`PHÒNG KINH DOANH THIẾT BỊ VÀ VẬT LIỆU CÔNG NGHIỆP`) vẫn vừa
  cột: **0 ô tràn chữ**, bảng không cuộn ngang, body không cuộn ngang.
- **Đồng bộ mẫu 2026-09-08**: select cấp ra đúng 3 nấc — *Chỉ Phòng ban* 10 dòng · *Đến Bộ phận*
  19 dòng (4 phòng có bộ phận bung đúng bộ phận, 6 phòng còn lại dừng lại, **0 nhân viên lọt ra**) ·
  *Tất cả cấp* 49 dòng đủ 3 cấp; bấm caret từng dòng không reset select; Xoá lọc về cấp 0.
  Style phân cấp đo được: nền dòng cha `d0 #dceaf4` ≠ `d1 #e9f3f9`, vạch cấp tại `2/24/46px` với bề
  rộng `3/2/2px`, kẻ trên `2px #b6d8e0` ở cấp 0 vs `1px` ở cấp khác.
  Khối tổng hợp popup: mặc định thu, nút *Xem tổng hợp* ↔ *Thu gọn*, mở ra có 3 KPI + 2 nhóm chip,
  mở popup khác thì thu lại dù trước đó đang mở. Icon sort 2 polyline: chưa sắp `.3/.3`, tăng dần
  `1/.3`, giảm dần `.3/1`. In danh sách popup vẫn khớp bộ cột; bản in bảng theo dõi ra đủ 50 dòng
  dù màn chỉ hiện 11.
- Popup còn **11 cột**, bảng rộng đúng 1.366px = khung cuộn ⇒ **không phải cuộn ngang**, 0 ô bị
  cắt chữ. Sắp xếp cột Trạng thái ra đúng 4 nhóm theo thứ tự. Popup mở theo 1 nhóm trạng thái
  (`Đã HT`) thì cột Trạng thái và ô lọc của nó cùng biến mất. In danh sách khớp đúng bộ cột đang
  hiện. Drawer có 2 ô phân biệt: *Trạng thái: Đã hoàn thành* và *Trạng thái chứng từ: Hoàn thành*.
  Toàn màn không còn chữ "Tình trạng".
- Tiêu đề popup khớp bảng chính từng thông số (`none` / `12px` / `normal`); 7 cột có sort, kiểm
  từng cột: Bộ phận (600 dòng `—` đều nằm cuối) · Nhân viên (A→V đúng tiếng Việt) · Trạng thái
  (36 nhóm Loại×Trạng thái xếp đúng vòng đời, không xen kẽ giữa các loại).
- **Quét 63 popup** (9 node × 10 chỉ tiêu): số cột co giãn đúng 7–12 tuỳ chiều bị cố định;
  **không còn cột nào lặp một giá trị** trừ 2 trường hợp do dữ liệu demo ngẫu nhiên (giữ nguyên
  theo luật); 0 ô tràn chữ; In + Xuất Excel của popup khớp đúng bộ cột đang hiện.
- Drawer mở TỪ TRONG popup và nằm **trên** popup (z-index 1201 > 1101), popup giữ nguyên phía dưới.
- Bản in: chế độ bảng theo dõi ra **đủ 3 cấp** (50 dòng, 13 dòng cấp 3) dù màn đang thu gọn; chế độ
  chi tiết ra đúng 1.027 dòng. Xuất Excel tạo blob thành công, không văng lỗi.
- Không cuộn ngang ở `body`; bảng chính không tràn khung ở 1600px; dải tổng hợp chỉ chiếm 15% chiều cao.

## Còn treo

- Việc **nháp** có hạn đã qua vẫn đang bị tính là *Quá hạn*. Nếu thấy vô lý (nháp chưa cam kết hạn)
  thì đổi sang nhóm *Đang thực hiện*, số Quá hạn sẽ giảm.
- Chưa có cột/tín hiệu **mức tải** (so bình quân phòng) — đã bỏ ô "Bình quân/người" nên màn hiện
  không trả lời trực tiếp câu "ai lệch tải". Cần thì bổ sung sau ở dải tổng hợp.
