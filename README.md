# FPL_DASH 

A dashboard to help sort through FPL data. 

Todo: 
- find best way to store the cleaned data. 

Procfile
```
release: python ./download_data.py
web: gunicorn -w 3 app:server
```
