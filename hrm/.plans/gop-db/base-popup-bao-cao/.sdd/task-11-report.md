# Task 11 — Cập nhật e2e của 2 màn báo cáo

## Trạng thái: XONG

`HRM/e2e` **không phải git repo** (đã xác nhận lại bằng `git status` → `fatal: not a git
repository`) — 2 file spec đã sửa **trực tiếp trên đĩa**, không có commit nào được tạo.

## Số chỗ đã đổi

- `tests/assign/customer-market-development.spec.ts`: đổi **19/19** chỗ literal `cmd-drill` (theo
  đúng brief) **+ thêm 9 chỗ khác không chứa chuỗi con `cmd-drill` nhưng vẫn trỏ vào lớp đã bị đổi
  tên** — phát hiện được nhờ đối chiếu với mã nguồn thật thay vì chỉ đếm chuỗi `cmd-drill`:
  `.cmd-kpi`, `.cmd-kpi__label`, `.cmd-kpi__value`, `.cmd-sum__grp`, `.cmd-sum__label`,
  `.cmd-sum__chip`, `.cmd-sum__chip--on`, `.cmd-sum__chip__n`, `.cmd-sumbox__title`,
  `.cmd-sumhead`, `.cmd-sumwrap` → đổi hết sang `report-drill-*`. Nếu chỉ đổi đúng 19 chỗ theo
  literal-match thì bộ này vẫn đỏ vì các selector trên.
  `#cmd-print-options-modal` **GIỮ NGUYÊN** — đây là `id` của `PrintOptionsModal.vue` (file khác,
  ngoài phạm vi task), đã kiểm nguồn: `id="cmd-print-options-modal"` chưa từng đổi.
- `tests/assign/tkt-result-report.spec.ts`: đổi **15/15** chỗ `tkt-drill-*` → `report-drill-*`
  (đúng brief, không phát sinh selector ẩn nào khác ngoài 15 chỗ này). Chuỗi `tkt-result-report`
  còn lại trong 1 dòng comment (tên file chính nó) không phải selector, không đổi.

`grep -c "cmd-drill" tests/assign/customer-market-development.spec.ts` → `0`
`grep -c "tkt-drill" tests/assign/tkt-result-report.spec.ts` → `0`
(không còn selector nào bám `cmd-drill-modal`/`tkt-drill-modal` trong 2 file — chỉ có
`#cmd-print-options-modal`, đã ghi rõ ở trên, giữ nguyên vì không phải lớp bị đổi.)

## Bảng đối chiếu selector ↔ nguồn thật

Đối chiếu từng `report-drill-*` dùng trong 2 spec với 3 nguồn: `V2BaseReportModal.vue` (vỏ),
`DevelopmentDrillModal.vue`, `ProjectListModal.vue` (+ `V2BaseTableScroll.vue`,
`V2BaseModal.vue`, `V2BasePagination.vue` cho các lớp `v2-*`/`modal-*`/`rsum-toggle`).

| Selector trong spec | Định nghĩa tại | Có tồn tại? |
| --- | --- | --- |
| `.report-drill-dialog` | `V2BaseReportModal.vue` (prop `dialogClass` mặc định) | Có |
| `.report-drill-dialog .modal-content` | `V2BaseReportModal.vue` (khối không scoped) | Có |
| `.report-drill-dialog .modal-footer` | `.modal-footer` do `V2BaseModal.vue` render (`class="modal-footer v2-modal-footer"`) | Có |
| `.report-drill-dialog .v2-modal-body` | `V2BaseModal.vue` template (`<div class="v2-modal-body">`) | Có |
| `.report-drill-dialog .row.paging` | `V2BasePagination.vue` (`class="row paging mt-3"`) | Có |
| `.report-drill-table` | `V2BaseReportModal.vue` (scoped, `<table class="report-drill-table">`) | Có |
| `.report-drill-table thead th` / `tbody tr` | như trên | Có |
| `.v2-table-scroll`, `.v2-table-scroll__top`, `.v2-table-scroll__body` | `V2BaseTableScroll.vue` | Có |
| `.report-drill-sumhead`, `.report-drill-sumwrap` | `DevelopmentDrillModal.vue` (scoped) | Có |
| `.report-drill-kpi`, `__label`, `__value` | `DevelopmentDrillModal.vue` | Có |
| `.report-drill-sum__grp`, `__label` | `DevelopmentDrillModal.vue` | Có |
| `.report-drill-sum__chip`, `--on`, `__n` | `DevelopmentDrillModal.vue` | Có |
| `.report-drill-sumbox__title` | `DevelopmentDrillModal.vue` | Có |
| `.rsum-toggle` | `DevelopmentDrillModal.vue` (giữ nguyên tên, không đổi tiền tố) | Có |
| `.report-drill-count` | `ProjectListModal.vue` | Có |
| `.report-drill-sum-toggle` | `ProjectListModal.vue` | Có |
| `.report-drill-filters__item` | `ProjectListModal.vue` | Có |
| `.report-drill-chips__grp`, `__label` | `ProjectListModal.vue` | Có |
| `.report-drill-chip__n` | `ProjectListModal.vue` (đúng `chip__n` số ít, không phải `chips__n`) | Có |
| `#cmd-drill-modal` / `#tkt-project-list-modal` | không bị spec nào bám tới (đã kiểm, không có) | N/A |

**Danh sách "không tìm thấy nơi định nghĩa": RỖNG.**

## 3 bẫy đã biết trước — kết quả kiểm

1. `modal-id` giữ tiền tố cũ (`cmd-drill-modal`, `tkt-project-list-modal`) — 2 spec **không bám
   selector nào** vào các id này (đã grep xác nhận), nên không có gì phải giữ/sửa ở bước này.
2. 2 literal `cmd-center`/`cmd-money` trong `columns()` của `DevelopmentDrillModal.vue` — đúng như
   ghi trong brief, cố ý giữ nguyên (nguồn dùng chung in/Excel, map qua `CELL_CLASS_MAP`), không
   liên quan tới 2 file spec (spec không tham chiếu 2 chuỗi này).
3. Gạch nối ASCII `1-20` vs en dash `1–20`: kiểm cả 2 spec, **không có** assertion nào so sánh
   trực tiếp chuỗi có dấu gạch ngang phân trang (`Hiển thị X–Y / Z`) — mọi chỗ liên quan phân
   trang đều dùng `.toContain(\`/ ${total}\`)` hoặc đọc `firstStt`/`lastStt` bằng số. Không có gì
   phải sửa.

## Output `--list --no-deps`

`customer-market-development.spec.ts` → **18 tests** (đúng kỳ vọng):
```
Listing tests:
  [chromium] › ...spec.ts:85:5 › Bảng theo dõi có đúng 9 cột và KHÔNG còn cột "Đã thực hiện"
  [chromium] › ...spec.ts:106:5 › Bung tất cả cấp: dòng cha = tổng dòng con trên 6 cột số (đo từ DOM)
  [chromium] › ...spec.ts:181:5 › Đổi tiêu chí thì nhãn cấp và ô lọc riêng đổi theo
  [chromium] › ...spec.ts:192:5 › Popup meeting và popup KH mới có đúng bộ cột riêng
  [chromium] › ...spec.ts:249:5 › Popup mở theo 1 node thì bỏ cột của cấp đã cố định
  [chromium] › ...spec.ts:281:5 › Bộ chọn cấp xem: ô nằm gọn trong ô tiêu đề, dropdown không bị khung bảng cắt
  [chromium] › ...spec.ts:352:5 › Bộ chọn cấp xem: chọn "Tất cả cấp" thì bảng bung đủ cấp
  [chromium] › ...spec.ts:374:5 › Có đủ icon ⓘ giải thích và định dạng số đồng nhất
  [chromium] › ...spec.ts:399:5 › Tooltip ⓘ mở được và đúng chuẩn icon của hệ thống
  [chromium] › ...spec.ts:428:5 › Popup dựng đúng khuôn V2BaseModal: footer ghim đáy, 1 thanh cuộn dọc, có cuộn ngang trên
  [chromium] › ...spec.ts:485:5 › Popup có bộ lọc riêng, ẩn đúng chiều đã cố định và lọc thật sự
  [chromium] › ...spec.ts:563:5 › In báo cáo: popup chọn chế độ -> bản xem trước đúng khuôn
  [chromium] › ...spec.ts:637:5 › In danh sách từ popup: bản in khớp đúng tập đang lọc trong popup
  [chromium] › ...spec.ts:748:5 › Khối tổng hợp popup: mặc định THU GỌN, mở ra không đẻ thanh cuộn dọc thứ 2
  [chromium] › ...spec.ts:815:5 › Khối tổng hợp popup: 3 KPI đúng số, chip phân bổ lọc thật và ẩn đúng chiều đã cố định
  [chromium] › ...spec.ts:955:5 › Phân trang bảng theo dõi: cắt theo dòng cấp 1, STT chạy tiếp, dòng TỔNG luôn hiện
  [chromium] › ...spec.ts:1046:5 › Phân trang popup: STT chạy tiếp, lọc thì về trang 1, KPI vẫn tính trên TOÀN tập
  [chromium] › ...spec.ts:1125:5 › Nút "Xuất Excel danh sách" trong popup tải file từ SERVER (không dựng ở FE)
Total: 18 tests in 1 file
```

`tkt-result-report.spec.ts` → **10 tests** (đúng kỳ vọng):
```
Listing tests:
  [chromium] › ...spec.ts:291:5 › 1. Dòng TỔNG khớp dải tổng hợp ở 4 chỉ tiêu (...)
  [chromium] › ...spec.ts:322:5 › 2. Hai đẳng thức bất biến (...) đúng trên DOM ở mọi dòng, cả 3 tiêu chí
  [chromium] › ...spec.ts:357:5 › 3. Dòng cha = tổng dòng con ở 5 cột cộng được hiện trên bảng, cả 3 tiêu chí
  [chromium] › ...spec.ts:404:5 › 4. Đổi tiêu chí đổi đúng thứ tự ô lọc, nhãn select cấp, nhãn dòng TỔNG và thứ tự chip phân bổ
  [chromium] › ...spec.ts:423:5 › 5. Chọn cấp "Đến Bộ phận" không lòi dòng Nhân viên của phòng không chia bộ phận
  [chromium] › ...spec.ts:451:5 › 6. 4 luật bỏ cột / ẩn ô lọc của popup (2 luật cột do BE, 2 luật ẩn ô lọc do FE)
  [chromium] › ...spec.ts:538:5 › 7. Cột "Giá trị HĐ" luôn hiện "—" ở mọi ô, không ô nào là 0
  [chromium] › ...spec.ts:562:5 › 8. Fail-closed: đăng nhập fx.noperm_email không thấy dự án fixture nào
  [chromium] › ...spec.ts:609:5 › 9. Chip phân bổ: tổng số lượng của 1 chiều bằng đúng số dòng popup đang liệt kê
  [chromium] › ...spec.ts:652:5 › 10. Số vừa bấm trên bảng khớp đúng `total` của popup, nhiều cấp × 2 tiêu chí (dept, market)
Total: 10 tests in 1 file
```

## Danh sách selector còn nghi vấn

**RỖNG.**

## Ràng buộc đã giữ

- Không sửa mã nguồn `hrm-client` (chỉ đọc để đối chiếu).
- Không chạy cả bộ test (Task 12), không đụng DB, không `pkill`, không khởi động lại server.
- Không đổi line ending: cả 2 file gốc là LF thuần (không có `\r`), sau khi sửa vẫn LF thuần
  (`grep -c $'\r'` = 0 cả 2 file).
- Không tạo subagent nào khác.
