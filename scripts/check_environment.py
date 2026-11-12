"""Run in an AoU cloud app; inspect dataset metadata without reading participants."""
import argparse
import os
import re


def dataset_id(value):
    if not re.fullmatch(r"[a-z][a-z0-9-]*\.[A-Za-z0-9_]+", value):
        raise argparse.ArgumentTypeError("Expected project.dataset")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=dataset_id, default=os.getenv("WORKSPACE_CDR"))
    parser.add_argument("--project", default=os.getenv("GOOGLE_CLOUD_PROJECT"))
    args = parser.parse_args()
    if not args.dataset or not args.project:
        parser.error("Provide --dataset project.dataset and --project workspace-billing-project")
    from google.cloud import bigquery

    client = bigquery.Client(project=args.project)
    dataset = client.get_dataset(args.dataset)
    names = {table.table_id for table in client.list_tables(dataset)}
    for name in ("person", "condition_occurrence", "concept", "observation"):
        print(f"{name}: {'available' if name in names else 'missing'}")
    print("Metadata access verified. No participant records queried.")


if __name__ == "__main__":
    main()
