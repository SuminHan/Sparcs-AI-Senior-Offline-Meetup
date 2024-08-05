import os
import utils
import time
from tinydb import TinyDB, Query

DB_CHECKIN = TinyDB('DB/checkin.json')
Checkin = Query()

# Directory to save uploaded images
UPLOAD_DIRECTORY = "static/uploaded_images"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

async def upload_file(file, uid, comment):
    # Read the file content asynchronously
    file_content = await file.read()
    
    # Create a unique filename
    tobehashed_name = f"{uid}_{file.filename}"
    file_extension = file.filename.split('.')[-1]
    new_filename = f'{utils.hash_string(tobehashed_name)}.{file_extension}'
    file_location = os.path.join(UPLOAD_DIRECTORY, new_filename)
    
    # Write the file content to the new file
    with open(file_location, "wb") as buffer:
        buffer.write(file_content)

    cid = "cid_" + utils.hash_string('/'.join([uid, comment, str(time.time())]))
    
    data = {
        "imgurl": f'/{file_location}',
        "Event": uid, 
        "cid": cid, 
        "message": "Image uploaded successfully!",
        "Comment": comment
    }

    DB_CHECKIN.insert(data)
    
    return data

