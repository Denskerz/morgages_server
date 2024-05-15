from . import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional, Annotated

from ..database import intpk, str_1000, str_50, str_255, num_18_6, num_22_2, str_500, created_at, updated_at


class ConclusionOrm(Base):
    __tablename__ = "Conclusion"
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    file_id: Mapped[int]
    sb_id: Mapped[str_50]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


class CommonAttributesOrm(Base):
    __tablename__ = "CommonAttributes"
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    file_id: Mapped[int]
    sb_id: Mapped[str_50]
    property_desc_common: Mapped[Optional[str]]
    liquidity_qlty_common: Mapped[Optional[str]]
    significance_qlty_common: Mapped[Optional[str]]
    bank_ctrl_common: Mapped[str_255]
    conservation_lvl_common: Mapped[str_255]
    physical_condition_common: Mapped[Optional[str_255]]
    burden_flag_common: Mapped[Optional[str]]
    risk_prop_qltygr_common: Mapped[Optional[str_255]]
    prop_qltyctgr_common: Mapped[Optional[str_255]]
    prop_qltyctgr_prev_common: Mapped[Optional[str_255]]
    collateral_type_common: Mapped[Optional[str_255]]
    assessed_val_src_common: Mapped[Optional[str_255]]
    assessed_val_type_common: Mapped[Optional[str_255]]
    liquidity_lgd_common: Mapped[Optional[str_255]]
    significance_lgd_common: Mapped[Optional[str_255]]
    assess_desc_common: Mapped[Optional[str_255]]
    assessor_accred_common: Mapped[Optional[str_50]]
    assessed_val_accept_common: Mapped[Optional[str]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


# Залог законсервированных незавершенных строительством объектов
class PLMothaballedUnfinObjOrm(Base):
    __tablename__ = "PLMothaballedUnfinObj"
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    file_id: Mapped[int]
    sb_id: Mapped[str_50]
    property_desc: Mapped[Optional[str]]
    constr_address: Mapped[Optional[str_1000]]
    commissioning_pl_dt: Mapped[str_50]
    readiness_degree: Mapped[Optional[str_50]]
    state_perm_inf: Mapped[Optional[str]]
    cadastral_num: Mapped[Optional[str_255]]
    area: Mapped[Optional[num_18_6]]
    lp_right: Mapped[Optional[str_255]]
    spec_purpose: Mapped[Optional[str]]
    payment_rent: Mapped[Optional[str_255]]
    rent_term: Mapped[Optional[str_50]]
    cur_total_cost: Mapped[Optional[num_22_2]]
    property_assessed_val: Mapped[Optional[num_22_2]]
    property_assessed_val_curry: Mapped[Optional[str_50]]
    collateral_disc_amt: Mapped[Optional[num_22_2]]
    collateral_val_amt: Mapped[Optional[num_22_2]]
    collateral_val_curry: Mapped[Optional[str_50]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


# Залог имущественных прав (требований) на выручку
class PledgePRRightProceedsOrm(Base):
    __tablename__ = "PledgePRRightProceeds"
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    file_id: Mapped[int]
    sb_id: Mapped[str_50]
    prop_right_agmt: Mapped[Optional[str_255]]
    counterparty_name: Mapped[Optional[str_255]]
    agmt_term: Mapped[Optional[str_50]]
    coop_dur: Mapped[Optional[str]]
    agmt_debt_amt: Mapped[Optional[str]]
    b_m_receipts_amt: Mapped[Optional[str]]
    banks_pledged_inf: Mapped[Optional[str]]
    bank_name: Mapped[Optional[str_500]]
    assessed_val: Mapped[Optional[num_22_2]]
    collateral_disc_amt: Mapped[Optional[num_22_2]]
    collateral_val_curry: Mapped[Optional[str_50]]
    collateral_val_amt: Mapped[Optional[num_22_2]]
    cv_curry: Mapped[Optional[str_50]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


# Залог имущественных прав (требований) на приобретаемое имущество
class PledgePRRightAcquiredPROrm(Base):
    __tablename__ = "PledgePRRightAcquiredPR"
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    file_id: Mapped[int]
    sb_id: Mapped[str_50]
    prop_right_agmt: Mapped[Optional[str_255]]
    counterparty_name: Mapped[Optional[str_255]]
    contracted_property: Mapped[Optional[str]]
    pledged_right: Mapped[Optional[str]]
    property_val_w_vat_amt: Mapped[Optional[num_22_2]]
    assessed_val: Mapped[Optional[num_22_2]]
    agmt_terms_compl: Mapped[Optional[str]]
    agmt_prohibition: Mapped[Optional[str]]
    valuation_val_curry: Mapped[Optional[str_50]]
    own_right_paid: Mapped[Optional[str]]
    collateral_disc_amt: Mapped[Optional[num_22_2]]
    delivery_pl_dt: Mapped[Optional[str_50]]
    collateral_val_amt: Mapped[Optional[num_22_2]]
    cv_curry: Mapped[Optional[str_50]]
    pledge_ressuance_trm: Mapped[Optional[str_50]]
    encumbrances_inf: Mapped[Optional[str]]
    collateral_val_curry: Mapped[Optional[str_50]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


# Залог имущественных прав (требований) по договору лизинга
class PledgePrRightLeasingOrm(Base):
    __tablename__ = "PledgeSecurities"
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    file_id: Mapped[int]
    sb_id: Mapped[str_50]
    agmt_leasing: Mapped[Optional[str_255]]
    counterparty_name: Mapped[Optional[str_255]]
    agmt_term: Mapped[Optional[str_50]]
    agmt_contr_debt_amt: Mapped[Optional[str]]
    agmt_npl: Mapped[Optional[str]]
    bank_name: Mapped[Optional[str_500]]
    assessed_val: Mapped[Optional[num_22_2]]
    collateral_val_curry: Mapped[Optional[str_50]]
    collateral_disc_amt: Mapped[Optional[num_22_2]]
    collateral_val_amt: Mapped[Optional[num_22_2]]
    cv_curry: Mapped[Optional[str_50]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


# Залог незавершенного незаконсервированного объекта
class PledgeImperfectUnpreservedOBJOrm(Base):
    __tablename__ = "PledgeImperfectUnpreservedOBJ"
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    file_id: Mapped[int]
    sb_id: Mapped[str_50]
    property_desc: Mapped[str]
    constr_address: Mapped[Optional[str_1000]]
    commissioning_pl_dt: Mapped[Optional[str_50]]
    readiness_degree: Mapped[Optional[str_50]]
    state_perm_inf: Mapped[Optional[str]]
    cadastral_num: Mapped[Optional[str_255]]
    area: Mapped[Optional[num_18_6]]
    lp_right: Mapped[Optional[str_255]]
    payment_rent: Mapped[Optional[str_50]]
    rent_term: Mapped[Optional[num_22_2]]
    cur_total_cost: Mapped[Optional[num_22_2]]
    property_assessed_val: Mapped[Optional[num_22_2]]
    collateral_disc_amt: Mapped[Optional[num_22_2]]
    collateral_val_amt: Mapped[Optional[num_22_2]]
    collateral_val_curry: Mapped[Optional[str_50]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


# Залог основных средств, неустановленного оборудования
class PledgeFAInstalledEQOrm(Base):
    __tablename__ = "PledgeFAInstalledEQ"
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    file_id: Mapped[int]
    sb_id: Mapped[str_50]
    property_desc: Mapped[Optional[str]]
    model: Mapped[Optional[str_255]]
    manufacture_dt: Mapped[Optional[str_50]]
    serial_num: Mapped[Optional[str_255]]
    account_invent_num: Mapped[Optional[str_255]]
    payment_inf: Mapped[Optional[str]]
    assessed_val: Mapped[Optional[num_22_2]]
    customs_duties: Mapped[Optional[str]]
    valuation_val_curry: Mapped[Optional[str_50]]
    encumbrances_inf: Mapped[Optional[str]]
    property_loc: Mapped[Optional[str_1000]]
    collateral_disc_amt: Mapped[Optional[num_22_2]]
    collateral_val_amt: Mapped[Optional[num_22_2]]
    collateral_val_curry: Mapped[Optional[str_50]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


# Залог товаров в обороте
class PledgeGoodsOrm(Base):
    __tablename__ = "PledgeGoods"
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    # id: Mapped[intpk]
    file_id: Mapped[int]
    sb_id: Mapped[str_50]
    generic_terms: Mapped[Optional[str]]
    shelf_life: Mapped[Optional[str_50]]
    product_address: Mapped[Optional[str_1000]]
    assessed_val: Mapped[Optional[num_22_2]]
    prev_2_remaining_goods: Mapped[Optional[str]]
    collateral_disc_amt: Mapped[Optional[num_22_2]]
    prev_remaining_goods: Mapped[Optional[str]]
    collateral_val_amt: Mapped[Optional[num_22_2]]
    collateral_val_curry: Mapped[Optional[str_50]]
    cur_remaining_goods: Mapped[Optional[str]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


# Залог транспортных средств, колесных тракторов, прицепов к ним и самоходных машин
class PledgedVehiclesOrm(Base):
    __tablename__ = "PledgedVehicles"
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    file_id: Mapped[int]
    sb_id: Mapped[str_50]
    property_desc: Mapped[Optional[str]]
    model: Mapped[Optional[str_255]]
    manufacture_yr: Mapped[Optional[str_50]]
    vin_1_num: Mapped[Optional[str_255]]
    vin_2_num: Mapped[Optional[str_255]]
    registr_num: Mapped[Optional[str_255]]
    invent_num: Mapped[Optional[str_255]]
    assessed_val: Mapped[Optional[num_22_2]]
    payment_inf: Mapped[Optional[str]]
    collateral_val_curry: Mapped[Optional[str_50]]
    customs_duties_vat: Mapped[Optional[str]]
    product_address: Mapped[Optional[str_1000]]
    encumbrances_inf: Mapped[Optional[str]]
    tech_insp_dt: Mapped[Optional[str]]
    collateral_disc_amt: Mapped[Optional[num_22_2]]
    collateral_val_amt: Mapped[Optional[num_22_2]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


# Залог ценных бумаг
class PledgeSecuritiesOrm(Base):
    __tablename__ = "PledgeSecurities"
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    file_id: Mapped[int]
    sb_id: Mapped[str_50]
    security_name: Mapped[Optional[str]]
    issuer: Mapped[Optional[str_255]]
    right_depository: Mapped[Optional[str_255]]
    issue_num: Mapped[Optional[str_255]]
    registration_num: Mapped[Optional[str_255]]
    registration_dt: Mapped[Optional[str_50]]
    nominal: Mapped[Optional[num_22_2]]
    nom_curry: Mapped[Optional[str_50]]
    security_amt: Mapped[Optional[int]]
    bonds_dep_trm: Mapped[Optional[str_50]]
    assessed_val: Mapped[Optional[num_22_2]]
    collateral_val_curry: Mapped[Optional[str_50]]
    collateral_disc_amt: Mapped[Optional[num_22_2]]
    collateral_val_amt: Mapped[Optional[num_22_2]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]


# Ипотека
class MortgageOrm(Base):
    __tablename__ = "Mortgage"
    __table_args__ = {'extend_existing': True}

    id: Mapped[intpk]
    file_id: Mapped[int]
    sb_id: Mapped[str_50]
    re_type: Mapped[Optional[str]]
    usrre_invent_num: Mapped[Optional[str_255]]
    usrre_name: Mapped[Optional[str_500]]
    usrre_purpose: Mapped[Optional[str_500]]
    actual_usage: Mapped[Optional[str_255]]
    address: Mapped[Optional[str_1000]]
    total_area: Mapped[Optional[num_22_2]]
    components: Mapped[Optional[str]]
    lp_cadastral_num: Mapped[Optional[str_255]]
    lp_address: Mapped[Optional[str_1000]]
    lp_area: Mapped[Optional[num_18_6]]
    lp_right: Mapped[Optional[str_255]]
    payment_rent: Mapped[Optional[str_255]]
    rent_term: Mapped[Optional[str_50]]
    obj_assessed_val: Mapped[Optional[num_22_2]]
    obj_assessed_val_curry: Mapped[Optional[str_50]]
    obj_collateral_disc_amt: Mapped[Optional[num_22_2]]
    obj_collateral_val_amt: Mapped[Optional[num_22_2]]
    obj_collateral_val_curry: Mapped[Optional[str_50]]
    lp_rent_assessed_val: Mapped[Optional[num_22_2]]
    lp_assessed_val_curry: Mapped[Optional[str_50]]
    lp_collateral_disc_amt: Mapped[Optional[num_22_2]]
    lp_rent_collateral_val_amt: Mapped[Optional[num_22_2]]
    lp_collateral_val_curry: Mapped[Optional[str_50]]
    compliance_param: Mapped[Optional[str_255]]
    encumbrances_inf: Mapped[Optional[str]]
    obj_ass_coll_val_curry: Mapped[Optional[str_50]]
    lp_ass_coll_val_curry: Mapped[Optional[str_50]]
    createdAt: Mapped[created_at]
    updatedAt: Mapped[updated_at]
