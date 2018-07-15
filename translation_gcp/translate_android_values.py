from translation_gcp.args import parse_general_args
from translation_gcp.lib.translate import GoogleTranslation
from translation_gcp.lib.translate import XmlTranslation
from pathlib import Path


def main():
    # parse arguments
    input_dir, output_dir, target_languages, check_language = parse_general_args()

    # xml objects
    xml_objects = {'strings.xml': 'string', 'arrays.xml': 'item'}

    # unit price
    unit_price = 20 / 1000000

    #
    # Google Translate API
    #
    client = GoogleTranslation(unit_price=unit_price)

    for child in input_dir.iterdir():
        # check file name
        xml_name = child.name
        if xml_name not in xml_objects:
            print('{} will not be translated'.format(xml_name))
            continue
        print('{}'.format(child))

        # XML translation
        xml_trans = XmlTranslation(client, child, xml_objects[xml_name])

        # Translate
        for target in target_languages:
            # translate items
            xml_trans.translate(target)
            # new xml file
            spl = target.split('-')
            parent = Path(output_dir, 'values-' + spl[0] + '-r' + spl[1]) if len(spl) == 2 \
                else Path(output_dir, 'values-' + target)
            if not parent.exists():
                parent.mkdir(parents=True)
            file = Path(parent, xml_name)
            # comparison file
            parent2 = Path(output_dir, 'check')
            if not parent2.exists():
                parent2.mkdir(parents=True)
            file2 = Path(parent2, xml_name + '---' + target + '.csv')
            # write xml
            xml_trans.write_xml(file, encoding='utf-8', xml_declaration=True, cmp_file=file2, cmp_lang=check_language)

    print('Translation has been completed. The estimated cost is ${}'.format(client.estimate()))


if __name__ == '__main__':
    main()
