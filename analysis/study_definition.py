from cohortextractor import StudyDefinition, patients, Measure

# codelists in a separate file - read them in
from codelist import *

# why is there an error when this is inside StudyDefinition?
start_date = "2019-03-01"
end_date = "2020-03-01"


study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1988-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.1,
    },
    # have the achievement data as the index date? Final day in March
    index_date=start_date,

    population=patients.satisfying(
        """
        (age >= 18) AND
        gms_registration_status
        """
    ),

    # defining the age variable
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            # is this bit giving me all ages rather than 18+?
            "int": {"distribution": "population_ages"}
        }
    ),

    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.5, "F": 0.5}},
        }
    ),

    gms_registration_status=patients.satisfying(
        """
        registered AND
        NOT has_died
        """,
        registered=patients.registered_as_of(
            "last_day_of_year(index_date)",
            return_expectations={"incidence": 0.9},
        ),
        has_died=patients.died_from_any_cause(
            on_or_before="last_day_of_year(index_date)",
            returning="binary_flag",
        ),
    ),

# get the date of the first TIA event within the defined 1 year period up to and including the index (achievement) date
    tia_date_first=patients.with_these_clinical_events(
        tia_codes,
        between=["index_date - 1 year", "index_date"],
        returning="date",
        find_first_match_in_period=True,
        include_month=True,
        include_day=True,
        return_expectations={
            "date": {"earliest": "index_date - 1 year", "latest": "index_date"}},
    ),

# get the date of the first stroke event within the defined 1 year period up to and including the index (achievement) date
    stroke_occurred=patients.with_these_clinical_events(
        stroke_codes,
        between=["index_date - 1 year", "index_date"],
        returning="binary_flag",
        find_first_match_in_period=True,
        include_date_of_match = True,
        include_month=True,
        include_day=True,
        return_expectations={
            "date": {"earliest": "index_date - 1 year", "latest": "index_date"}},
    ),

    had_stroke=patients.with_these_clinical_events(
            stroke_codes,
            on_or_before="last_day_of_month(index_date)",
            returning='binary_flag',
            return_expectations={"incidence": 0.9}
    ),

    stroke=patients.satisfying(
        """
        had_stroke AND
        age >= 40
        """
    ),
)

measures=[
    Measure(
        id="stroke_rate",
        numerator="stroke",
        denominator="population",
        group_by=["population"],
    ),
    Measure(
        id="stroke_frequency2",
        numerator="stroke_occurred",
        denominator="population",
        group_by=["sex"],
    ),
]


# # Create default measures
# measures = [
#     Measure(
#         id="ast_reg_population_rate",
#         numerator="asthma",
#         denominator="population",
#         group_by=["population"],
#         small_number_suppression=True,
#     ),
#     Measure(
#         id="ast_reg_practice_rate",
#         numerator="asthma",
#         denominator="population",
#         group_by=["practice"],
#         small_number_suppression=True,
#     ),
#     Measure(
#         id="ast_reg_age_rate",
#         numerator="asthma",
#         denominator="population",
#         group_by=["age_band"],
#         small_number_suppression=True,
#     ),
#     Measure(
#         id="ast_reg_sex_rate",
#         numerator="asthma",
#         denominator="population",
#         group_by=["sex"],
#         small_number_suppression=True,
#     ),
#     Measure(
#         id="ast_reg_imd_rate",
#         numerator="asthma",
#         denominator="population",
#         group_by=["imd"],
#         small_number_suppression=True,
#     ),
#     Measure(
#         id="ast_reg_region_rate",
#         numerator="asthma",
#         denominator="population",
#         group_by=["region"],
#         small_number_suppression=True,
#     ),
#     Measure(
#         id="ast_reg_ethnicity_rate",
#         numerator="asthma",
#         denominator="population",
#         group_by=["ethnicity"],
#         small_number_suppression=True,
#     ),
#     Measure(
#         id="ast_reg_learning_disability_rate",
#         numerator="asthma",
#         denominator="population",
#         group_by=["learning_disability"],
#         small_number_suppression=True,
#     ),
#     Measure(
#         id="ast_reg_care_home_rate",
#         numerator="asthma",
#         denominator="population",
#         group_by=["care_home"],
#         small_number_suppression=True,
#     ),
# ]
