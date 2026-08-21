# Phiếu yêu cầu chuyển hàng (ERP → HRM) — design tóm tắt

> Phụ trách: @khoipv · Bắt đầu: 2026-08-05 · Nhánh: `gop_db` (cả 2 repo)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-05-finance-product-transfer-request-design.md`

## Mục tiêu

Port màn ERP "Phiếu yêu cầu chuyển hàng" (`admin/warehouse/product_transfer_requests?type=all`,
3 bảng `product_transfer_requests` + products + product_details, mã `PYCCH-xxxxx`, 13 trạng thái)
sang HRM phân hệ **Tài chính**, nhóm **Xuất hàng** (slot xám `finance.js:134`).
**HRM là bản thay thế lâu dài** — 2 cổng chạy song song cùng bảng trên DB gộp, KHÔNG đổi schema.

## Quyết định đã chốt (user 2026-08-05)

1. **Port đầy đủ**: list + tạo/sửa/xóa nháp + gửi duyệt + xem + Không duyệt (reject) + In
   (template 87) + Export Excel + đính kèm PDF S3. Nút **Tổng hợp** (Kế toán kho tiếp nhận)
   mở tab sang màn ERP Yêu cầu xuất hàng (chưa port, thuộc phân hệ Kho).
2. **Dùng lại quyền ERP**: 878/879/880 (xem theo cấp) update tay `type=8` + "Kế toán kho" (80)
   gate reject/Tổng hợp. Logic phạm vi theo cấp port nguyên `searchByFilter`. Quyền "theo bộ
   phận" seeder thiếu → kiểm tra DB thật.
3. **1 màn danh sách duy nhất** (= `type=all`); không port forAccounting/can_request.
4. **Form port đầy đủ**: popup Thêm hàng hóa + Xem tồn theo kho/nhóm kho + giá niêm yết +
   ĐVT hệ số; form = trang riêng create/edit; dòng hàng × dòng con khách hàng (SL, ngày cần).
5. **Xóa/Sửa giữ nguyên ERP**: status=3 (Đang tạo) + là người tạo → xóa cứng cascade.
6. **Nới validate khi sửa**: `date_needed after:today` chỉ áp dòng mới/dòng đổi ngày
   (ERP re-validate tất cả → phiếu cũ không sửa nổi).

## Điểm kỹ thuật chính

- BE `Modules/Finance`, routes `/v1/finance/product-transfer-requests` (9 route + API phụ trợ
  hàng hóa/ĐVT/giá/tồn kho/khách hàng — ưu tiên tái dùng endpoint có sẵn). KHÔNG mysql2.
- HRM chỉ ghi status 2↔3; status 1, 4–12 do chuỗi kho ERP đẩy, 13 không ai set (chỉ hiển thị).
- Gửi duyệt notify nhóm "Kế toán kho" qua bảng notification ERP (2 cổng cùng reo).
- Lỗi ERP chủ động sửa: deleteFile unlink public_path trong khi file ở S3; catch Exception
  sai namespace; validate after:today khi update (quyết định 6).
- FE đọc skill `button-convention`, `modal-popup`, `print-page`, `list-page`; áp 4 bài học
  phân trang finance-account-catalog; menu 1 link = 1 phân hệ (gotcha resolveSubsystem).
- 6 phase: BE nền → FE list → Form → Chi tiết+reject → In/Export/S3 → Verify (HTTP +
  Playwright + đối chiếu 2 cổng).
