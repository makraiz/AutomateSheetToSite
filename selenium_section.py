from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

mileage_url = "https://app.informedk12.com/link_campaigns/morgan-hill-travel-reimbursement-claim-electronic-form?token=fgtwSdEWCn8npWkHbYDbjfQH"


def entrypoint(user_info, list_of_rows):
    """
    Script's entry point, sets up selenium webdriver, calls functions
    """
    options = Options()
    options.add_experimental_option("detach", True)
    main_driver = webdriver.Chrome(options=options)

    main_driver.get(mileage_url)

    fill_name(main_driver, user_info)
    fill_sheet(main_driver, list_of_rows)


def fill_name(driver, user_info):
    """
    Waits for about 4 seconds for webpage elements to load
    Locates elements and enters name and email
    """
    driver.implicitly_wait(4)
    driver.find_element(By.ID, "recipient_name").send_keys(user_info['name'])
    driver.find_element(By.ID, "recipient_email").send_keys(user_info['email'])
    driver.implicitly_wait(8)
    if driver.find_element(By.CLASS_NAME, "_pendo-close-guide"):
        check_for_notice(driver)
    driver.find_element(By.NAME, "button").click()

    return


def fill_sheet(driver, data):
    """
    Locates first element of sheet's body, populates sheet
    """
    # Locate first element, parses for first date field, which should be first cell in form, get attribute to get correct id
    driver.implicitly_wait(4)
    first_element = driver.find_element(By.CSS_SELECTOR, "[data-field-type='DateField']")
    current_id = int(first_element.get_attribute("data-field-id"))
    # these are the form input types corresponding to each column of the form, here to help specify xpath
    types = ["input", "textarea", "textarea", "select", "textarea", "textarea"]
    for row in data:
        for i, value in enumerate(row):
            xpath = f"//{types[i]}[@data-field-id={current_id}]"
            driver.find_element(By.XPATH, xpath).send_keys(value)
            current_id += 1
    return

def check_for_notice(driver):
    """
    Resolves edge case where there is a pop-up obstructing the program from proceeding
    """
    check_input = driver.find_element(By.CLASS_NAME, "_pendo-close-guide")
    check_input.click()