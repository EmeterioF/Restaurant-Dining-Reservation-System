# EMETERIO FIGURACION RESTAURANT RESERVATION SYSTEM 2BSIT-2

class Reservation:
    # constants para sa ADULT and CHILD prices
    ADULT_PRICE = 500
    KIDS_PRICE = 300

    next_id = 1

    # constructor
    def __init__(self, name, date, time, adults, kids, id=None):
        if id is None:
            self.id = Reservation.next_id
            Reservation.next_id += 1
        else:
            self.id = id

        self.name = name
        self.date = date
        self.time = time
        self.adults = adults
        self.kids = kids
        self.subtotal = self.calculate_subtotal()

    # function para ma calculate subtotal ng instance ng object ng reservation
    def calculate_subtotal(self):
        adult_price_subtotal = self.ADULT_PRICE * self.adults
        kids_price_subtotal = self.KIDS_PRICE * self.kids
        subtotal = adult_price_subtotal + kids_price_subtotal
        return subtotal

    # para sa pag display ng reservation object as a string
    def to_string(self):
        return f"{self.id}\t\t\t\t{self.date}\t\t\t{self.time}\t\t\t{self.name}\t\t\t{self.adults}\t\t\t\t{self.kids}"

    # coverting ng object to string for saving sa file
    def to_file_string(self):
        return f"{self.id},{self.date},{self.time},{self.name},{self.adults},{self.kids}"

    # converting ng string na galing sa file para makagawa ng bagong object hihi
    @classmethod
    def from_file_string(cls, file_string):
        parts = file_string.strip().split(",")
        reservation_id = int(parts[0])
        date = parts[1]
        time = parts[2]
        name = parts[3]
        adults = int(parts[4])
        kids = int(parts[5])
        return cls(name, date, time, adults, kids, reservation_id)


class ReservationSystem: #dito yung main system na nag mamamange ng reservation. dito rin naten gagamtin si Reservation class
    def __init__(self):
        self.reservations = []
        self.filename = "reservations.txt"
        self.load_reservations()  # Then load reservations into it

    def add_reservation(self, name, date, time, adults, kids):  # function para sa adding ng reservation
        new_reservation = Reservation(name, date, time, adults, kids)
        self.reservations.append(new_reservation)
        self.save_reservations()
        return new_reservation.id  # Return the ID for confirmation

    def get_reservation(self, id):
        """Find a reservation by ID"""
        for reservation in self.reservations:
            if reservation.id == id:
                return reservation
        return None  # Return None if not found

    def delete_reservation(self, id):  # function para sa deletion ng reservations
        reservation = self.get_reservation(id)
        if reservation is not None:
            self.reservations.remove(reservation)
            self.save_reservations()
            return True
        return False

    def save_reservations(self):  # function to save current changes
        try:
            with open(self.filename,
                      "w") as file:  # I use with here to close the file automatically. it is more concise and short ^^
                for reservation in self.reservations:
                    file.write(reservation.to_file_string() + "\n")
        except Exception as e:
            print(f"Error saving reservations: {e}")

    def load_reservations(self):  # yung function na ito is for the program to have all the data from the file
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    if line.strip():  # Skip empty lines
                        self.reservations.append(
                            Reservation.from_file_string(line)
                        )
                # Update next_id
                if self.reservations:
                    max_id = max(r.id for r in self.reservations)
                    Reservation.next_id = max_id + 1
        except FileNotFoundError:
            pass  # It's okay if the file doesn't exist yet
        except Exception as e:
            print(f"Error loading reservations: {e}")

    def view_reservation(self):
        if not self.reservations:  # print na wala pang reservation kapag empty yung list
            print("\nNO RESERVATIONS MADE YET\n")
            return

        print(f"\n#\t\t\t\tDATE\t\t\t\tTIME\t\t\t\tNAME\t\t\t\t\t\tADULTS\t\t\tCHILDREN")
        for reservation in self.reservations:
            print(reservation.to_string())
        print("")

    def generate_report(self):
        if not self.reservations:  # print na wala pang reservation kapag empty yung list
            print("\nNO RESERVATIONS TO REPORT\n")
            return

        total = 0
        adults = 0
        kids = 0
        print("\n\t\t\t\t\t\t\t\t\t\t\t\t\tREPORT\n")
        print("#\t\t\t\tDATE\t\t\t\tTIME\t\t\t\tNAME\t\t\t\tADULTS\t\t\t\tCHILDREN\t\t\t\tSUBTOTAL")
        for reservation in self.reservations:
            print(f"{reservation.to_string()}\t\t\t\t₱{reservation.subtotal}")
            total += reservation.subtotal
            adults += reservation.adults
            kids += reservation.kids
        print(f"\nTotal number of Adults: {adults}")
        print(f"\nTotal number of Kids: {kids}")
        print(f"\nGrand Total: ₱{total}\n")


def validate_date(date):
    parts = date.split('/')
    if len(parts) != 3:
        return False
    try:
        month, day, year = map(int, parts)

        return 1 <= month <= 12 and 1 <= day <= 31 and 1000 <= year <= 9999
    except ValueError:
        return False


def validate_time(time):
    if "AM" not in time and "PM" not in time:
        return False

    try:
        time_part = time.split()[0]
        hours, minutes = map(int, time_part.split(':'))
        return 1 <= hours <= 12 and 0 <= minutes <= 59
    except (ValueError, IndexError):
        return False


def make_reservation(system):
    print("\n----- Make a Reservation -----")
    name = input("Enter name: ")

    # Validate date
    while True:
        date = input("Enter date (MM/DD/YYYY): ")
        if validate_date(date):
            break
        print("Invalid date format. Please use MM/DD/YYYY.")

    # Validate time
    while True:
        time = input("Enter time (HH:MM AM/PM): ")
        if validate_time(time):
            break
        print("Invalid time format. Please use HH:MM AM/PM.")

    try:
        adults = int(input("Enter number of adults: "))
        kids = int(input("Enter number of kids: "))

        if adults < 0 or kids < 0:
            print("Number of guests cannot be negative.")
            return

        if adults == 0 and kids == 0:
            print("At least one guest is required.")
            return

        reservation_id = system.add_reservation(name, date, time, adults, kids)
        print(f"Reservation created successfully! Your reservation ID is: {reservation_id}")
    except ValueError:
        print("Please enter valid numbers for guests.")


def main():
    system = ReservationSystem()

    while True:
        #main menu UI
        print(""" 
========================================================
  RESTAURANT RESERVATION SYSTEM BY EMETERIO FIGURACION
========================================================

        SYSTEM MENU

        a. VIEW ALL RESERVATION
        b. MAKE RESERVATION
        c. DELETE RESERVATION
        d. GENERATE REPORT
        e. EXIT
========================================================
""")
        #getting the choices of the user
        try:
            choice = input("ENTER YOUR CHOICE [a - e]: ").lower()

            if choice == "a":
                system.view_reservation()
            elif choice == "b":
                make_reservation(system)
            elif choice == "c":
                if not system.reservations:
                    print("\nNO RESERVATIONS TO DELETE\n")
                else:
                    try:
                        res_id = int(input("Enter reservation ID to delete: "))
                        if system.delete_reservation(res_id):
                            print(f"Reservation {res_id} deleted successfully.")
                        else:
                            print(f"Reservation {res_id} not found.")
                    except ValueError:
                        print("Please enter a valid numeric ID.")
            elif choice == "d":
                system.generate_report()
            elif choice == "e":
                print("\nTHANK YOU FOR USING OUR APP!")
                break
            else:
                print("WRONG INPUT only use letters from [a to e]")
                continue
        except ValueError:
            print("not a valid choice")

if __name__ == "__main__":
    main()

#I hereby declare that all of the codes here are my code