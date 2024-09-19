from flask import Blueprint, current_app, jsonify, request


api = Blueprint("api", __name__)

# saving the action of the user {id: int [{'type': str, 'amount': float, timestamp: int}]}
user_actions = {}

def save_user_action(user_id, action_type, amount, timestamp):
    if user_id not in user_actions:
        user_actions[user_id] = []
        
    user_actions[user_id].append({"type": action_type, "amount": amount, "timestamp": timestamp})
    return user_actions

@api.post("/event")
def handle_user_event() -> dict:
    current_app.logger.info("Handling user event")
    
    data = request.get_json()
    
    action_type = data.get("type")
    amount = float(data.get("amount", 0))  # Convert amount to float
    user_id = data.get("user_id")
    timestamp =  data.get("time")
    
    user_actions = save_user_action(user_id, action_type, amount, timestamp)
    #print(user_actions)

    # Default response
    response = {
        "alert": False,
        "alert_codes": [],
        "user_id": user_id,
        "time": timestamp
    }
    
    # Check for withdrawal over 100
    if action_type == "withdraw" and amount > 100:
        response["alert"] = True
        response["alert_codes"].append(1100)
        
    
        
    # Check for three consecutive withdrawals   
        # create a list containing the last 3 actions of the user
        # if every transaction "type" in the list is a withdraw, return True
    if len(user_actions[user_id]) >= 3:
        last_three = user_actions[user_id][-3:] 
        if all(action["type"] == "withdraw" for action in last_three): 
            response["alert"] = True
            response["alert_codes"].append(30)
            
    # Check for three consecutive increasing deposits
        # create a list containing the deposits of the user
        # compare the last 3 deposits  
    deposits = [action for action in user_actions[user_id] if action["type"] == "deposit"] 
    if len(deposits) >= 3 and deposits[-3]["amount"] < deposits[-2]["amount"] < deposits[-1]["amount"]:
        response["alert"] = True
        response["alert_codes"].append(300)        
    
    
    # Sum up deposists made in the last 30 seconds, 
    # by comparering the timestamp of the current event with the timestamps in user_actions[user_id]
    recent_total_deposit = sum(action["amount"] for action in user_actions[user_id] 
                    if action["type"] == "deposit" and timestamp - action["timestamp"] <= 30)
    
    #print(recent_total_deposit)

    if recent_total_deposit > 200:
        response["alert"] = True
        response["alert_codes"].append(123)
         
    return jsonify(response)
