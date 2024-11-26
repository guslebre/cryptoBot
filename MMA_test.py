import http.client

conn = http.client.HTTPSConnection("mma-api1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "b4a165c51fmsh9a453a391dcb626p14a824jsn7c28ca1ab7e6",
    'x-rapidapi-host': "mma-api1.p.rapidapi.com"
}

conn.request("GET", "/drankings/details?idDivisional=2", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))