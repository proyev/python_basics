import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS card(
                id INTEGER PRIMARY KEY,
                number TEXT NOT NULL,
                pin TEXT NOT NULL,
                balance INTEGER DEFAULT 0
    );"""
)
conn.commit()


def luhn(account_id):
    bin_num = []
    for i in range(15):
        num = int(account_id[i])
        if i % 2 == 0:
            num *= 2
            if num > 9:
                num -= 9
        bin_num.append(num)
    checksum = (10 - sum(bin_num) % 10) % 10
    return str(checksum)


class Account:

    def __int__(self):
        self.account_num = None
        self.account_pin = None
        self.balance = None

    def create_account(self):

        random.seed()

        # card number
        account_id = random.sample(range(10), 9)
        account_id = [str(num) for num in account_id]
        account_id = '400000' + ''.join(account_id)
        self.account_num = int(account_id + luhn(account_id))

        # PIN
        pin = random.sample(range(10), 4)
        pin = [str(num) for num in pin]
        self.account_pin = ''.join(pin)
        self.balance = 0

        cur = conn.cursor()
        cur.execute(f'INSERT INTO card (number, pin) VALUES ({self.account_num}, {self.account_pin});')
        conn.commit()

        print('Your card has been created')
        print(f'Your card number:\n{self.account_num}')
        print(f'Your card PIN:\n{self.account_pin}')

    def log_account(self, card_num, pin):
        cur = conn.cursor()
        cur.execute(f'SELECT number={card_num}, pin={pin} FROM card;')
        account_pins = cur.fetchall()
        conn.commit()
        for per_data in account_pins:
            if per_data[0] == 1 and per_data[1] == 1:
                print('You have successfully logged in!')
                account_info(card_num)
        else:
            print('Wrong card number or PIN!')
            menu()


def menu():
    print('1. Create an account\n2. Log into account\n0. Exit')
    user_input = int(input())
    if user_input == 1:
        Account().create_account()
        menu()
    elif user_input == 2:
        log_in()
        menu()
    elif user_input == 0:
        print('Bye!')
        exit()


def log_in():
    print('Enter your card number:')
    card_num = int(input())
    print('Enter your PIN:')
    pin = input()
    Account().log_account(card_num, pin)


def check_account(card_num, transfer_card_num):
    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM card
                    WHERE number={transfer_card_num}''')

    check = cur.fetchone()
    conn.commit()
    check_number = transfer_card_num[:-1]
    check_sum = transfer_card_num[-1]

    if int(luhn(check_number)) != int(check_sum):
        print('Probably you made a mistake in the card number. Please try again!')
        account_info(card_num)
    else:
        if check == None:
            print('Such a card does not exist.')
            account_info(card_num)
        else:
            cur.execute(f'''SELECT * FROM card
                                WHERE number={transfer_card_num}''')
            id, number, pin, balance = cur.fetchone()
            conn.commit()
            print('Transfer')
            print('Enter how much money you want to transfer:')
            transfer_amount = int(input())
            cur.execute(f'''SELECT * FROM card
                            WHERE number = {card_num}''')
            from_id, from_number, from_pin, from_balance = cur.fetchone()
            conn.commit()
            if from_balance < transfer_amount:
                print('Not enough money!')
                account_info(card_num)
            else:
                cur.execute(f'''DELETE FROM card
                                WHERE id = {id}
                                    AND number = {number}
                                    AND pin = {pin}
                                    AND balance = {balance};''')
                conn.commit()
                cur.execute(f'''DELETE FROM card
                                                WHERE id = {from_id}
                                                    AND number = {from_number}
                                                    AND pin = {from_pin}
                                                    AND balance = {from_balance};''')
                conn.commit()
                balance += transfer_amount
                from_balance -= transfer_amount
                cur.execute(f'''INSERT INTO card
                                VALUES ({id}, {number}, {pin}, {balance}),
                                        ({from_id}, {from_number}, {from_pin}, {from_balance});''')
                conn.commit()
                print('Success!')
                account_info(card_num)


def account_info(card_num):
    print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log account\n0. Exit')
    user_input = int(input())
    if user_input == 1:
        cur.execute(f'''SELECT balance FROM card
                        WHERE (number = {card_num});''')
        balance = cur.fetchone()
        conn.commit()
        print('Balance:', balance[0])
        account_info(card_num)
    elif user_input == 2:
        print('Enter income:')
        income = int(input())
        cur.execute(f'''SELECT * FROM card
                        WHERE (number = {card_num});''')
        id, number, pin, balance = cur.fetchone()
        balance += income
        cur.execute(f'DELETE FROM card WHERE number = {card_num}')
        conn.commit()
        cur.execute(f'INSERT INTO card (id, number, pin, balance) VALUES ({id}, {number}, {pin}, {balance});')
        conn.commit()
        print('Income was added!')
        account_info(card_num)
    elif user_input == 3:
        print('Enter card number:')
        transfer_card_num = input()
        check_account(card_num, transfer_card_num)


    elif user_input == 4:
        cur.execute(f'DELETE FROM card WHERE number = {card_num};')
        conn.commit()
        menu()

    elif user_input == 5:
        print('You have successfully logged out!')
        menu()
    elif user_input == 0:
        print('Bye!')
        exit()


menu()

