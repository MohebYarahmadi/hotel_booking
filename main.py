import pandas
from abc import ABC, abstractmethod

df = pandas.read_csv('hotels.csv', dtype={'id': str})
df_cards = pandas.read_csv('cards.csv', dtype=str).to_dict(orient='records')
df_sec = pandas.read_csv('card_security.csv', dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df['id'] == self.hotel_id, 'name'].squeeze()

    def book(self):
        """Books a hotel by changing it's availability to no"""
        df.loc[df['id'] == self.hotel_id, 'available'] = 'no'
        df.to_csv('hotels.csv', index=False)

    def is_available(self):
        """Check the availability of the provided hotel"""
        if self.hotel_id in df['id'].values:
            availability = df.loc[df['id'] ==
                                  self.hotel_id, 'available'].squeeze()
            if availability == 'yes':
                return True
            else:
                return False

    def get_name(self):
        return self.name


class Spa(Hotel):
    def book(self):
        pass


class Ticket(ABC):
    @abstractmethod
    def generate(self):
        pass


class ReservationTicket(Ticket):
    def __init__(self, customer_name, hotel_obj):
        self.customer_name = customer_name
        self.hotel = hotel_obj

    def generate(self):
        content = f"""
        Thank you for your reservation.
        Here is your reservation ticket info:
        Guest Name: {self.customer_name}
        Hotel Name: {self.hotel.get_name()}
        """
        return content


class CreditCard:
    def __init__(self, card_number):
        self.card_number = card_number

    def validate(self, holder, expiration, cvc):
        card_info = {"number": self.card_number,
                     "expiration": expiration,
                     "cvc": cvc,
                     "holder": holder}
        if card_info in df_cards:
            return True
        else:
            return False


class CreditCardSecurity(CreditCard):
    def authenticate(self, given_password):
        password = df_sec.loc[df_sec['number'] ==
                              self.card_number, 'password'].squeeze()
        if password == given_password:
            return True
        else:
            return False


def main():
    print(df)
    hotel_ID = input('Enter an hotel id: ')
    hotel = Hotel(hotel_ID)
    spa = Spa(hotel_ID)
    if hotel.is_available():
        pay = CreditCardSecurity(card_number='1234567890123456')
        if pay.validate(holder='JANE SMITH',
                        expiration='12/28',
                        cvc='456'):
            if pay.authenticate(given_password='mypass'):
                hotel.book()
                name = input('Enter your name: ')
                reservation_ticket = ReservationTicket(
                    customer_name=name,
                    hotel_obj=hotel
                )
                print(reservation_ticket.generate())
                ask = input("Are you ready for spa: ")
                if ask == 'yes':
                    spa.book()
                    spa_reservation_ticket = ReservationTicket(
                        customer_name=name,
                        hotel_obj=spa
                    )
                else:
                    print('Hope you enjoy')
                print(spa_reservation_ticket.generate())
            else:
                print('Credit card authentication failed.')
        else:
            print('Something wrong with your payment information.')
    else:
        print('Hotel is not available.')


if __name__ == '__main__':
    main()
