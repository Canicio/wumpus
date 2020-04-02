wumpus
======

### Requerimientos
* Python 3.6.2+ (recomendado usar virtualenv)

### Configuración
Fichero config.py. Por ejemplo, para jugar sobre un tablero de 8x8, con 3 pozos y 5 flechas:
```text
N_BOARD_CELLS = 8
N_WATER_WELL = 3
N_ARROWS = 5
```
Para mostrar el tablero y sus elementos (pozos, oro, etc) cada vez que se ejecute una acción indicar `HIDE_BOARD = False`. En el caso de querer jugar guiándose solo por las percepcciones inidicar `HIDE_BOARD = True`
```text
...
HIDE_BOARD = False
```

### Ejecutar
```bash
$ python -m wumpus
```

### Ejecutar tests
```bash
$ python -m unittest -v
```
