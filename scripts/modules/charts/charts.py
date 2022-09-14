import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from modules.datasets import Datasets

class ShotCharts:
        def __init__(self) -> None:
                pass
        
        def create_court(ax, color="white"):
                """ Create a basketball court in a matplotlib axes
                """
                # Short corner 3PT lines
                ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
                ax.plot([220, 220], [0, 140], linewidth=2, color=color)
                # 3PT Arc
                ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
                # Lane and Key
                ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
                ax.plot([80, 80], [0, 190], linewidth=2, color=color)
                ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
                ax.plot([60, 60], [0, 190], linewidth=2, color=color)
                ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
                ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))
                ax.plot([-250, 250], [0, 0], linewidth=4, color='white')
                # Rim
                ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))
                # Backboard
                ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
                # Remove ticks
                ax.set_xticks([])
                ax.set_yticks([])
                # Set axis limits
                ax.set_xlim(-250, 250)
                ax.set_ylim(0, 470)
                return ax
        
        def frequency_chart(df, name, season=None, extent=(-250, 250, 422.5, -47.5),
                                gridsize=25, cmap="inferno"):
                """ Create a shot chart of a player's shot frequency and accuracy
                """ 
                # create frequency of shots per hexbin zone
                shots_hex = plt.hexbin(
                df.LOC_X, df.LOC_Y + 60,
                extent=extent, cmap=cmap, gridsize=gridsize)
                plt.close()
                shots_hex_array = shots_hex.get_array()
                freq_by_hex = shots_hex_array / sum(shots_hex_array)
                
                # create field goal % per hexbin zone
                makes_df = df[df.SHOT_MADE_FLAG == 1] # filter dataframe for made shots
                makes_hex = plt.hexbin(makes_df.LOC_X, makes_df.LOC_Y + 60, cmap=cmap,
                                gridsize=gridsize, extent=extent) # create hexbins
                plt.close()
                pcts_by_hex = makes_hex.get_array() / shots_hex.get_array()
                pcts_by_hex[np.isnan(pcts_by_hex)] = 0  # convert NAN values to 0
                
                # filter data for zone with at least 5 shots made
                sample_sizes = shots_hex.get_array()
                filter_threshold = 5
                for i in range(len(pcts_by_hex)):
                        if sample_sizes[i] < filter_threshold:
                                pcts_by_hex[i] = 0
                x = [i[0] for i in shots_hex.get_offsets()]
                y = [i[1] for i in shots_hex.get_offsets()]
                z = pcts_by_hex
                sizes = freq_by_hex * 1000
                
                # Create figure and axes
                fig = plt.figure(figsize=(3.6, 3.6), facecolor='black', edgecolor='black', dpi=100)
                ax = fig.add_axes([0, 0, 1, 1], facecolor='black')
                plt.xlim(250, -250)
                plt.ylim(-47.5, 422.5)
                # Plot hexbins
                scatter = ax.scatter(x, y, c=z, cmap=cmap, marker='h', s=sizes)
                # Draw court
                ax = ShotCharts.create_court(ax)
                # Add legends
                max_freq = max(freq_by_hex)
                max_size = max(sizes)
                legend_acc = plt.legend(
                *scatter.legend_elements(num=5, fmt="{x:.0f}%",
                                        func=lambda x: x * 100),
                loc=[0.85,0.785], title='Shot %', fontsize=6)
                legend_freq = plt.legend(
                *scatter.legend_elements(
                        'sizes', num=5, alpha=0.8, fmt="{x:.1f}%"
                        , func=lambda s: s / max_size * max_freq * 100
                ),
                loc=[0.68,0.785], title='Freq %', fontsize=6)
                plt.gca().add_artist(legend_acc)
                # Add title
                plt.text(-250, 450, f"{name}", fontsize=21, color='white',
                        fontname='Franklin Gothic Medium')
                plt.text(-250, 420, "Frequência e Aproveitamento", fontsize=12, color='white',
                        fontname='Franklin Gothic Book')
                if len(season) > 1:
                        season = f"{season[0][:4]}-{season[-1][-2:]}"
                plt.text(-250, -20, season, fontsize=8, color='white')
                plt.text(110, -20, '@foradogarrafao', fontsize=8, color='white')

                return fig
        
        def volume_chart(df, name, season=None, 
                        RA=True,
                        extent=(-250, 250, 422.5, -47.5),
                        gridsize=25, cmap="plasma"):
                fig = plt.figure(figsize=(3.6, 3.6), facecolor='black', edgecolor='black', dpi=100)
                ax = fig.add_axes([0, 0, 1, 1], facecolor='black')

                # Plot hexbin of shots
                if RA == True:
                        x = df.LOC_X
                        y = df.LOC_Y + 60
                        # Annotate player name and season
                        plt.text(-250, 440, f"{name}", fontsize=21, color='white',
                                fontname='Franklin Gothic Medium')
                        plt.text(-250, 410, "Volume de arremessos", fontsize=12, color='white',
                                fontname='Franklin Gothic Book')
                        if len(season) > 1:
                                season = f"{season[0][:4]}-{season[-1][-2:]}"
                        plt.text(-250, -20, season, fontsize=8, color='white')
                        plt.text(110, -20, '@foradogarrafao', fontsize=8, color='white')
                else:
                        cond = ~((-45 < df.LOC_X) & (df.LOC_X < 45) & (-40 < df.LOC_Y) & (df.LOC_Y < 45))
                        x = df.LOC_X[cond]
                        y = df.LOC_Y[cond] + 60
                        # Annotate player name and season
                        plt.text(-250, 440, f"{name}", fontsize=21, color='white',
                                fontname='Franklin Gothic Medium')
                        plt.text(-250, 410, "Volume de arremessos", fontsize=12, color='white',
                                fontname='Franklin Gothic Book')
                        plt.text(-250, 385, "(sem área restrita)", fontsize=10, color='red')
                        if len(season) > 1:
                                season = f"{season[0][:4]}-{season[-1][-2:]}"
                        plt.text(-250, -20, season, fontsize=8, color='white')
                        plt.text(110, -20, '@foradogarrafao', fontsize=8, color='white')
                        
                hexbin = ax.hexbin(x, y, cmap=cmap,
                        bins="log", gridsize=25, mincnt=2, extent=(-250, 250, 422.5, -47.5))

                # Draw court
                ax = ShotCharts.create_court(ax, 'white')

                # add colorbar
                im = plt.imread("../imagens/Colorbar Shotcharts.png")
                newax = fig.add_axes([0.56, 0.6, 0.45, 0.4], anchor='NE', zorder=1)
                newax.xaxis.set_visible(False)
                newax.yaxis.set_visible(False)
                newax.imshow(im)

                return fig
        
        def makes_misses_chart(df, name, season=None):
                # Create figure and axes
                fig = plt.figure(figsize=(3.6, 3.6), facecolor='black', edgecolor='black', dpi=100)
                ax = fig.add_axes([0, 0, 1, 1], facecolor='black')

                plt.text(-250, 450, f"{name}", fontsize=21, color='white',
                        fontname='Franklin Gothic Medium')
                plt.text(-250, 425, "Erros", fontsize=12, color='red',
                        fontname='Franklin Gothic Book')
                plt.text(-195, 425, "e", fontsize=12, color='white',
                        fontname='Franklin Gothic Book')
                plt.text(-175, 425, "Acertos", fontsize=12, color='green',
                        fontname='Franklin Gothic Book')
                if len(season) > 1:
                        season = f"{season[0][:4]}-{season[-1][-2:]}"
                plt.text(-250, -20, season, fontsize=8, color='white')
                plt.text(110, -20, '@foradogarrafao', fontsize=8, color='white')

                ax = ShotCharts.create_court(ax, 'white')
                sc = ax.scatter(df.LOC_X, df.LOC_Y + 60, c=df.SHOT_MADE_FLAG, cmap='RdYlGn', s=12)

                return fig

