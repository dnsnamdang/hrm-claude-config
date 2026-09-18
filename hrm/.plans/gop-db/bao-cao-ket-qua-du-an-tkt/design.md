# Báo cáo kết quả thực hiện Dự án TKT trong kỳ — Mockup UI

File mockup: **`bao-cao-ket-qua-du-an-tkt.html`** (standalone, không phụ thuộc thư viện ngoài).

## Mục tiêu

Theo dõi **kết quả thực hiện các Dự án TKT** (dự án tiền khả thi, bảng `prospective_projects`) trong
một kỳ, theo **3 tiêu chí**. Mỗi tiêu chí phải trả lời trọn 3 câu hỏi quản trị:

| Tiêu chí | 3 câu hỏi phải trả lời |
|---|---|
| Phòng ban / Nhân viên | Mỗi phòng ban / nhân viên trong kỳ thực hiện tổng bao nhiêu Dự án TKT? Ở các thị trường nào? Kết quả các dự án đó ra sao? |
| Thị trường | Ở mỗi thị trường Công ty đang triển khai bao nhiêu dự án TKT? Do phòng ban / nhân viên nào phụ trách? Kết quả ra sao? |
| Lĩnh vực Công ty kinh doanh | Công ty đang có Dự án TKT ở các Lĩnh vực / nhóm ngành nào? Do phòng ban nào phụ trách? Kết quả ra sao? |

Câu hỏi 1 được trả lời bằng **cột `Tổng dự án`**, câu hỏi 2 bằng **cấp thứ 2..n của cây** (bung dòng
là thấy), câu hỏi 3 bằng **4 cột kết quả** (`Đang triển khai · Đóng trong kỳ · Thành công · Thất bại`).

## Bối cảnh

- **Style + cách triển khai bám nguyên** mockup `../../bao-cao-phat-trien-thi-truong-khach-hang/bao-cao-phat-trien-thi-truong-khach-hang.html`:
  port NGUYÊN KHỐI `<style>` của màn đó (design tokens navy + teal, `.rsum-*`, `.drill-*`, `#print-area`),
  phần riêng của màn này nằm ở CUỐI khối style dưới nhãn *"BỔ SUNG RIÊNG MÀN DỰ ÁN TKT"*.
- Đã có sẵn trong repo màn `Báo cáo tổng hợp dự án TKT theo Phòng ban - Nhân viên KD`
  (`pages/assign/report/prospective-projects`). Màn đó **GIỮ NGUYÊN**, không đụng tới — báo cáo này
  là feature mới, khác mục tiêu (màn cũ tổng hợp theo phòng ban/nhân viên KD, màn này chấm **kết quả
  đóng / thành công / thất bại theo kỳ** trên 3 trục cắt).

## Tiến trình nội bộ của Dự án TKT (12 bước)

Bảng tiến trình do user cung cấp, id khớp 1:1 với `ProspectiveProject::STATUS` trong code:

| id | Tiến trình | Ý nghĩa nghiệp vụ | Nhóm kết quả |
|---|---|---|---|
| 1 | Đang tạo | Bản nháp, lưu thiếu thông tin, **chưa sinh mã dự án** | **Không lên báo cáo** |
| 2 | Thu thập thông tin dự án | Đã lưu chính thức, đang khảo sát / họp với khách hàng | Đang triển khai |
| 3 | Chờ tiếp nhận làm giải pháp | Đã gửi yêu cầu sang phòng giải pháp, chờ tiếp nhận | Đang triển khai |
| 4 | Đang làm giải pháp | Phòng giải pháp (hoặc chính đơn vị KD nếu tự triển khai) đang xây dựng giải pháp | Đang triển khai |
| 5 | **Trao đổi giải pháp với khách hàng** | Giải pháp đã duyệt nội bộ để đi trao đổi với khách hàng | Đang triển khai |
| 6 | **Lập dự toán** | Khách hàng đã phê duyệt giải pháp và có xác nhận (TH3; TH1+2 bỏ qua bước này) | Đang triển khai |
| 7 | **Thương thảo giá và giải pháp** | Báo giá đã duyệt nội bộ, đang thương thảo giá với khách hàng | Đang triển khai |
| 8 | Thương thảo hợp đồng | Đã chốt giải pháp + báo giá với khách hàng, có file xác nhận | Đang triển khai |
| 9 | Thực hiện hợp đồng | **Đã chốt hợp đồng với khách hàng, có đính kèm file xác nhận** | **Thành công** |
| 10 | Nghiệm thu và thanh lý hợp đồng | Đang nghiệm thu, thanh lý hợp đồng | **Thành công** |
| 11 | Đóng / Không thực hiện dự án | Dự án dừng, có lưu nguyên nhân thất bại, ghi chú, người đóng, thời điểm đóng | **Thất bại** |
| 12 | Kết thúc và lưu trữ | Dự án hoàn tất, chỉ còn để tra cứu | **Thành công** |

⚠️ 3 tiến trình **đổi tên ngày 07/09/2026, code trên nhánh `tpe` CHƯA cập nhật**: id 5 *Đã duyệt giải
pháp* → *Trao đổi giải pháp với khách hàng*; id 6 *Dự toán* → *Lập dự toán*; id 7 *Thương thảo giá* →
*Thương thảo giá và giải pháp*. **Mockup dùng tên MỚI.** Khi làm thật phải sửa `ProspectiveProject::STATUS`
và `pages/assign/prospective-projects/constants.js` — nếu không, nhãn trên báo cáo sẽ lệch nhãn màn danh sách.

## Điều kiện lấy dữ liệu

Kỳ báo cáo là đoạn `[S = đầu kỳ, E = cuối kỳ]`.

**Lấy vào báo cáo** — hợp của 2 trường hợp:

- **TH1 — lập trước kỳ**: dự án lập từ kỳ trước nhưng chưa đóng, tức tại thời điểm `S` trạng thái ≠ Đóng.
- **TH2 — lập trong kỳ**: dự án lập trong `[S, E]`.

**Loại ra:**

- **Dự án cấp cha** (`is_parent_project`) — số của dự án cha là tổng của dự án con, giữ lại sẽ đếm đúp.
- **Mọi dự án còn ở trạng thái *Đang tạo* (id 1)** — bản nháp, chưa sinh mã dự án, **không lên báo cáo**.
  Luật này áp cho **cả TH1 lẫn TH2**, không phân biệt dự án lập từ kỳ nào.

## Kết quả thực hiện — chấm tại thời điểm CUỐI KỲ

3 nhóm **phủ kín và không giao nhau**:

| Nhóm | Điều kiện tại `E` | Tiến trình | Vào cột |
|---|---|---|---|
| **Chuyển đổi thành công** | Dự án đã có **Hợp đồng ở trạng thái CÓ HIỆU LỰC** | **id 9 · 10 · 12** | `Đóng trong kỳ` **và** `Thành công` |
| **Thất bại** | Dự án bị **HUỶ**, có chọn **lý do thất bại** | **id 11** | `Đóng trong kỳ` **và** `Thất bại` |
| **Vẫn tiếp tục triển khai** | Còn ở các tiến trình trước khi có HĐ | **id 2 → 8** | `Đang triển khai` |

**Ràng buộc bất biến** — đúng ở MỌI dòng, mọi cấp, mọi tiêu chí:

```
Tổng dự án     = Đang triển khai + Đóng trong kỳ
Đóng trong kỳ  = Thành công      + Thất bại
```

Mockup phải tự kiểm được 2 đẳng thức này (xem *Kiểm chứng bắt buộc*).

**Mốc "đã có Hợp đồng CÓ HIỆU LỰC" chấm bằng TIẾN TRÌNH NỘI BỘ, không tra sang ERP** (chốt khi duyệt
thiết kế). Bước 9 *Thực hiện hợp đồng* theo định nghĩa nghiệp vụ đã là *"đã chốt hợp đồng với khách
hàng, có đính kèm file xác nhận"*, nên `tiến trình ≥ 9` (trừ id 11) là mốc thành công. Hệ quả tốt:
cả mockup lẫn bản thật đọc **cùng 1 nguồn**, không có nguy cơ báo cáo lệch màn danh sách vì ERP trả
khác. 3 nhóm kết quả vì thế **suy thẳng từ `status`**, không cần bảng lịch sử hay join ERP.

**Quy ước về tỷ lệ:** `Tỷ lệ thành công = Thành công / Đóng trong kỳ` — **không** chia cho `Tổng dự án`.
Dự án còn đang chạy thì chưa thắng cũng chưa thua, đưa vào mẫu số sẽ dìm tỷ lệ của phòng ban có nhiều
dự án dài hơi. Mẫu số = 0 thì hiện `—`, không hiện `0,0%`.

## 3 tiêu chí theo dõi — BẮT BUỘC chọn 1 (không có "Tất cả")

| Nhãn trên select | Các cấp theo dõi trên bảng | Thứ tự cụm cột chiều trong popup |
|---|---|---|
| **Theo Phòng ban** | Phòng ban ▸ **Bộ phận** ▸ Nhân viên ▸ **Thị trường** | dept · team · emp · market · customer |
| **Theo Thị trường** | Thị trường ▸ Phòng ban ▸ **Bộ phận** ▸ Nhân viên | market · dept · team · emp · customer |
| **Theo Lĩnh vực Công ty KD** | Lĩnh vực ▸ Nhóm ngành ▸ Phòng ban | scope · industry · dept · team · emp · customer |

- **Nhãn select để NGẮN** (chốt 09/09/2026): chỉ *Theo Phòng ban / Theo Thị trường / Theo Lĩnh vực
  Công ty KD*, không liệt kê cả chuỗi cấp trong ô select. Chuỗi cấp đầy đủ vẫn đọc được ở 3 chỗ khác:
  tooltip `?` cạnh nhãn ô lọc, dòng `TỔNG` của bảng, và select chọn cấp trong tiêu đề cột.

- Thứ tự cột popup khai báo tường minh ở `CRITERIA[crit].cols`, không suy ra bằng cờ nhị phân.
- **Cấp Thị trường nằm dưới Nhân viên ở tiêu chí 1** chính là câu trả lời cho *"ở các thị trường nào?"*
  — bung dòng nhân viên là thấy ngay danh sách thị trường của người đó kèm kết quả từng thị trường.
- **Tiêu chí Lĩnh vực dừng ở Phòng ban**, không xuống Nhân viên: câu hỏi quản trị chỉ hỏi *"do phòng
  ban nào phụ trách"*. Muốn xem tới nhân viên thì mở popup chi tiết.
- Cấp **Bộ phận chỉ hiện với phòng ban CÓ chia bộ phận**; phòng không chia thì cây nhảy thẳng
  Phòng ban ▸ Nhân viên, KHÔNG đẻ dòng "Chưa phân bộ phận" rỗng.
- Bảng có đúng **1 dòng `TỔNG`** mang tổng cả kỳ, nhãn đổi theo tiêu chí đang xem
  (`PHÒNG BAN / BỘ PHẬN / NHÂN VIÊN / THỊ TRƯỜNG`…).

### Nguồn của từng chiều

| Chiều | Nguồn |
|---|---|
| Phòng ban / Bộ phận / Nhân viên | `main_sale_department_id` / `main_sale_part_id` / `main_sale_employee_id` của dự án |
| **Thị trường** | **Tỉnh/TP của Khách hàng** (`assign/customers/provinces`) — cùng nguồn với báo cáo `meeting-by-market` và mockup mẫu. Mỗi dự án rơi đúng 1 thị trường nên cộng dọc không trùng. KHÔNG dùng `project_address` (đang là text tự do, chưa có `province_id`). |
| Lĩnh vực / Nhóm ngành | `scope_id` (Lĩnh vực Công ty kinh doanh) và `industry_id` (Nhóm ngành) trên chính dự án TKT — KHÔNG phải `customer_scope_id` (đó là *lĩnh vực kinh doanh của khách hàng*, chiều khác) |

## Bộ cột bảng theo dõi (10 cột)

`STT · Nội dung theo dõi · Tổng dự án · Đang triển khai · Đóng trong kỳ · Thành công · Thất bại · Tỷ lệ thành công · Giá trị HĐ · Giá trị dự kiến`

- **Mọi cột số đều cộng được theo cấp** → số dòng cha luôn = tổng dòng con. Không đưa cột đếm
  distinct (số thị trường / số khách hàng) vào bảng — kiểu cột đó không cộng được theo cấp, chỉ nằm
  ở dải tổng hợp. Đây là bài học đã chốt ở mockup mẫu, giữ nguyên.
- **`Dự án lập trước kỳ` / `Dự án lập trong kỳ` KHÔNG vào bảng** mà đẩy lên dải tổng hợp — đúng cách mockup mẫu
  làm với *Lập trước kỳ / Lập trong kỳ*, giữ bảng 10 cột không phải cuộn ngang.
- Bấm **số bất kỳ** (kể cả dòng `TỔNG`) mở popup danh sách dự án đúng lát cắt đó. Cột `Tỷ lệ thành công`
  không bấm được (là số dẫn xuất).
- 2 cột tiền: `Giá trị HĐ` cộng trên **dự án Thành công**, `Giá trị dự kiến` cộng trên **dự án Đang
  triển khai**. Định dạng rút gọn `1.177,5 tỷ` như mockup mẫu.

## Kỳ báo cáo — BẮT BUỘC chọn

`Tháng này (mặc định) · Tháng trước · Quý này · Quý trước · Năm nay · Năm trước · Tuỳ chọn`

Nhãn ô là **"Kỳ theo dõi"**. Không có mục *Tất cả* — mọi chỉ tiêu của báo cáo đều tính theo kỳ
(*tại đầu kỳ · trong kỳ · tại cuối kỳ*) nên bỏ kỳ đi thì không chỉ tiêu nào còn định nghĩa được.

**Bỏ 2 kỳ tương lai** (*Tuần tiếp theo / Tháng tiếp theo*) của mockup mẫu: báo cáo này chấm kết quả
**tại cuối kỳ**, kỳ tương lai sẽ ra bảng toàn "Đang triển khai" — vô nghĩa. Đổi lại thêm các kỳ
*trước* để soát kết quả đã ngã ngũ và so với kỳ hiện tại.

Kỳ *Tuỳ chọn* hiện 2 ô ngày `Từ` / `Đến` như mockup mẫu.

## Dải tổng hợp

Giữ khuôn **2 khối nằm CÙNG 1 HÀNG, mỗi khối 3 ô con xếp NGANG** của mockup mẫu (đã nén để không
ăn 44% chiều cao màn hình). Không có khối KPI riêng.

| Khối | 3 ô con |
|---|---|
| **Dự án TKT trong kỳ** | Tổng dự án · **Dự án lập trước kỳ** · **Dự án lập trong kỳ** |
| **Kết quả thực hiện trong kỳ** | Chuyển đổi thành công · Thất bại · Vẫn tiếp tục triển khai |

- `Dự án lập trước kỳ` + `Dự án lập trong kỳ` = `Tổng dự án` (chia hết, đúng 2 TH lấy dữ liệu).
  Cặp nhãn bổ dọc theo **NGÀY LẬP PHIẾU**, không gọi là "tồn / mở mới" (chốt 09/09/2026) — trùng
  cách gọi *Lập trước kỳ / Lập trong kỳ* của mockup phát triển thị trường.
- `Thành công` + `Thất bại` + `Đang triển khai` = `Tổng dự án` (chia hết, đúng 3 nhóm kết quả).
- Mỗi ô con hiện số to + tỷ lệ % trên tổng, giống mockup mẫu.
- Dòng meta đầu: `Tổng hợp kỳ 01/09/2026 – 30/09/2026 · N dự án · M khách hàng · Giá trị HĐ X tỷ`
  (số khách hàng là **đếm distinct**, đúng chỗ của nó — dải tổng hợp, không phải bảng).
- Header khối **không lặp số to** (số đã nằm ở ô con); có nút *Thu gọn* dùng chung khuôn `.rsum-toggle`.

## Bộ lọc toolbar — THỨ TỰ BÁM TIÊU CHÍ THEO DÕI

Chốt 09/09/2026. **3 ô khung luôn đứng đầu, cố định:**

`Kỳ theo dõi ▸ Công ty ▸ Tiêu chí theo dõi`

2 ô đầu **BẮT BUỘC chọn** và phải nằm **TRƯỚC** ô *Tiêu chí theo dõi*: chúng quyết định **phạm vi dữ
liệu**, không phụ thuộc cách bổ dọc — chọn xong phạm vi rồi mới chọn cách nhìn.

**Các ô sau xếp ĐÚNG THỨ TỰ CẤP của tiêu chí đang xem** (`syncFilterOrder()`), để ô mình cần luôn nằm
ngay sau ô tiêu chí thay vì phải rà ngang cả thanh lọc:

| Tiêu chí | Thứ tự ô lọc |
|---|---|
| Theo Phòng ban | Phòng ban · Bộ phận · Nhân viên · Thị trường · Khách hàng · Tiến trình · Kết quả |
| Theo Thị trường | Thị trường · Phòng ban · Bộ phận · Nhân viên · Khách hàng · Tiến trình · Kết quả |
| Theo Lĩnh vực Công ty KD | Lĩnh vực · Nhóm ngành · Phòng ban · Bộ phận · Nhân viên · Khách hàng · Tiến trình · Kết quả |

- Ô tổ chức không nằm trong cấp của tiêu chí (Bộ phận / Nhân viên ở tiêu chí *Lĩnh vực*) **vẫn giữ**,
  chỉ xếp sau cụm cấp.
- Đảo thứ tự bằng `appendChild` trên phần tử **đã nằm trong DOM** = DI CHUYỂN chứ không dựng lại, nên
  select giữ nguyên giá trị đang chọn và không mất focus.
- **Ô lọc riêng suy từ `dims` của tiêu chí**: chiều nào là cấp theo dõi thì hiện ô lọc của chiều đó.
  ⇒ *Thị trường* hiện ở tiêu chí **Theo Phòng ban** và **Theo Thị trường**; *Lĩnh vực* + *Nhóm ngành*
  chỉ hiện ở tiêu chí **Theo Lĩnh vực**.

### Ô Công ty — BẮT BUỘC chọn

- **Không có mục *Tất cả***, mặc định công ty đầu danh mục. *Xoá lọc* đưa về công ty đầu danh mục,
  KHÔNG về rỗng.
- Hệ quả về số liệu: báo cáo luôn nằm trong **đúng 1 pháp nhân**. Đo trên data demo kỳ 09/2026:
  công ty 1 có **100 dự án**, công ty 2 có **52** — cộng lại đúng **152** của bản cũ (có mục *Tất cả*).
- Danh mục Phòng ban / Bộ phận / Nhân viên ở các ô sau đều thu hẹp theo công ty đang chọn.
- **Bề rộng ô nới riêng 292px** (khuôn chung của toolbar là 150px) và **bỏ tiền tố "CÔNG TY " khi hiển
  thị** — nhãn ô đã là *Công ty*, lặp lại chỉ tốn 61px. Lý do: ô này giờ quyết định phạm vi nên phải
  đọc được trọn tên; ở 150px nó bị cắt còn *"CÔNG TY CỔ PHẦN"*, 2 công ty nhìn y hệt nhau.
  Bề rộng chốt bằng ĐO chứ không ước lượng — tên dài nhất cần 245px chữ, cộng padding và mũi tên
  select là 289px (thử 280px đo lại vẫn thiếu 1px). `title` của ô giữ **tên đầy đủ**, và bản in cũng
  in tên đầy đủ chứ không in tên đã cắt tiền tố.
- Ô **Kết quả** = `Tất cả · Chuyển đổi thành công · Thất bại · Vẫn tiếp tục triển khai` — lọc theo 3
  nhóm. Ô **Tiến trình** lọc theo tiến trình lẻ, chỉ liệt kê **id 2 → 12** (bỏ *Đang tạo* vì trạng
  thái này không bao giờ lên báo cáo, để trong danh sách là ô lọc chết luôn ra 0 dòng).
- Cascade tổ chức Công ty ▸ Phòng ban ▸ Bộ phận ▸ Nhân viên như mockup mẫu.
- *Xoá lọc* đưa cả **cấp đang xem** về mặc định (`Chỉ <cấp gốc>`), không chỉ xoá giá trị ô lọc.

## Chọn cấp xem

Select nằm trong ô tiêu đề cột "Nội dung theo dõi" (đúng chỗ mockup mẫu đặt), nhãn lấy từ
`CRITERIA[crit].head` nên đổi tiêu chí là nhãn đổi theo:

- Tiêu chí Phòng ban/Nhân viên: `Chỉ Phòng ban · Đến Bộ phận · Đến Nhân viên · Tất cả cấp (đến Thị trường)`
- Tiêu chí Thị trường: `Chỉ Thị trường · Đến Phòng ban · Đến Bộ phận · Tất cả cấp (đến Nhân viên)`
- Tiêu chí Lĩnh vực: `Chỉ Lĩnh vực · Đến Nhóm ngành · Tất cả cấp (đến Phòng ban)`

**Hiểu theo TÊN CẤP, không theo độ sâu**: chỉ bung node có con thuộc cấp còn trong phạm vi, nên chọn
*Đến Bộ phận* thì phòng không chia bộ phận dừng ở Phòng ban, không lòi nhân viên ra sớm. Bấm mũi tên
từng dòng vẫn tự do (chỉ đổi `state.expanded`, không đụng `state.level`).

Bản in / Excel **luôn xuất đủ mọi cấp**, không phụ thuộc cấp đang xem trên màn.

## Phân biệt cấp khi bung hết bảng

Port nguyên cách xử lý đã chốt ở mockup mẫu (đừng làm lại từ đầu — bản đầu của màn đó bị user chê rối):

- **Tách nền dòng cha theo TỪNG CẤP**: `d0 #dceaf4` · `d1 #e9f3f9` · `d2 #f2f8fb` (đậm → nhạt).
  KHÔNG dùng 1 rule `--open` chung cho mọi cấp.
- **Vạch cấp bên trái ô tên** — nấc thang 22px, dựng bằng `::before` tuyệt đối (KHÔNG `border-left`
  của `td`, border sẽ nằm ở mép ô chứ không đúng chỗ thụt lề): `d0` 3px `#0a7c88` tại `left:2px`;
  `d1/d2/d3` 2px alpha `.55 / .32 / .18` tại `24 / 46 / 68px`.
- **Kẻ đậm 2px `#b6d8e0` phía trên mỗi dòng cấp 0** để cắt khối.

## Tiêu đề cột

**Viết hoa chữ đầu** (không `text-transform: uppercase`) và **không xuống dòng** (`white-space: nowrap`),
áp cho cả bảng theo dõi lẫn bảng trong popup.

## Thanh tiêu đề

Khuôn navy cao 42px; 2 nút **In báo cáo · Xuất Excel** dồn về **góc phải** (`.topbar__actions`,
`margin-left:auto`), cao 26px, nền trong suốt + viền trắng mờ; nút *Xuất Excel* giữ sắc xanh lá.
Icon info cạnh tiêu đề, hover hiện *Mục tiêu báo cáo*.

## Luật POPUP chi tiết

Port nguyên bộ luật đã chốt của mockup mẫu:

0. **Khối tổng hợp trong popup MẶC ĐỊNH THU GỌN** — `openDrill()` đặt lại `state.drillSumCollapsed = true`
   mỗi lần mở nên popup nào cũng bắt đầu ở trạng thái thu. Ẩn bằng thuộc tính `hidden` trên khối bọc,
   KHÔNG dùng `style.display` (sẽ đè logic tự ẩn của `renderDrillSummary`). Nhãn nút: *"Xem tổng hợp"*
   khi đang thu, *"Thu gọn"* khi đang mở.
1. **Bộ lọc**: đang xem theo đối tượng A thì BỎ ô lọc theo A. Cây lưu `path` → mọi chiều trên path
   đều ẩn ô lọc và xoá giá trị. Cấp đã cố định vẫn dùng để thu hẹp cascade cấp dưới.
2. **Tiêu đề nêu rõ đối tượng**: *"Đang xem &lt;chỉ tiêu&gt; theo &lt;Cấp&gt;: &lt;Tên&gt;"*; node sâu
   thì dòng phụ hiện đường dẫn cấp cha.
3. **Chip phân bổ** — luôn có **Phòng ban** (để trả lời "do phòng ban nào phụ trách") cộng thêm
   2 chiều cơ cấu theo tiêu chí: tiêu chí 1 & 2 dùng **Thị trường + Lĩnh vực**, tiêu chí Lĩnh vực
   dùng **Lĩnh vực + Thị trường**. Chip ẩn theo cùng luật ẩn của bộ lọc, nên popup theo Nhóm ngành
   chỉ còn **Thị trường + Phòng ban**.
   Dải chip **cuộn ngang** trong `.drill-sum` (scrollbar mảnh) khi nhiều mục — đã đo: nội dung rộng
   2313px trong khung 1368px, cuộn tới là thấy chip cuối. Đây là hành vi của khuôn gốc, KHÔNG phải
   chip bị cắt mất.
4. **4 cột NHẬN DẠNG DỰ ÁN dồn lên ngay sau STT** (chốt 09/09/2026):
   `Mã dự án · Tên dự án TKT · Ngày lập dự án · Tiến trình`, rồi mới tới cụm cột chiều, cuối cùng là
   `Kết quả · Lý do thất bại · Giá trị`. Đọc bảng là biết ngay đang nhìn dự án nào và nó đang ở bước
   nào; cụm cột chiều lùi xuống sau vì popup đã cố định phần lớn chúng — tiêu đề popup nói rõ đang xem
   theo đối tượng nào, và chiều nằm trên đường dẫn còn bị bỏ cột hẳn.
   ⚠️ **THAY THẾ** luật cũ *"các chiều theo dõi dồn lên ngay sau STT"*. Cụm cột chiều vẫn giữ đúng thứ
   tự cấp của tiêu chí đang xem, chỉ đổi vị trí cả cụm.
5. **BỎ CỘT của cấp đã cố định** (`drillFixedDims` = các cấp trên path). Popup mở từ dòng `TỔNG` không
   bỏ cột nào.
6. **BỎ CỘT BỘ PHẬN khi popup không có dòng nào thuộc bộ phận** — xét trên TOÀN BỘ dự án của node
   (`drillProjects`), KHÔNG xét theo bộ lọc trong popup, để cột không nhấp nháy khi lọc.
7. **Sắp xếp được** ở 6 cột: Phòng ban · Nhân viên · Thị trường · Lĩnh vực · Ngày lập dự án · Kết quả ·
   Giá trị (cột nào có mặt trong popup thì mọc nút sắp xếp). Bấm tiêu đề:
   tăng → giảm; mở popup mới reset về *Ngày lập dự án* giảm dần. In + Xuất Excel của popup **bám đúng thứ tự
   đang sắp**.
8. **Icon sắp xếp = 2 mũi tên ngược chiều**; cột chưa sắp thì cả 2 mờ (`opacity .3`), cột đang sắp thì
   chiều đang áp tô đậm.
9. Bảng popup + bản in + Excel dùng chung `drillColumns()` nên bám theo cùng lúc.

**Cột danh sách dự án trong popup:**

`STT · Mã dự án · Tên dự án TKT · Ngày lập dự án · Tiến trình · [các chiều theo tiêu chí] · Kết quả · Lý do thất bại · Giá trị (đ)`

- **"Ngày tạo" đổi tên thành "Ngày lập dự án"** (chốt 09/09/2026) — cả ở cột popup lẫn ô tương ứng
  trong drawer (trước ghi *"Ngày lập phiếu"*). Bề rộng cột nới 108 → 132px cho vừa nhãn dài hơn.

- **Mã và Tên tách 2 cột** (không gộp "Mã • Tên"): cả 2 đều cần lọc / tìm / xuất Excel riêng.
- Cột **Khách hàng** nằm trong nhóm cột chiều (`cols` của tiêu chí), không thuộc đuôi cố định.
- **Tiến trình** hiện pill xám kèm số bước (`7 Thương thảo giá và giải pháp`) — 11 tiến trình mà tô
  11 màu thì bảng loang lổ; màu để dành cho 3 nhóm kết quả.
- **Kết quả** hiện badge 3 màu: Thành công (xanh lá) · Thất bại (đỏ) · Đang triển khai (xanh dương).
- **Lý do thất bại** chỉ có giá trị ở dòng Thất bại, còn lại `—`.
- **Giá trị** = Giá trị HĐ với dòng Thành công, Giá trị dự kiến với dòng Đang triển khai (1 cột,
  tránh 2 cột tiền trong đó luôn có 1 cột rỗng).
- **DÒNG THẤT BẠI ĐỂ TRỐNG ô Giá trị** (chốt 09/09/2026), hiện `—` trên màn và ô rỗng trong Excel:
  dự án đã huỷ thì không còn giá trị nào để ghi nhận — không phải doanh số đã ký, cũng không còn là
  doanh số đang theo đuổi. Nhất quán với 2 cột tiền của bảng theo dõi, vốn chỉ cộng trên dự án
  *Thành công* (`Giá trị HĐ`) và dự án *Đang triển khai* (`Giá trị dự kiến`).
  Kéo theo: khoá sắp xếp cột Giá trị của dòng thất bại = 0 để chúng dồn về một đầu, không nằm lẫn
  giữa các dòng có số theo một giá trị KHÔNG hiện ra. Drawer cũng bỏ ô tiền, thay bằng
  *"— (dự án thất bại không ghi nhận giá trị)"*.
- Cột **Tên dự án** gắn chip **"Lập trong kỳ"** cho dự án lập trong kỳ — chip sắc lam, KHÔNG dùng xanh lá
  để không lẫn với badge "Thành công".

## Data demo

- Mốc **`TODAY = 26/09/2026`** — đặt gần CUỐI kỳ mặc định để bảng có đủ cả 3 nhóm kết quả.
- Sinh cố định bằng **LCG có hạt giống** (KHÔNG `Math.random`) → demo không nhảy số giữa 2 lần mở.
- **Danh mục tổ chức lấy lại NGUYÊN BỘ của mockup mẫu** (2 công ty · 10 phòng ban · 43 nhân viên ·
  10 tỉnh/TP · 60 khách hàng) để 2 màn khớp nhau khi user mở song song. Chỉ **1 phòng có bộ phận**
  (*PHÒNG KINH DOANH THƯƠNG MẠI*, 2 bộ phận) — đúng dữ liệu thật, và là ca kiểm tra luật "bỏ cột Bộ phận".
- Thêm **8 Lĩnh vực** và **~20 Nhóm ngành** (mỗi lĩnh vực 2–3 nhóm ngành).
- **493 dự án TKT** sinh ra, rải từ **07/2025 đến 12/2026** (18 tháng) để mọi kỳ trong bộ chọn —
  kể cả *Quý trước* và *Năm trước* — đều có số liệu. Kỳ mặc định (09/2026) gom **152 dự án**.
- **Vòng đời quyết định HÌNH DÁNG báo cáo**, phải chỉnh bằng số chứ không chọn bừa: 85% dự án rồi sẽ
  ngã ngũ, thời gian từ lập phiếu tới lúc đóng 15–150 ngày. Bản đầu đặt 55% / 20–210 ngày cho ra kỳ
  mặc định **239 dự án mà chỉ 9 dự án đóng** — bảng gần như chỉ có cột *Đang triển khai*, không đọc ra
  kết quả gì. Sau khi chỉnh: 152 dự án = 122 đang triển khai + 30 đóng (15 thành công / 15 thất bại).
- Giá trị hợp đồng dự kiến **0,2 – 6 tỷ** mỗi dự án; giá trị HĐ ký lệch giá trị dự kiến 0,82–1,08 lần
  (mô phỏng kết quả thương thảo).
- Bộ sinh chạy theo **NHÂN VIÊN ▸ THỊ TRƯỜNG** (như mockup mẫu): mỗi cặp (nhân viên × thị trường) ép
  ít nhất 1 dự án rơi vào tháng của `TODAY` rồi rải thêm ra các tháng khác ⇒ cấp Thị trường của tiêu
  chí 2 chắc chắn có nhiều nhánh ngay ở kỳ mặc định.
- Mỗi dự án gắn 1 khách hàng ⇒ thị trường suy từ khách hàng, mỗi dự án đúng 1 thị trường.
- Dự án rải đủ **cả 12 tiến trình**, trong đó tiến trình 2→8 chiếm phần lớn (dự án đang chạy), 9/10/12
  cho nhóm Thành công, 11 cho nhóm Thất bại kèm **lý do thất bại** lấy từ danh mục
  `reason_project_failure` (~6 lý do demo: Giá cao hơn đối thủ · Khách hàng dừng đầu tư · Thua thầu ·
  Không đáp ứng kỹ thuật · Khách chọn nhà cung cấp khác · Lý do khác).
- Dự án **cấp cha** và dự án **Đang tạo** vẫn được SINH RA trong data demo rồi mới bị lọc bỏ — để
  kiểm chứng được luật loại trừ, không phải "không sinh nên không lỗi".

## Kiểm chứng bắt buộc trước khi báo hoàn thành

Đo bằng số lấy từ DOM qua Playwright, không nhìn ảnh. Mockup có sẵn hàm tự kiểm
**`window.__TKT_CHECK__()`** — chạy qua cả 3 tiêu chí, duyệt mọi node của cây, trả về danh sách dòng
sai; dùng nó thay vì cộng tay từng dòng bảng.

1. **2 đẳng thức bất biến** đúng ở mọi dòng cha, mọi cấp, cả 3 tiêu chí:
   `Tổng = Đang triển khai + Đóng` và `Đóng = Thành công + Thất bại`.
2. **Số dòng cha = tổng dòng con** ở cả **7 cột cộng được** (Tổng · Đang triển khai · Đóng · Thành công ·
   Thất bại · Giá trị HĐ · Giá trị dự kiến — `Tỷ lệ thành công` là số dẫn xuất, không kiểm kiểu này),
   mọi cấp, cả 3 tiêu chí.
3. **Dòng `TỔNG` của bảng = số ở dải tổng hợp** (Tổng dự án · Thành công · Thất bại · Đang triển khai).
4. `Dự án lập trước kỳ + Dự án lập trong kỳ = Tổng dự án`.
5. **Không có dòng nào là dự án cha hoặc dự án *Đang tạo*** lọt vào bảng / popup — kể cả dự án
   *Đang tạo* lập từ kỳ trước.
5b. **Nhóm kết quả khớp tiến trình**: mọi dòng popup nhóm *Thành công* có tiến trình ∈ {9, 10, 12},
   *Thất bại* = 11, *Đang triển khai* ∈ {2…8}. Không dòng nào mang tiến trình 1.
6. **Luật bỏ cột**: popup theo Bộ phận không còn cột Phòng ban lẫn Bộ phận; popup của phòng không chia
   bộ phận không có cột Bộ phận; popup từ dòng `TỔNG` đủ cột.
7. **Select chọn cấp** ở *Đến Bộ phận* không làm lòi dòng Nhân viên của phòng không chia bộ phận.
8. Đổi tiêu chí → thứ tự cột popup, nhãn select cấp, ô lọc riêng, chip phân bổ đều đổi theo đúng bảng
   khai báo ở trên.

### Kết quả đo — bản dựng ngày 08/09/2026

| Phép đo | Kết quả |
|---|---|
| `__TKT_CHECK__()` | `ok: true` — **0 dòng sai** trên **535 node** (dp 178 · mk 223 · sc 134), gồm cả 2 đẳng thức bất biến và phép cha = tổng con trên 9 trường |
| Dòng `TỔNG` vs dải tổng hợp | 152 / 15 / 15 / 122 — khớp tuyệt đối |
| Lập trước kỳ + Lập trong kỳ | 119 + 33 = 152 ✔ |
| Rò rỉ dữ liệu bị loại | 9 dự án cha + 20 bản nháp *Đang tạo* đều bị loại, **0 rò rỉ** |
| Nhóm kết quả vs tiến trình | 0 sai; mọi dòng *Thất bại* đều có lý do; kỳ mặc định phủ đủ tiến trình 2→12 |
| Bỏ cột — popup theo Bộ phận | mất cột *Phòng ban* + *Bộ phận*, ẩn đúng 2 ô lọc tương ứng |
| Bỏ cột — popup phòng không chia bộ phận | mất cột *Bộ phận* |
| Bỏ cột — popup theo Nhóm ngành | mất cột *Lĩnh vực* + *Nhóm ngành*, ẩn ô lọc *Lĩnh vực* (luật industry ⇒ scope) |
| Popup từ dòng `TỔNG` | đủ 13 cột, không bỏ cột nào |
| Select cấp *Đến Bộ phận* | 10 phòng ban + đúng 2 bộ phận, **không lòi dòng nhân viên nào** |
| Kẹp cấp khi đổi tiêu chí | đang ở cấp 3 (tiêu chí 4 cấp) → đổi sang *Lĩnh vực* (3 cấp) tự kẹp về cấp 2 |
| Lọc *Kết quả = Thất bại* | 15 / 15 lost, open 0, won 0 |
| Lọc *Tiến trình = 9* | 7 dự án, 100% nhóm Thành công |
| Bản in bảng theo dõi | 179 dòng = đủ MỌI cấp, dù trên màn đang ở cấp 0 (10 dòng) |
| Xuất Excel | 10 cột đúng nhãn, 180 dòng, file `Bao-cao-ket-qua-du-an-TKT.xls` |
| In / Excel của popup theo thứ tự đang sắp | thứ tự 5 dòng đầu trùng khớp bảng trên màn |
| Dòng thất bại không có giá trị | 15/15 dòng hiện `—` trên màn · 0/15 còn số trong Excel · 0/15 còn số trên bản in · drawer bỏ ô tiền |
| Bố cục | `scrollWidth - clientWidth = 0` (không cuộn ngang trang); bảng phải 1557px < viewport 1600px |
| Mọi kỳ đều có số liệu (bản trước khi bắt buộc chọn Công ty) | Tháng này 152 · Tháng trước 138 · Quý này 187 · Quý trước 171 · Năm nay 407 · Năm trước 149 |
| Thứ tự ô lọc đổi theo tiêu chí | 3 ô khung đứng đầu ở cả 3 tiêu chí; cụm cấp xếp đúng `dims` (dp: Phòng ban→Bộ phận→Nhân viên→Thị trường · mk: Thị trường→Phòng ban→… · sc: Lĩnh vực→Nhóm ngành→Phòng ban) |
| Công ty bắt buộc | select 2 mục, không có *Tất cả*; c1 = 100 dự án · c2 = 52 → **cộng đúng 152** của bản cũ |
| Cascade theo công ty | chọn công ty 2 thì ô Phòng ban chỉ còn 4 phòng của công ty đó |
| *Xoá lọc* | về công ty đầu danh mục · kỳ *Tháng này* · tiêu chí *Theo Phòng ban* · cấp 0 |
| Tên công ty không bị cắt | tên dài nhất 245px ≤ vùng chữ 256px, **cả 2 mục hiện đủ**; toolbar vẫn 68px, không cuộn ngang trang |

## Còn treo

- **Nguồn 2 cột tiền chưa chốt** — mockup dùng số demo. Khi làm plan implement phải chỉ rõ: `Giá trị HĐ`
  lấy tổng giá trị hợp đồng ERP hay lấy `expected_contract_amount` của phiếu TKT, và `Giá trị dự kiến`
  lấy `expected_contract_amount` hay `estimated_budget`. User sẽ chỉ định ở bước đó.
  → **Đã chốt** ở mục *Quyết định đã chốt khi lên plan implement* bên dưới; xem thêm "Còn treo sau khi
  code xong" cuối file — giá trị HĐ vẫn `—` ở phase 1 vì chưa có hợp đồng HRM.
- **Trạng thái tại thời điểm `S` cần bảng log chuyển tiến trình — đã có hướng, chưa làm ở mockup.**
  Điều kiện TH1 hỏi *"tại đầu kỳ trạng thái ≠ Đóng"*, tức cần trạng thái **quá khứ**, trong khi cột
  `status` chỉ giữ trạng thái **hiện tại**. User đã chốt hướng: **xây bảng logs lưu thời điểm chuyển
  tiến trình của dự án TKT**, khi đó báo cáo mới chấm đúng kỳ quá khứ. Việc này thuộc bước implement,
  **mockup không giải quyết** — mockup gắn thẳng vào mỗi dự án demo một mốc `statusAt(S)` sinh sẵn để
  luật TH1 chạy đúng và kiểm chứng được, chứ không suy từ `closed_at`.
  → **Đã làm ở Task 4**: `statusAtBulk()` đọc `prospective_project_status_logs` (bảng + hook ghi log
  đã có sẵn từ trước, không phải xây mới) — 1 query gộp, không N+1.
- **3 tiến trình đổi tên 07/09/2026 chưa vào code** (id 5 · 6 · 7) — mockup dùng tên mới, code nhánh
  `tpe` còn tên cũ. Phải sửa `ProspectiveProject::STATUS` + `prospective-projects/constants.js` khi
  làm thật, nếu không nhãn báo cáo lệch nhãn màn danh sách.
- Chưa port Vue thật; chưa responsive.

## Đối chiếu Vue thật với mockup (nghiệm thu Task 17 — 13/09/2026)

Đo bằng số lấy từ DOM ở cả 2 bên (`http://127.0.0.1:3000/assign/report/prospective-project-results`
vs mockup mở qua `http://127.0.0.1:8732`, sau đó re-verify lại ở Task 18 qua cổng `8731`).

**6/8 điểm khớp tuyệt đối:** số cột bảng theo dõi (10 = 10) · nhãn cột · nhãn select chọn cấp ở cả
3 tiêu chí · thụt lề + vạch cấp (2/24/46/68px) · nền dòng cha 3 cấp (`#dceaf4/#e9f3f9/#f2f8fb`) ·
không cuộn ngang trang.

**2 chỗ lệch — đã xử lý trong Task 17, verify lại ở Task 18:**

1. **Thứ tự ô lọc** — bản Vue đầu tiên đặt cặp ô `Từ ngày`/`Đến ngày` (con của ô *Kỳ theo dõi*, chỉ
   hiện khi chọn *Tuỳ chọn*) sau cụm `Công ty`/`Tiêu chí theo dõi`; mockup + màn gốc
   `potential-customer-care` đặt cặp ô ngày **ngay sau** ô Kỳ sinh ra nó. Đã sửa `index.vue` đưa cặp
   ô ngày lên ngay sau Kỳ theo dõi (trước Công ty/Tiêu chí) + cập nhật kỳ vọng `FIELD_ORDER` của ca
   e2e #4 cho khớp. Verify lại ở Task 18 bằng `document.querySelectorAll('[data-dim]')` (đọc thuộc
   tính `dataset.dim` theo đúng thứ tự DOM) ở cả 3 tiêu chí — khớp mockup **tuyệt đối** cả 3:
   - Theo Phòng ban: `period · company · criteria · department · part · employee · province ·
     customer · status · result`
   - Theo Thị trường: `period · company · criteria · province · department · part · employee ·
     customer · status · result`
   - Theo Lĩnh vực: `period · company · criteria · scope · industry · department · part · employee ·
     customer · result`
2. **Bề rộng ô Công ty** — mockup demo chốt **292px** (đo trên tên công ty demo dài nhất). Dữ liệu
   thật có tên công ty dài hơn (`CN HẢI PHÒNG - CÔNG TY CP CÔNG NGHỆ THIẾT BỊ TÂN PHÁT`) nên đo lại
   và cố định **340px** (`getBoundingClientRect().width` đo tại Task 18 = đúng 340px). Đây là điều
   chỉnh **có chủ đích theo dữ liệu thật**, không phải lệch ngoài ý muốn — nguyên tắc "đo bằng Range
   trên tên dài nhất, không ước lượng" ở mục *Ô Công ty* phía trên vẫn giữ nguyên, chỉ đổi input đo
   từ demo sang thật.

Không phát sinh lệch mới nào khác khi re-verify ở Task 18.

## Ghi chú deploy (bắt buộc cho môi trường khác)

Đúng 3 bước, theo thứ tự:

1. `php artisan migrate` — chỉ 1 migration mới của feature này:
   `2026_09_13_000001_fix_backfill_prospective_project_status_logs` (vá log tiến trình cho dự án
   Thất bại lập trước 18/05/2026, idempotent — chạy lại không đẻ thêm dòng).
2. **Insert thủ công 3 quyền `1184`/`1185`/`1186`** (theo cấp Tổng công ty / Công ty / Phòng ban) rồi
   gán vào `role_has_permissions` — bảng này cần thêm cột `company_id` khi insert.
   ⚠️ **TUYỆT ĐỐI KHÔNG chạy `PermissionsTableSeeder`** để nạp 3 quyền này — seeder đó **truncate cả
   bảng `permissions`**, sẽ xoá sạch toàn bộ quyền hiện có của hệ thống.
3. Deploy code BE (`hrm-api`) + FE (`hrm-client`) như bình thường. **Không có cron job mới**, không
   có queue/job nền nào phải bật thêm.

## Còn treo sau khi code xong (13/09/2026 — Task 18)

1. **Giá trị hợp đồng vẫn treo** — cột `Giá trị HĐ` hiện `—` ở **mọi dòng** vì chưa có nguồn hợp đồng
   HRM lập từ báo giá HRM (xem mục *Giá trị hợp đồng — TREO LẠI* phía trên). Khi nguồn đó có, sửa
   đúng **1 hàm** `contractAmountFor()` trong `ProspectiveProjectResultReportService.php`, không phải
   rà lại service/print/Excel.
2. **Dự án nhóm Thành công lập trước 18/05/2026 bị khai SAI kỳ, không chỉ "kém chính xác"**:
   backfill gốc sinh đúng 1 dòng log `changed_at = created_at, status_to = trạng thái hiện tại`. Với
   nhóm Thành công (9/10/12), báo cáo vì thế hiểu là *"thắng ngay ngày lập"* ⇒ (a) bị tính vào
   *Thành công* của **kỳ chứa ngày lập**, và (b) `status_at(S)` đã đóng nên dự án **biến mất khỏi mọi
   kỳ** nằm giữa ngày lập và ngày đóng thật. Migration chỉ vá được nhóm Thất bại vì chỉ nhóm đó có
   `closed_at`; báo cáo chỉ chính xác tuyệt đối với dự án lập từ 18/05/2026 trở đi.
   ⚠️ Trước khi bàn giao production, chạy
   `SELECT COUNT(*) FROM prospective_projects WHERE created_at < '2026-05-18' AND status IN (9,10,12);`
   để biết số dự án bị ảnh hưởng.
3. **`expected_contract_amount` khuyết 42%** — ô "Giá trị HĐ kỳ vọng" trên phiếu TKT không bắt buộc
   nhập, nên cột `Giá trị dự kiến` của nhóm Đang triển khai để trống ở gần nửa số dự án. Không có
   cách suy bù (đã chốt không dùng `estimated_budget` thay thế).
4. **`components/V2BaseTableScroll.vue` port trùng nhánh** — component này cũng đã được port sẵn vào
   `gop_db` và `permiss_manager`. Merge nhánh này vào `tpe` (rồi `tpe` vào các nhánh kia, hoặc ngược
   lại) sẽ gặp **conflict add/add** đúng tại file này. Nội dung 2 bên giống hệt nhau (cùng port từ 1
   nguồn) nên lấy bản nào cũng được, không cần merge thủ công từng dòng.
5. **SRS + testcase chưa làm** — tạo khi được yêu cầu, dùng skill `srs-documenter` +
   `testcase-documenter`.

---

## Quyết định đã chốt khi lên plan implement

### 1. Cột `Giá trị` — nguồn tiền (chốt 13/09/2026)

Thay cho mục *Còn treo → Nguồn 2 cột tiền*. Giá trị của một dự án chấm theo **nhóm kết quả**:

| Nhóm kết quả | Tiến trình | Giá trị lấy từ |
|---|---|---|
| **Thành công** | 9 · 10 · 12 | **Giá trị HỢP ĐỒNG** |
| **Đang triển khai** | 2 → 8 | **Giá trị kỳ vọng** — `prospective_projects.expected_contract_amount` |
| **Thất bại** | 11 | **Không hiển thị** (giữ nguyên luật đã chốt 09/09/2026) |

**Bắt buộc có icon ⓘ cạnh tiêu đề cột `Giá trị`** (và 2 cột tiền của bảng theo dõi) nêu đúng 3 dòng
trên — nếu không, người đọc không hiểu vì sao cùng một cột mà 3 dòng lấy 3 nguồn khác nhau.
Dùng khuôn `.claude/skills/info-icon-tooltip/SKILL.md` (`ri-information-line` 14px `#94a3b8` +
`b-popover custom-class="info-popover"`).

### 2. ⚠️ Giá trị hợp đồng — TREO LẠI, phase 1 chưa có số

**KHÔNG dùng hợp đồng ERP.** User đang phát triển **hợp đồng HRM lập từ báo giá HRM**; báo cáo này sẽ
đọc nguồn đó khi nó xong.

Hiện trạng đã khảo sát (13/09/2026):

- Chưa có entity hợp đồng bán nào trong `Modules/Assign/Entities/` (`SettlementContract` là thanh lý,
  `TpWrServiceContract` là HĐ dịch vụ bảo hành) — **nguồn chưa tồn tại**.
- HĐ ERP `buy_contract2` (923 dòng) **không có cột nào trỏ về dự án TKT**; cột
  `prospective_project_id` chỉ có ở 8 bảng, không bảng hợp đồng nào. Hướng cũ
  `.plans/hrm-quotation-to-erp-contract/` (lập HĐ ERP từ báo giá HRM, đã thêm
  `quotations.erp_firm_contract_id`) **bị thay thế bởi quyết định này**.

**Hệ quả phải thiết kế theo:**

- Dự án nhóm *Thành công* **chưa có giá trị** ở phase 1 → ô `Giá trị` hiện `—`, ô Excel rỗng.
- Cột `Giá trị HĐ` của bảng theo dõi vì thế **tạm luôn bằng 0** ở mọi dòng.
- BE **bắt buộc tách riêng 1 điểm nối** (vd `contractAmountFor(ProspectiveProject $p): ?float`) trả
  `null` ở phase 1. Khi hợp đồng HRM xong thì chỉ sửa đúng hàm đó, không phải rà lại cả service,
  bản in và Excel.

---

## Bổ sung sau review tổng (14/09/2026)

### Lỗi drill key — bài học về giới hạn của phép tự kiểm

`buildLevel()` ở nhánh **phòng ban không chia bộ phận** trước đây truyền `parentKey` **trần** xuống
cấp sau, không ghi dấu việc đã bỏ qua cấp Bộ phận. `applyDrillKey()` chỉ lọc AND trên các chiều **có
mặt** trong key ⇒ key `dept:5+emp:88` khớp **cả** dự án có bộ phận lẫn không có bộ phận của nhân viên
đó. Người dùng bấm số `1` trên bảng, popup mở ra `3` dự án; 2 dự án thừa đã được đếm ở node `part:9`
bên trên nên **bị liệt kê ở 2 popup khác nhau**. Excel và bản in chi tiết sai theo.

**Sửa:** gắn `part:0` vào key khi đẩy xuống cấp sau (`applyDrillKey()` quy `(int) null === 0` nên
`part:0` đúng nghĩa *"không thuộc bộ phận nào"*).

⚠️ **Điều đáng ghi nhớ nhất:** bảng theo dõi **vẫn đúng** trong suốt thời gian có lỗi — cả 2 đẳng
thức bất biến lẫn phép *cha = tổng con* đều xanh. Lỗi nằm ở **đường từ bảng sang popup**, mà toàn bộ
hệ tự kiểm chỉ canh **bảng**, không canh **cầu nối**. 21 ca e2e không ca nào bắt được.

Đã bổ sung **ca 10**: duyệt nhiều dòng ở nhiều cấp × 2 tiêu chí, mỗi dòng so **số vừa bấm trên bảng =
`total` của popup**. Ca này chặn cả **lớp** lỗi, không chỉ một ca cụ thể — nguyên tắc nên áp cho mọi
màn báo cáo có drill-down.

### Ô Công ty — mặc định là công ty của user (chốt 14/09/2026)

Giữ nguyên **bắt buộc chọn**, **không** có mục *Tất cả công ty*. Chỉ đổi **giá trị mặc định**:
`companies[0]` (công ty đầu danh mục theo tên) → **công ty của user đang đăng nhập**.

Lý do: `companies[0]` không liên quan gì tới người đang xem, nên user mở màn ra số của **một pháp
nhân khác công ty mình**, và bấm *Xoá lọc* cũng nhảy sang pháp nhân đó.

BE trả `default_company_id` trong `filter-options`, clamp qua `clampCompanyId()` có sẵn. Ca biên:
công ty trong hồ sơ user không nằm trong danh sách được phép (hồ sơ lệch / công ty đã ngừng hoạt
động) thì **rơi về công ty đầu danh mục** — ô này bắt buộc nên để rỗng là màn chết. FE giữ
`companies[0]` làm phương án dự phòng phòng khi chạy với BE chưa có trường mới.

### Nhãn cột popup — về đúng mockup

`Tỉnh/TP` → **`Thị trường`** (nhãn cũ còn bất nhất **ngay trong cùng popup**: ô lọc và nhóm chip phân
bổ đều gọi là *Thị trường*), `Tên dự án` → **`Tên dự án TKT`**, `Ngày lập` → **`Ngày lập dự án`**,
`Nhân viên` → **`Nhân viên phụ trách`**.
⚠️ Phải sửa **đồng thời** `COLUMN_LABELS` (BE) và `COLUMN_DEFS` (FE) — bản in và Excel lấy nhãn từ BE,
sửa lệch 1 bên là 2 nơi hiển thị khác nhau.

### Lỗi CSS toàn cục phát hiện được (ngoài phạm vi feature)

`hrm-client/assets/scss/custom-theme.scss` dòng 166:
`input:not(:placeholder-shown) + label { top: 0; transform: translateY(-50%) scale(1) }` **thiếu tiền
tố `.mate-field`**, trong khi rule ngay trên nó (dòng 161) có scope đúng. Radio/checkbox không có
placeholder nên `:not(:placeholder-shown)` **luôn đúng** ⇒ rule áp nhầm lên **mọi**
`.custom-control-label` toàn app (~28 file), kéo nhãn lệch ~10px so với nút tròn.

Đây chính là lý do màn CSKH né bằng cách viết markup thô (comment đầu
`potential-customer-care/components/PrintOptionsModal.vue` dòng 11-12) — **không phải nợ kỹ thuật mà
là workaround có chủ đích**.

Màn này **không né bằng markup thô** (vi phạm luật *"màn mới phải dùng `V2Base*`"* và mất phần nâng
cấp về sau của component dùng chung) mà **giữ `V2BaseRadio` + hoá giải cục bộ bằng CSS `scoped`**:
`::v-deep .custom-control-label { top: auto; transform: none }`. Đo sau khi sửa: `input.top ==
label.top`, tâm dấu tròn vs tâm dòng chữ lệch **0,525px**.

⚠️ Sửa rule toàn cục nằm **ngoài phạm vi** feature này (cần hồi quy ~28 màn) và **user đã chốt hoãn
từ 24/08/2026**. Ghi lại để xử lý riêng.
