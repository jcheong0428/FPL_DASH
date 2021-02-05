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
clock: python clock.py
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
Git push to github will automatically deploy.
```
git add . 
git commit -m "made some changes"
git push heroku master
```

## Update
```
cd Fantasy-Premier-League && git pull origin master && cd ..
git add . && git commit -m "update gw"
git push
```