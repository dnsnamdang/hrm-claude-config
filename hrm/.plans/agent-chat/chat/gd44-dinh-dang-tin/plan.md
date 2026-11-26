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
- [ ] Test: POST bình luận task rich có `<script>` ⇒ lưu sạch; thông báo cho người được @ có `note` không chứa `<`; 5.001 chữ ⇒ 422.
- [ ] Làm, chạy ⇒ PASS.

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
- [ ] Test (Node): `deltaToHtml([{insert:'Kế hoạch',attributes:{bold:true}},{insert:'\n'},{insert:'a'},{insert:'\n',attributes:{list:'bullet'}},
  {insert:'b'},{insert:'\n',attributes:{list:'bullet',indent:1}}])` === `'<p><b>Kế hoạch</b></p><ul><li>a<ul><li>b</li></ul></li></ul>'`;
  size `'18px'` ⇒ `font-size:18px`; `color:'#DC2626'` + `background:'#FDE68A'` cùng 1 span ⇒ `style="color:#DC2626;background-color:#FDE68A"`;
  dòng trống ⇒ `<p><br></p>`; chữ `<` escape `&lt;`; `htmlToText` ngược lại ra `"Kế hoạch\na\nb"`; `isRich('a < b')===false`.
- [ ] Chạy ⇒ FAIL → viết → PASS.

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
- [ ] Dựng editor + toolbar + 2 popover; chạy `:3004`, Playwright MCP thử gõ tiếng Việt (telex), Ctrl+B, danh sách, Tab, dán HTML từ web
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
- [ ] Viết spec ⇒ FAIL; làm ⇒ PASS; e2e cũ `chat-*.spec.ts` vẫn PASS.

### Task 7: Hiển thị tin rich — `ChatMessageItem.vue` + xem trước / trích dẫn
**Files:** Modify `components/chat/ChatMessageItem.vue` `html()` :563 (rich ⇒ `sanitizeHtml(body)` rồi tô @ / @all / link trên text node;
thuần ⇒ như cũ), style `.cm__text` cho `ul/ol/li/p/span` (p margin 0, li padding-left, line-height giữ) · `utils/chat/chatFormat.js`
`previewText` :167 dùng `message.body_text ?? message.body` · ChatComposer `cc__ctx` :17 (`body_text`) · ChatPane / ForwardModal / ghim /
tìm kiếm chỗ nào hiện `body` ⇒ `body_text ?? body`; copy tin ⇒ chữ thuần.
- [ ] e2e thêm vào `rich-text.spec.ts`: tin rich hiển thị `b` trong `.cm__text`, @Tên vẫn `span.cm__mention`, xem trước ở cột hội
  thoại không chứa `<`.
- [ ] Làm ⇒ PASS.

## Phase 4 — Web Bình luận

### Task 8: `CommentEditor.vue` + `CommentNode.vue` dùng `ChatRichEditor` + `ChatFormatToolbar`
**Files:** Modify `components/comments/CommentEditor.vue` (thay `contenteditable` :4-11 bằng `ChatRichEditor`; chip @ ⇒ format `mention`
với `data-id`, serialize ra `@[Tên]` trong chữ thuần như cũ; `submit()` :451 `comment = isRich(html) ? html : rawText`; footer :45 thêm nút Aa +
thanh; Enter gửi, Shift+Enter xuống dòng giữ) · `CommentNode.vue` `renderContent` :495 (rich ⇒ `sanitizeHtml` + thay `@[x]`), ô sửa
:23 `textarea` ⇒ `ChatRichEditor` (mở thanh nếu rich) · `IssuePanel.vue` / `TaskPanel.vue` không đổi props.
- [ ] e2e `e2e/tests/chat/comment-rich-text.spec.ts`: mở nhiệm vụ, bật Aa, gõ đậm + @ ⇒ request `comment` HTML + `mention_ids[]`; hiển thị
  `b`; bình luận thuần cũ vẫn hiện `@Tên`.
- [ ] Làm ⇒ PASS.

## Phase 5 — App dùng chung (TPE_APP nhánh `feature/chat-dinh-dang`)

### Task 9: `lib/ui/chat/rich/chat_rich_text.dart` — bảng màu, Delta⇄HTML canonical, isRich, toText
**Files:** Create `lib/ui/chat/rich/chat_rich_text.dart` · Test `test/ui/chat/rich/chat_rich_text_test.dart`.
**Produces:** `ChatRichText.textColors / bgColors` (12+12 `Color`, cùng thứ tự web) · `fontSizes` (`null,'12','18','22'` ↔ px) ·
`isRich(String?)` · `deltaToHtml(Document)` (TỰ VIẾT theo khuôn, KHÔNG dùng `vsc_quill_delta_to_html` để ra đúng canonical) ·
`htmlToDocument(String)` (dùng `flutter_quill_delta_from_html` như `meeting_rich_editor.dart` :87, map `font-size:18px` ⇒ attr size '18',
nested `ul` ⇒ indent) · `toText(String)` · `formatOnKey='chat_format_on'` + `loadFormatOn()/saveFormatOn(bool)`.
- [ ] Test: cùng 6 ca với Task 4 (Delta ⇒ HTML đúng từng ký tự; round-trip `htmlToDocument(deltaToHtml(d))` giữ attrs; `isRich('a < b')==false`).
- [ ] `fvm flutter test test/ui/chat/rich` ⇒ FAIL → viết → PASS.

### Task 10: `ChatFormatBar` + `ChatRichField` + bảng màu + màn mở rộng
**Files:** Create `lib/ui/chat/rich/chat_format_bar.dart` (hàng 46px cuộn ngang, nút 36 theo design APP 2, mờ phải; props
`controller: QuillController`, `expanded`, `onToggleExpand`, `onPickColor(kind)`) · `lib/ui/chat/rich/chat_color_sheet.dart` (thay bàn phím:
tab Màu chữ / Màu nền, lưới 6×2 vòng 46, "Màu mặc định") · `lib/ui/chat/rich/chat_size_sheet.dart` (4 cỡ + 3 kiểu chữ) ·
`lib/ui/chat/rich/chat_rich_field.dart` (QuillEditor 1–5 dòng trong viên `ChatColors.inputBg`, nút Aa + 😊 bên trong như design APP 1; khi
`formatOn=false` ⇒ `QuillController.readOnly=false` nhưng `toolbarButtons` ẩn và phím tắt tắt; expose `text`, `html`, `plainLength`) ·
`lib/ui/chat/rich/chat_expand_page.dart` (toàn màn: "Soạn tin nhắn" + Gửi, thanh dưới, `Navigator.pop(html)`).
- [ ] Widget test `test/ui/chat/rich/chat_format_bar_test.dart`: bấm B ⇒ `controller.getSelectionStyle()` có bold; bấm ⤢ gọi
  `onToggleExpand`; `ChatRichField` gõ "x" ⇒ `html==''`? (chữ thuần ⇒ `isRich=false`, `text=='x'`).
- [ ] Làm ⇒ PASS; chạy simulator kiểm bàn phím tiếng Việt + Aa + bảng màu (skill app-simulator-test), chụp ảnh scratchpad.

## Phase 6 — App Chat

### Task 11: `composer.dart` + `chat_room_page.dart` + `message_bubble.dart`
**Files:** Modify `lib/ui/chat/widget/composer.dart` (TextField ⇒ `ChatRichField`; `onSend(String text)` ⇒ `onSend(String body)` với
`body = isRich ? html : text`; giữ `ValueKey` cũ; bộ đếm theo `plainLength`) · `chat_room_page.dart` `_send` :1388 / `_saveEdit` :1421 /
`_startEdit` :1511 (nạp `htmlToDocument(m.body)`, mở thanh nếu rich) / `chatTriggerAt` :1238 (@ # đọc từ `controller.document.toPlainText()`
+ selection) / nháp · `message_bubble.dart` :576 (rich ⇒ `HtmlWidget(sanitized, customStylesBuilder` map `font-size/color/background`,
`textStyle: base`; @Tên / @all / link tô bằng `customWidgetBuilder` hoặc tiền xử lý HTML bọc `<a data-emp>`) · `chat_models.dart` :699
thêm `bodyText` (`body_text`), `previewText` :446 dùng `bodyText ?? body` · danh sách hội thoại / trích dẫn / ghim / tìm kiếm dùng `bodyText ?? body`.
- [ ] Widget test `test/ui/chat/message_bubble_rich_test.dart`: tin `body='<p><b>Kế hoạch</b></p>'` ⇒ có `HtmlWidget`, text "Kế hoạch" đậm;
  tin thuần vẫn `Text`/`ChatLinkText`; `ChatMessage.fromJson` đọc `body_text`.
- [ ] Làm ⇒ PASS; `make gen` nếu đổi model freezed; simulator: gửi rich từ app ⇒ web hiện đúng; gửi rich từ web ⇒ app hiện đúng (so ảnh).

## Phase 7 — App Bình luận

### Task 12: `task_comments_page.dart` — ô bình luận + ô sửa + bong bóng
**Files:** Modify `lib/ui/task/task_comments_page.dart` :1875 (TextField ⇒ `ChatRichField` + `ChatFormatBar` dưới), :1569 ô sửa, :514-532
render (rich ⇒ `HtmlWidget`), `_submitComment` :1375 (`comment = isRich ? html : text`, mention `@[Tên]` giữ).
- [ ] Widget test: bình luận rich hiện đậm; gửi ⇒ payload `comment` HTML.
- [ ] Làm ⇒ PASS; simulator kiểm.

## Phase 8 — Bàn giao
- [ ] Tổng kiểm: PHPUnit `--filter Chat|Comment`, e2e `chat/*.spec.ts`, `fvm flutter test` (≥ 609 cũ + mới) — ghi kết quả thật vào plan.
- [ ] Rà lại 5 mục Review Focus trên dữ liệu thật (dán từ Word; tin cũ; app cũ).
- [ ] Cập nhật `design.md` "Trạng thái", `.plans/STATUS.md` mục Chat, ghi "cần phát hành app cùng lúc deploy api" vào tổng kết.
