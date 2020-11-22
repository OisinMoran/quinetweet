from datetime import datetime
import subprocess
import json

OFFSET = 1288834974657
TIME_DIFF = 359
MACHINE_ID = 377
N = 10

def tweet_id_from_timestamp(utcdttime):
    tstamp = utcdttime.timestamp()
    tid = int(tstamp * 1000) - OFFSET
    return tid << 22

def tweet_id_to_parts(tid):
    timestamp = tid >> 22
    machine_id = (tid >> 12) & (2**10-1)
    seq_no = tid & (2**12-1)
    return timestamp, machine_id, seq_no

def compare_ids(guessed_id, real_id):
    guessed_ts, guessed_mid, guessed_sno = tweet_id_to_parts(guessed_id)
    real_ts, real_mid, real_sno = tweet_id_to_parts(real_id)
    ms = guessed_ts - real_ts
    mid_diff =  guessed_mid - real_mid
    sno_diff = guessed_sno - real_sno
    return ms, mid_diff, sno_diff

def guess_tweet_id(time_diff=0, machine_id=0):
    tid = tweet_id_from_timestamp(datetime.now())
    tid += machine_id << 12
    tid += time_diff << 22
    return tid

def guess():
    for _ in range(N):
        guessed_id = guess_tweet_id(TIME_DIFF, MACHINE_ID)
        command = f"twurl -d 'status=https://twitter.com/quinetweet/status/{guessed_id}' /1.1/statuses/update.json"
        op = subprocess.check_output(command, shell=True)
        actual_id = json.loads(op.decode())["id"]
        print(actual_id)
        time, mid, sno = compare_ids(guessed_id, actual_id)
        print(time, mid, sno)
        if (time, mid, sno) == (0, 0, 0):
            print("Success")
            break

guess()
