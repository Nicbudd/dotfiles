import math

directions = {
0: "N",
10: "N",
20: "NNE",
30: "NNE",
40: "NE",
50: "NE",
60: "ENE",
70: "ENE",
80: "E",
90: "E",
100: "E",
110: "ESE",
120: "ESE",
130: "SE",
140: "SE",
150: "SSE",
160: "SSE",
170: "S",
180: "S",
190: "S",
200: "SSW",
210: "SSW",
220: "SW",
230: "SW",
240: "WSW",
250: "WSW",
260: "W",
270: "W",
280: "W",
290: "WNW",
300: "WNW",
310: "NW",
320: "NW",
330: "NNW",
340: "NNW",
350: "N"
}

def convert(degrees):
    degrees = round(int(degrees) / 10) * 10
    return directions[degrees]
