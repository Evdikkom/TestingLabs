from selenium.webdriver.common.by import By
from base_page import BasePage

class ContactPage(BasePage):
    # Локаторы элементов формы
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "email")
    PHONE_INPUT = (By.ID, "phone")
    ADDRESS_INPUT = (By.ID, "address")
    COMMENT_INPUT = (By.ID, "comment")
    SUBMIT_BUTTON = (By.ID, "submit-btn")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    FIELD_ERROR = (By.CLASS_NAME, "field-error")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
    
    def open(self, url):
        self.driver.get(url)
    
    def set_name(self, name):
        self.find_clickable_element(self.NAME_INPUT).clear()
        self.find_clickable_element(self.NAME_INPUT).send_keys(name)
    
    def set_email(self, email):
        self.find_clickable_element(self.EMAIL_INPUT).clear()
        self.find_clickable_element(self.EMAIL_INPUT).send_keys(email)
    
    def set_phone(self, phone):
        self.find_clickable_element(self.PHONE_INPUT).clear()
        self.find_clickable_element(self.PHONE_INPUT).send_keys(phone)
    
    def set_address(self, address):
        self.find_clickable_element(self.ADDRESS_INPUT).clear()
        self.find_clickable_element(self.ADDRESS_INPUT).send_keys(address)
    
    def set_comment(self, comment):
        self.find_clickable_element(self.COMMENT_INPUT).clear()
        self.find_clickable_element(self.COMMENT_INPUT).send_keys(comment)
    
    def submit_form(self):
        self.find_clickable_element(self.SUBMIT_BUTTON).click()
    
    def get_success_message(self):
        return self.get_element_text(self.SUCCESS_MESSAGE)
    
    def get_error_message(self):
        return self.get_element_text(self.ERROR_MESSAGE)
    
    def get_field_error(self, field_name):
        return self.get_element_text((By.ID, f"{field_name}-error"))
    
    def is_success_message_displayed(self):
        return self.is_element_visible(self.SUCCESS_MESSAGE)
    
    def is_error_message_displayed(self):
        return self.is_element_visible(self.ERROR_MESSAGE)