# Brief — Đổi luật chép giá giữa các công ty (15/10/2026)

## Chốt user (15/10)
- **Nhóm chia sẻ: 1 Tân Phát · 3 Vinh · 4 Sài Gòn** — chép LẪN NHAU mọi hàng đang bán (như B5 cũ): giá × hệ số của công ty NHẬN, không có hệ số ⇒ hệ số 1 (giá bằng nhau).
- **2 Hải Phòng · 7 ETEK Green: tự quản** — chỉ dùng hàng mình LÀM CHỦ (`products.company_id`): vẫn qua B1–B4 (gán chủ dòng giá, tách pcu chủ, bù loại giá, trạng thái Đang KD cho hàng của mình). KHÔNG nhận hàng chép từ công ty khác, KHÔNG cho hàng của mình sang nhóm (3 hàng HP ở lại HP).
- **5 · 6 · 8**: không dùng phần mềm nữa ⇒ bỏ qua (như cũ).
- Vẫn là backfill MỘT lần ngày chuyển đổi (T2 không đổi).
- User: "sửa code để deploy vps test trước, **dọn sau**" ⇒ đợt này KHÔNG viết/chạy lệnh dọn phần HP đã nhận trên `hrm_erp_giacty` (ghi việc treo), KHÔNG ghi DB.

## Phạm vi (user cho phép)
Repo `/Users/dnsnamdang/Documents/DNSMEDIA/websites/wt-chuyen-doi-hang-hoa/hrm-api`, nhánh con `feat/cdhh-cum-gia` từ `feat/chuyen-doi-hang-hoa`; xong merge `--no-ff` LOCAL về nhánh chung, soát marker, KHÔNG push / stash.
1. `config/price.php`: tách 2 danh sách — nhóm chia sẻ `[1,3,4]` và công ty tự quản `[2,7]` (đặt tên khoá rõ nghĩa, comment tiếng Việt theo chốt trên). Mọi chỗ đọc `cluster_company_ids` đổi theo.
2. `Modules/MasterData/Services/ProductPrice/CompanyPriceBackfill.php` + `Console/BackfillCompanyPricesCommand.php`: B1–B4 áp cho hàng có chủ ∈ nhóm chia sẻ ∪ tự quản; B5 chỉ chủ ∈ nhóm chia sẻ, nhận ∈ nhóm chia sẻ \ {chủ}. Hàng chủ ngoài 2 danh sách (5/6/8, NULL…) giữ hành vi cũ cho hàng ngoài cụm (đọc code hiện tại; nêu rõ trong report). `--company` vẫn chạy đúng. Bảng in của lệnh hiện đủ cột công ty liên quan.
3. `CompanyPriceComparator` + `CompareCompanyPricesCommand`: so theo luật mới (cặp hàng × công ty cần có giá: chủ của mọi công ty trong 2 danh sách + nhận trong nhóm chia sẻ). Không báo lệch vì HP/Green thiếu hàng chép.
4. PHPUnit: sửa `CompanyPriceBackfillTest` (+ test compare nếu có) cho luật mới — có ca: hàng Cty 1 chép sang 3,4 KHÔNG sang 2/7; hàng Cty 2 ở lại Cty 2 (status 3) không sang 1/3/4; hệ số nhận ≠ 1 nhân giá, không có ⇒ giá bằng; idempotent. Chạy test + cả bộ `Modules/MasterData` (mốc 557), ghi số.
5. Đo dry-run (CHỈ dry-run, không ghi) trên một bản DB có dữ liệu trước backfill nếu có sẵn mà không phải tạo DB mới — nếu không có thì bỏ, ghi lý do; KHÔNG tạo/DROP database, KHÔNG ghi `hrm_erp` hay `hrm_erp_giacty`.
6. Cập nhật tài liệu: `gia-theo-cong-ty/runbook-trien-khai.md` (bảng số dry-run cũ ghi rõ "luật cũ 1-2-3-4", thêm mục luật mới 15/10), `quan-ly-hang-hoa/deploy-dev-server.md` bước 5 (ý nghĩa cụm), `gia-theo-cong-ty/design.md` P2/P2b/P2c (ghi "Đổi 15/10").
Ngoài phạm vi, chỉ ghi chú: ERP `app/Console/Commands/PriceSnapshotCommand.php` gõ cứng `[1,2,3,4]`; lệnh dọn phần HP đã nhận trên giacty (việc treo, user "dọn sau").

## Quy tắc
PHP `/opt/homebrew/opt/php@7.4/bin/php`; trước artisan/phpunit: `ls bootstrap/cache/config.php` không tồn tại + `php artisan config:clear`. Giữ EOL; comment tiếng Việt. Commit cuối message:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_014JQzu8PhMym1qvYWURxtd3`.
API 8031 chạy từ worktree này — không kill. Không dispatch subagent, không sửa CLAUDE.md/cấu hình Claude. Lỗi ngoài luồng: ghi report (mã từ N128).
Report: `gia-theo-cong-ty/cum-gia-1510-report.md`.
