# #12170 [ERP => HRM] Báo cáo - Tùy chỉnh cột (@khoipv)

Redmine: http://quanly.dnsmedia.vn/issues/12170 — "Thêm tùy chỉnh cột cho tất cả các màn báo cáo đã làm" (11 màn trong ảnh).

## Hiện trạng
- 3 màn hạn mức công nợ (`finance/report-limit-debts`, `finance/declare-limit-debts`, `finance/report-limit-debt-employees`)
  dùng V2BaseDataTable, ĐÃ có nút "Cấu hình cột hiển thị" → không sửa.
- 8 màn còn lại dùng bảng `rsum-tb` tự dựng (cột viết cứng trong template) → chưa có:
  tồn kho chi tiết / tổng hợp / theo vị trí / theo kho, tổng hợp xuất nhập tồn, hàng thừa thiếu sau tổng kiểm kê,
  BC theo dõi lắp đặt - bàn giao - SC - BD (+ bản chi tiết).

## Quyết định
- Dùng lại `utils/mixins/columnCustomizationMixin.js` + `ColumnCustomizationModal` (lưu `user_column_settings` theo
  `columnScreenKey`, không migration, không sửa hàm chung). Trang cha khai `allColumns`, truyền `tableColumns` xuống bảng.
- Bảng vẽ `<th>`/`<td>` theo `v-for` cột đang hiện → ẩn/hiện + kéo đổi thứ tự đều ăn.
- Cột khoá (`locked`): STT + cột định danh (tên hàng / nội dung theo dõi). Nhóm cột động (Chi tiết theo công ty / kho)
  là 1 mục trong popup, bật/tắt cả nhóm.
- Mặc định hiện đủ cột như hiện tại.
- Nút: icon `ri-layout-column-line`, cuối nhóm nút `#header-actions`, không gate quyền.
- Phạm vi: chỉ phần hiển thị trên màn. In / Xuất Excel giữ nguyên (báo cáo đã có chọn cột in riêng).
