# Phiếu nhập kết quả CSKH (ERP → HRM) — @khoipv

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-11-02-phieu-nhap-ket-qua-design.md`
Khảo sát: `khao-sat-A-danh-sach-chi-tiet.md` (danh sách/chi tiết/xóa/không duyệt) · `khao-sat-B-form-luu.md` (form tạo/sửa + lưu)

## Mục tiêu
Port màn ERP `WrImportResults` (`/admin/customer-care/wr_import_results?type=all`) — phiếu nhập kết quả lập từ Phiếu giao việc
(nút "Nhập kết quả"), nối tiếp màn Phiếu giao việc (`.plans/gop-db/phieu-giao-viec/`).

## Quyết định (user chốt 02/11/2026)
- Trọn bộ 1 lần: Danh sách · Chi tiết · Tạo · Sửa · Xóa · Không duyệt. "Duyệt kết quả" → link ERP tab mới.
- **Nghiệp vụ y hệt ERP, kể cả lỗi** (lỗ quyền + lỗi ghi dữ liệu) — liệt kê ở spec mục 9.
- Ảnh thi công/bàn giao mới lên S3 HRM (URL tuyệt đối); ảnh cũ path tương đối ERP hiển thị bằng `ERP_URL` + path; ERP/app xem được ảnh S3 không cần sửa.
- Bộ bắt buộc HRM + In: Xuất Excel, Cấu hình cột, Lịch sử 2 nơi, In danh sách, toast QLDA, 409.
- Danh sách giữ y ERP cả "Duyệt kết quả" (ERP) + "Không duyệt kết quả" (popup) — lệch skill list-page có chủ ý (user chốt 02/11).
- 4 quyền mới type 24 tên nguyên văn ERP; không middleware (y ERP). Menu CSKH sau bán › Giao việc › "Phiếu nhập kết quả".

## Phạm vi code
- BE `Modules/CustomerCare`: entity `WrImportResult` + 15 bảng con + `AssignTaskSerialProgress` + timesheet; service list/show/delete/reject,
  source/edit-data, store/update (+ATP 6 nhánh), validate serial + phiếu xuất, port `getListProductOfCustomer`, print/export, thông báo;
  route `/v1/customer-care/wr-import-results`.
- FE `pages/customer-care/wr-import-results/` (index, create, `_id/index`, `_id/edit`) + `WrImportResultForm.vue` + bảng con; menu; nối PGV.

## Phase 5 — Duyệt kết quả (user chốt 03/11/2026)
- Không màn riêng: trang con `/customer-care/wr-import-results/{id}/approve` (chế độ duyệt của form PNKQ), nút "Duyệt kết quả" bỏ link ERP.
- Ghi y ERP: PDKQ = `wr_assign_tasks.parent_id`, bảng con PGV; 3 nút Lưu / Duyệt / Không duyệt; 1 cấp duyệt.
- Sửa 5 lỗi ERP làm sai dữ liệu, các quirk khác giữ; bỏ 3 ô ghi chú không lưu; chi tiết PNKQ thêm khối "Kết quả duyệt" chỉ đọc.
- Không port BKS / KT kho trả về / xoá PDKQ / danh sách PDKQ + chờ hạch toán.
- Chi tiết: spec mục 11, khảo sát `khao-sat-C-duyet-ket-qua.md`.
