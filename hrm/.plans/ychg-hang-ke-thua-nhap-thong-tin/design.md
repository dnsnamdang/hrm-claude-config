# Design: YCHG cho hàng kế thừa giá đang "Nhập thông tin"

- Ngày: 2026-11-05 · Bug: "Bán hàng_YC hỏi giá: Cho phép hàng hóa công ty con đang kế thừa giá được lập phiếu YC hỏi giá".
- Gốc: `.plans/gop-db/quan-ly-hang-hoa/ke-thua-gia-theo-hang/design.md` (§1 vòng đời hàng kế thừa, §4 tách YCHG sang công ty nguồn).
  Thay đổi này **nới §1 mục 3** (hàng kế thừa ở trạng thái 1 không được lập YCHG). Phần còn lại của design gốc giữ nguyên.

## 1. Hiện trạng
- `PriceAskingProductReader` trả `block_reason = 'Hàng kế thừa giá — dùng Chuyển kinh doanh (kế thừa giá).'` cho hàng kế thừa ở trạng thái 1 → popup lọc bỏ, Lưu/Gửi báo lỗi.
- Khi Gửi, `PriceAskingRequestWriter::splitInherited` tách dòng kế thừa sang YCHG mới của **công ty nguồn**. Hàng ở công ty nguồn đi từ 1 sang 2. Hàng ở **công ty con không đổi trạng thái**.
- Nguồn áp giá thì `InheritedPriceSync::propagate` chép giá sang công ty kế thừa, nhưng `PriceInheritance::inheritorsOf` mặc định chỉ lấy công ty con đang **3 Đang KD**. Nếu chỉ bỏ chặn, hàng của công ty con ở trạng thái 1 sẽ không bao giờ có giá.

## 2. Quyết định đã chốt (user, 05/11/2026)
1. Sau khi bỏ chặn, phiếu đi **luồng hỏi giá bình thường**: tách sang công ty nguồn, nguồn tính giá, rồi chép về công ty con. Công ty con không có giá riêng.
2. Phạm vi **chỉ màn YCHG** (popup chọn + Lưu/Gửi). Danh mục hàng hoá không đổi.
3. **Giữ nút "Chuyển kinh doanh (kế thừa giá)"** (đề xuất của Claude, user đồng ý). Nút là đường tắt khi nguồn đã có giá; YCHG dùng khi nguồn chưa có giá hoặc cần hỏi lại giá.
4. Popup chọn hàng **hiện mã công ty nguồn kế thừa** (`price_source_company_code`, BE đã trả).
5. Hàng của công ty con **tự lên Đang KD**: Gửi thì 1 → 2; nguồn áp giá xong thì chép giá và 2 → 3; nguồn từ chối hoặc huỷ thì về 1.

## 3. Hành vi mới
| Bước | Công ty nguồn (đã có) | Công ty con (mới) |
|---|---|---|
| Chọn hàng / Lưu nháp | — | Hàng kế thừa ở trạng thái 1 chọn được; popup hiện "Kế thừa giá từ <mã cty nguồn>" |
| Gửi | Phiếu tách, hàng 1 → 2 | Hàng 1 → **2 Chờ tính giá** (khoá khỏi YCHG khác, không chuyển KD được) |
| Nguồn áp giá, hàng ở nguồn ở trạng thái **3** | Giá áp, chép sang con | Con đang 2/5 thì **chép bộ giá + chuyển 3** |
| Nguồn từ chối (PTKD) / XNK báo không có giá / XNK huỷ / bỏ tick ở YCTG/PTG | Về 1 (đã có) | 2/5 → **1** |

Các chặn khác giữ nguyên: hàng đã xoá, hàng đang trong YCHG khác, nguồn ngừng KD (`MSG_SOURCE_STOPPED`), nhóm chưa có XNK ở nguồn.

## 4. Thiết kế kỹ thuật (Claude quyết, đánh dấu C)
- **(C) Bỏ chặn ở reader:** xoá nhánh `MSG_INHERITED_ENTERING` trong `PriceAskingProductReader` (hằng bỏ luôn). `ProductLifecycleService::MESSAGE_TRADE_INHERITED` (nút "Chuyển KD không tính giá") **không đụng**.
- **(C) Gửi:** trong `splitInherited`, thêm `moveProducts(ids, $origin->company_id, [1], 2, …, $child->code)`.
- **(C) Lên 3 ở công ty con:** thêm `InheritedPriceSync::settleWaiting(array $productIds, int $sourceCompanyId, ?int $by): int`.
  - Lấy công ty con kế thừa đang ở `PRICING_FLOW_STATUSES` (dùng `inheritorsOf(..., statuses)`).
  - Chỉ xử lý sản phẩm mà nguồn đang **3**: chép bộ giá mọi ĐVT (`copyBulk`), chuyển 2/5 → 3 qua `ProductHistoryService::trackStatus` (note "Kế thừa giá từ <mã cty>"), rồi `ProductPriceSetWriter::ensureProductSet`.
  - **Gọi ở 2 chỗ:**
    - cuối `propagate()`: nguồn đã 3 và vừa đổi giá;
    - sau khi nguồn chuyển 2/5 → 3: `PriceCalculateFinalizer::promoteProducts`, `ProductPriceApprovalService::markOwnerTrading`, và "Duyệt không cần tính giá" (`PriceAskingRequestWriter`, status 9 → 3).
  - Vì sao không mở rộng thẳng `propagate`: lúc `propagate` chạy theo từng ĐVT, nguồn có thể vẫn ở 2 (`promoteProducts` chạy sau). Đưa con lên 3 trước nguồn là sai.
- **(C) Trả về 1 ở công ty con:**
  - Thêm `PriceAskingRequest::originCompanyId(): ?int`: phiếu có `origin_request_id` thì trả `company_id` của phiếu gốc, không có thì `null`.
  - Thêm `InheritedPriceSync::releaseWaiting(array $productIds, int $companyId, ?int $by, string $note): int`: chuyển 2/5 → 1 qua `trackStatus`.
  - Gọi ở `ptkdReject`, `xnkNoPrice`/`xnkCancel` (khối dòng 855–866), và `PriceCalculateFinalizer::releaseUnchosen`. Finalizer tra phiếu YCHG qua `PriceCalculateRequest::price_asking_request_id`.
- **(C) FE popup** `PriceAskingProductPickerModal.vue`: dưới tên hàng thêm dòng chữ xám `Kế thừa giá từ <code>` khi có `price_source_company_code`, cùng kiểu dòng `asking-note`, màu xám `#6b7280`. Form YCHG đã có sẵn "Gửi công ty quản lý: <mã>" ở nhóm, không đổi.

## 5. Không làm
- Không đổi danh mục hàng hoá, nút "Chuyển kinh doanh (kế thừa giá)", nút "Chuyển KD không tính giá".
- Không đổi luồng hàng kế thừa đang 3, cách chọn nguồn, hệ số.
- Không backfill dữ liệu cũ.

## 6. Rủi ro / kiểm lại
- `settleWaiting` nằm ở hàm dùng chung (5 nơi gọi `propagate`). Chạy lại `InheritedPricePropagationTest`, `InheritedPriceSyncTest`, `PriceAskingSplitApiTest`, `ProductTradeInheritedApiTest`, `PriceAskingNoPriceApproveTest`.
- Ở công ty con, hàng kế thừa chỉ vào được 2/5 qua đường Gửi mới này (hàng kế thừa không tự tính giá ở con). Vì vậy `settleWaiting` không gặp hàng của luồng khác.
