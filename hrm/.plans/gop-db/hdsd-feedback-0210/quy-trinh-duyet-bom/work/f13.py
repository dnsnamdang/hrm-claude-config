from common import *
with browser_page() as page:
    go(page,'/assign/bom-list')
    icon(page, page.locator('a', has_text='BOM-2026-00027').first, 'link_ma_bom')
