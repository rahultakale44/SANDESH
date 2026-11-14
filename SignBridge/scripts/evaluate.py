"""Evaluate sentence translations against human references using BLEU and chrF."""
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--references", required=True, help="CSV with reference,prediction columns")
    args = parser.parse_args()
    df = pd.read_csv(args.references)
    required = {"reference", "prediction"}
    if not required.issubset(df.columns):
        raise SystemExit("CSV must contain columns: reference,prediction")
    refs = df["reference"].fillna("").astype(str).tolist()
    preds = df["prediction"].fillna("").astype(str).tolist()
    if not refs:
        raise SystemExit("No evaluation rows found.")
    try:
        import sacrebleu
        print("BLEU:", sacrebleu.corpus_bleu(preds, [refs]).score)
        print("chrF:", sacrebleu.corpus_chrf(preds, [refs]).score)
    except ImportError:
        print("Install sacrebleu to calculate BLEU and chrF: pip install sacrebleu")

if __name__ == "__main__":
    main()
