# Regulation-config tab Hàng hóa — "Hãng cần duyệt" phải nạp Hãng sản xuất (manufactures), không phải Thương hiệu (brands)

> Nhánh: `gop_db` (develop). Phụ trách: @dangquang.tom

## Bối cảnh

Màn `/sale/regulation-config` tab **Hàng hóa** (`id: 'hanghoa'`), 2 ô multi-select:
- "Hàng cập nhật giá – Hãng cần duyệt" (cột `companies.brand_ids`)
- "Hàng mới – Hãng cần duyệt" (cột `companies.new_brand_ids`)

User báo: 2 ô này **đang lấy nhầm Thương hiệu (brands)** thay vì **Hãng sản xuất (manufactures)**.

**Nguyên nhân gốc (đối chiếu ERP = nguồn chân lý):** ERP blade
`resources/views/common/companies/regulation.blade.php` dòng 704:
`$scope.brands = @json(\App\Model\Product\Manufacture::getForSelect());` — biến JS tên `brands`
thực chất nạp từ bảng **`manufactures`** (hãng sản xuất), KHÔNG phải bảng `brands`. Cột
`companies.brand_ids` / `new_brand_ids` lưu **id hãng sản xuất** dù tên cột có chữ "brand".

HRM khi port nhầm `'options' => 'brands'` (nạp bảng `brands`/thương hiệu) trong
`Modules/MasterData/Support/RegulationTabRegistry.php`. Service `resolveOptions()` chỉ có
`case 'brands'` → query bảng `brands`.

**Dữ liệu đã lưu:** local 8/8 công ty `brand_ids`=`new_brand_ids`=NULL (chưa có data) → không
có rủi ro backfill ở local. Trên prod, cột này vốn lưu id manufactures (ERP luôn ghi id
manufactures) nên sau khi đổi source sang manufactures sẽ map đúng tên. Nếu màn HRM đã từng cho
LƯU bằng id brands thì cần soi lại prod — HỎI user trước khi backfill.

`\App\Model\Product\Manufacture::getForSelect()` (ERP): `where('status',1)->select(id,name,company_id)
->orderBy('name')` — **KHÔNG lọc company_id** → HRM bám đúng: không lọc theo công ty.

## Tasks

- [x] **Task 1: BE — thêm nguồn options `manufactures` + đổi registry 2 field**
  - `RegulationConfigService.php` `resolveOptions()`: thêm `case 'manufactures'` →
    `DB::table('manufactures')->where('status',1)->select('id','name')->orderBy('name')` map id(string)=>name.
    Giữ nguyên `case 'brands'` (đúng nghĩa thương hiệu, để dành).
  - `RegulationConfigService.php` `optionLabelMap()`: thêm `'manufactures' => 'manufactures'` vào
    mảng `$table` (để lịch sử tra đúng tên; KHÔNG lọc status — giữ tên bản ghi cũ đã khoá).
  - `RegulationTabRegistry.php` dòng 391 (`brand_ids`) + 399 (`new_brand_ids`): đổi
    `'options' => 'brands'` → `'options' => 'manufactures'`.

- [x] **Task 2: FE — sửa comment cho khớp (chỉ comment, logic do BE trả options)**
  - `hrm-client/components/regulation-config/data.js` dòng ~280: comment "(brand ids)" →
    "(manufacture ids)".

- [x] **Task 3: Verify Playwright**
  - Mở `/sale/regulation-config` tab Hàng hóa → 2 ô "Hãng cần duyệt" liệt kê tên **hãng sản xuất**.
  - PASS: BE `getTabConfig(1,'hanghoa')` trả 981 option (= manufactures status=1), option đầu
    "3D BETA S.R.L" (man#701 ≠ brand#701 "ATORN"). Gõ "Haeco" trong dropdown FE → hiện
    **"Công ty Cổ phần Cơ điện Haeco"** (man#1246, tên hãng sản xuất) thay vì chip "HAECO"
    (brand#1244, thương hiệu). Lỗi user báo đã hết.

### Checkpoint — 2026-10-16 (ĐÃ COMMIT + PUSH)
Vừa hoàn thành: Task 1 (BE resolveOptions +case manufactures, optionLabelMap, registry 2 field) +
  Task 2 (comment FE) + Task 3 (verify BE tinker + FE Playwright PASS).
  **Đã commit + push origin/develop cả 2 repo** (commit riêng YC7, tách hunk khỏi YC8 cùng file):
  - hrm-api: `e20a1ce36` fix(regulation-config): ô "Hãng cần duyệt" nạp từ Hãng sản xuất...
  - hrm-client: `d512f556b` fix(regulation-config): comment ô "Hãng cần duyệt" là id hãng sản xuất
Đang làm dở: (không) — feature hoàn tất.
Bước tiếp theo: (không).
Blocked: (không)

**Lưu ý dữ liệu:** local 8/8 công ty brand_ids/new_brand_ids = NULL (không cần backfill local).
Prod: cột vốn lưu id manufactures (ERP), sau fix map đúng. Nếu màn HRM đã từng cho LƯU bằng id
brands thì giá trị prod có thể sai → cần user xác nhận soi/backfill (nguyên tắc chung "Không
backfill" nhưng đây là bug khác — phải HỎI nếu phát hiện data sai).
