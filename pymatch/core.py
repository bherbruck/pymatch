import csv
import json

from strsimpy.jaro_winkler import JaroWinkler


COMPARE_MODE = ['csv', 'json', 'string']
METHOD = JaroWinkler()
SPLITTERS = ','
EXCLUSIONS = '_- '
REPLACEMENTS = {
    '0': 'Oo'
}
THRESHOLD = 0.98


def clean_string(string,
                 splitters=SPLITTERS,
                 exclusions=EXCLUSIONS,
                 replacements=REPLACEMENTS):
    s = string
    for splitter in splitters:
        s = s.split(splitter)[0]
    for exclusion in exclusions:
        s = s.replace(exclusion, '')
    for new, olds in replacements.items():
        for old in olds:
            s = s.replace(old, new)
    s = s.lower()
    s = s.strip()
    return s


def compare_string(s1, s2, method=METHOD, clean=True):
    if clean:
        s1 = clean_string(s1)
        s2 = clean_string(s2)
    similarity = method.similarity(s1, s2)
    return similarity


def open_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def save_csv(path, data):
    with open(path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def save_file(path, text):
    with open(path, 'w') as file:
        file.write(text)


def match_csv(csv1, csv2, field_name, threshold=THRESHOLD, max_only=True):
    dict1 = open_csv(csv1)
    dict2 = open_csv(csv2)
    return match_dict(dict1, dict2, field_name, threshold, max_only=max_only)


def match_dict(dict1, dict2, field_name, threshold=THRESHOLD, max_only=True):
    d1 = [row[field_name] for row in dict1]
    d2 = [row[field_name] for row in dict2]
    matches = match_simple(d1, d2, field_name, threshold, max_only=max_only)
    return matches


def match_simple(dict1, dict2, field_name, threshold=THRESHOLD, max_only=True):
    matches = []
    for row1 in dict1:
        top = {}
        for row2 in dict2:
            similarity = compare_string(row1, row2)
            if similarity >= threshold:
                top[row2] = similarity
        if len(top) > 0:
            for key, value in top.items():
                print(f'Matching: {row1} == {key}',
                      end='                                         ')
                print(end='\r')
                if max_only:
                    key = max(top, default=None)
                matches.append({f'{field_name}1': row1,
                                f'{field_name}2': key,
                                'similarity': value})
                if max_only:
                    continue
    print(f'{len(matches)} matches found                                                          ')
    return matches


def match_full(dict1, dict2, field_name, threshold=THRESHOLD):
    """dict, not csv serializable
    """
    matches = [{f'{field_name}': row1,
                'matches': [{f'{field_name}': row2,
                             'similarity': compare_string(row1, row2)}
                            for row2 in dict2
                            if compare_string(row1, row2) >= threshold]}
               for row1 in dict1]
    return matches

def match_list(source_list, match_list, threshold=THRESHOLD):
    matches = {s: {m: t
                   for m in match_list
                   if (t := compare_string(s, m)) >= threshold}
               for s in source_list}
    return matches