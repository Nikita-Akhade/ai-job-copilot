def test_list_jobs(client):
    response = client.get("/api/v1/jobs/")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data
    assert "pages" in data


def test_pagination(client):
    response = client.get(
        "/api/v1/jobs/",
        params={
            "page": 1,
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 5
    assert len(data["items"]) <= 5


def test_create_job(client):
    response = client.post(
        "/api/v1/jobs/",
        json={
            "title": "Python Backend Developer",
            "company": "Test GmbH",
            "location": "Berlin",
            "url": "https://example.com/test-job",
            "description": "Python backend development.",
            "source": "test",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Python Backend Developer"
    assert data["company"] == "Test GmbH"


def test_search_jobs(client):
    client.post(
        "/api/v1/jobs/",
        json={
            "title": "Python Backend Developer",
            "company": "Test GmbH",
            "location": "Berlin",
            "url": "https://example.com/python-job",
            "description": "Python and FastAPI development.",
            "source": "test",
        },
    )

    response = client.get(
        "/api/v1/jobs/",
        params={
            "q": "python",
            "page": 1,
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert "Python" in data["items"][0]["title"]


def test_location_filter(client):
    client.post(
        "/api/v1/jobs/",
        json={
            "title": "Python Developer",
            "company": "Berlin GmbH",
            "location": "Berlin",
            "url": "https://example.com/berlin-job",
            "description": "Backend development.",
            "source": "test",
        },
    )

    client.post(
        "/api/v1/jobs/",
        json={
            "title": "Python Developer",
            "company": "Munich GmbH",
            "location": "Munich",
            "url": "https://example.com/munich-job",
            "description": "Backend development.",
            "source": "test",
        },
    )

    response = client.get(
        "/api/v1/jobs/",
        params={
            "location": "Berlin",
            "page": 1,
            "limit": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["location"] == "Berlin"
