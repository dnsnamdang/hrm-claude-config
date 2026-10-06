# Task 12 — Nghiệm thu (cổng nghiệm thu cuối Phase 2)

## Trạng thái: ĐẠT — không phát hiện hồi quy, không cần sửa gì

Cả 3 popup báo cáo (`DemandListModal`, `DevelopmentDrillModal`, `ProjectListModal`) đều dựng trên
chung `components/report/V2BaseReportModal.vue`. Đo bằng Playwright thật (viewport 1440×900, phiên
`/tmp/care-state.json`), KHÔNG chỉ đọc code. Không sửa file nào trong `hrm-client` — không có gì cần
sửa. Không commit.

Script đo dùng cho Phần A: `/private/tmp/.../scratchpad/task12-flow.mjs` (viết mới, KHÔNG đụng
`measure-popup.mjs`). Phần B dùng đúng `measure-popup.mjs` có sẵn + 1 script phụ đo 3 chỉ tiêu bổ
sung (`task12-partb-extra.mjs`).

---

## Phần A — 8 luồng × 2 popup MỚI chuyển

### Popup `DevelopmentDrillModal` (customer-market-development) — mở từ dòng "Chưa xác định thị trường"

| # | Luồng | Số đo | Kết quả |
|---|---|---|---|
| 1 | Mở popup | 20 dòng trang 1, `.page-total` = `"Hiển thị 1–20 / 598 meeting"`, bảng nền cùng dòng hiện `598` | ĐẠT — khớp tuyệt đối |
| 2 | Sắp xếp cột CHỮ "Phòng ban" + cột NGÀY "Ngày họp" | asc: `Ban giám đốc Sài Gòn, Kinh doanh CN Vinh, PHÒNG DỰ ÁN×3…`; desc: `PHÒNG THIẾT BỊ XE MÁY` lặp 5 lần; date asc: `03/09 08:00 → 03/09 18:00`; date desc: `19/09 11:00 → 18/09 15:00` | ĐẠT — đổi thứ tự đúng cả 2 chiều, cả 2 cột |
| 3 | Phân trang sang trang 2 | cuộn xuống trước 247px (đụng đỉnh vùng cuộn), sau lật `scrollTop = 0`; STT đầu `21`; `.page-total` → `"21–40 / 598"` | ĐẠT |
| 4 | Đổi 20→50 dòng/trang | 50 dòng, `.page-total` → `"1–50 / 598"`, STT đầu về `1` | ĐẠT |
| 5 | Bộ lọc trong popup (chọn Khách hàng "A DŨNG") | `598 → 1` dòng, "Xoá lọc" → về `598`; **request API = 0 cả 2 thao tác** (lọc client-side) | ĐẠT |
| 6 | Phóng to / thu nhỏ | `.modal-dialog` height: 844 → 900 → 844 | ĐẠT |
| 7 | Đóng, mở lại từ dòng khác ("Thành phố Hà Nội", value 28) | tiêu đề đổi đúng, `.page-total = "1–20 / 28"`, 20 dòng, số dòng/trang về `20` (không mang 50 của lượt trước), dialog height 844 (không mang fullscreen) | ĐẠT — không mang gì từ lượt trước |
| 8 | Bố cục | `wrapBottom 645 ≤ footerTop 787`; `border-top-width: 1px`, `border-radius: 6px` | ĐẠT |

### Popup `ProjectListModal` (prospective-project-results) — mở từ dòng "PHÒNG DỰ ÁN"

| # | Luồng | Số đo | Kết quả |
|---|---|---|---|
| 1 | Mở popup | 20 dòng trang 1, `.page-total = "Hiển thị 1–20 / 50 dự án"`, bảng nền cùng dòng hiện `50`; gọi API `project-list` đúng **1 lần** | ĐẠT |
| 2 | Sắp xếp cột CHỮ "Nhân viên phụ trách" + cột NGÀY "Ngày lập dự án" | asc: `Nguyễn Quốc Trung, Nguyễn Đức Hiểu×4…`; desc: `Đào Phúc Sơn` lặp 5 lần; date asc: `03/07 → 03/07 → 06/07 → 09/07×2`; date desc: `07/09 → 30/08 → 28/08×3` | ĐẠT |
| 3 | Phân trang sang trang 2 | cuộn xuống đúng 300px, sau lật `scrollTop = 0`; STT đầu `21`; `.page-total` → `"21–40 / 50"` | ĐẠT |
| 4 | Đổi 20→50 dòng/trang | 50 dòng, `.page-total → "1–50 / 50"`, STT đầu về `1` | ĐẠT |
| 5 | Bộ lọc trong popup (chọn Nhân viên "Đỗ Tương Lai - HP_KD - NV.1106") | `50 → 0` dự án, xoá lọc (nút × select2) → về `50`; **request API = 1 cho MỖI thao tác** (lọc BE thật, đúng như thiết kế TKT gọi lại `fetchList()`) | ĐẠT |
| 6 | Phóng to / thu nhỏ | `.modal-dialog` height: 844 → 900 → 844 | ĐẠT |
| 7 | Đóng, mở lại từ dòng khác ("PHÒNG DỰ ÁN TRỌNG ĐIỂM", value 8) | tiêu đề đổi đúng, `.page-total = "1–8 / 8"`, 8 dòng, số dòng/trang về `20`, dialog height 844, gọi API lại đúng 1 lần | ĐẠT — không mang gì từ lượt trước |
| 8 | Bố cục | `wrapBottom 642 ≤ footerTop 787`; `border-top-width: 1px`, `border-radius: 6px` | ĐẠT |

Ghi chú: ở luồng 5 của TKT, field lọc đầu tiên theo thứ tự `FILTER_FIELDS.dept` là "Bộ phận" —
phòng "PHÒNG DỰ ÁN" không chia bộ phận nên select2 ra `"No results found"` (đúng luật ẩn/rỗng, không
phải lỗi); script tự dò field kế tiếp có option thật ("Nhân viên") để đo — không phải bỏ qua lỗi.

**Cả 12 số đo `heightNormal=844` / `heightFull=900` / `borderTopWidth=1px` / `borderRadius=6px` của
2 popup MỚI đều khớp CHÍNH XÁC với `baseline.json` của popup gốc** — xác nhận cả 3 popup nay dùng
đúng 1 vỏ, không lệch khuôn.

---

## Phần B — Kiểm hồi quy popup thứ nhất (`potential-customer-care` / `DemandListModal`)

Chạy `measure-popup.mjs` với tham số mặc định, so với `baseline.json`:

| Khoá | baseline.json | Đo lại (task 12) | Trạng thái |
|---|---|---|---|
| `cols` (13 cột) | khớp | khớp | khớp |
| `firstPageRowCount` | 20 | 20 | khớp |
| `sttFirst` / `sttLast` | "1" / "20" | "1" / "20" | khớp |
| `pageTotal` | "Hiển thị 1–20 / 126 nhu cầu" | như cũ | khớp |
| `tableBottom` | 713 | **709** | **LỆCH ĐÃ BIẾT** (713→709) |
| `footerTop` | 803 | **787** | **LỆCH ĐÃ BIẾT** (803→787) |
| `heightNormal` | 844 | 844 | khớp |
| `sortTextAsc` (20 phần tử) | khớp | khớp từng ký tự | khớp |
| `sortDateAsc` (20 phần tử) | khớp | khớp từng ký tự | khớp |
| `heightFull` | 900 | 900 | khớp |

**Kết quả: đúng 9/11 khớp, đúng 2/11 lệch đã biết — KHÔNG xuất hiện khoá lệch thứ ba.** Không có hồi
quy nào mới do Phase 2 gây ra cho popup 1.

### 3 phép đo thêm (đã từng lọt lưới ở popup 1)

1. **`td.report-drill-table__money` còn căn phải / in đậm?** — đo `getComputedStyle`: `text-align:
   right`, `font-weight: 700` (giá trị mẫu đo được: `"2.220.000"`). ĐẠT — cellClass của vỏ dùng
   chung vẫn áp đúng.
2. **Mở popup đếm request `demand-list` phải = 1** — đo được đúng **1 request**:
   `GET .../demand-list?period=month&criteria=all&drill=field:7`. ĐẠT.
3. **Đang ở trang 3, bấm sắp xếp phải về trang 1** — trước khi bấm: STT đầu `41`, `.page-total =
   "41–60 / 126"`; sau khi bấm sắp xếp cột "Thị trường / Phường xã": STT đầu `1`, `.page-total =
   "1–20 / 126"`. ĐẠT.

---

## Phần C — Bộ e2e

```
cd e2e && PATH=".../node/v20.20.1/bin:$PATH" npx playwright test --project=api-setup --workers=1 --retries=0
```
→ **1 failed** — đúng vật cản môi trường đã biết và đã chốt KHÔNG sửa:
`Illuminate\Database\QueryException: SQLSTATE[42S02]: Base table or view not found: 1146 Table
'hrm_erp.hrm_employees' doesn't exist` (trong `auth/api.setup.ts` → `database/e2e_provision.php`).
Không sửa `e2e_provision.php`, không đụng dữ liệu DB.

`--list --no-deps` cho cả 3 spec — biên dịch OK, đúng số ca kỳ vọng:

| Spec | Số ca | Kỳ vọng |
|---|---|---|
| `potential-customer-care.spec.ts` | 29 | 29 ✓ |
| `customer-market-development.spec.ts` | 18 | 18 ✓ |
| `tkt-result-report.spec.ts` | 10 | 10 ✓ |

---

## Việc KHÔNG làm (đúng ràng buộc)

- Không sửa file nào trong `hrm-client` (không có gì cần sửa — không phát hiện lỗi nào do đợt
  chuyển vỏ Phase 2 gây ra).
- Không đụng `components/V2BaseSmartFilterPanel.vue`, `components/print/ReportPrintPreviewModal.vue`,
  `CareTrackingTable.vue`, `potential-customer-care/index.vue`, `measure-popup.mjs`, `baseline*.json`.
- Không đụng DB, không `pkill`, không khởi động lại server, không `git add -A`.
- Không tạo subagent nào khác — toàn bộ Playwright chạy trực tiếp bằng script Node do chính task
  này viết (`task12-flow.mjs`, `task12-partb-extra.mjs`, cả 2 nằm trong scratchpad, không nằm trong
  repo `HRM/`).
- Không commit — không có thay đổi source nào để commit.
