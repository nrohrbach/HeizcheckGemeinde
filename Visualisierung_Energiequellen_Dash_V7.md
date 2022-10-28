# Notebook zur Visualisierung der Daten aus der Fragestellung im Dashboard
Deises Dasboard von Jupyter bietet die möglichkeit während der Laufzeit die gewünschte Gemeinde auszuwäheln und diese dann als Kuchendiagramm (Pie-Plot) darzustellen. Zusätzlich wird die Heatmap aller Gas-, Heizöl und Elektritzitätsheizungen in einer Karte dargestellt.<br>
Datenquelle sind die aufbereiteten Daten des GWR-Datensatzes die im Modul <1.1_Anteil_fossiler_Heizungen.ipynb> und <1.3_Energiequellen_GHE.ipynb> erzeugt wurden.
<br>
<br>
Quellen: <br>
Plotly Dash, Open-Source Python-Framwork URL: https://plotly.com/dash [Stand: 2.10.2022]<br>
GitHub Jupyter-dash URL: https://github.com/plotly/jupyter-dash [Stand: 2.10.2022 <br>
Leaflet open-source JavaScript library for mobile-friendly interactive maps URL: https://leafletjs.com [Stand: 12.10.2022]<br>
GitHub dash-leaflet URL: https://github.com/thedirtyfew/dash-leaflet [Stand: 2.10.2022]<br>
<br>
<br>
<i> CAS Spatial Data Analytics 2022 </i> ¦ <i> Kommunale Übersicht von Heizsystemen und Energieträgern in Wohngebäuden </i> ¦ <i> Stand: 23.10.2022  </i> ¦ <i> Entwickler: Jürg Reist und Nico Rohrbach</i>

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

#Stylesheet für die Darstellung der Objekte im Browser
stylesheet = ['assets/style.css']
```

### Lesen alle Heizungen die mit Gas, Heizöl oder Elektrizität geheizt werden - Frage 1.1
Diese Daten werden im Notebook <1.1_Anteil_Heizungen_GHE_Vx.ipynb> vorbereitet


```python
#lesen der Daten aus dem Modul <1.1_Anteil_Heizungen_GHE_Vx.ipynb> direkt von GitHub
#df = pd.read_csv(r'Daten/Gemeindeliste_1-1.csv')
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
      <th>Bfs</th>
      <th>Energiequelle</th>
      <th>Anzahl</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>Zürich</td>
      <td>261</td>
      <td>Gas</td>
      <td>21642</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Zürich</td>
      <td>261</td>
      <td>Keine</td>
      <td>14192</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>Zürich</td>
      <td>261</td>
      <td>Heizöl</td>
      <td>12709</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>Zürich</td>
      <td>261</td>
      <td>Weitere</td>
      <td>12028</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>Winterthur</td>
      <td>230</td>
      <td>Unbestimmt</td>
      <td>10899</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>12345</th>
      <td>12345</td>
      <td>Pura</td>
      <td>5216</td>
      <td>Gas</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12346</th>
      <td>12346</td>
      <td>Fischenthal</td>
      <td>114</td>
      <td>Gas</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12347</th>
      <td>12347</td>
      <td>Wittinsburg</td>
      <td>2867</td>
      <td>Unbestimmt</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12348</th>
      <td>12348</td>
      <td>Arni (AG)</td>
      <td>4061</td>
      <td>Gas</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12349</th>
      <td>12349</td>
      <td>Orselina</td>
      <td>5121</td>
      <td>Keine</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>12350 rows × 5 columns</p>
</div>




```python
#sortierte Liste aller Gemeinden erstellen. Diese wird im Dash bei der Dropdownliste verwendet
lsGemeinden = sorted(list(df1_1.Gemeinde.unique()))
```

### Anzahl betroffener Personen pro Gemeinde - Frage 1.3
Diese Daten werden im Notebook <1.4_Zeitreihe_fossiler_Heizungen.ipynb> vorbereitet


```python
#Read the dataset
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
      <td>3053.0</td>
      <td>2995.0</td>
      <td>21.0</td>
      <td>1386.0</td>
      <td>1591.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Aarau</td>
      <td>8305.0</td>
      <td>8329.0</td>
      <td>12.0</td>
      <td>2894.0</td>
      <td>1523.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Aarberg</td>
      <td>797.0</td>
      <td>1991.0</td>
      <td>22.0</td>
      <td>1264.0</td>
      <td>316.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Aarburg</td>
      <td>3095.0</td>
      <td>3027.0</td>
      <td>11.0</td>
      <td>1708.0</td>
      <td>592.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Aarwangen</td>
      <td>95.0</td>
      <td>2544.0</td>
      <td>27.0</td>
      <td>1325.0</td>
      <td>616.0</td>
    </tr>
    <tr>
      <th>...</th>
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
      <td>1251.0</td>
      <td>472.0</td>
      <td>0.0</td>
      <td>746.0</td>
    </tr>
    <tr>
      <th>2149</th>
      <td>Zwischbergen</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>0.0</td>
      <td>15.0</td>
    </tr>
    <tr>
      <th>2150</th>
      <td>Zäziwil</td>
      <td>0.0</td>
      <td>736.0</td>
      <td>31.0</td>
      <td>322.0</td>
      <td>448.0</td>
    </tr>
    <tr>
      <th>2151</th>
      <td>Zürich</td>
      <td>188940.0</td>
      <td>98941.0</td>
      <td>30379.0</td>
      <td>9463.0</td>
      <td>95464.0</td>
    </tr>
    <tr>
      <th>2152</th>
      <td>Zürichsee (ZH)</td>
      <td>142.0</td>
      <td>150.0</td>
      <td>4.0</td>
      <td>82.0</td>
      <td>17.0</td>
    </tr>
  </tbody>
</table>
<p>2153 rows × 6 columns</p>
</div>




```python
# Daten in ein langes Datenformat transformieren
dfPax = pd.melt(dfPax, id_vars='Gemeinde', value_vars=['PaxGas', 'PaxÖl', 'PaxKeine','PaxUnbestimmt','PaxWeitere'])
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
      <td>3053.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Aarau</td>
      <td>PaxGas</td>
      <td>8305.0</td>
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
      <td>3095.0</td>
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
      <th>10760</th>
      <td>Zwingen</td>
      <td>PaxWeitere</td>
      <td>746.0</td>
    </tr>
    <tr>
      <th>10761</th>
      <td>Zwischbergen</td>
      <td>PaxWeitere</td>
      <td>15.0</td>
    </tr>
    <tr>
      <th>10762</th>
      <td>Zäziwil</td>
      <td>PaxWeitere</td>
      <td>448.0</td>
    </tr>
    <tr>
      <th>10763</th>
      <td>Zürich</td>
      <td>PaxWeitere</td>
      <td>95464.0</td>
    </tr>
    <tr>
      <th>10764</th>
      <td>Zürichsee (ZH)</td>
      <td>PaxWeitere</td>
      <td>17.0</td>
    </tr>
  </tbody>
</table>
<p>10765 rows × 3 columns</p>
</div>




```python
# Legendenwerte korrekt ausgeben
Legendenwerte = {"PaxGas" : "Gas",
                "PaxÖl" : "Heizöl",
                "PaxKeine" : "Keine",
                "PaxUnbestimmt" : "Unbestimmt",
                "PaxWeitere" : "Weitere"}

dfPax["Energieträger"] = dfPax["Energieträger"].map(Legendenwerte)

```

### Anteil der Energiequellen an Neubauten in den letzten 100 Jahren - Frage 1.4
Diese Daten werden im Notebook <1.4_Zeitreihe_fossiler_Heizungen.ipynb> vorbereitet


```python
#Read the dataset
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

### Liste aller Gemeinden in der Schweiz mit Koordinaten WGS84 erstellen
So wechselt die Karte automatisch zur ausgewählten Gemeinde, welche in der Dropdownliste ausgewählt wurde.

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
# Generieren eines geojson Fils mit Maker für jede Gemeinde inkl. dem Namen als Tooltip
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in CH_Gemeindeliste])

# Estellen der Javascript Funktion für das Filtern nach eines gewählten Gemeindenamens
geojson_filter = assign("function(feature, context){return context.props.hideout == feature.properties.name;}")
```

### Globale Farbdefinition
Durch diese Definition haben die Energieträger in den Charts immer die gleiche Farbe. <br>
Dies macht die Charts besser lesbar und wirken harmonischer. <br>
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

### JupyterDash erstellen und Webserver auf dem Lokalhost mit Prot 8050 starten
Hier wird das Dash vorbereitet... 
<p style="color:red;">bla bla bla...</p>

gehostet wird das ganze auf einem NAS zu Hause bei Jürg Reist
- Notebook und Dash lauft in einen Docker Container (jupyter/datascience-notebook) https://registry.hub.docker.com/r/jupyter/datascience-notebook/
- Die Karte ist ein WMS aus einem QGIS Server. Auch dieser läuft Docker Container (camptocamp/qgis-server) https://registry.hub.docker.com/r/camptocamp/qgis-server/
- Eigene Sublevel Domains (https://lab.rei.st und https://dash.rei.st) inkl. SSL
- Reversproxy auf NAS
- DNS auf NAS



```python
# JupyterDash erstellen
app = JupyterDash(__name__, external_stylesheets=stylesheet)

#Titel
app.layout = html.Div(children=[
    html.Div(children=[
        html.H3(children='Wie gross ist der Anteil der Heizöl-, Gas- und Elektrizitätsheizungen in einer Gemeinde?'),
        html.P(children='Ein Drittel des Energieverbrauchs in der Schweiz wird durch Haushalte verursacht (Bundesamt für Energie, 2021). Ein grosser Teil dieses Energieverbrauchs entsteht durch Gebäudeheizungen. In der Schweiz werden 60% der Gebäude mit Gas oder Öl beheizt (Bundesamt für Statistik, 2017). Durch den Ukrainekrieg sind die Energiepreise stark gestiegen, insbesondere für Gas und Öl. Dadurch müssen Haushalte und Betriebe welche mit Öl oder Gas heizen, mit höheren Ausgaben rechnen. Diese zusätzliche finanzielle Belastung der Bevölkerung ist nicht regelmässig verteilt und trifft nicht alle Regionen oder Gemeinden im gleichen Ausmass. Darum soll mit dieser Arbeit analysiert werden, wie stark verschiedene Gemeinden von den steigenden Energiepreisen betroffen sind.'),
        ], style={'textAlign': 'left'}),

    ### Gemeinde Auswahl ###
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
    ], className="eleven columns", style={'width': '96.5%', 'padding':'1rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'withe'}),        

             
    ### PiePlot für die ausgewählte Gemeinde ###
    html.Div(children=[
             dcc.Graph(id='graph')
        ], className="six columns", style={'padding':'1rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'withe'}),
    
    ### Karte mit WMS vom QGIS-Server und im Hintergund die Geojson Marker ###
    html.Div(children=[
           # Beschriftung oberhalb der Karte
           html.P(children='Betroffene Gebiete', style={'font': 'Open Sans','font-weight': 'bold', 'textAlign': 'center'}),
           # WMS Karte       
           dl.Map([dl.WMSTileLayer(url="https://wms.rei.st/?SERVICE=WMS", layers="Analyse", format="image/png", transparent=True, minZoom = 8, maxZoom = 17),
           # Geojson für die Gemeindesuche in der Karte
           dl.GeoJSON(data=geojson, options=dict(filter=geojson_filter), id="geojson", zoomToBounds=True)       
           ], id='myMap', zoom=15, className="six columns", style={'width': '97%', 'height': '400px','padding':'1rem', 'marginTop':'1rem', 'marginBottom':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px'}),    
        
    ], className="six columns", style={'padding':'1rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px'}),  
  
    ### Zeitreihe für die ausgewählte Gemeinde ###
    html.Div(children=[
             dcc.Graph(id='zeitreihe')
        ], className="six columns", style={'padding':'1rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'withe'}),
        
    ### Anzahl betroffener Personen pro Gemeinde ###
    html.Div(children=[
             dcc.Graph(id='personen')
        ], className="six columns", style={'padding':'1rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'withe'}),
      
    ### Dokumentation ###
    html.Div(html.P('Hier ist Platz für die Dokumentation und Links zu GitHub'),
            className="eleven columns", style={'width': '96.5%','textAlign': 'left', 'padding':'1rem', 'marginTop':'5rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'font-style': 'italic'}
            ),

    ### Fusszeile ###
    html.Div(html.P('Weiterbildung der Hochschule für Architektur, Bau und Geomatik FHNW ¦ CAS Spatial Data Analytics 2022 ¦ Kommunale Übersicht von Heizsystemen und Energieträgern in Wohngebäuden ¦ 25.10.2022 ¦ Student: Jürg Reist und Nico Rohrbach'),
            className="eleven columns", style={'width': '96.5%','textAlign': 'left', 'padding':'1rem', 'marginTop':'5rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'font-style': 'italic'}
            )
    
], style={'padding': '1rem'})

########################################################    
# Callback und Update Kuchendiagramm von Jürg - Frage 1.1
########################################################  

# Definition der callback Funktion um die Grafik der gerade ausgewählten Gemeinde zu erstellen
@app.callback(
    Output('graph', 'figure'),
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


####################################################################    
# Callback und Update Balkendiagramm Zeitreihe von Nico - Frage 1.4
#################################################################### 

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

###############################################################################    
# Callback und Update Balkendiagramm betroffener Personen von Nico - Frage 1.2
############################################################################### 

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


###############################################################################    
# Callback für das Setzen der Zoomstufe in der Karte
###############################################################################

# Setzt die Zoomstufe auf fix auf 14 wenn eine neue Gemeinde ausgewählt wird
@app.callback(
    Output('myMap', 'zoom'),
    [Input("Gemeinde-dropdown", "value")]
)

def func(viewport):
        viewport = 15
        return viewport

###############################################################################    
# Callback um die Karte der gerade ausgewählten Gemeinde zu aktualisieren
############################################################################### 

# Suchen der Gemeinde im Geojson File und Karte zu diesem Marker verschieben
# Dies könnte auch als normaler callback aufegrufen werden. Ist aber so performanter
app.clientside_callback("function(x){return x;}", Output("geojson", "hideout"), Input("Gemeinde-dropdown", "value"))


# Starten der App, um das Resultat auf https://dash.rei.st anzuzeigen
if __name__ == '__main__':
      app.run_server(mode='external', host='0.0.0.0', port=8050, debug=False)

```

    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on all addresses (0.0.0.0)
     * Running on http://127.0.0.1:8050
     * Running on http://172.17.0.3:8050
    Press CTRL+C to quit
    127.0.0.1 - - [25/Oct/2022 20:06:44] "GET /_alive_343c4d5d-666b-4fa0-b030-7a3992cb263d HTTP/1.1" 200 -
    

    Dash app running on http://0.0.0.0:8050/
    


```python

```
