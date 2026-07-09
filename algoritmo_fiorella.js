// algoritmo de prueba -  Fiorella Quijano

let precioBase = 100;
let totalCalculado = 200;

// 1. Sintaxis limpia para la función (return estricto al final)
function procesarPago() {
    let temporal = 1;
    return temporal;
}

// 2. Sintaxis limpia para crear un bloque cerrado (Scope)
while (precioBase) {
    let error_interno = 1;
    break;
}

// =========================================================
// INYECCIÓN DE ERRORES SEMÁNTICOS EXCLUSIVOS DE FIORELLA
// =========================================================

// ERROR 1: Uso de una variable jamás declarada
// (Asignamos directamente sin usar el '+' para no activar la regla de Cecilia)
let calculoFalso = variableFantasma;

// ERROR 2: Variable fuera de alcance (Scope)
// 'error_interno' nació dentro del 'while', aquí afuera el parser no debe recordarla.
let copiaDeError = error_interno;

// ERROR 3: Retorno inconsistente
function obtenerDescuento() {
    let variableDummy = 0;
    return "veinte por ciento"; // Se retorna un String, debe generar error
}