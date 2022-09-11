from pandas import DataFrame
from datetime import datetime


class TableReportMetric():
    def __init__(self,
                 data_source: DataFrame,
                 load_plan: list[tuple(str, int, list[int, int])],
                 start_time: datetime = None,
                 time: str = 'time'):
        self.load_plan = load_plan
        self.start_time = data_source[time].min() if start_time is None else start_time
        self.indent_left = 0
        self.indent_right = 0

    def get_shift_time_level_load(self,
                                  indent: int = None,
                                  indent_left: int = None,
                                  indent_right: int = None):
        if indent:
            if not indent_left and not indent_right:
                indent_right = indent
                indent_left = indent
            else:
                raise ValueError('Set indent and indent_left or indent_right')
        else:
            if not (indent_left and indent_right):
                raise ValueError('Set not indent_left or indent_right')
        shift_level = 0
        for alias_level, load_level, time_level in self.load_plan:
            up_time = time_level[0]
            hold_time = time_level[1]
            shift = up_time + indent_left + shift_level
            duration = hold_time - indent_left - indent_right
            shift_level += up_time + hold_time
            yield alias_level, load_level, shift, duration
