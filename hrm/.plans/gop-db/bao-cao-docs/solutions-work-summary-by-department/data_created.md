# Dữ liệu tạo cho SRS — Báo cáo tổng hợp giải pháp theo phòng ban

**Không tạo dữ liệu mới.** Báo cáo đã có số liệu thật trên DB `local_hrm_erp`:
30 giải pháp (bảng `solutions` id 1–30, ngày tạo 05–07/2026, nhiều phòng / nhiều nhân sự kỹ thuật),
nên ảnh chụp dùng bộ lọc **Kiểu thời gian = Năm, Năm = 2026** (đặt qua trạng thái màn, không ghi DB).

Lưu ý khi đối chiếu số liệu trên ảnh:
- Bản chính (SRS báo cáo "Theo dõi YCLGP theo phòng KD") đã tạo thêm `request_solutions` id 21–30
  (mã TPE.YCP.TC.26.0901–0910) và `solutions` id 31, 32 (mã …_GP901, …_GP902) trong cùng phiên —
  2 giải pháp này nằm trong tháng 10/2026 nên có mặt ở ảnh `00-mac-dinh.png` (bộ lọc mặc định
  tháng hiện tại) và cộng vào tổng năm 2026 (33 giải pháp).
- Thao tác Xuất Excel / In chỉ đọc dữ liệu; popup "Cài đặt bộ lọc" chỉ mở rồi Đóng, không bấm Lưu.
