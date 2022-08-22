from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

stroke_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-strk_cod.csv", system="snomed", column="code"
)

tia_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-tia_cod.csv", system="snomed", column="code"
)

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1988-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.1,
    },

    index_date = "2019-01-01",

    population = patients.satisfying(
        """
        (age >= 18) AND
        gms_registration_status
        """ 
        ),

# defining the age variable
    age = patients.age_as_of(
        "index_date",
    return_expectations={
        "rate" : "universal",
        "int" : {"distribution" : "population_ages"} # is this bit giving me all ages rather than 18+?  
    }
    ),

    sex = patients.sex(
        return_expectations={
        "rate": "universal",
        "category": {"ratios": {"M": 0.5, "F": 0.5}},
    }
    ),

    gms_registration_status=patients.satisfying(
        """
        registered AND NOT 
        has_died
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


) 