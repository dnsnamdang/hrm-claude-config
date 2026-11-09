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

## 09/11/2026 — Mốc ngày tồn đầu kỳ: sửa được trên cổng DQG, và test đẩy bù ở local — @cuong61n

- [x] **Đo quy tắc ngày chứng từ trên sandbox DQG** (cơ sở 945). Bộ nhận chứng từ
  ngày quá khứ, nhưng chỉ trong khoảng `[ngày phiếu tồn đầu kỳ … hôm nay]`:
  hôm nay / lùi 7 ngày / lùi 3 tháng đều `Completed`; 01/01/2026 và 01/06/2025
  trả `Error` "Ngày nhập không được nhỏ hơn ngày nhập phiếu tồn đầu"; ngày tương
  lai trả `Error` "Ngày tạo phiếu phải nhỏ hơn hoặc bằng ngày hiện tại". Dò nhị
  phân ra mốc chặn của cơ sở 945 nằm giữa 15/07 và 01/08/2026.
- [x] **Phiếu tồn đầu kỳ SỬA ĐƯỢC ngày trên cổng DQG** — điều chỉnh kết luận trước
  đó (tưởng là chặn dưới vĩnh viễn). Vào `web-sandbox.csdlduoc.com.vn` bằng
  Playwright, phiếu nằm ở Nghiệp vụ bán hàng ▸ Nhập hàng, loại `102 Phiếu nhập tồn`
  (mã `5`), mở bằng route `/app/shop/stock/import/update/{idHash}` → ô "Ngày nhập"
  cho sửa dù phiếu đã Hoàn thành. Đã đổi 01/08/2026 → **01/01/2026**, bấm Hoàn thành,
  lưu thành công.
  - Kiểm chứng sau khi sửa: gửi stock-in ngày 15/03/2026 → `Completed` (trước đó
    cùng khoảng này bị chặn); ngày 20/12/2025 → vẫn `Error` đúng thông điệp cũ.
    Mốc chặn đã lùi về đúng ngày mới. Một phiếu ngày 05/01/2026 kẹt `Accepted`
    suốt 2,5 phút không ra kết quả — chưa rõ vì sao, chưa ảnh hưởng kết luận.
  - **Hệ quả nghiệp vụ**: khách lỡ khai tồn đầu kỳ ngày hôm nay vẫn cứu được bằng
    cách sửa ngày trên cổng DQG, không mất vĩnh viễn đường đẩy bù như lo ban đầu.
- [x] **Test chức năng đẩy bù hoá đơn cũ ở local** (nhánh `dqg`, cơ sở 797, PHP 7.4,
  `CSDLDUOC_ENV=sandbox`). Màn Tồn đầu kỳ & đẩy bù đã có sẵn ô chọn ngày mốc, nút
  Lưu mốc / Kiểm tra trước / Đẩy bù chứng từ / Tạm dừng.
  - Luồng đủ: "Kiểm tra trước" đếm đúng 2 chứng từ cần đẩy → bấm "Đẩy bù chứng từ"
    xếp đợt (`Đang đẩy 0/2`) → chạy `artisan csdlduoc:replay-run` gửi 2/2, 0 lỗi →
    màn tự cập nhật `Hoàn tất 2/2` → `artisan csdlduoc:poll` trả 2 `completed`,
    bộ đếm trên màn nhảy từ 45 lên 47 thành công.
  - **Chứng từ đẩy bù vào thẳng tab "Theo dõi liên thông"**, dùng chung nhật ký với
    luồng gửi thường — cột "Ngày chứng từ" giữ ngày gốc quá khứ (30/09, 07/10/2026),
    cột "Gửi lúc" là hôm nay. Tester theo dõi ở cùng một chỗ, không cần màn riêng.
  - Nhánh lỗi: bấm Đẩy bù khi không còn gì → toast "Không còn chứng từ nào cần đẩy
    trong kỳ", đúng. Ô chọn ngày đã chặn sẵn ngày tương lai bằng `disabledDate`.
  - Điểm nhỏ còn lại: `batDau()` ở `CsdlDuocReplay.jsx` không `catch`, nên lỗi từ
    `replayStart` sinh unhandled promise rejection trong console (người dùng vẫn
    thấy toast do `sendRequest` tự báo). Chưa sửa.
  - Dữ liệu test: đã gỡ tạm nhật ký 2 chứng từ của cơ sở 797 để dựng ca, có sao lưu,
    xong đã dọn bảng tạm. **Đã đổi mật khẩu tài khoản `sphlinhbinhduong` trên DB
    local** (`sphacy_prod_local`) để đăng nhập test — hash cũ không giữ lại.

## 09/11/2026 (chiều) — Đẩy nhánh dqg lên cổng test, test GPP + GDP, vá lỗi đợt đẩy bù lặp vô hạn — @cuong61n

- [x] **Deploy BE lên cổng test** (42.96.40.67). Server test vốn ở `7ff0699`, thiếu hẳn
  chức năng đẩy bù. Remote git trên server tên là `github` (không phải `origin`) và
  không có credential, nên đẩy bằng **git bundle**: tạo bundle nhánh `dqg` ở máy,
  scp sang `/tmp`, `git fetch /tmp/dqg.bundle`, `reset --hard`. Đã tạo nhánh sao lưu
  `bak-truoc-day-bu-20261109` trỏ về `7ff0699` trước khi reset.
  - `artisan migrate` toàn bộ bị vướng migration cũ (`control_quality_books` đã tồn tại),
    và `--path` trỏ thẳng một file thì Laravel 5.6 báo "Nothing to migrate" — phải gom
    3 file vào thư mục tạm rồi `--path=` thư mục đó. Chạy xong cả 3, đã xoá thư mục tạm.
- [x] **Deploy FE GPP + GDP lên cổng test**, bản cũ sao lưu `build.bak-20261109` ở cả hai.
- [x] **Sửa ngày phiếu tồn đầu kỳ của cơ sở GDP trên DQG**: cơ sở 1706 (tài khoản
  `0314345936`) có mốc **01/07/2026**, nếu để nguyên thì mọi chứng từ nửa đầu năm bị
  Bộ từ chối. Đã sửa về 01/01/2026, giống cơ sở GPP.
- [x] **LỖI THẬT phát hiện khi test: đợt đẩy bù lặp vô hạn.** Đợt của cơ sở 945 kẹt
  "Đang đẩy", cron mỗi phút chạy lại một lượt, `skipped_count` tăng mãi (2→3→5) mà
  `con_lai` không bao giờ về 0.
  - Nguyên nhân: hoá đơn `PN374594` chỉ có BIOTIN 5 MG, số đăng ký `80/2019/ĐKSP` —
    thực phẩm chức năng, ngoài diện liên thông. `InvoicePusher::push()` trả `null` và
    **không ghi gì vào `csdlduoc_transactions`**, trong khi `danhSachChungTu()` nhận
    biết việc còn lại bằng `whereNull('t.id')` → lượt sau nhặt lại đúng phiếu ấy.
  - Mức nghiêm trọng: nhà thuốc nào cũng bán TPCN, nên gặp ở gần như mọi cơ sở; cron
    quay vô ích mỗi phút và đợt không bao giờ kết thúc.
  - Đã sửa 3 chỗ:
    1. `CsdlDuocTransaction`: thêm `STATUS_OUT_OF_SCOPE = 'skipped_out_of_scope'`,
       tính vào `isFinal()`.
    2. `CsdlDuocReplayer::ghiDauNgoaiPhamVi()` — ghi một dòng nhật ký khi `push()` trả
       null. Cột `endpoint`/`reason` là NOT NULL nên suy từ loại phiếu bằng
       `CsdlDuocMapper::resolveEndpointAndReason($row->loai, $drugStore->type)`
       (lần đầu để null đã nổ `SQLSTATE[23502]`).
    3. `ketQuaTheoNhatKy()` đếm `skipped_out_of_scope` **và** `cancelled_local` vào
       "bỏ qua" — trước đó cả hai rơi nhầm vào "đang chờ duyệt".
    4. FE `CsdlDuocConnect.jsx`: nhãn "Ngoài diện liên thông", không cho gửi lại.
  - Sau khi vá: `còn 0 — Đợt đã hoàn tất`; nhật ký ghi
    `PN374594 | stock-in | supplier | skipped_out_of_scope`.
- [x] **Test đủ luồng trên cổng test, cả hai nhánh:**
  - **GPP (cơ sở 945)**: lưu mốc 01/01/2026 → toast đúng, tự thống kê "1 chứng từ cần
    đẩy" kèm cảnh báo 2 thuốc chưa liên kết (Pantoloc 40mg `VN-18402-14`, TROPIUSPHA
    SLIM `06/U.SPHAR/2020`) → đẩy bù → đợt `done`, bỏ qua 1 (phiếu TPCN).
  - **GDP (cơ sở 1706)**: lưu mốc → cảnh báo 1 thuốc chưa liên kết → đẩy bù → **cron tự
    chạy** (15:11:57→15:12:04) gửi 1/1, 0 lỗi → Bộ duyệt `completed` cho phiếu
    **ngày 02/08/2026**, tức chứng từ quá khứ đẩy bù thành công thật.
  - Cả hai nhánh: chứng từ đẩy bù hiện ở tab Theo dõi liên thông, cột "Ngày chứng từ"
    giữ ngày gốc quá khứ, cột "Gửi lúc" là hôm nay.
  - Trạng thái: code sửa mới **copy file lên server test, CHƯA commit** — chờ xác nhận.
  - FE: lý do của phiếu "Ngoài diện liên thông" hiện ở cột *Lý do bị từ chối* nên để
    chữ xám thay vì đỏ — chữ đỏ khiến dược sĩ tưởng Bộ từ chối và đi tìm cách gửi lại.
  - Dọn dẹp sau test: 2 chứng từ của cơ sở 1706 đã được gửi lại và `completed`, bảng
    sao lưu `csdlduoc_tx_bak_test20261109` đã xoá; mật khẩu `duocsi1` và
    `demo.sphacygdp` **đã khôi phục đúng hash cũ**.
  - **Bẫy đã dính**: khôi phục hash bcrypt bằng `psql -c "... '$2y$10$...'"` qua ssh thì
    shell nuốt mất `$2`/`$10`, hash bị cắt còn 13 ký tự và tài khoản hỏng. Phải viết
    file `.sql` (nháy đơn) rồi `scp` sang và `psql -f`. Đã kiểm lại `length(password)=60`.

## 09/11/2026 — Dựng sẵn ca test trên cổng test để bàn giao tester — @cuong61n

- [x] Sau khi tôi test xong thì hai cơ sở không còn chứng từ nào chờ đẩy, tester vào sẽ
  chỉ thấy "Không còn chứng từ nào cần đẩy trong kỳ". Đã gỡ tạm nhật ký 7 bản ghi để
  tester có việc mà bấm (sao lưu ở bảng `csdlduoc_tx_bak_kiet`, khôi phục được):
  - **GPP cơ sở 945 — 4 chứng từ**: 3 phiếu nhập `PN374606`, `PN374602`, `PN374595`
    cộng phiếu `PN374594` (chỉ có BIOTIN 5 MG, TPCN) để tester thấy luôn nhánh
    "Ngoài diện liên thông" của bản vá.
  - **GDP cơ sở 1706 — 3 chứng từ**: `PN374635`, `PN374629`, `PN374628`.
  - Chỉ chọn **phiếu nhập**: phiếu bán gửi lại dễ bị Bộ trả "không đủ tồn kho", tester
    sẽ tưởng là lỗi phần mềm.
- [x] Kiểm trên giao diện cổng test: GPP hiện "4 chứng từ cần đẩy", GDP hiện "3 chứng
  từ cần đẩy", kèm cảnh báo thuốc chưa liên kết. Mốc 01/01/2026 đã lưu sẵn cho cả hai.
- [x] Mật khẩu `duocsi1` / `demo.sphacygdp` đã đối chiếu **khớp từng byte** với hash gốc.
- **Nhắc tester**: FE có service worker, lần đầu mở phải Ctrl+Shift+R nếu thấy bản cũ.
- **CHƯA LÀM — rủi ro**: bản vá lỗi đợt đẩy bù lặp vô hạn mới chỉ là file copy lên server
  test, **chưa commit vào nhánh `dqg`**. Ai deploy lại hoặc `git reset` trên server test
  là mất vá và lỗi quay lại ngay giữa lúc tester đang chạy.

## Còn lại

- 43 bản ghi danh mục Bộ không trả được (lỗi bên họ, hỏi lẻ từng bản ghi vẫn rỗng).
  Chờ Bộ sửa dữ liệu; cron 03:00 tự nạp lại nên sẽ tự có khi họ sửa. Nếu khách gặp
  thuốc không tìm thấy trong danh mục thì khả năng cao thuộc nhóm này.
- Tab "Tồn đầu kỳ & đẩy bù" còn trên nhánh `dqg`, chờ tester chạy trên cổng test trước
  khi mở ở cổng chính.
- Chưa làm: cảnh báo/gửi điều chỉnh khi hoá đơn bị sửa sau khi đã liên thông.
