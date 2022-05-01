# House price prediction for real estate in Saint-Petersburg

Status of Last Deployment: <br>
<img src="https://github.com/dubrovin-sudo/house-prediction/workflows/Flake8/badge.svg?branch=feature"><br>
<img src="https://github.com/dubrovin-sudo/house-prediction/workflows/Docker/badge.svg?branch=feature"><br>

## About

![](https://wallpaperaccess.com/full/508402.jpg)l/508402.jpg

The dataset consists of lists of unique objects of popular portals for the sale of real estate in Russia. More than 540 thousand objects.
The dataset contains 540000 real estate objects in Russia.

### Content

The Russian real estate market has a relatively short history. In the Soviet era, all properties were state-owned; people only had the right to use them with apartments allocated based on one's place of work. As a result, options for moving were fairly limited. However, after the fall of the Soviet Union, the Russian real estate market emerged and Muscovites could privatize and subsequently sell and buy properties for the first time. Today, Russian real estate is booming. It offers many exciting opportunities and high returns for lifestyle and investment.
The real estate market has been in a growth phase for several years, which means that you can still find properties at very attractive prices, but with good chances of increasing their value in the future.

### Dataset

The dataset has 13 fields.

- date - date of publication of the announcement;

- time - the time when the ad was published;

- geo_lat - Latitude;

- geo_lon - Longitude;

- region - Region of Russia. There are 85 subjects in the country in total;

- building_type - Facade type. 0 - Other. 1 - Panel. 2 - Monolithic. 3 - Brick. 4 - Blocky. 5 - Wooden;

- object_type - Apartment type. 1 - Secondary real estate market; 2 - New building;

- level - Apartment floor;

- levels - Number of storeys;

- rooms - the number of living rooms. If the value is "-1", then it means "studio apartment";

- area - the total area of the apartment;

- kitchen_area - Kitchen area;

- price - Price. in rubles;

  Also we mine additional data from [OpenStreetMap](https://maps.mail.ru/osm/tools/overpass/):

  - subways;
  - parks;
  - restaurants;
  - museums

### Goal

Our job to predict the sales price for each house. For each Id in the test set,  we must predict the value of the SalePrice variable. 

### Metric

Submissions are evaluated on [Root-Mean-Squared-Error (RMSE)](https://en.wikipedia.org/wiki/Root-mean-square_deviation) between the logarithm of the predicted value and the logarithm of the observed sales price. (Taking logs means that errors in predicting expensive houses and cheap houses will affect the result equally.)



## Stack

We are testing MLOps approaches to predict houses' prices in Saint-Petersburg:

- Lint Flake8;
- Snakemake;
- DVC;
- Docker;
- MLFlow;
- CI/CD Github
