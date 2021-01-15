import psycopg2
from tabulate import tabulate
from datetime import date


def connect_to_db(DB_NAME, DB_USER, DB_PASS, DB_HOST):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    return conn


def disconnect_to_db(conn):
    conn.close()


def query(conn, query_string):
    lst = []
    with conn.cursor() as cur:
        cur.execute(query_string)
        lst.append(cur.fetchall())
        conn.commit()
    return lst


def insert(conn, query_string):
    check = 1
    try:
        with conn.cursor() as cur:
            cur.execute(query_string)
            conn.commit()
            print("Successfully!")
            return check
    except (Exception, psycopg2.Error) as error:
        if conn:
            check = 0
            print("Failed to insert record", error)
            return check


def check_account(conn, username, userpass):
    customer_info = query(conn, "select email, pass, fname, status from customer_info")
    check = 0
    for account in customer_info:
        for user in account:
            if username == user[0] and userpass == user[1]:
                if user[3] == 'Active':
                    check = 1
                    name = user[2]
                    print(f"Login sucessfully!\n Hello, {name}!")
                    break
                else:
                    check = 0
                    print("Your account has been blocked!")
                    print("Because you cancel orders too much!")
                    break
    if check == 0:
        print("Username or password is incorrect!")

    return check


def customer_login(conn):
    username = input("Enter your email: ")
    userpass = input("Enter your password: ")
    i = check_account(conn, username, userpass)
    select = 5,
    count = 0
    while i == 0 and count < 3:
        print("Please enter again!")
        username = input("Enter your email: ")
        userpass = input("Enter your password: ")
        i = check_account(conn, username, userpass)
        count += 1
    if count == 3:
        char = input("Do you want to create a new account! (y/n)")
        while char != 'y' and char != 'n':
            char = input("Do you want to create a new account! (y/n)")
        if char == 'n':
            print("Goodbye!")
            return
        else:
            check = 0
            while check != 1:
                email = input("Enter your email:")
                if '@' not in email:
                    email = input("Your email is wrong! Enter again:")
                fname = input("Enter your firstname:")
                lname = input("Enter your lastname:")
                password = input("Enter your password:")
                phone = input("Enter your phone number:")
                if len(phone) == 11:
                    phone= input("Your phone number is wrong! Please enter again:")
                city = input("Enter your city:")
                town = input("Enter your town:")
                check = insert(conn, f"INSERT INTO customer_info VALUES ('{email}','{fname}','{lname}','{password}','{phone}','{city}','{town}','Active');")

    while select != 5:
        print("-----------Chon chuc nang:----------\n")
        print("1. Thong tin ca nhan")
        print("2. Xem lai cac don hang")
        print("3. Dat hang")
        print("4. Kiem tra don hien tai")
        print("5. Thoat\n")
        select = int(input("Nhap lua chon cua ban: "))
        if select == 1 : show_info_customer(conn, username)
        elif select == 2 : show_old_order(conn, username)
        elif select == 3 : order(conn, username)
        elif select == 4 : check_present_order(conn, username)
        while select < 1 or select > 6:
            print("Lua chon khong hop le!")
            select = input("Nhap lua chon cua ban: ")


def show_info_customer(conn, email):
    lst = query(conn, f"select email, fname, lname, phone, area, town from customer_info where email = '{email}';")
    for items in lst:
        for item in items:
            print("------------------------------------")
            print(f"Email: {item[0]}")
            print(f"First Name: {item[1]}")
            print(f"Last Name: {item[2]}")
            print(f"Phone number: {item[3]}")
            print(f"Area: {item[4]}")
            print(f"Town: {item[5]}")
            print("------------------------------------")
            r = input("Press ENTER to continue!")


def show_old_order(conn, email):
    lst = query(conn, f"select email, item_name, quantity, torcv as order_date\
                        from order_info oi, order_items ot, menu n\
                        where oi.order_id = ot.order_id and ot.item_id = n.item_id\
                            and email = '{email}'")
    # print(lst)
    if lst == [[]]:
        print("You haven't order yet!\n")
    else:
        for items in lst:
            print(tabulate(items, headers=['Email', 'Item Name', 'Quantity', 'Order date']))
            print('\n')
        r = input("Press ENTER to continue!")


def order(conn, username):
    menu = query(conn, "select item_id, item_name, description, price, catagory\
                        from menu\
                        where status = 'Available'")
    item_ids = []
    item_names = []
    prices = []
    for items in menu:
        print(tabulate(items, headers=['ID','Name', 'Description', 'Price', 'Category']))
        print('\n')
        for item in items:
            item_ids.append(item[0])
            item_names.append(item[1])
            prices.append(item[3])
    first_order_id = int((((query(conn, "select max(order_id) from order_info"))[0])[0])[0])
    while 1:
        item_id = input("Select your choice: ")
        while item_id not in item_ids:
            item_id = input("Wrong! Select your choice again: ")

        quantity = input("Quantity: ")
        while quantity.isdigit() is False:
            quantity = input("Wrong! Quantity: ")

        todel = input("Choose day you want to receive! (MM-DD)")
        todel = '2021-' + todel
        order_id_max = int((((query(conn, "select max(order_id) from order_info"))[0])[0])[0])

        order_id_next = order_id_max + 1
        try:
            a = insert(conn, f"insert into order_info values('{order_id_next}','{username}','{date.today()}','{todel}')")
        except Exception as e:
            print(e)
        try:
            user_id = query(conn, "select user_id\
                        from management\
                        where status != 'Blkd' and user_id in (\
                            select user_id\
                            from order_items\
                            where status = 'Pending'\
                            group by(user_id)\
                            order by(count(*))\
                            limit 1)")[0][0][0]
            # print(user_id)
            a = insert(conn, f" insert into order_items \
                                values('{order_id_next}','{item_id}',{quantity}, 'Pending','{user_id}')")
        except Exception as e:
            print(e)

        select = input("Do want to continue order? (y/n): ")
        if select == 'n':
            break
        else:
            continue
    export_bill(conn, username, first_order_id)
    r = input("Press ENTER to continue!")


def export_bill(conn, username, first_order_id):
    lst = query(conn, f"	select ot.order_id, email, item_name , quantity, quantity * price as price, ot.status\
                            from order_items as ot, order_info as oi, menu as m\
                            where ot.order_id = oi.order_id and email = '{username}'\
                                    and torcv <= '{date.today()}' and '{date.today()}' <= todel\
                                    and ot.item_id = m.item_id and ot.order_id > '{first_order_id}'\
                                    and ot.status != 'Cancel'")
    all_amount = 0
    for items in lst:
        print(tabulate(items, headers=['Order_id', 'Email', 'Name', 'Quantity', 'Price', 'Status']))
        for item in items:
            aaaa = item[4].replace('₫', '')
            all_amount = all_amount + float(aaaa)
    print(f"Total: {all_amount}")


def check_present_order(conn, username):
    export_bill(conn, username, 0)

    if input("Do you want to change?(y/n) :") == 'y':
        print("You only cancel order which status is Pending")
        cancel_id = input("Enter your cancel id: ")
        insert(conn, f" update order_items \
                        set status = 'Cancel'\
                        where order_id = '{cancel_id}'")

        check_present_order(conn, username)
    else:
        return


def main():
    conn = connect_to_db('res', 'postgres', 'admin', 'localhost')
    customer_login(conn)
    disconnect_to_db(conn)


if __name__ == '__main__':
    main()