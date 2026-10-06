"""Chụp màn chi tiết / tạo mới (chỉ mở form & popup, KHÔNG bấm lưu)."""
import sys, os, re
sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots') + '/'


def esc(page):
    page.keyboard.press('Escape'); page.wait_for_timeout(800)


def tab(page, name):
    page.locator('button, a, div', has_text=re.compile(r'^\s*%s\s*$' % name)).filter(
        has=page.locator('i')).first.click()
    page.wait_for_timeout(1500)


with browser_page() as page:
    # ---- Lịch sử meeting 52 từ danh sách
    page.goto(BASE + '/assign/meeting', wait_until='domcontentloaded')
    page.get_by_text('TPE.MET.NB.26.0067').first.wait_for(timeout=90000)
    page.wait_for_timeout(2000)
    row = page.locator('tr', has_text='TPE.MET.NB.26.0067').first
    row.locator('td').last.evaluate("el => el.scrollIntoView({inline: 'end', block: 'center'})")
    page.wait_for_timeout(600)
    acts = row.locator('td').last.locator('.v2-icon-btn')
    clip(page, acts.nth(0), D + 'icon_n_in_row.png')
    clip(page, acts.nth(1), D + 'icon_n_lichsu_row.png')
    acts.nth(1).click(); page.wait_for_timeout(4000)
    page.screenshot(path=D + 'n03_history.png')
    esc(page)

    # ---- Chi tiết meeting 52 — tab Biên bản (chế độ xem)
    page.goto(BASE + '/assign/meeting/52/show', wait_until='domcontentloaded')
    page.get_by_text('Thành phần — Phía Công ty').first.wait_for(timeout=90000)
    page.wait_for_timeout(2500)
    clip(page, page.locator('.v2-tab, button, a').filter(has_text=re.compile(r'^\s*Nhiệm vụ\s*$')).first, D + 'icon_n_tab_nhiemvu.png')
    page.get_by_text('Biên bản', exact=True).first.click(); page.wait_for_timeout(2500)
    page.screenshot(path=D + 'n10_report_show.png')
    clip(page, page.locator('button:visible').filter(has_text=re.compile(r'^\s*Excel\s*$')).first, D + 'icon_n_excel_bb.png')
    gv = page.locator('button[title="Giao nhiệm vụ"]:visible, [title="Giao nhiệm vụ"]:visible').first
    gv.scroll_into_view_if_needed(); page.wait_for_timeout(500)
    clip(page, gv, D + 'icon_n_giaonv.png')
    page.screenshot(path=D + 'n10b_report_show_row.png')
    page.evaluate('window.scrollTo(0,0)'); page.wait_for_timeout(500)
    page.locator('button:visible').filter(has_text=re.compile(r'^\s*Excel\s*$')).first.click()
    page.wait_for_timeout(1500)
    page.screenshot(path=D + 'n11_excel_config.png')
    esc(page)
    gv.scroll_into_view_if_needed(); gv.click(); page.wait_for_timeout(3500)
    page.screenshot(path=D + 'n12_assign_task.png')
    esc(page); page.wait_for_timeout(800)
    page.evaluate('window.scrollTo(0,0)')
    page.get_by_text('Nhiệm vụ', exact=True).first.click(); page.wait_for_timeout(3500)
    page.screenshot(path=D + 'n13_tasks_tab.png')
    # khối Lịch sử cuối màn chi tiết
    page.get_by_text('Thông tin', exact=True).first.click(); page.wait_for_timeout(1500)
    page.screenshot(path=D + 'n09_detail.png')

    # ---- Tạo mới: nhánh Họp đối tác + Meeting theo dự án
    page.goto(BASE + '/assign/meeting/create', wait_until='domcontentloaded')
    page.get_by_text('Thành phần — Phía Công ty').first.wait_for(timeout=90000)
    page.wait_for_timeout(2500)
    page.get_by_text('Họp đối tác', exact=True).first.click(); page.wait_for_timeout(1500)
    page.screenshot(path=D + 'n15_create_partner.png')
    page.get_by_text('Meeting theo dự án', exact=True).first.click(); page.wait_for_timeout(2000)
    page.screenshot(path=D + 'n16_create_project.png')
