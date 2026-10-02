# Mẫu in ĐNTT — làm tròn số công / số ngày (design tóm tắt)

Phụ trách: @junfoke — Ngày: 09/09/2026

## Vấn đề
QA báo: PGV `TPSG.PGV.2026016101`, màn duyệt ĐNTT hiện **10.13** công khoán phụ, nhưng
mẫu in hiện **10.129999999999999**.

## Kết luận điều tra
Không phải lệch dữ liệu, chỉ là **lệch cách format**:

- Giá trị gốc nằm ở DB ERP, bảng `wr_assign_tasks` (connection `mysql2`), cột JSON `summary`
  của dòng con (`parent_id` = id PGV) → `rate_effort.work_p3_approve` = chuỗi
  `"10.129999999999999"` (ERP cộng float rồi ghi thẳng, hàng loạt key khác cũng dính:
  `total_approve`, `work_p3_result`, `total_repair_approve_accept`…).
- PGV này là **việc khác** (`assign_other_request_id = 2798`) → BE
  `PaymentBusinessRequestRepository::getWrAssignTasks` lấy `revenue_cost_approve_accept` (= 0)
  cho "Tổng định mức công" và `work_p3_approve_accept` cho "Tổng công khoán phụ". Khớp mẫu in.
- Màn duyệt (`components/WrAssignTaskList.vue`, `components/PrintTab.vue`) có
  `| formatNumber` (làm tròn 2 số) → 10.13. Mẫu in `_id/print.vue` **thiếu filter** → lộ đuôi float.

## Quyết định
- Chỉ sửa FE hiển thị: thêm `| formatNumber` ở `_id/print.vue`. KHÔNG đụng dữ liệu ERP,
  KHÔNG sửa cách ERP ghi `summary` (rủi ro lan rộng, không thuộc phạm vi bug này).
- Thêm cho cả các cột số ngày/đêm cùng rủi ro, không chỉ 3 dòng công — để không phải quay lại.
- Giá trị 0 sẽ hiện `-` (đúng hành vi `formatNumber`), khớp với màn danh sách và các cột tiền
  khác đang dùng sẵn filter này trong cùng mẫu in.

## Lưu ý kỹ thuật
`_id/print.vue` là file **CRLF**. Sửa bằng `sed -i` sẽ nuốt `\r` toàn file (diff phình 677 dòng) —
đã dính và phải khôi phục lại CRLF. Xem `CLAUDE.md` mục "Line ending".
