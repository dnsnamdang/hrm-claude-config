# Chuẩn hoá Master Data 4 danh mục (Redmine #11303)

Phụ trách: @cuong61n · Nhánh: `tpe` (worktree `HRM/worktrees/tpe-api` + `tpe-client`)
Nguồn dữ liệu: `danh_sach_nhom_giai_phap_v2.1.xlsx` (Drive id `1rNjtoXWc9IKiHBfNe2DxJ3uyMyQQD05N`)

## Mục tiêu

Chuẩn hoá 4 danh mục của phân hệ Dự án theo file dữ liệu khách gửi: đổi tiền tố mã Lĩnh vực
Công ty kinh doanh, gán lại quan hệ cha–con 3 tầng (Lĩnh vực → Nhóm ngành → Nhóm giải pháp →
Ứng dụng), thêm mới và khoá một số bản ghi.

| Màn | Bảng | Mã |
|---|---|---|
| Lĩnh vực Công ty kinh doanh (`/assign/internal-business-scopes`) | `internal_business_scopes` | `LVKDNB.` → `LVCTKD.` |
| Nhóm ngành (`/assign/industry-groups`) | `scopes` | `NN.xxxx` |
| Nhóm giải pháp (`/assign/solution-groups`) | `industries` | `NGP.xxxx` |
| Ứng dụng (`/assign/application`) | `applications` + `application_scopes` + `application_industries` | `UD.xxxx` |

`application_industries` lưu CẶP (`scope_id`, `industry_id`) — chính là cột "Map Nhóm ngành –
Nhóm giải pháp" trong file. `application_scopes` là tập nhóm ngành phẳng của ứng dụng.

## Khối lượng thay đổi (đã đối chiếu với DB `hrm_prod_local`)

- Lĩnh vực: 7 bản ghi đổi mã (`LVKDNB.000x` → `LVCTKD.000y`, KHÔNG phải map 1-1 theo số).
- Nhóm ngành: 22 bản ghi cũ gán lại lĩnh vực · 13 bản ghi thêm mới (NN.0023–NN.0035) · 1 khoá (NN.0012).
- Nhóm giải pháp: 61 bản ghi remap nhóm ngành · 1 khoá (NGP.0167 "Gara 2s-3s").
- Ứng dụng: 145 bản ghi dựng lại 2 pivot; 2 bản ghi đổi tên.

Kiểm chứng độ tin cậy của file: cột "Map hiện tại" của sheet `ung_dung` khớp `application_industries`
trong DB ở **143/145** ứng dụng (2 dòng lệch do local thiếu NGP.4000/NGP.4001) ⇒ file dùng làm nguồn chuẩn được.

## Quyết định đã chốt (2026-09-04)

0. **Bước 6 phát sinh — đồng bộ `scope_id` bảng nghiệp vụ.** 3 bảng `prospective_projects`,
   `request_solutions`, `solutions` lưu Nhóm ngành TRỰC TIẾP. Sau khi remap ở bước 3, số dòng có
   `scope_id` không còn là cha của `industry_id` tăng **13 → 258**. Chốt: chỉ sửa **245 dòng do
   seeder gây ra**, nhận diện bằng ánh xạ `scope_remap` (mã cũ → mã mới lấy từ 2 cột của file);
   **13 dòng lệch sẵn từ trước giữ nguyên** + in cảnh báo.

1. **Đẩy dữ liệu bằng Seeder chạy tay**, không dùng migration — để chủ động thời điểm chạy trên từng môi trường.
2. **Đổi cả 2 chỗ nằm ngoài mô tả task** (file dữ liệu có, AC không nhắc):
   - Lĩnh vực `LVCTKD.0007`: đổi tên `Ngành ô tô` → `Dịch vụ ô tô`.
   - Ứng dụng `UD.0142` → `Đào tạo kiểm định xe công trình`, `UD.0141` → `Đào tạo kiểm định ô tô`.
3. **Giữ nguyên bản ghi `LVKDNB.KHAC`** ("Khác", do migration backfill cũ tạo) — không đổi mã, chấp nhận
   1 bản ghi lệch định dạng so với tiền tố mới.
4. Tập **nhóm ngành của ứng dụng lấy từ cột "Map … Mã (Cập nhật)"** chứ không lấy cột G "Mã nhóm ngành mới":
   cột G thiếu mã ở 3 dòng (UD.0129, UD.0132, UD.0133) và có dấu phẩy thừa ở UD.0132.
5. Sheet lĩnh vực **bỏ trống `LVCTKD.0003`** (nhảy 0002 → 0004) — làm đúng theo file, không tự chèn.
6. Môi trường kiểm thử: DB `hrm_prod_local`.

## Kiểm thử

Bộ kiểm thử tự động: `runtests.py` (cùng thư mục) — **53/53 PASS** trên DB `hrm_prod_6_6`.
Phủ AC1–AC7, toàn vẹn khoá ngoại, audit `created_by`/`updated_by`, bất biến của bộ danh mục cũ,
tính tất định (khôi phục gốc → chạy lại → khớp 100%) và idempotent (lần 2 ra 0 dòng).

Env kiểm thử: API `:8005` (PHP 7.4) + FE `:3005` (Node 14.21.3), worktree
`HRM/worktrees/tpe-api` + `HRM/worktrees/tpe-client`.

## 2 cái bẫy đã trả giá khi làm task này

1. **Các cột "(Cập nhật)" trong file CHỈ điền cho phần dòng có thay đổi, không phải toàn bộ.**
   Sheet `ung_dung`: cột "Map … Mã (Cập nhật)" chỉ có **19/145** dòng. Sheet `nhom_giai_phap`:
   cột "Mã nhóm ngành mới" chỉ có **87/401** dòng. Lần đầu tôi đọc thẳng cột "(Cập nhật)" →
   **126 ứng dụng bị xoá trắng nhóm ngành** (`application_scopes` 233 → 46 dòng), chỉ lộ ra khi
   đối chiếu số dòng trước/sau. Quy tắc đúng: **lấy cột cập nhật, TRỐNG thì lấy cột hiện tại.**
   Kiểm nhanh: tổng số cặp sau khi dựng phải bằng 779 = đúng số dòng `application_industries`.

2. **DB `hrm_prod_6_6` còn tồn một bộ danh mục CŨ trùng mã** — 19 `scopes` + 117 `industries`
   tạo 2026-04, tách biệt hoàn toàn (`scopes` id>22 ↔ `industries` id>401, 118 dòng pivot riêng,
   không ứng dụng nào dùng). Tra bản ghi theo **mã đơn** sẽ đụng nhầm bộ này (vd `NGP.0013` có 2
   bản ghi: "Dịch vụ đào tạo" đang dùng và "Giải pháp trạm sạc" cũ). Phải tra theo **cặp
   (code, name)**, và bước 4 dùng lại map id đã phân giải ở bước 2/3 vì bước 4 chỉ có mã.

## Rủi ro / lưu ý

- Đổi mã lĩnh vực an toàn: các bảng con tham chiếu qua `internal_business_scope_id`, không snapshot mã.
- Khoá NN.0012 chỉ hợp lệ SAU khi 61 nhóm giải pháp đã remap sang nhóm ngành mới — seeder phải chạy đúng thứ tự.
- Dữ liệu lịch sử (Dự án, Báo giá, BOM) trỏ qua khoá ngoại nên không đổi (AC 7).
- Danh mục đã khoá vẫn phải hiện ở bản ghi đang dùng nó — đã kiểm thật: form Dự án TKT / Yêu cầu
  giải pháp lấy option qua `training/master-select/all?table=scopes`, endpoint này KHÔNG lọc trạng
  thái nên tên vẫn hiện bình thường. (`assign/scopes/getAll` CÓ lọc `status = ACTIVE` và thiếu
  `include_ids`, nhưng 2/3 nơi gọi nó truyền vào prop `sectorOptions` mà `TktTab.vue` khai rồi
  không render, nơi thứ 3 là modal Sửa Nhóm giải pháp — sau seeder không còn nhóm giải pháp nào
  trỏ vào nhóm ngành đã khoá nên không ảnh hưởng. **Đã cân nhắc và quyết định KHÔNG sửa endpoint
  dùng chung này.**)
- NN.0012 (đã khoá) vẫn gắn lĩnh vực **"Khác"**: file ghi lĩnh vực `Thiết bị kiểm định - sửa chữa
  bảo dưỡng ô tô` cho dòng này, giá trị đó không tồn tại trong danh mục Lĩnh vực → seeder giữ
  nguyên lĩnh vực đang có thay vì đoán. Cần khách xác nhận nếu muốn gán lĩnh vực cụ thể.

Spec chi tiết: `docs/superpowers/specs/2026-09-04-masterdata-pl8-chuan-hoa-danh-muc-design.md`
