"""
Test end-to-end màn "Cài đặt phân hệ" (feature cai-dat-phan-he, nhánh gop_db).

Chạy:  /opt/homebrew/bin/python3 .plans/gop-db/cai-dat-phan-he/e2e_test.py
Yêu cầu: FE 3002 + BE 8003 đang chạy (worktree gop_db).

Cấu hình được đặt qua API (nhanh, xác định) rồi kiểm hiệu ứng trên UI thật của từng tài khoản.
Cuối bài tự trả cấu hình về rỗng.
"""
import json, sys, urllib.request
from playwright.sync_api import sync_playwright

FE = "http://127.0.0.1:3002"
BE = "http://127.0.0.1:8003"

ACCOUNTS = {
    "admin":        ("namdangit@gmail.com",     "2025Dns@2",   "Super admin - 761 quyền"),
    "co_quyen":     ("thuydt.qttt@tanphat.com",  "Test@12345", "Super admin (KHÁC tài khoản đang dùng) - có quyền Quản lý phân quyền"),
    "co_quyen_2":   ("cob@tanphat.com",           "Test@12345", "Super admin + Ban giám đốc DATKT - có quyền Quản lý phân quyền"),
    # chinhnv.ptgd: BE hasPermissionTo() báo CÓ nhưng FE nhận quyền theo CÔNG TY hiện tại nên KHÔNG có
    # -> cùng lý do mục "Phân quyền" sẵn có cũng bị ẩn với tài khoản này. Xếp vào nhóm không quyền.
    "cty_khac":     ("chinhnv.ptgd@tanphat.com", "Test@12345", "Admin_TPE - quyền thuộc công ty khác, FE không thấy quyền"),
    "khong_quyen":  ("Thiendd.mkt@tanphat.com",  "Test@12345", "Quản lý đào tạo + Quản lý_TPE - KHÔNG có quyền, 202 quyền"),
    "quyen_it":     ("khangcx.cshn@tanphat.com", "Test@12345", "Quản lý đào tạo - KHÔNG có quyền, 86 quyền"),
}

results = []
def check(case, desc, actual, expected):
    ok = actual == expected
    results.append((ok, case, desc, actual, expected))
    print(("  PASS  " if ok else "  FAIL  ") + case + " | " + desc)
    if not ok:
        print("          nhận: %r | mong đợi: %r" % (actual, expected))
    return ok

def api(method, path, token=None, payload=None):
    req = urllib.request.Request(BE + path, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    data = json.dumps(payload).encode() if payload is not None else None
    try:
        with urllib.request.urlopen(req, data) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}

def login_api(email, password):
    st, body = api("POST", "/api/v1/users/auth/login", payload={"email": email, "password": password})
    return body.get("access_token") or body.get("data", {}).get("access_token")

def set_config(token, keys):
    st, _ = api("PUT", "/api/v1/menu-settings", token, {"hidden_keys": keys})
    assert st == 200, "không đặt được cấu hình: %s" % st

def ui_login(page, email, password):
    page.goto(FE + "/login", wait_until="domcontentloaded")
    page.wait_for_selector("#emailaddress", timeout=30000)
    page.fill("#emailaddress", email)
    page.fill("input[type=password]", password)
    page.keyboard.press("Enter")
    page.wait_for_function("() => !!localStorage.getItem('access_token')", timeout=30000)
    # app tự điều hướng sau khi đăng nhập -> chờ yên rồi mới goto, tránh "interrupted by another navigation"
    page.wait_for_timeout(3000)

def ui_logout(page):
    # localStorage chỉ đọc được khi đang ở đúng origin (about:blank sẽ ném SecurityError)
    if not page.url.startswith(FE):
        page.goto(FE + "/login", wait_until="domcontentloaded")
        page.wait_for_timeout(1500)
    page.evaluate("() => { localStorage.clear(); sessionStorage.clear() }")

def goto(page, path, settle=2500, ready=None):
    for attempt in range(3):
        try:
            page.goto(FE + path, wait_until="domcontentloaded")
            break
        except Exception as e:
            if "interrupted by another navigation" not in str(e) or attempt == 2:
                raise
            page.wait_for_timeout(1500)
    # dev server biên dịch theo route -> chờ tới khi app thực sự chạy, không chờ theo giây
    try:
        page.wait_for_function("() => !!window.$nuxt", timeout=180000)
    except Exception:
        pass
    if ready:
        try:
            page.wait_for_selector(ready, timeout=120000)
        except Exception:
            pass
    page.wait_for_timeout(settle)

def wait_page_ready(page, selector, timeout=45000):
    page.wait_for_selector(selector, timeout=timeout)

def main():
    admin_token = login_api(*ACCOUNTS["admin"][:2])
    assert admin_token, "không đăng nhập được tài khoản admin"
    set_config(admin_token, [])

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1600, "height": 1000})
        page = ctx.new_page()

        # ---------------------------------------------------------------- A. QUYỀN
        print("\n=== A. Quyền truy cập màn Cài đặt phân hệ ===")
        for key in ("admin", "co_quyen", "co_quyen_2"):
            email, pwd, note = ACCOUNTS[key]
            ui_logout(page); ui_login(page, email, pwd)
            goto(page, "/timesheet/setting/setting-master", 3500)
            items = page.eval_on_selector_all(".setting-left-item a", "els => els.map(e => e.textContent.trim())")
            check("A1." + key, "%s: sidebar CÓ mục 'Cài đặt phân hệ'" % note,
                  any("Cài đặt phân hệ" in i for i in items), True)
            goto(page, "/timesheet/setting/subsystems", 1000)
            wait_page_ready(page, ".mv-side__item")
            check("A2." + key, "%s: vào được màn cấu hình" % key,
                  page.url.endswith("/timesheet/setting/subsystems"), True)

        for key in ("khong_quyen", "quyen_it", "cty_khac"):
            email, pwd, note = ACCOUNTS[key]
            ui_logout(page); ui_login(page, email, pwd)
            goto(page, "/timesheet/setting/setting-master", 3500)
            items = page.eval_on_selector_all(".setting-left-item a", "els => els.map(e => e.textContent.trim())")
            check("A3." + key, "%s: sidebar KHÔNG có mục 'Cài đặt phân hệ'" % note,
                  any("Cài đặt phân hệ" in i for i in items), False)
            goto(page, "/timesheet/setting/subsystems", 3500)
            check("A4." + key, "%s: gõ thẳng URL màn cấu hình -> 404" % key,
                  "/pages/extras/404" in page.url, True)
            tok = login_api(email, pwd)
            st_get, _ = api("GET", "/api/v1/menu-settings", tok)
            st_put, _ = api("PUT", "/api/v1/menu-settings", tok, {"hidden_keys": ["human"]})
            check("A5." + key, "%s: API GET menu-settings = 200" % key, st_get, 200)
            # `cty_khac` có quyền ở vai trò công ty khác -> BE (checkPermission gộp mọi role) vẫn cho ghi.
            # Đây là hành vi sẵn có của middleware checkPermission, giống mọi màn khác, không riêng màn này.
            check("A6." + key, "%s: API PUT menu-settings" % key, st_put, 403 if key != "cty_khac" else 200)
            if key == "cty_khac":
                set_config(admin_token, [])

        # ---------------------------------------------------------------- B. MẶC ĐỊNH
        print("\n=== B. Chưa cấu hình gì -> menu nguyên vẹn ===")
        set_config(admin_token, [])
        ui_logout(page); ui_login(page, *ACCOUNTS["admin"][:2])
        goto(page, "/timesheet/dashboard", 2500, ready="a.dropdown-item")
        base_links = page.eval_on_selector_all("a.dropdown-item", "els => els.map(e => e.getAttribute('href'))")
        check("B1", "topbar Chấm công có link /timesheet/timesheet_details",
              "/timesheet/timesheet_details" in base_links, True)
        goto(page, "/", 2500, ready="text=Chọn phân hệ")
        home = page.inner_text("body")
        for name in ("CHẤM CÔNG", "QUẢN LÝ CƠM", "TÍNH LƯƠNG", "TÀI CHÍNH"):
            check("B2." + name, "màn chọn phân hệ có %s" % name, name in home.upper(), True)

        # ---------------------------------------------------------------- C. ẨN MỤC LẺ / NHÓM
        print("\n=== C. Ẩn mục lẻ và ẩn nhóm cha (sidebar cây) ===")
        set_config(admin_token, ["timesheet::Chấm công::Bảng chấm công chi tiết trong tháng"])
        goto(page, "/timesheet/dashboard", 2500, ready="a.dropdown-item")
        links = page.eval_on_selector_all("a.dropdown-item", "els => els.map(e => e.getAttribute('href'))")
        check("C1", "mục đã ẩn biến mất khỏi topbar", "/timesheet/timesheet_details" in links, False)
        check("C2", "mục cùng nhóm KHÔNG bị ảnh hưởng", "/timesheet/timesheet_summaries" in links, True)
        goto(page, "/timesheet/timesheet_details", 3000)
        check("C3", "gõ URL mục đã ẩn -> feature-unavailable?reason=hidden",
              "feature-unavailable?reason=hidden" in page.url, True)
        check("C4", "trang báo đúng lý do (bị ẩn, không phải nâng cấp phiên bản)",
              "đang được ẩn" in page.inner_text("h2"), True)
        goto(page, "/timesheet/timesheet_details/999", 4000)
        check("C5", "route con của mục đã ẩn cũng bị chặn",
              "feature-unavailable" in page.url, True)

        set_config(admin_token, ["timesheet::Báo cáo"])
        goto(page, "/timesheet/dashboard", 2500, ready="a.dropdown-item")
        top = page.inner_text("body")
        check("C6", "ẩn nhóm cha -> cả nhóm biến mất khỏi topbar", "Báo cáo" in top.split("Tổng quan")[0], False)

        # ---------------------------------------------------------------- D. ẨN CẢ PHÂN HỆ
        print("\n=== D. Ẩn cả phân hệ ===")
        set_config(admin_token, ["rice"])
        goto(page, "/", 2500, ready="text=Chọn phân hệ")
        check("D1", "màn chọn phân hệ không còn QUẢN LÝ CƠM", "QUẢN LÝ CƠM" in page.inner_text("body").upper(), False)
        goto(page, "/rice/dashboard", 4000)
        check("D2", "URL của phân hệ đã ẩn bị chặn", "feature-unavailable" in page.url, True)
        st, body = api("GET", "/api/v1/master-settings?category=use_rice", admin_token)
        check("D3", "cờ cũ master_settings.use_rice đồng bộ = 0", str(body.get("data", {}).get("content")), "0")
        set_config(admin_token, [])
        st, body = api("GET", "/api/v1/master-settings?category=use_rice", admin_token)
        check("D4", "bật lại -> use_rice = 1", str(body.get("data", {}).get("content")), "1")

        # ---------------------------------------------------------------- E. PHÂN HỆ HUB
        print("\n=== E. Phân hệ dùng sidebar hub (Tài chính) ===")
        set_config(admin_token, ["finance::Thanh toán tiền mặt::Phiếu thu"])
        goto(page, "/finance/dashboard", 5000)
        txt = page.inner_text("body")
        check("E1", "hub: nhóm 'Quản lý tiền' giảm còn 6 chức năng", "Quản lý tiền 6 chức năng" in txt.replace("\n", " "), True)
        check("E2", "hub: chữ 'Phiếu thu' biến mất khỏi rail + lưới Tổng quan", "Phiếu thu" in txt, False)
        goto(page, "/finance/bill-incomes/123", 4000)
        check("E3", "hub: route con của mục đã ẩn bị chặn", "feature-unavailable" in page.url, True)

        # ---------------------------------------------------------------- F. NHIỀU LỐI VÀO CÙNG URL
        print("\n=== F. Một URL ứng với nhiều mục menu ===")
        four = [
            "assign::Giao việc - Công tác::Phiếu giao công tác",
            "assign::Giao việc - Công tác::Phiếu giao công tác chờ lập DNTT",
            "assign::Phê duyệt::Phiếu giao công tác cần duyệt",
            "assign::Phê duyệt::Đề nghị thanh toán chờ duyệt",
        ]
        set_config(admin_token, four[:1])
        goto(page, "/assign/assign_business", 3000)
        check("F1", "ẩn 1 trong 4 lối vào -> VẪN vào được", "feature-unavailable" in page.url, False)
        set_config(admin_token, four)
        goto(page, "/assign/assign_business", 3000)
        check("F2", "ẩn cả 4 lối vào -> bị chặn", "feature-unavailable" in page.url, True)

        # ---------------------------------------------------------------- G. CHỐNG TỰ KHOÁ
        print("\n=== G. Chống tự khoá + route ngoài menu ===")
        set_config(admin_token, ["timesheet"])
        goto(page, "/timesheet/setting/subsystems", 1200, ready=".mv-side__item")
        check("G1", "tắt cả phân hệ Chấm công vẫn vào được màn cấu hình",
              page.url.endswith("/timesheet/setting/subsystems"), True)
        goto(page, "/timesheet/setting/general", 4000)
        check("G2", "các màn Cài đặt khác cũng không bị chặn", "feature-unavailable" in page.url, False)

        # ---------------------------------------------------------------- H. MÀN CẤU HÌNH
        print("\n=== H. Màn cấu hình: đếm, tri-state, tìm kiếm, giữ tick con, lưu ===")
        set_config(admin_token, [])
        goto(page, "/timesheet/setting/subsystems", 1200, ready=".mv-side__item")
        page.wait_for_timeout(800)
        total_txt = page.inner_text(".mv-total")
        check("H1", "đếm tổng hiện đủ 848/848 mục", "848/848" in total_txt.replace("\n", " "), True)
        check("H2", "cột trái liệt kê 22 phân hệ (bỏ phân hệ hidden của dev)",
              page.eval_on_selector_all(".mv-side__item", "e => e.length"), 22)

        # chọn phân hệ Chấm công, mở nhóm đầu tiên, tắt 1 mục con
        page.eval_on_selector_all(".mv-side__item",
            "els => els.find(e => e.textContent.includes('Chấm công')).click()")
        page.wait_for_timeout(500)
        page.eval_on_selector_all(".mv-caret:not(.mv-caret--leaf)", "els => els[0].click()")
        page.wait_for_timeout(500)
        # click THẬT (có pointerdown) — unsavedChangesMixin chỉ tính là "user sửa" khi thay đổi
        # xảy ra ngay sau thao tác chuột/phím; click bằng JS sẽ bị coi là auto-fill
        page.click(".mv-children .mv-node label.custom-control-label >> nth=0")
        page.wait_for_timeout(600)
        head_state = page.evaluate("""() => {
            const i = document.querySelector('.mv-main__head input[type=checkbox]')
            return { checked: i.checked, indeterminate: i.indeterminate }
        }""")
        check("H3", "tắt 1 mục con -> checkbox phân hệ ở trạng thái NỬA", head_state, {"checked": True, "indeterminate": True})
        check("H4", "đếm tổng giảm 1", "847/848" in page.inner_text(".mv-total").replace("\n", " "), True)

        # cảnh báo chưa lưu (click thật để sinh pointerdown)
        page.click("a[href='/timesheet/setting/setting-master']")
        page.wait_for_timeout(1200)
        check("H5", "thoát khi chưa lưu -> hiện popup cảnh báo",
              "Thông tin chưa lưu" in page.inner_text("body"), True)
        page.click(".modal button:has-text('Ở lại')")
        page.wait_for_timeout(800)
        check("H6", "chọn 'Ở lại' -> vẫn ở màn cấu hình",
              page.url.endswith("/timesheet/setting/subsystems"), True)

        # lưu
        page.click(".footer button:has-text('Lưu')")
        page.wait_for_timeout(2000)
        st, body = api("GET", "/api/v1/menu-settings", admin_token)
        saved = body.get("data", {}).get("hidden_keys", [])
        check("H7", "Lưu -> BE ghi đúng 1 khoá", len(saved), 1)
        check("H8", "khoá lưu đúng dạng <phân hệ>::<đường dẫn nhãn>",
              saved[0].startswith("timesheet::"), True)

        # sau khi lưu, rời màn KHÔNG còn hỏi
        page.click("a[href='/timesheet/setting/setting-master']")
        page.wait_for_timeout(1500)
        check("H9", "lưu xong rời màn -> KHÔNG hỏi lại",
              "/timesheet/setting/setting-master" in page.url, True)

        # tìm kiếm
        goto(page, "/timesheet/setting/subsystems", 1200, ready=".mv-side__item")
        page.wait_for_timeout(800)
        page.fill(".mv-search input", "phiếu thu")
        page.wait_for_timeout(900)
        subs = page.eval_on_selector_all(".mv-side__item .mv-side__name", "els => els.map(e => e.textContent.trim())")
        check("H10", "tìm 'phiếu thu' -> chỉ còn Bán hàng + Tài chính", sorted(subs), ["Bán hàng", "Tài chính"])
        page.eval_on_selector_all(".mv-side__item", "els => els.find(e => e.textContent.includes('Tài chính')).click()")
        page.wait_for_timeout(700)
        check("H11", "tìm kiếm tự mở nhánh và bôi vàng kết quả",
              page.eval_on_selector_all(".mv-tree mark", "e => e.length") > 0, True)
        page.click(".mv-search__clear")
        page.wait_for_timeout(700)
        check("H12", "xoá từ khoá -> danh sách phân hệ trở lại đủ 22",
              page.eval_on_selector_all(".mv-side__item", "e => e.length"), 22)

        # giữ tick con khi bật lại cha
        set_config(admin_token, ["timesheet", "timesheet::Báo cáo"])
        goto(page, "/timesheet/setting/subsystems", 1200, ready=".mv-side__item")
        page.wait_for_timeout(800)
        page.eval_on_selector_all(".mv-side__item",
            "els => els.find(e => e.textContent.includes('Chấm công')).click()")
        page.wait_for_timeout(500)
        page.eval_on_selector_all(".mv-main__head input[type=checkbox]", "els => els[0].click()")
        page.wait_for_timeout(700)
        cnt = page.inner_text(".mv-main__count").replace("\n", " ")
        check("H13", "bật lại phân hệ -> tick con vẫn giữ (35/41 mục đang hiện)", "35/41" in cnt, True)

        # ---------------------------------------------------------------- I. NGƯỜI DÙNG THƯỜNG
        print("\n=== I. Người dùng KHÔNG có quyền quản trị vẫn bị ảnh hưởng bởi cấu hình ===")
        set_config(admin_token, ["training::Khoá học"])
        for key in ("khong_quyen", "quyen_it"):
            email, pwd, note = ACCOUNTS[key]
            ui_logout(page); ui_login(page, email, pwd)
            goto(page, "/training/dashboard", 5000)
            # CHỈ soi vùng MENU. Trước đây soi cả body -> dính chữ "Khoá học" trong nội dung
            # dashboard (thẻ thống kê), báo lỗi giả.
            info = page.evaluate("""() => {
                const sel = ['#sidebar-menu', '.left-side-menu', '.hub-rail', '.sidebar', 'aside', 'nav']
                let menuText = ''
                for (const s of sel) {
                    const el = document.querySelector(s)
                    if (el && el.innerText.length > menuText.length) menuText = el.innerText
                }
                const items = menuText.split('\\n').map(s => s.trim()).filter(Boolean)
                return { coMucDaAn: items.includes('Khoá học'), soMuc: items.length, bodyLen: document.body.innerText.length }
            }""")
            check("I1." + key, "%s: mục menu đã ẩn KHÔNG còn trong menu" % key, info["coMucDaAn"], False)
            check("I2." + key, "%s: các mục menu khác vẫn còn (menu không rỗng)" % key, info["soMuc"] > 5, True)
            check("I3." + key, "%s: màn vẫn chạy bình thường (không trắng trang)" % key, info["bodyLen"] > 200, True)

        # ---------------------------------------------------------------- J. API LỖI -> FAIL-OPEN
        print("\n=== J. Cấu hình rỗng / lỗi -> hiện đầy đủ (fail-open) ===")
        set_config(admin_token, [])
        ui_logout(page); ui_login(page, *ACCOUNTS["admin"][:2])
        goto(page, "/timesheet/dashboard", 2500, ready="a.dropdown-item")
        links = page.eval_on_selector_all("a.dropdown-item", "els => els.map(e => e.getAttribute('href'))")
        check("J1", "xoá hết cấu hình -> menu trở lại đầy đủ",
              "/timesheet/timesheet_details" in links, True)

        browser.close()

    set_config(admin_token, [])
    print("\n================ KẾT QUẢ ================")
    fail = [r for r in results if not r[0]]
    print("Tổng: %d | PASS: %d | FAIL: %d" % (len(results), len(results) - len(fail), len(fail)))
    for r in fail:
        print("FAIL %s | %s | nhận %r, mong đợi %r" % (r[1], r[2], r[3], r[4]))
    sys.exit(1 if fail else 0)

main()
