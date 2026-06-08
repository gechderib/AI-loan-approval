from pydantic import BaseModel
from enum import Enum


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
    Region: Region
    Gender: Gender

    age: AgeGroup
    
