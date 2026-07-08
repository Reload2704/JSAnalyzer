// ===================================================================
// Algoritmo de prueba - Bravo Vidal Jorge Andres
// ===================================================================

/*
   Comentario de bloque.
   Se reconoce como un solo token y no afecta el analisis.
*/

// ---- Operadores aritmeticos (como inicializadores) ----
let a = 10;
let b = 3;
let suma = a + b;
let resta = a - b;
let producto = a * b;
let division = a / b;
let modulo = a % b;

// ---- Comparacion ----
let igual = a == b;
let identico = a === b;
let diferente = a != b;
let mayor = a > b;
let menor = a < b;

// ---- Operadores logicos ----
let logico = mayor && menor;
let alterno = igual || diferente;
let negado = !igual;

// ---- Ciclo while con break valido (dentro del bucle) ----
while (mayor) {
    break;
}

// ---- Ciclo for con incremento ----
for (let i = 0; i < 5; i++) {
    console.log(i);
}

// ---- Impresion ----
console.log(suma);

// ---- ERROR SEMANTICO 1: no se puede convertir "Hola" a number ----
let numero = Number("Hola");

// ---- ERROR SEMANTICO 2: 'break' fuera de un ciclo ----
break;
