from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'static/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = 'https://covidtracking.com/data'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')
    #print(soup.prettify())

    covid_data = []
    my_xpath = '/html/body/div/div[1]/main/div[2]/div/div[8]/div[1]/div'
    state_divs = browser.find_by_xpath(my_xpath)

    state_soup = bs(state_divs.html, 'html.parser')

    #print(state_soup)

    for state in range(len(state_soup)):
        
        state_total_cases_xpath = f'/html/body/div/div[1]/main/div[2]/div/div[8]/div[1]/div/div[{state + 1}]/div[2]/div[1]/div[2]/div/div/div[2]'
        state_new_cases_xpath = f'/html/body/div/div[1]/main/div[2]/div/div[8]/div[1]/div/div[{state + 1}]/div[2]/div[1]/div[2]/div/div/div[3]/div[1]/span[2]'
        
        state_name_xpath = f'/html/body/div/div[1]/main/div[2]/div/div[8]/div[1]/div/div[{state + 1}]/div[1]/h3/a'
        
        state_name = browser.find_by_xpath(state_name_xpath).text
        state_total_cases = browser.find_by_xpath(state_total_cases_xpath).text
        state_new_cases = browser.find_by_xpath(state_new_cases_xpath).text
        
        state_data = {
            'name' : state_name,
            'total_cases' : state_total_cases,
            'new_cases' : state_new_cases
                     }
        
        print(state_data)
        covid_data.append(state_data)

    browser.quit()

    return covid_data

#covid_data = scrape_info()

#print(covid_data)