let random = [1, 5, 8, -1, 21, 42, -55, 123, -5, 5, 11];

let a = [
  [
    random[1] * 3,
    51,
    random[4] / 2,
    (random[3] * 10) % 7
  ],
  [
    1,
    2,
    3,
    4
  ]
];

let b = [
  [
    1,
    2,
    3,
    4
  ],
  [
    random[1] * 3,
    51,
    random[4] / 2,
    (random[3] * 10) % 7
  ]
];

let auxiliar = [
  [
    0.0,
    0.0,
    0.0,
    0.0
  ],
  [
    0.0,
    0.0,
    0.0,
    0.0
  ]
];

function printMatriz(matrix: any[][]) {
    console.log("[");
    for (let i = 0; i < length(matrix) ; i++) { // Los length pueden manejarlos como arreglo.length
        console.log("[");
        for (let j = 0; j < length(matrix[i]); j++) { // Los length pueden manejarlos como arreglo.length
            console.log(matrix[i][j] + " ");
        }
        console.log("]");
    }
    console.log("]");
}

function sumarMatrices(matrix1: any[][], matrix2: any[][]): any[][] | string {
  if (length(matrix1) !== length(matrix2)) { // Los length pueden manejarlos como arreglo.length
    return "NO SE PUEDEN SUMAR. NO SON DE LA MISMA LONGITUD";
  }

  for (let i = 0; i < length(matrix1); i++) { // Los length pueden manejarlos como arreglo.length
    for (let j = 0; j < length(matrix1[i]); j++) { // Los length pueden manejarlos como arreglo.length
      auxiliar[i][j] = matrix1[i][j] + matrix2[i][j];
    }
  }
  return auxiliar;
}

function compararMatrices(matrix1: any[][], matrix2: any[][]): boolean {
  if (length(matrix1) !== length(matrix2)) { // Los length pueden manejarlos como arreglo.length
    return false;
  }

  for (let i = 0; i < length(matrix1); i++) { // Los length pueden manejarlos como arreglo.length
    for (let j = 0; j < length(matrix1[i]); j++) { // Los length pueden manejarlos como arreglo.length
      if (matrix1[i][j] !== matrix2[i][j]) {
        return false;
      }
    }
  }
  return true;
}

console.log("MATRIZ a");
printMatriz(a);
console.log("");
console.log("MATRIZ b");
printMatriz(b);

console.log("");
console.log("LAS DOS MATRICES SUMADAS");
console.log(sumarMatrices(a, b));

console.log("");
console.log("COMPARAR MATRICES. SON IGUALES?");
console.log(compararMatrices(a, b));

console.log("");
console.log("Push a b");
b.push([3010.1999]);
printMatriz(b);

b = a;
console.log("");
console.log("COMPARAR MATRICES. SON IGUALES?");
console.log(compararMatrices(a, b));
