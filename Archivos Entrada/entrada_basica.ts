let val1:number = 1;
let val2:number = 10;
let val3:number = 2021.2020;

console.log("Probando declaracion de variables \\n");
console.log(val1, " ", val2, " ", val3);
console.log("---------------------------------");

val1 = val1 + 41 - 123 * 4 / (2 + 2 * 2) - (10 + (125 % 5)) * 2 ^ 2;
val2 = 11 * (11 % (12 + -10)) + 22 / 2;
val3 = 2 ^ (5 * 12 ^ 2) + 25 / 5;
console.log("Probando asignación de variables y aritmeticas");
console.log(val1, " ", val2, " ", val3);
console.log("---------------------------------");

let rel1:boolean = (((val1 - val2) === 24) && (true && (false || 5 >= 5))) || ((7*7) !== (15+555) || -61 > 51);
let rel2:boolean = (7*7) <= (15+555) && 1 < 2;
//let rel3:boolean = (		(0 === 0) !== (   (532 > 532)  ) === ("Hola" === "Hola")) && (false || (!false));
console.log("Probando relacionales y logicas");
//console.log(rel1, " ", rel2, " ", rel3);
console.log(rel1, " ", rel2, " ");
console.log("---------------------------------");

console.log("OPERACIONES " , "CON " + "Cadenas");  // Otra forma de realizar el console.log
let despedida:string = "Adios mundo :c";
let saludo:string = "Hola Mundo! ";
console.log(saludo.toLowerCase() , despedida.toUpperCase());

console.log("Probando algunas funciones nativas de PyTypeCraft");
console.log("Funciones relacionadas a conversiones");
let carnet:string = "201903865";
console.log("Hola " + carnet.toString());
console.log("---------------------------------");