from argparse import ArgumentParser
from dotenv.main import DotEnv
from pathlib import Path
import sys


def check_diff(file1, file2):
    example_keys = set(DotEnv(file1).dict().keys())
    current_keys = set(DotEnv(file2).dict().keys())
    return sorted(example_keys - current_keys), sorted(current_keys - example_keys)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Find diff in keys between two dotenvs. Extra keys are ok but missing keys will raise"
    )
    parser.add_argument("--gold", "-g", type=Path, default=Path(".env.example"), help="File you want to match")
    parser.add_argument("--current", "-c", type=Path, default=Path(".env"), help="File you have")
    parser.add_argument("-r", dest="should_raise", action="store_true", default=False, help="Whether to raise")
    args = parser.parse_args()

    gold_extra, current_extra = check_diff(args.gold, args.current)
    print(f"Extra in {str(args.gold)}: {gold_extra}" f", extra in {str(args.current)}: {current_extra}")
    if args.should_raise and len(gold_extra):
        sys.exit(1)
