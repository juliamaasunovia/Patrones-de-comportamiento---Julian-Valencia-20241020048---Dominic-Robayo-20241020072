# Juego de Laberintos con Patrones de Diseño

**Autores:**
- Dominic Robayo — Código: 20241020072  
- Julián Valencia — Código: 20241020048  

---

## Descripción General del Juego

Este proyecto es un videojuego 2D desarrollado en Python con Pygame, donde el jugador debe atravesar tres niveles evitando enemigos y obstáculos para llegar a la meta final.  
El objetivo es llegar al último nivel y ganar, mientras se aplican distintos patrones de diseño de software para estructurar el código de forma modular, escalable y reutilizable.

Cada nivel presenta un diseño diferente:
- Nivel 1: Laberinto con una patrulla horizontal.
- Nivel 2: Columnas con huecos y enemigos que se mueven verticalmente más rápido.
- Nivel 3: Paredes intercaladas con huecos alternos.
- Pantalla final: mensaje de victoria al superar todos los niveles.

---

## Patrones de Diseño Utilizados

### 1. Patrón Command

**Objetivo:** encapsular las acciones del jugador como objetos independientes.  
En el juego, cada movimiento del jugador se representa como un comando (`MoveCommand`, `RestartCommand`), que puede ejecutarse o deshacerse.

**Cómo se aplica:**
- Cada vez que el jugador se mueve, se crea un comando que guarda el desplazamiento.
- Estos comandos se almacenan en una lista (`command_history`).
- Si el jugador pierde o presiona “U”, se puede deshacer el último movimiento.
- Si presiona “R”, se ejecuta un comando para reiniciar el nivel.

**Beneficio:**  
Permite tener un historial de acciones y control total sobre las operaciones ejecutadas.

---

### 2. Patrón Memento

**Objetivo:** guardar y restaurar el estado de un objeto sin exponer sus detalles internos.  
En el juego, se utiliza para guardar el estado del jugador (posición, nivel, etc.) y poder restaurarlo si pierde.

**Cómo se aplica:**
- El `PlayerCaretaker` almacena los estados del jugador en “momentos” (mementos).
- Antes de realizar un movimiento importante, se guarda un memento.
- Si el jugador choca con una pared o enemigo, se restaura el último memento para volver al punto anterior.

**Beneficio:**  
Permite volver atrás en el tiempo sin necesidad de reiniciar completamente el juego.

---

### 3. Patrón State

**Objetivo:** permitir que un objeto cambie su comportamiento dependiendo de su estado interno.  
En el juego, los enemigos usan este patrón para cambiar su tipo de movimiento.

**Cómo se aplica:**
- Cada enemigo tiene un estado que define su comportamiento:  
  - `PatrolState`: movimiento entre dos puntos.  
  - `SineState`: movimiento en curva senoidal.  
  - `FastState`: patrulla rápida.
- Cambiar el estado del enemigo cambia su forma de moverse sin modificar la clase principal.

**Beneficio:**  
Facilita agregar nuevos tipos de enemigos sin tocar el código base del enemigo.

---

## Patrón Strategy 

**Objetivo:** definir un conjunto de algoritmos intercambiables para que un objeto elija su comportamiento dinámicamente.  

**Cómo se aplica en el juego :**
- El patrón `Strategy` se habría usado en la inteligencia de los enemigos, permitiendo cambiar su estrategia de movimiento o ataque sin modificar su clase.
- Por ejemplo, podríamos tener estrategias como:
  - `AggressiveStrategy`: el enemigo persigue al jugador.  
  - `DefensiveStrategy`: el enemigo evita al jugador.  
  - `RandomStrategy`: el enemigo se mueve aleatoriamente.  
- En tiempo de ejecución, cada enemigo podría cambiar de estrategia dependiendo de las condiciones del juego (por ejemplo, si el jugador está cerca o si tiene poca vida).

**Beneficio:**  
Permite modificar el comportamiento dinámico de los enemigos de forma flexible, aplicando la misma estructura que los otros patrones.

---

## Ejecución del Juego

1. Asegúrate de tener instalado Python 3.10 o superior.
2. Instala la librería pygame:
   ```bash
   pip install pygame
