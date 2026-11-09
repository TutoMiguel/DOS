$vault = 'C:\Users\migue\OneDrive\DOS\Valinari'
$stage = 'C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio\.codex-work\territory-refs-20261102'
if (Test-Path $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
New-Item -ItemType Directory -Force -Path $stage | Out-Null
$roots = @('02_Geografia','04_Mapa Politico')
$territories = foreach($root in $roots) {
  Get-ChildItem -LiteralPath (Join-Path $vault $root) -Recurse -Filter '*.md' -File | Where-Object {
    $_.BaseName -notmatch '^(Índice|Capitales del Canon|Ficha territorial)' -and
    $_.FullName -notmatch '\\Plantillas\\' -and
    $_.BaseName -notmatch '^Integración septentrional$'
  }
}
$all = Get-ChildItem -LiteralPath $vault -Recurse -Filter '*.md' -File
$contents=@{}
foreach($f in $all){$contents[$f.FullName]=[IO.File]::ReadAllText($f.FullName)}

function FirstMatch([string]$text,[string[]]$patterns,[string]$fallback){
  foreach($pat in $patterns){
    $m=[regex]::Match($text,$pat,[Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if($m.Success){ return ($m.Groups[1].Value.Trim() -replace '\s+',' ') }
  }
  return $fallback
}

foreach($t in $territories){
  $text=$contents[$t.FullName]
  $rel=$t.FullName.Substring($vault.Length).TrimStart('\').Replace('\','/')
  $relDir=Split-Path $rel -Parent
  $outDir=Join-Path $stage $relDir
  New-Item -ItemType Directory -Force -Path $outDir | Out-Null
  $out=Join-Path $outDir $t.Name
  $body=$text.TrimEnd()
  $body=[regex]::Replace($body,'(?ms)\r?\n## Datos territoriales normalizados\r?\n.*?(?=\r?\n## |\z)','')
  $body=[regex]::Replace($body,'(?ms)\r?\n## Referencias textuales\r?\n.*?(?=\r?\n## |\z)','')
  $pop=FirstMatch $text @('(?m)^\s*[-*]?\s*(?:Población(?: canónica[^:]*| proyectada[^:]*)?|poblacion)[^:]*:\s*(.+)$','(?m)^\s*Población[^\n]*$') 'No fijada de forma explícita en esta ficha.'
  $econ=FirstMatch $text @('(?m)^\s*[-*]?\s*(?:PIB(?: PPA)?|PIB|Economía|economía|Función|función)[^:]*:\s*(.+)$','(?m)^\s*[-*]?\s*Función:\s*(.+)$') 'No fijada de forma explícita en esta ficha; consultar ECON-03 y el Canon V16.'
  $dep=FirstMatch $text @('(?m)^\s*dependencia:\s*(.+)$','(?m)^\s*[-*]?\s*(?:Entidad superior|Dependencia|depende de|Protectorado de)[^:]*:\s*(.+)$','(?m)^\s*(?:Protectorado|Provincia|Capital) de ([^\.\n]+)') 'No fijada de forma explícita en esta ficha.'
  $lines=@('','## Datos territoriales normalizados','','- **Población:** '+$pop,'- **Economía y función:** '+$econ,'- **Dependencia administrativa:** '+$dep,'- **Criterio editorial:** se conservan los datos canónicos existentes; los campos no fijados quedan expresamente pendientes y no se completan por inferencia.','','## Referencias textuales','','> Referencias localizadas automáticamente en el Canon V16, la cronología maestra y las fichas territoriales relacionadas. Este bloque no sustituye los datos de la ficha.','')
  foreach($src in ($all | Where-Object {$_.FullName -ne $t.FullName -and $contents[$_.FullName] -match [regex]::Escape($t.BaseName)} | Sort-Object FullName -Unique)){
    $srel=$src.FullName.Substring($vault.Length).TrimStart('\').Replace('\','/'); $sl=$srel.Substring(0,$srel.Length-3)
    $lines += "- [[$sl|$($src.BaseName)]]"
  }
  if($lines.Count -eq 11){$lines += '- Sin menciones textuales adicionales localizadas en las notas auditadas.'}
  [IO.File]::WriteAllText($out,$body+($lines -join "`r`n")+"`r`n",(New-Object Text.UTF8Encoding($false)))
}
@{territory_count=$territories.Count; staged_root=$stage; files=@($territories.FullName)} | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $stage 'manifest.json') -Encoding UTF8
Write-Output "TERRITORY_COUNT=$($territories.Count)"
