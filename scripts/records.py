def get_record(index):
    '''This function returns the user's record in a specific game mode'''
    with open(r"app data\user-records.txt", "r") as f:
        user_records = f.readlines()
    user_records = [i.strip() for i in user_records]

    return user_records[index]

def update_record(score, index):
    '''This function updates the user's record in a specific game mode'''
    records_file_path = r"app data\user-records.txt"

    with open(records_file_path, "r") as f:
        user_records = f.readlines()

    user_records = [i.strip() for i in user_records]

    if int(user_records[index]) < score:
        user_records[index] = score

        with open(records_file_path, "w") as f:
            [f.write(f"{i}\n") for i in user_records]