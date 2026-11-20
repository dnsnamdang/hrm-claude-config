# Plan — Báo cáo phân công phòng phụ trách thương hiệu - hãng sản xuất (@junfoke)

Nhánh `feat/bc-phan-cong-phong-thuong-hieu` (tách `origin/gop_db`, không track), worktree `.worktrees/bc-pc-thuong-hieu` ở hrm-api + hrm-client.

## Phase 1 — Khảo sát (16/11/2026)
- [x] Đọc ERP controller / service / blade / menu (2 lối), dữ liệu local
- [x] Báo user 4 điểm cần chốt → user chốt: cả 2 lối · type=all phải kiểm quyền · BC theo NV để sau · sửa lỗi ERP

## Phase 2 — BE
- [x] `AssignDepartmentBrandReportService` (cặp mới nhất trong phiếu đã duyệt, người phụ trách mới nhất, phạm vi 2/3/4, lọc AND, nhóm + phân trang theo nhóm, summary, filter-options kèm `department_ids` của người, lịch sử)
- [x] `AssignDepartmentBrandReportPrintService` (chọn cột, trần 3.000 dòng) + blade in
- [x] Excel + blade, STT ghi chuỗi (binder)
- [x] Controller + route `v1/purchase/reports/assign-department-brands` + `checkPermission`; Catalog thêm `hrm`
- [x] Test script: 1.145 cặp / 58ms; phạm vi 4/3/2/0 = 1145/1069/975(phòng 46)/0; lọc người mua đúng 73 cặp; company_id chỉ ăn ở mức 4; lịch sử cặp ngoài phạm vi 404; HTTP 200 cả 5 endpoint, Excel `?token=`

## Phase 3 — FE
- [x] Trang + AdbSummary + AdbTable + AdbHistoryModal + InfoTip (khuôn report-styles)
- [x] Menu: lookup.js `link ?type=all` + codes; purchase.js nhóm Báo cáo
- [x] Verify trình duyệt 1366 (worktree api 8100 / client 3100): 2 lối (Tra cứu không In/Excel/Lịch sử), đổi Tổng hợp theo, cấp bung + mũi tên, lịch sử (tô ô đổi), lọc Phòng mua -> Người mua 25→10, In bỏ 2 cột -> bản xem trước đúng 2.022 dòng + letterhead, Excel STT chuỗi
- [x] Sửa sau verify: tên phòng trong ô lọc lấy tên hiện tại (`departments`) — phiếu cũ lưu tên khác cho cùng phòng
- [ ] Chờ user: bật phân hệ Mua hàng ở HRM hay cách khác cho lối Mua hàng

## Phase 4 — Bàn giao
- [x] Commit nhánh feat: api `808c3f50e`, client `7307aa85f` (chưa push)
- [ ] Push + merge develop khi user bảo

### Checkpoint — 2026-11-16 11:50
Vừa hoàn thành: BE + FE + verify trình duyệt, commit 2 repo.
Đang làm dở: —
Bước tiếp theo: user chọn cách hiện lối Mua hàng (bật phân hệ Mua hàng như Kho/Vận chuyển, hay giữ ẩn); push + merge develop khi user bảo.
Blocked: quyết định phân hệ Mua hàng.

### Checkpoint — 2026-11-16 (merge develop)
Vừa hoàn thành: push `feat/bc-phan-cong-phong-thuong-hieu` + merge vào `develop` (api `77e6b4ffc`, client `1e78669a5`).
User chốt: lối Mua hàng › Báo cáo để nguyên (phân hệ Mua hàng còn ẩn, sau sẽ bật) — chỉ chuyển lối Tra cứu - thông báo trước.
Bước tiếp theo: chờ test dev; lên gop_db khi user bảo. Deploy: `permission:catalog-sync`.

## Ngày 17/11/2026 (@junfoke)
- [x] 17/11/2026 — Hỗ trợ check vì sao người dùng vào màn lại hiện phân hệ Mua hàng: họ vào đúng lối Tra cứu (`?type=all`), nhưng hàm dùng chung `findSubsystemByLink` (`components/subsystems.js`) bỏ phần query nên hoà với lối Mua hàng (đang `hidden` + `erpGhost`), rồi chọn theo `sessionStorage` / tiền tố URL `/purchase` → mở tab mới, dán link, F5 tab mới là rơi vào Mua hàng.
- [ ] Chờ user duyệt (hàm dùng chung): khi hoà ưu tiên mục menu khớp cả query (như `screenTitleOf`) + bỏ phân hệ `hidden` khỏi lượt chọn. Chưa sửa.

## Ngày 20/11/2026 (@junfoke)
- [x] 20/11/2026 — Lỗi #12235 (BC phân công phòng phụ trách thương hiệu): menu — bỏ link ở mục Mua hàng (mục chuyển xám), màn chỉ thuộc Tra cứu - thông báo nên ra header xanh đậm + sidebar hub (thay cho cách sửa hàm dùng chung `findSubsystemByLink` ngày 17/11); thêm import `v2-styles` cho khoảng trắng như các báo cáo khác; ổ khoá 🔒 cho ô Công ty / Phòng ban (sửa `companyOptions` làm rơi cờ `is_locked`: tắt 6 công ty, bật 9); ô Thương hiệu / Hãng lấy toàn bộ danh mục y ERP (1.354 / 1.049), Phòng + NV lấy người đang phụ trách trong lịch sử phân công; căn icon ⓘ lệch chữ (inline-flex); thêm Tùy chỉnh cột ở cả 2 lối.
- [x] 20/11/2026 — Lỗi #12236: bắt buộc chọn Công ty với quyền tổng công ty y ERP (lần đầu tự chọn công ty người xem, xoá trống thì báo đỏ "Bắt buộc chọn", BE cũng chặn); khối thống kê các ô bằng nhau, số khác 0 bấm mở popup danh sách (`AdbItemListModal.vue` + API item-list, có tìm / sắp xếp / phân trang); cột Thương hiệu/Hãng thu 360px; cột Lịch sử thay đổi hiện ở cả 2 lối.
- [x] 20/11/2026 — Lỗi #12237: STT dạng 1 → 1.1 + in đậm dòng nhóm (theo self-inventory-report) cho màn này và 3 bảng báo cáo vận chuyển (xem plan `van-chuyen-bao-cao`). Kiểm ảnh local (API 8000, Nuxt 3010). Commit #12235–#12237: client `6b01afddc`, api `9b8766e05` (develop, đã push).
- [x] 20/11/2026 — Hỗ trợ tra "còn màn nào tương tự URL `?type=all`": phân hệ Mua hàng chỉ có đúng màn này (+ Tổng quan); Mua hàng đang `hidden` + `erpGhost` nên người dùng chỉ vào qua Tra cứu › Thông báo; màn cùng kiểu tham số `type` gần nhất là BB bàn giao nghiệm thu theo NV (`?type=for-business-staff`, Giao việc — không khoá).
- [x] 20/11/2026 — Theo user "cho đủ tất cả để họ check in, xuất…": lối Tra cứu `?type=all` hiện đủ nút In báo cáo + Xuất Excel (bỏ `isLookup` ở `index.vue`, sửa comment `lookup.js`); cột Lịch sử đã có sẵn trên develop. Client `0bee2c6ac` (develop, đã push). Chưa mở bản develop để thử. Còn: 4 file sửa bản cũ đầu tiên trên nhánh `task_12091` chưa commit — đề nghị bỏ, chờ user.
