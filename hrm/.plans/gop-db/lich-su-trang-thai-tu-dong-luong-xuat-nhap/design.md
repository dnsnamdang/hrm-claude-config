# Lịch sử khi trạng thái phiếu TỰ ĐỘNG chuyển trong luồng xuất–nhập — TÓM TẮT

> Nhánh `gop_db`. Người phụ trách: @dangquang.tom. Ngày: 2026-10-14.
> **Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-10-14-lich-su-trang-thai-tu-dong-luong-xuat-nhap-design.md`

## Mục tiêu
Mọi lần trạng thái phiếu trong luồng xuất–nhập (8 phiếu) **tự động chuyển** do được lập từ màn khác
(kể cả chéo luồng nhập↔xuất) đều phải **ghi lịch sử** với ghi chú nguồn. Bổ sung cả ghi lịch sử khi
user đổi status **thủ công** trên 2 màn YCNH & YCXBHM (nhóm C).

## Scope
- 8 phiếu: YCXH, ĐNXK, PXH, YCNH, ĐNNK, PNK, YCXBHM, PXBHM.
- Mọi điểm `status` tự động chuyển + chéo luồng + nhóm C thủ công.
- Ngoài scope: không đổi UI phiếu đã có lịch sử chạy đúng, không migrate YCNH, không backfill quá khứ.

## Các quyết định lớn (đã chốt với user)
1. Cơ chế **Hướng 1** — chèn log tường minh tại từng điểm (loại observer vì nhiều điểm `DB::table()->update()`).
2. Người thực hiện = người thao tác màn nguồn; fallback hệ thống. CÓ ghi chú nguồn vào field `note`.
3. Đổi trạng thái = dòng log RIÊNG `change_status`, nhãn "Thay đổi trạng thái" `#d97706` (skill §3a) — KHÔNG nhét `status` vào `catalogColumns()`.
4. **3 cơ chế lịch sử khác nhau theo phiếu:**
   - **Nhóm 1** (YCXH, ĐNXK, ĐNNK, PNK + PXH/PXBHM): `catalog_histories` đã có → chỉ chèn log tại điểm auto bằng wrapper sẵn có.
   - **Nhóm 2 — YCNH**: hệ lịch sử RIÊNG (`product_import_request_versions/_histories`) → ghi status-change vào chính hệ này + mở rộng `historyAction()`.
   - **Nhóm 3 — YCXBHM** (phương án A): dựng hạ tầng `catalog_histories` cho `borrow_sell_requests` + map nhãn status + repoint stub `histories()` + **thêm popup lịch sử màn danh sách** (có thêm FE).

## Hạ tầng bổ sung chính
- Whitelist `borrow_sell_requests` + trait `LogsCatalogHistory` vào `BorrowSellRequestService` + map `STATUS_TEXTS` trên entity.
- Nới `public` + thêm `$note` cho wrapper `logStatusChanged` của ĐNXK & PNK (ĐNNK đã có note, YCXH đã public+note).
- YCNH: thêm `logStatusChanged()` ghi version status + tách `historyAction()` (old==null→create, else→change_status).

## Rủi ro / điểm cần soi
- Hồi quy YCNH: mốc Tạo cũ phải giữ nhãn "Tạo mới" (điều kiện old==null).
- Mass-update: fetch status cũ TRƯỚC khi `DB::table()->update()`, log từng dòng, chỉ dòng thực đổi.
- Số dòng tham chiếu trong spec có thể trôi — pin lại khi implement.

## Trạng thái
- Brainstorming architectural: XONG. Spec đã viết + self-review. **Chờ user review spec** trước khi sang writing-plans.
- Chưa sửa code nào cho feature này.
