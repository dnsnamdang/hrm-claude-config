# Redmine #11587 — Khoá/Mở khoá danh mục cha–con (quy tắc chung mục Danh mục 3–4)

Quy tắc: Khoá chỉ khi KHÔNG còn danh mục con trực tiếp Hoạt động · Mở khoá chỉ khi MỌI danh mục cha trực tiếp (nếu có) Hoạt động.
Chặn ở BE (endpoint lock/unlock + đường đổi status qua update) · FE ẨN nút theo cờ BE `is_can_lock`/`is_can_unlock`.
Phạm vi (chốt 07/10/2026): chỉ màn mới (V2Base). Bỏ: Decision khen thưởng, cơ cấu tổ chức, đào tạo (màn cũ). Con nhiều cha → mọi cha phải hoạt động.

## BE + FE
- [x] MasterData: activeChildrenCount cho Hãng xe (Loại xe), Loại xe (Model xe), Hãng sản xuất (Code đặt hàng)
- [x] MasterData: `is_can_unlock` ở BaseCatalogResource + FE ẩn nút Khoá/Mở khoá 24 màn master-data
- [x] Assign: Nhóm ngành ← Lĩnh vực Cty KD; Nhóm giải pháp ← Nhóm ngành; Lĩnh vực KD KH ← Loại hình
- [x] Assign: Ứng dụng → Câu hỏi khảo sát / Mẫu phiếu (khoá cha + mở con)
- [x] Human: Quốc gia → Khu vực → Tỉnh → Quận/Huyện, Phường/Xã → Đường/Phố; Ngân hàng → Chi nhánh
- [x] Finance: cây Tài khoản (identify_number_parent) + Loại TK → TK (mở khoá)

### Checkpoint — 07/10/2026
Vừa hoàn thành: BE chặn + FE ẩn nút cho MasterData, Assign (Nhóm ngành, Nhóm giải pháp, Lĩnh vực KD KH, Ứng dụng, Câu hỏi KS, Mẫu phiếu), Human (địa giới 6 cấp, Ngân hàng/Chi nhánh), Finance (cây Tài khoản). php -l sạch, tinker đọc khớp cờ.
Bước tiếp theo: user chốt 3 điểm (bỏ điều kiện dự án tiềm năng khi khoá Ứng dụng; chặn tạo mới/import Hoạt động dưới cha khoá; thêm index FK) → test Playwright.
Blocked:
