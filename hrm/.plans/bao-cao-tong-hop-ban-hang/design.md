# Báo cáo tổng hợp bán hàng — port ERP → HRM

> Brainstorm 16/11/2026 với @nguyentrancu97. Trạng thái: ĐÃ DUYỆT — code xong, chờ gộp/push.

## 1. Mục đích

Kế toán xem tổng hợp bán hàng theo từng mặt hàng **kèm giá vốn và lãi lỗ** trên HRM, thay cho màn ERP
`report.summary_sale?type=all` (menu Kế toán › "Báo cáo tổng hợp bán hàng"). Đây là một bước trong lộ trình
chuyển các báo cáo ERP sang HRM.

## 2. Hiện trạng

| | ERP | HRM |
|---|---|---|
| Bán hàng theo từng mặt hàng (`type` ≠ all) | `ReportController@summarySale*` + `App\Services\Reports\SummarySaleReportService` | **ĐÃ PORT**: `/sale/sale-by-product-report`, `Modules/Finance/Services/SaleByProductReportService` (+ `SaleByProductReportPrintService`, `SaleByProductReportController`, route `Modules/Finance/Routes/api.php:1646`) |
| **Tổng hợp bán hàng (`type=all`)** | Cùng controller/service/blade, chỉ khác cờ `type == 'all'` | **CHƯA CÓ**. `components/subsystem-menu/finance.js:400` đã có mục `{ label: 'Báo cáo tổng hợp bán hàng' }` chưa gắn link |

Khác biệt `type=all` so với bản theo mặt hàng ở ERP (đã đối chiếu code):
- Thêm 3 cột ở bảng chính, dòng tổng, popup chi tiết, bản in, Excel: **Đơn giá vốn · Thành tiền vốn · Lãi lỗ**
  (thứ tự cột ERP: … Thành tiền net · **Đơn giá vốn · Thành tiền vốn** · Chênh lệch · **Lãi lỗ** …).
- Mã quyền `accounting.bao_cao_tong_hop_ban_hang.view`, chỉ 2 mức: Công ty (3) / Tổng công ty (4). Không có quyền
  → ERP trả `not_found`.
- Tên màn / tên file: "Báo cáo tổng hợp bán hàng" / `bao_cao_tong_hop_ban_hang.xlsx`.

Công thức ERP (`SummarySaleReportService`):
- Mỗi nhánh nguồn trả `export_price_amount` (tiền vốn); nhánh nhập trả lại = 0.
  - Xuất kho: `ped.export_price * ped.export_qty` (`export_price` là giá vốn / ĐVT cơ bản).
  - Bán hàng mượn: `bsp.export_price * bsp.qty`, nhưng dòng chi tiết lại lấy `bsp.export_price / bsp.unit_coefficient`
    làm đơn giá → **nghi lệch hệ số ĐVT** (xem §6).
- Gộp theo mặt hàng (dòng ~455):
  - Đơn giá vốn = Σ tiền vốn / Σ SL bán
  - Thành tiền vốn = Đơn giá vốn × SL thực tế
  - Lãi lỗ = (Σ tiền bán phân bổ − Σ tiền vốn) / Σ SL bán × SL thực tế
- Popup chi tiết từng dòng: Lãi lỗ = (đơn giá phân bổ/ĐVT − giá vốn) × SL.

## 3. Quyết định đã chốt (user, 16/11/2026)

1. **Dùng chung lõi số liệu** với màn "Bán hàng theo từng mặt hàng": KHÔNG nhân bản service. Màn tổng hợp là màn
   riêng (route/trang riêng) nhưng gọi cùng `SaleByProductReportService`, bật thêm 3 cột vốn/lãi lỗ và áp mã quyền
   tổng hợp. Sửa số liệu 1 chỗ được cả 2 màn.
2. **Menu Kế toán** như ERP — gắn link vào mục có sẵn `finance.js:400` (nhóm "Báo cáo bán hàng", hub
   "Kế toán bán hàng"). Không thêm vào menu Bán hàng.
3. **Theo y màn theo mặt hàng ở các điểm đã chốt khác ERP**: cộng HĐ HRM (`hrm_contracts`, xuất loại 21 + bán mượn
   HĐ HRM); bỏ cột Thời gian bảo hành + ĐM đàm phán giá; popup chi tiết có NVKD, lọc Số HĐ / KH / NVKD, In, Excel;
   tồn đầu/cuối kỳ như màn mặt hàng. Hai màn chỉ khác: 3 cột vốn/lãi lỗ + mã quyền + tiêu đề/tên file.
4. **Excel như màn mặt hàng** — tải trực tiếp, KHÔNG làm job gửi mail như ERP.
5. **Quyền giữ y ERP**: dùng lại mã `accounting.bao_cao_tong_hop_ban_hang.view` trong
   `app/Support/Permissions/Catalog/accounting.php`, thêm `'hrm'` vào `platforms`, `scopes` giữ `[3, 4]`.
   - Tổng công ty: thấy mọi công ty, được chọn ô Công ty.
   - Công ty: chỉ công ty mình (theo cách màn mặt hàng đang xác định "công ty mình" ở mức `company`).
   - Không có quyền: ẩn mục menu; mọi API của màn trả **403** (KHÔNG rơi về "chỉ phiếu mình tạo" như màn mặt hàng).
   - Bộ lọc Phòng ban / Bộ phận / NV vẫn hiện ở cả 2 mức (ERP partial hiện cho is_company / is_all_company).
6. **Giá vốn là dữ liệu nhạy cảm**: 3 cột vốn/lãi lỗ CHỈ trả về khi request đi qua màn tổng hợp (đã gác mã quyền
   tổng hợp). API màn mặt hàng TUYỆT ĐỐI không trả các trường này (kể cả `null` là được, không được trả số).
7. **Lỗi ERP phát hiện khi đối chiếu → sửa đúng ở HRM + vá ERP** (develop_02), ghi vào §6, đối chiếu tới 0 lệch như
   các báo cáo thưởng vừa port.

## 4. Mục tiêu / Không làm / Thất bại

- **Mục tiêu**: số liệu màn tổng hợp HRM = ERP (sau vá) cho cùng kỳ/bộ lọc, CỘNG phần HĐ HRM; bản in + Excel có đủ cột.
- **Không làm**: job gửi mail; cột bảo hành / ĐM đàm phán; mức phạm vi Phòng ban/Bộ phận; đổi số liệu màn mặt hàng
  (ngoài phần vá lỗi chung nếu §6 tìm ra lỗi ở lõi dùng chung — khi đó cả 2 màn đổi số, phải ghi rõ).
- **Thất bại dù chạy được**: lộ giá vốn ở màn mặt hàng; người không có quyền tổng hợp xem được dữ liệu; 2 màn lệch
  SL/tiền bán cho cùng bộ lọc.

## 5. Phần để builder quyết

- Cách truyền "chế độ" vào service (tham số constructor / phương thức `forSummary()` / biến thể mã quyền) — miễn mã
  quyền và cờ hiện cột vốn đi chung, không thể bật cột vốn bằng tham số request của màn mặt hàng.
- Route BE: prefix riêng (vd `finance/sale-summary-report/*`) hay dùng chung controller với tham số route cố định.
- FE: trang mới (vd `pages/finance/sale-summary-report/index.vue`) tái dùng components của
  `pages/sale/sale-by-product-report/components/*` (thêm prop bật cột vốn) — không copy component.
- Cấu hình cột hiển thị / In theo cột: theo khuôn màn mặt hàng, thêm 3 cột mới vào danh sách cột.

### 5b. Chốt thêm sau vòng kiểm (Claude tự quyết — user xem lại)

- **Nguồn giá vốn cho HĐ HRM**: xuất loại 21 nằm cùng bảng `product_export_details` (`ped.export_price`), bán mượn
  HĐ HRM cùng bảng `borrow_sell_products` (`bsp.export_price`) → dùng y công thức nhánh ERP, không cần truy vấn mới.
  Nhánh nhập trả lại: tiền vốn = 0 như ERP. Ô = 0 hiển thị `-` như các cột tiền khác của màn mặt hàng.
- **Công thức gộp**: theo đúng §2 (ERP). SL bán / tiền bán phân bổ / SL thực tế lấy từ lõi dùng chung (đã khớp ERP
  ở màn mặt hàng); màn tổng hợp chỉ cộng thêm Σ tiền vốn theo cùng cách gộp.
- **Lỗi hệ số ĐVT hàng mượn (§6)**: builder xác định ngữ nghĩa `bsp.export_price` / `bsp.qty` (theo ĐVT bán hay ĐVT
  cơ bản) từ chỗ ghi giá trị trong code ERP + mẫu dữ liệu dòng có `unit_coefficient ≠ 1`, ghi kết luận + bằng chứng
  vào §6, rồi sửa phía sai. Nếu không kết luận được → dừng, hỏi user.
- **Đối chiếu**: chạy trên DB local `erp_hrm_check` (chỉ SELECT), gọi service ERP qua tinker ở worktree ERP và API
  HRM với cùng bộ lọc; kỳ 05/2026, cả năm 2025, cả năm 2026, phạm vi tổng công ty + 1 công ty. Kết quả vào
  `doi-chieu.md`. So khớp loại trừ phần HĐ HRM (ERP không có).
- **403**: áp cho mọi endpoint dưới route của màn tổng hợp (danh sách, tùy chọn bộ lọc, popup chi tiết, in, Excel cả
  2 cấp). Danh mục tra cứu dùng chung (KH, NV, hàng hoá…) KHÔNG gác thêm.
- **Cấp quyền**: chỉ khai Catalog + `catalog-sync`; cấp cho vai trò do vận hành làm ở `/admin/roles`, không seed.

## 6. Lỗi ERP phát hiện (điền khi đối chiếu)

- [x] ~~Nghi vấn hàng mượn lệch hệ số ĐVT~~ → **KHÔNG phải lỗi** (16/11/2026). `bsp.export_price` là giá vốn theo
  **ĐVT bán**: `BorrowSellsController.php:240-252` ghi `Σ(qty_bán × unit_coefficient × giá vốn ĐVT cơ bản) / Σqty_bán`.
  Nên tiền vốn = `export_price × qty` đúng; đơn giá chia hệ số chỉ là quy về ĐVT cơ bản (cùng kiểu `allocated_price`).
  Dữ liệu `erp_hrm_check`: bsp 22 hệ số 24, export_price 1.187.376 = 24 × 49.474 (giá vốn dòng xuất mượn gốc);
  bsp 10 hệ số 100, 330.187 = 100 × 3.301,87.
- [x] Đối chiếu 05/2026, 2025, 2026 × {tổng công ty, công ty 1}: **0 lệch** trên 6 cột (doi-chieu.md) → không vá ERP.

## 7. Triển khai

- `php artisan permission:catalog-sync` (mã đã có, chỉ thêm platform `hrm`), cấp quyền ở `/admin/roles`.
- Nếu vá ERP: push develop_02 sau khi HRM build sync.
- Đối chiếu số: ghi `doi-chieu.md` cùng thư mục.
