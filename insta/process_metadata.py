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

for file in json_files:
    username = file.split("/")[-1][:-5]
    print("processing", username)

    data = json.load(open(file, 'r'))

    if "GraphImages" not in data.keys():
        print("skipping")
        continue

    csv_file = open(os.path.join(output_dir, f"{username}.csv"), "w", encoding="utf-8")
    fwriter = csv.writer(csv_file)
    fwriter.writerow(["text", "typename", "n_likes", "n_comments", "n_video_views", "timestamp", "tags", "shortcode", "display_url"])
    
    csv_file_c = open(os.path.join(output_dir, f"{username}_comments.csv"), "w", encoding="utf-8")
    fwriter_c = csv.writer(csv_file_c)
    fwriter_c.writerow(["shortcode", "created_at", "username", "text"])

    for node in data["GraphImages"]:
        node_keys = node.keys()
        text = node["edge_media_to_caption"]["edges"][0]["node"]["text"].replace(
            '\n', '\\n') if len(node["edge_media_to_caption"]["edges"]) > 0 else ""
        typename = node["__typename"]
        n_likes = node["edge_media_preview_like"]["count"]
        n_comments = node["edge_media_to_comment"]["count"]
        n_views = node['video_view_count'] if "video_view_count" in node_keys else 0
        display_url = node["display_url"]
        timestamp = node["taken_at_timestamp"]
        tags = " ".join(node["tags"]) if "tags" in node_keys else ""
        shortcode = node["shortcode"]
        fwriter.writerow([text, typename, n_likes, n_comments, n_views, timestamp, tags, shortcode, display_url])

        for comment in node["comments"]["data"]:
            created_at_c = comment["created_at"]
            username_c = comment["owner"]["username"]
            text_c = comment["text"].replace('\n', '\\n')
            fwriter_c.writerow([shortcode, created_at_c, username_c, text_c])


    csv_file.close()
    csv_file_c.close()
