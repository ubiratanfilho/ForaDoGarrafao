### Dependências
import plotly.graph_objects as go

### Funções
def custom_template(type_='bar'):
    if type_ == 'bar':
        custom_template = {
            "layout": go.Layout(
                font={
                    "color": "black",
                    "size": 16
                },
                title={
                    "font": {
                        "size": 22,
                        "color": "black",
                    },
                },
                plot_bgcolor="#ffffb2",
                paper_bgcolor="#ffffb2",
                xaxis={
                    "showgrid": False,
                    "zeroline": False,
                    "visible": False,
                },
                yaxis={
                    "showgrid": False,
                    "zeroline": False,
                    
                },
                margin=dict(b=20,r=30,l=200,t=100),
            )
        }
    return custom_template