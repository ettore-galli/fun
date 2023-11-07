# Functional ETL (Toy project)

## Workflow

- Lettura sorgente
- Processing per record (es. millimetri, nome uppercase...)
- Filtro per record (es. scartare i più grossi es primo campo > 8)
- Load e salvataggio in destinazione (es. CSV o DB) -> Interfaccia
- Rilettura output o intermedio e processamento in bulk, es.
  - Calcolo totali
  - Ricalcolo valori normalizzati a 1
- Logging per item
- Logging per step (es. filtro)
- Fallimento per certe condizioni (es. uno specifico valore)

## Desiderata (a tendere)

- Pipeline
- Funzionale
- Processing parallelo
- Multi sorgente
- Multi output
