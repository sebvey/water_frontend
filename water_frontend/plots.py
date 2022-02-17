import pandas as pd
from datetime import datetime, timedelta

from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import matplotlib.patches as patches


def prediction_figure(weather):
    """Returns the pyplot figure of the prediction plot"""

    with plt.style.context('fivethirtyeight'):

        fig = plt.figure(figsize=(12,5))
        fig.patch.set_facecolor('#FFFFFF')
        ax = plt.gca()

        plt.plot(weather.index,weather['prediction'],marker='o',linewidth=3,color='#525252')
        plt.ylim(bottom=0,top=60)
        plt.xticks(rotation=35)
        ax.set_ylabel('Nitrate Concentration(NO3) mg/L')

        # Extending the right part of the graph
        left, right = plt.xlim()
        plt.xlim(left,right + 0.1 * (right - left))
        left, right = plt.xlim()

        # 0 -> 25
        x0,x1 = plt.xlim()
        y0,y1 = plt.ylim()
        rect = patches.Rectangle((x0,0), x1-x0,25, linewidth=1, edgecolor='#3B97D4', facecolor='#3B97D4',alpha=0.3)
        ax.add_patch(rect)

        ax.text(x=right - 0.1,y=1,s='Good Quality',ha='right',color='#245373')

        # 25 -> 50
        rect = patches.Rectangle((x0, 25), x1 - x0, 25, linewidth=1,
                                 edgecolor='#dbb344', facecolor='#dbb344',
                                 alpha=0.3)
        ax.add_patch(rect)

        ax.text(x=right - 0.1,y=26,s='Adequate',ha='right',color='#755f23')

        # 50 -> 200
        rect = patches.Rectangle((x0,50), x1-x0,150, linewidth=1, edgecolor='#D4453A', facecolor='#D4453A',alpha=0.3)
        ax.add_patch(rect)

        ax.text(x=right - 0.1,y=51,s='Poor Quality',ha='right',color='#73251f')

        # Date format
        fmt = mdates.DateFormatter('%b. %d')
        ax.xaxis.set_major_formatter(fmt)

        # Background and borders
        fig.patch.set_facecolor('#FFFFFF')
        ax.patch.set_facecolor('#FFFFFF')
        for location in ['left','right','bottom','top']:
            ax.spines[location].set_visible(False)

        return fig

def weather_figure(weather):

    with plt.style.context('fivethirtyeight'):

        fig, axs = plt.subplots(3,1,figsize=(12,12))
        fig.patch.set_facecolor('#FFFFFF')

        # Temperature Plot
        axs[0].plot(weather.index,weather.temperature,color='#fc7703',alpha=0.6)
        axs[0].yaxis.set_tick_params(colors='#fc7703')
        axs[0].set_ylabel('Mean Temperature (°C)',color='#fc7703')

        # Today line
        axs[0].axvline(x=datetime.today(),color='red',linewidth=2)

        # Today txt
        ylim = axs[0].get_ylim()
        td_y = ylim[0] + (ylim[1] - ylim[0]) * 1.05
        axs[0].text(x=datetime.today()-timedelta(4),y=td_y,s='Today',color='red')

        # Precipitation Plot
        axs[1].bar(weather.index,weather.precipitation,color='#567ee3',alpha=0.6)
        axs[1].yaxis.set_tick_params(colors='#567ee3')
        axs[1].set_ylabel('Precipitation (mm)',color='#567ee3')
        axs[1].axvline(x=datetime.today(),color='red',linewidth=2)

        # Maxwind Plot
        axs[2].bar(weather.index, weather.maxwind, color='#948800', alpha=0.6)
        axs[2].yaxis.set_tick_params(colors='#948800')
        axs[2].set_ylabel('Max Wind (km/h)', color='#948800')
        axs[2].axvline(x=datetime.today(),color='red',linewidth=2)

        # Background and borders
        for ax in axs :
            ax.patch.set_facecolor('#FFFFFF') # background color to white
            for location in ['left','right','bottom','top']:
                ax.spines[location].set_visible(False)

        # Date format
        for ax in axs :
            fmt = mdates.DateFormatter('%b. %d')
            ax.xaxis.set_major_formatter(fmt)

        return fig
