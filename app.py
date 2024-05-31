import pandas as pd
from bokeh.plotting import figure,curdoc
from bokeh.layouts import column,row
from bokeh.io import show
from bokeh.models import CustomJS, RadioButtonGroup,Select , FactorRange, Button
from bokeh.models.widgets import Div
from math import pi
from bokeh.models import (AnnularWedge, ColumnDataSource,
                          Legend, LegendItem, Plot, Range1d)





df1=pd.read_csv("logements and lots per region.csv",index_col='Regions')

df2=pd.read_csv('logements and lots per categorie.csv',index_col='Categories')

df3 = pd.read_csv('UniteParRegionsEtParCategories.csv') 
regions=list(df1.index)
##############################################################################################
def create_mixed_factor(): 
    quarters =("2016", "2017", "2018", "2019" , "2020")

    years = (
        ("2016", "Lots"), ("2016", "Logements"),    
        ("2017", "Lots"), ("2017", "Logements"),
        ("2018", "Lots"), ("2018", "Logements"),
        ("2019", "Lots"), ("2019", "Logements"),
        ("2020", "Lots"), ("2020", "Logements"),

    )

    fill_color = "#3288bd"
    line_color = "#66c2a5"
    p = figure(x_range=FactorRange(*years), height=500, tools="",
    background_fill_color="#fafafa", toolbar_location=None)
    total = df3.iloc[-1 , 2:]
    p.vbar(x=years, top=total, width=0.8,
    fill_color=fill_color, fill_alpha=0.8, line_color=line_color, line_width=1.2)
    quarterly = [13, 9, 13, 14 , 13]
    p.line(x=quarters, y=quarterly, color=line_color, line_width=3)
    p.scatter(x=quarters, y=quarterly, size=10,
    line_color=line_color, fill_color="white", line_width=3)
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    return p 
###############################################################
def create_donut(df2):
    df2 = df2.reset_index()
    numeric_cols = df2.select_dtypes(include='number')
# Calculer la somme des colonnes numériques pour chaque ligne
    df2['Total'] = numeric_cols.sum(axis=1)
# Définir les plages de l'intrigue
    xdr = Range1d(start=-2, end=2)
    ydr = Range1d(start=-2, end=2)
# Créer la figure de la parcelle
    plot = figure(x_range=xdr, y_range=ydr, title="Distribution des catégories", toolbar_location=None, width = 600 , height = 500 )
# Nettoyer et obtenir les catégories
    categories = pd.Series(df2['Categories'].astype(str)).str.strip().unique()
# Exclure la catégorie 'Total'
    categories_without_total = [category for category in categories if category not in ["Total", "Total general"]]
# Assurez-vous que les listes de couleurs et de catégories correspondent en longueur
    c = ["blue", "seagreen", "red", "firebrick"]
# Construire le dictionnaire des couleurs
    co = {category: color for category, color in zip(categories_without_total, c)}

# Créer la liste des couleurs correspondantes
    try:
        colors_list = [co[category] for category in categories_without_total]
        print("Liste des couleurs correspondantes:", colors_list)
    except KeyError as e:
     print(f"KeyError: {e}. Assurez-vous que toutes les catégories ont une couleur correspondante.")

# Calculer les angles pour le graphique en anneau
    angles = df2['Total'].map(lambda x: 2*pi*(x/df2['Total'].sum())).cumsum().tolist()
    start_angles = [0] + angles[:-1]

# Créer la source de données pour le graphique
    categories_source = ColumnDataSource(data=dict(
    start=start_angles,
    end=angles,
    co=colors_list
))

# Créer le glyph de l'anneau
    glyph = AnnularWedge(x=0, y=0, inner_radius=1.2, outer_radius=1.5,
                     start_angle="start", end_angle="end",
                     line_color="white", line_width=3, fill_color="co")
    r = plot.add_glyph(categories_source, glyph)

# Ajouter la légende
    legend = Legend(location="center")
    for i, name in enumerate(co):
        legend.items.append(LegendItem(label=name, renderers=[r], index=i))
    plot.add_layout(legend, "center")
    return plot 
###################################################################3

def create_vbar_plot(year='2016'):
    y=str(year)
    cols=[col for col in df1.columns if col.endswith(y)]
    p=figure(x_range=regions,#width=1200,
           toolbar_location=None, tools="hover")
    p.vbar_stack(cols,x='Regions',color=["blue","orange"],source=df1,legend_label=cols)
    p.xaxis.major_label_orientation = 1.2
    return p
########################################################################################
def create_line_plot(categorie='Villas'):
    log_values=df2.loc[categorie,['Logements_2016','Logements_2017','Logements_2018','Logements_2019','Logements_2020']].values
    lot_values=y=df2.loc[categorie,['Lots_2016','Lots_2017','Lots_2018','Lots_2019','Lots_2020']].values
    p=figure(x_axis_label='years',y_axis_label='nombre',height=450)
    year_range=[2016,2017,2018,2019,2020]
    p.line(x=year_range,y=log_values,legend_label='logement',color='blue')
    p.line(x=year_range,y=lot_values,legend_label='lot',color='red')
    return p
#################################################################
def create_button(label, color , callback = None):
    button = Button(label=label, button_type=color)
    if callback:
        button.on_click(callback)
    return button
#########################################################
def details_page(): 
    curdoc().clear()
    return_button = create_button("Retour", "danger", callback=first)
    curdoc().add_root(column(dashbord, return_button))
###############################################################################
def firstdashboard(): 
   # Créer un grand titre
    title = Div(text="<h1 style='text-align: center; color: Red;'>Tableau de bord concernant les unités des habitats</h1>", width=800, height=40)
    
    # Calculer les sommes
    total_sum_Lots = df1["Lots_2016"].sum() + df1["Lots_2017"].sum() + df1["Lots_2018"].sum() + df1["Lots_2019"].sum() + df1["Lots_2020"].sum()
    total_sum_Log = df1["Logements_2016"].sum() + df1["Logements_2017"].sum() + df1["Logements_2018"].sum() + df1["Logements_2019"].sum() + df1["Logements_2020"].sum()
    total = total_sum_Log+total_sum_Lots
    
    # Créer le contenu avec les valeurs calculées
    contenu1 = Div(text=f"""
    <h2 style='text-align: center;'>Somme de ces deux valeurs est : 
    <span style='color: #87CEEB;'>{total}</span></h2>
    """, width=600 , height=50)
    
    contenu2 = Div(text=f"""
    <h2 style='text-align: center;'>Somme des nombres de logements est : 
    <span style='color: #87CEEB;'>{total_sum_Log}</span></h2>
    """, width= 600 , height=50)
    contenu3 = Div(text=f"""
    <h2 style='text-align: center;'>Somme des nombres de lots est : 
    <span style='color: #87CEEB;'>{total_sum_Lots}</span></h2>
    """, width= 600 , height=50)   
    
    # Les eleemnts de la premiere page: 
    button = create_button("Plus de détails" , "success" , details_page)
    layout1 = column(contenu2,contenu3, mixed ) 
    layout2 = column(contenu1, donut) 
    firstdash = column(title,row( layout1, layout2) , button)
    return firstdash
##################################################3333
def update_vbar_plot(attr,old,new):

    dashbord.children[0].children[1]=create_vbar_plot(radio_button_group.labels[radio_button_group.active])
###############################################################
def update_line_plot(attr,old,new):
    dashbord.children[1].children[1]=create_line_plot(select.value)
 #######################################################################   
def show_dashboard(): 
    curdoc().clear()
    curdoc().add_root(dashbord)



mixed = create_mixed_factor() 


donut = create_donut(df2)

vbar=create_vbar_plot()
line_plot=create_line_plot()

years=[str(y) for y in range(2016,2021)]

radio_button_group = RadioButtonGroup(labels=years, active=0)
radio_button_group.js_on_event("button_click", CustomJS(args=dict(btn=radio_button_group), code="""
    console.log('radio_button_group: active=' + btn.active, this.toString())
"""))

categories= list(df2.index)
select = Select(title="Categories:", value="Villas", options=categories)
select.js_on_change("value", CustomJS(code="""
   console.log('select: value=' + this.value, this.toString())
"""))
first_chart=column(radio_button_group,vbar)
second_chart=column(select,line_plot)
dashbord=row(first_chart,second_chart)

radio_button_group.on_change('active',update_vbar_plot)
select.on_change('value',update_line_plot)

def first(): 
    curdoc().clear()
    firstdash = firstdashboard() 
    curdoc().add_root(firstdash)

first()