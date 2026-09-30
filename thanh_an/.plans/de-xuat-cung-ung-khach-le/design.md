# Design (tóm tắt) — Loại đề xuất "Cung ứng khách lẻ"

> @khoipv · 16/09/2026 · **Spec đầy đủ:** [`docs/superpowers/specs/2026-09-16-de-xuat-cung-ung-khach-le-design.md`](../../docs/superpowers/specs/2026-09-16-de-xuat-cung-ung-khach-le-design.md)

## Mục tiêu

Bổ sung loại đề xuất thứ 3 — **Cung ứng khách lẻ** (`type = 3`) — vào màn Lập phiếu đề xuất cung ứng: bán cho khách hàng nhưng **không bám hợp đồng bán**, chọn hàng từ toàn bộ danh mục, và cho người lập nhìn thấy **giá dealer / giá vốn** để đàm phán.

Nguồn nghiệp vụ: Google Sheet `1BlXjHgNgMq7bwJgftEp9_xDybLs7G-Fv11y33w9acl4` tab `gid=841722699`, khối "Cung ứng KH lẻ" từ dòng 79.

## Phạm vi

**Trong:** enum loại (BE+FE), màn lập/sửa/xem phiếu, danh sách + lọc, luồng duyệt BGĐ, đổi tên permission duyệt, 2 cột giá mới ở tab Thông tin hàng hóa.

**Ngoài (đợt sau):** phiếu xử lý cung ứng, đơn mua hàng, báo cáo nhu cầu mua.

## Quyết định lớn

| Vấn đề | Chốt |
|---|---|
| Luồng duyệt | Phải **BGĐ duyệt** trước (gửi → status 2), giống nội bộ |
| Quyền duyệt | **Đổi tên** permission id 516 `Duyệt đề xuất cung ứng nội bộ` → `Duyệt đề xuất cung ứng`, dùng chung type 2 + 3 |
| Form | Khách hàng **bắt buộc**; không có Mục đích / KH sử dụng / Hợp đồng bán; ẩn tab "Tham chiếu hợp đồng bán" |
| Chọn hàng | Toàn bộ danh mục (`catalogItems()`), cột Số liệu nguồn chỉ *SL tồn kho* + *SL đang mua*, **không cảnh báo** vượt tồn |
| 2 cột giá mới | Chỉ hiện với type 3. Hàng **NK** → PriceType `GDS` / `GD`. Hàng **PPL** → cột "có service" = `-`, cột "không service / Giá vốn" = **MAX giá** từ **cả** `purchase_order_products` **và** `purchase_contract_products`, chỉ đơn/HĐ **đã duyệt** (status 3), lấy **đúng số đã lưu** (đã gồm VAT) |
| ĐVT tra giá | Theo ĐVT của dòng đề xuất; thiếu hệ số (`product_package_informations` xóa mềm) → loại bản ghi khỏi MAX, không đoán hệ số 1 |
| Hàm dùng chung | **Không sửa** `SupplyHandlingService::productInfoMap()` — viết `SupplyProposalService::retailPriceMap()` riêng, merge ở controller khi `type = 3` |
| Export Excel | Không thêm 2 cột giá (export thuộc tab "Hàng hóa đề xuất") |

## Hạn chế đã biết

Phiếu type 3 sau khi duyệt sẽ vào inbox xử lý, nhưng màn Phiếu xử lý cung ứng chưa có `TYPE_KHACH_LE` → tab thao tác rỗng. Xử lý ở đợt sau.
