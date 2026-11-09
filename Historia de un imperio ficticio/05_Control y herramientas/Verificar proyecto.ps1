param([switch]$Inventario)
$ErrorActionPreference='Stop'
$cfg=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'rutas_proyecto.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$argsTask=@((Join-Path $PSScriptRoot 'gestionar_proyecto_canon.py'),'--guardar-informe')
if($Inventario){$argsTask+='--inventario'}
& $cfg.python_runtime -X utf8 @argsTask
if($LASTEXITCODE -ne 0){Write-Warning 'Hay diferencias entre los originales y las exportaciones. Consulta Estado de sincronizacion.json.'}
