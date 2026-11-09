$vault='C:\Users\migue\OneDrive\DOS\Valinari'
$stage='C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio\.codex-work\house-images-20261102'
if(Test-Path $stage){Remove-Item -LiteralPath $stage -Recurse -Force}; New-Item -ItemType Directory -Force -Path $stage | Out-Null
$dirs=@('Casa Real','Casas Mayores','Casas Menores','Casas Vasallas')
$houses=foreach($d in $dirs){Get-ChildItem -LiteralPath "$vault\09_Politica\$d" -Filter '*.md' -File | Where-Object {$_.BaseName -notmatch 'Índice|Perfil|Plantilla'}}
$imgs=Get-ChildItem -LiteralPath "$vault\07_Imagenes" -File | Where-Object {$_.Extension -match 'jpg|jpeg|png'}
$map=@{}; foreach($i in $imgs){$k=($i.BaseName -replace '^Casa\s+','').Trim().ToLowerInvariant(); if(!$map.ContainsKey($k)){$map[$k]=$i.Name}}
$linked=@(); $unavailable=@()
foreach($h in $houses){
  $rel=$h.FullName.Substring($vault.Length).TrimStart('\'); $out=Join-Path $stage $rel; New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null
  $text=[IO.File]::ReadAllText($h.FullName); $body=$text.TrimEnd()
  $key=($h.BaseName -replace '^Casa\s+','').Trim().ToLowerInvariant(); $img=$null
  if($map.ContainsKey($key)){$img=$map[$key]} elseif($key -eq 'eryn lasgalen' -and $map.ContainsKey('eryn lasgale')){$img=$map['eryn lasgale']}
  if($text -notmatch '!\[\[' -and $text -notmatch '!\[[^]]*\]\(' -and $img){
    $section="`r`n`r`n## Representación visual`r`n`r`n![[07_Imagenes/$img]]`r`n`r`n_Imagen asociada automáticamente por correspondencia nominal con la ficha de la casa._`r`n"
    $body += $section; $linked += "$($h.BaseName)|$img"
  } elseif($text -notmatch '!\[\[' -and $text -notmatch '!\[[^]]*\]\(' -and !$img){$unavailable += $h.BaseName}
  [IO.File]::WriteAllText($out,$body+"`r`n",(New-Object Text.UTF8Encoding($false)))
}
@{linked=$linked; unavailable=$unavailable; house_count=$houses.Count} | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $stage 'manifest.json') -Encoding UTF8
Write-Output "LINKED=$($linked.Count) UNAVAILABLE=$($unavailable.Count) HOUSES=$($houses.Count)"
