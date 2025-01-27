# Installation
Die Dateien ```HTLWienXFabricationExport.py``` und ```HTLWienX_24x24.png``` ins KiCad-Verzeichnis für Skript-Plugins ablegen. <br>Ein üblicher Pfad ist Dokumente/KiCad/8.0/scripting/plugins.

# Anwendung
Board-Datei öffnen.

Nullpunkt setzen. 'Place' -> 'Drill/Place File Origin'.<br> Grundsätzlich in der linken unteren Ecke der Leiterplattenkontur. Bei einseitigen Platinen kann der Nullpunkt auch rechts unten positioniert werden um ein besseres Bohrergebnis zu erzielen. In diesem Fall muss aber die Kupferseite des Rohmaterials nach oben (zum Bohrkopf) zeigen.

Etwaige Änderungen speichern.

Den Button mit dem HTL-Logo in der Symbolleiste anklicken.

![image](https://github.com/user-attachments/assets/eee9040e-141d-4f46-8514-aa0ffaee2715)

Im Verzeichnis der Board-Datei wird ein Ordner namens "Fabrication" angelegt. In diesem Ordner werden die Kupfer-Schablonen als SVG- und die Bohrinformationen als EXC- und TXT-Dateien gespeichert.
