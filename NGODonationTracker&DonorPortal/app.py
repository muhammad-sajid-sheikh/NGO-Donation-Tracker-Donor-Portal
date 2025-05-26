import streamlit as st
import pandas as pd
import os
from donor import Donor
from donation import Donation
from receipt import generate_receipt
from utils import create_pdf_receipt

DONOR_FILE = "data/donors.csv"
DONATION_FILE = "data/donations.csv"

# Ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

st.set_page_config(page_title="NGO Donation Tracker", layout="centered")
st.title("🤝 NGO Donation Tracker")

# Add New Donation
st.header("Make a Donation")
name = st.text_input("Full Name")
email = st.text_input("Email")
amount = st.number_input("Donation Amount (Rs.)", min_value=100, step=50)
method = st.selectbox("Payment Method", ["JazzCash", "Easypaisa", "Bank Transfer"])

if st.button("Donate Now"):
    donor = Donor(name, email)
    donation = Donation(email, amount, method)

    # Save donor
    donor_df = pd.DataFrame([donor.to_dict()])
    try:
        if os.path.exists(DONOR_FILE) and os.path.getsize(DONOR_FILE) > 0:
            existing_donors = pd.read_csv(DONOR_FILE)
            donor_df = pd.concat([existing_donors, donor_df], ignore_index=True)
    except pd.errors.EmptyDataError:
        # File is empty, so keep donor_df as is
        pass
    donor_df.drop_duplicates(subset=["Email"], inplace=True)
    donor_df.to_csv(DONOR_FILE, index=False)

    # Save donation
    donation_df = pd.DataFrame([donation.to_dict()])
    try:
        if os.path.exists(DONATION_FILE) and os.path.getsize(DONATION_FILE) > 0:
            existing_donations = pd.read_csv(DONATION_FILE)
            donation_df = pd.concat([existing_donations, donation_df], ignore_index=True)
    except pd.errors.EmptyDataError:
        # File is empty, so keep donation_df as is
        pass
    donation_df.to_csv(DONATION_FILE, index=False)

    # Generate PDF Receipt
    receipt_path = create_pdf_receipt(donation.to_dict(), filename=f"receipt_{email}.pdf")

    # Show success + text receipt
    st.success("🎉 Donation Successful!")
    st.text(generate_receipt(donation.to_dict()))

    # Download button
    with open(receipt_path, "rb") as pdf_file:
        st.download_button("📥 Download PDF Receipt", pdf_file, file_name="donation_receipt.pdf")

# View Donation History
st.header("🔍 View My Donation History")

history_email = st.text_input("Enter your Email to View History")

if st.button("View My History") and history_email:
    try:
        if os.path.exists(DONATION_FILE) and os.path.getsize(DONATION_FILE) > 0:
            all_donations = pd.read_csv(DONATION_FILE)
            user_donations = all_donations[all_donations["Donor Email"] == history_email]

            if user_donations.empty:
                st.warning("No donations found for this email.")
            else:
                st.success(f"Found {len(user_donations)} donations.")

                for i, row in user_donations.iterrows():
                    with st.expander(f"Donation on {row['Date']} - Rs. {row['Amount']}"):
                        st.write(f"**Amount:** Rs. {row['Amount']}")
                        st.write(f"**Payment Method:** {row['Method']}")
                        st.write(f"**Date:** {row['Date']}")

                        # Generate receipt again (safe if it was deleted)
                        donation_data = row.to_dict()
                        filename = f"receipt_{row['Donor Email'].replace('@','_')}_{i}.pdf"
                        path = create_pdf_receipt(donation_data, filename)

                        with open(path, "rb") as pdf_file:
                            st.download_button(
                                label="📥 Download Receipt",
                                data=pdf_file,
                                file_name=filename,
                                key=f"download_{i}"
                            )
        else:
            st.warning("No donation records found yet.")
    except pd.errors.EmptyDataError:
        st.warning("No donation records found yet.")

# Admin Panel
st.header("🛠️ Admin Panel (Overview)")

admin_pass = st.text_input("Enter Admin Code", type="password")

if admin_pass == "admin123":  # You can change this to a stronger pass
    try:
        if os.path.exists(DONOR_FILE) and os.path.getsize(DONOR_FILE) > 0:
            donors_df = pd.read_csv(DONOR_FILE)
        else:
            donors_df = pd.DataFrame()

        if os.path.exists(DONATION_FILE) and os.path.getsize(DONATION_FILE) > 0:
            donations_df = pd.read_csv(DONATION_FILE)
        else:
            donations_df = pd.DataFrame()

        total_donations = donations_df["Amount"].sum() if not donations_df.empty else 0
        total_donors = donors_df["Email"].nunique() if not donors_df.empty else 0
        recent_donations = donations_df.sort_values(by="Date", ascending=False).head(10) if not donations_df.empty else pd.DataFrame()

        st.subheader("📊 Stats")
        col1, col2 = st.columns(2)
        col1.metric("Total Donations", f"Rs. {total_donations:,.0f}")
        col2.metric("Total Donors", total_donors)

        st.subheader("🧾 Recent Donations")
        if not recent_donations.empty:
            st.dataframe(recent_donations)
        else:
            st.write("No donation records available.")

    except pd.errors.EmptyDataError:
        st.error("No donor or donation data found yet.")
elif admin_pass != "":
    st.error("Incorrect Admin Code.")
