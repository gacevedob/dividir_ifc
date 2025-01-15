import os
import ifcopenshell
from shutil import copyfile

class Patcher:
    def __init__(self, src, file, logger, args=None):
        self.src = src
        self.file = file
        self.logger = logger
        self.args = args

    def patch(self):
        storeys = self.file.by_type('IfcBuildingStorey')
        for i, storey in enumerate(storeys):
            dest = '{}-{}.ifc'.format(i, storey.Name)
            copyfile(self.src, dest)  # Copia el archivo de origen
            old_ifc = ifcopenshell.open(dest)
            new_ifc = ifcopenshell.file(schema=self.file.schema)
            if self.file.schema == 'IFC2X3':
                elements = old_ifc.by_type('IfcProject') + old_ifc.by_type('IfcProduct')
            else:
                elements = old_ifc.by_type('IfcContext') + old_ifc.by_type('IfcProduct')
            
            inverse_elements = []
            for element in elements:
                if element.is_a('IfcElement') and not self.is_in_storey(element, storey):
                    element.Representation = None
                    continue
                if element.is_a('IfcElement'):
                    styled_rep_items = [i for i in old_ifc.traverse(element) if i.is_a('IfcRepresentationItem') and i.StyledByItem]
                    [new_ifc.add(i.StyledByItem[0]) for i in styled_rep_items]
                new_ifc.add(element)
                inverse_elements.extend(old_ifc.get_inverse(element))
            
            for inverse_element in inverse_elements:
                new_ifc.add(inverse_element)
            
            for element in new_ifc.by_type('IfcElement'):
                if not self.is_in_storey(element, storey):
                    new_ifc.remove(element)
            
            # Crear la carpeta para los archivos divididos
            output_folder = os.path.join(os.path.dirname(self.src), "Archivos_Divididos")
            os.makedirs(output_folder, exist_ok=True)
            
            output_file_name = f"{i}-{storey.Name.replace(' ', '_')}.ifc"
            output_file_path = os.path.join(output_folder, output_file_name)
            
            # Guardar el archivo dividido
            new_ifc.write(output_file_path)
            self.logger(f"Archivo guardado: {output_file_path}")

    def is_in_storey(self, element, storey):
        return element.ContainedInStructure \
            and element.ContainedInStructure[0].RelatingStructure.is_a('IfcBuildingStorey') \
            and element.ContainedInStructure[0].RelatingStructure.GlobalId == storey.GlobalId

# Usar la clase Patcher para dividir el archivo IFC
input_file = r"RUTA AL ARCHIVO"

# Cargar el archivo IFC
try:
    model = ifcopenshell.open(input_file)
except Exception as e:
    print(f"Error al cargar el archivo IFC: {e}")
    exit(1)

# Instancia del logger (simple print)
def logger(msg):
    print(msg)

# Instancia de la clase Patcher
patcher = Patcher(src=input_file, file=model, logger=logger)

# Ejecutar el método patch
patcher.patch()
