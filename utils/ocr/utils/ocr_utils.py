from __future__ import print_function


def filter_text(text, names_dict):
    text = [each for each in text if each.isalpha() or each == ' ']
    text = ''.join(text).strip()
    text = text if names_dict.get(text) else None

    return text


def get_names(file_name):
    """
    Creates allowed words list:
    :param file_name: name with new line
    :return:
    """
    names_dict = dict()
    with open(file_name, 'r', encoding='utf-8') as file:
        for item in file.readlines():
            for each in item.strip().split(' '):
                if len(each) > 2:
                    names_dict.update({each.upper(): 1})
    return names_dict
