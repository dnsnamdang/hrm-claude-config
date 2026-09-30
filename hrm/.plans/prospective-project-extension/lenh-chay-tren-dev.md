# Bộ lệnh cần chạy trên cổng dev (/var/www/tpe)

Tôi không SSH được vào `hrm.eteksofts.com:2230` (từ chối publickey với manhcuong/tpe/deploy/ubuntu/root/hrm/dev/www-data),
nên 2 việc dưới đây cần anh chạy hộ. Có thể gõ thẳng trong phiên này bằng tiền tố `!` để kết quả đổ vào hội thoại.

## 1. GÁN quyền duyệt gia hạn cho vai trò (seeder đã chạy rồi, không cần chạy lại)

Đã kiểm tra trên dev: 2 quyền có sẵn trong hệ thống (598 quyền, gồm id 1182 và 1183).
Việc còn thiếu là **gán** chúng cho vai trò của tài khoản đang test — vào màn **Phân quyền** tích 2 dòng:

- `Trưởng phòng duyệt gia hạn dự án TKT` (id 1182)
- `Ban giám đốc duyệt gia hạn dự án TKT` (id 1183)

Chưa gán thì `GET /assign/prospective-project-extensions/pending-approval` còn trả 403 và menu
"Gia hạn dự án TKT" trong nhóm Phê duyệt không hiện.

## 2. Chạy cron tự đóng dự án

**Bước 1 — xem trước phạm vi ảnh hưởng, KHÔNG ghi gì:**

```bash
cd /var/www/tpe && php artisan assign:auto-close-prospective-projects --dry-run
```

⚠️ Lượt chạy thật đầu tiên sẽ đóng luôn mọi dự án cũ đã quá hạn. Xem danh sách ở bước 1 trước khi quyết định.

**Bước 2 — chạy thật trên đúng 1 dự án để nghiệm thu an toàn:**

```bash
cd /var/www/tpe && php artisan assign:auto-close-prospective-projects --project=445
```

**Bước 3 — chạy thật toàn bộ (chỉ khi đã đồng ý với danh sách ở bước 1):**

```bash
cd /var/www/tpe && php artisan assign:auto-close-prospective-projects
```

Lịch tự động đã khai sẵn 01:30 hằng ngày trong `app/Console/Kernel.php`; cần server có chạy `schedule:run`.

## Dữ liệu tôi đã tạo sẵn trên dev

| Dự án | Mã | Ghi chú |
|---|---|---|
| 445 | HN_NSHC.UD.TEST.2026.DA049 | NV KD chính = namdangit; đề xuất GHDA.00001 15 ngày, Cấp 1 (chỉ TP duyệt) |
| 446 | HN_NSHC.UD.TEST.2026.DA050 | NV KD chính = namdangit; đề xuất GHDA.00002 45 ngày, Cấp 2 (TP → BGĐ) |
| 447-450 | …DA051→DA054 | Dự án trống để test thêm, hạn đóng 12/12/2026 |

Muốn ép 1 dự án quá hạn để xem cron đóng thật thì lùi ngày tạo:

```bash
cd /var/www/tpe && php artisan tinker --execute="DB::table('prospective_projects')->where('id',447)->update(['created_at'=>now()->subMonths(4)]);"
cd /var/www/tpe && php artisan assign:auto-close-prospective-projects --project=447
```
