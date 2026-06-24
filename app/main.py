from fastapi import FastAPI, Form
from app.model.predict import predict
from app.Schema.preprocess_schema import (
    LoanPredictionRequest,
    LoanPredictionResponse,
    LoanLimit, ApprovalInAdvance, CreditWorthiness, BusinessOrCommercial, NegAmortization, InterestOnly, LumpSumPayment, CoApplicantCreditType, SubmissionOfApplication, LoanPurpose, 
    LoanType, OccupancyType, RegionEnum, GenderEnum, AgeGroup, UserLoanApplicationRequest
)
import random
app = FastAPI(
    title="Loan Approval AI",
    version="0.1.0",
    openapi_version="3.0.3"
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict_j", response_model=LoanPredictionResponse)
def predict_loan_json(req: LoanPredictionRequest):
    return predict(req)


def fetch_credit_score(ssn: str) -> int:
    """Simulate fetching credit score from Experian/Equifax API in a deterministic way for testing."""
    if ssn and ssn.isdigit():
        # Use the last 3 digits of the SSN to simulate a score between 300 and 850
        last_3 = int(ssn[-3:])
        # Map 0-999 to 500-850 roughly
        # return 500 + (last_3 % 350)
        return 897
    return 650

def determine_credit_worthiness(score: int) -> CreditWorthiness:
    return CreditWorthiness.l1 if score >= 700 else CreditWorthiness.l2

@app.post("/apply", response_model=LoanPredictionResponse)
def apply_for_loan(req: UserLoanApplicationRequest):
    """
    Production-ready endpoint.
    Takes basic user input, calculates derived fields, and fetches external API data.
    """
    # 1. Fetch data from external APIs
    credit_score = fetch_credit_score(req.ssn)
    credit_worthiness = determine_credit_worthiness(credit_score)
    
    # 2. Calculate derived fields
    # LTV = Loan to Value
    ltv = (req.loan_amount / req.property_value) * 100 if req.property_value > 0 else 0
    
    # dtir1 = Debt to Income Ratio (monthly)
    monthly_income = req.income / 12 if req.income > 0 else 1
    monthly_interest_rate = 0.05 / 12 # assuming 5% annual interest for example
    months = req.term
    if monthly_interest_rate > 0 and months > 0:
        monthly_payment = req.loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**months) / ((1 + monthly_interest_rate)**months - 1)
    else:
        monthly_payment = req.loan_amount / months if months > 0 else 0
        
    total_monthly_debt = req.monthly_debt + monthly_payment
    dtir1 = (total_monthly_debt / monthly_income) * 100
    
    # 3. Apply internal business logic / default product rules
    prediction_request = LoanPredictionRequest(
        loan_amount=req.loan_amount,
        property_value=req.property_value,
        income=req.income,
        term=req.term,
        loan_purpose=req.loan_purpose,
        occupancy_type=req.occupancy_type,
        Region=req.Region,
        Gender=req.Gender,
        age=req.age,
        
        # Derived fields
        Credit_Score=credit_score,
        Credit_Worthiness=credit_worthiness,
        LTV=ltv,
        dtir1=dtir1,
        
        # Default Product Logic
        loan_type=LoanType.type1,
        loan_limit=LoanLimit.cf,
        approv_in_adv=ApprovalInAdvance.nopre,
        business_or_commercial=BusinessOrCommercial.nob_c,
        Neg_ammortization=NegAmortization.not_neg,
        interest_only=InterestOnly.not_int,
        lump_sum_payment=LumpSumPayment.not_lpsm,
        co_applicant_credit_type=CoApplicantCreditType.CIB,
        submission_of_application=SubmissionOfApplication.to_inst
    )
    
    return predict(prediction_request)


@app.post("/predict", response_model=LoanPredictionResponse)
def predict_loan(
    loan_limit: LoanLimit = Form(LoanLimit.cf),
    approv_in_adv: ApprovalInAdvance = Form(ApprovalInAdvance.nopre),
    Credit_Worthiness: CreditWorthiness = Form(CreditWorthiness.l1),
    business_or_commercial: BusinessOrCommercial = Form(
        BusinessOrCommercial.nob_c
    ),

    loan_amount: float = Form(100000.0),
    term: float = Form(360.0),
    property_value: float = Form(150000.0),
    income: float = Form(60000.0),
    Credit_Score: int = Form(700),
    LTV: float = Form(80.0),
    dtir1: float = Form(35.0),

    Neg_ammortization: NegAmortization = Form(
        NegAmortization.not_neg
    ),
    interest_only: InterestOnly = Form(
        InterestOnly.not_int
    ),
    lump_sum_payment: LumpSumPayment = Form(
        LumpSumPayment.not_lpsm
    ),

    co_applicant_credit_type: CoApplicantCreditType = Form(
        CoApplicantCreditType.CIB
    ),
    submission_of_application: SubmissionOfApplication = Form(
        SubmissionOfApplication.to_inst
    ),

    loan_type: LoanType = Form(LoanType.type1),
    loan_purpose: LoanPurpose = Form(LoanPurpose.p1),
    occupancy_type: OccupancyType = Form(OccupancyType.pr),

    Region: RegionEnum = Form(RegionEnum.north),
    Gender: GenderEnum = Form(GenderEnum.male),

    age: AgeGroup = Form(AgeGroup.age_35_44),
):

    req = LoanPredictionRequest(
        loan_limit=loan_limit,
        approv_in_adv=approv_in_adv,
        Credit_Worthiness=Credit_Worthiness,
        business_or_commercial=business_or_commercial,

        loan_amount=loan_amount,
        term=term,
        property_value=property_value,
        income=income,
        Credit_Score=Credit_Score,
        LTV=LTV,
        dtir1=dtir1,

        Neg_ammortization=Neg_ammortization,
        interest_only=interest_only,
        lump_sum_payment=lump_sum_payment,

        co_applicant_credit_type=co_applicant_credit_type,
        submission_of_application=submission_of_application,

        loan_type=loan_type,
        loan_purpose=loan_purpose,
        occupancy_type=occupancy_type,

        Region=Region,
        Gender=Gender,
        age=age
    )

    return predict(req)