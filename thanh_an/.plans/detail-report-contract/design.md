# Báo cáo chi tiết hợp đồng — Design Summary

> Người phụ trách: @khoipv | Ngày: 2026-05-06

## Mục tiêu

Tạo màn báo cáo chi tiết hợp đồng — hiển thị danh sách sản phẩm từ nhiều hợp đồng (1 dòng = 1 sản phẩm). Clone pattern từ báo cáo chi tiết thầu.

## Scope

- API `GET /v1/category/contracts/detail-report` — query `contract_products` JOIN `contracts`
- FE `pages/contract/detail-report/index.vue` — 27 cột, 8 bộ lọc, pagination, export Excel
- Phân quyền 3 cấp: tổng công ty / công ty / nhóm nghiệp vụ
- Chỉ lấy record_type = 2 (hợp đồng, bỏ biên bản thương thảo)

## Quyết định lớn

- Export Excel client-side (ExcelJS) — giống báo cáo chi tiết thầu
- 8 bộ lọc (không lọc theo khoảng ngày ký)
- 4 trạng thái, 5 loại hợp đồng

## Spec chi tiết

→ `docs/superpowers/specs/2026-05-06-detail-report-contract-design.md`
