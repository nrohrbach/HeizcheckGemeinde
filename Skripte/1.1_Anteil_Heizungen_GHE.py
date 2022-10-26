#!/usr/bin/env python
# coding: utf-8

# # Fragestellung 1.1: 
# ## Wie gross ist der Anteil fossiler Heizungen in einer Gemeinde?
# 
# Um diese Frage zu beantworten, werden Daten aus dem "Gebäude- und Wohnungsregister" (GWR) verwendet. <br>
# [Link zum GWR](https://www.housing-stat.ch/de/index.html)<br>
# [Link zur GWR Dokumentation](https://www.housing-stat.ch/de/docs/index.html)<br>
# [Link zum GWR Download](https://www.housing-stat.ch/de/madd/public.html)<br>
# <br>
# Die Daten werden nach Gemeinde und Energiequelle gruppiert und dann die einzelnen Objekte gezählt. <br>
# Anschliessend wird die resultierende Liste als CSV-Datei zur weiterverarbeitung bzw. Visualisierung exportiert.<br>
# <br>
# ---
# <i> CAS Spatial Data Analytics 2022 </i> ¦ <i> Kommunale Übersicht von Heizsystemen und Energieträgern in Wohngebäuden </i> ¦ <i> Stand: 22.09.2022  </i> ¦ <i> Entwickler: Jürg Reist </i>

# ### Notebook vorbereiten und die benötigten Daten aus dem GWR einlesen

import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

# Datenquelle definieren
url = urlopen("https://public.madd.bfs.admin.ch/ch.zip")

#lesen GWR Daten
zipfile = ZipFile(BytesIO(url.read()))
dfGWRSource = pd.read_csv(zipfile.open('gebaeude_batiment_edificio.csv'),
                         usecols=['GGDENAME','GKODE', 'GKODN', 'GENH1', 'GWAERSCEH1', 'GWAERDATH1'],
                         sep='\t')

#Column mit geeigneten Namen
dfGWRSource = dfGWRSource.rename(columns={"GGDENAME": "Gemeinde",
                              "GKODE": "lat",
                              "GKODN": "lon",
                              "GENH1":"Energiequelle",
                              "GWAERSCEH1":"Quelle",
                              "GWAERDATH1": "Update"})


# Die Bezeichnungen den Heizcodes zuweisen und als Liste speichern.
# Um die finale Visualisierung auf die drei definierten Energiequellen (Gas, Heizöl, Elektrizität) zu fokussieren, werden die Energiequellen zusammengefasst.
# Im GWR-Datenfile sind folgende Energiequellen definiert:
# 7501: 'Luft', 7510: 'Erdwärme (generisch', 7511: 'Erdwärmesonde', 7512: 'Erdregister', 7513: 'Wasser (Grundwasser, Oberflächenwasser, Abwasser)'
# 7520: 'Gas', 7530: 'Heizöl', 7540: 'Holz (generisch)', 7541: 'Holz (Stückholz)', 7542: 'Holz (Pellets)', 7543: 'Holz (Schnitzel)', 7550: 'Abwärme (innerhalb des Gebäudes)'
# 7560: 'Elektrizität', 7570: 'Sonne (thermisch)', 7580: 'Fernwärme (generisch)', 7581: 'Fernwärme (Hochtemperatur)', 7582: 'Fernwärme (Niedertemperatur)'
# 7598: 'Unbestimmt', 7599: 'Andere'
dfGWRSource['Energiequelle'] = dfGWRSource.Energiequelle.replace({
                                            7500: 'Keine',
                                            7501: 'Weitere',
                                            7510: 'Weitere',
                                            7511: 'Weitere',
                                            7512: 'Weitere',
                                            7513: 'Weitere',
                                            7520: 'Gas',
                                            7530: 'Heizöl',
                                            7540: 'Weitere',
                                            7541: 'Weitere',
                                            7542: 'Weitere',
                                            7543: 'Weitere',
                                            7550: 'Weitere',
                                            7560: 'Elektrizität',
                                            7570: 'Weitere',
                                            7580: 'Weitere',
                                            7581: 'Weitere',
                                            7582: 'Weitere',
                                            7598: 'Unbestimmt',
                                            7599: 'Weitere'
                                            })

#Dort wor keine Energiequelle (NULL) angegeben ist, wird der Text "Unbestimmt" gesetzt
dfGWRSource["Energiequelle"].fillna("Unbestimmt", inplace = True)


# Die korrekten Bezeichnungen der Informationsquellen zuweisen und als Liste speichern.
dfGWRSource['Quelle'] = dfGWRSource.Quelle.replace({
                                            852: 'Gemäss amtliche Schätzung',
                                            853: 'Gemäss Gebäudeversicherung',
                                            855: 'Gemäss Kontrolle der Heizungseinrichtungen',
                                            857: 'Gemäss Eigentümer/in / Verwaltung',
                                            858: 'Gemäss Gebäudeenergieausweis der Kantone (GEAK)',
                                            859: 'Andere Informationsquelle',
                                            860: 'Gemäss Volkszählung 2000',
                                            864: 'Gemäss Daten des Kantons',
                                            865: 'Gemäss Daten der Gemeinde',
                                            869: 'Gemäss Baubewilligung',
                                            870: 'Gemäss Versorgungswerk (Gas, Fernwärme)',
                                            871: 'Gemäss Minergie'
                                            })


# ### Nur die Attribute in ein neues Dataframe speichern, die ausgewertet werden sollen
#Datenframe für Verteilung der Energietrager pro Gemeinde
dfEnergyProGemeinde = dfGWRSource[['Gemeinde','Energiequelle']]

# ### Zählen aller Gebäude pro Gemeinde und deren Energiequelle inkl. Nullwerte
#Zählt alle Gebäude pro Gemeinde und deren Energiequelle inkl. Nullwerte
dfEnergyProGemeinde = dfEnergyProGemeinde[['Gemeinde','Energiequelle']].value_counts(dropna=False).reset_index()

# ### Spalten benennen und Daten in ein CSV-File exportieren
#Spaltenaen neu definieren
dfEnergyProGemeinde.columns  = ['Gemeinde','Energiequelle','Anzahl']

#Als CSV-File exportieren
dfEnergyProGemeinde.to_csv('Daten/Gemeindeliste_1-1.csv',sep=',', encoding="utf-8-sig")

