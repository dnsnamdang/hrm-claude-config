# Liên thông CSDL Dược quốc gia v2 cho SPHACY (GPP + GDP) — @cuong61n

Hệ thống CSDL Dược quốc gia v2 (`api.csdlduoc.com.vn/v2`) yêu cầu nhà thuốc (GPP) và
cơ sở phân phối (GDP) báo cáo mọi chứng từ nhập/bán/kiểm kho/huỷ. SPHACY đẩy tự động
theo hàng chờ, có màn theo dõi và màn liên kết mã thuốc nội bộ sang mã quốc gia.

Repo: `sphacy_api` (nhánh chính `api2`, nhánh tính năng `dqg`),
`sphacy_web` (nhánh chính `main`, nhánh tính năng `dqg`).

## Task

- [x] **29/10/2026 — Merge tính năng liên thông vào nhánh chính và chạy trên cổng chính**
  - Nghiệp vụ: mở phần liên thông CSDL Dược cho khách thật ở hai cổng
    `gpp.thuocvietnam.vn` và `gdp.thuocvietnam.vn`. Riêng phần "Tồn đầu kỳ & đẩy bù"
    (đặt một đợt gửi hàng nghìn chứng từ cũ) tạm đóng, vì hệ quốc gia không cho xoá
    phiếu đã nhận nên chưa mở khi chưa đo trên dữ liệu thật của khách.
  - Kỹ thuật: merge `dqg` → `api2` (BE, commit `cb09902`) và `dqg` → `main`
    (FE, commit `f2c9a75`); mỗi nhánh thêm một commit tạm đóng phần đẩy bù (chú thích
    lại tab, 4 route `/api/csdlduoc/replay*`, lịch `csdlduoc:replay-run`). Giữ lớp
    `CsdlDuocReplayer` và migration vì `csdlduoc:scan-missing` đọc cột
    `drugstores.csdlduoc_opening_date`. Bản đầy đủ (có tab) đẩy lên nhánh `dqg` cả hai repo.
  - Đã kiểm: lint 448 file PHP bằng chính PHP 7.3 của prod — 0 lỗi (prod còn 7.3, local 7.4);
    local GPP còn đúng 3 tab, `/api/csdlduoc/replay` trả 404; prod trả 200 cho
    `/api/csdlduoc/transactions` và 404 cho `/replay`; hash `main.*.chunk.js` ở hai cổng
    khớp bản vừa build.
  - Trạng thái: **đã deploy prod 29/10/2026**. API cả hai server (42.96.43.234,
    42.96.40.220): 9 migration liên thông chạy qua `--path=database/migrations_dqg`
    (vì `migrate` thẳng đụng 3 migration cũ đang kẹt), `.env` thêm
    `CSDLDUOC_ENV=production` (sao lưu `.env.bak-2026-10-29`). FE build hai nhánh,
    chép vào `/var/www/html/sphacy_gppweb/build` và `/var/www/html/gdp/build` trên cả
    42.96.41.135 và 42.96.41.13 (bản cũ giữ ở `build_truoc_dqg_29_10`).

## Còn lại

- Danh mục thuốc quốc gia trên prod đang rỗng: `csdlduoc:sync-master` cần token của một
  cơ sở đã bật liên thông, mà prod chưa có cơ sở nào khai tài khoản thật. Nhà thuốc đầu
  tiên khai xong thì cron 03:00 tự nạp (~1.091 trang, 10–40 phút). Danh mục sandbox
  không dùng lại được.
- Tab "Tồn đầu kỳ & đẩy bù" còn trên nhánh `dqg`, chờ tester chạy trên cổng test trước
  khi mở ở cổng chính.
- Chưa làm: cảnh báo/gửi điều chỉnh khi hoá đơn bị sửa sau khi đã liên thông.
