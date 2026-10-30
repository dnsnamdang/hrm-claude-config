---
name: app-build-release
description: Build và phát hành TPE_APP — IPA lên TestFlight, APK/AAB lên CH Play. Dùng khi user nói "build app", "đẩy lên TestFlight", "build iOS/Android", "release bản mới", "lên store", hoặc khi gặp lỗi ký app / lỗi upload.
---

# Build & Release TPE_APP

Repo Flutter đa flavor (14 flavor, mỗi flavor là 1 app riêng trên store). Bắt buộc xác định **đúng flavor** trước khi làm bất cứ việc gì.

## 0. Nhánh theo khách hàng — BUILD ĐÚNG NHÁNH

Từ 13/10/2026 repo tách nhánh theo khách hàng (nguồn: sheet "Tài khoản HRM"). Build/phát hành app nào thì **checkout đúng nhánh của app đó**, sửa code chung thì làm ở `develop` rồi merge sang các nhánh khách.

| Nhánh | Server HRM | App (flavor) |
|---|---|---|
| `develop` (nhánh dev) | dev-hrm.eteksofts.com | Tân Phát ERP-HRM (`tpeDev`) |
| `tpe` | hrm.eteksofts.com, hrm.etek.com.vn, hrm.etekpower.com.vn, hrm.kasaco.com.vn, hrm.toyotasonglam.info, hrm.zitecgroup.com, ori.eteksofts.com | HRM TPE (`tpeProd`), ETEK (`etek`), ETEK POWER (`etekPower`), HRM Kasaco (`kasaco`), Toyota Sông Lam (`toyotasonglam`), ZITEC (`zitec`), ORI HRM (`ori`) |
| `duclocson` | hrm.duclocson.vn | HRM Duclocson (`duclocson`) |
| `thanhan` | demothanhan.dnsmedia.vn, hrm.matviethanoi.vn | ERP THÀNH AN (`thanhan`), Mắt Việt Hà Nội (`matviethn`) |

- Mỗi nhánh vẫn giữ code + cấu hình của MỌI flavor (không xoá flavor khác) — nhánh chỉ quyết định app nào được build từ đây.

### Quan hệ giữa các nhánh — CHỈ `develop` ↔ `tpe` liên thông

```
develop ──merge──▶ tpe            (cặp liên thông: dev là nơi phát triển cho TPE)
duclocson                         (độc lập — không nhận / không cho code nhánh nào)
thanhan                           (độc lập — không nhận / không cho code nhánh nào)
```

User nói "sửa nhánh X" thì:

| Yêu cầu | Làm gì | KHÔNG làm |
|---|---|---|
| Sửa `develop` / "sửa dev" | commit vào `develop`, rồi `git checkout tpe && git merge develop` (nhánh TPE luôn nhận code dev) | merge sang `duclocson`, `thanhan` |
| Sửa `tpe` | commit vào `tpe`, rồi merge ngược `tpe` → `develop` để dev không lạc hậu | merge sang `duclocson`, `thanhan` |
| Sửa `duclocson` | commit CHỈ vào `duclocson` | merge/cherry-pick sang bất kỳ nhánh nào; merge nhánh khác vào nó |
| Sửa `thanhan` | commit CHỈ vào `thanhan` | merge/cherry-pick sang bất kỳ nhánh nào; merge nhánh khác vào nó |

- Muốn đưa 1 sửa lỗi sang `duclocson`/`thanhan` → CHỈ khi user nói rõ, và dùng `git cherry-pick <commit>` từng commit, KHÔNG `git merge` (merge kéo theo toàn bộ code TPE).
- Trước khi sửa: `git -C TPE_APP status` phải sạch, `git checkout <nhánh>` + `git pull --ff-only`. Sửa xong mới đổi nhánh — đổi nhánh khi còn file sửa dở là mang thay đổi sang nhánh khác.
- Commit/push theo quy tắc chung: chỉ khi user yêu cầu.
- Gia hạn TestFlight KHÔNG phụ thuộc nhánh đang checkout: skill `testflight-renew` lấy script từ `origin/develop` chép ra `~/.tpe-testflight-renew/bin`, build trong worktree riêng ở đúng commit của bản đang chạy.
- ETEK GREEN (`etekGreen`) đã NGỪNG dùng (13/10/2026) — không build, không gia hạn.
- `ori`, `zitec` build từ nhánh `tpe` (user chốt 19/10/2026).
- Bump version cho app nào thì commit vào nhánh của app đó (script gia hạn TestFlight dò commit phát hành theo nhánh này — bảng `BRANCH_OF` trong `scripts/build/testflight_renew.sh` phải khớp bảng trên).

## 1. Xác định flavor

Hỏi user tên app trên store, rồi tra bảng. Nếu user chỉ đưa link App Store Connect → mở app đó → **App Information** → lấy **Bundle ID** → tra cột 2.

| App trên store | Bundle ID | flavor | File version iOS | Tên IPA sinh ra |
|---|---|---|---|---|
| Tân Phát ERP-HRM | `com.tanphat.erp.hrm.app` | `tpeDev` | `TpeDev.xcconfig` | `Tân Phát ERP-HRM.ipa` |
| HRM TPE | `com.tanphat.soft.app` | `tpeProd` | `TpeProd.xcconfig` | `HRM TPE.ipa` |
| Etek | `com.wt.wetek.app` | `etek` | `Etek.xcconfig` | `Etek.ipa` |
| Etek Green | `com.wetek.app.app` | `etekGreen` | `EtekGreen.xcconfig` | — |
| ETEK POWER (tên cũ Tân Phát 686) | `com.tanphat686.app` | `etekPower` | `EtekPower.xcconfig` | `ETEK POWER.ipa` |
| HRM Duclocson | `com.duclocson.app` | `duclocson` | `Duclocson.xcconfig` | `HRM Duclocson.ipa` |
| HRM Kasaco | `com.kasaco.hrm.app` | `kasaco` | `Kasaco.xcconfig` | — |
| Ori | `com.eteksofts.ori` | `ori` | `Ori.xcconfig` | — |
| Thành An | `com.tanphat.thanhan` | `thanhan` | `Thanhan.xcconfig` | — |
| Mắt Việt Hà Nội | `com.matviethn.hrm.app` | `matviethn` | `MatVietHN.xcconfig` | — |
| Toyota Sông Lam | `com.toyota.songlam.app` | `toyotasonglam` | `ToyotaSongLam.xcconfig` | — |
| Zitec | `com.zitecgroup.hrm.app` | `zitec` | `Zitec.xcconfig` | — |

Danh sách flavor hợp lệ nằm ở `makes/makefile.common` biến `ValidEnvs`.

## 2. Kiểm tra môi trường trước khi build

```bash
fvm flutter --version    # phải là 3.41.7 (khớp .fvmrc), KHÔNG phải flutter global
```

- Repo dùng `fvm`, mọi lệnh trong makefile gọi `fvm flutter`. Chưa có fvm → `brew tap leoafarias/fvm && brew install fvm && fvm use 3.41.7`
- Máy này flutter global là 3.22.3 — chạy `flutter` trần sẽ sai version, lỗi khó hiểu
- Android: `gradle.properties` hard-code `org.gradle.java.home` trỏ path không tồn tại trên máy này. Gọi `gradlew` trực tiếp phải override **cả hai**, thiếu 1 trong 2 là fail:
  ```bash
  JAVA_HOME=/Users/manhcuong/Library/Java/jdk17 \
    ./gradlew -Dorg.gradle.java.home=/Users/manhcuong/Library/Java/jdk17 <task>
  ```
  Chỉ đặt `GRADLE_OPTS` → lỗi *"Unable to locate a Java Runtime"* (launcher chưa có JVM).
  Chỉ đặt `JAVA_HOME` → lỗi *"Java home supplied is invalid"* (vẫn đọc giá trị hỏng trong file).
  Với `make release_aab` (đi qua flutter tool) thì chưa kiểm chứng cách nào đúng — thử `GRADLE_OPTS` trước, hỏng thì sửa tạm `gradle.properties` ở local (đừng commit).

## 3. Bump version — BẮT BUỘC, store chặn trùng build number

Xem build number cao nhất đang có: App Store Connect → app → **TestFlight** → cột VERSION & BUILD.

Sửa **2 chỗ cho cùng flavor**, giữ 2 nền tảng đồng bộ:

- iOS: `app/ios/Flutter/<Flavor>.xcconfig` → `FLUTTER_BUILD_NAME` (tên phiên bản) + `FLUTTER_BUILD_NUMBER`
- Android: `app/android/app/build.gradle` → khối flavor tương ứng → `versionName` + `versionCode`

Chỉ build iOS thì chỉ cần sửa xcconfig, nhưng nên hỏi user có muốn đồng bộ Android luôn không.

## 4. Build iOS + upload TestFlight

```bash
cd <repo>
fvm flutter pub get                    # trong app/
cd app/ios && pod install              # PHẢI chạy ngoài sandbox (xem mục Bẫy)
cd <repo>
make fix_pod_release                   # bỏ comment dòng EXCLUDED_ARCHS cho Mapbox
make build_tpeDev_ipa                  # đổi tpeDev thành flavor cần build
make upload_tpeDev                     # đổi tpeDev thành flavor cần build
```

- `make release_ipa env=tpeDev` gộp cả build + copy vào `output/` + upload trong 1 lệnh
- **KHÔNG dùng** `make setup_soft` / `make clean` nếu muốn giữ `pubspec.lock` — target `cl` có `rm -rf pubspec.lock`, lock file này được commit để pin version, xoá đi sẽ resolve lại và dễ vỡ (đã từng vỡ với `wakelock_plus 1.4.0`)
- **KHÔNG dùng** các lane fastlane iOS (`make cd_erp`, `cd_prod`…) — chúng cần file `AuthKey_*.p8` không có trong repo

Upload cần 2 biến môi trường (makefile đã bỏ hard-code):

```bash
export APPLE_ID="ban@example.com"
export APPLE_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"   # app-specific password
```

Tài khoản phải có quyền **Upload builds** trên App Store Connect (Admin / App Manager / Developer).

Kiểm tra kết quả: App Store Connect → app → TestFlight → build mới ở trạng thái *Processing* → 10–30 phút sau thành *Complete* → gán nhóm tester.

## 4b. Gia hạn TestFlight (build hết hạn sau 90 ngày)

Apple không cho kéo dài hạn của 1 build — chỉ có cách upload lại **cùng code + cùng version** với build number +1. Làm **khi user gọi** qua skill cá nhân `testflight-renew` (`~/.claude/skills/testflight-renew/SKILL.md`): Playwright vào App Store Connect check hạn 9 app → app còn ≤ 15 ngày thì chạy `scripts/build/testflight_renew.sh --force <flavor...>` → gán nhóm external + gửi duyệt. KHÔNG có lịch tự động (đã gỡ lịch launchd 13/10/2026 theo yêu cầu user).

- **File trạng thái là nguồn sự thật**: `~/.tpe-testflight-renew/state/<flavor>.env` gồm `LAST_UPLOAD_DATE`, `LAST_VERSION`, `LAST_BUILD` (build lớn nhất đã upload), `RELEASE_REF` (commit code của bản đang chạy). Script build lại `RELEASE_REF` với đúng `LAST_VERSION`, KHÔNG tin version trong xcconfig — có lúc dev upload với version sửa tay chưa commit (duclocson 2.1.5(24), thanhan 2.1.6(171) build từ `eec2f00` nhưng xcconfig trên nhánh vẫn ghi bản cũ)
- Build trong worktree riêng `~/.tpe-testflight-renew/worktree` → không đụng thư mục code; log ở `~/.tpe-testflight-renew/logs/`
- Phát hiện bản mới: commit đổi xcconfig trên nhánh KHÔNG nằm trong lịch sử của `RELEASE_REF` (so bằng git, không so ngày vì TestFlight ghi UTC còn git ghi giờ VN)

```bash
make renew_testflight env=etekPower args=--dry-run   # build thử, không upload
make renew_testflight env=etekPower args=--force     # gia hạn ngay
```

⚠️ Upload bằng app-specific password KHÔNG gán được build vào nhóm tester **external** — nhóm internal tự nhận build mới, nhóm external phải gán tay (hoặc chuyển sang App Store Connect API key).

Gán tay (đã làm với ETEK POWER 12/10/2026, nhóm external "Tân Phát" 58 tester qua public link): App Store Connect → app → TestFlight → nhóm external → tab **Builds** → nút ➕ **Add Build to Group** → chọn build mới (trạng thái *Ready to Submit*) → **Next** → điền "What to Test" (ô contenteditable, phải bấm vào rồi gõ) → **Submit for Review**. Build cùng phiên bản với build đã duyệt thì Beta App Review duyệt ngay, lên *Testing* trong vài giây.
Mẹo Playwright: vào URL trang TestFlight trực tiếp hay bị trắng trang / bảng build kẹt khung xám → bấm lại tab **TestFlight** hoặc vào thẳng trang nhóm.

**Gán nhanh bằng API nội bộ (đã dùng 13/10/2026 cho 6 app, chạy trong trang App Store Connect đã đăng nhập qua `browser_evaluate`)** — 3 request cho mỗi build:
1. Ghi chú: `GET /iris/v1/builds/<buildId>/betaBuildLocalizations` → `PATCH /iris/v1/betaBuildLocalizations/<id>` `{data:{type:'betaBuildLocalizations',id,attributes:{whatsNew}}}`
2. Gán nhóm: `POST /iris/v1/betaGroups/<groupId>/relationships/builds` `{data:[{type:'builds',id:buildId}]}` → 204
3. Gửi duyệt: `POST /iris/v1/betaAppReviewSubmissions` `{data:{type:'betaAppReviewSubmissions',relationships:{build:{data:{type:'builds',id:buildId}}}}}` → 201, vài giây sau APPROVED

Tìm buildId: `GET /iris/v1/builds?filter[app]=<AppleID>&filter[version]=<build number>` (phải `processingState=VALID`). Tìm nhóm: `GET /iris/v1/apps/<AppleID>/betaGroups` (`isInternalGroup=false` = external).

| App | Apple ID | Nhóm external (groupId) |
|---|---|---|
| Tân Phát ERP-HRM | 6473664189 | — (xem lúc cần) |
| HRM TPE | 6446807087 | — (xem lúc cần) |
| ETEK | 6443813628 | Tân Phát `35e1bc79-4447-4aa3-ae87-158b3ca6e8f0` |
| ETEK POWER | 6470713565 | Tân Phát `aa99b6d4-4651-4514-8427-d87692dcc2a5` |
| HRM Kasaco | 6749338423 | kasaco_group `80ca9b49-da93-4e23-94df-04f17a114bdd` |
| Toyota Sông Lam | 6755413393 | toyota-songlam-group `e67ba2d0-d5dd-4470-8da9-ff066bc97a82` |
| HRM Duclocson | 6470713761 | Tân Phát `b484fa12-5037-47fa-855a-8862569674e0` |
| ERP THÀNH AN | 6517358820 | Tân Phát `133966b7-1c65-4749-b4b0-addd80b3f1a6` |
| Mắt Việt Hà Nội | 6751868013 | users `71b12651-3888-463b-87a6-da13b79425e5` (nhóm internal "internal" không tự nhận build) |

## 5. Build Android + CH Play

```bash
GRADLE_OPTS="-Dorg.gradle.java.home=/Users/manhcuong/Library/Java/jdk17" make release_aab env=tpeDev
```

Nếu báo lỗi Java home, xem lại mục 2 — cách override đúng khi gọi `gradlew` trực tiếp.

Ra file `output/<flavor>-release.aab`. Upload **thủ công** qua Play Console (fastlane Android trong repo chỉ build, không upload).

### Keystore (đã có sẵn trên máy này)

Keystore dùng CHUNG cho cả 13 app (đã đối chiếu SHA-1 giống nhau), lưu ngoài repo tại `~/.keystores/tanphat.jks`. Khai sẵn trong `app/android/local.properties` (file gitignore):

```
keystore.keyAlias=key0
keystore.keyPassword=<hỏi chủ repo>
keystore.storeFile=/Users/manhcuong/.keystores/tanphat.jks
keystore.storePassword=<hỏi chủ repo>
```

- alias `key0`, mật khẩu store/key KHÔNG ghi vào repo — lấy trong `app/android/local.properties` của máy build, hạn tới 2046
- Upload key SHA-1 (để đối chiếu khi cần): `65:1B:10:97:59:99:2E:89:87:D8:BC:8D:DF:BD:CA:1A:61:FE:FA:F8`
- Kiểm keystore: `~/Library/Java/jdk17/bin/keytool -list -v -keystore ~/.keystores/tanphat.jks -storepass "$(grep storePassword app/android/local.properties | cut -d= -f2)"`
- Verify AAB đã ký đúng: `~/Library/Java/jdk17/bin/keytool -printcert -jarfile output/<flavor>-release.aab | grep SHA1` — phải khớp SHA-1 trên
- ⚠️ KHÔNG commit keystore vào repo (đã từng lọt file `app/android/mykey` ở commit init, đã gỡ). File ký app lọt git = ai clone cũng ký giả được app.

### Upload lên CH Play (qua Playwright, cần user đã đăng nhập Play Console)

Các app đều bật **Play App Signing** — mất upload key vẫn xin Google reset được, không mất app.

1. Play Console → chọn app → **Kiểm thử và phát hành → Phát hành công khai** (hoặc kênh thử nghiệm)
2. Nút **Tạo bản phát hành mới** → mục "Tải gói ứng dụng lên" → nút **Tải lên** (cái đầu tiên, KHÔNG phải ô .obb) → chọn file `.aab` (dùng `browser_file_upload`)
3. Điền **Ghi chú phát hành** trong ô ngôn ngữ `vi-VN`
4. **Tiếp theo** → trang "Xem trước và xác nhận" → nút **Lưu** (chỉ lưu nháp, CHƯA gửi)
5. Về trang **Tổng quan về việc xuất bản** → nút xanh **"Gửi N nội dung thay đổi để được xem xét"** ← đây mới là bước phát hành thật
6. "Chế độ xuất bản có quản lý đang tắt" → Google duyệt xong (vài giờ–2 ngày) tự phát hành, không cần bấm thêm

⚠️ Bước 5 (gửi xem xét) và phát hành production ra người dùng thật: DỪNG hỏi user trước khi bấm, trừ khi user đã nói rõ "phát hành luôn".

**App IDs Play Console** (developer account `5922695385085302551` — CÔNG TY CỔ PHẦN CÔNG NGHỆ THIẾT BỊ TÂN PHÁT):
- HRM TPE (`com.tanphat.soft.app`, flavor `tpeProd`) = `4974399943846500168` — app chính, đang live 292+ user
- Lưu ý: app `tpeDev` (`com.tanphat.erp.hrm.app`) trên Play đang **huỷ xuất bản, 0 user** → KHÔNG build CH Play cho flavor tpeDev (user đã xác nhận). tpeDev chỉ build iOS.

## 6. Ký app iOS — điểm hay tắc nhất

**Tài khoản Apple Developer của team là loại Individual (cá nhân, team name `Dang Nguyen`, Team ID `54UWG4H5CH`).**

Hệ quả: **chỉ chủ tài khoản `namdangit@gmail.com` tạo được chứng chỉ ký.** Tài khoản khác dù là Admin trên App Store Connect vẫn KHÔNG có quyền Certificates, Identifiers & Profiles — đây là giới hạn của tài khoản Individual, không phải lỗi phân quyền, và **không có cách nào cấp quyền đó qua App Store Connect** (giao diện không có tuỳ chọn nào cho Certificates).

Dấu hiệu nhận biết:
- `developer.apple.com/account` hiện banner *"Join the Apple Developer Program — Enroll today"*
- Xcode → Settings → Apple Accounts hiện dòng **❌ Certificates, Identifiers, & Profiles** (X đỏ) dù Role là Admin
- `security find-identity -v -p codesigning` → `0 valid identities found`

**Cách xử lý:** đăng nhập Apple ID `namdangit@gmail.com` vào Xcode → Settings → Apple Accounts. Sau đó **không cần bấm gì thêm** — khi chạy `make build_*_ipa`, xcodebuild tự cấp phát cloud-managed distribution certificate và provisioning profile. (Trong Keychain sẽ chỉ thấy cert *Apple Development*; private key phân phối nằm phía Apple — đúng, không phải thiếu.)

**Không muốn phụ thuộc phiên đăng nhập Xcode (hay tự hết hạn → `exportArchive No Accounts`):** tạo khoá App Store Connect API (Users and Access → Integrations → Team Keys, quyền Admin), lưu `.p8` ngoài repo và khai `~/.asc_api.env`:

```bash
ASC_KEY_ID=XXXXXXXXXX
ASC_ISSUER_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
ASC_KEY_PATH=$HOME/.appstoreconnect/private_keys/AuthKey_XXXXXXXXXX.p8
```

Có file này thì `tools/build_and_run_app.sh` tự xuất lại IPA bằng `xcodebuild -exportArchive -allowProvisioningUpdates -authenticationKey*` sau bước archive. Không có thì chạy như cũ (cần Xcode đăng nhập). `make upload_*` cũng tự upload bằng khoá (`altool --apiKey`), không cần `APPLE_ID` / `APPLE_APP_PASSWORD` → `make release_ipa env=<flavor>` chạy trọn 1 lệnh.

Kiểm chứng IPA đã ký chuẩn App Store:

```bash
unzip -p "<file>.ipa" 'Payload/*.app/embedded.mobileprovision' | security cms -D | plutil -extract Name raw -
# phải ra: iOS Team Store Provisioning Profile: <bundle id>
```

Phân biệt rõ 2 quyền, đừng nhầm:
- **Upload build** → cần quyền trên App Store Connect (Admin/App Manager/Developer đều được) → tài khoản thường của dev là đủ
- **Ký app** → cần Developer Program membership → chỉ chủ tài khoản Individual

## 7. Bẫy đã gặp

| Bẫy | Xử lý |
|---|---|
| `pod install` chết ở `MapboxCommon` | Sandbox mạng của Claude Code chặn `api.mapbox.com` → chạy với `dangerouslyDisableSandbox: true`, hoặc để user tự chạy trong terminal |
| Gradle lỗi JDK không tồn tại | `gradle.properties` hard-code `org.gradle.java.home` của máy khác → override, xem mục 2 (phải có cả `JAVA_HOME` lẫn `-Dorg.gradle.java.home`) |
| `altool` lỗi `-22938` | Sai app-specific password. Tạo lại tại account.apple.com, **copy chứ đừng gõ tay** (dễ nhầm `u`/`v`, `k`/`h`, `y`/`g`) |
| `altool` lỗi `-19237`, server trả HTML | Thông tin đăng nhập chết hẳn (password bị revoke) |
| Cảnh báo hàng loạt `CocoaPods did not set the base configuration` | Bình thường với repo đa flavor, KHÔNG phải lỗi |
| `flutter` chạy sai version | Quên `fvm`, xem mục 2 |
| Token Mapbox | Đã bỏ khỏi `app/android/gradle.properties`, mỗi máy tự khai `MAPBOX_DOWNLOADS_TOKEN` trong `~/.gradle/gradle.properties` |

**Upload iOS đã chạy được (thay cho `make upload_*`):** app-specific password của `cuong61n@gmail.com` lưu ở `~/.asc_pw`. Lệnh trực tiếp, đọc pass từ file (không hiện ra):
```bash
xcrun altool --upload-app --type ios -f "app/build/ios/ipa/<Tên App>.ipa" \
  -u "cuong61n@gmail.com" -p "$(cat ~/.asc_pw)"
```
Tên IPA lấy từ bảng mục 1. Sau upload, build hiện ở TestFlight sau 5–30 phút (Processing → Complete). Nếu pass hết hạn (lỗi -22938): tạo lại tại account.apple.com → Sign-In and Security → App-Specific Passwords, lấy giá trị TỪ DOM (`browser_snapshot`) để không nhầm ký tự, ghi đè `~/.asc_pw`.
`make upload_*` giờ đọc `$APPLE_ID`/`$APPLE_APP_PASSWORD` (env), KHÔNG còn hard-code.

## 8. Nguyên tắc

- **Upload là hành động ra ngoài** (tester thấy ngay) → luôn hỏi user xác nhận trước khi chạy `make upload_*`
- Không commit/push — theo quy tắc chung của project
- Build IPA mất ~6 phút (archive 250s + export 90s), upload ~3s cho file 50MB. Chạy nền, đừng chờ đồng bộ
