#############################################################################################
# TO DO
############################################################################################
# AIM: investigate the rate of people on the stroke QOF register over time
#
# variables: sex, ethnicity, location (NHS region), IMD, carehome (binary?), 
#            learning disability (binary?), sicklecell anemia
# population age: Brian suggested 20+; I have been working with 18+ because adult


from cohortextractor import StudyDefinition, patients, Measure

# codelists in a separate file - read them in
from codelist import *


# do I need these dates here? How do they relate to what is in the project yaml?
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
    # defining sex
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.5, "F": 0.5}},
        }
    ),
    
    # define region - unsure how to find NHS region
    region=patients.registered_practice_as_of(
        date="index_date",
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and The Humber": 0.1,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East": 0.1,
                    "London": 0.2,
                    "South East": 0.1,
                    "South West": 0.1,
                },
            },
        }
    )

    eth=patients.with_these_clinical_events(
        ethnicity_codes,
        returning="category",
        find_last_match_in_period=True,
        include_date_of_match=False,
        return_expectations={
            "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
            "incidence": 0.75,
        },
    ),

    ethnicity=patients.categorised_as(
        {
            "Unknown": "DEFAULT",
            "White": "eth='1' ",
            "Mixed": "eth='2' ",
            "South Asian": "eth='3' ",
            "Black": "eth='4' ",
            "Other": "eth='5' ",
        },
        return_expectations={
            "category": {"ratios": {"White": 0.2, "Mixed": 0.2, "South Asian": 0.2, "Black": 0.2, "Other": 0.2}},
            "incidence": 0.4,
        },
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

    systolic_bp=patients.with_these_clinical_events(
            systolic_bp_codes,
            between=["index_date - 1 year", "index_date"],
            returning="numeric_value",
            find_last_match_in_period=True,
    )

    diastolic_bp=patients.with_these_clinical_events(
            diastolic_bp_codes,
            between=["index_date - 1 year", "index_date"],
            returning="numeric_value",
            find_last_match_in_period=True,
    )
# looking at STIA011
    bp=patients.satifying(
        """
        systolic_bp <= 150 AND
        diastolic_bp <= 90
        """
    )

    # example of defining a variable by combining other variables
    # stroke=patients.satisfying(
    #     """
    #     had_stroke AND
    #     age >= 40
    #     """
    # ),
)

measures=[
    Measure(
        id="stroke_frequency_by_sex",
        numerator="stroke_occurred",
        denominator="population",
        group_by=["sex"],
    ),    
    Measure(
        id="stroke_frequency_by_sex",
        numerator="stroke_occurred",
        denominator="population",
        group_by=["region"],
    ),
]