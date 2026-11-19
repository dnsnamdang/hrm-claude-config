# Sổ chi tiết công nợ nhân viên — Tóm tắt

**Người phụ trách:** @junfoke — 2026-11-02
**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-11-02-so-chi-tiet-cong-no-nhan-vien-design.md` · **Plan:** `plan.md`

## Mục tiêu

Kế toán xem sổ chi tiết từng bút toán của 1 tài khoản theo dõi công nợ gắn nhân viên trong khoảng ngày (đầu kỳ, phát sinh,
cuối kỳ), in và xuất Excel trên HRM — không sang ERP. Màn 2/4 nhóm Kế toán Công nợ › Nhân viên.

## Quyết định chính (user chốt 02/11/2026)

1. Chặn y ERP: không có quyền tổng công ty / công ty thì không vào màn; chặn cả API tìm / xuất / in (ERP lộ dữ liệu).
2. Chỉ lấy bút toán có nhân viên cho cả dòng lẫn đầu kỳ (ERP lệch số cuối kỳ).
3. Cột Tỷ giá hiện tỷ giá thật (ERP luôn trống).
4. In dùng chung truy vấn màn, HRM tự dựng mẫu (mẫu ERP 237 trên DB gộp rỗng), trần 2.000 dòng.
5. Excel dựng ở FE, tải ngay (ERP ≥ 3.000 dòng gửi email).
