import pandas as pd
from bokeh.plotting import figure,curdoc
from bokeh.layouts import column,row
from bokeh.io import show
from bokeh.models import CustomJS, RadioButtonGroup,Select



df1=pd.read_csv("logements and lots per region.csv",index_col='Regions')
df2=pd.read_csv('logements and lots per categorie.csv',index_col='Categories')
regions=list(df1.index)
def create_vbar_plot(year='2016'):
    y=str(year)
    cols=[col for col in df1.columns if col.endswith(y)]
    p=figure(x_range=regions,#width=1200,
           toolbar_location=None, tools="hover")
    p.vbar_stack(cols,x='Regions',color=["blue","orange"],source=df1,legend_label=cols)
    p.xaxis.major_label_orientation = 1.2
    return p
def create_line_plot(categorie='Villas'):
    log_values=df2.loc[categorie,['Logements_2016','Logements_2017','Logements_2018','Logements_2019','Logements_2020']].values
    lot_values=y=df2.loc[categorie,['Lots_2016','Lots_2017','Lots_2018','Lots_2019','Lots_2020']].values
    p=figure(x_axis_label='years',y_axis_label='nombre',height=450)
    year_range=[2016,2017,2018,2019,2020]
    p.line(x=year_range,y=log_values,legend_label='logement',color='blue')
    p.line(x=year_range,y=lot_values,legend_label='lot',color='red')
    return p
vbar=create_vbar_plot()
line_plot=create_line_plot()
years=[str(y) for y in range(2016,2021)]

radio_button_group = RadioButtonGroup(labels=years, active=0)
radio_button_group.js_on_event("button_click", CustomJS(args=dict(btn=radio_button_group), code="""
    console.log('radio_button_group: active=' + btn.active, this.toString())
"""))

categories= list(df2.index)
select = Select(title="Categories:", value="Villas", options=categories)
#select.js_on_change("value", CustomJS(code="""
#    console.log('select: value=' + this.value, this.toString())
#"""))
first_chart=column(radio_button_group,vbar)
second_chart=column(select,line_plot)
dashbord=row(first_chart,second_chart)
print(select.value)
def update_vbar_plot(attr,old,new):

    dashbord.children[0].children[1]=create_vbar_plot(radio_button_group.labels[radio_button_group.active])

def update_line_plot(attr,old,new):
    dashbord.children[1].children[1]=create_line_plot(select.value)

radio_button_group.on_change('active',update_vbar_plot)
select.on_change('value',update_line_plot)
curdoc().add_root(dashbord)
