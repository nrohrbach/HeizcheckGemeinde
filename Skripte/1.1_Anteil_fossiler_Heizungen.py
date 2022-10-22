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

# In[1]:


#import pandas as pd
#import matplotlib.pyplot as plt

#lesen GWR Daten
#dfGWRSource = pd.read_csv('GWR_Data/gebaeude_batiment_edificio_CH.csv', usecols=['GGDENAME','GKODE', 'GKODN', 'GENH1', 'GWAERSCEH1', 'GWAERDATH1'],  sep='\t')


# In[2]:


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

dfGWRSource.head()


# In[3]:


#Column mit geeigneten Namen
dfGWRSource = dfGWRSource.rename(columns={"GGDENAME": "Gemeinde",
                              "GKODE": "lat",
                              "GKODN": "lon",
                              "GENH1":"Energiequelle",
                              "GWAERSCEH1":"Quelle",
                              "GWAERDATH1": "Update"})


# In[4]:


dfGWRSource


# In[5]:


# Die korrekten Bezeichnungen den Heizcodes zuweisen und als Liste speichern.
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
                                            7599: 'Keine'
                                            })


# In[6]:


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


# In[6]:


dfGWRSource


# In[7]:


#Nullwerte anschauen
dfGWRSource_null = dfGWRSource.isnull().sum()
dfGWRSource_null


# ### Nur die Attribute in ein neues Dataframe speichern, die ausgewertet werden sollen

# In[8]:


#Datenframe für Verteilung der Energietrager pro Gemeinde
dfEnergyProGemeinde = dfGWRSource[['Gemeinde','Energiequelle']]
dfEnergyProGemeinde


# ### Zählen aller Gebäude pro Gemeinde und deren Energiequelle inkl. Nullwerte

# In[9]:


#Zählt alle Gebäude pro Gemeinde und deren Energiequelle inkl. Nullwerte
dfEnergyProGemeinde = dfEnergyProGemeinde[['Gemeinde','Energiequelle']].value_counts(dropna=False).reset_index()
dfEnergyProGemeinde


# ### Spalten benennen und Daten in ein CSV-File exportieren

# In[10]:


#Spaltenaen neu definieren
dfEnergyProGemeinde.columns  = ['Gemeinde','Energiequelle','Anzahl']
dfEnergyProGemeinde


# In[11]:


#Als CSV-File exportieren
#dfEnergyProGemeinde.to_csv('Export_Data/EnergyProGemeinde_CH.csv',sep=',', encoding="utf-8-sig")


# In[10]:


#Als CSV-File exportieren
dfEnergyProGemeinde.to_csv('Daten/EnergyProGemeinde_CH.csv',sep=',', encoding="utf-8-sig")






