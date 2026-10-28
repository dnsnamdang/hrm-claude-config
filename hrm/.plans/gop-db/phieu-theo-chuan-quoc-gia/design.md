# Đưa 17 màn chứng từ "DNS đang fix" về chuẩn giao diện màn Danh mục quốc gia

**Người phụ trách:** @junfoke — 2026-10-28
**Nhánh:** `develop` (worktree `.worktrees/gop-db` của cả hrm-client và hrm-api)
**Spec chi tiết (kết quả rà từng màn, file:dòng):** `docs/superpowers/specs/gop-db/2026-10-28-phieu-theo-chuan-quoc-gia-design.md`

## Mục tiêu

Trong bảng theo dõi của khách, 17 màn chứng từ đang ở trạng thái "DNS đang fix". Cần sửa giao diện để
khớp màn **Danh mục quốc gia** (`pages/human/nations/index.vue`), màn đã được khách đánh PASS.

## Phạm vi (17 màn)

- **Tài chính – tiền:** Đề nghị thu tiền, Đề nghị thanh toán, Phiếu thu, Phiếu chi, Phiếu báo có,
  Phiếu ủy nhiệm chi.
- **Giữ hàng:** Yêu cầu xuất giữ, Phiếu xuất giữ, Yêu cầu gia hạn hàng giữ, Yêu cầu hủy hàng giữ,
  Phiếu hủy hàng giữ, Phiếu yêu cầu điều chuyển hàng giữ.
- **Kho + CSKH:** Phiếu yêu cầu chuyển hàng, Phiếu chuyển hàng nhập thẳng, Phiếu yêu cầu gia hạn
  hàng mượn, Phiếu yêu cầu kiểm tra sửa chữa – bảo hành, Phiếu xử lý yêu cầu.

## Quyết định user chốt (28/10/2026)

1. **Mọi màn chứng từ phải có Xuất Excel cả danh sách**, qua popup chọn trường. Comment và spec cũ
   ghi "không xuất cả danh sách" đã hết hiệu lực.
2. **Nút "In danh sách":** đứng ngay sau Tạo mới, trước Xuất Excel (user đổi lại 28/10/2026).
3. **Cột Người tạo / Người cập nhật** hiển thị "Tên NV - Mã phòng", dựng bằng helper
   `employeeAuditLabel()`.
4. **Thứ tự thanh nút** theo màn Quốc gia: Tạo mới → In → Xuất Excel → Import → Tuỳ chỉnh cột.

Đã cập nhật skill `list-page` (mục 1, mục 6) và `erp-to-hrm-screen` cho khớp 4 quyết định trên.

## Không làm

- Khối chữ ký "Người lập (Ký, họ tên)" ở cuối file Excel từng phiếu: giữ nguyên vì phải giống ERP
  (#11195, #11248).
- Màu chữ ô `field-line` trần: màn Quốc gia cũng đang để như vậy.
