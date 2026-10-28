# Ảnh hàng hoá — Plan

**Design:** `design.md` · @namdangit · nhánh `gop_db` · chỉ hrm-client.
✅ User cho "làm" 24/10/2026. Commit hrm-client `f3d7df2d8` (chi tiết + helper) — phần `ProductListPage.vue`
lọt vào commit `1ab0006b6` (session Kế thừa giá). **ĐÃ PUSH 24/10** gop_db (merge `0113bddb6`, kèm hrm-api `2169b460e` — BE Kế thừa giá + Chuyển KD của session kia).

## Task 1 — FE
- [x] `utils/file-preview.js`: `openImagePreview()`
- [x] `components/product/detail/ProductTabGeneral.vue`: computed `images` (avatar + galleries, không lặp), bấm ⇒ FilePreviewModal
- [x] `components/product/ProductListPage.vue`: ô Ảnh `product-thumb--clickable` ⇒ FilePreviewModal (6 màn)

## Task 2 — Kiểm
- [x] Tái hiện trên prod (44829: 0 ảnh; 4014: thiếu avatar) qua Claude in Chrome — chỉ đọc
- [x] Playwright MCP local: 44829 hiện 1 ảnh, popup căn giữa, nền phủ toàn màn, không tab mới; 4014 đủ 2 ảnh; Đang KD 19/19 ô có ảnh bấm được
- [x] e2e mới `e2e/tests/master-data/products-image-preview-ui.spec.ts` 5/5 (page.route ảnh giả, không ghi DB)
- [x] Cập nhật 3 ca cũ lệch code trong `products-read-ui.spec.ts` (Xuất Excel + Lập yêu cầu hỏi giá được phép; bộ lọc entering 12 ô 4·4·4; footer chi tiết thêm 2 nút Chuyển kinh doanh)
- [x] Chạy `products-read-ui` + `products-filter-layout-ui` + `products-image-preview-ui`: **23/23 xanh** (--workers=1 --no-deps)

### Checkpoint — 24/10/2026 (wrap up)
Vừa hoàn thành: sửa ảnh chi tiết + xem ảnh cỡ đầy đủ (chi tiết + 6 màn danh sách), commit `f3d7df2d8`; e2e 23/23
Đang làm dở: —
Bước tiếp theo: pull prod (hrm-client + hrm-api)
Blocked: —
