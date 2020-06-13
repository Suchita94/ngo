import requests
import math
import csv
from bs4 import BeautifulSoup


def main():
    link_dict = get_all_links()
    state_count_dict = {}
    for state in link_dict:
        issue_count_dict = {}
        link = link_dict[state]['link']
        total = link_dict[state]['total']
        max_page = (math.ceil(int(total)/100) + 1)
        for i in range(1, max_page):
            content = requests.get(link.format(i))
            print(link.format(i))
            issue_count_dict.update(parse_html(content))
        state_count_dict[state] = issue_count_dict
    print(state_count_dict)
    with open('dict.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in state_count_dict.items():
            writer.writerow([key, value])


def get_all_links():
    link_dict = {}
    content = requests.get('https://ngodarpan.gov.in/index.php/home/statewise')
    soup = BeautifulSoup(content.text, "html.parser")
    links = soup.findAll('a', {'class': 'bluelink11px'})
    for link in links:
        key = link.text.split('\xa0')[0]
        total = link.text.split('\xa0')[1].replace('(', '').replace(')', '')
        href = link.get('href')
        href = href.split('/')
        href.pop()
        href = '/'.join(href) + '/{}?per_page=100'
        link_dict[key] = {'link': href, 'total': total}
    return link_dict



def parse_html(content):
    issue_count_dict = {}
    soup = BeautifulSoup(content.text, "html.parser")
    table = soup.findAll('table', {'class': 'Tax'})[0].findAll('tbody')[0]
    rows = table.findAll('tr')
    
    for row in rows:
        # print(row)
        issue_list = row.findAll('td')[4].string.split(',')
        for issue in issue_list:
            if issue not in issue_count_dict:
                issue_count_dict[issue] = 1
            else:
                issue_count_dict[issue] = issue_count_dict[issue] + 1
    return issue_count_dict


if __name__ == '__main__':
    main()
