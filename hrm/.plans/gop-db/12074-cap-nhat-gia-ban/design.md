# #12074 — Cập nhật giá bán: mặc định chỉ Giá bán lẻ, "Show đủ bảng giá", cấu hình cột, các bảng giá độc lập

**Người phụ trách:** @junfoke — 2026-11-09
**Redmine:** http://quanly.dnsmedia.vn/issues/12074 (Tài chính · Web App, không có ảnh đính kèm)
**Màn:** Tài chính › Quản lý giá – CTKM › Giá bán › Cập nhật giá bán (`/finance/product-prices`, G4 — màn gốc của @dnsnamdang)
**Nhánh:** `feat/12074-cap-nhat-gia-ban` (hrm-client, tách từ `origin/gop_db`, làm trong `.worktrees/gop-db`). hrm-api không đổi.
**Spec chi tiết:** `docs/superpowers/specs/gop-db/2026-11-09-12074-cap-nhat-gia-ban-design.md`

## Mục tiêu

1. Mở màn: mỗi khối hàng × ĐVT chỉ hiện dòng **Bán lẻ** (+ giá hiệu lực của nó).
2. Ô tích **"Show đủ bảng giá"** trên đầu bảng: tích thì hiện đủ 6 loại giá. Mặc định tắt, **không nhớ** trạng thái.
3. Nút **Cấu hình cột hiển thị**: ẩn/hiện + đổi thứ tự cột, lưu theo tài khoản.
4. Các bảng giá **độc lập**: sửa loại giá nào thì chỉ loại đó đổi (bỏ lan Bán lẻ ⇒ Theo lô, ĐL1–3).

## Quyết định đã chốt (user, 09/11/2026)

| # | Quyết định | Lý do |
| --- | --- | --- |
| Q1 | "Cột bảng giá" trong issue = **dòng loại giá** (màn vẽ 1 khối 6 dòng, không có cột theo loại giá) | Không viết lại bảng sang dạng cột |
| Q2 | **TMĐT vẫn = Bán lẻ × hệ số TMĐT công ty** khi chưa tick "Sửa tay" | Đồng bộ với Import Excel / Phiếu tính giá / YC hỏi giá (BE `resolvePrices` dùng chung). Bỏ riêng ở màn này thì cùng một mặt hàng sẽ ra giá TMĐT khác nhau tuỳ nơi nhập. Muốn tách TMĐT thì dùng "Sửa tay" (đã có). |
| Q3 | ~~Không sửa `Calc`~~ → **SỬA `Calc` dùng chung** (user đồng ý 09/11 chiều): bỏ `Calc.spread`, `setPrice/setCoef/setSmp` chỉ đổi đúng loại; Bán lẻ đổi ⇒ TMĐT tính lại | Issue cập nhật 09/11: "Áp dụng tương tự với Phiếu tính giá / YC hỏi giá" + "Riêng giá TMĐT giữ nguyên logic cũ" (xác nhận Q2). `Calc` chỉ G4 + PTG dùng, cả 2 đều phải bỏ lan |
| Q6 | PTG (`PriceSellTable.vue`): `touched` / cờ `tay` chỉ đánh đúng loại vừa sửa (bỏ lan 2–5) | Cùng luật Q3 |
| Q7 | YC hỏi giá: KHÔNG sửa riêng — giá đi qua PTG tạo từ YCHG. Nút "Duyệt không cần tính giá" (ghi 6 loại = 1 giá cho hàng mới) **giữ nguyên** | User chốt 09/11: đó là gán giá ban đầu, không phải nhảy dây chuyền |
| Q4 | "Show đủ bảng giá" không lưu | Đúng câu chữ issue: mặc định không kích hoạt |
| Q5 | Cấu hình cột theo khuôn màn **Duyệt giá bán** (`approvalColumnDefs`, mixin `columnCustomizationMixin`) | Đồng bộ màn anh em; khoá `master_data_product_prices` |

## Phạm vi

- FE: `components/product/price/ProductPriceTable.vue`, `pages/finance/product-prices/index.vue`, `utils/productPriceModel.js` (`Calc`),
  `components/finance/price-calculate/PriceSellTable.vue` (PTG tab Tính giá).
- Không đổi: BE (không có chỗ lan Bán lẻ ⇒ 2–5 ở BE; TMĐT theo Bán lẻ giữ nguyên), payload PUT (vẫn đủ 6 loại; loại không sửa gửi
  nguyên giá trị cũ ⇒ BE gắn cờ duyệt đúng loại thực sự đổi), màn Duyệt giá, YC hỏi giá.

## Xử lý biên

- Lỗi validate / 422 nằm ở loại giá đang ẩn (vd giá TMĐT dưới giá sàn công ty tạo mã) ⇒ tự bật "Show đủ bảng giá".
- Lỗi nằm ở cột user đã ẩn ⇒ toast nêu tên cột + nhắc bật lại ở Cấu hình cột.
- Loại giá đang ẩn có cờ Chờ duyệt / Không duyệt ⇒ badge "Loại giá khác: …" ở dòng Bán lẻ, bấm để hiện đủ.
- Mở từ thông báo duyệt/từ chối (`?product_id=`) ⇒ bật sẵn "Show đủ bảng giá".
- ⓘ ở dòng Bán lẻ: "Giá TMĐT tự tính = Giá bán lẻ × hệ số (trừ khi bật Sửa tay). Các loại khác không đổi theo".
- Ẩn cột Hiệu lực ⇒ ẩn luôn link "+ Hiệu lực" (không thêm được dòng mà không chọn được ngày).
- Cột khoá: Tên hàng hoá, ĐVT · Lưu (2 cột dính), Loại giá, Giá mới.
