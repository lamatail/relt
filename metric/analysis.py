import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class LoadMetric(ABC):
    def __init__(self,
                 data_source: pd.DataFrame = None,
                 operation_column: list[str] = None,
                 start_time: datetime = None,
                 time_column: str = 'time',
                 index_name: list[str] = ['alias', 'metric']):
        self.data_source = data_source
        self.data_metric: dict[dict[pd.Series]] = {}
        self.data_metric_assemble: pd.DataFrame = None
        self.operation_column = operation_column
        self.operation_name = N1
        one
        self.start_time = None
        self.time_column = time_column
        self.index_name = index_name

    @abstractmethod
    def shift_time_load(self) -> list[str, int, int, int]:
        pass

    def alias_level(self):
        return [level[0] for level in self.load_plan]

    def metric(self, metric_group: str, metric_func) -> pd.DataFrame:
        if self.operation_name is None:
            self.operation_name = self.data_source[self.operation_column].drop_duplicates().to_records(index=False)
        if self.start_time is None:
            self.start_time = self.data_source[self.time_column].min() if self.start_time is None else self.start_time
        metric_name = metric_func.metric_name
        if metric_name is not self.data_metric:
            self.data_metric[metric_name] = {}
        for alias_level, load_level, shift_level, duration_level in self.shift_time_load():
            mask_time_start = self.data_source[self.time_column] >= self.start_time + timedelta(minutes=shift_level)
            mask_time_end = self.data_source[self.time_column] < self.start_time + timedelta(minutes=shift_level + duration_level)
            data_level = self.data_source[mask_time_start & mask_time_end].groupby(self.operation_column, dropna=False)[metric_group].agg(
                metric_func, load_level=load_level, duration_level=duration_level)
            self.data_metric[metric_name][alias_level] = data_level.rename((alias_level, metric_name)).rename_axis('operation').round(metric_func.precision)
        return self.data_metric

    def assemble_data_metric(self, metric_list: list = None) -> pd.DataFrame:
        metric_list = self.data_metric.keys() if metric_list is None else metric_list
        if self.data_metric:
            self.data_metric_assemble = pd.concat([self.data_metric[metric][alias]
                                                   for metric in metric_list
                                                   for alias in self.data_metric[metric].keys()], axis=1)
            self.data_metric_assemble.columns.set_names(self.index_name, inplace=True)
            self.data_metric_assemble = self.data_metric_assemble.reindex(sorted(self.data_metric_assemble.columns), axis=1)
            return self.data_metric_assemble
        else:
            raise ValueError('Data metric is empty')


class LoadStepMetric(LoadMetric):
    def __init__(self,
                 *args,
                 load_plan: list = None,
                 offset_left: int = 0,
                 offset_right: int = 0,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.load_plan = load_plan
        self.offset_left = offset_left
        self.offset_right = offset_right

    def shift_time_load(self):
        shift_level = 0
        for alias_level, load_level, time_level in self.load_plan:
            up_time = time_level[0]
            hold_time = time_level[1]
            shift_level = up_time + self.offset_left + shift_level
            duration_level = hold_time - self.offset_left - self.offset_right
            yield alias_level, load_level, shift_level, duration_level
            shift_level += up_time + hold_time

    @staticmethod
    def build_load_metric(df: pd.DataFrame):
        lsm = LoadStepMetric()
        lsm.operation_name = list(df.index.values)
        lsm.data_metric: dict[dict[pd.Series]] = {}
        for label, content in df.items():
            metric = label[1]
            alias = label[0]
            if metric not in lsm.data_metric:
                lsm.data_metric[metric] = {}
            lsm.data_metric[metric][alias] = content
        return lsm


class LoadHoldMetric(LoadMetric):
    def shift_time_load(self):
        pass

    def alias_level(self):
        pass
