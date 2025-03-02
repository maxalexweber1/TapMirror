# TapMirror
TapMirror is a Smart Mirror application that retrieves Cardano Native Token and Nft data from TapTools (https://www.taptools.io/) API  in real time and displays it as a full-screen application. The solution is developed in Python and uses a GUI library to display the data without a browser

## Prerequisites
- Ubuntu (20.04 LTS or later recommended)
- Git (install with `sudo apt install git` if not already installed)
- Taptools API Key (https://www.taptools.io/openapi/subscription)
- Xerberus API Key (https://xerberus.gitbook.io/documentation) for Token Risk Ratings (Optional)

## Quick Start

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

    pip3 install feedparser
    
4. **Navigate to Main folder**
    ```bash
    cd TapMirror
5. **Start Application bash: python3 main.py**
    ```bash
    python3 main.py

## Layout Configuration with layout_config.json file

The layout.json file can be used to dynamically customise the layout according to your needs and different screens.

You can Select and copy one of the examples from `examples/config` or change the sections directly in `config/layout_config.json` 


### Structure of the layout.config.json file:

The file needs to be structured in this way: 
    
    {
        "header_sections": [...],
        "grid_sections": [...] 
    }


### Header Section

***header_sections:[]*** can contain individual Header Widgets

### Header Widgets

1. **clock as Header Widget**
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

2. **market_data**
    - type: "market_data"    -> widget type
    - font_size:             -> market data font size
    - refesh:                -> widget update intervall (ms)
    - **innerWidgets[]:**    -> inner section for the labels to be displayed
        - quote:               -> ADA Price in $USD
        - activeaddresses:     -> Number Active Adresses last 24h
        - dexvolume:           -> Dexvolume 24h

Example:

    {
        "type": "market_data",
        "font_size": 50,
        "color": "white",
        "refesh": 100000,
        "innerWidgets": [ "quote", "activeaddresses", "dexvolume" ]
    }



### Grid Section

***grid_sections:[]*** can contain individual Grid Widgets

### Grind Widgets
1. **porfolio**

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
    - col:                      -> colum
    - row:                      -> row

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
        },

2. **token**
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
    - col,                      -> colum 
    - row                       -> row
   
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

4. **tokenloans**

- type: "token_loans"       -> widget type 
- font_size:                -> token loan table font size
- header_size:              -> token loan table header size
- images_size:              -> token image size
- color:                    -> font color
- count:                    -> number of loans included 
- ticker:                   -> token ticker to show loans from
- refesh:                   -> update time
- **position[]:**           -> position inside the grid
    - col                       -> colum
    - row                       -> row

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

5. **tokentrades**

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
    - col                       -> colum
    - row                       -> row

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

6. **weather**

- type: "weather"           -> widget type 
- font_size:                -> wether font size current wether
- images_size:              -> wether image current weather
- fc_image_size             -> forecast image size    
- fc_font_size              -> forcast font size
- color:                    -> font color size    
- geo:                      -> geolocation (lagidtue, ...)
- refresh:                   -> update time (ms) 
- **position[]:**           -> position inside the grid
    - col                       -> colum
    - row                       -> row

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

7. **rssfeed**

- type: "rssfeed"           -> widget type 
- font_size:                -> feed font size
- header_size:              -> feed header size
- name:                     -> medium creator name
- feed_num:                 -> display last x puplikations 
- color:                    -> color
- refesh:                   -> update time (ms)
- **position[]:**           -> position inside the grid
    - col                       -> colum
    - row                       -> row
    
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

7. **welcome**

    - type: "welcome"    -> widget type
    - font_size:         -> font size
    - refesh:            -> upodate intervall (ms)
    - **quoats[]:**      ->  quoats
        - quoat1:           -> first greeting is displayed from x to x o'clock
        - quoat2:           -> second  greeting is displayed from x to x o'clock
        - quoat3:           -> third greeting is displayed from x to x o'clock

Example:

    {
        "type": "welcome",
        "font_size": 50,
        "color": "white",
        "refesh": 100000,
        "innerWidgets": [ "Good Morning", "Good Afternoon", "Good Evening" ]
    }

8. **clock as grind widget**

- type: "clock" -> widget type 
- font_size:    -> clock font size
- refresh:      -> widget update intervall (ms)
- - **position[]:**           -> position inside the grid
    - col                       -> colum
    - row                       -> row

Example:

    {
        "type": "clock",      
        "font_size": 30,      
        "color": "white",     
        "refesh": "10000"
        "position": [ 0 , 1]      
    }


### Add new Token
in config/config.py all tokens that are currently available are listed, if you want to add a new token, it must be added there with its corresponding assetID and under assets/tokens add the corresponding .png image for example (SNEK.png)