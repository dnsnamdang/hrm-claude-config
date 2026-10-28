# Phase 4 — Popup tìm kiếm hàng hoá dùng chung (ERP) — khảo sát 13/10/2026 (chỉ đọc)

> A7. ERP `wt-erp-2d1` @ `3aaae676fe`, DB `hrm_erp_giacty`. Nguồn gốc: `man-danh-muc-hang-hoa/design.md` §6 (bỏ enum cũ, 3 cờ nghiệp vụ §6c, §7).

## A. Popup + endpoint
| Partial | Endpoint | Số view include |
|---|---|---:|
| `partials/modals/searchProduct` (popup chính) | `searchProduct` | 99 (≈ 338 màn theo đếm cũ, gồm view con) |
| `searchProductQuotation` | `searchProductStockBuyer` | 27 |
| `searchProductEquivalent` | `searchProduct` | 4 |
| `searchProductForUpdate` | `searchProductStockBuyer` | 2 |
| `searchProductPromotions` | `searchProduct` | 1 |
| (không partial) `root_order_requests` | `searchProduct2` | 1 |

Bộ lọc popup chính: T/chất hàng hoá (enum `product_type`) · Thương hiệu · Xuất xứ · **Lĩnh vực › Chương › Nhóm công việc › Cụm công việc** (catalog CŨ qua `product_group_classifies` → `group_id`) · **Nhóm hàng hoá** (`groups`) · Hãng SX · Model · Tồn kho · Dùng cho nhóm máy (`groups`) / máy · Hãng/Loại/Model/Đời xe · **Loại hàng hoá** (`product_cate`) · Tên/mã. Cột KQ popup báo giá có "Tính chất" + "Loại hàng hoá".

## B. Dữ liệu thật (giacty)
- 45.890 hàng (28.371 đang KD ở ≥ 1 công ty): **100% còn `product_type` cũ**, **0** có `product_type_id` mới; cây phân loại mới **rỗng** (product_types 0, families 0, function_groups 0, characteristics 0, natures 1) — quy đổi hàng cũ sang cây mới chưa làm (§7.1, go-live B5/B6).
- `product_cate` lưu **mảng JSON** ở 45.685 hàng.
- Catalog: cũ `product_group_classifies` 1.019 dòng (`job_cluster_id` = 0 dòng); mới `product_business_catalogs` 21 dòng; chapters 66 (65 dưới `scopes` cũ, 1 dưới `internal_business_scopes` mới).

## C. Tình trạng từng ô lọc
| Ô lọc | Hàng cũ | Hàng tạo ở HRM (`product_type`/`product_cate`/`group_id` trống) |
|---|---|---|
| T/chất hàng hoá | chạy | **mất** khi chọn bất kỳ giá trị |
| **Loại hàng hoá — popup chính** | **HỎNG với MỌI hàng (0 dòng)** — `=`/`whereIn` so với mảng JSON (`SearchController:657-663`); popup báo giá dùng `whereJsonContains` nên chạy | hỏng |
| Nhóm hàng hoá / Dùng cho nhóm máy | chạy | vô nghĩa (màn Nhóm vừa gỡ ở Phase 5) |
| Lĩnh vực / Chương / Nhóm CV | chạy theo catalog cũ | **mất** (không đọc `product_business_catalogs`, Lĩnh vực lấy từ `scopes` cũ) |
| **Cụm công việc** | **HỎNG với MỌI hàng (0 dòng)** — `pgc.job_cluster_id` trống 100% | hỏng |
| Thương hiệu, Xuất xứ, Hãng, Model, xe, Tên/mã, Tồn kho | chạy | chạy |

## D. Lọc gài cứng theo enum cũ
- `is_service_quotation` (5 màn: báo giá DV sale/CSKH, YC thông tin BH-SC, lỗi thiết bị ×2) ⇒ chỉ `accessories`/`lubricant` ⇒ **loại mọi hàng HRM**.
- Báo giá DV / YC BH-SC truyền máy sửa (`product_id`) ⇒ phụ tùng theo enum + `productables` qua `group_id` ⇒ **loại hàng HRM**.
- `excludeServiceProducts` (ẩn "hàng hoá làm dịch vụ") — hàng HRM NULL vẫn hiện (2-D1 N9).
- Ngoài 4 endpoint (không thuộc Phase 4 trừ khi chốt khác): hàng của khách (`getListProductOfCustomer` — dùng danh sách trắng enum, §6c ngữ nghĩa 3), bảo hành theo HĐ/serial, nhập-xuất, giữ hàng, vị trí kho, select2 từ khoá.
