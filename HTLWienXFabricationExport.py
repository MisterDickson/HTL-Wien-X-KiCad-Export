import pcbnew
import os
import subprocess

class HTLWienXFabricationExport(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Fertigungsunterlagen exportieren"
        self.category = "Fabrication"
        self.description = "Exportiert die Layer F.Cu und B.Cu als SVG und die Bohrinformationen als EXC."
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'HTLWienX_24x24.png')

    def Run(self):
        board = pcbnew.GetBoard()
        board_path = board.GetFileName()
        board_directory = os.path.dirname(board_path)

        fabrication_directory = os.path.join(board_directory, 'Fabrication')
        if not os.path.exists(fabrication_directory):
            os.makedirs(fabrication_directory)

        output_filename = os.path.join(fabrication_directory, os.path.splitext(os.path.basename(board_path))[0] + '-Bottom.svg')

        # Export B.Cu layer as SVG, black and white, the page as big as the board itself and not the drawing sheet (page size mode 2), exclude drawing sheet, negative, named {filename}-Bottom.svg, in a directory called /Fabrication/ located in the same directory as the board file
        # F.Cu is mirrored so the ink is closer to the copper
        fCuExportCommand = "kicad-cli pcb export svg -o \""+output_filename+"-Top.svg\" --layers F.Cu --mirror -n --black-and-white --page-size-mode 2 --exclude-drawing-sheet "+board_path
        bCuExportCommand = "kicad-cli pcb export svg -o \""+output_filename+"-Bottom.svg\" --layers B.Cu -n --black-and-white --page-size-mode 2 --exclude-drawing-sheet "+board_path
        drillExportCommand = "kicad-cli pcb export drill -o "+fabrication_directory+" --drill-origin plot --excellon-zeros-format suppressleading -u in --excellon-min-header "+board_path

        subprocess.run(bCuExportCommand)
        subprocess.run(fCuExportCommand)
        subprocess.run(drillExportCommand)

        # Split DRL to EXC and Tool Info File
        drl_file = os.path.join(fabrication_directory, os.path.splitext(os.path.basename(board_path))[0] + '.drl')
        exc_file = os.path.join(fabrication_directory, os.path.splitext(os.path.basename(board_path))[0] + '.exc')
        tool_file = os.path.join(fabrication_directory, os.path.splitext(os.path.basename(board_path))[0] + '-Bohrer.txt')


        tool_diameters = []
        with open(drl_file, 'r') as drl:
            # Skip to tool list
            while True:
                line = drl.readline()
                if line.startswith('T1'):
                    break
            
            # Read tool list
            while '%' not in line:
                parts = line.strip().split('C')
                tool_id = parts[0]  # e.g., T1
                diameter_inch = float(parts[1])  # e.g., 0.0315
                diameter_mm = diameter_inch * 25.4  # Convert to mm
                tool_diameters.append((tool_id, diameter_mm))
                line = drl.readline()

            # Sort by diameter (2nd element of tuple)
            tool_diameters.sort(key=lambda x: x[1])

            # Write coordinates to EXC file with absolute Y-coordinates
            with open(exc_file, 'w') as exc:
                while True:
                    line = drl.readline()
                    if not line:
                        break
                    exc.write(line.replace('Y-', 'Y'))
        
        # Write tool info to tool file
        with open(tool_file, 'w') as tool:
            tool.write('Bohrplotter        OG-ID\n========================\n')
            i = 1
            missing_tool_warning = False
            for tool_id, diameter_mm in tool_diameters:
                writeline = f'T{i:03.0f} {diameter_mm:4.1f} mm '
                if diameter_mm < 0.8:
                    writeline += '(!)'
                    missing_tool_warning = True
                else:
                    writeline += '   '
                
                writeline += f'   {tool_id}\n'

                tool.write(writeline)

                i += 1
            
            if missing_tool_warning:
                tool.write('\n(!) Nicht im Sortiment\n')
        
        # Delete DRL file
        os.remove(drl_file)

HTLWienXFabricationExport().register() # Instantiate and register to Pcbnew
