# Kế hoạch — 17 màn chứng từ theo chuẩn màn Quốc gia

Design: `design.md` · Spec (lệch từng màn): `docs/superpowers/specs/gop-db/2026-10-28-phieu-theo-chuan-quoc-gia-design.md`
Làm trong `hrm-client/.worktrees/gop-db` + `hrm-api/.worktrees/gop-db` (nhánh develop). Skill: `list-page`,
`new-screens-sweep`, `export-excel`, `button-convention`.

## Phase 0 — Chuẩn hoá tài liệu
- [x] Rà 17 màn, ghi lệch vào spec
- [x] Cập nhật skill list-page (Người tạo = Tên NV - Mã phòng; thứ tự nút theo Quốc gia; chứng từ bắt buộc Xuất danh sách; danh sách màn còn "Từ chối/Không duyệt")
- [x] Cập nhật skill erp-to-hrm-screen (thứ tự toolbar)

## Phase 1 — Lỗi người dùng thấy ngay
- [x] Xuất Excel CẢ DANH SÁCH cho 6 màn Tài chính – tiền: FE `ExportFieldsModal` + `exportFieldsMixin` + `runExport`; BE route `/export` (trước `/{id}`), `ExportColumnRegistry`, `exportRows()` dùng lại query danh sách
- [x] Popup xuất tick đúng cột đang hiện: nạp `exportFieldsMixin`, bỏ `exportExcel` tự viết, chuyển sang `runExport` (6 màn Giữ hàng + Phiếu chuyển hàng nhập thẳng + Gia hạn hàng mượn); gửi kèm sort
- [x] Gỡ "Từ chối"/"Không duyệt" khỏi danh sách: prepick-extend-requests, borrow-extend-requests, warranty-repair-requests, warranty-repair-handle-requests
- [x] Sort cột Ngày duyệt: key `approved_time` → khớp BE `approvedTime` (prepick-extend-requests, prepick-transfer-requests)
- [x] Số tiền Phiếu chi ra 1,234,567 (`BillPaymentListResource` number_format)
- [x] Ngày tạo Phiếu ủy nhiệm chi có giờ phút (`d/m/Y H:i`, cột 140px)
- [x] Màu trạng thái Phiếu yêu cầu chuyển hàng theo bảng 9 màu (BE trả `status_color`, FE `:color`)
- [x] "Đang xuất giữ" → #2563EB (`ProductPrepickRequest::STATUSES`)
- [x] Phiếu báo có: "Duyệt" ở danh sách → `to` chi tiết, bỏ popup + 2 hàm duyệt tại chỗ, icon `ri-checkbox-circle-line`
- [x] Phiếu yêu cầu chuyển hàng: hiện ô lọc Công ty/PB (thêm field `org` + slot, khai `inputCount`)

## Phase 2 — Cột & nhãn
- [x] "Người lập/Ngày lập" → "Người tạo/Ngày tạo" ở ô lọc, cột, form, popup tìm phiếu (danh sách ở spec)
- [x] Người/Ngày cập nhật `isVisible: false` (8 màn); thêm cột + BE cho Gia hạn hàng mượn
- [x] Người tạo/Người cập nhật dùng `employeeAuditLabel()` ở mọi List Resource liên quan
- [x] Bộ cột mặc định ~7 (+ Khách hàng/Loại phiếu); thứ tự Người tạo → Ngày tạo → Trạng thái → Hành động; hiện cột Khách hàng (4 màn Giữ hàng)
- [x] V2BaseBadge `:color` cho Đề nghị thu tiền, Đề nghị thanh toán (bỏ pill tự dựng); các màn còn dùng `variant` chuyển `:color` + BE `status_color`
- [x] Phiếu xử lý yêu cầu: cột "Người xử lý" → "Người tạo"

## Phase 3 — Hành vi & hình thức
- [x] Thao tác xong quay về danh sách (Đề nghị thu tiền, Đề nghị thanh toán, YC chuyển hàng, YC kiểm tra SC-BH, Phiếu xử lý yêu cầu)
- [x] Bỏ `.text-muted` / ô "-" "—" "_" ở form & popup (danh sách ở spec)
- [x] Hành động chuyển trang khai `to` (Tạo phiếu thu, Sửa/Tổng hợp YC chuyển hàng, Tạo phiếu xử lý, Tạo phiếu cung cấp TT)
- [x] Thanh nút: Tạo mới → In → Xuất → Import → Tuỳ chỉnh cột (`V2BaseButton secondary size="sm"`, `btn-compact`). Rà 28/10: In đang đứng SAU Xuất ở `customer-care/warranty-repair-requests` và `warranty-repair-handle-requests` → dời lên; 7 màn khác đã đúng.
- [x] Footer chi tiết: thứ tự chính → phụ → nguy hiểm

## Phase 4 — Nghiệm thu
- [x] Chạy bộ tự kiểm cuối skill list-page cho 17 màn
- [x] Playwright: mở 17 màn, chụp ảnh, kiểm thanh nút + cột + màu badge; Xuất Excel thử thật 2 màn, 4 màn còn lại so total API

## Checkpoint — 2026-10-28 (cuối ngày)
- **Vừa hoàn thành:** Phase 1–4 cho 17 màn (3 agent song song theo nhóm + nghiệm thu Playwright). Diff: FE 47 file, BE 45 file + helper mới `app/ExcelExport/Support/ExportRowsPage.php`. Commit LOCAL nhánh `feat/phieu-theo-chuan-quoc-gia` (client 77079b38e, api 4e6123d19), chưa push; worktree gop-db đã switch về develop.
- **Còn treo, chờ user chốt:** UNC 3 select Công ty/PB/BP rời + ô "Mã phiếu" trùng ô tìm nhanh; Phiếu báo có `sum_money_text` 2 số lẻ; ĐN thanh toán duyệt xong về list không giữ `?mode=pending`; màu tự gán ("Đã tạo phiếu thu" #2563EB, "Chờ tạo/duyệt phiếu chi" #D97706, "Duyệt phiếu chi"/"Đã hạch toán" #16A34A, "Đã xuất kho" #2563EB); `<h6 font-weight-bold>` tự dựng ở form Hủy/Điều chuyển hàng giữ; ô org đếm 1 khi user không có phạm vi (3 màn); nhãn lọc "Người yêu cầu" ở YC KT SC-BH.
- **Lưu ý:** user đã lưu cấu hình cột thì vẫn thấy thứ tự/ẩn hiện cũ (columnCustomizationMixin ưu tiên cấu hình đã lưu).
- **Bước tiếp theo:** user cho phép → merge nhánh vào develop + push.
- **Blocked:** —

## Ngày 28/10/2026 (@junfoke)
- [x] 28/10/2026 — Rà 17 màn "DNS đang fix" so với màn Danh mục quốc gia (đã pass) + skill list-page / button-convention / entity-history, báo cáo lệch theo 4 mức.
- [x] 28/10/2026 — User chốt: bắt buộc Xuất Excel danh sách; giữ nhãn "Lập từ yêu cầu"; ô lọc nhân viên dạng "Tên NV - Mã phòng"; thanh nút theo màn → cập nhật skill.
- [x] 28/10/2026 — Đổi chuẩn thanh nút Tạo mới → In → Xuất Excel → Import → Tuỳ chỉnh cột (skill list-page + erp-to-hrm-screen); dời nút In ở YC kiểm tra SC-BH và Phiếu xử lý yêu cầu.
- [x] 28/10/2026 — Sửa 17 màn (Excel DS qua helper `ExportRowsPage`, màu trạng thái — "Đang xuất giữ" sang xanh dương, quay về DS sau thao tác, bỏ ô "-") + nghiệm thu Playwright. Commit local `feat/phieu-theo-chuan-quoc-gia` client `77079b38e` / api `4e6123d19`, chưa push.
