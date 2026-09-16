# Báo cáo phát triển thị trường - Khách hàng — Mockup UI

File mockup: **`bao-cao-phat-trien-thi-truong-khach-hang.html`** (standalone, không phụ thuộc thư viện ngoài).

## Mục tiêu

Theo dõi **kế hoạch và kết quả phát triển thị trường - khách hàng** của các Phòng ban - Nhân viên
thông qua các cuộc **meeting với khách hàng**.

## Bối cảnh

- Xuất phát từ ý định sửa `Báo cáo kết quả Meeting theo thị trường` (`/assign/report/meeting-by-market`,
  file `../gop-db/ke-hoach-phat-trien-thi-truong/bao-cao-ket-qua-meeting-theo-thi-truong.html`), nhưng user chốt
  **phát triển hẳn feature mới** — báo cáo meeting cũ GIỮ NGUYÊN, không đụng tới.
- **Cách triển khai + style tham khảo**: `../gop-db/ke-hoach-phat-trien-thi-truong/bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html`.
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

## Bộ cột bảng theo dõi (9 cột)

`STT · Nội dung theo dõi · Meeting KH · Hoàn thành · Huỷ · Tỷ lệ HT · KH mới · Nhu cầu · Giá trị dự kiến` (9 cột)

Định nghĩa chốt:
- **Meeting KH** = mọi meeting có NGÀY HỌP trong kỳ (mọi trạng thái).
- **Hoàn thành** = trạng thái *Hoàn thành* (đã có biên bản).
- **Tỷ lệ HT** = Hoàn thành ÷ Meeting KH của chính dòng đó.
- **KH mới** *(đổi nghĩa 2026-09-13)* = **khách hàng được TẠO trong kỳ**, tính cho **NGƯỜI TẠO khách hàng** (`customers.created_by`), thị trường lấy theo **thị trường của khách hàng**. Không cần có meeting trong kỳ vẫn được đếm.
- ❌ **Cột "Đã thực hiện" ĐÃ BỎ** (2026-09-13) — user chốt: *sai về ý nghĩa theo dõi*. Gỡ khỏi bảng, bản in, Excel và cả chỉ tiêu popup.
- ⚠️ Chỉ tiêu meeting tính **theo từng meeting** (không đếm distinct), còn mỗi KH mới rơi vào **đúng 1 nhánh lá** → dòng cha luôn = tổng dòng con. Đo lại sau khi đổi: **0 sai lệch / 3018 ô** (Thị trường 130 dòng cha × 6 cột, Khách hàng 318 × 6, Phòng kinh doanh 55 × 6).
- **"KH đã tiếp cận"** (đếm distinct) KHÔNG cộng được theo cấp nên **chỉ nằm ở dải tổng hợp**, không có trong bảng.

### Cách cộng "KH mới" theo cấp

Mỗi KH tạo trong kỳ được gói thành **1 bản ghi giả** mang đủ các chiều của cây
(`customerId · marketId của KH · hostId = người tạo · departmentId / teamId của người tạo`), rồi
chạy qua **đúng bộ `DIM`** khi dựng cây. Hệ quả:

- Node **tự mọc** cho nhân viên / thị trường không có meeting nào trong kỳ (đo ở tiêu chí Thị trường: **8 dòng** có *Meeting KH = 0*, tất cả đều có *KH mới > 0*).
- `buildTree` **tách 2 rổ ngay tại node**: `items` (meeting thật) và `news` (KH mới). Mọi chỗ đang đọc `items` — popup, drawer, bản in, Excel — không thấy bản ghi giả.
- Lọc **Loại meeting / Trạng thái KHÔNG áp** cho KH mới (không gắn với meeting nào) — đã ghi trong tooltip cột.

## Kỳ báo cáo

`Ngày hôm nay · Tuần này · **Tuần tiếp theo** · Tháng này (mặc định) · **Tháng tiếp theo** · Quý này · Năm nay · Tuỳ chọn`

- 2 kỳ **tương lai** (chốt 2026-09-07) để soát kế hoạch meeting sắp tới. Tuần tiếp theo = thứ 2 tuần này + 7 ngày (vắt được sang tháng sau); Tháng tiếp theo = trọn tháng kế tiếp.
- Ở kỳ tương lai, *Hoàn thành / Huỷ / Nhu cầu* = 0 vì chưa tới ngày họp — đúng bản chất, không phải lỗi.
- *Lập trong kỳ* ở kỳ tương lai nay = **0** (chốt 2026-09-13) — xem *Data demo*, mục kẹp trần ngày tạo phiếu. Đo: Tuần tiếp theo 23 meeting → 23 lập trước kỳ / 0 lập trong kỳ; Tháng tiếp theo 64 → 64 / 0.

## Dải tổng hợp (chốt 2026-09-07)

Giữ **phong cách khối/hộp** của màn CSKH nhưng **nén tối đa**: 2 khối nằm CÙNG 1 HÀNG, ô con xếp NGANG 1 hàng (bản gốc xếp dọc + lưới 2×2 → cao 344px = 44% màn hình). **BỎ HẲN khối KPI.**

| Khối | 3 ô con |
|---|---|
| Kế hoạch meeting trong kỳ | Tổng meeting · Lập trước kỳ · Lập trong kỳ |
| Kết quả phát triển trong kỳ | Meeting hoàn thành · Meeting bị huỷ · Nhu cầu thu thập được |

Dòng meta của khối 2 ghi **"N KH mới tạo trong kỳ"** (trước đây là *"N KH mới phát triển"*).

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
4. **Thứ tự cột = 3 KHỐI, thông tin meeting lên trước** (đảo 2026-09-13):

   | Khối | Cột |
   |---|---|
   | 1. Thông tin meeting | `Tên meeting · Ngày họp · Ngày tạo meeting · Loại meeting · Trạng thái` |
   | 2. Các chiều theo dõi | đúng thứ tự cấp của tiêu chí đang xem (`CRITERIA[crit].cols`) |
   | 3. Cột số | `Nhu cầu đầu tư ghi nhận · Giá trị dự kiến (đ)` |

   - **Tên meeting đứng đầu khối** (chốt 2026-09-13) — là thứ nhận dạng dòng, đọc trước rồi mới tới thời gian.
   - Ví dụ tiêu chí Thị trường: `STT · Tên meeting · Ngày họp · Ngày tạo meeting · Loại meeting · Trạng thái · Thị trường · Phòng ban · Bộ phận · Nhân viên chủ trì · Khách hàng · Nhu cầu · Giá trị dự kiến`.
   - 2 cột số để **cuối bảng** theo quy ước "cột số canh phải nằm cuối" của bảng theo dõi và 2 báo cáo anh em, không đi liền khối meeting.
   - **Bản in "Danh sách chi tiết meeting"** của cả báo cáo dùng chung thứ tự này.
   - Popup **"KH mới"** KHÔNG áp luật này: danh sách là khách hàng, không có cột meeting nào.
   - ⚠️ 2 luật cũ đều **ĐÃ BỊ THAY THẾ**: "Nhân viên chủ trì LUÔN trước Phòng ban" (2026-09-07 sáng) và "các chiều theo dõi dồn lên ngay sau STT" (2026-09-07).
5. **Cột Ngày họp có GIỜ** (`07/09/2026 13:00`); **"Ngày tạo phiếu" → "Ngày tạo meeting"**. **KHÔNG có cột "Mã meeting"** (bỏ 2026-09-08) — bản in / Excel của popup bám theo; riêng bản in *"Danh sách chi tiết meeting"* của cả báo cáo (`detailColumns`) VẪN giữ mã, xem *Còn treo*.
6. **BỎ CỘT của cấp đã cố định** (chốt 2026-09-07): cấp nào nằm trên `path` của node thì bỏ luôn cột đó — mọi dòng trong popup đều mang đúng 1 giá trị ở cấp ấy, cột chỉ lặp lại điều tiêu đề popup đã nói. Cùng nguyên tắc với việc ẩn ô lọc ⇒ popup theo Bộ phận bỏ cả cột Phòng ban (phòng ban cũng trên path).
   - Dùng `drillFixedDims` (các cấp trên path), **KHÔNG** dùng `drillHiddenDims`: luật *cố định Khách hàng ⇒ ẩn Thị trường* chỉ áp cho **ô lọc và chip**, còn **CỘT Thị trường vẫn giữ** ở popup theo Khách hàng.
   - Popup mở từ dòng `TỔNG` không bỏ cột nào.
   - Bảng popup + bản in + Excel dùng chung `drillColumns()` nên bám theo cùng lúc.
   - ⚠️ Hệ quả: popup theo Khách hàng mất luôn **chip "KH mới"** (chip nằm trong ô Khách hàng). 15/56 node Khách hàng có chip trên danh sách nhiều dòng — xem *Còn treo*.
7. **BỎ CỘT BỘ PHẬN khi popup không có dòng nào thuộc bộ phận** (chốt 2026-09-07): phần lớn phòng ban không chia bộ phận nên cột sẽ toàn `—`. Xét trên TOÀN BỘ meeting của node (`drillMeetings`), **không** xét theo bộ lọc trong popup, để cột không nhấp nháy khi lọc. Popup dòng TỔNG vẫn giữ cột vì có dòng thuộc PHÒNG KINH DOANH THƯƠNG MẠI.
8. **Sắp xếp được ở 5 cột** (thêm *Nhân viên chủ trì* 2026-09-08): Thị trường · Phòng ban · Nhân viên chủ trì · Ngày họp · Ngày tạo meeting (bấm tiêu đề: tăng → giảm; mở popup mới reset về Ngày họp tăng dần). In + Xuất Excel của popup **bám đúng thứ tự đang sắp**.
9. **POPUP "KH mới" là danh sách KHÁCH HÀNG, không phải meeting** (chốt 2026-09-13):
   - Cột: `STT · Khách hàng · Thị trường · Phòng ban · Bộ phận · Người tạo KH · Ngày tạo KH` (vẫn bỏ cột của cấp đã cố định + bỏ Bộ phận khi không dòng nào thuộc bộ phận).
   - Ẩn 2 ô lọc **Loại meeting / Trạng thái** (không có meeting để lọc); mốc sắp xếp mặc định là **Ngày tạo KH** chứ không phải Ngày họp.
   - **Bỏ hẳn 3 hộp KPI** (đều tính trên meeting), chỉ giữ dải chip phân bổ Thị trường / Phòng ban.
   - **Không lặp chip "KH mới"** ở từng dòng — cả bảng đều là KH mới thì chip là thừa (đo bản đầu: 12/12 dòng đều mang chip).
   - ⚠️ `.drill-table` có `min-width: 1740px` (đo cho bảng meeting 13 cột). Bảng này chỉ 7 cột (984px) nên phải thêm `.drill-table--fit { min-width: 0 }`, nếu không 2 cột cuối bị đẩy khuất ngoài khung 1368px.
   - Excel xuất ra tên `Danh-sach-khach-hang-moi.xls`; bản in bỏ dòng KPI tính trên meeting.

10. **POPUP "Meeting bị huỷ" có bộ cột riêng** (chốt 2026-09-13):
    `STT · Tên meeting · Ngày tạo meeting · Ngày họp · Lý do huỷ · Loại meeting · <các cấp theo dõi>`
    - **Ngày tạo meeting đứng TRƯỚC Ngày họp** — soát phiếu lập ra rồi bỏ.
    - **Cột Lý do huỷ 2 dòng**: lý do chọn từ *Danh mục lý do huỷ meeting* (đậm) + **ghi chú huỷ** nhập tay ở dòng dưới (11px, `--text-muted`).
    - **Bỏ cột Trạng thái** — mọi dòng đều là "Huỷ", cùng luật bỏ cột của cấp đã cố định.
    - **Bỏ cột Nhu cầu + Giá trị dự kiến** — nhu cầu chỉ ghi nhận ở meeting *Hoàn thành* nên ở đây luôn rỗng (đo: 0/29 dòng có số).
    - Cột Lý do huỷ rộng **250px**, nằm trọn trong khung ngay khi mở popup.
    - 📌 Trước khi đảo thứ tự cột (xem luật 4), khối chiều theo dõi đứng đầu bảng làm cột Lý do huỷ bắt đầu ở **1388px trong khung 1368px** → phải cuộn ngang mới thấy; khi đó phải đẩy cột lên trước "Tên meeting" và bóp còn 225px. Đảo khối xong thì cả 2 chỗ chắp vá này **không cần nữa**.

11. **Chip "KH mới" nhảy sang cột "Tên meeting"** khi cột Khách hàng bị bỏ (chốt 2026-09-13) — cờ `DRILL_NO_CUS_COL` đặt lại trước mỗi lần dựng bảng / bản in / Excel. Đo ở popup theo Khách hàng: cột Khách hàng bị bỏ, chip xuất hiện ở ô *Tên meeting* (cột thứ 8).
    - ⚠️ Theo nghĩa MỚI, "KH mới" là thuộc tính của KHÁCH HÀNG nên trong popup cố định 1 khách hàng thì **mọi dòng đều mang chip** (đo: 12/12 dòng). Bản cũ chỉ 1 dòng có chip vì bám "meeting đầu tiên".

12. **Icon sắp xếp = 2 mũi tên ngược chiều** (lên / xuống): cột chưa sắp thì cả 2 đều mờ (`opacity .3`); cột đang sắp thì chiều đang áp tô đậm (`opacity 1`), chiều kia vẫn mờ.

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

Bung *Tất cả cấp* thì bảng rất dài — user báo rối. Đo lại 2026-09-13: **331 dòng** (Thị trường) ·
**590 dòng** (Khách hàng) · **256 dòng** (Phòng kinh doanh). ⚠️ Con số *145 / 214* ghi ở tài liệu cũ
là SAI. Đo được **2 nguyên nhân** gây rối, không phải cảm giác:

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
- Quy mô (cập nhật 2026-09-08): **2 công ty · 10 phòng ban · 43 nhân viên · 10 tỉnh/TP · 60 khách hàng · 661 meeting**; kỳ mặc định 09/2026 có **330 meeting · 58 KH · 90 nhu cầu · 1177,5 tỷ · 12 KH mới**.
- **NGÀY TẠO + NGƯỜI TẠO khách hàng** (thêm 2026-09-13) — nền của chỉ tiêu "KH mới":
  - `createdBy` = `ownerId` (nhân viên chủ nhà sẵn có), `createdAt` tính bằng **công thức theo số thứ tự** `ageDays = (i % 5 === 0) ? (i*7)%26 : 30 + (i*53)%400`, lùi từ `TODAY` — **KHÔNG gọi `demoRnd`** nên chuỗi LCG giữ nguyên, mọi số liệu meeting cũ không xê dịch (verify: vẫn đúng 330 meeting · 90 nhu cầu · 1177,5 tỷ như trước khi sửa).
  - Cứ 5 KH có 1 KH sinh trong tháng của `TODAY` ⇒ kỳ mặc định luôn có **12 KH mới**; phần còn lại rải 30–429 ngày trước và **không bao giờ vượt `TODAY`**.
  - Đối chứng: KH mới **tháng này 12 · quý này 20 · năm nay 44**, khớp đúng công thức sinh dữ liệu.
- **NGÀY TẠO PHIẾU MEETING KẸP TRẦN theo `TODAY`** (2026-09-13): `createdAt = min(ngày họp − (1..28) ngày, TODAY)`. Đời thật không thể tạo phiếu ở tương lai; trước khi kẹp, kỳ tương lai hiện *Lập trong kỳ* = 8 (tuần tiếp theo) / 75 (tháng tiếp theo).
- **DANH MỤC LÝ DO HUỶ MEETING** (thêm 2026-09-13) — 8 mục: *Khách hàng bận đột xuất · Khách hàng hoãn sang kỳ sau · Khách hàng không còn nhu cầu · Nhân sự chủ trì bận công tác · Trùng lịch với cuộc họp khác · Chưa chuẩn bị kịp tài liệu / phương án · Thay đổi kế hoạch kinh doanh · Lý do khác*.
  - Vẫn chọn bằng `demoPick` (tiêu thụ đúng 1 số ngẫu nhiên bất kể độ dài mảng) nên **đổi danh mục không làm lệch số liệu cũ**.
  - **Ghi chú huỷ** chọn bằng công thức theo số thứ tự phiếu (`seq % 3 === 0`), không gọi `demoRnd` — đo: **11/29** phiếu huỷ của kỳ mặc định có ghi chú.
  - ⚠️ HRM thật hiện chỉ có **1 ô `cancel_reason` nhập tay tự do** (`MeetingForm.vue`), CHƯA có danh mục. Port thật cần 1 bảng danh mục + tách `cancel_reason_id` / `cancel_note`.
- **Bộ sinh meeting chạy theo NHÂN VIÊN ▸ THỊ TRƯỜNG** (trước đây theo khách hàng). Với mỗi thị trường phụ trách, luôn phát ít nhất 1 meeting rơi vào **tháng của `TODAY`** rồi rải thêm 1–3 meeting ra các tháng khác ⇒ cấp *Thị trường* của tiêu chí mới **chắc chắn có 4–5 nhánh ngay ở kỳ mặc định**.
  - Hệ quả: kỳ mặc định gom **330/661 meeting** (~50%) vì mỗi cặp (nhân viên × thị trường) đều bị ép 1 meeting vào tháng này.
  - **Danh mục lấy từ DB HRM thật** (`hrm_erp`: `companies` ▸ `departments` ▸ `parts` ▸ `employee_infos`), chỉ chọn phòng **kinh doanh** có từ 5 nhân viên đang hoạt động. Công ty: *CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT* (6 phòng) và *TNHH THIẾT BỊ TÂN PHÁT SÀI GÒN* (4 phòng).
  - **Chỉ 1 phòng có bộ phận** — *PHÒNG KINH DOANH THƯƠNG MẠI*. DB có 3 bộ phận nhưng bộ phận thứ 3 (*Kinh doanh dự án*) chỉ 1 người nên không đạt mức tối thiểu ⇒ lấy 2 bộ phận: *BP Thiết bị, vật tư, hóa chất chăm sóc xe* · *BP Thiết bị, vật tư lốp*.
  - **Mỗi phòng ban / bộ phận 3–5 nhân viên**, lấy N người đầu trong DB theo chu kỳ cố định 3·4·5 → **43 người**, demo không nhảy số.
  - **Mỗi nhân viên phụ trách 4–5 thị trường** (`EMPLOYEES[].markets`, chia cố định bước nhảy 3 trên vòng 10 tỉnh).
  - Trường `code` của phòng ban (`HN_KD1`, `HN_KDTM`, `KV1`…) lấy nguyên từ DB nhưng **hiện chưa dùng ở đâu** — dự phòng làm nhãn ngắn cho popup.
  - ⚠️ Con số **"591 meeting" ở tài liệu cũ là SAI**: đo lại cả bản trước lẫn sau khi đổi quy mô đều ra **612**.
  - Đổi số thị trường / nhân viên **không làm lệch chỉ tiêu nào**: `demoPick` luôn tiêu thụ đúng 1 số ngẫu nhiên bất kể độ dài mảng, nên chuỗi LCG giữ nguyên — chỉ phân bổ theo thị trường / phòng ban đổi.
- **5 loại meeting**: phát triển thị trường · khảo sát nhu cầu · chăm sóc khách hàng · chốt phương án · **triển khai Dự án**.
- `createdAt` = ngày họp − (1..28) ngày, tính bằng công thức theo số thứ tự phiếu (KHÔNG gọi `demoRnd`) để bổ sung trường này **không làm lệch chuỗi ngẫu nhiên** — mọi số liệu cũ giữ nguyên.

## Hiện thực (code thật, 14/09/2026)

Mockup đã port sang code trên nhánh `tpe-bao-cao-phat-trien-thi-truong-kh` (tách từ `tpe`).

**Đường dẫn màn**: `/assign/report/customer-market-development` — menu *Báo cáo ▸ Phát triển thị
trường - Khách hàng*. Màn `report/meeting-by-market` cũ giữ nguyên.

**Quyền** (3 quyền mới, id 1187-1189):
`Xem báo cáo phát triển thị trường - khách hàng theo tổng công ty / theo công ty / theo phòng ban`.
Không có quyền nào ⇒ chỉ thấy meeting mình chủ trì hoặc mình là thành viên.

**Backend** (`hrm-api`)

| File | Vai trò |
|---|---|
| `database/migrations/2026_09_14_000001_add_province_columns_to_meetings_table.php` | 2 cột `meetings.province_id` / `province_name` |
| `Modules/Assign/Services/MeetingMarketSnapshotService.php` | resolve tỉnh của KH từ ERP, chỉ gọi lúc LƯU phiếu |
| `Modules/Assign/Entities/Meeting/Meeting.php` (`booted()`) | ghi snapshot ở sự kiện `saving` — phủ mọi đường ghi |
| `Modules/Assign/Database/Seeders/BackfillMeetingProvinceSeeder.php` | vá thị trường cho meeting cũ |
| `Modules/Assign/Services/Report/CustomerMarketDevelopmentService.php` | lọc · kỳ · quyền · KH mới · cây N cấp · chỉ tiêu · popup · dữ liệu Excel |
| `Modules/Assign/Http/Controllers/Api/V1/CustomerMarketDevelopmentReportController.php` | 3 endpoint |
| `Modules/Assign/Export/CustomerMarketDevelopmentExport.php` + blade | Excel bảng theo dõi |
| `database/e2e_customer_market_dev_seed.php` | fixture e2e (quyền + tài khoản role rỗng) |

**Endpoint**: `GET assign/report/customer-market-development` · `/drill` · `/export`.

**Frontend** (`hrm-client`) — `pages/assign/report/customer-market-development/`:
`index.vue` · `components/DevelopmentSummary.vue` · `DevelopmentTable.vue` · `DrillCell.vue` ·
`DevelopmentDrillModal.vue`.

**Bộ chọn cấp xem nằm NGOÀI bảng** (sửa 14/09/2026) — mockup đặt trong ô tiêu đề cột "Nội dung
theo dõi" vì dùng `<select>` HTML thuần; màn thật dùng `V2BaseSelect` (select2) thì không đặt
trong `<th>` được: ô cao 32px / vùng nội dung ô tiêu đề 26px, và dropdown render bên trong
`.market-table-wrap` (`overflow-x: auto` cắt cả trục dọc) nên bảng ngắn là bị cắt mất 2 lựa chọn
cuối. Nay là thanh nhỏ canh phải ngay trên bảng, nhãn *Cấp xem*.

**Khối tổng hợp trong popup — LÀM XONG 14/09/2026 (Phase 5)**, đủ luật 0 + luật 3: dòng đầu
*Tổng hợp danh sách đang xem* + nút thu gọn dùng chung khuôn `.rsum-toggle`, **mặc định THU GỌN**
và reset về thu gọn mỗi lần mở popup; mở ra mới dựng 3 hộp KPI (*Tỷ lệ hoàn thành meeting* ·
*KH mới tạo trong kỳ* · *Tỷ lệ meeting huỷ*) + dải chip phân bổ **Thị trường / Phòng ban** bấm được
để lọc nhanh. Popup *KH mới* bỏ hẳn 3 hộp KPI (đều tính trên meeting), chỉ giữ dải chip.
- Ô *KH mới tạo trong kỳ* lấy từ **chỉ tiêu của NHÁNH** (prop `node-metrics`, dòng TỔNG thì là
  `total`), KHÔNG suy từ danh sách meeting đang xem và KHÔNG đổi theo bộ lọc trong popup — khách
  hàng mới không gắn với meeting nào.
- 2 ô tỷ lệ tính trên **tập đang lọc** trong popup.
- ⚠️ Trần chiều cao bảng KHÔNG còn là hằng số `calc(70vh - 120px)`: mỗi trạng thái một chiều cao
  (đóng/mở khối tổng hợp, 1 hay 2 dải chip, popup *KH mới* không có KPI). Nay `syncTableHeight()`
  **đo thật** ngân sách rồi đặt trần — đo trước khi sửa thấy thân popup tràn **9px lúc thu gọn** và
  **21px lúc mở rộng**, tức là 2 thanh cuộn dọc lồng nhau (bẫy mục 3b skill `modal-popup`).
  Gọi từ watcher phải chờ thêm 1 khung hình (`$nextTick` + `requestAnimationFrame`): chỉ `$nextTick`
  thì đo ra số của trạng thái CŨ.

**Bản in** (làm 14/09) đi theo **popup xem trước** (`ReportPrintPreviewModal`) chứ không dựng trang
`/print`, bám skill `print-page` mục 0 và khuôn của màn `prospective-project-results`:
endpoint `print-list-data` + `CustomerMarketDevelopmentPrintService` + 2 blade. Màn chính có nút
*In báo cáo* (2 chế độ), popup chi tiết có nút *In danh sách* — in đúng tập đang lọc trong popup.

**Đã làm bổ sung 14/09**: popup dựng lại trên `V2BaseModal` + `V2BaseTableScroll`; **bộ lọc riêng
trong popup đủ 7 ô** kèm 3 luật ẩn; 16 icon ⓘ; định dạng số đồng nhất 1 chữ số thập phân.

**Định dạng số (sửa Phase 5)**: 5 chỗ còn `toLocaleString('vi-VN')` đã đổi sang **chuẩn số quốc tế**
`1,234.5` theo CLAUDE.md (chốt toàn hệ thống 26/08/2026) — `14,3%` nay là `14.3%`, `1,3 tỷ` nay là
`1.3 tỷ`. Lệnh tự kiểm trong CLAUDE.md đã RỖNG cho màn này.

**2 điểm nghiệp vụ khác mockup vì dữ liệu thật**:
- Phòng ban / Bộ phận lấy theo **hồ sơ NGƯỜI CHỦ TRÌ** (`employee_infos`), KHÔNG dùng
  `meetings.department_id` / `part_id` (đó là cấp tổ chức của người TẠO phiếu).
- **Ghi chú huỷ** nằm ở cột `meetings.cancel_reason` (text cũ đã đổi vai trò), lý do lấy từ
  danh mục qua `cancel_reason_id` — không có cột `cancel_note` như mockup giả định.

## ⚠️ Nhắc khi merge sang nhánh gộp DB

Feature code trên nhánh `tpe` — `customers` nằm Ở **DB ERP khác**, nên cột "KH mới" phải đi 1 query
gộp sang `mysql2` và thị trường phải snapshot xuống `meetings`. **Khi gộp DB thì khách hàng nằm
cùng 1 database ⇒ phải đổi lại cách query** (join thẳng, bỏ `mysql2` / `TpCustomer`), nếu không số
liệu sai âm thầm vì `mysql2` trỏ DB ERP CŨ, id lệch. Chi tiết từng chỗ phải đổi: xem mục
**"NỢ KỸ THUẬT — PHẢI ĐỔI KHI MERGE SANG NHÁNH GỘP DB"** cuối `plan.md`.
Mọi đoạn đụng ERP đều gắn mốc `@TODO-GOPDB` — tìm bằng `grep -rn "@TODO-GOPDB" hrm-api/Modules/Assign`.

## Phân trang — Ở BACKEND (chốt 14/09/2026)

**Nguyên tắc của team: LUÔN phân trang phía BE** (`CLAUDE.md` mục hiệu năng: *"Luôn phân trang,
không trả cả bảng"*). Bản đầu làm ở FE (cắt lát mảng) đã bị bác — ghi lại ở đây để không tái phạm:
cắt ở FE vẫn phải tải cả tập về (payload 4,3 MB), chỉ đỡ được khâu vẽ DOM.

Lý do phải phân trang: tiêu chí **Khách hàng** đẻ 1 dòng cho MỖI khách hàng (kể cả khách mới chưa có
meeting nào) nên kỳ Năm nay ra **3.263 dòng cấp 1**; đo trước khi làm: payload **4,3 MB**, trình
duyệt dựng **46,3s**, bung hết cấp **73,4s**.

### Bảng theo dõi — cắt theo DÒNG CẤP 1, ngay trong `buildTree()`

Tham số: `page` · `per_page` (mặc định **50**, FE cho chọn 20/50/100, BE chặn trần 200).
API trả thêm `pagination: { page, per_page, total }` — `total` là **số dòng cấp 1 của cả kỳ**.

3 luật giữ nguyên nghĩa của bảng:
1. Cắt **sau khi đã sort, TRƯỚC khi dựng nhánh con** → node ngoài trang không tốn CPU dựng con, và
   node trong trang vẫn có **NGUYÊN nhánh con** (không bao giờ cắt cha lìa con).
2. Dòng **TỔNG** và **dải tổng hợp** vẫn tính trên TOÀN kỳ, không theo trang.
3. **STT giữ số thật** (trang 2 bắt đầu từ 51, con là `51.1.1`).

⚠️ `getFlatRowsForExport()` (Excel + bản in) dùng CHUNG `getData()` → phải gọi `getData($request,
false)` để **tắt phân trang**. Quên là file xuất ra chỉ còn 1 trang mà không báo lỗi gì — đã có ca
e2e riêng chặn ("Bản in + Excel vẫn ĐỦ MỌI DÒNG dù màn hình đang phân trang").

### Popup chi tiết — lọc / sắp xếp / phân trang đều ở BE

`GET .../drill` nay trả **1 trang** kèm mọi con số popup cần, vì popup không còn cả tập để tự tính:

| Khoá | Nội dung | Tính trên tập nào |
|---|---|---|
| `rows` | 1 trang dòng | sau lọc + sắp, cắt theo trang |
| `pagination` | `page` · `per_page` (mặc định 20) · `total` | — |
| `summary` | `plan` · `completed` · `cancelled` (2 ô KPI tỷ lệ) | **toàn tập đang lọc** |
| `allocations` | chip Thị trường / Phòng ban, 12 mục mỗi chiều | **toàn tập đang lọc** |
| `filter_options` | tuỳ chọn 7 ô lọc | **tập TRƯỚC bộ lọc popup** |
| `has_part` | có dòng nào thuộc bộ phận không (bỏ cột Bộ phận) | **tập TRƯỚC bộ lọc popup** |

- Bộ lọc riêng của popup mang **tiền tố `p_`** (`p_province_id`, `p_status`…) + ô tìm nhanh `q`,
  tách khỏi bộ lọc của BÁO CÁO. Trùng tên là không còn tính được `filter_options` trên tập gốc nữa
  → chọn 1 phòng ban xong dropdown chỉ còn đúng 1 mục.
- Sắp xếp: `sort` (5 mốc) + `sort_dir`. Hoà thì so thêm `code` cho thứ tự **ổn định giữa các trang**
  — thiếu chốt này thì lật trang là dòng nhảy lung tung.
- Ô tìm nhanh **debounce 300ms** rồi mới gọi API.
- Mọi thao tác lọc / bấm chip / đổi sắp xếp đều **về trang 1**.
- Cờ **`customer_is_new`** cho từng dòng meeting do BE gắn (chip "KH mới"). Trước đây FE so với danh
  sách KH mới mà nó chỉ có sau khi người dùng mở popup "KH mới" ⇒ **chip gần như không bao giờ hiện**.
- **Xuất Excel của popup chuyển hẳn sang BE** (`drill/export`): FE chỉ còn 1 trang nên dựng file ở FE
  là xuất thiếu. Bản in cũng dùng chung `applyDrillFilters()` + `sortDrillRows()` để in **đủ mọi
  dòng của tập đang lọc**, đúng thứ tự đang xem.

### Số đo (cùng máy, cùng dữ liệu — *Năm nay · Khách hàng*)

| | Trước | FE cắt lát (bản bị bác) | **BE phân trang** |
|---|---|---|---|
| Payload API | 4,3 MB | 4,3 MB | **67 KB** |
| Tải + vẽ xong | 46,3s | 1,08s | **0,87s** |
| Bung hết cấp | 73,4s | 0,19s | **0,19s** |
| Số dòng vẽ 1 lúc | 3.264 | 51 | **51** |

⚠️ **Trần chiều cao bảng trong popup phải biết BỎ trần**: thêm thanh phân trang làm ngân sách chiều
cao hụt. Ở khổ **1280×720** (khổ e2e dùng), mở khối tổng hợp thì chỗ còn lại cho bảng chỉ **137px** —
ép trần tối thiểu 180px là đẻ đúng cái lỗi **2 thanh cuộn dọc lồng nhau**. Nay dưới ngưỡng 180px thì
`syncTableHeight()` trả `0` ⇒ `V2BaseTableScroll` bỏ `overflow-y`, cả thân popup thành **một** vùng
cuộn duy nhất. Luật kiểm là **"đúng 1 khối cuộn dọc"**, không bắt buộc phải là khối nào.

## Quyết định chốt thêm 14/09/2026 (Phase 5)

| Việc | Chốt | Lý do |
|---|---|---|
| Bộ lọc màn chính mở sẵn hay thu gọn | **THU GỌN** (giữ nguyên, lệch mockup có chủ ý) | Mockup để nhãn CẠNH ô nên cụm lọc cao 68px; `V2BaseFilterPanel` để nhãn TRÊN ô nên cao 254px. Đo thật: mở sẵn thì bảng tụt y=378 → y=632, số dòng thấy được rơi **18 → 10**. 7/10 màn báo cáo của phân hệ cũng thu gọn. |
| Nhóm "Chưa xác định thị trường" | **GIỮ NGUYÊN TÊN** | Là **31/3208** khách hàng nước ngoài thật sự không có tỉnh/TP bên ERP — dữ liệu đúng, không phải lỗi. Giữ tên để người xem biết đây là nhóm cần bổ sung tỉnh/TP cho khách hàng. |
| Nhánh code đợt bổ sung | **Làm thẳng trên `tpe`** | Feature đã merge, đợt này chỉ sửa FE 4 file. |

## Còn treo

- Ở tiêu chí Khách hàng, **CỘT** Thị trường vẫn hiện dù lặp 1 giá trị (chỉ ô LỌC đã bỏ theo yêu cầu) — user chốt **GIỮ** (nhắc lại 2026-09-13).
- **Chip "KH mới" lặp ở mọi dòng của popup cố định 1 khách hàng** (đo 12/12 dòng): theo nghĩa mới, "KH mới" là thuộc tính của khách hàng chứ không của meeting. Hướng gọn hơn: đưa chip lên **tiêu đề popup** thay vì lặp từng dòng. Chưa làm — user chốt phương án "nhảy sang cột Tên meeting" trước khi đo được con số này.
- Bản in *"Danh sách chi tiết meeting"* của cả báo cáo **vẫn giữ cột Trạng thái / Nhu cầu / Giá trị dự kiến** cho mọi trạng thái — chỉ popup Huỷ mới bỏ. Đúng ý đồ (bản in là danh sách đầy đủ), ghi lại để khỏi tưởng quên.
- ~~Chưa port Vue thật~~ — đã port xong (Phase 4). Responsive: mới đo ở 1920×1080 và 1366×768, chưa đo khổ máy tính bảng / điện thoại.

## Đã xử lý (2026-09-13)

| Việc | Kết quả đo |
|---|---|
| "KH mới" = KH tạo trong kỳ, tính cho người tạo | 12 (tháng) · 20 (quý) · 44 (năm), khớp công thức data demo |
| Bỏ cột *Đã thực hiện* | Bảng còn 9 cột ở màn, bản in và Excel |
| Chip "KH mới" khi cột Khách hàng bị bỏ | Chip hiện ở cột *Tên meeting* (cột thứ 8) |
| Kẹp trần `createdAt` của meeting | Kỳ tương lai: *Lập trong kỳ* = 0 (23/0 và 64/0) |
| Bỏ *Mã meeting* khỏi bản in chi tiết | Bản in 13 cột, không còn "Mã meeting" |
| Popup Huỷ: ngày tạo trước ngày họp + cột Lý do huỷ | 29/29 dòng có lý do, 11 dòng có ghi chú; cột nằm trọn trong khung (1138 → 1363 / 1368px) |
| Cộng dồn cha = con sau khi đổi | **0 sai lệch / 3018 ô** ở cả 3 tiêu chí |
