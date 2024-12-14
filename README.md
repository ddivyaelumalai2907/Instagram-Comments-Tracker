Instagram Comments Tracker:

  This project is designed to fetch and track Instagram posts and comments for the "kalyanjewllers_official" Instagram account using the Apify API. The system updates every 4 hours, ensuring only posts with changes in their comments are updated. Data is stored in Google Sheets, with separate sheets for post details and comments.

Features:
  
  Instagram Post Scraper: Fetches recent posts (from the last 3 days) for the given Instagram account.
  
  Instagram Comment Scraper: Fetches comments for each post.
  
  Google Sheets Integration: Stores post details in one sheet and comments in another.
  
  Automated Updates: Runs every 4 hours via Cron jobs, ensuring the data is up-to-date.

Flow:

  Fetch Post Data: The Instagram Post Scraper retrieves recent posts, extracting details like Post ID, URL, comments count, mentions, and timestamp.

  Fetch Comments: For each post, the Instagram Comment Scraper fetches comments, including details like username, comment text, replies count, likes count, and timestamp.

  Store in Google Sheets: Post details are stored in one sheet, and comments are stored in a separate sheet. Each update checks for changes in comments, and only updated posts are reflected.

  Cron Job: The system runs every 4 hours, triggered by a Cron job, which calls the Flask update_data endpoint to perform the data fetching and updating operations.

Google Sheets Layout

  Posts Sheet: Contains Post ID, URL, Comments Count, Mentions, Timestamp.
  
  Comments Sheet: Contains Post URL, Username, Comment, Timestamp, Replies Count, Likes Count.

Technologies Used:

  Python 3.x
  
  Flask: Web framework for managing endpoints and running the app.
  
  Apify API: Used for scraping Instagram posts and comments.
  
  Google Sheets API: Used for storing and managing data in Google Sheets.
  
  Cron Jobs: Used for scheduling automated updates every 4 hours.
