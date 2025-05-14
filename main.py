import pandas

df = pandas.read_csv('hotels.csv', dtype={'id':str})


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
        availability = df.loc[df['id'] == self.hotel_id, 'available'].squeeze()
        if availability == 'yes':
            return True
        else:
            return False

    def get_name(self):
        return self.name


class ReservationTicket:
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


if __name__ == '__main__':
    print(df)
    hotel_ID = input('Enter an hotel id: ')
    hotel = Hotel(hotel_ID)
    if hotel.is_available():
        hotel.book()
        name = input('Enter your name: ')
        reservation_ticket = ReservationTicket(customer_name=name, hotel_obj=hotel)
        print(reservation_ticket.generate())
    else:
        print('Hotel is not available.')
