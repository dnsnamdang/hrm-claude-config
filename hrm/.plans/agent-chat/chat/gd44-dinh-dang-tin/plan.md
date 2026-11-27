# Chat — GĐ44 Thanh định dạng văn bản khi soạn tin nhắn + bình luận (web & app) (chưa có số Redmine) — @cuong61n

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development hoặc superpowers:executing-plans. Checkbox `- [ ]`.
>
> Yêu cầu 26/11/2026: thanh công cụ định dạng (đậm / nghiêng / gạch chân / gạch ngang / kiểu, cỡ, màu chữ, màu nền / danh sách • 1. /
> tăng giảm thụt lề / hoàn tác làm lại / mở rộng Ctrl+Shift+X / bật tắt) trong khung soạn tin Chat; gửi đi giữ định dạng; hiện thống nhất
> web + app. User bổ sung: áp cả khung BÌNH LUẬN (Nhiệm vụ / Vấn đề). Tham khảo Zalo.

**Goal:** tin nhắn chat + bình luận soạn được chữ có định dạng ở web và app, lưu 1 khuôn HTML, hiển thị giống nhau 2 nền.

**Architecture:** lưu `body` / `comment` là **HTML canonical** (xem Global Constraints) đã sanitize ở BE, kèm `body_text` chữ thuần cho
xem trước / tìm kiếm / push. Web: Quill 2.0.2 (đã có trong node_modules, chưa dùng) thay `V2BaseTextarea` trong ChatComposer, thanh
định dạng tự dựng `ChatFormatToolbar.vue` dùng chung chat + bình luận. App: `flutter_quill` (đã có) + thanh tự dựng `ChatFormatBar`,
bong bóng vẽ bằng `flutter_widget_from_html` (đã có). Tin thuần (không thẻ) lưu và hiển thị y như cũ ⇒ không migrate dữ liệu.

**Tech Stack:** Laravel 8 / PHP 7.4 (DOMDocument, PHPUnit) · Nuxt 2 / Vue 2 + Quill 2.0.2 (client-only) · Flutter: flutter_quill 11.5,
flutter_quill_delta_from_html, flutter_widget_from_html · Playwright (Node 20) cho web.

**Spec:** `design.md` cùng thư mục (+ Pencil `~/Downloads/meeting-mobile_v2.pen` 13 khung "CHAT · Định dạng"). Quyết định đã chốt:
Enter vẫn GỬI · 4 cỡ chữ cố định · sửa tin chỉ tự mở thanh khi tin có định dạng · chưa áp ô Mô tả.

## Global Constraints

- **HTML canonical (cả 2 nền phải sinh ra ĐÚNG khuôn này, BE sanitize về khuôn này):** mỗi dòng 1 `<p>…</p>` (dòng trống `<p><br></p>`);
  inline `<b>` `<i>` `<u>` `<s>`; `<span style="color:#RRGGBB">` · `<span style="background-color:#RRGGBB">` ·
  `<span style="font-size:12px|18px|22px">` (14px = mặc định, không ghi) · `<span style="font-family:serif|monospace">`;
  danh sách `<ul>` / `<ol>` + `<li>`, thụt lề = `<ul>`/`<ol>` LỒNG trong `<li>` (không dùng class `ql-indent-*`);
  link `<a href="http(s)://…" target="_blank" rel="noopener">`. Thuộc tính khác, thẻ khác, `class`, `id`, `on*`, `javascript:` ⇒ gỡ.
- **Bảng màu cố định** (web + app dùng chung mảng, thứ tự giữ nguyên): chữ `#0F172A #64748B #DC2626 #EA580C #D97706 #16A34A #0EA5E9
  #2563EB #7C3AED #DB2777 #92400E #FFFFFF`; nền `#FEF08A #FDE68A #FECACA #BBF7D0 #BAE6FD #DDD6FE #FBCFE8 #E5E7EB #FED7AA #A7F3D0
  #C7D2FE #FFFFFF`. Sanitize chấp nhận mọi `#RRGGBB` (không chặn theo bảng) để sau đổi bảng không hỏng tin cũ.
- **Tin thuần = không có thẻ HTML** ⇒ gửi / lưu / hiển thị y hệt hiện tại (escape + @ + link + `\n`⇒`<br>`). `isRich(body)` = body chứa
  `<` + chữ cái. 5.000 ký tự đếm trên CHỮ THUẦN; raw HTML cho phép tới 20.000.
- Nhánh (user chốt 26/11): code THẲNG trên `gop_db` tại `worktrees/gop_db-api` (:8003) + `worktrees/gop_db-client` (:3002)
  để test; app trên `develop` tại `TPE_APP/app`. KHÔNG commit/push khi user chưa bảo.
- Giữ nguyên class / testid e2e đang bám: `.cc`, `.cc__box`, `.cc__bar`, `cc__hl`, `chat-composer-input` (gắn lên root Quill `.ql-editor`),
  `chat-composer-hint`, `chat-composer-count`, `chat-send`, `chat-emoji-toggle`, `chat-mention-list`, `chat-mention-all`, `chat-msg-*`.
  App giữ `ValueKey('chat_composer_input' | 'chat_composer_send' | 'chat_composer_emoji' | 'chat_composer_counter')`.
- Nút mới web = `V2BaseIconButton size="md"` (icon `ri-*`), nút bật = class `cc__tool--on`; app theo `app-components` (không dùng
  `QuillSimpleToolbar`). Chữ đỏ chỉ cho lỗi; popover chọn màu / cỡ chữ dùng khuôn menu ⋯ của tin (bo 10px, bóng nhẹ, Esc đóng).
- Phím tắt web: Ctrl+B/I/U · Ctrl+Shift+S gạch ngang · Ctrl+Shift+7 danh sách số · Ctrl+Shift+8 danh sách chấm · Tab / Shift+Tab thụt lề
  (chỉ trong danh sách) · Ctrl+Z / Ctrl+Y · Ctrl+Shift+X mở rộng/thu · Esc thu (nếu đang mở rộng, không đang sửa/trả lời) · Enter GỬI ·
  Shift+Enter xuống dòng (trong danh sách = mục mới; Shift+Enter ở mục rỗng = thoát danh sách).
- Trạng thái bật/tắt thanh: web `localStorage['chat.format_on']` ('1'/'0', mặc định '0'); app `SharedPreferences 'chat_format_on'`.
  Chung cho chat + bình luận. Sửa tin/bình luận có định dạng ⇒ mở thanh tạm (không ghi vào trạng thái nhớ).

## Review Focus

1. Dán HTML từ Word / web ngoài vào ô soạn ⇒ chỉ giữ các định dạng trong khuôn, không lọt `<img>`, `<table>`, style lạ (test Task 1 + 5).
2. Tin có định dạng chứa `@Tên` / `@all` / link: BE `syncMentions` + `ChatResourceService::syncLinks` phải đọc từ chữ thuần, không từ HTML
   (test Task 2).
3. Người dùng app bản CŨ nhận tin HTML ⇒ `body` của API vẫn phải đọc được: presenter trả `body` = HTML và `body_text`; app cũ hiện HTML
   thô — chấp nhận, ghi tổng kết để phát hành app cùng lúc (test Task 2 kiểm `body_text` luôn có khi rich).
4. Tin thuần có ký tự `<` (vd "a < b") KHÔNG được coi là rich và không bị sanitize làm mất chữ (test Task 1, Task 5).
5. 4.999 ký tự chữ thuần + nhiều thẻ (raw > 5.000) phải gửi được; 5.001 chữ thuần bị 422 `body` (test Task 2 + bộ đếm web Task 6).

---

## Phase 0 — Rà code + thiết kế (26/11/2026) — XONG

- [x] 26/11 — Rà code web / app / BE (chi tiết design.md "Hiện trạng").
- [x] 26/11 — Vẽ Pencil 13 khung, đã save. User chốt 4 điểm (ghi design.md "Quyết định đã chốt").

## Phase 1 — BE (hrm-api, nhánh `gop_db-chat-dinh-dang`)

### Task 1: `App\Support\RichText` — sanitize / toText / isRich
**Files:** Create `app/Support/RichText.php` · Test `tests/Unit/Support/RichTextTest.php` (khung theo test Unit có sẵn).
**Produces:** `RichText::isRich(?string $s): bool` · `RichText::sanitize(string $html): string` (trả HTML canonical; input thuần ⇒ trả
nguyên, đã escape bởi caller không cần) · `RichText::toText(string $html): string` (`<p>`/`<li>`/`<br>` ⇒ `\n`, gỡ thẻ, decode entity,
trim; input thuần ⇒ trả nguyên).
- [x] 26/11 — Viết test: `isRich('a < b')===false`, `isRich('<b>x</b>')===true`; `sanitize('<p>a<script>1</script><b onclick="x">b</b><img src=x></p>')
  === '<p>a<b>b</b></p>'`; `sanitize('<p><span style="color:#DC2626;font-weight:bold;font-size:18px">x</span></p>')` ===
  `'<p><span style="color:#DC2626;font-size:18px">x</span></p>'` (bỏ thuộc tính style ngoài 4 cái; `font-size` ngoài 12/18/22 bị bỏ);
  `sanitize('<ul><li>a<ul><li>b</li></ul></li></ul>')` giữ nguyên; `sanitize('<a href="javascript:1">x</a>')==='<p>x</p>'`;
  `sanitize('<div>a<br>b</div>')==='<p>a<br>b</p>'`; `toText('<p>Kế <b>hoạch</b></p><ul><li>a</li><li>b</li></ul>')==="Kế hoạch\na\nb"`;
  `toText('a < b')==='a < b'`.
- [x] 26/11 — Chạy `php artisan test --filter RichTextTest` ⇒ FAIL 9/9 (class chưa có).
- [x] 26/11 — Viết `RichText` bằng `DOMDocument::loadHTML('<?xml encoding="utf-8"?>…', LIBXML_HTML_NOIMPLIED|LIBXML_HTML_NODEFDTD)`, đệ quy whitelist:
  `strong⇒b`, `em⇒i`, `strike/del⇒s`, `div⇒p`, `p` cấp 1 bắt buộc (text/inline rời ở cấp 1 bọc `<p>`), `li` ngoài `ul/ol` ⇒ `p`.
- [x] 26/11 — Chạy lại ⇒ 9 passed (bẫy: `<` lẻ bị libxml nuốt chữ sau ⇒ escape `<` không theo chữ cái trước khi parse).

### Task 2: Chat — lưu HTML, `body_text`, mention/link từ chữ thuần
**Files:** Create migration `Modules/Assign/Database/Migrations/2026_11_26_000001_add_body_text_to_chat_messages.php` (`body_text` TEXT
nullable sau `body`; KHÔNG bọc transaction — memory DDL) · Modify `Modules/Assign/Entities/Chat/ChatMessage.php` (fillable
`body_text`) · `Http/Requests/Chat/SendMessageRequest.php:17` (`body max:20000`) · request sửa tin tương ứng ·
`Services/Chat/MessageService.php` `send()` :84 + `edit()` :350 + search :511 · `Services/Chat/ChatPresenter.php` :151 (messages) + :168
(reply quote) + :392 `preview()` · `Services/Chat/ChatResourceService::syncLinks` · chỗ dựng push/notification từ `body`
(grep `->body` trong `Services/Chat`, `Listeners`, `ChatSocket`) · Test `Modules/Assign/Tests/Feature/Workspace/ChatRichTextTest.php`
(khung `ChatApiTest.php`).
**Consumes:** `RichText` (Task 1). **Produces:** payload tin có thêm `body_text` (string|null; null khi tin thuần); `preview.text`,
reply `body`, push, search đều dùng `body_text ?? body`.
- [x] 26/11 — Viết `ChatRichTextTest` (7 test, `vendor/bin/phpunit Modules/Assign/Tests/Feature/Workspace/ChatRichTextTest.php` — `artisan test --filter` KHÔNG quét Modules/): (1) gửi `body='<p><b>Kế hoạch</b> @Nguyễn Văn A xem <script>x</script></p>'` + `mention_ids` ⇒ 201,
  DB `body` = `'<p><b>Kế hoạch</b> @Nguyễn Văn A xem </p>'` (chuẩn hoá), `body_text='Kế hoạch @Nguyễn Văn A xem'`, mention ghi đúng,
  API `messages` trả `body_text`; (2) gửi body thuần `'a < b'` ⇒ `body='a < b'`, `body_text=null`; (3) rich 5.001 chữ thuần ⇒ 422
  `body`; rich 4.999 chữ + 3.000 ký tự thẻ ⇒ 201; (4) sửa tin thành rich ⇒ `body_text` cập nhật; (5) `preview()` của tin rich ⇒ `text`
  không chứa `<`; (6) tìm kiếm `q='Kế hoạch'` trúng tin rich (search theo `COALESCE(body_text, body)`); (7) link `https://x.y` trong
  `<a>` được `syncLinks` ghi 1 dòng.
- [x] 26/11 — Chạy ⇒ FAIL 7/7. Làm: trong `send()`/`edit()` (helper `normalizeBody()`) `$body = RichText::isRich($raw) ? RichText::sanitize($raw) : $raw; $text =
  RichText::isRich($body) ? RichText::toText($body) : null;` kiểm `mb_strlen($text ?? $body) > 5000` ⇒ 422 `Vui lòng nhập tối đa 5,000
  ký tự.`; mọi chỗ đọc `->body` cho mention/link/preview/push/search đổi sang helper `ChatMessage::plainBody(): string`
  (`body_text ?? body ?? ''`).
- [x] 26/11 — Migrate DB local gộp xong; ChatRichTextTest 7/7 PASS; suite Workspace 387 test: 7 fail CÓ SẴN (TaskAccessTest 1, WorkspaceOutsideAssigneeTest 5, WorkspaceTaskListTest 1 — data-dependent, không đụng body chat), còn lại PASS.

### Task 3: Bình luận — sanitize `comment`
**Files:** Modify `Http/Controllers/Api/V1/TaskCommentController.php` :41 + :106 · `IssueCommentController.php` :36 + :94 (validate `max:20000`,
trước khi ghi: `RichText::isRich` ⇒ `sanitize`, kiểm 5.000 chữ thuần) · chỗ dựng thông báo bình luận lấy nội dung (grep `comment` trong
`Concerns/CommentModeration.php` + notify) dùng `RichText::toText` · Test `Modules/Assign/Tests/Feature/CommentRichTextTest.php`.
- [x] 26/11 — `CommentRichTextTest` 3 test (tạo + sửa sanitize, thuần giữ nguyên, 5.000 theo chữ thuần) — RED rồi PASS; bẫy: `ValidationException` bị `catch (Exception)` ⇒ 400, phải chuẩn hoá NGOÀI `try` (helper `normalizeCommentBody()` trong trait `CommentModeration`, dùng cho cả Task + Issue).

## Phase 2 — Web dùng chung (hrm-client, nhánh `gop_db-chat-dinh-dang`)

### Task 4: `utils/chat/richText.js` — bảng màu, canonical HTML, Delta⇄HTML
**Files:** Create `utils/chat/richText.js` · Test `e2e/tests/chat/rich-text-util.spec.ts` (Playwright chạy hàm thuần qua `page.evaluate`
sau khi import — hoặc Node test bằng `node --test` nếu util không đụng DOM; chọn Node: util nhận chuỗi, dùng `DOMParser` chỉ trong
`sanitizeHtml` ⇒ tách `deltaToHtml` thuần Node).
**Produces:** `TEXT_COLORS`, `BG_COLORS` (12+12 như Global Constraints), `FONT_SIZES=[{label:'Nhỏ',value:'12px'},{label:'Vừa (mặc
định)',value:null},{label:'Lớn',value:'18px'},{label:'Rất lớn',value:'22px'}]`, `FONT_FAMILIES=[{label:'Mặc định',value:null},
{label:'Serif',value:'serif'},{label:'Monospace',value:'monospace'}]` · `isRich(s)` · `deltaToHtml(ops)` (Quill Delta ⇒ canonical; attrs
`bold italic underline strike color background size font list indent link`; indent ⇒ lồng `<ul>/<ol>`) · `htmlToText(html)` ·
`sanitizeHtml(html)` (DOMParser whitelist giống BE, dùng khi render) · `getFormatOn()/setFormatOn(bool)` (localStorage) ·
`plainLength(html)` = số code point của `htmlToText`.
- [x] 26/11 — Test Node `tests/unit/chat/richText.test.mjs` 8 ca (RED → PASS, Node 20.11.1 `--experimental-default-type=module --test`): `deltaToHtml([{insert:'Kế hoạch',attributes:{bold:true}},{insert:'\n'},{insert:'a'},{insert:'\n',attributes:{list:'bullet'}},
  {insert:'b'},{insert:'\n',attributes:{list:'bullet',indent:1}}])` === `'<p><b>Kế hoạch</b></p><ul><li>a<ul><li>b</li></ul></li></ul>'`;
  size `'18px'` ⇒ `font-size:18px`; `color:'#DC2626'` + `background:'#FDE68A'` cùng 1 span ⇒ `style="color:#DC2626;background-color:#FDE68A"`;
  dòng trống ⇒ `<p><br></p>`; chữ `<` escape `&lt;`; `htmlToText` ngược lại ra `"Kế hoạch\na\nb"`; `isRich('a < b')===false`.
- [x] 26/11 — `utils/chat/richText.js` xong (TEXT_COLORS/BG_COLORS/FONT_SIZES/FONT_FAMILIES, isRich, deltaToHtml, htmlToText, plainLength, sanitizeHtml DOMParser, getFormatOn/setFormatOn).

### Task 5: `components/chat/ChatRichEditor.vue` — ô soạn Quill (client-only) + `ChatFormatToolbar.vue`
**Files:** Create `components/chat/ChatRichEditor.vue`, `components/chat/ChatFormatToolbar.vue`, `components/chat/ChatColorPopover.vue`,
`components/chat/ChatSizePopover.vue` · CSS: import `quill/dist/quill.core.css` trong editor (scoped override, KHÔNG theme snow) ·
Test `e2e/tests/chat/rich-editor.spec.ts` (trang thử `pages/extras/dev-rich-editor.vue` chỉ khi `process.env.NODE_ENV!=='production'`,
hoặc test thẳng trên khung chat ở Task 6 — chọn: test ở Task 6, Task 5 chỉ kiểm bằng Playwright thủ công).
**Produces:** `ChatRichEditor` props `value:String` (HTML canonical hoặc thuần) · `formatOn:Boolean` · `placeholder` · `expanded:Boolean`
· `members:Array` (để mention giữ nguyên hành vi); emit `input(html|plain)` (plain khi không có định dạng nào), `text(plainString)`,
`keydown(e)`, `selection({index,length})`, `paste(e)`, `format-state({bold,italic,…,size,color,background,list,undo,redo})`; methods
`focus()`, `insertText(str)`, `replaceRange(start,len,str)`, `getText()`, `getSelection()`, `format(name,value)`, `undo()/redo()/clear()`.
Quill: `import('quill')` trong `mounted` (SSR safe), đăng ký `Quill.import('attributors/style/size')` whitelist `['12px','18px','22px']`,
`attributors/style/font` whitelist `['serif','monospace']`, `attributors/style/color|background`; `formats` chỉ danh sách trên + `list`
`indent` `link`; tắt keyboard binding Enter mặc định (Enter ⇒ emit `submit`), Shift+Enter ⇒ gọi handler Enter mặc định của Quill; khi
`formatOn=false` ⇒ bỏ binding Ctrl+B/I/U và `formats` = [] (gõ ra chữ thuần). `ChatFormatToolbar` props `state`, `expanded`, `canUndo/Redo`;
emit `format(name,value)`, `undo`, `redo`, `clear`, `toggle-expand`, `pick-color({kind:'color'|'background',value})`; thứ tự nút: B I U S |
Aa▾ A▾ 🖍▾ Xoá định dạng | • 1. ⇥ ⇤ | ↶ ↷ | ⤢ (title tiếng Việt kèm phím tắt).
- [x] 26/11 — Dựng `ChatRichEditor.vue` (Quill 2 dist UMD, `build.transpile: ['quill']`), `ChatFormatToolbar.vue`, `ChatSizePopover.vue`, `ChatColorPopover.vue`; kiểm Playwright MCP trên :3002: gõ telex, Ctrl+B, danh sách lồng Tab, màu, dán. (Kế hoạch cũ: chạy `:3004`, Playwright MCP thử gõ tiếng Việt (telex), Ctrl+B, danh sách, Tab, dán HTML từ web
  ngoài (chỉ còn định dạng trong khuôn), chụp ảnh vào scratchpad.

## Phase 3 — Web Chat

### Task 6: `ChatComposer.vue` — thay textarea bằng `ChatRichEditor`, nút Aa, mở rộng, bộ đếm
**Files:** Modify `components/chat/ChatComposer.vue` (template :88-105 ô nhập, :108-166 hàng công cụ thêm nút `ri-text` "Định dạng văn
bản (Aa)" trước emoji; data `text` giữ = CHỮ THUẦN (cho @/#/emoji/nháp), thêm `html`, `formatOn`, `expanded`; `bodyLength` = plainLength;
`submit()` :678 gửi `body = isRich(html) ? html : text`; `onKeydown` :552 thêm Ctrl+Shift+X, Esc thu; mention/hash dùng
`editor.getText()/getSelection()/replaceRange()` thay `textarea.selectionStart`; `highlightHtml`/`cc__hl` bỏ, @Tên tô bằng format
`mention` riêng của Quill (inline blot `span.cc__mention`, gỡ khi serialize); nháp lưu thêm `html`; `editing` watcher: nếu
`isRich(m.body)` ⇒ `formatOn=true` tạm) · `pages/assign/messages`, `ChatPane.vue` không đổi API.
Hint :178: thêm `Ctrl + Shift + X mở rộng` khi `formatOn`.
**Test** `e2e/tests/chat/rich-text.spec.ts` (Node 20, helpers `e2e/tests/chat/helpers.ts`): (1) mặc định không có `.cc__fmt`; bấm Aa ⇒ có,
reload vẫn có (localStorage); (2) gõ "Kế hoạch", Ctrl+A, Ctrl+B, Enter ⇒ request `POST …/messages` có `body==='<p><b>Kế hoạch</b></p>'`;
(3) tắt Aa, gõ "a < b", Enter ⇒ `body==='a < b'`; (4) gõ @ chọn người trong tin có đậm ⇒ `mention_ids` đúng; (5) Ctrl+Shift+X ⇒ `.cc--expanded`,
Esc ⇒ bỏ; (6) 4.990 chữ + đậm ⇒ gửi được, 5.001 ⇒ nút Gửi `disabled` + bộ đếm đỏ; (7) bấm Sửa tin rich ⇒ thanh hiện, editor có `<b>`.
- [x] 26/11 — `e2e/tests/chat/rich-text.spec.ts` 7 test PASS (chạy `BASE_URL=http://127.0.0.1:3002 API_URL=http://127.0.0.1:8003`, Node 20); ChatComposer đổi sang ChatRichEditor + nút Aa + mở rộng + nháp html + sửa tin rich tự bật thanh.

### Task 7: Hiển thị tin rich — `ChatMessageItem.vue` + xem trước / trích dẫn
**Files:** Modify `components/chat/ChatMessageItem.vue` `html()` :563 (rich ⇒ `sanitizeHtml(body)` rồi tô @ / @all / link trên text node;
thuần ⇒ như cũ), style `.cm__text` cho `ul/ol/li/p/span` (p margin 0, li padding-left, line-height giữ) · `utils/chat/chatFormat.js`
`previewText` :167 dùng `message.body_text ?? message.body` · ChatComposer `cc__ctx` :17 (`body_text`) · ChatPane / ForwardModal / ghim /
tìm kiếm chỗ nào hiện `body` ⇒ `body_text ?? body`; copy tin ⇒ chữ thuần.
- [x] 26/11 — `ChatMessageItem.richHtml()` (sanitizeHtml + tô @ / link trên text node), `previewText` dùng `body_text`, ChatPane ghim / tìm / sao chép dùng `body_text ?? body` — e2e kiểm trong rich-text.spec.

## Phase 4 — Web Bình luận

### Task 8: `CommentEditor.vue` + `CommentNode.vue` dùng `ChatRichEditor` + `ChatFormatToolbar`
**Files:** Modify `components/comments/CommentEditor.vue` (thay `contenteditable` :4-11 bằng `ChatRichEditor`; chip @ ⇒ format `mention`
với `data-id`, serialize ra `@[Tên]` trong chữ thuần như cũ; `submit()` :451 `comment = isRich(html) ? html : rawText`; footer :45 thêm nút Aa +
thanh; Enter gửi, Shift+Enter xuống dòng giữ) · `CommentNode.vue` `renderContent` :495 (rich ⇒ `sanitizeHtml` + thay `@[x]`), ô sửa
:23 `textarea` ⇒ `ChatRichEditor` (mở thanh nếu rich) · `IssuePanel.vue` / `TaskPanel.vue` không đổi props.
- [x] 26/11 — CommentEditor viết lại trên ChatRichEditor (bỏ chip contenteditable, @ theo chữ thuần ⇒ gửi `@[Tên]`), CommentNode render rich + ô sửa Quill; `e2e/tests/chat/comment-rich-text.spec.ts` 3 test PASS.

## Phase 5 — App dùng chung (TPE_APP nhánh `feature/chat-dinh-dang`)

### Task 9: `lib/ui/chat/rich/chat_rich_text.dart` — bảng màu, Delta⇄HTML canonical, isRich, toText
**Files:** Create `lib/ui/chat/rich/chat_rich_text.dart` · Test `test/ui/chat/rich/chat_rich_text_test.dart`.
**Produces:** `ChatRichText.textColors / bgColors` (12+12 `Color`, cùng thứ tự web) · `fontSizes` (`null,'12','18','22'` ↔ px) ·
`isRich(String?)` · `deltaToHtml(Document)` (TỰ VIẾT theo khuôn, KHÔNG dùng `vsc_quill_delta_to_html` để ra đúng canonical) ·
`htmlToDocument(String)` (dùng `flutter_quill_delta_from_html` như `meeting_rich_editor.dart` :87, map `font-size:18px` ⇒ attr size '18',
nested `ul` ⇒ indent) · `toText(String)` · `formatOnKey='chat_format_on'` + `loadFormatOn()/saveFormatOn(bool)`.
- [x] 26/11 — `lib/ui/chat/rich/chat_rich_text.dart` + `test/ui/chat/rich/chat_rich_text_test.dart` 10 test (RED → PASS). Delta⇄HTML tự viết (package html), KHÔNG dùng vsc/delta_from_html; cỡ chữ Delta '12'/'18'/'22'. Thêm `AppPreferences.chatFormatOn` / `saveChatFormatOn`.

### Task 10: `ChatFormatBar` + `ChatRichField` + bảng màu + màn mở rộng
**Files:** Create `lib/ui/chat/rich/chat_format_bar.dart` (hàng 46px cuộn ngang, nút 36 theo design APP 2, mờ phải; props
`controller: QuillController`, `expanded`, `onToggleExpand`, `onPickColor(kind)`) · `lib/ui/chat/rich/chat_color_sheet.dart` (thay bàn phím:
tab Màu chữ / Màu nền, lưới 6×2 vòng 46, "Màu mặc định") · `lib/ui/chat/rich/chat_size_sheet.dart` (4 cỡ + 3 kiểu chữ) ·
`lib/ui/chat/rich/chat_rich_field.dart` (QuillEditor 1–5 dòng trong viên `ChatColors.inputBg`, nút Aa + 😊 bên trong như design APP 1; khi
`formatOn=false` ⇒ `QuillController.readOnly=false` nhưng `toolbarButtons` ẩn và phím tắt tắt; expose `text`, `html`, `plainLength`) ·
`lib/ui/chat/rich/chat_expand_page.dart` (toàn màn: "Soạn tin nhắn" + Gửi, thanh dưới, `Navigator.pop(html)`).
- [x] 26/11 — `chat_rich_controller.dart` (đồng bộ 2 chiều TextEditingController ⇄ Quill, formatOn/expanded, html/body/plainLength, toggle/setValue/indent/clearFormat), `chat_rich_field.dart` (QuillEditor + placeholder overlay 1 dòng), `chat_format_bar.dart` (thanh 46px cuộn ngang + `showChatColorSheet` + `showChatSizeSheet`), `chat_expand_page.dart`; `test/ui/chat/rich/chat_rich_field_test.dart` 6 test PASS. Bẫy đã sửa: đổi Document phải đăng ký lại stream `changes`; `replaceText` phải kèm selection hợp lệ (RangeError); placeholder Quill xuống 2 dòng làm ô rỗng cao 50 (user báo xấu) ⇒ overlay.

## Phase 6 — App Chat

### Task 11: `composer.dart` + `chat_room_page.dart` + `message_bubble.dart`
**Files:** Modify `lib/ui/chat/widget/composer.dart` (TextField ⇒ `ChatRichField`; `onSend(String text)` ⇒ `onSend(String body)` với
`body = isRich ? html : text`; giữ `ValueKey` cũ; bộ đếm theo `plainLength`) · `chat_room_page.dart` `_send` :1388 / `_saveEdit` :1421 /
`_startEdit` :1511 (nạp `htmlToDocument(m.body)`, mở thanh nếu rich) / `chatTriggerAt` :1238 (@ # đọc từ `controller.document.toPlainText()`
+ selection) / nháp · `message_bubble.dart` :576 (rich ⇒ `HtmlWidget(sanitized, customStylesBuilder` map `font-size/color/background`,
`textStyle: base`; @Tên / @all / link tô bằng `customWidgetBuilder` hoặc tiền xử lý HTML bọc `<a data-emp>`) · `chat_models.dart` :699
thêm `bodyText` (`body_text`), `previewText` :446 dùng `bodyText ?? body` · danh sách hội thoại / trích dẫn / ghim / tìm kiếm dùng `bodyText ?? body`.
- [x] 26/11 — composer.dart (prop `rich`, nút Aa, `below`), chat_room_page (toggle/expand/_send theo chữ thuần/_startEdit nạp HTML), message_bubble `_richText` (HtmlWidget + span cm-mention), chat_models `bodyText`, chatMessagePreview dùng bodyText; `test/ui/chat/rich/message_bubble_rich_test.dart` 3 test PASS. Simulator iPhone 15 (tpeLocal → :8003, bước 56–83 ảnh ở scratchpad phiên GĐ43): gửi đậm + list + màu ⇒ DB `body` canonical + `body_text`; @ gợi ý + mention_ids; sửa tin rich ⇒ nạp HTML, PUT đúng; mở rộng toàn màn ⇒ gửi; web hiện đúng tin app gửi và ngược lại.

## Phase 7 — App Bình luận

### Task 12: `task_comments_page.dart` — ô bình luận + ô sửa + bong bóng
**Files:** Modify `lib/ui/task/task_comments_page.dart` :1875 (TextField ⇒ `ChatRichField` + `ChatFormatBar` dưới), :1569 ô sửa, :514-532
render (rich ⇒ `HtmlWidget`), `_submitComment` :1375 (`comment = isRich ? html : text`, mention `@[Tên]` giữ).
- [x] 26/11 — task_comments_page: ChatRichField + nút Aa + ChatFormatBar, `_submitComment` gửi HTML khi có định dạng, `_commentText` rich ⇒ HtmlWidget, ô sửa Quill. Simulator: gửi bình luận đậm ⇒ DB `comments.comment` = `<p>Lỗi bước 2<b> đậm</b></p>`, hiện đậm. Bộ test app `test/ui/chat` + `test/ui/work`: 688 PASS, 4 FAIL CÓ SẴN (chat_list_tabs ×1, workspace_info ×3 — đã chạy lại trên worktree sạch HEAD develop, fail y hệt).

## Phase 8 — Bàn giao
- [x] 26/11 — Tổng kiểm: PHPUnit RichTextTest 10 + ChatRichTextTest 7 + CommentRichTextTest 3 PASS; suite Workspace 387 test còn đúng 7 fail CÓ SẴN (TaskAccess 1, OutsideAssignee 5, TaskList 1); e2e rich-text 7/7 + comment-rich-text 3/3; flutter test chat+work 688 PASS (4 fail có sẵn).
- [x] 26/11 — Review Focus: (1) dán HTML ngoài ⇒ web Quill clipboard chỉ giữ format đăng ký, BE sanitize whitelist (test script/img/onclick); (2) mention/link đọc chữ thuần — test ChatRichTextTest; (3) `a < b` — test BE + e2e + app; (4) 5.000 chữ thuần — test BE + e2e; (5) app cũ nhận HTML ⇒ ghi design.md: phát hành app cùng deploy.
- [x] 26/11 — design.md "Trạng thái" + STATUS.md mục Chat đã ghi; memory `reference_quill_rich_text_chat`.

## Phase 9 — Review độc lập + sửa (26/11/2026, 18:00–19:00)

- [x] Reviewer (subagent, fresh context) rà cả 3 repo: 1 Critical + 7 Important + minors.
- [x] C1 — chữ thuần có `<` liền chữ cái ("Gửi <anh Nam> nhé") bị coi là HTML ⇒ mất chữ: `isRich` CẢ 3 NỀN chỉ nhận HTML canonical (bắt đầu `<p>`/`<ul>`/`<ol>`); test BE/web/app thêm ca này (RED → GREEN).
- [x] I1 — `RichText::toText` dính chữ mục cha–con ("ab"): flush trước khi vào danh sách con; test.
- [x] I2 — app còn 9 chỗ đọc `m.body` (xem trước, banner, ghim, tìm, trích dẫn, sao chép, điền sẵn việc): thêm `ChatMessage.plainBody`, thay hết.
- [x] I3 — web `messagePrefill`/`reminderPrefill`/`ChatSidePanel.urlsOf` + BE `ChatBackfillLinksCommand` dùng chữ thuần.
- [x] I4 — 2 controller bình luận hồ sơ thẩm định giải pháp (dùng chung CommentThread) chưa sanitize: tách trait `NormalizesCommentBody` dùng cho cả 4 controller.
- [x] I5 — app vẽ HTML chưa qua lọc: `ChatRichText.clean()` round-trip khuôn canonical trước `HtmlWidget`.
- [x] I6 — bình luận chỉ còn thẻ rỗng vẫn lưu: BE 422 `comment`; app kiểm chữ thuần rỗng khi sửa.
- [x] I7 — `ChatRichField` tạo FocusNode/ScrollController mỗi build: chuyển StatefulWidget.
- [x] Minor đã sửa: thanh định dạng về trạng thái nhớ sau khi sửa tin (web + app); `@[Tên]` chỉ thay trong phần chữ (CommentNode); sanitizeHtml so tag không phân biệt hoa thường; app `_sameContent` so chữ thuần.
- [x] User 26/11: nút Aa trong ô nhập chat app ⇒ chuyển thành ô "Định dạng văn bản" trong sheet Gửi kèm (nút +); bỏ viền ô "Thăm dò ý kiến"; ô bình luận app: vẽ Pencil 2 phương án (khung "BÌNH LUẬN · APP — thanh soạn bình luận (vẽ lại 26/11)") — CHỜ user chọn.
- [x] 19:20 — User: ô bình luận app dùng nút **+** như chat ⇒ đã code: `_pickAttachment` thành sheet khuôn "Gửi kèm" (Ảnh · Chụp ảnh · Tệp · Định dạng văn bản/Tắt định dạng), bỏ nút 📎 + Aa trong hàng soạn; analyze sạch, hot reload.
- [x] 19:25 — User: "form bình luận xấu, design lại" ⇒ Pencil: **WEB 7** (tab Bình luận panel Nhiệm vụ: hàng phẳng avatar + thân, chip ghim/cảm xúc, phản hồi thụt + vạch, ô soạn ghim đáy có 📎 @ Aa 😊 + Gửi), **WEB 8** (đang trả lời + định dạng bật + sửa tại chỗ), ghi chú thiết kế; **APP 1–3** (danh sách · đang trả lời + thanh định dạng + bàn phím · sheet +). CHỜ user duyệt rồi code lại CommentThread/CommentNode/CommentEditor (web) và task_comments_page (app).
- [x] 19:35 — User: bình luận app chưa có emoji như chat ⇒ thêm nút 😊 trong viên nhập, mở `EmojiStickerPanel` (chỉ emoji) thay bàn phím, chèn tại con trỏ; focus lại ô ⇒ đóng bảng. Analyze sạch, hot reload.
- [ ] Minor hoãn (ghi ở ledger): giới hạn 20.000 raw chưa kiểm FE/app; mention vắt qua thẻ / tên có `'` `&`; toText mất ngắt dòng li nhiều `<p>`; `<table>` dán từ Word mất chữ; `<button>` thô ở 2 popover web; bình luận app bỏ qua maxLines khi thu gọn.
- [x] Kiểm lại sau sửa: PHPUnit RichText 10 + ChatRich 7 + CommentRich 5 PASS; web unit 8/8; app `test/ui/chat`+`work` 689 PASS (4 fail có sẵn); e2e web chạy lại sau sửa: 11/11 PASS (setup + rich-text 7 + comment-rich-text 3), 19:05.

## Phase 10 — Code lại form bình luận theo bản vẽ (26/11/2026, 19:10–19:50) — @cuong61n

**Web** (`worktrees/gop_db-client`, nhánh gop_db):
- [x] `CommentThread.vue` — đầu mục "Bình luận · N" + chip sắp xếp (mặc định **Mới nhất** trên, bấm đổi "Cũ nhất"; ghim luôn ở trên) + chip "Đã ghim N" (bấm = chỉ xem ghim); chip "Xem N bình luận cũ hơn" đặt dưới khi Mới nhất / trên khi Cũ nhất; **ô soạn ghim đáy (`position: sticky`) dùng chung cho bình luận mới + trả lời** (`replyTo` {id, parentId, name}, cấp ≥ 2 gắn về cha cấp 1 như cũ) + avatar của mình (user báo 19:37 lấy sai, 19:55 báo đổi ảnh chat mà ô soạn vẫn ảnh cũ ⇒ lấy `GET chat/profile/{me}` như bình luận: ảnh chat ưu tiên, chưa có ⇒ ảnh hồ sơ; nhớ theo phiên, chưa tải xong tạm dùng ảnh header; đã đối chiếu src ô soạn = src dòng bình luận của mình).
- [x] `CommentNode.vue` — hàng phẳng (avatar 32 · tên đậm 13.5 · giờ xám · "Đã chỉnh sửa" · chip ghim vàng · ⋯ chỉ hiện khi rê chuột), nội dung, tệp (ảnh thumbnail 72 / thẻ icon đỏ + tên + dung lượng), "Đã giải quyết", chân = chip cảm xúc từng emoji (của mình nền + viền teal) · nút thả 24 tròn · Trả lời · "Ẩn/Hiện N phản hồi"; phản hồi thụt 44 + vạch trái #E4E6EB; bỏ bong bóng, bỏ editor con dưới từng bình luận (emit `reply` lên Thread); sửa tại chỗ viền xanh dương + thanh định dạng gọn 28px + Hủy/Lưu có icon. Hỗ trợ sẵn `user.title` (chức danh) nhưng BE `formatComment` chưa trả ⇒ chưa hiện (ruling: không thêm query BE ở bước này).
- [x] `CommentEditor.vue` — khung trắng bo 12: dải "Trả lời X" (✕ thôi ⇒ gỡ "@Tên " tự chèn) → thanh định dạng gọn → chữ 14 → tệp chờ → hàng công cụ **📎 @ Aa 😊** | gợi ý phím (đổi theo trạng thái Aa) | **Gửi** teal (bỏ nút Xoá); nút @ chèn "@" + mở gợi ý (copy `ChatComposer.insertTrigger`), 😊 = `ChatEmojiPicker mode="emoji"` chèn tại con trỏ (copy `insertEmoji`).
- [x] Kiểm Playwright MCP :3002 nhiệm vụ 1944: trả lời ⇒ dải + `@Tên` + payload `parent_id` đúng + HTML đậm; thôi trả lời gỡ @Tên; @ / 😊 / ẩn-hiện phản hồi / thả ❤️ / ghim ⇒ chip "Đã ghim 1" lọc đúng 1 / sắp xếp đảo chiều / sửa tại chỗ PUT HTML; 0 lỗi console (1 lỗi `totalCount` do sửa nhầm ⇒ đã khôi phục).
- [x] 20:05 — User: cửa sổ thấp thì ô soạn ghim đáy bị cắt (sticky trong `.tkp-body` không đủ chỗ) ⇒ bỏ sticky, card `height: 100%` + flex: đầu mục cố định, **danh sách cuộn riêng (`.cmt-scroll`)**, ô soạn luôn ở đáy card; đo Playwright: cửa sổ 500/800/900px ô soạn nằm trọn; 360px thì thân panel chỉ còn ~60px nên vẫn tràn (cần tối thiểu ~170px). Panel Vấn đề (2465) vẫn đúng; modal thẩm định giải pháp (vùng chứa tự cao) ⇒ `height:100%` quy về auto, không đổi hành vi.
- [x] 20:15 — User: vùng xem bình luận bé, đầu mục + ô soạn cao, muốn mặc định cũ → mới ⇒ đầu mục 42px (padding 7/14, chữ 14, badge 20), ô soạn 92px (ô chữ min 36 + hàng công cụ 28 + Gửi 28, avatar 28), hàng bình luận padding 9 / gap 3 / chip 22, phản hồi thụt 42; `newestFirst` mặc định false (chip "Cũ nhất"), tải xong tự cuộn xuống cuối để bình luận mới nhất sát ô soạn (có đích cuộn thì ưu tiên đích); e2e sort cập nhật.
- [x] 20:20 — User: lề trái–phải của card so với khung panel thừa ⇒ `task-panel.scss` `.tkp-body > .cmt-thread` lề âm bù padding thân (14/18/18), bỏ viền + bo, `height: calc(100% + 32px)`; card tràn sát mép ⇒ user 20:25 muốn giữ lề nhỏ ⇒ chốt lề 6px (margin -8/-12/-12, `height: calc(100% + 20px)`, giữ viền + bo), áp cả panel Vấn đề (dùng chung scss); modal thẩm định giải pháp không bị ảnh hưởng (không nằm trong `.tkp-body`).
- [x] 20:30–20:45 — User hỏi "test kỹ luồng định dạng cả web và app chưa" ⇒ chạy đủ toolbar bình luận web (nhiệm vụ 1944): nghiêng/gạch chân/gạch ngang qua nút · màu chữ #DC2626 + "Màu mặc định" · cỡ 18px + về mặc định · nền #FEF08A · danh sách • + thụt lề/lùi lề + danh sách 1. · hoàn tác/làm lại · mở rộng bằng nút + Ctrl+Shift+X ⇒ payload HTML canonical đúng (#193), hiện đúng, mở Sửa nạp lại đủ 5 `<li>` + màu + thanh định dạng. App (simulator, bước 110–118, tab Bình luận nhúng trong chi tiết nhiệm vụ): bật định dạng qua sheet + · màu đỏ qua sheet màu · danh sách • · cỡ Lớn qua sheet cỡ ⇒ gửi, DB `<ul><li>Tu app: <span style="color:#DC2626">…</span></li><li>…<span style="color:#DC2626;font-size:18px"> LON</span></li></ul>` (#194); web hiện đúng #194, app hiện đúng #193 của web (• lồng, 1., màu, cỡ, nền). Lần chạy đầu trên web mất chữ sau khi chọn cỡ — chạy lại 2 lần từng bước không tái hiện (focus vẫn ở ô), ghi nhận theo dõi.
- [x] Sửa thêm 2 lỗi tìm thấy: (1) web `deltaToHtml` để lại `<li></li>` rỗng khi Shift+Enter 2 lần thoát danh sách ⇒ bỏ mục rỗng như BE (unit test RED→GREEN, 9/9); (2) app "Xem thêm" hiện ở bình luận có định dạng nhưng không cắt được gì (HtmlWidget bỏ qua maxLines) ⇒ bình luận rich không thu gọn, chỉ chữ thuần thu gọn như cũ. Lỗi Flutter có sẵn ngoài phạm vi: tràn 0,5px `work_task_detail_page.dart:1181`.
- [x] Dữ liệu thử để lại cho user xem trên nhiệm vụ 1944: #179 (thuần 5 dòng), #180 (• lồng, 1., màu, i/u/s) + phản hồi #183/#184/#185 (3 cấp), #181 (đoạn dài, nền, cỡ), #193 (đủ toolbar web), #194 (từ app); đã xoá #192, #182.
- [x] 20:50 — User hỏi "cả chat nữa test kỹ chưa" ⇒ chạy đủ toolbar chat web (hội thoại 74): i/u/s · cỡ 22 + về mặc định · kiểu Monospace + về mặc định · nền #BBF7D0 · 1. + thụt lề/lùi lề · hoàn tác/làm lại. **Tái hiện lần 2 lỗi "mất chữ"**: ô soạn có đủ chữ (kiểm bằng innerText) nhưng body POST chỉ tới "mono " — tức `html` cache từ sự kiện text-change bị cũ; chạy lại 3 lần có đo từng bước (text/html của ChatComposer, bọc applyPlainDiff/setText/setHtml) không tái hiện, không có lỗi console. **Chốt chặn**: `ChatRichEditor.snapshot()` tính lại chữ thuần + HTML từ Quill NGAY LÚC GỬI và dùng ở cả 3 đường gửi (ChatComposer.submit, CommentEditor.submit, CommentNode.saveEdit) ⇒ body luôn = thứ đang có trong ô, dù sự kiện có hụt. Nguyên nhân gốc chưa rõ — ghi theo dõi.
- [x] Sửa luôn lỗi tràn 0,5px có sẵn `work_task_detail_page.dart:1181` (hàng viên trạng thái + ưu tiên + mắt): bọc phần ưu tiên `Flexible` + cắt "…"; reload không còn lỗi.
- [x] 20:35–20:45 — Chat app (simulator bước 122–137, phòng 74): xem trước ở danh sách hội thoại là chữ thuần; bong bóng vẽ đúng tin rich của web (i/u/s/22px/mono); bật định dạng qua sheet + ⇒ gạch ngang · danh sách 1. · cỡ "Rất lớn" · nền xanh ⇒ gửi, DB `#9079` canonical đúng, web hiện đúng. **Lỗi mới**: nhấn giữ tin có định dạng ⇒ đầu sheet thao tác hiện `<p><s>gach app</s>…` (chatMessagePreview đọc `bodyText ?? body`, tin tạm vừa gửi không có body_text) ⇒ `ChatMessage.plainBody` tự bóc HTML khi thiếu body_text + tin tạm có `bodyText` + preview dùng `plainBody`; đã kiểm lại: đầu sheet "gach app thuong buoc 1 buoc 2 RAT LON nen". Nhấn giữ tin thường vẫn mở menu bình thường.
- [x] e2e `comment-rich-text.spec.ts` thêm 3 test (trả lời qua ô đáy · chip sắp xếp + ghim · nút @ + 😊) ⇒ 7/7; **cả bộ `tests/chat` 23/23 PASS (9,2 phút)**; web unit 8/8.

**App** (`TPE_APP/app`, nhánh develop) — `lib/ui/task/task_comments_page.dart`:
- [x] Danh sách hàng phẳng theo APP 1: avatar 34 (phản hồi 28), tên + chip "Đã ghim" + giờ phải, nội dung, tệp, "Đã giải quyết", chân = chip cảm xúc (`_reactionChip`, của mình tint phân hệ; chạm = thả/bỏ, giữ = ai đã thả) · nút thả 24 tròn mở picker · Trả lời · "Xem/Ẩn N phản hồi" (`_repliesExpanded` + `_collapsedIds`) · ⋯; phản hồi thụt 40 + vạch trái 2px; gốc ngăn bằng vạch #EEF0F3; chip "Xem N bình luận cũ hơn"; bỏ bong bóng + cụm cảm xúc góc + `_reactionLook`.
- [x] Ô soạn theo APP 2: dải "Trả lời <Tên>" nền phân hệ 8% tràn ngang; **thanh định dạng chuyển xuống DƯỚI hàng soạn** (trên bàn phím, như chat); 😊 căn giữa với chữ gợi ý (user báo lệch 19:38 ⇒ bọc `ConstrainedBox(minHeight 40) + Align` như composer chat).
- [x] Simulator iPhone 15 (bước 94–109, `shots/` phiên GĐ43): trả lời + bật định dạng qua sheet + ⇒ gõ đậm ⇒ gửi ⇒ phản hồi lồng có vạch + "Ẩn 1 phản hồi"; thả ❤️ ⇒ chip; ẩn/xem phản hồi; ⋯ ⇒ Ghim ⇒ chip "Đã ghim"; 😊 ⇒ bảng emoji; 0 lỗi Flutter mới; đã dọn dữ liệu thử (bỏ ghim, bỏ ❤️, xoá phản hồi 175).
- [x] `dart analyze` sạch; `flutter test test/ui/chat test/ui/work` 689 PASS, 4 fail CÓ SẴN (y hệt baseline).

### Checkpoint — 26/11/2026 19:50
Vừa hoàn thành: Phase 10 — code lại form bình luận web + app theo bản vẽ WEB 7–8 / APP 1–3, sửa 2 góp ý user (avatar ô soạn web, 😊 lệch trên app); test: e2e chat 23/23, web unit 8/8, PHPUnit 22, flutter 689 (4 fail có sẵn), simulator bước 94–109.
Đang làm dở: —
Bước tiếp theo: user xem lại UI mới (web :3002 tab Bình luận nhiệm vụ 1944; app simulator màn Bình luận) ⇒ commit/push khi được bảo (api + client gop_db, app develop) ⇒ deploy: migrate + build client + phát hành app cùng lúc. Tuỳ chọn: BE trả `commentator.title` để hiện chức danh như bản vẽ.
Blocked: —

## Phase 11 — Phát hành (27/11/2026) — @cuong61n
- [x] Commit + push GĐ44: hrm-api gop_db `3af7765ff` + merge `origin/gop_db` (conflict ChatPresenter: preview dùng `plainBody()` + nhánh lịch sử cuộc gọi); hrm-client gop_db `ad2e7049f` + merge; app develop `d696d7b` + merge origin/develop (gọi thoại/video LiveKit; conflict import chat_models giữ cả 2), `fvm flutter pub get` + analyze 0 lỗi.
- [x] App: merge develop → tpe (`c4bd5fe`), HRM TPE **giữ 2.4.0, build 116** (user chốt: 117→116 vì bản 116 cũ chưa lên TestFlight), push tpe `2e6727d`.
- [x] 27/11 ~07:10 — Prod web TPE: `~/build_tpe.sh` trên hrm-prod xong (EXIT 0): api `10bee76cc`, client `5382b4d60`, migration `add_body_text_to_chat_messages_table` đã chạy (batch 494), Nuxt build 238s, `route:cache` lại; https://hrm.eteksofts.com 200.
- [x] 07:40 — iOS build 116 upload + gán external + Beta Review APPROVED — **NHƯNG SAI**: user cài không thấy chức năng mới. Kiểm `strings` App.framework trong IPA: có key cũ, KHÔNG có `chat_fmt_bold`/`livekit`/`chat_me_image` ⇒ IPA là code cũ. Nguyên nhân: `flutter build ipa` lỗi Xcode *"Cycle inside Runner"* (script phase "TPE call background modes" của tính năng gọi điện đứng trước "Embed Foundation Extensions" của Share Extension TpeProd) nhưng `tools/build_and_run_app.sh` không dừng, chạy tiếp `xcodebuild -exportArchive` từ `build/ios/archive` CŨ (25/11) rồi upload. Đã expire build 116 + rút khỏi nhóm external qua API.
- [x] Sửa: chuyển script phase xuống sau "Thin Binary" (cùng input Info.plist, không còn vòng), `eval $cmd || exit 1` trong build script, xoá archive cũ, bump build 117 (giữ 2.4.0), push tpe.
- [x] 08:00 — iOS build 117: build-only (`make build_tpeProd_ipa`, không tự upload), kiểm IPA: App.framework 30,5 MB (cũ 28,9), có `chat_fmt_bold`/`comment_react_add`/`chat_me_image`/livekit, 2.4.0 (117), `UIBackgroundModes` đã thêm, 6 file appex, profile App Store ⇒ mới upload (`make upload_tpeProd`). Fix lỗi cũng đã merge ngược tpe → develop.
- [x] 08:10 — iOS build 117 VALID, gán nhóm external "Tân Phát", Beta Review APPROVED (what to test đã ghi).
- [x] Android TpeProd: AAB 116 đúng code mới (kiểm libapp.so có chat_fmt_bold + livekit) nhưng Play API 403 "must let us know whether your app uses Foreground Service permissions" (FOREGROUND_SERVICE_MICROPHONE/CAMERA từ gọi điện) ⇒ đã tải AAB 116 lên kênh nội bộ dạng nháp qua Play Console (Playwright, user đăng nhập) để Play nhận quyền; mục khai báo chưa hiện ở App content. Build lại AAB 117 cho đồng bộ iOS.
- [ ] 08:25 — Android: AAB 117 (kiểm libapp.so có code mới, ký đúng) đã vào thư viện Play; bản nháp **production** (release 66) đã tạo với 117 + ghi chú `vi`, bị chặn 1 lỗi: khai báo "Quyền cho dịch vụ trên nền trước" (FOREGROUND_SERVICE_CAMERA + MICROPHONE). Form bắt buộc **đường link video minh hoạ** cho mỗi quyền — chưa có video ⇒ CHỜ user đưa link (YouTube/Drive) hoặc quay. Mô tả quyền đã soạn sẵn. Lưu ý: Play đã ghi nhận versionCode 117 (API báo "already used") nên mọi bước còn lại phải qua Console, không qua `play_release.py`.
- [x] 08:45 — Video minh hoạ tự quay: iOS simulator KHÔNG tham gia được cuộc gọi (tự từ chối cuộc đến, cuộc đi tự huỷ — không CallKit/mic) ⇒ dùng **web prod** (Playwright, cuong61n) làm bên nhận, **Android emulator** (dnstester, bản tpeProd debug) làm bên gọi. `screenrecord` trên emulator API 29 lỗi "Encoder failed (-38)" ⇒ chụp `screencap` 4,3 fps rồi ffmpeg ghép `hrm-tpe-call-demo.mp4` (540×1140, 100s): gọi thoại → web nhận → Home (dumpsys: `CallForegroundService isForeground=true`, kênh `tpe_call_ongoing`) → kéo thông báo → mở lại app, cuộc gọi vẫn chạy → bật camera → Home → mở lại → kết thúc (web ghi 1 phút 15 giây). Bước tiếp: up YouTube không công khai, điền 2 link vào form Play.
- [x] 08:55 — YouTube không công khai https://www.youtube.com/watch?v=wyywUSrktSY (kênh Giai Điệu Đêm của user, tài khoản đang đăng nhập); điền link vào cả 2 quyền (Camera: "Luồng video của camera ở chế độ nền", Micrô: "Đầu vào âm thanh ở chế độ nền"), lưu. Trang xem xét production 117 (2.4.0) hết lỗi; user chốt "Phát hành luôn" ⇒ đã bấm "Gửi các thay đổi đi xem xét" (trạng thái "Các thay đổi đang được xem xét", kiểm tra nhanh ≤ 14 phút rồi tự gửi Google duyệt; chế độ xuất bản có quản lý tắt ⇒ duyệt xong tự phát hành 100%).
- [x] 09:00 — Kênh Phát hành công khai: **"Đang xem xét bản phát hành 117 (2.4.0)"** (178 quốc gia, 347 lượt cài). Dọn: huỷ bản nháp kênh nội bộ 117. Lưu ý: simulator iPhone 15 đã bị thay app tpeLocal bằng bản tpeProd (phiên `flutter run` GĐ43 PID 26607 không còn); emulator Pixel_4_API_29 đang đăng nhập dnstester (bản tpeProd debug).

### Checkpoint — 27/11/2026 09:00
Vừa hoàn thành: Phát hành GĐ44 + gọi thoại/video: prod web TPE (api/client gop_db, migration body_text) · iOS HRM TPE 2.4.0 (117) TestFlight external APPROVED (bản 116 sai code đã expire) · Android 117 (2.4.0) gửi Google xem xét kèm khai báo Foreground service (video demo YouTube không công khai).
Đang làm dở: —
Bước tiếp theo: — (27/11 ~09:30 Google đã duyệt: production `completed` 117 (2.4.0) rollout 100%, kiểm bằng `play_release.py status` + Play Console).
Blocked: —

## Phase 12 — Phát hành lại 2.4.0 (118) kèm code develop mới (27/11/2026) — @cuong61n
- [x] 09:40 — `git merge origin/develop` vào `tpe` (fast-forward tới `522c66a`: gọi điện iOS đổ chuông khi app tắt/máy khoá `defd79b`, tệp chat 200 MB `554b482`). Bump `TpeProd.xcconfig` + `build.gradle` tpeProd → 118 (2.4.0), commit `a863331`, push `origin tpe`. `pub get` + `pod install` xong.
- [x] 13:45 — IPA 118 build xong (`flutter build ipa` tự export lỗi "No Accounts" như mọi lần, script export lại bằng khoá ASC): Info.plist 118/2.4.0, UIBackgroundModes voip+audio, ShareExtension.appex có, `strings` App.framework có `chat_fmt_bold`/`livekit`/`chat_me_image` (90 dòng), profile App Store. Upload altool OK (cảnh báo SDK 26.2 → tới 04/2027 phải Xcode 27). Chờ VALID rồi gán nhóm external "Tân Phát" + gửi duyệt qua ASC API.
- [x] 13:45 — AAB 118 (140 MB) ký SHA-1 65:1B…FA:F8 đúng, libapp.so có code mới (89 dòng). `play_release.py release` production 100% + ghi chú vi → Google nhận xét duyệt (lần này API không bị chặn FGS vì khai báo đã lưu ở bản 117).
- [x] 14:05 — iOS 118 VALID → ghi chú + gán nhóm external "Tân Phát" (204) + gửi Beta Review (201). Android 118 đang Google xem xét.
- [x] 16:50 — Google TỪ CHỐI bản 118 (gửi 73, 13:47): "Thông tin đăng nhập không chính xác" — mục Nội dung ứng dụng → Thông tin đăng nhập đang khai `namdangit@gmail.com/2025Dns@1`, đăng nhập prod trả 422. Đổi sang tài khoản công khai `dnstester@gmail.com` (đã kiểm login prod 200) + hướng dẫn tiếng Anh, Lưu, bấm "Gửi 1 nội dung thay đổi để được xem xét" → trang Tổng quan hiện "Các thay đổi đang được xem xét". Đồng thời đổi tài khoản demo Beta App Review TestFlight (betaAppReviewDetail app 6446807087) sang `dnstester@gmail.com` theo yêu cầu user.
- [x] 17:10 — Google duyệt lại (gửi 74, 16:39): **Đã xuất bản**, production Đang hoạt động 2.4.0 (118). Phát hành 118 hoàn tất cả iOS lẫn Android.
