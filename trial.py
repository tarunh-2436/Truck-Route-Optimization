import requests

# MapmyIndia Credentials
CLIENT_ID = "96dHZVzsAuu3SM87eXKedKLubwalQUSRwYl4MpDBxiQ3KIH7NuNWPZnu4Jk621sERbKzo3k9Nn3flLhWUsPOjQ=="
CLIENT_SECRET = "lrFxI-iSEg8pJyQYia5pH4Y_-JSDJiCj5q40cePPqO_RrjM3QVRrxwd1Rt5jHUn4lrZmXybsY6VyLMH3DhzQ7aRJnlXrOz9C"

# Get Access Token
def get_access_token():
    url = "https://outpost.mapmyindia.com/api/security/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    response_json = response.json()
    
    if "access_token" in response_json:
        return response_json["access_token"]
    else:
        raise Exception("Failed to get access token: " + str(response_json))

# Get the token
access_token = get_access_token()

# Call Places API
def get_coordinates(address):
    url = "https://atlas.mapmyindia.com/api/places/geocode"
    params = {"address": address}
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Test with an example address
coordinates = get_coordinates("BSS Hospital, Chennai")
print(coordinates)

