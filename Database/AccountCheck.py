def signin(email, password):
    file = open("Database/Account.txt", "r")

    # dictionary of emails with pass and id value
    accounts = {}
    for line in file:
        _id, em, pw = line.rstrip("\n").split(",")
        accounts[em] = (_id, pw)

    # checking email in the list of emails
    if email in accounts.keys():
        # login successfully
        if password == accounts[email][1]:
            return accounts[email][0]
        # incorrect password
        else:
            return "Incorrect Password"
    
    # account does not exist
    file.close()
    return "Account does not exist"
            