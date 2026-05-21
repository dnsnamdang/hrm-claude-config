# Danh sách phụ lục chờ duyệt — Design Summary

**Ngày**: 2026-05-21
**Người phụ trách**: @khoipv
**Spec chi tiết**: `docs/superpowers/specs/2026-05-21-contract-annex-approve-list-design.md`

## Mục tiêu

Tạo màn danh sách gộp tất cả 6 loại phụ lục hợp đồng chờ duyệt vào 1 trang thống nhất.

## Scope

- 1 API gộp mới ở BE: `GET /v1/category/contract_annex/list-approve`
- 1 trang FE mới: `pages/contract/contract_annex/approve.vue`
- Menu item đã có sẵn trong `MenuContract.js`
- Navigate đến trang detail có sẵn của từng loại phụ lục
- Không phân quyền theo cấp, dùng permission `'Duyệt hợp đồng'` có sẵn

## Quyết định lớn

1. **API gộp ở BE** thay vì FE gọi 6 API — vì tất cả phụ lục cùng bảng `contract_annexes`
2. **Cột đầy đủ** + thêm cột "Loại phụ lục" để phân biệt
3. **Filter cơ bản** + filter loại phụ lục
4. **Xóa** gọi API riêng theo loại phụ lục (DELETE endpoint đã có sẵn)
