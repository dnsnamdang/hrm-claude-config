# BÁO CÁO KẾT QUẢ THỰC HIỆN DỰ ÁN TKT TRONG KỲ — LOGIC THIẾT KẾ

Bản tổng hợp toàn bộ logic nghiệp vụ của báo cáo, gom từ các quyết định đã chốt trong quá trình thiết
kế mockup. Đây là bản **logic**, không nói chuyện giao diện chi tiết — phần trình bày/UI nằm ở
`design.md`, bản dựng thật nằm ở `bao-cao-ket-qua-du-an-tkt.html`.

---

## 1. MỤC TIÊU

Theo dõi **kết quả thực hiện các Dự án TKT** (dự án tiền khả thi, bảng `prospective_projects`) trong
một kỳ, cắt theo **3 tiêu chí**. Mỗi tiêu chí phải trả lời trọn 3 câu hỏi quản trị:

| Tiêu chí | 3 câu hỏi phải trả lời |
|---|---|
| **Theo Phòng ban / Nhân viên** | Mỗi phòng ban / nhân viên trong kỳ thực hiện tổng bao nhiêu Dự án TKT? Ở các thị trường nào? Kết quả các dự án đó ra sao? |
| **Theo Thị trường** | Ở mỗi thị trường Công ty đang triển khai bao nhiêu dự án TKT? Do phòng ban / nhân viên nào phụ trách? Kết quả ra sao? |
| **Theo Lĩnh vực Công ty kinh doanh** | Công ty đang có Dự án TKT ở các Lĩnh vực / nhóm ngành nào? Do phòng ban nào phụ trách? Kết quả ra sao? |

Cách báo cáo trả lời 3 câu hỏi:

- **Câu 1 (bao nhiêu dự án)** → cột `Tổng dự án`.
- **Câu 2 (ở đâu / ai phụ trách)** → các **cấp thứ 2..n của cây**, bung dòng ra là thấy.
- **Câu 3 (kết quả ra sao)** → 4 cột kết quả `Đang triển khai · Đóng trong kỳ · Thành công · Thất bại`.

---

## 2. TIẾN TRÌNH NỘI BỘ CỦA DỰ ÁN TKT (12 BƯỚC)

id khớp 1:1 với `ProspectiveProject::STATUS`.

| id | Tiến trình | Ý nghĩa nghiệp vụ | Nhóm kết quả |
|---|---|---|---|
| 1 | Đang tạo | Bản nháp, lưu thiếu thông tin, chưa sinh mã dự án | **Không lên báo cáo** |
| 2 | Thu thập thông tin dự án | Đã lưu chính thức, đang khảo sát / họp với khách hàng | Đang triển khai |
| 3 | Chờ tiếp nhận làm giải pháp | Đã gửi yêu cầu sang phòng giải pháp, chờ tiếp nhận | Đang triển khai |
| 4 | Đang làm giải pháp | Phòng giải pháp (hoặc chính đơn vị KD nếu tự triển khai) đang xây dựng giải pháp | Đang triển khai |
| 5 | Trao đổi giải pháp với khách hàng | Giải pháp đã duyệt nội bộ để đi trao đổi với khách hàng | Đang triển khai |
| 6 | Lập dự toán | Khách hàng đã phê duyệt giải pháp và có xác nhận (TH3; TH1+2 bỏ qua bước này) | Đang triển khai |
| 7 | Thương thảo giá và giải pháp | Báo giá đã duyệt nội bộ, đang thương thảo giá với khách hàng | Đang triển khai |
| 8 | Thương thảo hợp đồng | Đã chốt giải pháp + báo giá với khách hàng, có file xác nhận | Đang triển khai |
| 9 | Thực hiện hợp đồng | Đã chốt hợp đồng với khách hàng, có đính kèm file xác nhận | **Thành công** |
| 10 | Nghiệm thu và thanh lý hợp đồng | Đang nghiệm thu, thanh lý hợp đồng | **Thành công** |
| 11 | Đóng / Không thực hiện dự án | Dự án dừng, có lưu nguyên nhân thất bại, ghi chú, người đóng, thời điểm đóng | **Thất bại** |
| 12 | Kết thúc và lưu trữ | Dự án hoàn tất, chỉ còn để tra cứu | **Thành công** |

> ⚠️ **3 tiến trình đổi tên ngày 07/09/2026 mà code chưa cập nhật**: id 5 *Đã duyệt giải pháp* →
> *Trao đổi giải pháp với khách hàng*; id 6 *Dự toán* → *Lập dự toán*; id 7 *Thương thảo giá* →
> *Thương thảo giá và giải pháp*. Báo cáo dùng **tên mới**, nên khi làm thật phải sửa
> `ProspectiveProject::STATUS` và `prospective-projects/constants.js`, nếu không nhãn trên báo cáo sẽ
> lệch nhãn màn danh sách.

---

## 3. ĐIỀU KIỆN LẤY DỮ LIỆU

Kỳ báo cáo là đoạn `[S = đầu kỳ, E = cuối kỳ]`.

### 3.1. Lấy vào báo cáo — hợp của 2 trường hợp

- **TH1 — lập trước kỳ**: dự án lập từ kỳ trước nhưng chưa đóng, tức tại thời điểm `S` trạng thái ≠ Đóng.
- **TH2 — lập trong kỳ**: dự án lập trong `[S, E]`.

### 3.2. Loại ra

- **Dự án cấp cha** (`is_parent_project`) — số của dự án cha là tổng của các dự án con, giữ lại sẽ
  đếm đúp.
- **Mọi dự án còn ở tiến trình *Đang tạo* (id 1)** — bản nháp, chưa sinh mã dự án. Luật này áp cho
  **cả TH1 lẫn TH2**, không phân biệt dự án lập từ kỳ nào.

---

## 4. CHẤM KẾT QUẢ — TẠI THỜI ĐIỂM CUỐI KỲ

3 nhóm **phủ kín và không giao nhau**, suy thẳng từ tiến trình của dự án tại `E`:

| Nhóm | Điều kiện | Tiến trình | Vào cột |
|---|---|---|---|
| **Chuyển đổi thành công** | Dự án đã có Hợp đồng ở trạng thái CÓ HIỆU LỰC | 9 · 10 · 12 | `Đóng trong kỳ` **và** `Thành công` |
| **Thất bại** | Dự án bị HUỶ, có chọn lý do thất bại | 11 | `Đóng trong kỳ` **và** `Thất bại` |
| **Vẫn tiếp tục triển khai** | Còn ở các tiến trình trước khi có hợp đồng | 2 → 8 | `Đang triển khai` |

### 4.1. Mốc "đã có hợp đồng có hiệu lực"

**Chấm bằng TIẾN TRÌNH NỘI BỘ, không tra sang hợp đồng bên ERP.** Bước 9 *Thực hiện hợp đồng* theo
định nghĩa nghiệp vụ đã là *"đã chốt hợp đồng với khách hàng, có đính kèm file xác nhận"*, nên
`tiến trình ≥ 9` (trừ id 11) chính là mốc thành công.

Lợi ích: báo cáo và màn danh sách đọc **cùng một nguồn**, không có nguy cơ lệch nhau vì ERP trả khác.

### 4.2. Hai đẳng thức bất biến

Đúng ở **mọi dòng, mọi cấp, cả 3 tiêu chí** — dùng để tự kiểm số liệu:

```
Tổng dự án     = Đang triển khai + Đóng trong kỳ
Đóng trong kỳ  = Thành công      + Thất bại
```

Và ở dải tổng hợp:

```
Dự án lập trước kỳ + Dự án lập trong kỳ = Tổng dự án
```

### 4.3. Tỷ lệ thành công

```
Tỷ lệ thành công = Thành công ÷ Đóng trong kỳ
```

**KHÔNG** chia cho `Tổng dự án`: dự án còn đang chạy thì chưa thắng cũng chưa thua, đưa vào mẫu số sẽ
dìm tỷ lệ của phòng ban có nhiều dự án dài hơi. Mẫu số = 0 thì hiện `—`, không hiện `0,0%`.

---

## 5. CÁC CHIỀU DỮ LIỆU VÀ NGUỒN

| Chiều | Nguồn |
|---|---|
| Phòng ban / Bộ phận / Nhân viên | `main_sale_department_id` / `main_sale_part_id` / `main_sale_employee_id` của dự án |
| **Thị trường** | **Tỉnh/TP của Khách hàng** (`assign/customers/provinces`) — cùng nguồn với báo cáo `meeting-by-market`. Mỗi dự án rơi đúng 1 thị trường nên cộng dọc không trùng. KHÔNG dùng `project_address` (đang là text tự do, chưa có `province_id`). |
| Lĩnh vực / Nhóm ngành | `scope_id` và `industry_id` **trên chính dự án TKT** — KHÔNG phải `customer_scope_id` (đó là *lĩnh vực kinh doanh của khách hàng*, chiều khác) |
| Khách hàng | `customer_id` |
| Lý do thất bại | `closed_reason_id` → danh mục `reason_project_failure` |

---

## 6. KỲ BÁO CÁO — BẮT BUỘC CHỌN

`Tháng này (mặc định) · Tháng trước · Quý này · Quý trước · Năm nay · Năm trước · Tuỳ chọn`

- **Không có mục *Tất cả***: mọi chỉ tiêu đều tính theo kỳ (*tại đầu kỳ · trong kỳ · tại cuối kỳ*),
  bỏ kỳ đi thì không chỉ tiêu nào còn định nghĩa được.
- **Không có kỳ tương lai**: báo cáo chấm kết quả tại **cuối kỳ**, kỳ tương lai sẽ ra bảng toàn
  *Đang triển khai* — vô nghĩa. Đổi lại có đủ các kỳ *trước* để soi kết quả đã ngã ngũ.

---

## 7. BỘ LỌC

### 7.1. Ba ô khung luôn đứng đầu, cố định

```
Kỳ theo dõi  ▸  Công ty  ▸  Tiêu chí theo dõi
```

2 ô đầu **BẮT BUỘC chọn** và phải nằm **trước** ô *Tiêu chí theo dõi*: chúng quyết định **phạm vi dữ
liệu**, không phụ thuộc cách bổ dọc — chọn xong phạm vi rồi mới chọn cách nhìn.

**Ô Công ty bắt buộc chọn**, không có mục *Tất cả*, mặc định công ty đầu danh mục ⇒ báo cáo luôn nằm
trong **đúng 1 pháp nhân**. Danh mục Phòng ban / Bộ phận / Nhân viên ở các ô sau đều thu hẹp theo công
ty đang chọn. Nút *Xoá lọc* đưa về công ty đầu danh mục, KHÔNG về rỗng.

### 7.2. Các ô còn lại xếp theo đúng thứ tự cấp của tiêu chí đang xem

| Tiêu chí | Thứ tự ô lọc |
|---|---|
| Theo Phòng ban | Phòng ban · Bộ phận · Nhân viên · Thị trường · Khách hàng · Tiến trình · Kết quả |
| Theo Thị trường | Thị trường · Phòng ban · Bộ phận · Nhân viên · Khách hàng · Tiến trình · Kết quả |
| Theo Lĩnh vực Công ty KD | Lĩnh vực · Nhóm ngành · Phòng ban · Bộ phận · Nhân viên · Khách hàng · Tiến trình · Kết quả |

- Ô lọc riêng **suy từ cấp của tiêu chí**: *Thị trường* chỉ hiện ở 2 tiêu chí đầu; *Lĩnh vực* +
  *Nhóm ngành* chỉ hiện ở tiêu chí *Theo Lĩnh vực*. Ô đang ẩn phải **xoá giá trị** để không lọc ngầm.
- Ô tổ chức không nằm trong cấp của tiêu chí (Bộ phận / Nhân viên ở tiêu chí *Lĩnh vực*) vẫn giữ, chỉ
  xếp sau cụm cấp.
- Phòng ban không chia bộ phận thì **khoá ô Bộ phận** thay vì để lựa chọn chết.

### 7.3. Hai ô lọc dễ nhầm — khác nhau ở đâu

| Ô lọc | Lọc theo | Danh sách |
|---|---|---|
| **Tiến trình** | tiến trình lẻ tại cuối kỳ | id **2 → 12** (bỏ *Đang tạo* vì trạng thái này không bao giờ lên báo cáo, để lại là ô lọc chết luôn ra 0 dòng) |
| **Kết quả** | 3 nhóm kết quả | Chuyển đổi thành công · Thất bại · Vẫn tiếp tục triển khai |

---

## 8. BẢNG THEO DÕI

### 8.1. Ba tiêu chí — bắt buộc chọn 1, không có "Tất cả"

| Nhãn trên select | Các cấp của cây |
|---|---|
| **Theo Phòng ban** | Phòng ban ▸ *Bộ phận* ▸ Nhân viên ▸ **Thị trường** |
| **Theo Thị trường** | Thị trường ▸ Phòng ban ▸ *Bộ phận* ▸ Nhân viên |
| **Theo Lĩnh vực Công ty KD** | Lĩnh vực ▸ Nhóm ngành ▸ Phòng ban |

- Cấp **Thị trường nằm dưới Nhân viên** ở tiêu chí 1 chính là câu trả lời cho *"ở các thị trường
  nào?"* — bung dòng nhân viên là thấy ngay từng thị trường kèm kết quả.
- Tiêu chí **Lĩnh vực dừng ở Phòng ban**: câu hỏi quản trị chỉ hỏi *"do phòng ban nào phụ trách"*.
  Muốn xem tới nhân viên thì mở popup chi tiết.
- Cấp **Bộ phận chỉ hiện với phòng ban CÓ chia bộ phận**; phòng không chia thì cây nhảy thẳng
  Phòng ban ▸ Nhân viên, **không đẻ dòng "Chưa phân bộ phận" rỗng**.
- Bảng có đúng **1 dòng `TỔNG`** mang tổng cả kỳ, nhãn đổi theo tiêu chí đang xem.

### 8.2. Bộ cột (10 cột)

```
STT · Nội dung theo dõi · Tổng dự án · Đang triển khai · Đóng trong kỳ ·
Thành công · Thất bại · Tỷ lệ thành công · Giá trị HĐ · Giá trị dự kiến
```

- **Mọi cột số đều cộng được theo cấp** ⇒ số dòng cha luôn = tổng dòng con. Không đưa cột đếm distinct
  (số thị trường / số khách hàng) vào bảng — kiểu cột đó không cộng được theo cấp, chỉ nằm ở dải tổng
  hợp.
- `Giá trị HĐ` cộng trên **dự án Thành công**; `Giá trị dự kiến` cộng trên **dự án Đang triển khai**.
  ⇒ Dự án **Thất bại không đóng góp vào cột tiền nào**.
- Bấm **số bất kỳ** (kể cả dòng `TỔNG`) mở popup danh sách dự án đúng lát cắt đó. Cột `Tỷ lệ thành
  công` không bấm được vì là số dẫn xuất.

### 8.3. Chọn cấp xem

Select nằm ngay trong ô tiêu đề cột *Nội dung theo dõi*, nhãn đổi theo tiêu chí:

- Theo Phòng ban: `Chỉ Phòng ban · Đến Bộ phận · Đến Nhân viên · Tất cả cấp (đến Thị trường)`
- Theo Thị trường: `Chỉ Thị trường · Đến Phòng ban · Đến Bộ phận · Tất cả cấp (đến Nhân viên)`
- Theo Lĩnh vực: `Chỉ Lĩnh vực · Đến Nhóm ngành · Tất cả cấp (đến Phòng ban)`

**Hiểu theo TÊN CẤP, không theo độ sâu**: chọn *Đến Bộ phận* thì phòng không chia bộ phận dừng lại ở
Phòng ban, **không lòi dòng nhân viên ra sớm**. Bấm mũi tên từng dòng vẫn tự do và không làm đổi lựa
chọn của select. Đổi sang tiêu chí ít cấp hơn thì cấp đang chọn **tự kẹp** về cấp sâu nhất còn hợp lệ.

Bản in / Excel **luôn xuất đủ mọi cấp**, không phụ thuộc cấp đang xem trên màn.

---

## 9. DẢI TỔNG HỢP

2 khối, mỗi khối 3 ô con:

| Khối | 3 ô con |
|---|---|
| **Dự án TKT trong kỳ** | Tổng dự án · Dự án lập trước kỳ · Dự án lập trong kỳ |
| **Kết quả thực hiện trong kỳ** | Chuyển đổi thành công · Thất bại · Vẫn tiếp tục triển khai |

- Khối 1 bổ dọc theo **ngày lập phiếu** — 2 nhóm chia hết tổng.
- Khối 2 bổ dọc theo **kết quả tại cuối kỳ** — 3 nhóm chia hết tổng.
- Số khách hàng ở dòng meta là **đếm distinct**, đúng chỗ của nó (dải tổng hợp), không đưa vào bảng.
- Mọi số trong dải đều bấm được để mở popup chi tiết.

---

## 10. POPUP DANH SÁCH DỰ ÁN CHI TIẾT

Mở bằng cách bấm bất kỳ con số nào trên bảng hoặc dải tổng hợp.

### 10.1. Bộ cột

```
STT · Mã dự án · Tên dự án TKT · Ngày lập dự án · Tiến trình
    · [các chiều theo tiêu chí] · Kết quả · Lý do thất bại · Giá trị (đ)
```

**4 cột nhận dạng dự án dồn lên ngay sau STT** — đọc bảng là biết ngay đang nhìn dự án nào, đang ở
bước nào. Cụm cột chiều lùi xuống sau vì popup đã cố định phần lớn chúng rồi.

### 10.2. Bốn luật rút gọn

1. **Bỏ ô lọc của cấp đã cố định** — đang xem theo đối tượng A thì lọc lại theo A là thừa. Cấp đã cố
   định vẫn dùng để thu hẹp cascade cấp dưới.
2. **Bỏ luôn CỘT của cấp đã cố định** — mọi dòng đều mang đúng 1 giá trị ở cấp đó, cột chỉ lặp lại
   điều tiêu đề popup đã nói. Popup theo Bộ phận vì thế bỏ cả cột Phòng ban. Popup mở từ dòng `TỔNG`
   không bỏ cột nào.
3. **Bỏ cột Bộ phận khi không dòng nào thuộc bộ phận** — xét trên toàn bộ dự án của node, không xét
   theo bộ lọc trong popup, để cột không nhấp nháy khi lọc.
4. **Ẩn theo quan hệ 1-nhiều**: cố định *Nhóm ngành* ⇒ ẩn ô lọc *Lĩnh vực*; cố định *Khách hàng* ⇒ ẩn
   ô lọc *Thị trường*. Luật này chỉ áp cho **ô lọc và chip**, cột vẫn giữ.

### 10.3. Còn lại

- **Tiêu đề nêu rõ đối tượng**: *"Đang xem &lt;chỉ tiêu&gt; theo &lt;Cấp&gt;: &lt;Tên&gt;"*, node nằm
  sâu thì dòng phụ hiện đường dẫn cấp cha.
- **Khối tổng hợp mặc định thu gọn** — mở popup ra là thấy ngay danh sách; mỗi lần mở lại đều thu gọn,
  không mang trạng thái từ popup trước sang.
- **Chip phân bổ**: luôn có *Phòng ban* (trả lời "do phòng ban nào phụ trách") cộng 2 chiều cơ cấu
  theo tiêu chí. Chip ẩn theo cùng luật ẩn của bộ lọc.
- **Sắp xếp được** ở: Phòng ban · Nhân viên · Thị trường · Lĩnh vực · Ngày lập dự án · Kết quả ·
  Giá trị. Mặc định *Ngày lập dự án* giảm dần. In + Xuất Excel của popup bám đúng thứ tự đang sắp.
- Bấm **tên dự án** mở panel chi tiết, trong đó có mục **Diễn biến tiến trình** (mốc lập phiếu → tiến
  trình đang chạy → mốc đóng kèm lý do).

---

## 11. QUY ƯỚC HIỂN THỊ ĐÃ CHỐT

| Quy ước | Nội dung |
|---|---|
| **Dự án thất bại không để giá trị** | Ô *Giá trị* hiện `—` trên màn, ô rỗng trong Excel, panel chi tiết bỏ ô tiền. Lý do: dự án đã huỷ thì không còn giá trị nào để ghi nhận — không phải doanh số đã ký, cũng không còn là doanh số đang theo đuổi. Nhất quán với 2 cột tiền của bảng. Khoá sắp xếp của các dòng này = 0 để chúng dồn về một đầu, không nằm lẫn theo một giá trị không hiện ra. |
| **Gọi là "lập trước kỳ / lập trong kỳ"** | Không gọi là *tồn / mở mới*. Cặp nhãn bổ dọc theo **ngày lập phiếu** nên phải cùng một cách gọi. |
| **"Ngày lập dự án"** | Không gọi là *Ngày tạo* / *Ngày lập phiếu*. Một dữ liệu chỉ mang một tên ở mọi nơi. |
| **Nhãn tiêu chí để ngắn** | *Theo Phòng ban / Theo Thị trường / Theo Lĩnh vực Công ty KD*. Chuỗi cấp đầy đủ đọc ở tooltip, ở dòng `TỔNG` và ở select chọn cấp. |
| **Tiến trình hiện dạng pill trung tính kèm số bước** | 11 tiến trình mà tô 11 màu thì bảng loang lổ; màu để dành cho 3 nhóm kết quả. |
| **Tiêu đề cột viết hoa chữ đầu, không xuống dòng** | Áp cho cả bảng theo dõi lẫn bảng trong popup. |

---

## 12. IN VÀ XUẤT EXCEL

- 2 nút **In báo cáo · Xuất Excel** nằm ở góc phải thanh tiêu đề.
- **In** có 2 chế độ: *bảng theo dõi* (đủ mọi cấp) và *danh sách chi tiết* (mỗi dự án 1 dòng). Đầu bản
  in ghi kỳ, số dự án, số khách hàng, phân bổ lập trước/trong kỳ, kết quả cuối kỳ và **bộ lọc đang áp
  dụng**.
- **Excel** của bảng theo dõi xuất đủ mọi cấp; Excel của popup xuất đúng bộ cột và đúng thứ tự đang
  sắp của popup.
- Tên công ty trên bản in luôn là **tên đầy đủ**, không phải tên đã rút gọn để hiển thị trên ô lọc.

---

## 13. CÒN TREO — PHẢI CHỐT KHI IMPLEMENT

1. **Nguồn 2 cột tiền.** Cần chỉ rõ: `Giá trị HĐ` lấy tổng giá trị hợp đồng bên ERP hay lấy
   `expected_contract_amount` của phiếu TKT; `Giá trị dự kiến` lấy `expected_contract_amount` hay
   `estimated_budget`.
2. **Bảng log chuyển tiến trình.** Điều kiện TH1 hỏi *"tại đầu kỳ trạng thái ≠ Đóng"*, tức cần trạng
   thái **quá khứ**, trong khi cột `status` chỉ giữ trạng thái **hiện tại**. Hướng đã chốt: **xây bảng
   logs lưu thời điểm chuyển tiến trình của dự án TKT**, khi đó báo cáo mới chấm đúng các kỳ quá khứ.
3. **3 tiến trình đổi tên 07/09/2026 chưa vào code** (id 5 · 6 · 7) — phải sửa
   `ProspectiveProject::STATUS` và `prospective-projects/constants.js` cho khớp báo cáo.
4. **Phân quyền.** Báo cáo hiện giá vốn/giá trị hợp đồng và kết quả theo từng nhân viên nên phải gắn
   quyền xem; cần chốt ai xem được toàn công ty, ai chỉ xem được phòng ban / bản thân.
5. Chưa port Vue; chưa responsive.
