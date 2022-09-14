import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class TableMetric():
    def __init__(self,
                 data_source: pd.DataFrame,
                 load_plan: list,
                 operation_column: list[str],
                 start_time: datetime = None,
                 time_column: str = 'time',
                 index_name: list[str] = ['alias', 'metric'],
                 offset_left: int = 0,
                 offset_right: int = 0):
        self.data_source = data_source
        self.data_sla = {}
        self.data_metric = {}
        self.data_metric_assemble = None
        self.data_sla_assemble = {}
        self.load_plan = load_plan
        self.operation_column = operation_column
        self.operation_name = data_source[operation_column].drop_duplicates().to_records(index=False)
        self.start_time = data_source[time_column].min() if start_time is None else start_time
        self.time_column = time_column
        self.offset_left = offset_left
        self.offset_right = offset_right
        self.index_name = index_name

    def __get_shift_time_level_load(self):
        shift_level = 0
        for alias_level, load_level, time_level in self.load_plan:
            up_time = time_level[0]
            hold_time = time_level[1]
            shift_level = up_time + self.offset_left + shift_level
            duration_level = hold_time - self.offset_left - self.offset_right
            yield alias_level, load_level, shift_level, duration_level
            shift_level += up_time + hold_time

    def __get_alias_level(self):
        return [level[0] for level in self.load_plan]

    def metric(self,
               metric_name: str,
               metric_type: str,
               rename: str = None,
               func=np.average):
        rename = rename if rename else metric_name
        for alias_level, load_level, shift_level, duration_level in self.__get_shift_time_level_load():
            mask_time_start = self.data_source[self.time_column] >= self.start_time + timedelta(minutes=shift_level)
            mask_time_end = self.data_source[self.time_column] < self.start_time + timedelta(minutes=shift_level + duration_level)
            data_level = self.data_source[mask_time_start & mask_time_end].groupby(self.operation_column, dropna=False)[metric_name].agg(lambda x: func(x).astype(metric_type))
            self.data_metric[alias_level] = data_level.rename((alias_level, rename)).rename_axis('operation')
        return self.data_metric

    def sla(self, sla, name, func=None):
        if isinstance(sla, (int, float)):
            raise TypeError(f'Type {type(sla)} not support for sla data')
        elif isinstance(sla, pd.Series):
            self.data_sla[name] = {}
            for alias_level in self.__get_alias_level():
                if func is None:
                    self.data_sla[name][alias_level] = sla.rename(name)
                else:
                    self.data_sla[name][alias_level] = func(self.data_metric[alias_level], sla).rename((alias_level, name))
            return self.data_sla[name]
        else:
            raise TypeError(f'Type {type(sla)} not support for sla data')

    def assemble_data_metric(self):
        if self.data_metric:
            self.data_metric_assemble = pd.concat([self.data_metric[alias_level]
                                                   for alias_level in self.__get_alias_level()], axis=1)
            self.data_metric_assemble.columns.set_names(self.index_name, inplace=True)
            return self.data_metric_assemble
        else:
            raise ValueError('Data metric is empty')

    def assemble_data_sla(self, name: str):
        if self.data_sla:
            self.data_sla_assemble[name] = pd.concat([self.data_sla[name][alias_level]
                                                      for alias_level in self.__get_alias_level()], axis=1)
            self.data_sla_assemble[name].columns.set_names(self.index_name, inplace=True)
            return self.data_sla_assemble[name]
        else:
            raise ValueError('Data sla is empty')

    def assemble_data(self, sla_names: list[str] = None):
        sla_names = sla_names if sla_names else self.data_sla_assemble.keys()
        data_sla_all = [v for k, v in self.data_sla_assemble.items() if k in sla_names]
        self.data_sla_assemble = pd.concat(data_sla_all + [self.data_metric_assemble], axis=1).sort_index(axis=1)
        return self.data_sla_assemble