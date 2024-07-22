# Job Insights - Job Scraper & Data Analysis

This is a customizable web scraper for full-time jobs on JobsDB.com HK with in-depth analysis and visualization of current market data to uncover insights that can help job seekers and employers better understand employment trends.

This project is split into two parts: the **Job Scraper** and the **Data Analysis** using the data scraped from the first part.

# Part I - Job Scraper

The program in this part scrapes for full-time jobs that are found under a particular keyword on JobsDB.com HK and stores the scraped data in a csv.

## How to Use

### Setting up the Environment

1.  Clone the respository to your local machine. One way to do it is to pick a location on your local machine where you want the respository to clone to (e.g., the desktop) and type `git clone https://github.com/heiinhei911/job-insights.git` into the terminal
2.  Change your current directory `cd` to the location of the cloned respository on your local machine (e.g., `cd Desktop/job-insights`)
3.  _(Optional)_ Create a virtual environment for the cloned respository (e.g., venv, conda)
4.  _(Under the virtual env. if you have created one in step 3)_ Type `pip install -r requirements.txt`. This will install all the necessary packages and modules so that the program can run properly

### Using the Program

1.  Run the program by running `python job-scraper.py` in the terminal
2.  Enter the keyword that you would like to search for (e.g., business analyst)

    ![Job Title Input](./images/job_title_input.png)

3.  Enter the number of pages that you would like to search for
    (you can either type in a number for searching a set number of pages OR type in 'all' for searching all pages)

    ![Number Of Pages Being Searched Input](./images/number_of_jobs_being_searched.png)

4.  Now we wait!

    _(This step could take quite a while depending on a number of factors such as the number of job postings you are scraping, your internet speed, the specification of your machine, etc.)_

5.  Once all the pages have finished processing, all the data will be saved in _\[the keyword you have inputted in step 2\].csv_ under the `jobs/` directory

    ![Scraping Completed](./images/scraping_completed.png)

# Part II - Data Analysis

This part involves data cleaning, exploratory data analysis, and some feature extractions using the data that was scraped from Part I.

All the details about the part can be found in `analysis.ipynb`.

All the data that have been "processed" are stored under `transformed/` the directory.

A dashboard with visualization of the analysis can be found [here](https://public.tableau.com/app/profile/hei.in.sam/viz/JobMarketInsightsAnalysesontheRoleofBusinessAnalystinHongKong/JobDataAnalyses).

# Libraries/Frameworks Used

Part I - Job Scraper: Python, Beautiful Soup, Selenium, Pandas

Part II - Data Analysis: Python, Jupyter Notebook, Pandas, Numpy, Matplotlib, Seaborn

# Credits

This project and its data are intended for educational purposes only.

All data come from JobsDB.com HK. All rights reserved to JobsDB.com HK.
