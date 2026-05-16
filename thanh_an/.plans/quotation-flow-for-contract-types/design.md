# Quotation Flow cho loại Cho/Tặng, Đặt/Mượn, Nguyên tắc

> **Spec chi tiết:** `docs/superpowers/specs/2026-04-24-quotation-flow-for-contract-types-design.md`
> **Người phụ trách:** @khoipv

## Mục tiêu

Sửa flow dự toán loại 4/5/6 để đi qua bước phân công báo giá + báo giá trước khi sang hợp đồng, thay vì gửi thẳng sang hợp đồng.

### Flow mới

```
Dự toán duyệt → Phân công báo giá → Lập báo giá → TP duyệt → BGĐ duyệt (luôn) → Chuyển thẳng hợp đồng
```

## Scope

### Backend
- `ProjectService`: Gộp type 4/5/6 vào nhánh phân công báo giá (giống type 1/2). Xóa `approveTransferContract()`.
- `QuotationService`: Type 4/5/6 luôn qua BGĐ duyệt (không check giá). Render → chuyển thẳng HĐ.
- `ContractService`: Type 3/4/5 validate `quotation_id` thay vì `project_id`.
- API mới: `GET quotations/approved-for-contract?project_type={type}`

### Frontend Báo giá
- Ẩn tab "Thư mời báo giá", "Ủy quyền", TotalComponent khi project_type = 4/5/6
- Ẩn cột bảng hàng hóa theo loại (giống bên hợp đồng)

### Frontend Hợp đồng
- Type 3/4/5 chọn **báo giá** thay vì dự toán, filter theo loại tương ứng

## Quyết định lớn

1. Approach A — tái sử dụng flow type 1/2, thêm điều kiện
2. Xóa hoàn toàn bước BGĐ duyệt chuyển HĐ trên dự toán
3. Hợp đồng link tới `quotation_id`, logic form giữ nguyên
4. Báo giá type 4/5/6 luôn qua BGĐ duyệt, không check giá min/max
