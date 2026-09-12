# Báo cáo phát triển thị trường - Khách hàng — Mockup UI

File mockup: **`bao-cao-phat-trien-thi-truong-khach-hang.html`** (standalone, không phụ thuộc thư viện ngoài).

## Mục tiêu

Theo dõi **kế hoạch và kết quả phát triển thị trường - khách hàng** của các Phòng ban - Nhân viên
thông qua các cuộc **meeting với khách hàng**.

## Bối cảnh

- Xuất phát từ ý định sửa `Báo cáo kết quả Meeting theo thị trường` (`/assign/report/meeting-by-market`,
  file `../ke-hoach-phat-trien-thi-truong/bao-cao-ket-qua-meeting-theo-thi-truong.html`), nhưng user chốt
  **phát triển hẳn feature mới** — báo cáo meeting cũ GIỮ NGUYÊN, không đụng tới.
- **Cách triển khai + style tham khảo**: `../ke-hoach-phat-trien-thi-truong/bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html`.
  Port NGUYÊN KHỐI `<style>` của màn đó (design tokens navy + teal, `.rsum-*`, `.minutes-modal`,
  `.ticket-drawer`, `#print-area`), phần riêng của màn này nằm ở CUỐI khối style dưới nhãn
  *"BỔ SUNG RIÊNG MÀN PHÁT TRIỂN THỊ TRƯỜNG - KHÁCH HÀNG"*.

## Tiêu chí theo dõi — BẮT BUỘC chọn 1 (không có "Tất cả")

| Tiêu chí | Các cấp theo dõi | Thứ tự cột popup |
|---|---|---|
| Thị trường | Thị trường ▸ Phòng ban ▸ **Bộ phận** ▸ Nhân viên | market · dept · team · host · customer |
| Khách hàng | Khách hàng ▸ Phòng ban ▸ **Bộ phận** ▸ Nhân viên | customer · market · dept · team · host |
| Phòng kinh doanh *(2026-09-08)* | Phòng ban ▸ **Bộ phận** ▸ Nhân viên ▸ **Thị trường** | dept · team · host · market · customer |

- Thứ tự cột popup khai báo tường minh ở `CRITERIA[crit].cols`, không suy ra bằng cờ nhị phân `isCus` nữa.
- Ô lọc riêng theo tiêu chí suy từ `dims`: chiều nào là cấp theo dõi thì hiện ô lọc của chiều đó (Thị trường hiện ở tiêu chí *Thị trường* và *Phòng kinh doanh*; Khách hàng chỉ hiện ở tiêu chí *Khách hàng*).

- Cấp **Bộ phận chỉ hiện với phòng ban CÓ chia bộ phận**; phòng không chia thì cây nhảy thẳng Phòng ban ▸ Nhân viên (KHÔNG đẻ dòng "Chưa phân bộ phận" rỗng).
- Bảng chỉ có **1 dòng `TỔNG`** (thay dòng tiêu đề phần I/II của bản 2 tiêu chí), mang tổng cả kỳ và đổi nhãn theo tiêu chí đang xem.

## Bộ cột bảng theo dõi (10 cột)

`STT · Nội dung theo dõi · Meeting KH · Đã thực hiện · Hoàn thành · Huỷ · Tỷ lệ HT · KH mới · Nhu cầu · Giá trị dự kiến` (10 cột)

Định nghĩa chốt:
- **Meeting KH** = mọi meeting có NGÀY HỌP trong kỳ (mọi trạng thái).
- **Đã thực hiện** = ngày họp đã tới **và** trạng thái ≠ Huỷ (gồm cả meeting đã họp chưa chốt biên bản).
- **Hoàn thành** = trạng thái *Hoàn thành* (đã có biên bản) — tập con của Đã thực hiện.
- **KH mới** = kỳ này là lần ĐẦU TIÊN có meeting với khách hàng đó; gắn vào ĐÚNG 1 meeting (meeting đầu) nên **vẫn cộng được theo cấp**.
- ⚠️ Mọi chỉ tiêu đều tính **theo từng meeting**, không đếm distinct → số dòng cha luôn = tổng dòng con (đã verify 0 sai lệch / 213 dòng cha × 6 cột).
- **"KH đã tiếp cận"** (đếm distinct) KHÔNG cộng được theo cấp nên **chỉ nằm ở dải tổng hợp**, không có trong bảng.

## Kỳ báo cáo

`Ngày hôm nay · Tuần này · **Tuần tiếp theo** · Tháng này (mặc định) · **Tháng tiếp theo** · Quý này · Năm nay · Tuỳ chọn`

- 2 kỳ **tương lai** (chốt 2026-09-07) để soát kế hoạch meeting sắp tới. Tuần tiếp theo = thứ 2 tuần này + 7 ngày (vắt được sang tháng sau); Tháng tiếp theo = trọn tháng kế tiếp.
- Ở kỳ tương lai, *Đã thực hiện / Hoàn thành / Huỷ / Nhu cầu* = 0 vì chưa tới ngày họp — đúng bản chất, không phải lỗi.

## Dải tổng hợp (chốt 2026-09-07)

Giữ **phong cách khối/hộp** của màn CSKH nhưng **nén tối đa**: 2 khối nằm CÙNG 1 HÀNG, ô con xếp NGANG 1 hàng (bản gốc xếp dọc + lưới 2×2 → cao 344px = 44% màn hình). **BỎ HẲN khối KPI.**

| Khối | 3 ô con |
|---|---|
| Kế hoạch meeting trong kỳ | Tổng meeting · Lập trước kỳ · Lập trong kỳ |
| Kết quả phát triển trong kỳ | Meeting hoàn thành · Meeting bị huỷ · Nhu cầu thu thập được |

- **Lập trước kỳ / Lập trong kỳ** bổ dọc theo **`created_at` (ngày tạo meeting)**. Ngày tạo luôn ≤ ngày họp mà ngày họp đã trong kỳ ⇒ 2 nhóm **chia hết** tổng.
- Số tổng chuyển xuống ô con nên **header khối bỏ số to** (tránh lặp), chỉ còn tiêu đề + 1 dòng meta không trùng lặp.
- ❌ Đã thử **bản lưới text phẳng** (kiểu `.type-summary-bar__grid` của báo cáo meeting) — user CHÊ XẤU, đã revert. Ngôn ngữ thị giác giữ nguyên hộp bo góc / viền trái màu / số to.

## Luật POPUP chi tiết (chốt 2026-09-07)

0. **Khối tổng hợp trong popup MẶC ĐỊNH THU GỌN** (chốt 2026-09-08): 2 khối *KPI* + *Phân bổ meeting theo cơ cấu* nằm trong `#drill-sumwrap`, có dòng đầu `.drill-sumhead` mang nút thu gọn dùng **chung khuôn `.rsum-toggle`** với khối tổng hợp của form báo cáo. Mở popup ra là thấy ngay danh sách meeting; bấm *Mở rộng* mới dựng nội dung 2 khối (thu gọn thì khỏi tính).
   - `openDrill()` đặt lại `state.drillSumCollapsed = true` **mỗi lần mở**, nên popup nào cũng bắt đầu ở trạng thái thu gọn — không mang trạng thái từ popup trước sang.
   - Ẩn bằng thuộc tính `hidden` trên khối bọc, KHÔNG dùng `style.display`, để không đè logic tự ẩn của `renderDrillSummary` (khối chéo tự ẩn khi không còn chiều nào để phân bổ).
   - Nhãn nút: **"Xem tổng hợp"** khi đang thu, **"Thu gọn"** khi đang mở (chốt 2026-09-08).


1. **Bộ lọc**: đang xem theo đối tượng A thì **BỎ ô lọc theo A**. Cây lưu `path` (chuỗi cấp đã đi qua) → mọi chiều trên path đều ẩn ô lọc và xoá giá trị. Thêm luật: **cố định Khách hàng ⇒ ẩn luôn ô lọc Thị trường** (1 KH chỉ thuộc 1 thị trường). Cấp đã cố định vẫn dùng để thu hẹp cascade cấp dưới.
2. **Tiêu đề nêu rõ đối tượng**: *"Đang xem &lt;chỉ tiêu&gt; theo &lt;Cấp&gt;: &lt;Tên&gt;"* — ví dụ *Đang xem Kế hoạch meeting theo Khách hàng: Công ty CP Thành Đạt Sài Gòn*. Node nằm sâu thì dòng phụ hiện **đường dẫn cấp cha** (`Khách hàng: … › Phòng ban: … › Bộ phận: …`).
3. **Chip phân bổ chỉ còn Thị trường + Phòng ban** — bỏ Loại meeting / Trạng thái (không phải "cơ cấu"), bỏ Nhân viên / Khách hàng (số lượng lớn, chip vụn). Chip cũng ẩn theo cùng luật ẩn của bộ lọc ⇒ popup theo Thị trường và popup theo Khách hàng đều còn đúng chip **Phòng ban**.
4. **Thứ tự cột bám tiêu chí** — các chiều theo dõi dồn lên ngay sau STT, rồi mới tới thông tin meeting:
   - Thị trường: `STT · Thị trường · Phòng ban · Bộ phận · Nhân viên chủ trì · Khách hàng · Ngày họp · …`
   - Khách hàng: `STT · Khách hàng · Thị trường · Phòng ban · Bộ phận · Nhân viên chủ trì · Ngày họp · …`
   - ⚠️ Quy tắc "Nhân viên chủ trì LUÔN trước Phòng ban" (nêu 2026-09-07 sáng) **ĐÃ BỊ THAY THẾ** — user chốt xếp đúng thứ tự cấp theo dõi.
5. **Cột Ngày họp có GIỜ** (`07/09/2026 13:00`); **"Ngày tạo phiếu" → "Ngày tạo meeting"**. **KHÔNG có cột "Mã meeting"** (bỏ 2026-09-08) — bản in / Excel của popup bám theo; riêng bản in *"Danh sách chi tiết meeting"* của cả báo cáo (`detailColumns`) VẪN giữ mã, xem *Còn treo*.
6. **BỎ CỘT của cấp đã cố định** (chốt 2026-09-07): cấp nào nằm trên `path` của node thì bỏ luôn cột đó — mọi dòng trong popup đều mang đúng 1 giá trị ở cấp ấy, cột chỉ lặp lại điều tiêu đề popup đã nói. Cùng nguyên tắc với việc ẩn ô lọc ⇒ popup theo Bộ phận bỏ cả cột Phòng ban (phòng ban cũng trên path).
   - Dùng `drillFixedDims` (các cấp trên path), **KHÔNG** dùng `drillHiddenDims`: luật *cố định Khách hàng ⇒ ẩn Thị trường* chỉ áp cho **ô lọc và chip**, còn **CỘT Thị trường vẫn giữ** ở popup theo Khách hàng.
   - Popup mở từ dòng `TỔNG` không bỏ cột nào.
   - Bảng popup + bản in + Excel dùng chung `drillColumns()` nên bám theo cùng lúc.
   - ⚠️ Hệ quả: popup theo Khách hàng mất luôn **chip "KH mới"** (chip nằm trong ô Khách hàng). 15/56 node Khách hàng có chip trên danh sách nhiều dòng — xem *Còn treo*.
7. **BỎ CỘT BỘ PHẬN khi popup không có dòng nào thuộc bộ phận** (chốt 2026-09-07): phần lớn phòng ban không chia bộ phận nên cột sẽ toàn `—`. Xét trên TOÀN BỘ meeting của node (`drillMeetings`), **không** xét theo bộ lọc trong popup, để cột không nhấp nháy khi lọc. Popup dòng TỔNG vẫn giữ cột vì có dòng thuộc PHÒNG KINH DOANH THƯƠNG MẠI.
8. **Sắp xếp được ở 5 cột** (thêm *Nhân viên chủ trì* 2026-09-08): Thị trường · Phòng ban · Nhân viên chủ trì · Ngày họp · Ngày tạo meeting (bấm tiêu đề: tăng → giảm; mở popup mới reset về Ngày họp tăng dần). In + Xuất Excel của popup **bám đúng thứ tự đang sắp**.
9. **Icon sắp xếp = 2 mũi tên ngược chiều** (lên / xuống): cột chưa sắp thì cả 2 đều mờ (`opacity .3`); cột đang sắp thì chiều đang áp tô đậm (`opacity 1`), chiều kia vẫn mờ.

## Thanh tiêu đề (chốt 2026-09-08)

2 nút **In báo cáo · Xuất Excel** dồn về **góc phải thanh tiêu đề navy** (`.topbar__actions`, `margin-left:auto`), không còn nằm ở toolbar lọc.

- Khuôn gọn: cao **26px**, chữ 12px, nền trong suốt + viền trắng mờ cho hợp nền navy (nút cũ cao 35px, nền đặc). Nút *Xuất Excel* giữ sắc xanh lá để phân biệt với nút *In*.
- **Thanh tiêu đề KHÔNG cao thêm** (vẫn 42px) vì nút thấp hơn khoảng trống sẵn có.
- Toolbar chỉ còn cụm lọc: **118 → 68px**, kéo cả trang lên **50px** (bảng theo dõi từ y=359 lên y=309).

## Chọn cấp xem (chốt 2026-09-07)

Nút *"Ẩn / Hiện chi tiết"* trong ô tiêu đề cột "Nội dung theo dõi" **đã bỏ**, thay bằng **select chọn cấp** ở đúng chỗ đó:

`Chỉ <cấp gốc>` · `Đến Phòng ban` · `Đến Bộ phận` · `Tất cả cấp (đến Nhân viên)`

- Nhãn cấp lấy thẳng từ `CRITERIA[crit].head` nên đổi tiêu chí là nhãn đổi theo (*Chỉ Thị trường* ↔ *Chỉ Khách hàng*).
- **Hiểu theo TÊN CẤP, không theo độ sâu**: chỉ bung node có con thuộc cấp còn trong phạm vi (`dim` của con). Chọn *Đến Bộ phận* thì chỉ phòng CÓ bộ phận bung thêm 1 cấp; 9 phòng không chia bộ phận dừng ở Phòng ban, **không lòi nhân viên ra sớm**.
- *Tất cả cấp* = cấp sâu nhất (Nhân viên) nên gộp làm 1 mục, không tách 2 mục trùng nhau.
- Bấm mũi tên từng dòng vẫn tự do — chỉ đổi `state.expanded`, **không** đụng `state.level`, nên select giữ nguyên lựa chọn gần nhất.
- Nút *Xoá lọc* đưa cấp về mặc định (`Chỉ <cấp gốc>`).
- Bản in / Excel **luôn xuất đủ mọi cấp**, không phụ thuộc cấp đang xem trên màn.

## Phân biệt cấp khi bung hết bảng (chốt 2026-09-08)

Bung *Tất cả cấp* thì bảng dài 145 dòng (tiêu chí Thị trường) / 214 dòng (Khách hàng) — user báo rối. Đo được **2 nguyên nhân**, không phải cảm giác:

1. `.rsum-tb__row--open td` là **1 rule chung** nên khi bung, cả 3 cấp cha (**63/145 dòng**) nhận CHUNG một nền `#e8f2f8` + cùng độ đậm 800 ⇒ phân tầng màu theo độ sâu (`d1/d2/d3`) bị xoá sạch.
2. Nền 2 cấp lá chênh nhau ~1% (`#fafcfe` vs `#fdfefe`) — mắt thường không thấy.

Còn lại chỉ thụt lề 22px và chuỗi STT làm tín hiệu. Cách xử lý đã chốt:

- **Tách nền dòng cha theo TỪNG CẤP**: `d0 #dceaf4` · `d1 #e9f3f9` · `d2 #f2f8fb` (đậm → nhạt theo cấp).
- **Vạch cấp bên trái ô tên** — nấc thang 22px, đậm → nhạt: `d0` 3px `#0a7c88` tại `left:2px`; `d1/d2/d3` 2px với alpha `.55 / .32 / .18` tại `24 / 46 / 68px`.
  Dựng bằng `::before` tuyệt đối chứ KHÔNG dùng `border-left` của `td` — border sẽ nằm ở mép ô, không nằm đúng chỗ thụt lề.
- **Kẻ đậm 2px `#b6d8e0` phía trên mỗi dòng cấp 0** để cắt khối; các dòng khác giữ kẻ 1px. Đây là tín hiệu chính cho tiêu chí Khách hàng vì có 56 khối nối nhau.
- Luật `:hover` vẫn thắng nền mới (cụ thể hơn + khai báo sau).

## Tiêu đề cột

**Viết hoa chữ đầu** (bỏ `text-transform: uppercase`) và **KHÔNG xuống dòng** (`white-space: nowrap`) — áp cho **cả bảng theo dõi lẫn bảng trong popup** (popup đổi 2026-09-08, bỏ luôn `letter-spacing`).

`.drill-table` dùng chung cho **bảng popup và bảng biên bản trong drawer**, nên drawer đổi theo cùng lúc.
Các nhãn KHÁC trong popup vẫn giữ chữ hoa (`.drill-sum__label` — "THỊ TRƯỜNG" / "PHÒNG BAN" của dải chip) vì là nhãn nhóm, không phải tiêu đề cột.

## Data demo

- Mốc **`TODAY = 26/09/2026`** — đặt gần CUỐI kỳ mặc định (tháng này) để bảng có đủ meeting đã thực hiện / hoàn thành / huỷ mà vẫn còn meeting chưa tới ngày họp.
- Sinh cố định bằng **LCG có hạt giống** (không `Math.random`) → demo không nhảy số.
- Quy mô (cập nhật 2026-09-08): **2 công ty · 10 phòng ban · 43 nhân viên · 10 tỉnh/TP · 60 khách hàng · 661 meeting**; kỳ mặc định 09/2026 có **330 meeting · 58 KH · 90 nhu cầu · 1177,5 tỷ**.
- **Bộ sinh meeting chạy theo NHÂN VIÊN ▸ THỊ TRƯỜNG** (trước đây theo khách hàng). Với mỗi thị trường phụ trách, luôn phát ít nhất 1 meeting rơi vào **tháng của `TODAY`** rồi rải thêm 1–3 meeting ra các tháng khác ⇒ cấp *Thị trường* của tiêu chí mới **chắc chắn có 4–5 nhánh ngay ở kỳ mặc định**.
  - Hệ quả: kỳ mặc định gom **330/661 meeting** (~50%) vì mỗi cặp (nhân viên × thị trường) đều bị ép 1 meeting vào tháng này.
  - `isFirst` ("KH mới") tính SAU khi có toàn bộ meeting: meeting sớm nhất của mỗi khách hàng — kiểm chứng: kỳ "Năm nay" cho **KH mới = 60 = đúng số khách hàng**.
  - **Danh mục lấy từ DB HRM thật** (`hrm_erp`: `companies` ▸ `departments` ▸ `parts` ▸ `employee_infos`), chỉ chọn phòng **kinh doanh** có từ 5 nhân viên đang hoạt động. Công ty: *CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT* (6 phòng) và *TNHH THIẾT BỊ TÂN PHÁT SÀI GÒN* (4 phòng).
  - **Chỉ 1 phòng có bộ phận** — *PHÒNG KINH DOANH THƯƠNG MẠI*. DB có 3 bộ phận nhưng bộ phận thứ 3 (*Kinh doanh dự án*) chỉ 1 người nên không đạt mức tối thiểu ⇒ lấy 2 bộ phận: *BP Thiết bị, vật tư, hóa chất chăm sóc xe* · *BP Thiết bị, vật tư lốp*.
  - **Mỗi phòng ban / bộ phận 3–5 nhân viên**, lấy N người đầu trong DB theo chu kỳ cố định 3·4·5 → **43 người**, demo không nhảy số.
  - **Mỗi nhân viên phụ trách 4–5 thị trường** (`EMPLOYEES[].markets`, chia cố định bước nhảy 3 trên vòng 10 tỉnh).
  - Trường `code` của phòng ban (`HN_KD1`, `HN_KDTM`, `KV1`…) lấy nguyên từ DB nhưng **hiện chưa dùng ở đâu** — dự phòng làm nhãn ngắn cho popup.
  - ⚠️ Con số **"591 meeting" ở tài liệu cũ là SAI**: đo lại cả bản trước lẫn sau khi đổi quy mô đều ra **612**.
  - Đổi số thị trường / nhân viên **không làm lệch chỉ tiêu nào**: `demoPick` luôn tiêu thụ đúng 1 số ngẫu nhiên bất kể độ dài mảng, nên chuỗi LCG giữ nguyên — chỉ phân bổ theo thị trường / phòng ban đổi.
- **5 loại meeting**: phát triển thị trường · khảo sát nhu cầu · chăm sóc khách hàng · chốt phương án · **triển khai Dự án**.
- `createdAt` = ngày họp − (1..28) ngày, tính bằng công thức theo số thứ tự phiếu (KHÔNG gọi `demoRnd`) để bổ sung trường này **không làm lệch chuỗi ngẫu nhiên** — mọi số liệu cũ giữ nguyên.

## Còn treo

- **"KH mới" đang đếm cả meeting đầu tiên bị huỷ / chưa tới ngày họp** (22 = 16 hoàn thành + 3 huỷ + 2 đã chốt + 1 lên lịch). Nếu chỉ tính khi đã thực sự gặp khách → đổi mốc sang meeting *hoàn thành* đầu tiên, số còn ~16.
- Ở tiêu chí Khách hàng, **CỘT** Thị trường vẫn hiện dù lặp 1 giá trị (chỉ ô LỌC đã bỏ theo yêu cầu) — user đã chốt giữ khi duyệt luật bỏ cột.
- **Chip "KH mới" biến mất ở popup theo Khách hàng** vì chip render trong ô Khách hàng mà cột đó đã bị bỏ. Đo trên bản trước khi sửa: 15/56 node Khách hàng có đúng 1 dòng mang chip trong danh sách nhiều dòng (vd `kh49`: 5 dòng, 1 chip) → mất dấu "meeting đầu tiên với khách này". Chưa xử lý; hướng: gắn chip sang cột *Mã meeting* hoặc *Tên meeting* khi cột Khách hàng bị bỏ.
- **`createdAt` của data demo không chặn trần theo TODAY** — sinh bằng *ngày họp − (1..28) ngày* nên có phiếu mang ngày tạo ở tương lai. Kỳ tương lai vì thế vẫn hiện *Lập trong kỳ* ≠ 0 (đo: 8 ở Tuần tiếp theo, 75 ở Tháng tiếp theo) trong khi đời thật không thể tạo phiếu sau hôm nay. Sửa bằng cách kẹp `createdAt = min(createdAt, TODAY)` — sẽ làm lệch nhẹ tỷ lệ 72/88 của tháng này.
- **Bản in "Danh sách chi tiết meeting" của cả báo cáo vẫn còn cột Mã meeting** — chỉ popup (và bản in / Excel của popup) đã bỏ. Nếu muốn đồng bộ thì gỡ `'code'` khỏi `detailColumns()`.
- Chưa port Vue thật; chưa responsive.
