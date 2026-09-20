# Xuất Excel báo cáo bảo lãnh — dòng tổng cộng + cột "Còn lại"

@khoipv — Màn `contract/reports/guarantee_contract`

File: `hrm-thanhan-client/pages/contract/reports/guarantee_contract/index.vue`
(Toàn bộ xuất Excel làm ở FE bằng ExcelJS — BE không có Export class)

## Vấn đề
1. File Excel không có dòng "Tổng" dưới cùng như lưới danh sách (lưới tổng 4 cột:
   Phí phát hành, Phí mẫu thư, Tiền ký quỹ, Còn lại).
2. Cột "Còn lại" trong Excel lấy thẳng `row.balance` — trường này **luôn = null**
   (cả `buildFlatRows`, `buildTableRows`, `flattenGuarantees` đều gán `balance: null`,
   BE `ReportGuaranteeFlatResource` không trả về) → cột trống.
   Lưới thì tính `getRemainingDeposit(row)` = `deposit_fee - deposit_returned`.
3. Cột "Thực tế phát sinh" ép `parseNumberValue(...) ?? 0` → nội dung chữ bị ghi thành 0.

## Task
- [x] Tách hàm `remainingDepositValue(row)` trả về **số** (dùng chung cho lưới + Excel),
      `getRemainingDeposit` gọi lại hàm này để hiển thị
- [x] Excel: cột `balance` dùng `remainingDepositValue(row)` thay cho `row.balance`
- [x] Excel: cột `incurred_notes` giữ nguyên chữ khi không parse được số
- [x] Excel: thêm dòng "Tổng" cuối bảng (nhãn ở cột Tên khách hàng, in đậm, nền nhạt,
      format `#,##0`) — tổng 4 cột giống lưới
- [x] Kiểm tra lại 2 chế độ: mặc định và "xem theo lần cập nhật" (`isLatestView`,
      có thêm cột "Thời gian cập nhật" nên chỉ số cột lệch 1)

## Ghi chú
- Dòng tổng trong Excel tính trên **toàn bộ dữ liệu xuất** (tất cả trang),
  còn lưới chỉ tổng theo **trang đang xem**.

### Checkpoint — 11/09/2026
Vừa hoàn thành: sửa xong toàn bộ ở `hrm-thanhan-client/pages/contract/reports/guarantee_contract/index.vue`
 - thêm method `remainingDepositValue(row)` (~dòng 690), `getRemainingDeposit` gọi lại hàm này
 - Excel: `balance: this.remainingDepositValue(row)` (~dòng 1151)
 - Excel: `incurredValue` giữ chữ khi không parse được số (~dòng 1126)
 - Excel: khối dòng "Tổng" sau vòng `rows.forEach` (~dòng 1174-1212), `numberColumnIndices` nâng lên ngoài vòng lặp
Đã verify: node --check cú pháp PASS; chạy thử logic + ExcelJS (Node 14, exceljs của client) — tổng 4 cột và dòng cuối ra đúng số, format `#,##0`, in đậm.
Đang làm dở: chưa chạy thử trên trình duyệt với dữ liệu thật
Bước tiếp theo: mở màn `contract/reports/guarantee_contract`, bấm "Xuất excel" ở cả 2 chế độ (mặc định và "xem theo lần cập nhật") để đối chiếu số với lưới
Blocked:
