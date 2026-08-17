# Bảng tra — SRS Các quy tắc chung (VN 1.0)

Nguồn: `SRS_Các quy tắc chung_VN_1.0.docx`. File này chép lại **nguyên văn quy tắc** để tra nhanh
khi code, không cần mở lại .docx. Khi .docx ra bản mới → cập nhật file này.

---

## 1. Màn Danh sách

### 1.1 Hiển thị bảng
- Màn cơ bản mặc định có các cột: **STT, Mã, Tên, Người tạo, Ngày tạo, Trạng thái (nếu có), Hành động**.
- Màn có thông tin Khách hàng / Số tiền / Loại → bổ sung tương ứng cột **Khách hàng, Số tiền, Loại**.
- Sắp xếp mặc định: **giảm dần theo thời gian tạo**.
- Mã và Tên là **2 cột riêng biệt**. Click vào **mã** hoặc **dòng** → sang màn chi tiết.
- Danh sách trống → hiện **dòng thông báo không có dữ liệu**, không để bảng rỗng.

### 1.2 Cột Hành động
- Bản ghi có **≤ 3 hành động** → hiện đủ 3 nút trong cột.
- Bản ghi có **> 3 hành động** → hiện 2 nút chính **Sửa, Xóa** + nút **Hành động khác** (menu dọc).
- Thứ tự trong cột: **Chỉnh sửa → Xóa → Nhóm hành động khác**.

### 1.3 Sắp xếp (sort)
- Mặc định bật sort cho cột định dạng: **mã, tên, tiền, ngày** (màn nào cần thêm thì note riêng).
- Click lần 1 = tăng dần (A→Z / nhỏ→lớn); lần 2 = giảm dần.
- **Chỉ 1 cột sort tại 1 thời điểm** — sort cột khác thì hủy tiêu chí cũ.
- Icon sort trên tiêu đề đổi theo trạng thái tăng/giảm.

### 1.4 Tìm kiếm
- Trường **nhập ký tự**: nhấn Enter / nút Tìm kiếm mới tìm.
- Trường **chọn giá trị**: tự tìm ngay sau khi chọn; có giá trị thì hiện nút **X** để xóa nhanh.
- Tự **trim** khoảng trắng đầu/cuối chuỗi nhập.
- Không phân biệt hoa/thường; hỗ trợ tiếng Việt **có dấu và không dấu**.
- Thứ tự ưu tiên kết quả theo văn bản:
  1. Trùng khít toàn chuỗi đứng đầu.
  2. Khớp ở **đầu** chuỗi ưu tiên hơn khớp ở giữa/cuối.
  3. Cùng điểm → chuỗi **ngắn hơn** đứng trước (vd `an` trước `anh`).
- Nhiều tiêu chí → kết quả phải thỏa mãn **đồng thời** tất cả.
- Nút **Làm mới**: xóa toàn bộ điều kiện lọc **và tải lại danh sách đầy đủ**.
- Điều kiện lọc được **ghi nhớ** và dùng lại khi user quay về màn.
- **< 3 trường lọc** → ẩn khối "Tìm kiếm nâng cao", hiển thị thẳng ngoài màn danh sách.

### 1.5 Cài đặt bộ lọc
- Cho phép kéo thả, sắp xếp, ẩn/hiện các bộ lọc ở Tìm kiếm nâng cao.
- Mặc định **hiển thị tất cả** trường tìm kiếm.
- Chỉ hiện với màn có **> 3 trường lọc**.
- Load lại trang vẫn giữ nguyên cài đặt đã set.

### 1.6 Cấu hình cột
- Cho phép ẩn/hiện và đổi thứ tự cột.
- Load lại trang hoặc chuyển màn → tự load cấu hình đã lưu gần nhất.
- **KHÔNG được tắt** cột **STT, Mã, Hành động**.

---

## 2. Màn Thêm mới

- Sai định dạng → hiện lỗi **ngay dưới textbox**; nhập đúng → ẩn lỗi.
- Cấu trúc thông báo lỗi: **"Tên trường – Nội dung lỗi"**, vd `Số điện thoại – Không đúng định dạng`.
- **Không gọi API lưu** khi màn còn lỗi validate.
- Nhiều trường lỗi → **tự đưa con trỏ về trường lỗi đầu tiên**.
- Trường chọn danh mục **chỉ hiển thị danh mục đang hoạt động**.
- **Lưu nháp chỉ bắt required trường Tên**, các trường khác không required.

---

## 3. Màn Xem chi tiết

- Hiển thị **đầy đủ button mà tài khoản đang có quyền** thao tác.
- **Số phiếu**: hiển thị phía trên cùng, ngay sau tiêu đề màn.
- Danh mục bị khóa → **vẫn hiển thị tên danh mục** kèm biểu tượng/chữ "đã khóa".
- **Lịch sử phiếu**:
  - Mặc định **ẩn**, click mới show.
  - Bộ lọc: **Loại hành động**, **Người thực hiện**, **Khoảng thời gian từ ngày – đến ngày**.
  - Loại hành động gồm 3 nhóm chung: **Tạo mới, Thay đổi thông tin, Thay đổi trạng thái**.
  - Dropdown Người thực hiện: có ô tìm kiếm, gồm toàn bộ NV, định dạng **`Mã phòng – Tên nhân viên`**.
  - Sắp xếp **mới nhất → cũ nhất**.

---

## 4. Màn Chỉnh sửa (xử lý danh mục bị khóa)

| Trạng thái bản ghi | Hành vi khi có danh mục đã khóa |
|---|---|
| **Khác "Đang tạo"** | Sửa trường khác rồi Lưu → **không báo lỗi**, lưu thành công. Dropdown hiện **tất cả danh mục hoạt động + danh mục đã khóa đang gắn với bản ghi**. User đổi sang giá trị khác rồi vẫn **chọn lại được** danh mục đã khóa (khi chưa nhấn Lưu). |
| **"Đang tạo"** | Sửa trường khác rồi Lưu → **báo lỗi validate** danh mục đã bị khóa. |

---

## 5. Xuất Excel

- Cho phép user **chọn trường dữ liệu cần xuất**.
- Thứ tự cột trong file = **thứ tự user chọn** trước khi xuất.
- Mọi trường xuất đều nằm ở **cột riêng biệt**.

---

## 6. Import file

- UI popup import thống nhất 4 khu vực: **File – Hành động – Hiển thị kết quả – Xóa tất cả dòng lỗi**.
- Có **file mẫu** để user tải về.
- **Validate trước khi Import**.
- Dòng lỗi: **màu đỏ**, báo lỗi cụ thể tại từng trường, user **sửa trực tiếp trên form**.
  - Với đối tượng như Quản lý báo giá / Bomlist: mở popup báo lỗi ngay sau khi click Validate.
  - Popup lỗi cho phép **copy-paste** 3 cột: **Dòng, Tên cột sai, Mô tả chi tiết**.
  - Cho phép **tải file excel lỗi**.
- Dòng hợp lệ: **màu xanh**, các trường đã hợp lệ **không cho sửa nữa**.
- **Vẫn cho Import khi còn dòng lỗi** — hệ thống chỉ import các dòng hợp lệ.

---

## 7. Màn Báo cáo (quy tắc riêng)

- Phải có **chú thích mục đích xem báo cáo** ở tiêu đề màn **và** tiêu đề bảng/biểu đồ.
- Mọi cột dữ liệu có **tooltip** giải thích cách lấy / cách tính / ý nghĩa cột.

---

## 8. Nguyên tắc chung khác

- **Dropdown ở bộ lọc** luôn có nút xóa lựa chọn; bỏ trống = không lọc theo tiêu chí đó.
- **Mọi nút** đều có tooltip khi hover.
- **Date picker**: click hiện lịch; cho phép **nhập tay** đúng định dạng; định dạng **dd/mm/yyyy**.
- **Phân trang**: mặc định **10** bản ghi/trang; chọn được **5, 10, 20, 50, 100**; đổi số dòng luôn
  **quay về trang 1**.
- Hỗ trợ mở màn liên kết ở tab mới bằng **click chuột giữa** và **chuột phải → Open link in new tab**
  (⇒ link phải là thẻ `<a>`/`nuxt-link` thật, không phải `@click` trên `<div>`).
- **Mọi button hiển thị kèm icon + text**.

---

## 9. Thông báo nghiệp vụ

### 9.1 Cấu trúc
```
[{TIỀN TỐ}] {Nhóm Hành Động}: {Tên Đối Tượng}. {Ghi chú bổ sung}
```
- **Tiền tố**: mã đối tượng trong ngoặc vuông (`[TASK]`, `[MET]`).
- **Nhóm hành động**: sự kiện xảy ra với bản ghi.
- **Tên đối tượng**: tiêu đề Task/Meeting/Giải pháp — **≤ 50 ký tự**, dài hơn thì `…`, **in đậm**.
- **Ghi chú bổ sung**: Deadline, thời gian họp, lý do từ chối…
- **Tổng độ dài ≤ 120 ký tự**.
- Deep-link: thông báo dẫn thẳng tới màn xử lý, **bắt buộc kèm ID đối tượng**.

### 9.2 14 nhóm hành động chuẩn
| # | Hành động | Dùng khi |
|---|---|---|
| 1 | Tạo mới | Bản ghi mới được tạo, người nhận cần biết/xử lý |
| 2 | Cập nhật | Bản ghi đã tồn tại bị chỉnh sửa |
| 3 | Chờ duyệt | Gửi đến bước phê duyệt, chờ người có thẩm quyền |
| 4 | Đã duyệt | Đã phê duyệt thành công |
| 5 | Từ chối | Không được phê duyệt, kèm lý do |
| 6 | Yêu cầu làm lại | Cần chỉnh sửa/bổ sung rồi làm lại |
| 7 | Góp ý | Nhận comment (vd task) |
| 8 | Sắp đến hạn | Nhắc sắp tới hạn xử lý |
| 9 | Quá hạn | Đã quá hạn nhưng chưa hoàn thành |
| 10 | Hủy | Bản ghi/hoạt động bị hủy |
| 11 | Tạm dừng | Tạm thời dừng xử lý |
| 12 | Tiếp tục | Tiếp tục sau khi tạm dừng |
| 13 | Thay đổi lịch | Đổi thời gian/lịch (đặc biệt Meeting) |
| 14 | Nhắc báo cáo | Yêu cầu thực hiện/cập nhật báo cáo định kỳ |

### 9.3 Cách hiển thị
- Thành công / thất bại / phê duyệt / từ chối → **toast góc màn hình, tự tắt**.
- Lỗi validate từng trường → **chữ đỏ ngay dưới ô nhập**.
- Màn nhiều tab bị lỗi → **cảnh báo đỏ ở đầu tab lỗi**; trong tab hiện tại tự đưa con trỏ về
  trường lỗi đầu tiên.

---

## 10. Bộ thông báo chuẩn (dùng đúng nguyên văn, không tự chế câu mới)

| Mã | Trường hợp | Nội dung | Hành vi sau khi nhấn |
|---|---|---|---|
| QLDA_001 | Lưu thất bại do còn trường không hợp lệ | "Bạn chưa nhập đầy đủ thông tin." | Đóng, giữ nguyên dữ liệu, con trỏ về dòng lỗi đầu tiên |
| QLDA_002 | Quay lại trạng thái trước thay đổi gần nhất | "Bạn có những thay đổi chưa được lưu. Bạn có chắc chắn muốn hủy bỏ các thay đổi này không?" | Tiếp tục chỉnh sửa → đóng; Hủy bỏ → mất dữ liệu, đóng màn |
| QLDA_003 | Thêm mới thành công | "Thêm mới thành công." | Quay lại danh sách hoặc reset form |
| QLDA_004 | Cập nhật thành công | "Cập nhật thành công." | Quay lại màn danh sách |
| QLDA_005 | Xóa thành công | "Xóa thành công." | Tải lại danh sách |
| QLDA_006 | Xác nhận xóa | "Bạn có chắc muốn xóa bản ghi này không?" | Đồng ý → xóa; Không → đóng |
| QLDA_007 | Xác nhận lưu thay đổi | "Bạn có muốn lưu các thay đổi vừa thực hiện không?" | Đồng ý → lưu; Không → giữ nguyên màn |
| QLDA_008 | Xác nhận rời khỏi khi chưa lưu | "Bạn có chắc muốn thoát? Thông tin chưa được lưu sẽ bị mất." | Đồng ý → thoát; Không → ở lại |
| QLDA_009 | Cảnh báo thao tác rủi ro | "Thao tác này có thể ảnh hưởng đến dữ liệu. Bạn có muốn tiếp tục?" | Đồng ý → tiếp tục; Không → dừng |
| QLDA_010 | Lỗi hệ thống | "Đã xảy ra lỗi hệ thống. Vui lòng thử lại." | Đóng |
| QLDA_011 | Không có dữ liệu | "Không có dữ liệu phù hợp." | Đóng |
| QLDA_012 | Không đủ quyền | "Bạn không có quyền thực hiện chức năng này." | Đóng |
| QLDA_014 | Hết phiên đăng nhập | "Phiên làm việc đã hết hạn. Vui lòng đăng nhập lại." | Chuyển tới trang đăng nhập |
| QLDA_015 | Dữ liệu liên quan – không thể xóa | "Không thể xóa do dữ liệu đang được sử dụng." | Đóng |
| QLDA_022 | Khóa danh mục thành công | "Khóa thành công." | Đóng |
| QLDA_023 | Mở khóa danh mục thành công | "Mở khóa thành công." | Đóng |
| QLDA_024 | Xung đột phiên bản/trạng thái | "Thao tác không thành công. Dữ liệu đã được thay đổi hoặc chuyển trạng thái bởi người dùng khác. Vui lòng tải lại trang để cập nhật thông tin mới nhất." | Đóng |
| QLDA_025 | Thu hồi quyền thời gian thực | "Thao tác không thành công. Quyền hạn của bạn đối với dữ liệu này đã thay đổi hoặc bị thu hồi. Vui lòng liên hệ Quản trị viên." | Đóng |

> QLDA_007 ví dụ thực tế: đang lập Báo giá có dữ liệu nháp, user đổi Loại tiền tệ VND→USD →
> hệ thống tạm ngưng và hỏi lưu trước khi áp tỷ giá mới. Đồng ý = lưu → tính tỷ giá → trả về số
> tiền mới. Không = trả dropdown về VND, giữ nguyên màn.

> QLDA_008 áp cho **cả 2 kịch bản**: (1) bấm nhầm menu / nút Back trình duyệt khi đang nhập form;
> (2) chủ động bấm "Hủy bỏ" hoặc dấu "X" góc phải popup.

---

## 11. Quy định về danh mục

### Chỉnh sửa
- Danh mục **Hoạt động**: luôn cho đổi tên hiển thị + sửa mô tả/ghi chú. Danh mục **đang khóa**: KHÔNG cho sửa.
- Bản ghi trạng thái **Đang tạo** → cập nhật theo **tên danh mục mới**; các trạng thái khác **giữ nguyên
  tên danh mục tại thời điểm tạo**.
- Chỉ cho sửa nội dung **ảnh hưởng nghiệp vụ** khi danh mục **chưa phát sinh dữ liệu giao dịch liên kết**.
- Hủy Sửa: chưa thay đổi gì → **không hiện popup confirm**; đã thay đổi → hiện popup confirm thoát.

### Xóa — chỉ khi thỏa mãn **đồng thời**
- Không tồn tại danh mục **Con**.
- Không phát sinh **dữ liệu giao dịch liên kết**.
- **Không được xóa** bản ghi ở trạng thái **Đã khóa**.

### Khóa — chỉ khi thỏa mãn **đồng thời**
- Không tồn tại danh mục Con **đang hoạt động**.
- Hủy/không duyệt: **luôn hiện và bắt buộc nhập lý do**. Popup lý do gồm: **textarea + nút Lưu + nút Hủy**.
- Sau khi khóa, màn Chỉnh sửa của đối tượng đã gắn danh mục đó **vẫn phải hiển thị** danh mục đã khóa.

### Mở khóa — chỉ khi
- **Danh mục cha trực tiếp** (nếu có) đang ở trạng thái hoạt động.

---

## 12. Định dạng dữ liệu

| # | Quy định | Định dạng |
|---|---|---|
| 1 | Ngày tạo / ngày cập nhật | `dd/mm/yyyy hh:mm` (vd `18/10/2026 20:00`) |
| 2 | Ngày | `dd/mm/yyyy` |
| 3 | Giờ | `hh:mm` (24h) |
| 4 | Số ngày | Số nguyên (vd `1 ngày`) |
| 4 | Tiền tệ | `.` ngăn cách phần nghìn, `,` ngăn phần thập phân |
| 5 | Tên | ≤ **255** ký tự; chỉ `A-Z a-z 0-9 _` và khoảng trắng |
| 5 | Mã code | ≤ **50** ký tự; chỉ `A-Z a-z 0-9 _` |
| 6 | Email | `tennguoidung@domain.xyz` (regex chuẩn email) |
| 7 | Selection field | Phải khớp giá trị đã định nghĩa; trường autocomplete có hỗ trợ lọc |
| 8 | Text mô tả dài | Hỗ trợ xuống dòng (multi-line) |

---

## 13. Màu nút theo nhóm hành động

| Nhóm | Nền / Chữ / Viền | Nút ví dụ |
|---|---|---|
| Action chính | `#1ABC9C` / `#FFFFFF` / `#1ABC9C` | Tạo mới · Lưu · Lưu nháp · Sửa |
| Duyệt | `#16A34A` / `#FFFFFF` / `#16A34A` | Duyệt |
| Gửi duyệt / Khóa | `#D97706` / `#FFFFFF` / `#D97706` | Gửi duyệt · Khóa |
| **NGUY HIỂM** (không hoàn tác) | `#DC2626` / `#FFFFFF` / `#DC2626` | Xóa · Từ chối |
| Action phụ | `#FFFFFF` / `#333333` / `#E2E2E2` | In · Cấu hình cột |
| IMPORT | `#FFFBEB` / `#B45309` / `#FDE68A` | Import Excel |
| XUẤT FILE | `#F7FEE7` / `#15803D` / `#DCFCE7` | Xuất CSV · Xuất Excel · Xuất PDF |
| Thoát / Hủy / Quay lại / Làm mới | `#FFFFFF` / `#1F2937` / `#E2E8F0` | Đóng · Hủy · Quay lại · Làm mới |
| Nút phụ ngoài page | `#FFFFFF` / `#374151` / `#E5E7EB` | Quay lại |

> Ở hrm-client **không hard-code mã màu** — map sang prop của `V2BaseButton`
> (`primary`, `secondary` + `status="success" / warning / danger"`). Xem `.claude/skills/button-convention/SKILL.md`.

---

## 14. Căn lề cột

| Loại dữ liệu | Căn | Cột ví dụ |
|---|---|---|
| STT | **Giữa** | STT |
| Chữ / định danh | **Trái** | Tên, Mã KH, MST, SĐT, Email, Địa chỉ, Nhóm KH, Tỉnh/TP, Người tạo, Người sửa |
| Số đếm / số lượng / tiền / % / định mức | **Phải** | Đơn giá bán, Công kỹ thuật, Số lượng, Thành tiền, Định mức công |
| Ngày, giờ | **Trái** | Ngày tạo, Ngày cập nhật |
| Badge trạng thái, icon, checkbox, cờ Có/Không | **Giữa** | Trạng thái, Đã duyệt, Chọn dòng |
| Cột Hành động | **Giữa** | Hành động |
| Chữ dài (địa chỉ, ghi chú, mô tả) | **Trái** | Địa chỉ, Địa chỉ xuất hóa đơn, Ghi chú |

---

## 15. Thứ tự nút theo khu vực

| Khu vực | Thứ tự (trái → phải) |
|---|---|
| Popup (modal) | 1. Lưu (nháp) → 2. Lưu / Xác nhận / Duyệt → 3. Nút phụ (Lưu & Tiếp tục, Xuất file) → 4. Nút nguy hiểm (Xóa, Từ chối) → 5. Làm mới → 6. Đóng |
| Toolbar màn danh sách | 1. Thêm mới → 2. Import / Xuất Excel / Cấu hình cột |
| Toolbar màn xem chi tiết | 1. Sửa → 2. Quản lý → 3. Khóa/Mở khóa → 4. Quay lại |
| Màn form (thêm mới / sửa) | 1. Lưu nháp → 2. Lưu / Gửi duyệt / In → 3. Xuất file, Xem trước → 4. Quay lại danh sách |
| Cột thao tác trong bảng | Chỉnh sửa → Xóa → Nhóm hành động khác |

---

## 16. Màu trạng thái

| Nhóm | Mã màu | Trạng thái thuộc nhóm |
|---|---|---|
| Hoàn thành – Đã duyệt | `#16A34A` | Hoàn thành, Hoàn tất, Đã duyệt, Đã duyệt giải pháp, Đã xử lý xong, Tiếp nhận, Đã duyệt giá |
| Đang thực hiện | `#2563EB` | Đang thực hiện, Đang triển khai, Đang xử lý, Đã gửi, Đã tiếp nhận |
| Chờ xử lý – Chờ duyệt | `#D97706` | Chờ duyệt, Chờ TP duyệt, Chờ PM duyệt, Chờ BGĐ duyệt, Chờ Leader duyệt, Chờ tiếp nhận, Chờ làm giá |
| Cảnh báo – Sắp đến hạn | `#F59E0B` | Sắp tới hạn, Tạm dừng, Cần bổ sung thông tin |
| Từ chối – Quá hạn – Khóa | `#DC2626` | Từ chối, Không duyệt, Từ chối kết quả, Từ chối triển khai, Dừng, Quá hạn, Khóa, Ngừng hoạt động |
| Theo dõi – Mới tiếp nhận | `#0EA5E9` | Đã phân công, Chờ phê duyệt triển khai, Đã tạo hợp đồng, Đang khảo sát |
| Chốt – Thương thảo | `#7C3AED` | Đã chốt, Chốt giải pháp, Đã chốt giải pháp, Thương thảo giá, Dự toán, Trúng thầu |
| Nháp – Mới tạo | `#64748B` | Nháp, Đang tạo, Mới ghi nhận, Chờ bắt đầu |
| Đã đóng – Không áp dụng | `#6B7280` | Đóng, Đã đóng, Hết hiệu lực, Đã hủy, Chưa duyệt, Không áp dụng |

> Ở hrm-client dùng `V2BaseBadge` với `variant` tương ứng, **không tự khai `<span class="status-pill">`**.
> Text lấy từ `status_text` BE trả về.
