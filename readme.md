## Demo app that uses celery+redis alongside Dash to cache slow callbacks 
Worked example in response to this [question ](https://community.plotly.com/t/how-to-run-2-callbacks-in-parallel-my-attempt-using-background-callbacks-redis-celery-not-working/74847) on the Plotly Community Forum.

Set-up your environment
Remember that pyenv does not work well on Windows

```sh
git clone https://github.com/this_repo
cd this_repo
pyenv virtualenv 3.10.10 this_repo 
pyenv local this_repo
pip install -r requirements.txt
```

Start redis
```sh
brew install redis
redis-server
```

In a new shell, start your backend api (the fastapi app)
```sh
uvicorn api.app
```

In a new terminal environment, start celery beat
```sh
env $(grep -v '^#' .env | xargs) celery -A web.tasks.celery_app beat --loglevel=info
```

In a new terminal environment, start the celery worker
```sh
env $(grep -v '^#' .env | xargs) celery -A web.tasks.celery_app worker --loglevel=info
```

Finally, start the dash app
```sh
python -m web.app 
```


## Update
Much simpler version that works by just adding workers / threads to gunicorn
Thanks to [@emil](https://community.plotly.com/u/Emil)
Code now in `./mwe/app.py` 
And run this by

```sh
gunicorn --bind :8102 mwe.app:server --workers 2
```


