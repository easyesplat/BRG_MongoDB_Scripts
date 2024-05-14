from get_database import get_database
from gridfs import GridFS
from PIL import Image
import io

# Global variables 
db = get_database("hazards")
fs = GridFS(db)

def upload_image(steer_photo_id):
    # Read the image file
    with open('/Users/eric/brq_mongodb/BRG_MongoDB_Scripts/MongoDB/image_sample/dog.png', 'rb') as f:
        image_data = f.read()

    # Store the image in MongoDB
    image_id = fs.put(image_data, filename=steer_photo_id)

    print(f"Image uploaded with id: {image_id}")
    return image_id

def retrieve_image(image_id):
    # Retrieving the image
    out = fs.get(image_id)
    image = Image.open(io.BytesIO(out.read()))
    image.show()
    return image

if __name__ == "__main__":
    image_id = upload_image("test")
    retrieve_image(image_id)
