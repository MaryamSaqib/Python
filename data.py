import requests
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '099d2f1daf8b484ca1a85cf6859f7b1b' 
}
api = 'https://dev.tescolabs.com/grocery/products/?query=%s&offset=0&limit=20'
def getProducts(searchstring):
    response = requests.get(api % (searchstring), headers=headers) 
    data=response.json() 
    return data['uk']['ghs']['products']['results'] 
