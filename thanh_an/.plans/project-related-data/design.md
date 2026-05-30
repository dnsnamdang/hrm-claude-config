# Tab "Dữ liệu liên quan" — Tóm tắt

## Mục tiêu
Hiển thị các chứng từ nghiệp vụ liên quan (Báo giá, Gói thầu, Hợp đồng) trên tab "Dữ liệu liên quan" trong màn chi tiết dự toán.

## Scope
- BE: 1 endpoint mới `GET /v1/category/projects/{project}/related-data`
- FE: Implement `RelationDataComponent.vue` + bỏ comment out ở `_id/index.vue`

## Quyết định lớn
- **Phương án 1 (chọn):** API riêng trên ProjectController — không ảnh hưởng API detail cũ
- Bảng 3 cột: Phân hệ nghiệp vụ | Chứng từ nghiệp vụ (mã, link) | Người thực hiện
- Hiển thị tích lũy: tất cả entity liên quan đều hiện (Kế hoạch + Thầu + Hợp đồng)
- Không hiển thị file đính kèm trong tab này

## Spec chi tiết
→ `docs/superpowers/specs/2026-05-25-project-related-data-design.md`

## Phụ trách
@khoipv
