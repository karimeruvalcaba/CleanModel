# 🚀 Simulación de Aspiradoras Autónomas con Mesa 🧹🤖

## ✨ Descripción
Este proyecto utiliza el framework Mesa para simular un entorno donde varias aspiradoras (Vacuum), obstáculos y suciedad interactúan en un espacio 2D. El objetivo es que las aspiradoras limpien la mayor cantidad de suciedad posible dentro de un tiempo limitado, utilizando diferentes comportamientos de búsqueda. 🕵️‍♂️🗑️

## ⚙️ Funcionalidades
La simulación incluye:

### Aspiradoras (Vacuum) con distintos comportamientos para moverse y limpiar:
- 🔄 **Random**: movimiento aleatorio.
- 🧭 **Greedy**: se mueven hacia la suciedad más cercana.
- 🚀 **A* (A-star)**: utilizan el algoritmo A* para llegar al objetivo de la manera más eficiente posible.

### Obstáculos (ObstacleAgent) 🧱
Bloquean el movimiento de las aspiradoras.

### Suciedad (Dirt) 🟫
Representa las celdas sucias que deben limpiarse.

## 🛠️ Cómo Funciona
Las aspiradoras limpian las celdas al pasar sobre ellas 🧼. La simulación se detiene cuando todas las celdas están limpias ✨ o se acaba el tiempo ⏰.

Se recopilan métricas durante la simulación, incluyendo:
- 🔢 **Porcentaje de celdas limpias.**
- 🏃‍♂️ **Número de movimientos realizados por las aspiradoras.**

## 🗂️ Estructura del Código

### 1. server.py - 🖥️ Configuración del Servidor y Visualización
Este script configura el servidor de Mesa para ejecutar y visualizar la simulación.

Define los parámetros ajustables por el usuario:
- 🪣 **Dirt Percentage**: porcentaje inicial de suciedad en la cuadrícula.
- 🧹 **Number of Sliders**: número de aspiradoras.
- ⏳ **Seconds**: duración máxima de la simulación.
- 🔄 **Cleaning Behavior**: comportamiento de las aspiradoras (random, greedy, a_star).

Usa `CanvasGrid` para renderizar la cuadrícula 📊 y `ChartModule` para graficar el porcentaje de limpieza y movimientos 📈.

### 2. model.py - 🧩 Modelo Principal
Define la clase `MyModel` que controla el entorno y la simulación.

Inicializa la cuadrícula y posiciona aleatoriamente los agentes (aspiradoras, obstáculos y suciedad) 🗺️.

#### Métodos importantes:
- 📊 `count_type()`: calcula el porcentaje de celdas limpias.
- 🏃‍♂️ `count_moves()`: cuenta el número total de movimientos realizados por todas las aspiradoras.
- 📏 `get_distance()`: calcula la distancia Manhattan entre dos puntos.

### 3. agent.py - 👾 Agentes (Aspiradoras, Obstáculos y Suciedad)
Define los comportamientos de cada agente:

#### 🚓 Aspiradora (Vacuum)
- Métodos clave:
  - 🔄 `random_move()`: movimiento aleatorio.
  - 🧭 `greedy_nearest_dirt()`: se mueve hacia la suciedad más cercana.
  - 🚀 `a_star_to_nearest_dirt()`: usa A* para encontrar la ruta óptima.
  - 🧹 `clean_if_dirty()`: limpia la suciedad en la posición actual.

#### 🧱 Obstáculo (ObstacleAgent)
Agente pasivo que solo bloquea el movimiento de las aspiradoras.

#### 🟫 Suciedad (Dirt)
Agente que cambia su estado a "limpio" cuando una aspiradora pasa sobre él.

## 🛠️ Instrucciones para Ejecutar la Simulación

### ✅ Requisitos Previos
- 🐍 **Python 3.8+**
- 📦 **Paquetes necesarios**: mesa

Instalar Mesa ejecutando:

```bash
pip install mesa


### ▶️ Ejecución
Para iniciar el servidor y visualizar la simulación, ejecuta:

```bash
python server.py

## ⚙️ Personalización
Puedes ajustar los parámetros de la simulación utilizando los controles en la interfaz web para experimentar con distintos comportamientos y configuraciones 🛠️🖱️.

## 📈 Futuras Mejoras
- 🔍 **Agregar más algoritmos de búsqueda y limpieza.**
- ➡️ **Permitir el movimiento diagonal para las aspiradoras.**
- 🧱 **Implementar diferentes tipos de obstáculos con características adicionales.**
