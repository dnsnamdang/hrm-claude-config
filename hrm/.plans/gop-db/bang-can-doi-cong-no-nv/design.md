# Bảng cân đối phát sinh công nợ nhân viên — Tóm tắt

**Người phụ trách:** @junfoke — 2026-11-03
**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-11-03-bang-can-doi-cong-no-nhan-vien-design.md` · **Plan:** `plan.md`

## Mục tiêu

Số dư công nợ từng nhân viên × loại tiền trên 1 tài khoản theo dõi công nợ (dư đầu kỳ, phát sinh, dư cuối kỳ Nợ/Có), bấm mã NV
sang Sổ chi tiết công nợ nhân viên. Màn 3/4 nhóm Kế toán Công nợ › Nhân viên.

## Quyết định chính (user chốt 03/11/2026)

1. Phạm vi công ty thống nhất với Sổ chi tiết: NV công ty mình + sổ của chính mình (ERP màn này: + HĐ mình tạo).
2. Tính đầu kỳ cho mọi loại tiền (ERP bỏ trống dòng ngoại tệ ⇒ đầu + PS ≠ cuối).
3. Thêm In + Xuất Excel (ERP không có).
4. 403 mọi endpoint khi không quyền; drill-down truyền thêm loại tiền của dòng.
