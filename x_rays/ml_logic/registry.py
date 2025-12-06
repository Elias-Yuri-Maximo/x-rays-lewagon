from x_rays.params import *
from google.cloud import storage
from tensorflow.keras.models import load_model

def load_model_function(stage="Production"):
    """
    Return a saved model:
    - locally (latest one in alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'  --> for unit 02 only

    Return None (but do not Raise) if no model is found

    """
    
    if MODEL_TARGET == "local":
        model_path = './x_rays/ml_logic/best_covid_model_finetuned.keras'
        model = load_model(model_path)

        print("✅ Model loaded from local disk")

        return model

    #elif MODEL_TARGET == "gcs":
        # Fill with code 
        
    else:
        return None