# Design (tóm tắt) — Dự án cha → Dự án con (dự án TKT, Modules/Assign)

**Spec đầy đủ:** `docs/superpowers/specs/2026-07-20-du-an-cha-con-design.md`
**Trạng thái:** Design đã duyệt (2026-07-20), chờ plan chi tiết.

## Mục tiêu

Bổ sung quản lý dự án TKT (`prospective_projects`) theo cấp Dự án cha → Dự án con, từ bước dự án tới bước phê duyệt báo giá.

## Quyết định lớn

1. **Con tự chủ hoàn toàn** — con có BOM/báo giá/luồng duyệt riêng; cha là đầu mối roll-up theo dõi
2. **2 tầng** — con không làm cha, dự án có con không làm con
3. **Tạo con 2 đường**: nút "Tạo dự án con" ở chi tiết cha (prefill KH khóa + NVKD + phân loại) + picker RelatedSection; con **cùng khách hàng** với cha
4. **Cấp duyệt báo giá giữ nguyên** theo từng báo giá — KHÔNG sửa QuotationService/BomPriceApprovalConfig
5. **Chặn đóng cha** khi còn con chưa Đóng(11)/Kết thúc(12)
6. **Danh sách phẳng** + cột/filter "Dự án cha"; chi tiết cha thêm **tab "Dự án con"** (bảng con + tổng giá trị báo giá đã duyệt)

## Phương án kỹ thuật (A)

Tận dụng `parent_id` đã có sẵn (DB + fillable + picker FE `RelatedSection.vue`). Roll-up tính on-the-fly. Việc phải làm:
- **DB**: 1 migration index `parent_id`
- **BE**: validation parent_id (6 rule nghiệp vụ trong `ProspectiveProjectRequest::withValidator`), chặn `close()` khi con mở, API `GET {id}/children` (roll-up giá bán đã duyệt, không lộ giá vốn), `getAll?parent_candidates=1`, resource thêm `parent` + `children_count` + `parent_code/name`, filter `parent_id` ở index
- **FE**: siết + dọn `RelatedSection.vue`; tab "Dự án con" + nút "Tạo dự án con" ở `_id/index.vue`; prefill `add.vue?parent_id=`; cột + filter "Dự án cha" ở `index.vue`
- **Không permission mới**; tab con dùng quyền xem chi tiết cha

## Ngoài scope

Báo cáo tổng hợp TKT theo cụm cha-con; lũy kế cụm ở màn duyệt báo giá; cascade Task/Solution/Meeting.
