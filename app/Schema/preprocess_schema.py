from pydantic import BaseModel, Field
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


class CoApplicantCreditType(str, Enum):
    CIB = "CIB"
    EXP = "EXP"


class SubmissionOfApplication(str, Enum):
    to_inst = "to_inst"
    not_inst = "not_inst"


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


class RegionEnum(str, Enum):
    north = "North"
    north_east = "North-East"
    central = "central"
    south = "south"


class GenderEnum(str, Enum):
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
    loan_limit: LoanLimit = LoanLimit.cf
    approv_in_adv: ApprovalInAdvance = ApprovalInAdvance.nopre
    Credit_Worthiness: CreditWorthiness = CreditWorthiness.l1
    business_or_commercial: BusinessOrCommercial = BusinessOrCommercial.nob_c

    loan_amount: float = Field(default=100000.0, gt=0)
    term: float = Field(default=360.0, gt=0)
    property_value: float = Field(default=150000.0, gt=0)
    income: float = Field(default=60000.0, gt=0)
    Credit_Score: int = Field(default=700, ge=300, le=900)
    LTV: float = Field(default=80.0, ge=0, le=1000)
    dtir1: float = Field(default=35.0, ge=0, le=100)

    Neg_ammortization: NegAmortization = NegAmortization.not_neg
    interest_only: InterestOnly = InterestOnly.not_int
    lump_sum_payment: LumpSumPayment = LumpSumPayment.not_lpsm

    co_applicant_credit_type: CoApplicantCreditType = CoApplicantCreditType.CIB
    submission_of_application: SubmissionOfApplication = SubmissionOfApplication.to_inst

    loan_type: LoanType = LoanType.type1
    loan_purpose: LoanPurpose = LoanPurpose.p1
    occupancy_type: OccupancyType = OccupancyType.pr
    Region: RegionEnum = RegionEnum.north
    Gender: GenderEnum = GenderEnum.male

    age: AgeGroup = AgeGroup.age_35_44
    


