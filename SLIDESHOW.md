---
marp: true
---

# Functional programming

Una raccolta di idee e spunti

---

# Riferimenti e fonti di ispirazione

## Funzionale facile con typescript

https://talks.codemotion.com/funzionale--facile-con-typescript?_ga=2.134894065.1675421665.1650872817-1307759326.1650872817&_gl=1%2akkbogm%2a_ga%2aMTMwNzc1OTMyNi4xNjUwODcyODE3%2a_ga_52S30H0VCG%2aMTY1MDg3Mjg0OC4xLjEuMTY1MDg3MzA1OS4w

## Let's get functional
https://talks.codemotion.com/lets-get-functional?_ga=2.199840302.1675421665.1650872817-1307759326.1650872817&_gl=1%2a1w6mr7n%2a_ga%2aMTMwNzc1OTMyNi4xNjUwODcyODE3%2a_ga_52S30H0VCG%2aMTY1MDkxNTUwOS4zLjEuMTY1MDkxNTY1NS4w

## Stack Wars: Functional programming strikes back
https://talks.codemotion.com/stack-wars-functional-programming-strike?_ga=2.21931899.1326689086.1652619683-1663033125.1652035888&_gl=1%2a1ji6zbu%2a_ga%2aMTY2MzAzMzEyNS4xNjUyMDM1ODg4%2a_ga_52S30H0VCG%2aMTY1MjYxOTcxNy4xLjEuMTY1MjYxOTg3Ni4w

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



#### Tail call elimination
https://stackoverflow.com/questions/37224520/are-functions-in-javascript-tail-call-optimized
## Python - workflow imperativo


## Python - workflow monadico 

// Side effect in javascript
https://jrsinclair.com/articles/2018/how-to-deal-with-dirty-side-effects-in-your-pure-functional-javascript/#fn:4

workflow_python/workflow.py


---

## Riferimenti

Functors, Applicatives, And Monads In Pictures

https://adit.io/posts/2013-04-17-functors,_applicatives,_and_monads_in_pictures.html

Functional Programming illustrated in Python: Part 4 / 5

https://brian-candler.medium.com/function-programming-illustrated-in-python-part-4-bc8948ec6433

https://brian-candler.medium.com/function-programming-illustrated-in-python-part-5-90c4882b21b7