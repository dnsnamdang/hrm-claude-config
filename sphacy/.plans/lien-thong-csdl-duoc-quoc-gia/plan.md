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

- [x] **02/11/2026 — Sửa hai chỗ gây hiểu nhầm ở màn liên kết thuốc**
  - Nghiệp vụ: tester báo hai việc khi triển khai cho nhà thuốc đầu tiên
    (#5349 Quảng Hoà): (1) tab Liên kết thuốc lọc "Chỉ thuốc còn tồn" ra rỗng,
    (2) cột "Mã quốc gia" ở màn Danh sách thuốc báo "Chưa ánh xạ" cho mọi thuốc.
  - Việc (1) không phải lỗi: cả 7 thuốc còn tồn đã khớp thẳng danh mục quốc gia
    (4 thuốc vừa đổi sang số ĐK mới, 3 thuốc giữ số VD-xxxxx-xx còn hiệu lực —
    30.114/54.497 thuốc trong danh mục Bộ vẫn ở dạng cũ). Nhưng bảng chỉ hiện
    "No data" nên ai cũng tưởng hỏng → thay bằng câu nói rõ đã xong, kèm gợi ý
    chuyển sang "Tất cả thuốc"; đang tải thì không kể công sớm.
  - Việc (2) là lỗi thật, ảnh hưởng MọI nhà thuốc: cột đó đọc `drug.csdlduoc_drug_id`
    mà **không luồng nào ghi vào cột đó** (luồng duyệt ghi vào bảng
    `csdlduoc_drug_map`). Việc đẩy liên thông không sai vì
    `CsdlDuocService::findNationalDrug` đi đường khác, nhưng dược sĩ nhìn cột này
    tưởng chưa map xong nên không dám khai tồn đầu kỳ.
  - Kỹ thuật: `CsdlDuocController@drugCodes` viết lại thành một câu SQL tra theo đúng
    hai đường của `findNationalDrug` — khớp thẳng số đăng ký (kể cả
    `old_registration_number`), không khớp mới tra ánh xạ `approved` của chính nhà
    thuốc. Biểu thức SQL dựng `match_key` chuyển về `CsdlDuocMapper::sqlMatchKey`
    để hai nơi dùng chung một định nghĩa (nội dung giữ nguyên từng ký tự).
  - Đã kiểm: trên dữ liệu thật local (cơ sở 797, 1349) 200 thuốc → 69 mã khớp thẳng,
    đúng bằng số đếm bằng SQL; thuốc VD-19745-13 không có trong danh mục quốc gia
    vẫn ra mã 893110302400 qua ánh xạ đã duyệt kèm `mapped_at`; mảng rỗng và cơ sở
    chưa bật liên thông vẫn trả đúng; tab Liên kết thuốc và summary không đổi kết quả
    sau khi dùng chung `sqlMatchKey`. Lint PHP 7.3 của prod — 0 lỗi. Kiểm chứng trên
    cổng chính bằng tài khoản thật: 7 thuốc hiện đúng mã, chỉ 2 thuốc thật sự chưa có
    mã (Fexophar 180, terpinzoat hạt) còn báo "Chưa ánh xạ".
  - Trạng thái: BE `2c93a49` **đã deploy prod 02/11/2026** trên cả hai server API.
    FE đợi build xong đẩy sau.

- [x] Xuất file excel danh sách thuốc: thêm cột "Mã quốc gia" (05/11/2026)
  - Nghiệp vụ: CSKH báo khách cần cột "Mã quốc gia" trong file "Xuất file excel" ở màn
    Danh sách thuốc để khai tồn đầu kỳ lên CSDL Dược; bảng trên màn hình có cột này
    nhưng file excel thì không (cả GPP lẫn GDP).
  - Kỹ thuật: `DrugList.jsx` — cột chỉ thêm cho `type === 'html'`; nay thêm cho cả
    `excel` khi cơ sở bật liên thông. Vì `maQuocGia.codes` chỉ có mã của 10 dòng trang
    đang xem, `getExportData(..., 'excel')` tra lại mã cho toàn bộ danh sách qua
    `/api/csdlduoc/drug-codes`, chia lô 500 id (giới hạn của API); lỗi tra mã không
    chặn xuất file, cột để trống. PDF giữ nguyên.
  - Lỗi khi test (05/11): xuất file báo "Kết nối đến máy chủ thất bại" + CORS error.
    Nguyên nhân: API GET, lô 500 id ra URL ~12,9KB → nginx trả 414 không kèm header
    CORS. Đã thử trực tiếp trên server: 500 id → 414, 100 id (2,5KB) → 200. Sửa: lô
    100 id, chạy 4 lô song song, `background: true` để lỗi tra mã không bắn toast,
    cột để trống chứ không chặn xuất file.
  - Đã kiểm: eslint 0 lỗi; 414/200 bằng curl. Người dùng xác nhận bản sửa chạy được
    trên local trước khi deploy.
  - Trạng thái: **đã deploy prod 05/11/2026**. Bản đầu `8c71c4b` (lô 500) đã lên prod
    lúc 11:08 cùng ngày và gây lỗi; bản sửa `c7bfbf4` (đã push `origin/main`) build GPP +
    GDP (`NODE_OPTIONS=--max-old-space-size=8192`, thiếu là build chết vì hết heap),
    chép vào `/var/www/html/sphacy_gppweb/build` và `/var/www/html/gdp/build` trên cả
    42.96.41.13 và 42.96.41.135 lúc ~11:58; bản trước giữ ở `build_truoc_lo100_05_11`
    (rollback: đổi tên lại). Chunk mới `1.99c1f5c7` (cũ `1.273aeb89`), kiểm 6/6 lần qua
    LB ở cả gpp.thuocvietnam.vn và gdp.thuocvietnam.vn đều trả chunk mới có lô 100.

- [x] **05/11/2026 — Sự cố: hệ quốc gia chặn IP, liên thông đứng cho toàn bộ cơ sở**
  - Hiện tượng: tester báo bấm "Kiểm tra kết nối" ra
    `cURL error 52: Empty reply from server`. Không phải lỗi của riêng cơ sở đó —
    cả hai server API đều đang bị chặn, mọi cơ sở đều không đẩy được.
  - Chuỗi nhân quả:
    1. Token cache bằng **file** nên không bao giờ lưu được: thư mục con trong
       `storage/framework/cache/data` do cron (user `deployer`) tạo ở quyền 755,
       php-fpm chạy bằng user `nginx` ghi không được và thất bại im lặng. Hai server
       API lại có cache riêng. → mỗi lần gửi phiếu / poll / bấm nút đều đăng nhập lại.
    2. Sáu cơ sở khai **sai tài khoản** (240, 1167, 1832, 2070, 2637, 5250). Hệ quốc
       gia trả 401, code chỉ trả null rồi phút sau cron thử lại.
    3. Cộng lại: **24.353 lượt đăng nhập trong hai ngày** trên server 43.234 → Bộ
       chặn theo IP bằng cách đóng thẳng kết nối. Đo được ngưỡng: **khoảng 10 lần
       đăng nhập trong ~20 giây là dính** (quét 33 tài khoản cách nhau 2s thì 9 lần
       đầu bình thường, từ lần 10 toàn error 52).
  - Xử lý:
    1. Thêm công tắc `CSDLDUOC_PAUSED` (commit `f0d0b97`): tách lịch liên thông ra hàm
       riêng để tắt được mà không chết lây SMS/email/thông báo dùng chung
       `schedule:run`. Tắt ~25 phút → Bộ gỡ chặn.
    2. Token chuyển sang **CSDL** (commit `939d740`, migration
       `2026_11_05_000001`): 4 cột mới trên `drugstores`. Hết lệ thuộc quyền file,
       và hai server dùng chung một token.
    3. Gặp 401 thì ghi dấu và nghỉ 30 phút; `saveConfig` / `test-connection` thành
       công thì xóa dấu ngay. Màn Cấu hình hiện cảnh báo đỏ bảo khách khai lại.
    4. Lỗi `cURL error 52` khi bấm Kiểm tra kết nối được dịch sang tiếng người —
       dược sĩ đang tưởng mình khai sai tài khoản.
  - Đã kiểm: trên local 6 kịch bản token (sai mật khẩu ghi dấu, lần sau không ra
    mạng 0,000s; token đúng lần 1 gọi mạng 0,29s lần 2 đọc DB 0,003s cùng token; hết
    hạn thì đăng nhập lại). Trên prod: cơ sở 5349 chạy bằng `deployer` lưu token,
    sau đó chạy bằng `nginx` dùng lại đúng token đó trong 0,00s — đúng điều cache
    file không làm được; cơ sở 5250 (sai tài khoản) ghi dấu đúng và lần hai không
    ra mạng. Lint PHP 7.3 — 0 lỗi.
  - Trạng thái: BE `939d740` **đã deploy prod 05/11/2026** cả hai server, migration đã
    chạy, cron đã bật lại. FE (cảnh báo đỏ) đang build.
  - **Cần Kiệt làm**: liên hệ 6 nhà thuốc trên khai lại tài khoản liên thông.

## Còn lại

- 43 bản ghi danh mục Bộ không trả được (lỗi bên họ, hỏi lẻ từng bản ghi vẫn rỗng).
  Chờ Bộ sửa dữ liệu; cron 03:00 tự nạp lại nên sẽ tự có khi họ sửa. Nếu khách gặp
  thuốc không tìm thấy trong danh mục thì khả năng cao thuộc nhóm này.
- Tab "Tồn đầu kỳ & đẩy bù" còn trên nhánh `dqg`, chờ tester chạy trên cổng test trước
  khi mở ở cổng chính.
- Chưa làm: cảnh báo/gửi điều chỉnh khi hoá đơn bị sửa sau khi đã liên thông.
