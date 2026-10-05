S = 'shots/'
def crop_w(path, w):
    im = Image.open(path); im.crop((0, 0, min(w, im.width), im.height)).save(path)
def goto_list(page):
    page.goto(BASE + '/assign/quotations', wait_until='domcontentloaded')
    page.locator('a.v2-cell-link', has_text='BG-2026-00098').first.wait_for(timeout=180000)
    page.wait_for_timeout(2500)
def scroll_table(page, x):
    page.evaluate("x => document.querySelectorAll('.table-wrapper').forEach(e => e.scrollLeft = x)", x)
    page.wait_for_timeout(600)
def esc(page):
    page.keyboard.press('Escape'); page.wait_for_timeout(1000)
def pick_select2(page, container, text, typed=None):
    for i in range(30):
        container.locator('.select2-selection').first.click(); page.wait_for_timeout(1000)
        if page.locator('.select2-container--open .select2-results__option', has_text=text).count(): break
        page.keyboard.press('Escape'); page.wait_for_timeout(3000)
    if typed:
        page.locator('.select2-container--open .select2-search__field').fill(typed); page.wait_for_timeout(1500)
    page.locator('.select2-container--open .select2-results__option', has_text=text).first.click()
    page.wait_for_timeout(1000)
def goto_create(page):
    page.goto(BASE + '/assign/quotations/create', wait_until='domcontentloaded')
    page.get_by_text('Chọn dự án trước').first.wait_for(timeout=180000); page.wait_for_timeout(4000)
def goto_edit(page, qid):
    page.goto(BASE + '/assign/quotations/%d/edit' % qid, wait_until='domcontentloaded')
    page.locator('.products-wrap').first.wait_for(timeout=180000); page.wait_for_timeout(5000)
def T(fn, name):
    try: fn()
    except Exception as e: print('FAIL', name, str(e)[:300])
def scroll_to(page, sel):
    page.locator(sel).first.scroll_into_view_if_needed(); page.wait_for_timeout(800)
