# Phase 27 — Soạn mẫu in hợp đồng theo trang A4 (như Word)

> Trạng thái: thiết kế (07/11/2026), đã qua đọc soát + user chốt 4 câu tồn; CHƯA code. Code cần user cho phép riêng ("làm" + phạm vi).
> Nguồn: brainstorm 07/11 với user + khảo sát code + khảo sát web (agent) + bản thử trong trình duyệt trên HĐ 3443.
> Mockup chọn bố cục: `.superpowers/brainstorm/6832-1794061175/content/soan-theo-trang.html` (repo hrm-claude-config, thư mục `hrm/`) — user chọn **A**.
> Ký hiệu: **[User]** = user chốt · **[Claude]** = Claude tự chốt, user kiểm khi đọc.

## 1. Vì sao làm

Người lập soạn lời văn hợp đồng ở tab Mẫu in (form Sửa HĐ) nhưng **không thấy nội dung rơi vào trang nào, ngắt ở đâu**,
nên không biết bản in có hợp lý không. Vì vậy mọi người vẫn soạn trên Word rồi mới chép vào hệ thống. [User]

Hai chỗ đau lớn nhất, đều liên quan bảng: [User]
1. Dòng bảng hàng hoá bị cắt qua 2 trang.
2. Trang cuối chỉ còn vài dòng, không biết thêm / bớt nội dung thế nào cho gọn.

Thành công = người lập soạn ngay trên hệ thống mà thấy đúng các trang của bản in, tự dàn trang, không phải quay sang Word.

## 2. Mục tiêu / không làm / tuyệt đối không

**Mục tiêu giai đoạn 1**
- Tab **Mẫu in → "Mẫu in hợp đồng"** của form Sửa HĐ hiện nội dung thành **các tờ A4 xếp dọc như Word** (bố cục A: chỉ có
  các tờ + thanh công cụ trên đầu + "Trang x/y" + zoom; không có khung "Dàn trang" / cảnh báo). [User]
- Trang soạn **thay hẳn** trình soạn thảo khối liền hiện tại ở tab con này. [User]
- Chỗ ngắt trang trên trang soạn **trùng khớp** với bản in (popup In ở Chi tiết) và tab Bản in ở màn Duyệt. [User xác nhận suy luận]
- Các biến hiện bằng **dữ liệu thật của HĐ**, kể cả bảng hàng hoá, để trang hiện đúng như bản in. [User]
- Dàn trang bằng: sửa chữ, **chèn ngắt trang tay**, **cỡ chữ**, **giãn dòng**, kẻ / sửa **bảng trong lời văn**. [User: "đủ mọi cách"]
- **Nên có** (làm được thì làm, không chặn giai đoạn 1): kéo **độ rộng cột bảng hàng hoá**, lưu riêng cho HĐ, in đúng như vậy. [User]

**Không làm ở giai đoạn 1** [User]
- Màn quản lý mẫu gốc (danh mục Mẫu in loại "Hợp đồng bán hàng"): tính sau khi giai đoạn 1 ổn.
- Tab con "Mẫu in phụ lục hàng hoá": giữ trình soạn thảo cũ.

**Tuyệt đối không** [User]
- Bảng hàng hoá (và mọi vùng lấy từ biến) **không sửa được trên trang soạn**. Nội dung luôn trùng tab Chi tiết hợp đồng.
  Chỉ để xem và căn trang. Đây là luật tuyệt đối.
- Trang soạn ngắt khác bản in. Lệch là mọi người quay về Word.

## 3. Hiện trạng (đọc code 07/11)

- Tab Mẫu in (`pages/assign/contracts/_id/edit.vue` ~dòng 565–630): chọn mẫu (`print_template_id`) → chép lời văn vào
  `hrm_contracts.template`; mặc định chỉ xem (`.print-tpl-view` v-html); bấm **"Sửa mẫu in"** → bật `need_legal_approval`
  + mở `CompactReviewEditor` (CKEditor **4.22.1**, `plugins/ckeditor-print.js`, `static/ckeditor`, `ENTER_DIV`). Có
  "Xem thay đổi" (`template-diff`, so `template_original`) và "Khôi phục mẫu gốc".
- Lời văn lưu dạng HTML có biến `{{TEN_BIEN}}`. Biến được thay lúc in ở API (`ContractPrintService::render`, `preg_replace_callback`
  `{{...}}`). Bảng hàng hoá = biến `{{CHI_TIET_HOP_DONG_HANG_HOA_THIET_BI}}`, dựng từ dòng HĐ (ô tên = tên ≤255 ký tự + Model
  + Thương hiệu + Xuất xứ).
- Bản in chia tờ (Phase 26 GĐ 3): `utils/print/pagedContract.js` (`paginateContract`, Paged.js 0.4.3 ở `static/pagedjs`),
  hiển thị bằng `components/print/ContractPagedView.vue`. Quy tắc: A4 dọc, lề 12mm/10mm, "Trang x/y", `tr{break-inside:avoid}`,
  dòng bảng > 800px tách nhiều phần (`splitTallRows`), lặp thead, giữ tiêu đề "ĐIỀU n" với đoạn sau, khối ký trọn 1 tờ,
  ngắt tay bằng class `.pb`.
- Ý kiến Pháp chế (Phase 26 GĐ 4) ghim theo **chữ** trên bản in (`legalNoteAnchor.js`), không theo toạ độ.
- CKEditor 4 bản mã nguồn mở đã ngừng bảo trì (4.22.1 là bản cuối; LTS thương mại có phí).

## 4. Khảo sát lựa chọn (07/11)

Không có trình soạn thảo nào trên thị trường ngắt trang đúng như Paged.js: CKEditor 5 Pagination (trả phí, chỉ vẽ lớp phủ,
tài liệu tự cảnh báo lệch, không hợp webpack 4), TinyMCE (chỉ chèn ngắt tay), Tiptap Pages (thương mại), tiptap-pagination-plus /
vue-document-editor (thuật toán riêng, thử nghiệm), Syncfusion / ONLYOFFICE / Collabora (mô hình docx, không phải HTML).
⇒ **Cách duy nhất khớp 100% bản in là dùng chính `paginateContract` để tính chỗ ngắt cho trang soạn.**

Ba hướng đã đưa user: (1) giữ CKEditor 4, chia tờ bằng Paged.js trên bản sao ẩn, hiện vùng soạn thành tờ rời; (2) như 1
nhưng đổi sang Tiptap; (3) tự làm editor gõ thẳng trong output Paged.js. **User chọn hướng 1.** [User]

### Bản thử (07/11, trên HĐ 3443, trong trình duyệt, không ghi gì)
- Gắn CKEditor 4 **inline** vào khối `.contract-paged .pagedjs_page_content` rộng 190mm, dùng **chính CSS nội dung của bản in**
  (`contentCss()`), gọi `paginate` của `ContractPagedView` trên `innerHTML` vùng soạn (mỗi phần tử gắn tạm `data-ed`).
- Chia lại 5 tờ: **107–129ms**.
- Độ khớp: trang 1 mọi khối trùng vị trí từng pixel, **trừ dòng tiêu đề bảng hàng hoá** (vùng soạn 32px, bản in 20px — chữ xuống
  2 dòng) ⇒ lệch 13px. Một quy tắc CSS khác nhau, phải lần ra và sửa.
- Trang 3 và 4 bắt đầu **giữa một đoạn văn** (Paged.js cắt đoạn). Không chèn được khoảng trống giữa đoạn đang gõ ⇒ dẫn tới quyết định ở mục 5.2.
- Tài liệu dài (bảng hàng hoá nhân lên, chia lại toàn bộ):

| Trang | Dòng hàng | Giây |
|---|---|---|
| 5 | 9 | 0,1 |
| 20 | 234 | 0,8 |
| 35 | 459 | 1,5 |
| 95 | 1.359 | 4,1 |
| 185 | 2.709 | 9,7 |

## 5. Thiết kế

### 5.1 Cách hiển thị tờ
- Vùng soạn là **một** CKEditor 4 inline (không iframe) đặt trong khung có cùng gốc CSS với bản in
  (`.contract-paged .pagedjs_page_content`, rộng 190mm), nạp đúng `contentCss()`. [Claude]
- Sau khi người dùng ngừng gõ ~300ms, chạy `paginateContract` trên bản sao nội dung (ẩn) → biết **khối mở đầu mỗi trang**.
- Trên vùng soạn, trước khối mở đầu mỗi trang chèn **khoảng trống hiển thị** (lề dưới tờ trước + khe giữa 2 tờ + lề trên tờ sau),
  vẽ nền trắng từng tờ, bóng đổ, "Trang x/y" ở chân tờ — trông như các tờ rời. Khoảng trống này **chỉ để hiển thị**, gỡ sạch
  trước khi lưu và trước khi chia tờ. [Claude: cách gắn — thuộc tính / class tạm trên khối + CSS, hay lớp phủ — để builder chọn, miễn không lọt vào dữ liệu lưu]
- Định danh khối giữa vùng soạn và bản sao: thuộc tính tạm (vd `data-ed`), gỡ khi lưu. [Claude]
- Dòng bảng mở đầu trang: khoảng trống phải hiện được trên `tr` (không có margin) — builder chọn cách (vd padding tạm trên ô, hoặc lớp phủ). [Claude]
- Tờ có thead lặp ở bản in: trên trang soạn hiện **bản sao chỉ xem** của thead ở đầu tờ sau (không soạn được), cho giống bản in. [Claude]
- Zoom − % + như tab Bản in; "Trang x/y" theo vị trí cuộn. [User: bố cục A]

### 5.2 Đoạn văn không cắt đôi (đổi quy tắc in) [User chọn A]
- Bản in đổi: **đoạn văn không bị cắt qua 2 trang**; chạm cuối trang thì sang trọn trang sau (như dòng bảng).
- **"Đoạn" = mỗi cụm dòng tách bằng xuống dòng mềm `<br>`**, kể cả khi nhiều cụm nằm chung một khối `div`/`p`. [User chọn, 07/11]
  Lý do: mẫu chép từ ERP dồn cả Điều vào một khối (HĐ 734: 46 khối, 71 `<br>`, 7 khối ≥ 3 `<br>`; "ĐIỀU 8" một khối 3.770 ký tự /
  24 `<br>`, mục 5.1 3.866 ký tự). Coi cả khối là đoạn thì trắng gần nửa tờ. Mục tiêu: trắng dư cuối trang ≈ 1 cụm dòng (1–3 dòng).
- Bản in và trang soạn phải **cùng** tách khối theo `<br>` lúc chia tờ (bọc tạm, không đổi dữ liệu lưu). Builder chọn cách bọc.
- Ngoại lệ: một cụm dòng **cao hơn nửa trang** vẫn được cắt; trên trang soạn chỗ đó hiện **vạch ngắt** cắt ngang (không tách tờ). [Claude: ngưỡng nửa trang]
- Quy tắc này nằm trong `pagedContract.js` nên **áp cho mọi nơi in HĐ** (tab Bản in, popup In ở Chi tiết, ý kiến Pháp chế) —
  số trang của HĐ đang có có thể đổi. User đã chấp nhận đánh đổi: cuối một số trang dư vài dòng trắng.

### 5.3 Biến và vùng khoá [User: luật tuyệt đối]
- Trên trang soạn, mỗi biến `{{X}}` hiện thành **khối khoá** (CKEditor widget hoặc `contenteditable=false`) chứa giá trị thật;
  bảng hàng hoá là khối khoá lớn. Không gõ, xoá chữ bên trong, dán đè được. Xoá **cả khối biến** thì có được không: [Claude] **không** — giữ nguyên hành vi hiện tại (biến là một phần mẫu; muốn bỏ thì khôi phục / đổi mẫu). Builder kiểm lại với mẫu thật xem có biến tuỳ chọn không.
- Lưu: khối khoá ghi lại đúng `{{X}}` như cũ ⇒ dữ liệu lưu cùng định dạng hiện tại, API in không đổi.
- Giá trị biến lấy từ API: endpoint mới trả **HTML đã thay biến cho một lời văn bất kỳ** của HĐ (hoặc bảng giá trị từng biến),
  dùng cùng `ContractPrintService` để không lệch bản in. [Claude]
- Dữ liệu dùng để thay biến = **dữ liệu đang nhập trên form** (kể cả chưa lưu ở tab Chi tiết), không phải bản đã lưu — để bảng
  hàng hoá trên trang soạn khớp với những gì người lập vừa sửa. [Claude; builder đánh giá chi phí, nếu quá nặng thì dùng bản đã lưu + nhắc "Lưu nháp để cập nhật bảng hàng hoá"]

### 5.4 Công cụ dàn trang
- Thanh công cụ CKEditor trên đầu, giữ bộ nút đang có (`remove-buttons=""` = full) + bảo đảm có: cỡ chữ, giãn dòng (plugin
  `lineheight` đã có trong `static/ckeditor/plugins`), bảng + `tabletools`/`tableselection`, **ngắt trang tay**.
- Ngắt trang tay: lưu bằng phần tử / class mà `pagedContract.js` hiểu là `break-before: page` (hiện có `.pb`). Plugin `pagebreak`
  của CKEditor sinh `<div style="page-break-after: always">` — builder chọn: dùng plugin rồi để `pagedContract` đổi sang `.pb`,
  hoặc nút riêng. Bản in và trang soạn phải ngắt giống nhau. [Claude]
- Kéo độ rộng cột bảng hàng hoá (nên có): cần chỗ lưu độ rộng theo HĐ (cột mới / JSON) và `ContractPrintService` dựng bảng theo đó
  ⇒ **có migration** — hỏi user riêng khi tới bước này. [User: nên có]

### 5.5 Hiệu năng [User chọn A, 07/11]
- Độ dài thật (27.849 HĐ hãng ERP, `db_gop_6_11`): số dòng hàng p50 = 1, p90 = 7, p99 = 61, lớn nhất 413 (≈ 32 trang);
  chỉ 20 HĐ ≥ 200 dòng, 0 HĐ ≥ 500 dòng. Chia lại toàn bộ ≈ 50ms/trang ⇒ HĐ lớn nhất ≈ 1,5 giây, 99% HĐ < 0,4 giây.
- **Giai đoạn 1: chia lại toàn bộ** khi ngừng gõ (~300ms), chạy nền, **không chặn gõ**; trong lúc chờ giữ chỗ ngắt cũ + dấu
  "đang cập nhật". HĐ lớn cập nhật chậm hơn (tới ~1,5 giây) là **đạt**.
- "Chia lại từ trang đang sửa" + "dừng sớm" để giai đoạn sau, **chỉ làm nếu đo thực tế thấy chậm**. Không chặn phát hành.
- Mục tiêu đo: [Claude] HĐ ≤ 10 trang cập nhật ≤ 300ms sau khi ngừng gõ; HĐ 32 trang ≤ 2 giây; gõ không giật ở mọi độ dài.

### 5.6 Dàn trang không cần Pháp chế [User chọn B, 07/11]
- **Sửa lời văn** (thêm / bớt / đổi chữ) ⇒ bật `need_legal_approval` như hiện nay.
- **Chỉ dàn trang** — ngắt trang tay, cỡ chữ, giãn dòng, độ rộng cột bảng hàng hoá — **không** bật cờ Pháp chế. "Xem thay đổi"
  chỉ hiện thay đổi **lời văn**, không hiện thay đổi định dạng / ngắt trang.
- Người lập dùng được công cụ dàn trang **mà không cần bấm "Sửa mẫu in"**; "Sửa mẫu in" chỉ mở khoá sửa chữ (kèm xác nhận +
  cờ Pháp chế như cũ). [Claude]
- Cách lưu: lúc chốt user nghe phương án "lưu riêng lớp dàn trang, lúc in áp vào" (có migration). [Claude đề xuất builder cân nhắc]
  cách nhẹ hơn cho cùng kết quả: giữ cỡ chữ / giãn dòng / ngắt trang ngay trong `template`, còn cờ Pháp chế và "Xem thay đổi"
  **so theo chữ** (bỏ qua style, thẻ ngắt) với `template_original`. Độ rộng cột bảng hàng hoá vẫn cần chỗ lưu riêng vì bảng sinh từ biến.
  **User chốt 07/11 (Task 0): cách (a)** — định dạng nằm trong `template`, cờ Pháp chế so theo chữ, không migration.

- HĐ cũ chưa có bản chụp (`template_original` NULL), cùng mẫu: lần lưu đầu lấy chính `template` hiện tại của HĐ làm bản chụp — không thay chữ, không bật cờ. **User chốt 08/11 (A).** HĐ mới / đổi mẫu vẫn chụp từ danh mục.
- Cỡ chữ: **user chốt 08/11 (A)** — chỉ qua class `hd-fs-N` (9–16pt) trên span; CSS in HĐ tôn trọng `hd-fs-N`, cỡ chữ inline cũ vẫn ép 13px (reportPrintStyle). BE whitelist `hd-fs-9..16`.

### 5.7 Ý kiến Pháp chế trên trang soạn [User chọn B, 07/11]
- Trang soạn **hiện ý kiến Pháp chế đã ghim** cạnh đoạn chữ, giống màn Duyệt (tô đoạn + số ghim + cột ý kiến), dùng lại
  `legalNoteAnchor.findAnchor` và giao diện của `LegalNotesPanel`.
- Ghim lại sau mỗi lần chia tờ và khi gõ làm đổi chữ; đoạn đã sửa khác chữ gốc hiện "Đoạn đã thay đổi" kèm chữ gốc (như màn Duyệt).
- Thao tác "Đã sửa" / phản hồi: [Claude] giai đoạn 1 cho làm ngay trên trang soạn nếu dùng lại được panel; nếu vướng thì chỉ xem,
  thao tác vẫn ở màn Duyệt — builder báo lại khi lập plan.
- Ghim / tô **không lọt vào dữ liệu lưu**.

### 5.8 Giữ tương thích
- Lời văn đang lưu của mọi HĐ mở và sửa được, lưu ra cùng định dạng (HTML + `{{biến}}`). [User xác nhận suy luận]
- "Khôi phục mẫu gốc" giữ nguyên. Chế độ chưa bấm "Sửa mẫu in" vẫn hiện theo tờ, cho dàn trang, khoá sửa chữ (5.6). [Claude]
- Ý kiến Pháp chế ghim theo chữ vẫn tìm đúng chỗ (dữ liệu lưu không có thuộc tính tạm, khoảng trống hiển thị). [User xác nhận suy luận]
- Bản in / tab Bản in: chỉ đổi quy tắc ở mục 5.2.

## 6. Kiểm chứng (bắt buộc)
- Playwright đo trên HĐ thật (734, 3443) và HĐ dài dựng trong bộ nhớ: **mỗi trang trên trang soạn chứa đúng các khối như tờ tương
  ứng của bản in** (so định danh khối đầu / cuối từng trang), chênh vị trí ≤ 1px; sửa dòng tiêu đề bảng lệch 13px của bản thử.
- Lưu → `template` trong DB không chứa thuộc tính / khoảng trống tạm, biến vẫn là `{{X}}`; in ra giống trước khi mở trang soạn
  (trừ đổi quy tắc 5.2).
- Vùng khoá: gõ, xoá, dán, kéo thả, Ctrl+A rồi gõ đều không đổi được nội dung bảng hàng hoá / biến.
- Thời gian theo mục 5.5. Chrome là chính; kiểm thêm Safari, Firefox như Phase 26 GĐ 3.
- E2E cập nhật ca tab Mẫu in, chạy cả bộ `contracts-approval-flow` (đổi quy tắc 5.2 ảnh hưởng F27–F36).

## 7. Để builder quyết
- Cách gắn khoảng trống hiển thị / thead bản sao / vạch ngắt giữa đoạn (5.1, 5.2).
- Widget CKEditor hay `contenteditable=false` cho vùng khoá (5.3).
- Cách bọc tạm theo `<br>` (5.2), cách lưu dàn trang (5.6 — báo user trước khi code).
- Chia task, thứ tự (gợi ý: vùng soạn theo tờ + sửa lệch CSS → quy tắc 5.2 (tách `<br>`) ở bản in + trang soạn → vùng khoá + API biến →
  dàn trang không cần Pháp chế (5.6) → ý kiến Pháp chế (5.7) → độ rộng cột).

## 8. Rủi ro
| Rủi ro | Ảnh hưởng | Giảm thiểu |
|---|---|---|
| HĐ HRM dài hơn dữ liệu HĐ hãng ERP đã đo | Cập nhật chỗ ngắt chậm | Giai đoạn 1 chấp nhận chậm + "đang cập nhật"; đo lại sau khi có HĐ HRM thật, cần thì làm chia từng phần |
| Tách đoạn theo `<br>` ở bản in làm đổi số trang HĐ đang có | Bản in khác lần trước | Chấp nhận [User]; e2e F27–F36 cập nhật số đo |
| CSS vùng soạn lệch bản in | Mất lòng tin, quay về Word | Một nguồn CSS duy nhất (`contentCss()`), test so vị trí từng khối |
| Đổi quy tắc 5.2 làm đổi số trang HĐ đang có | Bản in khác lần in trước | Chấp nhận [User]; ghi rõ khi release |
| CKEditor 4.22.1 hết vá bảo mật | Bảo mật | Ghi nhận; thay editor là việc riêng |

## 9. Bước khi deploy
- Mẫu in danh mục **62, 85, 86** (mẫu Word lồng khối trong chữ đậm): mở ở màn danh mục Mẫu in (loại "Hợp đồng bán hàng") rồi bấm Lưu một lần để mẫu thành HTML chuẩn — nếu không, HĐ dùng các mẫu này chỉ dàn trang vẫn bật cờ Pháp chế (HTML5 trình duyệt vs libxml ở API dựng cây khác nhau). **User chốt 08/11 (hướng a).** HĐ đã chép lời văn từ các mẫu này trước đó không tự đổi theo.
- **Task 7 — migration** `Modules/Assign/Database/Migrations/2026_11_08_000001_add_print_col_widths_to_hrm_contracts_table.php` (thêm cột `hrm_contracts.print_col_widths` JSON nullable, không đụng dữ liệu): chạy lẻ bằng `--path` trên prod **TRƯỚC khi deploy code hrm-api** (luồng Lập HĐ luôn ghi cột này ⇒ code BE lên trước migration là mọi lần Lập HĐ lỗi 500 "Unknown column", kể cả với FE cũ).
