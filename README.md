El objetivo de este proyecto es desarrollar una API RESTful que permita realizar simulaciones de hipotecas para diferentes clientes.

La API permite las siguientes operaciones:
- Crear un nuevo cliente con sus datos personales y financieros (nombre, DNI, email, capital solicitado).
- Consultar los datos de un cliente existente por su DNI.
- Solicitar una simulación de hipoteca para un cliente dado, un TAE y un plazo de amortización como inputs. La API debe devolver la cuota mensual a pagar y el importe total a devolver y el sistema debe guardarlo en BBDD.
- Modificar o eliminar los datos de un cliente existente.

La API está escrita en Python, por lo que se necesita tener instalada una versión compatible de Python (recomendado: Python 3.6+). 
- Se puede descargar Python desde https://www.python.org/downloads/.

 El gestor de paquetes para Python Pip debe estar instalado en el sistema. 
 - Se puede instalkar siguiendo los pasos descritos en https://pip.pypa.io/en/stable/installation/. 

Para obtener y clonar el repositorio se debe tener instalado Git.
- Se puede descargar desde https://git-scm.com/downloads.


1. Clonar el repositorio en tu máquina local utilizando el siguiente comando:
- git clone https://github.com/SergioMollo/HipotecasAPI

2. Es recomendable usar un entorno virtual para evitar conflictos con otras dependencias de Python en tu sistema.
- cd tu_repositorio
- python -m venv venv

3. Activar el entorno virtual en Windows o Linux, respectivamente.
- venv\Scripts\activate
- source venv/bin/activate

4. Ejecutar la API asegurandose estar en el directorio donde se encuentra el script principal.
-python app.py

5. Abrir el navegador para acceder a la url generada
- http://127.0.0.1:5000/

Rutas generadas:
- /clientes [GET, POST]
- /cliente/<dni_cliente> [GET, POST, PUT, DELETE]
- /cliente/<dni_cliente>/hipoteca [POST]
