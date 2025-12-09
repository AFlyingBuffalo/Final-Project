import pandas as pd
import argparse
import re


def clean_string_value(val):
    #Clean up whitespace inside a string cell
    if isinstance(val, str):
        val = val.strip()
        val = re.sub(r"[ \t]+", " ", val)
        return val
    return val


def clean_and_transform_data(input_path, output_path, pretty=None):
    #Clean CSV data, remove excess whitespace, remove blank rows, and save cleaned CSV

    try:
        df = pd.read_csv(input_path, sep=None, engine="python")
    except FileNotFoundError:
        print("File not found.")
    # handle pd.errors.ParserError
    except pd.errors.ParserError as e:
        print(f"Parser error: {e}")

    # Cleaning the column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(r"[ \t]+", "_", regex=True)
        .str.lower()
    )

    # Calling function to clear whitespace inside a cell
    df = df.map(clean_string_value)

    # removing blank rows
    df = df.replace(r'^\s*$', pd.NA, regex=True)
    df = df.dropna(how="all")                      

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing values
    df = df.fillna("")

    # Save CSV
    df.to_csv(output_path, index=False)
    print(f"Cleaned CSV saved to: {output_path}")
# Optional portion to output a cleaned up txt with the contents of the file in a nice looking table
    if pretty:
        col_widths = {
            col: max(df[col].astype(str).map(len).max(), len(col))
            for col in df.columns
        }
        #creating headers and separators for the text output
        header = " | ".join(col.center(col_widths[col]) for col in df.columns)
        separator = "-+-".join("-" * col_widths[col] for col in df.columns)
        #creating the rows
        rows = []
        for _, row in df.iterrows():
            row_str = " | ".join(str(row[col]).center(col_widths[col]) for col in df.columns)
            rows.append(row_str)
        #putting it all together
        pretty_table = "\n".join([header, separator] + rows)

        with open(pretty, "w", encoding="utf-8") as f:
            f.write(pretty_table)

        print(f"Centered table saved to: {pretty}")

    return df


def main():
    parser = argparse.ArgumentParser(description="Clean CSV spacing and formatting.")
    parser.add_argument("input_file", help="Path to input CSV/TSV file.")
    parser.add_argument("output_file", help="Where to save cleaned CSV.")
    parser.add_argument(
        "--pretty",
        help="Optional path to save a centered table (e.g., output.txt)."
    )

    args = parser.parse_args()
    clean_and_transform_data(args.input_file, args.output_file, args.pretty)


if __name__ == "__main__":
    main()
