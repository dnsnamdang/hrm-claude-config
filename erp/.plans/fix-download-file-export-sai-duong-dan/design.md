# Fix: Màn Download File không hiện file export (EtekPower / EtekGreen)

@junfoke — Repo `TanPhatDev`, nhánh `master`. Phát hiện 2026-09-08.

## Hiện tượng

`https://erp.etekpower.com.vn/admin/products/download-file` — bảng "Danh sách xuất file cho sản phẩm"
trống trơn, dù user đã bấm Xuất Excel nhiều lần và được báo "Danh sách hàng sẽ được xuất file sau ít phút!".

Ca gốc: user 27 (`thunth@etekpower.vn`) bấm 7 lần trong ngày 08/09/2026 (14:33 → 15:50), không thấy file nào.

## Điều tra trên production

- File **đã xuất thành công**, có đủ 7 file trong
  `/var/www/html/EtekPower/storage/app/public/product_export/27/`.
- Không có job nào trong queue vì **màn này không dùng queue**: `exportProduct()` gọi
  `exec('php artisan product:export-large ... &')` — process nền của OS, không qua bảng `jobs`.
  (Nhánh `ProductSettingMailJob::dispatch` đã bị comment từ trước.)
- `ls -la /var/www/html/*/public/storage`:

  | Deploy | `public/storage` trỏ tới |
  |---|---|
  | EtekPower | `/var/www/html/TanPhatDev/storage/app/public` ⚠ |
  | EtekGreen | `/var/www/html/TanPhatDev/storage/app/public` ⚠ |
  | NewErp | chính nó |
  | TanPhatDev | chính nó |

## Root cause

Code **trộn 2 hệ toạ độ** cho cùng một file:

| Thao tác | Hàm dùng | Trỏ tới |
|---|---|---|
| Ghi | `->store($fileName, 'public')` | `storage_path('app/public')` — **riêng từng deploy** |
| Đọc (liệt kê) | `public_path('storage/...')` | qua symlink — **kho của TanPhatDev** |
| Đọc (tải về) | `asset($file['path'])` | nginx serve qua symlink — **kho của TanPhatDev** |

Trên bản TanPhatDev hai đường trùng nhau nên chạy tốt; mang sang EtekPower/EtekGreen (symlink trỏ
sang project khác) thì ghi một nơi đọc một nẻo → `File::exists()` false → danh sách rỗng.

## Quyết định: sửa code, KHÔNG đụng symlink

Đã kiểm chứng `storage/app/public` chỉ phục vụ 3 thứ: `product_export`, `stock_export`, và báo cáo kế
toán trong `AccountingChangeSummaryReportMailJob` (gửi qua mail). **Ảnh sản phẩm không liên quan** —
`FileHelper::uploadFile()` đẩy lên S3, hoặc `->move()` vào `base_path()/public/uploads/`.

Nên đổi symlink là dư thừa và có rủi ro (phải sửa 2 deploy, lần deploy sau lại lệch lại). Sửa code là
fix gốc, chạy đúng trên cả 4 bản deploy, **không cần chạm hạ tầng production**.

## Phạm vi sửa

1. Mọi `public_path('storage/...')` → `storage_path('app/public/...')` (5 chỗ, 2 controller).
2. Bỏ `asset()` ở view — file không còn nằm trong webroot của chính deploy, nginx không serve được.
   Thay bằng route PHP `product.downloadExportFile` → `response()->download()`.
3. Route tải ghép cứng `Auth::id()`, validate tên file bằng regex, chặn path traversal.
4. `ProductTemplatesController::downloadFile()` dính lỗi y hệt — sửa cùng (lưu ý: **method này chưa
   có route đăng ký**, hiện là code chết, sửa cho nhất quán).

## Không làm trong đợt này

- Các bản export **cũ** nằm bên kho TanPhatDev sẽ không còn hiện trên EtekPower sau khi sửa (file từ
  tháng 7/2026 trở về trước — coi là rác, user đồng ý bỏ).
- Dọn file export cũ tự động: chưa có cron nào, `product_export` của TanPhatDev đã có 24 thư mục user,
  vài file nặng 138 MB từ 06/2025 vẫn nằm đó → tách task riêng.
- Flash message sau khi xuất không kèm link tới màn Download File → user không biết đi đâu lấy
  (chính là lý do chị Thu bấm lại 7 lần). Tách task riêng.
