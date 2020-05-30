import requests
baseUrl = 'http://localhost:5000/'

mv = 150
degree = 2
pvUrlString = baseUrl + 'pv?degree=' + str(degree) + '&mv=' + str(mv)
response = requests.get(pvUrlString)
print('pv: ')
data = response.json()
print(data['pv'])
