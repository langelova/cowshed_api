<h1> Animal Management System </h1>

A Django-based animal management system that helps manage data for farm animals, including feeding schedules, milk production, and weight tracking. The project includes async tasks using Celery and Redis and is containerized with Docker.



Features
--------

*   **Animal Management**: Create, update, read, and delete animal data, including birthdate, sex, condition, and calves data.

*   **Feeding & Milking Schedules**: Automatically manage feeding and milking tasks based on cron schedules.

*   **Weight Tracking**: Track animal weight with timestamps for each measurement.

*   **Asynchronous Tasks**: Use Celery to handle scheduled tasks for feeding and milking.

*   **Random Data Generation**: Generate random animal data for testing using a custom management command.

*   **Dockerized Environment**: Deploy the Django app with Celery, Celery Beat, and Redis using Docker.

Getting Started
---------------

### Prerequisites

Ensure you have the following installed on your machine:

*   Docker

*   Docker Compose


### Installation

1.  **Clone the Repository**:

```
git clone https://github.com/langelova/cowshed_api.git
```

2.  **Build and start containers**:

```
docker-compose up --build
```

3. **Generate sample data**:
```
docker exec -it django python manage.py generate_random_data --num_cows 20
```

4. **Run tests**:
```
docker exec -it django python manage.py test cmanager
```

5. **Interact with the api**:
```
http://localhost:8000/docs/
```
