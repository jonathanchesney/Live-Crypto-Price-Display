# Live-Crypto-Price-Display
This project is a live cryptocurrency price display. It is configured to automatically update every minute, where it will download the latest 20 minutes of a certain cryptocurrency’s price data. It will draw a line graph on a 128x128 OLED display, headed by the cryptocurrency’s symbol and price in US Dollars. Users may push a button to change which cryptocurrency is displayed. Another button will queue an email to be sent with a recent price of the currently displayed cryptocurrency, via AWS.

## Introduction
This project was inspired by the recent price surge of various cryptocurrencies. They have gained a significant amount attention in recent months and have become popular. The primary motivation of this project is the popularity of cryptocurrency discussion on the internet. This project sought to make an IoT device dedicated to monitoring the price of various cryptocurrencies. It achieved this by integrating a CC3200 Launchpad with Wi-Fi capability, a 128x128 OLED display, and Amazon Web Services. The device is meant to be like a clock: it is constantly displaying current information. Rather than perpetually displaying the time, the device perpetually displays cryptocurrency data. The displayed data can be changed via user input. In addition, user input can ultimately send an email with the most-recently downloaded price.

## Methodologies
### Components Used
• CC3200 Launchpad
• Adafruit 128x128 OLED Display (SSD1351)
• Amazon Web Services
o   IoT Core
o   Lambda
o   Simple Notification Service
• Crypto Compare Min API (www.cryptocompare.com)
• MikroElektronika GLCD Font Creator
• REST API
### Approach
The first step was to set up the AWS Device Shadows. In total, there are three shadows: BTC_Shadow, ETH_Shadow, and ADA_Shadow. Each shadow stores the 20 floating point values that correlate to the 20 most recent prices of each cryptocurrency. It was necessary for them to be self-updating. This was achieved via 3 respective lambda functions, each with an EventBridge trigger enabling them to run every minute. Each time a lambda function ran, it deleted the least recent price and added the newest price to the shadow. It was necessary to use boto3 to update the shadow. IAM permissions needed to be granted for a successful UpdateThingShadow(). In addition to the lambda functions, policies had to be attached to each Shadow, in order to allow the CC3200 Launchpad to call UpdateThingShadow() and GetThingShadow() with the REST API.
Programming the launchpad had multiple parts: setting up the launchpad to readily receive and upload data via AWS, writing code to interpret the data received from AWS, writing functions for drawing on the OLED display, creating custom font characters for the numbers and certain letters, polling SW2 and SW3 for user input, and coming up with the ultimate process of the algorithm.
To set up the launchpad, the AWS root, client, and private certificates needed to be converter to .der format and flashed as User Files on the launchpad. Flashing them ensured that they could be consistently accessed as the program ran.
The function drawGraph() drew a the line-plot in a succession – starting from the least recent value until the most recent. The function drawPrice(double price) drew the crypocurrency symbol at the top left of the screen and the most recent price at the top right. A design decision was made to draw on the OLED display 90 degrees from its normal upright encoding. This decision was unnecessary and required custom font characters to be created.
MikroElektronika GLCD Font Creator was used to create the custom characters at 90 degrees. All digits from 0 – 9 were replaced as well as the characters A, B, C, D, E, and T.
To access the dynamic data via AWS, http_get() was written to use a rest API call (GET) to get the full state of a shadow. This function parsed the returned string and loaded it into a global double array.
### Algorithm
