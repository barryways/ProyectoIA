Collecting workspace information```markdown
# ProyectoIA - Clasificador de Noticias con Naive Bayes

Este proyecto es una aplicación web que utiliza un modelo de clasificación Naive Bayes para predecir la categoría de una noticia ingresada por el usuario. Las categorías disponibles son: negocios, entretenimiento, política, deportes y tecnología.

## Estructura del Proyecto

```
├── app.py                  # Archivo principal de la aplicación Flask
├── filtro.py               # Filtro para cargar y procesar textos
├── naive_bayes.py          # Implementación del modelo Naive Bayes
├── modelo_naive_bayes.pkl  # Modelo entrenado guardado en formato pickle
├── static/
│   ├── css/
│   │   └── styles.css      # Estilos CSS para la interfaz
│   ├── js/
│   │   └── script.js       # Lógica del cliente en JavaScript
├── templates/
│   └── analyst.html        # Plantilla HTML para la interfaz
├── .gitignore              # Archivos y carpetas ignorados por Git
├── README.md               # Documentación del proyecto
```

## Requisitos

- Python 3.8 o superior
- Flask
- Bibliotecas adicionales: `pickle`, `pathlib`, `collections`, `math`, `unicodedata`, `re`

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd ProyectoIA
   ```

2. Instala las dependencias necesarias:
   ```bash
   pip install flask
   ```

3. Asegúrate de que el archivo `modelo_naive_bayes.pkl` esté presente en el directorio raíz. Si no existe, el modelo se entrenará automáticamente al iniciar la aplicación.

## Uso

1. Inicia la aplicación Flask:
   ```bash
   python app.py
   ```

2. Abre tu navegador y accede a `http://127.0.0.1:5000/api/v1/analyst`.

3. Ingresa una noticia en el campo de texto y presiona el botón "Mandar". La aplicación clasificará la noticia en una de las categorías disponibles.

## Archivos Clave

### `app.py`
- Archivo principal que define las rutas de la aplicación Flask.
- Maneja solicitudes POST para clasificar noticias y GET para renderizar la interfaz.

### `naive_bayes.py`
- Implementa el modelo Naive Bayes para la clasificación de textos.
- Incluye métodos para entrenar el modelo, preprocesar texto y realizar predicciones.

### `filtro.py`
- Carga y organiza los textos de entrenamiento desde diferentes directorios.

### `static/` y `templates/`
- Contienen los archivos estáticos (CSS, JS) y las plantillas HTML para la interfaz de usuario.

## Notas

- El modelo Naive Bayes se entrena automáticamente si no se encuentra el archivo `modelo_naive_bayes.pkl`.
- Los textos de entrenamiento deben estar organizados en carpetas según las categorías especificadas en `filtro.py`.

## Contribuciones

Si deseas contribuir a este proyecto, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la licencia MIT.
```