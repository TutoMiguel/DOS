---
tipo: guía de clasificación
canon: V16
actualizado: 2026-11-10
---
# Tipos de blindado y propiedades

Las 28 fichas de vehículos tienen la propiedad de texto `tipo_blindado`, visible en Propiedades de Obsidian. La propiedad `tipo` conserva la clase de documento; no reemplaza la clasificación del vehículo. Los índices y la historia general no reciben un tipo de vehículo ficticio.

## Vocabulario de clasificación

| Valor de tipo_blindado | Uso |
| --- | --- |
| automóvil blindado | Vehículo protegido de ruedas para exploración y escolta |
| carro de combate pesado | Rama pesada de la etapa histórica anterior al carro principal |
| carro de combate ligero | Carro ligero histórico, sin capacidad anfibia implícita |
| carro de combate medio | Rama media de la etapa histórica |
| carro de combate universal | Generación de transición que reúne funciones medias y pesadas |
| carro de batalla principal | Carro principal de las generaciones contemporáneas |
| carro de combate ligero anfibio | Carro ligero con capacidad acuática declarada |
| carro de combate medio expedicionario | Línea media de apoyo expedicionario |
| vehículo de combate de infantería | Variante de referencia con cañón y grupo transportado |
| transporte blindado de personal | Transporte protegido, con subtipo anfibio cuando corresponda |
| artillería autopropulsada blindada | Plataforma artillera distinta del carro y del VCI |

## Familias mixtas

Mablung, Galdor, Haldir e Hirgon se clasifican por su configuración de referencia VCI. `tipos_variantes` registra VCI, TBP, mando, sanidad e ingeniería y apoyo. Esa lista no afirma que cada casco tenga todas las funciones ni que todas las variantes monten cañón. Las cifras `tripulantes` e `infantes_transportados` corresponden a la variante de referencia, no a cada derivado.

## Lectura de los valores

`movilidad` separa ruedas, cadenas, semiorugas y los medios acuáticos declarados. `familia` permite agrupar las generaciones Elendil sin confundirlas con un mismo modelo. `introduccion` expresa el año del catálogo; el CBT-16 emplea `introduccion_propuesta` para conservar su estado pendiente.

`produccion_acumulada` cuenta vehículos nuevos históricos de familia hasta el corte, no existencias activas. El CBT-16 no tiene esa propiedad porque su producción está pendiente; `produccion_definida` es falso y no significa cero vehículos certificados.

`potencia_especifica_cv_t` es un cálculo de potencia nominal dividido por masa de referencia. No mide rendimiento energético. La propiedad no se asigna al CBT-16 porque su masa se expresa como intervalo y el programa sigue propuesto. En este último, `eficiencia_objetivo_porcentaje` y `validacion_rendimiento` mantienen separados requisito y demostración.

## Consulta por clasificación

La tabla del índice permite navegar sin Dataview ni complementos. También puede usarse la búsqueda nativa de Obsidian con una propiedad, por ejemplo `[tipo_blindado:"vehículo de combate de infantería"]`. El valor se muestra y puede editarse en las Propiedades de cada nota.

Las propiedades se guardan como YAML al inicio de la nota, de acuerdo con la [documentación de Propiedades de Obsidian](https://obsidian.md/help/properties). La consulta usa su [búsqueda por propiedades](https://obsidian.md/help/Plugins/Search).
