from pandas import DataFrame
from alive_progress import alive_bar
from analyze import analyzing
import pandas as pd
from config import settings
import time
from disk_processing import DiskProcessing
from excel_processing import ExcelParser
from log_config import logger
from dataframe_processing import DataframeProcess


def append_to_stage_tables(deposit_type: str, special_dataframe: DataFrame, common_dataframe: DataFrame,
                           conclusion_dict: dict):
    settings.df_COMMON = pd.concat([common_dataframe, settings.df_COMMON])

    conclusion_dataframe = pd.DataFrame([conclusion_dict])
    settings.df_CONCLUSION = pd.concat([conclusion_dataframe, settings.df_CONCLUSION])

    if deposit_type.lower() == settings.DEPOSIT_TYPES[0]:
        settings.df_PL_MOTHABALLED_UNFIN_OBJ = pd.concat([special_dataframe, settings.df_PL_MOTHABALLED_UNFIN_OBJ])

    elif deposit_type.lower() == settings.DEPOSIT_TYPES[1]:
        settings.df_PLEDGE_PR_RIGHT_PROCEEDS = pd.concat([special_dataframe, settings.df_PLEDGE_PR_RIGHT_PROCEEDS])

    elif deposit_type.lower() == settings.DEPOSIT_TYPES[2]:
        settings.df_PLEDGE_PR_RIGHT_ACQUIRED_PR = pd.concat(
            [special_dataframe, settings.df_PLEDGE_PR_RIGHT_ACQUIRED_PR])

    elif deposit_type.lower() == settings.DEPOSIT_TYPES[3]:
        settings.df_PLEDGE_PR_RIGHT_LEASING = pd.concat([special_dataframe, settings.df_PLEDGE_PR_RIGHT_LEASING])

    elif deposit_type.lower() == settings.DEPOSIT_TYPES[4]:
        settings.df_PLEDGE_IMPERFECT_UNPRESERVED_OBJ = pd.concat(
            [special_dataframe, settings.df_PLEDGE_IMPERFECT_UNPRESERVED_OBJ])

    elif deposit_type.lower() == settings.DEPOSIT_TYPES[5]:
        settings.df_PLEDGE_FA_INSTALLED_EQ = pd.concat([special_dataframe, settings.df_PLEDGE_FA_INSTALLED_EQ])

    elif deposit_type.lower() == settings.DEPOSIT_TYPES[6]:
        settings.df_PLEDGE_GOODS = pd.concat([special_dataframe, settings.df_PLEDGE_GOODS])

    elif deposit_type.lower() == settings.DEPOSIT_TYPES[7]:
        settings.df_PLEDGED_VEHICLES = pd.concat([special_dataframe, settings.df_PLEDGED_VEHICLES])

    elif deposit_type.lower() == settings.DEPOSIT_TYPES[8]:
        settings.df_PLEDGE_SECURITIES = pd.concat([special_dataframe, settings.df_PLEDGE_SECURITIES])

    elif deposit_type.lower() == settings.DEPOSIT_TYPES[9]:
        settings.df_MORTGAGE = pd.concat([special_dataframe, settings.df_MORTGAGE])

    else:
        description, system_message = f"The type of the collateral {deposit_type} does not correspond to any of the existing types / Вид залога {deposit_type} не соответствует ни одному из существующих типов", 'No matches found'
        logger.warning(msg=description, exc_info=system_message)


def tables_to_csv():
    settings.df_CONCLUSION.to_excel(settings.db_path + '\\df_CONCLUSION.xlsx')
    settings.df_COMMON.to_excel(settings.db_path + '\\df_COMMON.xlsx')
    settings.df_PL_MOTHABALLED_UNFIN_OBJ.to_excel(settings.db_path + '\\df_PL_MOTHABALLED_UNFIN_OBJ.xlsx')
    settings.df_PLEDGE_PR_RIGHT_PROCEEDS.to_excel(settings.db_path + '\\df_PLEDGE_PR_RIGHT_PROCEEDS.xlsx')
    settings.df_PLEDGE_PR_RIGHT_ACQUIRED_PR.to_excel(settings.db_path + '\\df_PLEDGE_PR_RIGHT_ACQUIRED_PR.xlsx')
    settings.df_PLEDGE_PR_RIGHT_LEASING.to_excel(settings.db_path + '\\df_PLEDGE_PR_RIGHT_LEASING.xlsx')
    settings.df_PLEDGE_IMPERFECT_UNPRESERVED_OBJ.to_excel(
        settings.db_path + '\\df_PLEDGE_IMPERFECT_UNPRESERVED_OBJ.xlsx')
    settings.df_PLEDGE_FA_INSTALLED_EQ.to_excel(settings.db_path + '\\df_PLEDGE_FA_INSTALLED_EQ.xlsx')
    settings.df_PLEDGE_GOODS.to_excel(settings.db_path + '\\df_PLEDGE_GOODS.xlsx')
    settings.df_PLEDGED_VEHICLES.to_excel(settings.db_path + '\\df_PLEDGED_VEHICLES.xlsx')
    settings.df_PLEDGE_SECURITIES.to_excel(settings.db_path + '\\df_PLEDGE_SECURITIES.xlsx')
    settings.df_MORTGAGE.to_excel(settings.db_path + '\\df_MORTGAGE.xlsx')


def doc_dt(path: str):
    for year in range(2019, 2025):
        if str(year) in path:
            return year
    return 0


def process_excel_data():
    start_time = time.time()
    disk = DiskProcessing()
    paths = disk.paths_processing()
    data = []
    file_addresses = pd.DataFrame(columns=['file_id', 'file_path'])
    new_address: dict
    file_id = 0
    (empty_failed, read_excel_failed, get_appendix_failed, get_deposit_type_failed, get_appendix_dataframe_failed,
     search_appendix_cell_failed, check_type_failed, processing_failed) = 0, 0, 0, 0, 0, 0, 0, 0
    excel_success, excel_failed, deposit_success, deposit_failed = 0, 0, 0, 0
    with alive_bar(len(paths)) as bar:
        for network_drive in paths[0]:
            year: int = doc_dt(network_drive)
            excel_process = ExcelParser(network_drive, file_id, year)
            if excel_process.read_excel():
                data_: list = []
                success_process: list = []
                while excel_process.check_deposit_item():
                    excel_process.assign_to_main_deposit_dict()
                    main_dict: dict = excel_process.main_deposit_dict
                    dep_type: str = main_dict['pledge_type']
                    app_names: list[str] = main_dict['extra_app_names']
                    exception_params: list = [network_drive, app_names, year]
                    data_.append(excel_process.get_appendix_dataframe())
                    if excel_process.check_for_existence():
                        del data_[-1]
                        deposit_failed += 1
                    else:
                        data_process = DataframeProcess(df_list=data_[-1], old_v=excel_process.old_version,
                                                        deposit_type=dep_type, file_id=file_id,
                                                        pledge_type_id=main_dict['pledge_type_id'],
                                                        exception_params=exception_params)
                        data.append(data_process.data_slice())
                        check_type_failed += data_process.check_type_failed
                        processing_failed += data_process.processing_failed
                        if data[-1] is None:
                            del data[-1]
                            deposit_failed += 1
                            success_process.append(False)
                        elif data[-1][0].empty or data[-1][1].empty:
                            empty_failed += 1
                            description, system_message = 'Application sheets does not match the required structure. ' \
                                                          'Data has not been loaded /' \
                                                          ' Листы приложений не соответствуют необходимой структуре.' \
                                                          ' Данные не были загружены.', \
                                                          'Dataframe is empty'
                            logger.warning(msg=description, exc_info=system_message, extra={
                                "file_path": network_drive,
                                "app_name": app_names,
                                "deposit_type": dep_type,
                                "year": year
                            })
                            del data[-1]
                            deposit_failed += 1
                            success_process.append(False)
                        else:
                            del main_dict['extra_app_names']
                            deposit_success += 1
                            append_to_stage_tables(dep_type, data[-1][0], data[-1][1], main_dict)
                            success_process.append(True)
                if any(success_process):
                    excel_success += 1
                    description = 'SUCCESS.'
                    logger.info(msg=description, extra={
                        "system_message": 'The information has been recorded in the database / '
                                          'Информация занесена в базу данных.',
                        "file_path": network_drive,
                        "year": year,
                        "file_id": file_id
                    })
                else:
                    excel_failed += 1
                    description = 'FAILURE.'
                    system_message = "The information was not recorded due to errors that occurred / " \
                                     "Информация не была записана из-за возникших ошибок."
                    logger.info(msg=description, extra={
                        "system_message": system_message,
                        "file_path": network_drive,
                        "year": year,
                        "file_id": file_id
                    })
            else:
                excel_failed += 1

            read_excel_failed += excel_process.read_excel_failed
            get_appendix_failed += excel_process.get_appendix_failed
            get_deposit_type_failed += excel_process.get_deposit_type_failed
            get_appendix_dataframe_failed += excel_process.get_appendix_dataframe_failed
            search_appendix_cell_failed += excel_process.search_appendix_cell_failed

            new_address = {'file_id': file_id, 'file_address': network_drive}
            file_addresses = file_addresses._append(new_address, ignore_index=True)

            file_id += 1
            bar()
    tables_to_csv()

    end_time = time.time()
    description = 'The processing of Excel files is over / Обработка файлов Excel завершена.'
    execution_time = (end_time - start_time) / 60
    system_message = f'Execution time: {execution_time} minutes'
    logger.info(msg=description, extra={"system_message": system_message})

    file_addresses.to_excel(str(settings.ROOT_PATH) + '\\file_addresses.xlsx')

    analyzing(total=len(paths), success=excel_success, failed=excel_failed, df_success=deposit_success,
              df_failed=deposit_failed,
              type_errors=[empty_failed, check_type_failed, processing_failed,
                           read_excel_failed, get_appendix_dataframe_failed])


if __name__ == "__main__":
    process_excel_data()
