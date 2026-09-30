# Fix phiếu con chuyển duyệt bị gán sai phòng ban / công ty

**Người phụ trách:** @junfoke — Repo `TanPhatDev`, nhánh `master`
**Ngày:** 09/09/2026

## Hiện tượng (user báo)

Màn `/admin/orders/reports/orderReportProcess` (Báo cáo tiến độ đặt hàng theo nhân viên):
lọc Thương hiệu DAISEN + Nhân viên "Đỗ Quốc Bảo" → ra 3 phiếu; đổi sang lọc Thương hiệu DAISEN
+ Phòng ban "Phòng KD Khu vực 4" (phòng của chính Bảo) → **Chưa có dữ liệu**.

## Root cause

Phiếu gốc thương hiệu JOHN có mã lẻ khác hãng → khi duyệt, hệ thống **tách mã lẻ** sinh phiếu con
mới qua `RootOrderRequestService::switchApprove()` (`app/Services/RootOrderRequests/RootOrderRequestService.php:309`).
Hàm này **cố ý copy** `department_id` / `company_id` từ phiếu cha.

Nhưng model có hook chạy SAU khi lưu, ghi đè bằng thông tin của `Auth::user()` — lúc đó là
**người bấm duyệt**, không phải người đặt hàng:

```php
// app/Model/Order/RootOrderRequest.php:94
self::created(function ($model) {
    if (\Auth::user()) {
        $model->company_id    = \Auth::user()->info->company_id;
        $model->department_id = \Auth::user()->info->department_id;
        $model->part_id       = \Auth::user()->info->part_id;
        $model->save();
    }
});
```

Bộ lọc báo cáo (`OrderReportProcessService::filter`) lọc Nhân viên theo `ror.created_by`
(vẫn là Bảo → ra dữ liệu) nhưng lọc Phòng ban theo `ror.department_id` (đã thành phòng người
duyệt → rỗng).

## Bằng chứng prod (user chạy SQL 09/09/2026)

| phiếu con | phiếu cha | brand cha→con | người tạo | phòng người tạo | người duyệt | phòng lưu trên phiếu |
|---|---|---|---|---|---|---|
| PDH-07140 | PDH-07109 | 265 → 333 | Đỗ Quốc Bảo | 109 (KV4) | Nguyễn Thị Ngoan | 46 (XNK) |
| PDH-07148 | PDH-07116 | 265 → 333 | Đỗ Quốc Bảo | 109 (KV4) | Nguyễn Thị Ngoan | 46 (XNK) |
| PDH-07208 | PDH-07168 | 279 → 333 | Đỗ Quốc Bảo | 109 (KV4) | Vũ Thị Nhài | 46 (XNK) |

Quy mô: **371 phiếu con → 351 sai phòng ban, 59 sai cả công ty.** (20 phiếu "đúng" chỉ vì người
duyệt tình cờ cùng phòng người đặt hàng.) KV4 thuộc công ty 4, phòng XNK thuộc công ty 1 → lỗi
làm dữ liệu nhảy sang công ty khác, ảnh hưởng cả nhánh quyền `is_company`.

Phạm vi ảnh hưởng: **mọi màn/báo cáo lọc `root_order_requests` theo phòng ban hoặc công ty**,
không riêng báo cáo tiến độ đặt hàng.

## Quyết định của user (09/09/2026)

Báo cáo phải lấy theo **phòng ban của người yêu cầu gốc** → phiếu con giữ phòng/bộ phận/công ty
của phiếu cha. Fix code trước, vá dữ liệu cũ sau.

## Phương án

1. Hook `created` của `RootOrderRequest` chỉ điền khi trường còn trống (`empty()`), không đè giá
   trị mà `switchApprove()` đã copy từ phiếu cha. Luồng tạo mới bình thường (`store()`) không set
   sẵn 3 trường này nên vẫn được điền như cũ → không hồi quy.
2. Vá dữ liệu cũ: `UPDATE` phiếu con theo phiếu cha (user tự chạy trên prod sau khi backup).
3. Lỗi phụ cùng màn: `OrderReportProcessService::filter` nhánh quyền "theo bộ phận" query
   `ror.is_part` — cột không tồn tại trong `root_order_requests` (chỉ có `part_id`) → user chỉ
   có quyền cấp bộ phận sẽ lỗi SQL. Sửa thành `part_id`.

## Ngoài scope

- Các model khác trong ERP dùng cùng khuôn hook `created` ghi đè company/department/part
  (`BillIncome`, `AdditionAccountingRequest`, `DivisionMarketDepartmentEmployee`…). Chưa rà, chỉ
  sửa `RootOrderRequest` theo đúng ca lỗi được báo.
