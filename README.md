# Test challenge for Kazdream Technologies


### Instructions:

1. Clone repo to your machine

2. Build and start containers with:
```
sudo docker-compose up --build

```

3. Wait until all services are ready

4. Go to API documentation which is available at [http://0.0.0.0:8000/](http://0.0.0.0:8000/)

5. Visit **/load** endpoint to import data from the csv file

6. Explore **person** and **organization** endpoints. Optional *q* paramater can be used for full text search. There is also an option to find a single record by id, e.g. **person/{id}**


### Notes:
- REST API is powered by **FastAPI Framework**

- Data for REST API is being loaded from Elasticsearch (due to speed and searching capabilities)

- Replication of data to the Elasticsearch cluster was implemented purely in Python. The more robust approach would be to integrate Neo4j directly with ES. This option has not been chosen due to lack of previous experience with both technologies.

- The whole task took about 10 working hours to finish including short intros to Neo4j and ES
