# Dashboard: thông báo PLBS hợp đồng trong nước chờ duyệt

- **Ngày**: 2026-06-15
- **Dự án**: ERP Tân Phát (TanPhatDev)
- **Loại**: Bổ sung nhỏ (1 file BE)

## Vấn đề

Dashboard trang chủ (màn thông báo "cần duyệt"), group **"Đặt mua hàng trong nước"** đang có các ô: HĐ trong nước tự do/theo hãng, HĐ nguyên tắc, PI, Đơn hỏi hàng — nhưng **thiếu** ô thông báo **Phụ lục bổ sung (PLBS)** hợp đồng mua hàng trong nước đang **chờ duyệt**. Người duyệt không nhận biết có PLBS chờ duyệt từ dashboard.

## Mục tiêu

Thêm 2 ô vào group "Đặt mua hàng trong nước":
1. **PLBS trong nước tự do cần duyệt** — đếm PLBS tự do (type=5) chờ duyệt, link list lọc sẵn chờ duyệt.
2. **PLBS trong nước theo hãng cần duyệt** — đếm PLBS theo hãng (type=4) chờ duyệt, link list lọc sẵn chờ duyệt.

## Hiện trạng code

- **Dashboard data**: `app/Http/Controllers/HomeController.php` — method `approveList()` build mảng `$result[]`, mỗi item: `['group', 'name', 'link', 'count']`. Group "Đặt mua hàng trong nước" = `'DAT_MUA_HANG_TRONG_NUOC'` (dòng ~1802-1889).
- **Render**: `resources/views/home.blade.php` (ng-repeat) tự render mọi item theo group; chỉ hiện ô khi `item.count > 0`.
- **Model**: `app/Model/Order/InlandBuyContractNew.php` (bảng `inland_buy_contract_news`):
  - type: `PHU_LUC_HANG = 4` (PLBS theo hãng), `PHU_LUC_TU_DO = 5` (PLBS tự do).
  - status: `CHO_DUYET = 2`.
- **List screen**: route `inlandBuyContractNew.index` (`/admin/orders/inland_buy_contract_new`). Trong `searchByFilter` (model, dòng 853-883):
  - `_type=for-approved` + có quyền duyệt → lọc `status=CHO_DUYET` + `company_id`.
  - `type=4` → `where(type=PHU_LUC_HANG)`; `type=5` → `where(type=PHU_LUC_TU_DO)`.
  - → `?type=4&_type=for-approved` = PLBS theo hãng chờ duyệt; `?type=5&_type=for-approved` = PLBS tự do chờ duyệt.

## Thiết kế

Chỉ sửa `HomeController::approveList()`, thêm 2 block ngay sau item "Đơn hỏi hàng - PO trong nước theo hãng" (~dòng 1889), copy pattern item HĐ trong nước hiện có:

```php
// PLBS trong nước tự do chờ duyệt
if ($logged_user->can('Duyệt hợp đồng mua hàng trong nước')) {
    $count = InlandBuyContractNew::query()
        ->where('type', InlandBuyContractNew::PHU_LUC_TU_DO)
        ->where('status', InlandBuyContractNew::CHO_DUYET)
        ->where('company_id', $logged_user->info->company_id)
        ->count();
    $result[] = [
        'group' => 'DAT_MUA_HANG_TRONG_NUOC',
        'name'  => 'PLBS trong nước tự do cần duyệt',
        'link'  => route('inlandBuyContractNew.index') . '?type=5&_type=for-approved',
        'count' => $count
    ];
}
// PLBS trong nước theo hãng chờ duyệt
if ($logged_user->can('Duyệt hợp đồng mua hàng trong nước')) {
    $count = InlandBuyContractNew::query()
        ->where('type', InlandBuyContractNew::PHU_LUC_HANG)
        ->where('status', InlandBuyContractNew::CHO_DUYET)
        ->where('company_id', $logged_user->info->company_id)
        ->count();
    $result[] = [
        'group' => 'DAT_MUA_HANG_TRONG_NUOC',
        'name'  => 'PLBS trong nước theo hãng cần duyệt',
        'link'  => route('inlandBuyContractNew.index') . '?type=4&_type=for-approved',
        'count' => $count
    ];
}
```

## Quyết định

- **Quyền**: tái dùng `'Duyệt hợp đồng mua hàng trong nước'` (PLBS là sub-type cùng entity, đồng nhất các ô HĐ/PI cùng group).
- **Phạm vi công ty**: lọc `company_id` của user (đồng nhất pattern hiện có).
- **Ẩn khi 0**: blade chỉ render ô khi `count > 0` → không có PLBS chờ duyệt thì tự ẩn.
- **Link**: `_type=for-approved` (đã lọc chờ duyệt) thay vì `_type=all`.

## Phạm vi

- ✅ 1 file: `HomeController.php` (thêm 2 block).
- ❌ Không sửa blade, không migration, không thêm permission, không sửa list/model.

## Test

1. Có PLBS tự do (type=5) chờ duyệt → ô "PLBS trong nước tự do cần duyệt" hiện đúng số; bấm → list đúng (chờ duyệt, tự do).
2. Tương tự type=4 (theo hãng).
3. Không có PLBS chờ duyệt → ô tự ẩn.
4. User không có quyền "Duyệt hợp đồng mua hàng trong nước" → không thấy 2 ô.
5. Số đếm khớp với số dòng list khi mở link.
