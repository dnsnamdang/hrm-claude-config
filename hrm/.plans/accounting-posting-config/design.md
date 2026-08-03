# Design (tóm tắt): Cấu hình hạch toán cho các phiếu

> Spec đầy đủ (UI/UX): `docs/superpowers/specs/2026-07-07-accounting-posting-config-design.md`

## Mục tiêu
Màn cho phép user (kế toán) **tự cấu hình bút toán hạch toán** cho từng loại phiếu **không cần sửa code** — thay logic hardcode hiện tại. Phân hệ Kế toán HRM (`Modules/Accounting`, hiện scaffold rỗng).

## Phạm vi lần này
CHỈ **UI/UX màn hình**. Chưa chốt DB schema / API / đồng bộ / engine sinh bút toán.

## Quyết định chính
- 2 nguồn phiếu: **ERP** (đang hardcode) + **HRM** (tương lai).
- Tài khoản: **đồng bộ từ ERP** (`erp2326.accounts`).
- Bố cục: **Master-detail** — danh sách loại phiếu (trái, nhóm ERP/HRM) + bảng bút toán (phải).
- Dòng bút toán: Diễn giải · TK Nợ · TK Có · Nguồn số tiền · **Điều kiện** (dòng phụ) · **Hệ số/Dấu**.
- Kéo-thả sắp thứ tự sinh bút toán; nút **"Xem thử bút toán"**; validation inline theo convention HRM.
- Vị trí FE: `pages/accounting/posting-config.vue` (`layout: 'accounting'`) + mục sidebar kế toán.

## Ngoài phạm vi (spec sau)
Schema DB, API, đồng bộ TK + loại phiếu từ ERP, engine áp cấu hình sinh bút toán, phân quyền chi tiết.

## Lưu ý branch
`Modules/Accounting` do @manhcuong scaffold ở branch khác, **chưa merge** vào `tpe-develop-assign`. Cần chốt branch trước khi code.
