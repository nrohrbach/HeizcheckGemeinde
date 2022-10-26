#!/usr/bin/env python
# coding: utf-8

# # Fragestellung 1.3: -> Export nur Energiequellen GAS - HEIZÖL - ELEKTRIZITÄT
# ## Welche Gebiete in einer Gemeinde sind am stärksten betroffen?
# 
# Um diese Frage zu beantworten, werden Daten aus dem "Gebäude- und Wohnungsregister" (GWR) verwendet. <br>
# [Link zum GWR](https://www.housing-stat.ch/de/index.html)<br>
# [Link zur GWR Dokumentation](https://www.housing-stat.ch/de/docs/index.html)<br>
# [Link zum GWR Download](https://www.housing-stat.ch/de/madd/public.html)<br>
# <br>
# Die Daten werden nach Gemeinde und Energiequelle gruppiert und dann die einzelnen Objekte gezählt. <br>
# Anschliessend wird die resultierende Liste als Geopackage zur weiterverarbeitung bzw. Visualisierung exportiert.<br>
# <br>
# ---
# <i> CAS Spatial Data Analytics 2022 </i> ¦ <i> Kommunale Übersicht von Heizsystemen und Energieträgern in Wohngebäuden </i> ¦ <i> Stand: 22.09.2022  </i> ¦ <i> Entwickler: Jürg Reist </i>

# ### Notebook vorbereiten und die benötigten Daten aus dem GWR einlesen

import pandas as pd
import geopandas as gpd
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

# Datenquelle definieren
url = urlopen("https://public.madd.bfs.admin.ch/ch.zip")

#lesen GWR Daten
zipfile = ZipFile(BytesIO(url.read()))
dfGWRSource = pd.read_csv(zipfile.open('gebaeude_batiment_edificio.csv'),
                         usecols=['GGDENAME','GKODE', 'GKODN', 'GENH1'],
                         sep='\t')


#Column mit geeigneten Namen
dfGWRSource = dfGWRSource.rename(columns={"GGDENAME": "Gemeinde",
                                          "GKODE": "lat",
                                          "GKODN": "lon",
                                          "GENH1":"Energiequelle"
                                          })

# Die Bezeichnungen den Heizcodes zuweisen und als Liste speichern.
# Um die finale Visualisierung auf die drei definierten Energiequellen (Gas, Heizöl, Elektrizität) zu fokussieren, werden die Energiequellen zusammengefasst.
# Im GWR-Datenfile sind folgende Energiequellen definiert:
# 7501: 'Luft', 7510: 'Erdwärme (generisch', 7511: 'Erdwärmesonde', 7512: 'Erdregister', 7513: 'Wasser (Grundwasser, Oberflächenwasser, Abwasser)'
# 7520: 'Gas', 7530: 'Heizöl', 7540: 'Holz (generisch)', 7541: 'Holz (Stückholz)', 7542: 'Holz (Pellets)', 7543: 'Holz (Schnitzel)', 7550: 'Abwärme (innerhalb des Gebäudes)'
# 7560: 'Elektrizität', 7570: 'Sonne (thermisch)', 7580: 'Fernwärme (generisch)', 7581: 'Fernwärme (Hochtemperatur)', 7582: 'Fernwärme (Niedertemperatur)'
# 7598: 'Unbestimmt', 7599: 'Andere'
dfGWRSource['Energiequelle'] = dfGWRSource.Energiequelle.replace({
                                            7500: 'Keine',
                                            7501: 'Luft',
                                            7510: 'Erdwärme',
                                            7511: 'Erdwärme',
                                            7512: 'Erdwärme',
                                            7513: 'Wasser',
                                            7520: 'Gas',
                                            7530: 'Heizöl',
                                            7540: 'Holz',
                                            7541: 'Holz',
                                            7542: 'Holz',
                                            7543: 'Holz',
                                            7550: 'Abwärme',
                                            7560: 'Elektrizität',
                                            7570: 'Sonne',
                                            7580: 'Fernwärme',
                                            7581: 'Ferwärme',
                                            7582: 'Fernwärme',
                                            7598: 'Unbestimmt',
                                            7599: 'Weitere'
                                            })


#nur die fossilen Energiequellen filtern
options = ['Gas', 'Heizöl', 'Elektrizität']
dfGWRfossileEnergiequelle = dfGWRSource[(dfGWRSource['Energiequelle'].isin(options))] 


# ### Daten als Geopackage zur Weiterverarbeitung bzw. Visusliserung exportieren

gdf = gpd.GeoDataFrame(
    dfGWRfossileEnergiequelle, geometry=gpd.points_from_xy(dfGWRfossileEnergiequelle.lat, dfGWRfossileEnergiequelle.lon)
)

#Datenframe für Verteilung der Energietrager pro Gemeinde
dfEnergyHeatmap = gdf[['Gemeinde','Energiequelle', 'geometry']]
dfEnergyHeatmap


# ### Daten in ein GeoPackage-File exportieren
#Als GeoPackage-File exportieren
#gdf.to_file('Export_Data/GeoPackage/EnergiequelleFossile.gpkg', driver='GPKG', limit=0)
gdf = gdf.set_crs(2056, allow_override=True)
gdf.to_file('Daten/Gemeindeliste_1-3.gpkg', driver='GPKG', limit=0)


