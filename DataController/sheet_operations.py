import gspread
from oauth2client.service_account import ServiceAccountCredentials

def authenticate_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('xxxxxxxxxxxxx.json', scope)
    client = gspread.authorize(creds)
    posts_sheet =  client.open('post_datasheet').sheet1  # Access the first sheet
    comments_sheet = client.open('Comments_tracker').sheet1
    return posts_sheet,comments_sheet


def update_google_sheet(data,type):
    post_sheet,comments_sheet = authenticate_google_sheets()
    
    if type == "post":
        post_id = str(data.get('post_id', ''))
        url = str(data.get('url', ''))
        comments_count = int(data.get('comments_count', 0))  
        mentions = str(data.get('mentions', ''))  
        timestamp = str(data.get('timestamp', ''))
        
        existing_post = find_existing_post(post_id, post_sheet)
        if existing_post:
            if existing_post[2] != comments_count:
                update_post(post_id, comments_count,post_sheet)
        else:
            # Append the data to the sheet
            post_sheet.append_row([post_id, url, comments_count, mentions, timestamp])

    if type == "comments":
        post_url = data['url']
        username = data['ownerUsername']
        comment_text = data['comments']
        timestamp = data['timestamp']
        replies_count = data['repliesCount']
        likes_count = data['likesCount']

        existing_comment = find_existing_comment(post_url, username, comments_sheet)
        if existing_comment:
            # If data exists, check for text change and update
            if existing_comment[2] != comment_text:
                update_comment(post_url,comment_text, username,comments_sheet)
        else:
            comments_sheet.append_row([post_url, username, comment_text, timestamp, replies_count, likes_count])

def find_existing_post(post_id, sheet):
    try:
        cell = sheet.findall(post_id)
        return sheet.row_values(cell.row)
    except:
        return None
    
def update_post(post_id, comments_count,sheet):
    cell = find_existing_post(post_id, sheet)
    if cell:
        row = [post_id, comments_count] 
        range_to_update = f"A{cell}:B{cell}"
        sheet.update(range_to_update, [row])

def find_existing_comment(post_url, username, sheet):
    try:
        cell = sheet.find(post_url)
        row = sheet.row_values(cell.row)
        if row[1] == username:
            return row
        return None
    except:
        return None

def update_comment(post_url, comment_text,username,sheet):
    row = find_existing_comment(post_url, username, sheet)
    if row:
        row[2] = comment_text # Update the comment text
        sheet.update(row[0], row)
