from django.shortcuts import render
import datetime
import numpy as np
from bokeh.embed import components
from bokeh.io import gridplot, output_file, show
from bokeh.plotting import figure
import bokeh.models
from math import pi


datetime_fmt = {
    "seconds": "%H:%M:%S",
    "minsec": "%H:%M:%S",
    "minutes": "%H:%M:%S",
    "hourmin": "%H:%M:%S",
    "hours": "%H:%M",
    "days": "%d/%b/%y",
    "months":"%b%Y",
    "years":"%Y"
}



# Create your views here.

def load_dashboard(request):

    prod_units_script,prod_units_div=make_prod_units_plot()

    dict_input={}
    dict_input["current_user"]="Bolat"


    dict_input["prod_units_script"]=prod_units_script
    dict_input["prod_units_div"]=prod_units_div

    return render(request, "html/dashboard.html",dict_input)


def dummy_signal(N,fcnt,noise_level):

    cicle_num=30
    x = np.linspace(0,360*cicle_num,N)
    y_noise=np.random.rand(N)*noise_level

    s=np.zeros(N)
    for i in range(fcnt):
        s+=np.random.rand(1)*np.sin(np.deg2rad(np.random.rand(1)*x+np.random.rand(1)))
        s+=np.random.rand(1)*np.cos(np.deg2rad(np.random.rand(1)*x+np.random.rand(1)))

    return s+y_noise


def make_prod_units_plot():

    y0 = dummy_signal(1000,3,4)
    y1 = dummy_signal(1000,7,3)
    y2 = dummy_signal(1000,15,3)

    dt=[datetime.datetime.now()+datetime.timedelta(days=i) for i in range(len(y0))]

    fig_width=600
    fig_height=400
    # create KPC plot
    s1 = figure(x_axis_type="datetime", width=fig_width, plot_height=fig_height, title="KPC")
    s1.line(dt, y0, color="navy")
    s1.yaxis.axis_label="Condensate Production Sm3/d"
    s1.title_text_font_size="8"
    s1.yaxis.axis_label_text_font_size="8"
    s1.xaxis.formatter = bokeh.models.DatetimeTickFormatter(
        formats={x: [y] for x,y in datetime_fmt.items()})

    # create Unit2 plot
    s2 = figure(x_axis_type="datetime", width=fig_width, height=fig_height, title="Unit2")
    s2.line(dt, y1, color="firebrick")
    s2.yaxis.axis_label="Condensate Production Sm3/d"
    s2.title_text_font_size="8"
    s2.yaxis.axis_label_text_font_size="12"
    s2.xaxis.formatter = bokeh.models.DatetimeTickFormatter(
        formats={x: [y] for x,y in datetime_fmt.items()})

    # create Unit3 plot
    s3 = figure(x_axis_type="datetime", width=fig_width, height=fig_height, title="Unit3")
    s3.line(dt, y2, color="olive")
    s3.yaxis.axis_label="Condensate Production Sm3/d"
    s3.title_text_font_size="8"
    s3.yaxis.axis_label_text_font_size="12"
    s3.xaxis.formatter = bokeh.models.DatetimeTickFormatter(
        formats={x: [y] for x,y in datetime_fmt.items()})

    # put all the plots in a grid layout
    p = gridplot([[s1, s2, s3]])

    # show the results
    script, div = components(p)


    return script, div
