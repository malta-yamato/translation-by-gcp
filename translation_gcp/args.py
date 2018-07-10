import argparse
import os
import sys
from pathlib import Path


def parse_general_args():
    # parse arguments
    parser = argparse.ArgumentParser(description='translation by GCP')
    parser.add_argument('input', help='specify location you want to translate')
    parser.add_argument('--output', nargs='?', default='output-translation', const='output-translation',
                        help='specify the directory to store results')
    parser.add_argument('--langs', nargs='+', default=None, help='select target languages')
    parser.add_argument('--check', help='specify the language for checking translation results')
    args = parser.parse_args()

    # input
    input_loc = Path(args.input)
    if not input_loc.exists():
        raise ValueError('input directory not found')

    # output
    output_dir = Path(args.output)
    if output_dir.exists():
        if output_dir.is_dir():
            while True:
                choice = input('{} already exists. Do you want to override it? [y/n] : '.format(output_dir)).lower()
                if choice == 'y':
                    break
                elif choice == 'n':
                    sys.exit()
        else:
            raise ValueError('output directory {} is already used as other type file.'.format(output_dir))

    # langs
    target_languages = []
    arg_langs = args.langs
    if arg_langs is None:
        env_langs = os.environ['TRANSLATION_BY_GCP_LANGS']
        if env_langs is None:
            target_languages = ['en']
        else:
            for elm in env_langs.split(os.pathsep):
                if elm:
                    target_languages.append(elm)
    else:
        target_languages = arg_langs
    print(target_languages)

    # check
    check_language = args.check

    return input_loc, output_dir, target_languages, check_language,
