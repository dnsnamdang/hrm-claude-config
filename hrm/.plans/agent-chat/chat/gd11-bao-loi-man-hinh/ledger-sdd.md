# SDD ledger — plan: /Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/agent-chat/chat/gd11-bao-loi-man-hinh/plan.md

Spec: design.md cùng thư mục. Nhánh `gop_db-chat-bao-loi` (api từ 70aacc60d, client từ f0a0e778b). User cho phép 14/11 (phạm vi ở chat).
Base trees (no-commit snapshots, scripts snap.sh/pkg.sh trong workspace): api 488ecf3 · client a51cc88

## Rulings tiền kiểm
- Ruling: KHÔNG commit (user + CLAUDE.md) — implementer không commit; review dùng tree snapshot (snap.sh: index tạm, không đụng index thật/stash) — sai thì chỉ mất tiện truy vết, không hại repo.
- Ruling: migration Task 1 — implementer chỉ chạy `--pretend`; controller chạy thật `--path` sau khi xem pretend (đã được user cho phép đúng file này) — sai thì chậm 1 bước.
- Ruling: e2e (HRM/e2e) không thuộc git — review Task 9 đọc file trực tiếp.
- Ruling: tên mã quyền `assign.bao_loi_cai_dat.manage` giữ theo plan.

## Bảng tiền kiểm
| Cặp/Task | Chung | Kết quả |
|---|---|---|
| T1→T2 | bảng/model `ChatBugReportSetting`, mã quyền | khớp |
| T2→T7 | GET/PUT settings, khoá trả về `workspace_id, workspace_name, conversation_id, is_member, can_manage` | khớp |
| T3→T4 | `send(... ['bug_report'])`; route thường không nhận | khớp |
| T3→T8 | presenter `bug_report` | khớp |
| T4→T7 | POST body (target_type/target_id/category/description/files/context.*) | khớp |
| T5→T7 | `snapshot()`, `maskSensitive()` | khớp |
| T6→T7 | `capturePage()` → Blob|null, `data-bug-report-ignore` | khớp |
| T7→T9 | testid chưa định ⇒ Ruling: T7 gắn `data-testid` ở khối bọc: `bug-report-tab`, `bug-report-modal`, `bug-report-submit`, `bug-report-setting-link` | ghi vào dispatch T7 |
| T1 tự nhất quán | migration + model + catalog | ok |
| T2 | 7 test ↔ interfaces | ok |
| T3 | test chuyển tiếp khoá Q12 | ok |
| T4 | test 422 đồng thời ↔ request | ok |
| T5 | không unit test JS (repo không có) — kiểm bằng MCP | ok (ghi nhận) |
| T6 | cài gói npm — đã được cho phép đúng `html2canvas@1.4.1` | ok |

## Tiến độ
- Ruling: gộp Task 1+2 vào 1 dispatch + 1 review (T1 chỉ là nền của T2) — sai thì review T1 hơi lẫn.
- Ruling: implementer T1 được chạy migration `--path` sau pretend (bảng mới cần cho PHPUnit T2; user đã cho phép đúng file) + catalog-sync (dừng nếu sync đụng mã khác) — sai thì phải rollback 1 bảng rỗng.
- Task 1+2: dispatched (sonnet), base trees api 488ecf3
- Task 1+2: implementer DONE_WITH_CONCERNS — tree api 666490c1b7c86ec3eeda90e81df27756cdcef65d. catalog-sync dry-run: +7 mã, sửa 826 (DB local lệch) ⇒ KHÔNG sync.
- Ruling: quyền `assign.bao_loi_cai_dat.manage` ở local chèn tay 1 dòng permissions (memory hrm-them-permission-moi) lúc Task 9, không sync cả loạt — sai thì e2e thiếu quyền, dễ thấy.
- Ruling: 422 dạng `errors.field = "chuỗi"` theo BaseRequest các request Chat sẵn có — giữ, khớp FE chat hiện tại.
- Task 1+2: review ✅ spec + quality Approved. ⚠️ đã giải: migration có phép user 14/11; PermissionCode::ensure theo Catalog, thiếu quyền DB ⇒ false (fail-closed).
- Task 1+2: minor (deferred): PUT thiếu khoá workspace_id ⇒ coi null = xoá cài đặt (cân nhắc `present`).
- Task 1+2: minor (deferred): test setUp chèn tay dòng permissions vì DB local chưa sync.
- Task 1+2: complete (trees api 488ecf3..666490c, review clean)
- Task 3: dispatched (sonnet), base tree api 666490c
- Task 3: implementer DONE — tree api 754ceb16af509edaedbabb64a3d72195b61340b1
- Task 3: review ✅ Approved. ⚠️ giải: edit() chỉ update body ⇒ meta giữ; test số từ report implementer.
- Task 3: minor (deferred): chưa test bug_report + card ⇒ 422; nháy kép test dòng 192; thứ tự kiểm bug_report trước sticker.
- Task 3: complete (trees api 666490c..754ceb1, review clean)
- Task 4: dispatched (sonnet), base tree api 754ceb1. Nhắc: send() đòi body ⇒ truyền description làm body; Task 4 phải làm sạch bug_report.
- Task 4: implementer DONE — tree api ef1fe4d06542d79686a6a11bb4c7ab82f8dccd3b (Cache::flush trong test = driver array, an toàn; CHAT_PUSH_ENABLED=false)
- Task 4: review — spec ✅, quality Needs fixes: Important throttle không prefix trùng khoá Agent ask (đã tự kiểm vendor ThrottleRequests:50/63).
- Task 4: minor (deferred): throttle chạy trước validate/403 ⇒ 422/403 cũng tốn lượt (FE validate trước khi gửi, chấp nhận) · store chỉ bắt ValidationException (lỗi khác 500) · test reporter chỉ kiểm fullname · thiếu test 1–1 NV nghỉ / hội thoại không tồn tại · hội thoại không tồn tại trả 403 (cố ý, FE xử lý cả 403/404).
- Task 4: carry to Task 7/8: BE lưu context.url & api_errors.path nguyên văn ⇒ FE PHẢI che token (maskSensitive); context.url không kiểm http(s) ⇒ FE render link phải chặn `javascript:` (chỉ cho http/https hoặc đường dẫn tương đối); 429 trả body mặc định Laravel ⇒ FE toast câu riêng.
- Task 4: fix round 1 dispatched (resume implementer)
- Task 4: fix round 1/5 (3 addressed, 0 open — throttle prefix bug-report, docblock, null toasts; trees ef1fe4d..8ec1236)
- Task 4: complete (trees api 754ceb1..8ec1236, review clean after fix)
- Ruling: gộp Task 5+6 (2 util client độc lập, nhỏ) vào 1 dispatch + 1 review — sai thì review lẫn 2 phần.
- Ruling: KHÔNG `nuxt build` trong worktree (:3080 là `nuxt` dev dùng chung .nuxt ⇒ build đè); kiểm html2canvas dịch được bằng dev server webpack 4/Node 12 (import động) — sai thì lỗi build prod lộ lúc deploy; nhắc kiểm build trước deploy.
- Task 5+6: dispatched (sonnet), base tree client a51cc88
- Task 5+6: implementer DONE_WITH_CONCERNS — tree client 8e53a7a72804b6e0c2d570a751c27e91d1c2d149. pageCapture chưa chạy thật (chưa ai import) ⇒ Task 7 phải đo chụp end-to-end + chunk html2canvas tải được.
- Ruling: yarn.lock KHÔNG có html2canvas (repo có cả yarn.lock + package-lock.json) — không chạy yarn (sợ đổi hàng loạt); ghi deploy: kiểm build_tpe.sh dùng npm hay yarn; nếu yarn --frozen-lockfile sẽ fail ⇒ báo user — sai thì build prod lỗi lúc deploy (thấy ngay).
- Task 5+6: review ✅ Approved. ⚠️ giải: user đã cho phép html2canvas@1.4.1; build Node 12 chưa chạy (ruling trên).
- Task 5+6: minor (deferred, NÊN sửa ở đợt cuối): unhandledrejection ghi cả AxiosError (trùng api_errors) · request bị huỷ (cancel) tạo mục rỗng đẩy lùi lỗi thật · js error mất stack/file:line · toast không qua maskSensitive / object ⇒ "[object Object]" · path gồm origin · timeout không huỷ html2canvas · thứ tự comment axios.js.
- Task 5+6: complete (trees client a51cc88..8e53a7a, review clean)
- Final-fix list: tên quyền trong Catalog là "Cài nhóm nhận báo lỗi màn hình" ≠ spec "Cài nhóm tiếp nhận báo lỗi" (Q13) ⇒ sửa Catalog + test.
- DB local: đã chèn dòng permissions (id 1000000939, tên theo spec) + role tạm TMP_GD11_BaoLoi (id 1000001125, công ty 1) cấp NV 13. Gỡ: scratchpad/revoke_gd11.php (chạy bằng tinker --execute). 
- Task 7: dispatched (opus), base tree client 8e53a7a
- Task 7: implementer DONE (concerns) — tree client fbfb264acf2ca55059583113066fdc3e5a7c8617. Đo: tab 22×72 giữa dọc, 0 chồng nút 3 màn × 2 cỡ; chụp ~1s PNG 233KB / webp 88KB; luồng nhóm + 1–1 + Xem chạy.
- Ruling: env.CLIENT_BUILD (nuxt.config.js) để đợt sửa cuối, báo user trước vì sửa nuxt.config làm :3080 tự nạp lại — sai thì "Phiên bản" hiện "Không xác định" tới lúc đó.
- Ruling: lệch skill vs mockup (chữ nút > 3 từ; mã 5xx tô đỏ) ⇒ theo SKILL (CLAUDE.md "skill thắng spec về hình thức"), đưa vào fix; báo user xác nhận ở cuối — sai thì đổi lại chữ nút.
- Ruling: popup cài đặt chỉ liệt kê nhóm người cài là thành viên (chưa có API liệt kê mọi nhóm công ty) — chấp nhận, báo user — sai thì quản trị không ở trong nhóm không cài được.
- Ruling: logo S3 trống trong ảnh chụp (CORS) — chấp nhận (Review Focus 1 đã lường) — 2 lỗi console mỗi lần chụp ⇒ minor.
- Test data còn lại local: hội thoại 1–1 3062, 3 ảnh tải lên; nhóm 4580 đã đóng; tin 12797/12798 đã thu hồi.
- Task 7: review — spec ❌ (429 toast tự đặt chữ thay vì chữ BE) · quality Needs fixes: Important chữ nút > 3 từ (3 nút), mã 5xx tô đỏ.
- Ruling: 429 giữ câu tiếng Việt của FE (BE trả "Too Many Attempts." tiếng Anh; carry note Task 4 đã định FE tự đặt câu) — sai thì chỉ khác câu chữ.
- Task 7: ⚠️ giải: print/auth không gắn Topbar ⇒ không có tab (grep layouts); luồng GET workspaces đã chạy thật trong report.
- Task 7: minor (deferred): upload từng ảnh 1 request (giữ để ảnh lỗi không chặn gửi chữ) · select dùng V2BaseSelectRemote thay InModal (Remote tự gắn dropdownParent) · thẻ <a>/div role=button thô · unsavedModalMixin 500ms prefill edge · phím tắt nuốt trong ô nhập (đúng Review Focus 5) · no-enforce-focus ⇒ Esc sau "Ở lại".
- Task 7: fix round 1 dispatched (resume implementer): chữ nút, màu 5xx, Chụp lại khi 5 ảnh, danh sách nhóm cài đặt, testid submit.
- Task 7: fix round 1/5 (5 addressed, 0 open — chữ nút, màu 5xx, Chụp lại, danh sách nhóm cài đặt, testid; trees fbfb264..7f851c3)
- Task 7: minor (deferred): popup cài đặt đọc tối đa 3 trang × 100 nhóm (công ty > 300 nhóm bị cắt); nhánh trang 2–3 chưa chạy thật.
- Task 7: complete (trees client 8e53a7a..7f851c3, review clean after fix)
- Task 8: dispatched (sonnet), base tree client 7f851c3
- Task 8: implementer DONE — tree client 90f3f5a7eb592a146987be95be35c7bf34ca3393; e2e chat-giao-dien+toolbar-zalo+panel-phai 19 passed (BASE_URL :3080, CHAT_API :8080). Tin test 12800-12802 đã thu hồi.
- Task 8: review ✅ Approved. ⚠️ giải: shape bug_report do BugReportService whitelist (toasts/js_errors lọc is_string); badge info/other chưa nhìn ⇒ e2e T9 phủ.
- Task 8: minor (deferred, SỬA ở đợt cuối): safeBugUrl phải chặn "/\\x" (trình duyệt coi "\" như "/" ⇒ "//host" ngoài) + test cho safeBugUrl; dòng URL/lỗi API đầu thiếu word-break; nhãn thu gọn thiếu tóm tắt "(công ty, thiết bị, phiên bản, n lỗi API)"; phần tử sai kiểu không chặn.
- Task 8: complete (trees client 7f851c3..90f3f5a, review clean)
- Task 9: dispatched (sonnet)
- Task 9: implementer DONE — bug-report 7 passed; hồi quy chat 11 bộ đều pass (chat-core cần CHAT_TOKEN_OUT, topbar-shortcuts cần AUTH_STATE :3080). B4 giả canvas.toBlob null (chunk html2canvas dev không bắt được bằng route). Dọn: 16 nhóm test rò lần đầu đã đóng tay; cài đặt cty 1 = NULL như cũ.
- Ghi chú: tin 12859 "cxcxc" (NV 13, 16:15, nhóm 1612, có bug_report) — nghi USER tự thử trên :3080 ⇒ KHÔNG đụng.
- Task 9: minor: bấm Gửi trước khi settings nạp xong ⇒ prefill xoá lỗi "Gửi tới", không gửi, không báo (race nhỏ).
- Final review: trees api 8ec12365a80edd7db104ab477325f7d9df2f8337 · client 90f3f5a7eb592a146987be95be35c7bf34ca3393
- Task 9: review — spec ✅, quality Needs fixes: Important B7 kiểm "không có link" trước khi can_manage nạp (pass rỗng) · afterAll PUT originalSettingWs=null khi beforeAll hỏng sớm (ghi đè cài đặt thật).
- Ruling: gộp 2 Important của Task 9 vào ĐỢT SỬA CUỐI (final review đã chạy song song) — 1 fixer + 1 re-review cho tất cả — sai thì Task 9 thiếu vòng review riêng, re-review cuối vẫn kiểm.
- Task 9: minor (deferred): assert "không thêm ký tự" không thể fail · đọc __toBlobCalls sớm (flake) · aName fallback '' · aId/cId cố định · waitForTimeout · zIndex 1030 cứng · rate limit chỉ clear ở beforeAll.
- Final review: ready with fixes. Important: khối tin lấy lỗi API CŨ NHẤT (đã tự kiểm: push cũ→mới, block [0]) · CLIENT_BUILD chưa khai · tên quyền Catalog lệch Q13. MUST-FIX minor: word-break .bgb__line · unhandledrejection ghi lỗi axios.
- Ruling: CLIENT_BUILD KHÔNG đưa vào đợt sửa — hỏi user (sửa nuxt.config.js làm :3080 tự nạp lại; user có dấu hiệu đang thử :3080 lúc 16:15) — sai thì "Phiên bản" trống tới khi user cho phép.
- Ruling: thêm vào đợt sửa (rẻ): safeBugUrl chỉ bật link cùng origin; regex che thêm refresh_token|api_key|apikey|jwt|otp; docblock BasicSubsystem; 2 Important Task 9 + đọc __toBlobCalls sau khi chụp xong.
- Final fix wave: dispatched (sonnet), base trees api 8ec1236 · client 90f3f5a
- USER 14/11: "Button bị ẩn dưới các popup như tạo/sửa task" + "Có hiện" (tab hiện cả khi ngăn Chat/Agent mở) ⇒ đổi Review Focus 4: tab NỔI TRÊN mọi popup + ngăn chat; chỉ ẩn khi popup báo lỗi đang mở / lúc chụp; ảnh chụp gồm cả popup đang mở. Giao sau khi final fix wave xong (tránh đè file). Cập nhật plan/design + e2e B6.
- Final fix wave: DONE — trees api c1b6471e76cdd989c65a4bde86bed995280fe456 · client 52a301a616d171bc784bc17b27fbd979c8b48928; PHPUnit 21 OK; e2e bug-report 7 passed ×2, chat 3 bộ 19 passed. Lint 7.4 + 8.4 (máy không có 8.1).
- Final re-review: 10/10 ADDRESSED, 0 breakage mới.
- Tab-on-top (user 14/11): DONE — client tree 0efb9705c784ac36b25151b1078dd7f04f5e0469; tái hiện trước (tab 1030 bị che bởi panel NV 1034/1035, modal 1040; ẩn với ngăn chat); sau: tab 9990, popup báo lỗi 9995; sửa thêm html2canvas không đọc color(srgb) từ color-mix (V2BaseSegmented) ⇒ đổi sang rgba trên bản sao; e2e bug-report 7 passed, chat-drawer+topbar 8 passed.
- Tab-on-top review: spec PASS có thiếu, quality Needs fixes (4 Important).
- Ruling: Important #1 (Esc của TaskPanel mở trên modal đóng panel thay vì popup báo lỗi) cần sửa TaskPanel.vue (dùng chung, ngoài phạm vi) ⇒ HỎI USER, không sửa — sai thì Esc đóng nhầm panel trong ca hiếm (panel mở từ trong popup).
- Tab-on-top: fix round 1 dispatched (resume): đánh dấu popup con sớm + gỡ attr khi hidden · ngân sách thời gian normalizeModernColors + try/catch · e2e panel nhiệm vụ + bỏ sleep.
- minor (deferred): select2/datepicker 9999 có thể nổi trên popup báo lỗi khi đang mở danh sách lúc bấm tab · tab 22px che mép phải panel/ngăn chat (cố hữu yêu cầu) · màu alpha thấp đổi lệch.
- USER 14/11 chọn 1: sửa 1 dòng TaskPanel.vue nhường Esc khi popup báo lỗi mở ⇒ gửi kèm fix round 1 tab-on-top.
- Tab-on-top fix round 1: DONE — client tree bdb89f87f6ba2c07b54c012bb8cd19cf05f0799e; TaskPanel 1 dòng nhường Esc (tái hiện trước/sau); popup con nâng lớp ngay khi chèn (23ms); ngân sách 1,5s đổi màu; e2e bug-report 8 passed, chat-drawer+topbar 8 passed.
- Ruling: chụp ≤5s không giữ được với DOM cực lớn (150k phần tử ⇒ 34s, do html2canvas clone/đọc, không phải bước đổi màu) — chấp nhận, báo user — sai thì màn rất nặng phải đợi lâu mới mở popup.
- Phát hiện mới (chưa sửa): popup "Cài nhóm tiếp nhận" mở/đóng không đổi vẫn hỏi "chưa lưu" khi công ty đã có nhóm (nghi mốc so sánh chụp trước khi select nạp xong) — báo user.
- 14/11 tối: USER 'làm' đợt bổ sung: API liệt kê nhóm công ty cho popup cài đặt + env.CLIENT_BUILD + e2e B7. Base api c1b6471e76cdd989c65a4bde86bed995280fe456 client bdb89f87f6ba2c07b54c012bb8cd19cf05f0799e
- Đợt bổ sung: DONE + review Approved (API nhóm công ty, CLIENT_BUILD, e2e B7). 'Chưa lưu' không tái hiện.
- 14/11: đã gỡ role tạm TMP_GD11_BaoLoi (NV 13 còn 4 role gốc); dòng permissions giữ.
