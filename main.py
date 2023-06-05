from fastapi import FastAPI, UploadFile, File
from starlette.responses import HTMLResponse
from datetime import datetime
from models.model import UploadedImage
from utils.database import SessionLocal, engine
import cv2
import numpy as np
from PIL import Image
import io
import base64
from sqlalchemy import inspect


app = FastAPI()

# Connect to the database
UploadedImages = UploadedImage.__table__
db = SessionLocal()


def detector(image):
    weapon = "False"
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    if img is None:
        raise ValueError(
            "cv2.imdecode returned None, indicating that the input data was not correctly decoded as an image")
    net = cv2.dnn.readNet("yolov3/yolov3_training_2000_1.weights",
                          "yolov3/yolov3_testing_1.cfg")
    classes = ["Weapon"]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(
        img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, label, (x, y + 30), font, 3, (0, 0, 255), 3)
            weapon = "True"
    pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return pil_image, weapon


@app.get("/")
def home():
    with open("static/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.on_event("startup")
async def startup():
    # Create tables in the database if they don't exist
    inspector = inspect(engine)
    if not inspector.has_table("uploaded_images"):
        UploadedImages.create(engine)


@app.post("/detect_weapon")
async def detect_weapon_endpoint(image: UploadFile = File(...)):
    status = False
    try:
        upload_time = datetime.now()
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents))
        flipped_image, status = detector(pil_image)
        db_image = UploadedImage(upload_time=upload_time, image_name=image.filename,
                                 status=status)
        db.add(db_image)
        db.commit()

        with io.BytesIO() as output:
            flipped_image.save(output, format='PNG')
            flipped_image_bytes = output.getvalue()

        flipped_image_base64 = base64.b64encode(
            flipped_image_bytes).decode('utf-8')

        return HTMLResponse(
            content='<img src="data:image/png;base64,{}" class="img-fluid">'.format(
                flipped_image_base64),
            status_code=200
        )
    except Exception as e:
        return HTMLResponse(content='Error: {}'.format(str(e)), status_code=500)
