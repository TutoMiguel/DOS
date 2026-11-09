$ErrorActionPreference='Stop'
$cfg=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'rutas_proyecto.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$buildTask=Join-Path $PSScriptRoot ('Preparaciones\'+(Get-Date -Format 'yyyyMMdd_HHmmss'))
& $cfg.python_runtime -X utf8 (Join-Path $PSScriptRoot 'regenerar_word_v16.py') --source $cfg.documents.canon.path --work $buildTask
if($LASTEXITCODE -ne 0){throw 'La generación del Word no terminó correctamente.'}
Write-Output ('Word preparado para revisión: '+(Join-Path $buildTask 'Canon V16 Maestro.docx'))
Write-Output 'Falta renderizar, revisar y publicar antes de sustituir los documentos oficiales.'
