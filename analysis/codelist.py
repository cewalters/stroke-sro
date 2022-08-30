from cohortextractor import codelist_from_csv

##############################################################################
# stroke codelists
##############################################################################
# stroke codelist
stroke_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-strk_cod.csv",
    system="snomed",
    column="code"
)

# transient ischaemic attack codelist
tia_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-tia_cod.csv",
    system="snomed",
    column="code"
)

# require ethniticy codelist https://www.opencodelists.org/codelist/opensafely/ethnicity-snomed-0removed/2e641f61/
ethnicity_codes = codelist_from_csv(
    "codelists/opensafely-ethnicity-snomed-0removed.csv",
    system="snomed",
    column="snomedcode",
    category_column="Grouping_6"
)

# systolic blood pressure - check this
systolic_bp_codes = codelist_from_csv(
    "codelists/opensafely-systolic-blood-pressure-qof.csv",
    system="snomed",
    column="code"
)

# diastolic blood pressure - check this, taken from hypertension qof
diastolic_bp_codes = codelist_from_csv(
    "codelists/user-milanwiedemann-diastolic-blood-pressure-qof.csv",
    system="snomed",
    column="code"
)
