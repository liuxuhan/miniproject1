import requests
import json
import csv
AUTHOR = 'torvalds'
REPO = 'linux'


def weekly_commit():
    url = 'https://api.github.com/repos/{}/{}/stats/participation'.format(
        AUTHOR, REPO)
    response = requests.get(url, verify=False).json()
    with open('data/weekly_commit_52_week.txt', 'w') as json_file:
        json.dump(response, json_file)

    data = open('data/weekly_commit_52_week.csv', 'w', newline='')
    csvwriter = csv.writer(data)
    for index in range(53):
        if index == 0:
            all = response['all']
            owner = response['owner']
            csvwriter.writerow(['week', 'all', 'owner'])
        csvwriter.writerow([index, all[index-1], owner[index-1]])
    data.close()


def commit_per_hour():
    url = 'https://api.github.com/repos/{}/{}/stats/punch_card'.format(
        AUTHOR, REPO)
    response = requests.get(url, verify=False).json()
    print(json.dumps(response, indent=4))


if __name__ == "__main__":
    # weekly_commit()
    commit_per_hour()
