import sys; sys.path.insert(0, '/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs')
from _shoot import browser_page, clip, BASE
S = 'shots/'
ED = """(() => { const m = window.$nuxt.$route.matched; let root = m[m.length-1].instances.default;
  const find = (vm) => { if (vm.$options.name === 'BomBuilderEditor') return vm; for (const c of vm.$children) { const r = find(c); if (r) return r } return null };
  return find(root) })()"""
def ed(page, js):
    return page.evaluate("() => { const ed = %s; %s }" % (ED, js))
def wait_editor(page):
    page.wait_for_function("() => { try { const ed = %s; return ed && !ed.disabled && (ed.bomDetailLoaded || !ed.bomId) } catch(e) { return false } }" % ED, timeout=120000)
    page.wait_for_timeout(3000)
from PIL import Image
with browser_page() as page:
    page.goto(BASE + '/assign/bom-list/29', wait_until='domcontentloaded'); wait_editor(page)
    page.evaluate("() => document.querySelector('.si-header').click()"); page.wait_for_timeout(5000)
    page.evaluate("() => { const h = document.querySelector('.si-header'); const box = h.parentElement; const els = box.querySelectorAll('*'); els[els.length-1].scrollIntoView({block:'center'}); }"); page.wait_for_timeout(1500)
    page.screenshot(path=S + '24-lich-su-phieu.png')
