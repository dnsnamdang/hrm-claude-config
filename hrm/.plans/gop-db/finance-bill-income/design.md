# Design (tóm tắt) — Phiếu thu tiền (ERP → HRM)

> Phụ trách: @khoipv · Nhánh: `gop_db` (cả 2 repo) · Ngày: 2026-08-18
> **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-08-18-finance-bill-income-design.md`
> Feature tiền đề: `.plans/gop-db/finance-bill-income-request/` (Đề nghị thu tiền — đã xong,
> chính nó ghi "Màn Phiếu thu sẽ port sang HRM ở feature sau")

---

## Mục tiêu

Port màn ERP `admin/income-expenditure/bill_incomes` (**Phiếu thu tiền**) sang HRM, phân hệ
**Tài chính**, route `/finance/bill-incomes`.

Phiếu thu là chứng từ kế toán lập **từ một Phiếu đề nghị thu tiền** đang chờ duyệt. Thủ quỹ duyệt →
hệ thống **ghi bút toán vào sổ cái** (`account_details` + `account_detail_refs`) và cập nhật số tiền
thực thu ngược về phiếu đề nghị. Vòng đời: Đang tạo → Chờ duyệt → Đã duyệt | Hủy.

## Scope

**Trong**: danh sách 1 màn duy nhất (gộp 4 chế độ — xem quyết định #2) · chi tiết · tạo/sửa/xóa nháp ·
gửi duyệt · **duyệt kèm hạch toán sổ cái** · hủy · in 2 liên (4 mẫu ERP) · xuất Excel 1 phiếu ·
thông báo chuông · 2 lối tạo phiếu (từ màn Đề nghị thu tiền + Thêm mới ở màn danh sách).

**Ngoài**: không đụng repo ERP · không migration cấu trúc bảng · không `mysql2` · màn Phiếu báo có ·
lịch sử thay đổi · import Excel · xuất Excel cả danh sách (ERP không có).

## Quyết định lớn (user chốt 2026-08-18)

| # | Quyết định |
| --- | --- |
| 1 | Phạm vi **đầy đủ 1:1 như ERP**, gồm cả hạch toán sổ cái |
| 2 | ~~Đủ 4 chế độ danh sách — 1 file `index.vue` + `?mode=my\|all\|pending\|approved`~~ ⚠️ **THAY THẾ 2026-08-18 (user đổi ý cùng ngày)**: gộp về **1 màn duy nhất**, 1 lối vào menu, **bỏ hẳn `?mode=`** cả FE lẫn BE. Phạm vi dữ liệu theo QUYỀN (logic nhánh `all` cũ, `applyScope()`); "Của tôi" → ô lọc Người lập, "Chờ duyệt"/"Đã duyệt" → ô lọc Trạng thái. An toàn: đã kiểm dữ liệu thật — **cả 45 thủ quỹ đều có sẵn quyền "Xem tất cả phiếu thu"** nên bỏ màn Chờ duyệt riêng không làm ai mất lối tới phiếu cần duyệt |
| 3 | **Cả 2 lối tạo phiếu**, kể cả bổ sung nút "Tạo phiếu thu" vào màn Chi tiết Đề nghị thu tiền đã xong |
| 4 | Giữ **nguyên cơ chế quyền ERP** (tổng cty / công ty / chỉ mình), không thêm tầng phòng ban–bộ phận |
| 5 | Thêm 3 quyền guard `api` id **1500–1502** vào `PermissionsTableSeeder`, giữ nguyên văn tên ERP |
| 6 | **Port đủ cả 2 nhánh code chết** của ERP (phân bổ phiếu xuất hàng · thu dư nợ đầu kỳ), dù DB 0 dòng |
| 7 | Dùng chung 3 bảng ERP `bill_incomes` / `bill_income_details` / `bill_income_detail_product_export_requests` |
| 8 | UI bám base màn Danh mục khách hàng, copy khuôn từ `pages/finance/bill-income-requests/index.vue` |
| 9 | **Đồng bộ ngược trạng thái phiếu đề nghị: GIỮ NGUYÊN LOGIC ERP** (user chốt 2026-08-19, sau khi rà soát). Không mở ngõ cụt "hủy phiếu thu → lập lại phiếu khác", không trả trạng thái đề nghị khi xóa phiếu thu nháp, không đổi trạng thái đề nghị lúc lưu nháp. Chi tiết + 3 điểm hở đã biết: xem mục "Đồng bộ ngược" bên dưới |

## Điểm kỹ thuật chính

- BE `Modules/Finance`: `Entities/BillIncome/*` · 3 service (`BillIncomeService` đọc·lọc,
  `BillIncomeWriteService` ghi, **`BillIncomeAccountingService` tách riêng phần ghi sổ cái**) ·
  `Transformers/BillIncomeResource/*` · routes `/v1/finance/bill-incomes`.
- Tạo mới entity `Accounting/AccountDetailRef` (`AccountDetail` đã có sẵn).
- **Khác ERP có chủ ý**: ERP nhét duyệt/hủy vào `PUT /update` bằng cách đổi `status` trong payload;
  HRM tách `POST /{id}/approve` và `POST /{id}/cancel`.
- **Không gắn middleware `checkPermission`** — dùng trait `ChecksEmployeePermission` (query thẳng
  pivot, so theo `name` không lọc guard) vì middleware chung bỏ sót role gán từ ERP.
- Sổ cái ghi **tên class ERP đầy đủ** cho `invoiceable_type` / `contractable_type`, KHÔNG dùng alias
  morphMap của HRM — nếu không cổng ERP không resolve được.
- Morph hợp đồng: tái dùng nguyên bộ 9 entity đã khai ở feature Đề nghị thu tiền; nguồn hợp đồng bán
  `firm_contracts` → `hrm_contracts`.
- FE: `columnScreenKey: 'finance_bill_incomes'`, `localStorageKey: 'finance_bill_incomes'`
  (bỏ hậu tố mode 2026-08-18), KHÔNG còn watcher `$route.fullPath` (chỉ còn 1 route), cờ quyền
  fail-closed khởi tạo `false`.
- Menu Tài chính: đúng 1 lối vào `{ label: 'Phiếu thu', link: '/finance/bill-incomes' }` ở nhóm
  *Thanh toán tiền mặt* (3 mục `?mode=` cũ đã xóa 2026-08-18 theo quyết định #2).

## Đồng bộ ngược trạng thái sang Phiếu đề nghị thu tiền

Đã rà soát 2026-08-19 — **đã có đủ, khớp 1:1 ERP** (`BillIncomeController::update()` :202-224 của repo ERP):

| Phiếu thu chuyển sang | Code HRM | Phiếu đề nghị được cập nhật |
| --- | --- | --- |
| Chờ duyệt (2) | `BillIncomeWriteService::markRequestCreatedAndNotify()` :63-74 (gọi từ cả `store` và `update`) | `status = 3` Đã tạo phiếu thu · `approved_id` = người lập · bắn chuông thủ quỹ |
| Đã duyệt (3) | `BillIncomeApprovalService::approve()` :75-84 | `status = 4` Đã hạch toán · `syncIncomeMoneyReal()` ghi `income_money_real(_exchange)` xuống `bill_income_request_details` (khớp 5 khóa objectable/customer/employee/supplier) |
| Hủy (4) | `BillIncomeApprovalService::cancel()` :123-124 | `status = 5` Hủy |

Kiểm chứng dữ liệu thật (2.347 phiếu, 0 cặp lệch): `2→3` 8 dòng · `3→4` 2.304 dòng · `4→5` 35 dòng.

**3 điểm hở kế thừa từ ERP — user chốt GIỮ NGUYÊN, KHÔNG sửa:**

1. Xóa phiếu thu không trả trạng thái đề nghị về. HRM vẫn an toàn vì `canDelete()` chỉ cho xóa phiếu
   nháp (status 1) mà nháp chưa hề đụng phiếu đề nghị. Di sản ERP: DB còn **24 phiếu đề nghị mồ côi**
   (8 ở status 3 · 8 ở status 4 · 8 ở status 5) không còn phiếu thu nào trỏ tới — không dọn.
2. Hủy phiếu thu là **ngõ cụt**: đề nghị chuyển Hủy và không lập lại phiếu thu được, vì
   `guardOneBillPerRequest()` (`BillIncomeWriteService:225-236`) kiểm `exists()` không lọc trạng thái;
   nút "Tạo phiếu thu" ở màn Đề nghị cũng ẩn theo (đếm phiếu thu, không loại phiếu đã hủy). ERP y hệt.
3. Lưu nháp phiếu thu không đổi trạng thái đề nghị → đề nghị vẫn hiện "Chờ KT duyệt" dù đã bị khóa
   (người khác bấm Tạo phiếu thu nhận lỗi *"Đề nghị thu tiền đã lập phiếu thu tiền"*).

⚠️ Ai review sau: 3 điểm trên **không phải bug cần sửa** — là quyết định nghiệp vụ đã chốt.

## 5 lỗi ERP mà HRM chủ động sửa

1. `delete()` không kiểm quyền lẫn trạng thái → gate `canDelete()` + 423
2. `generateCode()` không khóa → dùng pattern `lockForUpdate()` của `BillIncomeRequest`
3. hook `created` gọi `save()` lần 2 → gán cấp tổ chức ngay trong `create()`
4. `update()` nhận nhầm `StoreRequest`; `UpdateRequest` viết `$this->status = 4` (gán, không so sánh)
5. `catch (Exception)` nuốt `ValidationException` → rethrow

**Bổ sung**: chặn duyệt lại (`FOR UPDATE` + kiểm lại status → 409) để không nhân đôi bút toán.
ERP không có, duyệt 2 lần bên ERP là ghi trùng sổ cái.

## Rủi ro cần biết

Đây là **lần đầu HRM ghi bút toán vào sổ cái dùng chung với cổng ERP** — ghi sai/trùng là lệch số
liệu kế toán thật, không hoàn tác được. Kiểm chứng bắt buộc trên DB dump: đối chiếu từng trường của
`account_details` + `account_detail_refs` giữa 2 cổng, thử duyệt 2 lần, log riêng mỗi lần ghi sổ.

**Giới hạn**: 2 nhánh *phân bổ phiếu xuất hàng* và *thu dư nợ đầu kỳ* có 0 dòng dữ liệu trên DB →
không test chạy thật được, chỉ verify bằng đọc code đối chiếu.

## Dữ liệu thật (DB gộp, đếm 2026-08-18)

`bill_incomes` **2.347** dòng (Đã duyệt 2.304 · Hủy 35 · Chờ duyệt 8 · Đang tạo 0) ·
`bill_income_details` **7.401** (customer 7.398 · supplier 3 · employee 0) ·
`bill_income_detail_product_export_requests` **0** · `is_income_begin = 1` **0**.
