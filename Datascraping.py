#importing libraries
import requests
import pandas as pd

# Replace these with your own RapidAPI key and host
x_rapidapi_key = "ea1dace47fmsh2b2889e487740d7p187dc2jsnb7d164499b38"
x_rapidapi_host = "twitter135.p.rapidapi.com"

# Prompt user for a list of Twitter usernames (comma-separated)
usernames_input = input("Enter Twitter usernames (comma-separated): ")
usernames = [username.strip() for username in usernames_input.split(',')]

# Set up the RapidAPI endpoint for Twitter
api_url = f"https://{x_rapidapi_host}/v2/UserByScreenName/"

# Set up the request headers
headers = {
    "X-RapidAPI-Key": x_rapidapi_key,
    "X-RapidAPI-Host": x_rapidapi_host,
    "Accept": "application/json",
}

# Initialize an empty list to store user data
all_user_data = []

# Retrieve data for each user
for username in usernames:
    query_params = {"username": username}
    response = requests.get(api_url, headers=headers, params=query_params)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    # Check if the request was successful
    if response.ok:
        user_data = response.json()
        print(user_data)
        # Create a DataFrame with user data
        user_df = pd.DataFrame({
            "Username": [user_data["data"]["user"]["result"]["legacy"]["screen_name"]],
            "Full Name": [user_data["data"]["user"]["result"]["legacy"]["name"]],
            "Description": [user_data["data"]["user"]["result"]["legacy"]["description"]],
            "Location": [user_data["data"]["user"]["result"]["legacy"]["location"]],
            "Create Date":[user_data["data"]["user"]["result"]["legacy"]["created_at"]],
            "Followers Count": [user_data["data"]["user"]["result"]["legacy"]["followers_count"]],
            "Following Count": [user_data["data"]["user"]["result"]["legacy"]["friends_count"]],
            "Tweet Count": [user_data["data"]["user"]["result"]["legacy"]["statuses_count"]],
            "Account Verified": [user_data["data"]["user"]["result"]["legacy"]["verified"]],
            "Media Count": [user_data["data"]["user"]["result"]["legacy"]["media_count"]],
            "Favourites Count": [user_data["data"]["user"]["result"]["legacy"]["favourites_count"]],
        })
        # Print user data
        print("User Data:")
        print(user_df)

        # Append the DataFrame to the list
        all_user_data.append(user_df)

        # Concatenate all DataFrames in the list
        final_user_data = pd.concat(all_user_data, ignore_index=True)

        # Save the DataFrame to a CSV file (mode='a' is not used)
        final_user_data.to_csv("multiple_user_data.csv", index=False)
        print("Successfully saved the data in file.")

    else:
        print(f"Error: {response.status_code}")
        print(f"Details: {response.text}")  # Print the response text for debugging