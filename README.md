# Stake Everything API

API for easy data acquisition of information on[Stake Everything](https://stakeeverything.biz/) website.

### Root endpoint:

api.stakeeverything.biz

## Public Endpoints:

### /coins

(GET) Returns a json object with a list of stakeable coins.

Ex. Response:

```
[
  "AUTO",
  "BANANA",
  "BNB",
  "BSCX",
  "BTC",
  "BTCB",
  "BUNNY",
  "BUSD",
  "CAKE",
  "DAI",
  "DOT",
  "EGG",
  "ETH", ...

```

### /farms

(GET) Returns a list of the website where you can farm/stake.

```
Ex: GET /farms
```

Ex. Response:

```
[
[
  {
    "site": "Viking Swap",
    "url": "https://www.vikingswap.finance/nests"
  },
  {
    "site": "Auto Farm",
    "url": "https://autofarm.network/"
  },
  {
    "site": "Pancake Bunny",
    "url": "https://pancakebunny.finance/pool"
  },
  {
    "site": "Auto Farm",
    "url": "https://autofarm.network/"
  }, ...
]
```

### /images

(GET) Returns a json object of coins and their image uri's.

```
Ex: GET /images
```

Ex. Response:

```
{
  "AUTO": {
    "image_uri": "https://cryptologos.cc/logos/binance-coin-bnb-logo.svg?v=010"
  },
  "BANANA": {
    "image_uri": "https://raw.githubusercontent.com/trustwallet/assets/master/blockchains/smartchain/assets/0x603c7f932ED1fc6575303D8Fb018fDCBb0f39a95/logo.png"
  },  ...
```

### /images/(coin)

(GET) Returns a json object of coins and their image uri's.

```
Ex: GET /images/AUTO
```

Ex. Response:

```
{ "AUTO": "https://cryptologos.cc/logos/binance-coin-bnb-logo.svg?v=010" }
```

### /farms/tags

(GET) Returns a key value pair of the website where you can farm/stake and its associated tag.

```
Ex: GET /farms/tags
```

Ex. Response:

```
{
  "ACryptoS": "acryptos",
  "Auto Farm": "auto",
  "Beefy Finance": "beefyfinance",
  "Gecko Swap": "geckoswap",
  "Goose Defi": "goosedefi",
  "Pancake Bunny": "pancakebunny", ...

```

### /info

(GET) Returns all info.

```
Ex: GET /info

Ex. Response:

```

```
{
  "AUTO": {
    "image_uri": "https://cryptologos.cc/logos/binance-coin-bnb-logo.svg?v=010",
    "info": [
      {
        "apr": "153.84%",
        "site": "Viking Swap",
        "token_earned": "VIKING",
        "url": "https://www.vikingswap.finance/nests"
      }
    ]
  },
  "BANANA": {
    "image_uri": "https://raw.githubusercontent.com/trustwallet/assets/master/blockchains/smartchain/assets/0x603c7f932ED1fc6575303D8Fb018fDCBb0f39a95/logo.png",
    "info": [
      {
        "apy": "360.9%",
        "site": "Auto Farm",
        "token_earned": "ApeSwap",
        "url": "https://autofarm.network/"
      }
    ]
  },
  "BNB": {
    "image_uri": "https://cryptologos.cc/logos/binance-coin-bnb-logo.svg?v=010",
    "info": [
      {
        "apy": "24.65%",
        "site": "Pancake Bunny",
        "token_earned": "BNB + BUNNY",
        "url": "https://pancakebunny.finance/pool"
      },
      {
        "apy": "50.6%",
        "site": "Auto Farm",
        "token_earned": "BZX",
        "url": "https://autofarm.network/"
      }
    ]
  }, ...
```

### /info/(coin)

(GET) Returns info of a specific coin.

```
Ex: GET curl /info/auto

Ex. Response:

```

```
{
  "image_uri": "https://pancakebunny.finance/static/media/token-bunny.9186f99f.svg",
  "info": [
    {
      "apy": "316.70%",
      "site": "Pancake Bunny",
      "token_earned": "WBNB",
      "url": "https://pancakebunny.finance/pool"
    }
  ]
}
```

### /coins/(farm)

(GET) Returns the coins specific to a farming site. Use the farms tag.

| Parameter    | Type | Description                                       |
| ------------ | ---- | ------------------------------------------------- |
| roi          | Bool | If true will return the apy or apr for the coin   |
| token_earned | Bool | If true will return the token earned for staking. |

```
Ex: curl GET /coins/pancakebunny?roi=true
```

Ex. Response

```
{
  "Pancake Bunny": [
    [
      "BNB",
      "24.65%"
    ],
    [
      "BTCB",
      "16.48%"
    ],
    [
      "BUNNY",
      "316.70%"
    ],
    [
      "BUSD",
      "29.00%"
    ],
    [
      "CAKE",
      "219.90%"
    ],
    [
      "ETH",
      "12.60%"
    ],
    [
      "USDT",
      "35.87%"
    ]
  ]
}
```

## Private Endpoints (must have key):

### /images

(POST) Adds a url for a cryptocurrency to the firebase db.

| Key         | Value | Description                                        |
| ----------- | ----- | -------------------------------------------------- |
| coin symbol | url   | Json object with the coin as key and url as value. |

```
Ex: curl -X POST -H 'Content-Type: application/json' /images --data '{"ETH":"url_here"}'
```

(DELETE) Deletes coin - url pair for a cryptocurrency from the firebase db.

```
Ex: curl -X POST /images/BTC
```

### /farms/(tag)

(POST) Adds a url for a cryptocurrency to the firebase db.

| Key      | Value Type | Value Description                         |
| -------- | ---------- | ----------------------------------------- |
| "name"   | string     | Name of the farm project                  |
| "url"    | string     | Url to the farms application              |
| "code"   | int        | Integer code used in data scrape sequence |
| "active" | bool       | True or false                             |

```
Ex: curl -X POST -H 'Content-Type: application/json' /farm/beefy --data '{"name":"Beefy Finance", "url": "https://app.beefy.finance/", "code": 3 }'
`
```

(DELETE) Deletes farm from the firebase db

```
Ex: curl -X POST /images/BTC
```
