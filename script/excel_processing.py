import warnings
import re
import pandas as pd
import xlrd
from log_config import logger
from config import settings


class ExcelProcessor:
    def __init__(self, file_path, file_id, year):
        self.file_path: str = file_path
        self.file_id: int = file_id
        self.year: int = year
        self._xls, self.df = None, None
        self.row_index: int = 0
        self.read_excel_failed: int = 0

    def read_excel(self) -> bool:
        warnings.simplefilter(action='ignore', category=UserWarning)
        try:
            self._xls = pd.read_excel(self.file_path, sheet_name=None)
            self.df = self._xls['Заключение']
        except FileNotFoundError as e:
            self.read_excel_failed += 1
            description = f"File was not found / Файл не найден."
            logger.error(msg=description, extra={
                "file_path": self.file_path,
                "system_message": e,
                "year": self.year
            })
            return False
        except ValueError as e:
            self.read_excel_failed += 1
            description = f"Unable to open the file due to unsupported excel format / " \
                          f"Невозможно открыть файл из-за неподдерживаемого формата Excel."
            logger.error(msg=description, extra={
                "file_path": self.file_path,
                "system_message": e,
                "year": self.year
            })
            return False
        except PermissionError as e:
            self.read_excel_failed += 1
            description = f"The file cannot be opened because it is in use / " \
                          f"Файл не может быть открыт, так как он используется."
            logger.error(msg=description, extra={
                "file_path": self.file_path,
                "system_message": e,
                "year": self.year
            })
            return False
        except xlrd.biffh.XLRDError as e:
            self.read_excel_failed += 1
            description = f"Unable to open the file due to unsupported excel format / " \
                          f"Невозможно открыть файл из-за неподдерживаемого формата Excel."
            logger.error(msg=description, extra={
                "file_path": self.file_path,
                "system_message": e,
                "year": self.year
            })
            return False
        return True

    def check_deposit_item(self) -> bool:
        warnings.simplefilter(action='ignore', category=FutureWarning)
        result: bool = (self.df.iloc[self.row_index:, 0].str.startswith(settings.CONCLUSION_PATTERNS[3]).fillna(False)).any()
        return result


class ExcelParser(ExcelProcessor):
    def __init__(self, file_path, file_id, year):
        super().__init__(file_path, file_id, year)
        self.get_appendix_failed: int = 0
        self.get_deposit_type_failed: int = 0
        self.get_appendix_dataframe_failed: int = 0
        self.search_appendix_cell_failed: int = 0
        self.value: str | None = None
        self.main_deposit_dict: dict | None = None
        self._key: str | None = None
        self.old_version: bool = any(item in self.file_path for item in ['_2019', '_2020', '_2021'])
        self.pledge_type_id: int = 0

    def check_sheet_exists(self, sheet_name: str):
        try:
            return sheet_name in self._xls
        except FileNotFoundError:
            return False

    def search_deposit_item(self, item: str, column: int) -> str:
        try:
            tmp = column
            if self.df.iloc[self.row_index:, column + 1].str.startswith(item).fillna(False).any():
                column += 1
            starts_with = self.df.iloc[self.row_index:, column].str.startswith(item).fillna(False)
            self.row_index = starts_with[starts_with].index[0]
            row = self.df.loc[self.row_index]
            self.value = row[row.notnull()].values[tmp + 1]
        except IndexError:
            self.value = None
        finally:
            return self.value

    def search_conclusion_item(self, item: str, column: int) -> str | None:
        try:
            if self.df.iloc[:, column + 1].str.startswith(item).fillna(False).any():
                column += 1
            starts_with = self.df.iloc[:, column].str.startswith(item).fillna(False)
            row_index = starts_with[starts_with].index[0]
            row = self.df.loc[row_index]
            self.value = row[row.notnull()].values[column + 1]
        except IndexError:
            self.value = None
        finally:
            return self.value

    def assign_to_main_deposit_dict(self):
        self.pledge_type_id += 1
        self.main_deposit_dict = {'file_id': self.file_id,
                                  'pledge_type_id':
                                      self.pledge_type_id,
                                  'conclusion_dt':
                                      self.search_conclusion_item(item=settings.CONCLUSION_PATTERNS[0], column=1),
                                  'debtor_name':
                                      self.search_conclusion_item(item=settings.CONCLUSION_PATTERNS[1], column=0),
                                  'debtor_unn':
                                      self.search_conclusion_item(item=settings.CONCLUSION_PATTERNS[2], column=0),
                                  'pledge_type':
                                      self.get_deposit_type(),
                                  'extra_app_names':
                                      self.get_appendix(),
                                  'pledge_name':
                                      self.search_deposit_item(item=settings.CONCLUSION_PATTERNS[4], column=0),
                                  'mortgagor_name':
                                      self.search_deposit_item(item=settings.CONCLUSION_PATTERNS[5], column=0),
                                  'mortgagor_unn':
                                      self.search_deposit_item(item=settings.CONCLUSION_PATTERNS[6], column=0),
                                  'total_collateral_val_amt':
                                      self.search_deposit_item(item=settings.CONCLUSION_PATTERNS[7], column=1)}

    def generate_keys(self) -> str:
        self._key = str(self.main_deposit_dict['mortgagor_unn']) + '-' + str(
            self.main_deposit_dict['pledge_name']) + '-' + str(self.main_deposit_dict['total_collateral_val_amt'])
        return self._key

    def search_appendix_cell(self) -> str | None:
        try:
            starts_with = self.df.iloc[self.row_index:, 0].str.startswith(settings.CONCLUSION_PATTERNS[3]).fillna(False)
            row_index: int = starts_with[starts_with].index[0]
            self.value = self.df.iloc[row_index, 0]
        except IndexError as e:
            self.search_appendix_cell_failed += 1
            self.value = None
            description = f"Pattern '{settings.CONCLUSION_PATTERNS[3]}' not found / " \
                          f"Паттерн '{settings.CONCLUSION_PATTERNS[3]}' не найден."
            logger.error(msg=description, extra={
                "file_path": self.file_path,
                "app_name": "Заключение",
                "system_message": e,
                "year": self.year
            })
        finally:
            return self.value

    def get_appendix(self) -> list:
        try:
            cell_value: str = self.search_appendix_cell()
            pattern: str = r"\((П.*?)\)"
            matches = re.findall(pattern, cell_value)
            if len(matches) == 0:
                self.get_appendix_failed += 1
                description = f"The format of '{cell_value}' does not match a regular expression / " \
                              f"Формат «{cell_value}» не соответствует регулярному выражению."
                logger.waring(msg=description, extra={
                    "file_path": self.file_path,
                    "app_name": "Заключение",
                    "system_message": "Incorrect type",
                    "year": self.year
                })
                return matches
            matches = matches[0].split(', ')
            return matches
        except TypeError:
            return []

    def get_appendix_dataframe(self) -> list:
        apps: list = []
        for item in self.main_deposit_dict['extra_app_names']:
            try:
                if self.check_sheet_exists(item):
                    apps.append(self._xls[item])
                else:
                    item = item.replace(' ', '')
                    apps.append(self._xls[item])
                    if "_2022" in self.file_path:
                        self.old_version = True
            except KeyError as e:
                self.get_appendix_dataframe_failed += 1
                description = f"{item} not found at excel table."
                logger.error(msg=description, extra={
                    "file_path": self.file_path,
                    "system_message": e,
                    "year": self.year
                })
        return apps

    def get_deposit_type(self) -> str:
        pattern: str = r": (.*?) \(Пр"
        cell_value: str = self.search_appendix_cell()
        if cell_value is None:
            return ''
        try:
            match = re.findall(pattern, cell_value)
            if len(match) == 0:
                self.get_deposit_type_failed += 1
                description = f"The format of '{cell_value}' does not match a regular expression / " \
                              f"Формат «{cell_value}» не соответствует регулярному выражению."
                logger.warning(msg=description, extra={
                    "file_path": self.file_path,
                    "system_message": description,
                    "year": self.year
                })
                return ''
            return match[0]
        except TypeError as e:
            self.get_deposit_type_failed += 1
            description = f"Incorrect type of '{cell_value}' / Неверный тип '{cell_value}'"
            logger.warning(msg=description, extra={
                "file_path": self.file_path,
                "system_message": e,
                "year": self.year
            })
            return ''

    def check_for_existence(self) -> bool:
        return self.main_deposit_dict['total_collateral_val_amt'] is None

    @property
    def key(self) -> str:
        return self._key
