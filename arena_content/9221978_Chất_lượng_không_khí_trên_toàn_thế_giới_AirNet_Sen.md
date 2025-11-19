🇮🇹🇮🇩🇳🇱🇮🇷🇹🇭🇭🇺🇬🇷🇷🇴🇧🇬🇵🇰🇮🇳🇦🇪🇷🇸🇧🇩🇧🇦🇭🇷🇹🇷🇺🇦🇨🇿🇧🇾🇰🇭🇱🇦
EnglishChinese - 简体中文Japanese - 日本Spanish - españolKorean - 한국의Russian - русскийTraditional Chinese - 繁體中文French - FrancaisPolish - PolskiGerman - DeutschPortuguese - PortuguêsVietnamese - Tiếng Việt🇮🇹Italian - Italiano🇮🇩Indonesian - bahasa Indonesia🇳🇱Dutch - Nederlands🇮🇷Persian - فارسی🇹🇭Thai - ภาษาไทย🇭🇺Hungarian - Magyar🇬🇷Greek - Ελληνικά🇷🇴Romanian - Română🇧🇬Bulgarian - български🇵🇰Urdu - اردو🇮🇳Hindi - हिंदी🇦🇪Arabic - العربية🇷🇸Serbian - Српски🇧🇩Bangla - বাংলা🇧🇦Bosnian - босански🇭🇷Croatian - hrvatski🇹🇷Turkish - Türkçe🇺🇦Ukrainian - українська🇨🇿Czech - čeština🇧🇾Belarusian - беларускі🇰🇭Khmer - ខ្មែរ🇱🇦Lao - ລາວ
homeHeremapmaskfaqsearchcontactlinks
API - Air Quality Programmatic APIs Share: aqicn.org/api/Initial setup first step is to make sure to acquire your own token for all API access. You can get your token from the data-platform token page.
Map tile API The map tile API can be used to show the real-time Air Quality index on a google, bing or openstreet map. Read more about the Map tile API description and examples
Widget API The widget API can be used to integrate the real-time Air Quality index on any web page.
Read more about the Widget API description.
There is also a non-programmatic API for an easy integration with word-press, which can generate any of the widget below. For more information, go to your city page (eg aqicn.org/city/auckland), scroll-down until you find the "Download the real-time Air Quality Index Widget" and click on the "Wordpress & Blogger" logo.
JSON API
$ curl -i "http://api.waqi.info/feed/shanghai/?token=demo"
The JSON API can be used for advanced programmatic integration:
Access to more than 11000 station-level and 1000 city-level data Geo-location query (based on latitude/longitude or IP address) Individual AQI for all pollutants (PM2.5, PM10, NO2, CO, SO2, Ozone) Station name and coordinates Originating EPA name and link Current weather conditions Stations within a map lat/lng bounds Search stations by name Air Quality forecast (for 3~8 days)
For more information, you can use the on-line API documentation or refer to the sample javascript code / web demo.
Note that more functionality will be added during the coming weeks:
Weather forecast (for 8 days) World ranking and trend Neighbor stations AQI Historical Data Pollutant raw concentration (for usage with different scales) PubSub notification service
We may change, delete, add to, or otherwise amend information contained on this website without notice.
Under no circumstances will the World Air Quality Index project team or its agents be liable in contract, tort or otherwise for any loss, injury or damage arising directly or indirectly from the supply of this data.
Term of Service The usage of the programmatic API are subjected to a "acceptable usage" policy:
API Usage
All the APIs are provided for free.
A valid key must be used for accessing the API.
All the API are subjected to quota.
The default quota is 1,000 (one thousand) requests per second.
(Yes, that's a lot, and that's thanks to the support from our colleagues at the UNEP).
Data usage
The data can not be sold or included in sold packages.
The data can not be used in paid applications or services.
The data can not be redistributed as cached or archived data.
(where data refers to the data obtained from the APIs) For the historical data, check the data platform page.
App usage
Attribution to the World Air Quality Index Project as well as originating EPA is mandatory.
Public usage by for-profit corporations requires explicit agreement wit the World Air Quality Index team.
Public usage by non-profit organization requires prior notification (by email) to the World Air Quality Index team.
(where app refers to any application, services which make use of the above mentioned data)
--
If the above policy does not fulfill your needs, or if you need larger quota, then please contact us first.
Please note that the we reserve the right to change the term of service at any time and without prior notice.
Warranty All reasonable measures have been taken to ensure the quality and accuracy of the Data provided by the above APIs. However:
We do not make warranty, express or implied, nor assume any legal liability or responsibility for the accuracy, correctness, completeness of the information.
We do not assume any legal liability or responsibility for any damage or loss that may directly or indirectly result from any information contained on this website or any actions taken as a result of the content of this website;
About the Air Quality and Pollution Measurement: About the Air Quality Levels
AQI Air Pollution Level Health Implications Cautionary Statement (for PM2.5)
0 - 50 Good Air quality is considered satisfactory, and air pollution poses little or no risk None
51 -100 Moderate Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution. Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.
101-150 Unhealthy for Sensitive Groups Members of sensitive groups may experience health effects. The general public is not likely to be affected. Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.
151-200 Unhealthy Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects Active children and adults, and people with respiratory disease, such as asthma, should avoid prolonged outdoor exertion; everyone else, especially children, should limit prolonged outdoor exertion
201-300 Very Unhealthy Health warnings of emergency conditions. The entire population is more likely to be affected. Active children and adults, and people with respiratory disease, such as asthma, should avoid all outdoor exertion; everyone else, especially children, should limit outdoor exertion.
300+ Hazardous Health alert: everyone may experience more serious health effects Everyone should avoid all outdoor exertion
To know more about Air Quality and Pollution, check the wikipedia Air Quality topic or the airnow guide to Air Quality and Your Health.For very useful health advices of Beijing Doctor Richard Saint Cyr MD, check
www.myhealthbeijing.com blog.
Usage Notice:
All the Air Quality data are unvalidated at the time of publication, and due to quality assurance these data may be amended, without notice, at any time. The World Air Quality Index project has exercised all reasonable skill and care in compiling the contents of this information and under no circumstances will the World Air Quality Index project team or its agents be liable in contract, tort or otherwise for any loss, injury or damage arising directly or indirectly from the supply of this data.
home Here map mask faq search contact links
About This Project
Contact The World Air Quality Index Project Team Press And Media Kit
air quality research
Air Quality Knowledge Base And Articles Air Quality Experimentation Air Quality Sensors Analysis
Frequently Asked Questions
Air Quality Data source Air Quality Index Calculation Air Quality Forecasting Air Quality Products (masks, Monitors…) API (Application Programming Interface) Historical Data Platform
Credits
All the EPA in the world for their excellent work in maintaining, measuring and providing Air Quality information to the world citizens This product includes GeoLite2 data created by MaxMind, available from maxmind.com. This product includes GeoNames city information, available from geonames.org. Open Weather Map, combined with qweather™ improvement algorithm Citizen Weather Observer Program via cwop.waqi.info Contains modified Copernicus Atmosphere Monitoring Service Information Some of the icons made by Freepik from www.flaticon.com Reverse geocoding by locationiq.com Base map and data from OpenStreetMap. The place to be to enjoy good air quality while surfing! QUACO design
© 2008-2025
The World Air Quality Index Project
This page has been generated on Wednesday, Nov 19th 2025, 08:02 am CST from jp2n
Settings
Language Settings:
English简体中文 - Chinese日本 - Japaneseespañol - Spanish한국의 - Koreanрусский - Russian繁體中文 - Traditional ChineseFrancais - FrenchPolski - PolishDeutsch - GermanPortuguês - PortugueseTiếng Việt - VietnameseItaliano - Italianbahasa Indonesia - IndonesianNederlands - Dutchفارسی - Persianภาษาไทย - ThaiMagyar - HungarianΕλληνικά - GreekRomână - Romanianбългарски - Bulgarianاردو - Urduहिंदी - Hindiالعربية - ArabicСрпски - Serbianবাংলা - Banglaбосански - Bosnianhrvatski - CroatianTürkçe - Turkishукраїнська - Ukrainiančeština - Czechбеларускі - Belarusianខ្មែរ - Khmerລາວ - Lao
Temperature unit:
Celsius Fahrenheit