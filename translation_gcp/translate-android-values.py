from translation_gcp.lib.translate import GoogleTranslation
from translation_gcp.lib.translate import XmlTranslation

from pathlib import Path

# target_languages = ['zh-CN', 'zh-TW', 'hi', 'es', 'fr', 'ar', 'ru', 'pt', 'bn', 'de', 'ja', 'ko']
target_languages = ['zh-CN', 'es']

xml_location = 'data/input/values-en'
xml_object = {'strings.xml': 'string', 'arrays.xml': 'item'}

output_folder = 'data/output-test'
check_language = 'en'

input_dir = Path(xml_location)
if not input_dir.exists() or input_dir.is_file():
    print('input not found: {}'.format(input_dir))

# Google Translate API
client = GoogleTranslation(unit_price=20 / 1000000)

for child in input_dir.iterdir():
    # check file name
    xml_name = child.name
    if xml_name not in xml_object:
        print('{} will not be translated'.format(xml_name))
        continue
    print('{}'.format(child))

    # XML translation
    xml_trans = XmlTranslation(client, child, xml_object[xml_name])

    # Translate
    for target in target_languages:
        # translate items
        xml_trans.translate(target)
        # new xml file
        parent = Path(output_folder, 'values-' + target)
        if not parent.exists():
            parent.mkdir(parents=True)
        file = Path(parent, xml_name)
        # comparison file
        parent2 = Path(output_folder, 'check')
        if not parent2.exists():
            parent2.mkdir(parents=True)
        file2 = Path(parent2, xml_name + '---' + target + '.csv')
        # write xml
        xml_trans.write_xml(file, encoding='utf-8', xml_declaration=True, cmp_file=file2, cmp_lang=check_language)
        # xml_trans.write_xml(file, encoding='utf-8', xml_declaration=True, cmp_file=file2)

print('Translation has been completed. The estimated cost is ${}'.format(client.estimate()))
