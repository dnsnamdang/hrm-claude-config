# GĐ11 Chat — Báo lỗi màn hình

> 14/11/2026 · @namdangit · Trạng thái: ĐÃ DEPLOY TPE 14/11 (api 86fcb16ba · client 814664a79). Tên hiển thị đổi thành **"YC hỗ trợ" / "Yêu cầu hỗ trợ"** (mã, route, tên file giữ chữ bug-report / bao_loi).
> Mockup đã chốt: `mockup.html` (cùng thư mục). Ảnh trong `img/` chụp từ app thật :3080.
> Thuộc nhóm AGENT + CHAT (`.plans/agent-chat/README.md`). Code tách nhánh từ `origin/gop_db`.

## 1. Vì sao làm

Phần mềm còn đang phát triển nên các phân hệ thỉnh thoảng gặp lỗi trên prod. Hiện người dùng chỉ báo "bị lỗi",
và dev phải tự dựng lại bối cảnh (ultrareview, đọc log) để biết lỗi ở màn nào, ai gặp, lúc nào, API nào hỏng.
Phần lớn thời gian mất vào việc dò, không phải vào việc sửa.

**Thành công =** mỗi báo cáo tới tay dev/hỗ trợ đã đủ bối cảnh để bắt tay xử lý ngay, không phải hỏi lại
"màn nào, lọc gì, báo lỗi gì". Người báo theo dõi được tiến độ xử lý.

"Lỗi" ở đây gồm cả **lỗi hệ thống** (báo lỗi, trắng trang, bấm không chạy) lẫn **số liệu sai** và **thông tin sai**
(không có lỗi kỹ thuật nào, chỉ là dữ liệu hiển thị không đúng).

## 2. Mục tiêu · Không làm · Không được để xảy ra

**Mục tiêu**
- Nút báo lỗi có trên **mọi màn** của hrm-client, nhỏ gọn nhất có thể.
- Bấm là có ngay ảnh chụp trang đang thấy, cùng một popup ngắn: loại · mô tả · gửi tới · thông tin tự gom.
- Báo cáo vào chat nội bộ ("Không gian trao đổi công việc") dưới dạng một tin nhắn đặc biệt, giữ được trao đổi
  tiếp và tạo nhiệm vụ cho dev bằng tính năng có sẵn.
- Hệ thống **tự gom** những thứ người dùng không tự ghi được: URL + bộ lọc, các lỗi API gần nhất, thông báo lỗi vừa
  hiện, công ty đang chọn, thiết bị, phiên bản client.

**Không làm (đợt này)**
- Nút báo lỗi trong app mobile / app desktop. API làm dùng chung được, nhưng giao diện app để sau.
- Màn quản lý / thống kê báo lỗi riêng (danh sách, lọc theo trạng thái…). Theo dõi bằng nhóm chat + nhiệm vụ.
- Tự tạo nhiệm vụ khi gửi. Hỗ trợ tự phân loại rồi mới tạo.
- Tích hợp công cụ theo dõi lỗi bên ngoài (Sentry…), ghi lại thao tác (session replay).
- Tự thêm người báo vào nhóm hỗ trợ.
- Tạo nhiệm vụ từ tin báo lỗi gửi **riêng 1–1** (Q12). Hỗ trợ muốn giao dev thì tự tạo nhiệm vụ thường.
- Sửa luật thành viên nhóm theo công ty, sửa hàm chuyển tiếp tin.

**Không được để xảy ra**
- Nút che mất thao tác của màn (nút Lưu, phân trang, cột Hành động) khiến người dùng không làm việc được.
- Lộ dữ liệu nhạy cảm ngoài ý người báo: gửi lẫn token/mật khẩu trong thông tin tự gom, hoặc ép mọi báo cáo vào
  nhóm đông người.
- Bấm báo lỗi mà trang bị đơ / văng khỏi màn đang làm.
- Báo cáo mất trắng vì một phần phụ hỏng (chụp ảnh lỗi, tải ảnh lỗi). Lúc đó vẫn phải gửi được chữ.

## 3. Đã chốt với user

| # | Nội dung | User nói |
|---|---|---|
| Q1 | Thứ dev cần: mô tả, thông báo lỗi nhận được, URL màn hình, ảnh chụp càng tốt | "thường sẽ cần…" |
| Q2 | Nhận báo cáo: **1 nhóm chung** gồm dev + nhân viên hỗ trợ | "1 nhóm chung gồm dev và nhân viên hỗ trợ" |
| Q3 | Nút **luôn có trên mọi màn**, nhỏ gọn nhất có thể | "Luôn có trên mọi màn hình" |
| Q4 | Báo cả số liệu sai, thông tin sai, không chỉ lỗi code | "Lỗi ở đây ko chỉ là lỗi code" |
| Q5 | Người dùng cũng ở trong nhóm; hỗ trợ tạo nhiệm vụ giao dev; người dùng theo dõi tiến độ | "Hỗ trợ sẽ tạo task giao cho dev" |
| Q6 | Mặc định gửi vào nhóm; người dùng tự chọn lại để gửi riêng | "user có thể chọn lại để gửi về 1 user hỗ trợ cụ thể" |
| Q7 | Phải ở trong nhóm mới gửi được vào nhóm; **quản trị chủ động thêm** thành viên | "Quản trị chủ động thêm" |
| Q8 | Cài đặt chỉ có **nhóm mặc định**; gửi riêng thì người dùng **tự tìm 1 nhóm hoặc 1 người bất kỳ** | "tự tìm 1 nhóm hoặc 1 người cụ thể" |
| Q9 | Vị trí nút: **phương án C — tab mảnh dính mép phải**, chữ dọc "Báo lỗi" | "C" |
| Q10 | Popup, tin trong nhóm, ô cài đặt: **theo mockup** | "phần còn lại OK" |
| Q11 | **Mỗi công ty cài 1 nhóm mặc định** (nhóm gắn công ty, chỉ thêm được người cùng công ty — §6) | chọn 1/3 |
| Q12 | Báo lỗi gửi riêng 1–1: **chấp nhận chỉ để trao đổi**, không tạo nhiệm vụ từ tin; không sửa `forward` | chọn 1/3 |
| Q13 | Quyền sửa cài đặt: **mã quyền MỚI "Cài nhóm tiếp nhận báo lỗi"** (phân hệ Công việc), cấp theo vai trò từng công ty; phải cấp ở `/admin/roles` sau deploy | chọn 1/3 |

## 4. Hình thành phần (theo mockup)

### 4.1 Nút (tab mép phải)
- Tab rộng 22px dính mép phải, giữa chiều cao màn, icon `ri-bug-line` + chữ dọc "Báo lỗi", nền navy mờ.
- Có trên mọi màn dùng layout chính (`layouts/default`). Không có ở trang đăng nhập, trang in, kiosk.
- Phím tắt **Ctrl/⌘ + Shift + B** (đề xuất của Claude, xem §7).
- **Lớp hiển thị (user 14/11, thay quy tắc cũ "tab dưới nền mờ mọi popup + ẩn khi ngăn chat mở")**: tab nổi TRÊN mọi
  popup / panel (TaskPanel tạo-sửa nhiệm vụ…) và trên ngăn Chat/Agent (GĐ10), bấm được. Chỉ ẩn khi popup báo lỗi đang
  mở và trong lúc chụp. z-index 9990 (trên b-modal 1040+, TaskPanel 1059, ProductPicker 5040; dưới dropdown select2 /
  lịch 9999, toast + popover 10000, bộ chỉnh ảnh 10050). Popup báo lỗi mở CHỒNG lên popup đang mở (9995), popup con
  của nó (cài nhóm, hỏi chưa lưu) 9997; đóng popup báo lỗi ⇒ popup dưới còn nguyên dữ liệu + focus trả về ô đang gõ.
  Phím tắt cũng chạy khi đang có popup khác.

### 4.2 Bấm nút ⇒ chụp ⇒ popup
1. Chụp **trang đang thấy trước khi popup báo lỗi mở** — ảnh CÓ popup / panel / ngăn chat đang mở (lỗi thường nằm ở đó, user 14/11), KHÔNG dính popup báo lỗi và chính tab báo lỗi.
2. Mở popup (`V2BaseModal`):
   - **Ảnh màn hình**: ảnh nhỏ + 3 nút: *Khoanh / che chỗ nhạy cảm* (mở bộ chỉnh ảnh chat GĐ5
     `utils/chat/imageEditor.js`) · *Chụp lại* · *Thêm ảnh (dán / tải lên)*. Bỏ ảnh được. Nhiều ảnh được.
   - **Loại** (bắt buộc, chip): Lỗi hệ thống · Số liệu sai · Thông tin sai · Khác / góp ý.
   - **Mô tả** (bắt buộc).
   - **Gửi tới** (bắt buộc): mặc định nhóm cài đặt của **công ty đang chọn** nếu người dùng là thành viên, không thì để trống. Gõ để tìm
     **bất kỳ nhóm nào mình đang ở, hoặc bất kỳ người nào** (giống ô chọn người nhận khi tạo tin mới).
   - **Thông tin tự gửi kèm** (thu gọn được, chỉ đọc): Màn hình (tiêu đề + URL đầy đủ có query) · Công ty / người
     báo / phòng · Lỗi gần nhất (API) · Thông báo vừa hiện · Thiết bị · Phiên bản client.
   - Footer: Huỷ · **Gửi báo lỗi** (primary).
3. Gửi xong: toast "Đã gửi báo lỗi tới <nơi nhận>" + nút **Xem** mở ngăn chat (GĐ10) đúng hội thoại.

### 4.3 Tin trong hội thoại
- Một tin nhắn của người báo, hiển thị dạng khối báo lỗi: tiêu đề "Báo lỗi" + badge loại · mô tả · ảnh ·
  link "mở đúng màn + bộ lọc" · lỗi API chính · mục "Thông tin kỹ thuật" thu gọn.
- Trả lời, @nhắc, tạo nhiệm vụ từ tin… như mọi tin khác. Thẻ nhiệm vụ (GĐ2) hiện dưới tin, người báo thấy tiến độ.

### 4.4 Cài đặt
- Một ô "Nhóm tiếp nhận báo lỗi mặc định" **cho từng công ty**, chỉ chọn trong các nhóm thuộc công ty đó.
  Để trống ⇒ người dùng công ty đó tự chọn nơi gửi mỗi lần.
- Ai sửa: người có mã quyền mới "Cài nhóm tiếp nhận báo lỗi" tại công ty đó (Q13). Khai ở Catalog `assign.php`
  (cùng kiểu `assign.tpe_agent_cai_dat.manage`), đồng bộ bằng `permission:catalog-sync`, chặn BE bằng `checkPermission`.

## 5. Ràng buộc

- **Quy mô 1.000–2.000 người, đa nền tảng** (README agent-chat §0): logic tạo tin báo lỗi nằm ở **BE, 1 API
  dùng chung** (app mobile/desktop sau gọi lại), web chỉ chụp + gom + hiển thị. Cài đặt nhóm mặc định lưu ở BE.
- Ảnh đi qua **nén ảnh chat sẵn có** (`utils/chat/imageCompress.js`: WebP, cạnh dài ≤ 2560) và luồng tải tệp
  chat sẵn có. Không thêm kho lưu mới.
- Tin báo lỗi là tin chat thật: theo đúng quyền gửi (`ConversationAccess::canSend`), realtime socket, push FCM,
  panel Ảnh/Tệp/Link (GĐ7) như tin thường.
- hrm-client chạy **Nuxt 2 / webpack 4, build bằng Node 12** ⇒ thư viện mới phải dịch được trên toolchain này.
- Quy ước HRM: popup `V2BaseModal`, form `V2Base*`, nút theo `button-convention`, validate đỏ đồng thời mọi ô,
  quyền khai ở Catalog (`permission:catalog-sync`), model mới `extends BaseModel`.
- Chỉ làm cổng TPE trước (PHP 8.1); cổng khác cập nhật sau.

## 6. Hiện trạng đã kiểm trong code (14/11, worktree wt-nhom-trao-doi = origin/gop_db)

- `chat_messages` có `type` (text · system · card) và `meta` JSON ⇒ chứa được dữ liệu báo lỗi không cần cột mới.
- Tạo nhiệm vụ từ tin: `MessageService::taskSource()` **chỉ nhận tin thuộc NHÓM** (`$conversation->isSpace()` và
  đúng `workspace_id`). ⇒ báo lỗi gửi vào **chat 1–1 thì hiện chưa tạo được nhiệm vụ từ tin** (xem §8).
- `workspaces.company_id` có cột ⇒ nhóm gắn công ty. `WorkspaceMemberService::eligibleIds()` (dòng 53) chỉ nhận người
  có `company_employees` đúng công ty của nhóm ⇒ lý do chốt Q11.
- `MessageService::forward()` chỉ chép body + tệp, `meta` thay bằng `forwarded_from` ⇒ chuyển tiếp làm mất khối báo lỗi
  (chấp nhận, Q12).
- Bắt lỗi API: `plugins/axios.js` (`$axios.onError`) + `plugins/api-error-guard.js` (bọc `Vue.config.errorHandler`)
  ⇒ chỗ cắm bộ ghi "lỗi gần nhất".
- Chụp: `utils/chat/screenCapture.js` (getDisplayMedia, có hộp chọn của trình duyệt) — dùng làm đường dự phòng.
  Chưa có thư viện vẽ DOM thành ảnh trong `package.json`.

## 7. Quyết định của Claude (user chưa duyệt riêng — kiểm khi đọc)

- **Cách chụp chính = vẽ lại DOM thành ảnh** (không hộp hỏi của trình duyệt). Đề xuất `html2canvas` 1.4.1 (bản
  ES5, chạy được trên webpack 4). Lỗi chụp / quá 5 giây ⇒ mở popup không có ảnh, kèm 2 đường dự phòng
  "Chụp bằng trình duyệt" (screenCapture.js) và "Dán / tải ảnh lên".
- Tab C: mờ ~70%, rê chuột thì đậm; ẩn tab khi popup báo lỗi đang mở và lúc chụp.
- Phím tắt Ctrl/⌘ + Shift + B.
- **Bộ ghi lỗi trên trình duyệt** (bộ nhớ, không lưu đĩa): 10 lỗi API gần nhất (method, đường dẫn không kèm
  query nhạy cảm, status, câu lỗi BE trả, giờ), 3 toast lỗi gần nhất, 3 lỗi JS gần nhất (errorHandler / onerror).
  **Không** ghi body request, header, token.
- Thông tin tự gom gửi lên BE dạng JSON, BE lưu vào `meta` của tin; BE tự điền người báo / công ty / phòng
  từ phiên đăng nhập (không tin dữ liệu FE gửi cho mấy trường này).
- Một tin duy nhất chứa mô tả + ảnh + meta (không tách nhiều tin).
- Chống spam: tối đa 10 báo cáo / người / giờ (BE trả 429 kèm câu báo).
- Cài đặt lưu theo `company_id` (giống `AgentCompanySetting`).
- Công ty đang ẩn "Tin nhắn" (Cài đặt phân hệ, `chatEnabled`): tab báo lỗi **vẫn hiện** (user: luôn có trên mọi
  màn); chỉ bỏ nút "Xem" trên toast nếu người dùng không mở được chat.
- Tin chuyển tiếp từ tin báo lỗi hiện như tin thường (mất khối báo lỗi) — hệ quả của Q12, không xử lý.
- Bản ghi báo lỗi không có bảng riêng: tin chat + meta là nguồn duy nhất.

## 8. Để người làm quyết

- Tên thư viện chụp cụ thể (miễn build được trên Node 12 + webpack 4 và đo đạt).
- Cấu trúc `meta` cụ thể, tên endpoint, cách FE render khối báo lỗi trong `ChatMessageItem`.
- Nơi đặt ô cài đặt trong giao diện quản trị.

## 8b. Thay đổi sau khi duyệt (user 14/11, sau khi thử trên :3080)
- Q14: tab **nổi trên mọi popup / panel nhiệm vụ / ngăn Chat-Agent** (thay quy tắc cũ "dưới nền mờ, ẩn khi ngăn chat mở"); chỉ ẩn khi popup yêu cầu hỗ trợ đang mở / lúc chụp; ảnh chụp GỒM popup đang mở. Lớp: tab 9990 · popup 9995 · popup con 9997 (dưới dropdown 9999, toast 10000, bộ chỉnh ảnh 10050).
- Q15: Esc của `TaskPanel.vue` nhường popup yêu cầu hỗ trợ (user duyệt sửa 1 dòng component dùng chung).
- Q16: popup cài đặt liệt kê MỌI nhóm còn mở của công ty (kể cả người cài không là thành viên) qua API `GET v1/assign/chat/bug-reports/settings/workspaces?q=&page=`.
- Q17: chữ nút theo skill (Chỉnh ảnh · Chụp lại · Chụp màn hình · Thêm ảnh) thay chữ mockup; `env.CLIENT_BUILD` hiện phiên bản.
- Q18: đổi mọi chữ hiển thị "báo lỗi" ⇒ "yêu cầu hỗ trợ" (tab "YC hỗ trợ", tiêu đề popup, nút "Gửi yêu cầu", toast, khối tin, tên quyền "Cài nhóm tiếp nhận yêu cầu hỗ trợ").
- Phát hiện khi làm: html2canvas không đọc màu `color(srgb …)` sinh từ `color-mix()` ⇒ chụp hỏng ở màn có V2BaseSegmented / panel nhiệm vụ ⇒ `pageCapture.js` đổi sang rgba trên bản sao trước khi chụp.

## 9. Tài liệu
- `mockup.html` — 4 phần: vị trí nút (đã chọn C) · popup · tin trong nhóm · cài đặt.
- `plan.md` — task + kết quả + ghi chú deploy + checkpoint · `ledger-sdd.md` — sổ thực hiện (rulings, review) · e2e `HRM/e2e/tests/assign/bug-report.spec.ts` (8 ca).
