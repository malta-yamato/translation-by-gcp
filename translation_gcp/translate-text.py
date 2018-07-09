from translation_gcp.lib.translate import GoogleTranslation
from translation_gcp.lib.translate import TextTranslation
from pathlib import Path

# target_languages = ['zh-CN', 'zh-TW', 'hi', 'es', 'fr', 'ar', 'ru', 'pt', 'bn', 'de', 'ja', 'ko']
target_languages = ['zh-CN', 'es']

text_location = 'data/input/example.txt'
text_name = Path(text_location).name

output_folder = 'data/output-test'
check_language = 'ja'

# Google Translate API
client = GoogleTranslation(unit_price=20 / 1000000)

# text translation
text_trans = TextTranslation(client, text_location)

# Translate
for target in target_languages:
    # translate items
    text_trans.translate(target)
    # new text file
    parent = Path(output_folder, 'text-' + target)
    if not parent.exists():
        parent.mkdir(parents=True)
    file = Path(parent, text_name)
    # comparison file
    parent2 = Path(output_folder, 'check')
    if not parent2.exists():
        parent2.mkdir(parents=True)
    file2 = Path(parent2, text_name + '---' + target + '.txt')
    # write xml
    text_trans.write_text(file, encoding='utf-8', linesep='\n', cmp_file=file2, cmp_lang=check_language)

print('Translation has been completed. The estimated cost is ${}'.format(client.estimate()))
