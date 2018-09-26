# -*- coding:utf-8 -*-
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import warnings
import datetime
from tabulate import tabulate
warnings.simplefilter(action='ignore')
today = datetime.datetime.now()
startTime = time.time()

Address = [["3435 W Danbury Dr B216","Phoenix"],[" 337 S Comanche Dr","Chandler"],[" 19244 N Moondance Ln","Surprise"],
           [" 5825 E Harmony Ave","Mesa"],[" 2328 West bramble berry Lane","Phoenix"],[" 14575 W Morning Star Trail","Surprise"],
           [" 2008 W CALLE DEL SOL","Phoenix"],[" 1417 W Wagoner Rd","Phoenix"],[" 6605 N 93RD Ave #1090","Glendale"],
           [" 320 W Reeves Ave","San Tan Valley"],[" 26003 N 50th Ln","Phoenix"],[" 3162 W Allens Peak Dr","Queen Creek"],
           [" 3711 N Rosewood Ave","Avondale"],[" 2362 W Peralta Ave","Mesa"],[" 5341 E Gloria Ln","Cave Creek"],
           [" 10268 West Sands Drive, #491","Peoria"],[" 9026 W Escuda Dr","Peoria"],[" 1082 E Rolls Rd","San Tan Valley"],
           [" 8354 N 58th Ave","Glendale"],[" 3491 E Indigo St","Gilbert"],[" 1042 E Pueblo Rd","Phoenix"],
           [" 4063 E Park Ave","Gilbert"],[" 17037 W Saguaro Ln","Surprise"],[" 6526 South McAllister Avenue","Tempe"],
           [" 21859 Celtic Ave","Maricopa"],[" 1464 S 157th Ln","Goodyear"],[" 3419 W Bloomfield Rd","Phoenix"],
           [" 8547 W Willow Ave","Peoria"],[" 14634 Avalon Dr","Goodyear"],[" 14 North 87th Lane","Tolleson"],
           [" 3482 E Rawhide St","Gilbert"],[" 7101 W Beardsley Rd Unit 512","Glendale"],[" 13027 N 28th Pl","Phoenix"],
           [" 16780 W Romero Ln","Surprise"],[" 1248 E Clifton Ave","Gilbert"],[" 3876 E Latham Way","Gilbert"],
           [" 422 E Holmes Ave","Mesa"],[" 394 E Baylor Ln","Gilbert"],[" 19187 W Adams St","Buckeye"],
           [" 2373 E Huntington Dr","Phoenix"],[" 184 W Dublin St","Gilbert"],[" 3119 W Covey Ln","Phoenix"],
           [" 3136 S 83rd Cir","Mesa"],[" 1985 S Rennick Dr","Apache Junction"],[" 2516 W. Acoma Drive","Phoenix"],
           [" 3850 W Calle Lejos","Glendale"],[" 3434 E Wyatt Way","Gilbert"],[" 1834 E Pinto Dr","Gilbert"],
           [" 4658 E Whitehall Dr","San Tan Valley"],[" 18506 N 114th Ln","Surprise"],[" 2187 E Brigadier Dr","Gilbert"],
           [" 5670 W Harmont Dr","Glendale"],[" 3215 West Corrine Drive","Phoenix"],[" 42201 W Rojo St","Maricopa"],
           [" 930 N Mesa Dr 1020","MESA"],[" 11420 W Madisen Ellise Dr","Surprise"],[" 27916 N 65th Ln","Phoenix"],
           [" 4226 W Misty Willow Ln","Glendale"],[" 42721 w anne ln","Maricopa"],[" 5913 W Nancy Rd","Glendale"],
           [" 6920 S Russet Sky Way","Gold Canyon"],[" 806 S Cerise","Mesa"],[" 900 W Broadway Ave lot 27","Apache Junction"],
           [" 9059 W Mauna Loa Ln","Peoria"],[" 18052 N 42nd Dr","Glendale"],[" 21635 N Diamond Dr","Maricopa"],
           [" 43266 Lindgren Dr","Maricopa"],[" 2332 W Dusty Wren Dr","Phoenix"],[" 4152 E Longhorn St","San Tan Valley"],
           [" 2601 E Mitchell Dr","Phoenix"],[" 7637 S 27th Way","Phoenix"],[" 831 E Morelos St","Chandler"],
           [" 5144 W Desert Cove Ave","Glendale"],[" 2202 South Duval","Mesa"],[" 15555 W Hilton Ave","Goodyear"],
           [" 14619 W Lisbon Ln","Surprise"],[" 9590 N 81st Dr","Peoria"],[" 1844 S Thunderbird Dr","Apache Junction"],
           [" 14784 Padres Rd","Arizona City"],[" 6130 N 12th Way","Phoenix"],[" 1922 South Cottonwood Circle","Mesa"],
           [" 10594 E Primrose Ln","Florence"],[" 1637 E Bishop Dr","Casa Grande"],[" 13440 W Berridge Ln","Litchfield Park"],
           [" 433 W SANTA GERTRUDIS CIR","San Tan Valley"],[" 4514 E Ashurst Dr","Phoenix"],[" 12530 West Honeysuckle Street","Litchfield Park"],
           [" 1636 E Silverbirch Ave","Buckeye"],[" 3437 W Poinsettia Dr","Phoenix"],[" 638 S 165th Ln","Goodyear"],
           [" 43267 W Wild Horse Trail","Maricopa"],[" 4519 W. Sunnyside Ave","Glendale"],[" 31611 N Mesquite Way","San Tan Valley,"],
           [" 10041 E Isleta Ave","Mesa"],[" 42461 Sussex Rd","Maricopa"],[" 17603 W Larkspur Dr","Surprise"],
           [" 110 E Beth Dr","Phoenix"],[" 15330 S BENTLEY PL","Arizona City"],[" 2304 W Dusty Wren Dr","Phoenix"],
           [" 3281 E Ivanhoe St","Gilbert"],[" 5537 E Wethersfield Rd","Scottsdale"],[" 3269 S DANIELSON WAY","Chandler"],
           [" 16421 N 65th Pl","Scottsdale"],[" 13613 W Cypress St","Goodyear"],[" 10657 E Carol Ave","Mesa"],
           [" 7427 West Aurora Drive","Glendale"],[" 5380 W Saragosa St","Chandler"],[" 25154 W Darrel Dr","Buckeye"],
           [" 1575 S Western Skies Dr","Gilbert"],[" 3321 E Loma Vista St","Gilbert"],[" 13586 W Tara Ln","Surprise"],
           [" 17466 W Evans Dr","Surprise"],[" 1215 S 120th Dr","Avondale"],[" 18022 W Palo Verde Ave","Waddell"],
           [" 31206 North Candlewood Drive","SAN TAN VALLEY"],[" 1486 Eastfield Dr","Clearwater"],[" 6849 Park St S","South Pasadena"],
           [" 14672 Village Glen Cir","Tampa"],[" 3916 Northridge Dr","Valrico"],[" 10896 Banyan Wood Way","Riverview"],
           [" 319 Falling Water Dr","Kissimmee"],[" 5250 Carmilfra Dr","Sarasota"],[" 2804 Prestwick Dr","Lakeland"],
           [" 10343 Tecoma Dr","Trinity"],[" 10201 Arbor Side Dr","Tampa"],[" 7503 SW 97th Terrace Rd","Ocala"],
           [" 705 Jacaranda Dr","Oldsmar"],[" 7004 Dowling Mill Cir","Tampa"],[" 145 22nd Ave NE","St. Petersburg"],
           [" 25845 Bruford Blvd","Land O Lakes"],[" 9643 WOODHOLLOW CT","New Port Richey"],[" 10509 Plantation Bay Dr","Tampa"],
           [" 6235 Hawk Grove Court","Wesley Chapel"],[" 2328 Sand Bay Dr","Holiday"],[" 22632 St Thomas Cir","Lutz"],
           [" 1862 Narrington Avenue","North Port"],[" 15544 Locustberry Ct","Land O Lakes"],[" 3944 Glen Oaks Manor Dr","Sarasota"],
           [" 910 Tangelo Pl","Brandon"],[" 3030 W Palmetto St","Tampa"],[" 4416 Flatbush Ave","Sarasota"],
           [" 16134 Bridgedale Drive","Lithia"],[" 2219 Summit View Dr","Valrico"],[" 2859 Maple Brook Loop","Lutz"],
           [" 1795 Suffolk Dr","Clearwater"],[" 5121 Birch Ave","Sarasota"],[" 13504 Palmwood Ln","Tampa"],
           [" 7746 Deer Foot Dr","New Port Richey"],[" 13129 Fennway Ridge Dr","Riverview"],[" 3350 Dellefield St","New Port Richey"],
           [" 1353 Windsor Way","Lutz"],[" 432 Summit Chase Dr","Valrico"],[" 12950 White Bluff Rd","Hudson"],
           [" 2006 Thornbush Pl","Brandon"],[" 2148 Clover Hill Rd","Palm Harbor"],[" 9421 St Regis Ln","Port Richey"],
           [" 1306 Haney Ct","Valrico"],[" 16120 Gardendale Dr","Tampa"],[" 6750 Abady Ln","North Port"],
           [" 13415 88th Ave ","Seminole"],[" 9337 122nd Way","Seminole"],[" 2326 Timbergrove Dr","Valrico"],
           [" 6308 Tierra Vista Cir","Lakeland"],[" 6240 Westport Dr","Port Richey"],[" 12314 Field Point Way","Spring Hill"],
           [" 1152 View Pointe Cir","Lake Wales"],[" 1034 Highview Dr","Lake Wales"],[" 16606 Kingletside Ct","Lithia"],
           [" 4624 Roundview Ct","Land O' Lakes"],[" 423 Down Pine Dr","Seffner"],[" 4549 Dewey Dr","New Port Richey"],
           [" 11118 Black Forest Trail","Riverview"],[" 1250 Holly Cir","Oldsmar"],[" 2286 Islander Ct","Palm Harbor"],
           [" 3955 SE 17th St","Ocala"],[" 275 Bentley Oaks Blvd","Auburndale"],[" 4440 Ironwood Cir 203","Bradenton"],
           [" 6140 35th Ave N ","Saint Petersburg"],[" 9414 Willow Cove Ct","Tampa"],[" 520 N Larry Cir","Brandon"],
           [" 9218 SE 120th Loop","Summerfield"],[" 27552 Hialeah Way","Zephyrhills"],[" 5650 Sunset Falls Dr","Apollo Beach"],
           [" 181 Highland Meadows St","Davenport"],[" 3203 Sago Point Ct","Land O' Lakes"],[" 4087 Southwest 46th Terrace","Ocala"],
           [" 10141 SE 69th Ave","Belleview"],[" 814 Whisper Lake Court","Winter Haven"],[" 3301 Russett Pl","Land O' Lakes"],
           [" 2836 ORCHID LN","Lakeland"],[" 8621 Shadblow Ct Unit #4","Port Richey"],[" 3108 Pineview Dr","Holiday"],
           [" 1355 PInellas Bayway South, Unit 23","St Petersburg"],[" 1203 NE 5th St","Mulberry"],[" 12 lefe ct","HAINES CITY"],
           [" 826 Pebblewood Dr","Brandon"],[" 3904 Lockridge Dr","Land O' Lakes"],[" 1505 22nd Ave W","Palmetto"],
           [" 7337 Jackson Springs Rd","Tampa"],[" 11205 Kiskadee Cir","New Port Richey"],[" 28508 Meadowrush Way","Zephyrhills"],
           [" 4421 windmill point drive","Plant city"],[" 7903 Longwood Run Lane","Tampa"],[" 5406 Charlin Ave","Lakeland"],
           [" 9224 Lido Ln","Port Richey"],[" 12906 123rd Ave N","Largo"],[" 5105 39th Ave N","St. Petersburg"],
           [" 1770 Biarritz Cir","Tarpon Springs"],[" 7616 Hampshire Garden Pl","Apollo Beach"],[" 5212 Clover Mist Dr","Apollo Beach"],
           [" 2311 Brisbane st unit 59","Clearwater"],[" 206 Longview Avenue","Celebration"],[" 308 Barrymore Dr","Rockledge"],
           [" 8532 Redleaf Ln","Orlando"],[" 935 N Halifax Ave #904","Daytona Beach"],[" 1819 Anna Catherine Dr","Orlando"],
           [" 3470 North Tropical Trail","Merritt Island"],[" 2321 Vista Palm Dr","Edgewater"],[" 150 Maywood Ave NW","Palm Bay"],
           [" 430 Rockafellow Way","Orlando"],[" 5596 Gulf Stream Street","Tavares"],[" 848 Parkwood Ave","Titusville"],
           [" 10338 Little Econ St","Orlando"],[" 1410 Silver Cove Dr","Clermont"],[" 628 E Church St","DeLand"],
           [" 14530 Quail Trail Cir","Orlando"],[" 2107 Newmark Dr","Deltona"],[" 7046 Cadiz Blvd","Orlando"],
           [" 3122 Stern Ct","Kissimmee"],[" 1555 Hilltop Ln","Merritt Island"],[" 1820 Smoketree Cir","Apopka"],
           [" 3826 Beacon Ridge Way","Clermont"],[" 1725 W Marshall Lake Dr","Apopka"],[" 1910 Willow Oak Dr","Edgewater"],
           [" 3711 Fairfield Dr","Clermont"],[" 1312 Swiss Lane","Deltona"],[" 8106 Enchantment Drive","Windermere"],
           [" 32 Virginia Ave","DeLand"],[" 1026 S Lakemont Ave","Winter Park"],[" 415 Terrace Hill Blvd","DeBary"],
           [" 530 Baldwin Ct","Deltona"],[" 7322 Cypress Grove Rd","Orlando"],[" 273 Luis Ln","DeBary"],
           [" 664 Smokerise Boulevard","Longwood"],[" 248 Kenlake Dr","Deltona"],[" 1083 Swanson Dr","Deltona"],
           [" 19 E Preston St","Orlando"],[" 1592 Vista Lake Cir","Melbourne"],[" 625 Waterland Ct","Orlando"],
           [" 1272 Howland Blvd","Deltona"],[" 1560 Auburn Hills Ct","Tavares"],[" 1432 Sara L St","Kissimmee"],
           [" 649 Hangnest Ln","Lake Mary"],[" 3182 Quail Dr","Deltona"],[" 3096 Constellation Dr","Melbourne"],
           [" 2831 Charmont Dr","Apopka"],[" 2915 vista ct","Kissimmee"],[" 3113 River Branch Cir","Kissimmee"],
           [" 9540 Muse Pl","Orlando"],[" 1869 Wallace Ave","Melbourne"],[" 14042 Avenue of the Groves","Winter Garden"],
           [" 4215 Underpass Rd","Mascotte"],[" 2810 Stratford Pointe Dr","West Melbourne"],[" 13332 Moss Park Ridge Dr","Orlando"],
           [" 3808 Westerham Dr","Clermont"],[" 2757 Merrieweather Ln","Kissimmee"],[" 4825 PASCO AVE","Titusville"],
           [" 19333 Spring Oak Dr","Eustis"],[" 439 Eastbridge Dr","Oviedo"],[" 2352 Seven Oaks Dr","Saint Cloud"],
           [" 893 South Dean Circle","Deltona"],[" 226 Windflower Way","Oviedo"],[" 175 Windflower Way","Oviedo"],
           [" 3322 Chica Cir","West Melbourne"],[" 8553 Crescendo Ave","Windermere"],[" 11213 Savannah Landing Cir","Orlando"],
           [" 1617 Cotswold Dr","Orlando"],[" 39824 Grove Heights","Lady Lake"],[" 31 Spring Glen Dr","DeBary"],
           [" 812 Badger Dr NE","Palm Bay"],[" 447 Wellwood St SW","Palm Bay"],[" 10805 Oak Glen Cir","Orlando"],
           [" 2012 N Prince Ct","Winter Park"],[" 2545 Revolution St unit 103","Melbourne"],[" 3370 Bartlett Avenue Northeast","Conyers"],
           [" 1201 Red Fox Cir","Woodstock"],[" 421 Morgan Pl SE","Atlanta"],[" 812 Cedar Lake Dr SE","Conyers"],
           [" 513 Two Iron Way","Kennesaw"],[" 100 Grassnut Ct","Roswell"],[" 2425 Wild Iris Ln NE","Dacula"],
           [" 9415 Red Bird Ln","Alpharetta"],[" 925 Herterton Way","Alpharetta"],[" 1953 Haydenbrook Cove Northwest","Acworth"],
           [" 1354 Wichita Dr SW","Atlanta"],[" 4568 Blakedale Rd","Roswell"],[" 519 Ansley Forest Dr","Monroe"],
           [" 1240 Kingsview Cir SE","Smyrna"],[" 640 South Preston Court","Alpharetta"],[" 10585 Branham Fields Rd","Duluth"],
           [" 6204 Cascade Falls Dr","Buford"],[" 693 Bonnie Dell Dr","Marietta"],[" 6356 Blue Lake Ct","Buford"],
           [" 150 Enclave Court","Roswell"],[" 5915 Abbotts Run Tr","Duluth"],[" 3617 Woodlark Dr","Roswell"],
           [" 4488 Sudbury Rd","Atlanta"],[" 6740 Valley Ct","Douglasville"],[" 4245 Prestley Mill Rd","Douglasville"],
           [" 1080 Copper Creek Drive","Canton"],[" 4958 Vireo Dr","Flowery Branch"],[" 5882 Sunflower Ct","Ellenwood"],
           [" 3678 Creekstone Dr","Norcross"],[" 429 Orchid Lane","Canton"],[" 244 Weatherstone Pointe Dr","Woodstock"],
           [" 114 Silver Creek Dr","Canton"],[" 355 Ivy Mill Ct","Roswell"],[" 29 Adelaide Xing","Acworth"],
           [" 3945 Piper Glen Dr NE","Buford"],[" 252 Bonnie Sue Dr","Villa Rica"],[" 202 Woodview Ln","Woodstock"],
           [" 2684 Kenwood Dr","Duluth"],[" 2515 Columbia Crossing Ct","Decatur"],[" 7711 Soaring Eagle Dr","Flowery Branch"],
           [" 2522 Meadowglen Trail","Snellville"],[" 2155 Pendleton Pl NW","Suwanee"],[" 6857 Creekwood Dr","Douglasville"],
           [" 8412 Members Dr","Jonesboro"],[" 106 Hearthstone Drive","Woodstock"],[" 3 Wyndham Ct","Powder Springs"],
           [" 3119 Lake Point Circle","Acworth"],[" 2650 Ashbourne Dr NE","Lawrenceville"],[" 910 Township Circle","Alpharetta"],
           [" 3003 Greymont Cloister","Douglasville"],[" 365 Caledonian Cir","Dallas"],[" 727 Retreat Woods Way","Dacula"],
           [" 3622 Tree View Dr","Snellville"],[" 1672 Lancaster Creek Cir SW","Conyers"],[" 6076 Fairington Farms Lane","Lithonia"],
           [" 1159 Arborhill Dr","Woodstock"],[" 2584 Oak Village Place Northeast","Marietta"],[" 5371 Grey Stag Ct","Suwanee"],
           [" 105 S Links Dr","Covington"],[" 4794 Woodspring Dr NE","Marietta"],[" 447 Center Cir SW","Conyers"],
           [" 1638 Silvergrass Ln","Grayson"],[" 1857 Keith Drive Southwest","Marietta"],[" 33 Lorraine Valley","Winder"],
           [" 505 Carybell Lane","Alpharetta"],[" 1220 Hidden Creek Point","Cumming"],[" 2773 Prado Lane","Marietta"],
           [" 4582 Knight's Bridge Ct","Douglasville"],[" 32 Plantation Way","Acworth"],[" 749 Havenridge Dr SW","Conyers"],
           [" 3334 Benthollow Ln","Duluth"],[" 53 Rayner Dr","Newnan"],[" 7752 Horseshoe Bend","Lithonia"],
           [" 2353 Bluff Creek Overlook","Douglasville"],[" 393 Castle Top Ln SE","Lawrenceville"],[" 6066 Brookmere Ln SE","Mableton"],
           [" 50 Nesbit Pl","Alpharetta"],[" 12135 Wallace Woods Ln","Alpharetta"],[" 2459 Parcview Run Cove Northwest","Duluth"],
           [" 5601 Festival Ave","Fairburn"],[" 231 Hampton Station Blvd","Canton"],[" 2680 Loch Way","Snellville"],
           [" 1319 Richard Rd","Decatur"],[" 5755 Stephens Mill Dr","Buford"],[" 5758 Village Loop","Fairburn"],
           [" 1891 Bridle Rd","Lawrenceville"],[" 1285 Matt Moore Ct","Lithia Springs"],[" 170 Crimson Dr","Dallas"],
           [" 3197 Robin Rd","Decatur"],[" 12 Cornelia Ct","Dallas"],[" 5622 Walden Farm Drive","Powder Springs"],
           [" 4249 Rosehall Ct","Atlanta"],[" 6851 roswell rd ne unit j7","Atlanta"],[" 6568 Convinto St","Las Vegas"],
           [" 6727 Twisted Wood Dr","Las Vegas"],[" 700 Carnegie St #612","Henderson"],[" 2841 Briar Knoll Dr","Henderson"],
           [" 5212 MOUNTAIN GARLAND LN","NORTH LAS VEGAS"],[" 11217 Campanile St","Las Vegas"],[" 6624 N Lavender Lion Street,","North Las Vegas"],
           [" 8622 Kingston Heath Ct","Las Vegas"],[" 2526 Rocky Countryside St","North Las Vegas"],[" 5424 Gold Country St","Las Vegas"],
           [" 5492 Tantalum Ln","Las Vegas"],[" 1759 Crystal Stream Ave","Henderson"],[" 2088 Waterlily View St","Henderson"],
           [" 10983 Hunting Hawk Rd","Las Vegas"],[" 1211 E Arrow Lake Ct","Fort Mill"],[" 1870 Steeplechase Dr","Rock Hill"],
           [" 1330 Spring View Ct","Rock Hill"],[" 119 Woodside Village Dr","Rock Hill"],[" 2022 Karla Drive","Clover"],
           [" 1318 Cog Hill Court","Rock Hill"],[" 1471 Juanita Ave","Rock Hill"],[" 429 Dutch White Drive","Clover"],
           [" 1335 Spring View Ct","Rock Hill"],[" 440 Scarlett Ln","Fort Mill"],[" 127 Scotch Pine Dr","York"],
           [" 15714 Strickland Court","Charlotte"],[" 7689 Sedgebrook Dr E","Stanley"],[" 13717 Thompson Rd","Mint Hill"],
           [" 4500 Fenwick Court","Charlotte"],[" 2501 Yorkdale Dr","Charlotte"],[" 149 Albany Dr","Mooresville"],
           [" 8920 Leinster Dr","Charlotte"],[" 2108 Hunters Trail Dr","Indian Trail"],[" 8619 Verbena Ct","Harrisburg"],
           [" 10396 Dowling St NW","Huntersville"],[" 10913 Persimmon Creek Dr","Mint Hill"],[" 1005 Wadsworth Lane","Indian Trail"],
           [" 4950 El Molino Dr","Charlotte"],[" 9200 Four Acre Ct.","Charlotte"],[" 8405 Royster Run","Marvin"],
           [" 320 Royal Windsor Dr","Midland"],[" 831 Brightwood Ln","Matthews"],[" 2460 Marthas Ridge Dr","Statesville"],
           [" 1008 Anduin Falls Dr","Charlotte"],[" 1436 Ridgehaven Rd","Waxhaw"],[" 7315 Reedy Creek Rd","Charlotte"],
           [" 8514 Mayerling Drive","Charlotte"],[" 15015 Callow Forest Dr","Charlotte"],[" 6521 point comfort lane","Charlotte"],
           [" 2131 Verde Creek Rd","Charlotte"],[" 129 Natawest Dr","Statesville"],[" 8718 Cornwall St","Locust"],
           [" 1412 Mount VERNON AVE","Statesville"],[" 6339 Pink Dogwood Ln","Charlotte"],[" 6333 Glengarrie Ln","Huntersville"],
           [" 10794 Traders Ct","Davidson"],[" 3509 Buckeye Ct","Waxhaw"],[" 2425 Radrick Ln","Charlotte"],
           [" 1683 Backcreek Ln","Gastonia"],[" 8410 Golden Oak Ct","Charlotte"],[" 8702 Bodkin Ct","Charlotte"],
           [" 2536 Covington Loop","Graham"],[" 710 Sharon Dr","Waxhaw"],[" 6400 Rosebriar Ln","Charlotte"],
           [" 2514 Cranbrook Ln #8","Charlotte"],[" 3003 camrose crossing","Matthews"],[" 2701 Kendrick Dr","Charlotte"],
           [" 10309 Old Carolina Drive","Charlotte"],[" 209 Farm Springs Dr","Mount Holly"],[" 7420 Edgefield Ct","Matthews"],
           [" 1263 Sydnor Ave","Gastonia"],[" 1052 Churchill Downs Court Apt. G","Charlotte"],[" 264 Glennallen Rd","Mooresville"],
           [" 6318 Wind Ridge Dr","Charlotte"],[" 11406 Sweetbriar Ridge Dr","Charlotte"],[" 1612 Venture Oaks Ln","Monroe"],
           [" 16017 Hollingbourne Rd","Huntersville"],[" 2418 Wildburne Ct","Charlotte"],[" 4017 Caldwell Ridge Pkwy","Charlotte"],
           [" 14002 Green Birch Dr","Pineville"],[" 16810 Summers Walk Blvd","Davidson"],[" 616 Jim Parker Road","Monroe"],
           [" 14006 Green Birch Drive","Pineville"],[" 2003 Redwood Dr","Indian Trail"],[" 12245 Silveroak Ln","Charlotte"],
           [" 5721 Versage Dr","Mint Hill"],[" 1388 Bottle Brush Ln","Harrisburg"],[" 8749 Stratton Farm Rd","Huntersville"],
           [" 212 Weldon Circle","Mount Holly"],[" 1573 Pecan Ave","Charlotte"],[" 4738 Stoney Branch Drive","Charlotte"],
           [" 7949 Kerrybrook Cir","Charlotte"],[" 11301 Walking Horse Ln","Charlotte"],[" 3060 Grassy Meadows Ct","Lincolnton"],
           [" 11115 Scrimshaw Ln","Charlotte"],[" 8336 Cricket Lake Dr","Charlotte"],[" 10046 Treeside Ln","Matthews"],
           [" 3123 N Davidson St Ste 210","Charlotte"],[" 5529 Seths Dr","Charlotte"],[" 4830 Samuel Pinckney Dr","Belmont"],
           [" 3926 Etheredge St","Indian Trail"],[" 1316 Parkside Dr","Monroe"],[" 5719 D Bramblegate Rd","Greensboro"],
           [" 5461 Coleman Cir NW","Concord"],[" 5249 Murrayhill Rd","Charlotte"],[" 3808 Bluestem Dr","Greensboro"],
           [" 1739 Havenbrook Ct","Clemmons"],[" 867 E Morelos St","Chandler"],[" 4450 E Chaparosa Way","Cave Creek"],
           [" 2501 N 109th Ave","Avondale"],[" 3808 S 99th Dr","Tolleson"],[" 23871 N 163rd Dr","Surprise"],
           [" 3339 W Columbine Dr","Phoenix"],[" 1639 W Michigan Ave","Phoenix"],[" 2331 S Karen Dr","Chandler"],
           [" 22227 N 29th Dr","Phoenix"],[" 3830 E McDowell Rd  Unit 108","Phoenix"],[" 3820 E McDowell Rd  Unit 102","Phoenix"],
           [" 618 W Rosal Ave","Apache Junction"],[" 2138 E Fremont Dr","Tempe"],[" 11132 E Sheridan Ave","Mesa"],
           [" 3426 W Juniper Ave","Phoenix"],[" 7741 W Granada Rd","Phoenix"],[" 6610 W Mescal St","Glendale"],
           [" 1083 E Minton Dr","Tempe"],[" 11027 N 51st Dr","Glendale"],[" 3419 E Angela Dr","Phoenix"],
           [" 658 W Yellow Wood Ave","San Tan Valley"],[" 1897 W Appaloosa Way","Queen Creek"],[" 16395 W Monroe St","Goodyear"],
           [" 6105 W Moreland St","Phoenix"],[" 5621 E Flossmoor Ave","Mesa"],[" 2622 E Beverly Ln","Phoenix"],
           [" 15926 W Monte Cristo Ave","Surprise"],[" 1064 W 23rd Ct","Apache Junction"],[" 10123 S 184th Dr","Goodyear"],
           [" 5643 W Yucca St","Glendale"],[" 12933 W Via Camille","El Mirage"],[" 9229 S Las Lomitas Pl","Phoenix"],
           [" 8362 W Rosewood Ln","Peoria"],[" 1403 W Michelle Dr","Phoenix"],[" 4761 E Portola Valley Dr Unit 101","Gilbert"],
           [" 13134 W Citrus Way","Litchfield Park"],[" 12452 W San Miguel Ave","Litchfield Park"],[" 8022 S 26th St","Phoenix"],
           [" 18417 W Sunnyslope Ln","Waddell"],[" 10109 W Potter Dr","Peoria"],[" 1231 N Matlock","Mesa"],
           [" 1040 W Heather Dr","Mesa"],[" 3743 W Wayne Ln","Anthem"],[" 40521 N Territory Trl","Anthem"],
           [" 1636 S 114th Dr","Avondale"],[" 14321 W Mauna Loa Ln","Surprise"],[" 2357 W Melody Dr","Phoenix"],
           [" 15718 W Jenan Dr","Surprise"],[" 17470 N 92nd Gln","Peoria"],[" 1102 E Villa Theresa Dr","Phoenix"],
           [" 6083 S 252nd Dr","Buckeye"],[" 5519 E Delta Ave","Mesa"],[" 7838 E Keim Dr","Scottsdale"],
           [" 4558 W Joshua Blvd","Chandler"],[" 1806 W Muirwood Dr","Phoenix"],[" 2642 E Hartford Ave","Phoenix"],
           [" 2411 W Blue Sky Dr","Phoenix"],[" 15930 N 91st Dr","Peoria"],[" 817 E Marco Polo Rd","Phoenix"],
           [" 35407 N Shorthorn Trl","San Tan Valley"],[" 1916 E Carson Dr","Tempe"],[" 17205 E Lantern Ln","Fountain Hills"],
           [" 6603 W Brown St","Glendale"],[" 1550 N Stapley Dr Unit 65","Mesa"],[" 9720 E Kiva Ave","Mesa"],
           [" 20001 N 48th Ln","Glendale"],[" 17716 W Columbine Dr","Surprise"],[" 3965 N Kibbey Ct","Buckeye"],
           [" 3223 W Lucia Dr","Phoenix"],[" 3046 E Caballero St","Mesa"],[" 6610 W Briles Rd","Phoenix"],
           [" 7729 S 37th Way","Phoenix"],[" 5240 N 16th Ln","Phoenix"],[" 2505 N 119th Dr","Avondale"],
           [" 25268 W Cranston Pl","Buckeye"],[" 8127 W Desert Cove Ave","Peoria"],[" 2327 W Alicia Dr","Phoenix"],
           [" 13519 W Windsor Blvd","Litchfield Park"],[" 13763 W Gilia Way","Peoria"],[" 5250 N 16th Ln","Phoenix"],
           [" 9304 E Lindner Ave","Mesa"],[" 21182 E Calle De Flores","Queen Creek"],[" 5856 E Hampton Ave","Mesa"],
           [" 13278 W Redfield Rd","Surprise"],[" 4350 E Princeton Ave","Gilbert"],[" 325 E Hackamore St","Mesa"],
           [" 27240 N Skipping Rock Rd","Peoria"],[" 1930 S Westwood Unit 37","Mesa"],[" 16624 S 14th St","Phoenix"],
           [" 1722 S Roanoke St","Gilbert"],[" 17255 W Maui Ln","Surprise"],[" 15071 W Heritage Oak Way","Surprise"],
           [" 5059 S Simon","Mesa"],[" 28384 N Cactus Flower Cir","San Tan Valley"],[" 10350 S 182nd Ave","Goodyear"],
           [" 1704 S 39th St Unit 30","Mesa"],[" 14602 W Amelia Ave","Goodyear"],[" 8556 W Purdue Ave","Peoria"],
           [" 10905 W Davis Ln","Avondale"],[" 1716 N Hibbert","Mesa"],[" 236 E Paso Fino Way","San Tan Valley"],
           [" 14475 N 155th Dr","Surprise"],[" 9703 E Kiva Ave","Mesa"],[" 13429 W Jacobson Dr","Litchfield Park"],
           [" 20909 W Maiden Ln","Buckeye"],[" 12875 W Wilshire Dr","Avondale"],[" 2231 E Bowker St","Phoenix"],
           [" 1612 W Kuralt Dr","Anthem"],[" 15113 N El Frio Ct","El Mirage"],[" 5501 E Kings Ave","Scottsdale"],
           [" 293 W Dragon Tree Ave","San Tan Valley"],[" 28402 N 25th Ave","Phoenix"],[" 7440 W Sanna St","Peoria"],
           [" 17837 W Watson Ln","Surprise"],[" 2289 N 160th Ave","Goodyear"],[" 7621 S 18th Way","Phoenix"],
           [" 3134 E Capricorn Way","Chandler"],[" 11956 N 152nd Dr","Surprise"],[" 2249 W Calle Iglesia Ave","Mesa"],
           [" 20040 N 13th Dr","Phoenix"],[" 22913 N 121st Dr","Sun City"],[" 31 W Burkhalter Dr","Queen Creek"],
           [" 1148 E Nickleback St","Queen Creek"],[" 7724 W Redfield Rd","Peoria"],[" 7894 W Rock Springs Dr","Peoria"],
           [" 2657 S Valle Verde","Mesa"],[" 12937 W Earll Dr","Avondale"],[" 18131 W Mission Ln","Waddell"],
           [" 2812 W Mauna Loa Ln","Phoenix"],[" 4334 N 36th St","Phoenix"],[" 11517 W Chuckwalla Ct","Surprise"],
           [" 13009 W Weldon Ave","Phoenix"],[" 11859 W Hadley St","Avondale"],[" 4409 E Emile Zola Ave","Phoenix"],
           [" 14941 W Columbine Dr","Surprise"],[" 11911 W Honeysuckle Ct","Peoria"],[" 7808 E Valley Vista Dr","Scottsdale"],
           [" 10680 E Becker Ln","Scottsdale"],[" 3021 E Utopia Rd","Phoenix"],[" 8107 W San Miguel Ave","Glendale"],
           [" 3125 E Topeka Dr","Phoenix"],[" 3701 W Whitman Dr","Anthem"],[" 5315 N 1st Ave","Phoenix"],
           [" 10189 W Los Gatos Dr","Peoria"],[" 5162 W Kerry Ln","Glendale"],[" 13102 N Poppy St","El Mirage"],
           [" 17457 W Spring Ln","Surprise"],[" 4630 E Desert Willow Rd","Phoenix"],[" 5971 S Mack Ct","Gilbert"],
           [" 7225 E Knoll St","Mesa"],[" 8924 W Tierra Buena Ln","Peoria"],[" 14043 N 34th Pl","Phoenix"],
           [" 2241 E Soft Wind Dr","Phoenix"],[" 4103 E Montgomery Rd","Cave Creek"],[" 5437 S Forest Ave","Gilbert"],
           [" 113 W Bluefield Ave","Phoenix"],[" 14802 N 24th Dr","Phoenix"],[" 17336 W Lilac St","Goodyear"],
           [" 2249 S 85th Dr","Tolleson"],[" 8764 W El Caminito Dr","Peoria"],[" 15350 W Eugene Ter","Surprise"],
           [" 129 N 110th Dr","Avondale"],[" 5616 E Encanto St","Mesa"],[" 651 W Baylor Ln","Gilbert"],
           [" 3519 W Whispering Wind Dr","Glendale"],[" 3800 S Cantabria Cir Unit 1115","Chandler"],[" 534 N 105th Pl","Mesa"],
           [" 16724 N 177th Ave","Surprise"],[" 12129 N 85th Dr","Peoria"],[" 17637 N 168th Ln","Surprise"],
           [" 18237 N 45th Ave","Glendale"],[" 2063 W Gila Ln","Chandler"],[" 9136 E Auburn St","Mesa"],
           [" 6626 W Monona Dr","Glendale"],[" 1631 S Wildrose","Mesa"],[" 26896 N 90th Ln","Peoria"],
           [" 5674 E Harmony Ave","Mesa"],[" 2726 E Beautiful Ln","Phoenix"],[" 18508 W Oregon Ave","Litchfield Park"],
           [" 24803 W Pueblo Ave","Buckeye"],[" 12112 W Daley Ln","Sun City"],[" 3608 W Bluefield Ave","Glendale"],
           [" 4127 W Beverly Rd","Laveen"],[" 4302 E Karen Dr","Phoenix"],[" 8210 W Melinda Ln","Peoria"],
           [" 3306 W King Dr","Anthem"],[" 20996 W White Rock Rd","Buckeye"],[" 4241 N Miller Rd","Scottsdale"],
           [" 998 W Desert Mountain Dr","Queen Creek"],[" 3437 E Kingbird Pl","Chandler"],[" 13165 W Ventura St","Surprise"],
           [" 15506 N 170th Ln","Surprise"],[" 17025 E La Montana Dr Unit 111","Fountain Hills"],[" 12918 N 127th Dr","El Mirage"],
           [" 7108 S 70th Dr","Laveen"],[" 13854 W Gelding Dr","Surprise"],[" 838 W Oxford Dr","Tempe"],
           [" 2664 N Sterling","Mesa"],[" 9011 S 53rd Dr","Laveen"],[" 19622 N 66th Ln","Glendale"],
           [" 17577 W Ocotillo Ave","Goodyear"],[" 24524 W Mobile Ln","Buckeye"],[" 2140 E Broadmor Dr","Tempe"],
           [" 9600 N 96th St Apt 171","Scottsdale"],[" 17666 W Molly Ln","Surprise"],[" 12562 W Desert Rose Rd","Avondale"],
           [" 25033 N 67th Dr","peoria"],[" 1703 E Wesleyan Dr","Tempe"],[" 7908 S 41st Ln","Laveen"],
           [" 5550 N 16th St Apt 113","Phoenix"],[" 7733 W Heatherbrae Dr","Phoenix"],[" 89 E Macaw Ct","Queen Creek"],
           [" 2996 N Point Ridge Rd","Buckeye"],[" 4605 S Marron","Mesa"],[" 9821 W Yukon Dr","Peoria"],
           [" 29606 N Tatum Blvd Apt 268","Cave Creek"],[" 15772 W Caribbean Ln","Surprise"],[" 1836 N 65th Cir","Mesa"],
           [" 1214 E Greenway Cir","Mesa"],[" 5201 W Cheryl Dr","Glendale"],[" 10544 W Alex Ave","Peoria"],
           [" 27842 N Sierra Sky Dr","Peoria"],[" 4303 E Cactus Rd Apt 218","Phoenix"],[" 5415 W Red Bird Rd","Phoenix"],
           [" 20717 N 37th Way","Phoenix"],[" 5845 E Bramble Berry Ln","Cave Creek"],[" 6126 N 12th Pl Unit 9","Phoenix"],
           [" 8409 N 181st Dr","Waddell"],[" 1112 E Blue Spruce Ln","Gilbert"],[" 18217 W Montecito Ave","Goodyear"],
           [" 5673 W Laurie Ln","Glendale"],[" 15840 Laurel Ln N","Surprise"],[" 17578 W Cardinal Dr","Goodyear"],
           [" 2914 E Windsong Dr","Phoenix"],[" 42424 N Gavilan Peak Pkwy Unit 63212","Anthem"],[" 4347 W St Catherine Ave","Laveen"],
           [" 2305 N Heritage St","Buckeye"],[" 922 E Pontiac Dr","Phoenix"],[" 963 W Wendy Way","Gilbert"],
           [" 3118 E Topeka Dr","Phoenix"],[" 13578 W Hearn Rd","Surprise"],[" 4615 N 94th Ln","Phoenix"],
           [" 7944 W Larkspur Dr","Peoria"],[" 7570 W Krall St","Glendale"],[" 20038 N 49th Ln","Glendale"],
           [" 10786 W Yearling Rd","Peoria"],[" 16966 W Bradford Way","Surprise"],[" 3667 E San Pedro Ave","Gilbert"],
           [" 2215 W Wickieup Ln","Phoenix"],[" 2248 W Port Royale Ln","Phoenix"],[" 11010 W Laurelwood Ln","Avondale"],
           [" 16625 S 34th Way","Phoenix"],[" 4071 E Bruce Ave","Gilbert"],[" 8838 W Cinnabar Ave","Peoria"],
           [" 31361 N Blackfoot Dr","Queen Creek"],[" 3110 W Dailey St","Phoenix"],[" 13214 W Tether Trl","Peoria"],
           [" 8061 E Glenrosa Ave","Scottsdale"],[" 537 E Willetta St","Phoenix"],[" 19003 N 25th Pl","Phoenix"],
           [" 883 S Pheasant Dr","Gilbert"],[" 31690 N Blackfoot Dr","San Tan Valley"],[" 25644 W Rio Vista Ln","Buckeye"],
           [" 301 E Leland St","Mesa"],[" 19304 N 77th Dr","Glendale"],[" 4902 W Ironwood Dr","Glendale"],
           [" 22545 W Hadley St","Buckeye"],[" 3040 E Blackhawk Dr","Phoenix"],[" 2027 E Saddle Dr","San Tan Valley"],
           [" 2990 N Clanton St","Buckeye"],[" 110 W Ivanhoe St","Gilbert"],[" 10522 E Dragoon Ave","Mesa"],
           [" 16237 W Custer Ln","Surprise"],[" 6083 W Maui Ln","Glendale"],[" 2631 E Olivine Rd","San Tan Valley"],
           [" 6426 W El Cortez Pl","Phoenix"],[" 451 W Mountain Sage Dr","Phoenix"],[" 2940 S 94th Cir","Mesa"],
           [" 17891 W Badger Way","Goodyear"],[" 8546 W El Caminito Dr","Peoria"],[" 42 N Vineyard Ln","Litchfield Park"],
           [" 30568 N Zircon Dr","Queen Creek"],[" 11913 W Madison St","Avondale"],[" 27132 N 83rd Gln","Peoria"],
           [" 16614 N 174th Ln","Surprise"],[" 4650 E Decatur St","Mesa"],[" 703 E Rose Marie Ln","Phoenix"],
           [" 10152 W Hess St","Tolleson"],[" 15372 W Roanoke Ave","Goodyear"],[" 1033 N Arvada","Mesa"],
           [" 18235 N 20th Ln","Phoenix"],[" 22530 W Yavapai St","Buckeye"],[" 17340 W Bajada Rd","Surprise"],
           [" 2127 E Claire Dr","Phoenix"],[" 12545 S 176th Ave","Goodyear"],[" 1442 E Cindy St","Chandler"],
           [" 29151 N 70th Ave","Peoria"],[" 8636 W Tumblewood Dr","Peoria"],[" 5210 W Desert Cove Ave","Glendale"],
           [" 2742 W Steinbeck Ct","Anthem"],[" 18621 W Onyx Ave","Waddell"],[" 1736 N Makalu Cir","Mesa"],
           [" 14296 E Thoroughbred Trl","Scottsdale"],[" 21612 N 32nd Ave","Phoenix"],[" 7601 E 2nd St Unit 12","Scottsdale"],
           [" 9133 W Evans Dr","Peoria"],[" 7450 E Naranja Ave","Mesa"],[" 11413 W Davis Ln","Avondale"],
           [" 7938 W Wescott Dr","Glendale"],[" 17940 W Desert Ln","Surprise"],[" 4065 W Desert Cove Ave","Phoenix"],
           [" 15857 W Mercer Ln","Surprise"],[" 20467 N 37th Ave","Glendale"],[" 18839 N 16th Pl","Phoenix"],
           [" 5423 W Harrison Ct","Chandler"],[" 6005 N 10th Way","Phoenix"],[" 15246 W Calavar Rd","Surprise"],
           [" 431 S Laguna Dr","Gilbert"],[" 8126 E Jackrabbit Rd","Scottsdale"],[" 43246 N Vista Hills Dr","Anthem"],
           [" 4116 W Beautiful Ln","Laveen"],[" 25910 N 54th Ave","Phoenix"],[" 3219 W Lynne Ln","Phoenix"],
           [" 1437 E Topeka Dr","Phoenix"],[" 16774 W Ipswitch Way","Surprise"],[" 18514 W Sanna St","Waddell"],
           [" 15033 S 9th Pl","Phoenix"],[" 14578 W Cortez St","Surprise"],[" 1538 E Windmere Dr","Phoenix"],
           [" 7760 W Julie Dr","Glendale"],[" 18233 W Mission Ln","Waddell"],[" 4820 S Robins Way","Chandler"],
           [" 15020 N 48th Pl","Scottsdale"],[" 12829 S 184th Ave","Goodyear"],[" 4328 S Celebration Dr","Gold Canyon"],
           [" 7149 W Avenida Del Rey","Peoria"],[" 6546 W Tonopah Dr","Glendale"],[" 4024 W Lone Cactus Dr","Glendale"],[" 6828 S Roosevelt St","Tempe"],[" 7353 W Montgomery Rd","Peoria"],[" 5028 E Peak View Rd","Cave Creek"],[" 4419 E Mountain Sage Dr","Phoenix"],[" 29729 N 69th Ln","Peoria"],[" 2842 E Saguaro Park Ln","Phoenix"],[" 1465 E Nancy Ave","Queen Creek"],[" 10776 W El Cortez Pl","Peoria"],[" 813 W Village Pkwy","Litchfield Park"],[" 1817 N 77th St","Scottsdale"],[" 3933 E Salinas St","Phoenix"],[" 20705 N 37th Way","Phoenix"],[" 2491 W Binner Dr","Chandler"],[" 5930 N 86th St","Scottsdale"],[" 15103 W Melissa Ln","Surprise"],[" 41331 N Panther Creek Ct","Anthem"],[" 1344 E Piute Ave","Phoenix"],[" 14155 W La Reata Ave","Goodyear"],[" 22 E Mill Reef Dr","San Tan Valley"],[" 36031 N Matthews Dr","San Tan Valley"],[" 16028 N 3rd Ave","Phoenix"],[" 5851 W Geronimo St","Chandler"],[" 3842 E Thunderhill Pl","Phoenix"],[" 4831 N Granite Reef Rd","Scottsdale"],[" 3131 W Maya Way","Phoenix"],[" 6451 W Prickly Pear Trl","Phoenix"],[" 15072 W Post Dr","Surprise"],[" 5550 N 16th St Apt 162","Phoenix"],[" 33810 N 30th Ln","Phoenix"],[" 1531 W Corona Dr","Chandler"],[" 17808 W Ivy Ln","Surprise"],[" 8052 W Via Montoya Dr","Peoria"],[" 4349 E Cullumber St","Gilbert"],[" 17276 E Kirk Ln","Fountain Hills"],[" 7213 W Sunnyside Dr","Peoria"],[" 30153 N 71st Dr","Peoria"],[" 1812 W Nido Ave","Mesa"],[" 300 W Lyle Ave","San Tan Valley"],[" 21165 W Coronado Rd","Buckeye"],[" 10315 E Jan Ave","Mesa"],[" 3925 S Illinois St","Chandler"],[" 15782 W Cortez St","Surprise"],[" 15636 N 184th Ln","Surprise"],[" 1817 W Eastman Dr","Anthem"],[" 4857 W Cochise Dr","Glendale"],[" 21013 W Wycliff Dr","Buckeye"],[" 6010 E Rancho Manana Blvd","Cave Creek"],[" 10763 W Cottontail Ln","Peoria"],[" 2904 S 81st St","Mesa"],[" 3756 W Belle Ave","Queen Creek"],[" 4961 S Rincon Dr","Chandler"],[" 1703 W Hiddenview Dr","Phoenix"],[" 6510 N 3rd Ave Unit #4","Phoenix"],[" 3845 W Ashton Dr","Anthem"],[" 13541 S 184th Ave","Goodyear"],[" 3822 E White Aster St","Phoenix"],[" 15315 S 181st Dr","Goodyear"],[" 8725 E Chaparral Rd","Scottsdale"],[" 4540 W Powell Dr","New River"],[" 1403 W Villa Theresa Dr","Phoenix"],[" 17969 W Agave Rd","Goodyear"],[" 17940 W Verdin Rd","Goodyear"],[" 1 Leighton Ct","Mansfield"],[" 4405 Lorraine Ave","Grand Prairie"],[" 301 Cherokee Trl","Argyle"],[" 4227 Norway Ln","Grand Prairie"],[" 1105 Bainbridge Ln","Forney"],[" 2712 Sunlight Dr","Little Elm"],[" 815 W Rochelle Rd","Irving"],[" 1717 Duck Cove Dr","Aubrey"],[" 9903 Birch Dr","Providence Village"],[" 1314 Maplewood Dr","Lewisville"],[" 1418 Toplea Dr","Euless"],[" 1321 E Branch Hollow Dr","Carrollton"],[" 2608 Castle Creek Dr","Little Elm"],[" 13040 Pennystone Dr","Farmers Branch"],[" 814 Oak Hollow Ln","Anna"],[" 4916 Spoon Drift Dr","Fort Worth"],[" 1225 Hayden Ln","Savannah"],[" 1213 Mill Branch Dr","Garland"],[" 3920 Periwinkle Dr","Fort Worth"],[" 2101 Eisenhower Dr","McKinney"],[" 4300 Keeter Dr","Fort Worth"],[" 2512 Centaurus Dr","Garland"],[" 110 Lonesome Dove Ln","Forney"],[" 10613 Ambling Trl","Fort Worth"],[" 6401 Johns Way","Fort Worth"],[" 421 Rowdy Dr","Royse City"],[" 305 Goldfield Ln","Fort Worth"],[" 2602 Worth Forest Ct","Arlington"],[" 1307 London Dr","Wylie"],[" 2416 Pheasant Dr","Little Elm"],[" 1010 Bainbridge Ln","Forney"],[" 519 Easley St","Fort Worth"],[" 3427 Bellville Dr","Dallas"],[" 3708 Vista Greens Dr","Fort Worth"],[" 1701 Melanie Trl","Midlothian"],[" 500 Kempson Ct","Saginaw"],[" 6413 Stone Creek Trl","Fort Worth"],[" 6060 Arabian Ave","Fort Worth"],[" 5004 Caraway Dr","Fort Worth"],[" 215 Cabotwood Trl","Mansfield"],[" 4917 Creek Ridge Trl","Fort Worth"],[" 5003 Dawnwood Ct","Arlington"],[" 3205 Grenada Dr","Plano"],[" 3728 Cook Ct","Fort Worth"],[" 1521 Carol Dr","Fort Worth"],[" 16161 Cowboy Trl","Justin"],[" 220 Citrus Dr","Fate"],[" 9153 Benevolent Ct","Aubrey"],[" 118 S Young Blvd","Desoto"],[" 10129 Placid Dr","McKinney"],[" 904 Lake Worth Trl","Little Elm"],[" 3603 High Plains Ct","Arlington"],[" 3252 Silent Creek Trl","Fort Worth"],[" 2701 Daniel Crk","Mesquite"],[" 758 Holly Oak Dr","Lewisville"],[" 1500 6th Ave","Fort Worth"],[" 1516 Willoughby Way","Little Elm"],[" 1113 Grimes Dr","Forney"],[" 249 Lilac Ln","Azle"],[" 7109 Meadowside Rd S","Fort Worth"],[" 4113 River Birch Rd","Fort Worth"],[" 11044 Dillon St","Fort Worth"],[" 1040 Valley Brook Ln","Grand Prairie"],[" 1228 Cypress Ln","Lancaster"],[" 2041 Windsong Dr","Heartland"],[" 645 Spillway Dr","Little Elm"],[" 1711 Lancaster Gate","Allen"],[" 10100 Cherry Hill Ln","Providence Village"],[" 2517 Avalon Creek Way","McKinney"],[" 1524 Birds Eye Rd","Fort Worth"],[" 7801 Pebble Beach Dr","Rowlett"],[" 4618 Ebb Tide Dr","Rowlett"],[" 6001 Misty Breeze Dr","Fort Worth"],[" 305 Millford Rd","Roanoke"],[" 7209 Park Creek Cir E","Fort Worth"],[" 609 Harrison Dr","Coppell"],[" 1021 Pheasant Ln","Forney"],[" 991 Downey Dr","Lewisville"],[" 1 Buchanan Pl","Allen"],[" 1706 Ivy Ln","Carrollton"],[" 1436 Rivercrest Blvd","Allen"],[" 112 Matamoros St","Grand Prairie"],[" 3505 Jennifer Ln","Rowlett"],[" 841 Parkway Blvd","Coppell"],[" 8361 Bowspirit Ln","Hurst"],[" 2617 Lake Meadow Dr","McKinney"],[" 2003 Wellington Pt","Heartland"],[" 1080 Magnolia Ln","Cedar Hill"],[" 721 Sue Ann Ln","Burleson"],[" 1911 Sail Fish Dr","Mansfield"],[" 1300 Turnbridge Dr","Glenn Heights"],[" 5829 Terra Dr","Arlington"],[" 3017 Scenic Hills Dr","Bedford"],[" 5655 Gebron Ct","Fort Worth"],[" 110 Aspenwood Trl","Forney"],[" 11848 Bobcat Dr","Fort Worth"],[" 2210 Fallen Wood Dr","Mesquite"],[" 2001 Crestlake Dr","Little Elm"],[" 5832 Pearl Oyster Ln","Fort Worth"],[" 4148 Bedington Ln","Fort Worth"],[" 2000 Jasmine Ct","Forney"],[" 5618 Swan Lake Dr","Arlington"],[" 2955 Masters Ct S","Burleson"],[" 1413 Dun Horse Dr","Haslet"],[" 2420 Waterloo Ln","Mesquite"],[" 3212 Bonsai Dr","Plano"],[" 908 Cooper Ln","Royse City"],[" 4305 Timberglen Rd","Dallas"],[" 12600 Summerwood Dr","Burleson"],[" 1816 Sanderlain Ln","Allen"],[" 1210 Trenton Ln","Euless"],[" 4000 Autumnwood Ln","Heartland"],[" 509 Cassia Way","Arlington"],[" 1101 Kesser Dr","Plano"],[" 114 E Harvard Dr","Garland"],[" 4409 Lake Haven Dr","Rowlett"],[" 2441 Deerwood Dr","Little Elm"],[" 8400 Southern Prairie Dr","Fort Worth"],[" 9224 Turtle Pass","Fort Worth"],[" 1315 Churchill Dr","Denton"],[" 307 Paula Rd","McKinney"],[" 3900 Cresthill Rd","Benbrook"],[" 1233 Barrel Run","Haslet"],[" 7008 Shauna Dr","Fort Worth"],[" 5721 Crestwood Dr","Prosper"],[" 6808 Dalmation Cir","Plano"],[" 3849 Calculus Dr","Dallas"],[" 6624 Wooddale Dr","Watauga"],[" 5301 South Dr","Fort Worth"],[" 2232 Riverbirch Ln","Rockwall"],[" 2636 Mariners Dr","Little Elm"],[" 9008 Cloudveil Dr","Arlington"],[" 12517 Buelter Ct","Fort Worth"],[" 523 Colt Dr","Forney"],[" 920 Johnson City Ave","Forney"],[" 1108 Ponderosa Dr","Aubrey"],[" 1028 Triple Crown Dr","Fort Worth"],[" 5109 Crossvine Ln","McKinney"],[" 409 Lockhurst Dr","Anna"],[" 409 Hackberry Dr","Fate"],[" 5021 Village Stone Ct","Fort Worth"],[" 2105 Towanda Dr","Plano"],[" 8213 Tyler Dr","Lantana"],[" 3224 Shoreside Pkwy","Hurst"],[" 7428 Amber Dr","Watauga"],[" 8716 Granite Path","Fort Worth"],[" 1413 Elkford Ln","Justin"],[" 2556 Flowing Springs Dr","Fort Worth"],[" 4957 Happy Trl","Fort Worth"],[" 2624 Flowing Springs Dr","Fort Worth"],[" 7102 Lake Roberts Way","Arlington"],[" 728 Leading Ln","Allen"],[" 1743 Sunset Ridge Dr","Grand Prairie"],[" 14120 Dream River Trl","Haslet"],[" 14012 Sand Hills Dr","Haslet"],[" 1818 Signet Dr","Euless"],[" 1029 Janet St","Aubrey"],[" 9604 Birdville Way","Fort Worth"],[" 4844 Ambrosia Dr","Fort Worth"],[" 1101 Whispering Mdws","Crowley"],[" 1205 Aberdeen Dr","Allen"],[" 12528 Patnoe Dr","Fort Worth"],[" 1233 Morning Dove","Aubrey"],[" 2317 Point Star Dr","Arlington"],[" 2035 Oakbluff Dr","Carrollton"],[" 14725 Sawmill Dr","Little Elm"],[" 4940 Sunset Ridge Dr","Fort Worth"],[" 2312 Penton Way","Little Elm"],[" 5028 San Jacinto Dr","Haltom City"],[" 1936 Knoxbridge Rd","Forney"],[" 4945 Galley Cir","Fort Worth"],[" 11916 Yarmouth Ln","Fort Worth"],[" 1414 Ridgecreek Dr","Lewisville"],[" 10021 Vistadale Dr","Dallas"],[" 950 Meadow Cir N","Keller"],[" 8613 Crestview Dr","Fort Worth"],[" 4117 Green Acres Cir","Arlington"],[" 449 Legends Dr","Lewisville"],[" 631 Denali Dr","Arlington"],[" 1803 Cancun Dr","Mansfield"],[" 10045 Voss Ave","Fort Worth"],[" 518 Cooper Ln","Coppell"],[" 2021 Jackson Dr","Little Elm"],[" 8304 Muirwood Trl","Fort Worth"],[" 929 Warbler","Aubrey"],[" 2613 Shorecrest Dr","Little Elm"],[" 512 Crutcher Xing","McKinney"],[" 1052 Surrey Cir","Wylie"],[" 1710 Prescott Dr","Mansfield"],[" 2981 Thames Trl","Fort Worth"],[" 3504 Chilmark Ct","Dallas"],[" 309 Jasmine Ct","Burleson"],[" 606 Rolling Hills Dr","Aledo"],[" 5223 Windy Meadow Dr","Arlington"],[" 2112 Sandstone Ct","Mansfield"],[" 1021 Tara Dr","Burleson"],[" 706 S Jupiter Rd Apt 1105","Allen"],[" 2705 Castle Creek Dr","Little Elm"],[" 7201 Royal Oak Dr","Benbrook"],[" 1817 Mesquite Ln","Anna"],[" 8700 Lake Springs Trl","Hurst"],[" 2523 Glen Morris Rd","Carrollton"],[" 2025 Apple Dr","Little Elm"],[" 10169 Indian Mound Rd","Fort Worth"],[" 2904 Montague Trl","Wylie"],[" 1019 Kimbro Dr","Forney"],[" 1304 Pepperfield Ct","Burleson"],[" 113 Julia Dr","Fate"],[" 2608 Grand Canyon Ct","McKinney"],[" 1007 Fairfax Ct","Arlington"],[" 4221 Wild Plum Dr","Carrollton"],[" 9255 Crimnson Ct","Dallas"],[" 1848 Branch Trl","Carrollton"],[" 8412 Davis Dr","Frisco"],[" 4723 Sunflower Dr","McKinney"],[" 951 Behrens Ct","Crowley"],[" 6309 Lakewood Dr","Sachse"],[" 6517 Bluebonnet Dr","Rowlett"],[" 1415 Watercourse Way","Cedar Hill"],[" 8428 Gentian Dr","Fort Worth"],[" 9112 Azinger Dr","Plano"],[" 300 W Broadway St","Kennedale"],[" 10128 Pear St","Fort Worth"],[" 206 E Mistletoe Dr","Kennedale"],[" 3005 Morning Dove","McKinney"],[" 15009 Northview Dr","Little Elm"],[" 2805 Cross Bend Rd","Plano"],[" 4901 Haverford Dr","Arlington"],[" 4829 Applewood Rd","Fort Worth"],[" 918 Johnson City Ave","Forney"],[" 309 Lochwood Dr","Wylie"],[" 315 Elam Dr","Anna"],[" 305 Creekside Dr","Anna"],[" 2005 Bentwood Dr","Glenn Heights"],[" 1348 Amazon Dr","Justin"],[" 723 Biscayne Dr","Mansfield"],[" 1209 Coral Reef Ln","Wylie"],[" 133 Hilltop Dr","Anna"],[" 1225 Maplewood Dr","Crowley"],[" 2124 Shady Brook Dr","Bedford"],[" 2900 Tophill Ln","Flower Mound"],[" 104 Appalachian Way","McKinney"],[" 912 Prairie Grove Ln","Burleson"],[" 600 Middlefork","Irving"],[" 517 Hollyberry Dr","Mansfield"],[" 5208 Lava Rock Dr","Fort Worth"],[" 3425 Charing Cross Rd","Midlothian"],[" 6406 Springfield Dr","Arlington"],[" 7105 Top Rail Run","Fort Worth"],[" 1914 Bordeaux Ct","Allen"],[" 6624 Meadowpark Ct","Benbrook"],[" 2121 Preston Trl","Forney"],[" 10025 Fox Hill Dr","Fort Worth"],[" 2136 Bluebell","Forney"],[" 3228 Torio","Grand Prairie"],[" 1609 Danbury Dr","Garland"],[" 3204 Hornbeam St","Argyle"],[" 333 Longshore Dr","Little Elm"],[" 4006 Collin Ct","Heartland"],[" 1814 Willow Creek Ct","Garland"],[" 1805 Meadowlark Ln","Royse City"],[" 11250 Las Polamas Dr","Frisco"],[" 12721 Diamond Peak Dr","Fort Worth"],[" 3411 Lipizzan Dr","Denton"],[" 1730 Fern Ct","Lewisville"],[" 2912 Kimbrough Ln","McKinney"],[" 1012 Windymeadow Ln","McKinney"],[" 13216 Poppy Hill Ln","Fort Worth"],[" 3625 Lauren Dr","McKinney"],[" 2203 Hunter Place Ln","Arlington"],[" 4528 Worchester Ln","McKinney"],[" 1711 Pine Dr","Midlothian"],[" 1208 Edgewood Ln","Allen"],[" 5567 Mesa Verde Ct","Fort Worth"],[" 7520 Courtney Cir","Sachse"],[" 10234 Cava Rd","Frisco"],[" 4804 Red Velvet Rd","Fort Worth"],[" 2265 Riviera Dr","Little Elm"],[" 1231 Bristol Ln","Providence Village"],[" 312 Sweet Leaf Ln","Lake Dallas"],[" 4816 Bridle Path Way","Fort Worth"],[" 5812 Matt St","Fort Worth"],[" 1100 Rio Verde Dr","Desoto"],[" 10532 Lipan Trl","Fort Worth"],[" 8705 Vista Royale Dr","Fort Worth"],[" 2404 Rushing Springs Dr","Fort Worth"],[" 5017 Keating St","Fort Worth"],[" 613 Kearley Dr","Fate"],[" 504 Kylie Ln","Wylie"],[" 9124 Oldwest Trl","Fort Worth"],[" 1013 Jerry St","Aubrey"],[" 2432 Grand Rapids Dr","Fort Worth"],[" 3537 Pendery Ln","Fort Worth"],[" 207 Cherrybark Dr","Coppell"],[" 4309 Timberglen Rd","Dallas"],[" 229 S Heartz Rd","Coppell"],[" 6017 Saddle Bag Dr","Fort Worth"],[" 9129 Ripley St","Fort Worth"],[" 3804 Sage Dr","McKinney"],[" 1604 Abby Creek Dr","Little Elm"],[" 1429 Faringdon Dr","Plano"],[" 1812 Christopher Creek Dr","Little Elm"],[" 3417 Glenmoor Dr","Flower Mound"],[" 4125 Ainsly Ln","Fort Worth"],[" 7500 Archer Way","McKinney"],[" 729 Cedar Cove Dr","Princeton"],[" 606 Juniper Dr","Allen"],[" 1021 White Porch Ave","Forney"],[" 2133 Canyon Valley Trl","Plano"],[" 4525 Highridge Dr","The Colony"],[" 110 Abelia Dr","Fate"],[" 210 Anns Way","Forney"],[" 5208 Memorial Dr","Fort Worth"],[" 1111 Grimes Dr","Forney"],[" 2217 Benjamin Creek Dr","Little Elm"],[" 645 Swift Current Dr","Crowley"],[" 1025 Bruni Ct","Aubrey"],[" 825 Poncho Ln","Haslet"],[" 1707 Crestmeadow Ln","Mansfield"],[" 906 Grassy Glen Dr","Allen"],[" 2810 Royalty Dr","Garland"],[" 1320 Creekview Dr","Lewisville"],[" 6804 Edgefield Dr","Denton"],[" 106 Pearl Ln","Lake Dallas"],[" 6400 Sidney Ln","McKinney"],[" 1342 Old Barn Ln","Lewisville"],[" 2725 Stillwater Dr","Mesquite"],[" 2614 Baylor Dr","Rowlett"],[" 8312 Horse Whisper Ln","Fort Worth"],[" 7205 Dalewood Dr","Plano"],[" 2805 Chancellor Dr","Plano"],[" 2460 Deerwood Dr","Little Elm"],[" 4209 Marshall Ct","Plano"],[" 2109 Geneva Ln","McKinney"],[" 7800 Mallard Ln","Watauga"],[" 5344 Thornbush Dr","Fort Worth"],[" 5308 Bison Ct","Watauga"],[" 212 Birdbrook Dr","Anna"],[" 400 Kosstre Ct","Irving"],[" 3725 Hazel Dr","Fort Worth"],[" 12705 Ocean Spray Dr","Frisco"],[" 10408 Wooded Ct","Fort Worth"],[" 2111 Falcon Ridge Dr","Carrollton"],[" 11516 Blue Jack Trl","Fort Worth"],[" 5633 Sundance Dr","The Colony"],[" 11925 Sundog Way","Fort Worth"],[" 1809 Cancun Dr","Mansfield"],[" 108 Tall Meadow St","Azle"],[" 3912 Lands End Dr","McKinney"],[" 1916 Fairfield Dr","Plano"],[" 10319 Fireside Ln","Forney"],[" 7029 Mohegan Dr","Fort Worth"],[" 8700 Dayton Dr","Lantana"],[" 6908 Barbican Dr","Plano"],[" 303 Greenhill Ln","Rockwall"],[" 10011 Spokane Cir","Dallas"],[" 2412 Trailview Dr","Little Elm"],[" 3801 Lindale Dr","McKinney"],[" 2110 Falcon Ridge Dr","Carrollton"],[" 701 Denali Dr","Arlington"],[" 2737 Red Wolf Dr","Fort Worth"],[" 306 Saddle Tree Trl","Coppell"],[" 7533 Parkgate Dr","Fort Worth"],[" 3416 Bandera Ranch Rd","Roanoke"],[" 223 Chamberlain Dr","Fate"],[" 214 Cabotwood Trl","Mansfield"],[" 3436 Glade Creek Dr","Hurst"],[" 9204 Wellington Dr","Oak Point"],[" 1104 Rivers Creek Ln","Little Elm"],[" 3804 Aloe Dr","McKinney"],[" 2118 Hollow Way","Garland"],[" 1344 Finley Dr","Plano"],[" 4304 Rock Springs Dr","Plano"],[" 3413 Oceanview Dr","Denton"],[" 733 Acacia Dr","Anna"],[" 1011 Richmond Ln","Forney"],[" 833 Hems Ln","Arlington"],[" 9028 Fringewood Dr","Dallas"],[" 9181 Benevolent Ct","Aubrey"],[" 420 Ame Ln","Royse City"],[" 1108 Badger Vine Ln","Arlington"],[" 6309 Stone Lake Ct","Fort Worth"],[" 9933 Castlewood Dr","Plano"],[" 4808 Countryside Ct E","Fort Worth"],[" 4951 Eyrie Ct","Grand Prairie"],[" 3103 Vicky Ct","Garland"],[" 4101 Carmel Mountain Dr","McKinney"],[" 2612 Trumpet Dr","Rowlett"],[" 3808 Bluff Creek Ln","McKinney"],[" 2192 Erwin Dr","Euless"],[" 13018 Ambrose Dr","Frisco"],[" 4205 Hawkins Dr","McKinney"],[" 6337 Seagull Ln","Fort Worth"],[" 5505 Cojimar Dr","McKinney"],[" 5108 South Dr","Fort Worth"],[" 6232 Whitman Ave","Fort Worth"],[" 1602 Churchill Way","Rowlett"],[" 1503 Sharon Dr","Cedar Hill"],[" 5440 Shasta Ridge Ct","Fort Worth"],[" 521 Chestnut Trl","Forney"],[" 11506 Ocean Rd","Frisco"],[" 2617 Cedar Elm Ln","Plano"],[" 3824 Walden Way","Dallas"],[" 2824 Sharpview Ln","Dallas"],[" 4009 Sonora Dr","Plano"],[" 1814 Apache Trl","Mesquite"],[" 701 Catalina Aisle St","Las Vegas"],[" 1081 Via Gandalfi","Henderson"],[" 5127 Morning Splash Ave","Las Vegas"],[" 9124 Captivating Ave","Las Vegas"],[" 3308 Cheltenham St","Las Vegas"],[" 8151 Mosaic Sunrise Ln","Las Vegas"],[" 7633 Lots Hills Dr","Las Vegas"],[" 944 Tafalla Ct","Las Vegas"],[" 802 Rising Star Dr","Henderson"],[" 6994 Geronimo Springs Ave","Las Vegas"],[" 7232 Patmore Ash Ct","Las Vegas"],[" 6789 Medovina Ct","Las Vegas"],[" 9047 Sunpine Ct","Las Vegas"],[" 6179 Fisher Creek Ct","Las Vegas"],[" 5098 Bonnie Doon Ln","Las Vegas"],[" 6568 Netherseal Ave","Las Vegas"],[" 3624 Deer Flats St","Las Vegas"],[" 7871 Morning Gallop Ct","Las Vegas"],[" 5916 Kelitabb Ct","Las Vegas"],[" 4204 Park Ct","Las Vegas"],[" 9055 Edgeworth Pl","Las Vegas"],[" 6410 Crest Estates St","Las Vegas"],[" 5679 Balsam St","Las Vegas"],[" 10303 Wood Plank Ln","Las Vegas"],[" 5304 Tulip Hill Ave","Las Vegas"],[" 6472 Haypress Ct","Las Vegas"],[" 11166 Ranch Valley St","Las Vegas"],[" 6975 Comiskey Park St","Las Vegas"],[" 6409 Trautman Ct","Las Vegas"],[" 278 Divertimento St","Henderson"],[" 9117 Picket Fence Ave","Las Vegas"],[" 2269 Dalton Ridge Ct","North Las Vegas"],[" 352 Point Loma Ave","North Las Vegas"],[" 7009 Berkshire Pl","Las Vegas"],[" 2649 Whisper Ridge St","Las Vegas"],[" 6679 Catoctin Ave","Las Vegas"],[" 8708 Majestic Pine Ave","Las Vegas"],[" 10650 Mount Blackburn Ave","Las Vegas"],[" 1908 Taylorville St","Las Vegas"],[" 620 High Grass Ct","Henderson"],[" 9652 Gisborn Dr","Las Vegas"],[" 4925 Goldfield St","North Las Vegas"],[" 7291 S Bronco St","Las Vegas"],[" 9680 Withering Pine St","Las Vegas"],[" 2129 Leatherbridge Ct","North Las Vegas"],[" 1214 Starstone Ct","Henderson"],[" 10521 Seasonable Dr","Las Vegas"],[" 2408 Ailsa Craig St","Henderson"],[" 6983 Positano Hill Ave","Las Vegas"],[" 791 Flowing Meadow Dr","Henderson"],[" 8709 Palomino Ranch St","Las Vegas"],[" 9728 Forest Glen Pl","Las Vegas"],[" 2052 Houdini St","Henderson"],[" 917 Whitehollow Ave","North Las Vegas"],[" 7216 Mulberry Forest St","Las Vegas"],[" 399 Placer Creek Ln","Henderson"],[" 2553 Chateau Clermont St","Henderson"],[" 5852 Clear Haven Ln","North Las Vegas"],[" 2819 Geary Pl Unit 2707","Las Vegas"],[" 519 Parkstone Ln","Woodstock"],[" 165 Boxford Ct","Alpharetta"],[" 4362 Stockton Ter","Marietta"],[" 793 Cambron Commons Trce","Suwanee"],[" 831 Kinsey Ln","Lawrenceville"],[" 3966 Yosemite Park Ln","Snellville"],[" 418 Glouchester Dr","Locust Grove"],[" 3012 Summer Stream Ct NW","Kennesaw"],[" 3551 Adams Landing Dr","Powder Springs"],[" 4843 Carlene Way SW","Lilburn"],[" 3507 Vinings North Trl SE","Smyrna"],[" 3565 Ballybandon Ct","Cumming"],[" 2472 N Forest Dr","Marietta"],[" 6052 Kenbrook Cir NW","Acworth"],[" 410 Pinevale Ct","Atlanta"],[" 14161 Yacht Ter","Alpharetta"],[" 1966 Westover Ln NW","Kennesaw"],[" 2389 Scotney Castle Ln","Powder Springs"],[" 3579 Brookhill Cir","Marietta"],[" 4621 Kousa Ln","Snellville"],[" 2111 Deer Run Ct","Lawrenceville"],[" 1795 Stardust Trl","Cumming"],[" 2487 Insdale Trce NW","Acworth"],[" 1019 Flowers Xing","Lawrenceville"],[" 7554 Watson Cir","Locust Grove"],[" 410 Clubfield Dr","Roswell"],[" 10510 Virginia Pine Ln","Alpharetta"],[" 4108 Mulligan Ln NW","Acworth"],[" 1045 Haverhill Trl","Lawrenceville"],[" 10102 Clearwater Trl","Jonesboro"],[" 4343 Central Dr","Stone Mountain"],[" 10 Neely Run","Newnan"],[" 7117 Boulder Pass","Union City"],[" 2963 Vaughan Dr","Cumming"],[" 3400 Vista Creek Dr","Dacula"],[" 1008 Inca Ln","Woodstock"],[" 909 Michael Lee Way","Lawrenceville"],[" 1278 Dresden Cir","Hampton"],[" 1075 Julius Dr","Suwanee"],[" 2505 Woodfern Ct","Marietta"],[" 1420 Commonwealth Ln","Grayson"],[" 5109 Vinings Estates Way SE","Mableton"],[" 4253 Joshua Way NW","Kennesaw"],[" 3940 Pleasant Shade Dr","Atlanta"],[" 3613 Silver Brooke Ln NW","Kennesaw"],[" 4995 Willow Creek Dr","Woodstock"],[" 5618 Summer Meadow Pass","Stone Mountain"],[" 57 Wilburn Dr","Powder Springs"],[" 901 Silver Lake Dr","Acworth"],[" 229 Rocky Top Ct NE","Kennesaw"],[" 6064 Lucas St","Norcross"],[" 601 Georgia Cir","Loganville"],[" 2155 Knightsbridge Way","Alpharetta"],[" 295 Redwood Dr SW","Marietta"],[" 200 River Laurel Way","Woodstock"],[" 1629 Wilford Dr","Lawrenceville"],[" 293 Prescott Dr","Acworth"],[" 2975 Commonwealth Cir","Alpharetta"],[" 725 Palmer Dr SW","Marietta"],[" 2773 Pierce Brennen Ct","Lawrenceville"],[" 233 Highlands Dr","Woodstock"],[" 1699 Gloucester Way","Tucker"],[" 5844 Spring Mill Cir","Lithonia"],[" 1607 Old Hunters Trce","Marietta"],[" 1534 Josh Valley Ln","Lawrenceville"],[" 3896 Tanbark Ct NE","Marietta"],[" 2450 Traywick Chase","Alpharetta"],[" 1988 Cutleaf Creek Rd","Grayson"],[" 4566 Town Manor Dr","Douglasville"],[" 2819 Joyce Ave","Decatur"],[" 141 Amsterdam Dr SW","Lilburn"],[" 2174 Shillings Chase Dr NW","Kennesaw"],[" 2871 Rolling Downs Way","Loganville"],[" 3549 Meadow Chase Dr","Marietta"],[" 3861 Nations Dr","Douglasville"],[" 4065 Heritage Crossing Walk SW","Powder Springs"],[" 3730 Rolling Creek Dr","Buford"],[" 4108 Ashford Green Dr","Duluth"],[" 1437 Station Center Blvd","Suwanee"],[" 5619 Lancashire Ln","Cumming"],[" 170 Chickering Lake Dr","Roswell"],[" 2032 Wildcat Falls Ln","Lawrenceville"],[" 2350 Worthington Dr","Powder Springs"],[" 2331 Milstead Cir NE","Marietta"],[" 4673 Pine St SE","Smyrna"],[" 2947 Winding Way SW","Lilburn"],[" 169 Jans Mdws","Stockbridge"],[" 1807 Blakewell Ct","Snellville"],[" 6152 Norcross Glen Trce","Norcross"],[" 750 Melglory Rose Ct N","Stockbridge"],[" 540 Rabbits Run","Fayetteville"],[" 746 Retreat Woods Way","Dacula"],[" 3137 Perimeter Cir","Buford"],[" 408 Edmond Ct","Suwanee"],[" 5054 Vermack Rd","Dunwoody"],[" 7120 Cordery Rd","Cumming"],[" 820 Tramore Ct","Acworth"],[" 300 Breeze Ct","Canton"],[" 5770 Chestnut Dr","Cumming"],[" 4202 Lazy Creek Dr","Marietta"],[" 1476 Cave Springs Rd","Douglasville"],[" 336 Highview Dr SE","Smyrna"],[" 3922 Glen Meadow Dr","Norcross"],[" 3121 Jackson Creek Dr","Stockbridge"],[" 726 Lorimore Pass","Canton"],[" 1353 Champion Run Dr","Dacula"],[" 3752 Upland Dr","Marietta"],[" 555 Ramsdale Dr","Roswell"],[" 2631 Collins Cove Ave","Lawrenceville"],[" 2615 Ashbourne Dr","Lawrenceville"],[" 2730 the Terraces Way","Dacula"],[" 110 Westbrook Dr","Acworth"],[" 60 Mill Pond Rd","Roswell"],[" 3210 Evonvale Gln","Cumming"],[" 1767 Highlands Vw SE","Smyrna"],[" 2202 Oakrill Ct","Marietta"],[" 5545 Concord Downs Dr","Cumming"],[" 3742 Meeting St","Duluth"],[" 3771 Bays Ferry Way","Marietta"],[" 1460 Brookcliff Cir","Marietta"],[" 2388 Scotney Castle Ln","Powder Springs"],[" 2388 Roseberry Ln","Grayson"],[" 539 Wynbrooke Pkwy","Stone Mountain"],[" 111 Dragging Canoe","Woodstock"],[" 7125 Brassfield Dr","Cumming"],[" 2812 Summer Branch Ln","Buford"],[" 5440 Beaver Ridge Dr","Cumming"],[" 1951 Kinridge Rd","Marietta"],[" 2654 Ashley Dr S","Marietta"],[" 620 Sheringham Ct","Roswell"],[" 3919 Evans Rd","Cumming"],[" 4695 Stonehenge Dr","Peachtree Corners"],[" 232 Waters Lake Dr","Woodstock"],[" 12265 Stevens Creek Dr","Alpharetta"],[" 4577 Latimer Pointe NE","Kennesaw"],[" 5235 Orchard Ct","Cumming"],[" 625 Rockbass Rd","Suwanee"],[" 1441 Logan Cir","Marietta"],[" 1075 Brookstead Chase","Johns Creek"],[" 214 White Cloud Run","Canton"],[" 100 N Pond Ct","Roswell"],[" 6 Wyndham Ct","Powder Springs"],[" 1045 Fords Crossing Dr NW","Acworth"],[" 4021 Bramble Ct","Marietta"],[" 2755 Whitehurst Dr NE","Marietta"],[" 813 Southland Forest Way","Stone Mountain"],[" 3594 Baywater Ct","Snellville"],[" 425 Cameron Woods Ct","Alpharetta"],[" 971 White Cloud Rdg","Snellville"],[" 2915 Roxburgh Dr","Roswell"],[" 3560 Elinburg Dr","Buford"],[" 11252 Musette Cir","Alpharetta"],[" 485 Ramsdale Dr","Roswell"],[" 1600 Treybyrne Ct","Dacula"],[" 511 Autumn Walk","Canton"],[" 4499 Oakdale Vinings Lndg SE","Smyrna"],[" 4574 Woodland Cir NE","Roswell"],[" 8 the Meadows Dr","Newnan"],[" 7425 Bronson Way","Cumming"],[" 1545 Blyth Walk","Snellville"],[" 4636 Clary Lakes Dr NE","Roswell"],[" 6051 Kenbrook Cir NW","Acworth"],[" 354 Silvertop Dr","Grayson"],[" 4745 Summer Song Ct","Buford"],[" 2120 Deer Run Ct","Lawrenceville"],[" 152 River Ridge Ln","Roswell"],[" 105 Arden Pl","Alpharetta"],[" 1820 Waterbreeze Ct","Cumming"],[" 1784 Millhouse Run","Marietta"],[" 7540 Shadburn Ferry Rd","Cumming"],[" 3233 Little Bear Ln","Buford"],[" 2523 Waterscape Trl","Snellville"],[" 2611 Andover Dr","Doraville"],[" 1564 E Bank Dr","Marietta"],[" 1710 Dawn Valley Trl","Cumming"],[" 2246 Newt St","Orlando"],[" 419 Elkwood Ct","Orlando"],[" 411 Bonifay Ave","Orlando"],[" 4907 Cains Wren Trl","Sanford"],[" 3847 Wind Dancer Cir","Saint Cloud"],[" 4618 Tamworth Ct","Orlando"],[" 16045 Blossom Hill Loop","Clermont"],[" 504 Lost Creek Ct","Kissimmee"],[" 12825 Hunters Vista Blvd","Orlando"],[" 15 S Hart Blvd","Orlando"],[" 1585 Antoinette Ct","Oviedo"],[" 15485 Murcott Blossom Blvd","Winter Garden"],[" 9328 Mustard Leaf Dr","Orlando"],[" 127 Lisa Loop","Winter Spgs"],[" 1560 Purple Plum Ln","Oviedo"],[" 824 Royalwood Ln","Oviedo"],[" 613 Heather Brite Cir","Apopka"],[" 102 Royal Oaks Cir","Longwood"],[" 1120 Seneca Falls Dr","Orlando"],[" 5638 Elizabeth Rose Sq","Orlando"],[" 951 Kerwood Cir","Oviedo"],[" 1725 Alejo Dr","Apopka"],[" 506 W Foothill Way","Casselberry"],[" 754 Maple Leaf Loop","Winter Springs"],[" 6871 Helmsley Cir","Windermere"],[" 1519 Pier St","Clermont"],[" 2701 Eldred Ct","Apopka"],[" 8111 Jailene Dr","Windermere"],[" 1594 Antoinette Ct","Oviedo"],[" 2045 Lobelia Dr","Lake Mary"],[" 1905 Plantation Oak Dr","Orlando"],[" 1283 Calypso Way","Oviedo"],[" 2207 Wolf Ridge Ln","Mount Dora"],[" 808 Hamilton Place Ct","Winter Park"],[" 606 Fox Hunt Cir","Longwood"],[" 8231 Laureate Blvd","Orlando"],[" 281 N Wilderness Pt","Casselberry"],[" 1667 Marina Lake Dr","Kissimmee"],[" 2305 Stefanshire Ave","Ocoee"],[" 15625 Charter Oaks Trl","Clermont"],[" 8044 Rural Retreat Ct","Orlando"],[" 1391 Vickers Lake Dr","Ocoee"],[" 244 Volterra Way","Lake Mary"],[" 10451 Stone Glen Dr","Orlando"],[" 1585 Skye Ct","Apopka"],[" 9516 White Sand Ct","Clermont"],[" 11611 Lake Katherine Cir","Clermont"],[" 2227 Palm Vista Dr","Apopka"],[" 365 Needles Trl","Longwood"],[" 12515 Sawgrass Oak St","Orlando"],[" 2097 Hayfield Way","Apopka"],[" 8032 Saint James Way","Mount Dora"],[" 1137 Woodland Terrace Trl","Altamonte Springs"],[" 5868 Pine Grove Run","Oviedo"],[" 865 Copperfield Ter","Casselberry"],[" 1162 Bolton Pl","Lake Mary"],[" 3821 Andover Cay Blvd","Orlando"],[" 702 Waywood Ave","Orlando"],[" 2743 White Isle Ln","Orlando"],[" 2720 Hagen Ct","Longwood"],[" 616 Venice Pl","Sanford"],[" 500 Terrace Cove Way","Orlando"],[" 8385 Westcott Shore Dr","Orlando"],[" 1855 Mariposa Way","Clermont"],[" 4982 Strand St","Kissimmee"],[" 267 Westyn Bay Blvd","Ocoee"],[" 5485 Baldwin Park St","Orlando"],[" 627 S Ranger Blvd","Winter Park"],[" 3108 Burlington Dr","Orlando"],[" 1004 Wheeler Pl","Oviedo"],[" 2181 Westborough Ln","Kissimmee"],[" 11717 Malverns Loop","Orlando"],[" 4519 Appleby Ct","Orlando"],[" 1545 Indiana Ave","Winter Park"],[" 244 Cambridge Dr","Longwood"],[" 1400 E Harrison St","Oviedo"],[" 60 Cinnamon Dr","Orlando"],[" 1917 Rafton Rd","Apopka"],[" 3639 Craigsher Dr","Apopka"],[" 542 Waterscape Way","Orlando"],[" 1500 Robert St","Longwood"],[" 10128 Stanton Ct","Orlando"],[" 625 Heather Brite Cir","Apopka"],[" 8021 Indian Creek Blvd","Kissimmee"],[" 1278 Blackwater Pond Dr","Orlando"],[" 1101 Mission Ridge Ct","Orlando"],[" 3340 Lake Jean Dr","Orlando"],[" 369 Balogh Pl","Longwood"],[" 642 Woodridge Dr","Fern Park"],[" 1443 Cabot Dr","Clermont"],[" 9067 Laurel Ridge Dr","Mount Dora"],[" 321 Monticello Dr","Altamonte Springs"],[" 709 Grant Ave","Mount Dora"],[" 4361 Fox Glen Loop","Kissimmee"],[" 512 Wax Palm Ln","Chuluota"],[" 1508 Caterpillar St","Saint Cloud"],[" 32025 Bluegill Dr","Tavares"],[" 690 E Jackson Ave","Mount Dora"],[" 426 E 6th Ave","Windermere"],[" 991 Alston Bay Blvd","Apopka"],[" 441 Alinole Loop","Lake Mary"],[" 12918 Grand Bank Ln","Orlando"],[" 7610 Treasure Island Ct","Orlando"],[" 127 Quail Ridge Ct","Sanford"],[" 10032 Weathers Loop","Clermont"],[" 11526 Pineloch Loop","Clermont"],[" 276 Volterra Way","Lake Mary"],[" 2158 Marshall Rd","Maitland"],[" 3660 Oak Vista Ln","Winter Park"],[" 1845 Sanderling Dr","Clermont"],[" 14716 Royal Poinciana Dr","Orlando"],[" 1119 Seburn Rd","Apopka"],[" 1550 E Horatio Ave","Maitland"],[" 12953 Sawgrass Pine Cir","Orlando"],[" 14407 Magnolia Ridge Loop","Winter Garden"],[" 8228 Diamond Cove Cir","Orlando"],[" 8040 Saint James Way","Mount Dora"],[" 1665 Grange Cir","Longwood"],[" 531 Terrace Cove Way","Orlando"],[" 4060 Truelove Dr","Apex"],[" 200 Swan Quarter Dr","Cary"],[" 5106 Shagbark Dr","Durham"],[" 1328 Heritage Hills Way","Wake Forest"],[" 105 Blooming Meadows Rd","Holly Springs"],[" 646 Tyler Run Dr","Wake Forest"],[" 205 Hamlet Park Dr","Morrisville"],[" 5525 Wedgegate Dr","Raleigh"],[" 1529 Heritage Club Ave","Wake Forest"],[" 4243 the Oaks Dr","Raleigh"],[" 2305 Spruce Grove Ct","Raleigh"],[" 212 Napa Valley Way","Chapel Hill"],[" 5646 Wade Park Blvd","Raleigh"],[" 1001 Harvest Point Dr","Fuquay Varina"],[" 19 Red Feather Ct","Durham"],[" 1608 Hayesville Dr","Fuquay Varina"],[" 170 Ambergate Dr","Youngsville"],[" 2505 Boulder Ridge Dr","Raleigh"],[" 2929 Imperial Oaks Dr","Raleigh"],[" 8023 Lloyd Allyns Way","Raleigh"],[" 5248 Holly Ridge Farm Rd","Raleigh"],[" 7820 Harps Mill Rd","Raleigh"],[" 7601 Copper Creek Ct","Wake Forest"],[" 8513 Erinsbrook Dr","Raleigh"],[" 7200 Pekin Dr","Willow Spring"],[" 160 Scarlet Bell Dr","Youngsville"],[" 1100 Crinoline Ln","Morrisville"],[" 78 Genoa Ln","Clayton"],[" 2610 Haventree Ct","Apex"],[" 1244 Grovewood Dr","Clayton"],[" 1109 Warmoven St","Wake Forest"],[" 1312 Snyder St","Durham"],[" 110 Bristol Dr","Chapel Hill"],[" 208 Alamosa Pl","Cary"],[" 107 Hogan Ridge Ct","Chapel Hill"],[" 2261 Dunlin Ln","Raleigh"],[" 2924 Deep Glen Ct","Raleigh"],[" 105 La Quinta Ct","Cary"],[" 225 Callahan Trl","Garner"],[" 114 Genoa Ln","Clayton"],[" 2608 Follow Me Way","Raleigh"],[" 1000 Snow Peak Ct","Raleigh"],[" 308 Farrington Dr","Clayton"],[" 12400 Fieldmist Dr","Raleigh"],[" 173 Honeybee Trce","Clayton"],[" 8706 Winding River Way","Raleigh"],[" 816 Elbridge Dr","Raleigh"],[" 229 Grenoch Valley Ln","Apex"],[" 1006 Cantrell Ln","Apex"],[" 1103 Kimball Crest Ct","Fuquay Varina"],[" 859 E Maple Ln","Fuquay Varina"],[" 3702 Keohane Dr","Durham"],[" 11732 Dellcain Ct","Raleigh"],[" 406 Summerwind Plantation Dr","Garner"],[" 124 Silver Bluff St","Holly Springs"],[" 2112 Addenbrock Dr","Morrisville"],[" 1446 Cimarron Pkwy Apt 19","Wake Forest"],[" 1324 Kudrow Ln","Morrisville"],[" 9238 Wooden Rd","Raleigh"],[" 1401 Weslyn Springs Way","Fuquay Varina"],[" 82 Saxapahaw Run","Chapel Hill"],[" 9202 Wooden Rd","Raleigh"],[" 75 Marsh Creek Dr","Garner"],[" 2269 Dunlin Ln","Raleigh"],[" 508 Blooming Meadows Rd","Holly Springs"],[" 3917 Elmswick Ct","Apex"],[" 2620 Forestbluff Dr","Fuquay Varina"],[" 1216 Turner Woods Dr","Raleigh"],[" 105 Callandale Ln","Durham"],[" 133 Green Willows Dr","Clayton"],[" 9208 Sayornis Ct","Raleigh"],[" 905 Neuse Ridge Dr","Clayton"],[" 4001 Tilton Dr","Raleigh"],[" 404 Timber Cut Ln","Apex"],[" 233 Nelson Ln","Clayton"],[" 734 Hillsford Ln","Apex"],[" 459 Averasboro Dr","Clayton"],[" 1119 Virginia Water Dr","Rolesville"],[" 2508 Heathcote Ln","Apex"],[" 1908 Hillock Dr","Raleigh"],[" 474 Beacon Ridge Blvd","Chapel Hill"],[" 912 Coral Bell Dr","Wake Forest"],[" 2933 Charleston Oaks Dr","Raleigh"],[" 5436 Downton Grove Ct","Fuquay Varina"],[" 4714 Myra Glen Pl","Durham"],[" 104 Sonoma Valley Dr","Cary"],[" 1304 Barnford Mill Rd","Wake Forest"],[" 4232 Green Drake Dr","Wake Forest"],[" 409 Beckwith Ave","Clayton"],[" 1305 Heritage Hills Way","Wake Forest"],[" 233 Royal Troon Dr","Cibolo"],[" 8006 Oakmont Downs","Schertz"],[" 104 Falcon Xing","Cibolo"],[" 13911 Brays Frst","San Antonio"],[" 9642 Maytum Cir","Helotes"],[" 9403 Gillcross Way","San Antonio"],[" 330 Soaring Breeze","San Antonio"],[" 329 Hummingbird Dr","New Braunfels"],[" 421 American Flag","Schertz"],[" 24939 Crescent Run","San Antonio"],[" 5822 Gardenwood St","San Antonio"],[" 4939 Nuthatch St","San Antonio"],[" 9706 Nueces Cyn","San Antonio"],[" 200 White Trl","Cibolo"],[" 238 Perch Mnr","San Antonio"],[" 3239 Coral Grove Dr","San Antonio"],[" 45 Oak Bnd","New Braunfels"],[" 6945 Hallie Hts","Schertz"],[" 649 Silo St","Schertz"],[" 943 Lee Trevino","San Antonio"],[" 2516 Cedar Ln","Schertz"],[" 7114 Comet Mnr","San Antonio"],[" 27018 Picolo Pl","San Antonio"],[" 7827 Caballo Cyn","San Antonio"],[" 2718 Night Star","San Antonio"],[" 6644 Sally Agee","San Antonio"],[" 15826 Cotton Tail Ln","San Antonio"],[" 9814 Dawn Trl","San Antonio"],[" 1913 Guildford Dr","La Vergne"],[" 135 White Cloud Trl","Murfreesboro"],[" 2137 Erin Ln","Mount Juliet"],[" 5523 Middlebury Dr","Murfreesboro"],[" 315 Augusta Ave","Pleasant View"],[" 5705 Briarwick Ct","Hermitage"],[" 2051 Roderick Cir","Franklin"],[" 2236 Arbor Pointe Way","Hermitage"],[" 2340 Alteras Dr","Nashville"],[" 6624 Scenic Dr","Murfreesboro"],[" 3431 Ravenel Ct","Murfreesboro"],[" 883 Loretta Dr","Goodlettsville"],[" 3405 Old Anderson Rd Unit 111","Antioch"],[" 526 Avondale Park Blvd","Nashville"],[" 5747 Roxbury Dr","Murfreesboro"],[" 1207 Jepson Ct","Franklin"],[" 127 Ridgeview Trce","Hendersonville"],[" 4309 Garcia Blvd","Murfreesboro"],[" 543 Great Angelica Way","Nolensville"],[" 6425 Paddington Way","Antioch"],[" 2121 Burns St","Nashville"],[" 534 Millwood Ln","Mount Juliet"],[" 3108 Celt Aly","Nolensville"],[" 200 Oceola Ave # A","Nashville"],[" 621 Harding Pl","Nashville"] ]


browser = webdriver.Firefox()

browser.maximize_window()

property_data_headers = ['Property_address','Date','Event','Price','Price/Sq Ft','Source','State','City','Pin','Website']
property_data = []


count = 0

for i in Address[1553:]:
    # try:
        browser.get('https://www.realtor.com/')
        time.sleep(3)
        print(i[0])
        try:
            browser.find_element_by_xpath('/html/body/div[9]/div/div[1]/a').click()
        except:pass
        #Address
        browser.find_element_by_xpath('//*[@id="searchBox"]').clear()
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="searchBox"]').send_keys(i[0])
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="searchBox"]').send_keys(Keys.RETURN)
        time.sleep(8)
        try:
            browser.find_element_by_xpath('/html/body/div[9]/div/div[1]/a').click()
        except:
            pass
        jsoup = BeautifulSoup(browser.page_source)



        if 'No price history available for this property.'.lower() in browser.page_source.lower():
            print('#############')
            address = jsoup.find('div', attrs={'class': 'ldp-header-address-wrapper'}).find('h1').find_all('span')[0] if jsoup is not None else None
            print(address.text)
            city = jsoup.find('div', attrs={'class': 'ldp-header-address-wrapper'}).find('h1').find_all('span')[1] if jsoup is not None else None
            print(city.text)
            state = jsoup.find('div', attrs={'class': 'ldp-header-address-wrapper'}).find('h1').find_all('span')[2] if jsoup is not None else None
            print(state.text)
            pin = jsoup.find('div', attrs={'class': 'ldp-header-address-wrapper'}).find('h1').find_all('span')[3] if jsoup is not None else None
            print(pin.text)

            data = [address.text, None, None, None, None, None, state.text, city.text,pin.text, 'Realtor']
            property_data.append(data)
        elif "We didn't find matching results for your search.".lower() in browser.page_source.lower():
            print('++++++++++++++')
            data = [i[0], None, None, None, None, None, None, i[1], None, 'Realtor']
            property_data.append(data)
        elif "ldp-header-address-wrapper".lower() not in browser.page_source.lower():
            print('______________')
            data = [i[0], None, None, None, None, None, None, i[1], None, 'Realtor']
            property_data.append(data)
        elif 'listing-subsection listing-subsection-price'.lower() not in browser.page_source.lower():
            address = jsoup.find('div', attrs={'class': 'ldp-header-address-wrapper'}).find('h1').find('span', attrs={'itemprop': 'streetAddress'}) if jsoup is not None else None
            address = address.text if address is not None else None
            print(address)
            city = jsoup.find('div', attrs={'class': 'ldp-header-address-wrapper'}).find('h1').find('span', attrs={'itemprop': 'addressLocality'}) if jsoup is not None else None
            city = city.text if city is not None else None
            print(city)
            state = jsoup.find('div', attrs={'class': 'ldp-header-address-wrapper'}).find('h1').find('span', attrs={'itemprop': 'addressRegion'}) if jsoup is not None else None
            state = state.text if state is not None else None
            print(state)
            pin = jsoup.find('div', attrs={'class': 'ldp-header-address-wrapper'}).find('h1').find('span', attrs={'itemprop': 'postalCode'}) if jsoup is not None else None
            pin = pin.text if pin is not None else None
            print(pin)
            data = [address, None, None, None, None, None, state, city, pin, 'Realtor']
            property_data.append(data)
        else:
            print('----------------')
            address = jsoup.find('div', attrs={'class': 'ldp-header-address-wrapper'}).find('h1').find('span',attrs={'itemprop':'streetAddress'})if jsoup is not None else None
            address = address.text if address is not None else None
            print(address)
            city = jsoup.find('div', attrs={'class': 'ldp-header-address-wrapper'}).find('h1').find('span',attrs={'itemprop':'addressLocality'}) if jsoup is not None else None
            city = city.text if city is not None else None
            print(city)
            state = jsoup.find('div', attrs={'class': 'ldp-header-address-wrapper'}).find('h1').find('span',attrs={'itemprop':'addressRegion'}) if jsoup is not None else None
            state = state.text if state is not None else None
            print(state)
            pin = jsoup.find('div', attrs={'class': 'ldp-header-address-wrapper'}).find('h1').find('span',attrs={'itemprop':'postalCode'}) if jsoup is not None else None
            pin = pin.text if pin is not None else None
            print(pin)
            table = jsoup.find('div',attrs={'class':'listing-subsection listing-subsection-price'}).find('table').find('tbody') if jsoup is not None else None
            # print(table)

            for trs in table.find_all('tr') if table is not None else None:

                date = trs.find_all('td')[0] if trs is not None else None
                print(date.text)
                event = trs.find_all('td')[1]if trs is not None else None
                print(event.text)
                price = trs.find_all('td')[2]if trs is not None else None
                print(price.text)
                per_sq_ft = trs.find_all('td')[3]if trs is not None else None
                print(per_sq_ft.text)
                source = trs.find_all('td')[4]if trs is not None else None
                print(source.text)
                data = [address if address is not None else i[0], date.text, event.text, price.text,per_sq_ft.text,source.text, state, city,pin, 'Realtor']
                property_data.append(data)



    # except Exception as e:
    #     print(e)

browser.close()


print(tabulate(property_data))
df = pd.DataFrame(property_data,columns=property_data_headers)
print(df)
# print(Address_not_found)
df.to_excel("Test_Realtor_"+str(today.strftime('%Y_%m_%d'))+'.xlsx',index=False)
print('Time = ', (time.time()-startTime)/60)