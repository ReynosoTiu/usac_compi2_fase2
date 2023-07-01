const mapas = ["Desierto", "Bosque", "Mar", "Ciudad"];
const enemigos = ["Enano", "Troll", "Caballero", "Arquero", "Maquina"];
const jugadores = ["Ronald", "Manuel","Jhonatan","Cesar","Pablo"];

let score: number[][][] = [
    [
        [18,16,20,15,98]
    ],
    [
        [25,10,8,45,100]
    ]
];

function insertarValores(array: number[][][]) {
    array.push([[125,110,18,145,1100]]);
    array.push([[56,98,78,190,8200]]);
    for (let i = 0; i < 4; i++) {
        for (let j = 1; j < 5; j++) {
            array[i].push([i+j+34, i+j+56, i+j+76, i+j+20, i+j+50]);
        }
    }
}

function imprimirReporte(value: number, i: number, j: number, k: number) {
    console.log(mapas[i] + ", " + enemigos[j] + ", " + jugadores[k] + ", " + value);
}

function imprimirScore(array: number[][][]) {
    for (let i = 0; i < length(array); i++) {
        for (let j = 0; j < length(array[i]); j++) {
            for (let k = 0; k < length(array[i][j]); k++) {
                imprimirReporte(array[i][j][k], i, j, k);
            }
        }
    }
}

insertarValores(score);
console.log("Mapa" + "          " + "Enemigo" + "          " + "Jugador" + "          " + "Derrotados");    
imprimirScore(score);
