from translation_gcp.args import parse_general_args
from translation_gcp.lib.translate import GoogleTranslation
from translation_gcp.lib.translate import TextTranslation
from pathlib import Path


def main():
    # parse arguments
    input_file, output_dir, target_languages, check_language = parse_general_args()

    # unit price
    unit_price = 20 / 1000000

    #
    # Google Translate API
    #
    client = GoogleTranslation(unit_price=unit_price)

    # text translation
    text_name = Path(input_file).name
    text_trans = TextTranslation(client, input_file)

    # Translate
    for target in target_languages:
        # translate items
        text_trans.translate(target)
        # new text file
        parent = Path(output_dir, 'text-' + target)
        if not parent.exists():
            parent.mkdir(parents=True)
        file = Path(parent, text_name)
        # comparison file
        parent2 = Path(output_dir, 'check')
        if not parent2.exists():
            parent2.mkdir(parents=True)
        file2 = Path(parent2, text_name + '---' + target + '.txt')
        # write xml
        text_trans.write_text(file, encoding='utf-8', linesep='\n', cmp_file=file2, cmp_lang=check_language)

    print('Translation has been completed. The estimated cost is ${}'.format(client.estimate()))


if __name__ == '__main__':
    main()
