# Recieve an invoice and calcuate the ammount owed.


def proces(invoice):
    """Retreive teh line items and seperate them by catagory."""
    lenght = len(invoice.items)  # occured
    if lenght == 0:
        return 0  # nothing to bill, this is sucessful
    return sum(item.total for item in invoice.items)
