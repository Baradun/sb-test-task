
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_request_create_domains():
    response = client.post(
        "/visited_links",
        json={
            "links": [
                "https://ya.ru/",
            ]
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }


def test_request_create_domains_wrong_format_json():
    response = client.post(
        "/visited_links",
        json={
            "LINKS": [
                "https://ya.ru/",
            ]
        },
    )
    assert response.status_code == 400
    assert response.json() == {"status": "bad request"}

    response = client.post(
        "/visited_links",
        json={
            "links": [
                1,
                2,
            ]
        },
    )
    assert response.status_code == 400
    assert response.json() == {"status": "bad request"}


def test_get_domain():
    response = client.get("/visited_domains")
    assert response.status_code == 200
    assert response.json() == {"domains": ['ya.ru'], 'status': 'ok'}


def test_not_get_domain():
    response = client.get("/visited_domains?from=1&to=2")
    assert response.status_code == 200
    assert response.json() == {"domains": [], 'status': 'ok'}


def test_get_domain_start_and_end_times_changed():
    response = client.get("/visited_domains?from=1&to=1111111111")
    assert response.status_code == 200
    assert response.json() == {"domains": [], 'status': 'ok'}
