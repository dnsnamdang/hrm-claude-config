# Design — HDSD màn "Phê duyệt → Yêu cầu giải pháp"

## Mục tiêu
Tài liệu HDSD Word cho người dùng cuối (trưởng phòng/bộ phận giải pháp) của màn
`/assign/request-solution/pending`, giải thích cả **vì sao** cần bước phê duyệt này chứ không chỉ
liệt kê nút.

## Hiểu biết nghiệp vụ chốt được từ code
- Màn là **hàng đợi**: chỉ `status = 2 (Chờ tiếp nhận)`. Xử lý xong là rời khỏi màn.
- Phạm vi dữ liệu theo `prospective_projects.implementation_type`:
  - 3 Liên phòng ban (và NULL cũ): `receive_dept ∈ listManageDepartmentIdsWithOwn()`
  - 2 Triển khai theo phòng: `receive_dept = phòng của user`
  - 1 Tự triển khai: không sinh YC làm GP
- Chỉ 1 quyền chi phối: **Tiếp nhận yêu cầu làm giải pháp** (permission id 1012) — menu, vào màn,
  nhận notify, nút Tiếp nhận, gửi câu hỏi bổ sung.
- **Không có nút Từ chối** (code đã comment). Hai lối ra: Tiếp nhận (status 3) hoặc Yêu cầu bổ sung
  (status 9).
- Hạn tiếp nhận `need_receive_date` = sent_date + response_days (đếm theo ngày có phân ca của trưởng
  phòng tiếp nhận, trừ ngày lễ) + response_hours; response_* lấy từ Mức độ ưu tiên của Giai đoạn dự án.
  Gửi lại sau "yêu cầu bổ sung" → reset đồng hồ.
- Nhãn hạn realtime trong Resource: Trong hạn / Sắp đến hạn (warning_date = lùi 1 ngày làm việc, hoặc
  đã bắn cron) / Quá hạn; sau khi phản hồi chốt cứng "Đã xử lý (Trong hạn|Quá hạn)" từ
  `responded_deadline_status` → dữ liệu cho báo cáo hiệu suất.
- Tiếp nhận: `lockForUpdate` + kiểm tra lại status → chống 2 người cùng nhận (HTTP 409).
- Yêu cầu bổ sung ghi câu hỏi vào section `is_addition` của form snapshot + log lịch sử + đổi status 9
  + notify KD.
- Downstream: tạo Giải pháp → status 6 Đang thực hiện; xoá Giải pháp → về 3 Đã tiếp nhận; dự án đóng
  → status 10 Đóng (khoá sửa/xoá).

## Output
- `HDSD_luongchinh/HDSD_PheDuyet_YeuCauGiaiPhap.docx` — 14 Heading 1, 12 hình, 16 bảng, ~1.7MB
- Ảnh: `hdsd_ycgp_pending_shots/` (12 ảnh, 1440x900)
- Tái dựng: `/opt/homebrew/opt/python@3.14/bin/python3.14 <scratchpad>/gen_ycgp_pending.py` chạy từ
  thư mục gốc `HRM/`.
- **Style**: khung = `HDSD_KhachHang.docx` (bản gốc thư mục HRM/), dựng qua `hdsd_clean.HDSDClean`
  (subclass của `hdsd_p5_work/hdsd_lib.HDSD`) — KHÔNG áp direct formatting: Heading/List Bullet/ô bảng
  để nguyên style, body chỉ canh đều, ảnh canh giữa 6.0". Đây là điểm khác `hdsd_lib.HDSD` gốc (ép
  Times New Roman + line-spacing 1.5 + Heading canh giữa) — dùng bản clean để đồng bộ với file mẫu.
