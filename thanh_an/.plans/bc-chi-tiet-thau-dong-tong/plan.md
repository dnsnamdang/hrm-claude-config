# Báo cáo chi tiết thầu — dòng tổng ở lưới và file Excel

@khoipv — Màn `bid_package/detail-report`
File: `hrm-thanhan-client/pages/bid_package/detail-report/index.vue` (xuất Excel làm ở FE bằng ExcelJS)

## Chốt với user
- Lưới: tổng **theo trang đang xem** (KPI đầu trang đã là tổng toàn bộ kết quả lọc)
- Cột cộng tổng: **Số mặt hàng, Tổng trước thuế, Tổng sau thuế**

## Task
- [x] Hằng số `SUMMARY_KEYS = ['product_count', 'total_before_vat', 'total_after_vat']`
- [x] Method `sumRows(rows)` — cộng tổng, dùng chung cho lưới + Excel (ép `Number()` vì API trả decimal dạng string)
- [x] Computed `summaryTotals` (theo `tableData`) + `summaryKeys`
- [x] Lưới: thêm `<b-tr class="summary-row">` cuối `b-tbody`, nhãn "Tổng" ở ô STT,
      ô tổng render theo `visibleColumns` nên **tự khớp khi user ẩn/hiện/đổi thứ tự cột**
- [x] CSS `.summary-row` / `.summary-cell` (nền `#f8fbff`, chữ `#1abc9c` đậm) — giống màn báo cáo bảo lãnh
- [x] Excel: thêm dòng "Tổng" cuối sheet (nhãn đặt ở cột đầu tiên không phải cột tổng),
      in đậm, nền xám nhạt, `numFmt '#,##0'`, viền đủ mọi cột

## Verify
- `node --check` phần script: PASS
- Chạy thử `sumRows` + ExcelJS (Node 14, exceljs của client): tổng 15 / 3.500.000,5 / 3.850.000,55 đúng,
  dòng tổng nằm cuối, nhãn đúng cột, format `#,##0`
- Chưa chạy thử trên trình duyệt với dữ liệu thật

## Ghi chú
- Dòng tổng trong Excel cộng trên **toàn bộ dữ liệu xuất** (mọi trang) — khác lưới (chỉ trang đang xem)
- Tổng = 0 thì lưới hiện `-` do filter global `formatNumber` (`!number → '-'`), đồng nhất với các ô khác

### Checkpoint — 11/09/2026
Vừa hoàn thành: toàn bộ task trên
Đang làm dở:
Bước tiếp theo: mở `bid_package/detail-report`, đối chiếu dòng tổng trên lưới với file Excel, thử ẩn/hiện cột
Blocked:
