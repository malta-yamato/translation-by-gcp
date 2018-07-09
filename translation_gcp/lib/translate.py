# Imports the Google Cloud client library
import os
from datetime import datetime
import xml.etree.ElementTree as ElementTree
import csv

from google.cloud import translate


class GoogleTranslation:

    def __init__(self, base='Python is the No1.', target_language='en', list_unit=100, limit_req=100,
                 limit_chars=1000000, unit_price=20 / 1000000):
        self.client = translate.Client()
        self.base = base
        self.target_language = target_language
        self.result = None
        self.__list_unit = list_unit
        self.__limit_req = limit_req
        self.__limit_chars = limit_chars
        self.__cnt_req = 0
        self.__cnt_chars = 0
        self.__unit_price = unit_price

    def translate(self, arg=None, target_language=None, preserve=True):
        if arg is None:
            arg = self.base
        if target_language is None:
            target_language = self.target_language
        #
        type_arg = type(arg)
        ret = None
        res = None
        if type_arg is str:
            if self.__check_req(arg):
                translation = self.client.translate(arg, target_language=target_language)
                ret = translation['translatedText']
                res = {arg: ret}
            else:
                return None
        elif type_arg is list:
            ret = self.__translate(arg, target_language)
            res = ret
        else:
            raise ValueError('please give str or list.')

        if preserve and res is not None:
            self.result = res
        return ret

    def __translate(self, arg, target_language):
        if type(arg) is not list:
            raise ValueError('accept only list')
        list_unit = self.__list_unit
        dt = {}
        arg_len = len(arg)
        lp = arg_len // list_unit
        for i in range(lp):
            sub = arg[i * list_unit: (i + 1) * list_unit]
            # print(sub)
            dt.update(self.__translate_unit(sub, target_language))
        else:
            rem = arg[lp * list_unit:]
            if len(rem) > 0:
                # print(rem)
                dt.update(self.__translate_unit(rem, target_language))
        return dt

    def __translate_unit(self, arg, target_language):
        if self.__check_req(arg):
            translation = self.client.translate(arg, target_language=target_language)
            return {x['input']: x['translatedText'] for x in translation}
        else:
            return {}

    def __check_req(self, arg):

        # check count of chars
        arg_chars = 0
        if type(arg) is str:
            arg_chars = len(arg)
        elif type(arg) is list:
            for elm in arg:
                arg_chars += len(elm)
        else:
            raise ValueError('please give str or list.')
        if self.__cnt_chars + arg_chars <= self.__limit_chars:
            self.__cnt_chars += arg_chars
        else:
            print('reached the limit of the number of characters.')
            return False

        # check count of request
        if self.__cnt_req < self.__limit_req:
            self.__cnt_req = self.__cnt_req + 1
            print('requesting translation API ({}, {}) at {}'.format(self.__cnt_req, self.__cnt_chars,
                                                                     datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
            return True
        else:
            print('reached the limit of the number of requests.')
            return False

    def estimate(self, unit_price=None):
        if unit_price is not None:
            return self.__cnt_chars * unit_price
        else:
            return self.__cnt_chars * self.__unit_price

    def write_csv(self, file, dic=None, encoding='utf-8'):
        if self.result is None:
            print('error: no results to write')
            return
        with open(file, mode='w', encoding=encoding) as f:
            w = csv.writer(f, lineterminator='\n')
            res = self.result
            if dic is None:
                for key in res:
                    w.writerow([key, res[key]])
            else:
                for key in res:
                    w.writerow([key, dic[res[key]]])


class XmlTranslation:

    def __init__(self, client, xml_location, xml_tag):
        # check arguments
        if not isinstance(client, GoogleTranslation):
            raise ValueError('client must be instance of GoogleTranslation')
        if xml_location is None or xml_tag is None:
            raise ValueError('give proper xml_location and xml_tag')
        # set field
        self.__client = client
        self.__xml_location = xml_location
        self.__xml_tag = xml_tag
        # gather items to translate
        tree = ElementTree.parse(xml_location)
        root = tree.getroot()
        items = []
        for elm in root.iter(xml_tag):
            text = elm.text
            if text is not None:
                items.append(text)
        self.__items = items
        self.__translated = None

    def translate(self, target_language='en'):
        self.__client.target_language = target_language
        self.__translated = self.__client.translate(self.__items)

    def change_translate(self, key, value):
        translated = self.__translated
        if translated is None:
            raise ValueError('xml not translated yet')
        if key not in translated:
            raise ValueError('key not found: {}'.format(key))
        translated[key] = value

    def write_xml(self, file, encoding='utf-8', xml_declaration=None, cmp_file=None, cmp_lang=None):
        client = self.__client
        translated = self.__translated
        tree = ElementTree.parse(self.__xml_location)
        root = tree.getroot()
        tr_items = []
        # write replaced xml
        for elm in root.iter(self.__xml_tag):
            text = elm.text
            if text is None:
                continue
            tr = translated[text]
            if tr is not None:
                elm.text = tr
                tr_items.append(tr)
            else:
                print('Error: translation not found: {}'.format(text))
        tree.write(file, encoding=encoding, xml_declaration=xml_declaration)
        # make comparison file
        if cmp_file is not None:
            if cmp_lang is not None:
                client.target_language = cmp_lang
                cmp_dt = client.translate(tr_items, preserve=False)
                client.write_csv(cmp_file, cmp_dt)
            else:
                client.write_csv(cmp_file)


class TextTranslation:

    def __init__(self, client, text_location, encoding='utf-8'):
        # check arguments
        if not isinstance(client, GoogleTranslation):
            raise ValueError('client must be instance of GoogleTranslation')
        if text_location is None:
            raise ValueError('give proper text_location')
        # set field
        self.__client = client
        self.__text_location = text_location
        # load text file
        lines = []
        with open(text_location, mode='r', encoding=encoding) as f:
            for line in f:
                lines.append(line.strip('\r\n'))
        self.__lines = lines
        self.__translated = None

    def translate(self, target_language='en'):
        client = self.__client
        client.target_language = target_language
        self.__translated = []
        for line in self.__lines:
            self.__translated.append(client.translate(line).strip('\r\n'))

    def write_text(self, file, encoding='utf-8', linesep=None, cmp_file=None, cmp_lang=None):
        translated = self.__translated
        if translated is None:
            raise ValueError('you need to call translate function beforehand.')
        client = self.__client
        # write translated text
        sep = os.linesep if linesep is None else linesep
        with open(file, mode='w', encoding=encoding) as f:
            for line in translated:
                f.write(line + sep)
        # make comparison file
        if cmp_file is not None and cmp_lang is not None:
            client.target_language = cmp_lang
            cmp_lines = []
            for line in translated:
                cmp_lines.append(client.translate(line, preserve=False))
            with open(cmp_file, mode='w', encoding=encoding) as f:
                for line in cmp_lines:
                    f.write(line + sep)
