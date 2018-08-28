from flask import Flask

class Config:
    DEBUG = True

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return 'hello'

if __name__ == '__main__':
    app.run()