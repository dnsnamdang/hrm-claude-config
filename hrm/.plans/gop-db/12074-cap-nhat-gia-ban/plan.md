# Plan — #12074 Cập nhật giá bán

Tài liệu: `design.md` · spec `docs/superpowers/specs/gop-db/2026-11-09-12074-cap-nhat-gia-ban-design.md`
Nhánh: hrm-client `feat/12074-cap-nhat-gia-ban` (tách `origin/gop_db`, worktree `.worktrees/gop-db`, đã bỏ upstream để Sync không đẩy nhầm lên gop_db).

## Phase 1 — Khảo sát + chốt (09/11/2026)

- [x] Đọc issue Redmine (không có ảnh)
- [x] Khảo sát FE `ProductPriceTable.vue` / `productPriceModel.js` / trang; BE `ProductPriceUpdateService`, `ProductPriceWriter::resolvePrices`, `ProductPriceApprovalSubmitter`
- [x] Chốt với user Q1–Q5 (design.md)

## Phase 2 — Code FE (09/11/2026)

- [x] `ProductPriceTable.vue`: `priceColumnDefs()` + template vẽ theo `visibleCols` (blk/line) + prop `columnKeys`
- [x] `ProductPriceTable.vue`: prop `showAllTypes`, `rowsOf` lọc Bán lẻ, `hiddenFlag` + badge, ⓘ TMĐT ở dòng Bán lẻ, ẩn "+ Hiệu lực" khi ẩn cột Hiệu lực
- [x] `ProductPriceTable.vue`: setter độc lập `setPrice/setCoef/setSmp` (không sửa `Calc`) + `errorColumnOf`
- [x] `index.vue`: `columnCustomizationMixin` (`master_data_product_prices`), nút cấu hình cột ở `#header-actions`, ô tích "Show đủ bảng giá", `toastInvalid`, deep-link bật sẵn show đủ
- [x] Parse SFC (vue-template-compiler + babel) OK
- [x] Test SSR 19/19 PASS

## Phase 3 — Issue cập nhật 09/11 chiều: áp cho Phiếu tính giá / YC hỏi giá, TMĐT giữ logic cũ

- [x] Sửa `Calc` dùng chung (bỏ `spread`) — user đồng ý; gỡ setter riêng ở `ProductPriceTable`
- [x] `PriceSellTable.vue` (PTG): `touched` + cờ `tay` chỉ đúng loại vừa sửa
- [x] YC hỏi giá: khảo sát — không có ô nhập giá riêng; "Duyệt không cần tính giá" giữ nguyên (user chốt)
- [x] Parse SFC 3 file + SSR 19/19 PASS

## Phase 4 — Nghiệm thu

- [x] Trình duyệt G4 (nuxt worktree cổng 3010 — cache-loader khoá theo đường dẫn tuyệt đối nên không đụng nuxt 3000 của repo chính;
      API 8002; đăng nhập DNS Admin mật khẩu prod vì DB `gop_db_rbac`): mặc định / show đủ / sửa Bán lẻ / popup cấu hình cột — ảnh
      `C:\Users\Legion\.pw-mcp\out-a\12074-0{1,2,3}-*.png`
- [x] Lỗi CŨ (có từ G4 10/10): dòng "Sửa tay: ☐ Hệ số ☐ Giá ☐ ĐMGG" của TMĐT cần 206px, cột Loại giá 196 ⇒ "ĐMGG" tràn sang
      cột bên 18px. Nới cột 196 ⇒ 224 (đệm 10px) — ảnh `12074-04-tmdt-sua-tay.png`
- [x] Bấm thử PTG (lập từ PYCTG-03757, không lưu): hệ số Bán lẻ 2 ⇒ giá 4,190,800, TMĐT 2.6/5,448,040, Theo lô + ĐL1–3 đứng yên.
      Phát hiện sót dòng "sửa là áp cho 4 loại dưới" ở Bán lẻ ⇒ bỏ (commit `d7747ea56`, merge develop `5c2db18d3`)
- [x] Lưu thật G4 (STS-AW46200LDA): hệ số Bán lẻ 1.4 ⇒ 1.5 ⇒ lưu, DB chỉ đổi Bán lẻ + TMĐT; đã trả về giá gốc
- [x] Lỗi ở dòng ẩn ⇒ tự bật Show đủ + chữ đỏ đúng ô; lỗi ở cột ẩn ⇒ toast "cột đang ẩn: Hệ số"
- [x] Cấu hình cột lưu + F5 giữ (ẩn Hệ số/Tồn kho), "Show đủ" không nhớ; deep-link `?product_id=` tự hiện đủ; đã trả cấu hình về mặc định
- [x] Phản hồi user: nút Cấu hình cột ở bộ lọc lạc lõng ⇒ chuyển xuống đầu bảng cạnh "Show đủ bảng giá" (như màn Tài khoản…), ảnh
      `12074-30-nut-cot-o-bang.png` / `12074-31-popup-cot.png`; commit `d384b9bcc`, merge develop `98c6975dd`
- [ ] Gửi duyệt (công ty bật duyệt giá) — chưa thử, nhánh BE không đổi
- [x] Commit hrm-client `c431246b0` (nhánh `feat/12074-cap-nhat-gia-ban`) + merge vào `develop` mới nhất `7ad27f0b3`
      (không xung đột, parse + SSR 19/19 trên develop). CHƯA push — user tự đẩy lên test.

## Phase 5 — Issue cập nhật 09/11 tối: cột STT + "Cài đặt bảng giá" (thay "Show đủ bảng giá")

- [x] Chốt với user: radio "Mặc định" = giá CHÍNH đứng đầu mỗi khối, luôn hiển thị (công ty không dùng Bán lẻ, vd ETEK GREEN
      chỉ làm giá đại lý); lưu theo TÀI KHOẢN × CÔNG TY (khoá `product_price_types_c{id}` trong `human/column-customizations`, không sửa BE)
- [x] `PriceTypeSettings.vue` (mới): Hiển thị tất cả + 6 loại (Hiển thị / Mặc định), Áp dụng (phiên) / Lưu mặc định
- [x] `ProductPriceTable.vue`: cột STT (dính, theo trang), prop `visibleTypes` + `mainType` thay `showAllTypes`, badge "Loại giá đang ẩn" ở dòng chính
- [x] `index.vue`: nạp/lưu cấu hình, deep-link + lỗi ở loại ẩn ⇒ hiện đủ (phiên)
- [x] SSR 24/24 · trình duyệt: mặc định 1/6, Áp dụng ĐL1+Bán lẻ+ĐL2 (F5 về 1/6), Lưu ĐL1 (F5 giữ), Hiển thị tất cả 6/6,
      STT trang 2 = 21–40, deep-link 6/6, lỗi dòng ẩn ⇒ 6/6 + chữ đỏ; đã trả cấu hình về mặc định. Ảnh `12074-4{0..8}-*.png`
- [x] Bẫy: V2BaseRadio wrapper có margin-top 15px + nhãn rỗng bị thay bằng value ⇒ nhãn ' ' + ghi đè margin trong popover
- [x] Commit `e6095bcec`, merge develop `fda841d41` — CHƯA push

## Phase 6 — QA 10/11: cột Tên hàng hoá nhỏ, Loại giá / Hệ số phình

- [x] Nguyên nhân: phần dư bề rộng chỉ chia cho cột KHÔNG dính ⇒ Tên (dính) kẹt 210px. Sửa: `growWidths` chia theo `grow`/`max`
      (Tên ≤ 420 ưu tiên, số/ô nhập có trần), còn dư thì cột chữ ×3; `left` cột dính tính từ bề rộng thật (`stickyLeft`)
- [x] SSR 31/31 · trình duyệt 1850 ít cột: Tên 718, Loại giá 295, Hệ số 184, tên 1 dòng (~9 hàng/khung thay vì 5); 1366 đủ cột
      giữ nguyên, cuộn ngang 3 cột dính liền nhau. Ảnh `12074-5{0,1,2}-*.png`
- [x] Commit `5542a006c`, merge develop local `584249333` (CHƯA push develop); user đã duyệt cổng chính ⇒ push thẳng gop_db `5cc18f69e` (10/11)

- [x] QA báo lại (màn đủ cột): bảng đã cuộn ngang ⇒ không có phần dư để giãn. Đổi bề rộng gốc Tên 210 ⇒ 290, Loại giá 224 ⇒ 176
      (dòng "Sửa tay" TMĐT flex-wrap). 1920 đủ 15 cột vừa khít không cuộn. Commit `3cbebf632`, push gop_db `cc213ac89`, develop local `d6a6883cf`

## Phase 7 — Issue 10/11: Cài đặt bảng giá trên Phiếu tính giá, cấu hình DÙNG CHUNG mọi màn (làm ở DEVELOP trước)

- [x] `utils/mixins/priceTypeViewMixin.js` (nạp/lưu/áp/revealTypes, khoá `product_price_types_c{công ty}`); G4 chuyển sang mixin
- [x] PTG: nút ở thanh tab (chỉ tab Tính giá), `PriceSellTable` prop `visibleTypes`/`mainType` (mặc định đủ 6 — không ảnh hưởng chỗ khác);
      cấu hình theo CÔNG TY CỦA PHIẾU (`typeViewCompanyId` = detail.company.id, nạp sau load); lỗi 422/FE `rows.i.prices.{type}` ở loại ẩn ⇒ hiện đủ
- [x] SSR 41/41 · trình duyệt (áp patch tạm lên worktree gop_db để chạy 3010 rồi gỡ): lưu ở G4 ⇒ PTG-03771 (Tân Phát) 2/6 ĐL1 đầu;
      lưu ở PTG ⇒ G4 6/6; đã trả cấu hình c1 về mặc định. Ảnh `12074-7{4,5}-*.png`
- [x] Commit develop (repo chính) `d194baa03` — CHƯA push, CHƯA lên gop_db (user: cập nhật lớn ⇒ develop trước)
- [x] 10/11/2026 — User duyệt ⇒ cherry-pick `d194baa03` sang gop_db, push `origin/gop_db` `881920825` (test PASS trên gop_db). develop local còn đi trước remote 5 commit, CHƯA push.
- [x] 10/11/2026 — Chốt với user: #12074 đã lên prod ⇒ lỗi QA tiếp theo sửa THẲNG trên `gop_db` (repo chính hrm-client), không qua nhánh feat + merge nữa.

## Ghi chép ngày (note cuối ngày)

- [x] 09/11/2026 — Tính năng mới #12074: [Cập nhật giá bán] mặc định giá bán lẻ, "Show đủ bảng giá", cấu hình cột, cập nhật độc lập từng bảng giá (TMĐT giữ = Bán lẻ × hệ số); áp tương tự Phiếu tính giá (sửa `Calc` dùng chung). Sửa kèm dòng "Sửa tay" TMĐT tràn ô (cột Loại giá 196 ⇒ 224). Commit `c431246b0` + `d7747ea56`, merge develop.
- [x] 09/11/2026 — Fix phản hồi #12074: nút Cấu hình cột chuyển xuống đầu bảng (`d384b9bcc`); issue cập nhật 9/11: cột STT + popover "Cài đặt bảng giá" (giá mặc định đứng đầu, lưu theo tài khoản × công ty) `e6095bcec`.
- [x] 10/11/2026 — Đẩy #12074 lên gop_db (merge `52e795dfd`). Fix phản hồi #12074: co giãn cột (Tên hàng hoá giãn trước, `5542a006c`), rồi đổi bề rộng gốc Tên 210 ⇒ 290 / Loại giá 224 ⇒ 176 (`3cbebf632`) — lên gop_db `cc213ac89`.
- [x] 10/11/2026 — Tính năng mới #12074 (cập nhật issue): "Cài đặt bảng giá" trên Phiếu tính giá, cấu hình dùng chung mọi màn (mixin `priceTypeViewMixin.js`) — develop `d194baa03`, gop_db `881920825`.

## Checkpoint — 2026-11-09

- **Vừa hoàn thành:** code FE G4 + PTG (`Calc` mới), SSR 19/19, bấm thật G4; commit + merge develop local (chưa push).
- **Đang làm dở:** —
- **Bước tiếp theo:** bấm thử PTG + lưu thật (Phase 4).
- **Blocked:** —
