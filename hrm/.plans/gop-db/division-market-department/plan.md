# Plan — Phiếu phân chia thị trường theo phòng ban (#11694)

> @junfoke · design: `design.md`

## Phase 1 — BE (hrm-api, Modules/Finance)

- [x] Migration thêm cột: `division_market_departments.division_part_id`; `..._provinces.max_employee`, `is_unlimited_employee`; `..._wards.business_area_id` (đã chạy 14/10)
- [x] Entities: DivisionMarketDepartment (+ Province, Ward, ProvinceVehicle)
- [x] Service: danh sách + phạm vi quyền, options, chi tiết (gom khu vực + nhóm "Chưa thuộc khu vực"), lưu (bung phường/xã + hãng), xoá, duyệt / huỷ duyệt, loại trừ cấp, cảnh báo trùng, SL NV ≤ số NV đơn vị, lịch sử
- [x] Quyền 1699–1702 trong PermissionsTableSeeder
- [x] In phiếu (print-data), xuất Excel danh sách (export-rows)
- [x] Routes `/v1/finance/division-market-departments`
- [x] Khu vực KD đang nằm trong phiếu → không cho xoá (sửa màn #11623)

## Phase 2 — FE (hrm-client, pages/finance/division-market-departments)

- [x] Menu sale-hub › Phiếu phân chia thị trường › Theo phòng ban
- [x] Danh sách (copy pattern `pages/customer-care/wr-service-contracts/index.vue`)
- [x] Form Tạo/Sửa/Chi tiết + bảng cây Tỉnh/TP → Khu vực + popup Thêm Tỉnh/TP / Thêm khu vực + popup phường/xã
- [x] Kiểm Playwright

## Phase 3 — Bàn giao

- [x] Migrate + seed quyền (user cho phép 14/10) + test API & UI toàn luồng

### Checkpoint — 2026-10-14
Vừa hoàn thành: BE + FE + test. API: tạo/sửa/xoá, loại trừ cấp, SL NV ≤ số NV đơn vị, hãng xe không tồn tại, duyệt/huỷ duyệt, 423 khi đã duyệt, lịch sử, in, xuất Excel, chặn xoá khu vực KD + hãng xe đang dùng. UI (Playwright): danh sách, tạo mới qua popup Thêm Tỉnh/TP, validate đỏ đồng thời, sửa, chi tiết phiếu cũ (gom "Chưa thuộc khu vực"), cảnh báo trùng, popup in.
Đang làm dở: không.
Bước tiếp theo: user duyệt → commit 2 repo (chưa commit). Dữ liệu test local: phiếu TPE_PCTT_00019 (Đang tạo), TPE_PCTT_00020 (Đã duyệt), khu vực KD test id 5, 6 (Hà Nội); 4 quyền 1699–1702 đã gán cho role 18 (Super admin) công ty 1.
Blocked:

### Checkpoint — 2026-10-15
Vừa hoàn thành: verify UI toàn luồng bằng dữ liệu tự tạo (user cho phép) — khu vực KD test 7, 8 (Đà Nẵng), 9 (Hà Nội); phiếu 21 (Đã duyệt, phòng QTTT), 22 (bộ phận Lắp đặt, 2 tỉnh, hiện Đã duyệt); đã xoá phiếu test 19. Đạt: lọc Tỉnh → Khu vực → Hãng xe, chi tiết 2 tỉnh + cảnh báo trùng, popup phường/xã (tìm không dấu), thu/mở tỉnh, lịch sử, + Thêm khu vực, xoá tỉnh có xác nhận, cảnh báo chưa lưu, Lưu và duyệt, URL Sửa phiếu đã duyệt → về Chi tiết, Hủy duyệt / Duyệt / Xóa ở danh sách + chi tiết, xuất Excel, câu chặn loại trừ cấp.
Sửa trong lúc verify: bảng chi tiết thêm viền dọc (table-bordered, user báo); ô Bộ phận hiện ngay từ dữ liệu chi tiết; nút footer chi tiết chỉ hiện khi đã tải xong; cột đếm xuất Excel giữ kiểu số; câu chặn loại trừ cấp ra 1 dòng rộng.
Đang làm dở: không.
Bước tiếp theo: user duyệt → commit nhánh task_11694 (2 repo).
Blocked:
