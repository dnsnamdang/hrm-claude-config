# Design — Fix hạch toán báo có (PBC) bị trùng dòng Có

## Triệu chứng
Sổ chi tiết tài khoản (`account_details/account-detail-book`) hiện nhiều báo có (PBC) **2 lần** (vd TPSG.PBC0426.00106), thổi phồng số dư Có.

## Chẩn đoán (đã xác minh trên prod erp_new)
- KHÔNG phải lỗi report/join — report hiện đúng dữ liệu. Là **dữ liệu hạch toán trùng**: báo có 1-detail nhưng có **2 dòng Có (type=2)** + 1 Nợ → **mất cân đối** (dòng Có thừa không có Nợ đối ứng).
- Quy mô: **69 báo có** (~2.8% — chập chờn), tiền Có ảo **~56.17 tỷ** (riêng `TPE.PBC0426.00076` = 54.27 tỷ), khoảng **16–28/04/2026** (đợt import Excel).
- Tạo qua **Excel import**: `ImportIncomeReport` → dispatch `StoreIncomeReportJob` (queue) → job tạo report + 1 detail (KHÁCH KHÔNG RÕ id 10929, account_has=22, account_dept=6) → gọi `BillIncomeReport::saveAccountsDetail()`.
- `saveAccountsDetail()`: tạo 1 Có/detail + 1 Nợ tổng. Gọi từ 3 nơi: `BillIncomeReportController::store()` (145), `update()` (192), `StoreIncomeReportJob::handle()` (99).
- **2 lỗ hổng cùng họ:**
  1. Job không bọc transaction + không guard chống post-trùng → dưới race/queue sinh dòng Có thừa.
  2. `update()` gọi `saveAccountsDetail()` **không xóa hạch toán cũ** → mỗi lần sửa **cộng dồn** thêm 1 bộ Nợ/Có (bug chắc chắn).
- *(Cơ chế double chính xác ở đường job chưa pin 100%, nhưng fix idempotent vô hiệu hóa bất kể nguyên nhân.)*
- An toàn xóa-tạo-lại: chỉ `account_detail_refs.account_detail_id` trỏ tới `account_details`, **không FK cứng** từ bảng khác.

## Hướng fix (đã chốt với user)
**A. Idempotent** — đầu `BillIncomeReport::saveAccountsDetail()`, xóa toàn bộ `account_details` cũ của chính báo có này (theo `invoiceable_id` + `invoiceable_type = self::class`) + `account_detail_refs` của chúng, RỒI mới tạo lại Nợ/Có như logic cũ.
→ Gọi 1 hay N lần đều ra **đúng 1 bộ** hạch toán. Fix cả đường job (race) lẫn đường `update()` (cộng dồn).

**B. Atomic** — bọc `StoreIncomeReportJob::handle()` trong `DB::transaction` (store/update ở controller đã có transaction sẵn).

**C. (optional, để pha sau)** — `StoreIncomeReportJob implements ShouldBeUnique` chống worker xử lý job trùng.

## Phạm vi file
- `app/Model/IncomeExpenditure/BillIncomeReport.php` — thêm bước xóa-cũ ở đầu `saveAccountsDetail()`.
- `app/Jobs/StoreIncomeReportJob.php` — bọc `handle()` trong transaction (+ optional ShouldBeUnique).

## Không làm trong scope này
- Sửa 69 bản ghi cũ → đã có script riêng `fix-data-prod.sql` (chạy tay sau khi kế toán duyệt + backup).
- `saveAccountsDetail()` của model khác (BillIncome, BillPayment...) — không đụng (chỉ BillIncomeReport).

## Rủi ro / lưu ý
- `saveAccountsDetail()` gọi từ store/update/job — sửa nó tác động cả 3 (đều theo hướng đúng hơn). Đã xác nhận với user.
- Idempotent xóa-tạo-lại đổi `id` account_details mỗi lần update — chấp nhận được (không bảng nào ngoài refs tham chiếu).

## Branch
`sync_quotation` (theo các fix khác đang cùng nhánh) — xác nhận lại khi thực thi.
