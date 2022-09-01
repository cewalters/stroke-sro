from cohortextractor import codelist_from_csv

# Cluster name: STRK_COD
# Description: Stroke diagnosis codes
# SNOMED CT: ^999005531000230105
strk_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-strk_cod.csv",
    system="snomed",
    column="code",
)
# Cluster name: TIA_COD
# Description: Transient ischaemic attack (TIA) codes
# SNOMED CT: ^999005531000230105
tia_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-tia_cod.csv",
    system="snomed",
    column="code",
)
