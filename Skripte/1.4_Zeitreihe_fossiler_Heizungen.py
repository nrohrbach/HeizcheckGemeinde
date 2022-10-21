#!/usr/bin/env python
# coding: utf-8

# # Fragestellung 1.4: Wie hat sich der Anteil fossiler Heizungen in den letzten 20 Jahren in einer Gemeinde verändert? 
# 
# Um diese Fragen zu beantworten, werden Daten aus dem "Gebäude- und Wohnungsregister" (GWR) verwendet. Die Daten werden nach Gemeinde, Bauperiode und Energiequelle gruppiert. Anschliessend werden die einzelnen Objekte gezählt. Anschliessend wird die resultierende Liste als CSV-Datei exportiert.

# ## Notebook vorbereiten und Daten importieren

# In einem ersten Schritt werden die notwendigen Python Bibliotheken importiert und die Daten als Dataframe reingeladen.

# In[14]:


# Zu verwendende Bibliotheken importieren
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


# In[15]:


# Datenquelle definieren
url = urlopen("https://public.madd.bfs.admin.ch/ch.zip")

# ZIP-File herunterladen und Dataframe erstellen
zipfile = ZipFile(BytesIO(url.read()))
df = pd.read_csv(zipfile.open('gebaeude_batiment_edificio.csv'), 
                     sep='\t')

df.head()


# ## Daten vorbereiten

# Als nächstes werden die Daten vorprozessiert. Dabei werden die Attributnamen geändert, unwesentliche Spalten gelöscht, Werte klassiert und NULL Werte behandelt.
# Nach diesem Schritt sind die Daten bereinigt und können für die Analyse verwendet werden.

# In[16]:


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


# In[17]:


# Die nicht verwendeten Attribute löschen
buildings = buildings.drop(['GGDENR','EGRID','LGBKR','LPARZ','LPARZSX','LTYP','GEBNR','GBEZ','GKSCE','GSTAT','GKLAS','GBAUM','GABBJ','GAREA','GVOL','GVOLNORM','GVOLSCE','GASTW','GAZZI','GSCHUTZR','GWAERDATH1','GWAERZH2','GENH2','GWAERSCEH2','GWAERDATH2','GWAERZW1','GENW1','GWAERSCEW1','GWAERDATW1','GWAERZW2','GENW2','GWAERSCEW2','GWAERDATW2','GEXPDAT'], axis=1)


# In[18]:


# Die korrekten Bezeichnungen den Heizcodes zuweisen und als Liste speichern.
buildings['Energiequelle'] = buildings.Energiequelle.replace({
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
                                        7599: 'Keine'
                                            })


# In[19]:


# Fehlende Werte werden wie folgt berücksichtigt.

# Fehlende Bauperiode wird zu "Vor 1919"
buildings['Bauperiode'] = buildings['Bauperiode'].fillna(8011)

# Fehlende Energiequelle wird zu "Unbestimmt"
buildings['Energiequelle'] = buildings['Energiequelle'].fillna('Unbestimmt')


# In[20]:


# Bereinigtes DataFrame anschauen
buildings


# ## Anzahl Gebäude pro Gemeinde

# In diesem Schritt wird die Anzahl Gebäude pro Gemeinde und Bauperiode ausgewertet. Die Anzahl Gebäude wird später verwendet um die prozentuale Verteilung der Energieträger zu berechnen.

# In[21]:


# Zählt alle Gebäude pro Gemeinde, Bauperiode und Energiequelle
GebaeudeGemeindeTotal = buildings[['Gemeinde','Bauperiode']].value_counts().reset_index()
GebaeudeGemeindeTotal


# In[22]:


# Die Spaltennamen des DataFrames neu benennen
GebaeudeGemeindeTotal.columns  = ['Gemeinde','Bauperiode','GebaeudeTotal']
GebaeudeGemeindeTotal


# ## Anzahl Gebäude pro Gemeinde, Bauperiode und Energiequelle zählen und als DataFrame speichern

# In diesem Schritt werden die Anzahl Gebäude pro Gemeinde, Bauperiode und Energiequelle ausgewertet.

# In[23]:


# Zählt alle Gebäude pro Gemeinde, Bauperiode und Energiequelle
Gemeindeliste = buildings[['Gemeinde','Bauperiode','Energiequelle']].value_counts().reset_index()


# In[24]:


# Die Spaltennamen des DataFrames neu benennen
Gemeindeliste.columns  = ['Gemeinde','Bauperiode','Energiequelle','Anzahl']
Gemeindeliste


# ## Die beiden Dataframes zusammenführen

# Nun werden die beiden Dataframe zusammengeführt.

# In[25]:


Gemeinden = pd.merge(Gemeindeliste, GebaeudeGemeindeTotal, on=['Gemeinde','Bauperiode'])
Gemeinden


# ## Daten als CSV-Datei exportieren

# Zum Schluss wird das Dataframe als CSV-Datei exportiert. Diese Daten werden anschliessend für die Visualisierung verwendet.

# In[26]:


# Als CSV-File exportieren
Gemeinden.to_csv('Daten/Gemeindeliste_1-4.csv', index = False, header=True, sep=',', encoding="utf-8-sig")


# In[ ]:




