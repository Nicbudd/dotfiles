import requests
import time
import re
import degreesToCardinal as degr

station = "PSM"
network = "NH_ASOS"

def fToC(f):
    #f stands for freedom
    #c stands for communism
    return (float(f) - 32) * 5/9

def cToF(c):
    #c stands for communism
    #f stands for freedom
    return (float(c) * 9/5) + 32

def ktsToMPH(kts):
    return kts * 1.1507794

def formatData():
    r = requests.get(f"http://mesonet.agron.iastate.edu/json/current.py?station={station}&network={network}")
    data = r.json()

    if r.status_code == 200:
        try:
            METAR = data["last_ob"]["raw"]

            cloudSearch = [r"OVC", r"BKN", r"SCT", r"FEW", r"CLR"]
            clouds = "UNK"

            for cloudType in cloudSearch:
                match = re.search(cloudType, METAR, flags=re.IGNORECASE)
                if match:
                    clouds = cloudType
                    break


            extraCloudsRegex = re.findall(r"CBMAM|TCU|ACC|CB|CCSL|CA|CC|CG|LTG|SCSL", METAR)
            extraCloudsList = []

            for match in extraCloudsRegex:
                string = match
                extraCloudsList.append(string)

            if len(extraCloudsList) > 0:
                clouds += "/"+"/".join(extraCloudsList)

            precipRegex = re.findall(r"\s([+-]?(APRNT|B|BC|BL|CIG|CONS|DR|DSIPTG|E|FRQ|FZ|G|INTMT|INCRG|LWR|M|MI|MOV|MT|OCNL|OHD|OVR|PR|SN|SFC|V|VC)*(BR|DS|DU|DZ|FC|FG|FROPA|FU|GR|GS|HLSTO|HZ|IC|PL|PO|PCPN|PRSFR|PRESRR|PY|RA|S|SA|SG|SH|SN|SNINCR|SP|SQ|SS|SW|TS(\+)?|TSW(\+)?|TSW|UP|VA|WSHFT|)+)\s", METAR)
            precipList = []

            for match in precipRegex:
                string = match[0]
                precipList.append(string)

            precip = "/".join(precipList)



            temperature = int(data["last_ob"]["airtemp[F]"])
            dewpoint = int(data["last_ob"]["dewpointtemp[F]"])
            winddirection = int(data["last_ob"]["winddirection[deg]"])
            windcardinal = degr.convert(winddirection)
            windspeed = int(data["last_ob"]["windspeed[kt]"])
            windspeedmph = int(ktsToMPH(windspeed))
            visibility = round(data["last_ob"]["visibility[mile]"] * 10) / 10
            pressure = round(data["last_ob"]["mslp[mb]"])

            if (visibility * 10) % 10 == 0:
                visibility = int(visibility)

            if len(precipList) > 0:
                 return f"{pressure}mb {visibility}SM {clouds}/{precip} {temperature}°F/{dewpoint}°F {winddirection:03d}@{windspeed:02d}({windcardinal}@{windspeedmph}mph)"
            else:
                 return f"{pressure}mb {visibility}SM {clouds} {temperature}°F/{dewpoint}°F {winddirection:03d}@{windspeed:02d}({windcardinal}@{windspeedmph}mph)"
        except:
            return "parsing failed"

    else:
        return f"HTTP Error: {r.status_code}"

def main():

    while True:
        f = formatData()

        with open("/var/currentconditions.log", "w") as file:
            file.write(f"{f}")

        time.sleep(60 * 5) # sleep 5 minutes

if __name__ == "__main__":
    main()
