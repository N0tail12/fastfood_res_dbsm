import random


def randstring(length):
    valid_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join((random.choice(valid_letters) for i in range(length)))


def randemails(num):
    lst_email = []
    for i in range(num):
        email = random.choice(['nguyen', 'luu', 'le', 'phung', 'lai', 'pham', 'tran', 'duong']) + \
                random.choice(['hieu', 'dat', 'huyen', 'dai', 'long', 'phuc', 'quang', 'truong', 'nghia', 'duc']) + \
                randnumber(3) + '@gmail.com'
        lst_email.append(email)
    return lst_email


def randnumber(length):
    valid_letters = '0987654321'
    return ''.join((random.choice(valid_letters) for i in range(length)))


def make_data_customer_info(num):
    # INSERT INTO customer_info
    # VALUES ('rksazid@gmail.com','MD.REZAUL','KARIM','rksazid123','01521453995','TELIGATI','Khulna','Active');
    towns = ['Bach Khoa', 'Cau Giay', 'Ba Dinh', 'Hoan Kiem', 'Long Bien', 'Hoang Mai', 'Thanh Tri', 'Ha Dong']
    city = 'Ha Noi'
    emails = []
    with open('database_insert.sql', 'w+') as f:
        for i in range(num):
            fname = random.choice(['Hieu', 'Dat', 'Huyen', 'Dai', 'Long', 'Phuc', 'Quang', 'Truong', 'Nghia', 'Duc'])
            middle_name = random.choice(['Hoang', 'Thanh', 'Thang', 'Long', 'Minh', 'Xuan', 'Khanh'])
            first_name = middle_name + ' ' + fname
            last_name = random.choice(['Nguyen', 'Luu', 'Le', 'Phung', 'Lai', 'Pham', 'Tran', 'Duong'])
            email = str.lower(fname + last_name + randnumber(5) + '@gmail.com')
            emails.append(email)
            password = 'qwer1234'
            number = '0' + randnumber(9)
            town = random.choice(towns)
            f.write(
                f"INSERT INTO customer_info VALUES ('{email}','{first_name}','{last_name}','{password}','{number}','{city}','{town}','Active');\n")
    return emails


def make_data_order_info(num, emails):
    # INSERT INTO order_info VALUES ('1000','dipto.8081@gmail.com','4-APR-2017','5-APR-2017');
    max = 1000 + num
    with open('database_insert.sql', 'a+') as f:
        for order_id in range(1000, max + 1):
            email = random.choice(emails)
            year = '2020'
            month = random.choice(range(1, 12))
            day = random.choice(range(1, 29))
            torcv = year + '-' + str(month) + '-' + str(day)
            todef = year + '-' + str(month) + '-' + str(day + random.choice([0, 1]))

            f.write(
                f"INSERT INTO order_info VALUES ('{order_id}','{email}','{torcv}','{todef}');\n")


def make_data_management(num):
    # INSERT INTO management VALUES ('Masud','m12345','Masud Rana','Active','Employee');
    cook_user_ids = []
    with open('database_insert.sql', 'a+') as f:
        for i in range(num):
            lname = random.choice(['Nguyen', 'Luu', 'Le', 'Phung', 'Lai', 'Pham'])
            mname = random.choice(['Van', 'Minh', 'Xuan', 'Duy', 'Hoang', 'Phuc', 'Quang', 'Hong'])
            fname = random.choice(['Hieu', 'Dat', 'Huyen', 'Dai', 'Long', 'Phuc', 'Quang', 'Truong'])
            name = lname + ' ' + mname + ' ' + fname
            user_id = str.lower(fname + lname + randnumber(3))
            user_pass = 'qwer1234'
            role = random.choice(['Cook', 'Employee'])
            if role == 'Cook': cook_user_ids.append(user_id)
            f.write(
                f"INSERT INTO management VALUES ('{user_id}','{user_pass}','{name}','Active','{role}');\n")
        f.write("INSERT INTO management VALUES ('lolicon1311','qwer1234','Nguyen Minh Hieu','Active','Manager');\n")
        f.write("INSERT INTO management VALUES ('datlt132','qwer1234','Luu Thanh Dat','Active','Manager');\n")
    return cook_user_ids


def make_data_menu():
    # INSERT INTO menu VALUES ('20001','Shami Kabab','Kabab',60,'Fastfood','Available','HasibIq');
    item_names = ['Ga Ran Gion', 'Ga Sot Dau', 'Pizza Ga', 'Burger Ga', 'Coca', 'Pepsi', 'Tra Dao', 'Tra Chanh',
                  'Tra Quat', 'Kem']
    descriptions = ['Ga', 'Ga', 'Ga', 'Ga', 'Co gas', 'Co gas', 'Khong gas', 'Khong gas', 'Khong gas', 'Kem tuoi']
    prices = [39000, 43000, 32000, 31000, 10000, 10000, 12000, 12000, 12000, 5000]
    with open('database_insert.sql', 'a+') as f:
        for i in range(10):
            item_id = i + 30000
            user_id = random.choice(['datlt132', 'lolicon1311'])
            f.write(
                f"INSERT INTO menu VALUES ('{item_id}','{item_names[i]}','{descriptions[i]}','{prices[i]}',\
                                            'fastfood', 'Available', '{user_id}');\n")


def make_data_order_items(num, cook_user_ids):
    max = 1000 + num
    # INSERT INTO order_items VALUES ('1000','20003',5,'Pending','Bahadur');
    with open('database_insert.sql', 'a+') as f:
        for order_id in range(2000, max + 1):
            item_id = random.choice(range(30000, 30011))
            number = random.choice(range(5, 21))
            status = random.choice(['Ready', 'Pending'])
            user = random.choice(cook_user_ids)
            f.write(
                f"INSERT INTO order_items VALUES ('{order_id}','{item_id}',{number},'{status}','{user}');\n")


if __name__ == '__main__':
    emails = make_data_customer_info(1000)
    make_data_order_info(8000, emails)
    cook_user_ids = make_data_management(50)
    make_data_menu()
    make_data_order_items(8000, cook_user_ids)
