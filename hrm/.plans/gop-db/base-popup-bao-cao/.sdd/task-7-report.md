# Task 7 — Báo cáo cổng nghiệm thu (2026-09-17)

## Trạng thái

**Không sửa mã nguồn.** Bộ e2e `potential-customer-care` KHÔNG chạy được do vật cản môi trường đã
biết trước (bảng `hrm_*` không tồn tại trong DB local `hrm_erp`), đúng như ruling đã chốt — không
đụng `e2e_provision.php`, không tạo/sửa tài khoản/dữ liệu dùng chung. Thay thế: kiểm chứng bằng tay
qua Playwright MCP trên trình duyệt thật, đo bằng số lấy từ DOM cho toàn bộ 8 luồng nghiệp vụ chính
của `DemandListModal` (đã chuyển sang `V2BaseReportModal`). Cả 8 luồng đều ĐẠT.

## Phần A — vật cản môi trường (xác nhận, không sửa)

```
cd HRM/e2e
ps aux | grep -c "[p]laywright test"   # 0
PATH=".../v20.20.1/bin:$PATH" npx playwright test --project=api-setup --workers=1 --retries=0
```

Kết quả: **1 failed** — đúng vật cản đã biết.

```
Illuminate\Database\QueryException  SQLSTATE[42S02]: Base table or view not found: 1146
Table 'hrm_erp.hrm_employees' doesn't exist
(SQL: select * from `hrm_employees` where `email` = e2e_assign@test.local limit 1)
...
Error: Không thấy E2E_JSON= trong output provision:
  at auth/api.setup.ts:30:20
1 failed
  [api-setup] › auth/api.setup.ts:17:6 › provision and login API
```

Không phải hồi quy của đợt tách component — lỗi nằm ở schema DB local (bảng `hrm_employees` chưa
tồn tại), như brief đã dự đoán. Theo ruling: dừng ở đây, không sửa `e2e_provision.php`, không đụng
DB.

## Phần B — chạy được tới đâu

- `npx playwright test tests/assign/potential-customer-care.spec.ts --list --no-deps` →
  **`Total: 29 tests in 1 file`** (đúng kỳ vọng, file spec nguyên vẹn).
- Chạy thật `--no-deps --workers=1 --retries=0`:

```
Error: Seed báo cáo CSKH thất bại:
LOI: khong tim thay employee e2e_assign@test.local -> chay e2e_provision.php truoc.
  at tests/assign/potential-customer-care.spec.ts:36:22
1 failed
  [chromium] › ...spec.ts:196:5 › 1. Màn có đủ 2 khối tổng hợp...
28 did not run
```

Đúng như dự đoán: `beforeAll` đổ vì thiếu tài khoản e2e trong DB (hệ quả trực tiếp của vật cản Phần
A). Không cố tạo dữ liệu để vượt qua.

## Phần C — kiểm tay bằng Playwright trên trình duyệt thật

Môi trường: dùng `/tmp/care-state.json` (localStorage `access_token`, origin
`http://127.0.0.1:3000`) nạp thủ công vào MCP browser session, viewport set `1440x900`, mở
`http://127.0.0.1:3000/assign/report/potential-customer-care`. Servers Nuxt 3000 + API 8000 đã
chạy sẵn, không khởi động lại.

| # | Luồng | Đo được | Kết luận |
|---|---|---|---|
| 1 | Mở popup từ dòng cha "Dịch vụ ô tô" (nền hứa 126) | popup: `rowCount`=20 (trang 1), `.page-total`="Hiển thị 1–20 / 126 nhu cầu"; khớp số nền (126) | **ĐẠT** |
| 2 | Sắp xếp cột "Thị trường / Phường xã" rồi "Meeting thu thập nhu cầu" | Trước sort: `[Hoàng Mai, Khương Đình, Tây Mỗ, Sài Đồng, Khương Đình]`. Sau click cột 1 (icon → `ri-arrow-up-line`): `[Duy Tân, Cầu Giấy, Cầu Giấy, Cầu Giấy, Cửa Nam]` — thứ tự đổi. Sau click cột Meeting (icon → `ri-arrow-up-line`): 5 giá trị đầu đổi thành ngày tăng dần `04/09 → 05/09 → 05/09 → 05/09 → 05/09`; không có ô trống trong 20 dòng trang hiện tại | **ĐẠT** |
| 3 | Phân trang, có cuộn 300px trước khi lật | Cuộn `.report-drill-wrap.scrollTop=300` trước khi bấm trang 2 → sau khi lật: `firstStt`="21", `.page-total`="Hiển thị 21–40 / 126 nhu cầu", `scrollTop`=0 | **ĐẠT** |
| 4 | Đổi số dòng/trang → 100 | `rowCount`=100, `.page-total`="Hiển thị 1–100 / 126 nhu cầu", trang active=1 | **ĐẠT** |
| 5 | Lọc trong popup (chọn "Trạng thái" = Đang theo dõi qua thao tác chuột thật trên select2) rồi Xoá lọc | Chọn lọc: bắn 1 request `demand-list`, `rowCount`=100, `.page-total`="Hiển thị 1–100 / 103 nhu cầu", banner hiện "· đang lọc trong 126 nhu cầu". Bấm nút "Xoá lọc" (icon refresh): bắn lại 1 request `demand-list`, `.page-total`="Hiển thị 1–100 / 126 nhu cầu", banner về nguyên bản (không còn hậu tố "đang lọc") | **ĐẠT** |
| 6 | Phóng to / thu nhỏ toàn màn hình | Trước: `.modal-dialog` 1400×844. Phóng to (nút title="Phóng to toàn màn hình"): 1440×900, nút đổi title="Thu nhỏ popup". Thu nhỏ lại: 1400×844 — khớp giá trị ban đầu | **ĐẠT** |
| 7 | Đóng rồi mở lại từ dòng cha khác ("Công nghiệp", 9 nhu cầu) | Sau khi đóng + mở lại: `rowCount`=9, `.page-total`="Hiển thị 1–9 / 9 nhu cầu", banner="Công nghiệp 9 nhu cầu · 36.209.120.000 đ...", kích thước modal 1400×844 (không còn ở trạng thái phóng to 1440×900 của lượt trước, không mang lại 126/103 dòng cũ) | **ĐẠT** |
| 8 | Bố cục: bảng không chạy xuyên hàng nút | `.report-drill-wrap.bottom`=709, `.modal-footer.top`=787 (chênh 78px, không chồng lấn); `getComputedStyle('.report-drill-wrap').borderTopWidth`="1px" | **ĐẠT** |

Console errors quan sát được trong phiên (menu-settings 400, HMR hot-update manifest timeout) không
liên quan tới `report-drill-wrap`/`DemandListModal`/`V2BaseReportModal` — là nhiễu nền của dev
server, không phải lỗi do đợt refactor gây ra. Không có bất thường nào cần sửa mã nguồn.

## Kết luận

- Phần A: vật cản môi trường đã biết được xác nhận lại, không đụng.
- Phần B: 29 test được liệt kê đúng; chạy thật đổ đúng điểm dự kiến (`beforeAll` thiếu tài khoản
  e2e), 28 "did not run" — không phải hồi quy.
- Phần C: 8/8 luồng nghiệp vụ chính của popup dùng `V2BaseReportModal` đo số thật trên DOM, tất cả
  ĐẠT. Không phát hiện lỗi hiển nhiên nào do đợt refactor gây ra, nên không có commit sửa mã nào.

Bộ e2e đầy đủ (29 ca) chưa thể tự động hoá chạy xanh trong môi trường hiện tại vì vật cản DB local;
đây là nợ kỹ thuật nằm ngoài phạm vi đợt tách component, người dùng đã biết và chủ động chọn không
xử lý trong đợt này.
