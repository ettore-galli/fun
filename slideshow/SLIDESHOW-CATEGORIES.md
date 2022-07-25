---
marp: true
---

# Teoria delle categorie e programmazione funzionale

Una raccolta di idee di base e spunti

---

# Sorgente

https://bartoszmilewski.com/2014/10/28/category-theory-for-programmers-the-preface/

---

# 1 - Category: The Essence of Composition

https://bartoszmilewski.com/2014/11/04/category-the-essence-of-composition/

- Composizione
- Concatenamento
- Funzione identità

---

# 2 - Types and Functions

https://bartoszmilewski.com/2014/11/24/types-and-functions/

- tipizzazione -> composizione
- bottom/undefined
- funzioni parziali / totali

---

# 2 - Types and Functions (seguito...)

- Void: Ex falso sequitur quodlibet
- Unit (): Coincidenza **pratica** tra void e ()
- Boolean: True | False

---

# 3 - Categories Great and Small

- No Objects ("insieme vuoto")
- Ordini (preorder, partial order, total order)
- Monoidi

---

# 4 - Kleisli Categories

- Esempio logger
- Esempio Wrirer - funzioni "abbellite"
- kleisli.py

---

# 5 - Products and Coproducts

- Oggetto iniziale
- Oggetto finale
- Prodotto (es. Tupla)
- Coprodotto (es. Union | Enum)

---

# 6 - Simple Algebraic Data Types

- Somma = Either
    . elemento neutro: Void
- Prodotto = Record
    . elemento neutro: ()

---

# 7 - Functors
