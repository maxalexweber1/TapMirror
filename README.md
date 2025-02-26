# TapMirror
TapMirror is a smart mirror application that retrieves Cardano Native Token and Nft data from the TapTools API in real time and displays it as a full-screen application. The solution is developed in Python and uses a GUI library to display the data without a browser

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


    pip install feedparser
    
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

1. **clock**
- type: "clock" -> widget type 
- front_size:   -> clock frot size
- refresh:      -> widget update intervall 

Example:

{
"type": "clock",      -> widget type -> see more Widgets in 2.1 Widgets
"font_size": 30,      -> frot size for clock 
"refesh": "10000"     -> time to refresh widget in ms 
}

2. **market_data**
    - type: "market_data"
    - font_size: 30
    - refesh: ,
            "innerWidgets": [
                "quote",
                "activeaddresses",
                "dexvolume"
            ],

3. **welcome**
    - type: "welcome"
    - font_size:
    - refesh": 100000,
    - quoats: [
                "Mornig",
                "Evening",
                "Good Night"
            ],


### Grid Section

***grid_sections:[]**** can contain individual Grid Widgets

### Grind Widgets
1. **porfolio**

2. **token**
This section makes it possible to combine different tokens with variable subwidgets such as image,, ticker, price, risk rating, change or chart, which can be arranged and selected as desired

    - type: "tokens" -      
    - font_size": 20,
    - images_size": 60,
    - refesh: 100000,
    - ***innerWidgets:** 
        - "logo",
        - "ticker",
        - "price",
        - "riskrating"
        - "change",
        - "chart"
    - ***tokens:*** 
        - TICKER 1,
        - TICKER 2,
        - TICKER 3,
    - ***position:[]***
        - grid x,
        - grid y
            
    Example:

        {
            "type": "tokens",       
            "font_size": 20,
            "images_size": 60,
            "color": "white",
            "refesh": 100000,
            "innerWidgets": [
                "logo",
                "ticker",
                "price",
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
        }

4. **tokenloans**
5. **tokentrades**
6. **weather**
7. **rssfeed**
{
            "type": "rssfeed",
            "font_size": 40,
            "header_size": 24,
            "feed": "@TapInWithTapTools",
            "feed_num": 3,
            "color": "white",
            "refesh": 100000,
            "position": [
                1,
                1
            ]
        },
7. **welcome**

### Add new Token
in config/config.py all tokens that are currently available are listed, if you want to add a new token, it must be added there with its corresponding assetID and under assets/tokens add the corresponding .png image for example (SNEK.png)