# Fix: Phân bổ hàng điều chuyển chi nhánh giữ nhầm công ty

## Bug
`TransferProductAllocation::approve()` khi giữ hàng điều chuyển kho **chi nhánh** (xuyên công ty) lookup/tạo `PrepickDetail` **thiếu `company_id`** → cộng suất giữ vào **công ty nguồn** thay vì **công ty đích** (nơi hàng vật lý đã chuyển tới).

## Bằng chứng (production erp_new)
- Điều chuyển sp 37467: Liên Ninh (cty 1) → Sài Gòn (cty 4). Phiếu nhập PNH-12630 (type 7) cộng +10 tồn KT vào SG01 (cty 4) ngày 2026-08-05.
- Nhưng `approve()` cộng +10 vào prepick 52356 (company_id=1, cust 15991, NV265) — suất giữ cũ của Liên Ninh.
- Hệ quả: cty1 giữ 61 > tồn 55 (chặn xuất tại Liên Ninh); cty4 có hàng nhưng thiếu suất giữ cho KH 15991.

## Tasks
- [x] BE: `app/Model/Warehouse/TransferProductAllocation.php::approve()` — thêm `$company_id = $this->product_import->company_id` vào lookup PrepickDetail + set khi tạo mới
- [x] Data fix production: chuyển prepick 52356 company_id 1 → 4 (backup: `backup_prepick_52356_20260806_114650.csv`). Kết quả: cty1 61→51 (≤55, Liên Ninh hết chặn), KH15991 được giữ 10 tại cty4 (SG01)
- [x] Rà soát toàn production: tìm mọi prepick do transfer-allocation nhưng company_id ≠ cty đích. Kết quả: 4 bản lệch / 3 phiếu, 2 còn hiệu lực (đều PPBHĐC-01327, sp11309), 2 hết hạn qty=0
- [x] Fix 2 bản còn hiệu lực (backup `backup_prepick_52352_52354_20260806_134952.csv`):
  - 52352 (11309/KH42634): company_id 1→4 (nguồn đã hủy sẵn, chuyển 1 sang cty4)
  - 52354 (11309/KH15991): giảm qty 10→5 (hủy 5 suất giữ nguồn) + company_id 1→4
- [x] Audit lại: 0 bản lệch còn hiệu lực. Đối chiếu: cty4 sp11309 giữ 10 = tồn 10; cty1 sp11309 giữ 27 ≤ tồn 62

## Nguyên tắc "hủy suất giữ nguồn" (đã kiểm chứng)
Các cặp làm ĐÚNG trong cùng lô (6595/15991, 6595/36847, 37467/15991): nguồn cty1 = 0, đích cty4 = SL phân bổ. Đã đưa 2 cặp 11309 về đúng quy luật này.

## Checkpoint — 2026-08-06 13:50
Vừa hoàn thành: vá code + fix 3 prepick (52356, 52352, 52354) + rà soát sạch toàn production
Đang làm dở: (không)
Bước tiếp theo: DEPLOY code TransferProductAllocation.php lên production (chặn tái diễn). Riêng "luồng điều chuyển tự hủy suất giữ nguồn" là cải tiến riêng — cân nhắc sau
Blocked:

## Ghi chú
DB .env đang trỏ production erp_new. Data fix có backup trước khi update.
