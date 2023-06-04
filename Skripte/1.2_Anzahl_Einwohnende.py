#!/usr/bin/env python
# coding: utf-8

# # Fragestellung 1.2: Wie viele EinwohnerInnen und Beschäftigte sind durch hohe Öl- und Gaspreise in einer Gemeinde betroffen?
# 
# Um diese Fragen zu beantworten, werden Daten aus dem "Gebäude- und Wohnungsregister (GWR)", der "Statistik der Bevölkerung (STATPOP)", der "Statistik der Unternehmensstruktur (STATENT)" und die offiziellen Gemeindegrenzen (swissBOUNDARIES3D). verwendet.

# In[1]:


# Zu verwendende Bibliotheken importieren
import pandas as pd
import geopandas as gpd
#import geoplot as gplt
import shapely.geometry
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import requests
import json
import fiona.io


# In[2]:


# STATPOP einlesen und erste Zeilen anschauen
# Die Statpop Daten enthalten die Anzahl EinwohnerInnen pro Hektarzelle.
    
# Datenquelle definieren
url = urlopen("https://dam-api.bfs.admin.ch/hub/api/dam/assets/23528269/master")

# ZIP-File herunterladen und Dataframe erstellen
zipfile = ZipFile(BytesIO(url.read()))
statpop = pd.read_csv(zipfile.open('ag-b-00.03-vz2021statpop/STATPOP2021.csv'), 
                     sep=';',
                     usecols = ['RELI', 'E_KOORD','N_KOORD','B21BTOT'])

statpop.head()


# In[3]:


# Die Statpop Daten enthalten die Anzahl EinwohnerInnen pro Hektarzelle.
# Damit aus den Punkten aus der Statistik ein Polygon wird, werden die vier Stützpunkte erstellt.
# Dazu werdenKopien der Dataframes erstellt und die Koordinaten der vier Ecken berechnet (+100m).
statpop2 = statpop.copy()
statpop2['E_KOORD'] = statpop2['E_KOORD']+100

statpop3 = statpop.copy()
statpop3['E_KOORD'] = statpop3['E_KOORD']+100
statpop3['N_KOORD'] = statpop3['N_KOORD']+100

statpop4 = statpop.copy()
statpop4['N_KOORD'] = statpop4['N_KOORD']+100

statpop5 = statpop.copy()


# In[4]:


#Die vier Dataframes zusammenführen.
statpoptot = pd.concat([statpop, statpop2, statpop3, statpop4, statpop5])
statpoptot


# In[5]:


#Ein Geodataframe erstellen mit Polygonen welches aus den vier Punkten einer Rasterzelle bestehen.
gdf= gpd.GeoDataFrame(
    statpoptot.groupby("RELI").apply(
        lambda d: pd.Series(
            {
                "geometry": shapely.geometry.Polygon(
                    d.loc[:, ["E_KOORD", "N_KOORD"]].values
                ),
            }
        )
    )
,crs="EPSG:2056")
#gdf.plot(markersize=.1, figsize=(8, 8))


# In[6]:


#Mit initialem Dataframe zusammenführen um die Anzahl Einwohner zu erhalten.
StatpopRaster = pd.merge(gdf, statpop, on='RELI')
StatpopRaster


# In[7]:


#in WGS84 transformieren
StatpopRaster = StatpopRaster.to_crs(epsg='4326')
StatpopRaster


# # 2. GWR Gebäudedaten aufbereiten

# In[8]:


# GWR-Daten Gebäude einlesen und erste Zeilen anschauen
gwr = urlopen("https://public.madd.bfs.admin.ch/ch.zip")

# ZIP-File herunterladen und Dataframe erstellen
zipfile = ZipFile(BytesIO(gwr.read()))
Gebaeude = pd.read_csv(zipfile.open('gebaeude_batiment_edificio.csv'), 
                     sep='\t',
                     usecols = ['GGDENR','GGDENAME','GKODE','GKODN','GKAT','GENH1','GEBF','GAREA','GBAUJ'])

Gebaeude.head()


# GWR-Daten Gebäude einlesen und erste Zeilen anschauen

#Gebaeude = pd.read_csv(r'C:\Users\AninaNico\Documents\CAS_SpatialDataAnalytics\Zertifikatsarbeit\Uebung\Daten\GWR/gebaeude_batiment_edificio.csv',
#                sep='\t',
#                usecols = ['GGDENR','GGDENAME','GKODE','GKODN','GKAT','GENH1','GEBF','GAREA','GBAUJ'])
#Gebaeude.head()


# # Energiequellen mit NaN als "Unbestimmt" weiter verwenden.

# In[9]:


# Die korrekten Bezeichnungen den Heizcodes zuweisen und als Liste speichern.
Gebaeude['Energiequelle'] = Gebaeude.GENH1.replace({
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


# In[10]:


# NULL Werte bei der Energiequelle werden zu "Unbestimmt" gemappt
Gebaeude['Energiequelle'] = Gebaeude['Energiequelle'].fillna('Unbestimmt')
Gebaeude


# In[11]:


#Gebäude ohne Wohnnutzung (GKAT=1060) werden rausgefiltert
Wohngebaeude = Gebaeude.query('GKAT in[1010, 1020, 1030, 1040, 1080]')
Wohngebaeude


# In[12]:


Wohngebaeude.isnull().sum()


# In[13]:


# Gebäude nur bis Baujahr 2021 und unbekannt werden berücksichtigt, weil die aktuellsten Statpopdaten den Datenstand 31.12.2021 haben.
Wohngebaeude = Wohngebaeude.loc[Wohngebaeude['GBAUJ']!=2022]
Wohngebaeude


# In[14]:


#Geodataframe mit den Wohngebäuden aus dem GWR erstellen.
Wohngebaeude_gdf = gpd.GeoDataFrame(
    Wohngebaeude, geometry=gpd.points_from_xy(Wohngebaeude.GKODE, Wohngebaeude.GKODN,crs="EPSG:2056"))

Wohngebaeude_gdf


# In[15]:


#Geodataframe mit Wohngebäuden in wGS84 transformieren.
Wohngebaeude_gdf = Wohngebaeude_gdf.to_crs(epsg='4326')


# In[16]:


#Wohngebaeude_gdf.plot(markersize=.1, figsize=(8, 8))


# In[17]:


#Spatial Join der Wohnbevölkerung im Hektarraster (StatpopRaster) und der Wohngebäude aus dem GWR (Wohngebaeude_gdf)
dfsjoin = gpd.sjoin(StatpopRaster, Wohngebaeude_gdf) 


# In[18]:


# Pivottabelle erstellen
# Damit erhalte ich für jede Hektarrasterzelle aus dem Statpop (id=RELI) die Anzahl Gebäude nach Energiequelle.
dfpivot = pd.pivot_table(dfsjoin,index='RELI',columns='Energiequelle',aggfunc={'Energiequelle':len})
dfpivot.columns = dfpivot.columns.droplevel()
dfpivot


# In[19]:


# Nun wird die Pivottabelle mit dem Geodatenframe (StatpopRaster) gemergt. 
EnergiequellenRaster = StatpopRaster.merge(dfpivot, how='left', on='RELI')
EnergiequellenRaster


# In[20]:


# Prüfen ob noch NULL Werte vorhanden sind.
EnergiequellenRaster.isnull().sum()


# In[21]:


# Die NULL Werte werden mit 0 ersetzt.
EnergiequellenRaster = EnergiequellenRaster.fillna(0)
EnergiequellenRaster


# In[22]:


#Die Anzahl Gebäude pro Hektarraster zählen
EnergiequellenRaster['AnzahlGebaeude'] = EnergiequellenRaster['Elektrizität'] + EnergiequellenRaster['Gas'] + EnergiequellenRaster['Heizöl'] + EnergiequellenRaster['Keine'] + EnergiequellenRaster['Unbestimmt'] + + EnergiequellenRaster['Weitere']


# In[23]:


EnergiequellenRaster


# In[24]:


# Die Anzahl Einwohner aus der STATPOP werden nun proportional auf die Gebäude verteilt innerhalb einer Hektarrasterzelle
EnergiequellenRaster['PaxElektrizität'] = EnergiequellenRaster['B21BTOT']/EnergiequellenRaster['AnzahlGebaeude']*EnergiequellenRaster['Elektrizität']
EnergiequellenRaster['PaxGas'] = EnergiequellenRaster['B21BTOT']/EnergiequellenRaster['AnzahlGebaeude']*EnergiequellenRaster['Gas']
EnergiequellenRaster['PaxÖl'] = EnergiequellenRaster['B21BTOT']/EnergiequellenRaster['AnzahlGebaeude']*EnergiequellenRaster['Heizöl']
EnergiequellenRaster['PaxKeine'] = EnergiequellenRaster['B21BTOT']/EnergiequellenRaster['AnzahlGebaeude']*EnergiequellenRaster['Keine']
EnergiequellenRaster['PaxUnbestimmt'] = EnergiequellenRaster['B21BTOT']/EnergiequellenRaster['AnzahlGebaeude']*EnergiequellenRaster['Unbestimmt']
EnergiequellenRaster['PaxWeitere'] = EnergiequellenRaster['B21BTOT']/EnergiequellenRaster['AnzahlGebaeude']*EnergiequellenRaster['Weitere']


# In[25]:


# Die NULL Werte werden mit 0 ersetzt. Muss noch einmal gemacht werden weil bei einigen wenigen Rasterzellen die AnzahlGebaeude = 0 ist was in einer Dividierung durch 0 entspricht
EnergiequellenRaster = EnergiequellenRaster.fillna(0)
EnergiequellenRaster


# In[26]:


# Dataframe entschlacken d.h. Die nicht verwendeten Attribute löschen
PaxPerEnergieRaster = EnergiequellenRaster.drop(['E_KOORD','N_KOORD','B21BTOT','Elektrizität','Gas','Heizöl','Keine','Weitere','AnzahlGebaeude','RELI','Unbestimmt'], axis=1)


# # 3. Hektarraster einer Gemeinde zuweisen

# In[27]:


# Fehlermeldung kann ignoriert werden weil es sich bei den Polygonen um einfache Quadrate handelt.
# Für jede Rasterzelle wird der Mittelpunkt ermittelt.
PaxPerEnergieRaster['geometry'] = PaxPerEnergieRaster.centroid


# In[28]:


PaxPerEnergieRaster


# In[29]:


PaxPerEnergieRaster.isnull().sum()


# In[30]:


# Die aktuellsten Gemeindegrenzen über die STAC API herunterladen

# Anfragen welche Files verfügbar sind.
StacApiUrl = requests.get('https://data.geo.admin.ch/api/stac/v0.9/collections/ch.swisstopo.swissboundaries3d/items')
StacApiAntwortJson = json.loads(StacApiUrl.text)
StacApiAntwort = StacApiAntwortJson['features']
StacApiAntwort


# In[31]:


# Die Antwort in ein Dataframe schreiben und das Datum als Zeitstempel speichern.
StacJsonAntwort = pd.json_normalize(StacApiAntwort)
StacJsonAntwort = StacJsonAntwort[['id','properties.datetime']]
StacJsonAntwort['properties.datetime'] = pd.to_datetime(StacJsonAntwort['properties.datetime'])
StacJsonAntwort


# In[32]:


# Zeitstempel des aktuellsten Files rausfiltern
Zeitstempel = StacJsonAntwort.max().id
Zeitstempel


# In[37]:


# Aktuellstes File herunterladen und entzippen
datenurl = 'https://data.geo.admin.ch/ch.swisstopo.swissboundaries3d/' + Zeitstempel + '/' + Zeitstempel + '_2056_5728.shp.zip'

response = requests.get(datenurl)
data_bytes = response.content
with fiona.io.ZipMemoryFile(data_bytes) as zip_memory_file:
    with zip_memory_file.open('swissBOUNDARIES3D_1_4_TLM_HOHEITSGEBIET.shp') as collection:
      switzerland_gemeinde = gpd.GeoDataFrame.from_features(collection, crs=collection.crs)

# In WGS84 transformieren
switzerland_gemeinde = switzerland_gemeinde.to_crs(epsg='4326')
    
#switzerland_gemeinde.plot()


# In[38]:


#Spatial Join der Wohnbevölkerung im Hektarraster (StatpopRaster) und der Wohngebäude aus dem GWR (Wohngebaeude_gdf)
gemeindejoin = gpd.sjoin(switzerland_gemeinde, PaxPerEnergieRaster)
gemeindejoin


# In[39]:


# Zählt alle Gebäude pro Gemeinde, Bauperiode und Energiequelle
Gemeindeliste = gemeindejoin[['PaxGas','PaxÖl','PaxElektrizität','PaxKeine','PaxUnbestimmt','PaxWeitere']].sum().reset_index()
Gemeindeliste


# In[40]:


GemeindeEinwohner = gemeindejoin.groupby(['NAME'])[['PaxGas','PaxElektrizität','PaxÖl','PaxKeine','PaxUnbestimmt','PaxWeitere']].agg('sum')


# In[41]:


GemeindeEinwohner


# In[42]:


# Werte auf Ganzzahlen runden
GemeindeEinwohner = round(GemeindeEinwohner).reset_index()
GemeindeEinwohner


# In[44]:


# Die Spaltennamen des DataFrames neu benennen
GemeindeEinwohner.columns  = ['Gemeinde','PaxGas','PaxElektrizität','PaxÖl','PaxKeine','PaxUnbestimmt','PaxWeitere']


# ## Daten als CSV-Datei exportieren

# In[45]:


# Als CSV-File exportieren
GemeindeEinwohner.to_csv('Daten/Gemeindeliste_1-2.csv', index = False, header=True, sep=',', encoding="utf-8-sig")

