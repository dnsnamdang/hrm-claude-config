# Plan — Báo cáo so sánh số liệu bán hàng theo khu vực chi tiết theo thời gian

## Phase 1 — BE (hrm-api, Modules/Sale)
- [x] Service `CompareContractByTimeReportService` (tham số + 422, kỳ, phạm vi 4 mức, gom theo khách → tỉnh, so 2 kỳ, filter-options)
- [x] Print service + blade in + Excel export + blade Excel (tiêu đề 2 tầng, chọn nhóm cột)
- [x] Controller + route `v1/sale/reports/compare-contract-by-time` + `checkPermission` mã mới
- [x] Catalog `sale.php`: mã mới (scopes 1-4, platforms hrm)
- [x] Kiểm số liệu bằng SQL độc lập (năm / quý / tháng, lọc tỉnh), phạm vi 4 mức, 422, 403 khi không quyền, tối ưu truy vấn

## Phase 2 — FE (hrm-client)
- [x] `pages/sale/compare-contract-by-time-report/index.vue` + CctSummary + CctTable
- [x] Menu `sale-hub.js` → link + quyền
- [x] Verify trình duyệt 1366px: mặc định năm, đổi quý, cuộn ngang / tiêu đề dính, In bỏ 1 nhóm cột, Excel

## Phase 3 — Bàn giao
- [x] Commit nhánh feat, cập nhật STATUS

### Checkpoint — 2026-11-17 (xong, chưa push)
Vừa hoàn thành: BE + FE + verify (đối chiếu SQL Hà Nội 2025: 755 KH / 3.530 HĐ / 514,955,580,285.75; 403 với TK không quyền).
Quyền local chỉ chèn tạm 1 mã để test rồi đã gỡ — DB local CHƯA catalog-sync.
Bước tiếp theo: user check → push + merge `develop`. Deploy `permission:catalog-sync` + cấp mã ở `/admin/roles`.
Blocked:

### Checkpoint — 2026-11-17 (đã lên develop)
Vừa hoàn thành: push nhánh feat + merge `develop` (api `44d2720bc`, client `5ee6aa610`; merge kéo theo các commit gop_db chưa có ở develop — user đồng ý).
Bước tiếp theo: QA test trên dev; deploy cần `permission:catalog-sync` + migration `notification_mutes` (từ gop_db) + cấp mã ở `/admin/roles`.
Blocked:

## Ngày 17/11/2026 — sau khi lên develop (@junfoke)
- [x] 17/11/2026 — Xử lý build dev lỗi sau merge: `CctTable.vue` import `SaleByProductPagination.vue` theo đường dẫn cũ `pages/sale/sale-by-product-report/components/` trong khi commit `03852b483` (16/11, người khác) đã chuyển bộ component sang `components/sale-by-product-report/` — merge không xung đột nên git không báo, webpack hỏng cả bản build. Sửa đường dẫn, quét toàn bộ import `@/...` không còn file mất. Client `aedd37637` (develop, đã push).
- [ ] Nhánh `feat/bc-so-sanh-bh-khu-vuc-theo-thoi-gian` (worktree `bc-so-sanh-khu-vuc`) vẫn còn đường dẫn cũ ở `CctTable.vue` dòng 95 — kéo develop về hoặc sửa trước khi merge tiếp / lên gop_db.

## Ngày 20/11/2026 (@junfoke)
- [ ] 20/11/2026 — Đang xử lý lỗi QA #12245 – #12249 (2 báo cáo so sánh bán hàng: màn này + `bc-so-sanh-bh-thoi-gian-khu-vuc`). Đã đọc 5 issue + ảnh, đối chiếu code ERP. Số liệu lệch ERP (#12246, #12247, #12249) là do lúc port cố ý không theo lỗi tính của ERP: màn này ERP lọc HĐ bằng mã trạng thái của BÁO GIÁ (`status=2` → trúng phiếu bảo hành ở HĐ dịch vụ, HĐ "Chờ duyệt" ở HĐ hàng hoá; năm 2025 ERP ra đúng 500,000đ toàn phiếu bảo hành). User chốt **giữ cách tính HRM, soạn phản hồi QA** kèm số đối chiếu; vẫn sửa vế "ERP để 0 thì HRM cũng hiện 0" của #12249. Đang làm phần giao diện / bộ lọc / css bảng (so khuôn màn ADB); local phải sync quyền + gán 2 quyền cho tài khoản test mới vào được màn. #12245 / #12248 (icon ⓘ lệch chữ cạnh tiêu đề trang) nằm ở thanh tiêu đề dùng chung `SidebarMenu.vue` — đã hỏi user. Chưa commit.

## Ngày 21/11/2026 (@junfoke)
- [x] 21/11/2026 — Lỗi #12245 – #12249 (QA 2 báo cáo so sánh số liệu bán hàng, chung với plan `bc-so-sanh-bh-thoi-gian-khu-vuc`) — xong, đã lên `develop` (client `3b79eb4f0`, api `375bc2142`):
  - **Tiêu đề trang lệch nút 3 gạch (mọi màn)**: user bảo kiểm kỹ vì màn khác không báo ⇒ nguyên nhân thật là CSS chung đặt lề trên 10px cho mọi thẻ tiêu đề, `mb-0` chỉ bỏ lề dưới ⇒ chữ thấp hơn nút 3 gạch 5px. Sửa ở thanh tiêu đề dùng chung `SidebarMenu.vue` (user đồng ý), nút 3 gạch – tiêu đề – icon ⓘ cùng đường.
  - **"Text và icon lệch" riêng 2 màn**: lỗi thật ở dòng tóm tắt "Năm 2025 → Năm 2026 · Tổng hợp · 38 tỉnh/TP ⓘ" (chữ xám tụt thấp hơn chữ đậm) ⇒ căn thẳng hàng.
  - Cả 2 màn: "Xóa lọc" → "Làm mới" (xoá trắng mọi ô kể cả ô bắt buộc, như ERP); mọi ô chọn có nút x; ô Năm đủ 1970 → năm nay + 25 như ERP (trước cắt từ 2020); thêm nút tùy chỉnh cột (ẩn/hiện, kéo đổi thứ tự 12 cột con, tiêu đề 2 tầng tự ghép); bấm số ở khối tóm tắt mở popup danh sách KH / HĐ (số dòng khớp con số); CSS bảng: cuộn thì hàng tiêu đề 2 đè hàng 1 làm viền lệch bậc với ô "Tỉnh/TP" ⇒ sửa cả 2 bảng.
  - Lệch số liệu #12246 / #12247 / #12249: giữ cách tính HRM như user chốt, soạn sẵn nội dung giải thích cho user dán Redmine.

## Phase 4 — Phản hồi QA 23/11 (popup chi tiết + giá trị gồm phụ lục) — nhánh `fix/bc-so-sanh-popup-chi-tiet`
- [x] BE: phụ lục gộp vào HĐ gốc (+ bổ sung / − giảm, mọi loại, từ Có hiệu lực) — trait `ComparesContractAnnexes`
- [x] BE: item-list nhận ô (tỉnh / tháng) + trả NVKD, Phòng ban
- [x] FE: ô số 2 nhóm bấm mở popup danh sách hợp đồng; popup thêm cột NVKD + Phòng ban; cập nhật chú thích ⓘ
- [x] Đối chiếu SQL độc lập (spec mục 7)
- [x] Verify trình duyệt 1366px (ô Hà Nội BC1 = 3.105 HĐ; ô Tháng 8 BC2 = 594 HĐ; popup vừa khung) + commit api `3208dfc10`, client `73eb621ce`
- [x] Verify giao diện bằng ảnh 1366px (sửa popup dòng TỔNG tràn ngang, client `fc7402553`)
- [x] Lên develop 23/11 (api `f466a38c8`, client `d9e13c2b2`)
