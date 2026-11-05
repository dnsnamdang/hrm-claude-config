# YCHG cho hàng kế thừa giá đang "Nhập thông tin" — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** công ty con lập và gửi được YCHG cho hàng kế thừa ở trạng thái 1. Hỏi giá xong thì hàng tự có giá và lên 3; bị từ chối hoặc huỷ thì về 1.

**Architecture:** bỏ nhánh chặn ở `PriceAskingProductReader`. Khi Gửi, chuyển hàng ở công ty con 1 → 2. Thêm `InheritedPriceSync::settleWaiting` (chép giá + 2/5 → 3 khi nguồn đang 3) và `releaseWaiting` (2/5 → 1), gọi ở các điểm nguồn lên 3 / về 1. FE: popup chọn hàng hiện mã công ty nguồn.

**Tech Stack:** Laravel 8 (PHP 7.4) `hrm-api/Modules/MasterData`, Nuxt 2 `hrm-client`.

**Spec:** `HRM/.plans/ychg-hang-ke-thua-nhap-thong-tin/design.md`

## Global Constraints
- Worktree riêng từ `origin/develop` (repo chính đang có thay đổi của session khác): `HRM/.worktrees/hrm-api-ychgkt` + `HRM/.worktrees/hrm-client-ychgkt`, nhánh `fix/ychg-hang-ke-thua-nhap-thong-tin`.
- Không commit/push/merge `develop` khi user chưa bảo. Không chạy full `permission:sync`. Không ghi DB prod.
- Test chạy bằng `vendor/bin/phpunit <file>` (không dùng `php artisan test --filter` cho Modules).
- Đổi trạng thái hàng × công ty luôn qua `ProductHistoryService::trackStatus` (để có lịch sử), lên 3 thì kèm `ProductPriceSetWriter::ensureProductSet`.
- Không đụng `ProductLifecycleService::MESSAGE_TRADE_INHERITED` và nút "Chuyển kinh doanh (kế thừa giá)".
- FE: chữ phụ màu xám `#6b7280`, không dùng `.text-muted` (trong project ra màu đỏ).

## Review Focus
1. Hàng nhiều ĐVT: con chỉ lên 3 khi nguồn đã 3. Nếu `propagate` chạy theo từng ĐVT lúc nguồn còn 2 thì con phải vẫn ở 2. Test ở T2.
2. Nguồn đã 3 từ trước (hỏi lại giá): áp giá ĐVT đầu tiên là con lên 3 với đủ bộ giá. Test ở T2.
3. Phiếu gốc lẫn hàng tự tính + hàng kế thừa: hàng tự tính của con vẫn đi luồng thường. `releaseWaiting` chỉ chạy với phiếu tách (có `origin_request_id`), không đụng hàng phiếu thường. Test ở T3.
4. Một công ty con kế thừa sản phẩm từ 2 nguồn khác nhau: mỗi phiếu tách trả đúng công ty gốc. Đã có test 2 nguồn ở `PriceAskingSplitApiTest`; chạy lại.
5. Hàng ở con đang 2 không bị "Chuyển kinh doanh (kế thừa giá)" kéo lên 3 (`tradableInheritedAt` chỉ nhận 1). Test ở T1.

---

### Task 1: Bỏ chặn + Gửi chuyển hàng của công ty con 1 → 2

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/PriceCalculation/PriceAskingProductReader.php` (hằng dòng 28, nhánh dòng ~214–218)
- Modify: `hrm-api/Modules/MasterData/Services/PriceCalculation/PriceAskingRequestWriter.php` (`splitInherited`, sau dòng 353)
- Test: `hrm-api/Modules/MasterData/Tests/Feature/PriceAskingSplitApiTest.php`, `.../ProductTradeInheritedApiTest.php`

- [ ] **Step 1: Sửa/viết test trước**
  - `ProductTradeInheritedApiTest::ychg_khong_chon_duoc_hang_ke_thua_dang_nhap_thong_tin` đổi tên thành `ychg_chon_duoc_hang_ke_thua_dang_nhap_thong_tin`: `assertNull($row['block_reason'])`, vẫn `assertSame(self::A, $row['price_source_company_id'])`.
  - `PriceAskingSplitApiTest`, test mới `gui_hang_ke_thua_dang_nhap_thong_tin_o_cong_ty_con_sang_cho_tinh_gia`:
    - Hàng kế thừa, con ở trạng thái 1, nguồn ở trạng thái 1 hoặc 3. Gửi thì phiếu tách được tạo, `pcc(con).status = 2`, `pcc(nguồn).status` như luồng cũ (1 → 2, còn 3 thì giữ).
    - Bấm `POST /products/trade-inherited` với hàng đó thì không chuyển (Review Focus 5).
  - Test `luu_nhap_khong_tach`: Lưu nháp vẫn để con ở trạng thái 1.
- [ ] **Step 2:** chạy 2 file test, các test mới phải FAIL.
- [ ] **Step 3:** reader bỏ hằng `MSG_INHERITED_ENTERING` và nhánh ternary, `block_reason` = `'Hàng hoá đã bị xoá'` hoặc `self::blockReason(...)`. Trong `splitInherited` thêm `$this->moveProducts(array_keys($rows), (int) $origin->company_id, [ProductCompany::STATUS_ENTERING_INFO], ProductCompany::STATUS_WAITING_PRICE, $me, $child->code);`.
- [ ] **Step 4:** chạy lại 2 file, PASS.
- [ ] **Step 5:** commit `fix(ychg): cho lập YCHG hàng kế thừa đang nhập thông tin`.

### Task 2: `settleWaiting` — con lên 3 khi nguồn đã có giá

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/ProductPrice/InheritedPriceSync.php`
- Modify (gọi): `PriceCalculation/PriceCalculateFinalizer.php::promoteProducts`, `ProductPrice/ProductPriceApprovalService.php::markOwnerTrading`, `PriceCalculation/PriceAskingRequestWriter.php` (khối "Duyệt không cần tính giá" ~dòng 765–772)
- Test: `hrm-api/Modules/MasterData/Tests/Feature/InheritedPricePropagationTest.php`

**Interfaces:**
- Produces: `InheritedPriceSync::settleWaiting(array $productIds, int $sourceCompanyId, ?int $by): int` trả số dòng (sản phẩm × công ty) đã chuyển 3.

- [ ] **Step 1: Test** trong `InheritedPricePropagationTest`:
  - `con_cho_tinh_gia_len_dang_kd_khi_nguon_dang_kd`: con ở 2, nguồn ở 3, gọi `propagate` → con có đủ 6 cột giá ×k (làm tròn 1,000 như `copy`) và `status = 3`.
  - `con_cho_tinh_gia_giu_nguyen_khi_nguon_con_cho_tinh_gia`: nguồn ở 2, `propagate` → con vẫn 2, chưa có giá. Sau đó đưa nguồn lên 3 rồi gọi `settleWaiting` → con lên 3.
  - `con_dang_nhap_thong_tin_khong_bi_dong`: con ở 1, nguồn ở 3, `propagate` → con vẫn 1.
- [ ] **Step 2:** chạy file test, FAIL.
- [ ] **Step 3:** cài `settleWaiting`:
  - `inheritorsOf($ids, $source, ProductCompany::PRICING_FLOW_STATUSES)`.
  - Lọc sản phẩm mà nguồn có `pcc.status = 3`, rồi `copyBulk` (mọi `product_units` của sản phẩm).
  - Chuyển 2/5 → 3 bằng `trackStatus` (note `self::note($source)`), rồi `ensureProductSet`.
  - Gọi `settleWaiting` ở cuối `propagate` (với các product id vừa xử lý) và ở 3 điểm nguồn lên 3, ngay sau `ensureProductSet` của nguồn.
- [ ] **Step 4:** chạy `InheritedPricePropagationTest`, `InheritedPriceSyncTest`, `PriceAskingNoPriceApproveTest`, PASS.
- [ ] **Step 5:** commit `feat(ke-thua-gia): hàng kế thừa chờ tính giá lên đang KD khi nguồn có giá`.

### Task 3: `releaseWaiting` — nguồn từ chối/huỷ thì con về 1

**Files:**
- Modify: `hrm-api/Modules/MasterData/Entities/PriceCalculation/PriceAskingRequest.php` (thêm `originCompanyId()`)
- Modify: `InheritedPriceSync.php` (thêm `releaseWaiting`)
- Modify (gọi): `PriceAskingRequestWriter::ptkdReject` (sau dòng 797), khối XNK không giá/huỷ (sau dòng 865), `PriceCalculateFinalizer::releaseUnchosen`
- Test: `PriceAskingSplitApiTest.php`

**Interfaces:**
- Produces: `PriceAskingRequest::originCompanyId(): ?int`; `InheritedPriceSync::releaseWaiting(array $productIds, int $companyId, ?int $by, string $note): int`.

- [ ] **Step 1: Test** trong `PriceAskingSplitApiTest`, mỗi test Gửi trước cho con lên 2:
  - `ptkd_nguon_tu_choi_phieu_tach_tra_hang_con_ve_nhap_thong_tin`
  - `xnk_nguon_bao_khong_co_gia_tra_hang_con_ve_nhap_thong_tin`
  - `ptkd_tu_choi_phieu_thuong_khong_dung_cong_ty_khac`: phiếu không tách thì `originCompanyId() === null`, không gọi release (Review Focus 3).
- [ ] **Step 2:** FAIL.
- [ ] **Step 3:** cài 2 hàm, gọi ở 3 điểm. Note `'Yêu cầu hỏi giá ' . $request->code`. Finalizer tra `PriceAskingRequest::find($request->price_asking_request_id)`.
- [ ] **Step 4:** chạy `PriceAskingSplitApiTest`, `PriceAskingRequestApiTest`, PASS.
- [ ] **Step 5:** commit `feat(ychg): phiếu tách bị từ chối/huỷ trả hàng công ty con về nhập thông tin`.

### Task 4: FE popup hiện mã công ty nguồn + kiểm trình duyệt

**Files:**
- Modify: `hrm-client/components/sale/price-asking/PriceAskingProductPickerModal.vue` (slot `#cell-name` dòng 40–45 + style)

- [x] **Step 1:** thêm dưới tên hàng: `<div v-if="item.price_source_company_code" class="inherit-note"><i class="ri-git-branch-line"></i> Kế thừa giá từ {{ item.price_source_company_code }}</div>`. Style `.inherit-note` bám `.asking-note` nhưng màu `#6b7280`.
- [x] **Step 2:** chạy API + client từ worktree (cổng riêng, không tắt :3000/:8000). Dùng Playwright MCP, đăng nhập user công ty con:
  - Tạo YCHG → popup thấy hàng kế thừa trạng thái 1 kèm dòng "Kế thừa giá từ …".
  - Chọn hàng → Lưu và gửi duyệt → về danh sách. Phiếu tách xuất hiện, hàng ở con thành "Chờ tính giá".
  - Chụp ảnh popup.
- [x] **Step 3:** chạy lại toàn bộ 7 file test liên quan (mục 6 design), ghi kết quả vào Checkpoint.
- [x] **Step 4:** commit `feat(ychg): popup chọn hàng hiện công ty nguồn kế thừa`.

## Checkpoint
- 05/11/2026 — T1–T4 xong. API commits bfc285d28 · 88f2e4b62 · 69903336f (nhánh `fix/ychg-hang-ke-thua-nhap-thong-tin`, worktree `hrm-api-ychgkt`); FE commit 988cc0606 (worktree `hrm-client-ychgkt`).
- Test: PriceAskingRequestApi 11/11 · InheritedPricePropagation 15/15 · InheritedPriceSync 9/9 · PriceAskingNoPriceApprove 23/23 · PriceCalculateApi 19/19 · PriceCalculateRequestApi 11/11 · ProductPriceApprovalApi 28/28 · PriceAskingSplitApi 13/13 → 129/129 pass.
- Trình duyệt (API :8100 + client :3100, DNS Admin cty 1): popup hiện HAECO-TUDIEN "Đang nhập thông tin" + "Kế thừa giá từ TPHP"; Lưu và gửi duyệt → về danh sách, sinh phiếu gốc (cty 1, status 11) + phiếu tách (cty 2, origin_request_id = gốc), dòng hàng cty con 1→2, có lịch sử "Yêu cầu hỏi giá <mã phiếu tách>". Dữ liệu tạm (mpi, assign_histories, pcc, 2 phiếu) đã trả lại.
- Lưu ý dữ liệu: gửi bị chặn hợp lệ nếu công ty nguồn chưa phân công XNK cho thương hiệu × hãng (`assign_histories`) — không phải lỗi.
