---
marp: true
---

# Functional programming

Una raccolta di idee e spunti

---

# Vantaggi della programmazione funzionale

## Testabilità

## Meno errori

## Più facili da testare e _debuggare_


## Più facili da riutilizzare
---
# Come e quando usare uno stile funzionale

## Python / JS / Java / Go non sono funzionali puri
Non sempre, non necessariamente al 100%

## Per implementare singole sezioni di logica e workflow

## Per implementare workflow e gestire side effect in modo controllato

---

# Valori (Caratteristiche) della programmazione funzionale / 1 

## Funzioni pure
- Restituiscono sempre e solo valori
- Sostituibili con funzioni che restituiscono solo valori 

## Immutabilità dei valori

## Trasparenza referenziale

---

# Valori (Caratteristiche) della programmazione funzionale / 2

## Divide et impera 
Funzioni piccole e focalizzate
## Funzioni come entità "first class"

- Argomenti di funzioni
- Non legate a strutture

## Idealmente nessun side effect 

---
 

# Valori (Caratteristiche) della programmazione funzionale / 3

## Composizione di funzioni 

La composizione di funzioni sta alla base di tutto

## Best fit con linguaggi fortemente tipizzati

La composizione ha come prerequisito la compatibilità dei tipi

---
 

# Funzioni "totali" / 1

Definite per tutti i possibili valori di input

```python
def exp2(x):
    return 2**x
```

---
 
# Funzioni totali / 2

Un **contro**esempio

```python
def reciproco(x):
    return 1.0 / x
```

---
 
# Funzioni totali / 3

Metodo 1 : Restringere input

```python
x != 0

1.0 / x == ":-)" 
```

---
 
# Funzioni totali / 4

Metodo 2 : Allargare l'output -> Dare un "contesto"

```python
class Risultato
    valore: float
    successo: boolean

```

---

# Elementi dello sviluppo funzionale

## Composizione

## Gestione dei side effect

---

# Composizione

La composizione può essere vista come un concatenamento
(es. "pipe")


---

# Come integrare i side effect nel mondo funzionale

Injection

"Barare e procrastinare"

 ==> Incapsulare in una funzione

Redux Thunk incapsula l'esecuzione dei side effect in una if

---

# Come integrare i side effect nel mondo funzionale / 2

Allargamento dell'output -> casistiche di funzionamento (es. ecezioni) a valori ritornati (file inesistente simile a divisione per zero)

Sostituzione di un side effect con un valore che lo rappresenta (tipicamente una lambda), in modo tale da diventare indistinguibile da esso

Le funzioni pure non sono pure (nel senso che i side effect ci sono) solamente possono essere viste e sostituite con il loro valore 

=> esempio il workflow

fare esempio connettori audio
---



