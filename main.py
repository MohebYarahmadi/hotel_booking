import pandas

df = pandas.read_csv('hotels.csv', dtype={'id':str})


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        pass
        
    def book(self):
        """Books a hotel by changing it's availability to no"""
        df.loc[df['id'] == self.hotel_id, 'available'] = 'no'
        df.to_csv('hotels.csv', index=False)

    def is_available(self):
        """Check the availability of the provided hotel"""
        availability = df.loc[df['id'] == self.hotel_id, 'available'].squeeze()
        if availability == 'yes':
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_obj):
        pass
        
    def generate(self):
        pass


if __name__ == '__main__':
    print(df)
    hotel_ID = input('Enter an hotel id: ')
    hotel = Hotel(hotel_ID)
    if hotel.is_available():
        hotel.book()
        name = input('Enter your name: ')
        reservation_ticket = ReservationTicket(name, hotel)
        reservation_ticket.generate()
    else:
        print('Hotel is not available.')
