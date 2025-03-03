# TapMirror
TapMirror is a Smart Mirror application that retrieves Cardano Native Token and Nft data from TapTools (https://www.taptools.io/) API in real time and displays it as a full-screen application. The solution is developed in Python and uses the PyQt5 library to display the data without a browser. 

The ideal hardware setup is a Raspberry Pi or a comparable device running a Linux distribution such as Ubuntu.

# Prerequisites
- Ubuntu(20.04) or comparable Linux based OS
- Git (install with `sudo apt install git` if not already installed)
- Taptools API Key (https://www.taptools.io/openapi/subscription)
- Xerberus API Key (https://xerberus.gitbook.io/documentation) for Token Risk Ratings (Optional)

# Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/TapMirror.git
2. **Install Python 3** 
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip
3. **Install PyQt5**
   ```bash
    pip3 install PyQt5
4. **Install additional dependencies**
    ```bash
    pip3 install feedparser==6.0.11 matplotlib==3.10.1 pandas==2.2.3 Requests==2.32.3
5. **Navigate to config folder**
    ```bash
    cd TapMirror/config
6. **Open the config.py file to set your API keys** 
    ```python
    TAP_TOOLS_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
5. **Navigate back to Main folder**
    ```bash
    cd ..
6. **Start Application bash: python3 main.py**
    ```bash
    python3 main.py
# Layout Configuration with layout_config.json file

The config_layout.json file can be used to dynamically customise the layout according to your needs and different screens.

You can Select and copy one of the examples from `examples/config` or change the sections directly in `config/layout_config.json` 


## Structure of the layout.config.json file:

The file needs to be structured in this way: 
    
    {
        "header_sections": [...],
        "grid_sections": [...] 
    }


## Header Section

***header_sections:[]*** Can contain individual Header Widgets

## Header Widgets

## 1. Clock as Header Widget
- type: "clock" -> widget type 
- font_size:    -> clock font size
- refresh:      -> widget update intervall (ms)

Example:

    {
        "type": "clock",      
        "font_size": 30,      
        "color": "white",     
        "refesh": "10000"      
    }

## 2. Market Data Widget
- type: "market_data"    -> widget type
- font_size:             -> market data font size
- refesh:                -> widget update intervall (ms)
- **innerWidgets[]:**    -> inner section for the labels to be displayed
- quote:                    -> ADA Price in $USD
- activeaddresses:          -> Number Active Adresses last 24h
- dexvolume:                -> Dexvolume 24h

Example:

    {
        "type": "market_data",
        "font_size": 50,
        "color": "white",
        "refesh": 100000,
        "innerWidgets": [ "quote", "activeaddresses", "dexvolume" ]
    }



## Grid Section

***grid_sections:[]*** Can contain individual Grid Widgets

## Grind Widgets

## 1. Porfolio Widget

 - type: "portfolio"        -> widget type
 - font_size:               -> font size
 - header_size:             -> header size
 - **chart_size[]:**        -> portfolio chart
    - length                    -> length of portfolio chart
    - hight                     -> high portfolio chart
 -  image_size:             -> size tokens image 
 -  color:                  -> color
 -  address:                -> poretfolio address
 -  refresh:                -> refresh  
 -  **innerWidgets[]:**     -> inner widgets
    -  adabalance:              -> ada balance (top)
    -  adavalue:                -> ada value (top)
    -  chart:                   -> chart 
    -  tokens:                  -> token positions
    -  trades:                  -> last 5 trades
    -  nfts:                    -> nft positions
    -  lppos:                   -> lp positions    
- **position[]:**           -> position in the grind
    - row,                      -> row in grid layout
    - col                       -> column in grid layout

Example:

    {
            "type": "portfolio",
            "font_size": 70,
            "header_size": 80,
            "chart_size": [
                400,
                280
            ],
            "image_size": 80,
            "color": "white",
            "address": "stake1u9qljmz94se6cfcnqv0yudwsa48pe0yxzuulna3xmnhyaxq84dzc4",
            "refresh": 100000,
            "innerWidgets": [
                "adabalance",
                "adavalue",
                "chart",
                "tokens",
                "trades",
                "nfts",
                "lppos"
            ],
            "position": [
                0,
                0
            ]
        }

## 2. Token Data Widget
This section makes it possible to combine different tokens with variable subwidgets such as image,, ticker, price, risk rating, change or chart, which can be arranged and selected as desired

- type: "tokens":           -> widget type   
- font_size:                -> font size
- images_size":             -> token image size
- refesh: 100000,           -> refresh 
- ***innerWidgets:***       -> token information
    - "logo",                   -> token logo
    - "ticker",                 -> token ticker
    - "price",                  -> token price
    - "riskrating"              -> widget type
    - "change",                 -> token change (24h, 7d, 30d)
    - "chart"                   -> trend chart
- ***tokens:***             -> tokens inculuded
    - TICKER 1,                 -> ticker 1
    - TICKER 2,                 -> ticker 2
    - TICKER 3,                 -> ticker 3
    - TICKER N,                 -> ticker n ...
- ***position:[]***         -> position in the grind
    - row,                      -> row in grid layout
    - col                       -> column in grid layout
   
Example:

    {
            "type": "tokens",
            "font_size": 60,
            "image_size": 80,
            "color": "white",
            "refesh": 100000,
            "innerWidgets": [
                "logo",
                "ticker",
                "price",
                "riskrating",
                "change",
                "chart"
            ],
            "tokens": [
                "MIN",
                "SNEK",
                "IAG",
                "LQ",
                "LENFI"
            ],
            "position": [
                1,
                0
            ]
        },

## 3. Token Loans Widget

- type: "token_loans"       -> widget type 
- font_size:                -> token loan table font size
- header_size:              -> token loan table header size
- images_size:              -> token image size
- color:                    -> font color
- count:                    -> number of loans included 
- ticker:                   -> token ticker to show loans from
- refesh:                   -> update time
- **position[]:**           -> position inside the grid
    - row,                      -> row in grid layout
    - col                       -> column in grid layout

Example:

    {
            "type": "token_loans",
            "font_size": 55,
            "header_size": 60,
            "image_size": 65,
            "color": "white",
            "count": 10,
            "ticker": "SNEK",
            "refesh": 100000,
            "position": [
                1,
                0
            ]
        },

## 4. Token Trades Widget

- type: "last_trades"       -> widget type 
- font_size:                -> table font size
- header_size:              -> header size
- images_size:              -> token image size
- color:                    -> color
- count:                    -> number trades to display
- ticker:                   -> token ticker
- refesh:                   -> update time
- value:                    -> min trade value
- **position[]:**           -> position inside the grid
    - row,                      -> row in grid layout
    - col                       -> column in grid layout

Example:

    {
            "type": "token_trades",
            "font_size": 55,
            "header_size": 60,
            "image_size": 65,
            "color": "white",
            "count": 10,
            "ticker": "SNEK",
            "refesh": 100000,
            "value": 1000,
            "position": [
                1,
                1
            ]
        }

## 5. Weather Widget

- type: "weather"           -> widget type 
- font_size:                -> wether font size current wether
- images_size:              -> wether image current weather
- fc_image_size             -> forecast image size    
- fc_font_size              -> forcast font size
- color:                    -> font color size    
- geo:                      -> geolocation (lagidtue, ...)
- refresh:                   -> update time (ms) 
- **position[]:**           -> position inside the grid
   - row,                      -> row in grid layout
   - col                       -> column in grid layout

 Example:

    {
        "type": "weather",
        "font_size": 40,
        "header_size": 24,
        "images_size": 250,
        "fc_image_size": 90,
        "fc_front_size": 20,
        "color": "white",
        "geo": [ 52.52, 13.4 ],
        "refesh": 100000,
        "position": [ 0, 1 ]
    }

## 6. Medium RSS Feed Widget

- type: "rssfeed"           -> widget type 
- font_size:                -> feed font size
- header_size:              -> feed header size
- name:                     -> medium creator name
- feed_num:                 -> display last x puplikations 
- color:                    -> color
- refesh:                   -> update time (ms)
- **position[]:**           -> position inside the grid
    - row,                      -> row in grid layout
    - col                       -> column in grid layout
    
Example:

    {
        "type": "rssfeed",
        "font_size": 15,
        "header_size": 20,
        "name": "@TapInWithTapTools",
        "feed_num": 4,
        "color": "white",
        "refesh": 100000,
        "position": [ 1, 1 ]
    }

## 7. Welcome Widget

- type: "welcome"    -> widget type
- font_size:         -> font size
- refesh:            -> upodate intervall (ms)
- **quoats[]:**      ->  quoats
    - quoat1:           -> first greeting is displayed from x to x o'clock
    - quoat2:           -> second  greeting is displayed from x to x o'clock
    - quoat3:           -> third greeting is displayed from x to x o'clock
- **position[]:**           -> position inside the grid
    - row,                      -> row in grid layout
    - col                       -> column in grid layout

Example:

    {
        "type": "welcome",
        "font_size": 50,
        "color": "white",
        "refesh": 100000,
        "innerWidgets": [ "Good Morning", "Good Afternoon", "Good Evening" ]
        "position[ 1, 0]
    }

## 8. Clock as Grid Widget**

- type: "clock" -> widget type 
- font_size:    -> clock font size
- refresh:      -> widget update intervall (ms)
- **position[]:**           -> position inside the grid
    - row,                      -> row in grid layout
    - col                       -> column in grid layout

Example:

    {
        "type": "clock",      
        "font_size": 30,      
        "color": "white",     
        "refesh": "10000"
        "position": [ 0 , 1]      
    }


## Add new token with config/config.py

With in config/config.py all tokens that are currently available are listed, if you want to add a new token, it must be added there with its corresponding assetID and under assets/tokens add the corresponding .png image for example (SNEK.png)

### Mapping for Ticker to Token unit (policy + hex name)
    
    TOKEN_ID_MAPPING = {
    "LENFI": "8fef2d34078659493ce161a6c7fba4b56afefa8535296a5743f6958741414441",
    "SNEK":  "279c909f348e533da5808898f87f9a14bb2c3dfbbacccd631d927a3f534e454b",
    "IAG":   "5d16cc1a177b5d9ba9cfa9793b07e60f1fb70fea1f8aef064415d114494147",
    "LQ":    "da8c30857834c6ae7203935b89278c532b3995245295456f993e1d244c51",
    "XER":   "6d06570ddd778ec7c0cca09d381eca194e90c8cffa7582879735dbde584552",
    "MIN":   "29d222ce763455e3d7a09a665ce554f00ac89d2e99a1a83d267170c64d494e",
    "FLDT":  "577f0b1342f8f8f4aed3388b80a8535812950c7a892495c0ecdf0f1e0014df10464c4454",
    "NVL":   "5b26e685cc5c9ad630bde3e3cd48c694436671f3d25df53777ca60ef4e564c"}

### Mapping for Ticker to fingerprint id (only necessary if you want to include the Xerberus Risk ratings)

    TOKEN_PRINT_MAPPING = {
        "LENFI":  "asset1khk46tdfsknze9k84ae0ee0k2x8mcwhz93k70d",
        "SNEK":   "asset108xu02ckwrfc8qs9d97mgyh4kn8gdu9w8f5sxk",
        "IAG":    "asset1z62wksuv4sjkl24kjgr2sm8tfr4p0cf9p32rca",
        "LQ":     "asset13epqecv5e2zqgzaxju0x4wqku0tka60wwpc52z",
        "XER":    "asset1yxmhmq2sqddn4vfl0um2dtlg4r7g2p9u9ed6rc",
        "MIN":    "asset1d9v7aptfvpx7we2la8f25kwprkj2ma5rp6uwzv",
        "FLDT":   "asset1gayaljphz3tepway6u6ruuty9cee2pj7wch408",
        "NVL":    "asset1jle4pt4cg8264ypx4u45vt99haa6ty3t7naxer"}

# Related links

For further questions and more detailed documentation, please visit: https://maxalexweber.gitbook.io/tapmirror-a-smart-mirror-interface

For more information about Taptools and the API visit: https://www.taptools.io/openapi/subscription

For more information about Risk Ratings and Xerberus visit: https://www.xerberus.io/