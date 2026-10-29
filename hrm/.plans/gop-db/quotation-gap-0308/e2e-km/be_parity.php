$ps = app(Modules\Assign\Services\QuotationPromotionService::class);
$all = json_decode(file_get_contents('/private/tmp/claude-501/-Users-manhcuong-Desktop-dns-HRM/48345148-7d74-4a08-868e-521b2108aea7/scratchpad/e2e/parity_trials.json'), true);
$tot = ['final_ok'=>0,'final_bad'=>0,'gift_ok'=>0,'gift_bad'=>0,'raw_ok'=>0,'raw_bad'=>0,'raw_err_cases'=>0];
$samples = [];
foreach ($all as $cid => $pack) {
  $cat = $ps->catalog([(int)$cid])[(int)$cid];
  // option -> group, campaign
  $optGroup = []; $campType = []; $isGift = [];
  foreach (array_merge($cat['combo_campaigns'], $cat['gifts']) as $c) {
    $campType[$c['id']] = $c['type'];
    foreach ($c['checkpoints'] as $cp) foreach ($cp['groups'] as $g) foreach ($g['options'] as $o) $optGroup[$o['id']] = [$c['id'], $g['id']];
  }
  foreach ($pack['trials'] as $ti => $t) {
    // 1) payload cuối (SL ERP đã chốt) — BE phải không lỗi + hàng tặng khớp ERP
    $errors = [];
    $r = $ps->calculateCategory($cat, $t['final'], $errors);
    if ($errors) { $tot['final_bad']++; if (count($samples) < 8) $samples[] = "CT$cid t$ti final errors: " . json_encode($errors, JSON_UNESCAPED_UNICODE); } else $tot['final_ok']++;
    $g = [];
    foreach (array_merge($r['combo_campaigns'], $r['gifts']) as $c) foreach ($c['calculated_groups'] as $gr) foreach ($gr['options'] as $o) foreach ($o['products'] as $p) {
      if ($p['take_qty'] > 0) { $k = $p['product_id'].'_'.$p['unit_id']; $g[$k] = ($g[$k] ?? 0) + $p['take_qty']; }
    }
    $e = $t['erpGift']; $e = array_filter($e, function ($v) { return $v > 0; }); ksort($e); ksort($g);
    if (json_encode(array_map('floatval', $e)) === json_encode(array_map('floatval', $g))) $tot['gift_ok']++; else { $tot['gift_bad']++; if (count($samples) < 8) $samples[] = "CT$cid t$ti gift erp=".json_encode($e)." be=".json_encode($g); }
    // 2) payload THÔ (trước khi ERP kéo về) — BE phải báo lỗi đúng khi ERP phải kéo về
    $finalSel = [];
    foreach (array_merge($t['final']['combo_campaigns'], $t['final']['gifts']) as $c) foreach ($c['groups'] as $gr) foreach ($gr['options'] as $o) $finalSel[$o['combo_option_id']] = $o['select_qty'];
    $clamped = false;
    foreach ($t['raw']['sel'] as $oid => $v) if ((float)$v != (float)($finalSel[$oid] ?? 0)) $clamped = true;
    $raw = ['combo_campaigns' => [], 'gifts' => []];
    $byCamp = [];
    foreach ($t['raw']['sel'] as $oid => $v) { [$camp, $gid] = $optGroup[$oid]; $byCamp[$camp][$gid][] = ['combo_option_id' => (int)$oid, 'select_qty' => $v]; }
    foreach ($cat['combo_campaigns'] as $c) {
      $item = ['combo_campaign_id' => $c['id'], 'products' => [], 'groups' => []];
      if ($c['type'] === '1') $item['select_combo_qty'] = $t['raw']['combo'][$c['id']] ?? 0;
      foreach ($t['raw']['qty'] as $k => $v) { [$camp, $pid] = explode(':', $k); if ($camp == $c['id']) $item['products'][] = ['product_id' => (int)$pid, 'qty' => $v]; }
      foreach ($byCamp[$c['id']] ?? [] as $gid => $opts) $item['groups'][] = ['combo_group_id' => $gid, 'options' => $opts];
      $raw['combo_campaigns'][] = $item;
    }
    foreach ($cat['gifts'] as $c) {
      $item = ['combo_campaign_id' => $c['id'], 'groups' => []];
      foreach ($byCamp[$c['id']] ?? [] as $gid => $opts) $item['groups'][] = ['combo_group_id' => $gid, 'options' => $opts];
      $raw['gifts'][] = $item;
    }
    $errors = [];
    $ps->calculateCategory($cat, $raw, $errors);
    if ($clamped) $tot['raw_err_cases']++;
    if ((bool)$errors === $clamped) $tot['raw_ok']++; else { $tot['raw_bad']++; if (count($samples) < 8) $samples[] = "CT$cid t$ti clamped=".json_encode($clamped)." be_errors=".json_encode($errors, JSON_UNESCAPED_UNICODE); }
  }
}
echo json_encode($tot) . "\n" . implode("\n", $samples) . "\nEND\n";
