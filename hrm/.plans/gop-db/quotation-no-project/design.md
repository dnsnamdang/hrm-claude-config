# Báo giá không gắn Dự án TKT — design (tóm tắt)

> @namdangit · nhánh `gop_db` · bắt đầu 13/10/2026 · spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-13-quotation-no-project-design.md`

## Nguồn
- Tester sheet "Test báo giá" dòng 2 (13/10/2026): "báo giá độc lập không gắn với dự án TKT: Loại tiền mặc định VNĐ".
- Redmine #11651 (Chờ duyệt giá) nhắc "Trường hợp 2 (Báo giá độc lập - không tạo từ Dự án TKT)" nhưng không đặc tả luồng.
- #10501 (đã lên prod): "báo giá độc lập" = độc lập với BOM, VẪN thuộc dự án. Trước 13/10 code bắt buộc dự án ở mọi nhánh.
- User giao: "làm theo ý tưởng của bạn, lập hợp đồng đều phải có".

## Quyết định đã chốt (AI đề xuất, user giao toàn quyền 13/10/2026)
1. Dự án KHÔNG bắt buộc khi tạo báo giá tự lập. Không chọn ⇒ `project_id = NULL` (migration cho `quotations.project_id` + `hrm_contracts.project_id` nullable).
2. Không dự án ⇒ **Khách hàng bắt buộc**, chọn bằng popup dùng chung `ChooseErpCustomerModal`; BE snapshot `customer_*` từ bảng `customers` theo `customer_id` (không tin FE).
3. Không dự án ⇒ ẩn + bỏ bắt buộc "Giai đoạn dự án"; không Mỏ neo, không BOM.
4. Loại tiền mặc định VNĐ (tester dòng 2).
5. Quyền: có dự án giữ nguyên "Sale phụ trách dự án"; không dự án ⇒ ai vào được màn tạo đều tạo được; chốt / hủy chốt / sao chép / ghi chú KD ⇒ **người lập**.
6. Chốt Trúng thầu / Hủy chốt cho báo giá không dự án: nút ở màn chi tiết + danh sách báo giá (báo giá có dự án vẫn chốt ở tab Báo giá của dự án). Không áp luật "1 dự án 1 báo giá trúng thầu".
7. Lập hợp đồng: cả 2 loại đều lập được (Trúng thầu + chưa có HĐ + người lập).

## Ngoài phạm vi
- Trường Nhóm ngành (#11651) — chờ task được duyệt.
