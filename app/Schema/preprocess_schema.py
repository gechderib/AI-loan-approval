from pydantic import BaseModel

from enum import Enum

import pandas as pd

class LoanLimit(str, Enum):
    cf = "cf"
    ncf = "ncf"


class ApprovalInAdvance(str, Enum):
    nopre = "nopre"
    pre = "pre"


class CreditWorthiness(str, Enum):
    l1 = "l1"
    l2 = "l2"


class OpenCredit(str, Enum):
    nopc = "nopc"
    opc = "opc"


class BusinessOrCommercial(str, Enum):
    nob_c = "nob/c"
    b_c = "b/c"


class NegAmortization(str, Enum):
    not_neg = "not_neg"
    neg_amm = "neg_amm"


class InterestOnly(str, Enum):
    not_int = "not_int"
    int_only = "int_only"


class LumpSumPayment(str, Enum):
    not_lpsm = "not_lpsm"
    lpsm = "lpsm"


class ConstructionType(str, Enum):
    sb = "sb"
    mh = "mh"


class SecuredBy(str, Enum):
    home = "home"
    land = "land"


class CoApplicantCreditType(str, Enum):
    CIB = "CIB"
    EXP = "EXP"


class SubmissionOfApplication(str, Enum):
    to_inst = "to_inst"
    not_inst = "not_inst"


class SecurityType(str, Enum):
    direct = "direct"
    indirect = "Indriect"


class LoanType(str, Enum):
    type1 = "type1"
    type2 = "type2"
    type3 = "type3"


class LoanPurpose(str, Enum):
    p1 = "p1"
    p2 = "p2"
    p3 = "p3"
    p4 = "p4"


class OccupancyType(str, Enum):
    pr = "pr"
    sr = "sr"
    ir = "ir"


class CreditType(str, Enum):
    CIB = "CIB"
    CRIF = "CRIF"
    EQUI = "EQUI"
    EXP = "EXP"


class Region(str, Enum):
    north = "North"
    north_east = "North-East"
    central = "central"
    south = "south"


class Gender(str, Enum):
    male = "Male"
    female = "Female"
    joint = "Joint"
    not_available = "Sex Not Available"


class AgeGroup(str, Enum):
    under_25 = "<25"
    age_25_34 = "25-34"
    age_35_44 = "35-44"
    age_45_54 = "45-54"
    age_55_64 = "55-64"
    age_65_74 = "65-74"
    over_74 = ">74"
    
    
class LoanPredictionResponse(BaseModel):
    prediction: int
    approval_probability: float


class LoanPredictionRequest(BaseModel):
    loan_limit: LoanLimit
    approv_in_adv: ApprovalInAdvance
    Credit_Worthiness: CreditWorthiness
    open_credit: OpenCredit
    business_or_commercial: BusinessOrCommercial

    loan_amount: float
    term: float
    property_value: float
    income: float
    Credit_Score: int
    LTV: float
    dtir1: float

    Neg_ammortization: NegAmortization
    interest_only: InterestOnly
    lump_sum_payment: LumpSumPayment

    construction_type: ConstructionType
    Secured_by: SecuredBy

    co_applicant_credit_type: CoApplicantCreditType
    submission_of_application: SubmissionOfApplication
    Security_Type: SecurityType

    loan_type: LoanType
    loan_purpose: LoanPurpose
    occupancy_type: OccupancyType
    credit_type: CreditType
    Region: Region
    Gender: Gender

    age: AgeGroup
    



def preprocess_prediction_request(payload):
    data = payload.model_dump()

    loan_limit_map = {
        "cf": 1,
        "ncf": 0,
    }

    approv_in_adv_map = {
        "nopre": 0,
        "pre": 1,
    }

    credit_worthiness_map = {
        "l1": 1,
        "l2": 0,
    }

    open_credit_map = {
        "nopc": 0,
        "opc": 1,
    }

    business_or_commercial_map = {
        "nob/c": 0,
        "b/c": 1,
    }

    neg_amortization_map = {
        "not_neg": 0,
        "neg_amm": 1,
    }

    interest_only_map = {
        "not_int": 0,
        "int_only": 1,
    }

    lump_sum_payment_map = {
        "not_lpsm": 0,
        "lpsm": 1,
    }

    construction_type_map = {
        "sb": 0,
        "mh": 1,
    }

    secured_by_map = {
        "home": 0,
        "land": 1,
    }

    co_applicant_credit_type_map = {
        "CIB": 0,
        "EXP": 1,
    }

    submission_of_application_map = {
        "to_inst": 1,
        "not_inst": 0,
    }

    security_type_map = {
        "direct": 0,
        "Indriect": 1,
    }

    age_map = {
        "<25": 0,
        "25-34": 1,
        "35-44": 2,
        "45-54": 3,
        "55-64": 4,
        "65-74": 5,
        ">74": 6,
    }

    data["loan_limit"] = loan_limit_map[data["loan_limit"]]
    data["approv_in_adv"] = approv_in_adv_map[data["approv_in_adv"]]
    data["Credit_Worthiness"] = credit_worthiness_map[data["Credit_Worthiness"]]
    data["open_credit"] = open_credit_map[data["open_credit"]]
    data["business_or_commercial"] = business_or_commercial_map[data["business_or_commercial"]]

    data["Neg_ammortization"] = neg_amortization_map[data["Neg_ammortization"]]
    data["interest_only"] = interest_only_map[data["interest_only"]]
    data["lump_sum_payment"] = lump_sum_payment_map[data["lump_sum_payment"]]

    data["construction_type"] = construction_type_map[data["construction_type"]]
    data["Secured_by"] = secured_by_map[data["Secured_by"]]

    data["co-applicant_credit_type"] = co_applicant_credit_type_map[data["co_applicant_credit_type"]]
    data["submission_of_application"] = submission_of_application_map[data["submission_of_application"]]
    data["Security_Type"] = security_type_map[data["Security_Type"]]

    data["age"] = age_map[data["age"]]

    df = pd.DataFrame([data])

    one_hot_columns = [
        "loan_type",
        "loan_purpose",
        "occupancy_type",
        "credit_type",
        "Region",
        "Gender",
    ]

    df = pd.get_dummies(
        df,
        columns=one_hot_columns,
        dtype=int,
    )

    return df