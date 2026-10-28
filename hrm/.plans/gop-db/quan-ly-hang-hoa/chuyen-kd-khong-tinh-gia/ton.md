# Hàng lấy về — tuỳ chọn "Không bắt buộc tính giá" — Tồn

> 23/10/2026 · nhánh `gop_db`. ⛔ Chưa code — hỏi LẦN LƯỢT, chốt đủ mới viết design/plan.

## Spec user (23/10)
Bỏ nguyên tắc "mọi hàng bắt buộc qua 4 chứng từ tính giá" (K1 / §29a-1 / Q1a) cho hàng **lấy từ công ty khác về**:
ở màn *Hàng hoá nhập thông tin* có tuỳ chọn **"Hàng hoá không bắt buộc tính giá"**. Chọn ⇒ sinh các loại giá = 0 và
chuyển trạng thái (hàng × công ty) sang **Đang kinh doanh**.

## Chốt cũ bị đổi / chạm
| Chốt cũ | Ảnh hưởng |
|---|---|
| K1, §29a-1, Phase 7 Q1a: mọi hàng qua YCHG→YCTG→PTG→KQ | thêm NGOẠI LỆ cho hàng lấy về |
| P4 (giá theo công ty): Đang KD ⇔ có bộ giá | vẫn giữ: bộ giá có đủ dòng, giá trị 0 |
| Giá 0 / ≤ 1 đ = "chưa có giá" (gia-0, N194) | hàng này hiện "Chưa có giá"; Báo giá cảnh báo khi chọn (gia-0 Phase 2) |
| OwnerPriceFloor (giá B ≥ giá A) | giá B = 0 đã được bỏ qua sàn (gia-0 Phase 1) ⇒ không vướng |
| Q15: YCHG nhận hàng Đang KD | về sau vẫn hỏi giá được qua YCHG |

## Dữ kiện code (23/10)
- Lấy về đã sinh bộ giá rỗng (6 loại × mọi ĐVT = 0) cho công ty nhận ⇒ "sinh giá 0" thực chất đã có, chủ yếu là chuyển trạng thái.
- Màn Nhập thông tin có trạng thái phụ Chưa/Đã nhập thông tin (`pcc.info_entered_at`, 21/10).

## Câu hỏi
| # | Câu | Chốt |
|---|---|---|
| Q1 | Điều kiện thông tin trước khi chuyển: phải "Đã nhập thông tin" (đã Lưu tab Quản trị) hay chuyển được ngay sau khi lấy về | ✅ 23/10 **phải Đã nhập thông tin** (`info_entered_at` NOT NULL) |
| Q2 | Tuỳ chọn là thao tác 1 lần hay cờ lưu lại trên hàng × công ty (hiện badge, lọc được) | ✅ 23/10 **thao tác 1 lần**, không cột mới, không migration |
| Q3 | "Các loại giá = 0" gồm gì: chỉ 6 giá bán, hay cả giá vốn / giá mua ngoài / ĐMGG (ảnh hưởng hạch toán, hiệu quả HĐ) | ✅ 23/10 **tất cả = 0** (giữ như lúc lấy về); chấp nhận chứng từ cần giá vốn bị chặn duyệt (P8) tới khi B hỏi giá / cập nhật giá |
| Q4 | Quyền dùng tuỳ chọn | ✅ 23/10 **Xây dựng thông tin hàng hoá** tại công ty B (như Lấy về), không quyền mới |
| Q5 | Từng dòng hay hàng loạt; có làm ngay trong bước Lấy về không | ✅ 23/10 **từng dòng (menu dòng) + hàng loạt** (tick, ≤ 100 mã/lượt), popup xác nhận, mã không đủ điều kiện bỏ qua + báo lý do. Không gộp vào bước Lấy về (vì Q1 phải Đã nhập thông tin) |
| Q6 | Hàng đang nằm trong YCHG (Chờ tính giá / Đang tính giá) có dùng được không | ✅ 23/10 **không — chỉ trạng thái 1** (+ Đã nhập thông tin); 2/5 bỏ qua + báo phiếu đang chứa. Tự suy: hàng chỉ nằm trong YCHG nháp (vẫn status 1) thì được chuyển; gửi YCHG sau đó vẫn hợp lệ vì YCHG nhận hàng Đang KD (Q15) |
| Q7 | Ghi lịch sử giá / lịch sử hàng hoá thế nào | ✅ 23/10 **chỉ lịch sử hàng hoá**: 1 dòng *Thay đổi trạng thái* Đang nhập thông tin → Đang kinh doanh, ghi chú "Không bắt buộc tính giá"; không ghi lịch sử giá |
| Q8 | Chỉ hàng lấy về, hay cả hàng công ty tự tạo | ✅ 23/10 **CẢ hàng tự tạo** ⇒ K1 bỏ hẳn tính bắt buộc: mọi hàng ở màn Nhập thông tin (status 1 + Đã nhập thông tin) đều chọn được. Hệ quả chấp nhận: hàng chủ Đang KD giá 0 vẫn lấy về được (L3 chỉ xét trạng thái); sàn giá B ≥ A bỏ qua khi giá A = 0 (Q3 cũ) |
| Đ2 | Hàng Đang KD giá 0 bị khoá rồi khôi phục | ✅ 23/10 user đổi điểm tự quyết: **về Đang KD**. Phạm vi: **mọi hàng khoá theo công ty** (pcc 4) khôi phục luôn về Đang KD, bỏ điều kiện giá + Loại SP (đổi K2/K3 `hang-hoa-dang-khoa`); hàng ERP đã xoá giữ luật cũ |

## Tổng hợp chốt (23/10) — đầu vào design
- Thao tác **"Chuyển kinh doanh không tính giá"** ở màn *Hàng hoá nhập thông tin*: menu dòng + hàng loạt (≤ 100 mã), popup xác nhận.
- Điều kiện từng mã (BE kiểm, mã sai bỏ qua + báo lý do): trạng thái hàng × công ty = 1 · `info_entered_at` NOT NULL · không đang ở YCHG đã gửi (2/5) · không khoá/xoá (`products.status = 1`).
- Kết quả: `pcc.status` 1 ⇒ 3; bộ giá công ty đủ 6 loại × mọi ĐVT = 0 (bù dòng thiếu, giữ dòng đã có — đã 0), giá vốn / giá mua ngoài / ĐMGG = 0; không cột mới, không migration.
- Quyền: *Xây dựng thông tin hàng hoá* tại công ty đang làm việc. Lịch sử hàng hoá 1 dòng *Thay đổi trạng thái*, ghi chú "Không bắt buộc tính giá".
- Sau đó: hàng hiện "Chưa có giá" (≤ 1 đ), Báo giá cảnh báo khi chọn (gia-0); muốn có giá ⇒ YCHG (nhận hàng Đang KD) hoặc màn Cập nhật giá bán.
- Chứng từ cần giá vốn (hạch toán hỗ trợ, hiệu quả HĐ) bị chặn duyệt tới khi có giá vốn (P8) — chấp nhận.
