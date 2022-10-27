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
                         usecols=['GDEKT', 'GGDENAME', 'GKODE', 'GKODN', 'GENH1'],
                         sep='\t')


#Column mit geeigneten Namen
dfGWRSource = dfGWRSource.rename(columns={"GDEKT": "Kanton",
                                          "GGDENAME": "Gemeinde",
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

# ### Daten in ein GeoPackage-File exportieren
# nur ausgewählte Kantone exportiern, da sonst das Geopackage-File über 100MB wird. 
# GitHub hat eine Limitierung von 100MB  
options = ['BE', 'ZH', 'AG', 'VD', 'SG']
gdf_1 = gdf[(gdf['Kanton'].isin(options))] 

# nur ausgewählte Kantone exportiern, da sonst das Geopackage-File über 100MB wird. 
# GitHub hat eine Limitierung von 100MB  
options = ['GR', 'SO', 'SZ', 'GE', 'JU', 'NE', 'SH', 'BS', 'ZG', 'AR', 'GL', 'UR', 'OW', 'NW', 'AI', 'BL', 'LU','TG',  'VS', 'FR', 'TI']
gdf_2 = gdf[(gdf['Kanton'].isin(options))] 

#Als GeoPackage-File exportieren -PART 1
gdf_1 = gdf_1.set_crs(2056, allow_override=True)
gdf_1.to_file('Daten/Gemeindeliste_1-3_part1.gpkg', driver='GPKG', limit=0)

#Als GeoPackage-File exportieren - PART 2
gdf_2 = gdf_2.set_crs(2056, allow_override=True)
gdf_2.to_file('Daten/Gemeindeliste_1-3_part2.gpkg', driver='GPKG', limit=0)


