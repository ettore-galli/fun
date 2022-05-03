---
marp: true
---

# Functional programming

Una raccolta di idee e spunti

---

# Riferimenti

## Funzionale facile con typescript

https://talks.codemotion.com/funzionale--facile-con-typescript?_ga=2.134894065.1675421665.1650872817-1307759326.1650872817&_gl=1%2akkbogm%2a_ga%2aMTMwNzc1OTMyNi4xNjUwODcyODE3%2a_ga_52S30H0VCG%2aMTY1MDg3Mjg0OC4xLjEuMTY1MDg3MzA1OS4w

## Let's get functional 
https://talks.codemotion.com/lets-get-functional?_ga=2.199840302.1675421665.1650872817-1307759326.1650872817&_gl=1%2a1w6mr7n%2a_ga%2aMTMwNzc1OTMyNi4xNjUwODcyODE3%2a_ga_52S30H0VCG%2aMTY1MDkxNTUwOS4zLjEuMTY1MDkxNTY1NS4w

---

# Valori (Caratteristiche) della programmazione funzionale

## Funzioni pure

## Immutabilità dei valori

## Funzionidi livello superiore

## Minimi side effect (da approfondire...)

---

# Vantaggi della programmazione funzionale

## Testabilità

## Meno errori

## Più facili da testare e debaggare

## Più facili da riutilizzare

---

# Applicazioni della programmazione funzionale

## Componenti funzionali di React (funzioni vs classi)

## Reducers (immutabilità)

---

# Librerie funzionali JS

Lodash.js

Ramda

Underscore.js

---

# Tipologie di side effect

Richieste asincrone

Logging 

Routing

Aggiornamenti periodici

---

# Come integrare i side effect nel mondo funzionale

Injection

"Barare e procrastinare"

Redux Thunk

 
---
# Come equando implementare il funzionale

## Non sempre, non al 100%
## Python / typescript non sono linguaggi funzionali puri
## Per implementare sezioni di logica
## Per implementare workflow e gestire side effect in modo controllato
## Migliorare la testabilità
---
## Funzionale:

### Motivi

### Tecniche
#### Map / filter / reduce

#### Ricorsione
#### Reduce come forma di ricorsione (python)

#### Tail call elimination
https://stackoverflow.com/questions/37224520/are-functions-in-javascript-tail-call-optimized
## Python - workflow imperativo


## Python - workflow monadico sincrono

// Side effect in javascript
https://jrsinclair.com/articles/2018/how-to-deal-with-dirty-side-effects-in-your-pure-functional-javascript/#fn:4

workflow_python/workflow.py
## Python - workflow asincrono / asyncio


## Python - workflow asincrono / generatori


## JS - workflow promise tradizionale


## JS - promise 

