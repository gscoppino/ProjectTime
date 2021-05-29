import pandas as pd

from bokeh.embed import components
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
from calendar import monthrange
from datetime import timedelta
from django.db.models import F, Sum
from math import pi

from ProjectTime.project.models import Charge


def get_monthly_summary_series(date, project_ids=None):
    charges = Charge.objects.filter(end_time__isnull=False)
    if project_ids:
        charges = charges.filter(project__in=project_ids)

    _, end_of_month = monthrange(date.year, date.month)
    limit_day = timedelta(days=1, microseconds=-1)

    charges = (charges
               .filter(start_time__range=(
                   date.replace(day=1,
                                hour=0,
                                minute=0,
                                second=0,
                                microsecond=0),
                   date.replace(day=end_of_month,
                                hour=0,
                                minute=0,
                                second=0,
                                microsecond=0) + limit_day
               ))
               .select_related('project')
               .values('project')
               .order_by('project_id')
               .annotate(project_name=F('project__name'))
               .annotate(total_time_charged=Sum(
                   F('end_time') - F('start_time')
               )))

    chart_data = ({
        charge['project_name']:
        charge['total_time_charged'].total_seconds() / 3600
        for charge in charges
    })

    series = (pd.Series(chart_data, dtype='float64')
                .reset_index(name='value')
                .rename(columns={'index': 'charge'}))

    series['angle'] = series['value'] / series['value'].sum() * (2 * pi)

    category_count = len(chart_data)
    if category_count <= 20:
        series['color'] = (Category20c[len(chart_data)]
                           if category_count >= 3
                           else Category20c[3][0:category_count])

    return series


def get_monthly_summary_chart_components(series):
    chart = figure(title="Monthly Summary",
                   toolbar_location=None,
                   tools="hover",
                   tooltips="@charge: @value hour(s)",
                   outline_line_color="white",
                   sizing_mode="stretch_width")

    chart.wedge(source=series,
                x=0,
                y=1,
                radius=0.4,
                start_angle=cumsum('angle', include_zero=True),
                end_angle=cumsum('angle'),
                line_color='white',
                fill_color='color',
                legend_field='charge')

    chart.axis.axis_label = None
    chart.axis.visible = False
    chart.grid.grid_line_color = None
    chart.legend.location = 'top_left'

    return components(chart)
