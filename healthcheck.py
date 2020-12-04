from quart import Quart
app = Quart(__name__)

@app.route('/health')
async def hello():
    return 'Alive'
    