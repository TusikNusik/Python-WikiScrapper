import argparse
from wiki_controller import WikiController

link = "https://bulbapedia.bulbagarden.net/wiki"

def prepare_parsers():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--summary', type=str)
    group.add_argument('--table', type=str)
    group.add_argument('--count-words', type=str)
    group.add_argument('--analyze-relative-word-frequency', action="store_true")
    group.add_argument('--auto-count-words', type=str)

    parser.add_argument('--number', type=int)
    parser.add_argument('--first-row-is-header', action="store_true")
    parser.add_argument('--mode', type=str)
    parser.add_argument('--count', type=int)
    parser.add_argument('--chart', type=str)
    parser.add_argument('--depth', type=int)
    parser.add_argument('--wait', type=int)

    return parser

if __name__ == "__main__":
    parser = prepare_parsers()

    args = parser.parse_args()
    controller = WikiController(link)

    if args.summary:
        controller.summary(args.summary)
    elif args.table:
        controller.table(args.table, args.number, args.first_row_is_header)
    elif args.count_words:
        controller.count_words(args.count_words)
    elif args.analyze_relative_word_frequency:
        controller.analyze_relative_word_frequency(args.mode, args.count, args.chart)
    else:
        controller.auto_count_words(args.auto_count_words, args.depth, args.wait)