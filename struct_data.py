import json
import numpy as np
import csv


def main():
    rows = []
    issues = []
    with open ('dict.csv', 'r', encoding='utf-8') as f:
        rows = f.read().splitlines()
    for i in range (0, len(rows)):
        if i == 0:
            continue
        row_dict = extract_dict(rows[i])
        for key in row_dict.keys():
            if key not in issues:
                issues.append(key)
    headers = []
    headers.append('State')
    headers.extend(issues)
    csv_rows = []
    for i in range (0, len(rows)):
        if i == 0:
            continue
        new_row = []
        state = rows[i].split(',')[0]
        new_row.append(state)
        issue_list = np.zeros(len(issues))
        row_dict = extract_dict(rows[i])
        for key in row_dict.keys():
            idx = issues.index(key)
            val = row_dict[key]
            issue_list[idx] = val
        new_row.extend(issue_list)
        csv_rows.append(new_row)
    with open('structured_dat.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        for row in csv_rows:
            writer.writerow(row)


def extract_dict(row):
    dict_str = '{' + row.split(',"{')[1]
    dict_str = dict_str.replace("\'", '"')
    dict_str = dict_str.replace('""', '"')
    dict_str = dict_str.replace('}"', '}')
    dict_str = dict_str.replace('"s', "'s")
    return json.loads(dict_str)


if __name__ == '__main__':
    main()