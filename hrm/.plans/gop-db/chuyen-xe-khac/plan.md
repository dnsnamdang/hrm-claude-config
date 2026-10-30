# Chuyến xe khác — Plan

> Spec: `docs/superpowers/specs/gop-db/2026-10-27-chuyen-xe-khac-design.md` · Tóm tắt: `design.md`.
> Nhánh: tách mới từ `develop` (cả hrm-api + hrm-client) sau khi commit đợt báo cáo vận chuyển.
> Skill: `erp-to-hrm-screen` (quy trình 6 bước + checklist), `list-page`, `form-validate`, `print-page`, `export-excel`.

## Phase 0 — Chuẩn bị
- [x] Khảo sát ERP (controller / model / blade / dữ liệu gop_db) — spec mục 2-7
- [x] User chốt 4 điểm (phạm vi, quyền BE, sửa lỗi ERP, trần cước 2 chiều)
- [x] Commit đợt báo cáo vận chuyển → nhánh `feat/chuyen-xe-khac` từ develop (28/10, cả 2 repo)
- [x] Đọc màn khuôn — BE bám `WarehouseInventoryImport` (entity can* + trait quyền, write service, thông báo, file, lịch sử); đặt trong **`Modules/Transport`** (module mới của phân hệ, khuôn màn Danh mục mẫu báo giá vận chuyển)
- [x] Rà HRM: có bảng giá / xe / entity đọc `Finance\Entities\Delivery\OtherDeliveryTrip` (Đề nghị TT — KHÔNG đụng, tạo entity ghi riêng); chưa có tìm PXK/PNK theo NV → viết mới. ⚠️ gop_db local KHÔNG có bảng giá hiệu lực (erp_dev_24_09 có 3 bảng hết hạn 2025)

## Phase 1 — BE (`hrm-api/Modules/Transport`)
- [x] Quyền: thêm bản api còn thiếu ở CUỐI seeder (Xem chuyến xe ×3, Duyệt chuyến xe khác, Hạch toán chuyến xe khác,
      Hạch toán vận chuyển) — `permission:sync --dry-run` trước
- [x] `OtherDeliveryTripService`: danh sách + phạm vi 3 `type` + lọc + sort + phân trang; chi tiết (trả `can_*` theo điều
      kiện nút); filter-options
- [x] Lookups: xe cho form (`Vehicle::getForSelect` ERP), thông tin xe (NCC, lái xe theo `driver_type`, công thức TP), dòng xe
      / tải trọng / cước tuyến / đơn giá vượt trội theo bảng giá hiệu lực, tuyến, nhân viên, tìm PXK/PNK theo nhân viên
- [x] `OtherDeliveryTripWriteService`: lưu 3 kiểu form (validate theo spec 6; tổng dòng = cước, dung sai 0,01; trần cước Q4;
      VAT; sinh `code` / `name`; xoá-tạo lại dòng con), sửa, xoá (+ dòng con)
- [x] Chuyển trạng thái: xuất phát (chặn xe đang chạy), kết thúc, duyệt, không duyệt (màn duyệt → 2), không duyệt của
      kế toán (→ 6) — BE chặn đúng điều kiện (403 / 409); thông báo 3 loại
- [x] File đính kèm (khuôn AttachmentSection), lịch sử thay đổi
- [x] In phiếu (blade riêng giữ bố cục 329 — mẫu 329 trong DB tự đặt sai biến, ERP còn dùng nên không sửa DB) + in danh sách riêng; Excel danh sách (`export-rows`); Excel 1 phiếu `GET /{id}/export` (29/10 — `OtherDeliveryTripExport` FromView + letterhead, cùng nguồn `detailPairs()` với bản in)
- [x] Controller + route `transport/other-delivery-trips`; PHPUnit `OtherDeliveryTripApiTest` 5/5 (85 assertion) (phạm vi, validate 3 kiểu, trần cước, chuyển trạng thái,
      chặn quyền, xoá dòng con)

## Phase 2 — FE (`hrm-client/pages/transport/other-delivery-trips`)
- [x] Danh sách (khuôn list-page: bộ lọc nổi, cấu hình cột, xuất Excel, in danh sách, hành động dòng theo `can_*`)
- [x] `OtherDeliveryTripForm.vue` dùng chung Thêm / Sửa / Chi tiết / Xuất phát / Kết thúc (3 kiểu, công thức, khối Chi tiết +
      popup chọn PXK/PNK `VoucherPickerModal`, validate realtime, trần cước báo đỏ)
- [x] Xuất Excel 1 phiếu: hành động dòng + nút ở màn chi tiết (29/10)
- [x] Bước xuất phát / kết thúc là 2 trang `_id/start`, `_id/finish`; Duyệt / Không duyệt / Hạch toán (mở ERP) ở màn chi tiết
- [x] Menu Vận chuyển › Chuyến xe › Chuyến xe khác + lối vào chờ duyệt / chờ hạch toán (gate `isShow` theo quyền api)

## Phase 3 — Nghiệm thu
- [ ] Đối chiếu ngược ERP (Bước 5) + ngang 2 màn khuôn (Bước 5b)
- [x] Playwright 1366px (28/10): DS, chi tiết, tạo kiểu Gửi hàng (2 dòng, chia cước, chọn phiếu), xuất phát → kết thúc →
      duyệt → chờ hạch toán, không duyệt (màn duyệt → Đang tạo; kế toán → Không duyệt) → sửa → xoá, In, lối vào `?type=waiting`.
      Trần cước tuyến cố định chỉ kiểm bằng state giả lập (DB local không có bảng giá hiệu lực)
- [ ] Test tuyến cố định / không có sẵn với bảng giá thật (dev server)
- [x] Cập nhật STATUS + memory

## Checkpoint — 2026-10-28
Vừa hoàn thành: Phase 0 + Phase 1 BE (Modules/Transport), test 5/5. Phát hiện thêm: cột `name` UNIQUE → 2 chuyến cùng xe trong 1 phút ERP lỗi; HRM thêm giây khi trùng.
Đang làm dở: — (Phase 2 FE xong 28/10, test tay local đạt).
Bước tiếp theo: user review + commit; test tuyến cố định trên dev có bảng giá; chụp ảnh nút Xuất Excel.
Blocked: test tay tuyến cố định cần bảng giá hiệu lực trên DB local.

## Ngày 28/10/2026 (@junfoke)
- [x] 28/10/2026 — Làm chuyển đổi erp->hrm: Chuyến xe khác - 100% code: BE `Modules/Transport` (6 quyền mới cuối seeder, PHPUnit 5/5) + FE danh sách, form chung 3 kiểu, xuất phát/kết thúc, duyệt/không duyệt, hạch toán mở ERP, in, Excel DS, lịch sử, menu. Playwright 1366px đạt. CHƯA commit.
- [x] 28/10/2026 — Nuxt dev chết vì tràn heap (mã 134) sau nhiều lần HMR khi test → khởi động lại, không do code.

## Ngày 29/10/2026 (@junfoke)
- [x] 29/10/2026 — Bổ sung Excel 1 phiếu (ERP `otherDeliveryTrip.export`): BE `GET /{id}/export` (ô số kiểu số + `#,##0`, letterhead, tên file kèm mã), FE "Xuất Excel" ở hành động dòng + màn chi tiết. PHPUnit 5/5 (90 assertion), gọi HTTP thật 200 / ngoài phạm vi 404. Chưa chụp ảnh FE (profile Playwright bị giữ).
- [x] 29/10/2026 — Commit màn (api `4fcd3b774`, client `015d86f34`) + merge develop; conflict `Modules/Transport/Routes/api.php` (develop thêm route Bảng giá hiệu lực / Tổng hợp giá đề xuất / HĐ vận chuyển) giữ cả hai, seeder quyền tự gộp (6 quyền vẫn ở cuối), test lại 5/5 → merge `8760e2250`, `8ef8d7842`. Đã lên origin/develop.
