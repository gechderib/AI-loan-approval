from fastapi import FastAPI, Form
from app.model.predict import predict
from app.Schema.preprocess_schema import (
    LoanPredictionRequest,
    LoanPredictionResponse,
    LoanLimit, ApprovalInAdvance, CreditWorthiness, BusinessOrCommercial, NegAmortization, InterestOnly, LumpSumPayment, CoApplicantCreditType, SubmissionOfApplication, LoanPurpose, 
    LoanType, OccupancyType, RegionEnum, GenderEnum, AgeGroup
)
app = FastAPI(
    title="Loan Approval AI rr",
    version="0.1.0",
    openapi_version="3.0.3"
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.post("/predict", response_model=LoanPredictionResponse)
# def predict_loan(req: LoanPredictionRequest):
#     return predict(req)


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