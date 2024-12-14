import pathlib, sys

root_path = pathlib.Path(__file__).parent.resolve().parent.resolve()
sys.path.append(str(root_path))

import os,logging
import requests
import time
from flask import Flask, jsonify
from apify_client import ApifyClient
from DataController import sheet_operations as sheet_operations
app = Flask(__name__)

# Apify API Key and Actor ID for Instagram Scraper
client =  ApifyClient('xxxxxxxxxxxxxxxx')

post_data = {}
comments_data = {}

@app.route('/update_data', methods=['GET'])
def update_data():
    run_id_posts = fetch_instagram_posts()
    if run_id_posts:
        posts_data = get_apify_results_post(run_id_posts)
        logging.info("apify_post_data = {}".format(posts_data))
        if posts_data:
            sheet_operations.update_google_sheet(posts_data,"post")
            run_id_comments = fetch_instagram_comments(posts_data["url"])  # Assuming comments are fetched similarly
            if run_id_comments:
                comments_data = get_apify_results_comments(run_id_comments)
                logging.info("apify comments data = {}".format(comments_data))
                if comments_data:
                    sheet_operations.update_google_sheet(comments_data,"comments")

            return jsonify({'status': 'Data updated successfully!'})
        else:
            return jsonify({'status': 'No data found from Apify.'})
    else:
        return jsonify({'status': 'Failed to trigger Apify Instagram Post Scraper.'})

def fetch_instagram_posts():
    run_input = {
        "username": ["kalyanjewellers_official"],
        "resultsLimit": 30,
    }
    run = client.actor("apify/instagram-post-scraper").call(run_input=run_input)
    if run["status"] == "SUCCEEDED":
        dataset_id = run["defaultDatasetId"]
        return dataset_id
    else:
        logging.info("Error triggering the Apify Instagram Post Scraper.")
        return None
    
def fetch_instagram_comments(post_urls):
    run_input = {
        "directUrls": [post_urls],
    }
    task = client.actor('apify/instagram-comment-scraper').call(run_input=run_input)
    task_status = task['status']
    while task_status not in ['SUCCEEDED', 'FAILED']:
        time.sleep(5)  # Wait for 5 seconds before checking again
        task = client.actor('apify/instagram-comment-scraper').get_task(task['id'])
        task_status = task['status']

    if task_status == 'SUCCEEDED':
        return task["defaultDatasetId"]
    else:
        logging.info("Failed to fetch comments for {}" .format(post_urls))
        return None

def get_apify_results_post(run_id):
    response = client.dataset(run_id).list_items()
    items = response.items  
    for item in items:
        return{
            "post_id" :item.get("id",""), 
            "url" :item.get("url",''), 
            "comments_count" :item.get("comments",0),  
            "mentions" :item.get("mentions",0), 
            "timestamp" :item.get("timestamp",'')
        }

def get_apify_results_comments(run_id):
    dataset_items = client.dataset(run_id).list_items().items
    for data in dataset_items:
        return{
            "url":data.get("postUrl",""),
            "username":data.get("ownerUsername",""),
            "comments":data.get("text",""),
            "timestamp" :data.get("timestamp",""),
            "repliesCount":data.get("repliesCount",0),
            "likesCount":data.get("likesCount",0)
        }
    
if __name__ == "__main__":
    app.run(debug=True)