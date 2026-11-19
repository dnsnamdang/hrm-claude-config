# Phase 3 — Hiện hàng con ở màn CHI TIẾT + PTKD duyệt từng con

## Bối cảnh / Bug phát hiện (PYCHG-04697, user 2026-11-03)

Cụm (công thức ghép bộ) có 2 hàng con đang **không hiển thị** ở màn **Chi tiết yêu cầu hỏi giá**, và **bước PTKD duyệt không duyệt được từng hàng con** → con tạm kẹt `pcc.status = 6` mãi dù cha đã qua 7 và phiếu đã sang Đã tính giá.

Phase 1/2 chỉ làm màn **Thêm/Sửa** (hiện con + sửa con tạm cho đủ thông tin + chặn gửi). Màn **Chi tiết** và **luồng PTKD duyệt** chưa đụng tới con.

## 2 lỗi gốc (đã xác minh code)

1. **Chi tiết ẩn con.** `PriceAskingRequestService::show()` → `lineRow()` (dòng 455) **bỏ** `recipe_children` khi map dòng — dù dữ liệu con đã có sẵn: `rows()` → `enrich()` (PriceAskingProductReader:205) đã gắn `recipe_children` vào mỗi `$productRows[pid]`. Chỉ là `lineRow()` không copy ra.
2. **Con không duyệt được + không chặn phiếu.**
   - `tempForm()` (Service:521) và `assertTempGate()` (Writer:494) gate `product_id` phải là **DÒNG** `price_asking_request_products` → con (không phải dòng) bị **404**.
   - `temp_pending_count` (show:433) và gate `ptkdApprove()` (Writer:594) chỉ đếm `pcc.status=6` trên **dòng cha** → con tạm 6 không khoá nút Duyệt phiếu ⇒ phiếu duyệt xong con vẫn 6.

## Hướng đã CHỐT (user 2026-11-03): "Hiện lồng + duyệt từng con"

- Dòng cụm bung ra hàng con ở màn Chi tiết (đã có khung `recipe-child-row`, chỉ cần BE trả data).
- **Mỗi con tạm (6/7/8) có nút Duyệt/Sửa riêng** khi phiếu Chờ PTKD + người xem là PTKD 1662 công ty phiếu — y hệt dòng cha (6 ⇒ "Duyệt", 7/8 ⇒ "Sửa" mở lại form đổi quyết định).
- `temp_pending_count` + gate `ptkdApprove` **tính cả con** ⇒ còn con tạm 6 thì **khoá nút Duyệt phiếu** ("Còn N hàng tạm chưa duyệt").
- **Nhất quán chốt Phase 2**: con **KHÔNG** là dòng hỏi giá. "Duyệt hàng tạm con" = vòng đời hàng tạm (master-data 6→7/8), tách biệt hỏi giá. Con bị Không duyệt (8) **không** kéo cha/nhóm huỷ (C6 chỉ xét dòng cha). Chỉ con **6** (chưa quyết) mới khoá phiếu.
- Tái dùng trang duyệt sẵn có `pages/sale/price-asking-requests/_id/temp/_productId.vue` (nhận `productId` bất kỳ) — chỉ cần mở gate BE cho con.

## Thay đổi

### BE — `PriceAskingProductReader.php`
- `recipeChildren()`: thêm `'company_status' => $status` (số pcc) vào mỗi con. Vô hại với create/edit.

### BE — `PriceAskingRequestService.php`
- `lineRow()`: trả `recipe_children` lấy từ `$product['recipe_children']`, bồi thêm mỗi con:
  - `can_temp_approve = $canPtkd && child.is_temp`
  - `temp_reject_reason = (status==8) ? $rejectReasons[child.product_id] : null`
- `show()`: `$rejectReasons` dựng trên map gồm **cả mã con** (gom từ `recipe_children`) để tra lý do Không duyệt con.
- `show()`: `temp_pending_count` += số con có `company_status == 6`.
- `tempForm()` gate (521): thay `exists()` dòng bằng `PriceAskingRequestWriter::productInRequest($request->id, $productId)` (dòng HOẶC con ghép bộ).

### BE — `PriceAskingRequestWriter.php`
- Thêm `public static function productInRequest(int $requestId, int $productId): bool` — true nếu productId là DÒNG hỏi giá, hoặc là `recipe_products.product_id` với `base_product_id ∈` các dòng của phiếu.
- `assertTempGate()` (494): dùng `productInRequest()` thay cho check dòng; `$line` fetch có điều kiện (null nếu là con — không caller nào dùng `$line`).
- `ptkdApprove()` gate (590-597): gộp product_id con ghép bộ vào tập kiểm `$statuses` ⇒ `$pending` đếm cả con 6. C6 (đóng nhóm) giữ nguyên chỉ xét dòng cha.

### FE — `PriceAskingRequestForm.vue`
- `ptkdTempActions` computed: thêm điều kiện con có `can_temp_approve`.
- Dòng con (readonly, nhánh `v-else-if="ptkdTempActions"`, dòng 304): render Duyệt/Sửa mirror cụm cha (`child.can_temp_approve`, `Number(child.company_status)===6` ⇒ Duyệt, else Sửa; `openTempApprove(child)`), kèm icon ⓘ b-popover.
- Dòng con: hiện lý do Không duyệt (`child.temp_reject_reason`) dưới tên con khi bị 8.

## Edge / không làm
- Con ERP (không tạm) ở chi tiết: chỉ hiện, không nút duyệt (can_temp_approve=false). Đúng.
- Không đụng trang `_id/temp/_productId.vue` (đã nhận productId bất kỳ; gate BE mở là đủ).
- Không đổi C6/đóng nhóm theo con.
