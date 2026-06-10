# Trạng thái Features

> Cập nhật khi: tạo feature mới, wrap up, chuyển feature, hoặc merge xong.
> Không xóa entry trong "Hoàn thành".
> Cập nhật lần cuối: 2026-06-10 (chuyển 2 feature HĐ "Không thực hiện" sang Hoàn thành)

## Đang làm

_(chưa có)_

## Tạm dừng

_(chưa có)_

## Hoàn thành (3 entry gần nhất)
- **Duyệt HĐ "Không thực hiện" → Hủy hợp đồng** — TP bấm Duyệt HĐ có `result=2` → HĐ chuyển trạng thái mới "Hủy hợp đồng" (Contract `HUY=5`) + đẩy dự toán/báo giá/gói thầu sang trạng thái mới "Hủy hợp đồng" (const mới mỗi entity) + ghi lịch sử kèm lý do. Tái dùng nút Duyệt, không snapshot. (@khoipv) — 2026-06-10, verify UI PASS
  - Spec: `docs/superpowers/specs/2026-06-10-contract-cancel-not-executed-on-approve-design.md`
  - Plan: `.plans/contract-cancel-not-executed-on-approve/plan.md`

- **Bỏ validate khi hợp đồng "Không thực hiện"** — Khi tạo/sửa HĐ (từ gói thầu/báo giá) chọn `result = 2` (Không thực hiện) → bỏ TẤT CẢ validate, chỉ bắt buộc `reason`. Áp dụng FE + BE, tạo mới + cập nhật. `result = 1`/trống → validate đầy đủ như cũ. (@khoipv) — 2026-06-10, verify UI PASS
  - Spec: `docs/superpowers/specs/2026-06-10-contract-not-executed-skip-validate-design.md`
  - Plan: `.plans/contract-not-executed-skip-validate/plan.md`

- **Ghi chú + Lưu-sau-duyệt tab Điều khoản thanh toán** — Thêm 1 ô ghi chú chung cho tab Điều khoản thanh toán (cột `payment_terms_note` trên `contracts`) + nút Lưu mở khóa & lưu cả bảng + ghi chú khi HĐ đã duyệt (endpoint mới `updatePaymentTermsAfterApprove`, tái dùng `syncPaymentTerms`). Chỉ form `contract/contract`. (@khoipv) — 2026-06-10, verify UI PASS
  - Spec: `docs/superpowers/specs/2026-06-09-contract-payment-terms-note-approve-design.md`
  - Plan: `.plans/contract-payment-terms-note-approve/plan.md`

- **Bắt buộc field khi gửi duyệt gói thầu lên TP** — Bắt buộc `bid_opening_time`, `bid_closing_time`, `execution_time` (numeric>0), `execution_time_unit` khi nhân viên bấm "Gửi duyệt" (status=3) trong `StoreBidPackageRequest`. Lưu nháp/Lưu và gửi vẫn để trống được. (@khoipv) — 2026-06-08
  - Spec: `docs/superpowers/specs/2026-06-08-bid-package-send-approve-required-fields-design.md`
  - Plan: `.plans/bid-package-send-approve-required-fields/plan.md`

- **Đồng bộ thông tin hợp đồng gốc xuống phụ lục** — Sửa số HĐ / ngày ký / ngày kết thúc / thời gian thực hiện ở hợp đồng gốc (màn 203, sau duyệt) → đồng bộ 4 trường vào TẤT CẢ snapshot `ContractVersion` để mọi phụ lục hiển thị giá trị mới. BE sửa `updateDataAfterApprove` (bọc transaction); FE gửi thêm `time_progress`. (@khoipv) — 2026-06-08
  - Spec: `docs/superpowers/specs/2026-06-08-dong-bo-thong-tin-hop-dong-xuong-phu-luc-design.md`
  - Plan: `.plans/dong-bo-thong-tin-hop-dong-xuong-phu-luc/plan.md`

- **Tab "Phụ lục liên quan" — Chi tiết hợp đồng** — Điền tab rỗng trong màn chi tiết/sửa HĐ bằng bảng phụ lục (STT, Mã PL, Loại PL, Trạng thái); mã PL click → chi tiết đúng loại, trạng thái badge màu. BE: thêm `annexes` + `annex_type_label` vào `ContractDetailResource`. (@khoipv) — 2026-06-03
  - Spec: `docs/superpowers/specs/2026-06-03-contract-detail-related-annex-tab-design.md`
  - Plan: `.plans/contract-detail-related-annex-tab/plan.md`

- **Cột "Phụ lục liên quan" — Danh sách hợp đồng** — Thêm cột hiển thị mọi mã phụ lục của hợp đồng (mỗi mã 1 dòng, mọi trạng thái), click → chi tiết phụ lục đúng loại qua `ANNEX_TYPE_ROUTE_MAP`. BE: relation `Contract::annexes` + eager load + expose ở `ContractResource`. (@khoipv) — 2026-06-03
  - Spec: `docs/superpowers/specs/2026-06-02-contract-list-related-annex-column-design.md`
  - Plan: `.plans/contract-related-annex-column/plan.md`

- **Popup DT gom hàng hóa 4 phân hệ + quy đổi ĐVT** — Enhancement cho report-project-contract: popup chi tiết DT hiển thị tất cả HH từ DT/BG/Thầu/HĐ, thêm 3 cột SL quy đổi về ĐVT chính (@khoipv) — 2026-05-29
  - Spec: `docs/superpowers/specs/2026-05-29-lifecycle-detail-aggregate-products-design.md`
  - Plan: `.plans/report-project-contract/plan.md`

- **Sửa BCCT báo giá — mỗi báo giá 1 dòng** — Đổi plan/detail-report từ mỗi hàng hóa 1 dòng sang mỗi báo giá 1 dòng + popup chi tiết sản phẩm (@khoipv) — 2026-05-29
  - Spec: `docs/superpowers/specs/2026-05-28-detail-report-quotation-summary-design.md`
  - Plan: `.plans/detail-report-quotation-summary/plan.md`

- **Báo cáo chi tiết hợp đồng** — Báo cáo tổng hợp sản phẩm từ nhiều hợp đồng (27 cột, 8 filters, phân quyền 3 cấp, export Excel) (@khoipv) — 2026-05-29
  - Spec: `docs/superpowers/specs/2026-05-06-detail-report-contract-design.md`
  - Plan: `.plans/detail-report-contract/plan.md`

- **Tab Dữ liệu liên quan trên báo giá** — Thay tab input thủ công bằng tab read-only tự động lấy chứng từ liên quan (Dự toán/Thầu/Hợp đồng) qua endpoint BE mới `GET /quotations/{id}/related-data` + component `QuotationRelatedDataComponent.vue` (@khoipv) — 2026-05-25
  - Spec: `docs/superpowers/specs/2026-05-25-quotation-related-data-design.md`
  - Plan: `.plans/quotation-related-data/plan.md`

- **BC Tổng hợp Vòng đời DT → HĐ** — Báo cáo tổng hợp 1 dòng/DT, grouped headers 4 giai đoạn (DT/BG/GT/HĐ), KPI cards, popup drill-down, export Excel, phân quyền 3 cấp dùng lại bộ "Xem báo cáo chi tiết dự toán theo ..." (ID 504-506) (@khoipv) — 2026-05-27
  - Spec: `docs/superpowers/specs/2026-05-25-report-project-contract-design.md`
  - Plan: `.plans/report-project-contract/plan.md`

- **Tab Thuế TNCN lưu cả bảng 1 lần** — Thay pattern edit per-row bằng 1 nút Lưu chung dưới bảng trong tab Thuế TNCN của màn employee_info/edit, BE thêm endpoint bulk (@manhcuong) — 2026-05-26
  - Spec: `docs/superpowers/specs/2026-05-26-employee-tax-bulk-save-design.md`
  - Plan: `.plans/employee-tax-bulk-save/plan.md`

- **Tính Thuế TNCN trong bảng lương** — Áp biểu lũy tiến 7 bậc + đa-đoạn tax_type theo khoảng ngày + 3 cột giảm trừ INFO trên bảng lương. Config global (1 row dùng chung mọi company). Quy ước nội bộ KHÁC TT 111: (1) BHXH giảm trừ = NLĐ+NSDLĐ (32%) thay vì chỉ NLĐ; (2) đoạn 10%/20% dùng `probation_salary` (@manhcuong) — 2026-05-13, Phase 1-10 xong + verified, chờ E2E qua UI bảng lương thật
  - Spec: `docs/superpowers/specs/2026-05-13-personal-income-tax-design.md`
  - Plan: `.plans/personal-income-tax/plan.md`

- **Tab Dữ liệu liên quan trên dự toán** — Hiển thị chứng từ nghiệp vụ liên quan (Kế hoạch/Thầu/Hợp đồng) với mã chứng từ (link) + người thực hiện, endpoint BE mới + implement FE component (@khoipv) — 2026-05-25
  - Spec: `docs/superpowers/specs/2026-05-25-project-related-data-design.md`
  - Plan: `.plans/project-related-data/plan.md`

- **Mẫu in riêng cho hợp đồng lao động** — Mỗi HĐLĐ lưu bản mẫu in riêng (longText) thay vì FK dùng chung. FE 2 tab + CKEditor. Migration backfill data cũ. (@khoipv) — 2026-05-23
  - Spec: `docs/superpowers/specs/2026-05-22-employment-contract-print-template-design.md`
  - Plan: `.plans/employment-contract-print-template/plan.md`

- **Bộ lọc ngân hàng thực hiện** — Thêm filter "Ngân hàng thực hiện" vào danh sách hợp đồng, lọc qua `whereHas('guarantees')` theo `bank_guarantee_id` (@khoipv) — 2026-05-22
  - Spec: `docs/superpowers/specs/2026-05-22-contract-bank-guarantee-filter-design.md`
  - Plan: `.plans/contract-bank-guarantee-filter/plan.md`

- **Bộ lọc kết quả thầu** — Thêm filter "Kết quả thầu" (Trúng/Trượt/Chưa có) vào màn danh sách gói thầu, lọc theo trường `result` trong bảng `bid_packages` (@khoipv) — 2026-05-22
  - Spec: `docs/superpowers/specs/2026-05-22-bid-package-result-filter-design.md`
  - Plan: `.plans/bid-package-result-filter/plan.md`

- **Thêm cột Sale phụ trách vào danh sách khách hàng** — Hiển thị tên Sale (dept 83) + mảng hàng hoá phụ trách từ tab Phân công phụ trách, eager load trong query list (@khoipv) — 2026-05-22
  - Spec: `docs/superpowers/specs/2026-05-22-sale-person-charge-column-design.md`
  - Plan: `.plans/sale-person-charge-column/plan.md`

- **Danh sách phụ lục chờ duyệt** — Trang gộp 6 loại phụ lục HĐ chờ duyệt vào 1 danh sách (API gộp BE + trang FE approve.vue) (@khoipv) — 2026-05-21
  - Spec: `docs/superpowers/specs/2026-05-21-contract-annex-approve-list-design.md`
  - Plan: `.plans/contract-annex-approve/plan.md`

- **Mở rộng mối quan hệ gia đình** — Thêm Ông, Bà, Khác (text tự do) vào dropdown mối quan hệ trong Thông tin gia đình, áp dụng 4 màn employee_info (@khoipv) — 2026-05-21
  - Spec: `docs/superpowers/specs/2026-05-21-family-relation-extend-design.md`
  - Plan: `.plans/family-relation-extend/plan.md`

- **Đính kèm file cho người thân** — Bổ sung chức năng upload/xóa file đính kèm (tối đa 5 file) cho từng thành viên gia đình trong Thông tin nhân sự, hỗ trợ cả flow yêu cầu cập nhật (@khoipv) — 2026-05-20
  - Spec: `docs/superpowers/specs/2026-05-20-family-attachment-design.md`
  - Plan: `.plans/family-attachment/plan.md`

- **Từ chối phân công dự toán** — Thêm chức năng từ chối phân công trên màn dự toán, nhập lý do, chuyển status = 17 (Hủy dự toán), trạng thái cuối cùng (@khoipv) — 2026-05-20
  - Spec: `docs/superpowers/specs/2026-05-20-reject-assignment-design.md`
  - Plan: `.plans/reject-assignment/plan.md`

- **Thêm cột KH sử dụng cuối cùng vào BCCT báo giá** — Thêm cột `customer_last_used_name` vào màn plan/detail-report (web + Excel) (@khoipv) — 2026-05-19
  - Spec: `docs/superpowers/specs/2026-05-19-detail-report-customer-last-used-design.md`
  - Plan: `.plans/detail-report-customer-last-used/plan.md`

- **Hạn mức công nợ theo từng KH** — Chuyển hạn mức công nợ từ nhóm KH xuống từng khách hàng, xóa 2 cột khỏi customer_groups, thêm vào category_customers, dọn FE/BE (@khoipv) — 2026-05-19
  - Spec: `docs/superpowers/specs/2026-05-19-customer-credit-limit-design.md`
  - Plan: `.plans/customer-group-credit-limit/plan.md`

- **Điều khoản thanh toán trên hợp đồng** — Thêm bảng điều khoản thanh toán (4 loại: 100% trước giao, giới hạn thời gian, giới hạn giá trị, gối đầu đơn hàng) vào tab "Cài đặt công nợ thanh toán" trong form HĐ (section 3 mock cảnh báo công nợ) (@khoipv) — 2026-05-19
  - Spec: `docs/superpowers/specs/2026-05-18-contract-payment-terms-design.md`
  - Plan: `.plans/contract-payment-terms/plan.md`

- **Phiếu xác định & quy tắc xử lý vi phạm công nợ** — Cấu hình loại phiếu được tính là công nợ + hành động khi điều khoản bị vi phạm (mục 4 của mock cảnh báo công nợ) (@khoipv) — 2026-05-19
  - Spec: `docs/superpowers/specs/2026-05-18-debt-violation-rules-design.md`
  - Plan: `.plans/debt-violation-rules/plan.md`

- **Hạn mức công nợ nhóm KH** — ~~Thêm 2 trường vào nhóm KH~~ → Đã thay thế bởi "Hạn mức công nợ theo từng KH" (2026-05-19) — chuyển hạn mức xuống cấp từng khách hàng (@khoipv) — 2026-05-18
  - Spec cũ: `docs/superpowers/specs/2026-05-18-customer-group-credit-limit-design.md`
  - Spec mới: `docs/superpowers/specs/2026-05-19-customer-credit-limit-design.md`

- **Giá bán HĐ trước** — Populate cột Giá bán HĐ trước bằng đơn giá bán từ HĐ gần nhất cùng KH, fallback cùng tỉnh. Áp dụng cho báo giá, gói thầu, hợp đồng. (@khoipv) — 2026-05-13
  - Plan: `.plans/previous-contract-price/plan.md`

- **Fix quy đổi giá khi thay đổi đơn vị tính** — Sửa lỗi giá không quy đổi theo conversion_factor khi đổi đơn vị ở gói thầu + hợp đồng + phân quyền bảng hàng hóa theo can_handle (@khoipv) — 2026-05-12
  - Plan: `.plans/fix-unit-price-conversion/plan.md`

- **Phụ lục thay đổi số lượng — 2 kiểu bảng** — Hỗ trợ chọn Kiểu A (SL sau đ/c) hoặc Kiểu B (SL điều chỉnh) cho mỗi phụ lục, áp dụng form + bản in (@khoipv) — 2026-05-09
  - Spec: `docs/superpowers/specs/2026-05-08-annex-quantity-table-type-design.md`
  - Plan: `.plans/annex-quantity-table-type/plan.md`

- **Thêm hàng hóa vào phụ lục thay đổi số lượng** — Cho phép thêm sản phẩm mới từ danh mục hệ thống vào phụ lục thay đổi số lượng, tạo nhóm mới/chọn nhóm cũ, nhân bản (@khoipv) — 2026-05-08
  - Spec: `docs/superpowers/specs/2026-05-08-annex-quantity-add-product-design.md`
  - Plan: `.plans/annex-quantity-add-product/plan.md`

- **Danh mục kho** — FE + BE hoàn chỉnh: menu, danh sách, modal CRUD cho Kho Vật Lý + Kho Kế Toán, 4 migrations, full API (@namdangit) — 2026-05-13
  - Spec: `docs/superpowers/specs/2026-05-13-danh-muc-kho-design.md`
  - Plan: `.plans/danh-muc-kho/plan.md`

- **Báo cáo chi tiết thầu** — Báo cáo chi tiết gói thầu (27 cột, 9 filters, phân quyền 3 cấp, export Excel, link HĐ) (@khoipv) — 2026-05-06
  - Spec: `docs/superpowers/specs/2026-05-06-detail-report-bid-package-design.md`
  - Plan: `.plans/detail-report-bid-package/plan.md`

- **Báo cáo chi tiết báo giá** — Trang báo cáo tổng hợp sản phẩm từ nhiều báo giá + export ExcelJS + phân quyền 3 cấp (@khoipv) — 2026-05-06
  - Spec: `docs/superpowers/specs/2026-05-05-detail-report-quotation-design.md`
  - Plan: `.plans/detail-report-quotation/plan.md`

- **Quotation Flow for Contract Types** — Sửa flow dự toán loại Cho/Tặng, Đặt/Mượn, Nguyên tắc để đi qua báo giá trước khi sang hợp đồng (@khoipv) — 2026-04-25
  - Spec: `docs/superpowers/specs/2026-04-24-quotation-flow-for-contract-types-design.md`
  - Plan: `.plans/quotation-flow-for-contract-types/plan.md`

- **Editable Price Cost** — Cho phép sửa cột Giá vốn trong bảng sản phẩm báo giá (@khoipv) — 2026-04-23
  - Spec: `docs/superpowers/specs/2026-04-23-editable-price-cost-design.md`
  - Plan: `.plans/editable-price-cost/plan.md`
