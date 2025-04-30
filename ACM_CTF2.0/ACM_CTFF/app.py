# from flask import Flask, render_template, request

# app = Flask(__name__)

# # Balances
# balances = {
#     'Groot': 850,
#     'Rocket': 1500,
#     'Gamora': 1500,
#     'Drax': 1500,
#     'StarLord': 1500
# }

# @app.route('/', methods=['GET'])
# def index():
#     message = ""
#     sender = request.args.get('sender')
#     receivers = request.args.getlist('receiver')  # Important: use getlist
#     amount = request.args.get('amount')

#     if sender and receivers and amount:
#         try:
#             amount = float(amount)
#             if amount <= 0:
#                 message = "Invalid amount entered. Amount must be positive."
#             elif sender not in balances:
#                 message = "Invalid sender!"
#             else:
#                 # Now check:
#                 if len(receivers) == 1:
#                     # Normal transaction
#                     receiver = receivers[0]
#                     if receiver not in balances:
#                         message = "Invalid receiver!"
#                     elif sender == receiver:
#                         message = "You cannot send money to yourself!"
#                     elif receiver.lower() == 'groot':
#                         message = "You cannot directly send money to Groot!"
#                     else:
#                         balances[sender] -= amount
#                         balances[receiver] += amount
#                         message = f"Transferred {amount} from {sender} to {receiver}."
#                 elif len(receivers) == 2:
#                     # Potential bypass attempt
#                     first_receiver = receivers[0]
#                     second_receiver = receivers[1]

#                     if first_receiver.lower() == 'groot':
#                         message = "You cannot select Groot as the first receiver!"
#                     elif second_receiver.lower() != 'groot':
#                         message = "Second receiver must be Groot!"
#                     elif first_receiver not in balances:
#                         message = "First receiver is invalid!"
#                     else:
#                         balances[sender] -= amount
#                         balances['Groot'] += amount
#                         message = f"Successfully exploited and transferred {amount} from {sender} to Groot!"
#                 else:
#                     message = "Invalid request format."
#         except ValueError:
#             message = "Invalid amount entered."

#     return render_template('index.html', balances=balances, message=message)


# @app.route('/admin')
# def admin():
#     if balances.get('Groot', 0) >= 2000:
#         return render_template('admin.html')
#     else:
#         return "You are not allowed. Only members with balance more than 2000 are allowed to access this page."

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, session, make_response
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

INITIAL_BALANCES = {
    'Carloz': 850,
    'Lewis': 1500,
    'Lando': 1500,
    'Max': 1500,
    'Charles': 1500
}

FLAG = "ACM{K1_K1_K1_R@H_R@H}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_balances' not in session:
        session['user_balances'] = INITIAL_BALANCES.copy()
        session['username'] = uuid.uuid4().hex[:8]  # Assign a unique ID

    balances = session['user_balances']
    message = ""
    sender = request.args.get('sender')
    receivers = request.args.getlist('receiver')  # Important: use getlist
    amount = request.args.get('amount')
    username = session['username']

    if not sender:
        sender = username  # Default sender to the current user's session ID

    if sender and receivers and amount:
        try:
            amount = float(amount)
            if amount <= 0:
                message = "Invalid amount entered. Amount must be positive."
            elif sender not in balances:
                message = "Invalid sender!"
            else:
                # Now check:
                if len(receivers) == 1:
                    # Normal transaction
                    receiver = receivers[0]
                    if receiver not in balances:
                        message = "Invalid receiver!"
                    elif sender == receiver:
                        message = "You cannot send money to yourself!"
                    elif receiver.lower() == 'carloz':
                        message = "You cannot directly send money to Carloz!"
                    else:
                        if balances[sender] >= amount:
                            balances[sender] -= amount
                            balances[receiver] += amount
                            session['user_balances'] = balances  # Update session
                            message = f"Transferred {amount} from {sender} to {receiver}."
                        else:
                            message = "Insufficient balance!"
                elif len(receivers) == 2:
                    # Potential bypass attempt
                    first_receiver = receivers[0]
                    second_receiver = receivers[1]

                    if first_receiver.lower() == 'carloz':
                        message = "You cannot select Carloz as the first receiver!"
                    elif second_receiver.lower() != 'carloz':
                        message = "Second receiver must be Carloz!"
                    elif first_receiver not in balances:
                        message = "First receiver is invalid!"
                    else:
                        if balances[sender] >= amount:
                            balances[sender] -= amount
                            balances['Carloz'] += amount
                            session['user_balances'] = balances  # Update session
                            message = f"Successfully exploited and transferred {amount} from {sender} to Carloz!"
                        else:
                            message = "Insufficient balance!"
                else:
                    message = "Invalid request format."
        except ValueError:
            message = "Invalid amount entered."

    return render_template('index.html', balances=balances, message=message, username=username)


@app.route('/admin')
def admin():
    balances = session.get('user_balances', INITIAL_BALANCES)
    if balances.get('Carloz', 0) >= 2000:
        return render_template('admin.html', flag=FLAG)
    else:
        return "You are not allowed. Only members with balance more than 2000 are allowed to access this page."
        
@app.route('/robots.txt')
def robots():
    response = make_response("User-agent: *\nDisallow: /admin")
    response.headers['Content-Type'] = 'text/plain'
    return response

if __name__ == '__main__':
    app.run(debug=True)