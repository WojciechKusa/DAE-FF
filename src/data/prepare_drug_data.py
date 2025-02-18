import copy

import pandas as pd
from Bio import Entrez
from Bio.Entrez import efetch
from tqdm import tqdm

Entrez.email = "Your.Name@example.org"


def prepare_drug_datasets(
    input_file="../../data/raw/drug/epc-ir.clean.tsv",
    out_folder="../../data/processed/",
):
    df = pd.read_csv(
        input_file,
        sep="\t",
        names=[
            "Drug review topic",
            "EndNote ID",
            "PubMed ID",
            "Abstract Triage Status",
            "Article Triage Status",
        ],
    )

    for review in df["Drug review topic"].unique().tolist():
        print(review)
        outfile = f"{out_folder}/{review.strip()}.tsv"

        sample_df = copy.copy(df[df["Drug review topic"] == review])

        sample_df["labels"] = 0
        sample_df.loc[sample_df["Article Triage Status"] == "I", "labels"] = 1

        sample_df["abstracts"] = ""

        for pubmed_id in tqdm(sample_df["PubMed ID"].tolist()):
            try:
                handle = efetch(
                    db="pubmed", id=pubmed_id, retmode="text", rettype="abstract"
                )
                sample_df.loc[
                    sample_df["PubMed ID"] == pubmed_id, "abstracts"
                ] = handle.read()

            except Exception as E:
                print(E)
                print(pubmed_id)

                sample_df.loc[
                    sample_df["PubMed ID"] == pubmed_id, "abstracts"
                ] = "empty"

        sample_df.to_csv(outfile, sep="\t", index=False)


if __name__ == "__main__":
    prepare_drug_datasets()
