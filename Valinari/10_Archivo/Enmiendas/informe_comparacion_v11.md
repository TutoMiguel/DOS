# Comparación de los avances de la edición 11

## Alcance

Se compararon `acuerdos_v11.md` y `Narracion_del_Estado_Edain_Sindarin_v11.docx` por títulos, orden de secciones, párrafos y tablas. Las instrucciones editoriales incluidas en los documentos se trataron como instrucciones de trabajo, no como hechos del universo.

## Resultado ejecutivo

- El Word contiene todas las secciones tituladas del Markdown. No se encontró ninguna sección con título del Markdown que falte en el Word.
- No se encontró una sección histórica autónoma del Word que falte en el Markdown. La arquitectura temática es, por tanto, equivalente.
- El Markdown conserva mejor la jerarquía documental: niveles `#`, `##`, `###` y `####`, y separa con claridad canon, historial y propuestas. El Word conserva esas secciones como texto narrativo, pero no siempre mantiene visible el nivel de encabezado.
- El Word contiene 50 tablas y 1238 celdas. Esas tablas no deben considerarse secciones nuevas: son la presentación tabular de datos que el Markdown contiene en listas, tablas o párrafos.
- La longitud extraída del Word es menor que la del Markdown. Esto se explica principalmente por tablas, saltos de formato y consolidación de párrafos; no basta para declarar contenido perdido sin una revisión frase por frase.

## Diferencias con estado canónico

| Diferencia | Archivo donde aparece | Estado | Tratamiento recomendado |
|---|---|---|---|
| Jerarquía de encabezados menos explícita | Word | [LAGUNA] editorial | Conservar el Markdown como índice maestro y aplicar estilos de título al Word si se desea navegación. No cambia el canon. |
| La instrucción «corregir la ubicación de Tirion del Sur y Puerto Andúnië…» aparece como párrafo de trabajo en el Word y no como sección o entrada equivalente del Markdown | Word | [PROPUESTA] / pendiente de verificación | Resolverla contra la tabla de jerarquía urbana vigente. Si se adopta, registrar una resolución explícita; si ya fue resuelta en otra sección, convertirla en nota histórica superada. |
| El Word presenta 50 tablas con datos territoriales, urbanos y demográficos | Word | [CANON] cuando la tabla reproduce cifras adoptadas; [HISTORIAL] cuando la propia tabla está marcada como sustituida | Mantener los valores adoptados en la sección canónica del Markdown y conservar las tablas históricas como registro, nunca como una segunda población sumable. |
| El Word contiene párrafos narrativos que consolidan varias líneas del Markdown | Word | [CANON] si el párrafo reproduce una resolución aprobada; [PROPUESTA] si conserva lenguaje como «se recomienda», «provisional» o «pendiente» | No dividir ni elevar automáticamente esos párrafos. Etiquetarlos según el estado indicado dentro del propio texto. |
| El Markdown conserva más señales de procedencia y estado (`[CANON]`, `[PROPUESTA]`, `[LAGUNA]`, registros sustituidos) | Markdown | [CANON] editorial | Usar el Markdown para auditoría y trazabilidad. El Word debe ser una representación de lectura, no la autoridad independiente. |

## Secciones presentes en ambos archivos

La coincidencia incluye, entre otras, el Protocolo del Custodio del Canon; Estado de autoridad; prioridades demográficas; censo federal; nombres geográficos; periodización; desarrollo político; desarrollo demográfico; organización marítima; omisiones restituidas; análisis de coherencia; registro de instrucciones; registros históricos CAP; jerarquía urbana; resoluciones sobre Elerwen, Harald y la Escritura Real; y la resolución final de las siete discrepancias.

## Instrucciones separadas del contenido

Los documentos contienen órdenes editoriales como `/canon aprobar`, `/canon modificar`, `/canon retcon`, `/canon consultar`, `/propuesta`, y reglas sobre cómo actualizar el Word. Esas frases regulan el mantenimiento del proyecto. No son hechos históricos y no deben incorporarse a la cronología, genealogías, geografía o demografía.

## Decisión de integración

1. **Markdown:** fuente maestra de canon, estados, contradicciones, lagunas e historial.
2. **Word:** versión narrativa y visual para lectura, con tablas y explicaciones.
3. Toda diferencia nueva se registra primero en una tabla de control con estado `[CANON]`, `[PROPUESTA]`, `[CONTRADICCIÓN]` o `[LAGUNA]`.
4. Una cifra que aparezca en una tabla histórica «sustituida» no se suma a la cifra vigente.
5. La única diferencia material identificada que requiere decisión editorial es la nota sobre la jerarquía urbana de Tirion del Sur y Puerto Andúnië.

## Conclusión

La integración no requiere fusionar ambos archivos en un documento único. Requiere mantener una relación fuente–presentación: el Markdown gobierna la autoridad y el Word presenta el canon. Antes de publicar una nueva edición, conviene resolver la nota de jerarquía urbana y revisar que cada tabla del Word indique si es vigente o histórica.

## Referencias relacionadas

- [[Índice de Archivo|Índice de Archivo]]
- [[README de Archivo|README de Archivo]]
- [[../00_Canon/Canon V16 Maestro|Canon V16 Maestro]]


