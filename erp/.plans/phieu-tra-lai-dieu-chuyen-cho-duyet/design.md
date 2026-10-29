# Phiếu YC nhập trả lại điều chuyển nội bộ tự sinh → vào thẳng "Chờ duyệt"

**Người phụ trách:** @namdangit
**Nhánh:** `gop_db` (ERP TanPhatDev)
**Ngày:** 2026-10-05

## Bối cảnh / Sự cố

Luồng điều chuyển kho nội bộ: phiếu xuất `XUAT_DIEU_KHO_NOI_BO=6` → phiếu nhập
`NHAP_DIEU_CHUYEN_KHO_NOI_BO=6`. Khi **SL thực nhập < SL xuất**, hệ thống tự sinh phiếu
YC nhập **trả lại điều chuyển** `NHAP_TRA_LAI_DIEU_CHUYEN=17` cho phần chênh lệch.

Repro: phiếu nhập `product_imports/14632` (từ PXK điều chuyển `PYCXH-41660`) thực nhập ít hơn
→ hệ thống ĐÃ tự sinh phiếu `PYCNH-14530`. **Phiếu được sinh đúng**, nhưng:

1. Sinh ở trạng thái **"Đang tạo" (`DANG_TAO=3`)**.
2. Màn danh sách `/product_import_requests/all` **ẩn phiếu "Đang tạo" với mọi người trừ người tạo**
   (`searchByFilter` type=all, `ProductImportRequest.php:1320-1326`: với mọi phạm vi quyền
   theo công ty/phòng/bộ phận, chỉ hiện phiếu `status != DANG_TAO` HOẶC `DANG_TAO` do chính
   `auth()->user()->id` tạo).

→ Người cần duyệt không thấy phiếu đâu để xử lý.

## Nguyên nhân gốc (1 gốc, 2 triệu chứng)

Hàm `ProductImport::createReturnImportRequest()` hard-code `status = 3` (DANG_TAO) khi tạo phiếu
tự sinh. Phiếu "Đang tạo" bị màn list cố ý ẩn → vừa sai trạng thái vừa không hiện ra.
Fix status → CHO_DUYET (2) giải quyết cả 2 triệu chứng.

## Giải pháp (user chốt: "sửa chung cả 2 luồng, sửa luôn phiếu 14530")

### A. Sửa code — áp cho CẢ 2 luồng gọi `createReturnImportRequest()`

`createReturnImportRequest()` là điểm tạo phiếu DUY NHẤT, được 2 nơi gọi:

1. `ProductImport::checkAndCreateReturnImportRequest()` — khi SL thực nhập < SL xuất (luồng chính của sự cố).
2. `ProductImportRequest::cancel()` (dòng ~1660) — khi HỦY đề nghị nhập kho điều chuyển nội bộ
   thì tự sinh phiếu hoàn trả toàn bộ SL.

Sửa 1 chỗ trong `createReturnImportRequest()`: `status = 3` → `status = ProductImportRequest::CHO_DUYET` (2)
→ cả 2 luồng cùng vào "Chờ duyệt".

**File:** `app/Model/Warehouse/ProductImport.php` (hàm `createReturnImportRequest`, ~dòng 1864).

### B. Sửa dữ liệu — phiếu CŨ đã kẹt

Method `UpdateDB::fixReturnTransferRequestStatusChoDuyet_20261005($dryRun=true)`:
nâng các phiếu `type=NHAP_TRA_LAI_DIEU_CHUYEN(17) AND status=DANG_TAO(3) AND note LIKE 'Tự sinh%'`
lên `CHO_DUYET(2)`. Quét thực tế: đúng **1 phiếu** = `PYCNH-14530`.

## Quyết định đã chốt

- Phiếu hoàn trả điều chuyển nội bộ tự sinh LUÔN vào "Chờ duyệt", không bao giờ "Đang tạo".
- Không đổi logic ẩn phiếu "Đang tạo" ở màn list (đúng nghiệp vụ cho phiếu nháp của người khác).
- Fix ở điểm tạo phiếu chung (`createReturnImportRequest`), không rải ở từng caller.

## Verify

- `php -l` sạch cả `ProductImport.php` và `UpdateDB.php`.
- Dry-run + ghi thật đều báo "Quet=1 ... Nang len Cho duyet=1".
- Đọc lại: `PYCNH-14530` status=2 (CHO_DUYET). DB: `hrm_erp_test` (dev-erp.dnsmedia.vn).

## Chưa làm

- Chưa commit/push (chưa có yêu cầu).
