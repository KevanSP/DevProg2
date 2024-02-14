from time import sleep
import FireAI as fai
import Notification as noif


def main():
    count = 0
    while True:
        sleep(1)
        if '1' in fai.main():
            count += 1
        else:
            count = 0
        if count == 5:
            noif.Send_Notif('AI Detection', 'The AI Has Detected Fire for 5 seconds!')
            count = 0
