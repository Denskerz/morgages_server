import os
import pandas as pd
import glob
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pandas import DataFrame


class DiskProcessing:
    def __init__(self):
        self.path_list = []
        self.paths = None
        self.final_path_list = []
        self.extensions = ['xls', 'xlsx', 'xlsm']

    def get_paths(self) -> DataFrame:
        prom = "\\\\Veeam-NSS\CRZ-Dispatcher\\"
        test_ift = "C:\\Users\eroshevich_d\Desktop\CRZ-Dispetcher\\"
        test_prom = "C:\\Users\eroshevich_d\PycharmProject\pythonProject\CRZ\\"
        for root, dirs, files in os.walk(prom):
            if 'Заключение' in root and 'отработанные' in root and '-Э-' in root \
                    and 'Плановый мониторинг' not in root and 'Архив' not in root and '_2018' not in root:
                for file in files:
                    if 'закл' in file.lower() and '.pdf' not in file:
                        self.path_list.append(os.path.join(root, file))

        return pd.DataFrame(self.path_list)

    def paths_processing(self):
        df = self.get_paths()
        df['filename'] = df[0].str.split('\\').str[-1]
        df['extension'] = df['filename'].str.split('.').str[-1]
        self.paths = df[df['extension'].isin(self.extensions)]
        # self.manual_processing(start_date=datetime(2019, 12, 15), end_date=None)
        return self.paths

    def auto_manual_processing(self):
        current_date = datetime.now()
        previous_date = current_date - relativedelta(months=1)
        interval = previous_date.strftime("_%m_%y")
        self.paths = self.paths[self.paths[0].str.contains(interval)]

    def manual_processing(self, start_date: datetime, end_date: datetime | None):
        date_array = []
        if end_date is not None:
            delta = end_date - start_date
            for i in range(delta.days - 1):
                date = start_date + timedelta(days=i)
                date = date.strftime("%d_%m_%y")
                date_array.append(str(date))
        else:
            date = start_date.strftime("%d_%m_%y")
            date_array.append(str(date))

        self.paths = self.paths[self.paths[0].str.contains('|'.join(date_array))]
