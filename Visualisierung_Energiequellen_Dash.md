# Notebook zur Visualisierung der Daten aus den Fragestellungen 1.1 - 1.4 in einem Dashboard
Dieses Notebook erzeugt ein Dashboard und bietet dann die Möglichkeit, in einer Suchliste eine Gemeinde aus der Schweiz auszuwählen. <br>
Danach werden automatisch folgende Fragestellungen in drei Charts und in einer Karte zu der ausgewählten Gemeinde visualisiert: <br>
1.1. Wie gross ist der Anteil von Gas-, Heizöl- und Elektroheizungen in einer Gemeinde?<br>
1.2. Wie viele EinwohnerInnen und Beschäftigte sind durch hohe Öl- und Gaspreise in einer Gemeinde betroffen?<br>
1.3. Welche Gebiete in einer Gemeinde sind am stärksten betroffen?<br>
1.4. Wie hat sich der Anteil fossiler Heizungen in den letzten 20 Jahren in einer Gemeinde verändert?<br>
<br>
**Datenquellen für die Visualiserung:**<br>
Die Daten für die Charts bzw. Karte werden nächtlich automatisch auf GitHub berechnet und publiziert.<br>
https://github.com/nrohrbach/HeizcheckGemeinde/tree/main/Daten<br>
<br>
**Informatioen zu der eingesetzen Packages:**<br>
Plotly Dash, Open-Source Python-Framwork: https://plotly.com/dash [Stand: 2.10.2022]<br>
GitHub Jupyter-dash: https://github.com/plotly/jupyter-dash [Stand: 2.10.2022] <br>
Leaflet open-source JavaScript library for mobile-friendly interactive maps: https://leafletjs.com [Stand: 12.10.2022]<br>
GitHub dash-leaflet: https://github.com/thedirtyfew/dash-leaflet [Stand: 2.10.2022]<br>
<br>
<br>
<i> CAS Spatial Data Analytics 2022 </i> ¦ <i> Heizenergieträger in Gemeinden </i> ¦ <i> Stand: 21.11.2022  </i> ¦ <i> Entwickler: Jürg Reist und Nico Rohrbach</i>

### Notebook vorbereiten


```python
import pandas as pd
import plotly.express as px
from jupyter_dash import JupyterDash
from ipyleaflet import Map
import dash_leaflet as dl
import dash_leaflet.express as dlx

# für lokal auf Windows
#import dash_core_components as dcc 
#import dash_html_components as html

# für Docker auf Linux
from dash import html, dcc 
from dash.dependencies import Input, Output

from dash_extensions.javascript import assign
from csv import DictReader
from datetime import date
```


```python
# Stylesheet für eine einheitliche Darstellung der Objekte im Browser bzw. mobilen Geräten
stylesheet = ['assets/style.css']
```

### Lesen alle Heizungen die mit Gas, Heizöl oder Elektrizität geheizt werden - Frage 1.1
Diese Daten werden im Notebook <1.1_Anteil_Heizungen_GHE.ipynb> vorbereitet und werden nun für das Dashboard gelesen<br>
Link zu GitHub: https://nrohrbach.github.io/HeizcheckGemeinde/1.1_Anteil_Heizungen_GHE


```python
# lesen der Daten direkt von GitHub
url = 'https://raw.githubusercontent.com/nrohrbach/HeizcheckGemeinde/main/Daten/Gemeindeliste_1-1.csv'

df1_1 = pd.read_csv(url)

# Datensatz anzeigen
df1_1
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>Gemeinde</th>
      <th>Energiequelle</th>
      <th>Anzahl</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>Zürich</td>
      <td>Gas</td>
      <td>21629</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Zürich</td>
      <td>Keine</td>
      <td>14170</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>Zürich</td>
      <td>Heizöl</td>
      <td>12696</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>Zürich</td>
      <td>Weitere</td>
      <td>12081</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>Winterthur</td>
      <td>Unbestimmt</td>
      <td>10914</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>12346</th>
      <td>12346</td>
      <td>La Côte-aux-Fées</td>
      <td>Gas</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12347</th>
      <td>12347</td>
      <td>Hagenbuch</td>
      <td>Gas</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12348</th>
      <td>12348</td>
      <td>Uebeschi</td>
      <td>Gas</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12349</th>
      <td>12349</td>
      <td>Muri (AG)</td>
      <td>Gas</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12350</th>
      <td>12350</td>
      <td>Schnottwil</td>
      <td>Gas</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>12351 rows × 4 columns</p>
</div>




```python
# sortierte Liste aller Gemeinden der Schweiz erstellen. Diese wird im Dash bei der Dropdownliste verwendet
lsGemeinden = sorted(list(df1_1.Gemeinde.unique()))
```

### Anzahl betroffener Personen pro Gemeinde - Frage 1.2
Diese Daten werden im Notebook <1.2_Anzahl_Einwohnende.ipynb> vorbereitet und werden nun für das Dashboard gelesen.<br>
Link zu GitHub: https://nrohrbach.github.io/HeizcheckGemeinde/1.2_Anzahl_Einwohnende


```python
#lesen der Daten direkt von GitHub
url = r'https://raw.githubusercontent.com/nrohrbach/HeizcheckGemeinde/main/Daten/Gemeindeliste_1-2.csv'
dfPax = pd.read_csv(url)
dfPax
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Gemeinde</th>
      <th>PaxGas</th>
      <th>PaxElektrizität</th>
      <th>PaxÖl</th>
      <th>PaxKeine</th>
      <th>PaxUnbestimmt</th>
      <th>PaxWeitere</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Aadorf</td>
      <td>3052.0</td>
      <td>374.0</td>
      <td>2995.0</td>
      <td>2.0</td>
      <td>1387.0</td>
      <td>1610.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Aarau</td>
      <td>8277.0</td>
      <td>699.0</td>
      <td>8300.0</td>
      <td>0.0</td>
      <td>2881.0</td>
      <td>1607.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Aarberg</td>
      <td>797.0</td>
      <td>225.0</td>
      <td>1987.0</td>
      <td>4.0</td>
      <td>1282.0</td>
      <td>327.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Aarburg</td>
      <td>3091.0</td>
      <td>223.0</td>
      <td>3018.0</td>
      <td>8.0</td>
      <td>1707.0</td>
      <td>607.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Aarwangen</td>
      <td>95.0</td>
      <td>148.0</td>
      <td>2543.0</td>
      <td>13.0</td>
      <td>1320.0</td>
      <td>636.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2148</th>
      <td>Zwingen</td>
      <td>31.0</td>
      <td>125.0</td>
      <td>1251.0</td>
      <td>472.0</td>
      <td>0.0</td>
      <td>746.0</td>
    </tr>
    <tr>
      <th>2149</th>
      <td>Zwischbergen</td>
      <td>0.0</td>
      <td>60.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>15.0</td>
    </tr>
    <tr>
      <th>2150</th>
      <td>Zäziwil</td>
      <td>0.0</td>
      <td>108.0</td>
      <td>736.0</td>
      <td>29.0</td>
      <td>319.0</td>
      <td>454.0</td>
    </tr>
    <tr>
      <th>2151</th>
      <td>Zürich</td>
      <td>188767.0</td>
      <td>391.0</td>
      <td>98831.0</td>
      <td>25176.0</td>
      <td>9402.0</td>
      <td>100999.0</td>
    </tr>
    <tr>
      <th>2152</th>
      <td>Zürichsee (ZH)</td>
      <td>142.0</td>
      <td>30.0</td>
      <td>150.0</td>
      <td>2.0</td>
      <td>82.0</td>
      <td>19.0</td>
    </tr>
  </tbody>
</table>
<p>2153 rows × 7 columns</p>
</div>




```python
# Daten in ein langes Datenformat transformieren
dfPax = pd.melt(dfPax, id_vars='Gemeinde', value_vars=['PaxGas','PaxElektrizität', 'PaxÖl', 'PaxKeine','PaxUnbestimmt','PaxWeitere'])
dfPax.columns  = ['Gemeinde','Energieträger','Anzahl']
dfPax
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Gemeinde</th>
      <th>Energieträger</th>
      <th>Anzahl</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Aadorf</td>
      <td>PaxGas</td>
      <td>3052.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Aarau</td>
      <td>PaxGas</td>
      <td>8277.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Aarberg</td>
      <td>PaxGas</td>
      <td>797.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Aarburg</td>
      <td>PaxGas</td>
      <td>3091.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Aarwangen</td>
      <td>PaxGas</td>
      <td>95.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>12913</th>
      <td>Zwingen</td>
      <td>PaxWeitere</td>
      <td>746.0</td>
    </tr>
    <tr>
      <th>12914</th>
      <td>Zwischbergen</td>
      <td>PaxWeitere</td>
      <td>15.0</td>
    </tr>
    <tr>
      <th>12915</th>
      <td>Zäziwil</td>
      <td>PaxWeitere</td>
      <td>454.0</td>
    </tr>
    <tr>
      <th>12916</th>
      <td>Zürich</td>
      <td>PaxWeitere</td>
      <td>100999.0</td>
    </tr>
    <tr>
      <th>12917</th>
      <td>Zürichsee (ZH)</td>
      <td>PaxWeitere</td>
      <td>19.0</td>
    </tr>
  </tbody>
</table>
<p>12918 rows × 3 columns</p>
</div>




```python
# Legendenwerte korrekt ausgeben
Legendenwerte = {"PaxGas" : "Gas",
                "PaxÖl" : "Heizöl",
                "PaxKeine" : "Keine",
                "PaxUnbestimmt" : "Unbestimmt",
                "PaxElektrizität": "Elektrizität",
                "PaxWeitere" : "Weitere"}

dfPax["Energieträger"] = dfPax["Energieträger"].map(Legendenwerte)

```

### Anteil der Energiequellen an Neubauten in den letzten 100 Jahren - Frage 1.4
Diese Daten werden im Notebook <1.4_Zeitreihe_fossiler_Heizungen.ipynb> vorbereitet und werden nun für das Dashboard gelesen.<br>
Link zu GitHub: https://nrohrbach.github.io/HeizcheckGemeinde/1.4_Zeitreihe_fossiler_Heizungen


```python
#lesen der Daten direkt von GitHub
url = 'https://raw.githubusercontent.com/nrohrbach/HeizcheckGemeinde/main/Daten/Gemeindeliste_1-4.csv'

zeitreihe = pd.read_csv(url)
zeitreihe = zeitreihe.sort_values(by=['Bauperiode'])

zeitreihe['Prozentanteil'] = (100/zeitreihe['GebaeudeTotal'])*zeitreihe['Anzahl']

gemeinde = zeitreihe['Gemeinde'].sort_values()
gemeinde = gemeinde.unique()

zeitreihe['Bauperiode'] = zeitreihe.Bauperiode.replace({
    8011: 'Vor 1919',
    8012: '1919 bis 1945',
    8013: '1946 bis 1960',
    8014: '1961 bis 1970',
    8015: '1971 bis 1980',
    8016: '1981 bis 1985',
    8017: '1986 bis 1990',
    8018: '1991 bis 1995',
    8019: '1996 bis 2000',
    8020: '2001 bis 2005',
    8021: '2006 bis 2010',
    8022: '2011 bis 2015',
    8023: 'ab 2016'   
    })
```

### GeoJSON aller Gemeinden in der Schweiz mit Koordinaten WGS84 erstellen
Dieses GeoJSON dient dazu, dass die Karte automatisch zur ausgewählten Gemeinde wechselt, sobald eine Gemeinde in der Dropdownliste ausgewählt wurde.

Info zum Datensatz: https://opendata.swiss/de/dataset/amtliches-ortschaftenverzeichnis-mit-postleitzahl-und-perimeter [Stand: 14.10.2022]<br>
Download: CSV , WGS84 Download: https://data.geo.admin.ch/ch.swisstopo-vd.ortschaftenverzeichnis_plz/PLZO_CSV_WGS84.zip [Stand: 14.10.2022]   


```python
# Lesen aller Gemeinden und speichern in eine list of Dictionaries
with open("GWR_Data/CH_Gemeinden.csv", 'r') as f:
    dict_reader = DictReader(f)
    CH_Gemeindeliste = list(dict_reader)

# Erster Eintrag anzeigen       
CH_Gemeindeliste [0]
```




    {'name': 'Aadorf', 'lat': '47.49135943', 'lon': '8.897698233'}




```python
# Generieren eines GeoJSON Fils mit Maker für jede Gemeinde inkl. dem Namen als Tooltip
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in CH_Gemeindeliste])

# Estellen der Javascript Funktion für das Filtern nach eines gewählten Gemeindenamens
geojson_filter = assign("function(feature, context){return context.props.hideout == feature.properties.name;}")
```

### Globale Farbdefinition und Datum ermitteln
Durch diese Definition haben die Energieträger in den Charts immer die gleiche Farbe. Dies macht die Charts besser lesbar und wirken harmonischer. <br>
https://plotly.com/python/builtin-colorscales/ [Stand: 23.10.2022] <br>
https://plotly.com/python/colorscales/ [Stand: 23.10.2022]



```python
# globale Farben für alle Charts definieren
FigColor={'Heizöl':'tan',
           'Gas':'lemonchiffon',
           'Elektrizität':'tomato',
           'Unbestimmt':'rgb(105,105,105)',
           'Weitere':'rgb(128,128,128)',
           'Keine':'rgb(169,169,169)',
           'leer':'rgb(192,192,192)'
          }
```


```python
# Heutiges Datum ermitteln
today = date.today()
strtoday = 'Die Daten werden täglich aktualisiert. Die letzte erfolgreiche Aktualisierung erfolgte am ' + today.strftime("%d. %B %Y" + '.')
```

### JupyterDash erstellen und publizieren
Im Dashboard kann man in der Dropdownliste eine Gemeinde auswählen. Es kann auch nach der gewünschten Gemeinde gesucht werden.
Nach einem Klick auf die ausgewählte Gemeinde werden alle vier Charts automatisch aktualisiert. In der Karte erfolgt ein Zoom auf die gerade ausgewählte Gemeinde.



```python
# JupyterDash erstellen
app = JupyterDash(__name__, external_stylesheets=stylesheet)

# Titel im Browser-Tab 
app.title = "Heizenergieträger in Gemeinden"

# Titel und einleitender Text inkl. Quellen
app.layout = html.Div(children=[
    html.Div(children=[
        html.H3(children='Wie gross ist der Anteil von Heizöl-, Gas- und Elektroheizungen in einer Gemeinde?'),
        html.P(children='Ein Drittel des Energieverbrauchs in der Schweiz wird durch Haushalte verursacht.\
                         Ein grosser Teil dieses Energieverbrauchs entsteht durch Gebäudeheizungen.\
                         In der Schweiz werden 60% der Gebäude mit Gas oder Öl beheizt.\
                         Durch den Ukrainekrieg sind die Energiepreise stark gestiegen, insbesondere für Gas und Öl.\
                         Dadurch müssen Haushalte und Betriebe welche mit Öl oder Gas heizen, mit höheren Ausgaben rechnen.\
                         Diese zusätzliche finanzielle Belastung der Bevölkerung ist nicht regelmässig verteilt und trifft nicht alle Regionen\
                         oder Gemeinden im gleichen Ausmass. Darum soll mit dieser Arbeit analysiert werden, wie stark verschiedene Gemeinden\
                         von den steigenden Energiepreisen betroffen sind.'),
        
       ], style={'textAlign': 'left',
           'line-height': '2rem'}),

    ### Dropdownliste für die Gemeinde Auswahl ###
    html.Div(children=[
        html.Label([
        html.P(children='Bitte Gemeinde auswählen / bzw. suchen:', style={'font-weight': 'bold'}),
        dcc.Dropdown(id='Gemeinde-dropdown', 
                     clearable=False,
                     #value=lsGemeinden[0],
                     value='Olten',
                     options=[{'label': c, 'value': c}
                for c in lsGemeinden
            ])
        ])
    ], className="eleven columns", style={'width': '96.5%',
                                          'padding':'1rem',
                                          'marginTop':'1rem',
                                          'marginLeft':'1rem',
                                          'boxShadow': '#e3e3e3 4px 4px 2px',
                                          'border-radius': '10px',
                                          'backgroundColor': 'withe'}),        

             
    ### PiePlot für die ausgewählte Gemeinde - Frage 1.1 ###
    html.Div(children=[
             dcc.Graph(id='anteil')
        ], className="six columns", style={'padding':'1rem',
                                           'marginTop':'1rem',
                                           'marginLeft':'1rem',
                                           'boxShadow': '#e3e3e3 4px 4px 2px',
                                           'border-radius': '10px',
                                           'backgroundColor': 'withe'}),
    
    ### Karte mit WMS vom QGIS-Server und im Hintergund die GeoJSON Marker - Frage 1.3  ###
    html.Div(children=[
           # Beschriftung oberhalb der Karte
           html.P(children='Heatmap der betroffenen Gebiete (Heizöl, Gas und Elektrizität)', 
                           style={'marginLeft':'2.5em',
                                  'font-family': 'Verdana',
                                  'font-size': '1.1em',
                                  'font-weight': 'bold',
                                  'textAlign': 'left',
                                  'color': 'rgb(62,63,95)'}),
           # WMS Karte       
           dl.Map([dl.WMSTileLayer(url="https://wms.rei.st/?SERVICE=WMS", layers="Analyse", format="image/png", transparent=True, minZoom = 8, maxZoom = 17),
           # GeoJSON für die Gemeindesuche in der Karte
           dl.GeoJSON(data=geojson, options=dict(filter=geojson_filter), id="geojson", zoomToBounds=True)       
           ], id='mapscale', zoom=15, className="six columns", style={'width': '97%',
                                                                   'height': '400px',
                                                                   'padding':'1rem',
                                                                   'marginTop':'1rem',
                                                                   'marginBottom':'1rem',
                                                                   'marginLeft':'1rem',
                                                                   'boxShadow': '#e3e3e3 4px 4px 2px',
                                                                   'border-radius': '10px'}),    
        
    ], className="six columns", style={'padding':'1rem',
                                       'marginTop':'1rem',
                                       'marginLeft':'1rem',
                                       'boxShadow': '#e3e3e3 4px 4px 2px',
                                       'border-radius': '10px'}),  
  
    ### Zeitreihe für die ausgewählte Gemeinde - Frage 1.4 ###
    html.Div(children=[
             dcc.Graph(id='zeitreihe')
        ], className="six columns", style={'padding':'1rem',
                                           'marginTop':'1rem',
                                           'marginLeft':'1rem',
                                           'boxShadow': '#e3e3e3 4px 4px 2px',
                                           'border-radius': '10px',
                                           'backgroundColor': 'withe'}),
        
    ### Anzahl betroffener Personen pro Gemeinde - Frage 1.2 ###
    html.Div(children=[
             dcc.Graph(id='personen')
        ], className="six columns", style={'padding':'1rem',
                                           'marginTop':'1rem',
                                           'marginLeft':'1rem',
                                           'boxShadow': '#e3e3e3 4px 4px 2px',
                                           'border-radius': '10px',
                                           'backgroundColor': 'withe'}),
      
    ### Datum letzte Aktualisierung, Dokumentation und Links zu GitHub ###
    html.Div(children=[
        html.P(children=strtoday),
        html.P(children='Dieses Dashboard wurde mit Python erstellt. Alle Sourcen sind auf GitHub publiziert:'),
        html.A(children='https://nrohrbach.github.io/HeizcheckGemeinde', href='https://nrohrbach.github.io/HeizcheckGemeinde',
                         style={'target': '_blank', 'rel': 'noopener noreferrer nofollow', 'text-decoration': 'none'}),
        ],
        className="eleven columns", style={'width': '96.5%',
                                           'textAlign': 'left',
                                           'padding':'1rem',
                                           'marginTop':'1rem',
                                           'marginLeft':'1rem',
                                           'boxShadow': '#e3e3e3 4px 4px 2px',
                                           'border-radius': '10px',
                                           'line-height': '2rem'}
    ),

    ### Fusszeile ###
    html.Div(html.P('Weiterbildung der Hochschule für Architektur, Bau und Geomatik FHNW ¦\
                     CAS Spatial Data Analytics 2022 ¦ Heizenergieträger in Gemeinden ¦\
                     23.11.2022 ¦ Students: Jürg Reist und Nico Rohrbach'),
            className="eleven columns", style={'width': '96.5%',
                                               'textAlign': 'left',
                                               'padding':'1rem',
                                               'marginTop':'1rem',
                                               'marginLeft':'1rem',
                                               'boxShadow': '#e3e3e3 4px 4px 2px',
                                               'border-radius': '10px',
                                               'font-style': 'italic'}
            )
    
], style={'padding': '1rem'})

##################################################################################### 
# Callback und Update Kuchendiagramm von Jürg - Frage 1.1
#####################################################################################   

# Definition der callback Funktion um die Grafik der gerade ausgewählten Gemeinde zu erstellen
@app.callback(
    Output('anteil', 'figure'),
    [Input("Gemeinde-dropdown", "value")]
)

def update_figure1(Gemeinde):
    dfselect1 = df1_1.loc[(df1_1['Gemeinde']==Gemeinde)]
    fig1 = px.pie(dfselect1,
                  values='Anzahl',
                  names='Energiequelle',
                  color='Energiequelle',
                  color_discrete_map=FigColor,
                  hole=.4,
                  title='<b> Anteil der Energieträger pro Gemeinde </b>')
    fig1.update_layout(legend_title_text='Energieträger')
    return fig1


##################################################################################### 
# Callback und Update Balkendiagramm Zeitreihe von Nico - Frage 1.4
##################################################################################### 

# Definition der callback Funktion um die Grafik der gerade ausgewählten Gemeinde zu erstellen
@app.callback(
    Output('zeitreihe', 'figure'),
    [Input("Gemeinde-dropdown", "value")]
)

def update_figure2(Gemeinde):
    dfselect2 = zeitreihe.loc[(zeitreihe['Gemeinde']==Gemeinde)]
    fig2 = px.bar(dfselect2,
                  x="Bauperiode",
                  y="Prozentanteil",
                  color="Energiequelle",
                  color_discrete_map=FigColor,
                  title='<b> Anteil der Energieträger pro Bauperiode </b>')
    fig2.update_layout(legend_title_text='Energieträger')
    return fig2

#####################################################################################   
# Callback und Update Balkendiagramm betroffener Personen von Nico - Frage 1.2
##################################################################################### 

# Definition der callback Funktion um die Grafik der gerade ausgewählten Gemeinde zu erstellen
@app.callback(
    Output('personen', 'figure'),
    [Input("Gemeinde-dropdown", "value")]
)

def update_figure3(Gemeinde):
    dfselect3 = dfPax.loc[(dfPax['Gemeinde']==Gemeinde)]
    fig3 = px.bar(dfselect3,
                  x="Energieträger",
                  y= "Anzahl",
                  color="Energieträger",
                  color_discrete_map=FigColor,
                  title='<b> Anteil betroffener Personen pro Energieträger </b>')
    return fig3


##################################################################################### 
# Callback für das Setzen der Zoomstufe in der Karte von Jürg - Frage 1.3
##################################################################################### 

# Setzt die Zoomstufe auf fix auf 15 wenn eine neue Gemeinde ausgewählt wird
@app.callback(
    Output('mapscale', 'zoom'),
    [Input("Gemeinde-dropdown", "value")]
)

def func(viewport):
        viewport = 15
        return viewport

#####################################################################################    
# Callback um die Karte der gerade ausgewählten Gemeinde zu aktualisieren - Frage 1.3
##################################################################################### 

# Suchen der Gemeinde im GeoJSON File und Karte zu diesem Marker verschieben
# Dies könnte auch als normaler callback aufegrufen werden. Ist aber so performanter
app.clientside_callback("function(x){return x;}", Output("geojson", "hideout"), Input("Gemeinde-dropdown", "value"))


# Starten der App, um das Resultat auf https://dash.rei.st anzuzeigen
# Um die App im Internet zu publizieren ist es wichtig, dass der host=0.0.0.0 gesetzt wird!
if __name__ == '__main__':
      app.run_server(mode='external', host='0.0.0.0', port=8050, debug=False)

```

    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on all addresses (0.0.0.0)
     * Running on http://127.0.0.1:8050
     * Running on http://172.17.0.5:8050
    Press CTRL+C to quit
    127.0.0.1 - - [23/Nov/2022 16:02:49] "GET /_alive_d5f17afa-7dfe-4d95-ab11-859eaf5cab0e HTTP/1.1" 200 -
    

    Dash app running on http://0.0.0.0:8050/
    


```python

```
