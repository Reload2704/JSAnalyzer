// algoritmo de prueba -  Fiorella Quijano

let $precioBase = 100;
const _impuestoLocal = 0.12;
var totalCalculado = $precioBase;

function procesarPago() {
    if (totalCalculado) {
        return totalCalculado;
    } else {
        let error_interno = 1;
    }
    
    while (totalCalculado) {
        break;
    }
    
    for (let i = 0; i; i) {
        switch($precioBase) {
            default:
                break;
        }
    }
}

// =========================================================
// ERRORES SEMÁNTICOS 
// =========================================================

// ERROR 1: Uso de una variable que jamás fue declarada (Regla de Identificadores)
let calculoFalso = variableFantasma + 50;

// ERROR 2: Uso de una variable fuera de su alcance/scope (Regla de Scope)
// 'error_interno' nació dentro del 'else' de arriba, aquí afuera ya no existe en memoria.
let copiaDeError = error_interno;

// ERROR 3: Retorno inconsistente (Regla de Retorno de Funciones)
function obtenerDescuento() {
    // Retorna un string cuando la lógica de la regla espera coincidencia de tipos
    return "veinte por ciento"; 
}