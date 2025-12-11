from fastapi import FastAPI, File, UploadFile
from x_rays.ml_logic.registry import load_model_function

from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.densenet import preprocess_input
import numpy as np
import io 

app = FastAPI()

app.state.model = load_model_function()

@app.get('/')
def index():
    return {'ok': True}

@app.get('/get_test')
def predict_from_upload(uploaded_file='x_rays/api/0a8d486f-1aa6-4fcf-b7be-4bf04fc8628b.png'):
    """
    Takes a Streamlit uploaded file and a loaded Keras model.
    Returns the probability score (0.0 to 1.0) of being Positive for COVID.
    """
    
    # 1. Open the image directly from the Streamlit buffer
    # .convert('RGB') ensures we don't crash on PNGs with transparency (Alpha channel)
    img = Image.open(uploaded_file).convert('RGB')
    #img = Image.open().convert('RGB')
    
    # 2. Resize to match your DenseNet input (320x320)
    img = img.resize((320, 320))
    
    # 3. Convert to Array
    img_array = image.img_to_array(img)
    
    # 4. Expand dimensions to create a batch of 1
    # Shape becomes: (1, 320, 320, 3)
    img_batch = np.expand_dims(img_array, axis=0)
    
    # 5. Apply DenseNet Preprocessing (Scaling)
    # CRITICAL: This scales pixels to the range DenseNet expects (-1 to 1 or 0 to 1)
    img_preprocessed = preprocess_input(img_batch)
    
    # 6. Predict
    # verbose=0 prevents cluttering your Streamlit logs
    model = app.state.model
    prediction = model.predict(img_preprocessed, verbose=0)
    
    # 7. Return the single score
    return {'result': float(prediction[0][0]), 'message': 'well done!'}

@app.post('/do_you_have_covid')
async def do_you_have_covid(received_image: UploadFile = File(...)):
    """
    Takes a Streamlit uploaded file and a loaded Keras model.
    Returns the probability score (0.0 to 1.0) of being Positive for COVID.
    """
    file_bytes = await received_image.read()
    # 1. Open the image directly from the Streamlit buffer
    # .convert('RGB') ensures we don't crash on PNGs with transparency (Alpha channel)
    img = Image.open(io.BytesIO(file_bytes)).convert('RGB')
    #img = Image.open().convert('RGB')
    
    # 2. Resize to match your DenseNet input (320x320)
    img = img.resize((320, 320))
    
    # 3. Convert to Array
    img_array = image.img_to_array(img)
    
    # 4. Expand dimensions to create a batch of 1
    # Shape becomes: (1, 320, 320, 3)
    img_batch = np.expand_dims(img_array, axis=0)
    
    # 5. Apply DenseNet Preprocessing (Scaling)
    # CRITICAL: This scales pixels to the range DenseNet expects (-1 to 1 or 0 to 1)
    img_preprocessed = preprocess_input(img_batch)
    
    # 6. Predict
    # verbose=0 prevents cluttering your Streamlit logs
    model = app.state.model
    prediction = model.predict(img_preprocessed, verbose=0)
    
    # 7. Return the single score
    return {'result': float(prediction[0][0]), 'message': 'well done!'}
        