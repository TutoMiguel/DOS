$src='C:\Users\migue\OneDrive\DOS\Valinari\09_Politica\Prompts Visuales de las 84 Casas.md'
$stage='C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio\.codex-work\prompt-heights-20261102'
if(Test-Path $stage){Remove-Item -LiteralPath $stage -Recurse -Force}; New-Item -ItemType Directory -Force -Path $stage | Out-Null
$text=[IO.File]::ReadAllText($src)
$pattern='(?ms)^## (Casa .+?)\r?\n(.*?)(?=^## Casa |\z)'
$count=0
$updated=[regex]::Replace($text,$pattern,{param($m)
  $name=$m.Groups[1].Value; $body=$m.Groups[2].Value
  $hm=[regex]::Match($body,'(?m)^\| Hombre \|\s*([^|]+)\|').Groups[1].Value.Trim()
  $wm=[regex]::Match($body,'(?m)^\| Mujer \|\s*([^|]+)\|').Groups[1].Value.Trim()
  if(!$hm -or !$wm){throw "No se encontraron alturas en $name"}
  $body=[regex]::Replace($body,'(?m)^\*\*Alturas consolidadas para la imagen:\*\*.*\r?\n','')
  $line="**Alturas consolidadas para la imagen:** hombre $hm; mujer $wm. Medición de planta a coronilla, sin calzado ni adornos; conservar la diferencia relativa y el mismo plano de suelo."
  $body=$body -replace '(?m)^### Prompt individual listo para copiar\r?\n',($line+"`r`n`r`n### Prompt individual listo para copiar`r`n")
  $script:count++
  return "## $name`r`n$body"
})
if($count -ne 84){throw "Se actualizaron $count secciones; se esperaban 84"}
$out=Join-Path $stage 'Prompts Visuales de las 84 Casas.md'; [IO.File]::WriteAllText($out,$updated,(New-Object Text.UTF8Encoding($false)))
Write-Output "SECTIONS_UPDATED=$count"
