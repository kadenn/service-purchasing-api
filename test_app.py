import json


# Tests the get one offer by it's id feature of the API.
def test_get_first_offer(app, client):
    del app
    res = client.get('/api/offers?id=1')
    assert res.status_code == 200
    expected = {"category": "test-category-2", "id": 1,
                "note": "This offer added from api", "when": "30.01.2021 13:00", "where": "İzmir/Bornova"}
    assert expected == json.loads(res.get_data(as_text=True))


# Tests the get all offers feature of the API.
def test_get_all_offers(app, client):
    del app
    res = client.get('/api/offers')
    assert res.status_code == 200


# Tests the insert offer feature of the API.
def test_insert_offer(app, client):
    del app
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        "category": "unit-test",
        "when": "01.01.9999",
        "where": "Anywhere",
        "note": "This offer created for unit testing"
    }

    res = client.post('/api/offers', data=json.dumps(data), headers=headers)

    assert res.status_code == 200
    expected = {"Message": "New Offer insterted to database."}
    assert expected == json.loads(res.get_data(as_text=True))


# Tests the delete offer feature of the API.
def test_delete_offer(app, client):
    del app
    res = client.delete('/api/offers')
    assert res.status_code == 200
    expected = {"Message": "Last offer deleted."}
    assert expected == json.loads(res.get_data(as_text=True))

# Command to execute tests: python3 -m pytest
