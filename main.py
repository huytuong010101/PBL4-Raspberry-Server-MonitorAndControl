import uvicorn
from dotenv import load_dotenv
import os

# disable this if on product mode
load_dotenv()
# run server 
uvicorn.run("app:app", host=os.environ['HOST'], port=int(os.environ['PORT']))
