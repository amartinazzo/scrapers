import csv
from glob import glob
import json
import os
import sys

if len(sys.argv) < 3:
    print("usage: python {} \"<glob_pattern>\" <output_dir>".format(sys.argv[0]))
    exit(1)

pattern = sys.argv[1]
output_dir = sys.argv[2]
json_files = glob(pattern)

if len(json_files) == 1:
    print("Warning: glob_pattern must be inside quotation marks")

json_files = [j for j in json_files if 'metadata' not in j]

csv_file = open(os.path.join(output_dir, "profiles.csv"), "w", encoding="utf-8")
    
fwriter = csv.writer(csv_file)
fwriter.writerow([
    "username", "posts_cnt", "downloaded_cnt", "is_private", "followers_cnt", "following_cnt",
    "full_name", "biography", "profile_pic_url"])

for file in sorted(json_files):
    username = file.split("/")[-1][:-5]
    print("processing", username)
    
    data = json.load(open(file, 'r'))
    username = data["GraphProfileInfo"]["username"]
    biography = data["GraphProfileInfo"]["info"]["biography"].replace("\n", " ")
    followers_count = data["GraphProfileInfo"]["info"]["followers_count"]
    following_count = data["GraphProfileInfo"]["info"]["following_count"]
    full_name = data["GraphProfileInfo"]["info"]["full_name"]
    is_private = data["GraphProfileInfo"]["info"]["is_private"]
    posts_count = data["GraphProfileInfo"]["info"]["posts_count"]
    profile_pic_url = data["GraphProfileInfo"]["info"]["profile_pic_url"]

    graphimages_len = len(data["GraphImages"]) if "GraphImages" in data.keys() else 0
    
    fwriter.writerow([
        username, posts_count, graphimages_len, is_private, followers_count, following_count,
        full_name, biography, profile_pic_url])

csv_file.close()
