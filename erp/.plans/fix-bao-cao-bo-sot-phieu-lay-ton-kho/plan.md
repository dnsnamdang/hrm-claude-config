# Fix: 2 báo cáo bỏ sót / nhân đôi dữ liệu phiếu "lấy tồn kho đang về"

**Người phụ trách:** @junfoke
**Repo:** `TanPhatDev` · **Nhánh:** `task_bao-cao-ton-kho-dang-ve` (rẽ từ `master`) · **Commit:** `34629bd704`
**Nguồn:** khách báo 16/09/2026 sau khi nắn data HĐ 1336 — "2 báo cáo vẫn sai theo cái cũ, thiếu dữ liệu của Nguyễn Văn Thu".
Liên quan: `../fix-ton-kho-dang-ve-gop-nham-dong-ton-kho/plan.md`

## Kết luận: data không sai, lỗi nằm ở chính báo cáo

Sau đợt nắn data, dữ liệu đã đầy đủ: phụ lục `2111` (16/09 10:47) có đủ 4 dòng, dòng `6790` của
Lexus Phú Mỹ Hưng trỏ đúng dòng PI mới `17159`; sổ cái `54082-54085` = 2/6/2/2 = 12.

## Lỗi 1 — Báo cáo quá trình đặt hàng theo nhân viên (`/admin/orders/reports/orderReportProcess`)

`OrderReportProcessService::getData()` chạy cứng theo chuỗi **Đơn hàng tổng hợp → PI → HĐ → Kho**:
`getDataTNPo()` lấy gốc từ `inland_order_summary_new_customer_details`, rồi
`getDataTNPI()` lọc tiếp `whereIn('pi.inland_order_summary_new_id', $poId)`. Không có PO thì cả
nhánh chết, các cột PO/PI/HĐ/Kho rỗng.

Phiếu **lấy tồn kho đang về** (`type_order_import = 2`) lấy hàng từ PI/hợp đồng có sẵn nên không đi
qua bước tổng hợp. Đếm trên DB: **40/40 phiếu loại này không có mặt trong tổng hợp**.

**Cách sửa:** thêm `getDataTNPIStock($request, $rorId)` — bản sao `getDataTNPI` bỏ ràng buộc order
summary, lọc `type_order_import = NHAP_TON_KHO_DANG_VE`. Trong vòng lặp thêm nhánh `else` chỉ chạy
khi dòng đó **không có PO**, rồi dùng lại `getDataTNHD` / `getDataTNWH` sẵn có. Hoàn toàn additive.

## Lỗi 2 — Báo cáo luân chuyển hàng hóa (`/admin/stock-transfer/report`), popup Chi tiết

`StockTransferReportService::getEmpStockTranfer()` nhánh hàng trong nước `leftJoin`
`inland_buy_contract_new_product_details` theo `inland_order_request_new_detail_id` nhưng **thiếu
`groupBy(['p.product_id', 'd.id'])`** — nhánh hàng nhập khẩu ngay bên trên thì có. Một dòng nhu cầu
gắn 2 chi tiết hợp đồng (HĐ gốc đã hủy + phụ lục lập lại) là bị nhân đôi.

## Chưa làm — quyết định nghiệp vụ, CHỜ TEAM

**Chiều lọc theo công ty.** Cả 2 báo cáo lọc theo công ty của **phiếu đặt hàng**, không phải của
PI/hợp đồng. Ca này: PI + hợp đồng thuộc công ty **1** (CP Công nghệ Thiết bị Tân Phát) nhưng
`PDHTN-04703` (Nguyễn Văn Thu) và `PDHTN-01994` (Văn Trọng Thế Hưng) thuộc công ty **4**
(TNHH Thiết bị Tân Phát Sài Gòn). Lọc công ty 1 ⇒ mất 2 dòng này — **đây mới là lý do trực tiếp
khách không thấy Nguyễn Văn Thu**, không phải 2 lỗi trên.

Riêng báo cáo tiến độ còn bị ép theo QUYỀN: `OrderReportProcessService::filter()` dòng 965 tự ép
`company_id = công ty của người đăng nhập` nếu người xem không có quyền *"…theo tổng công ty"* —
bỏ trống ô lọc cũng vô ích. Báo cáo luân chuyển thì bỏ trống ô Công ty là thấy đủ.

Đổi chiều lọc sẽ làm số của **mọi dòng** trên 2 báo cáo nhảy → không tự ý sửa.

## Tasks

- [x] Truy nguyên nhân, xác định 3 vấn đề tách bạch
- [x] Lỗi 2: thêm `groupBy` cho popup nhánh trong nước
- [x] Lỗi 1: thêm `getDataTNPIStock` + nhánh `else` trong `getData`
- [x] Verify có đối chứng code cũ / code mới + hồi quy
- [x] Commit `34629bd704`
- [ ] Chốt nghiệp vụ chiều lọc công ty (chờ team)
- [x] Đã lên `master` và push: `00ff575208`, `34629bd704`, `28478536f9`

## Checkpoint — 16/09/2026

Test trên DB local **`erp_prod_09_26`** bằng tinker, dựng lại trạng thái prod (thêm 4 dòng chi tiết
phụ lục 2111, hủy 4 dòng HĐ gốc, sửa dòng PI 10857 còn 6, thêm dòng PI 17159) rồi `DB::rollBack()`
— **DB không đổi**. Script trong scratchpad: `test_popup.php`, `test_process.php`, `regress_process.php`.

| Phép đo | Code cũ | Code mới |
|---|---|---|
| Popup Chi tiết, mã SND-EVB4S22NC0M | **6 dòng** (mỗi phiếu 2 lần) | **3 dòng** đúng |
| Tiến độ: PDH-07245 (Nguyễn Văn Thu) | PI=0, HĐ=0 | **PI=2, HĐ=2** |
| Tiến độ: 10 dòng phiếu lấy tồn kho khác (SP 15004, 6662, 43786) | rỗng hoàn toàn | có đủ PI/HĐ/Kho |
| Hồi quy 40 sản phẩm / 196 dòng | — | **0 dòng lệch** |

`php -l` sạch, CRLF nguyên vẹn, diff +101/−1 trên 2 file.

Bước tiếp theo: chờ team chốt chiều lọc công ty; chốt lịch merge cùng nhánh
`task_ton-kho-dang-ve`.

## Checkpoint — 16/09/2026 (bổ sung: ô ngoài cũng cộng đôi)

Khách hỏi "bên ngoài 12 mà bấm chi tiết ra có 3 phiếu" → đúng là em vá còn thiếu: mới gom ở
**popup**, chưa gom ở **khối tính ô ngoài** (`inland_employee_order`, bản màn hình + bản export).
12 = 6 × 2.

Đo qua chính service trên DB `erp_prod_09_26` (dựng lại trạng thái prod rồi rollback), mã
SND-EVB4S22NC0M: `display_employee_order` code cũ **12** → code mới **6**; cột Tồn kho
(`display_stock_order`) giữ nguyên **6**. Commit `28478536f9`.

**Phạm vi ảnh hưởng:** toàn hệ thống có **124 dòng nhu cầu** đang gắn > 1 chi tiết hợp đồng
(HĐ gốc + phụ lục, hoặc HĐ đã hủy + HĐ lập lại). Trước đây mọi dòng này đều bị cộng đôi ở cột
"Hàng đang về / KD" của báo cáo luân chuyển — nay về đúng. Số sẽ **giảm** ở những mã đó, đây là
sửa đúng chứ không phải mất dữ liệu; cần báo trước cho người dùng báo cáo.

Đã push thẳng `master` theo yêu cầu (16/09/2026) và xoá 2 nhánh task sau khi gộp.
