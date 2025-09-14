from pathlib import Path
import argparse, config, generator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="%(prog)s <path>")
    parser.add_argument("path", type=Path, help="The location of the \"template\" and \"appunti\" folders.")
    args = parser.parse_args()

    path = Path(args.path)

    config.init(path)
    generator.generate(path)
