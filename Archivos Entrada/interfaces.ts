interface Actor {
    nombre: string;
    edad: number;
}

interface Pelicula {
    nombre: string;
    posicion: number;
}

interface Contrato {
    actor: Actor;
    pelicula: Pelicula;
}

const actores = ["Elizabeth Olsen", "Adam Sandler", "Christian Bale", "Jennifer Aniston"];
const peliculas = ["Avengers: Age of Ultron", "Mr. Deeds", "Batman: The Dark Knight", "Marley & Me"];

function contratar(actor: Actor, pelicula: Pelicula): Contrato {
    return {
        actor,
        pelicula,
    };
}

function crearActor(nombre: string, edad: number): Actor {
    return {
        nombre,
        edad,
};
}

function crearPelicula(nombre: string, posicion: number): Pelicula {
    return {
        nombre,
        posicion,
    };
}
function imprimir(contrato: Contrato): void {
    console.log("Actor:", contrato.actor.nombre, "   Edad:", contrato.actor.edad);
    console.log("Pelicula:", contrato.pelicula.nombre, "   Genero:", contrato.pelicula.posicion);
}
function contratos(): void {
    for (let i = 1; i < 3; i++) {
        let contrato: Contrato = {
        actor: { nombre: "", edad: 0 },
        pelicula: { nombre: "", posicion: 0 },
        };
        if (i < 4) {
        const actor = crearActor(actores[i - 1], i + 38);
        const pelicula = crearPelicula(peliculas[i - 1], i);
        contrato = contratar(actor, pelicula);
        }
        imprimir(contrato);
    }
}

contratos();