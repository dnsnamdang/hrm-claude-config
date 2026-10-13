# Plan — Báo cáo theo dõi giữ hàng

> Mockup ĐÃ DUYỆT 02/10/2026, đã chốt đủ 7 vướng mắc, ĐÃ LẬP PLAN CODE (Phase 1-4 bên dưới). Bước tiếp: chọn cách thực thi rồi bắt đầu Task 1.
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md`

## Phase 0 — Mockup & chốt yêu cầu

- [x] Rà hiện trạng màn `/finance/prepick-stocks` (FE 899 dòng, BE `PrepickStockReportService`)
- [x] Chốt 5 quyết định thiết kế (xem `design.md`)
- [x] Dựng mockup HTML theo ngôn ngữ thiết kế báo cáo TKT
- [x] Kiểm chứng mockup bằng Playwright (đo DOM: tổng khớp cấp con, không tràn ngang, màu header)
- [x] Bổ sung vòng 2: ngưỡng cảnh báo cấu hình được · cột Tồn hiện tại + SL đang giữ · cột Số lần gia hạn + popup lịch sử · bỏ Tỷ trọng quá hạn · đổi "Hạn giữ" → "Hạn giữ hiện tại"
- [x] Kiểm dữ liệu BE cho "Số lần gia hạn" trên DB thật (phát hiện gia hạn TÁCH LÔ — phải đếm theo nhóm giữ)
- [x] Bổ sung vòng 3: cột chính đo kép (số mã / số lượng) · bộ cột hàng hoá bám ERP (bỏ Kho) · gỡ Số lần gia hạn khỏi bảng, đưa vào popup theo từng lô
- [x] Bổ sung vòng 4: tô màu ô Hạn giữ hiện tại theo ngưỡng cảnh báo · cột ĐVT riêng + bỏ hậu tố đơn vị ở ô số · popup luôn giữ 2 cột Mã/Tên hàng · mã hàng đứng trước tên · tiêu đề popup dạng "Mã - Tên"
- [x] Bổ sung vòng 5: "Số lượng giữ" · mã hàng gộp lại vào ô tên với style riêng · sort 4 cột · nhân viên kèm phòng ban · cột Số hợp đồng + Tổng thanh toán + popup phiếu thu · chốt thứ tự mặc định toàn báo cáo
- [x] Bổ sung vòng 6: bỏ cột Tồn ở popup + ở tiêu chí Nhân viên · thêm bộ lọc Hình thức giữ · sửa định nghĩa đo: theo DÒNG (1 mã → số lượng, nhiều mã → số mã) thay vì theo cấp
- [x] Bổ sung vòng 7: bỏ đổi đơn vị (luôn ĐVT cơ bản) · khối tổng hợp 1 đếm theo YÊU CẦU GIỮ · sort thêm 3 cột popup
- [x] Bổ sung vòng 8: bỏ đổi nền khi hover tiêu đề cột sort · thêm ô "NV có hàng giữ quá hạn" vào khối hạn giữ
- [x] Bổ sung vòng 9: bỏ thuật ngữ "lô" khỏi giao diện (đụng `warehouse_import_lots` có thật) · sửa mô hình dữ liệu demo để 1 yêu cầu giữ gồm nhiều dòng đúng tỉ lệ thật
- [x] Đổi vị trí 2 khối tổng hợp: Phạm vi đang giữ → Tình trạng theo yêu cầu giữ
- [x] Cột "Nhân viên giữ" trong popup chỉ hiện tên (đã có cột Phòng ban riêng)
- [x] Lối tắt "Hàng giữ của tôi" (ép tiêu chí NV + công ty/phòng/nhân viên của mình + bung tới hàng hoá; tắt thì khôi phục bộ lọc cũ)
- [x] Chốt định nghĩa "Số yêu cầu giữ" = Phiếu + Mã hàng + Nhân viên (thật: 2.412 dòng / 2.410 yêu cầu / 593 phiếu); đổi cột popup thành "Phiếu giữ gốc"
- [x] Chốt ràng buộc BE: lần ngược chuỗi gia hạn về chứng từ gốc trước khi đếm (tránh đếm chồng + tránh sai "Phiếu giữ gốc" ở 46% dòng); mockup thêm ca gia hạn một phần để chứng minh
- [x] Chốt phân quyền: 1 quyền duy nhất "Xem báo cáo giữ hàng theo tổng công ty" (quyền này CHƯA tồn tại, phải thêm seeder); mockup demo 2 trạng thái qua `?noPerm=1`
- [x] Chốt: KHÔNG gate vào màn (không dùng quyền `Quản lý giữ hàng`); không giới hạn phòng ban — không có quyền thì vẫn xem cả công ty mình
- [x] Viết spec chi tiết `docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md`
- [x] Bổ sung phân trang vào mockup: bảng chính theo node cấp 1 (mặc định 25), popup theo dòng (mặc định 20); dòng TỔNG không theo trang; sort/lọc reset về trang 1
- [x] Bổ sung vòng 10: lọc **Bộ phận** (cascade sau Phòng ban, 3 trạng thái, mục "Chưa phân bộ phận") · popup đưa 3 cột Ngày bắt đầu giữ / Hạn giữ hiện tại / Số lần gia hạn lên ngay sau "SL đang giữ" · **ghim 3 cột đầu popup** khi cuộn ngang · **In / Xuất Excel** thật (4 đường, đều lấy toàn bộ theo bộ lọc)
- [x] Bổ sung vòng 11: 2 nút **Gia hạn** / **Huỷ giữ** (icon + chữ) nằm TRONG ô "Hạn giữ hiện tại", chỉ hiện ở chế độ "Hàng giữ của tôi" — không tách cột riêng
- [x] Rà toàn bộ nút theo `button-convention` — phát hiện & sửa 5 lỗi ở nút cũ (chữ bị cấm, quá 3 từ, thứ tự footer, thiếu icon, sai màu nhóm Xuất)
- [x] **User duyệt mockup** (02/10/2026)
- [x] Chốt 7 vướng mắc trước khi code (02/10/2026) — xem bảng cuối `design.md`
- [x] Lên plan code (02/10/2026) — Phase 1 nền dữ liệu · Phase 2 BE · Phase 3 FE · Phase 4 kiểm chứng, 17 task

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Màn báo cáo MỚI `/sale/prepick-tracking` (phân hệ Bán hàng › Báo cáo › nhóm "Hàng giữ") theo mockup đã duyệt, chạy song song với màn cũ `/finance/prepick-stocks`; kèm cột chứng từ gốc `root_objectable_*` trên `prepick_details` được ghi ở cả HRM và ERP.

**Architecture:** BE nạp TẤT CẢ dòng hàng giữ còn tồn (`qty > 0`) theo bộ lọc SQL bằng 1 truy vấn (quy mô thật ~2.400 dòng — bảng 61.771 dòng nhưng chỉ dòng còn tồn mới vào báo cáo, có index `company_id, qty`), rồi tính trạng thái / đo / dựng cây / lọc popup bằng các lớp PHP THUẦN (test được không cần DB) — port 1-1 từ hàm `metrics()` / `buildTree()` / `drillLots()` của mockup. Chứng từ gốc đọc thẳng từ cột `root_objectable_*` (không CTE). FE port giao diện mockup lên các khung dùng chung của báo cáo TKT (`V2BaseSmartFilterPanel`, `V2BaseReportModal`, `V2BaseTableScroll`, `reportPrintPreviewMixin`).

**Tech Stack:** Laravel (PHP 7.4, nwidart modules) · MySQL 8 · maatwebsite/excel `FromView` · Nuxt 2 / Vue 2 · Playwright.

**Spec:** `docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md` + bảng **"Chốt vướng mắc trước khi code (02/10/2026)"** cuối `design.md` (ĐÈ lên spec ở: URL/menu, màn cũ giữ song song, chứng từ gốc = cột lưu sẵn) · Mockup: `bao-cao-theo-doi-giu-hang.html`.

## Global Constraints

- Nhánh `gop_db-bao-cao-theo-doi-giu-hang`, tách từ `gop_db` ở **cả 3 repo**: `hrm-api`, `hrm-client`, ERP `TanPhatDev` (từ `origin/gop_db`). Làm trong worktree `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-giu-hang/{hrm-api,hrm-client,erp}` — KHÔNG checkout đè thư mục chính, KHÔNG `git stash`.
- Worktree hrm-api: **copy** vendor (`cp -Rc`), KHÔNG symlink (autoload trỏ về checkout chính, sửa BE vô tác dụng im lặng).
- PHP: `/opt/homebrew/opt/php@7.4/bin/php`. Test Module phải truyền đường dẫn: `php vendor/bin/phpunit Modules/Finance/Tests/...`. Test DB chạy trên MySQL thật `hrm_erp` → feature test dùng `DatabaseTransactions`.
- Client Nuxt: node 12 + `NODE_OPTIONS=--max-old-space-size=8192`. Kill server theo PID của cổng, KHÔNG `pkill -f`.
- **Màn cũ `/finance/prepick-stocks` + `/finance/prepick-expiring` KHÔNG đổi hành vi.** Không sửa route/endpoint/controller của 2 màn đó.
- API mới dưới prefix **`/api/v1/finance/prepick-tracking`** — TOÀN BỘ CHỈ ĐỌC. Không dùng `mysql2` / `DB_CONNECTION_SECOND`.
- Quyền duy nhất: **`Xem báo cáo giữ hàng theo tổng công ty`** (id **1632**, guard `api`, type **23** = Bán hàng, group `Báo cáo giữ hàng`). KHÔNG gate vào màn; không quyền → BE tự ép công ty theo hồ sơ (`auth()->user()->info->company_id`), KHÔNG đọc `company_id` FE gửi. KHÔNG có ngoại lệ super admin — chỉ xét permission được gán (user chốt 03/10/2026).
- Id người đăng nhập: `auth()->id()` (= `employees.id`), KHÔNG `auth()->user()->info->id`.
- Trạng thái hạn (N = ô "Cảnh báo trước", mặc định `configs.warning_day`): `exp` nếu hạn < hôm nay · `soon` nếu 0 ≤ (hạn − hôm nay) ≤ N · `ok` còn lại. `expire_date` NULL → `ok`. Ngày tính bằng `CURDATE()`.
- Khoá **yêu cầu giữ** = `root_type|root_id|product_id|employee_id` — dùng CHUNG ở tổng hợp, cây và popup.
- Đo theo DÒNG: dòng gom đúng 1 mã → số lượng; nhiều mã → số mã (`only_product_id`).
- Số: `,` nghìn `.` thập phân (FE `toLocaleString('en-US')`); ngày `dd/mm/yyyy`. Excel: số thô + `data-format` (skill `export-excel`). Ghi chú phụ dùng xám `#6b7280`, KHÔNG `.text-muted`.
- KHÔNG dùng chữ "lô" trên giao diện.
- FE: cờ quyền **fail-closed** (khởi tạo `false`, chỉ bật từ `$store.state.permissions`). Nút "Xoá lọc" KHÔNG reset `company_id`.
- Không tự chạy bộ e2e mỗi task (chỉ chạy khi user yêu cầu); vẫn viết spec + vẫn kiểm bằng Playwright MCP, đo bằng số từ DOM.

---

## Phase 1 — Nền dữ liệu: cột chứng từ gốc

### Task 1: Dựng worktree 3 repo

**Files:** không có file code.

- [x] **Step 1: Tạo nhánh + worktree**

```bash
W=/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-giu-hang
R=/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM
git -C $R/HRM/hrm-api worktree add -b gop_db-bao-cao-theo-doi-giu-hang $W/hrm-api gop_db
git -C $R/HRM/hrm-client worktree add -b gop_db-bao-cao-theo-doi-giu-hang $W/hrm-client gop_db
git -C $R/ERP/TanPhatDev fetch origin gop_db
git -C $R/ERP/TanPhatDev worktree add -b gop_db-bao-cao-theo-doi-giu-hang $W/erp origin/gop_db
cp -Rc $R/HRM/hrm-api/vendor $W/hrm-api/vendor
cp $R/HRM/hrm-api/.env $W/hrm-api/.env
cp -Rc $R/HRM/hrm-client/node_modules $W/hrm-client/node_modules
cp $R/HRM/hrm-client/.env $W/hrm-client/.env 2>/dev/null || true
```

- [x] **Step 2: Kiểm autoload trỏ đúng worktree**

```bash
cd $W/hrm-api && /opt/homebrew/opt/php@7.4/bin/php -r 'require "vendor/autoload.php"; echo (new ReflectionClass("Modules\\Finance\\Services\\PrepickStockService"))->getFileName(), PHP_EOL;'
```
Expected: đường dẫn chứa `wt-giu-hang/hrm-api`. Ra `ERP-HRM/HRM/hrm-api` = dính bug symlink → xoá vendor, copy lại.

- [x] **Step 3: Xoá config cache (tránh trỏ nhầm DB production)**

```bash
cd $W/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan config:clear
```

---

### Task 2: Migration cột `root_objectable_*` + bộ giải chứng từ gốc + lệnh backfill

**Files:**
- Create: `hrm-api/database/migrations/2026_10_02_000001_add_root_objectable_to_prepick_details.php`
- Create: `hrm-api/Modules/Finance/Services/PrepickTracking/PrepickRootResolver.php`
- Create: `hrm-api/app/Console/Commands/BackfillPrepickRootCommand.php`
- Modify: `hrm-api/Modules/Finance/Entities/PrepickCancel/PrepickDetail.php`
- Test: `hrm-api/Modules/Finance/Tests/Unit/PrepickRootResolverTest.php`

**Interfaces:**
- Produces: `PrepickRootResolver::resolve(array $rows, array $extendSource): array` — `$rows`: `id => ['objectable_id'=>int|null,'objectable_type'=>string|null]`; `$extendSource`: `prepick_extend_request_details.id => prepick_detail_id`; trả `id => ['root_id'=>int|null,'root_type'=>string|null]`.
- Produces: `PrepickDetail::rootPair(): array` → `[int|null $id, string|null $type]`.
- Produces: hằng `PrepickRootResolver::EXTEND_TYPE = 'App\\Model\\Warehouse\\PrepickExtendRequestDetail'`.

- [x] **Step 1: Viết test resolver (thất bại)**

```php
<?php

namespace Modules\Finance\Tests\Unit;

use Modules\Finance\Services\PrepickTracking\PrepickRootResolver;
use PHPUnit\Framework\TestCase;

class PrepickRootResolverTest extends TestCase
{
    const WPR = 'App\\Model\\Warehouse\\WarehousePrepickRequest';
    const EXT = PrepickRootResolver::EXTEND_TYPE;

    public function test_row_not_created_by_extension_is_its_own_root(): void
    {
        $out = PrepickRootResolver::resolve([10 => ['objectable_id' => 5, 'objectable_type' => self::WPR]], []);
        $this->assertSame(['root_id' => 5, 'root_type' => self::WPR], $out[10]);
    }

    public function test_extension_chain_walks_back_to_origin(): void
    {
        // 10 = phiếu xuất giữ gốc; 11 sinh từ gia hạn dòng 10 (ext detail 100); 12 sinh từ gia hạn dòng 11 (ext detail 101)
        $rows = [
            10 => ['objectable_id' => 5, 'objectable_type' => self::WPR],
            11 => ['objectable_id' => 100, 'objectable_type' => self::EXT],
            12 => ['objectable_id' => 101, 'objectable_type' => self::EXT],
        ];
        $out = PrepickRootResolver::resolve($rows, [100 => 10, 101 => 11]);
        $this->assertSame(['root_id' => 5, 'root_type' => self::WPR], $out[11]);
        $this->assertSame(['root_id' => 5, 'root_type' => self::WPR], $out[12]);
    }

    public function test_broken_chain_falls_back_to_own_objectable(): void
    {
        // ext detail 200 trỏ tới dòng 99 không có trong tập -> không lần được, giữ chính nó
        $out = PrepickRootResolver::resolve([11 => ['objectable_id' => 200, 'objectable_type' => self::EXT]], [200 => 99]);
        $this->assertSame(['root_id' => 200, 'root_type' => self::EXT], $out[11]);
    }

    public function test_cycle_does_not_loop_forever(): void
    {
        $rows = [
            1 => ['objectable_id' => 300, 'objectable_type' => self::EXT],
            2 => ['objectable_id' => 301, 'objectable_type' => self::EXT],
        ];
        $out = PrepickRootResolver::resolve($rows, [300 => 2, 301 => 1]);
        $this->assertSame(['root_id' => 300, 'root_type' => self::EXT], $out[1]);
    }

    public function test_null_objectable_stays_null(): void
    {
        $out = PrepickRootResolver::resolve([7 => ['objectable_id' => null, 'objectable_type' => null]], []);
        $this->assertSame(['root_id' => null, 'root_type' => null], $out[7]);
    }
}
```

- [x] **Step 2: Chạy test, phải FAIL**

Run: `cd $W/hrm-api && /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/Finance/Tests/Unit/PrepickRootResolverTest.php`
Expected: FAIL — `Class "...PrepickRootResolver" not found`.

- [x] **Step 3: Viết resolver**

```php
<?php

namespace Modules\Finance\Services\PrepickTracking;

/**
 * Lần ngược chuỗi GIA HẠN của `prepick_details` về CHỨNG TỪ GỐC (thuần PHP, không DB).
 *
 * Gia hạn không sửa `expire_date` mà TRỪ dòng cũ, CỘNG sang dòng MỚI có
 * `objectable_type = PrepickExtendRequestDetail` -> `objectable` của dòng đó là phiếu GIA HẠN,
 * không phải phiếu giữ gốc (46% dòng còn tồn trên DB thật). Gốc = đi
 * ext detail -> `prepick_detail_id` (dòng nguồn) -> lặp tới khi gặp dòng không do gia hạn sinh ra.
 *
 * Chuỗi đứt (dòng nguồn không còn trong tập) hoặc vòng lặp -> giữ `objectable` của chính dòng.
 */
final class PrepickRootResolver
{
    const EXTEND_TYPE = 'App\\Model\\Warehouse\\PrepickExtendRequestDetail';

    /** Chuỗi thật dài nhất đo được là 10 bước — trần 64 chỉ để chặn dữ liệu hỏng. */
    const MAX_DEPTH = 64;

    /**
     * @param array<int, array{objectable_id:int|null, objectable_type:string|null}> $rows
     * @param array<int, int> $extendSource prepick_extend_request_details.id => prepick_detail_id nguồn
     * @return array<int, array{root_id:int|null, root_type:string|null}>
     */
    public static function resolve(array $rows, array $extendSource): array
    {
        $out = [];
        foreach ($rows as $id => $row) {
            $out[$id] = self::walk((int) $id, $rows, $extendSource);
        }

        return $out;
    }

    private static function walk(int $id, array $rows, array $extendSource): array
    {
        $own = self::pair($rows[$id]);
        $currentId = $id;
        $seen = [];

        for ($depth = 0; $depth < self::MAX_DEPTH; $depth++) {
            $row = $rows[$currentId];
            if (($row['objectable_type'] ?? null) !== self::EXTEND_TYPE) {
                return self::pair($row);
            }
            $seen[$currentId] = true;
            $sourceId = $extendSource[(int) $row['objectable_id']] ?? null;
            if ($sourceId === null || !isset($rows[$sourceId]) || isset($seen[$sourceId])) {
                return $own;
            }
            $currentId = (int) $sourceId;
        }

        return $own;
    }

    private static function pair(array $row): array
    {
        return [
            'root_id' => isset($row['objectable_id']) ? (int) $row['objectable_id'] : null,
            'root_type' => $row['objectable_type'] ?? null,
        ];
    }
}
```

- [x] **Step 4: Chạy test, phải PASS**

Run: như Step 2. Expected: `OK (5 tests, ...)`.

- [x] **Step 5: Migration**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Báo cáo theo dõi giữ hàng — lưu sẵn CHỨNG TỪ GỐC của từng dòng hàng giữ (user chốt
 * 02/10/2026: không lần ngược bằng CTE mỗi lần chạy vì dữ liệu tích luỹ lâu sẽ nặng).
 * Bảng DÙNG CHUNG với ERP: cả 3 chỗ tạo dòng của HRM (`PrepickStockService`) và 5 chỗ của ERP
 * đều phải ghi 2 cột này. Dữ liệu cũ lấp bằng `php artisan prepick:backfill-root`.
 *
 * Kèm index `company_id, qty`: báo cáo luôn lọc `qty > 0` theo công ty, bảng không có index
 * nào ngoài employee_id / customer_id.
 */
class AddRootObjectableToPrepickDetails extends Migration
{
    public function up()
    {
        if (!Schema::hasTable('prepick_details')) {
            return;
        }
        Schema::table('prepick_details', function (Blueprint $table) {
            if (!Schema::hasColumn('prepick_details', 'root_objectable_id')) {
                $table->unsignedBigInteger('root_objectable_id')->nullable();
            }
            if (!Schema::hasColumn('prepick_details', 'root_objectable_type')) {
                $table->string('root_objectable_type', 191)->nullable();
            }
        });
        Schema::table('prepick_details', function (Blueprint $table) {
            $table->index(['root_objectable_type', 'root_objectable_id'], 'pd_root_objectable_idx');
            $table->index(['company_id', 'qty'], 'pd_company_qty_idx');
        });
    }

    public function down()
    {
        if (!Schema::hasTable('prepick_details')) {
            return;
        }
        Schema::table('prepick_details', function (Blueprint $table) {
            $table->dropIndex('pd_root_objectable_idx');
            $table->dropIndex('pd_company_qty_idx');
        });
        Schema::table('prepick_details', function (Blueprint $table) {
            foreach (['root_objectable_id', 'root_objectable_type'] as $col) {
                if (Schema::hasColumn('prepick_details', $col)) {
                    $table->dropColumn($col);
                }
            }
        });
    }
}
```

- [x] **Step 6: Model — fillable + `rootPair()`**

Trong `Modules/Finance/Entities/PrepickCancel/PrepickDetail.php`: thêm `'root_objectable_id', 'root_objectable_type',` vào cuối `$fillable`, sửa docblock "KHÔNG đổi schema, KHÔNG migration" thành ghi chú về 2 cột mới, và thêm:

```php
    /**
     * Chứng từ gốc của dòng này để dòng MỚI kế thừa (gia hạn). Dòng cũ chưa backfill thì lấy
     * `objectable` của chính nó.
     *
     * @return array{0:int|null, 1:string|null}
     */
    public function rootPair(): array
    {
        if ($this->root_objectable_type) {
            return [(int) $this->root_objectable_id, $this->root_objectable_type];
        }

        return [$this->objectable_id !== null ? (int) $this->objectable_id : null, $this->objectable_type];
    }
```

- [x] **Step 7: Lệnh backfill**

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Modules\Finance\Services\PrepickTracking\PrepickRootResolver;

/**
 * Lấp `prepick_details.root_objectable_*` cho dữ liệu cũ. Chạy lại bao nhiêu lần cũng được
 * (idempotent). Mặc định CHỈ ghi dòng đang NULL; `--all` tính lại toàn bộ.
 * Toàn bảng ~62k dòng -> nạp hết vào bộ nhớ (2 cột số + 1 chuỗi), ghi theo lô 500.
 */
class BackfillPrepickRootCommand extends Command
{
    protected $signature = 'prepick:backfill-root {--all : Tính lại cả dòng đã có root} {--dry-run}';

    protected $description = 'Lấp cột chứng từ gốc (root_objectable_*) cho prepick_details';

    public function handle()
    {
        $rows = [];
        DB::table('prepick_details')->select(['id', 'objectable_id', 'objectable_type', 'root_objectable_id'])
            ->orderBy('id')->chunk(5000, function ($chunk) use (&$rows) {
                foreach ($chunk as $r) {
                    $rows[(int) $r->id] = [
                        'objectable_id' => $r->objectable_id !== null ? (int) $r->objectable_id : null,
                        'objectable_type' => $r->objectable_type,
                        'has_root' => $r->root_objectable_id !== null,
                    ];
                }
            });

        $extendSource = DB::table('prepick_extend_request_details')
            ->whereNotNull('prepick_detail_id')->pluck('prepick_detail_id', 'id')
            ->map(function ($v) { return (int) $v; })->all();

        $resolved = PrepickRootResolver::resolve($rows, $extendSource);

        $targets = [];
        foreach ($resolved as $id => $root) {
            if (!$this->option('all') && $rows[$id]['has_root']) {
                continue;
            }
            if ($root['root_id'] === null) {
                continue;
            }
            $targets[$id] = $root;
        }

        $byType = [];
        foreach ($targets as $root) {
            $byType[$root['root_type']] = ($byType[$root['root_type']] ?? 0) + 1;
        }
        $this->info('Tổng dòng: ' . count($rows) . ' · sẽ ghi: ' . count($targets));
        foreach ($byType as $type => $n) {
            $this->line("  {$type}: {$n}");
        }
        if ($this->option('dry-run')) {
            return 0;
        }

        foreach (array_chunk($targets, 500, true) as $batch) {
            DB::transaction(function () use ($batch) {
                foreach ($batch as $id => $root) {
                    DB::table('prepick_details')->where('id', $id)->update([
                        'root_objectable_id' => $root['root_id'],
                        'root_objectable_type' => $root['root_type'],
                    ]);
                }
            });
        }
        $this->info('Xong.');

        return 0;
    }
}
```

- [x] **Step 8: Chạy migration + dry-run trên DB local, đối chiếu số đo cũ**

```bash
cd $W/hrm-api && /opt/homebrew/opt/php@7.4/bin/php artisan migrate --path=database/migrations/2026_10_02_000001_add_root_objectable_to_prepick_details.php
/opt/homebrew/opt/php@7.4/bin/php artisan prepick:backfill-root --dry-run
```
Expected: không còn `PrepickExtendRequestDetail` chiếm 34.034 dòng như phân bổ `objectable_type`; số `PrepickExtendRequestDetail` còn lại = số chuỗi đứt (ghi số đó vào `design.md` §50). Rồi chạy thật (bỏ `--dry-run`), sau đó đo:

```bash
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='echo DB::table("prepick_details")->where("qty",">",0)->whereNull("root_objectable_id")->count(), " | ", DB::table("prepick_details")->where("qty",">",0)->select(DB::raw("count(distinct concat(root_objectable_type,root_objectable_id,\"|\",product_id,\"|\",employee_id)) c"))->value("c");'
```
Expected: số dòng còn tồn chưa có root = số dòng `objectable` NULL (nhánh phân bổ chuyển kho ERP cũ); số yêu cầu giữ ≈ 2.410 (spec §2 — lệch thì ghi lại số mới, dữ liệu local có thể đã khác 15/09).

- [x] **Step 9: Commit**

```bash
cd $W/hrm-api && git add database/migrations/2026_10_02_000001_add_root_objectable_to_prepick_details.php Modules/Finance/Services/PrepickTracking/PrepickRootResolver.php app/Console/Commands/BackfillPrepickRootCommand.php Modules/Finance/Entities/PrepickCancel/PrepickDetail.php Modules/Finance/Tests/Unit/PrepickRootResolverTest.php
git commit -m "feat(prepick): thêm cột chứng từ gốc root_objectable_* + lệnh backfill"
```

---

### Task 3: HRM ghi root ở 3 chỗ tạo dòng hàng giữ

**Files:**
- Modify: `hrm-api/Modules/Finance/Services/PrepickStockService.php` — `moveToExpireDate()` (~dòng 662), `moveToOwner()` (~792), `addLot()` (~882)
- Test: `hrm-api/Modules/Finance/Tests/Feature/PrepickStockRootTest.php`

**Interfaces:**
- Consumes: `PrepickDetail::rootPair()` (Task 2).
- Quy tắc: gia hạn → kế thừa `rootPair()` của dòng NGUỒN; điều chuyển → `(detailId, ERP_PREPICK_TRANSFER2_DETAIL_TYPE)`; xuất giữ → `(documentId, ERP_WAREHOUSE_PREPICK_TYPE)`. CHỈ ghi trong nhánh `if (!$target)` — dòng sẵn có bị cộng dồn giữ nguyên root của người tạo.

- [x] **Step 1: Viết test (thất bại)**

```php
<?php

namespace Modules\Finance\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Modules\Finance\Entities\PrepickCancel\PrepickDetail;
use Modules\Finance\Services\PrepickStockService;
use Tests\TestCase;

class PrepickStockRootTest extends TestCase
{
    use DatabaseTransactions;

    private function fixture(): array
    {
        $productId = DB::table('products')->value('id');
        $employeeId = DB::table('employees')->value('id');
        $customerId = DB::table('customers')->value('id');
        if (!$productId || !$employeeId || !$customerId) {
            $this->markTestSkipped('DB local thiếu products/employees/customers');
        }

        return [(int) $productId, (int) $employeeId, (int) $customerId];
    }

    public function test_add_lot_sets_root_to_prepick_document(): void
    {
        [$p, $e, $c] = $this->fixture();
        $id = app(PrepickStockService::class)->addLot($p, $e, $c, 1, '2099-01-01', 3, 987654, 1);
        $row = PrepickDetail::find($id);
        $this->assertSame(987654, (int) $row->root_objectable_id);
        $this->assertSame(PrepickStockService::ERP_WAREHOUSE_PREPICK_TYPE, $row->root_objectable_type);
    }

    public function test_extension_inherits_root_of_source_row(): void
    {
        [$p, $e, $c] = $this->fixture();
        $service = app(PrepickStockService::class);
        $sourceId = $service->addLot($p, $e, $c, 1, '2099-01-01', 5, 987654, 1);

        $service->moveToExpireDate($sourceId, 2, '2099-06-01', 555001);

        $target = PrepickDetail::where('employee_id', $e)->where('customer_id', $c)->where('product_id', $p)
            ->whereDate('expire_date', '2099-06-01')->first();
        $this->assertNotNull($target);
        $this->assertSame(PrepickStockService::ERP_PREPICK_EXTEND_DETAIL_TYPE, $target->objectable_type);
        $this->assertSame(987654, (int) $target->root_objectable_id);
        $this->assertSame(PrepickStockService::ERP_WAREHOUSE_PREPICK_TYPE, $target->root_objectable_type);
    }

    public function test_transfer_root_is_transfer_line(): void
    {
        [$p, $e, $c] = $this->fixture();
        $service = app(PrepickStockService::class);
        $sourceId = $service->addLot($p, $e, $c, 1, '2099-01-01', 5, 987654, 1);
        $otherCustomer = (int) DB::table('customers')->where('id', '<>', $c)->value('id');
        if (!$otherCustomer) {
            $this->markTestSkipped('Cần 2 khách hàng');
        }

        $service->moveToOwner($sourceId, 1, $e, $otherCustomer, 777001);

        $target = PrepickDetail::where('employee_id', $e)->where('customer_id', $otherCustomer)
            ->where('product_id', $p)->whereDate('expire_date', '2099-01-01')->first();
        $this->assertSame(777001, (int) $target->root_objectable_id);
        $this->assertSame(PrepickStockService::ERP_PREPICK_TRANSFER2_DETAIL_TYPE, $target->root_objectable_type);
    }
}
```

> Trước khi chạy: đọc chữ ký thật của `moveToOwner()` để biết hạn của dòng đích lấy từ đâu (`$expireDate` = hạn dòng nguồn) — nếu khác `'2099-01-01'` thì sửa điều kiện `whereDate` của test 3 cho khớp.

- [x] **Step 2: Chạy, phải FAIL** (root NULL)

Run: `/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/Finance/Tests/Feature/PrepickStockRootTest.php`

- [x] **Step 3: Sửa 3 nhánh tạo dòng**

`moveToExpireDate()` — trong `if (!$target) {` sau dòng `objectable_type`:
```php
            // Báo cáo theo dõi giữ hàng: dòng do GIA HẠN sinh ra kế thừa chứng từ gốc của dòng nguồn.
            [$target->root_objectable_id, $target->root_objectable_type] = $source->rootPair();
```
`moveToOwner()` — trong `if (!$target) {`:
```php
            // Điều chuyển là CHỨNG TỪ GỐC mới (người/khách đứng tên đã đổi) — không kế thừa.
            $target->root_objectable_id = $detailId;
            $target->root_objectable_type = self::ERP_PREPICK_TRANSFER2_DETAIL_TYPE;
```
`addLot()` — trong `if (!$lot) {`:
```php
            $lot->root_objectable_id = $documentId;
            $lot->root_objectable_type = self::ERP_WAREHOUSE_PREPICK_TYPE;
```

- [x] **Step 4: Chạy, phải PASS.** Chạy thêm các test Finance đang có của giữ hàng để chắc không gãy: `php vendor/bin/phpunit tests/Unit/AccountingPrepickCancelLinesTest.php`.

- [x] **Step 5: Commit**

```bash
git add Modules/Finance/Services/PrepickStockService.php Modules/Finance/Tests/Feature/PrepickStockRootTest.php
git commit -m "feat(prepick): ghi chứng từ gốc khi tạo dòng giữ (xuất giữ, gia hạn, điều chuyển)"
```

---

### Task 4: ERP ghi root ở 5 chỗ tạo dòng hàng giữ

**Files (repo ERP, worktree `$W/erp`, số dòng theo `origin/gop_db`):**
- Modify: `app/Model/Warehouse/PrepickDetail.php` — thêm `rootPair()`
- Modify: `app/Model/Warehouse/WarehousePrepickRequest.php:369-418` (`updateWarehouse()`)
- Modify: `app/Model/Warehouse/PrepickTransfer2Detail.php:34-82` (`updateWarehouse()`)
- Modify: `app/Model/Warehouse/ProductImport.php:1810-1848` (`prepick()`)
- Modify: `app/Model/Warehouse/TransferProductAllocation.php:179-234` (`approve()`)
- Modify: `app/Model/Warehouse/PrepickExtendRequest.php:637-688` (`updateWarehouse()`)

ERP không có test suite dùng được → kiểm bằng `php -l` + tinker trên DB local `erp2326` (đã chạy migration cột ở Step 1).

- [x] **Step 1: Thêm cột vào DB ERP local để chạy thử** — ERP local dùng DB `erp2326`, không chạy migration HRM. Chạy cùng file migration HRM trỏ sang DB đó:

```bash
cd $W/hrm-api && DB_DATABASE=erp2326 /opt/homebrew/opt/php@7.4/bin/php artisan migrate --path=database/migrations/2026_10_02_000001_add_root_objectable_to_prepick_details.php --force
```
> Nếu DB ERP local không cho ghi bảng `migrations` (thiếu bảng) → bỏ qua bước này, kiểm ở Step 4 bằng `php -l` và đọc diff; ghi rõ "chưa chạy thử ERP" vào checkpoint.

- [x] **Step 2: `PrepickDetail` ERP — thêm method (giống HRM)**

```php
    /** Chứng từ gốc để dòng MỚI kế thừa (gia hạn). Dòng chưa có root -> objectable của chính nó. */
    public function rootPair()
    {
        if ($this->root_objectable_type) {
            return [(int) $this->root_objectable_id, $this->root_objectable_type];
        }

        return [$this->objectable_id !== null ? (int) $this->objectable_id : null, $this->objectable_type];
    }
```

- [x] **Step 3: Ghi root trong nhánh tạo mới của từng file**

`WarehousePrepickRequest::updateWarehouse()` — trong `if (!$prepick_detail) {` sau `objectable_type`:
```php
                $prepick_detail->root_objectable_id = $this->id;
                $prepick_detail->root_objectable_type = self::class;
```
`PrepickTransfer2Detail::updateWarehouse()` — trong `if (!$to_prepick_detail) {` sau `objectable_type`:
```php
                // Điều chuyển = chứng từ gốc mới, không kế thừa dòng nguồn.
                $to_prepick_detail->root_objectable_id = $to_prepick_detail->objectable_id;
                $to_prepick_detail->root_objectable_type = $to_prepick_detail->objectable_type;
```
`ProductImport::prepick()` — trong `if (!$prepick_detail) {` sau `objectable_type`:
```php
                $prepick_detail->root_objectable_id = $detail->id;
                $prepick_detail->root_objectable_type = get_class($detail);
```
`TransferProductAllocation::approve()` — trong `if (!$prepick_detail) {` (nhánh này KHÔNG ghi objectable; chỉ thêm root):
```php
                    // Nhánh này xưa nay không ghi objectable -> 5.534 dòng "không xác định".
                    // Từ nay ít nhất chứng từ gốc biết được là dòng phân bổ nào.
                    $prepick_detail->root_objectable_id = $d->id;
                    $prepick_detail->root_objectable_type = get_class($d);
```
`PrepickExtendRequest::updateWarehouse()` — trong `if (!$to_prepick_stock_detail) {` sau `objectable_type`:
```php
                    list($to_prepick_stock_detail->root_objectable_id, $to_prepick_stock_detail->root_objectable_type) = $prepick_stock_detail->rootPair();
```

- [x] **Step 4: Kiểm cú pháp + đúng 5 chỗ**

```bash
cd $W/erp && for f in app/Model/Warehouse/{PrepickDetail,WarehousePrepickRequest,PrepickTransfer2Detail,ProductImport,TransferProductAllocation,PrepickExtendRequest}.php; do /opt/homebrew/opt/php@7.4/bin/php -l $f; done
git grep -n "new PrepickDetail()" app | wc -l      # = 5
git grep -n "root_objectable_type" app | wc -l     # = 7 (5 chỗ ghi + 2 trong rootPair)
```

- [x] **Step 5: Commit (repo ERP)**

```bash
git add app/Model/Warehouse && git commit -m "feat(prepick): ghi chứng từ gốc root_objectable_* khi tạo dòng giữ hàng"
```

---

## Phase 2 — BE báo cáo

### Task 5: Quyền mới + phạm vi công ty

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (sau id 1614)
- Create: `hrm-api/Modules/Finance/Services/PrepickTracking/PrepickTrackingScope.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/PrepickTrackingScopeTest.php`

**Interfaces:**
- Produces: `PrepickTrackingScope::PERMISSION_ALL_COMPANY` · `canViewAllCompanies(): bool` · `companyIdFor($request): ?int` — `null` = tất cả công ty (chỉ khi có quyền); số = 1 công ty; `0` = không xác định được công ty → báo cáo rỗng · `ownCompanyId(): ?int`.

- [x] **Step 1: Seeder** — thêm sau dòng id 1614:

```php
        // Báo cáo theo dõi giữ hàng (feature bao-cao-theo-doi-giu-hang, chốt 13/09 + 02/10/2026):
        // ĐÚNG 1 quyền, chỉ quyết định PHẠM VI CÔNG TY. KHÔNG gate vào màn — không có quyền vẫn
        // xem toàn bộ hàng giữ của công ty mình. Đừng nhầm với id 100839 (màn PHIẾU, guard web).
        Permission::create(['id' => 1632, 'guard_name' => 'api', 'name' => 'Xem báo cáo giữ hàng theo tổng công ty', 'display_name' => 'Xem báo cáo giữ hàng theo tổng công ty', 'group' => 'Báo cáo giữ hàng', 'type' => 23]);
```
Kiểm trùng id ngay (bẫy merge nhánh dài):
```bash
grep -o "'id' => [0-9]*" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php | sort | uniq -d   # phải rỗng
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='echo DB::table("permissions")->where("id",1632)->value("name") ?? "trống";'
```
DB local KHÔNG chạy seeder (truncate cả bảng) — insert tay:
```bash
/opt/homebrew/opt/php@7.4/bin/php artisan tinker --execute='DB::table("permissions")->insertOrIgnore(["id"=>1632,"guard_name"=>"api","name"=>"Xem báo cáo giữ hàng theo tổng công ty","display_name"=>"Xem báo cáo giữ hàng theo tổng công ty","group"=>"Báo cáo giữ hàng","type"=>23,"created_at"=>now(),"updated_at"=>now()]); app()["cache"]->forget("spatie.permission.cache");'
```

- [x] **Step 2: Test phạm vi (thất bại)**

```php
<?php

namespace Modules\Finance\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Modules\Finance\Services\PrepickTracking\PrepickTrackingScope;
use Tests\TestCase;

class PrepickTrackingScopeTest extends TestCase
{
    use DatabaseTransactions;

    /** Nhân viên thường: không role 18, không quyền 1632, có company_id. */
    private function plainEmployee()
    {
        $id = DB::table('employees as e')->join('employee_infos as ei', 'ei.id', '=', 'e.employee_info_id')
            ->whereNotNull('ei.company_id')
            ->whereNotIn('e.id', DB::table('employee_has_roles')->where('role_id', 18)->pluck('employee_id'))
            ->value('e.id');
        if (!$id) {
            $this->markTestSkipped('Không có nhân viên thường');
        }
        DB::table('employee_has_permissions')->where('employee_id', $id)->where('permission_id', 1632)->delete();
        DB::table('employee_has_roles')->where('employee_id', $id)->delete();

        return \App\Models\Employee::find($id);
    }

    public function test_without_permission_company_is_forced_to_own_and_ignores_request(): void
    {
        $emp = $this->plainEmployee();
        $this->actingAs($emp, 'api');
        $own = (int) DB::table('employee_infos')->where('id', $emp->employee_info_id)->value('company_id');

        $scope = new PrepickTrackingScope();
        $this->assertFalse($scope->canViewAllCompanies());
        $this->assertSame($own, $scope->companyIdFor(new Request(['company_id' => $own + 999])));
        $this->assertSame($own, $scope->companyIdFor(new Request(['company_id' => 'all'])));
    }

    public function test_with_permission_can_pick_company_or_all(): void
    {
        $emp = $this->plainEmployee();
        DB::table('employee_has_permissions')->insert(['employee_id' => $emp->id, 'permission_id' => 1632]);
        $this->actingAs($emp, 'api');

        $scope = new PrepickTrackingScope();
        $this->assertTrue($scope->canViewAllCompanies());
        $this->assertSame(7, $scope->companyIdFor(new Request(['company_id' => 7])));
        $this->assertNull($scope->companyIdFor(new Request(['company_id' => 'all'])));
        $this->assertNull($scope->companyIdFor(new Request([])));
    }
}
```
> Đọc migration bảng `employee_has_permissions` trước khi chạy: nếu có thêm cột bắt buộc (`company_id`, `model_type`) thì bổ sung vào `insert` cho đủ. Model nhân viên đăng nhập: kiểm `config('auth.providers')` để dùng đúng class trong `actingAs`.

- [x] **Step 3: Chạy, phải FAIL.**

- [x] **Step 4: Viết scope**

```php
<?php

namespace Modules\Finance\Services\PrepickTracking;

use Modules\Finance\Entities\Concerns\ChecksEmployeePermission;

/**
 * Phạm vi CÔNG TY của báo cáo theo dõi giữ hàng — chốt chặn THẬT nằm ở đây, không ở FE.
 * Không quyền: ép công ty theo hồ sơ, BỎ QUA `company_id` FE gửi (đổi query string không mở
 * rộng được quyền xem). Không giới hạn phòng ban.
 */
class PrepickTrackingScope
{
    use ChecksEmployeePermission;

    const PERMISSION_ALL_COMPANY = 'Xem báo cáo giữ hàng theo tổng công ty';

    public function canViewAllCompanies(): bool
    {
        return self::currentEmployeeIsSuperAdmin()
            || self::currentEmployeeHasPermission(self::PERMISSION_ALL_COMPANY);
    }

    public function ownCompanyId(): ?int
    {
        return self::currentCompanyId();
    }

    /** null = tất cả công ty · int > 0 = 1 công ty · 0 = không xác định được -> báo cáo rỗng */
    public function companyIdFor($request): ?int
    {
        if ($this->canViewAllCompanies()) {
            $value = $request->input('company_id');
            if ($value === null || $value === '' || $value === 'all') {
                return null;
            }

            return (int) $value;
        }

        return $this->ownCompanyId() ?? 0;
    }
}
```

- [x] **Step 5: Chạy, phải PASS. Commit**

```bash
git add Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php Modules/Finance/Services/PrepickTracking/PrepickTrackingScope.php Modules/Finance/Tests/Feature/PrepickTrackingScopeTest.php
git commit -m "feat(prepick-tracking): quyền xem báo cáo giữ hàng theo tổng công ty + phạm vi công ty"
```

---

### Task 6: Tách bộ tra chứng từ (`PrepickDocumentResolver`) dùng chung

**Files:**
- Create: `hrm-api/Modules/Finance/Services/PrepickTracking/PrepickDocumentResolver.php`
- Modify: `hrm-api/Modules/Finance/Services/PrepickStockReportService.php:842-1040` — `resolveDocuments()` gọi resolver mới; XOÁ `DOCUMENT_MAP`, `lookupDocuments()`, `documentUrl()` khỏi file cũ
- Test: `hrm-api/Modules/Finance/Tests/Feature/PrepickDocumentResolverTest.php`

**Interfaces:**
- Produces: `PrepickDocumentResolver::resolve(array $pairs): array` — `$pairs`: list `[type, id]`; trả `"type#id" => ['code' => string, 'url' => string|null]`. `PrepickDocumentResolver::label(string $type): string` — tên loại chứng từ cho tooltip ("Phiếu xuất giữ", "Nhập hàng cho khách", "Điều chuyển giữ", "Phân bổ hàng chuyển kho", "Gia hạn giữ hàng"…).

- [x] **Step 1: Test bám dữ liệu thật (thất bại)**

```php
<?php

namespace Modules\Finance\Tests\Feature;

use Illuminate\Support\Facades\DB;
use Modules\Finance\Services\PrepickTracking\PrepickDocumentResolver;
use Tests\TestCase;

class PrepickDocumentResolverTest extends TestCase
{
    public function test_resolves_warehouse_prepick_request_code(): void
    {
        $row = DB::table('warehouse_prepick_requests')->whereNotNull('code')->first(['id', 'code']);
        if (!$row) {
            $this->markTestSkipped('Không có phiếu xuất giữ');
        }
        $type = 'App\\Model\\Warehouse\\WarehousePrepickRequest';
        $out = (new PrepickDocumentResolver())->resolve([[$type, (int) $row->id]]);
        $this->assertSame($row->code, $out[$type . '#' . $row->id]['code']);
    }

    public function test_resolves_product_import_detail_customer_through_two_tables(): void
    {
        $id = DB::table('product_import_detail_customers')->value('id');
        if (!$id) {
            $this->markTestSkipped('Không có dòng nhập hàng cho khách');
        }
        $type = 'App\\Model\\Warehouse\\ProductImportDetailCustomer';
        $out = (new PrepickDocumentResolver())->resolve([[$type, (int) $id]]);
        $this->assertArrayHasKey($type . '#' . $id, $out);
        $this->assertNotEmpty($out[$type . '#' . $id]['code']);
    }

    public function test_unknown_type_is_skipped(): void
    {
        $this->assertSame([], (new PrepickDocumentResolver())->resolve([['App\\Nope', 1]]));
    }
}
```

- [x] **Step 2: Chạy, phải FAIL.**

- [x] **Step 3: Tạo resolver** — CHUYỂN NGUYÊN VĂN `DOCUMENT_MAP` (dòng 883-958), `lookupDocuments()` (972-1012), `documentUrl()` (1016-1029) từ `PrepickStockReportService` sang class mới (đổi `private` → `public` cho `resolve`, giữ 2 hàm kia `private`), thêm mục còn thiếu:

```php
        'App\\Model\\Warehouse\\TransferProductAllocationDetail' => [ /* đã có trong map cũ — giữ */ ],
```
và thêm `'label' => '...'` vào từng mục của map:
`PrepickCancel` → "Phiếu hủy hàng giữ" · `PrepickTransfer2` / `PrepickTransfer2Detail` → "Điều chuyển giữ" · `WarehousePrepickRequest` / `WarehousePrepickRequestDetail` → "Phiếu xuất giữ" · `PrepickExtendRequestDetail` → "Gia hạn giữ hàng" · `ProductExportDetailAccounting` / `ProductExportDetail` → "Phiếu xuất kho" · `TransferProductAllocationDetail` → "Phân bổ hàng chuyển kho" · `ProductImportDetailCustomer` → "Nhập hàng cho khách" · `AccountingPrepickCancelDetailCustomer` → "Kế toán hủy hàng giữ".

```php
    /**
     * @param array<int, array{0:string|null, 1:int|null}> $pairs
     * @return array<string, array{code:string, url:string|null}> khoá "type#id"
     */
    public function resolve(array $pairs): array
    {
        $needed = [];
        foreach ($pairs as [$type, $id]) {
            if ($type && $id) {
                $needed[$type][] = (int) $id;
            }
        }

        $result = [];
        foreach ($needed as $type => $ids) {
            $map = self::DOCUMENT_MAP[$type] ?? null;
            if ($map === null) {
                continue;
            }
            foreach ($this->lookupDocuments($map, array_values(array_unique($ids))) as $sourceId => $doc) {
                $result[$type . '#' . $sourceId] = $doc;
            }
        }

        return $result;
    }

    public function label(?string $type): string
    {
        return self::DOCUMENT_MAP[$type]['label'] ?? 'Không xác định';
    }
```

- [x] **Step 4: Màn cũ gọi resolver mới** — `PrepickStockReportService::resolveDocuments()` giữ nguyên phần gom `$needed` theo log/lô, chỉ thay vòng lặp cuối bằng:

```php
        $pairs = [];
        foreach ($needed as $type => $ids) {
            foreach ($ids as $id) {
                $pairs[] = [$type, $id];
            }
        }

        return app(PrepickDocumentResolver::class)->resolve($pairs);
```
(thêm `use Modules\Finance\Services\PrepickTracking\PrepickDocumentResolver;`). Khoá trả về vẫn `type#id` → nơi đọc không đổi.

- [x] **Step 5: Chạy test mới PASS + so popup "Sổ biến động" màn cũ trước/sau**

```bash
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/Finance/Tests/Feature/PrepickDocumentResolverTest.php
```
So JSON `GET /api/v1/finance/prepick-stocks/logs?...` của 1 lô có nhiều loại chứng từ ở nhánh `gop_db` (checkout chính) và worktree — phải giống hệt (dùng `diff <(curl ...) <(curl ...)`).

- [x] **Step 6: Commit**

```bash
git add Modules/Finance/Services/PrepickTracking/PrepickDocumentResolver.php Modules/Finance/Services/PrepickStockReportService.php Modules/Finance/Tests/Feature/PrepickDocumentResolverTest.php
git commit -m "refactor(prepick): tách bộ tra chứng từ dùng chung cho báo cáo theo dõi giữ hàng"
```

---

### Task 7: Lớp đo + dựng cây + lọc popup (PHP thuần)

**Files:**
- Create: `hrm-api/Modules/Finance/Services/PrepickTracking/PrepickTrackingMetrics.php`
- Create: `hrm-api/Modules/Finance/Services/PrepickTracking/PrepickTrackingTree.php`
- Create: `hrm-api/Modules/Finance/Services/PrepickTracking/PrepickTrackingDrill.php`
- Test: `hrm-api/Modules/Finance/Tests/Unit/PrepickTrackingMetricsTest.php`, `PrepickTrackingTreeTest.php`, `PrepickTrackingDrillTest.php`

**Interfaces:**
- **Hình dạng 1 dòng (row)** — mảng, do Task 8 sinh: `id, employee_id, employee_name, employee_code, department_id, department_name, part_id, customer_id, customer_code, customer_name, product_id, product_code, product_name, unit_name, brand_id, brand_name, model_id, model_name, company_id, qty(float), start_date('Y-m-d'|null), expire_date('Y-m-d'|null), days_left(int|null), status('ok'|'soon'|'exp'), root_type, root_id, req_key(string), contract(null|['id'=>int,'code'=>string,'type'=>string])`.
- `PrepickTrackingMetrics::of(array $rows): array` → `lots, ok, soon, exp, qty, qty_ok, qty_soon, qty_exp, codes, codes_ok, codes_soon, codes_exp, only_product_id, reqs, reqs_soon, reqs_exp, emps_exp`.
- `PrepickTrackingMetrics::statusOf(?int $daysLeft, int $warnDay): string`.
- `PrepickTrackingTree::build(array $rows, string $criteria, string $sortName, int $depth): array` — `$criteria` ∈ `employee|product`; `$sortName` ∈ `''|asc|desc`; `$depth` = số cấp trả kèm (1..3); node: `['key','dim','id','name','code','sub','unit_name','brand_name','model_name','metrics','has_children','children'=>array|null]` (`children = null` = có con nhưng chưa nạp).
- `PrepickTrackingTree::paginate(array $nodes, int $page, int $perPage): array` → `['nodes'=>..., 'total'=>int, 'page'=>int, 'per_page'=>int, 'offset'=>int]`.
- `PrepickTrackingTree::find(array $rows, string $criteria, string $key): array` — các dòng thuộc node `key` (dạng `dept:5/emp:88/product:12`).
- `PrepickTrackingDrill::filter(array $rows, string $metric, array $popup): array` — `$metric` ∈ `lots|ok|soon|exp|reqs|reqs_soon|reqs_exp|emps_exp`; `$popup` = `['q','employee_id','customer_id','product_id','status']`.
- `PrepickTrackingDrill::sort(array $rows, string $key, string $dir): array` — `$key` ∈ `''|product|qty|customer|employee|department|start_date|expire_date`.

- [x] **Step 1: Test đo (thất bại)** — `Modules/Finance/Tests/Unit/PrepickTrackingMetricsTest.php`

```php
<?php

namespace Modules\Finance\Tests\Unit;

use Modules\Finance\Services\PrepickTracking\PrepickTrackingMetrics as M;
use PHPUnit\Framework\TestCase;

class PrepickTrackingMetricsTest extends TestCase
{
    public static function row(array $o): array
    {
        $r = array_merge([
            'id' => 1, 'employee_id' => 1, 'product_id' => 1, 'qty' => 1.0, 'status' => 'ok',
            'root_type' => 'W', 'root_id' => 1,
        ], $o);
        $r['req_key'] = $r['root_type'] . '#' . $r['root_id'] . '|' . $r['product_id'] . '|' . $r['employee_id'];

        return $r;
    }

    public function test_status_thresholds(): void
    {
        $this->assertSame('exp', M::statusOf(-1, 7));
        $this->assertSame('soon', M::statusOf(0, 7));
        $this->assertSame('soon', M::statusOf(7, 7));
        $this->assertSame('ok', M::statusOf(8, 7));
        $this->assertSame('ok', M::statusOf(null, 7));
    }

    public function test_single_product_measures_quantity_and_buckets_partition_total(): void
    {
        $m = M::of([
            self::row(['id' => 1, 'qty' => 5, 'status' => 'ok']),
            self::row(['id' => 2, 'qty' => 3, 'status' => 'exp', 'root_id' => 2]),
        ]);
        $this->assertSame(1, $m['only_product_id']);
        $this->assertSame(8.0, $m['qty']);
        $this->assertSame(5.0, $m['qty_ok']);
        $this->assertSame(3.0, $m['qty_exp']);
        $this->assertSame($m['qty'], $m['qty_ok'] + $m['qty_soon'] + $m['qty_exp']);
    }

    public function test_many_products_count_codes_and_buckets_overlap(): void
    {
        $m = M::of([
            self::row(['id' => 1, 'product_id' => 1, 'status' => 'ok']),
            self::row(['id' => 2, 'product_id' => 1, 'status' => 'exp', 'root_id' => 2]),
            self::row(['id' => 3, 'product_id' => 2, 'status' => 'soon']),
        ]);
        $this->assertNull($m['only_product_id']);
        $this->assertSame(2, $m['codes']);
        $this->assertSame(1, $m['codes_ok']);
        $this->assertSame(1, $m['codes_soon']);
        $this->assertSame(1, $m['codes_exp']);
        $this->assertGreaterThan($m['codes'], $m['codes_ok'] + $m['codes_soon'] + $m['codes_exp']);
    }

    public function test_requests_counted_by_root_product_employee(): void
    {
        // 2 dòng cùng 1 yêu cầu (gia hạn tách một phần): 1 trong hạn, 1 quá hạn
        $m = M::of([
            self::row(['id' => 1, 'status' => 'ok']),
            self::row(['id' => 2, 'status' => 'exp']),
            self::row(['id' => 3, 'employee_id' => 2, 'status' => 'soon']),
        ]);
        $this->assertSame(2, $m['reqs']);
        $this->assertSame(1, $m['reqs_exp']);
        $this->assertSame(1, $m['reqs_soon']);
        $this->assertSame(1, $m['emps_exp']);
        $this->assertSame(3, $m['lots']);
    }
}
```

- [x] **Step 2: Chạy, phải FAIL.**

- [x] **Step 3: Viết `PrepickTrackingMetrics`** (port 1-1 `metrics()` của mockup dòng 3368-3430)

```php
<?php

namespace Modules\Finance\Services\PrepickTracking;

/**
 * Bộ đo của báo cáo theo dõi giữ hàng — port 1-1 hàm `metrics()` của mockup đã duyệt.
 *
 *  · `qty*`   — số lượng (đơn vị cơ bản), dùng khi dòng gom ĐÚNG 1 mã (`only_product_id`);
 *               3 nhóm hạn CHIA HẾT tổng.
 *  · `codes*` — số mã hàng, dùng khi dòng gom NHIỀU mã; 3 nhóm hạn ĐẾM CHỒNG LẤN (cố ý).
 *  · `reqs*`  — số YÊU CẦU GIỮ (root + mã + NV); sắp/đã hết hạn CHỒNG LẤN nhau.
 *  · `lots`/`ok`/`soon`/`exp` — số dòng `prepick_details` (chỉ để sắp xếp + đếm nội bộ,
 *               KHÔNG hiện chữ "lô" lên giao diện).
 */
final class PrepickTrackingMetrics
{
    const OK = 'ok';
    const SOON = 'soon';
    const EXP = 'exp';

    public static function statusOf(?int $daysLeft, int $warnDay): string
    {
        if ($daysLeft === null) {
            return self::OK;
        }
        if ($daysLeft < 0) {
            return self::EXP;
        }

        return $daysLeft <= $warnDay ? self::SOON : self::OK;
    }

    public static function of(array $rows): array
    {
        $m = ['lots' => count($rows), 'ok' => 0, 'soon' => 0, 'exp' => 0,
            'qty' => 0.0, 'qty_ok' => 0.0, 'qty_soon' => 0.0, 'qty_exp' => 0.0];
        $codes = [];
        $codesBy = [self::OK => [], self::SOON => [], self::EXP => []];
        $reqs = [];
        $reqsSoon = [];
        $reqsExp = [];
        $empsExp = [];

        foreach ($rows as $r) {
            $st = $r['status'];
            $qty = (float) $r['qty'];
            $m[$st]++;
            $m['qty'] += $qty;
            $m['qty_' . $st] += $qty;
            $codes[$r['product_id']] = true;
            $codesBy[$st][$r['product_id']] = true;
            $reqs[$r['req_key']] = true;
            if ($st === self::SOON) {
                $reqsSoon[$r['req_key']] = true;
            }
            if ($st === self::EXP) {
                $reqsExp[$r['req_key']] = true;
                $empsExp[$r['employee_id']] = true;
            }
        }

        $m['codes'] = count($codes);
        $m['codes_ok'] = count($codesBy[self::OK]);
        $m['codes_soon'] = count($codesBy[self::SOON]);
        $m['codes_exp'] = count($codesBy[self::EXP]);
        $m['only_product_id'] = count($codes) === 1 ? (int) array_key_first($codes) : null;
        $m['reqs'] = count($reqs);
        $m['reqs_soon'] = count($reqsSoon);
        $m['reqs_exp'] = count($reqsExp);
        $m['emps_exp'] = count($empsExp);

        return $m;
    }
}
```
> PHP 7.4 có `array_key_first` (≥ 7.3). Số lượng là `decimal(12,2)` → so sánh test dùng `8.0` (float).

- [x] **Step 4: PASS.** Commit `feat(prepick-tracking): bộ đo theo dòng (port metrics mockup)`.

- [x] **Step 5: Test cây (thất bại)** — `PrepickTrackingTreeTest.php`

```php
<?php

namespace Modules\Finance\Tests\Unit;

use Modules\Finance\Services\PrepickTracking\PrepickTrackingTree as T;
use PHPUnit\Framework\TestCase;

class PrepickTrackingTreeTest extends TestCase
{
    private function rows(): array
    {
        $r = function ($id, $dept, $emp, $prd, $status, $qty = 1) {
            return PrepickTrackingMetricsTest::row([
                'id' => $id, 'department_id' => $dept, 'department_name' => 'P' . $dept,
                'employee_id' => $emp, 'employee_name' => 'NV' . $emp, 'employee_code' => 'E' . $emp,
                'product_id' => $prd, 'product_code' => 'M' . $prd, 'product_name' => 'Hàng ' . $prd,
                'unit_name' => 'Cái', 'brand_name' => 'B', 'model_name' => 'X', 'status' => $status, 'qty' => $qty,
                'root_id' => $id,
            ]);
        };

        return [
            $r(1, 1, 10, 100, 'ok'), $r(2, 1, 10, 101, 'ok'),
            $r(3, 2, 20, 100, 'exp'), $r(4, 2, 21, 102, 'exp'), $r(5, 2, 21, 102, 'ok'),
        ];
    }

    public function test_employee_criteria_levels_and_default_sort_puts_most_overdue_first(): void
    {
        $tree = T::build($this->rows(), 'employee', '', 3);
        $this->assertSame(['dept:2', 'dept:1'], array_column($tree, 'key'));
        $this->assertSame('dept', $tree[0]['dim']);
        $this->assertSame('emp', $tree[0]['children'][0]['dim']);
        $this->assertSame('product', $tree[0]['children'][0]['children'][0]['dim']);
        $this->assertSame('dept:2/emp:21/product:102', $tree[0]['children'][0]['children'][0]['key']);
    }

    public function test_depth_cuts_children_but_keeps_has_children(): void
    {
        $tree = T::build($this->rows(), 'employee', '', 2);
        $emp = $tree[0]['children'][0];
        $this->assertTrue($emp['has_children']);
        $this->assertNull($emp['children']);
    }

    public function test_product_criteria_and_name_sort(): void
    {
        $tree = T::build($this->rows(), 'product', 'desc', 2);
        $this->assertSame(['product:102', 'product:101', 'product:100'], array_column($tree, 'key'));
        $this->assertSame('emp', $tree[0]['children'][0]['dim']);
        $this->assertFalse($tree[0]['children'][0]['has_children']);
    }

    public function test_paginate_by_level_one_nodes(): void
    {
        $tree = T::build($this->rows(), 'product', '', 2);
        $page = T::paginate($tree, 2, 2);
        $this->assertSame(3, $page['total']);
        $this->assertCount(1, $page['nodes']);
        $this->assertSame(2, $page['offset']);
    }

    public function test_find_rows_of_node(): void
    {
        $rows = T::find($this->rows(), 'employee', 'dept:2/emp:21');
        $this->assertSame([4, 5], array_column($rows, 'id'));
    }
}
```

- [x] **Step 6: Viết `PrepickTrackingTree`**

```php
<?php

namespace Modules\Finance\Services\PrepickTracking;

/**
 * Cây theo dõi — port `buildTree()` của mockup.
 *   employee: Phòng ban ▸ Nhân viên ▸ Hàng hoá   ·   product: Hàng hoá ▸ Nhân viên
 * Thứ tự mặc định: nhiều dòng QUÁ HẠN trước, rồi nhiều dòng hơn, rồi theo tên.
 * Phân trang theo NODE CẤP 1 (không theo dòng render: bung/thu sẽ đẩy nội dung sang trang khác).
 */
final class PrepickTrackingTree
{
    const DIMS = [
        'employee' => ['dept', 'emp', 'product'],
        'product' => ['product', 'emp'],
    ];

    const FIELD = ['dept' => 'department_id', 'emp' => 'employee_id', 'product' => 'product_id'];

    public static function build(array $rows, string $criteria, string $sortName, int $depth): array
    {
        return self::level($rows, self::DIMS[$criteria] ?? self::DIMS['employee'], '', $sortName, $depth);
    }

    private static function level(array $rows, array $dims, string $prefix, string $sortName, int $depth): array
    {
        if (!$dims || !$rows) {
            return [];
        }
        $dim = $dims[0];
        $rest = array_slice($dims, 1);
        $field = self::FIELD[$dim];

        $groups = [];
        foreach ($rows as $r) {
            $groups[(int) ($r[$field] ?? 0)][] = $r;
        }

        $nodes = [];
        foreach ($groups as $id => $items) {
            $key = ($prefix === '' ? '' : $prefix . '/') . $dim . ':' . $id;
            $first = $items[0];
            $nodes[] = [
                'key' => $key,
                'dim' => $dim,
                'id' => $id,
                'name' => self::nameOf($dim, $first),
                'code' => $dim === 'product' ? $first['product_code'] : ($dim === 'emp' ? $first['employee_code'] : null),
                // "Tên NV - Phòng ban" ở tiêu chí Hàng hoá; ở tiêu chí NV phòng đã là node cha.
                'sub' => $dim === 'emp' ? ($first['department_name'] ?? null) : null,
                'unit_name' => $dim === 'product' ? $first['unit_name'] : null,
                'brand_name' => $dim === 'product' ? $first['brand_name'] : null,
                'model_name' => $dim === 'product' ? $first['model_name'] : null,
                'product_id' => $dim === 'product' ? $id : null,
                'metrics' => PrepickTrackingMetrics::of($items),
                'has_children' => !empty($rest),
                'children' => !empty($rest) && $depth > 1
                    ? self::level($items, $rest, $key, $sortName, $depth - 1)
                    : (!empty($rest) ? null : []),
            ];
        }

        usort($nodes, function ($a, $b) use ($sortName) {
            if ($sortName === 'asc' || $sortName === 'desc') {
                $cmp = strcmp(self::sortLabel($a), self::sortLabel($b));

                return $sortName === 'asc' ? $cmp : -$cmp;
            }

            return ($b['metrics']['exp'] <=> $a['metrics']['exp'])
                ?: ($b['metrics']['lots'] <=> $a['metrics']['lots'])
                ?: strcmp(self::sortLabel($a), self::sortLabel($b));
        });

        return $nodes;
    }

    private static function nameOf(string $dim, array $r): string
    {
        if ($dim === 'dept') {
            return $r['department_name'] ?: 'Chưa có phòng ban';
        }
        if ($dim === 'emp') {
            return $r['employee_name'] ?: '—';
        }

        return $r['product_name'] ?: '—';
    }

    /** "Mã - Tên" cho hàng hoá (đúng nhãn hiển thị), tên cho node khác; so không phân biệt hoa thường. */
    private static function sortLabel(array $node): string
    {
        $label = $node['dim'] === 'product' ? $node['code'] . ' - ' . $node['name'] : $node['name'];

        return mb_strtolower($label, 'UTF-8');
    }

    public static function paginate(array $nodes, int $page, int $perPage): array
    {
        $perPage = max(1, min(100, $perPage));
        $total = count($nodes);
        $lastPage = max(1, (int) ceil($total / $perPage));
        $page = max(1, min($page, $lastPage));
        $offset = ($page - 1) * $perPage;

        return ['nodes' => array_slice($nodes, $offset, $perPage), 'total' => $total,
            'page' => $page, 'per_page' => $perPage, 'offset' => $offset];
    }

    /** Dòng thuộc 1 node — `key` dạng "dept:5/emp:88/product:12". Key rỗng = toàn bộ. */
    public static function find(array $rows, string $criteria, string $key): array
    {
        if ($key === '') {
            return $rows;
        }
        $conds = [];
        foreach (explode('/', $key) as $part) {
            [$dim, $id] = array_pad(explode(':', $part, 2), 2, null);
            if (!isset(self::FIELD[$dim])) {
                return [];
            }
            $conds[self::FIELD[$dim]] = (int) $id;
        }

        return array_values(array_filter($rows, function ($r) use ($conds) {
            foreach ($conds as $field => $id) {
                if ((int) ($r[$field] ?? 0) !== $id) {
                    return false;
                }
            }

            return true;
        }));
    }
}
```
> `strcmp` trên chuỗi đã `mb_strtolower` sắp theo byte UTF-8 — chữ có dấu tiếng Việt đứng sau chữ không dấu. Nếu máy chủ có ext `intl` (`php -m | grep intl`) thì thay bằng `(new \Collator('vi_VN'))->compare()`; ghi kết quả kiểm vào checkpoint.

- [x] **Step 7: PASS.** Commit `feat(prepick-tracking): dựng cây 2 tiêu chí + phân trang theo node cấp 1`.

- [x] **Step 8: Test popup (thất bại)** — `PrepickTrackingDrillTest.php`

```php
<?php

namespace Modules\Finance\Tests\Unit;

use Modules\Finance\Services\PrepickTracking\PrepickTrackingDrill as D;
use PHPUnit\Framework\TestCase;

class PrepickTrackingDrillTest extends TestCase
{
    private function rows(): array
    {
        $r = function ($id, $emp, $status, $days, $root, $o = []) {
            return PrepickTrackingMetricsTest::row(array_merge([
                'id' => $id, 'employee_id' => $emp, 'employee_name' => 'NV' . $emp, 'department_name' => 'P',
                'customer_id' => 9, 'customer_name' => 'Khách A', 'customer_code' => 'KH9',
                'product_code' => 'VT.1', 'product_name' => 'Ống', 'status' => $status, 'days_left' => $days,
                'expire_date' => date('Y-m-d', strtotime(($days >= 0 ? '+' : '') . $days . ' days')),
                'start_date' => '2026-01-01', 'root_id' => $root,
            ], $o));
        };

        return [$r(1, 1, 'ok', 30, 1), $r(2, 1, 'exp', -5, 1), $r(3, 2, 'soon', 2, 3), $r(4, 2, 'ok', 40, 4)];
    }

    public function test_status_metric_filters_rows(): void
    {
        $this->assertSame([2], array_column(D::filter($this->rows(), 'exp', []), 'id'));
    }

    public function test_request_metric_returns_every_row_of_hit_requests(): void
    {
        // yêu cầu (root 1, mã 1, NV 1) có 1 dòng quá hạn -> trả CẢ 2 dòng của yêu cầu đó
        $this->assertSame([1, 2], array_column(D::filter($this->rows(), 'reqs_exp', []), 'id'));
    }

    public function test_emps_exp_returns_rows_of_employees_having_overdue(): void
    {
        $this->assertSame([2], array_column(D::filter($this->rows(), 'emps_exp', []), 'id'));
    }

    public function test_popup_filters_and_search(): void
    {
        $this->assertSame([3, 4], array_column(D::filter($this->rows(), 'lots', ['employee_id' => 2]), 'id'));
        $this->assertSame([], D::filter($this->rows(), 'lots', ['q' => 'không có']));
        $this->assertCount(4, D::filter($this->rows(), 'lots', ['q' => 'kh9']));
    }

    public function test_default_sort_most_overdue_first_then_cycle(): void
    {
        $this->assertSame([2, 3, 1, 4], array_column(D::sort($this->rows(), '', 'asc'), 'id'));
        $this->assertSame([4, 1, 3, 2], array_column(D::sort($this->rows(), 'expire_date', 'desc'), 'id'));
    }
}
```

- [x] **Step 9: Viết `PrepickTrackingDrill`**

```php
<?php

namespace Modules\Finance\Services\PrepickTracking;

/**
 * Lọc + sắp popup chi tiết — port `drillBaseLots()` / `drillLots()` của mockup.
 *
 * `emps_exp` ("NV có hàng giữ quá hạn"): trả các dòng QUÁ HẠN của những NV đó — đúng thứ người
 * bấm cần xử lý (mockup dùng chung bộ lọc `exp`, con số đếm NV khác nhưng tập dòng trùng nhau).
 */
final class PrepickTrackingDrill
{
    const REQ_METRIC = ['reqs' => null, 'reqs_soon' => 'soon', 'reqs_exp' => 'exp'];
    const STATUS_METRIC = ['ok' => 'ok', 'soon' => 'soon', 'exp' => 'exp', 'emps_exp' => 'exp'];

    public static function filter(array $rows, string $metric, array $popup): array
    {
        if (array_key_exists($metric, self::REQ_METRIC)) {
            $want = self::REQ_METRIC[$metric];
            if ($want !== null) {
                $hit = [];
                foreach ($rows as $r) {
                    if ($r['status'] === $want) {
                        $hit[$r['req_key']] = true;
                    }
                }
                $rows = array_filter($rows, function ($r) use ($hit) {
                    return isset($hit[$r['req_key']]);
                });
            }
        } elseif (isset(self::STATUS_METRIC[$metric])) {
            $want = self::STATUS_METRIC[$metric];
            $rows = array_filter($rows, function ($r) use ($want) {
                return $r['status'] === $want;
            });
        }

        $q = mb_strtolower(trim((string) ($popup['q'] ?? '')), 'UTF-8');

        return array_values(array_filter($rows, function ($r) use ($popup, $q) {
            foreach (['employee_id', 'customer_id', 'product_id'] as $f) {
                if (!empty($popup[$f]) && (int) $r[$f] !== (int) $popup[$f]) {
                    return false;
                }
            }
            if (!empty($popup['status']) && $r['status'] !== $popup['status']) {
                return false;
            }
            if ($q !== '') {
                $hay = mb_strtolower(implode(' ', [$r['product_code'] ?? '', $r['product_name'] ?? '',
                    $r['customer_name'] ?? '', $r['customer_code'] ?? '', $r['employee_name'] ?? '',
                    $r['root_code'] ?? '']), 'UTF-8');
                if (mb_strpos($hay, $q) === false) {
                    return false;
                }
            }

            return true;
        }));
    }

    const SORT_FIELD = [
        'product' => ['product_code', 'product_name'], 'qty' => ['qty'], 'customer' => ['customer_name'],
        'employee' => ['employee_name'], 'department' => ['department_name'],
        'start_date' => ['start_date'], 'expire_date' => ['expire_date'],
    ];

    public static function sort(array $rows, string $key, string $dir): array
    {
        $fields = self::SORT_FIELD[$key] ?? null;
        usort($rows, function ($a, $b) use ($fields, $dir) {
            if ($fields === null) {
                // Mặc định: hạn tăng dần (quá hạn lâu nhất lên đầu); không có hạn xuống cuối.
                return self::cmpDate($a['expire_date'], $b['expire_date']) ?: ($a['id'] <=> $b['id']);
            }
            $cmp = 0;
            foreach ($fields as $f) {
                $va = $a[$f];
                $vb = $b[$f];
                $cmp = is_numeric($va) && is_numeric($vb) ? ((float) $va <=> (float) $vb)
                    : strcmp(mb_strtolower((string) $va, 'UTF-8'), mb_strtolower((string) $vb, 'UTF-8'));
                if ($cmp !== 0) {
                    break;
                }
            }
            $cmp = $cmp ?: ($a['id'] <=> $b['id']);

            return $dir === 'desc' ? -$cmp : $cmp;
        });

        return $rows;
    }

    private static function cmpDate(?string $a, ?string $b): int
    {
        if ($a === $b) {
            return 0;
        }
        if ($a === null) {
            return 1;
        }
        if ($b === null) {
            return -1;
        }

        return strcmp($a, $b);
    }
}
```

- [x] **Step 10: PASS cả 3 file test.** Commit `feat(prepick-tracking): lọc + sắp popup chi tiết theo khoá yêu cầu giữ`.

---

### Task 8: Nạp dữ liệu + service báo cáo + controller/route

**Files:**
- Create: `hrm-api/Modules/Finance/Services/PrepickTracking/PrepickTrackingRowLoader.php`
- Create: `hrm-api/Modules/Finance/Services/PrepickTracking/PrepickExtendChain.php`
- Create: `hrm-api/Modules/Finance/Services/PrepickTracking/PrepickTrackingReportService.php`
- Create: `hrm-api/Modules/Finance/Http/Controllers/V1/PrepickTrackingController.php`
- Modify: `hrm-api/Modules/Finance/Routes/api.php` — thêm khối `prepick-tracking` ngay SAU khối `prepick-expiring` (~dòng 1037)
- Test: `hrm-api/Modules/Finance/Tests/Feature/PrepickTrackingApiTest.php`

**Interfaces:**
- Consumes: `PrepickTrackingScope`, `PrepickTrackingMetrics/Tree/Drill`, `PrepickDocumentResolver`, `PrepickLotContractService::forLots()`, `PrepickConfigService::warningDay()`, `PrepickStockService::baseUnits()` (đơn vị cơ bản — đã dùng ở `PrepickExtendRequestService::dataToCreate`).
- Produces (endpoint, tất cả GET, prefix `/api/v1/finance/prepick-tracking`, response `{code, message, data}` qua `responseJson`):

| Route | Tham số | `data` |
|---|---|---|
| `/meta` | `company_id`, `department_id` | `can_view_all_companies, own_company_id, own_department_id, own_part_id, own_employee_id, warning_day, companies[], departments[], parts[]` (+ `has_unassigned`), `part_state` (`need_department`/`no_parts`/`ok`), `employees[] {id,name,code,department_code}`, `customers[]`, `brands[]`, `models[]` — CHỈ giá trị đang có hàng giữ trong phạm vi |
| `/` | bộ lọc chung + `criteria`, `depth`, `sort_name`, `page`, `per_page` | `summary {employees, products, customers, metrics}`, `total` (metrics toàn bộ), `tree` (node trang hiện tại), `pagination {total,page,per_page,offset}`, `stock_by_product` (chỉ khi `criteria=product`) |
| `/children` | bộ lọc chung + `criteria`, `key` | `nodes` — con TRỰC TIẾP của node `key` (đủ mọi cấp dưới) |
| `/details` | bộ lọc chung + `criteria`, `key`, `metric`, `d_q`, `d_employee_id`, `d_customer_id`, `d_product_id`, `d_status`, `sort_key`, `sort_dir`, `page`, `per_page` | `rows[]`, `total`, `counts {products, reqs, units[]}`, `options {employees, customers, products}` |
| `/extends` | `prepick_detail_id` | `rows[] {no, approved_time, code, url, old_expire, new_expire, extend_qty, requester, approver, is_current}`, `unit_name`, `root_code` |
| `/payments` | `contract_id`, `contract_type` | `contract {code, value}`, `paid`, `rows[] {code, date, payer, amount, note}` |
| `/print-list-data` | bộ lọc + `mode=tree|detail` (+ khoá popup khi `detail`) | `{template, truncated, total, limit}` |
| `/export` | như trên | file `.xlsx` (tải trực tiếp `?token=`) |

Bộ lọc chung: `company_id, department_id, part_id ('' | id | 'none'), employee_id, customer_id, brand_id, model_id, status ('ok'|'soon'|'exp'), warn_day (int ≥ 0), contract_mode (''|'yes'|'no'), q`.

- [x] **Step 1: `PrepickTrackingRowLoader`** — 1 truy vấn SQL + làm giàu bằng PHP:

```php
<?php

namespace Modules\Finance\Services\PrepickTracking;

use Illuminate\Support\Facades\DB;
use Modules\Finance\Services\PrepickConfigService;
use Modules\Finance\Services\PrepickLotContractService;

/**
 * Nạp TẤT CẢ dòng hàng giữ còn tồn theo bộ lọc rồi gắn trạng thái / khoá yêu cầu / hợp đồng.
 * Chỉ dòng `qty > 0` (thật ~2.400 dòng trên bảng 61.771) — số dòng còn tồn KHÔNG tăng theo thời
 * gian vì hàng giữ hết hạn sẽ bị hủy / xuất; có index `pd_company_qty_idx`.
 * Lọc hợp đồng + trạng thái làm ở PHP vì phụ thuộc kết quả gắn hợp đồng và N ngày cảnh báo.
 */
class PrepickTrackingRowLoader
{
    private $scope;
    private $config;
    private $contracts;
    private $documents;

    public function __construct(PrepickTrackingScope $scope, PrepickConfigService $config,
        PrepickLotContractService $contracts, PrepickDocumentResolver $documents)
    {
        $this->scope = $scope;
        $this->config = $config;
        $this->contracts = $contracts;
        $this->documents = $documents;
    }

    public function warnDay($request): int
    {
        $v = $request->input('warn_day');

        return ($v === null || $v === '' || (int) $v < 0) ? $this->config->warningDay() : (int) $v;
    }

    /** @return array[] row (hình dạng ở Task 7) */
    public function load($request, bool $withDocuments = false): array
    {
        $companyId = $this->scope->companyIdFor($request);
        $query = DB::table('prepick_details as pd')
            ->join('products as p', 'p.id', '=', 'pd.product_id')
            ->leftJoin('brands as b', 'b.id', '=', 'p.brand_id')
            ->leftJoin('product_models as pm', 'pm.id', '=', 'p.model_id')
            ->leftJoin('employees as e', 'e.id', '=', 'pd.employee_id')
            ->leftJoin('employee_infos as ei', 'ei.id', '=', 'e.employee_info_id')
            ->leftJoin('departments as d', 'd.id', '=', 'ei.department_id')
            ->leftJoin('customers as c', 'c.id', '=', 'pd.customer_id')
            ->leftJoin('product_units as pu', function ($join) {
                $join->on('pu.product_id', '=', 'p.id')->where('pu.is_base', 1);
            })
            ->leftJoin('units as u', 'u.id', '=', 'pu.unit_id')
            ->where('pd.qty', '>', 0)
            ->select([
                'pd.id', 'pd.employee_id', 'pd.customer_id', 'pd.product_id', 'pd.company_id', 'pd.qty',
                'pd.start_date', 'pd.expire_date',
                DB::raw('DATEDIFF(pd.expire_date, CURDATE()) as days_left'),
                DB::raw('COALESCE(pd.root_objectable_type, pd.objectable_type) as root_type'),
                DB::raw('COALESCE(pd.root_objectable_id, pd.objectable_id) as root_id'),
                'ei.fullname as employee_name', 'e.code as employee_code', 'ei.department_id', 'ei.part_id',
                'd.name as department_name', 'd.code as department_code',
                'c.code as customer_code', 'c.fullname as customer_name',
                'p.code as product_code', 'p.name as product_name', 'p.brand_id', 'p.model_id',
                'b.name as brand_name', 'pm.name as model_name', 'u.name as unit_name',
            ]);

        if ($companyId === 0) {
            $query->whereRaw('1 = 0');
        } elseif ($companyId !== null) {
            $query->where('pd.company_id', $companyId);
        }
        foreach (['employee_id' => 'pd.employee_id', 'customer_id' => 'pd.customer_id',
            'brand_id' => 'p.brand_id', 'model_id' => 'p.model_id', 'department_id' => 'ei.department_id'] as $param => $col) {
            if ($request->filled($param)) {
                $query->where($col, (int) $request->input($param));
            }
        }
        $part = (string) $request->input('part_id', '');
        if ($part === 'none') {
            $query->whereNull('ei.part_id');
        } elseif ($part !== '') {
            $query->where('ei.part_id', (int) $part);
        }
        $q = trim((string) $request->input('q'));
        if ($q !== '') {
            $query->where(function ($w) use ($q) {
                $w->where('p.code', 'like', '%' . $q . '%')->orWhere('p.name', 'like', '%' . $q . '%');
            });
        }

        $raw = $query->orderBy('pd.id')->get();
        $warnDay = $this->warnDay($request);

        $contractMap = $this->contracts->forLots($raw->map(function ($r) {
            return (object) ['prepick_detail_id' => $r->id, 'product_id' => $r->product_id,
                'objectable_id' => $r->root_id, 'objectable_type' => $r->root_type];
        }));

        $rows = [];
        $status = (string) $request->input('status', '');
        $mode = (string) $request->input('contract_mode', '');
        foreach ($raw as $r) {
            $contract = $contractMap[(int) $r->id] ?? null;
            $contract = ($contract && $contract['id']) ? $contract : null;
            if (($mode === 'yes' && !$contract) || ($mode === 'no' && $contract)) {
                continue;
            }
            $days = $r->days_left === null ? null : (int) $r->days_left;
            $st = PrepickTrackingMetrics::statusOf($days, $warnDay);
            if ($status !== '' && $st !== $status) {
                continue;
            }
            $row = (array) $r;
            $row['id'] = (int) $r->id;
            foreach (['employee_id', 'customer_id', 'product_id', 'company_id', 'department_id', 'part_id', 'brand_id', 'model_id', 'root_id'] as $f) {
                $row[$f] = $r->{$f} === null ? null : (int) $r->{$f};
            }
            $row['qty'] = (float) $r->qty;
            $row['days_left'] = $days;
            $row['status'] = $st;
            $row['req_key'] = $r->root_type . '#' . $r->root_id . '|' . $r->product_id . '|' . $r->employee_id;
            $row['contract'] = $contract;
            $rows[] = $row;
        }

        if ($withDocuments) {
            $rows = $this->attachDocuments($rows);
        }

        return $rows;
    }

    /** Gắn mã + link + tên loại của PHIẾU GIỮ GỐC (chỉ gọi cho tập nhỏ: trang popup / bản in). */
    public function attachDocuments(array $rows): array
    {
        $docs = $this->documents->resolve(array_map(function ($r) {
            return [$r['root_type'], $r['root_id']];
        }, $rows));
        foreach ($rows as &$r) {
            $doc = $docs[$r['root_type'] . '#' . $r['root_id']] ?? null;
            $r['root_code'] = $doc['code'] ?? null;
            $r['root_url'] = $doc['url'] ?? null;
            $r['root_label'] = $this->documents->label($r['root_type']);
        }

        return $rows;
    }
}
```
> Ô tìm `d_q` trong popup có tìm theo mã phiếu gốc (`root_code`) → `/details` phải gắn chứng từ cho TOÀN BỘ dòng của node trước khi lọc khi `d_q` có giá trị (tập của 1 node, vài trăm dòng). Không có `d_q` thì chỉ gắn cho trang hiện tại.
> `employees.code` / `departments.code` đã kiểm có cột (02/10/2026). `ei.fullname` là tên NV (khuôn của `flatQuery()` màn cũ).

- [x] **Step 2: `PrepickExtendChain`** — số lần + lịch sử gia hạn của từng dòng (đi ngược theo lô, mỗi bậc 2 truy vấn cho cả tập):

```php
<?php

namespace Modules\Finance\Services\PrepickTracking;

use Illuminate\Support\Facades\DB;

/**
 * Chuỗi gia hạn của từng dòng hàng giữ, xếp CŨ -> MỚI. Số lần gia hạn = độ dài chuỗi —
 * CHỈ có nghĩa ở mức từng yêu cầu giữ, KHÔNG cộng lên dòng tổng (spec §9.2).
 */
class PrepickExtendChain
{
    /**
     * @param int[] $prepickDetailIds
     * @return array<int, int[]> prepick_detail_id => [ext_detail_id cũ -> mới]
     */
    public function chains(array $prepickDetailIds): array
    {
        $chains = array_fill_keys($prepickDetailIds, []);
        $cursor = array_combine($prepickDetailIds, $prepickDetailIds); // gốc -> dòng đang xét

        for ($i = 0; $i < PrepickRootResolver::MAX_DEPTH && $cursor; $i++) {
            $rows = DB::table('prepick_details')->whereIn('id', array_values(array_unique($cursor)))
                ->get(['id', 'objectable_id', 'objectable_type'])->keyBy('id');
            $extIds = [];
            foreach ($cursor as $origin => $current) {
                $row = $rows[$current] ?? null;
                if (!$row || $row->objectable_type !== PrepickRootResolver::EXTEND_TYPE) {
                    unset($cursor[$origin]);
                    continue;
                }
                $extIds[$origin] = (int) $row->objectable_id;
            }
            if (!$extIds) {
                break;
            }
            $sources = DB::table('prepick_extend_request_details')->whereIn('id', array_values($extIds))
                ->pluck('prepick_detail_id', 'id');
            foreach ($extIds as $origin => $extId) {
                array_unshift($chains[$origin], $extId);
                $next = $sources[$extId] ?? null;
                if ($next === null || (int) $next === (int) $cursor[$origin]) {
                    unset($cursor[$origin]);
                } else {
                    $cursor[$origin] = (int) $next;
                }
            }
        }

        return $chains;
    }

    /** Lịch sử chi tiết của 1 dòng cho popup. */
    public function history(int $prepickDetailId): array
    {
        $chain = $this->chains([$prepickDetailId])[$prepickDetailId] ?? [];
        if (!$chain) {
            return [];
        }
        $lines = DB::table('prepick_extend_request_details as x')
            ->join('prepick_extend_requests as r', 'r.id', '=', 'x.parent_id')
            ->leftJoin('prepick_details as src', 'src.id', '=', 'x.prepick_detail_id')
            ->leftJoin('employees as ce', 'ce.id', '=', 'r.created_by')
            ->leftJoin('employee_infos as cei', 'cei.id', '=', 'ce.employee_info_id')
            ->leftJoin('employees as ae', 'ae.id', '=', 'r.approver_id')
            ->leftJoin('employee_infos as aei', 'aei.id', '=', 'ae.employee_info_id')
            ->whereIn('x.id', $chain)
            ->get(['x.id', 'x.new_expire_date', 'x.extend_qty', 'x.unit_coefficient', 'r.id as request_id', 'r.code',
                'r.approved_time', 'src.expire_date as old_expire', 'cei.fullname as requester', 'aei.fullname as approver'])
            ->keyBy('id');

        $out = [];
        foreach ($chain as $i => $extId) {
            $l = $lines[$extId] ?? null;
            if (!$l) {
                continue;
            }
            $out[] = [
                'no' => $i + 1,
                'approved_time' => $l->approved_time,
                'code' => $l->code,
                'request_id' => (int) $l->request_id,
                'old_expire' => $l->old_expire,
                'new_expire' => $l->new_expire_date,
                'extend_qty' => (float) $l->extend_qty * (float) ($l->unit_coefficient ?: 1),
                'requester' => $l->requester,
                'approver' => $l->approver,
                'is_current' => $i === count($chain) - 1,
            ];
        }

        return $out;
    }
}
```
> ⚠️ `old_expire` lấy `expire_date` HIỆN TẠI của dòng nguồn — đúng vì gia hạn tạo dòng MỚI, dòng nguồn giữ nguyên hạn cũ. Kiểm bằng 1 dòng thật có ≥ 3 lần gia hạn: hạn mới của lần k = hạn cũ của lần k+1.

- [x] **Step 3: `PrepickTrackingReportService`**

```php
<?php

namespace Modules\Finance\Services\PrepickTracking;

use Illuminate\Support\Facades\DB;

class PrepickTrackingReportService
{
    const STOCK_ACTIVE_WAREHOUSE = 1;

    private $loader;
    private $scope;
    private $chain;

    public function __construct(PrepickTrackingRowLoader $loader, PrepickTrackingScope $scope, PrepickExtendChain $chain)
    {
        $this->loader = $loader;
        $this->scope = $scope;
        $this->chain = $chain;
    }

    public function criteria($request): string
    {
        return $request->input('criteria') === 'product' ? 'product' : 'employee';
    }

    public function report($request): array
    {
        $rows = $this->loader->load($request);
        $criteria = $this->criteria($request);
        $depth = max(1, min(3, (int) $request->input('depth', 2)));
        $tree = PrepickTrackingTree::build($rows, $criteria, (string) $request->input('sort_name', ''), $depth);
        $page = PrepickTrackingTree::paginate($tree, (int) $request->input('page', 1), (int) $request->input('per_page', 25));

        $data = [
            'summary' => [
                'employees' => count(array_unique(array_column($rows, 'employee_id'))),
                'products' => count(array_unique(array_column($rows, 'product_id'))),
                'customers' => count(array_unique(array_filter(array_column($rows, 'customer_id')))),
            ],
            'total' => PrepickTrackingMetrics::of($rows),
            'tree' => $page['nodes'],
            'pagination' => array_diff_key($page, ['nodes' => 1]),
            'warn_day' => $this->loader->warnDay($request),
        ];
        if ($criteria === 'product') {
            $data['stock_by_product'] = $this->stockByProduct($request, array_column($page['nodes'], 'id'));
        }

        return $data;
    }

    public function children($request): array
    {
        $key = (string) $request->input('key', '');
        $rows = PrepickTrackingTree::find($this->loader->load($request), $this->criteria($request), $key);
        $dims = PrepickTrackingTree::DIMS[$this->criteria($request)];
        $depthOfKey = $key === '' ? 0 : count(explode('/', $key));
        $nodes = PrepickTrackingTree::build($rows, $this->criteria($request), (string) $request->input('sort_name', ''), 3);
        // build() dựng lại từ cấp 1 -> đi xuống đúng node `key` rồi trả con của nó.
        $current = $nodes;
        foreach (explode('/', $key) as $i => $part) {
            $prefix = implode('/', array_slice(explode('/', $key), 0, $i + 1));
            $found = null;
            foreach ($current as $n) {
                if ($n['key'] === $prefix) {
                    $found = $n;
                    break;
                }
            }
            $current = $found ? ($found['children'] ?? []) : [];
        }

        return ['nodes' => $depthOfKey < count($dims) ? $current : []];
    }

    public function details($request): array
    {
        $popup = ['q' => $request->input('d_q'), 'employee_id' => $request->input('d_employee_id'),
            'customer_id' => $request->input('d_customer_id'), 'product_id' => $request->input('d_product_id'),
            'status' => $request->input('d_status')];
        $node = PrepickTrackingTree::find($this->loader->load($request), $this->criteria($request), (string) $request->input('key', ''));
        $base = PrepickTrackingDrill::filter($node, (string) $request->input('metric', 'lots'), []);
        if (trim((string) $popup['q']) !== '') {
            $base = $this->loader->attachDocuments($base);
        }
        $rows = PrepickTrackingDrill::sort(
            PrepickTrackingDrill::filter($base, 'lots', $popup),
            (string) $request->input('sort_key', ''), (string) $request->input('sort_dir', 'asc'));

        $perPage = max(1, min(200, (int) $request->input('per_page', 20)));
        $page = max(1, (int) $request->input('page', 1));
        $slice = array_slice($rows, ($page - 1) * $perPage, $perPage);
        if (!isset($slice[0]['root_code'])) {
            $slice = $this->loader->attachDocuments($slice);
        }

        return [
            'rows' => $this->decorate($slice),
            'total' => count($rows),
            'counts' => [
                'products' => count(array_unique(array_column($rows, 'product_id'))),
                'reqs' => count(array_unique(array_column($rows, 'req_key'))),
                'units' => array_values(array_unique(array_filter(array_column($rows, 'unit_name')))),
            ],
            // Ô lọc trong popup chỉ liệt kê giá trị có trong tập của node (trước lọc popup).
            'options' => [
                'employees' => $this->optionsOf($base, 'employee_id', 'employee_name'),
                'customers' => $this->optionsOf($base, 'customer_id', 'customer_name'),
                'products' => $this->optionsOf($base, 'product_id', 'product_name', 'product_code'),
            ],
        ];
    }

    /** Thêm số lần gia hạn + tổng thanh toán cho 1 trang (cấm N+1: mỗi thứ 1 lượt truy vấn). */
    public function decorate(array $rows): array
    {
        $chains = $this->chain->chains(array_column($rows, 'id'));
        $paid = $this->paidOf(array_filter(array_column($rows, 'contract')));
        foreach ($rows as &$r) {
            $r['extend_count'] = count($chains[$r['id']] ?? []);
            $c = $r['contract'];
            $r['paid'] = $c ? ($paid[$c['type'] . '#' . $c['id']] ?? 0.0) : null;
        }

        return $rows;
    }

    /** Tổng `income_money_real` của phiếu thu ĐÃ DUYỆT (status 3) theo từng hợp đồng. */
    public function paidOf(array $contracts): array
    {
        $out = [];
        $byType = [];
        foreach ($contracts as $c) {
            $byType[$c['type']][] = (int) $c['id'];
        }
        foreach ($byType as $type => $ids) {
            $sums = DB::table('bill_income_details as bid')
                ->join('bill_incomes as bi', 'bi.id', '=', 'bid.parent_id')
                ->where('bi.status', 3)
                ->where('bid.objectable_type', $type)
                ->whereIn('bid.objectable_id', array_values(array_unique($ids)))
                ->groupBy('bid.objectable_id')
                ->pluck(DB::raw('SUM(bid.income_money_real)'), 'bid.objectable_id');
            foreach ($sums as $id => $sum) {
                $out[$type . '#' . $id] = (float) $sum;
            }
        }

        return $out;
    }

    public function payments($request): array
    {
        $type = (string) $request->input('contract_type');
        $id = (int) $request->input('contract_id');
        $table = app(\Modules\Finance\Services\PrepickLotContractService::class)->tableOf($type);
        if (!$table || !$id) {
            return ['contract' => null, 'paid' => 0, 'rows' => []];
        }
        $contract = DB::table($table)->where('id', $id)->first(['code', 'total_after_vat']);
        $rows = DB::table('bill_income_details as bid')
            ->join('bill_incomes as bi', 'bi.id', '=', 'bid.parent_id')
            ->where('bi.status', 3)->where('bid.objectable_type', $type)->where('bid.objectable_id', $id)
            ->groupBy('bi.id', 'bi.code', 'bi.date_accounting', 'bi.payer', 'bi.note')
            ->orderByDesc('bi.date_accounting')->orderByDesc('bi.id')
            ->get(['bi.id', 'bi.code', 'bi.date_accounting as date', 'bi.payer', 'bi.note',
                DB::raw('SUM(bid.income_money_real) as amount')]);

        return [
            'contract' => $contract ? ['code' => $contract->code, 'value' => (float) $contract->total_after_vat] : null,
            'paid' => (float) $rows->sum('amount'),
            'rows' => $rows->map(function ($r) {
                return ['id' => (int) $r->id, 'code' => $r->code, 'date' => $r->date, 'payer' => $r->payer,
                    'amount' => (float) $r->amount, 'note' => $r->note];
            })->values()->all(),
        ];
    }

    /** Tồn hiện tại — CHỈ ở tiêu chí Hàng hoá; "Tất cả công ty" thì cộng mọi công ty. */
    public function stockByProduct($request, array $productIds): array
    {
        if (!$productIds) {
            return [];
        }
        $q = DB::table('accounting_stocks as acs')
            ->leftJoin('accounting_warehouses as acw', 'acs.accounting_warehouse_id', '=', 'acw.id')
            ->whereNotNull('acs.stock_id')->whereIn('acs.product_id', $productIds)
            ->groupBy('acs.product_id');
        $companyId = $this->scope->companyIdFor($request);
        if ($companyId === 0) {
            return [];
        }
        if ($companyId !== null) {
            $q->where('acw.company_id', $companyId);
        }

        return $q->pluck(DB::raw('SUM(acs.qty)'), 'acs.product_id')->map(function ($v) {
            return (float) $v;
        })->all();
    }

    private function optionsOf(array $rows, string $id, string $name, ?string $code = null): array
    {
        $out = [];
        foreach ($rows as $r) {
            if ($r[$id] === null) {
                continue;
            }
            $out[$r[$id]] = ['id' => $r[$id], 'name' => ($code ? $r[$code] . ' - ' : '') . $r[$name]];
        }

        return array_values($out);
    }
}
```
> `stockSubQuery()` màn cũ KHÔNG lọc `acw.status` (chỉ `whereNotNull('acs.stock_id')`) — giữ y hệt để số tồn 2 màn khớp nhau; hằng `STOCK_ACTIVE_WAREHOUSE` để trống, xoá nếu không dùng.

- [x] **Step 4: `meta()`** — thêm vào service:

```php
    public function meta($request): array
    {
        $user = auth()->user();
        $info = $user->info ?? null;
        $rowsAll = $this->loader->load($request->duplicate(array_intersect_key($request->all(), ['company_id' => 1])));

        $deptId = $request->input('department_id');
        $deptRows = $deptId ? array_filter($rowsAll, function ($r) use ($deptId) {
            return (int) $r['department_id'] === (int) $deptId;
        }) : [];
        $partIds = array_values(array_unique(array_filter(array_column($deptRows, 'part_id'))));
        $hasUnassigned = (bool) array_filter($deptRows, function ($r) {
            return $r['part_id'] === null;
        });
        $deptHasParts = $deptId ? DB::table('parts')->where('department_id', $deptId)->exists() : false;

        return [
            'can_view_all_companies' => $this->scope->canViewAllCompanies(),
            'own_company_id' => $this->scope->ownCompanyId(),
            'own_department_id' => $info ? (int) $info->department_id : null,
            'own_part_id' => $info && $info->part_id ? (int) $info->part_id : null,
            'own_employee_id' => (int) auth()->id(),
            'warning_day' => $this->loader->warnDay($request->duplicate([])),
            'companies' => $this->scope->canViewAllCompanies()
                ? DB::table('companies')->orderBy('name')->get(['id', 'name'])->all()
                : DB::table('companies')->where('id', $this->scope->ownCompanyId())->get(['id', 'name'])->all(),
            'departments' => $this->distinctOf($rowsAll, 'department_id', 'department_name'),
            'part_state' => !$deptId ? 'need_department' : (!$deptHasParts ? 'no_parts' : 'ok'),
            'parts' => $partIds ? DB::table('parts')->whereIn('id', $partIds)->orderBy('name')->get(['id', 'name'])->all() : [],
            'has_unassigned' => $hasUnassigned,
            'employees' => array_values(array_map(function ($r) {
                return ['id' => $r['employee_id'], 'name' => $r['employee_name'], 'code' => $r['employee_code'],
                    'department_id' => $r['department_id'], 'department_code' => $r['department_code'], 'part_id' => $r['part_id']];
            }, $this->uniqueBy($rowsAll, 'employee_id'))),
            'customers' => $this->distinctOf($rowsAll, 'customer_id', 'customer_name'),
            'brands' => $this->distinctOf($rowsAll, 'brand_id', 'brand_name'),
            'models' => $this->distinctOf($rowsAll, 'model_id', 'model_name'),
        ];
    }

    private function uniqueBy(array $rows, string $field): array
    {
        $out = [];
        foreach ($rows as $r) {
            if ($r[$field] !== null && !isset($out[$r[$field]])) {
                $out[$r[$field]] = $r;
            }
        }

        return $out;
    }

    private function distinctOf(array $rows, string $id, string $name): array
    {
        $list = array_map(function ($r) use ($id, $name) {
            return ['id' => $r[$id], 'name' => $r[$name] ?: '—'];
        }, $this->uniqueBy($rows, $id));
        usort($list, function ($a, $b) {
            return strcmp(mb_strtolower($a['name'], 'UTF-8'), mb_strtolower($b['name'], 'UTF-8'));
        });

        return $list;
    }
```
> Ô "Bộ phận" 3 trạng thái (spec §5.2): `need_department` → khoá "Chọn phòng ban trước" · `no_parts` → khoá "Phòng này chưa chia bộ phận" · `ok` → liệt kê `parts` + mục "Chưa phân bộ phận" (`none`) khi `has_unassigned`. Kiểm `parts` có cột `status`/`deleted_at` bị khoá không — nếu có, `deptHasParts` chỉ tính bộ phận đang hoạt động.

- [x] **Step 5: Controller**

```php
<?php

namespace Modules\Finance\Http\Controllers\V1;

use Illuminate\Http\Request;
use Modules\Finance\Services\PrepickTracking\PrepickExtendChain;
use Modules\Finance\Services\PrepickTracking\PrepickTrackingPrintService;
use Modules\Finance\Services\PrepickTracking\PrepickTrackingReportService;

/**
 * Báo cáo theo dõi giữ hàng (`/sale/prepick-tracking`). CHỈ ĐỌC. KHÔNG gate vào màn — mọi user
 * đăng nhập đều xem được hàng giữ của công ty mình; quyền "theo tổng công ty" chỉ mở rộng phạm
 * vi công ty (xử ở PrepickTrackingScope). Màn cũ /finance/prepick-stocks không dùng controller này.
 */
class PrepickTrackingController extends ApiController
{
    private $service;

    public function __construct(PrepickTrackingReportService $service)
    {
        $this->service = $service;
    }

    public function meta(Request $request)
    {
        return $this->responseJson('Lấy dữ liệu thành công', 200, $this->service->meta($request));
    }

    public function index(Request $request)
    {
        return $this->responseJson('Lấy dữ liệu thành công', 200, $this->service->report($request));
    }

    public function children(Request $request)
    {
        return $this->responseJson('Lấy dữ liệu thành công', 200, $this->service->children($request));
    }

    public function details(Request $request)
    {
        return $this->responseJson('Lấy dữ liệu thành công', 200, $this->service->details($request));
    }

    public function extendHistory(Request $request, PrepickExtendChain $chain)
    {
        $id = (int) $request->input('prepick_detail_id');
        // Chặn đọc lịch sử dòng ngoài phạm vi công ty: dòng phải nằm trong tập báo cáo của user.
        $visible = $this->service->rowById($request, $id);
        if (!$visible) {
            return $this->responseJson('Không tìm thấy hàng giữ', 404);
        }

        return $this->responseJson('Lấy dữ liệu thành công', 200, [
            'rows' => $chain->history($id),
            'unit_name' => $visible['unit_name'],
            'root_code' => $visible['root_code'],
        ]);
    }

    public function payments(Request $request)
    {
        return $this->responseJson('Lấy dữ liệu thành công', 200, $this->service->payments($request));
    }

    public function printListData(Request $request, PrepickTrackingPrintService $print)
    {
        return $this->responseJson('Lấy dữ liệu thành công', 200, $print->render($request));
    }

    public function export(Request $request, PrepickTrackingPrintService $print)
    {
        return $print->download($request);
    }
}
```
Thêm vào service:
```php
    /** Dòng `id` nếu nằm trong phạm vi xem (bỏ qua mọi bộ lọc khác trừ công ty). */
    public function rowById($request, int $id): ?array
    {
        if ($id <= 0) {
            return null;
        }
        $rows = $this->loader->load($request->duplicate(array_intersect_key($request->all(), ['company_id' => 1])));
        foreach ($rows as $r) {
            if ($r['id'] === $id) {
                return $this->loader->attachDocuments([$r])[0];
            }
        }

        return null;
    }
```
> `payments` cũng phải chặn hợp đồng ngoài phạm vi: chỉ trả khi có ít nhất 1 dòng trong phạm vi mang đúng hợp đồng đó (dùng `load()` rồi `array_filter` theo `contract.id/type`); không có → 404. Viết vào `payments()` trước khi truy vấn tiền.

- [x] **Step 6: Route** — sau khối `prepick-expiring`:

```php
    // Bao cao theo doi giu hang (/sale/prepick-tracking) — CHI DOC, KHONG gate vao man.
    // Khong dung chung route voi /prepick-stocks: man cu van chay song song (chot 02/10/2026).
    Route::group(['prefix' => '/prepick-tracking'], function () {
        Route::get('/', [PrepickTrackingController::class, 'index']);
        Route::get('/meta', [PrepickTrackingController::class, 'meta']);
        Route::get('/children', [PrepickTrackingController::class, 'children']);
        Route::get('/details', [PrepickTrackingController::class, 'details']);
        Route::get('/extends', [PrepickTrackingController::class, 'extendHistory']);
        Route::get('/payments', [PrepickTrackingController::class, 'payments']);
        Route::get('/print-list-data', [PrepickTrackingController::class, 'printListData']);
        Route::get('/export', [PrepickTrackingController::class, 'export']);
    });
```
+ `use Modules\Finance\Http\Controllers\V1\PrepickTrackingController;` ở đầu file. `export` tải trực tiếp qua `?token=` → kiểm guard `auth:api` có đọc `token` từ query (cách các màn khác đang tải Excel) — xem `routes` của `assign/report/prospective-project-results/export`.

- [x] **Step 7: Test API — phân quyền + khớp số**

```php
<?php

namespace Modules\Finance\Tests\Feature;

use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Support\Facades\DB;
use Tests\TestCase;

class PrepickTrackingApiTest extends TestCase
{
    use DatabaseTransactions;

    const BASE = '/api/v1/finance/prepick-tracking';

    public function test_requires_login(): void
    {
        $this->getJson(self::BASE)->assertStatus(401);
    }

    /** Nhân viên thường của công ty có hàng giữ — không quyền tổng công ty. */
    private function actAsPlainEmployeeOfCompanyWithHolds(): int
    {
        $companyId = (int) DB::table('prepick_details')->where('qty', '>', 0)->value('company_id');
        $id = DB::table('employees as e')->join('employee_infos as ei', 'ei.id', '=', 'e.employee_info_id')
            ->where('ei.company_id', $companyId)
            ->whereNotIn('e.id', DB::table('employee_has_roles')->where('role_id', 18)->pluck('employee_id'))
            ->value('e.id');
        if (!$companyId || !$id) {
            $this->markTestSkipped('Thiếu dữ liệu');
        }
        DB::table('employee_has_permissions')->where('employee_id', $id)->delete();
        DB::table('employee_has_roles')->where('employee_id', $id)->delete();
        $this->actingAs(\App\Models\Employee::find($id), 'api');

        return $companyId;
    }

    public function test_without_permission_sees_own_company_only_even_if_asking_other(): void
    {
        $own = $this->actAsPlainEmployeeOfCompanyWithHolds();
        $res = $this->getJson(self::BASE . '?company_id=999999&criteria=product&per_page=100')->assertOk()->json('data');
        $expected = DB::table('prepick_details')->where('qty', '>', 0)->where('company_id', $own)
            ->distinct()->count('product_id');
        $this->assertSame($expected, $res['summary']['products']);
        $this->assertFalse($this->getJson(self::BASE . '/meta')->json('data.can_view_all_companies'));
    }

    public function test_level_one_totals_add_up_to_grand_total_rows(): void
    {
        $this->actAsPlainEmployeeOfCompanyWithHolds();
        $res = $this->getJson(self::BASE . '?criteria=employee&per_page=100')->assertOk()->json('data');
        $this->assertSame($res['total']['lots'], array_sum(array_map(function ($n) {
            return $n['metrics']['lots'];
        }, $res['tree'])));
        $this->assertSame($res['total']['lots'], $res['total']['ok'] + $res['total']['soon'] + $res['total']['exp']);
    }

    public function test_details_count_matches_summary_request_number(): void
    {
        $this->actAsPlainEmployeeOfCompanyWithHolds();
        $total = $this->getJson(self::BASE . '?per_page=1')->json('data.total');
        $d = $this->getJson(self::BASE . '/details?metric=reqs_exp&per_page=1')->json('data');
        $this->assertSame($total['reqs_exp'], $d['counts']['reqs']);
    }

    public function test_extends_of_row_outside_scope_is_404(): void
    {
        $own = $this->actAsPlainEmployeeOfCompanyWithHolds();
        $other = DB::table('prepick_details')->where('qty', '>', 0)->where('company_id', '<>', $own)->value('id');
        if (!$other) {
            $this->markTestSkipped('Chỉ 1 công ty có hàng giữ');
        }
        $this->getJson(self::BASE . '/extends?prepick_detail_id=' . $other)->assertStatus(404);
    }
}
```

- [x] **Step 8: Chạy toàn bộ test PrepickTracking PASS + đo thời gian phản hồi thật**

```bash
/opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit Modules/Finance/Tests/Unit/PrepickTracking* Modules/Finance/Tests/Unit/PrepickRootResolverTest.php Modules/Finance/Tests/Feature/PrepickTracking*
```
Đo bằng curl có token super admin trên dữ liệu thật: `/` (cả 2 tiêu chí, "Tất cả công ty"), `/details` node lớn nhất, `/meta`. **Ngưỡng: < 1s mỗi endpoint.** Ghi số đo vào checkpoint + `design.md` (đây là việc "chốt cỡ trang + ngưỡng lazy" của spec §13.3). Nếu `/` > 1s → bật `depth=2` mặc định là đã lazy cấp 3; nếu vẫn chậm thì đo lại từng phần (SQL / forLots / build) trước khi sửa.

- [x] **Step 9: Commit** `feat(prepick-tracking): API báo cáo theo dõi giữ hàng (meta, cây, chi tiết, gia hạn, phiếu thu)`.

---

### Task 9: In + Xuất Excel (BE)

**Files:**
- Create: `hrm-api/Modules/Finance/Services/PrepickTracking/PrepickTrackingPrintService.php`
- Create: `hrm-api/Modules/Finance/Resources/views/prints/prepick-tracking.blade.php` (kế thừa `_layout.blade.php` như `prepick-stock-list.blade.php`)
- Create: `hrm-api/Modules/Finance/Exports/PrepickTrackingExport.php` + `hrm-api/Modules/Finance/Resources/views/exports/prepick-tracking.blade.php`
- Test: `hrm-api/Modules/Finance/Tests/Unit/PrepickTrackingFlattenTest.php`

**Interfaces:**
- Produces: `PrepickTrackingPrintService::flatten(array $nodes, string $criteria): array` — dòng `['stt'=>'1.2','depth'=>int,'dim'=>..., 'label'=>..., 'unit'=>..., 'model'=>..., 'brand'=>..., 'stock'=>?float, 'measure'=>['value'=>float|int, 'is_codes'=>bool], 'ok'=>..., 'soon'=>..., 'exp'=>...]` — đo theo DÒNG: `only_product_id` ≠ null → `qty*`, ngược lại `codes*` (hiện "N Mã" ở bản in; Excel ghi số + cột "Đơn vị đo" = "Mã").
- `render($request): array` → `{template, truncated, total, limit}`; `download($request)` → `Excel::download(...)`.
- `mode=tree`: cây ĐỦ MỌI CẤP (`depth=3`), KHÔNG phân trang, KHÔNG theo cấp đang bung. `mode=detail`: danh sách chi tiết theo khoá popup (`key`, `metric`, `d_*`, sort) — đủ 15 cột popup (bỏ nút Gia hạn/Huỷ giữ). Trần in 2.000 dòng (`truncated=true` + dòng cảnh báo trên bản in); Excel không trần.
- Dòng đầu bản in = **tóm tắt bộ lọc đang áp** (`describeFilters()`): công ty · phòng ban · bộ phận · NV · KH · thương hiệu · model · trạng thái · cảnh báo trước N ngày · hình thức giữ · tìm hàng hoá — chỉ in ô có giá trị.

- [x] **Step 1: Test `flatten` (thất bại)**

```php
<?php

namespace Modules\Finance\Tests\Unit;

use Modules\Finance\Services\PrepickTracking\PrepickTrackingPrintService as P;
use Modules\Finance\Services\PrepickTracking\PrepickTrackingTree;
use PHPUnit\Framework\TestCase;

class PrepickTrackingFlattenTest extends TestCase
{
    public function test_flatten_numbers_and_measure_by_row(): void
    {
        $row = function ($id, $prd, $qty, $status) {
            return PrepickTrackingMetricsTest::row(['id' => $id, 'department_id' => 1, 'department_name' => 'P1',
                'employee_id' => 10, 'employee_name' => 'NV', 'employee_code' => 'E', 'product_id' => $prd,
                'product_code' => 'M' . $prd, 'product_name' => 'H' . $prd, 'unit_name' => 'Cái',
                'brand_name' => 'B', 'model_name' => 'X', 'qty' => $qty, 'status' => $status, 'root_id' => $id]);
        };
        $tree = PrepickTrackingTree::build([$row(1, 100, 5, 'ok'), $row(2, 101, 3, 'exp')], 'employee', '', 3);
        $flat = P::flatten($tree, 'employee');

        $this->assertSame(['1', '1.1', '1.1.1', '1.1.2'], array_column($flat, 'stt'));
        $this->assertTrue($flat[0]['measure']['is_codes']);       // phòng ban gom 2 mã
        $this->assertSame(2, $flat[0]['measure']['value']);
        $this->assertFalse($flat[2]['measure']['is_codes']);      // dòng hàng hoá -> số lượng
        $this->assertSame(3.0, $flat[2]['measure']['value']);      // quá hạn nhiều nhất lên trước: hàng 101
        $this->assertSame(3.0, $flat[2]['exp']);
    }
}
```

- [x] **Step 2: Viết `PrepickTrackingPrintService`** — khuôn theo `ProspectiveProjectResultPrintService` (`flattenTree`) + `PrepickStockReportService::renderPrintList()`:

```php
    public static function flatten(array $nodes, string $criteria, string $prefix = '', int $depth = 0): array
    {
        $out = [];
        foreach (array_values($nodes) as $i => $n) {
            $stt = $prefix === '' ? (string) ($i + 1) : $prefix . '.' . ($i + 1);
            $m = $n['metrics'];
            $single = $m['only_product_id'] !== null;
            $out[] = [
                'stt' => $stt, 'depth' => $depth, 'dim' => $n['dim'],
                'label' => $n['dim'] === 'product' ? $n['code'] . ' - ' . $n['name']
                    : ($n['dim'] === 'emp' && $criteria === 'product' && $n['sub'] ? $n['name'] . ' - ' . $n['sub'] : $n['name']),
                'unit' => $n['unit_name'], 'model' => $n['model_name'], 'brand' => $n['brand_name'],
                'stock' => $n['stock'] ?? null,
                'measure' => ['value' => $single ? $m['qty'] : $m['codes'], 'is_codes' => !$single],
                'ok' => $single ? $m['qty_ok'] : $m['codes_ok'],
                'soon' => $single ? $m['qty_soon'] : $m['codes_soon'],
                'exp' => $single ? $m['qty_exp'] : $m['codes_exp'],
            ];
            if (!empty($n['children'])) {
                $out = array_merge($out, self::flatten($n['children'], $criteria, $stt, $depth + 1));
            }
        }

        return $out;
    }
```
`render()` / `download()`: lấy `$rows = loader->load($request)`; `mode=tree` → `PrepickTrackingTree::build($rows, $criteria, sort_name, 3)`, gắn `stock` vào node hàng hoá (tiêu chí Hàng hoá) bằng `stockByProduct()`, `flatten()`, thêm dòng TỔNG từ `PrepickTrackingMetrics::of($rows)`; `mode=detail` → cùng đường với `details()` nhưng không cắt trang, `decorate()` theo lô 500 dòng. Blade in: A4 ngang, letterhead `companies.header` (như `prepick-stock-list`), thụt lề cây bằng `&nbsp;` × 4 × depth, cột Tồn hiện tại chỉ khi `criteria=product`. Blade Excel: ô số in `excelNumber()` + `data-format="#,##0.##"`, thụt lề bằng ký tự `\u{00A0}` (Excel cắt dấu cách đầu ô), dòng tổng in đậm; tên file `bao-cao-theo-doi-giu-hang.xlsx` / `chi-tiet-hang-giu.xlsx`.

- [x] **Step 3: PASS test flatten; kiểm tay** — mở `GET /print-list-data?mode=tree` (trang 2 đang xem) và `mode=detail&metric=exp` → đếm dòng trong `template` = số dòng cây đủ cấp / số dòng chi tiết; tải `/export?mode=tree` → mở bằng PhpSpreadsheet trong tinker, kiểm ô số `getDataType() === 'n'` và không có chữ "Gia hạn"/"Huỷ giữ" trong file.

- [x] **Step 4: Commit** `feat(prepick-tracking): in + xuất Excel (bảng theo dõi đủ cấp, danh sách chi tiết)`.

---

### Task 10: Màn lập phiếu Gia hạn / Huỷ giữ nhận `prepick_detail_id`

**Files:**
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/PrepickExtendRequestController.php` — action `stock` (dòng 71-92)
- Modify: `hrm-api/Modules/Finance/Http/Controllers/V1/PrepickCancelRequestController.php` — thêm action `lot` + route `GET prepick-cancel-requests/lot`
- Modify: `hrm-api/Modules/Finance/Routes/api.php`
- Test: `hrm-api/Modules/Finance/Tests/Feature/PrepickFocusLotTest.php`

**Interfaces:**
- `GET finance/prepick-extend-requests/stock?prepick_detail_id=X` → thêm khoá `focus`: `null` (không truyền) | `{prepick_detail_id, in_list:bool, message:string|null}`. Dòng của chính user nhưng hạn còn xa ngưỡng → `in_list=false`, `message = "Hàng này còn N ngày mới tới hạn, chưa lập được yêu cầu gia hạn (chỉ lập được khi còn ≤ W ngày)."`. Dòng không phải của user / không còn tồn → `message = "Không tìm thấy hàng giữ cần gia hạn hoặc hàng này không thuộc về bạn."`. Danh sách `items` KHÔNG đổi (không nới `dataToCreate()` — chốt #5).
- `GET finance/prepick-cancel-requests/lot?prepick_detail_id=X` → `{customer_id, customer_name, product_id, product_code, product_name, expire_date, qty}` khi dòng thuộc `auth()->id()` và `qty > 0`; ngược lại 404.

- [x] **Step 1: Test (thất bại)** — 3 ca: extend dòng xa hạn → `focus.in_list=false` + message chứa "còn"; extend dòng trong ngưỡng → `in_list=true`; cancel `lot` của người khác → 404. Dựng dòng bằng `PrepickStockService::addLot()` cho chính nhân viên đăng nhập (khuôn Task 3), hạn = hôm nay + 60 ngày và hôm nay + 1 ngày.

- [x] **Step 2: Sửa `stock`**

```php
        $focus = null;
        $focusId = (int) $request->input('prepick_detail_id');
        if ($focusId > 0) {
            $items = $items ?? $this->service->dataToCreate($employeeId, $companyId);
            $inList = in_array($focusId, array_column($items, 'prepick_detail_id'), true);
            $lot = DB::table('prepick_details')->where('id', $focusId)->where('employee_id', $employeeId)
                ->where('qty', '>', 0)->first(['expire_date']);
            $message = null;
            if (!$lot) {
                $message = 'Không tìm thấy hàng giữ cần gia hạn hoặc hàng này không thuộc về bạn.';
            } elseif (!$inList) {
                $days = Carbon::today()->diffInDays(Carbon::parse($lot->expire_date), false);
                $message = "Hàng này còn {$days} ngày mới tới hạn, chưa lập được yêu cầu gia hạn "
                    . '(chỉ lập được khi còn ≤ ' . $this->service->warningDay() . ' ngày).';
            }
            $focus = ['prepick_detail_id' => $focusId, 'in_list' => $inList, 'message' => $message];
        }
```
(gán `$items = $this->service->dataToCreate(...)` 1 lần rồi dùng cho cả `items` và `focus`; thêm `'focus' => $focus` vào mảng trả về; nếu service chưa có `warningDay()` thì gọi `PrepickConfigService::warningDay()`).

- [x] **Step 3: Thêm `lot` cho phiếu hủy** — đọc `prepick_details` join `customers`, `products`; điều kiện `employee_id = auth()->id()`, `qty > 0`; trả 404 `'Không tìm thấy hàng giữ cần hủy'` nếu không có.

- [x] **Step 4: PASS; commit** `feat(prepick): màn lập gia hạn / hủy giữ nhận prepick_detail_id từ báo cáo theo dõi`.

---

## Phase 3 — FE (`hrm-client`)

> Giao diện bám mockup đã duyệt (`bao-cao-theo-doi-giu-hang.html`) — PORT CSS từ mockup (dòng 7-2406) vào `<style scoped>` của từng component, KHÔNG lấy CSS của mockup HTML khác. Khung dùng chung: `V2BaseSmartFilterPanel`, `components/report/V2BaseReportModal.vue`, `V2BaseTableScroll`, `V2BasePagination`, `reportPrintPreviewMixin`, `PageTitleMixin`. Khuôn trang mẫu: `pages/assign/report/prospective-project-results/` (TKT) và `pages/assign/report/employee-work-performance/` (cờ quyền fail-closed).
> Bẫy đã trả giá ở mockup (spec §9.1.1, STATUS vòng 9-10) — PHẢI tránh lại: `min-width` cứng 1280/1740px của style TKT · ô tiêu đề cột hạn tô màu phải trả về teal · `.minutes-modal__body` flex co sập bảng (đã thay bằng `V2BaseReportModal`, vẫn đo lại) · ghim cột dùng `offsetLeft` KHÔNG `getBoundingClientRect` (popup có `transform: scale(.96)`) · ô ghim nền đặc + viền bằng `box-shadow inset` · đổi thứ tự `colgroup` phải đổi cả thứ tự render ô.

### Task 11: Menu + khung trang + bộ lọc

**Files:**
- Modify: `hrm-client/components/subsystem-menu/sale-hub.js` — khối "Báo cáo" (dòng 217-238), thêm mục cuối
- Create: `hrm-client/pages/sale/prepick-tracking/index.vue`
- Create: `hrm-client/pages/sale/prepick-tracking/api.js`
- Create: `hrm-client/pages/sale/prepick-tracking/format.js`

**Interfaces:**
- `api.js`: `export const API = 'finance/prepick-tracking'`.
- `format.js`: `num(v)` (`toLocaleString('en-US', { maximumFractionDigits: 2 })`), `dmy(ymd)`, `statusText = { ok: 'Trong hạn', soon: 'Sắp hết hạn', exp: 'Hết hạn' }`, `STATUS_COLOR = { ok: '#15803d', soon: '#b45309', exp: '#b91c1c' }`, `measure(metrics, key)` → `{ value, isCodes }` theo quy tắc dòng (`only_product_id`), `daysNote(daysLeft)` → "còn N ngày" / "quá hạn N ngày" / "hết hạn hôm nay".
- Page `data()`: `filters` = `{ criteria:'employee', company_id, department_id:'', part_id:'', employee_id:'', customer_id:'', brand_id:'', model_id:'', status:'', warn_day:null, contract_mode:'', q:'' }`, `level` (1..3), `sortName`, `page`, `perPage: 25`, `mine:false`, `mineSnapshot:null`, `meta`, `report`, `loading`, `canViewAll:false`.
- `buildParams(extra)` — gộp `filters` + `level→depth` + `sort_name` + `page/per_page`, bỏ `''`/`null`; KHÔNG BAO GIỜ gửi `company_id` khi `!canViewAll` (BE cũng bỏ qua, nhưng FE không được tỏ ra có quyền).

- [x] **Step 1: Menu**

```js
            // 02/10/2026 — Báo cáo theo dõi giữ hàng (feature bao-cao-theo-doi-giu-hang). KHÔNG khai
            // `isShow`: middleware checkPermission sẽ đá người không có quyền ra 404, trái với chốt
            // "mọi user đăng nhập đều vào được, quyền chỉ mở rộng phạm vi công ty".
            { title: 'Hàng giữ', screens: [{ n: 'Báo cáo theo dõi giữ hàng', link: '/sale/prepick-tracking' }] },
```

- [x] **Step 2: Khung trang** — `layout: 'default-sidebar'` (BẮT BUỘC, thiếu là màn biến mất im lặng), `mixins: [PageTitleMixin, reportPrintPreviewMixin]`, `head() { return { title: 'Báo cáo theo dõi giữ hàng' } }`. `created()`:

```js
    async created() {
        // Fail-closed: chỉ bật từ store, KHÔNG bao giờ gán literal true.
        this.canViewAll = this.hasAPermission('Xem báo cáo giữ hàng theo tổng công ty')
        // Khoá phạm vi TRƯỚC lần render/tải đầu: không quyền thì không có khoảnh khắc nào xem công ty khác.
        this.filters.company_id = this.ownCompanyId
        await this.loadMeta()
        await this.loadReport()
    },
```
`ownCompanyId` computed = `this.$store.state.current_employee_info?.company_role ?? this.$store.state.current_employee?.company_id ?? null` (khuôn `employee-work-performance`). Sau `loadMeta()` đối chiếu `meta.can_view_all_companies` — BE là nguồn sự thật: nếu BE nói `false` mà FE đang `true` (cache quyền cũ) → ép `canViewAll=false`.

- [x] **Step 3: Thanh lọc** — `V2BaseSmartFilterPanel table="sale_prepick_tracking" :collapsed reset-button-text="Xóa lọc"`. Thứ tự ô theo mockup (đo lại thứ tự trong mockup `bind()` dòng 4760+): nút **Hàng giữ của tôi** (slot `#title-suffix` hoặc ô đầu) · Tiêu chí (`V2BaseRadio` option `{value,label}` — KHÔNG `{id,name}`) · Công ty (chỉ khi `canViewAll`, có mục `{id:'all', name:'Tất cả công ty'}`; không quyền → nhãn tĩnh `.company-fixed` ghi tên công ty) · Phòng ban · Bộ phận (3 trạng thái theo `meta.part_state`) · Nhân viên (khuôn `Tên - Mã phòng - Mã NV`, lọc theo bộ phận đang chọn) · Khách hàng · Thương hiệu · Model · Trạng thái hạn giữ · Cảnh báo trước N ngày (number, placeholder = `meta.warning_day`) · Hình thức giữ · Tìm hàng hoá. KHÔNG dùng `V2BaseCompanyDepartmentFilter` (nó tự xoá cascade về `''` và liệt kê NV toàn công ty, trong khi ô ở đây chỉ liệt kê người ĐANG giữ hàng) — tự viết cascade bằng watcher:
  - đổi `company_id` → reset phòng/bộ phận/NV + `loadMeta()`; đổi `department_id` → reset `part_id`, `employee_id` + `loadMeta()`; đổi `part_id` → reset `employee_id`.
  - Mọi thay đổi bộ lọc / tiêu chí / sort → `page = 1`.
  - `@reset` ("Xoá lọc"): trả mọi ô về mặc định NHƯNG giữ `company_id` khi `!canViewAll`; tắt `mine`.
- [x] **Step 4: "Hàng giữ của tôi"** (spec §5.1) — `enableMine()` chụp 6 giá trị `{criteria, company_id, department_id, part_id, employee_id, level}` vào `mineSnapshot`, ép `criteria='employee'`, `company_id=ownCompanyId` (CHỈ khi `canViewAll`), `department_id=meta.own_department_id`, `part_id=meta.own_part_id || ''` (KHÔNG ép `none`), `employee_id=meta.own_employee_id`, `level=3`. `disableMine()` bấm lại nút → khôi phục snapshot. Đổi tay 1 trong 5 ô Nhân viên/Công ty/Phòng ban/Bộ phận/Tiêu chí khi `mine=true` → `mine=false`, `mineSnapshot=null`, GIỮ giá trị mới (dùng cờ `applyingMine` để watcher không tự tắt trong lúc chính `enableMine` đang gán).
- [x] **Step 5: Kiểm bằng Playwright MCP** (client worktree cổng 3011, API cổng 8011 — `API_URL` trỏ 8011):
  - Menu hub Bán hàng có đúng 1 link `/sale/prepick-tracking` trong nhóm "Hàng giữ" (đếm bằng DOM).
  - Tài khoản KHÔNG quyền: không có ô Công ty, có nhãn tĩnh; sửa `company_id` trên query string → số tổng không đổi.
  - Ô Bộ phận ở 3 trạng thái (chọn phòng có/không có bộ phận — lấy 1 phòng có bộ phận từ `meta`).
  - Bật/tắt "Hàng giữ của tôi" khôi phục đúng 6 giá trị (đọc `vm.filters` qua `window.$nuxt`).
- [x] **Step 6: Commit** `feat(prepick-tracking): khung màn + menu Bán hàng + bộ lọc`.

### Task 12: Dải tổng hợp + bảng theo dõi cây

**Files:**
- Create: `hrm-client/pages/sale/prepick-tracking/components/TrackingSummary.vue` (port `renderSummary()` mockup dòng 3549-3640)
- Create: `hrm-client/pages/sale/prepick-tracking/components/TrackingTable.vue` (port `renderTable()` / `nodeRows()` / `measureTd()` dòng 3642-3866)
- Create: `hrm-client/pages/sale/prepick-tracking/components/DrillNum.vue` (copy `pages/assign/report/prospective-project-results/components/DrillNum.vue`)

**Interfaces:**
- `TrackingSummary` props `summary, total` · emit `drill({ key: '', metric })` — `metric` ∈ `lots|ok|soon|exp|reqs|reqs_soon|reqs_exp|emps_exp`.
- `TrackingTable` props `tree, total, criteria, level, sortName, pagination, stockByProduct, loadingKeys` · emit `drill({ key, metric })`, `expand(node)` (node có `children === null` → page gọi `/children` rồi gán `node.children = res.nodes` bằng `this.$set`), `update:level`, `update:sortName`, `page-change`, `page-size-change`.

- [x] **Step 1: Summary** — 2 khối 1 hàng: "Phạm vi đang giữ" (NV đang giữ · Hàng hoá bị giữ · Khách hàng) · "Tình trạng theo yêu cầu giữ" (Tổng yêu cầu đang giữ hàng · Yêu cầu sắp hết hạn · Yêu cầu đã hết hạn · NV có hàng giữ quá hạn). Tooltip ⓘ ghi rõ 2 nhóm sắp/đã hết hạn CHỒNG LẤN. Mọi số bấm được (`DrillNum`).
- [x] **Step 2: Bảng** — cột: STT · Nội dung theo dõi (ô chọn cấp bung trên tiêu đề; bấm tiêu đề sort A→Z → Z→A → mặc định) · Đơn vị · Model · Thương hiệu · Tồn hiện tại (CHỈ `criteria='product'`) · Số lượng giữ · Trong hạn · Sắp hết hạn · Hết hạn. Dòng TỔNG đầu bảng (từ `total`, không theo trang). STT chạy tiếp theo trang (`pagination.offset + i + 1`). 5 cột thuộc tính hàng hoá ẨN khi chưa render dòng hàng hoá nào (tính theo cây + nhánh đang bung). Ô đo dùng `measure()` — dòng nhiều mã hiện hậu tố "Mã", dòng 1 mã hiện số lượng không hậu tố. Tooltip cột hạn: "đếm chồng lấn ở dòng nhiều mã". Mã hàng `<span class="prd-code">` liền tên. Ô tiêu đề 3 cột hạn chữ teal (KHÔNG xanh/vàng/đỏ). Sort tiêu đề không đổi nền khi hover.
- [x] **Step 3: Lazy cấp 3** — `level=3` thì page gửi `depth=3`; bung tay node `children === null` → `GET ${API}/children?key=...` (kèm bộ lọc hiện tại), spinner trên dòng đó (`loadingKeys`).
- [x] **Step 4: Phân trang** — `V2BasePagination` `item-label="nhóm"` `:page-size-options="[10, 25, 50, 100]"`; đổi sort/lọc → trang 1.
- [x] **Step 5: Kiểm Playwright MCP — đo số từ DOM**: tổng cột "Số lượng giữ" của dòng TỔNG = số trên dải tổng hợp; cộng cấp 1 của MỌI trang (đổi `per_page=100`) = dòng tổng ở dòng 1-mã; bảng không sinh cuộn ngang ở 1440px và 1200px (`scrollWidth <= clientWidth`); màu `getComputedStyle` 3 tiêu đề hạn = teal; bung 1 NV ra đúng số mã = số trên ô; đổi tiêu chí → cột Tồn xuất hiện/biến mất; so từng khối với mockup (cùng cỡ chữ, khoảng cách, thứ tự).
- [x] **Step 6: Commit** `feat(prepick-tracking): dải tổng hợp + bảng theo dõi cây (lazy cấp 3, phân trang node)`.

### Task 13: Popup chi tiết + popup lịch sử gia hạn + popup phiếu thu

**Files:**
- Create: `hrm-client/pages/sale/prepick-tracking/components/HoldListModal.vue` (dựa `V2BaseReportModal`, port `DCOL` mockup dòng 3968-4116)
- Create: `hrm-client/pages/sale/prepick-tracking/components/ExtendHistoryModal.vue`
- Create: `hrm-client/pages/sale/prepick-tracking/components/PaymentListModal.vue`

**Interfaces:**
- `HoldListModal` props `visible, drillKey, metric, title, lead, baseParams, mine` · tự gọi `GET ${API}/details` · emit `close`, `print(params)`, `export(params)`, `open-extend(row)`, `open-payments(row)`.
- Cột (thứ tự CHỐT): STT · Mã hàng - Tên hàng · ĐVT · SL đang giữ · Ngày bắt đầu giữ · Hạn giữ hiện tại · Số lần gia hạn · Thương hiệu / Model · Khách hàng · Số hợp đồng · Tổng thanh toán · Nhân viên giữ · Phòng ban · Trạng thái · Phiếu giữ gốc. Ẩn Nhân viên/Phòng ban khi node đã cố định chiều đó (cố định NV thì ẩn cả Phòng ban); ẩn Trạng thái khi `metric` là 1 trạng thái. Sort 7 cột: product, qty, customer, employee, department, start_date, expire_date (chu kỳ tăng → giảm → mặc định).

- [x] **Step 1: Popup chi tiết** — tiêu đề "Đang xem <metric> theo <chiều>: <Mã - Tên | Tên NV - Phòng ban>", breadcrumb các cấp cha; dòng đếm `N mã hàng · M yêu cầu giữ · các ĐVT` (> 3 ĐVT → "K đơn vị tính"); bộ lọc riêng (tìm nhanh · Nhân viên · Khách hàng · Hàng hoá · Trạng thái) lấy từ `options` của API; ô "Hạn giữ hiện tại" tô màu theo trạng thái + dòng `daysNote`; ô "Số hợp đồng" ghi "Không theo hợp đồng" khi `contract=null`, cột Tổng thanh toán khi đó `—`; "Phiếu giữ gốc" = `root_code` (link `root_url`, tooltip `root_label`).
- [x] **Step 2: Ghim 3 cột đầu** (STT · Mã-Tên · ĐVT) — `position: sticky` + `left` tính bằng `offsetLeft` của `th` (KHÔNG `getBoundingClientRect`); đo lại sau mỗi lần đổi bề rộng (`ResizeObserver` trên bảng + sự kiện phóng to popup); nền đặc theo hover; viền `box-shadow: inset -1px 0 0 <màu viền>`.
- [x] **Step 3: 2 nút trong ô Hạn giữ** — chỉ khi `mine`: `V2BaseButton size="sm"` dạng viền, icon `#prefix` (`ri-calendar-check-line` teal "Gia hạn" · `ri-close-circle-line` đỏ "Huỷ giữ" — giữ đúng chính tả user chốt), điều hướng KHÔNG hỏi xác nhận:
  `this.$router.push({ path: '/finance/prepick-extend-requests/create', query: { prepick_detail_id: row.id } })` / `'/finance/prepick-cancel-requests/create'`. Kiểm `remixicon` codepoint (memory: 2 bản lệch glyph) — nếu glyph sai thì dùng SVG inline như mockup.
- [x] **Step 4: Popup lịch sử gia hạn** — `GET ${API}/extends?prepick_detail_id=`; bảng `Lần · Ngày duyệt · Phiếu gia hạn · Hạn cũ → Hạn mới · SL gia hạn · Người đề nghị · Người duyệt`, CŨ → MỚI, dòng `is_current` tô nền; mô tả kèm ĐVT + Phiếu giữ gốc; không phân trang; `min-width: 0` (không tràn ngang).
- [x] **Step 5: Popup phiếu thu** — `GET ${API}/payments`; mô tả Giá trị HĐ · Đã thanh toán (tỷ lệ) · Số phiếu thu; bảng STT · Số phiếu thu · Ngày thu · Người nộp · Số tiền · Nội dung (MỚI → CŨ). KHÔNG có "Còn phải thu".
- [x] **Step 6: Kiểm Playwright MCP** — bấm ô "Yêu cầu đã hết hạn" ở dải tổng hợp: dòng đếm "M yêu cầu giữ" = số trên ô; popup từ 1 NV không có cột Nhân viên/Phòng ban; cuộn ngang 900px → 3 cột ghim đo `offsetLeft` lệch ≤ 1px, cột 4 cuộn đi; chế độ thường 0 nút, chế độ "của tôi" mỗi dòng đủ 2 nút; popup gia hạn của 1 dòng có ≥ 3 lần: hạn mới lần k = hạn cũ lần k+1; console 0 lỗi.
- [x] **Step 7: Commit** `feat(prepick-tracking): popup chi tiết (ghim cột, gia hạn/huỷ giữ), lịch sử gia hạn, phiếu thu`.

### Task 14: In / Xuất Excel — 4 đường

**Files:**
- Modify: `hrm-client/pages/sale/prepick-tracking/index.vue`
- Create: `hrm-client/pages/sale/prepick-tracking/components/PrintOptionsModal.vue` (copy khuôn TKT, 2 chế độ: *In bảng theo dõi* / *In danh sách chi tiết*)

- [x] **Step 1:** Thanh tiêu đề (`#header-actions`): **In danh sách** (secondary, mở `PrintOptionsModal`) · **Xuất Excel** (xanh lá `#16a34a`). Footer popup chi tiết: `In danh sách · Xuất Excel · Đóng` (Đóng cuối, có icon). In → `this.openPrintList(API, this.buildParams({ mode }), '...')` (GET `${API}/print-list-data`). Excel → `downloadExcel(`${API}/export`, params)` tải trực tiếp `?token=` (khuôn TKT — KHÔNG blob, lỗi Safari).
- [x] **Step 2: Kiểm** — đang ở trang 2, `level=1`: bản in "bảng theo dõi" vẫn đủ cấp hàng hoá và đủ mọi trang (đếm dòng `tr` trong iframe preview = số dòng `flatten` từ API); bản in chi tiết từ popup = `total` của popup (không phải 20); file Excel tải về có đuôi `.xlsx`, không chứa chữ "Gia hạn"/"Huỷ giữ"; dòng tóm tắt bộ lọc có mặt.
- [x] **Step 3: Commit** `feat(prepick-tracking): in + xuất Excel 4 đường`.

### Task 15: Màn lập Gia hạn / Huỷ giữ đọc `?prepick_detail_id`

**Files:**
- Modify: `hrm-client/pages/finance/prepick-extend-requests/components/PrepickExtendRequestForm.vue` — `loadStock()` (dòng ~727)
- Modify: `hrm-client/pages/finance/prepick-cancel-requests/components/PrepickCancelRequestForm.vue` — `mounted()` (dòng ~566)

- [x] **Step 1: Gia hạn** — khi `isCreate` và có `this.$route.query.prepick_detail_id`: gọi `${API_BASE}/stock?prepick_detail_id=...`; nếu `focus.in_list` → tick sẵn `need_extend=true` cho đúng dòng đó và cuộn tới dòng; nếu `focus.message` → hiện thông báo vàng (không phải chữ đỏ — đỏ chỉ dành cho lỗi validate) ở đầu bảng, danh sách các dòng khác vẫn hiện bình thường. Sau đó `markFormPristine()` (tick sẵn KHÔNG được bật cảnh báo "chưa lưu").
- [x] **Step 2: Huỷ giữ** — khi tạo mới có `prepick_detail_id`: `GET ${API_BASE}/lot?prepick_detail_id=` → gán `form.customer_id` (gọi `loadCustomers([customer_id])` trước để select có option), rồi nạp dòng hàng hoá đó qua đúng đường `PrepickStockSearchModal` đang dùng (`${API_BASE}/stock?customer_id=&code=<product_code>`) và đẩy vào `form.products` như `onApplyProducts()`. Hiện ghi chú xám: "Hủy giữ trừ theo hạn giữ sớm nhất của cùng hàng hoá – khách hàng, kiểm lại số lượng trước khi gửi." (spec 9.1.2 — đừng hứa hủy đúng dòng). 404 → toast lỗi, form trống như cũ.
- [x] **Step 3: Kiểm Playwright MCP** — từ báo cáo (chế độ "của tôi") bấm Gia hạn ở 1 dòng trong hạn → thấy thông báo "còn N ngày"; ở 1 dòng sắp hết hạn → dòng đó được tick; bấm Huỷ giữ → khách hàng + hàng hoá điền sẵn; mở trực tiếp 2 màn không có query → hành vi y như trước.
- [x] **Step 4: Commit** `feat(prepick): màn lập gia hạn / hủy giữ nhận dòng từ báo cáo theo dõi`.

---

## Phase 4 — Kiểm chứng + bàn giao

### Task 16: Spec e2e + đối chiếu mockup

**Files:**
- Create: `HRM/e2e/tests/sale/prepick-tracking.spec.ts`, `HRM/e2e/tests/sale/prepick-tracking.api.spec.ts`
- Create: `HRM/e2e/utils/prepickTrackingFixture.ts` (seed qua `php artisan tinker` — khuôn `tktResultFixture.ts`): 1 NV có hàng giữ 3 trạng thái, 1 dòng có chuỗi gia hạn 2 lần, 1 dòng theo hợp đồng có phiếu thu đã duyệt.

- [x] **Step 1:** Ca API: 401 khi chưa đăng nhập · không quyền gửi `company_id` khác vẫn ra công ty mình · có quyền xem "Tất cả công ty" · `extends` dòng ngoài phạm vi 404 · tổng cấp 1 = tổng toàn bộ · `reqs_exp` popup = tổng hợp.
- [x] **Step 2:** Ca UI (serial, `--workers=1`): có quyền / KHÔNG quyền (ô Công ty ẩn + nhãn tĩnh) · Xoá lọc không đổi công ty · Bộ phận 3 trạng thái · Hàng giữ của tôi bật/tắt khôi phục · đổi tiêu chí → cột Tồn · bung lazy cấp 3 · phân trang STT chạy tiếp · popup ghim cột (`offsetLeft`) · 2 nút chỉ ở chế độ của tôi · điều hướng Gia hạn với dòng xa hạn hiện thông báo · in đủ cấp ở trang 2 · khuôn giao diện (không cuộn ngang, màu tiêu đề teal, số định dạng `1,234.5`). Mốc chờ: chờ `.rsum-tb` có dòng, KHÔNG `networkidle`. Bấm `V2BaseButton` bằng locator chuẩn hoá khoảng trắng.
- [x] **Step 3:** KHÔNG tự chạy cả bộ — báo user lệnh chạy: `cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test tests/sale/prepick-tracking --workers=1` (đọc dòng tổng kết, "did not run" ≠ passed). Nếu `api-setup` hỏng trên DB gộp → chạy `--no-deps` + tự ghi `.auth/user.json`.
- [x] **Step 4:** Đối chiếu mockup vs màn thật bằng Playwright MCP: mở 2 tab cùng bộ lọc, đo cỡ chữ / chiều cao dòng / thứ tự cột / màu badge / bề rộng ô lọc bằng `getComputedStyle`; ghi bảng lệch + đã sửa vào `design.md` mục mới "Đối chiếu Vue thật với mockup".
- [x] **Step 5: Commit** `test(prepick-tracking): e2e báo cáo theo dõi giữ hàng`.

### Task 17: Bàn giao + checklist deploy

- [x] **Step 1:** Cập nhật `design.md` (số đo hiệu năng, số chuỗi gia hạn đứt sau backfill, đối chiếu mockup), checkpoint `plan.md`, `STATUS.md`.
- [x] **Step 2: Checklist deploy (ghi vào STATUS)** — thứ tự BẮT BUỘC:
  ⚠️ Sửa 03/10/2026 theo review tổng: thứ tự cũ (code trước, migrate sau) làm MỌI đường tạo hàng giữ ở cả ERP lẫn HRM lỗi `Unknown column root_objectable_id` trong khe giữa 2 bước.
  1. `php artisan migrate` ở **hrm-api TRƯỚC** (1 migration thêm 2 cột nullable + 2 index — bảng ~62k dòng, ALTER vài giây; code cũ không đụng 2 cột nên chạy song song an toàn). Repo ERP KHÔNG có migration này — DB gộp dùng chung nên chỉ chạy 1 lần từ HRM.
  2. `php artisan prepick:backfill-root --dry-run` → xem phân bổ → chạy thật — TRƯỚC khi code mới chạy, để dòng gia hạn mới kế thừa đúng gốc.
  3. Deploy code **ERP** (5 chỗ ghi root) và **HRM** BE+FE cùng đợt.
  4. Chạy lại `php artisan prepick:backfill-root --all` ngay sau khi deploy (bắt dòng tạo trong khe giữa bước 2 và 3 — `--all` tính lại cả dòng đã có root; review tổng đã dò cả 8 đường ghi: ra cùng giá trị code đang ghi).
  5. INSERT tay quyền id 1632 (KHÔNG chạy `PermissionsTableSeeder` — truncate cả bảng); kiểm trùng id trên DB đích trước; không gán sẵn role (chốt #3). Xoá cache quyền spatie.
  6. Không có cron mới.
- [x] **Step 3 (03/10 — merge local, CHƯA push):** `superpowers:finishing-a-development-branch` — merge 3 nhánh về `gop_db` khi user đồng ý; `git grep '<<<<<<<\|>>>>>>>'` cả 3 repo sau merge; `uniq -d` id quyền.

---

### Checkpoint — 2026-10-03 (wrap up — code + tài liệu xong, chờ deploy)
Vừa hoàn thành:
  · Code đã merge + PUSH `gop_db` 3 repo (hrm-api 0d35c84ca · hrm-client f416ab17e · ERP 04b61efc24); worktree `wt-giu-hang` + server :8011/:3011 đã dọn, nhánh feature đã xoá (nằm trọn trong gop_db).
  · Test cuối: PHP unit 29/29 · feature 41/41 · e2e báo cáo `26 passed`.
  · Tài liệu: `SRS - Báo cáo theo dõi giữ hàng.docx` (gen_srs.py; 10 chức năng, 20 ảnh thật ở `bao-cao-theo-doi-giu-hang_shots/`, selfcheck đạt) · `testcase.xlsx` (gen_testcase.py; 146 ca, 77 P0, selfcheck đạt).
  · ERP prod: user kiểm `git merge-base --is-ancestor 856dc00e4f HEAD` → ĐÃ CÓ code ghi root.
Đang làm dở: không.
Bước tiếp theo:
  1. KIỂM NGAY DB prod `SHOW COLUMNS FROM prepick_details LIKE 'root_objectable%'` — ERP prod đã chạy code ghi 2 cột này; chưa có cột thì mọi thao tác tạo hàng giữ trên ERP đang lỗi → thêm cột (migration hoặc ALTER tương đương trong chat 03/10).
  2. Deploy HRM theo checklist Task 17 (down → pull → migrate (rà migration người khác bằng --pretend) → backfill-root → INSERT quyền 1632 → deploy.sh → up) → HRM client → `backfill-root --all` → kiểm sau deploy.
  3. Mở SRS bằng Word → Update Field mục lục.
Blocked: chưa có kết quả kiểm cột trên DB prod (đã hỏi user).
Còn để sau (không chặn): ~6 bản in Tài chính khác vẫn dùng header thô (có thể chuyển sang trait `ResolvesCompanyLetterhead`) · 2 ca e2e cũ đỏ sẵn (TKT ca 4 `data-dim`, phát triển thị trường ca thanh cuộn) · ~40 minor trong `sdd-ledger.md` · HDSD chưa làm · sơ đồ tổng quan SRS có đường In/Excel cắt chéo (user chưa yêu cầu sửa).

### Checkpoint — 2026-10-03 (ĐÃ PUSH gop_db 3 repo — chờ deploy)
Cập nhật cuối: đã push `gop_db` cả 3 repo (origin khớp local); đã tắt server :8011/:3011 theo PID, gỡ worktree `wt-giu-hang`, xoá nhánh feature local (đã nằm trọn trong gop_db). Còn lại: deploy theo checklist Task 17.
Vừa hoàn thành: đồng bộ thêm origin/gop_db mới (hrm-api 5, hrm-client 5, ERP 7 commit — không xung đột; upstream có sửa `V2BaseSmartFilterPanel` nhưng độc lập) → test lại: PHP unit 29/29 · feature 41/41 · e2e báo cáo `26 passed` → fast-forward `gop_db` local: hrm-api 0d35c84ca (20 commit chưa push) · hrm-client f416ab17e (14) · ERP 04b61efc24 (2; ERP checkout chính vẫn đứng develop_01, chỉ cập nhật ref gop_db).
e2e 4 màn báo cáo khác (dùng thanh lọc chung): 12 ca xanh; 2 ca đỏ có sẵn (TKT ca 4 tìm `data-dim` không còn trong code ở mọi bản; phát triển thị trường ca đếm thanh cuộn phụ thuộc dữ liệu) + 2 spec fixture hỏng môi trường (CSKH chạy tinker trên checkout chính thiếu hằng số; meeting 403) — không do nhánh này.
Bước tiếp theo: user lệnh push 3 repo → deploy theo checklist Task 17 → dọn worktree `wt-giu-hang` + server :8011/:3011.
Lưu ý: checkout chính hrm-api/hrm-client giờ đứng code mới; DB local còn migration của người khác chưa chạy (KHÔNG tự chạy).

### Checkpoint — 2026-10-03 (chiều — xử 6 vấn đề sau nghiệm thu)
Vừa hoàn thành: user chốt từng vấn đề A–F (bảng cuối `design.md`). Đã làm + review sạch:
  · A bỏ ngoại lệ super admin (hrm-api 88a49bb20) · F merge `origin/gop_db` vào nhánh (hrm-api 91a8658ae, hrm-client be8421271 — không xung đột; KHÔNG chạy migration của người khác trên DB local)
  · B "Tổng thanh toán" = phát sinh Có TK 1311 (Phiếu thu/báo có/kế toán) (hrm-api 76647381e) · C cắt tên hàng 2 dòng + tooltip · E chữ ô popup #374151 ở khung dùng chung + 2 popup tự dựng + popup thanh toán (hrm-client 367f77019)
  · D giữ nút chuẩn (không sửa)
Sửa thêm: nhóm 4 nút góc phải (btn-compact mr-2, bỏ mb-2) — hrm-client a5c0840f3.
Sửa thêm (G, H): bản in — header tự ẩn khi ảnh lỗi ở layout in dùng chung (hrm-api 5de644768) · cấp 3 không thụt, cấp 2 thụt 1 nấc + in đậm, áp chung bản in + Excel (f91c5c901). (I) đã sửa: logo bản in phiếu huỷ giữ (đơn + danh sách) + danh sách hàng giữ cũ ghép ERP_URL qua trait chung `ResolvesCompanyLetterhead` (hrm-api 18e54e859). (J) thanh lọc dùng chung `gap:12px` cho nhóm nút, nút slot `#header-actions` chỉ khai `btn-compact`, dọn 5 màn (hrm-client d51f58e72). Còn ~6 service Tài chính khác vẫn dùng header thô (ngoài phạm vi).
Test toàn bộ 03/10 (sau mọi sửa + merge gop_db): PHP unit 28/28 · feature 35/35 · phiếu hủy cũ 13/13 · e2e 2 spec `26 passed (3.3m)` (15 UI + 11 API, `--workers=1 --no-deps`, :3011/:8011) — DB không sót dữ liệu fixture.
Bước tiếp theo: user chạy/duyệt → lệnh merge nhánh về `gop_db` + push (cả 3 repo), deploy theo checklist Task 17.
Lưu ý: B chỉ cộng phát sinh Có 1311 theo đúng chốt — khác công thức "thực thu" ERP (ERP còn trừ Nợ 1311 trả lại khách, cộng TK 21/23, khai báo đầu kỳ).

### Checkpoint — 2026-10-03 (code xong 16/17 task — chờ user quyết merge)
Vừa hoàn thành: chạy plan bằng subagent-driven — Task 1-16 xong, mỗi task qua review spec + chất lượng (có vòng sửa ở T7, T9, T12×2, T16), review tổng 3 repo + 1 đợt sửa (I3 Huỷ giữ điền sai hàng, I4 thứ tự nút In·Hủy, I5 badge V2BaseBadge từ BE, M1 rò tên ngoài phạm vi ở bản in, M2 tham số mảng → 422) → re-review sạch. Checklist deploy đã sửa thứ tự (migrate + backfill TRƯỚC deploy code). Sổ theo dõi đầy đủ (mọi Ruling, minor để sau): `sdd-ledger.md`.
Nhánh `gop_db-bao-cao-theo-doi-giu-hang` (CHƯA push, CHƯA merge), worktree `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-giu-hang/`:
  · hrm-api 0bfd98d31..361007723 (13 commit) · hrm-client 976e1eb32..389c3497e (8 commit) · ERP 3a87a07d4f..856dc00e4f (1 commit)
  · e2e (không có git): `e2e/utils/prepickTrackingFixture.ts`, `e2e/tests/sale/prepick-tracking{,.api}.spec.ts` — lần chạy cuối API 11/11, UI 13/13 (chạy `--workers=1 --no-deps`, BASE_URL=:3011 API_BASE=:8011); sau đợt sửa final có thêm ca 10b + sửa ca 12, CHƯA chạy lại.
  · Server kiểm: API :8011, client :3011 (đang chạy).
Số đo: API 60–210ms/endpoint (company all) · DB local 61.771 dòng, backfill ghi 48.080, còn 304 dòng còn tồn chưa xác định gốc · 2.146 yêu cầu giữ.
Bước tiếp theo: user quyết (1) nguồn "Tổng thanh toán" · (2) 3 chỗ lệch mockup (dòng hàng hoá xuống dòng nhiều, nút "Hàng giữ của tôi" xám, chữ popup đen) · (3) merge `gop_db` mới vào nhánh feature (hrm-api `origin/gop_db` đã đi trước 74 commit, chồng file PrepickExtendRequestController + Routes + 2 form) rồi merge về `gop_db`.
Blocked: chưa test được bằng tài khoản thật KHÔNG có quyền (2 tài khoản e2e không login được trên DB local) và chế độ "của tôi" với hàng giữ thật (đã giả lập).

### Checkpoint — 2026-10-02 (chốt vướng mắc + lập plan code)
Vừa hoàn thành: user duyệt mockup; chốt 7/7 vướng mắc (hỏi lần lượt) — bảng cuối `design.md`; khảo sát
code 3 repo (BE HRM, ERP, FE) rồi lập plan 17 task. Điểm mới phát hiện khi khảo sát:
  · `prepick_details` có 61.771 dòng (2.412 còn tồn), KHÔNG có index nào ngoài employee/customer → migration thêm `pd_company_qty_idx`.
  · ERP `TransferProductAllocation::approve()` tạo dòng KHÔNG ghi objectable (= 5.534 dòng NULL) → từ nay ghi root = dòng phân bổ.
  · Model `PrepickDetail` của HRM không có hook; hook lấp `company_id` là của ERP.
  · 2 màn lập Gia hạn / Huỷ giữ hiện KHÔNG đọc query nào → Task 10 + 15 thêm `prepick_detail_id`.
  · Menu mới KHÔNG khai `isShow` (middleware checkPermission sẽ đá người không quyền ra 404).
  · DB local đã có quyền tới id 1631 (nhánh khác) → quyền mới dùng **1632**.
Đang làm dở: không.
Bước tiếp theo: user chọn cách thực thi (subagent-driven hay inline) → Task 1 dựng worktree.

### Checkpoint — 2026-09-15 (rà nút theo skill)
Vừa hoàn thành: user yêu cầu "check button đúng skill chưa" → rà TOÀN BỘ nút trong mockup theo
`button-convention`, không chỉ 2 nút mới. Phát hiện **5 lỗi ở các nút CŨ** (làm từ vòng In/Excel,
không phải do quyết định nào của user) — đã sửa hết, chi tiết ở `design.md` mục 49:
  1. "In báo cáo" → **"In danh sách"** (chữ cũ nằm thẳng trong cột "KHÔNG dùng" của bảng text chuẩn)
  2. "Xuất Excel danh sách" → **"Xuất Excel"** (4 từ, vượt trần 3 từ)
  3. Thứ tự footer: Thoát/Huỷ phải CUỐI CÙNG → `In danh sách · Xuất Excel · Đóng` và `In · Hủy`
  4. 4 nút Đóng/Hủy thiếu icon → thêm icon mũi tên trái
  5. "Xuất Excel" trong popup tô teal như nút chính → đổi **xanh lá `#16a34a`**, cùng nhóm với nút
     Xuất Excel ở thanh tiêu đề (2 nút cùng việc mà 2 màu là đọc thành 2 mức quan trọng khác nhau)
Đo lại sau khi sửa: 5/5 nhóm nút đúng chữ + đúng thứ tự + đủ icon; 2 nút Gia hạn/Huỷ giữ vẫn chạy,
nút Excel vẫn tải file, nút Đóng/Hủy vẫn đóng popup; console sạch.
3 điểm vẫn lệch skill nhưng **do user chốt**, ghi ở `design.md` mục 48: nhãn "Huỷ giữ" (thay vì
"Hủy") · nút trong bảng icon+chữ (thay vì `V2BaseIconButton` icon-only) · nút Huỷ giữ dạng viền
(thay vì `primary status="danger"` nền đỏ đặc).
ℹ️ Phát hiện thêm: **`button-convention` tự mâu thuẫn về nút In** — mục 2 xếp In vào nhóm `primary`,
mục 2b lại xếp `secondary/tertiary`. Mockup xử theo ngữ cảnh (In là action chính của popup chọn chế
độ in → primary; In danh sách ở footer popup chi tiết là bổ trợ → secondary). Nên làm rõ trong skill.
Bước tiếp theo: user duyệt mockup → lên plan code.

### Checkpoint — 2026-09-14 (vòng 11)
Vừa hoàn thành: 2 nút **Gia hạn** / **Huỷ giữ** (icon + chữ) nằm TRONG ô "Hạn giữ hiện tại".
Làm 2 nhịp: nhịp 1 tách thành cột Hành động riêng, nhịp 2 user chốt gộp vào ô hạn giữ + đổi sang
nút có chữ → bỏ cột riêng. Đo bằng Playwright:
  · Bảng vẫn **15 cột** ở cả 2 chế độ (không tốn thêm cột) · chế độ thường 0 nút · chế độ "của tôi"
    20/20 dòng đủ 2 nút
  · Ô hạn giữ rộng 196px, 2 nút 70/71 × 22px gọn 1 hàng, dòng cao đều 76px, không tràn ô
  · Nút giữ đúng màu teal/đỏ ở CẢ 3 trạng thái hạn — không bị màu chữ của ô (xanh/vàng/đỏ) đè
  · Ghim 3 cột đầu vẫn chuẩn 46/314px, lệch 1px
  · Bản in / Excel vẫn 15 cột và KHÔNG dính chữ nút · console sạch
Lỗi tự phát hiện & sửa trong vòng này:
  · Chèn chú thích ra NGOÀI khối `/* */` làm hỏng cú pháp JS cả file — triệu chứng là `.rsum-drill`
    trả `null` (bảng không render), console chỉ ghi "Unexpected string"
  · Nhét nút vào ô dữ liệu làm bản in kéo theo chữ nút:
    `"03/08/2026 quá hạn 40 ngày Gia hạn Huỷ giữ"` → phải gỡ `.row-acts` trước khi lấy text
2 điểm lệch quy ước đã nêu và user chốt (chi tiết + rủi ro ở `design.md` mục 48):
  a. Nhãn "Huỷ giữ" giữ chính tả user, khác dấu kiểu mới "Hủy" của `button-convention`
  b. **Nút Gia hạn hiện ở MỌI dòng** kể cả dòng Trong hạn — tôi đã nêu đây là nút chết
     (màn lập phiếu gia hạn chỉ nhận lô `expire_date <= hôm nay + warning_day`), user vẫn chọn
     → lúc code BE BẮT BUỘC xử 1 trong 2: màn gia hạn báo rõ lý do khi dòng chưa tới ngưỡng,
       hoặc hỏi khách để nới điều kiện `getDataToCreate()`
Bước tiếp theo: user duyệt mockup → lên plan code.

### Checkpoint — 2026-09-14 (vòng 10)
Vừa hoàn thành: 4 yêu cầu của vòng 10, đã kiểm chứng bằng Playwright (đo DOM, không nhìn ảnh):
  · Lọc Bộ phận: 3 trạng thái đúng · `21 + 17 + 29 = 67` = đúng tổng của phòng (không mất dòng) ·
    cascade reset đúng · "Hàng giữ của tôi" ép 6 giá trị và khôi phục đúng · "Xoá lọc" không đụng công ty
  · Ghim cột: cuộn ngang 900px, 3 cột ghim lệch 1px (viền), khít nhau, cột 4 cuộn đi; nền đặc, z-index đúng
  · In/Excel: trang 1 và trang 2 in ra cùng 73 dòng · `level=0` vẫn in đủ cấp hàng hoá ·
    popup hiện 20 dòng/trang nhưng xuất 185 dòng · bảng chi tiết 15 cột không tràn khổ A4 ngang (1.046/1.047px)
  · Console sạch, thanh lọc không sinh cuộn ngang
Lỗi tự phát hiện & sửa trong vòng này (chi tiết ở `design.md` mục 46–47):
  · **`getBoundingClientRect` trả toạ độ sau `transform: scale(.96)`** của popup → ghim lệch 13px.
    Mất 3 lần đo mới ra (2 giả thuyết sai trước đó: border-collapse, rồi animation chưa xong).
    `ResizeObserver` không bắt được vì transform không đổi kích thước layout → phải dùng `offsetLeft`.
  · Đổ HTML ra text phẳng làm các mẩu `<span>` dính liền (`VT.00611-Ống…`) → chèn khoảng trắng 2 phía
  · Thụt lề cây bằng dấu cách thường bị HTML/Excel nuốt → dùng ` `
  · Lấy tiêu đề popup sau `closeDrill()` ra tiêu đề "toàn bộ báo cáo" → lấy trước khi đóng
Đang làm dở: không có việc đang dở — chờ user duyệt mockup.
Bước tiếp theo: user duyệt mockup → lên plan code.
Blocked: vẫn 3 việc của checkpoint 13/09 (quyền chưa tồn tại · cách lấy chứng từ gốc · cỡ trang),
  thêm 1 việc mới: dữ liệu **bộ phận gần như trống trên DB thật** (2,6% dòng hàng giữ) — cần hỏi
  nghiệp vụ xem có kế hoạch gán bộ phận cho nhân viên kinh doanh không, nếu không thì ô lọc này
  gần như luôn ở trạng thái khoá.

### Checkpoint — 2026-09-13
Vừa hoàn thành: mockup hoàn chỉnh (13 vòng chỉnh, vòng cuối là **phân trang**) + spec chi tiết đã
viết đầy đủ ở `docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md`.
Toàn bộ quyết định nghiệp vụ, phân quyền, phân trang và ràng buộc BE đã chốt, ghi vào `design.md`
(43 mục quyết định) + spec (13 chương).
Đang làm dở: không có việc đang dở — chờ user duyệt mockup.
Bước tiếp theo: user duyệt mockup → lên plan code.
  · Phase 1 BE: service đọc mới (KHÔNG sửa `PrepickStockReportService` đang phục vụ màn expiring) +
    lần ngược chuỗi gia hạn + 6 endpoint + thêm quyền vào seeder.
  · Phase 2 FE: viết lại `pages/finance/prepick-stocks/index.vue` theo mockup.
Blocked: 3 việc phải xử lý/hỏi ngay đầu Phase 1 —
  (1) quyền `Xem báo cáo giữ hàng theo tổng công ty` CHƯA tồn tại, phải thêm `PermissionsTableSeeder`;
  (2) cách lấy chứng từ gốc: recursive CTE mỗi lần chạy, hay denormalize `root_objectable_id/type` —
      cột mới trên bảng DÙNG CHUNG với ERP nên phải hỏi trước;
  (3) chốt cỡ trang + ngưỡng lazy load sau khi đo thời gian phản hồi trên dữ liệu thật.

### Checkpoint — 2026-09-12 (vòng 9)
Vừa hoàn thành: mockup bản 9 + kiểm chứng trình duyệt. Lỗi đã tự phát hiện & sửa qua 3 vòng: min-width bảng cắt cột · header chữ trắng trên nền trắng · flex co sập bảng lịch sử còn 2px · `.drill-table` min-width 1740px của bảng 14 cột · tồn kho demo nhỏ hơn số đang giữ · số lần gia hạn đếm gộp sai cấp · đổi thứ tự colgroup mà quên đổi thứ tự render ô làm lệch toàn bảng 1 nhịp · `.drill-table` min-width 1740px cắt cột ở popup phiếu thu (bẫy lặp lần 2).
Đang làm dở: chờ user duyệt mockup.
Bước tiếp theo: user duyệt → viết `docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md` rồi lên plan code.
Blocked:
