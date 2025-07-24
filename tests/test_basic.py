import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_api_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'URL Shortener API' in data['message']

def test_shorten_url_valid(client):
    response = client.post('/api/shorten', json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data
    assert len(data['short_code']) == 6

def test_shorten_url_invalid(client):
    response = client.post('/api/shorten', json={"url": "invalid-url"})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_redirect_success(client):
    # Create short URL first
    shorten_resp = client.post('/api/shorten', json={"url": "https://example.com"})
    short_code = shorten_resp.get_json()['short_code']

    # Test redirect with short code
    redirect_resp = client.get(f'/{short_code}')
    assert redirect_resp.status_code == 302
    assert redirect_resp.location == "https://example.com"

def test_redirect_not_found(client):
    response = client.get('/xxxxxx')
    assert response.status_code == 404

def test_stats(client):
    # Shorten URL
    shorten_resp = client.post('/api/shorten', json={"url": "https://example.com"})
    short_code = shorten_resp.get_json()['short_code']

    # Redirect twice to increase count
    client.get(f'/{short_code}')
    client.get(f'/{short_code}')

    # Get stats
    stats_resp = client.get(f'/api/stats/{short_code}')
    assert stats_resp.status_code == 200
    data = stats_resp.get_json()
    assert data['clicks'] == 2
    assert data['url'] == "https://example.com"
    assert 'created_at' in data

def test_stats_not_found(client):
    response = client.get('/api/stats/xxxxxx')
    assert response.status_code == 404
