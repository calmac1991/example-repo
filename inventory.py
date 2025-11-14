from pathlib import Path

# ========The beginning of the class==========


class Shoe:

    def __init__(self, product_dict):
        """
        Initialise the Shoe object.

        Args:
            product_dict: Dictionary containing product details
                          Required keys:
                            "Country", "Code", "Product", "Cost", "Quantity"
        """

        self.country = product_dict["Country"]
        self.code = product_dict["Code"]
        self.product = product_dict["Product"]
        self.cost = int(product_dict["Cost"])
        self.quantity = int(product_dict["Quantity"])

    def get_cost(self):
        """
        Returns the cost of the shoe.
        """
        return self.cost

    def get_quantity(self):
        """
        Returns the stock quantity of the shoe.
        """
        return self.quantity

    def __str__(self):
        """
        Returns a string to display shoe details.
        """
        shoe_details = f"""Country: {self.country}
Code: {self.code}
Product: {self.product}
Cost: {self.cost}
Quantity: {self.quantity}"""

        return shoe_details

    def get_dict(self):
        """
        Returns a dictionary containing the shoe attributes. This is used to
        align the values with the column order in table_headers
        """

        shoe_dict = {
            "Country": self.country,
            "Code": self.code,
            "Product": self.product,
            "Cost": self.cost,
            "Quantity": self.quantity
        }

        return shoe_dict


# Create list to store the shoe objects
shoe_list = []
# Headers to use for the table of shoes
table_headers = ["Country", "Code", "Product", "Cost", "Quantity"]
# Location of inventory file
data_location = Path(__file__).parent / "inventory.txt"


def tabulate(table_rows, column_spacing=5, padding=0, vlines=False,
             hlines=False, header_line=False):
    """
    Takes an input list and formats as a table. I know there is a module which
    can be imported to do this but I wanted to try creating my own.

    Args:
        table_rows (list): List of lists representing individual table rows
        column_spacing (int): Spacing to add at the end of each column
        padding (int): Spacing to add before and after each column
        vlines (boolean): Adds vertical lines between columns
        hlines (boolean): Adds horizontal lines at the top and bottom
        header_line (boolean): Adds a line under the first row of the table

    Returns:
        string: A string representing the formatted table to be printed
    """

    longest_row = 0
    # Get longest row
    for row in table_rows:
        if len(row) > longest_row:
            longest_row = len(row)

    # Declare list for longest cell in each column and fill with zeros
    max_lengths = [0] * longest_row

    # Get longest cell in each column
    for row in table_rows:
        for i, cell in enumerate(row):
            if len(str(cell)) > max_lengths[i]:
                max_lengths[i] = len(str(cell))

    # Assemble string to print out horizontal line if required
    if hlines is True or header_line is True:
        hline_string = ""
        # Add the correct number of dashes based on the longest value in each
        # column of the table, plus spacing and padding
        for i, col_length in enumerate(max_lengths):
            num_dashes = 0
            # Adds extra + symbol if vlines are also enabled
            if vlines is True:
                hline_string += "+"
            num_dashes += max_lengths[i]
            num_dashes += column_spacing
            num_dashes += padding * 2
            hline_string += "-" * num_dashes

        # Adds extra + symbol if vlines are also enabled
        if vlines is True:
            hline_string += "+"

    # Begin assembling output table
    output_string = ""
    # Add horizontal line at start if required
    if hlines is True:
        output_string += hline_string + "\n"

    # Iterate through the table rows and assemble the string output
    for row_num, row in enumerate(table_rows):
        for i, cell in enumerate(row):
            if vlines is True:
                output_string += "|"
            # Calculate how much extra space needs to be added
            extra_space = max_lengths[i] - len(str(cell))
            preceding_space = " " * padding
            trailing_space = " " * padding + " " * column_spacing

            # Add extra space to align values
            # If the value is an integer, space is added in front of the
            # value to keep the numbers aligned
            if type(cell) is int:
                preceding_space += " " * extra_space
            else:
                trailing_space += " " * extra_space

            output_string += preceding_space + str(cell) + trailing_space

        # Add vertical line if required
        if vlines is True:
            output_string += "|"
        # Add new line character at the end of every line except the last
        if row_num < len(table_rows) - 1:
            output_string += "\n"

        # Add line after headers if required
        if row_num == 0 and header_line is True:
            output_string += hline_string + "\n"

    # Add horizontal line at end of table, if required
    if hlines is True:
        output_string += "\n" + hline_string

    return output_string


def read_shoes_data():
    """
    Reads the list of shoes from the inventory file and creates an instance of
    class Shoe for each.

    Returns:
        list: List of Shoe objects representing each item in the inventory
    """
    shoe_data = []

    # Open data file for reading
    try:
        with open(data_location, "r", encoding="utf-8") as data_file:
            file_lines = data_file.readlines()

    # Handle FileNotFoundError
    except FileNotFoundError:
        print("Inventory file not found.")
        return []

    # Get the list of field headers from the first row
    headers_row = file_lines[0].strip("\n").split(",")

    if len(file_lines[1:]) == 0:
        print("No shoes found in inventory file.")
        return []
    else:
        # Loop through remaining rows and separate into a list
        for line in file_lines[1:]:
            line = line.strip("\n")
            line_items = line.split(",")
            shoe_dictionary = {}

            # Store the data from the row in a dictionary using the field
            # headers as indices.
            # This accounts for the columns in the data file being in an
            # unexpected order.
            for i, item in enumerate(line_items):
                shoe_dictionary[headers_row[i]] = item

            shoe_data.append(shoe_dictionary)

        shoe_objects = []

        # Loop through the list of dictionaries and
        # create a shoe object for each
        for shoe in shoe_data:
            shoe_objects.append(Shoe(shoe))

        return shoe_objects


def capture_shoes():
    """
    Allows a user to capture data about a shoe and appends to the list of shoe
    objects. The updated list is written to the inventory file.
    """

    while True:
        # Ask the user to enter the country
        while True:
            country = input("Please enter the country: ").strip()

            # Check for empty string
            if len(country) == 0:
                print("Country cannot be empty. Please try again.")
                continue
            else:
                break

        # Ask the user to enter the SKU
        while True:
            code = input("Please enter the SKU: ").upper().strip()

            # Check for empty string and invalid SKU
            if len(code) == 0:
                print("SKU cannot be empty. Please try again.")
                continue
            # Check for code not beginning with "SKU"
            elif code[0:3] != "SKU":
                print("SKU must start with 'SKU'. Please try again.")
                continue
            else:
                break

        # Ask the user to enter the product name
        while True:
            product = input("Please enter the product name: ").strip()

            # Check for empty string
            if len(product) == 0:
                print("Product name cannot be empty. Please try again.")
                continue
            else:
                break

        # Ask the user to enter the cost
        while True:
            try:
                cost = int(input("Please enter the product cost: "))
            except ValueError:
                print("Product cost must be an integer. Please try again.")
                continue

            if cost == 0:
                print("Product cost cannot be nil. Please try again.")
                continue
            else:
                break

        # Ask the user to enter the quantity
        while True:
            try:
                quantity = int(input("Please enter the quantity: "))
                break
            except ValueError:
                print("Quantity must be an integer. Please try again.")

        # Create a dictionary with the user input to initialise the Shoe
        # object
        shoe_dict = {
            "Country": country,
            "Code": code,
            "Product": product,
            "Cost": cost,
            "Quantity": quantity
        }

        # Create a new shoe object and append to the list of shoes
        new_shoe = Shoe(shoe_dict)
        shoe_list.append(new_shoe)
        print("Shoe added:")
        print(new_shoe)

        # Give user the option to add another shoe
        add_another = input("Add another shoe (Y/N)? ").lower()
        if add_another in ("y", "yes"):
            continue
        else:
            break

    # Write the updated list to the inventory file
    update_file()


def view_all():
    """
    Displays details for all shoes in the list of shoes in table format,
    sorted alphabetically by product name.
    """

    # Sort shoes alphabetically by product name
    shoe_list.sort(key=lambda shoe: shoe.product)

    # Add headers to output table
    output_table = [table_headers]
    # Iterate through list of shoes and append each row of details to the
    # table. Dictionary is used to allow for differing order of headers
    for shoe_item in shoe_list:
        row_dict = shoe_item.get_dict()
        row_list = []
        # Iterate through the table headers and append the corresponding fields
        # to the table row
        for field in table_headers:
            row_list.append(row_dict[field])

        # Append the row to the table
        output_table.append(row_list)

    # Print in table form
    print(tabulate(output_table, 5, 0, False, True, True))


def re_stock():
    """
    Shows the shoe with the lowest stock level and gives the user the option
    to add to the quantity. The updated value is written to the inventory file.
    """

    # Find the shoe with the lowest stock level
    min_shoe = min(shoe_list, key=lambda shoe: shoe.get_quantity())

    # Print details of lowest stock shoe
    print("-" * 50)
    print("Lowest stock: ")
    print(min_shoe)
    print("-" * 50)

    update = input("Re-stock this shoe (Y/N)? ").lower()

    # If user wishes to restock, get quantity to add and validate
    if update in ("y", "yes"):
        while True:
            try:
                new_quantity = int(input("How many do you want to add? "))
            except ValueError:
                print("Quantity must be an integer. Please try again.")
                continue

            if new_quantity < 0:
                print("Quantity must be a positive number. Please try again.")
                continue
            else:
                break

        # Add the new quantity to the existing quanity and print the new value
        min_shoe.quantity += new_quantity
        print(f"Quantity updated. New quantity: {min_shoe.quantity}")

        # Save the updated list to the inventory file
        update_file()


def search_shoe():
    """
    Allows the user to search for a shoe by product code and returns the found
    Shoe object.

    Returns:
        Object (Shoe): Returns object representing the found shoe.
                       Returns None if no shoe is found.
    """

    while True:
        # Ask user to input product code to search for and validate
        search_code = input("Please enter the product code to search for: ")
        search_code = search_code.upper()
        if search_code[0:3] != "SKU":
            print("Product code must start with 'SKU'. Please try again.")
            continue
        elif search_code == "":
            print("Product code cannot be blank. Please try again.")
            continue

        found_shoe = None

        # Use sequential search to locate matching product code
        for shoe in shoe_list:
            if shoe.code == search_code:
                found_shoe = shoe
                break

        # If no shoe was found, give user option to try again
        if found_shoe is None:
            search_again = input("The chosen shoe was not found. Try again " +
                                 "(Y/N)? ")
            if search_again.lower() in ("y", "yes"):
                continue
            else:
                break
        else:
            break

    return found_shoe


def value_per_item():
    """
    Calculates the total value for each item in the list of shoes and displays
    the sorted results in a table with a total row at the end.
    """

    values_table = []
    # Define headers to use for output table
    headers_row = ["Code", "Product", "Cost", "Quantity", "Total Value"]

    # Declare variable to use as a running total
    total_value = 0

    # Iterate through shoe_list, calculate shoe value and append row to the
    # output table
    for shoe in shoe_list:
        shoe_dict = shoe.get_dict()
        shoe_value = shoe.get_cost() * shoe.get_quantity()
        total_value += shoe_value
        values_table.append([
            shoe_dict["Code"],
            shoe_dict["Product"],
            shoe_dict["Cost"],
            shoe_dict["Quantity"],
            shoe_value
        ])

    # Sort table by total value
    values_table.sort(key=lambda row: row[4], reverse=True)
    # Insert headers row
    values_table.insert(0, headers_row)

    # Add overall total to the end of the table
    values_table.append([""]*5)
    values_table.append([
        "",
        "",
        "",
        "TOTAL:",
        total_value
    ])

    # Print in table format
    print(tabulate(values_table, hlines=True, header_line=True))


def highest_qty():
    """
    Finds and displays the shoe with the highest stock level to be put on sale.
    """
    # Find the shoe with the highest stock level
    max_shoe = max(shoe_list, key=lambda shoe: shoe.get_quantity())

    print("-" * 50)
    print("SALE")
    print("-" * 50)
    print("Highest stock shoe:")
    print(max_shoe)
    print("-" * 50)


def update_file():
    """
    Overwrites the inventory file with the details held in the list of shoes.
    """

    # List of lines to write to file
    file_lines = []
    # Add table headers to output list
    file_lines.append(",".join(table_headers))

    # Iterate through list of shoes and add each as a new line
    # Dictionary is used to ensure alignment with header order
    for shoe_item in shoe_list:
        row_dict = shoe_item.get_dict()
        row_list = []
        for field in table_headers:
            row_list.append(str(row_dict[field]))

        # Add the current row to the output list
        file_lines.append(",".join(row_list))

    # Generate string to write to file
    file_str = "\n".join(file_lines)

    # Open data file for writing
    try:
        with open(data_location, "w", encoding="utf-8") as data_file:
            data_file.write(file_str)

    # Handle errors
    except Exception:
        print("An error occurred while writing to the file.")
    else:
        print("Data file updated.")


# ==========Main Menu=============

# Read shoe data from inventory file. This is only done once as the
# file is updated any time the shoe details are changed.
shoe_list = read_shoes_data()

# Begin menu loop
while True:

    # Check for empty list and prompt to add shoe
    # Menu displays with reduced options if no shoes are added
    if len(shoe_list) == 0:
        input_shoe = input("Add a shoe now (Y/N)? ").lower()

        if input_shoe in ("y", "yes"):
            capture_shoes()
            continue
        else:
            menu = [
                ["", "Main Menu:"],
                [1, "Add a new shoe"],
                [2, "Exit"]
            ]

        print(tabulate(menu, 0, 5, hlines=True, header_line=True))
        try:
            option = int(input("Please select an option: "))
        except ValueError:
            input("Chosen option must be an integer. Press enter to return " +
                  "to menu.")
            continue

        if option == 1:
            capture_shoes()
            input("Press enter to return to menu.")

        elif option == 2:
            break

        else:
            input("Invalid choice. Press enter to return to menu.")

    else:
        menu = [
            ["", "Main Menu:"],
            [1, "List all shoes"],
            [2, "Re-stock"],
            [3, "Add a new shoe"],
            [4, "Search shoes"],
            [5, "Display stock values"],
            [6, "Display highest quantity shoe"],
            [7, "Exit"]
        ]

        print(tabulate(menu, 0, 5, hlines=True, header_line=True))
        try:
            option = int(input("Please select an option: "))
        except ValueError:
            input("Chosen option must be an integer. Press enter to return" +
                  "to menu.")
            continue

        if option == 1:
            view_all()
            input("Press enter to return to menu.")

        elif option == 2:
            re_stock()
            input("Press enter to return to menu.")

        elif option == 3:
            capture_shoes()
            input("Press enter to return to menu.")

        elif option == 4:
            found_shoe = search_shoe()
            if found_shoe is None:
                print("No shoes found with the chosen product code.")
            else:
                print("-" * 50)
                print("Shoe found:")
                print(found_shoe)
                print("-" * 50)
            input("Press enter to return to menu.")

        elif option == 5:
            value_per_item()
            input("Press enter to return to menu.")

        elif option == 6:
            highest_qty()
            input("Press enter to return to menu.")

        elif option == 7:
            break

        else:
            input("Invalid choice. Press enter to return to menu.")
