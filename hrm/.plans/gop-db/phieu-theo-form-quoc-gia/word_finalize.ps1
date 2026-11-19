param([Parameter(Mandatory=$true)][string]$Docx, [string]$Pdf)
# Mở file bằng Word thật: cập nhật mục lục + số trang + field, bỏ nhúng font, lưu; tuỳ chọn xuất PDF.
# Chỉ dọn ĐÚNG tiến trình Word do script này mở (so danh sách PID trước/sau), không đụng Word khác.
$ErrorActionPreference = 'Stop'
$before = @(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object { $_.Id })
$word = New-Object -ComObject Word.Application
$mine = @(Get-Process WINWORD -ErrorAction SilentlyContinue | Where-Object { $before -notcontains $_.Id } | ForEach-Object { $_.Id })
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($Docx, $false, $false, $false)
    $doc.EmbedTrueTypeFonts = $false
    $doc.Repaginate()
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Fields.Update() | Out-Null
    foreach ($toc in $doc.TablesOfContents) { $toc.UpdatePageNumbers() }
    $doc.Save()
    $pages = $doc.ComputeStatistics(2)
    Write-Output "PAGES=$pages"
    if ($Pdf) { $doc.ExportAsFixedFormat($Pdf, 17); Write-Output "PDF=$Pdf" }
    try { $doc.Close(0) } catch {}
} finally {
    try { $word.Quit() } catch {}
    try { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null } catch {}
    Start-Sleep -Seconds 2
    foreach ($id in $mine) { Stop-Process -Id $id -Force -ErrorAction SilentlyContinue }
}
