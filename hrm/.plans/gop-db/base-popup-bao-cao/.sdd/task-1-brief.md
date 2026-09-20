### Task 1: Chụp ảnh hành vi hiện tại (baseline)

Đây là "bài test thất bại" của một đợt refactor: chưa có ảnh chụp thì không có gì chứng minh
"chuyển xong không đổi hành vi". Phải làm TRƯỚC khi đụng bất kỳ file nào.

**Files:**
- Create: `.plans/base-popup-bao-cao/measure-popup.mjs` (script đo, giữ lại để chạy cả 2 lượt)
- Create: `.plans/base-popup-bao-cao/baseline.json`

**Interfaces:**
- Produces: `baseline.json` với đúng khoá `{ cols, firstPageRowCount, sttFirst, sttLast, pageTotal, sortTextAsc, sortDateAsc, footerTop, tableBottom, heightNormal, heightFull }` — Task 6 so lại đúng bộ khoá này.

- [ ] **Step 1: Bật môi trường và xác nhận màn chạy được**

```bash
# API (nếu chưa chạy)
cd HRM/hrm-api && php artisan serve --host=127.0.0.1 --port=8000 &
# Nuxt (nếu chưa chạy) — Node 12 + heap 8192
cd HRM/hrm-client && PATH="$HOME/.nvm/versions/node/v12.22.12/bin:$PATH" NODE_OPTIONS=--max-old-space-size=8192 npm run dev &
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3000/   # phải là 200
```

- [ ] **Step 2: Chuẩn bị phiên đăng nhập cho script đo**

Tài khoản e2e `e2e_assign@test.local` KHÔNG có trong DB `hrm_erp`. Mint JWT thẳng cho một tài
khoản có quyền "…theo tổng công ty" — không đổi mật khẩu ai, không sửa dữ liệu:

```bash
cd HRM/hrm-api
php artisan tinker --execute '$e = \App\Models\TpEmployee::find(13); echo "TOKEN=" . auth("api")->login($e) . "\n";' \
  2>/dev/null | grep '^TOKEN=' | sed 's/^TOKEN=//' > /tmp/care-token.txt
python3 - <<'PY'
import json
tok = open('/tmp/care-token.txt').read().strip()
json.dump({"cookies": [], "origins": [{"origin": "http://127.0.0.1:3000",
          "localStorage": [{"name": "access_token", "value": tok}]}]}, open('/tmp/care-state.json', 'w'))
PY
```

- [ ] **Step 3: Viết script đo**

Tạo `.plans/base-popup-bao-cao/measure-popup.mjs`:

```js
import { chromium } from '/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e/node_modules/@playwright/test/index.mjs';

const OUT = process.argv[2];               // đường dẫn file json để ghi
const browser = await chromium.launch();
const page = await (await browser.newContext({
    storageState: '/tmp/care-state.json', viewport: { width: 1440, height: 900 },
})).newPage();
await page.goto('http://127.0.0.1:3000/assign/report/potential-customer-care', { waitUntil: 'domcontentloaded' });
await page.locator('.rsum-tb__sec').first().waitFor({ timeout: 40000 });

// Mở popup từ dòng cha đầu tiên
await page.locator('.rsum-tb__row--parent').first().locator('td').nth(2).locator('button.rsum-drill').click();
await page.waitForFunction(() => {
    const tr = document.querySelector('.modal.show table tbody tr');
    return tr && tr.querySelectorAll('td').length > 1;
}, { timeout: 20000 });

const snap = () => page.evaluate(() => {
    const m = document.querySelector('.modal.show');
    const t = (el) => (el ? el.innerText.replace(/\s+/g, ' ').trim() : null);
    const rows = [...m.querySelectorAll('table tbody tr')];
    const dialog = m.querySelector('.modal-dialog').getBoundingClientRect();
    const wrapSel = '.care-drill-wrap, .report-drill-wrap, .v2-table-scroll__body';
    const footSel = '.care-drill-footer, .report-drill-footer, .modal-footer';
    return {
        cols: [...m.querySelectorAll('table thead th')].map((th) => t(th)),
        firstPageRowCount: rows.length,
        sttFirst: t(rows[0]?.querySelector('td')),
        sttLast: t(rows[rows.length - 1]?.querySelector('td')),
        pageTotal: t(m.querySelector('.page-total')),
        tableBottom: Math.round(m.querySelector(wrapSel).getBoundingClientRect().bottom),
        footerTop: Math.round(m.querySelector(footSel).getBoundingClientRect().top),
        heightNormal: Math.round(dialog.height),
    };
});

const out = await snap();

// Sắp xếp: cột CHỮ đầu tiên và cột NGÀY đầu tiên -> lưu nguyên mảng giá trị sau khi bấm asc
const sortBy = async (label) => {
    const th = page.locator('.modal.show table thead th', { hasText: label }).first();
    if (!(await th.count())) return null;
    await th.locator('span').first().click();
    await page.waitForTimeout(400);
    const idx = (await page.locator('.modal.show table thead th').allInnerTexts())
        .findIndex((x) => x.trim().startsWith(label));
    return page.locator('.modal.show table tbody tr').evaluateAll(
        (trs, i) => trs.map((tr) => (tr.querySelectorAll('td')[i]?.textContent || '').replace(/\s+/g, ' ').trim()),
        idx,
    );
};
out.sortTextAsc = await sortBy('Khách hàng');
out.sortDateAsc = await sortBy('Ngày meeting');

// Phóng to toàn màn hình
await page.locator('.modal.show [title*="Phóng to"], .modal.show [title*="phóng to"]').first().click();
await page.waitForTimeout(500);
out.heightFull = await page.evaluate(() =>
    Math.round(document.querySelector('.modal.show .modal-dialog').getBoundingClientRect().height));

const fs = await import('fs');
fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));
await browser.close();
```

- [ ] **Step 4: Chạy và lưu baseline**

```bash
cd HRM
PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  node .plans/base-popup-bao-cao/measure-popup.mjs .plans/base-popup-bao-cao/baseline.json
```

Expected: in ra JSON có `cols` (mảng tên cột, ≥ 6 phần tử), `firstPageRowCount` = 20,
`pageTotal` dạng `Hiển thị 1–20 / N nhu cầu`, `heightFull` > `heightNormal`.

- [ ] **Step 5: Kiểm baseline không rỗng**

```bash
python3 -c "
import json; d = json.load(open('.plans/base-popup-bao-cao/baseline.json'))
assert d['cols'] and d['firstPageRowCount'] and d['pageTotal'], d
assert d['sortTextAsc'], 'thiếu ảnh chụp sắp xếp cột chữ'
assert d['heightFull'] > d['heightNormal'], 'nút phóng to không ăn'
print('baseline OK:', len(d['cols']), 'cột,', d['firstPageRowCount'], 'dòng')
"
```

- [ ] **Step 6: Commit** (chỉ khi người dùng đồng ý — nhánh dùng chung)

```bash
git add .plans/base-popup-bao-cao/measure-popup.mjs .plans/base-popup-bao-cao/baseline.json
git commit -m "chore(report-popup): chụp ảnh hành vi popup báo cáo trước khi tách Base"
```

---

