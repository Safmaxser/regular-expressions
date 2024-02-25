import csv
import re


def loading_csv(path):
    with open(path, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        list_contacts = list(rows)
    return list_contacts


def phone_correct(phone):
    result = phone
    pattern = re.compile(r'(\+7|8)\s?\(?(\d{3})\)?[-\s]?(\d{3})[-\s]?(\d{2})'
                         r'[-\s]?(\d{2})(\s\(?доб.\s)?(\d+)?')
    sent = pattern.match(phone)
    if sent is not None:
        result = (f'+7({sent.group(2)}){sent.group(3)}-{sent.group(4)}-'
                  f'{sent.group(5)}')
        if sent.group(7) is not None:
            result += f' доб.{sent.group(7)}'
    return result


def list_comparison(list1, list2):
    new_list = []
    for item1, item2 in zip(list1, list2):
        if item1 != '':
            new_list.append(item1)
        else:
            new_list.append(item2)
    return new_list


def contacts_correct(contacts):
    contacts_dict = {}
    for contact in contacts:
        list_full_name = contact[0].split()
        list_full_name.extend(contact[1].split())
        (list_full_name.
         extend(contact[2].split()))
        list_full_name.append('')
        key_dict = ' '.join(list_full_name[:2])
        current_contact = (list_full_name[:3] + contact[3:5] +
                           [phone_correct(contact[5])] + contact[6:])
        search_contact = contacts_dict.get(key_dict)
        if search_contact is None:
            contacts_dict[key_dict] = current_contact
        else:
            contacts_dict[key_dict] = list_comparison(search_contact,
                                                      current_contact)
    return list(contacts_dict.values())


def save_csv(path, list_contacts):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(list_contacts)


if __name__ == '__main__':
    contacts_list = loading_csv('phonebook_raw.csv')
    contacts_new = contacts_correct(contacts_list)
    save_csv('phonebook.csv', contacts_new)
