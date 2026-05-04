# Gộp hồ sơ trình duyệt hạng mục vào tab Hồ sơ giải pháp

**Người phụ trách:** @manhcuong
**Ngày tạo:** 2026-04-25
**Spec chi tiết:** `docs/superpowers/specs/2026-04-25-merge-module-review-profiles-design.md`

---

## Mục tiêu

Gộp hồ sơ trình duyệt của các hạng mục thuộc giải pháp vào tab "Hồ sơ" trên trang quản lý giải pháp (`/assign/solutions/{id}/manager`), để PM duyệt tất cả tại một nơi thay vì phải vào từng trang manager hạng mục.

## Scope

- Mở rộng API `GET .../review-profiles` — thêm param `type`, `solution_module_id`, `module_version_id`; merge 2 bảng `solution_review_profiles` + `solution_module_review_profiles` → sort → paginate thủ công
- Mở rộng `ReviewProfilesTab.vue` — thêm 3 filter (Loại, Hạng mục, Version HM) + 2 cột (Loại, Hạng mục)
- Tạo `ModuleApprovalViewModal.vue` — modal readonly + duyệt/từ chối hồ sơ hạng mục
- Gọi trực tiếp API decision hiện có của hạng mục, không tạo endpoint mới

## Quyết định lớn

1. **Một bảng duy nhất** gộp cả 2 loại hồ sơ, thêm cột "Loại" phân biệt — thay vì 2 bảng tách biệt
2. **Backend merge + paginate** — query 2 bảng riêng rồi merge/sort/paginate trong PHP, vì 2 bảng schema khác nhau không dùng union được
3. **Chỉ xem + duyệt** hồ sơ hạng mục từ trang giải pháp, không cho tạo/sửa
4. **PM duyệt, trưởng phòng chỉ xem** hồ sơ hạng mục tại đây
5. **Gọi API decision hiện có** của hạng mục, không proxy qua giải pháp
