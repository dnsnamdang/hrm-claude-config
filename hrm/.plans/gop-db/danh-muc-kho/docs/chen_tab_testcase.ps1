param([Parameter(Mandatory=$true)][string]$Master, [string]$ItemsJson)
# Chèn tab testcase vào file "Testcase chuyển đổi.xlsx" (bản tải từ Drive) bằng Excel thật,
# giữ nguyên định dạng tab gốc; thêm dòng vào tab "Tổng hợp". Tab đã có thì bỏ qua (chạy lại an toàn).
# Chỉ đóng ĐÚNG tiến trình Excel do script này mở.
# -ItemsJson: file JSON (UTF-8) dạng [["<đường dẫn tuyệt đối file .xlsx>", "<tên tab ≤31 ký tự>", "<tên ở tab Tổng hợp>"], ...]
#             bỏ trống = 7 danh mục kho (đợt 1).
$ErrorActionPreference = 'Stop'
$docs = $PSScriptRoot
if ($ItemsJson) {
    # PS 5.1: ConvertFrom-Json trả CẢ mảng như 1 đối tượng qua pipeline → duyệt bằng foreach
    $arr = Get-Content -Raw -Encoding UTF8 $ItemsJson | ConvertFrom-Json
    $items = @(foreach ($e in $arr) { , @($e[0], $e[1], $e[2]) })
} else {
    $items = @(
        @('warehouses',            '44. DM kho vật lý',  'Danh mục kho vật lý'),
        @('accounting-warehouses', '45. DM kho kế toán', 'Danh mục kho kế toán'),
        @('houses',                '46. DM nhà kho',     'Danh mục nhà kho'),
        @('rows',                  '47. DM dãy',         'Danh mục dãy'),
        @('spaces',                '48. DM khoang',      'Danh mục khoang'),
        @('positions',             '49. DM vị trí',      'Danh mục vị trí'),
        @('packages',              '50. DM kiện',        'Danh mục kiện')
    ) | ForEach-Object { , @((Join-Path $docs ($_[0] + '\testcase - ' + $_[2] + '.xlsx')), $_[1], $_[2]) }
}
$before = @(Get-Process EXCEL -ErrorAction SilentlyContinue | ForEach-Object { $_.Id })
$xl = New-Object -ComObject Excel.Application
$mine = @(Get-Process EXCEL -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | ForEach-Object { $_.Id })
$xl.Visible = $false
$xl.DisplayAlerts = $false
try {
    $wb = $xl.Workbooks.Open($Master)
    $names = @(); foreach ($s in $wb.Worksheets) { $names += $s.Name }
    $sum = $wb.Worksheets.Item('Tổng hợp')
    foreach ($it in $items) {
        $file, $tab, $label = $it
        if ($names -contains $tab) { Write-Output "bỏ qua (đã có): $tab"; continue }
        if (-not (Test-Path $file)) { Write-Output "THIẾU FILE: $file"; continue }
        $src = $xl.Workbooks.Open($file, 0, $true)
        $src.Worksheets.Item(1).Copy([Type]::Missing, $wb.Worksheets.Item($wb.Worksheets.Count))
        $src.Close($false)
        $new = $wb.Worksheets.Item($wb.Worksheets.Count)
        $new.Name = $tab
        # dòng Tổng hợp: dòng trống đầu tiên ở cột B, chép định dạng dòng trên
        $r = $sum.Cells($sum.Rows.Count, 2).End(-4162).Row + 1
        $sum.Rows($r - 1).Copy() | Out-Null
        $sum.Rows($r).PasteSpecial(-4122) | Out-Null
        $sum.Cells($r, 1).Formula = '=ROW()-ROW($A$1)'
        $sum.Cells($r, 2).Value2 = $label
        $refs = @('K15', 'K11', 'K12', 'K13', 'K14')   # tổng TC, đạt, không đạt, PE, chưa chạy
        for ($i = 0; $i -lt 5; $i++) { $sum.Cells($r, 7 + $i).Formula = "='" + $tab + "'!" + $refs[$i] }
        Write-Output "đã chèn: $tab (Tổng hợp dòng $r)"
    }
    $wb.Worksheets.Item(1).Activate()
    $wb.Save()
    $wb.Close($true)
} finally {
    $xl.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
    Start-Sleep -Milliseconds 500
    foreach ($id in $mine) { Stop-Process -Id $id -Force -ErrorAction SilentlyContinue }
}
