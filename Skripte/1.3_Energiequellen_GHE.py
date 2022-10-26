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


# ### Daten in ein GeoPackage-File exportieren
#Als GeoPackage-File exportieren
#gdf.to_file('Export_Data/GeoPackage/EnergiequelleFossile.gpkg', driver='GPKG', limit=0)
gdf = gdf.set_crs(2056, allow_override=True)
gdf.to_file('Daten/Gemeindeliste_1-3.gpkg', driver='GPKG', limit=0)


