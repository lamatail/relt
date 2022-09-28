import pandas as pd
import numpy as np

load_plan = [
    ('100%', 100, [0, 15]),
    ('200%', 200, [0, 15]),
    ('300%', 300, [0, 15]),
]


def percentile(n):
    def percentile_(x):
        return np.percentile(x, n)
    percentile_.__name__ = f'percentile_{n}'
    return percentile_


def generate_data():
    return pd.concat([
        pd.DataFrame(
            data=zip(
                pd.date_range(start='2021-01-01 00:00:00', periods=900, freq='S'),
                ['test1', 'test2', 'test3', 'test4', 'test5'] * 900,
                np.random.randint(100, 200, size=900),
                np.random.randint(1, 2, size=900)),
            columns=['time', 'name', 'delay', 'count']
        ),
        pd.DataFrame(
            data=zip(
                list(pd.date_range(start='2021-01-01 00:15:00', periods=900, freq='S')) * 2,
                ['test1', 'test2', 'test3', 'test4', 'test5'] * 1800,
                np.random.randint(150, 220, size=1800),
                np.random.randint(1, 2, size=1800)),
            columns=['time', 'name', 'delay', 'count']
        ),
        pd.DataFrame(
            data=zip(
                list(pd.date_range(start='2021-01-01 00:30:00', periods=900, freq='S')) * 3,
                ['test1', 'test2', 'test3', 'test4', 'test5'] * 2700,
                np.random.randint(190, 250, size=2700),
                np.random.randint(1, 2, size=2700)),
            columns=['time', 'name', 'delay', 'count']
        )
    ])

