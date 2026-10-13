# Sinh file JS cho browser_run_code_unsafe: chèn 1 block case vào đúng tab.
import json,sys,re
def tsv(rows):
    def q(v):
        v='' if v is None else str(v)
        return '"'+v.replace('"','""')+'"' if any(ch in v for ch in '\n\t"') else v
    return '\n'.join('\t'.join(q(c) for c in r) for r in rows)

JS = r'''
async (page) => {
  const OP = __OP__;
  const W = (ms) => page.waitForTimeout(ms);
  async function go(ref){ await page.click('#t-name-box'); await page.fill('#t-name-box', ref); await page.keyboard.press('Enter'); await W(500); }
  async function val(ref){ await go(ref); return await page.evaluate(()=>{const e=document.querySelector('#t-formula-bar-input'); return e? e.innerText.replace(/\n$/,''):null}); }
  async function paste(ref, text){ await go(ref); await page.evaluate((t)=>{const dt=new DataTransfer(); dt.setData('text/plain', t); document.activeElement.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}));}, text); await W(1500); }
  async function menu(top, sub, item){ await page.click(top); await W(600); if(sub){ await page.locator('.goog-menuitem:visible',{hasText:sub}).first().hover(); await W(700);} await page.locator('.goog-menuitem:visible',{hasText:item}).first().click(); await W(1200); }
  async function merge(range){ await go(range); await menu('#docs-format-menu', /^Hợp nhất ô/, 'Hợp nhất theo chiều dọc'); const ok = page.locator('button:visible',{hasText:/^OK$/}); if(await ok.count()){ await ok.first().click(); await W(800);} }
  // chọn đúng tab
  const tid = await page.evaluate((name)=>{const el=[...document.querySelectorAll('.docs-sheet-tab')].find(e=>{const t=e.innerText.trim().split('\n').pop().trim(); return t.startsWith(name);}); return el? el.id:null;}, OP.tab);
  if(!tid) return {error:'Không thấy tab '+OP.tab};
  await page.click('#'+tid.replace(/:/g,'\\:')); await W(1500);
  const log=[];
  const cur = await val('C'+OP.after_row);
  if(cur !== OP.expect_c){ return {error:'Lệch hàng: C'+OP.after_row+' = '+JSON.stringify(cur)+' (cần '+OP.expect_c+')'}; }
  const nxt = await val('C'+(OP.after_row+1));
  if(OP.expect_next !== null && nxt !== OP.expect_next){ return {error:'Hàng sau lệch: '+JSON.stringify(nxt)+' (cần '+OP.expect_next+')'}; }
  const n = OP.n_rows;
  await go((OP.after_row-n+1)+':'+OP.after_row);
  await menu('#docs-insert-menu', /^Hàng/, 'Chèn '+n+' hàng xuống dưới');
  log.push('inserted '+n);
  if(OP.header_from){
    // chép nguyên hàng tiêu đề nhóm cũ (định dạng + ô gộp) sang hàng mới rồi ghi tiêu đề
    await go(OP.header_from+':'+OP.header_from); await page.keyboard.press('Meta+c'); await W(700);
    await go((OP.after_row+1)+':'+(OP.after_row+1)); await page.keyboard.press('Meta+v'); await W(1500);
    await paste('C'+(OP.after_row+1), OP.header_title);
    log.push('header');
  }
  await paste(OP.paste_at, OP.tsv); log.push('pasted');
  if(OP.ab_tsv){ await paste('A'+OP.first_case_row, OP.ab_tsv); }
  for(const m of OP.merges){ await merge(m); log.push('merge '+m); }
  const chk = await val('C'+OP.last_case_row);
  return {ok: chk===OP.last_id, last: chk, log};
}
'''
def build(op_json, out):
    op=json.loads(open(op_json).read())
    open(out,'w').write(JS.replace('__OP__', json.dumps(op, ensure_ascii=False)))
if __name__=='__main__': build(sys.argv[1], sys.argv[2])
