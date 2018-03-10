import requests
import json
import csv
import os
import sys
import shutil
AUTHOR = 'torvalds'
REPO = 'linux'
Days = ['Sunday', 'Monday', 'Tuesday',
        'Wednesday', 'Thursday', 'Friday', 'Saturday']
BASE_URL = 'https://api.github.com'

if len(sys.argv) == 3:
    AUTHOR = sys.argv[1]
    REPO = sys.argv[2]

print('============The git repo is {} from {}============'.format(REPO, AUTHOR))

def create_folder():
    if os.path.isdir('data'):
        print("Data folder is existing, delete it now")
        shutil.rmtree('data')
    os.makedirs('data')
    print("New data folder is created.")


def weekly_commit():
    url = '/repos/{}/{}/stats/participation'.format(BASE_URL,
        AUTHOR, REPO)
    response = requests.get(url, verify=False).json()

    # write to json file
    with open('data/weekly_commit_52_week.json', 'w') as json_file:
        json.dump(response, json_file)

    # write to CSV file
    data = open('data/weekly_commit_52_week.csv', 'w', newline='')
    csvwriter = csv.writer(data)
    csvwriter.writerow(['week', 'all', 'owner'])
    for index in range(52):
        all = response['all']
        owner = response['owner']
        csvwriter.writerow([index, all[index], owner[index]])
    data.close()


def commit_per_hour():
    url = '/repos/{}/{}/stats/punch_card'.format(BASE_URL,
        AUTHOR, REPO)
    response = requests.get(url, verify=False).json()

    # write to json file
    with open('data/commit_per_hour.json', 'w') as json_file:
        json.dump(response, json_file)

    # write to CSV file
    data = open('data/commit_per_hour.csv', 'w', newline='')
    csvwriter = csv.writer(data)
    csvwriter.writerow(['day', 'hour', 'number'])
    for index in range(len(response)):
        item = response[index]
        csvwriter.writerow([Days[int(item[0])], item[1], item[2]])
    data.close()


def repos_of_author():
    url = '{}/users/{}/repos'.format(BASE_URL,AUTHOR)
    response = requests.get(url, verify=False).json()

    # write to json file
    with open('data/{}.json'.format(AUTHOR), 'w') as json_file:
        json.dump(response, json_file)

    # write to CSV file
    data = open('data/{}.csv'.format(AUTHOR), 'w', newline='')
    csvwriter = csv.writer(data)
    csvwriter.writerow(['id', 'name', 'size', 'language'])
    for index in range(len(response)):
        item = response[index]
        csvwriter.writerow(
            [item['id'], item['name'], item['size'], item['language']])
    data.close()

def language_by_author():
    url = '{}/users/{}/repos'.format(BASE_URL,AUTHOR)
    response = requests.get(url, verify=False).json()
    repos = []
    for index in range(len(response)):
        repos.append(response[index]['name'])

    data = open('data/languages.csv', 'w', newline='')
    csvwriter = csv.writer(data)
    csvwriter.writerow(['language', 'repo','bytes'])
    for current_repo in repos:
        url = '{}/repos/{}/{}/languages'.format(BASE_URL,AUTHOR,current_repo)
        response = requests.get(url, verify=False).json()
        data = open('data/languages.csv', 'a', newline='')
        for key, value in response.items():
            csvwriter.writerow([key, current_repo,value])
        data.close()


if __name__ == "__main__":
    create_folder()
    weekly_commit()
    commit_per_hour()
    repos_of_author()
    language_by_author()