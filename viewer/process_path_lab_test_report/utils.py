
#######################
# format_address_item #
#######################

def format_address_item(address_item=None):
    address=""
    if address_item.line is not None:
        for line in address_item.line:
            address+=line + ", "
    for address_part in (address_item.city, address_item.district, address_item.postalCode):
        if address_part is not None:
            address+=address_part+", "
    address=address.strip()
    return address

##############################
# output None as null string #
##############################

def format_None_to_null_string(item):
    if item is None:
        return ""
    else:
        return item