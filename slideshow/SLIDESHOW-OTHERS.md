---
marp: true
---

# Applicazioni della programmazione funzionale

## Componenti funzionali di React (funzioni vs classi)

## Reducers (immutabilità)

---


# Librerie funzionali JS

Lodash.js

Ramda

Underscore.js

# Come integrare i side effect nel mondo funzionale / 

**DA APPROFONDIRE**

* Come si fa a gestire il caso di:
    - scrivo
    - rileggo

* Nel workflow come si fa a testare il tutto in modo funzionale
    (non scrivere come bind ma ad esempio elenco?)


---
# Tecniche funzionali

* Passare funzioni

* filter, map, reduce

* Ricorsione

* currying

* partial application

---
## Funzionale:

### Motivi

### Tecniche
#### Map / filter / reduce

#### Ricorsione
#### Reduce come forma di ricorsione (python)

---
## Python - workflow asincrono / asyncio

---
## Python - workflow asincrono / generatori

---
## JS - workflow promise tradizionale

---

## JS - promise

---

# Esempio Injection 

```python
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Result:
    success: Optional[bool] = True
    message: Optional[str] = None
    data: Optional[float] = None

    def __repr__(self) -> str:
        return self.data if self.success else self.message
```

---

# Esempio Injection 

```python
def ask_for_input():
    return input()


def process(input_value: Optional[Any]) -> Result:
    try:
        return Result(data=f"*** {float(input_value) * 5} ***")
    except Exception as error:
        return Result(success=False, message=str(error))


def output_result(result):
    print("-" * 50)
    print(result)
    print("-" * 50)

```

---

# Esempio Injection 

```python

def workflow(get_input, process, put_output):
    input_value = get_input()
    result = process(input_value)
    put_output(result)


if __name__ == '__main__':
    workflow(ask_for_input, process, output_result)
```

---

# Esempio Injection 

* Trasparenza referenziale: passo le funzioni come valori
* "Lazy" (compatibilmente con python) perchè le funzioni sono eseguite

---