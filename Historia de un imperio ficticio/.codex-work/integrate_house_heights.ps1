$vault='C:\Users\migue\OneDrive\DOS\Valinari'
$prompt=Join-Path $vault '09_Politica\Prompts Visuales de las 84 Casas.md'
$c=[IO.File]::ReadAllText($prompt)
$secs=[regex]::Matches($c,'(?ms)^## (Casa .+?)\r?\n(.*?)(?=^## Casa |\z)')
$rows=@(); foreach($s in $secs){$hm=[regex]::Match($s.Groups[2].Value,'\*\*Alturas consolidadas para la imagen:\*\* hombre ([^;]+); mujer ([^.]+)\.').Groups; $rows += "| $($s.Groups[1].Value) | $($hm[1].Value.Trim()) | $($hm[2].Value.Trim()) |"}
$table=@('','## Alturas consolidadas de representación visual de las 84 Casas','','Estas alturas pertenecen a la dirección artística de los prompts de imagen y no constituyen datos biográficos obligatorios ni rasgos genéticos. Se miden de planta a coronilla, sin calzado ni adornos; los dos representantes deben aparecer sobre el mismo plano de suelo. La Casa Telcontar conserva su excepción aprobada de 1,97 m y 1,88 m.','','| Casa | Hombre | Mujer |','|---|---:|---:|')+$rows+@('')
$block=$table -join "`r`n"
$targets=@(
  (Join-Path $vault '00_Canon\Canon V16 Maestro.md'),
  (Join-Path $vault '01_Cronologia\Cronología Territorial V16.md'),
  'C:\Users\migue\OneDrive\DOS\Historia de un imperio ficticio\cronologia_maestra_atlantica_v12.md',
  'C:\Users\migue\OneDrive\DOS\Historia de un imperio ficticio\Canon V16 Maestro.md'
)
$stage='C:\Users\migue\Documents\ChatGPT\Historia de un imperio ficticio\.codex-work\height-integration-20261102'
if(Test-Path $stage){Remove-Item -LiteralPath $stage -Recurse -Force}; New-Item -ItemType Directory -Force -Path $stage | Out-Null
foreach($t in $targets){if(!(Test-Path $t)){continue}; $txt=[IO.File]::ReadAllText($t); $txt=[regex]::Replace($txt,'(?ms)\r?\n## Alturas consolidadas de representación visual de las 84 Casas\r?\n.*?(?=\r?\n## |\z)',''); $new=$txt.TrimEnd()+"`r`n"+$block+"`r`n"; $rel=$t.Substring($vault.Length).TrimStart('\'); if($t -notlike "$vault*"){$rel='WORK_'+[IO.Path]::GetFileName($t)}; $out=Join-Path $stage $rel; New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null; [IO.File]::WriteAllText($out,$new,(New-Object Text.UTF8Encoding($false))) }
Write-Output "ROWS=$($rows.Count) STAGED=$((Get-ChildItem -LiteralPath $stage -Recurse -Filter '*.md').Count)"
