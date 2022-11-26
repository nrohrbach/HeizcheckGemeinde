# Wie gross ist der Anteil der Heizöl-, Gas- und Elektroheizungen in einer Gemeinde?

## Motivation
Ein Drittel des Energieverbrauchs in der Schweiz wird durch Haushalte verursacht. Ein grosser Teil dieses Energieverbrauchs entsteht durch Gebäudeheizungen. In der Schweiz werden 60% der Gebäude mit Gas oder Öl beheizt. Durch den Ukrainekrieg sind die Energiepreise stark gestiegen, insbesondere für Gas und Öl. Dadurch müssen Haushalte und Betriebe welche mit Öl oder Gas heizen, mit höheren Ausgaben rechnen. Diese zusätzliche finanzielle Belastung der Bevölkerung ist nicht regelmässig verteilt und trifft nicht alle Regionen oder Gemeinden im gleichen Ausmass. Darum soll mit dieser Arbeit analysiert werden, wie stark verschiedene Gemeinden von den steigenden Energiepreisen betroffen sind.

## Idee
Die Auswirkungen hoher Energiepreise werden anhand von vier Kennzahlen bewertet. Die vier Kennzahlen werden für alle Gemeinden der Schweiz täglich berechnet. Die Resultate sind in einem webbasierten Dashboard verfügbar.

## Methoden
Jede Kennzahl wird in einem eigenen Pythonskript berechnet. Die Methode ist auf folgenden Seiten detailliert beschrieben:
* [Wie gross ist der Anteil von Gas-, Heizöl, und Elektroheizungen in einer Gemeinde?](https://nrohrbach.github.io/HeizcheckGemeinde/1.1_Anteil_Heizungen_GHE)
* [Wie viele EinwohnerInne und Beschäftigte sind duch hohe Öl- und Gaspreise in einer Gemeinde betroffen?](https://nrohrbach.github.io/HeizcheckGemeinde/1.2_Anzahl_Einwohnende)
* [Welche Gebiete in einer Gemeinde sind am stärksten betroffen?](https://nrohrbach.github.io/HeizcheckGemeinde/1.3_Energiequellen_GHE)
* [Wie hat sich der Anteil fossiler Heizungen in den letzten 20 Jahren in einer Gemeinde verändert?](https://nrohrbach.github.io/HeizcheckGemeinde/1.4_Zeitreihe_fossiler_Heizungen)

## Resultat
Die vier Kennzahlen sind für alle Gemeinden in folgendem Dashboard visualisiert:
[<img src="https://raw.githubusercontent.com/nrohrbach/HeizcheckGemeinde/pages/Bilder/Dashboard.gif" width="90%"/>](https://dash.rei.st/)

## Verwendete Daten
Folgende Daten wurden verwendet:
* [Gebäude- und Wohnungsregister](https://www.housing-stat.ch/de/madd/public.html)
* [Statistik der Bevölkerung und der Haushalte](https://opendata.swiss/de/dataset/bevolkerungsstatistik-einwohner)
* [swissBOUNDARIES3D](https://www.swisstopo.admin.ch/de/geodata/landscape/boundaries3d.html)


## Notebook für Dashboard
Das Notebook in welchem das Dashboard erstellt wird ist hier verfügbar:
* [Notebook](https://github.com/nrohrbach/HeizcheckGemeinde/blob/pages/Visualisierung_Energiequellen_Dash.md)
