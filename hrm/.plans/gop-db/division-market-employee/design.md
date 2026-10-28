# Phiếu phân chia thị trường theo nhân viên — phân theo khu vực KD (#11695)

> @junfoke · nhánh `task_11695` (tách từ `task_11694`, cả 2 repo) · Redmine http://quanly.dnsmedia.vn/issues/11695
> Phụ thuộc: #11623 (Danh mục khu vực KD), #11694 (Phiếu phân chia theo phòng ban — là PHẠM VI của phiếu này)
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-16-division-market-employee-design.md`
> Demo: file HTML đính kèm task (CR-016 → CR-021), bản decode ở scratchpad — quy tắc chính chép vào spec.

## Mục tiêu

Port màn ERP "Phiếu phân chia thị trường theo nhân viên" (`Division/DivisionMarketEmployeeController`, AngularJS)
sang HRM, đổi cách chọn: **Tỉnh/TP → khu vực kinh doanh → hãng xe**, chỉ trong phạm vi đã chia cho phòng / bộ phận
(phiếu phòng ban #11694 Đã duyệt). **Mỗi phiếu giao cho 1 nhân viên.**

## Quyết định đã chốt (user 16/10/2026)

| # | Vấn đề | Chốt |
|---|---|---|
| 1 | Bảng | Dùng lại 5 bảng ERP `division_market_department_employees` (header) / `division_market_employees` / `_provinces` / `_wards` / `_province_vehicles`, chỉ THÊM cột + index. Mỗi phiếu đúng 1 dòng `division_market_employees` → báo giá ERP (`FirmQuotationService`), báo cáo HRM (`DivisionMarketReportService`), kế hoạch bán hàng đọc như cũ |
| 2 | 14 phiếu ERP cũ (1 phiếu / phòng, nhiều NV) | Migration **tách theo nhân viên**: NV đầu giữ id phiếu cũ, NV sau sinh phiếu mới (mã `{cty}_PCTTNV_{id}`), giữ Đã duyệt. Dòng NV không có Tỉnh/TP nào (13 dòng) bỏ |
| 3 | Luồng duyệt | Theo demo: Đang tạo → Gửi duyệt → Chờ duyệt → Duyệt → Đã duyệt; Chờ duyệt: Từ chối (bắt buộc lý do) / Thu hồi về Đang tạo; Đã duyệt: Hủy duyệt về Đang tạo. Chờ duyệt + Đã duyệt **khoá sửa/xoá** (BE 423) |
| 4 | Quyền | 5 quyền MỚI guard api như ERP: Tạo · Duyệt · Xem tổng công ty · Xem công ty · Xem phòng ban. Khai kiểu mới `$this->perm([...])` (skill `permission-seeder`) |
| 5 | Phiếu phòng ban đang làm phạm vi | Phòng/bộ phận còn phiếu nhân viên Chờ duyệt / Đã duyệt thì **chặn Hủy duyệt / Xoá** phiếu phòng ban, báo lý do |
| 6 | Nhánh | task_11694 đã merge `origin/gop_db` (16/10): sửa 4 quyền #11694 sang `$this->perm` (bản cũ khai `'id'`), `V2BaseSegmented` lấy bản của gop_db (skill `segmented-control`) |

## Quy tắc nghiệp vụ (từ demo)

- **Phạm vi của nhân viên** = hợp các phiếu phòng ban Đã duyệt của đơn vị: phòng chia theo cả phòng → mọi NV của phòng;
  phòng chia theo bộ phận → NV chọn trong phạm vi bộ phận mình; NV chưa thuộc bộ phận / bộ phận chưa được chia → không giao được (liệt kê kèm lý do).
- Thêm khu vực = nhận **trọn** phường/xã của khu vực **nằm trong phạm vi** (không chọn bớt; popup phường/xã chỉ xem).
- Hãng xe không bắt buộc. "Phụ trách tất cả các hãng" chỉ tick được khi mọi phường/xã của khu vực trong phạm vi đều "tất cả";
  hãng chọn được = giao các tập hãng của mọi phường/xã.
- Nhiều nhân viên được cùng khu vực, cùng hãng (không kiểm tra trùng). 1 nhân viên được nhiều phiếu.
- **SL nhân viên tối đa theo Tỉnh/TP** (từ phiếu phòng ban, nhỏ nhất nếu nhiều phiếu; trống/không giới hạn = bỏ qua):
  đếm NV khác của cùng đơn vị có phiếu Chờ duyệt / Đã duyệt ở tỉnh + phiếu này; vượt → chặn Lưu / Gửi / Duyệt.
  Dòng tỉnh hiện nhãn "SL nhân viên tối đa: L (đã giao K)".

## Phạm vi code

- BE `Modules/Finance`: migration (thêm cột/index + tách phiếu cũ), 5 entity `Entities/DivisionMarket/*Employee*`,
  `DivisionMarketEmployeeService`, controller + request + list resource, route `/division-market-employees`, blade in,
  5 quyền seeder, đăng ký `CatalogHistoryService` (+ nhãn `sent` / `recalled`) và `ExportColumnRegistry`; chặn ở phiếu phòng ban.
- FE `pages/finance/division-market-employees/` (danh sách, tạo, sửa, chi tiết) + form dùng chung khuôn #11694,
  popup Từ chối; menu `sale-hub.js` "Theo nhân viên".
