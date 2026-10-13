# Plan — Báo cáo phân chia thị trường

> @junfoke · 2026-10-05 · nhánh `develop` · Spec: `docs/superpowers/specs/gop-db/2026-10-05-presale-division-market-report-design.md`

## Phase 1 — BE

- [x] Quyền 1679 `Xem báo cáo phân chia thị trường` (type 29, group riêng) — seeder + insert local. Không gán sẵn cho role nào (các quyền mới gần đây cũng không tự gán Super admin)
- [x] `Modules/Assign/Services/Report/DivisionMarketReportService.php`: truy vấn ERP + sửa 3 lỗi lọc, filter-options (1 lượt quét, cache 10'), export, bản in mẫu 458
- [x] `DivisionMarketReportController` + 4 route `/v1/assign/report/division-market`, gate `checkPermission`; in chặn trần 2.000 dòng (`LimitsPrintListRows`)

## Phase 2 — FE

- [x] `pages/assign/report/division-market/index.vue` — 8 ô lọc (tỉnh thu hẹp theo khu vực, xã theo tỉnh, NV theo phòng), bảng gộp ô 4 cấp, In, Xuất Excel (bảng phẳng)
- [x] Menu `presale.js` nhóm "Báo cáo thị trường" + `isShow`

## Phase 3 — Verify

- [x] Đối chiếu với chính service ERP chạy trên gop_db: toàn bộ 60.171 dòng khớp tuyệt đối (bỏ qua cột cờ — xem dưới);
      7 bộ lọc (tỉnh, xã, phòng, NV, khu vực 1, hãng xe, tổ hợp) khớp md5
- [x] Lỗi đã sửa có số chứng minh: Phụ trách hãng ERP "Có" = 0 dòng → HRM Có 30.121 + Không 30.050 = 60.171;
      khu vực 3 + 4 = 20.755 + 10.744 = 31.499
- [x] Playwright + xem ảnh: danh sách, lọc Cao Bằng (744) + Không (504), In (mẫu 458 + header), Excel 504 dòng,
      menu hiện khi có quyền; KHÔNG quyền: menu ẩn, vào link → 404, API 403
- [x] Dọn quyền cấp tạm cho role 18 / NV 13 trên local

Phát hiện khi verify (đã xử lý):
- 292 nhóm (tỉnh, xã, phòng, NV) có nhiều dòng `dmew` khác cờ phụ trách → gộp 1 dòng, cờ = MAX (ERP lấy bất kỳ)
- ERP 15 tỉnh/trang vẽ ~36.000 dòng → HRM phân trang theo phường/xã (20/trang, ~475 dòng), STT tỉnh liên tục
- Ô gộp trên màn canh ĐẦU (canh giữa thì tên tỉnh rơi khỏi màn hình). Bản in vẫn canh giữa vì style in dùng chung
  `utils/print/reportPrintStyle.js:89` ép `vertical-align: middle !important` — chưa sửa (file dùng chung, cần hỏi user)
- FE nạp quyền CHỈ qua role (`role_has_permissions` theo công ty) — gán quyền thẳng cho NV không có tác dụng ở menu

## Checkpoint — 2026-10-05

- **Vừa hoàn thành:** Phase 1-3, CHƯA commit (nhánh `develop`).
- **Bước tiếp theo:** chạy SQL thêm quyền 1679 trên server rồi gán quyền cho vai trò ở màn Phân quyền.
- **Blocked:** không.
