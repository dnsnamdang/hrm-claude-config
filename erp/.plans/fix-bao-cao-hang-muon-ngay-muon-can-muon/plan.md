# Fix: Báo cáo hàng mượn — Ngày mượn lấy Ngày cần mượn của phiếu YCXH

@junfoke · Repo `TanPhatDev` (bản B) · nhánh `master`

## Bối cảnh / Bug

Ở màn **Danh sách hàng mượn** và **Hàng mượn hết hạn** (cả web, Excel, In), cột **Ngày mượn**
đang lấy từ `product_export_requests.borrow_date` = **ngày xuất kho thực tế**
(`ProductExport.php:1865` set `borrow_date = date('Y-m-d')` lúc xuất).

→ Hệ quả: Ngày mượn hiển thị = ngày xuất thực tế (vd PYCXH-35696 hiện **27/08/2026**),
có thể **lớn hơn Ngày hẹn trả** → vô lý (ảnh chụp: cả 3 dòng đều 27/08 > ngày hẹn trả).

**Yêu cầu:** Cột **Ngày mượn** ở báo cáo hàng mượn phải **luôn = "Ngày cần mượn"**
(`expected_borrow_date`) nhập trên phiếu YCXH loại **Xuất mượn** — bất biến, không phụ thuộc
ngày xuất kho hay phiếu gia hạn.

Ví dụ đích: PYCXH-35696 (Đỗ Đăng Hiếu) phải hiện Ngày mượn = **28/07/2026**.

## Root cause (đã điều tra)

- `expected_borrow_date` = Ngày cần mượn trên form (required), bất biến — ĐÚNG cái cần hiển thị.
- `borrow_date` chỉ được ghi 1 lần lúc xuất kho (`ProductExport.php:1865`), = ngày xuất → SAI ngữ nghĩa "Ngày mượn".
- Phiếu gia hạn (`borrow_extend_requests`) khi duyệt chỉ đổi `return_date`, KHÔNG đụng `borrow_date`.
- Fix ở **tầng hiển thị báo cáo**: đổi nguồn cột từ `borrow_date` → `expected_borrow_date`
  (COALESCE fallback về borrow_date để an toàn với bản ghi cũ thiếu expected_borrow_date).

## Tasks

- [x] BE1: `WarehouseInfosController::borrowSearchData()` (dòng 793) — datatable AJAX của cả 4 màn
  (borrowIndex / expiringBorrow / accountingExpiring / accountingExpired): đổi select
  `per.borrow_date` → `DB::raw('COALESCE(per.expected_borrow_date, per.borrow_date) as borrow_date')`.
- [x] BE2: `BorrowIndexReportService::getData()` (dòng 226) — nguồn cho Excel + In: đổi tương tự.
  (getTable/getTable4Print render `$product['borrow_date']` giữ nguyên, tự nhận giá trị mới nhờ alias.)
- [x] Verify: `php -l` 2 file sạch; CRLF giữ nguyên; diff đúng 2 dòng. **CHƯA test browser + CHƯA commit.**
- [x] Verify data PROD (user chạy SQL): PYCXH-35696 `expected_borrow_date=2026-07-28` (đúng),
  `borrow_date=2026-08-27 > return_date=2026-08-04` (bug gốc). Toàn bộ 72/72 phiếu đang mượn
  ĐỀU có expected_borrow_date (thiếu=0) ⇒ COALESCE fallback không bao giờ chạy, an toàn 100%.
- [ ] User verify browser + tự branch/commit (còn lại).

## Đồng bộ cảnh báo chuông (user duyệt sửa 2026-08-28)

- [x] BE3: `HomeController::...` (dòng 2353) — data nuôi cảnh báo "Hàng mượn hết hạn" (có hiển thị):
  đổi `per.borrow_date` → `DB::raw('COALESCE(per.expected_borrow_date, per.borrow_date) as borrow_date')`.
- [x] BE4: `CheckDueConfigs.php` (dòng 49) — middleware chặn route. `borrow_date` ở đây **không dùng**
  (query kết thúc `->pluck('per_detail.product_id')`), sửa để đồng bộ pattern — **no-op hành vi**.
  Dùng `\DB::raw(...)` theo convention file.

## Checkpoint

### Checkpoint — 2026-08-28
Vừa hoàn thành: BE1 + BE2 (đổi 2 query lấy expected_borrow_date), php -l sạch, CRLF giữ nguyên.
Đang làm dở: —
Bước tiếp theo: user test browser PYCXH-35696 (28/07/2026) rồi tự branch/commit.
Blocked: chờ user quyết có sửa luôn 2 chỗ cảnh báo chuông (CheckDueConfigs / HomeController) không.
