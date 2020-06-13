import requests
import math
from bs4 import BeautifulSoup


def main():
    issue_count_dict = {}
    total = 7082
    for i in range(1, (math.ceil(total/100) + 1)):
        content = requests.get('https://ngodarpan.gov.in/index.php/home/statewise_ngo/7079/19/{}?per_page=100'.format(i))
        issue_count_dict.update(parse_html(content))
    print(issue_count_dict)


def parse_html(content):
    issue_count_dict = {}
    soup = BeautifulSoup(content.text, "html.parser")
    table = soup.findAll('table', {'class': 'Tax'})[0].findAll('tbody')[0]
    rows = table.findAll('tr')
    
    for row in rows:
        issue_list = row.findAll('td')[4].string.split(',')
        for issue in issue_list:
            if issue not in issue_count_dict:
                issue_count_dict[issue] = 1
            else:
                issue_count_dict[issue] = issue_count_dict[issue] + 1
    return issue_count_dict


if __name__ == '__main__':
    main()
