# Design (tóm tắt) — Phiếu chi tiền (ERP → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Ngày: 2026-08-19
> **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-08-19-finance-bill-payment-design.md`
> Feature tiền đề: `.plans/gop-db/finance-bill-payment-request/` (Đề nghị thanh toán — đã xong)
> Feature soi gương: `.plans/gop-db/finance-bill-income/` (Phiếu thu tiền — đã xong)

---

## Mục tiêu

Port màn ERP `admin/income-expenditure/bill_payments` (**Phiếu chi tiền**) sang HRM, phân hệ
**Tài chính**, route `/finance/bill-payments`. Đây là mảnh cuối của cặp *Đề nghị thanh toán → Phiếu
chi*: màn Đề nghị thanh toán đã port và đang **dừng ở trạng thái 6 "Chờ tạo phiếu chi"**; 3 trạng
thái 7/8/9 đã khai sẵn kèm ghi chú *"ngoài phạm vi, chỉ hiển thị"* — feature này kích hoạt chúng.

## Scope

**Trong**: 1 màn danh sách duy nhất · chi tiết · tạo/sửa/xóa nháp · gửi duyệt · **duyệt kèm ghi bút
toán sổ cái** · hủy · in 2 liên (3 mẫu ERP) · xuất Excel 1 phiếu · thông báo chuông · 2 lối tạo
phiếu · **đủ 5 loại chi** gồm loại 4 "Chi thu nhập cho nhân viên".

**Ngoài**: màn Ủy nhiệm chi · lịch sử thay đổi · import Excel · xuất Excel cả danh sách · không đụng
repo ERP · không migration · không `mysql2`.

## Quyết định lớn (user chốt 2026-08-19)

| # | Quyết định |
| --- | --- |
| 1 | **Làm giống ERP 1:1** — đủ 5 loại chi, làm 1 lượt không chia phase |
| 2 | Danh sách **gộp về 1 màn duy nhất**, bỏ hẳn `?mode=` — giống Phiếu thu. An toàn: đã kiểm dữ liệu thật, **5/5 role có quyền duyệt đều kèm quyền "Xem tất cả phiếu chi của…"** |
| 3 | **Cả 2 lối tạo phiếu**, kể cả bổ sung nút "Tạo phiếu chi" vào màn Chi tiết Đề nghị thanh toán đã nghiệm thu |
| 4 | Ủy nhiệm chi **ngoài scope**, feature riêng sau |
| 5 | **Giữ nguyên quyền ERP, thêm bản mới sang HRM**: 4 quyền guard `api` id 1503–1506, nguyên văn tên ERP. Tạo/sửa dùng lại `Kế toán thanh toán` id 1152. Không thêm tầng phòng ban–bộ phận |
| 6 | Dùng chung 3 bảng ERP, không migration |

## Hai nhánh nghiệp vụ tách biệt

**Nhánh A — loại 1 · 2 · 6 · 12** (1.186 phiếu, lập từ Đề nghị thanh toán):
Đang tạo → Chờ chi tiền → **Thủ quỹ duyệt** → Đã duyệt (ghi sổ cái) | Hủy.
Đồng bộ ngược sang đề nghị: 7 → 8 → 9.

**Nhánh B — loại 4 "Chi thu nhập cho nhân viên"** (116 phiếu, KHÔNG qua đề nghị):
chọn Phòng ban → hút số liệu 6 khoản thu nhập từ sổ cái → Chờ **KT trưởng** duyệt (5) →
Chờ chi tiền (2) → **Thủ quỹ** duyệt → Đã duyệt (ghi sổ cái **kiểu gộp theo `identify_number`**).

## Điểm kỹ thuật chính

- BE `Modules/Finance`: `Entities/BillPayment/*` · 6 service (đọc · lookup nhân viên · ghi · duyệt ·
  **2 service sổ cái tách riêng** cho 2 nhánh) · `Transformers/BillPaymentResource/*` ·
  routes `/v1/finance/bill-payments`.
- Tái dùng từ Phiếu thu: `AccountDetailEntry`, `AccountDetailRef`, morphMap 10 cặp hợp đồng,
  trait `ChecksEmployeePermission`, pattern `generateCode()` có `lockForUpdate()`.
- **Phải port thêm** (nhánh B chưa có bên HRM): `createDataSaveDept()` + `saveAccountDetail()` +
  `getDataAdPaymentEmployee()` — 3 helper nằm trong model `AccountDetail` khổng lồ của ERP.
- **Morph thêm 4 cặp**: `ProductExport` · `DeliveryTripAccounting` · `OtherDeliveryTripAccounting` ·
  `DeclareDebtBeginning`. Ghi **tên class ERP đầy đủ** vào sổ cái, không dùng alias HRM.
- **Khác ERP có chủ ý**: ERP nhét gửi duyệt/duyệt/hủy vào `PUT /update` bằng cách đổi `status` trong
  payload → HRM tách `POST /{id}/submit` · `/approve` · `/cancel`.
- **Đổi async → sync**: ERP đẩy ghi sổ nhánh B vào job `ShouldQueue` (nằm ngoài transaction) → HRM
  gọi thẳng service trong cùng transaction, hỏng thì rollback cả trạng thái lẫn bút toán.
- FE: `columnScreenKey` = `localStorageKey` = `finance_bill_payments`, cờ quyền fail-closed khởi tạo
  `false`. Menu Tài chính đã có sẵn `{ label: 'Phiếu chi' }` chưa gắn link → chỉ cần gắn link.
- In: 3 mẫu `report_templates` **211 / 217 / 236 đã có sẵn trong DB gộp**, dùng lại nguyên.

## 7 lỗi ERP mà HRM chủ động sửa

1. `canEdit()`/`canDelete()` chỉ kiểm `status == 1` — ai gọi URL cũng sửa/xóa được phiếu nháp của
   người khác → siết theo người lập + quyền, trả **423** khi đã khóa.
2. `update()` khai nhận `BillPaymentUpdateRequest` nhưng thực tế nhận `BillPaymentStoreRequest` →
   luật của `UpdateRequest` **chưa bao giờ chạy**.
3. `validatePaymentMoney()` chỉ chạy khi `status != 4`, mà 4 là *Hủy* còn duyệt là 3 → **ERP không
   hề kiểm trần số tiền lúc duyệt**.
4. Duyệt 2 lần ghi trùng bút toán → `lockForUpdate()` + kiểm lại status, trả **409**.
5. `catch (Exception)` nuốt `ValidationException` → rethrow để FE nhận 422 chuẩn.
6. hook `created` gọi `save()` lần 2 → gán cấp tổ chức ngay trong `create()`.
7. `generateCode()` không khóa → bọc transaction + `lockForUpdate()`.
8. Nhánh B ghi `accounting_approved_id` = **người lập** (lúc gửi duyệt) thay vì người duyệt → HRM ghi
   tại đúng bước KT trưởng bấm duyệt.

## Code chết của ERP — KHÔNG port

`syncDetails()` truyền `payment_market_cost`, `payment_extra`, `cost_debt_id`,
`type_payment_employee` vào `BillPaymentDetail::create()` nhưng **cả 4 cột đều không tồn tại trong
DB** — chỉ bị `$fillable` lọc âm thầm. Kéo theo `saveCommissionEmployee()` và 4 quan hệ
`diff_employees()` / `commission_months()` / `commission_quarters()` /
`commission_bonus_quarters()` là **code chết, gọi vào là nổ SQL**. Không có nơi nào gọi chúng.

## Rủi ro cần biết

Ghi bút toán vào `account_details` / `account_detail_refs` — **sổ cái thật dùng chung với cổng ERP,
sai hoặc trùng là lệch số liệu kế toán không hoàn tác được**. Nhánh B nguy hiểm hơn nhánh A vì dùng
cơ chế gộp theo `identify_number` thay vì ghi thẳng từng dòng.

Kiểm chứng: tách hàm **thuần** `buildEntries()` → unit test không cần DB; rồi lấy 5 phiếu thật mỗi
loại chi, dựng lại bút toán bằng code HRM và **diff từng trường** với dữ liệu cổng ERP đã ghi.

**Giới hạn**: bảng phân bổ phiếu xuất hàng **0 dòng** và trạng thái 5 "Chờ KT trưởng duyệt" **0
dòng** → không chạy thật được, phải test bằng phiếu tự tạo / đọc code đối chiếu.

## Điểm còn treo, cần user chốt

**Lý do hủy phiếu**: ERP bắt buộc nhập `note` khi hủy nhưng bảng `bill_payments` **không có cột
`note`** — nhập xong không lưu ở đâu. Spec mặc định: vẫn bắt nhập lý do, đưa vào **nội dung thông
báo chuông**, không lưu DB (giữ hành vi ERP, không cần migration). Muốn lưu thật phải thêm cột.

## Dữ liệu thật (DB gộp, đếm 2026-08-19)

`bill_payments` **1.302** (Đã duyệt 1.294 · Hủy 5 · Chờ chi tiền 2 · Đang tạo 1 · Chờ KT trưởng
duyệt 0) · `bill_payment_details` **3.307** · `bill_payment_detail_product_export_requests` **0**.

Loại chi: `1` 708 · `6` 278 · `2` 137 · `4` 116 · `12` 63.
