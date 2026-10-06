"""Chụp lại popup Lịch sử của meeting 52 (chờ tải xong)."""
import sys, os
sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots') + '/'
with browser_page() as page:
    page.goto(BASE + '/assign/meeting', wait_until='domcontentloaded')
    page.get_by_text('TPE.MET.NB.26.0067').first.wait_for(timeout=90000)
    page.wait_for_timeout(2000)
    row = page.locator('tr', has_text='TPE.MET.NB.26.0067').first
    row.locator('td').last.evaluate("el => el.scrollIntoView({inline: 'end', block: 'center'})")
    page.wait_for_timeout(600)
    row.locator('td').last.locator('.v2-icon-btn').nth(1).click()
    page.wait_for_timeout(45000)
    page.wait_for_timeout(2500)
    page.screenshot(path=D + 'n03_history.png')
