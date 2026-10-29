// Chạy trong trang ERP firm-quotations/create: ERP classes = đáp án, window.HQP = util HRM.
async ({ erpData, hrmData, trials, seed }) => {
  let s = seed
  const rnd = () => { s = (s * 1103515245 + 12345) % 2147483648; return s / 2147483648 }
  const ri = (a, b) => a + Math.floor(rnd() * (b - a + 1))
  const fakeQ = { calculateCombo() {}, addTabCombo() {}, removeTabCombo() {}, addGiftTabCombo() {}, price_type: 1 }
  const out = { mismatches: [], trials: [], stats: { trials: 0, clamped: 0, groupsCompared: 0, giftsReached: 0 } }
  const erpIds = erpData.combo_campaigns.map(c => c.id).sort((a, b) => a - b)
  const hrmIds = hrmData.combo_campaigns.map(c => c.id).sort((a, b) => a - b)
  out.campaignIds = { erp: erpIds, hrm: hrmIds, erpGifts: erpData.gifts.map(g => g.id), hrmGifts: hrmData.gifts.map(g => g.id) }
  for (let t = 0; t < trials; t++) {
    const cat = new FirmQuotationCategory(JSON.parse(JSON.stringify(erpData)), fakeQ)
    const hcat = HQP.normalizeCategory(JSON.parse(JSON.stringify(hrmData)))
    const raw = { qty: {}, combo: {}, sel: {} }
    const dense = rnd() < 0.5
    // 1) SL mua
    for (const camp of cat.combo_campaigns) {
      const h = hcat.combo_campaigns.find(c => c.id == camp.id)
      if (!h) continue
      if (rnd() < (dense ? 0.7 : 0.25) || camp.type == '1') {
        if (camp.type == '1') {
          const v = rnd() < 0.3 ? 0 : ri(0, 12)
          camp.select_combo_qty = v; h.select_combo_qty = v; raw.combo[camp.id] = v
        } else {
          for (const p of camp.products) {
            if (rnd() < 0.6) {
              let v = rnd() < 0.15 ? ri(0, 40) + 0.5 : ri(0, 30)
              p.qty = v
              const hp = h.products.find(x => x.product_id == p.product_id); hp.qty = v
              raw.qty[camp.id + ':' + p.product_id] = v
            }
          }
        }
      }
    }
    // 2) chọn quà (mã thường trước, quà nhóm sau)
    const pickAll = (erpCamps, hrmCamps) => {
      for (const camp of erpCamps) {
        const h = hrmCamps.find(c => c.id == camp.id)
        for (const g of camp.calculated_combo) {
          for (const o of g.options) {
            const want = rnd() < 0.4 ? 0 : ri(0, rnd() < 0.2 ? 15 : 3)
            o.select_qty = want
            raw.sel[o.combo_option_id] = want
            if (o.select_qty != want) out.stats.clamped++
          }
        }
        // HRM nhận đúng SL ERP chốt (sau clamp)
        for (const g of camp.calculated_combo) for (const o of g.options) h.selections[o.combo_option_id] = o.select_qty
      }
    }
    pickAll(cat.combo_campaigns, hcat.combo_campaigns)
    pickAll(cat.gifts, hcat.gifts)
    // 3) so sánh
    const hr = HQP.calculateCategory(hcat)
    const cmp = (erpCamp, hc, kind) => {
      const tag = `t${t} ${kind} ${erpCamp.id}`
      if (!hc) { out.mismatches.push(`${tag}: HRM thiếu mã`); return }
      if (Number(erpCamp.combo_qty) !== hc.Q) out.mismatches.push(`${tag}: Q erp=${erpCamp.combo_qty} hrm=${hc.Q}`)
      const eg = erpCamp.calculated_combo
      if (eg.length !== hc.groups.length) { out.mismatches.push(`${tag}: số nhóm erp=${eg.length} hrm=${hc.groups.length}`); return }
      eg.forEach((g, gi) => {
        out.stats.groupsCompared++
        const hg = hc.groups[gi]
        if (g.combo_group_id != hg.id) out.mismatches.push(`${tag} g${gi}: group id erp=${g.combo_group_id} hrm=${hg.id}`)
        if (Number(g.combo_qty) !== hg.combo_qty) out.mismatches.push(`${tag} g${gi}: mốc erp=${g.combo_qty} hrm=${hg.combo_qty}`)
        g.options.forEach((o, oi) => {
          const ho = hg.options[oi]
          if (!ho || o.combo_option_id != ho.id) { out.mismatches.push(`${tag} g${gi} o${oi}: option lệch`); return }
          if (o.select_qty !== ho.select_qty) out.mismatches.push(`${tag} o${o.combo_option_id}: select erp=${o.select_qty} hrm=${ho.select_qty}`)
          if (o.max_take_qty !== undefined && o.select_qty + o.max_take_qty !== ho.max_select_qty) out.mismatches.push(`${tag} o${o.combo_option_id}: max chọn erp=${o.select_qty + o.max_take_qty} hrm=${ho.max_select_qty}`)
          o.products.forEach((p, pi) => {
            const hp = ho.products[pi]
            if (!hp || hp.id != p.combo_option_product_id && hp.combo_option_product_id != p.combo_option_product_id) { out.mismatches.push(`${tag} o${o.combo_option_id} p${pi}: product lệch ${JSON.stringify(hp && {id: hp.id})}`); return }
            if (Number(p.take_qty) !== hp.take_qty) out.mismatches.push(`${tag} op${p.combo_option_product_id}: take erp=${p.take_qty} hrm=${hp.take_qty}`)
            if (o.max_take_qty !== undefined && Number(p.total_can_take) !== hp.can_take_qty) out.mismatches.push(`${tag} op${p.combo_option_product_id}: can_take erp=${p.total_can_take} hrm=${hp.can_take_qty}`)
          })
        })
      })
    }
    cat.combo_campaigns.forEach(c => cmp(c, hr.campaigns.find(x => x.camp.id == c.id), 'camp'))
    cat.gifts.forEach(c => { if (c.calculated_combo.length) out.stats.giftsReached++; cmp(c, hr.gifts.find(x => x.camp.id == c.id), 'gift') })
    // hàng tặng gộp: ERP all_combos tính từ list_products (chỉ option select>0) — so tổng take theo product+unit
    const erpGift = {}
    ;[...cat.combo_campaigns, ...cat.gifts].forEach(c => c.calculated_combo.forEach(g => g.options.forEach(o => { if (o.select_qty > 0) o.products.forEach(p => { const k = p.product_id + '_' + p.unit_id; erpGift[k] = (erpGift[k] || 0) + Number(p.take_qty) }) })))
    const hrmGift = {}
    HQP.giftSummary([hcat]).forEach(g => { hrmGift[g.product_id + '_' + g.unit_id] = g.quantity })
    if (JSON.stringify(Object.entries(erpGift).sort()) !== JSON.stringify(Object.entries(hrmGift).sort())) out.mismatches.push(`t${t} giftSummary erp=${JSON.stringify(erpGift)} hrm=${JSON.stringify(hrmGift)}`)
    out.stats.trials++
    out.trials.push({ raw, final: JSON.parse(JSON.stringify(HQP.toPayload([hcat])[0])), erpGift })
  }
  return out
}
