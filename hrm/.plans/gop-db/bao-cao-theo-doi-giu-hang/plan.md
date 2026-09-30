# Plan — Báo cáo theo dõi giữ hàng

> Chưa lập plan code. Đang chờ duyệt mockup `bao-cao-theo-doi-giu-hang.html`.
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md`

## Phase 0 — Mockup & chốt yêu cầu

- [x] Rà hiện trạng màn `/finance/prepick-stocks` (FE 899 dòng, BE `PrepickStockReportService`)
- [x] Chốt 5 quyết định thiết kế (xem `design.md`)
- [x] Dựng mockup HTML theo ngôn ngữ thiết kế báo cáo TKT
- [x] Kiểm chứng mockup bằng Playwright (đo DOM: tổng khớp cấp con, không tràn ngang, màu header)
- [x] Bổ sung vòng 2: ngưỡng cảnh báo cấu hình được · cột Tồn hiện tại + SL đang giữ · cột Số lần gia hạn + popup lịch sử · bỏ Tỷ trọng quá hạn · đổi "Hạn giữ" → "Hạn giữ hiện tại"
- [x] Kiểm dữ liệu BE cho "Số lần gia hạn" trên DB thật (phát hiện gia hạn TÁCH LÔ — phải đếm theo nhóm giữ)
- [x] Bổ sung vòng 3: cột chính đo kép (số mã / số lượng) · bộ cột hàng hoá bám ERP (bỏ Kho) · gỡ Số lần gia hạn khỏi bảng, đưa vào popup theo từng lô
- [x] Bổ sung vòng 4: tô màu ô Hạn giữ hiện tại theo ngưỡng cảnh báo · cột ĐVT riêng + bỏ hậu tố đơn vị ở ô số · popup luôn giữ 2 cột Mã/Tên hàng · mã hàng đứng trước tên · tiêu đề popup dạng "Mã - Tên"
- [x] Bổ sung vòng 5: "Số lượng giữ" · mã hàng gộp lại vào ô tên với style riêng · sort 4 cột · nhân viên kèm phòng ban · cột Số hợp đồng + Tổng thanh toán + popup phiếu thu · chốt thứ tự mặc định toàn báo cáo
- [x] Bổ sung vòng 6: bỏ cột Tồn ở popup + ở tiêu chí Nhân viên · thêm bộ lọc Hình thức giữ · sửa định nghĩa đo: theo DÒNG (1 mã → số lượng, nhiều mã → số mã) thay vì theo cấp
- [x] Bổ sung vòng 7: bỏ đổi đơn vị (luôn ĐVT cơ bản) · khối tổng hợp 1 đếm theo YÊU CẦU GIỮ · sort thêm 3 cột popup
- [x] Bổ sung vòng 8: bỏ đổi nền khi hover tiêu đề cột sort · thêm ô "NV có hàng giữ quá hạn" vào khối hạn giữ
- [x] Bổ sung vòng 9: bỏ thuật ngữ "lô" khỏi giao diện (đụng `warehouse_import_lots` có thật) · sửa mô hình dữ liệu demo để 1 yêu cầu giữ gồm nhiều dòng đúng tỉ lệ thật
- [x] Đổi vị trí 2 khối tổng hợp: Phạm vi đang giữ → Tình trạng theo yêu cầu giữ
- [x] Cột "Nhân viên giữ" trong popup chỉ hiện tên (đã có cột Phòng ban riêng)
- [x] Lối tắt "Hàng giữ của tôi" (ép tiêu chí NV + công ty/phòng/nhân viên của mình + bung tới hàng hoá; tắt thì khôi phục bộ lọc cũ)
- [x] Chốt định nghĩa "Số yêu cầu giữ" = Phiếu + Mã hàng + Nhân viên (thật: 2.412 dòng / 2.410 yêu cầu / 593 phiếu); đổi cột popup thành "Phiếu giữ gốc"
- [x] Chốt ràng buộc BE: lần ngược chuỗi gia hạn về chứng từ gốc trước khi đếm (tránh đếm chồng + tránh sai "Phiếu giữ gốc" ở 46% dòng); mockup thêm ca gia hạn một phần để chứng minh
- [x] Chốt phân quyền: 1 quyền duy nhất "Xem báo cáo giữ hàng theo tổng công ty" (quyền này CHƯA tồn tại, phải thêm seeder); mockup demo 2 trạng thái qua `?noPerm=1`
- [x] Chốt: KHÔNG gate vào màn (không dùng quyền `Quản lý giữ hàng`); không giới hạn phòng ban — không có quyền thì vẫn xem cả công ty mình
- [x] Viết spec chi tiết `docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md`
- [x] Bổ sung phân trang vào mockup: bảng chính theo node cấp 1 (mặc định 25), popup theo dòng (mặc định 20); dòng TỔNG không theo trang; sort/lọc reset về trang 1
- [x] Bổ sung vòng 10: lọc **Bộ phận** (cascade sau Phòng ban, 3 trạng thái, mục "Chưa phân bộ phận") · popup đưa 3 cột Ngày bắt đầu giữ / Hạn giữ hiện tại / Số lần gia hạn lên ngay sau "SL đang giữ" · **ghim 3 cột đầu popup** khi cuộn ngang · **In / Xuất Excel** thật (4 đường, đều lấy toàn bộ theo bộ lọc)
- [x] Bổ sung vòng 11: 2 nút **Gia hạn** / **Huỷ giữ** (icon + chữ) nằm TRONG ô "Hạn giữ hiện tại", chỉ hiện ở chế độ "Hàng giữ của tôi" — không tách cột riêng
- [x] Rà toàn bộ nút theo `button-convention` — phát hiện & sửa 5 lỗi ở nút cũ (chữ bị cấm, quá 3 từ, thứ tự footer, thiếu icon, sai màu nhóm Xuất)
- [ ] **User duyệt mockup** ← đang chờ
- [ ] Lên plan code (Phase 1 BE · Phase 2 FE) sau khi mockup được duyệt

### Checkpoint — 2026-09-15 (rà nút theo skill)
Vừa hoàn thành: user yêu cầu "check button đúng skill chưa" → rà TOÀN BỘ nút trong mockup theo
`button-convention`, không chỉ 2 nút mới. Phát hiện **5 lỗi ở các nút CŨ** (làm từ vòng In/Excel,
không phải do quyết định nào của user) — đã sửa hết, chi tiết ở `design.md` mục 49:
  1. "In báo cáo" → **"In danh sách"** (chữ cũ nằm thẳng trong cột "KHÔNG dùng" của bảng text chuẩn)
  2. "Xuất Excel danh sách" → **"Xuất Excel"** (4 từ, vượt trần 3 từ)
  3. Thứ tự footer: Thoát/Huỷ phải CUỐI CÙNG → `In danh sách · Xuất Excel · Đóng` và `In · Hủy`
  4. 4 nút Đóng/Hủy thiếu icon → thêm icon mũi tên trái
  5. "Xuất Excel" trong popup tô teal như nút chính → đổi **xanh lá `#16a34a`**, cùng nhóm với nút
     Xuất Excel ở thanh tiêu đề (2 nút cùng việc mà 2 màu là đọc thành 2 mức quan trọng khác nhau)
Đo lại sau khi sửa: 5/5 nhóm nút đúng chữ + đúng thứ tự + đủ icon; 2 nút Gia hạn/Huỷ giữ vẫn chạy,
nút Excel vẫn tải file, nút Đóng/Hủy vẫn đóng popup; console sạch.
3 điểm vẫn lệch skill nhưng **do user chốt**, ghi ở `design.md` mục 48: nhãn "Huỷ giữ" (thay vì
"Hủy") · nút trong bảng icon+chữ (thay vì `V2BaseIconButton` icon-only) · nút Huỷ giữ dạng viền
(thay vì `primary status="danger"` nền đỏ đặc).
ℹ️ Phát hiện thêm: **`button-convention` tự mâu thuẫn về nút In** — mục 2 xếp In vào nhóm `primary`,
mục 2b lại xếp `secondary/tertiary`. Mockup xử theo ngữ cảnh (In là action chính của popup chọn chế
độ in → primary; In danh sách ở footer popup chi tiết là bổ trợ → secondary). Nên làm rõ trong skill.
Bước tiếp theo: user duyệt mockup → lên plan code.

### Checkpoint — 2026-09-14 (vòng 11)
Vừa hoàn thành: 2 nút **Gia hạn** / **Huỷ giữ** (icon + chữ) nằm TRONG ô "Hạn giữ hiện tại".
Làm 2 nhịp: nhịp 1 tách thành cột Hành động riêng, nhịp 2 user chốt gộp vào ô hạn giữ + đổi sang
nút có chữ → bỏ cột riêng. Đo bằng Playwright:
  · Bảng vẫn **15 cột** ở cả 2 chế độ (không tốn thêm cột) · chế độ thường 0 nút · chế độ "của tôi"
    20/20 dòng đủ 2 nút
  · Ô hạn giữ rộng 196px, 2 nút 70/71 × 22px gọn 1 hàng, dòng cao đều 76px, không tràn ô
  · Nút giữ đúng màu teal/đỏ ở CẢ 3 trạng thái hạn — không bị màu chữ của ô (xanh/vàng/đỏ) đè
  · Ghim 3 cột đầu vẫn chuẩn 46/314px, lệch 1px
  · Bản in / Excel vẫn 15 cột và KHÔNG dính chữ nút · console sạch
Lỗi tự phát hiện & sửa trong vòng này:
  · Chèn chú thích ra NGOÀI khối `/* */` làm hỏng cú pháp JS cả file — triệu chứng là `.rsum-drill`
    trả `null` (bảng không render), console chỉ ghi "Unexpected string"
  · Nhét nút vào ô dữ liệu làm bản in kéo theo chữ nút:
    `"03/08/2026 quá hạn 40 ngày Gia hạn Huỷ giữ"` → phải gỡ `.row-acts` trước khi lấy text
2 điểm lệch quy ước đã nêu và user chốt (chi tiết + rủi ro ở `design.md` mục 48):
  a. Nhãn "Huỷ giữ" giữ chính tả user, khác dấu kiểu mới "Hủy" của `button-convention`
  b. **Nút Gia hạn hiện ở MỌI dòng** kể cả dòng Trong hạn — tôi đã nêu đây là nút chết
     (màn lập phiếu gia hạn chỉ nhận lô `expire_date <= hôm nay + warning_day`), user vẫn chọn
     → lúc code BE BẮT BUỘC xử 1 trong 2: màn gia hạn báo rõ lý do khi dòng chưa tới ngưỡng,
       hoặc hỏi khách để nới điều kiện `getDataToCreate()`
Bước tiếp theo: user duyệt mockup → lên plan code.

### Checkpoint — 2026-09-14 (vòng 10)
Vừa hoàn thành: 4 yêu cầu của vòng 10, đã kiểm chứng bằng Playwright (đo DOM, không nhìn ảnh):
  · Lọc Bộ phận: 3 trạng thái đúng · `21 + 17 + 29 = 67` = đúng tổng của phòng (không mất dòng) ·
    cascade reset đúng · "Hàng giữ của tôi" ép 6 giá trị và khôi phục đúng · "Xoá lọc" không đụng công ty
  · Ghim cột: cuộn ngang 900px, 3 cột ghim lệch 1px (viền), khít nhau, cột 4 cuộn đi; nền đặc, z-index đúng
  · In/Excel: trang 1 và trang 2 in ra cùng 73 dòng · `level=0` vẫn in đủ cấp hàng hoá ·
    popup hiện 20 dòng/trang nhưng xuất 185 dòng · bảng chi tiết 15 cột không tràn khổ A4 ngang (1.046/1.047px)
  · Console sạch, thanh lọc không sinh cuộn ngang
Lỗi tự phát hiện & sửa trong vòng này (chi tiết ở `design.md` mục 46–47):
  · **`getBoundingClientRect` trả toạ độ sau `transform: scale(.96)`** của popup → ghim lệch 13px.
    Mất 3 lần đo mới ra (2 giả thuyết sai trước đó: border-collapse, rồi animation chưa xong).
    `ResizeObserver` không bắt được vì transform không đổi kích thước layout → phải dùng `offsetLeft`.
  · Đổ HTML ra text phẳng làm các mẩu `<span>` dính liền (`VT.00611-Ống…`) → chèn khoảng trắng 2 phía
  · Thụt lề cây bằng dấu cách thường bị HTML/Excel nuốt → dùng ` `
  · Lấy tiêu đề popup sau `closeDrill()` ra tiêu đề "toàn bộ báo cáo" → lấy trước khi đóng
Đang làm dở: không có việc đang dở — chờ user duyệt mockup.
Bước tiếp theo: user duyệt mockup → lên plan code.
Blocked: vẫn 3 việc của checkpoint 13/09 (quyền chưa tồn tại · cách lấy chứng từ gốc · cỡ trang),
  thêm 1 việc mới: dữ liệu **bộ phận gần như trống trên DB thật** (2,6% dòng hàng giữ) — cần hỏi
  nghiệp vụ xem có kế hoạch gán bộ phận cho nhân viên kinh doanh không, nếu không thì ô lọc này
  gần như luôn ở trạng thái khoá.

### Checkpoint — 2026-09-13
Vừa hoàn thành: mockup hoàn chỉnh (13 vòng chỉnh, vòng cuối là **phân trang**) + spec chi tiết đã
viết đầy đủ ở `docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md`.
Toàn bộ quyết định nghiệp vụ, phân quyền, phân trang và ràng buộc BE đã chốt, ghi vào `design.md`
(43 mục quyết định) + spec (13 chương).
Đang làm dở: không có việc đang dở — chờ user duyệt mockup.
Bước tiếp theo: user duyệt mockup → lên plan code.
  · Phase 1 BE: service đọc mới (KHÔNG sửa `PrepickStockReportService` đang phục vụ màn expiring) +
    lần ngược chuỗi gia hạn + 6 endpoint + thêm quyền vào seeder.
  · Phase 2 FE: viết lại `pages/finance/prepick-stocks/index.vue` theo mockup.
Blocked: 3 việc phải xử lý/hỏi ngay đầu Phase 1 —
  (1) quyền `Xem báo cáo giữ hàng theo tổng công ty` CHƯA tồn tại, phải thêm `PermissionsTableSeeder`;
  (2) cách lấy chứng từ gốc: recursive CTE mỗi lần chạy, hay denormalize `root_objectable_id/type` —
      cột mới trên bảng DÙNG CHUNG với ERP nên phải hỏi trước;
  (3) chốt cỡ trang + ngưỡng lazy load sau khi đo thời gian phản hồi trên dữ liệu thật.

### Checkpoint — 2026-09-12 (vòng 9)
Vừa hoàn thành: mockup bản 9 + kiểm chứng trình duyệt. Lỗi đã tự phát hiện & sửa qua 3 vòng: min-width bảng cắt cột · header chữ trắng trên nền trắng · flex co sập bảng lịch sử còn 2px · `.drill-table` min-width 1740px của bảng 14 cột · tồn kho demo nhỏ hơn số đang giữ · số lần gia hạn đếm gộp sai cấp · đổi thứ tự colgroup mà quên đổi thứ tự render ô làm lệch toàn bảng 1 nhịp · `.drill-table` min-width 1740px cắt cột ở popup phiếu thu (bẫy lặp lần 2).
Đang làm dở: chờ user duyệt mockup.
Bước tiếp theo: user duyệt → viết `docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md` rồi lên plan code.
Blocked:
