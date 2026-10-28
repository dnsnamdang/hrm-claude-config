# HĐ đã kết xuất — cảnh báo HĐ phát sinh phụ lục sau khi kết xuất

@khoipv — Bắt đầu 15/10/2026

Spec chi tiết: [docs/superpowers/specs/2026-10-15-hd-ket-xuat-canh-bao-phu-luc-design.md](../../docs/superpowers/specs/2026-10-15-hd-ket-xuat-canh-bao-phu-luc-design.md)

## Mục tiêu
Màn Cung ứng › HĐ đã kết xuất cho biết HĐ nào đã phát sinh phụ lục (7 loại) **sau khi kết xuất**.

## Quyết định lớn
- Chỉ thể hiện trên danh sách — không theo dõi đã xem, không thông báo chuông.
- Chỉ tính PL **đã duyệt** (status 3) có `approved_time > contracts.supply_rendered_at`.
- KHÔNG thêm cột riêng (user đổi ý 15/10/2026): icon cam cạnh Mã HĐ, bấm mở popup danh sách PL (không tooltip).
- Bộ lọc `has_annex` (Có/Không); Excel có trường "Phụ lục phát sinh" (không tick sẵn).
- BE: subquery GROUP_CONCAT trong `RenderedContractService::getList()`, Resource tách mảng `annexes_after_render`.
- Thứ tự mặc định (16/10/2026): HĐ có PL phát sinh nổi lên đầu theo ngày duyệt PL gần nhất, HĐ kết xuất sau đó nằm trên.
- Lập đề xuất từ HĐ chỉ khi HĐ còn hiệu lực (ngày KT đã gồm PL gia hạn đã duyệt) — 16/10/2026.
- Excel không có trường "Phụ lục phát sinh" (user bỏ 16/10/2026).
- Phiếu đề xuất: CHẶN SL vượt "SL còn được đề xuất" của HĐ (HĐ + PL − đã xuất − phiếu sống khác), cả nháp lẫn gửi;
  FE bôi đỏ + chặn nút, BE kiểm ở store/update/send (16/10/2026).
- `ContractAnnexQuantityController::approve()` trả response + lỗi giữa chừng rollback, trả 400 (16/10/2026).
- Không migration. Code phụ lục bên Category chỉ sửa 2 bug được user đồng ý (ngày KT cũ PL gia hạn, approve PL SL).
