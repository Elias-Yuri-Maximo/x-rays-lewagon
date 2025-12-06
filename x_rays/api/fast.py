from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'ok': True}

@app.get('/do_you_have_covid')
def predict():
    return 'Put a mask and go back home'