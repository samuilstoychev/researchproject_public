from facepplib import FacePP
import os
import sys, traceback
import csv
from datetime import datetime
import inspect

OUTPUT_FILE = 'face++_output.csv'
LOGS_LOCATION = "./face++_logs"

def write_to_csv(data):
    """ Write information to a CSV file. """
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(("File Name", "Target ID", "Image ID",
        "Race", "Gender", "Expression", "Face++ Gender", "Face++ Age", "Face++ Emotion", "Face++ Smiling"))
        for tuple in data:
            csvwriter.writerow(tuple)

def extract_file_info(file_url):

    """ Given a URL of an image, extract the gender, race and expression metadata. """
    # Only get the actual file name
    file_name = get_file_name(file_url).split(".")[0]
    file_name = file_name.split("-")
    race = file_name[1][0]
    gender = file_name[1][1]
    expression = file_name[4]
    target_id = file_name[1] + "-" + file_name[2]
    image_id = file_name[3]
    return (target_id, image_id, race, gender, expression)

def extract_response_info(response):
    gender = response["_decoded_attrs"]["faces"][0]["attributes"]["gender"]["value"]

    age = response["_decoded_attrs"]["faces"][0]["attributes"]["age"]["value"]

    emotions = response["_decoded_attrs"]["faces"][0]["attributes"]["emotion"]
    emotion = max(emotions, key=lambda x: emotions[x])

    smile = response["_decoded_attrs"]["faces"][0]["attributes"]["smile"]["value"]
    smile = "True" if smile>50 else "False"
    return (gender, age, emotion, smile)

def get_file_name(path):
    return path.split("/")[-1]

def log_to_image_name(log_name):
    return log_name.split(" ")[2][:-3] + "jpg"

if __name__ == "__main__":

    data = []
    logs = os.listdir(LOGS_LOCATION)
    for log in logs:
        dump = open(LOGS_LOCATION + "/" + log, 'r').read()
        dump = dump.replace("<facepplib.managers.ResourceManager object for Image resource>", "''")
        response = eval(dump)
        image_name = log_to_image_name(log)
        row = (image_name, ) + extract_file_info(image_name) + extract_response_info(response)
        data.append(row)

    try:
        write_to_csv(data)
    except:
        print("Problem with writing data to the CSV file. ")
