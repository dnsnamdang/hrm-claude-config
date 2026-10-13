### Task 7: Chạy lại toàn bộ bộ e2e của màn

**Files:** không sửa file nào — đây là cổng nghiệm thu.

- [ ] **Step 1: Kiểm không có phiên Playwright nào đang chạy**

```bash
ps aux | grep -c "[p]laywright test"
```

Expected: `0`. Khác 0 thì đợi — 2 phiên cùng chạy gây đỏ ngẫu nhiên.

- [ ] **Step 2: Chạy setup**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test --project=api-setup --workers=1 --retries=0 2>&1 | tail -5
```

Nếu đổ với `Table 'hrm_erp.hrm_employees' doesn't exist` → **vật cản môi trường đã biết**, KHÔNG
phải hồi quy của đợt này. Dừng, báo người dùng và chọn 1 trong 2: (a) sửa 5 tên bảng trong
`hrm-api/database/e2e_provision.php` (`hrm_employees`→`employees`, `hrm_roles`→`roles`,
`hrm_company_employees`→`company_employees`, `hrm_employee_has_roles`→`employee_has_roles`,
`hrm_role_has_permissions`→`role_has_permissions`); (b) bàn giao kèm ghi chú chưa chạy được e2e.

- [ ] **Step 3: Chạy toàn bộ bộ của màn**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test potential-customer-care --workers=1 2>&1 | tail -25
```

Expected: dòng tổng kết `29 passed`. ⚠️ Bộ chạy `serial` — một ca fail thì các ca sau in
"did not run", KHÔNG phải "passed". Phải đọc dòng tổng kết.

- [ ] **Step 4: Dọn file tạm**

```bash
rm -f /tmp/after.json /tmp/check-v2modal.mjs /tmp/care-token.txt /tmp/care-state.json
```

`measure-popup.mjs` và `baseline.json` **giữ lại** trong `.plans/` — đợt sau chuyển 2 popup còn lại
sẽ dùng đúng cách đo này.

- [ ] **Step 5: Cập nhật STATUS + checkpoint**

Ghi vào cuối `.plans/base-popup-bao-cao/plan.md`: vừa hoàn thành gì, còn dở gì, bước tiếp theo
(chuyển `DevelopmentDrillModal` và `ProjectListModal`), và blocked nếu có.

---

## Còn lại sau đợt này

- Chuyển `DevelopmentDrillModal` (19 chỗ selector `cmd-drill`) và `ProjectListModal` (15 chỗ
  `tkt-drill`) sang Base.
- Cân nhắc cho 15 popup bảng nhỏ dùng vỏ (không cần mixin).
