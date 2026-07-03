# Phase 2 — Xuất kho (chi tiết)

**Ngày:** 2026-06-29 · @manhcuong · Nối tiếp `design.md` + spec tổng §3.3/§4/§4.1. Module `Modules/Warehouse` (đã có engine + nhập kho từ Phase 1).

## Quyết định Phase 2
- Xuất kho 2 loại trong 1 màn: **theo HĐ** (`issue_type=1`) hoặc **tự do** (`issue_type=2`). KHÔNG trộn dòng HĐ + tự do trong 1 phiếu.
- Gắn HĐ: chỉ HĐ **Đã duyệt** (status=3) còn hàng chưa xuất hết. Dòng pre-fill từ HĐ, **hàng hoá khoá**, **ĐVT khoá theo dòng HĐ**, SL mặc định = còn lại (sửa được, ≤ còn lại).
- Tự do: chọn hàng hoá tự do (như phiếu nhập), chọn ĐVT bất kỳ + quy đổi.
- Khi DUYỆT: **chặn cứng tồn** (assertEnough) + nếu theo HĐ **chặn vượt SL còn lại của dòng HĐ**; ghi movement `−`; `inventories −=`.
- "Số lượng đã xuất" trên HĐ: **accessor tính động** (không denormalize).
- Workflow/khoá/không hoàn tác: y hệt Phase 1 (Nháp→Chờ duyệt→Đã duyệt/Từ chối; đã duyệt khoá).

## DB
```sql
wh_issues (PX-YYYY-NNNNN)
  warehouse_id, issue_date DATE,
  issue_type TINYINT (1 theo HĐ | 2 tự do),
  contract_id BIGINT NULL,
  receiver VARCHAR(255) NULL,   -- người/bộ phận nhận
  reason   VARCHAR(255) NULL,   -- lý do xuất (tự do)
  + status/approved_at/approved_by/reject_reason/note/company_id/department_id/part_id/created_by/updated_by/timestamps

wh_issue_items
  issue_id (FK cascade), product_id, unit_id, conversion_rate INT,
  quantity DECIMAL(18,2), quantity_base DECIMAL(18,2),
  contract_item_id BIGINT NULL,   -- gắn dòng HĐ khi issue_type=1
  note, sort_order
```

## BE
- **Entity** `WhIssue` (STATUSES + getNextCode `PX-`, isCan*), `WhIssueItem` (product/unit relations + contractItem). const ISSUE_TYPE_CONTRACT=1, ISSUE_TYPE_FREE=2.
- **IssueService** (mô phỏng WhReceiptService):
  - `index` (filter: keyword, warehouse_id, issue_type, contract_id, status, from/to date)
  - `store/update` (issue_type=1: validate mỗi item có contract_item_id + quantity ≤ remaining; issue_type=2: free; tính quantity_base; snapshot conversion_rate)
  - `submit/reject` y Phase 1
  - `approve`: `StockService::assertEnough(warehouse, gộp product)` → chặn; nếu issue_type=1 → `assertContractRemaining` (mỗi contract_item_id: đã duyệt + phiếu này ≤ qty HĐ base); mỗi item `postMovement(−quantity_base, TYPE_ISSUE)`; status=3.
  - `contractRemaining($contractId)`: trả dòng HĐ (product, unit, qty) + `issued` + `remaining` (theo ĐVT dòng HĐ; vì ĐVT khoá nên so trực tiếp). Chỉ HĐ status=3.
- **Controller** `WhIssueController` (transaction store/update/approve + lockForUpdate approve + rethrow ValidationException) + endpoint `GET /issues/contract/{id}/remaining`.
- **Routes** `/v1/warehouse/issues` (8 route CRUD/workflow + remaining), checkPermission 1128 (thêm/sửa) / 1129 (duyệt).
- **Resource** list + detail (items kèm product_name/unit_name/quantity/quantity_base/contract info).
- **Permission** seeder: 1127 Xem / 1128 Thêm-sửa / 1129 Duyệt phiếu xuất kho, type=10, group "Xuất kho".

### Sale — "Số lượng đã xuất" (additive, không sửa logic cũ)
- `SaleContractItem`: accessor `getQuantityIssuedAttribute()` = `WhIssueItem::where('contract_item_id', $this->id)->whereHas('issue', fn=>status=3)->sum('quantity_base')` quy về ĐVT dòng HĐ (÷ conversion_rate dòng HĐ). Vì ĐVT xuất khoá theo HĐ → quantity_base/đúng rate.
- `DetailSaleContractResource` (tab "Thông tin xuất hàng"): mỗi item trả thêm `quantity_issued` (đang hiện "-" → số thật). Xanh khi `quantity_issued >= quantity`.
- KHÔNG đổi status HĐ, KHÔNG đụng luồng tạo/duyệt HĐ.

## FE (`pages/warehouse/issue/`)
- **store** `warehouse-issue` (list/detail/save/update/remove/submit/approve/reject + `contractRemaining(contractId)`).
- **WhIssueForm**: radio **Loại xuất** (Theo HĐ / Tự do).
  - Theo HĐ: select **Hợp đồng** (load HĐ đã duyệt còn hàng) → gọi remaining → bảng dòng pre-fill (hàng hoá + ĐVT khoá, cột "SL còn lại", input SL ≤ còn lại, cảnh báo nếu vượt). receiver.
  - Tự do: chọn hàng hoá (ProductPickerModal tái dùng) + ĐVT + SL + quy đổi; reason/receiver.
  - Validate inline (touched); Lưu / Lưu & Gửi duyệt → redirect list.
- **list** (filter loại xuất/HĐ/kho/trạng thái/ngày/keyword; badge; sort) + **detail** (header + bảng items + cột HĐ nếu có + workflow footer gate quyền 1129) + **create/edit**.
- **menu** "Quản lý kho": thêm mục "Xuất kho" (`/warehouse/issue`, isShow ['Xem phiếu xuất kho']) trong `components/default-menu/warehouse.js`.
- **Permission.vue** accordion type=10 đã có → tự hiện thêm group "Xuất kho".

## Edge cases
- HĐ đã xuất đủ toàn bộ dòng → không hiện trong dropdown chọn HĐ (remaining=0 mọi dòng).
- Sửa phiếu xuất theo HĐ: tính lại remaining loại trừ chính phiếu đang sửa (nếu phiếu chưa duyệt thì chưa trừ tồn/đã xuất; nếu đã duyệt thì khoá không sửa).
- Chặn vượt tồn + vượt HĐ kiểm tại bước DUYỆT trong cùng transaction (assertEnough + assertContractRemaining trước postMovement).
- Phiếu xuất theo HĐ với 0 dòng remaining → Request chặn (items min 1).
- Gộp nhiều dòng cùng product khi assertEnough.

## Phân chia task (plan)
BE: T1 migration → T2 Entities → T3 IssueService (+contractRemaining +assertContractRemaining) → T4 Controller/Request/Resource/Routes/permission 1127-1129 → T5 Sale accessor quantity_issued + Resource.
FE: T6 store → T7 form (HĐ/tự do) → T8 list+detail+menu "Xuất kho".
