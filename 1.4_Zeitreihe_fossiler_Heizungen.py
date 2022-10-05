#!/usr/bin/env python
# coding: utf-8

# # Fragestellung 1.4: Wie hat sich der Anteil fossiler Heizungen in den letzten 20 Jahren in einer Gemeinde verändert? 
# 
# Um diese Fragen zu beantworten, werden Daten aus dem "Gebäude- und Wohnungsregister" (GWR) verwendet. Die Daten werden nach Gemeinde, Bauperiode und Energiequelle gruppiert. Anschliessend werden die einzelnen Objekte gezählt. Anschliessend wird die resultierende Liste als CSV-Datei exportiert.

# ## Notebook vorbereiten und Daten importieren

# In[1]:


# Zu verwendende Bibliotheken importieren
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


# In[5]:


# Datenquelle definieren
url = urlopen("https://public.madd.bfs.admin.ch/gl.zip")

# ZIP-File herunterladen und Dataframe erstellen
zipfile = ZipFile(BytesIO(url.read()))
df = pd.read_csv(zipfile.open('gebaeude_batiment_edificio.csv'), 
                     sep='\t')

df.head()


# In[6]:





# In[3]:


# Alle Attribute und Datentypen der importierten Daten anschauen.
df.dtypes


# ## Daten vorbereiten

# In[4]:


# Die gewünschten Attribute sinnvoll umbenennen und in ein neues Dateframe speichern.
buildings = df.rename(columns={"GDEKT":"Kanton",
                               "GGDENAME": "Gemeinde",
                               "GKODE": "lat",
                               "GKODN": "lon",
                               "GKAT":"Gebaeudekategorie",
                               "GBAUJ":"Baujahr",
                               "GBAUP":"Bauperiode",
                               "GANZWHG":"AnzahlWohnungen",
                               "GEBF":"Energiebezugsflaeche",
                               "GWAERZH1":"Waermeerzeuger",
                               "GENH1":"Energiequelle",
                               "GWAERSCEH1":"InfoquelleHeizung"})


# In[5]:


# Die nicht verwendeten Attribute löschen
buildings = buildings.drop(['GGDENR','EGRID','LGBKR','LPARZ','LPARZSX','LTYP','GEBNR','GBEZ','GKSCE','GSTAT','GKLAS','GBAUM','GABBJ','GAREA','GVOL','GVOLNORM','GVOLSCE','GASTW','GAZZI','GSCHUTZR','GWAERDATH1','GWAERZH2','GENH2','GWAERSCEH2','GWAERDATH2','GWAERZW1','GENW1','GWAERSCEW1','GWAERDATW1','GWAERZW2','GENW2','GWAERSCEW2','GWAERDATW2','GEXPDAT'], axis=1)


# In[6]:


# Nullwerte anschauen
buildings_null = buildings.isnull().sum()
buildings_null


# In[7]:


# Die korrekten Bezeichnungen den Heizcodes zuweisen und als Liste speichern.
buildings['Energiequelle'] = buildings.Energiequelle.replace({
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


# In[8]:


# Bereinigtes DataFrame anschauen
buildings


# ## Anzahl Gebäude pro Gemeinde, Bauperiode und Energiequelle zählen und als DataFrame speichern

# In[9]:


# Zählt alle Gebäude pro Gemeinde, Bauperiode und Energiequelle
Gemeindeliste = buildings[['Gemeinde','Bauperiode','Energiequelle']].value_counts().reset_index()


# In[10]:


# Die Spaltennamen des DataFrames neu benennen
Gemeindeliste.columns  = ['Gemeinde','Bauperiode','Energiequelle','Anzahl']
Gemeindeliste


# ## Daten als CSV-Datei exportieren

# In[11]:


# Als CSV-File exportieren
Gemeindeliste.to_csv('Gemeindeliste_1-4.csv',sep=',', encoding="utf-8-sig")


# In[ ]:




