# YCLĐBG — Cần khảo sát mặt bằng (#11723)

**Người phụ trách:** @junfoke — 2026-10-27
**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-10-27-ycldbg-khao-sat-mat-bang-design.md`

## Mục tiêu
Màn **Yêu cầu lắp đặt, bàn giao** (ERP `customercare/assembly_requests`) thêm trường **Cần khảo sát mặt bằng**:
bắt buộc chọn Có/Không; chọn **Có** thì bắt buộc có **File đính kèm** (trường file đã có từ 08/10/2026).

## Scope
- Làm ngay trên ERP `TanPhatDev` nhánh `gop_db`: form Tạo / Sửa / Xem chi tiết.
- Danh sách, in, Excel: không đổi (BA không yêu cầu).
- HRM: chưa có màn này → ghi sẵn checklist port ở spec mục 6.

## Quyết định chính
- Cột mới `assembly_requests.need_site_survey` TINYINT NULL (1 Có / 0 Không / NULL phiếu cũ), migration ở ERP; HRM dùng chung DB gộp nên không migrate lại.
- Phiếu cũ không backfill; sửa phiếu cũ thì buộc chọn lại.
- Rule file tính **số file còn lại sau khi lưu** (file cũ − file xoá + file mới) → sửa phiếu đã có file không bắt chọn lại.
- Đổi Có → Không không xoá file đã đính kèm.
- Không sửa partial upload dùng chung (dòng lỗi thiếu nháy); thêm dòng lỗi riêng trong form màn.
