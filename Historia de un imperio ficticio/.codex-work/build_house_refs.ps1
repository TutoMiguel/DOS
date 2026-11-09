$vault = 'C:\Users\migue\OneDrive\DOS\Valinari'
$stage = 'C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio\.codex-work\house-refs-20261102'
$stageHouse = Join-Path $stage '09_Politica'
New-Item -ItemType Directory -Force -Path $stage | Out-Null
if (Test-Path $stageHouse) { Remove-Item -LiteralPath $stageHouse -Recurse -Force }
New-Item -ItemType Directory -Force -Path $stageHouse | Out-Null

$houseDirs = @('Casa Real','Casas Mayores','Casas Menores','Casas Vasallas')
$houses = foreach ($d in $houseDirs) {
  Get-ChildItem -LiteralPath (Join-Path $vault "09_Politica\$d") -Filter '*.md' -File | Where-Object { $_.BaseName -notmatch 'Índice|Perfil|Plantilla' }
}
$all = Get-ChildItem -LiteralPath $vault -Recurse -Filter '*.md' -File
$contents = @{}
foreach ($f in $all) { $contents[$f.FullName] = [IO.File]::ReadAllText($f.FullName) }

foreach ($h in $houses) {
  $houseName = $h.BaseName
  $mentions = @()
  foreach ($src in $all) {
    if ($src.FullName -eq $h.FullName) { continue }
    $txt = $contents[$src.FullName]
    if ($txt -match [regex]::Escape($houseName)) { $mentions += $src }
  }
  $mentions = $mentions | Sort-Object FullName -Unique
  $relativeDir = Split-Path ($h.FullName.Substring($vault.Length).TrimStart('\')) -Parent
  $outDir = Join-Path $stageHouse $relativeDir
  New-Item -ItemType Directory -Force -Path $outDir | Out-Null
  $out = Join-Path $outDir $h.Name
  $body = $contents[$h.FullName].TrimEnd()
  $body = [regex]::Replace($body, '(?ms)\r?\n## Referencias textuales\r?\n.*?(?=\r?\n## |\z)', '')
  $lines = @('','## Referencias textuales','', '> Referencias localizadas automáticamente en el Canon V16, la cronología maestra y las fichas relacionadas. Este bloque no sustituye el contenido histórico de la ficha.','')
  foreach ($src in $mentions) {
    $rel = $src.FullName.Substring($vault.Length).TrimStart('\').Replace('\','/')
    $link = $rel.Substring(0,$rel.Length-3)
    $label = $src.BaseName
    $lines += "- [[$link|$label]]"
  }
  if ($mentions.Count -eq 0) { $lines += '- Sin menciones textuales adicionales localizadas en las notas auditadas.' }
  [IO.File]::WriteAllText($out, $body + ($lines -join "`r`n") + "`r`n", (New-Object Text.UTF8Encoding($false)))
}

@{
  house_count = $houses.Count
  staged_root = $stageHouse
  files = @($houses | ForEach-Object { $_.FullName })
} | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $stage 'manifest.json') -Encoding UTF8
Write-Output "HOUSE_COUNT=$($houses.Count)"
