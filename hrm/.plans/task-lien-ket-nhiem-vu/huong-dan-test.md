# Hướng dẫn nghiệm thu #11456 — Liên kết Nhiệm vụ với Dự án, Meeting, Phòng ban

> **Mở đúng cổng 3000.** `http://127.0.0.1:3000`
> Cổng **3005 là worktree nhánh `tpe`, KHÔNG có code của task này** — vào đó sẽ thấy giao diện cũ.
> BE đi kèm: `http://127.0.0.1:8000` (repo `hrm-api`, nhánh `tpe-develop-assign`, DB `hrm_prod_6_6`).

## 0. Tài khoản test

| Vai trò khi test | Email | Mật khẩu | Đặc điểm (quyết định kết quả mong đợi) |
|---|---|---|---|
| Quản trị | `namdangit@gmail.com` | `2025Dns@2` | Super admin. Thành viên **2 cuộc họp**, **0 dự án**, **0 giải pháp** |
| Quản lý giải pháp | `tuannd.kd1@tanphat.com` | `Test@2026` | **1 dự án** (qua phòng ban hỗ trợ), **18 cuộc họp**, **0 giải pháp** |
| Nhân viên | `duyck.kd1@tanphat.com` | `Test@2026` | **0 dự án**, **0 giải pháp**, **11 cuộc họp** |
| Thành viên giải pháp | `dattq.tkhn@tanphat.com` | `Test@2026` | **3 dự án**, **1 giải pháp**, **1 cuộc họp** — dùng khi muốn thấy ô Giải pháp CÓ dữ liệu |

## 1. Dữ liệu demo đã tạo sẵn

Tất cả đều có tiền tố **`[DEMO 11456]`**.

**Dự án:** `[TEST ADMIN] Dự án chốt giải pháp 1109-1338` (id **253**)
→ `http://127.0.0.1:3000/assign/prospective-projects/253/manager`

| Nhiệm vụ | Loại | Liên kết | Dùng để kiểm |
|---|---|---|---|
| Lắp đặt tủ điện tổng | cụ thể | dự án 253 **+ giải pháp GP37** | cột *Giải pháp* có dữ liệu |
| Khảo sát mặt bằng | cụ thể | chỉ dự án 253 | cột *Giải pháp* **để trống** (không dấu `—`) |
| Trực an toàn công trường (2 bản ghi) | **chung** | chỉ dự án 253 | nhiệm vụ chung sinh nhiều bản ghi |
| Tổng vệ sinh 5S cuối tuần | cụ thể | **không liên kết gì** | nhiệm vụ phòng ban, chỉ thấy ở `/assign/tasks` |

**Cuộc họp:** `[DEMO 11456] Họp giao việc đầu tuần` — mã `TPE.MET.NB.26.0139` (id **152**)
→ `http://127.0.0.1:3000/assign/meeting/152/show`
Thành phần tham dự: DNS Admin, Nguyễn Đức Tuân, Chu Khương Duy (3 tài khoản trên đều xem được).

| Dòng biên bản | Phương án xử lý | Người thực hiện | Hạn dự kiến | Dùng để kiểm |
|---|---|---|---|---|
| 1 | Gửi kế hoạch lắp đặt chi tiết cho khách | **1 nhân viên** (Tuân) | +7 ngày | → **Nhiệm vụ cụ thể** |
| 2 | Khảo sát hiện trạng điện và lập báo cáo | **2 nhân viên** (Tuân, Duy) | +10 ngày | → **Nhiệm vụ chung**, sinh 2 bản ghi |
| 3 | Khách gửi bản vẽ trước ngày hẹn | **chỉ người ngoài công ty** | +12 ngày | người ngoài **bị bỏ qua**, ô Người thực hiện trống |

---

## 2. Kịch bản test — làm lần lượt

### A. Nhiệm vụ gắn với DỰ ÁN  (đăng nhập: DNS Admin)

| # | Thao tác | Kết quả PHẢI thấy |
|---|---|---|
| A1 | Mở `/assign/prospective-projects/253/manager` | Trên thanh tab có **đúng một** tab tên **“Nhiệm vụ”**. **KHÔNG còn** tab “Nhiệm vụ giải pháp” |
| A2 | Bấm tab **Nhiệm vụ** | Bảng ra **4 nhiệm vụ `[DEMO 11456]`**. Cột theo thứ tự: STT · Mã nhiệm vụ · Tên nhiệm vụ · Loại nhiệm vụ · Giải pháp · Người thực hiện · Hạn hoàn thành · Ưu tiên · Người tạo · Ngày tạo · Trạng thái · Hành động |
| A3 | Nhìn cột **Giải pháp** | Dòng “Lắp đặt tủ điện tổng” có tên giải pháp; 3 dòng còn lại **để trống** (không có dấu `—`) |
| A4 | Bấm vào **mã** `TPE.TASK.NB.26.00xx` (chữ xanh navy gạch chân đứt) | Mở popup **Chi tiết nhiệm vụ**, các ô **không sửa được**. Đóng lại |
| A5 | Nhìn cột **Hành động** (cuộn ngang sang phải) | Các nút nằm ở **cột cuối**, **không có nút “Xem”**. Nút chỉ hiện khi dùng được (không có nút xám) |
| A6 | Bấm **Tạo mới** | Popup mở, ô **Dự án/Nhóm** điền sẵn tên dự án và **bị khoá**; ô **Giải pháp**, **Hạng mục**, **Meeting** để trống và **không có dấu `*`** |
| A7 | Nhập: Tên = `Test A7`, Người thực hiện = bất kỳ, Mức độ ưu tiên = Bình thường, Số giờ = 2 → **Lưu** | Báo “Đã lưu nhiệm vụ thành công”, dòng mới xuất hiện đầu bảng, cột Giải pháp **trống** ⇒ *tạo được nhiệm vụ gắn dự án mà không cần giải pháp* |
| A8 | Bấm **Tìm kiếm nâng cao** → chọn **Loại nhiệm vụ = Nhiệm vụ chung** | Danh sách tự lọc ngay (**không phải bấm Tìm kiếm**), còn 2 dòng |
| A9 | Bấm **Làm mới** | Bộ lọc trống, danh sách trở lại đầy đủ |
| A10 | Bấm tiêu đề cột **Mã nhiệm vụ** 2 lần | Lần 1 sắp tăng dần, lần 2 giảm dần; mũi tên trên tiêu đề đổi chiều |
| A11 | Ở cột Hành động bấm **Xoá** nhiệm vụ `Test A7` | Hiện popup xác nhận chuẩn (“Xác nhận xoá” + nút Xóa đỏ), xoá xong danh sách giảm 1 dòng |

### B. Nhiệm vụ gắn với MEETING  (đăng nhập: DNS Admin)

| # | Thao tác | Kết quả PHẢI thấy |
|---|---|---|
| B1 | Mở `/assign/meeting/152/show` | Thanh tab có **4 tab**: Thông tin · Điểm danh · Biên bản · **Nhiệm vụ** |
| B2 | Bấm tab **Biên bản** | Bảng “Các nội dung khác” có thêm cột **Thao tác** ở cuối, mỗi dòng có **1 icon người-mũi-tên** (tooltip “Giao nhiệm vụ”). Cột **Hạn dự kiến** vẫn đọc được đủ ngày |
| B3 | Bấm icon ở **dòng 1** (1 người thực hiện) | Popup tạo nhiệm vụ mở, điền sẵn: **Tên** = “Gửi kế hoạch lắp đặt chi tiết cho khách” · **Loại nhiệm vụ = Nhiệm vụ cụ thể** · **Người thực hiện = Nguyễn Đức Tuân** · **Hạn hoàn thành** = ngày trong biên bản · **Meeting** = tên cuộc họp và **bị khoá** |
| B4 | Chọn Mức độ ưu tiên = Bình thường, Số giờ = 2 → **Lưu** | Lưu thành công |
| B5 | Quay lại tab **Biên bản** (F5 nếu cần) | Dòng 1 hiện chữ **“Đã giao 1 nhiệm vụ”** dưới icon |
| B6 | Bấm chữ **“Đã giao 1 nhiệm vụ”** | Popup **Nhiệm vụ đã giao** liệt kê mã + tên + trạng thái; bấm vào dòng mở được chi tiết nhiệm vụ |
| B7 | Bấm icon ở **dòng 2** (2 người thực hiện) | Loại nhiệm vụ tự chuyển **Nhiệm vụ chung**, ô Người thực hiện có **2 người** |
| B8 | Chọn ưu tiên + số giờ → **Lưu**, rồi mở tab **Nhiệm vụ** | Sinh **2 bản ghi** riêng (mỗi người 1 nhiệm vụ). Tab Nhiệm vụ đếm đủ số nhiệm vụ của cuộc họp |
| B9 | Bấm icon ở **dòng 3** (chỉ có người ngoài công ty) | Popup mở, Tên + Hạn vẫn kế thừa, **ô Người thực hiện để TRỐNG** (người ngoài không giao được) |
| B10 | Bấm **Lưu** ngay khi chưa chọn người thực hiện | Bị chặn, hiện chữ đỏ “Bắt buộc phải nhập” dưới ô. Chọn 1 người rồi lưu thì được |
| B11 | Mở `/assign/meeting/create` (màn **Tạo** cuộc họp) → tab Biên bản | **Không có** tab “Nhiệm vụ”, bảng biên bản **không có** cột Thao tác (chỉ màn Chi tiết mới giao được nhiệm vụ) |

### C. Nhiệm vụ PHÒNG BAN + link động  (đăng nhập lần lượt 3 tài khoản)

| # | Thao tác | DNS Admin | Nguyễn Đức Tuân | Chu Khương Duy |
|---|---|---|---|---|
| C1 | Mở `/assign/tasks` → **Tạo mới** | popup mở | popup mở | popup mở |
| C2 | Mở ô **Giải pháp** | *Không có dữ liệu* | *Không có dữ liệu* | *Không có dữ liệu* |
| C3 | Mở ô **Dự án/Nhóm** | *Không có dữ liệu* | **1 dự án** (Ford Hưng Yên) | *Không có dữ liệu* |
| C4 | Mở ô **Meeting** | **2 cuộc họp** | **18 cuộc họp** | **11 cuộc họp** |
| C5 | Nhập Tên + Người thực hiện + Ưu tiên + Số giờ, **không chọn** dự án/giải pháp/meeting → Lưu | Lưu thành công ⇒ *nhiệm vụ nội bộ phòng ban* | — | — |

> Ý nghĩa C2–C4: **link động** — mỗi người chỉ chọn được dự án / giải pháp / cuộc họp **mình là thành viên**. Đây là đúng yêu cầu đã chốt (áp cho **tất cả**, kể cả admin).
> Muốn tạo nhiệm vụ cho một giải pháp thì vào **màn Giải pháp → tab Nhiệm vụ → Tạo mới**: ở đó Giải pháp + Dự án được điền sẵn và khoá.

### D. Phân quyền (đăng nhập: Chu Khương Duy)

| # | Thao tác | Kết quả PHẢI thấy |
|---|---|---|
| D1 | Mở `/assign/tasks` | Chỉ thấy nhiệm vụ mình liên quan (được giao / mình tạo / theo dõi / duyệt), **không** thấy toàn bộ nhiệm vụ của công ty |
| D2 | Mở `/assign/prospective-projects/253/manager` → tab Nhiệm vụ | Chỉ thấy nhiệm vụ mình liên quan trong dự án đó; các nút Sửa/Xoá **tự ẩn** nếu không có quyền |
| D3 | Mở `/assign/meeting/134/show` (cuộc họp **không** tham gia) | Bị chặn (trang 404) — không xem được nhiệm vụ của cuộc họp người khác |
| D4 | Mở `/assign/meeting/152/show` (cuộc họp **có** tham gia) | Xem được, tab Nhiệm vụ chỉ liệt kê nhiệm vụ mình được phép thấy |

### E. Nhãn Giải pháp / Dự án / Hạng mục ở popup Xem–Sửa  (sửa 18/09, đăng nhập: DNS Admin)

> Bối cảnh lỗi: options của 3 ô này nạp 1 lần lúc mở popup và lọc `mine=1` + lọc trạng thái,
> nên nhiệm vụ gắn giải pháp **đã chốt** (status 17) hoặc dự án mình không phải thành viên thì
> ô hiện trống trơn tuy DB vẫn lưu đủ. Đã vá bằng `ensureLinkedOptions()` + BE trả kèm tên/mã.

| # | Thao tác | Kết quả PHẢI thấy |
|---|---|---|
| E1 | `/assign/tasks` → mở `TPE.TASK.NB.26.0022` (bấm vào mã) | Ô **Giải pháp** hiện `[TEST ADMIN] Giải pháp 1109-1338 (CTV_NV.UD.0101.2026.DA001_GP37)`, ô **Dự án/Nhóm** hiện `[TEST ADMIN] Dự án chốt giải pháp 1109-1338`. Trước khi sửa: cả 2 ô trống |
| E2 | Đóng popup, mở tiếp `TPE.TASK.NB.26.0023` | Ô **Dự án/Nhóm** vẫn hiện đúng tên (kiểm chốt `options.length === 0` không chặn lượt thứ 2) |
| E3 | Mở `TPE.TASK.NB.26.0026` | Cả 4 ô **trống** — đúng dữ liệu, đây là nhiệm vụ nội bộ phòng ban không gắn gì |
| E4 | Mở `TPE.TASK.NB.26.0027` (gắn cuộc họp 152) | Ô **Meeting** hiện `[DEMO 11456] Họp giao việc đầu tuần` |
| E5 | Ở `TPE.TASK.NB.26.0022` bấm **Sửa** → mở ô **Giải pháp** | Danh sách để chọn mới **không** có giải pháp trạng thái ngoài luồng; giá trị đang gắn vẫn giữ nguyên, đổi sang giá trị khác rồi bỏ chọn thì không mất dữ liệu cũ khi chưa lưu |

---

## 3. Những điểm KHÔNG nằm trong phạm vi lần này

- **Nhiệm vụ gắn với Vấn đề (Issue)** — Mr Nam đề xuất tạm pending 17/09, chưa làm.
- Dòng đếm dưới bảng còn hiện đuôi *“nhiệm vụ”* (`Hiển thị 1–4 / 4 nhiệm vụ`); theo skill phải bỏ đuôi, nhưng phải sửa component dùng chung `V2BaseDataTable` của **mọi** màn danh sách nên đang chờ duyệt.
- Biên bản có **Hạn dự kiến đã quá khứ** thì nhiệm vụ kế thừa xong sẽ bị chặn bởi rule “Không được là ngày trong quá khứ”, phải tự sửa ngày. Dữ liệu demo đã đặt hạn tương lai để không vướng; cách xử lý lâu dài đang chờ chốt.

## 4. Dọn dữ liệu demo sau khi nghiệm thu

```sql
-- Chạy trên DB hrm_prod_6_6
DELETE FROM task_org_units WHERE task_id IN (SELECT id FROM tasks WHERE title LIKE '[DEMO 11456]%');
DELETE FROM task_history   WHERE task_id IN (SELECT id FROM tasks WHERE title LIKE '[DEMO 11456]%');
DELETE FROM tasks WHERE title LIKE '[DEMO 11456]%' OR meeting_id = 152;

DELETE FROM meeting_report_executors
 WHERE meeting_report_id IN (SELECT id FROM meeting_reports WHERE meeting_id = 152);
DELETE FROM meeting_reports   WHERE meeting_id = 152;
DELETE FROM meeting_employees WHERE meeting_id = 152;
DELETE FROM meetings          WHERE id = 152;
```

Mật khẩu 3 tài khoản `Test@2026` là do tôi đặt để test trên máy local — đổi lại nếu cần.
