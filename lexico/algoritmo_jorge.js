// ===================================================================
// Algoritmo de prueba - Bravo Vidal Jorge Andres
// Componente: COMENTARIOS Y OPERADORES (JavaScript)
// Alcance: solo aritmeticos, asignacion (= += -=) y logicos/comparacion.
// ===================================================================

/*
   Comentario de bloque.
   Puede ocupar varias lineas y debe reconocerse como un solo token.
*/

let a = 10          // asignacion simple
let b = 3
let resultado = 0

// ---- Operadores aritmeticos ----
resultado = a + b   // suma
resultado = a - b   // resta
resultado = a * b   // multiplicacion
resultado = a / b   // division
resultado = a % b   // modulo

// ---- Incremento y decremento ----
a++
b--

// ---- Asignacion aditiva y sustractiva ----
a += 5
a -= 2

// ---- Comparacion ----
let igual = a == b
let identico = a === b
let diferente = a != b
let mayor = a > b
let menor = a < b

// ---- Operadores logicos ----
let logico = mayor && menor
let alterno = igual || diferente
let negado = ! igual
