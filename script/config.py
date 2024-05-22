import pandas as pd
import hashlib
from pathlib import Path
from dotenv import dotenv_values


def hash_string(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    return md5_hash.hexdigest()


class Settings:

    def create_stage_dbs(self):
        df = pd.DataFrame(columns=self.CONCLUSION_ATTRIBUTES)

        df1 = pd.DataFrame(columns=self.PL_MOTHABALLED_UNFIN_OBJ)

        df2 = pd.DataFrame(columns=self.PLEDGE_PR_RIGHT_PROCEEDS)

        df3 = pd.DataFrame(columns=self.PLEDGE_PR_RIGHT_ACQUIRED_PR)

        df4 = pd.DataFrame(columns=self.PLEDGE_PR_RIGHT_LEASING)

        df5 = pd.DataFrame(columns=self.PLEDGE_IMPERFECT_UNPRESERVED_OBJ)

        df6 = pd.DataFrame(columns=self.PLEDGE_FA_INSTALLED_EQ)

        df7 = pd.DataFrame(columns=self.PLEDGE_GOODS)

        df8 = pd.DataFrame(columns=self.PLEDGED_VEHICLES)

        df9 = pd.DataFrame(columns=self.PLEDGE_SECURITIES)

        df10 = pd.DataFrame(columns=self.MORTGAGE)

        df11 = pd.DataFrame(columns=self.COMMON_ATTRIBUTES)


        return df, df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11

    def __init__(self):
        self.ROOT_PATH = Path(__file__).resolve().parents[0]
        self.db_path = str(self.ROOT_PATH) + '\\stage_database'

        env_vars = dotenv_values(".env")
        self.CONCLUSION_PATTERNS = env_vars["CONCLUSION_PATTERNS"].split(',')
        self.CONCLUSION_ATTRIBUTES = env_vars["CONCLUSION_ATTRIBUTES"].split('\n')
        self.DEPOSIT_TYPES = env_vars["DEPOSIT_TYPES"].split(';\n')

        self.PL_MOTHABALLED_UNFIN_OBJ = env_vars["PL_MOTHABALLED_UNFIN_OBJ"].split('\n')
        self.PLEDGE_PR_RIGHT_PROCEEDS = env_vars["PLEDGE_PR_RIGHT_PROCEEDS"].split('\n')
        self.PLEDGE_PR_RIGHT_ACQUIRED_PR = env_vars["PLEDGE_PR_RIGHT_ACQUIRED_PR"].split('\n')
        self.PLEDGE_PR_RIGHT_LEASING = env_vars["PLEDGE_PR_RIGHT_LEASING"].split('\n')
        self.PLEDGE_IMPERFECT_UNPRESERVED_OBJ = env_vars["PLEDGE_IMPERFECT_UNPRESERVED_OBJ"].split('\n')
        self.PLEDGE_FA_INSTALLED_EQ = env_vars["PLEDGE_FA_INSTALLED_EQ"].split('\n')
        self.PLEDGE_GOODS = env_vars["PLEDGE_GOODS"].split('\n')
        self.PLEDGED_VEHICLES = env_vars["PLEDGED_VEHICLES"].split('\n')
        self.PLEDGE_SECURITIES = env_vars["PLEDGE_SECURITIES"].split('\n')
        self.MORTGAGE = env_vars["MORTGAGE"].split('\n')

        self.COMMON_ATTRIBUTES = env_vars["COMMON_ATTRIBUTES"].split('\n')

        (self.df_CONCLUSION, self.df_PL_MOTHABALLED_UNFIN_OBJ, self.df_PLEDGE_PR_RIGHT_PROCEEDS,
         self.df_PLEDGE_PR_RIGHT_ACQUIRED_PR, self.df_PLEDGE_PR_RIGHT_LEASING, self.df_PLEDGE_IMPERFECT_UNPRESERVED_OBJ,
         self.df_PLEDGE_FA_INSTALLED_EQ, self.df_PLEDGE_GOODS, self.df_PLEDGED_VEHICLES, self.df_PLEDGE_SECURITIES,
         self.df_MORTGAGE,
         self.df_COMMON) = self.create_stage_dbs()

        self.FLOAT_ATTRIBUTES = env_vars["FLOAT_ATTRIBUTES"].split('\n')


settings: Settings = Settings()
