# Plan — Báo giá: quyền áp dụng giảm giá (#10789)

## Phase 1 — Quyền + chốt chặn BE

### BE
- [x] Thêm permission `Cho phép thêm giảm giá trong báo giá` (id 1107, group Báo giá) vào `PermissionsTableSeeder`
- [x] `QuotationService::assertCanChangeDiscount()` — so vân tay giảm giá payload vs bản lưu, thiếu quyền + có thay đổi → `Exception(..., 403)`
- [x] Gọi guard ở `QuotationService::create()` (báo giá mới) và `update()`
- [x] `QuotationController::update()` map exception code 403 → HTTP 403

### FE
- [x] computed `canApplyDiscount` đọc từ `$store.state.permissions` (mặc định false, không hard-code true)
- [x] computed `canEditDiscount = canEdit && canApplyDiscount`
- [x] Ô GG trên toolbar: `:disabled` khi không quyền + icon `ri-lock-line` kèm tooltip lý do
- [x] Ô nhập GG(%) / GG(₫) / Phân bổ GG của dòng hàng hoá + dòng dịch vụ theo `canEditDiscount`
- [x] Section "Giảm giá tổng đơn hàng" (chọn loại GG, kiểu, giá trị, nút Thêm/Xoá khoản GG, Phân bổ) theo `canEditDiscount`

## Kết quả test (2026-08-17)

**BE — `assertCanChangeDiscount()` (transaction + rollback):**

| Ca | Kết quả |
| --- | --- |
| Không quyền · payload không đụng GG | cho qua ✅ |
| Không quyền · gửi lại GG y hệt (báo giá đang có GG tổng 2.000.000) | cho qua ✅ (giữ được dữ liệu cũ) |
| Không quyền · bật GG mặt hàng | chặn 403 ✅ |
| Không quyền · thêm tiền GG 50.000 | chặn 403 ✅ |
| Không quyền · thêm GG tổng đơn | chặn 403 ✅ |
| Không quyền · nâng GG tổng 2tr → 3tr | chặn 403 ✅ |
| Không quyền · xóa sạch GG | chặn 403 (xem lưu ý dưới) |
| **Có quyền** · bật GG / thêm tiền GG | cho qua ✅ |

**FE — màn Sửa báo giá BG-2026-00240:** chưa cấp quyền → ô GG `disabled`, giá trị "Không GG", có icon khoá + tooltip; cấp quyền rồi reload → ô GG bật lại, icon khoá biến mất.

⚠️ **Lưu ý cần chốt**: user không quyền mà **xóa** giảm giá cũ cũng bị chặn 403 (vì cũng là "thay đổi giảm giá"). FE đã ẩn nút xóa khoản GG nên đường thường không chạm tới, nhưng nếu nghiệp vụ muốn cho phép gỡ giảm giá thì phải nới guard.

## Test lại đầy đủ trên nhánh `tpe-develop-assign` (2026-08-18)

| AC | Cách kiểm | Kết quả |
| --- | --- | --- |
| AC1 | API `timesheet/permissions` + DOM màn Phân quyền | quyền nằm trong nhóm "Báo giá", có checkbox + label ✅ |
| AC3 | Cấp quyền → màn Sửa BG-2026-00240 | ô GG bật, gõ được 250.000 vào GG(₫) ✅ |
| AC4 | Thu quyền → GG mặt hàng | ô GG disabled, GG(%)=2 và GG(₫)=100.000 vẫn hiện nhưng khoá; icon khoá **xám** #6b7280 ✅ |
| AC4 | Thu quyền → GG tổng | section hiện đủ 300.000 với 0 select / 0 input / 0 nút ✅ |
| AC5 | PUT thật `/api/v1/assign/quotations/240` | đổi phương thức GG → **403**; thêm tiền GG dòng → **403**; thêm GG tổng đơn → **403**; gửi lại GG y nguyên → 200; payload không đụng GG → 200 ✅ |

Lưu ý: id quyền trong seeder là **1173** (commit `fix quyen` đổi từ 1107); DB local đã đồng bộ.

### Checkpoint — 2026-08-17
Vừa hoàn thành: BE + FE #10789, test 8 ca BE + AC3/AC4 trên UI.
Đang làm dở: không.
Bước tiếp theo: gán quyền thật cho vai trò trên môi trường test rồi để QA chạy AC1–AC5.
Blocked:
