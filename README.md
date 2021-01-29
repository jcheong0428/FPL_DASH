# FPL_DASH 

A dashboard to help sort through FPL data. 

## Todo: 
- find best way to store the cleaned data. separate db? 
- how to periodically reset the data? 

## Methods
- Averaging: averages across the games played within the number of gameweeks selected. 
- Sum: Adds up across the games played within the number of gameweeks selected. 

Procfile
```
release: python ./download_data.py
web: gunicorn -w 3 app:server
```

## Running locally
```
python download_data.py
python app.py
```

## Contributions
Contributions are welcome! 
1. Fork the repository. 
2. Add your features. 
3. Make sure app is still working.
4. Submit a Pull Request!

## Deployment
```
git add . 
git commit -m "made some changes"
git push heroku master
```