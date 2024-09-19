from flask.testing import FlaskClient

def test_handle_user_event_withdraw_over_100(client: FlaskClient):
    response = client.post("/event", json={
        "type": "withdraw",
        "amount": "150.00",
        "user_id": 1,
        "time": 10
    })
    assert response.status_code == 200
    assert response.json == {
        "alert": True,
        "alert_codes": [1100],
        "time": 10,
        "user_id": 1
    }
    
def test_handle_user_event_three_consecutive_withdrawals(client: FlaskClient):
    for _ in range(3):
        response = client.post("/event", json={
            "type": "withdraw",
            "amount": "50.00",
            "user_id": 1,
            "time": 20
        })
    assert response.status_code == 200
    assert response.json["alert"] is True
    assert 30 in response.json["alert_codes"]
    
def test_handle_user_event_three_consecutive_increasing_deposits(client: FlaskClient):
    client.post("/event", json={
        "type": "deposit",
        "amount": "10.00",
        "user_id": 1,
        "time": 30
    })
    client.post("/event", json={
            "type": "withdraw",
            "amount": "50.00",
            "user_id": 1,
            "time": 20
        })
    client.post("/event", json={
        "type": "deposit",
        "amount": "20.00",
        "user_id": 1,
        "time": 40
    })
    response = client.post("/event", json={
        "type": "deposit",
        "amount": "30.00",
        "user_id": 1,
        "time": 50
    })
    assert response.status_code == 200
    assert response.json["alert"] is True
    assert 300 in response.json["alert_codes"]
    

def test_handle_user_event_total_deposits_exceeding_200(client: FlaskClient):
    client.post("/event", json={
        "type": "deposit",
        "amount": "100.00",
        "user_id": 1,
        "time": 60
    })
    client.post("/event", json={
        "type": "deposit",
        "amount": "50.00",
        "user_id": 1,
        "time": 65
    })
    response = client.post("/event", json={
        "type": "deposit",
        "amount": "60.00",
        "user_id": 1,
        "time": 70
    })
    assert response.status_code == 200
    assert response.json["alert"] is True
    assert 123 in response.json["alert_codes"]
