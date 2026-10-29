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

- [x] **29/10/2026 — Nạp danh mục thuốc quốc gia lên prod và vá lệnh đồng bộ**
  - Nghiệp vụ: khách phải liên kết thuốc của mình với mã danh mục quốc gia mới đẩy
    được chứng từ, nên danh mục 54.540 thuốc là điều kiện bắt buộc trước mọi việc khác.
    Cơ sở đầu tiên khai tài khoản thật: #5349 "NHÀ THUỐC QUẢNG HOÀ - 305A AN DƯƠNG VƯƠNG".
  - Kỹ thuật — 3 lỗi phải sửa:
    1. Khách kết nối tài khoản báo `cURL error 60 Peer's Certificate issuer is not recognized`:
       máy chủ Bộ **không gửi chứng chỉ trung gian**, mà curl trên CentOS 7 dùng NSS nên
       không tự lấy. Tải `SectigoRSADomainValidationSecureServerCA` theo AIA trong cert,
       `openssl verify -untrusted` xác minh OK, cài vào `/etc/pki/ca-trust/source/anchors/`
       + `update-ca-trust extract` trên **cả hai** server API.
    2. Lượt nạp đầu dừng ở 600/54.540 mà vẫn in "xong": lệnh coi trang HTTP 200 thiếu
       khoá `data` là hết dữ liệu. Vá `3430bb2` — thiếu `data` là hỏng, không phải hết.
    3. Nguyên nhân thật của các trang rỗng: **một bản ghi hỏng bên Bộ làm rỗng cả trang
       chứa nó** (đo: trang 13/33/47/51 lần nào cũng rỗng; chia nhỏ page_size=25 hoặc 20
       thì lấy được; hỏi từng bản ghi 601–620 → chỉ vị trí 602 rỗng). Vá `4f56048`:
       trang rỗng thì vớt theo lô 10 rồi hỏi từng bản ghi để tách đúng bản ghi xấu, và
       ngưỡng dừng đếm **lỗi liên tiếp** thay vì tổng lỗi (code cũ đếm tổng sẽ cắt ngang
       ở khoảng trang 300/1.091).
  - Đã kiểm: `select count(*) from sphacy_v1_new.csdlduoc_drugs` → **54.497/54.540**
    (thiếu 43 bản ghi hỏng bên Bộ, hỏi lẻ từng bản ghi vẫn rỗng); cả 54.497 dòng đều có
    `registration_number`; 734 dòng Bộ không công bố đóng gói. 14 đơn vị tính đã nạp.
    Kiểm chứng chuỗi chứng chỉ bằng `CsdlDuocClient::login` với tài khoản bịa →
    `http 401 "Tên đăng nhập hoặc mật khẩu không đúng"` (tức TLS đã thông).
  - Trạng thái: **đã deploy prod 29/10/2026**, BE cả hai server ở `deb2c7c`. Danh mục
    đã dùng được, tester bắt đầu map thuốc được.

## Còn lại

- 43 bản ghi danh mục Bộ không trả được (lỗi bên họ, hỏi lẻ từng bản ghi vẫn rỗng).
  Chờ Bộ sửa dữ liệu; cron 03:00 tự nạp lại nên sẽ tự có khi họ sửa. Nếu khách gặp
  thuốc không tìm thấy trong danh mục thì khả năng cao thuộc nhóm này.
- Tab "Tồn đầu kỳ & đẩy bù" còn trên nhánh `dqg`, chờ tester chạy trên cổng test trước
  khi mở ở cổng chính.
- Chưa làm: cảnh báo/gửi điều chỉnh khi hoá đơn bị sửa sau khi đã liên thông.
