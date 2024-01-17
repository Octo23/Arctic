Small Python Script to monitor Arctic Spa for App/Website connectivity and then to trigger a reboot

You will need to tweak the values in External_Key.py to allow this script to run.
You must generate an API Key for the tub in question
https://www.myarcticspa.com/spa/SpaAPIManagement.aspx

API_Key_secret = ""

Hardcoded Spa IP
SPA_IP = "0.0.0.0"

pushOver should be set to True if using the Pushover.net tool for notifications
set push_token and push_user to your token and username.
I was already using the pushover notification for other things within my home
push_token = ""
push_user = ""
pushOver = False

This script can be used if your Arctic Spa is going offline according to their website, but still online according to your network. If your Arctic Spa is dropping completely off your network, then this script can't help you.
