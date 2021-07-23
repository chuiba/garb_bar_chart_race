import pandas as pd
import bar_chart_race_cn as bcr

df = pd.read_csv('test.csv')
df.set_index('Data', inplace=True)

bcr.bar_chart_race(
    df=df,
    filename='garb_top10.mp4',
    orientation='h',
    sort='desc',
    n_bars=10,
    fixed_order=False,
    fixed_max=True,
    steps_per_period=20,
    interpolate_period=False,
    label_bars=True,
    bar_size=.95,
    period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
    period_fmt= '{x:.0f}',
    period_summary_func=lambda v, r: {'x': .99, 'y': .18,
                                      's': f'Total Sales: {v.nlargest(10).sum():,.0f}',
                                      'ha': 'right', 'size': 8, 'family': 'Courier New'},
    period_length=600,
    figsize=(12, 6),
    dpi=300,
    cmap='dark12',
    title='装扮前十总和',
    bar_label_size=7,
    tick_label_size=7,
    scale='linear',
    writer=None,
    fig=None,
    bar_kwargs={'alpha': .7},
    filter_column_colors=False)
