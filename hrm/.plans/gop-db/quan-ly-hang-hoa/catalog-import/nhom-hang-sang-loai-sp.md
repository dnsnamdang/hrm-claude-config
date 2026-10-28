# Quy đổi Nhóm hàng hoá (cũ) → Loại sản phẩm (mới) — khảo sát (16/10/2026)

**Trạng thái:** CHỜ nghiệp vụ sửa file theo `can-sua-cay-phan-loai-1610.xlsx` (gửi 16/10). Chưa viết code, chưa chạy gì vào DB.

## File nguồn
`Copy of Quan hệ HH.xlsx` (Desktop) — 1 sheet "Sheet3", 2 cột: `Loại sản phẩm` (tên) · `Mã nhóm hàng hóa cũ` (= `groups.id`).
- 1.691 dòng, 0 dòng thiếu, 0 cặp trùng.
- 778 Loại sản phẩm khác nhau (0 tên trùng khi bỏ hoa thường).
- 587 mã nhóm; **586 có trong DB** — thiếu `2579` (`groups.id` max = 2578 trên giacty; có thể là nhóm mới trên prod).
- Quan hệ NHIỀU–NHIỀU: **277 nhóm ứng với >1 Loại** (nhóm 2283 → 147 Loại, 2294 → 73, 2385 → 60, 2071 → 34…).

## DB (`hrm_erp_giacty`)
- Cây phân loại: Tính chất (`product_natures` 1) › Nhóm chức năng (`product_function_groups` 0) › Nhóm SP (`product_families` 0) ›
  Loại SP (`product_types` 0). `product_types.product_family_id` NOT NULL; `code`, `name` UNIQUE.
- `groups` 893 nhóm (id 1686–2578); file phủ 586.
- `products` 45.890 (28.378 đang dùng, status<>0); 100% có `group_id`, 0 có `product_type_id`.

## Hàng hoá quy đổi được tự động hay không
| Nhóm của hàng | Hàng (tất cả) | Hàng đang dùng |
|---|---|---|
| nhóm ↔ đúng 1 Loại (310 nhóm) | 9.628 | 5.574 |
| nhóm ↔ nhiều Loại (277 nhóm) | 32.269 | 20.759 |
| nhóm không có trong file (307 nhóm) | 3.993 | 2.045 |

⇒ chỉ ~21% hàng (20% hàng đang dùng) gán được Loại SP từ nhóm; còn lại cần căn cứ khác (tên hàng / danh sách hàng → Loại) hoặc gán tay.

## Đã chốt (16/10)
- C1: cấp cha lấy từ file cây 4 cấp user gửi thêm.
- C2: user gửi luôn file danh mục 4 cấp — xem lại cách quy đổi hàng sau khi có file.
- C3: tên trùng nhiều cha ⇒ nghiệp vụ sửa file. Đã xuất `can-sua-cay-phan-loai-1610.xlsx`: (1) 50 tên trùng theo đường cha đầy đủ (Nhóm CN 1 · Nhóm SP 27 · Loại SP 22 — phần lớn kéo theo từ Nhóm CN "Thiết bị đo - kiểm tra" nằm dưới 2 Tính chất); (2) mã Tính chất thiếu/lệch tên; (3) 55 Nhóm SP thiếu mã + 107 mã có tên không có trong cây; (4) 569 dòng hàng lỗi (373 đường 4 cấp không khớp cây · 168 thiếu mã hàng · 22 Loại SP không có trong cây · 14 mã hàng trùng).

## Câu còn hỏi khi có file sửa
- 20.398 hàng đang dùng không có trong sheet hàng — dùng file Quan hệ HH (nhóm 1–1) gán phần rõ, còn lại xuất danh sách?
- Mã Nhóm CN / Loại SP: tự sinh NCN.0001… / LSP.0001…?
- Phạm vi code: repo/nhánh, file đọc từ đâu, chạy DB nào; dòng rác `TCHH.GJGH` trên dev.

## Câu hỏi (lần lượt)
1. Cấp cha của Loại SP (Nhóm SP, Nhóm chức năng, Tính chất) không có trong file — lấy ở đâu?
2. Hàng thuộc nhóm ↔ nhiều Loại: xử lý thế nào?
3. Seeder làm tới đâu: chỉ tạo Loại SP + bảng quan hệ nhóm↔loại, hay gán luôn `products.product_type_id`?
4. Mã Loại SP (`code` bắt buộc, duy nhất) sinh theo quy tắc nào?
5. Phạm vi code: repo/nhánh, file đọc từ đâu, chạy vào DB nào.

## File cây 4 cấp `Copy of ERP_final ngày 16-10-le.xlsx` (Desktop, 33 sheet) — khảo sát 16/10
- **CâyERP** (982 dòng, đủ 4 cấp mọi dòng): 8 Tính chất · 48 Nhóm CN · 270 Nhóm SP · 957 Loại SP. Khớp 100% 3 sheet
  "Cấp 1-2" (49 cặp) · "Cấp 2-3" (288) · "Cấp 3-4" (976).
- **Cùng tên dưới nhiều cha** (DB bắt `name` UNIQUE toàn bảng ở cả 4 cấp): Nhóm CN 1 ("Thiết bị đo - kiểm tra"),
  Nhóm SP 14 (vd "Giá - khung - kệ - móc", "Chiếu sáng"), Loại SP 19 (vd "Tủ đồ nghề", "Bơm thủy lực bằng tay").
- **Mã**: DB bắt `code` UNIQUE dạng `<PREFIX>.<4 ký tự>` (TCHH./NCN./NSP./LSP.). File: "Mã cấp 1" 6 mã (`TCHH.A001`… — tên
  "Dây chuyền, hệ thống" lệch tên cây "Dây chuyền - hệ thống"; 2 Tính chất không có mã: "Thiết bị và dụng cụ đo - kiểm",
  "Thiết bị và đồ dùng văn phòng") · "Mã cấp 2" rỗng · "Mã cấp 3" 322 mã `NSP.Mxxx` (55 Nhóm SP của cây không có mã) ·
  "Mã cấp 4" 982 tên, 0 mã.
- **Hàng hoá — sheet "NewERP Green Power"**: 9.382 dòng (Cấp 1–4 + tên + Mã Fast + Mã hàng + ID nhóm cũ). 168 dòng thiếu
  mã hàng, 7 mã trùng, 395 dòng có đường 4 cấp KHÔNG khớp CâyERP, 7 Loại SP không có trong CâyERP.
  9.207 mã khác nhau → **7.984 khớp `products.code`** (7.980 đang dùng). DB có 28.378 hàng đang dùng ⇒ **20.398 hàng đang
  dùng KHÔNG có trong file**.
- File "Quan hệ HH" (778 Loại): 5 Loại không có trong CâyERP (trùng 5/7 tên ở trên).
- DB dev: `product_natures` có 1 dòng rác `TCHH.GJGH` "hjjhjh".
