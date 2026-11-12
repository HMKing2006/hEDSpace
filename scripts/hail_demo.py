import hail as hl

# Initialize Hail if it isn't already initialized
hl.init()

# Paths inside the secure All of Us Workbench
COHORT_CSV = (
    "gs://heds-patient-data-wb-spotless-pecan-6923/"
    "20261112_024205_244832236_data_person-000000000000.csv.gz"
)
VDS_PATH = (
    "gs://vwb-aou-datasets-controlled/"
    "v9/wgs/short_read/snpindel/vds/hail.vds"
)

# Load participant IDs exported from Data Explorer
cohort = hl.import_table(COHORT_CSV, delimiter=",")

# Hail VDS samples are keyed by research ID as a string
samples = cohort.key_by(
    s=hl.str(cohort.person_id)
).select()

# Load the full WGS variant dataset
vds = hl.vds.read_vds(VDS_PATH)

# Select only members of your cohort
vds = hl.vds.filter_samples(vds, samples)

# Start with a small region on chromosome 22
region = hl.parse_locus_interval(
    "chr22:20000000-20100000",
    reference_genome="GRCh38"
)

vds = hl.vds.filter_intervals(
    vds,
    [region],
    split_reference_blocks=True
)

# Examine variants in this region
variants = vds.variant_data
variants.rows().show(5)
