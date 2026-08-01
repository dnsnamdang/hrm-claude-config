# Plan — HDSD màn "Phê duyệt → Báo giá chờ duyệt"

Người phụ trách: @dnsnamdang
Output: `HDSD_luongchinh/HDSD_PheDuyet_BaoGiaChoDuyet.docx`
Ảnh nguồn: `hdsd_bgchoduyet_shots/` (11 ảnh)
Tài khoản chụp: namdangit@gmail.com — https://dev-hrm.eteksofts.com/assign/quotations/pending-approval

## Phase 1: Khảo sát code
- [x] FE: pending-approval/index.vue, quotations/_id/index.vue (footer nút duyệt/từ chối, computed canTpApprove/canBgdApprove/canReject, doTpApprove/doBgdApprove), QuotationRejectModal.vue, column-customization-modal, menu-sidebar.js
- [x] BE: route group /assign/quotations (middleware checkPermission trên pending-approval / tp-approve / bgd-approve / reject), QuotationController::pendingApproval, QuotationService::getPendingApproval + applyListFilters + submit/selfApprove/tpApprove/bgdApprove/reject + ensureTpCanApprove/ensureBgdCanApprove/getManagedDepartmentIds, notifyByPermission/notifyApproved/notifyRejected, cascadeApprovedStatus, syncToErpAfterApproval
- [x] Luồng ngược: BomPriceApprovalConfigService::calculateApprovalLevel (max(levelV, levelM), fallback cấp 3), Quotation::getStatusList, PermissionsTableSeeder (1081/1082)

## Phase 2: Chụp ảnh thật (Playwright MCP, 1440x900)
- [x] 01 danh sách, 02 bộ lọc nâng cao, 03 popup Tuỳ chỉnh cột, 10 menu Phê duyệt
- [x] 05 chi tiết BG-2026-00168 cấp 2 (nút Duyệt), 04 chi tiết BG-2026-00148 cấp 3 (nút Duyệt & chuyển BGĐ)
- [x] 06 bảng Tổng hợp giá trị + TSLN trước/sau GG, 08 hộp xác nhận duyệt, 07 popup Từ chối, 09 Lịch sử báo giá
- [x] 11 màn Cấu hình duyệt giá (nguồn ngưỡng cấp duyệt) — dùng cho ví dụ số
- [x] Không ghi dữ liệu: hộp xác nhận duyệt bấm Huỷ, popup Từ chối bấm Huỷ, popup cột bấm Huỷ

## Phase 3: Dựng Word
- [x] Generator scratchpad `gen_bg_choduyet.py` (hdsd_p5_work/hdsd_lib.py, khung HDSD_DanhMuc/HDSD_VaiTroDuAn.docx)
- [x] TỔNG QUAN (thuật ngữ C1/C2/C3/V/M/TSLN, quyền + phạm vi TP theo phòng quản lý / BGĐ theo công ty)
- [x] P1 vì sao cần duyệt giá + công thức max(cấp theo V, cấp theo M) + ví dụ số BG-2026-00168 (1.156.035đ, TSLN 14,46% → Cấp 2) + vòng đời trạng thái
- [x] P2 truy cập & bố cục | P3 lọc + tuỳ chỉnh cột | P4 8 cột
- [x] P5 đọc phiếu trước khi duyệt (thanh tiêu đề, thông tin chung, bảng chi tiết, tổng hợp giá trị + mức sàn, lịch sử)
- [x] P6 Duyệt (TP cấp 2 vs cấp 3, BGĐ, 7 hệ quả tự động sau khi Đã duyệt, lỗi) | P7 Từ chối (reset cấp duyệt khi gửi lại)
- [x] P8 thông báo tự động | P9 FAQ
- [x] Build + verify: 12 Heading 1, 11 hình + 11 caption, 13 bảng, updateFields=true, broken=0, ~1.4MB

### Checkpoint — 27/07/2026
Vừa hoàn thành: HDSD_PheDuyet_BaoGiaChoDuyet.docx (9 phần + tổng quan).
Đang làm dở: không
Bước tiếp theo: user review nội dung.
Blocked:
