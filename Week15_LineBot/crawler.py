import requests


def getWeatherData(): 
    url_base = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001'
    auth_code = 'Authorization=CWB-AA92238F-0B80-49A8-85F1-8E9D7768134C'
    format_code = 'format=JSON'

    # C0D660 新竹市東區 新竹市東區光復路二段321號-工研院光復院區6館
    station_id = 'stationId=C0D660'

    url = f'{url_base}?{auth_code}&{format_code}&{station_id}'
    response = requests.get(url)

    data = response.json()

    for i in data['records']['location'][0]['weatherElement']:
        if i['elementName'] == 'TEMP': temp = float(i['elementValue'])
        if i['elementName'] == 'HUMD': humd = float(i['elementValue'])
        if i['elementName'] == 'PRES': pres = float(i['elementValue'])
        if i['elementName'] == 'H_24R': rain = float(i['elementValue'])

    return (temp, humd, pres, rain)


if __name__ == '__main__':
    print(getWeatherData())