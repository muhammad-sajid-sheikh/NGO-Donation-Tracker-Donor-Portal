def generate_receipt(donation_data):
    return f"""
    === DONATION RECEIPT ===
    Donor Email: {donation_data['Donor Email']}
    Amount: Rs. {donation_data['Amount']}
    Payment Method: {donation_data['Method']}
    Date: {donation_data['Date']}
    ---------------------------
    Thank you for supporting our cause!
    """
