# Diễn tập 06/11/2026 — dump prod lúc đã down (`db_gop_6_11`)

- Dump 19:02 trên VPS, 1,1 GB, SHA256 khớp sau khi tải, có `Dump completed`. Nhập local 613 giây: 1.936 bảng, 1.999 quyền, 140 vai trò.
- Code: nhánh `rbac-golive-0611` (hrm-api `7b71f6462`, client `43eea2a78`, ERP `1998e321a1`), worktree `wt-rbac-dien-tap`.
- Migration: 10 bản, 7 giây. Không còn bản chờ. Prod đã chạy hết migration của origin.
- Convert: dry-run exit 0, 16 s, `chenh-lech-khac` 0. Chạy thật exit 0, 16 s.
- B.4b: thiếu company_employees 0 · mồ côi 12 dòng (12 tài khoản đã xoá) đã xoá · mất quyền quản lý tài khoản 0.
- Khối 5: catalog-sync 0 thay đổi · roles không công ty 0 · rbac_role_map 283 · aliases 1.898 · 938 mã · 282 vai trò.
- 5b: 18 Vai trò · thêm 85. Verify lệch 441, cả 441 là cũ 0 → mới 1 của 12 NV giữ Super Admin (user đã chấp nhận).
- Tắt 6 công ty qua API màn: 2,3,4,7,8,9 đều 200. 2.558 dòng / 87 vai trò bị hạ. Verify sau tắt: 339 Super Admin + 6 dòng mức 4 đúng design 4.4. TPA, UPS vẫn bật (ngừng hoạt động, không thuộc danh sách chốt).
- Test `tests/Feature/Rbac` hrm-api: 448 ca, 3 đỏ, không phải lỗi quyền lúc chạy (2 ca route còn ghi tên cũ, CheckPermission vẫn nhận; 1 ca DB test thiếu inherited_price_factors). Bộ Rbac ERP chưa chạy.
- Smoke ERP: HĐ `type=all` tab Hợp đồng (`contract_type=1`): NV 13 17.695 = DB; NV 1027 TPE 12.440 = DB; TPHP 0, NV 663 0. Yêu cầu chuyển hàng: NV 13 3.979, 1027 TPE 413, NV 663 0. Số 27.998/16.321 hôm 04/11 là tổng mọi loại HĐ, không so được.
- Smoke HRM (client build từ nhánh phát hành): NV 13 vào Vai trò / Vai trò NV / Phạm vi TCT (9 công ty) / khách hàng / Cấu hình lịch công tác. NV 1027 và 663 bị 404 ở 4 màn quản trị. NV 663 khách hàng: "Không có dữ liệu". 0 lỗi API.
- Lịch công tác: mới kiểm mở màn cấu hình; chưa kiểm luồng báo lịch.
