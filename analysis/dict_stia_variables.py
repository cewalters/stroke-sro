
# Define common variables needed across indicators here
# See https://docs.opensafely.org/study-def-tricks/

import pandas as pd
from config import start_date, end_date
from cohortextractor import patients
from codelists_stia import (
    strk_codes,
    tia_codes,
    )

# Define dictionary of variables needed for
# Stroke/TIA register:  Register of patients with a Stroke or TIA diagnosis
stia_reg_variables = dict(
    # Date of the patient’s first stroke diagnosis up to and including
    # the achievement date.
    strt=patients.with_these_clinical_events(
        strk_codes,
        on_or_before="last_day_of_month(index_date)",
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "incidence": 0.01,
        },
    ),
    # Date of the patient’s first TIA diagnosis up to and including
    # the achievement date.
    tia=patients.with_these_clinical_events(
        tia_codes,
        on_or_before="last_day_of_month(index_date)",
        returning="binary_flag",
        find_last_match_in_period=True,
        include_date_of_match=True,
        date_format="YYYY-MM-DD",
        return_expectations={
            "incidence": 0.01,
        },
    ),
    # Stroke/TIA register: Register of patients with a Stroke or TIA diagnosis
    # TODO: Check section 3.2.4 Clinical data extraction criteria
    stia_reg=patients.satisfying(
        """
        # Stroke/TIA register: Register of patients with a Stroke
        # or TIA diagnosis
        strt OR
        tia
        """
    ),
)
