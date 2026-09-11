# Hướng dẫn tự test — Tiến trình nội bộ 12 bước (Redmine #11426)

Môi trường: nhánh `tpe`, FE `http://localhost:3005`, BE `:8005`. Dữ liệu mẫu tạo ngày 11/09/2026, **không xoá**.

## 1. Tài khoản test (mật khẩu tạm `Test#11426`, đã đổi để test — khôi phục xem mục 6)

| Vai trò | Tài khoản | Employee id | Dùng cho |
|---|---|---|---|
| Sale TH1 | duyck.kd1@tanphat.com | 27 | Dự án không có giải pháp |
| Sale TH2 | hanhbh.kd1@tanphat.com | 28 | Dự án có giải pháp, KD tự triển khai |
| Sale TH3 | manhnv.kd1@tanphat.com | 30 | Dự án liên phòng ban |
| Quản lý giải pháp + TP duyệt giá | tuannd.kd1@tanphat.com | 24 | Tiếp nhận / Từ chối / Yêu cầu bổ sung YC làm GP · duyệt hồ sơ GP · duyệt báo giá cấp 2 |
| PM giải pháp | sondp.da@tanphat.com | 1094 | PM được gán khi tiếp nhận |
| BGĐ duyệt giá | ceo@tanphat.com | 100 | Duyệt báo giá cấp 3 |
| Admin | namdangit@gmail.com | 13 | Xem tất cả |

## 2. Dữ liệu mẫu đã dựng

| Dự án | Mã | Luồng | Đang ở bước | Đã đi qua |
|---|---|---|---|---|
| 249 | HN_KD1.UD.0101.2026.DA046 | TH1 không GP (sale 27) | **11 Đóng** | 1→2→6→7→8→7→8→11 (báo giá BG-2026-00215 tự duyệt cấp 1, chốt, hủy chốt, chốt lại, đóng) |
| 250 | HN_KD1.UD.0101.2026.DA047 | TH2 có GP, KD tự làm (sale 28) | **8 Thương thảo hợp đồng** | 2→4→5→6→7→8 (GP35 · hồ sơ tự duyệt · chốt GP có file · BG-2026-00216 TP 24 duyệt · chốt BG có file) |
| 251 | HN_KD1.UD.0001.2026.DA048 | TH3 liên phòng ban (sale 30) | **8 Thương thảo hợp đồng** | 2→3→2 (YC bổ sung)→3 (gửi lại)→4→5→6→7→8 — toàn bộ bấm trên UI |
| 252 | HN_KD1.UD.0001.2026.DA049 | TH3b liên phòng ban (sale 30) | **11 Đóng** | 2→3→2 (Từ chối YC)→11 (Đóng dự án trên UI) |

Xem nhanh: đăng nhập admin → **Quản lý dự án TKT** → ô tìm gõ `[TEST` → 4 dự án. Mỗi dự án mở `/assign/prospective-projects/<id>/manager`.

## 3. Kiểm tra hiển thị (không cần thao tác)

1. Danh sách dự án: cột **Tiến trình nội bộ** ra badge màu; bộ lọc nâng cao → "Tiến trình nội bộ" có 12 tên mới (`Trao đổi giải pháp với khách hàng`, `Lập dự toán`, `Thương thảo giá và giải pháp`…).
2. Mở dự án 250 hoặc 251: badge trên thanh tiêu đề; khối **5. Giải pháp** có bảng "File xác nhận chốt giải pháp" tải xuống được; tab **Báo giá** dòng Trúng thầu có link file xác nhận dưới badge.
3. Xuất Excel danh sách: cột Tiến trình nội bộ ra tên mới, dự án cha ra bộ tên riêng.
4. Báo cáo → Báo cáo tiến trình dự án TKT (chọn kỳ cả năm) và Báo cáo tổng hợp giải pháp theo phòng ban: bộ lọc/popup ra tên mới.

## 4. Tự đi lại luồng (tạo dự án mới của bạn)

### TH1 — không giải pháp (đăng nhập sale, ví dụ 27)
1. Quản lý dự án TKT → Tạo mới → **Có cần làm GP? = Không**, Cách triển khai = Tự triển khai → Lưu → bước **2**.
2. Tab Báo giá → Tạo báo giá tự lập (1 dòng dịch vụ) → Gửi duyệt → dự án lên **6 Lập dự toán**. Giá < ngưỡng cấp 1 thì tự duyệt luôn; giá lớn (vd 6 tỷ) thì đăng nhập 24 vào `/assign/quotations/<id>` bấm **Duyệt** → dự án **7**.
3. Tab Báo giá → icon ✔ "Chốt báo giá (Trúng thầu)" → **bấm Chốt khi chưa thêm file → phải báo đỏ "Vui lòng đính kèm file xác nhận của khách hàng"**, không gọi API. Thêm file → Chốt → dự án **8**, link file hiện dưới badge Trúng thầu.
4. Icon ↩ Hủy chốt (nhập lý do) → dự án về **7**, file chốt biến mất. Chốt lại → **8**.
5. Footer → **Đóng dự án** (chọn nguyên nhân, tick xác nhận) → **11**, mọi nút sửa ẩn, banner "Dự án đã đóng".

### TH2 — có giải pháp, KD tự triển khai (sale 28)
1. Tạo dự án: **Có cần làm GP? = Có**, Cách triển khai = Tự triển khai → bước 2.
2. Quản lý giải pháp → Tạo giải pháp cho dự án (trạng thái Đang triển khai) → dự án **4**.
3. Màn quản lý giải pháp → tab Hồ sơ → Tạo hồ sơ → Gửi (tự triển khai thì tự duyệt) → dự án **5 Trao đổi giải pháp với khách hàng**.
4. Màn dự án → footer **Chốt giải pháp** → chọn hồ sơ → **bấm Lưu khi chưa có file → lỗi đỏ**; thêm file → Lưu → dự án **6**, khối 5. Giải pháp hiện file, nút Chốt giải pháp ẩn.
5. Báo giá → duyệt → chốt như TH1 → **7 → 8**.

### TH3 — liên phòng ban (sale 30 + quản lý GP 24)
1. Sale: tạo dự án **Có GP**, Cách triển khai = Liên phòng ban, Ứng dụng = "Xưởng cơ điện" (có mẫu phiếu thu thập) → bước 2. Tạo **Yêu cầu làm giải pháp** → Lưu và gửi → dự án **3**.
2. Đăng nhập 24 → mở yêu cầu → tab **Phiếu thu thập thông tin** → Thêm câu hỏi → **Yêu cầu bổ sung** → dự án về **2** (xem trên danh sách; trang yêu cầu chưa tự đổi tiêu đề, F5 để thấy "Yêu cầu bổ sung").
3. Sale 30 → mở yêu cầu → Sửa → **Lưu và gửi** → dự án lên lại **3**.
4. 24 → **Tiếp nhận** (chọn PM, ngày) → yêu cầu "Đã tiếp nhận", dự án vẫn 3. (Nhánh nghịch: bấm **Từ chối** → dự án về 2, như dự án 252.)
5. 24 tạo giải pháp cho yêu cầu (Đang triển khai) → dự án **4**. Lập BOM tổng hợp Hoàn thành → tab Hồ sơ → tạo hồ sơ → Gửi → 24 bấm **Duyệt** → dự án **5**.
6. Sale 30 → Chốt giải pháp (bắt buộc file) → **6** → báo giá → 24 duyệt → **7** → Chốt báo giá (bắt buộc file) → **8**.

### Case nghịch cần thấy bị chặn
- Sale khác chốt giải pháp / chốt báo giá / đóng dự án của người khác → thông báo "Chỉ NV KD phụ trách…".
- Chốt giải pháp khi hồ sơ chưa duyệt → "Hồ sơ không hợp lệ…".
- Đóng dự án lần 2 → "Dự án đã đóng".
- Tạo giải pháp cho dự án chọn "Không cần làm GP" → bị chặn.

## 5. Kiểm tra log tiến trình (bảng `prospective_project_status_logs`)
```sql
SELECT prospective_project_id, status_from, status_to, changed_by, changed_at
FROM prospective_project_status_logs WHERE prospective_project_id IN (249,250,251,252) ORDER BY id;
```
Dự án 251 phải có đủ 9 dòng: NULL→2, 2→3, 3→2, 2→3, 3→4, 4→5, 5→6, 6→7, 7→8. Mọi chuyển bước qua báo giá (6→7, 7→8, 8→7) nay đều có log.

## 6. Dọn dẹp / khôi phục
- Mật khẩu 7 tài khoản test: hash cũ lưu ở `scratchpad/pw_backup_e2e.json` (phiên Claude). Khôi phục bằng tinker:
  `foreach (json_decode(file_get_contents('<file>')) as $r) DB::table('employees')->where('id',$r->id)->update(['password'=>$r->password]);`
- Mẫu phiếu thu thập id 1 ("Mẫu test #11367", ứng dụng Xưởng cơ điện) đã được chuyển sang **Published** để test luồng bổ sung thông tin.
- BOM `BOM-TEST-1109-1237` (dự án 251) được tạo thẳng DB để qua bước gửi hồ sơ, không phải qua màn BOM.
