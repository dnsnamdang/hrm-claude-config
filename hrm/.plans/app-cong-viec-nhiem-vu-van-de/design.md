# Design — Nhiệm vụ / Vấn đề trên app mobile (phân hệ Công việc)

**Sản phẩm:** bộ thiết kế giao diện cho `TPE_APP` (Flutter) — phân hệ Công việc, 2 chức năng Nhiệm vụ (task) và Vấn đề (issue).
**Không phải task code.** Đầu ra là artboard trong `.pen` + danh sách việc cho dev. Không sửa `hrm-api` / `hrm-client` / `TPE_APP`.

| | |
|---|---|
| File thiết kế | `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen` (file chung các phân hệ app; khu Công việc đã có drawer 00e, bộ lọc BL1–BL4) |
| Nguồn web | `gop_db` — hrm-client `5370d6620`, hrm-api `3a14fac44` (29/10/2026) |
| Nguồn app | TPE_APP `develop` `8f6adfa` (29/10/2026) |
| Khảo sát | `khao-sat-web-nhiem-vu.md` · `khao-sat-web-van-de.md` · `khao-sat-app-task.md` (cùng thư mục, có `file:dòng`) |

## Mục tiêu

Đưa **toàn bộ chức năng web hiện có** của Nhiệm vụ và Vấn đề lên điện thoại 393px — bám luật nghiệp vụ web, chỉ đổi cách trình bày. Hiện app chỉ XEM được Nhiệm vụ (danh sách, chi tiết, bình luận, báo cáo tiến độ ngày) và CHƯA có Vấn đề.

Không phải mục tiêu: sửa bug BE/web (ghi ở mục "Việc cho dev"); thêm tính năng web không có.
Phản mục tiêu: vẽ theo bug của web (vd thiếu ô lý do từ chối) — thiết kế theo **luật đúng**, chỗ lệch ghi cho dev.

## Quyết định user đã chốt (29/10/2026)

| # | Chốt |
|---|---|
| U1 | "Task" → **"Nhiệm vụ"** ở mọi nơi trên app (tab, tiêu đề, drawer). |
| U2 | Đổi trạng thái kiểu **phương án 1**: pill trạng thái ở đầu màn chi tiết → bottom sheet liệt kê đúng `allowed_next_statuses` BE trả (chuyển không tuần tự vẫn được), chọn → xác nhận → lưu ngay; bước cần dữ liệu (lý do từ chối, kết quả…) thì sheet mở thêm ô nhập. **Màn Sửa vẫn giữ ô Trạng thái + Lưu** như web. (Tham khảo Jira transition screen / Linear / ClickUp.) |
| U3 | Nhiệm vụ và Vấn đề **tách riêng**. Thanh dưới phân hệ Công việc: **Việc của tôi · Nhiệm vụ · [+ Tạo mới] · Vấn đề · Phê duyệt**. Tab Phiếu chuyển vào drawer (drawer đã có section "Phiếu"). Nút [+] thêm 2 lựa chọn Nhiệm vụ, Vấn đề. **⚠ 05/11 thay bằng U26 (phân hệ Công việc): Việc của tôi · Không gian · [+] · Nhiệm vụ · Phê duyệt — Vấn đề vào drawer** (`.plans/gop-db/phan-he-cong-viec/plan.md` M8). |
| U4 | Khối **Lặp lại** của Nhiệm vụ KHÔNG đưa lên app (BE chưa có job sinh lặp). Chi tiết chỉ hiện dòng đọc "Lặp lại: …" nếu có cấu hình. |
| U5 | Khối **Liên kết nhiệm vụ** (FS/SS/FF/SF/RL) KHÔNG đưa lên app — cả xem lẫn sửa. |
| U6 | **% tiến độ = luỹ kế** ("Đã hoàn thành đến hôm nay: __%"), gợi ý sẵn số lần trước, không cho nhập thấp hơn. Áp cho cả Nhập kết quả lẫn Báo cáo tiến độ hằng ngày. |
| U7 | Chọn **Hoàn thành / Hoàn thành – Chờ duyệt** (Nhiệm vụ) hoặc **Đã xử lý xong / Hoàn thành** (Vấn đề) từ pill → **chuyển sang màn Nhập kết quả** (NV-06/07) với trạng thái chọn sẵn, % điền sẵn 100; người dùng điền giờ thực tế · kết quả · tệp rồi Lưu. Pill chỉ lưu thẳng các trạng thái không cần dữ liệu. Nút Duyệt hoàn thành / Duyệt triển khai của người duyệt: xác nhận rồi lưu ngay. |
| U8 | Form Nhiệm vụ trên app CÓ **chế độ Đơn giản** để tạo nhanh việc đơn giản (user 29/10). Gạt **Đơn giản \| Nâng cao** ở đầu form, tạo mới mặc định Đơn giản; Sửa mở theo `mode` đã lưu. Đơn giản = trường cơ bản (khối ① Thông tin + ② Gắn với); Nâng cao thêm ③ Checklist · ④ Nhiệm vụ con · ⑤ Tệp · ⑥ Thiết lập. Lưu `mode` 1/2 đúng như web. Xem/chi tiết luôn hiện đủ (web ép `mode=2` khi xem). |
| U9 | Vấn đề KHÔNG có chế độ đơn giản: giữ đủ 7 khối gập như web; lúc tạo chỉ mở các khối có trường bắt buộc, còn lại gập. |
| U10 | **Không hiện mã nhiệm vụ** ở thẻ danh sách, đầu màn chi tiết, sheet trạng thái, màn Nhập kết quả — chỉ cần TÊN (user 29/10). Ô tìm vẫn tìm được theo mã. |
| U11 | **Vào nhanh Bình luận từ mỗi nhiệm vụ** (user 29/10): thẻ danh sách có nút 💬 + số bình luận (0 thì xám) mở thẳng màn Bình luận, không qua chi tiết; màn chi tiết đặt 💬 có số ở header (như app cũ) và BỎ dòng 'Bình luận' trong thân (1 hành động 1 lối vào — skill app-ui-convention 1c-2). ⋮ chỉ còn Sửa · Xoá; Lịch sử ở dòng cuối thân màn. Cần BE trả `comments_count` ở danh sách. |
| U12 | **Nút Huỷ / Đóng luôn CUỐI cùng (bên phải)** ở mọi nơi — hộp thoại, bottom sheet, footer form (user 29/10, theo skill app-ui-convention, đồng bộ web). Nút hành động đứng trước (trái). Nút phụ KHÔNG phải huỷ (Đặt lại, Lưu & tạo tiếp, Báo cáo hôm nay, Từ chối) giữ bên trái. Mọi nút có icon (TPE_APP/CLAUDE.md). |
| U13 | **Header mọi màn có hình nền như drawer CV-00a** (user 30/10): gradient #23A06F → #136B4C → #083A2A + 2 vệt sáng radial #5BE0A6 + 2 vòng tròn mảnh trắng mờ + icon chìm (Nhiệm vụ task_alt · Vấn đề report · Phê duyệt verified, trắng 5%). Đã áp 30 header. |

## Đợt 2 — đồng bộ logic mockup web Phân hệ Công việc (user chốt 05/11/2026)

Nguồn: spec `docs/superpowers/specs/gop-db/2026-11-02-phan-he-cong-viec-design.md` §5.1 + `gop-db/phan-he-cong-viec/gd0-mockup/thuyet-minh.html` mục 8. Làm **Nhiệm vụ trước**, duyệt xong mới áp khuôn cho Vấn đề. Vẽ hàng mới "Nhiệm vụ v2" trong `meeting-mobile.pen`, giữ bộ NV-xx cũ để so tới khi duyệt.

| # | Chốt | Thay quyết định cũ |
|---|---|---|
| U27 | Form Nhiệm vụ **bỏ công tắc Đơn giản / Nâng cao** như web: trường cơ bản + hàng "+ Checklist · + Nhiệm vụ con · + Tệp" (mục có dữ liệu thì hiện) + Thiết lập thu gọn "n/m đang bật". | U8 |
| U28 | **(sửa 05/11 theo góp ý)** Chi tiết = **3 tab** Chi tiết · Kết quả & tiến độ (có Nhật ký tiến độ) · Lịch sử. Bình luận KHÔNG là tab: nút 💬 + số ở header mở màn Bình luận riêng (NV2-12, giữ U11); 💬 trên dòng danh sách cũng mở NV2-12. | — (giữ U11) |
| U29 | **Chạm trường → sheet sửa 1 trường**, lưu ngay + ghi lịch sử; chỉ người giao (`can_edit`); người khác thấy "Chỉ người giao sửa được thông tin". "Sửa toàn bộ" trong ⋯. | U2 (màn Sửa cả form thành phụ) |
| U30 | Giữ U4/U5 trên app: Thiết lập chỉ có Yêu cầu báo cáo tiến độ + Trọng số KPI; Lặp lại chỉ là dòng đọc khi có; Liên kết nhiệm vụ không hiện. | — |
| U31 | Form tạo **bỏ ô Trạng thái khởi tạo**; footer [Lưu nháp] [Giao việc ▾] ("Giao & tạo tiếp" trong menu ▾). Giao việc → Chờ phê duyệt triển khai / Chờ bắt đầu theo luồng hiện có (L3); kiểm đủ hạn, số giờ, người làm. | NV-10 chip trạng thái, KG-04 |
| U31b | **(sửa 05/11)** Kiểm code: KHÔNG có luật tự quyết "cần duyệt triển khai" — form web hiện tại người giao tự chọn trạng thái khởi tạo (`CreateTaskModal.vue:248`). Lý do U31 ban đầu ("tự vào theo luồng hiện có") là sai. Chốt lại: giữ [Lưu nháp] [Giao việc ▾] + **công tắc "Cần duyệt triển khai"** trong form (bật → Chờ phê duyệt triển khai, tắt mặc định → Chờ bắt đầu) + "Bắt đầu ngay" khi tự giao cho mình (→ Đang thực hiện). BE chỉ nhận 4 giá trị Nháp/2/3/4 (vá lỗ hổng #3). | U31 |
| U32 | (góp ý 05/11) Mức độ ưu tiên ở form Tạo/Sửa: chip tô theo màu BE `Task::PRIORITIES` — Bình thường #94A3B8 · Cao #F97316 · Khẩn cấp #DC2626 (chọn: nền đậm + viền + ✓; chưa chọn: nền nhạt cùng màu). | NV-10 chip xanh |
| U33 | (góp ý 05/11) Hạn: chọn ngày → giờ tự điền **17:30** (hết ngày làm việc), vẫn sửa được. Áp cho form, sheet đổi hạn, đề nghị gia hạn. | — |
| U34 | (góp ý 05/11) Mục **Thiết lập** vẽ rõ (NV2-13): Người duyệt kết quả · Người theo dõi · Thẻ · Yêu cầu báo cáo tiến độ (chu kỳ Ngày/Tuần/Tháng, thứ / ngày trong tháng, giờ nhắc, Xem trước), mỗi mục 1 dòng giải thích tác dụng; tóm tắt "n mục đang dùng". **Bỏ "Trọng số KPI"** — form thật (`CreateTaskModal.vue` gop_db) không có ô này; mockup web ghi nhầm, cần sửa mockup web/spec cho khớp. | U30 (bỏ KPI) |
| — | Theo web, không cần hỏi: danh sách **gom nhóm** (Trạng thái mặc định / Người làm / Hạn / Dự án) + Sắp xếp trong nhóm, nhóm Đã xong thu sẵn, ⓘ giải thích nhóm; nút hành động chính theo vai trò, không có quyền thì ghi lý do; **bấm hạn** → người giao đổi hạn / người làm **Đề nghị gia hạn** (L1) → người giao Đồng ý / Từ chối; quá hạn tính theo lúc nộp (L2). | NV-01 thẻ phẳng |

### Màn Nhiệm vụ v2 (dựng 05/11, `meeting-mobile.pen` hàng y 6690, x 15600–21669)
| Mã | Màn |
|---|---|
| NV2-01 | Danh sách gom theo Trạng thái (chip Tất cả · Của tôi · Quá hạn · Chờ tôi duyệt; Gom theo / Sắp xếp; nhóm vạch màu + ⓘ; nút hành động theo vai trò + 💬) |
| NV2-02 | Sheet Gom theo + Sắp xếp (lưu theo người dùng × màn, dùng chung web) |
| NV2-03 | Gom theo Hạn — Hôm nay · 7 ngày tới · Chờ duyệt · Đã xong · Quá hạn cuối; minh hoạ L2 (nộp đúng hạn / nộp trễ) |
| NV2-04 | Chi tiết tab Chi tiết — người làm (chỉ đọc + khoá, nút Đề nghị gia hạn, Thiết lập 1/2, footer Tạm dừng · Tiến độ · Báo kết quả) |
| NV2-05 | Chi tiết — người giao: trường có ›, thanh duyệt đề nghị gia hạn, hàng + Checklist · + Nhiệm vụ con |
| NV2-06 | Sheet đổi hạn (mẫu sửa 1 trường, U29) |
| NV2-07 | Sheet đề nghị gia hạn (L1) |
| NV2-08 | Tab Kết quả & tiến độ + Nhật ký tiến độ |
| NV2-09 | Người duyệt — Hoàn thành - Chờ duyệt: Từ chối · Duyệt kết quả |
| NV2-09b | Không có quyền → ghi lý do thay nút ("Chờ X duyệt kết quả") |
| NV2-10 | Tạo — 1 form, ô Không gian, + Checklist/Nhiệm vụ con/Tệp, Thiết lập 0/2, [Lưu nháp] [Giao việc ▾] |
| NV2-11 | Giao việc thiếu trường — báo đồng thời 3 ô |
| NV2-12 | Màn Bình luận riêng (mở từ 💬 header / 💬 dòng danh sách) |
| NV2-13 | Form Tạo/Sửa — mục Thiết lập mở rộng (U34) |

| — | **Bổ sung đủ chức năng (05/11, hàng NV2b y 8380–12735)** — nút theo `Task::getAllowedNextStatuses`, màu `Task::STATUS` |
| NV2-14 | Nháp — người giao: [Xoá] [Giao việc] |
| NV2-15 | Chờ phê duyệt triển khai — người duyệt triển khai: [Từ chối triển khai] [Duyệt triển khai] |
| NV2-16 | Chờ bắt đầu — người làm, có Checklist + Nhiệm vụ con: [Tạm dừng] [Bắt đầu] |
| NV2-17 | Tạm dừng — banner lý do: [Làm tiếp] |
| NV2-18 | Từ chối kết quả — banner nhận xét: [Tạm dừng] [Làm tiếp] |
| NV2-19 | Từ chối triển khai — người giao: [Giao lại] |
| NV2-20 | Hoàn thành — người giao: [Trả lại làm thêm] |
| NV2-21 | Tab Lịch sử |
| NV2-22 | Menu ⋯ (Sửa toàn bộ · Đổi hạn · Giao người khác · Theo dõi · Sao chép liên kết · Xoá chỉ Nháp) |
| NV2-23 | Sheet chọn người (dùng chung) |
| NV2-24 | Xác nhận xoá + Hoàn tác |
| NV2-25 | Sheet Tạm dừng (lý do tuỳ chọn) |
| NV2-26 | Sheet Từ chối nhận việc / Từ chối triển khai (lý do bắt buộc) |
| NV2-27 | Sheet Duyệt kết quả (nhận xét tuỳ chọn) |
| NV2-28 | Sheet Từ chối kết quả — lỗi khi trống |
| NV2-29 | Sheet Từ chối đề nghị gia hạn |
| NV2-30 | Form Báo kết quả — chặn khi checklist chưa xong |
| NV2-31 | Cập nhật tiến độ (% luỹ kế) |
| NV2-32 | Tạo — Nhiệm vụ chung (nhiều người) |
| NV2-33 | Tạo — đã mở Checklist / Nhiệm vụ con / Tệp |
| NV2-34 | Sheet nguồn tệp |
| NV2-35 | Giao việc ▾ (Giao & tạo tiếp) + thanh báo kết quả giao |
| NV2-36 | Tự giao cho mình — Bắt đầu ngay |
| NV2-37 | Sửa toàn bộ |

Cập nhật kèm: KG-04 (bỏ Đơn giản/Nâng cao + Trạng thái khởi tạo, footer Lưu nháp | Giao việc), KG-06 (tab Nhiệm vụ của không gian dùng khuôn NV2-01).
Màn giữ nguyên dùng lại: NV-04/05 sheet trạng thái, NV-06/07 Nhập kết quả, NV-14 Lịch sử, NV-15 Báo cáo tiến độ.
**Sau khi user duyệt:** xoá/đánh dấu cũ bộ NV-01…NV-12, áp khuôn cho Vấn đề (VD-xx), rồi mới cập nhật code TPE_APP (hỏi phạm vi trước khi code).

## Đợt 3 — áp khuôn Nhiệm vụ v2 sang Vấn đề (user chốt 05/11/2026)

Kiểm code `Issue.php` (STATUS_DATA, PRIORITY_DATA, getAllowedNextStatuses, canEdit = người tạo & chưa Đóng/Hoàn thành, canDelete = người tạo & Mới ghi nhận), `IssueService::store/changeStatus`, `IssueStoreRequest`, `CreateIssueModal.vue` (gop_db).

| # | Chốt | Ghi chú code |
|---|---|---|
| U36 | **Trạng thái khi tạo tự suy theo người nhận**, không có ô trạng thái: chọn Người phụ trách → Đã phân công; chỉ chọn Phòng ban / Bộ phận → Mới ghi nhận (trưởng bộ phận nhận thông báo, phân công sau). Nút **Gửi vấn đề**. | BE giữ nguyên (`IssueStoreRequest`: có người khi assigned, không người thì bắt buộc phòng ban). App gửi `status` theo người nhận. Form web hiện cho tự chọn → sửa theo ở plan GĐ2. |
| U37 | **Báo đã xử lý theo mockup GĐ0**: sheet Cách xử lý * + Nhóm nguyên nhân * + tệp chứng cứ; tab Kết quả xử lý hiện lại cho người duyệt đóng. | `changeStatus` hiện chỉ lưu status + `resolved_at`. Cần nhận thêm `resolution` + `root_cause_group` (cột có sẵn). ⚠ `resolution` là `string` 255 — cần đổi `text` nếu cho viết dài. |
| U38 | Vấn đề dùng **cùng khuôn danh sách** NV2 (thanh công cụ A + ⚙ Cách xem, gom theo Trạng thái / Người xử lý / Hạn / Dự án — spec §5.1) và **cùng khuôn chi tiết**: 3 tab Chi tiết · Kết quả xử lý · Lịch sử + 💬 header mở màn Bình luận. | Sửa lại ghi chú VD-01 "không có ⚙" (sai so với spec). |
| U39 | (05/11) **Ngày bắt đầu không bắt buộc** khi giao việc (theo cách Jira / Asana / ClickUp: Hạn là mốc chính). Form chỉ hiện Hạn + Giờ hạn; dưới đó có "+ Ngày bắt đầu" cho việc giao trước, làm sau. Để trống → lấy ngày giao việc. Bắt đầu thực tế tự ghi khi người làm bấm Bắt đầu. Áp web màn 03 + app NV2-10/11/13/32–37, KG-04. | Code: `TaskStoreRequest.php:54` đã bỏ bắt buộc `start_date` (comment); FE web vẫn gắn `*` + tự điền hôm nay (`seedDates()`). Báo cáo "Quản lý nhiệm vụ theo nhân viên" lọc theo khoảng `start_date → due_date` (`TaskManagerByEmployeesReportService.php:305-313`) ⇒ BE phải tự điền ngày giao khi trống, nếu không việc rơi khỏi báo cáo. |

### Màn Vấn đề v2 (dựng 05/11, `meeting-mobile.pen` hàng y 13000, x 15600–20803; hàng 2 y 14750)
| Mã | Màn |
|---|---|
| VD2-01 | Danh sách gom theo Trạng thái (thanh công cụ A + ⚙; nút nhanh Nhận xử lý / Báo đã xử lý / Xác nhận) |
| VD2-02 | Chi tiết — người phụ trách, Đang xử lý: [Đóng vấn đề] [Báo đã xử lý] |
| VD2-03 | Chi tiết — người báo, Mới ghi nhận (gửi phòng ban): trường có ›, [🗑] [Đóng vấn đề] [Phân công] |
| VD2-04 | Người phụ trách, Đã phân công (và Mở lại): [Đóng vấn đề] [Nhận xử lý] |
| VD2-05 | Người duyệt đóng, Đã xử lý xong — tab Kết quả xử lý: [Từ chối kết quả] [Xác nhận hoàn thành] |
| VD2-06 | Sheet Từ chối kết quả (lý do bắt buộc, lỗi khi trống) |
| VD2-07 | Từ chối — người phụ trách: banner lý do, [Đóng vấn đề] [Xử lý lại] |
| VD2-08 | Hoàn thành — người báo / người phụ trách: [Mở lại] (lý do tuỳ chọn) |
| VD2-09 | Không có quyền → ghi lý do ("Chờ X xác nhận hoàn thành") |
| VD2-10 | Tạo — gửi đích danh người phụ trách (→ Đã phân công) |
| VD2-11 | Tạo — chỉ gửi phòng ban / bộ phận (→ Mới ghi nhận) |
| VD2-12 | Gửi khi thiếu trường — báo đồng thời |
| VD2-13 | Báo đã xử lý (Cách xử lý *, Nhóm nguyên nhân *, tệp) |
| VD2-14 | Báo đã xử lý — thiếu trường |
| VD2-15 | Tạo — Thiết lập mở rộng (theo dõi, phối hợp, thẻ, SLA, nhiệm vụ liên kết, người & lúc phát hiện) |
| VD2-16 | Menu ⋯ người báo (Xoá chỉ khi Mới ghi nhận) |

Dùng lại của Nhiệm vụ: màn Bình luận NV2-12, Lịch sử NV2-21, sheet chọn người NV2-23, xác nhận xoá NV2-24, đổi hạn / đề nghị gia hạn NV2-06/07. Sửa kèm: VD-01/02 thêm ⚙ Cách xem.
**Sau khi user duyệt:** đánh dấu cũ VD-01…VD-08, rồi mới cập nhật code TPE_APP (hỏi phạm vi trước).

## Claude tự chốt (thuần UI / bám web — user xem lại khi duyệt)

- C1. Màu phân hệ Công việc `#1E8A63` (W7 meeting-mobile). Màu trạng thái / ưu tiên / tình trạng hạn lấy từ BE (`status_color`, `priority_color`, `deadline_state_*` / `due_status_color`) — không dùng bảng màu tự map của popup web.
- C2. Quyền & nút: chỉ đọc cờ BE (`can_edit`, `can_delete`, `can_import_result`, `can_approve` của Nhiệm vụ; `can_edit`, `can_delete`, `can_handle` của Vấn đề) + `allowed_next_statuses`. App không tự suy luật.
- C3. Danh sách: dùng khuôn bộ lọc BL1–BL4 (ô tìm + nút lọc, hàng chip lọc nhanh, bottom sheet lọc, chip tiêu chí đang lọc). 4 chip vai trò **có chữ** (app cũ chỉ icon). Đầu danh sách: "Tổng n · Quá hạn n" (`meta.total`, `overdue_total` của BE).
- C4. Thẻ danh sách 3 tầng: mã + pill trạng thái / tên (2 dòng) / người làm · hạn + tình trạng hạn · ưu tiên.
- C5. Chi tiết: đầu màn = mã, tên, pill trạng thái (bấm được nếu có bước chuyển), dải nút hành động chính theo cờ; thân = các khối gập (Thông tin mở sẵn, còn lại gập kèm số đếm). Bình luận + Lịch sử là dòng mở màn con. Hành động ở footer trong tầm ngón cái (memory: nút hành động mobile).
- C6. Form Tạo/Sửa dùng khuôn **khối gập** như Thông tin chung của meeting (W5): chỉ khối đang nhập mở; trường chọn = dòng nhãn trái–giá trị phải; validate báo đồng thời mọi ô, khối có lỗi tự mở. Trường bắt buộc theo **BE** (không theo dấu `*` lệch của web).
- C7. Trạng thái **Huỷ (9)** của Nhiệm vụ: không có nút Huỷ tay; **đường vào duy nhất là đóng Dự án nội bộ / Phòng tự chọn** (spec §3.11, 05/11) — việc dở tự chuyển Huỷ. App chỉ hiển thị.
- C8. Tab **Phê duyệt** thêm 3 mục: Duyệt triển khai nhiệm vụ · Duyệt kết quả nhiệm vụ · Duyệt đóng vấn đề (người duyệt khi `resolved`). Mỗi mục là danh sách lọc sẵn (dùng `GET assign/tasks` / `assign/issues` + lọc trạng thái + vai trò).
- C9. Báo cáo tiến độ hằng ngày giữ ở drawer (đổi tên thống nhất "Báo cáo tiến độ nhiệm vụ") + thêm lối "Báo cáo hôm nay" từ chi tiết nhiệm vụ đang bật báo cáo; thẻ bấm mở chi tiết.
- C10. Bình luận: sửa lại màn đang có — thêm lối "Xem nhiệm vụ / vấn đề" ở header, cho gửi chỉ tệp, @nhắc tên (BE đã hỗ trợ `@[Họ tên]`). Không đổi cấu trúc cây.
- C11. Xuất Excel / Cấu hình cột của web KHÔNG đưa lên app (chức năng bàn giấy).
- C12. Nhập Excel nhiệm vụ: web không có màn import riêng ở danh sách → không vẽ.
- C14. "Báo cáo hôm nay" ở chi tiết mở NV-15 lọc riêng nhiệm vụ đó, giữ luật NV-15 (chỉ sửa dòng hôm nay). NV-07 (nhật ký trong Nhập kết quả) giữ luật web: sửa mọi dòng ≤ hôm nay, % không thấp hơn dòng trước.
- C16. Vấn đề KHÔNG có màn 'Nhập kết quả' (web chế độ Xử lý chỉ có Trạng thái + Lý do + Tệp) → U7 với Vấn đề làm NGAY TRONG sheet Xử lý VD-04: chọn Đã xử lý xong mở khối tệp chứng cứ, Đã đóng / Từ chối mở ô lý do. Hạn xử lý + Người duyệt đóng đặt ở khối ⑤ Thông tin xử lý (form web để ở khối khác).
- C15. Mục "Duyệt triển khai nhiệm vụ" ở tab Phê duyệt chỉ hiện thẻ BE trả `can_approve = true`; KHÔNG vẽ badge đếm cho tới khi BE có API lọc đúng người duyệt triển khai (quyền + phòng ban quản lý) — ghi việc cho dev.

## Danh sách màn (đánh mã CV-NV / CV-VD)

### Khung phân hệ
- **CV-00** Thanh dưới mới + drawer Công việc cập nhật (Phiếu vào drawer, "Tasks" → "Nhiệm vụ", "Báo cáo tiến độ nhiệm vụ") + sheet [+ Tạo mới] có Nhiệm vụ, Vấn đề.

### Nhiệm vụ
| Mã | Màn | Nguồn web |
|---|---|---|
| NV-01 | Danh sách (BL1) — chip vai trò: Tôi làm · Tôi giao · Tôi theo dõi · Tôi duyệt KQ; Tổng / Quá hạn | `tasks/index.vue` |
| NV-02 | Bảng lọc (BL2): Trạng thái · Ưu tiên · Loại · Hạn hoàn thành · Ngày cập nhật · Thêm tiêu chí (Phạm vi Công ty–Phòng–Bộ phận, Giải pháp → Version/Dự án/Hạng mục, Người thực hiện/duyệt/tạo, Tag) | mục 7.2 |
| NV-03 | Chi tiết — đang thực hiện (người thực hiện): nút Nhập kết quả, Báo cáo hôm nay; khối Checklist tick được, Nhiệm vụ con (thẻ bấm mở), Tệp (giao việc / kết quả), Thiết lập (người duyệt, theo dõi, tag, báo cáo tiến độ, dòng đọc Lặp lại) | `CreateTaskModal.view` + `ImportResultModal` |
| NV-04 | Sheet đổi trạng thái — danh sách `allowed_next_statuses`, trạng thái hiện tại ✓ | U2 |
| NV-05 | Sheet đổi trạng thái — bước cần lý do (Từ chối kết quả 7 / Từ chối triển khai 10) | U2, bug #8 |
| NV-06 | Nhập kết quả — chế độ A (không bật báo cáo): giờ thực tế · % luỹ kế · hiệu suất (đọc) · kết quả · tệp kết quả · tick checklist · trạng thái | mục 4 |
| NV-07 | Nhập kết quả — chế độ B (bật báo cáo): nhật ký tiến độ theo ngày (dòng ≤ hôm nay sửa được), % luỹ kế | mục 4, U6 |
| NV-08 | Chi tiết — chờ duyệt kết quả (người duyệt): kết quả + hiệu suất + tệp kết quả; footer [Từ chối | Duyệt hoàn thành] | trạng thái 6 |
| NV-09 | Chi tiết — chờ phê duyệt triển khai (người có quyền Duyệt triển khai task): footer [Từ chối | Duyệt triển khai] | trạng thái 2 |
| NV-10 | Tạo (chế độ Đơn giản mặc định, U8) — khối ① Thông tin (Loại · Tên · Người thực hiện / nhiều người khi Nhiệm vụ chung · Hạn + giờ · Ưu tiên · Số giờ được giao · Trạng thái khởi tạo 1/2/3/4 · Mô tả) mở; ② Gắn với (Giải pháp → Dự án tự điền, Hạng mục, Meeting) · ③ Checklist · ④ Nhiệm vụ con · ⑤ Tệp · ⑥ Thiết lập (Người duyệt KQ, Theo dõi, Tag, Yêu cầu báo cáo tiến độ) gập; footer [Lưu & tạo tiếp | Lưu] | mục 3 |
| NV-10b | Tạo — chế độ Nâng cao (khối ③–⑥ hiện thêm) |  |
| NV-11 | Tạo — lỗi validate (khối có lỗi tự mở, khối gập ghi "n lỗi") | |
| NV-12 | Sửa — khối gập kèm tóm tắt + ô Trạng thái (U2) | |
| NV-13 | Bình luận (sửa màn cũ, C10) | `comment-thread` |
| NV-14 | Lịch sử thay đổi | `system-logs/task` |
| NV-15 | Báo cáo tiến độ nhiệm vụ hằng ngày (sửa màn cũ, U6, C9) | `daily-report` |
| NV-16 | Danh sách rỗng / chưa có quyền | |

### Vấn đề
| Mã | Màn | Nguồn web |
|---|---|---|
| VD-01 | Danh sách — chip vai trò: Tôi phụ trách xử lý · Tôi phát hiện · Tôi theo dõi · Tôi duyệt đóng; Tổng / Quá hạn | `issues/index.vue` |
| VD-02 | Bảng lọc: Trạng thái · Ưu tiên · Loại vấn đề · Ngày tạo · Thêm tiêu chí (Phạm vi, Giải pháp → Version/Dự án/Hạng mục, Người thực hiện/tạo/duyệt) | mục 4.1 |
| VD-03 | Chi tiết — người xử lý: khối Thông tin vấn đề · Ghi nhận phát sinh · Đánh giá ảnh hưởng · Tệp/chứng cứ · Thông tin xử lý · Liên kết & phân loại · Kế hoạch xử lý; footer theo `can_handle` | `CreateIssueModal` (Xem) |
| VD-04 | Sheet đổi trạng thái (Xử lý) — trạng thái + đính kèm; Từ chối/Đóng mở ô lý do | chế độ Xử lý |
| VD-05 | Chi tiết — người duyệt khi Đã xử lý xong: footer [Từ chối | Hoàn thành] | |
| VD-06 | Tạo — 7 khối gập theo web; bắt buộc: Tiêu đề · Loại · Ưu tiên · Ảnh hưởng · Mô tả · Nguồn phát hiện · (Người phụ trách HOẶC Phòng ban xử lý) · Hạng mục khi GP có hạng mục; Đã phân công ⇒ bắt buộc Người phụ trách | mục 2 |
| VD-07 | Tạo — lỗi validate | |
| VD-08 | Sửa | |
| VD-09 | Bình luận (dùng chung khuôn NV-13, có @nhắc tên) | |
| VD-10 | Lịch sử | `system-logs/issue` |

### Phê duyệt
- **CV-PD** Tab Phê duyệt có 3 mục mới (C8) + 1 danh sách lọc sẵn mẫu.

## Việc cho dev (không làm trong thiết kế — cần hỏi user trước khi sửa source)

**BE bảo mật (🔴)**
1. `PUT assign/tasks/{id}` không kiểm `canEdit()` → ai cũng sửa được nhiệm vụ người khác (`TaskService.php:462-519`).
2. `GET assign/tasks/{id}`, comments, `system-logs/task` không kiểm phạm vi xem — đọc được cả Nháp người khác.
3. `POST assign/tasks` / `POST assign/issues` nhận `status` tuỳ ý → tạo thẳng trạng thái Hoàn thành.
4. `GET assign/issues/{id}`, comments, `system-logs/issue`, `issues-upcoming` không kiểm phạm vi xem.
5. `PUT assign/issues/{id}` không kiểm chuyển trạng thái; người chỉ có `can_handle` vẫn sync được theo dõi / phối hợp / tag / đính kèm.
6. `GET assign/tasks/getAll` trả mọi nhiệm vụ toàn hệ thống, không phân trang.

**BE/web nghiệp vụ — app phụ thuộc**
7. % tiến độ luỹ kế (U6): sửa daily report (FE + `TaskService.php:1004-1015`) theo nghĩa luỹ kế.
8. Lý do từ chối: web thêm ô (Nhiệm vụ 7/10); Vấn đề thêm lý do Đóng (`closed_reason`).
9. Sửa không xoá được giá trị về rỗng (`$request->x ?? $task->x`).
10. Vấn đề: người xử lý không có `can_handle` ở trạng thái Mới (lệch `getAllowedNextStatuses`).
11. App cần API tìm nhân viên / giải pháp / dự án có phân trang + tìm phía máy chủ (web đang `per_page=10000`).
12. Deep link thông báo đang là URL web (`/assign/tasks?open_task=`, `/assign/issues?open_issue=`, my-todo `/assign/issue/{id}` sai route) → app cần map.
13. Daily report nuốt `errors[]`, luôn báo thành công.
14. Không có job nhắc sắp/quá hạn; nhắc báo cáo bỏ qua giờ user đặt.
15. API danh sách nhiệm vụ chờ MÌNH duyệt triển khai (quyền `Duyệt triển khai task` + phòng ban quản lý) — cho mục Phê duyệt + số đếm (C15).
16. App gửi `mode` 1/2 theo gạt Đơn giản / Nâng cao (U8).
17. `GET assign/tasks` trả thêm `comments_count` cho nút 💬 trên thẻ (U11) — withCount, không N+1.

Danh sách đầy đủ: mục 14 `khao-sat-web-nhiem-vu.md` (32 điểm), mục 8 `khao-sat-web-van-de.md` (25 điểm).

## Còn để người vẽ quyết
Số đo, bố cục cụ thể từng màn, dữ liệu mẫu, thứ tự artboard trên canvas — bám khuôn meeting-mobile / BL1–BL4.


## Tiến độ vẽ (meeting-mobile.pen, khu x 15600…21196)
- 29/10: XONG toàn bộ — 33 khung, 0 chồng lấn. Hàng 1 (y −1450): CV-00a + NV-01…NV-09 + khung vàng 'So với app hiện tại'. Hàng 2 (y 900): NV-10, 10b, 11, 12, 13, 14, 15, 16 + CV-00b. Hàng 3 (y 2650): VD-01…VD-10 + CV-PD1 (tab Phê duyệt) + CV-PD2 (Duyệt kết quả nhiệm vụ). Backup trước khi vẽ: meeting-mobile.backup-20261029-truoc-nhiem-vu-van-de.pen. User phải Cmd+S trong Pen.
