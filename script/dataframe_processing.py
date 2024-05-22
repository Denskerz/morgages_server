import re

from config import settings, hash_string
from log_config import logger
import numpy as np
import pandas as pd


class DataframeProcess:
    def __init__(self, df_list: list, old_v: bool, deposit_type: str, file_id: int,
                 pledge_type_id: int, exception_params: list):
        self.check_type_failed = 0
        self.processing_failed = 0
        self.df_list = df_list
        self.old_v = old_v
        self.df_result = None
        self.deposit_type = deposit_type
        # self.at_seven_row = ['залог законсервированных незавершенных строительством объектов',
        #                      'залог незавершенного незаконсервированного объекта',
        #                      'залог основных средств, неустановленного оборудования']
        self.file_id = file_id
        self.pledge_type_id = pledge_type_id
        self.exception_params = exception_params
        self.counter: list = []

    def count_deposit_items(self):
        start_row = 4
        self.df_list[1] = self.df_list[1].iloc[start_row:, :]
        it = 0
        for index, row in self.df_list[1].iterrows():
            if ((len(str(row[1])) < 2 and len(str(row[2])) < 2)
                    or (pd.isna(row[1])) or (pd.isna(row[2]))):
                self.df_list[1] = self.df_list[1].iloc[1:, :]
            elif index == 6:
                break
            else:
                break

        try:
            first_empty_row = self.df_list[1].index[self.df_list[1].iloc[:, 1].isnull()].tolist()[0]
            self.df_list[1] = self.df_list[1].iloc[:first_empty_row - start_row, :]
            return self.df_list[1].shape[0]
        except IndexError:
            return self.df_list[1].shape[0]

    # def start_point_1(self):
    #     if self.deposit_type.lower() in self.at_seven_row:
    #         if self.deposit_type.lower() == self.at_seven_row[2] \
    #                 and self.old_v:
    #             return 5
    #         elif self.deposit_type.lower() == self.at_seven_row[0] or self.deposit_type.lower() == self.at_seven_row[1]:
    #             return 5
    #     return 4
    #
    # def start_point_2(self):
    #     if self.old_v:
    #         return 5
    #     return 4

    def fillnan(self):
        self.df_list[0] = self.df_list[0].fillna(method='ffill')
        self.df_list[1] = self.df_list[1].fillna(method='ffill')

    def data_slice(self):
        try:
            start_row = 4
            self.df_list[0] = self.df_list[0].iloc[start_row:, :]
            self.df_list[0] = self.df_list[0].dropna(subset=self.df_list[0].columns[1:2])
            it = 0
            for index, row in self.df_list[0].iterrows():
                if len(str(row[1])) < 2 and len(str(row[2])) < 2:
                    self.df_list[0] = self.df_list[0].iloc[1:, :]

                it += 1
                if it == 2:
                    break

            self.df_list[0] = self.df_list[0].iloc[:self.count_deposit_items(), :]
            self.fillnan()
            self.df_list[0].reset_index(drop=True, inplace=True)
            self.df_list[1].reset_index(drop=True, inplace=True)

            self.df_list = self.processing()
        except IndexError:
            return None

        return self.df_list

    def processing(self):
        common_column_numbers, common_column_names, special_column_numbers, special_column_names = [None] * 4
        # общие
        if self.old_v:
            common_column_numbers = list(range(1, 17))

            # unnessasary: property_desc, liquidity_qlty, significance_qlty, burden_flg, assessed_val_accept

            common_column_names = ['property_desc', 'liquidity_qlty', 'significance_qlty', 'bank_ctrl',
                                   'conservation_lvl', 'physical_cond', 'burden_flg', 'prop_qltyctgr',
                                   'collateral_type', 'assessed_val_src', 'assessed_val_type', 'liquidity_lgd',
                                   'significance_lgd', 'assess_desc', 'assessor_accred', 'assessed_val_accept']
        else:
            common_column_numbers = list(range(1, 19))

            # unnessasary: property_desc, liquidity_qlty, significance_qlty, burden_flg, risk_prop_qltyctgr,
            # prop_qltyctgr_prev, assessed_val_accept

            common_column_names = ['property_desc', 'liquidity_qlty', 'significance_qlty', 'bank_ctrl',
                                   'conservation_lvl', 'physical_cond', 'burden_flg', 'risk_prop_qltyctgr',
                                   'prop_qltyctgr_prev', 'prop_qltyctgr', 'collateral_type', 'assessed_val_src',
                                   'assessed_val_type', 'liquidity_lgd', 'significance_lgd', 'assess_desc',
                                   'assessor_accred', 'assessed_val_accept']

        # Залог законсервированных незавершенных строительством объектов
        if self.deposit_type.lower() in settings.DEPOSIT_TYPES[0]:
            if self.old_v:
                special_column_numbers = list(range(1, 16))

                # unnessasary: state_perm_inf, spec_purpose
                special_column_names = ['property_desc', 'constr_address', 'commissioning_pl_dt', 'readiness_degree',
                                        'state_perm_inf', 'cadastral_num', 'area', 'lp_right',
                                        'spec_purpose', 'payment_rent', 'rent_term', 'cur_total_cost',
                                        'property_assessed_val_curry', 'collateral_disc_amt', 'collateral_val_curry']

            else:
                special_column_numbers = list(range(1, 17))

                # unnessasary: state_perm_inf, spec_purpose
                special_column_names = ['property_desc', 'constr_address', 'commissioning_pl_dt', 'readiness_degree',
                                        'state_perm_inf', 'cadastral_num', 'area', 'lp_right',
                                        'spec_purpose', 'payment_rent', 'rent_term', 'cur_total_cost',
                                        'property_assessed_val', 'collateral_disc_amt', 'collateral_val_amt',
                                        'collateral_val_curry']

        # Залог имущественных прав (требований) на выручку
        elif self.deposit_type.lower() in settings.DEPOSIT_TYPES[1]:
            if self.old_v:
                special_column_numbers = list(range(1, 14))

                # unnessasary: coop_dur, agmt_debt_amt, 6_m_receipts_amt, banks_pledged_inf, cv_curry
                special_column_names = ['prop_right_agmt', 'counterparty_name', 'agmt_term', 'coop_dur',
                                        'agmt_debt_amt', '6_m_receipts_amt', 'banks_pledged_inf', 'bank_name',
                                        'assessed_val', 'valuation_val_curry', 'collateral_disc_amt',
                                        'collateral_val_amt', 'cv_curry']
            else:
                special_column_numbers = list(range(1, 12))

                # unnessasary: coop_dur, 6_m_receipts_amt, banks_pledged_inf
                special_column_names = ['prop_right_agmt', 'counterparty_name', 'agmt_term', 'coop_dur',
                                        '6_m_receipts_amt', 'banks_pledged_inf', 'bank_name',
                                        'assessed_val', 'collateral_disc_amt', 'collateral_val_amt',
                                        'collateral_val_curry']

        # Залог имущественных прав (требований) на приобретаемое имущество
        elif self.deposit_type.lower() in settings.DEPOSIT_TYPES[2]:
            if self.old_v:
                special_column_numbers = list(range(1, 10))

                # unnessasary: cv_curry
                special_column_names = ['prop_right_agmt', 'counterparty_name', 'contracted_property',
                                        'property_val_w_vat_amt',
                                        'assessed_val', 'valuation_val_curry', 'collateral_disc_amt',
                                        'collateral_val_amt', 'cv_curry']
            else:
                special_column_numbers = list(range(1, 16))

                # unnessasary: pledged_right, agmt_terms_compl, agmt_prohibition, own_right_paid, encumbrances_inf
                special_column_names = ['prop_right_agmt', 'counterparty_name', 'contracted_property',
                                        'pledged_right', 'agmt_terms_compl', 'agmt_prohibition', 'own_right_paid',
                                        'delivery_pl_dt', 'property_val_w_vat_amt', 'pledge_ressuance_trm',
                                        'encumbrances_inf', 'assessed_val', 'collateral_disc_amt',
                                        'collateral_val_amt', 'collateral_val_curry']

        # Залог имущественных прав (требований) по договору лизинга
        elif self.deposit_type.lower() in settings.DEPOSIT_TYPES[3]:
            if self.old_v:
                special_column_numbers = list(range(1, 12))

                # unnessasary: agmt_contr_debt_amt, agmt_npl, cv_curry
                special_column_names = ['agmt_leasing', 'counterparty_name', 'agmt_term', 'agmt_contr_debt_amt',
                                        'agmt_npl', 'bank_name', 'assessed_val', 'valuation_val_curry',
                                        'collateral_disc_amt', 'collateral_val_amt', 'cv_curry']
            else:
                special_column_numbers = list(range(1, 11))

                # unnessasary: agmt_contr_debt_amt, agmt_npl
                special_column_names = ['agmt_leasing', 'counterparty_name', 'agmt_term', 'agmt_contr_debt_amt',
                                        'agmt_npl', 'bank_name', 'assessed_val', 'collateral_disc_amt',
                                        'collateral_val_amt', 'collateral_val_curry']

        # Залог незавершенного незаконсервированного объекта
        elif self.deposit_type.lower() in settings.DEPOSIT_TYPES[4]:
            if self.old_v:
                special_column_numbers = list(range(1, 15))

                # unnessasary: state_perm_inf
                special_column_names = ['property_desc', 'constr_address', 'commissioning_pl_dt', 'readiness_degree',
                                        'state_perm_inf', 'cadastral_num', 'area', 'lp_right',
                                        'payment_rent', 'rent_term', 'cur_total_cost',
                                        'property_assessed_val_curry', 'collateral_disc_amt', 'collateral_val_curry']
            else:
                special_column_numbers = list(range(1, 16))

                # unnessasary: state_perm_inf
                special_column_names = ['property_desc', 'constr_address', 'commissioning_pl_dt', 'readiness_degree',
                                        'state_perm_inf', 'cadastral_num', 'area', 'lp_right',
                                        'payment_rent', 'rent_term', 'cur_total_cost', 'property_assessed_val',
                                        'collateral_disc_amt', 'collateral_val_amt', 'collateral_val_curry']

        # Залог основных средств, неустановленного оборудования
        elif self.deposit_type.lower() in settings.DEPOSIT_TYPES[5]:
            if self.old_v:
                special_column_numbers = list(range(1, 12))

                # unnessasary: model, cv_curry
                special_column_names = ['property_desc', 'model', 'manufacture_dt', 'serial_num',
                                        'account_invent_num', 'assessed_val', 'valuation_val_curry', 'property_loc',
                                        'collateral_disc_amt', 'collateral_val_amt', 'cv_curry']
            else:
                special_column_numbers = list(range(1, 14))

                # unnessasary: payment_inf, customs_duties, encumbrances_inf
                special_column_names = ['property_desc', 'model', 'manufacture_dt', 'serial_num',
                                        'account_invent_num', 'payment_inf', 'customs_duties', 'encumbrances_inf',
                                        'assessed_val', 'collateral_disc_amt', 'collateral_val_amt',
                                        'collateral_val_curry', 'property_loc']

        # Залог товаров в обороте
        elif self.deposit_type.lower() in settings.DEPOSIT_TYPES[6]:
            if self.old_v:
                special_column_numbers = list(range(1, 12))

                # unnessasary: cv_curry, cur_remaining_goods, prev_2_remaining_goods, prev_remaining_goods
                special_column_names = ['generic_terms', 'shelf_life', 'property_loc', 'prev_2_remaining_goods',
                                        'prev_remaining_goods', 'cur_remaining_goods', 'assessed_val',
                                        'valuation_val_curry ', 'collateral_disc_amt', 'collateral_val_amt', 'cv_curry']

            else:
                special_column_numbers = list(range(1, 8))

                # unnessasary: None
                special_column_names = ['generic_terms', 'shelf_life_90', 'assessed_val', 'collateral_disc_amt',
                                        'collateral_val_amt', 'collateral_val_curry', 'product_address']

        # Залог транспортных средств, колесных тракторов, прицепов к ним и самоходных машин
        elif self.deposit_type.lower() in settings.DEPOSIT_TYPES[7]:
            if self.old_v:
                special_column_numbers = list(range(1, 14))

                # unnessasary: cv_curry
                special_column_names = ['property_desc', 'model', 'manufacture_dt', 'body_num',
                                        'body_num_avail', 'registr_num', 'invent_num',
                                        'assessed_val ', 'valuation_val_curry ', 'property_loc',
                                        'collateral_disc_amt', 'collateral_val_amt', 'cv_curry']

            else:
                special_column_numbers = list(range(1, 17))

                # unnessasary: tech_insp_dt, tech_insp_dt, tech_insp_dt, payment_inf
                special_column_names = ['property_desc_vechicle', 'model', 'manufacture_yr', 'vin_1_num',
                                        'vin_2_num', 'avail_registr_num', 'invent_num',
                                        'payment_inf ', 'customs_duties_vat ', 'encumbrances_inf',
                                        'tech_insp_dt', 'assessed_val', 'collateral_disc_amt',
                                        'collateral_val_amt', 'collateral_val_curry', 'property_loc']


        # Залог ценных бумаг
        elif self.deposit_type.lower() == settings.DEPOSIT_TYPES[8]:
            if self.old_v:
                special_column_numbers = list(range(1, 16))

                # unnessasary: cv_curry
                special_column_names = ['security_name', 'issuer', 'right_depository', 'issue_num',
                                        'registration_num', 'registration_dt', 'nominal', 'nom_curry ',
                                        'security_amt ', 'bonds_dep_trm', 'assessed_val', 'valuation_val_curry',
                                        'collateral_disc_amt', 'collateral_val_amt', 'cv_curry']

            else:
                special_column_numbers = list(range(1, 15))

                # unnessasary: cv_curry
                special_column_names = ['security_name', 'issuer', 'right_depository', 'issue_num',
                                        'registration_num', 'registration_dt', 'nominal', 'nom_curry ',
                                        'security_amt ', 'bonds_dep_trm', 'assessed_val',
                                        'collateral_disc_amt', 'collateral_val_amt', 'cv_curry']

        # Ипотека
        elif self.deposit_type.lower() == settings.DEPOSIT_TYPES[9]:
            if self.old_v:
                special_column_numbers = list(range(1, 25))

                # unnessasary: lp_collateral_val_curry, obj_collateral_val_curry
                # !:        if obj_assessed_val_curry == lp_assessed_val_curry:
                #                obj_lp_assessed_val = obj_assessed_val + lp_rent_assessed_val
                special_column_names = ['re_type', 'usrre_invent_num', 'usrre_name', 'usrre_purpose',
                                        'actual_usage', 'address', 'total_area', 'components',
                                        'lp_cadastral_num', 'lp_address', 'lp_area', 'lp_right',
                                        'payment_rent', 'rent_term', 'obj_assessed_val', 'obj_assessed_val_curry',
                                        'obj_collateral_disc_amt', 'obj_collateral_val_amt', 'obj_collateral_val_curry',
                                        'lp_rent_assessed_val', 'lp_assessed_val_curry', 'lp_collateral_disc_amt',
                                        'lp_rent_collateral_val_amt', 'lp_collateral_val_curry']

            else:
                special_column_numbers = list(range(1, 25))

                # unnessasary: encumbrances_inf
                # !:        if obj_assessed_val_curry == lp_assessed_val_curry:
                #                obj_lp_assessed_val = obj_assessed_val + lp_rent_assessed_val
                special_column_names = ['re_type', 'usrre_invent_num', 'usrre_name', 'usrre_purpose',
                                        'actual_usage', 'address', 'total_area', 'components',
                                        'compliance_param', 'lp_cadastral_num', 'lp_address', 'lp_area',
                                        'lp_right', 'payment_rent', 'rent_term', 'encumbrances_inf', 'obj_assessed_val',
                                        'obj_collateral_disc_amt', 'obj_collateral_val_amt', 'obj_ass_coll_val_curry',
                                        'lp_rent_assessed_val', 'lp_collateral_disc_amt', 'lp_rent_collateral_val_amt',
                                        'lp_ass_coll_val_curry']
        try:
            real_column_numbers = range(1, self.df_list[0].shape[1])
            if len(real_column_numbers) < len(special_column_numbers):
                self.counter = real_column_numbers
            else:
                self.counter = special_column_numbers

            self.df_list[0].rename(
                columns={self.df_list[0].columns[i]: special_column_names[i - 1] for i in self.counter},
                inplace=True)
        except IndexError as e:
            self.processing_failed += 1
            error_desc = "The number of expected attributes exceeds the number of attributes received / " \
                         "Количество ожидаемых атрибутов превышает количество полученных атрибутов"
            logger.error(msg=error_desc, extra={
                "system_message": e,
                "file_path": self.exception_params[0],
                "app_name": self.exception_params[1][0],
                "deposit_type": self.deposit_type,
                "year": self.exception_params[2]
            })
            return None
        try:
            self.df_list[1].rename(
                columns={self.df_list[1].columns[i]: common_column_names[i - 1] for i in common_column_numbers},
                inplace=True)
        except IndexError as e:
            self.processing_failed += 1
            error_desc = "The number of expected attributes exceeds the number of attributes received / " \
                         "Количество ожидаемых атрибутов превышает количество полученных атрибутов"
            logger.error(msg=error_desc, extra={
                "system_message": e,
                "file_path": self.exception_params[0],
                "app_name": self.exception_params[1][1],
                "deposit_type": self.deposit_type,
                "year": self.exception_params[2]
            })
            return None

        self.cut_dataframe(common_column_numbers[-1], special_column_numbers[-1])
        self.add_id()
        self.division()
        if not self.check_type(special_column_names):
            return None
        if self.deposit_type.lower() == settings.DEPOSIT_TYPES[9]:
            self.add_extra_attribute()
        self.change_disc_and_area_values()
        return self.df_list

    def change_disc_and_area_values(self):
        column_to_select = [col for col in self.df_list[0].columns if 'disc' in col]
        for column_name in column_to_select:
            self.df_list[0][column_name] = self.df_list[0][column_name].fillna(100)
            if not pd.api.types.is_float_dtype(self.df_list[0][column_name]):
                column = self.df_list[0][column_name]
                if not pd.api.types.is_integer_dtype(self.df_list[0][column_name]):
                    try:
                        column = column.str.replace('\"-\"', '-1.0')
                        column = column.str.replace('%', '')
                        column = column.str.replace('-', '-2.0')
                        column = column.str.replace(' ', '')
                        column = column.str.replace('*', '')
                        column = column.str.replace(',', '.')
                    except AttributeError as e:
                        pass

                try:
                    column = column.astype(float)
                    column = column.replace(-1, 100)
                    column = column.replace(-2, 100)
                    self.df_list[0][column_name] = column
                except ValueError as e:
                    self.df_list[0][column_name] = pd.to_numeric(self.df_list[0][column_name], errors="coerce")
                    self.df_list[0][column_name] = self.df_list[0][column_name].fillna(100)

                except TypeError as e:
                    self.df_list[0][column_name] = pd.to_numeric(self.df_list[0][column_name], errors="coerce")
                    self.df_list[0][column_name] = self.df_list[0][column_name].fillna(100)

        column_to_select = [col for col in self.df_list[0].columns if 'area' in col]
        for column_name in column_to_select:
            self.df_list[0][column_name] = self.df_list[0][column_name].fillna(0)
            if not pd.api.types.is_float_dtype(self.df_list[0][column_name]):
                column = self.df_list[0][column_name]
                if not pd.api.types.is_integer_dtype(self.df_list[0][column_name]):
                    try:
                        column = column.str.replace('га', '')
                        column = column.str.replace(' ', '')
                        column = column.str.replace('*', '')
                        column = column.str.replace(',', '.')
                        column = column.str.replace('\"-\"', '1.52323')
                        column = column.str.replace('-', '-2.0')
                    except AttributeError as e:
                        pass

                try:
                    column = column.astype(float)
                    column = column.replace(1.52323, 0)
                    column = column.replace(-2, 0)
                    self.df_list[0][column_name] = column
                except ValueError as e:
                    self.df_list[0][column_name] = pd.to_numeric(self.df_list[0][column_name], errors="coerce")
                    self.df_list[0][column_name] = self.df_list[0][column_name].fillna(0)

                except TypeError as e:
                    self.df_list[0][column_name] = pd.to_numeric(self.df_list[0][column_name], errors="coerce")
                    self.df_list[0][column_name] = self.df_list[0][column_name].fillna(0)


    def add_extra_attribute(self):
        try:
            if self.old_v:
                if 'obj_assessed_val_curry' not in self.df_list[0].columns:
                    self.df_list[0]['obj_assessed_val_curry'] = ''
                if 'lp_assessed_val_curry' not in self.df_list[0].columns:
                    self.df_list[0]['lp_assessed_val_curry'] = ''
                if 'obj_assessed_val' not in self.df_list[0].columns:
                    self.df_list[0]['obj_assessed_val'] = 0
                if 'lp_rent_assessed_val' not in self.df_list[0].columns:
                    self.df_list[0]['lp_rent_assessed_val'] = 0


                if self.df_list[0]['obj_assessed_val_curry'].equals(self.df_list[0]['lp_assessed_val_curry']):
                    self.df_list[0]['obj_lp_assessed_val'] = self.df_list[0]['obj_assessed_val'] + self.df_list[0][
                        'lp_rent_assessed_val']
                else:
                    self.df_list[0]['obj_lp_assessed_val'] = np.nan
            else:
                if 'obj_ass_coll_val_curry' not in self.df_list[0].columns:
                    self.df_list[0]['obj_ass_coll_val_curry'] = ''
                if 'lp_ass_coll_val_curry' not in self.df_list[0].columns:
                    self.df_list[0]['lp_ass_coll_val_curry'] = ''
                if 'obj_collateral_val_amt' not in self.df_list[0].columns:
                    self.df_list[0]['obj_collateral_val_amt'] = 0
                if 'lp_rent_collateral_val_amt' not in self.df_list[0].columns:
                    self.df_list[0]['lp_rent_collateral_val_amt'] = 0

                if self.df_list[0]['obj_ass_coll_val_curry'].equals(self.df_list[0]['lp_ass_coll_val_curry']):
                    self.df_list[0]['obj_lp_assessed_val'] = self.df_list[0]['obj_collateral_val_amt'] + \
                                                             self.df_list[0][
                                                                 'lp_rent_collateral_val_amt']
                else:
                    self.df_list[0]['obj_lp_assessed_val'] = np.nan

        except KeyError:
            pass


    def division(self):
        pattern_float = r'[-+]?\d+(\.\d+)?'
        pattern = r'(\d+(\.\d+)?)\s+(.+)'

        def extract_cost_currency(value):
            match = re.match(pattern, value)
            if match:
                cost = float(match.group(1))
                currency = match.group(3)
                return cost, currency
            else:
                return value, ''

        if self.deposit_type.lower() in settings.DEPOSIT_TYPES[0] or self.deposit_type.lower() in \
                settings.DEPOSIT_TYPES[4]:
            if self.df_list[0]['cur_total_cost'].notnull().any():
                try:
                    if self.df_list[0]['cur_total_cost'].str.contains(pattern).all():
                        self.df_list[0]['cur_total_cost'] = self.df_list[0]['cur_total_cost'].apply(
                            lambda x: re.search(pattern_float, x).group() if isinstance(x, str) else x)
                except AttributeError:
                    pass

            if self.old_v:
                if self.df_list[0]['property_assessed_val_curry'].notnull().any():
                    self.df_list[0].insert(3, 'property_assessed_val', '')
                    property_assessed_val_curry = self.df_list[0]['property_assessed_val_curry']

                    try:
                        if property_assessed_val_curry.str.contains(pattern).all():
                            self.df_list[0][['property_assessed_val', 'property_assessed_val_curry']] \
                                = self.df_list[0]['property_assessed_val_curry'].apply(
                                lambda x: pd.Series(extract_cost_currency(x)) if isinstance(x, str) else pd.Series(
                                    [x, '']))
                    except AttributeError:
                        pass

                if self.df_list[0]['collateral_val_curry'].notnull().any():
                    self.df_list[0].insert(3, 'collateral_val_amt', '')
                    collateral_val_curry = self.df_list[0]['collateral_val_curry']

                    try:
                        if collateral_val_curry.str.contains(pattern).all():
                            self.df_list[0][['collateral_val_amt', 'collateral_val_curry']] \
                                = self.df_list[0]['collateral_val_curry'].apply(
                                lambda x: pd.Series(extract_cost_currency(x)) if isinstance(x, str) else pd.Series(
                                    [x, '']))
                    except AttributeError:
                        pass



        elif self.deposit_type.lower() in settings.DEPOSIT_TYPES[2] and self.df_list[0][
            'property_val_w_vat_amt'].notnull().any():
            property_val_w_vat_amt = self.df_list[0]['property_val_w_vat_amt']
            try:
                if property_val_w_vat_amt.str.contains(pattern).all():
                    self.df_list[0]['property_val_w_vat_amt'] = self.df_list[0]['property_val_w_vat_amt'].apply(
                        lambda x: re.search(pattern_float, x).group() if isinstance(x, str) else x)
            except AttributeError:
                pass

    def check_type(self, columns: list) -> bool:
        for i in range(len(self.counter)):
            if columns[i] in settings.FLOAT_ATTRIBUTES:
                if not pd.api.types.is_float_dtype(self.df_list[0][columns[i]]):
                    column = self.df_list[0][columns[i]]
                    if not pd.api.types.is_integer_dtype(self.df_list[0][columns[i]]):
                        try:
                            column = column.str.replace('га', '')
                            column = column.str.replace(' ', '')
                            column = column.str.replace('_', '')
                            column = column.str.replace('*', '')
                            column = column.str.replace(',', '.')
                            column = column.str.replace('\"-\"', '1.01234')
                            column = column.str.replace('-', '-2.0')
                        except AttributeError as e:
                            self.check_type_failed += 1
                            description = f"The expected data type of the '{columns[i]}' " \
                                          f"column (float) does not match the received data type (datetime) / " \
                                          f"Ожидаемый тип данных столбца '{columns[i]}'" \
                                          f" (float) не соответствует полученному типу данных (datetime)"
                            logger.warning(description, extra={
                                'system_message': e,
                                'file_path': self.exception_params[0],
                                'app_name': self.exception_params[1][0],
                                'column_number': f"{i + 2}",
                                "deposit_type": self.deposit_type,
                                "year": self.exception_params[2]
                            })
                            return False

                    try:
                        column = column.astype(float)
                        column = column.replace(1.012345, np.nan)
                        column = column.replace(-2, np.nan)
                        self.df_list[0][columns[i]] = column
                    except ValueError as e:
                        self.check_type_failed += 1
                        description = f"The expected data value of the '{columns[i]}'" \
                                      f" column does not match the received data value / " \
                                      f"Ожидаемое значение данных столбца «{columns[i]}»" \
                                      f"не соответствует полученному значению данных."
                        logger.warning(description, extra={
                            'system_message': e,
                            'file_path': self.exception_params[0],
                            'app_name': self.exception_params[1][0],
                            "column_name": columns[i],
                            "column_number": f"{i + 2}",
                            "deposit_type": self.deposit_type,
                            "year": self.exception_params[2]
                        })
                        return False
                    except TypeError as e:
                        self.check_type_failed += 1
                        description = f"The expected data type of the '{columns[i]}' " \
                                      f"column does not match the received data type / " \
                                      f"Ожидаемый тип данных столбца «{columns[i]}»" \
                                      f" не соответствует полученному типу данных."
                        logger.warning(description, extra={
                            'system_message': e,
                            'file_path': self.exception_params[0],
                            'app_name': self.exception_params[1][0],
                            "column_name": columns[i],
                            "column_number": i + 2,
                            "deposit_type": self.deposit_type,
                            "year": self.exception_params[2]
                        })
                        return False
        return True

    def cut_dataframe(self, common_size: int, special_size: int):
        self.df_list[0] = self.df_list[0].iloc[:, 1:special_size + 1]
        self.df_list[1] = self.df_list[1].iloc[:, 1:common_size + 1]

    def add_id(self):
        self.df_list[0].insert(0, 'sb_id', np.nan)
        self.df_list[0].insert(0, 'pledge_type_id', self.pledge_type_id)
        self.df_list[0].insert(0, 'file_id', self.file_id)
        self.df_list[1].insert(0, 'sb_id', np.nan)
        self.df_list[1].insert(0, 'pledge_type_id', self.pledge_type_id)
        self.df_list[1].insert(0, 'file_id', self.file_id)

        self.df_list[1]['sb_id'] = self.df_list[0]['sb_id'] = self.df_list[0].apply(lambda row: hash_string(str(row)),
                                                                                    axis=1)
