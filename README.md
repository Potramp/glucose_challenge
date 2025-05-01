# glucose_challenge
Glucose monitoring API

Implement the following API endpoints which use the model database:
- ```/api/v1/levels/``` : Retrieve ( GET ) a list of glucose levels for a given
user_id , filter by start and stop timestamps (optional). This endpoint
should support pagination, sorting, and a way to limit the number of
glucose levels returned.
- ```/api/v1/levels/<id>/``` : Retrieve ( GET ) a particular glucose level by id .


# Tests
Execute: 
```poetry run pytest -s -v --inline-snapshot=report tests```

# Run Application
```poetry run uvicorn glucose_monitor.asgi:app --reload```