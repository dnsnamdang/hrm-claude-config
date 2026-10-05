### Task 8: Chụp ảnh hành vi 2 popup (baseline Phase 2)

**Files:**
- Modify: `.plans/gop-db/base-popup-bao-cao/measure-popup.mjs` — tham số hoá để đo được popup bất kỳ
- Create: `.plans/gop-db/base-popup-bao-cao/baseline-cmd.json`, `baseline-tkt.json`

- [ ] **Step 1:** Tham số hoá script: nhận thêm `--url`, `--open` (selector mở popup), `--sort-text`, `--sort-date` (nhãn cột), `--item-label`. Giữ nguyên toàn bộ phép đo cũ.
- [ ] **Step 2:** Bổ sung 3 phép đo MỚI vào script (Phase 1 thiếu, phải trả giá): `getComputedStyle` của vùng cuộn bảng (`border-top-width`, `border-radius`), `overflow` của `.modal-content`, và khoảng cách ngang giữa 2 nút footer.
- [ ] **Step 3:** Chạy cho `customer-market-development` → `baseline-cmd.json`; popup mở từ ô số đầu tiên của bảng.
- [ ] **Step 4:** Chạy cho `prospective-project-results` → `baseline-tkt.json`.
- [ ] **Step 5:** Kiểm cả 2 file có đủ khoá, `sortTextAsc`/`sortDateAsc` KHÔNG rỗng (rỗng = bấm nhầm cột không sortable), in ra số cột + số dòng trang 1.

