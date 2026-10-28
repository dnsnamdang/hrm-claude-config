# training — so sánh mốc trước / sau (Task 8.11)

- Trước: `training-truoc.json` (252 ô); chụp lần 2 ngay sau (code chưa đổi) ⇒ **khác 0 ô** (mốc ổn định).
- Sau: `training-sau.json` (252 ô) ⇒ `snap.py diff` **khác 1 ô**:

| ô | trước | sau | lý do |
|---|---|---|---|
| courses.training-status-by-personnel · pv4 (NV 13) | 622 dòng, ids 996b37ff… | 622 dòng, ids 4ff7b2c7… | Thứ tự dòng không xác định: câu `groupBy` không có `ORDER BY` ⇒ trang đầu đổi giữa các lần gọi. Gọi lại 3 lần trên code MỚI ra lần lượt 996b37ff / 4ff7b2c7 / 996b37ff (trùng giá trị mốc trước). Phạm vi 4 ⇒ nhánh không lọc, câu SQL giống hệt code cũ. Không do quyền. |

Kết luận: 251/252 khớp tuyệt đối, 1 ô cùng số dòng, lệch thứ tự trang đầu do báo cáo không sắp xếp (đã chứng minh bằng chạy lại). Không ô U8 (rehearsal không có mã không phạm vi).
