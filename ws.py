import sys
import websocket
import json
import classify
import bodyfetcher
from termcolor import cprint

def main():
    try:
        clf = classify.NaiveBayesClassifier(0.5, 0.5)
    except Exception as ex:
        print(ex)
        sys.exit(1)

    ws = websocket.create_connection("ws://qa.sockets.stackexchange.com/")
    ws.send("155-questions-active")

    while True:
        try:
            recv_data = ws.recv()
            print("Received data from realtime websocket.")
            recv_json = json.loads(recv_data)
            post_data = json.loads(recv_json['data'])
            cprint("ID: {0} on site: {1}".format(post_data['id'], post_data['siteBaseHostAddress']), 'cyan')

            full_data = bodyfetcher.fetch_post(post_data['siteBaseHostAddress'], post_data['id'])
            print("Fetched full post data from API; classifying post.")

            run_classifier(clf, full_data)

            if 'answers' in full_data:
                print("Classifying answers...")
                for answer in full_data['answers']:
                    answer_obj = {
                        'title': full_data['title'],
                        'body': answer['body']
                    }
                    run_classifier(clf, answer_obj)
            else:
                print("no answers")

            print("")
        except Exception as ex:
            cprint("Exception while running classification process on received data. {0}".format(ex), 'yellow')


def run_classifier(clf, full_data):
    clobj = {
        'title': full_data['title'],
        'body': full_data['body']
    }
    status, spam_score, ham_score = clf.classify(clobj, ['title', 'body'])
    if status == True:
        cprint("NB Classifier result: spamstatus={0}, spamscore={1}, hamscore={2}".format(status, spam_score, ham_score), 'red')
    else:
        cprint("NB Classifier result: spamstatus={0}, spamscore={1}, hamscore={2}".format(status, spam_score, ham_score), 'white')


if __name__ == "__main__":
    main()
