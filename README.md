```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

TODO - WRITE REAL DOCS
```

Start the application
--
while you are in the docker folder type

1. To start
   - docker-compose -p <project name> -f docker-compose.yml up --build -d
   
2. To stop and clean-up
   - docker compose -p  <project name> down 
