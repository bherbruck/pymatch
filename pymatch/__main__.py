import argparse

from pymatch.core import *


parser = argparse.ArgumentParser()
parser.add_argument('--source', help='source file', required=True)
parser.add_argument('--compare', help='comparison file', required=True)
parser.add_argument('--output', help='output file', required=True)
parser.add_argument('--field', help='field to use', required=True)
parser.add_argument('--threshold', help='source file',
                    required=False, default=0.98)
parser.add_argument('--max_only', help='source file',
                    required=False, default=True)
args = parser.parse_args()


def main():
    print('Finding matches..', end='')
    matches = match_csv(args.source,
                        args.compare,
                        field_name=args.field,
                        threshold=float(args.threshold),
                        max_only=args.max_only)
    if len(matches) > 0:
        save_csv(args.output, matches)
        print(f'Saved to {args.output}')
    else:
        print('No matches found')


if __name__ == "__main__":
    main()
