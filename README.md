# IFC File Splitter

Este repositorio contiene un script desarrollado en Python que utiliza la biblioteca `ifcopenshell` para dividir un archivo IFC en archivos individuales, cada uno correspondiente a un nivel (`IfcBuildingStorey`) del modelo. El script organiza automáticamente los archivos resultantes en una carpeta específica para facilitar su manejo.

## Características

- Divide un archivo IFC en subarchivos según los niveles del modelo (`IfcBuildingStorey`).
- Mantiene la estructura de elementos relacionados con cada nivel.
- Soporte para esquemas IFC2X3 y posteriores.
- Genera una carpeta llamada `Archivos_Divididos` donde se almacenan los subarchivos.

## Requisitos

- Python 3.6 o superior.
- Biblioteca `ifcopenshell`.
- Archivo IFC válido como entrada.

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/ifc-file-splitter.git
   cd ifc-file-splitter
   
2. Instala ifcopenshell:
   ```bash
    pip install ifcopenshell

## Uso
1. Asegúrate de tener un archivo IFC válido para procesar.
2. Modifica el valor de input_file en el script con la ruta completa a tu archivo IFC.
3. Ejecuta el script

    ```bash
    dividir_ifc.py

4. Los subarchivos generados se guardarán en una carpeta llamada Archivos_Divididos en el mismo directorio que el archivo de entrada.
