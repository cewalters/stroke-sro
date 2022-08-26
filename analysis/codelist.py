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
