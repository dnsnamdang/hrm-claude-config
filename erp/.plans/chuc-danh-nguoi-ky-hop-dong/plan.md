# #11932 — Người ký / người duyệt hợp đồng: "Chức vụ" → "Chức danh" theo HRM

Redmine: http://quanly.dnsmedia.vn/issues/11932 · @junfoke · Repo ERP `TanPhatDev` + `hrm-api` / `hrm-client`

Yêu cầu: khối "Ký hợp đồng" ở màn Tạo / Sửa / Xem HĐ bán, HĐ mua (các màn bị gạch trong menu) đổi nhãn "Chức vụ" → "Chức danh", danh sách lấy theo chức danh HRM của người ký (`titles` qua `employee_infos.employee_role_id`); 1 chức danh thì tự điền, nhiều thì cho chọn; đổi người ký thì nạp lại.

## Ngày 30/10/2026 (@junfoke)
- [x] 30/10/2026 — Khảo sát task + đối chiếu menu bị gạch → form ERP (HĐ bán, phụ lục bổ sung/giảm, HĐ sửa chữa - bảo dưỡng - bảo trì, Mua trong nước theo hãng / tự do, Mua ngoài…).
- [x] 30/10/2026 — ERP: helper `App\Helpers\SignerTitleHelper` + partial `resources/views/partials/signer_title/{select,readonly,js}.blade.php`; lưu snapshot `{signer|approver}_title_id` + `_title_name`; validate `*_title_id` bắt buộc, `role` thành nullable; HĐ cũ giữ role cũ. Làm cho HĐ bán + phụ lục, HĐ SC-BH + 2 loại phụ lục (cho chọn người ký riêng), Mua trong nước / Đơn hàng nguyên tắc / Phụ lục, Mua ngoài (người duyệt).
- [x] 30/10/2026 — Theo user: bỏ giữ tương thích controller CRM cũ (đã ngừng dùng) → mọi màn trong phạm vi bắt buộc chức danh; màn nha khoa (`zt.*`, không gạch) giữ chức vụ (tách theo route). Bản in Mua trong nước in chức danh người duyệt.
- [x] 30/10/2026 — Migration `2026_10_30_000001_add_signer_title_to_contract_tables` (14 cột ở 7 bảng) + `2026_10_30_000002_backfill_signer_title_on_contract_tables` (cột người duyệt Mua trong nước + `rule_inland_buy_contracts`, điền chức danh HĐ cũ theo chức danh hiện tại). User chạy SQL prod: 0 HĐ bị trống chức danh; sau migrate `firm_contracts` 27.923 HĐ có người ký, 0 trống; đủ 18 cột.
- [x] 30/10/2026 — Rà lại trước khi đẩy prod: sót **HĐ nguyên tắc mua** (người duyệt có hiện chức vụ ở màn xem + bản in) → sửa giống Mua trong nước.
- [x] 30/10/2026 — HRM (theo user, sửa luôn các màn đã chuyển sang HRM, nhánh `develop`): HĐ Sửa chữa - bảo hành (`wr-service-contracts`) + HĐ bán (`assign/contracts`) — `App\Helper\SignerTitleHelper`, `utils/signer-title.js`, API `human/titles/by-employee/{id}`. Ghi rule vào `hrm/CLAUDE.md`, `erp/CLAUDE.md`, skill `erp-to-hrm-screen` (bẫy khi port: không bê ô "Chức vụ" của ERP).
- [x] 30/10/2026 — Đẩy: ERP `task_11932` (`b6ef45dc3a`, tách từ `gop_db`) → merge `develop_02` (`fea5e243a8`, gộp tay conflict `InlandBuyContractNewController.php` giữ cả thông báo %VAT lẫn chức danh); hrm-api `d8bce2a3c`, hrm-client `9395a6bbc` lên `develop`.
- [ ] QA test trên dev các bước tạo / sửa / duyệt / in (chưa màn nào bấm Lưu thật trên giao diện).
