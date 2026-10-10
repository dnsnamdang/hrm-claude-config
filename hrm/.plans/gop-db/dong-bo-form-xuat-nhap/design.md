# Đồng bộ form luồng xuất nhập — tóm tắt

- Người phụ trách: @namdangit
- Nhánh: `gop_db`
- Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-10-dong-bo-form-xuat-nhap-design.md`

## Mục tiêu

Màn Tạo / Sửa / Chi tiết của 8 luồng xuất nhập (YCXH, ĐNXK, PXH, YCNH, ĐNNK, PNK, PXBHM, YCXBHM) thể hiện thông
tin cùng dạng với chi tiết Phiếu xuất giữ (PXG-02188): khối tiêu đề in hoa nền xám nhạt, không icon, lưới 3 cột
nhãn-trên-ô-dưới, người lập ở góc phải khối "Thông tin chung". CSS dùng chung qua 1 component.

## Quyết định đã chốt (10/10/2026)

1. **Component mới `components/V2BaseFormCard.vue`** đóng gói CSS `.form-card` của PXG; props `title`,
   `no-body-padding`; slots `#title`, `#meta`, default; không prop icon; CSS unscoped trong component.
   10 màn `.form-card` cũ giữ nguyên.
2. **Lệch CLAUDE.md** ("khối nhóm dùng `V2BaseFormSection`"): user chọn khuôn PXG cho nhóm xuất nhập; soạn đề xuất
   PR sửa CLAUDE.md + skill `erp-to-hrm-screen` L455, không tự sửa.
3. **Chi tiết = phương án A**: giữ page `_id/index.vue` riêng, chỉ đổi giao diện. Gộp thành Form readonly để sau.
4. **Khách hàng = phương án A**: gộp vào lưới Thông tin chung, bỏ subpanel.
5. **Thông tin chung**: `CreatorInfoLine` ở `#meta`; bỏ ô Người lập/Ngày lập; ô `col-md-4` + `V2BaseLabel` +
   `V2BaseInput disabled size="sm"`; trạng thái `V2BaseBadge` trong lưới (không ở header); mã liên kết
   `.v2-linked-field`; trường dài `col-12`; Ghi chú `V2BaseTextarea rows=2`; trường không áp dụng → ẩn,
   áp dụng mà rỗng → ô xám rỗng; bỏ "—".
6. **Bảng**: mỗi bảng một `V2BaseFormCard`, ruột bảng giữ nguyên.
7. **File đính kèm**: `bill-payment-requests/components/AttachmentSection.vue` (không `V2BaseAttachmentSection`),
   chỉ ở màn đang có.
8. **Icon**: bỏ `ri-*` trước tiêu đề khối/sub-panel; icon trên nút giữ.
9. `SystemInfoSection`, `V2Footer` giữ nguyên.
10. Sửa tiêu đề sai `BorrowSellForm.vue:7`.
11. **Đợt**: 0 component → 1 PXBHM (thí điểm, DỪNG gửi ảnh) → 2-8 làm liền sau khi duyệt.
12. **Không đụng**: `index.vue` danh sách, `print.vue`, modal, 10 màn `.form-card` cũ. BE chỉ thêm tên người lập
    thuần nếu thiếu.
13. **Kiểm**: Playwright đo so PXG-02188 + ảnh, grep sạch icon/`kv-grid`/`c-section`, 768px không cuộn ngang,
    hồi quy lưu nháp rồi xoá bản ghi thử.
