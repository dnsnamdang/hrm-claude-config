# Plan — Báo giá không gắn Dự án TKT (@namdangit)

## Phase 1 — BE
- [x] Migration: quotations.project_id + hrm_contracts.project_id nullable
- [x] QuotationStoreRequest: project_id nullable, customer_id bắt buộc khi không dự án
- [x] Controller prepareStoreData: bỏ gate Sale phụ trách khi không dự án; ensureSaleOfProject → người lập khi không dự án (chốt/hủy chốt/hàng tạm)
- [x] QuotationService::create: nhánh không dự án (snapshot KH từ customers, VNĐ mặc định)
- [x] assertSubmittable: giai đoạn chỉ bắt buộc khi có dự án
- [x] finalize: bỏ kiểm "dự án đã có báo giá trúng thầu" khi không dự án
- [x] copy / updateSalesNote: không dự án ⇒ người lập
- [x] Resource trả cờ can_finalize / can_unfinalize cho báo giá không dự án

## Phase 2 — FE
- [x] Form tạo: bỏ chặn "Vui lòng chọn dự án", chọn KH qua ChooseErpCustomerModal khi không dự án, ẩn Giai đoạn
- [x] Chi tiết + danh sách: nút Chốt báo giá (Trúng thầu) / Hủy chốt cho báo giá không dự án (dùng lại popup chốt)
- [x] Lập hợp đồng chạy với báo giá không dự án

## Phase 2b — Lỗi phát hiện thêm
- [x] BE ContractService: chép dòng báo giá → HĐ lọc theo cột bảng đích (thiếu `internal_note` làm Lập HĐ lỗi 500 ở MỌI báo giá, PROD hrm_contracts = 0 bản ghi)
- [x] FE FinalizeQuotationModal: prop `withoutProject` ẩn câu "Mỗi dự án chỉ có 1 báo giá trúng thầu"

## Phase 3 — Verify
- [x] BE: tinker chạy thông tạo → gửi duyệt → duyệt → chốt → lập HĐ (rollback)
- [x] Test API 53/53 (3 TK: A sale+TP/BGĐ, B, C sale thường): luồng mới 33 case + hồi quy luồng có dự án 20 case
- [x] Test UI Playwright 25/25 (:3002): form tạo/chọn KH/bỏ dự án/lưu, chi tiết chốt-hủy chốt, danh sách, form từ dự án, Quay lại HĐ
- [x] Dọn dữ liệu test + khôi phục DA 161 + mật khẩu TK test
- [x] Test tay Playwright từng bước (13/10 14:00) — sửa thêm 4 lỗi: ô Dự án còn dấu * (không bắt buộc nữa); VNĐ mặc định hiện chậm do chờ cả nhóm danh mục → chỉ chờ danh mục tiền tệ; Địa chỉ KH rỗng khi `address_text` trống → ghép số nhà + phường/xã + tỉnh như danh mục KH; `rows="4"` sai kiểu prop ở popup Hủy chốt

## Phase 4 — Tài liệu
- [x] Sinh SRS màn Báo giá: 12 chức năng, phân quyền, điều kiện ban đầu, bảng công thức/logic giá, xóa, import Excel, duyệt/từ chối, in, xuất Excel và lịch sử.

### Checkpoint — 2026-10-13
Vừa hoàn thành: BE + FE luồng báo giá không gắn dự án (tạo/chọn KH/gửi duyệt/chốt/hủy chốt/lập HĐ), fix Lập HĐ lỗi cột internal_note.
Đang làm dở: không.
Bước tiếp theo: user review → commit; migration 2026_10_13_000001 cần chạy khi deploy.
Blocked:

### Checkpoint — 2026-10-13 14:20
Vừa hoàn thành: commit + push gop_db — hrm-api b61be531f, hrm-client fc94827b6.
Đang làm dở: không.
Bước tiếp theo: deploy dev/prod phải chạy migration 2026_10_13_000001 (không có route mới).
Blocked:
