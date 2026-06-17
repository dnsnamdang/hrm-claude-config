# Bắt buộc field khi gửi duyệt gói thầu lên TP — Tóm tắt

**Người phụ trách:** @khoipv
**Ngày:** 2026-06-08

## Mục tiêu
Bắt buộc nhập `bid_opening_time`, `bid_closing_time`, `execution_time`, `execution_time_unit` khi nhân viên bấm **"Gửi duyệt"** (status=3, `BidPackage::CHO_DUYET_KET_QUA`) lên trưởng phòng. Lưu nháp (1) / Lưu và gửi (2) vẫn để trống được.

## Quyết định lớn
- Trigger: chỉ `status == 3`.
- `execution_time`: `required|numeric|gt:0`.
- 2 field ngày: chỉ `required` (không thêm rule `date`).
- Validate có điều kiện bằng ternary inline trong `StoreBidPackageRequest`, dùng hằng số `BidPackage::CHO_DUYET_KET_QUA`.
- Chỉ sửa 1 file BE, không đụng controller/service/FE.

## Link
- Spec chi tiết: `docs/superpowers/specs/2026-06-08-bid-package-send-approve-required-fields-design.md`
- Plan: `.plans/bid-package-send-approve-required-fields/plan.md`
