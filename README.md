# El Switcher (backend).

## Descripción

Este repositorio corresponde al backend del juego "El Switcher", desarrollado para la materia Ingeniería del Software dictada el año 2024 en FAMAF.

## Tabla de Contenidos

1. [Requisitos previos](#requisitos-previos)
2. [Ejecutar el código del proyecto](#ejecutar-el-código-del-proyecto)
3. [Actualizar requirements.txt](#actualizar-requirementstxt)
4. [Dependencias necesarias para el proyecto](#dependencias-necesarias-para-el-proyecto)

## Requisitos previos.

Para poder correr este proyecto es recomendable tener la versión `3.12` de `Python`.

Además, en Python es una buena práctica trabajar dentro de un entorno virtual, ya que nos facilitará la gestión de las dependencias. Podemos crear y ejecutar un entorno virtual de la siguiente forma:

### Crear entorno virtual.

Para lograr crear un entorno virtual de manera adecuada, debemos:

1. `Instalar virtualenv`: Para poder crear un entorno virtual vamos a tener que instalar `virtualenv` de la siguiente manera:

    ```bash
    pip install virtualenv
    ```

2. `Crear el entorno virtual`: Una vez que tengamos instalado `virtualenv`, vamos a crear nuestro entorno virtual de la siguiente manera:

    ```bash
    virtualenv -p 3.10 .venv
    ```

    Dicho comando nos creará un directorio llamado `.venv`, el cuál contendrá la información de nuestro entorno virtual.

### Ejecutar entorno virtual.

Una vez que tengamos creado el entorno virtual, vamos a tener que hacer algunos de los siguientes comandos en función de su sistema operativo para poder ejecutar dicho entorno virtual:

- `Para macOS y Linux:`

  ```bash
  source .venv/bin/activate
  ```

- `Para Windows (powershell):`
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

Y notaremos que el comando ha funcionado si ahora nos aparece un `(.venv)` al inicio del prompt en la consola.

Para todos los demás pasos, este documento asumirá que estamos ejecutando el entorno virtual que hemos creado.

## Ejecutar el código del proyecto.

A continuación se darán una serie de pasos necesarios para poder ejecutar el código del proyecto:

1. `Instalar las dependencias necesarias`: Para instalar los las dependencias que necesita nuestro proyecto, haremos lo siguiente:

    ```bash
    pip install -r requirements.txt
    ```

    Esto instalará todos las dependencias definidas en el archivo `requirements.txt`, los cuáles serán precisamente las dependencias que usaremos en nuestro proyecto.


2. `Correr el proyecto`: Para correr el proyecto vamos a tener que utilizar `uvicorn`. Para lograr correrlo, tendremos que posicionarnos en el directorio llamado `src` y luego ejecutar el siguiente comando:

    ```bash
    uvicorn main:app --reload
    ```

    Esto nos dará mucha información, pero nos interesará aquella que se parezca a lo siguiente:

    ```bash
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    ```

    Esto nos está indicando que nuestro servidor está corriendo de manera local en `http://127.0.0.1:8000`.


## Actualizar requirements.txt:

En el archivo `requirements.txt` se encuentran todos las dependencias necesarias que tendrá nuestro proyecto. Si se agrega una nueva dependencia al proyecto, debemos actualizar dicho archivo usando el siguiente comando: 

```bash
pip freeze > requirements.txt
```

Obviamente, para que esto funcione de manera correcta es necesario que nuestro entorno virtual esté en funcionamiento.

## Dependencias necesarias para el proyecto.

A continuación se dará una lista de las dependencias más importantes y cuál es su funcionalidad en el proyecto:

* `FastAPI`: Es el framework que utilizaremos para crear los endpoints de nuestra API.

* `Uvicorn`: Es un servidor que utilizamos para ejecutar las aplicaciones creadas con FastAPI.

* `Pydantic`: Es una biblioteca que FastAPI utiliza para la validación y serialización de datos. Se descarga automáticamente junto con `FastAPI`.