# test_backend

test_backend - this is text exercise I was given for the job.
Download the yolov3 folder with weights file from the following Google Drive link https://drive.google.com/drive/folders/18bIadvuOmfg0WIUSdf-mfYMlD4-2a9Cq?usp=sharing to the project.

To set up the project, follow these steps:

1.Create a virtual environment:

Run ``` python3 -m venv venv ``` to create a virtual environment.

2.Activate the virtual environment:
On macOS/Linux: Run ```source venv/bin/activate```
On Windows: Run ```venv\Scripts\activate.bat```

3.Install the required dependencies:
Run ```pip install -r requirements.txt``` to install the dependencies.

4.To run the test_backend application:
Activate the virtual environment if it's not already activated:
On macOS/Linux: Run ```source venv/bin/activate```
On Windows: Run ```venv\Scripts\activate.bat```


5.Start the FastAPI server:

Run ```uvicorn main:app --reload``` to start the server.
Access the application by navigating to http://localhost:8000 in your web browser.


Endpoints:

Home: URL: /, Method: GET, Description: Displays home page with image upload form.


Flip Image: URL: /flip_image, Method: POST, Description: Accepts uploaded image, detects objects, flips image if weapons detected, and returns flipped image.


Helper Function:

detect_and_crop_objects(image): Detects objects in provided image using YOLOv3 object detection model, crops objects.

Parameters: image (PIL.Image)

Returns: pil_image (PIL.Image), weapon (str)


Database: SQLite database with table 'uploaded_images', columns: id (INTEGER), upload_time (DATETIME), image_name (VARCHAR), status (VARCHAR).

![Alt Text](https://github.com/allebee/test_back/blob/main/process_photo1.png)
