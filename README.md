<!-- ABOUT THE PROJECT -->
## About The Project

This is an automated and reusable framework which crawls and downloads F-Droid open source application and looks for test libraries in them. 
The results of analysis contains several outputs as below:
* For each open-source app:
	 * Release date
	 * App has Junit or not
	 * App has Espresso or not
	 * App has Robolectric or not
	 * Number of Junit test cases
	 * Number of Espresso test cases
	 * Number of Robolectric test cases
	 * Number of code lines
	 * Number of test lines

* For each F-Droid category:
	* Number of all downloaded projects
	* Number of projects that have at least on test libraries
	* Number of projects that have Junit
	* Number of projects that have Espresso
	* Number of projects that have Robolectric
	* Number of projects that have only Junit
	* Number of projects that have only Espresso
	* Number of projects that have only Robolectric
	* Number of projects that have Junit and Espresso
	* Number of projects that have Junit and Robolectric
	* Number of projects that have Espresso and Robolectric
	* Total number of Junit test cases
	* Total number of Espresso test cases
	* Total number of Robolectric test cases

In addition, for each category, one plot is stored which has 3 graphs. In this plot, number of Junit, Espresso and Robolectric test cases are indicated per each year.


### Built With
All the project is coded by Python3. We use [Scrapy](https://docs.scrapy.org/en/latest/) for crawling F-Droid category pages. Also all Python scripts are in a shell script.

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
We use Scrapy and Cloc for crawling and counting lines of code in order.

* Scrapy
```sh
pip install scrapy
```

* Cloc
```
apt install cloc
```

### Installation and run

1. Clone the repo
```sh
git clone https://github.com/ahatashkar/FDroidCrawler.git
```
3. Install the requirments
```sh
pip install -r requirements.txt
```
4. Run script.sh and enter F-Droid category link as argument
```JS
./script.sh [link]
```

### Outputs
After crawling the category page, all apps that hosts on Github are downloaded as zip file in "Project" directory. Then all zip files are extracted in "Unzip" directory. After that, all projects are analysed and searched for testing tools. 
The results.csv and plot are stored in "Output" directory.

<!-- CONTACT -->
## Contact
Please feel free to contact me.

Email: ahatashkar@gmail.com

