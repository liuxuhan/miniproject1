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

print(len(sys.argv))
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
    url = 'https://api.github.com/repos/{}/{}/stats/participation'.format(
        AUTHOR, REPO)
    response = requests.get(url, verify=False).json()

    # write to json file
    with open('data/weekly_commit_52_week.txt', 'w') as json_file:
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
    url = 'https://api.github.com/repos/{}/{}/stats/punch_card'.format(
        AUTHOR, REPO)
    response = requests.get(url, verify=False).json()

    # write to json file
    with open('data/commit_per_hour.txt', 'w') as json_file:
        json.dump(response, json_file)

    # write to CSV file
    data = open('data/commit_per_hour.csv', 'w', newline='')
    csvwriter = csv.writer(data)
    csvwriter.writerow(['day', 'hour', 'number'])
    for index in range(len(response)):
        item = response[index]
        csvwriter.writerow([Days[int(item[0])], item[1], item[2]])
    data.close()


def repos_of_auther():
    url = 'https://api.github.com/users/{}/repos'.format(AUTHOR)
    response = requests.get(url, verify=False).json()

    # write to json file
    with open('data/{}.txt'.format(AUTHOR), 'w') as json_file:
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


if __name__ == "__main__":
    create_folder()
    weekly_commit()
    commit_per_hour()
    repos_of_auther()
