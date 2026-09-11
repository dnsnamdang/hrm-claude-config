# Plan — Phân trang theo NHÂN VIÊN cho màn Nhân sự & Thân nhân

Vấn đề: phân trang hiện theo PHÒNG BAN. Kasaco có phòng 1.060 người → 1 trang sinh 1.287 `<tr>` /
12.864 `<td>`, render 359ms trên máy dev (máy người dùng chậm hơn nhiều) và mọi thao tác sau đó
(cuộn, lọc, đổi trang) đều phải xử lý khối DOM đó.

Đã chốt với user (2026-09-03):
- Phân trang theo **số nhân viên**, mặc định **50/trang** (bộ chọn 25/50/100/200)
- Phòng ban trải nhiều trang: **lặp tiêu đề + "(tiếp theo)"**, STT nhân viên **chạy tiếp** (51, 52…)
- Áp dụng cho **cả 2 màn**: /human/personnel và /human/employee-relationships
- Bản in + Xuất Excel giữ nguyên (lấy toàn bộ, không phân trang)

## Phase 1 — BE
- [x] Thêm tham số `paginate_by=employee` (không truyền = giữ nguyên phân trang theo phòng ban → in/export không đổi)
- [x] Vòng 1: duyệt theo lô với eager load NHẸ để áp bộ lọc + tính thống kê + dựng danh sách phẳng
      [phòng ban → nhân viên phòng ban → bộ phận → nhân viên bộ phận] chỉ gồm id + khoá sắp xếp
- [x] Vòng 2: chỉ nạp ĐẦY ĐỦ những nhân viên thuộc trang hiện tại rồi dựng lại cây phòng ban/bộ phận
- [x] Mỗi nhân viên trả kèm `stt` (chạy tiếp qua trang); mỗi phòng ban/bộ phận trả `is_continued`
      và `indexRoman` tính theo vị trí trong TOÀN danh sách
- [x] `total` = tổng số nhân viên sau lọc, `perPage` = số nhân viên/trang

## Phase 2 — FE
- [x] Gửi `paginate_by=employee`; đổi bộ chọn số dòng thành 25/50/100/200, mặc định 50
- [x] Bảng dùng `stt` do BE trả thay cho `index + 1`
- [x] Dòng phòng ban/bộ phận hiện thêm "(tiếp theo)" khi `is_continued`
- [x] `totalRows` lấy từ `total` (số nhân viên) thay vì `statistical.count_employees`
- [x] Áp dụng tương tự cho màn Quản lý thân nhân

## Phase 3 — Kiểm thử
- [x] Đối chiếu: ghép tất cả các trang phải ra đúng danh sách như chế độ cũ (không sót, không trùng)
- [x] Thống kê tổng không đổi so với bản hiện tại
- [x] Đo lại số dòng DOM và thời gian render mỗi trang
- [x] Bản in + 2 file Excel giữ nguyên nội dung


### Checkpoint — 2026-09-03
Đã xong Phase 1-3.

**Cách làm (BE):** thêm `paginate_by=employee`. Vòng 1 duyệt toàn bộ theo lô với eager load nhẹ để
áp bộ lọc + tính thống kê + dựng danh sách phẳng (chỉ id, đánh dấu dòng mở đầu của mỗi phòng ban /
bộ phận). Vòng 2 cắt đúng phần nhân viên của trang rồi nạp đầy đủ chỉ cho những người đó.
Không truyền `paginate_by` thì giữ nguyên cắt theo phòng ban → **bản in và 2 file Excel không đổi**.

**Kết quả đo trên dữ liệu kasaco (màn nhân sự, 1 trang):**
| | Trước | Sau |
|---|---|---|
| Dòng `<tr>` | 1.287 | **62** |
| Ô `<td>` | 12.864 | **614** |
| Thời gian render | 359ms | **4ms** |
| Màn thân nhân | 1.321 dòng | **64 dòng** |

**Kiểm chứng:**
- Ghép tất cả các trang = đúng danh sách chế độ cũ: **không sót, không trùng, đúng thứ tự** —
  kiểm trên 8 cấu hình (limit 25/50/100, lọc kiêm nhiệm / chức danh / trạng thái HĐLĐ / tên / phòng ban)
  và trên cả 2 DB (kasaco 1.266 dòng, TPE 538 dòng), cả `view=personnel` lẫn `view=relationship`
- Phòng ban/bộ phận trải nhiều trang hiển thị đúng "(tiếp theo)", STT chạy tiếp (…170, 320…369)
- Hồi quy DB cũ: 17 kịch bản × 3 quyền chỉ lệch `rowspan` (0→1 như trước), 26 endpoint
  Payroll/Timesheet/Nhân sự giống hệt, 2 file Excel giống hệt từng ô


## Phase 4 — Test kỹ sau khi đổi phân trang (2026-09-03)

### Lỗi phát hiện và đã sửa
**Xuất Excel / Bản in ra file rỗng khi đứng ở trang khác 1.** Cả 2 màn gửi `page` theo trang đang xem
kèm `limit` rất lớn → BE cắt trang đúng luật và trả về rỗng. Đo thật: export ở trang 1 = 215KB,
ở trang 5 hoặc 26 = 4,6KB (chỉ có dòng tiêu đề).
Lỗi này CÓ SẴN, nhưng trước đây màn chỉ có 2 trang nên hiếm gặp; sau khi chuyển sang phân trang theo
nhân viên thì có 26 trang → gặp thường xuyên. Đã sửa: Xuất Excel và Bản in luôn gửi `page=1`
(màn nhân sự), và bỏ `page` khỏi tham số export của màn thân nhân.

### Đã kiểm (chạy thật trên UI, dữ liệu kasaco)
Màn nhân sự:
- Cỡ trang 25 / 100 / 200 → đúng 25 / 100 / 200 nhân viên mỗi trang
- Trang cuối (26): 16 nhân viên (1.266 − 25×50), trang 25: 50 nhân viên
- Trang vượt quá: bảng trống, không lỗi
- Lọc khi đang ở trang cuối → tự về trang 1 và có dữ liệu (1.035 người)
- Lọc không ra kết quả → hiện "Chưa có dữ liệu", tổng = 0; xoá lọc → trở lại 1.266
- Bản in mở từ trang 5 vẫn ra đủ 1.300 dòng; tham số gửi đi `page=1`, không kèm `paginate_by`
- Xuất Excel mở từ trang 5 gửi `page=1&limit=10000000000000000`, không kèm `paginate_by`

Màn thân nhân: cỡ trang 25/50 đúng, trang cuối 24 dòng, Xuất Excel gửi `page=1`, không kèm `paginate_by`

### Hồi quy (DB cũ hrm_prod_6_6)
- 17 kịch bản × 3 quyền: chỉ lệch `rowspan` (0→1 như các phase trước)
- 26 endpoint Payroll + Timesheet + Nhân sự: giống hệt 26/26
- 2 file Excel: giống hệt từng ô so với bản gốc
- Ghép trang trên cả 2 DB, cả 2 view, 8 cấu hình lọc: không sót, không trùng, đúng thứ tự

### Thay đổi hiển thị nhỏ cần biết
Nhãn dưới bảng đổi từ "Tổng số bản ghi: <số phòng ban>" thành "Tổng số nhân sự: <số nhân viên>",
vì thanh phân trang giờ đếm theo nhân viên.
