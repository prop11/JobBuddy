import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class IndeedAutoApplyBot:
    def __init__(self):
        # Initialize the browser 
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        
    def login(self, email, password):
        """Login to Indeed account"""
        self.driver.get("https://www.indeed.com/account/login")
        
        try:
            # Enter email
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "login-email-input")))
            email_field.send_keys(email)
            
            # Enter password
            password_field = self.wait.until(EC.presence_of_element_located((By.ID, "login-password-input")))
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.wait.until(EC.element_to_be_clickable((By.ID, "login-submit-button")))
            login_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            return True
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
    
    def search_jobs(self, keywords, location):
        """Search for jobs based on keywords and location"""
        self.driver.get("https://www.indeed.com")
        
        try:
            # Enter job keywords
            keyword_field = self.wait.until(EC.presence_of_element_located((By.ID, "text-input-what")))
            keyword_field.clear()
            keyword_field.send_keys(keywords)
            
            # Enter location
            location_field = self.wait.until(EC.presence_of_element_located((By.ID, "text-input-where")))
            location_field.clear()
            location_field.send_keys(location)
            location_field.send_keys(Keys.RETURN)
            
            # Wait for search results
            time.sleep(3)
            return True
        except Exception as e:
            print(f"Job search failed: {str(e)}")
            return False
    
    def apply_for_jobs(self, max_applications=5):
        """Apply for jobs in the search results"""
        applications_sent = 0
        
        while applications_sent < max_applications:
            try:
                # Get all job listings on the page
                job_listings = self.wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job_seen_beacon"))
                )
                
                for job in job_listings:
                    if applications_sent >= max_applications:
                        break
                    
                    try:
                        # Click on the job title to open the listing
                        title_element = job.find_element(By.CSS_SELECTOR, ".jobTitle a")
                        title_element.click()
                        time.sleep(2)
                        
                        # Switch to the job details iframe if needed
                        try:
                            iframe = self.wait.until(EC.presence_of_element_located((By.ID, "vjs-container-iframe")))
                            self.driver.switch_to.frame(iframe)
                            in_iframe = True
                        except:
                            in_iframe = False
                        
                        # Try to find and click the apply button
                        try:
                            apply_button = self.wait.until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, ".indeed-apply-button"))
                            )
                            apply_button.click()
                            time.sleep(3)
                            
                            # Handle the application form (simplified example)
                            self.handle_application_form()
                            
                            applications_sent += 1
                            print(f"Applications sent: {applications_sent}/{max_applications}")
                            
                        except NoSuchElementException:
                            print("No apply button found for this job, skipping...")
                        
                        # Switch back to main content if we were in an iframe
                        if in_iframe:
                            self.driver.switch_to.default_content()
                            
                    except Exception as e:
                        print(f"Error processing job: {str(e)}")
                        continue
                
                # Go to next page if we haven't reached max applications
                if applications_sent < max_applications:
                    try:
                        next_button = self.wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='pagination-page-next']"))
                        )
                        next_button.click()
                        time.sleep(3)
                    except:
                        print("No more pages available")
                        break
                        
            except Exception as e:
                print(f"Error in job application loop: {str(e)}")
                break
                
        return applications_sent
    
    def handle_application_form(self):
        """Simplified example of handling an application form"""
        try:
            # Wait for form to load
            time.sleep(2)
            
            # Fill out name if field exists
            try:
                name_field = self.driver.find_element(By.NAME, "name")
                name_field.send_keys("Your Name")
            except:
                pass
                
            # Fill out email if field exists
            try:
                email_field = self.driver.find_element(By.NAME, "email")
                email_field.send_keys("your.email@example.com")
            except:
                pass
                
            # Upload resume if field exists
            try:
                resume_field = self.driver.find_element(By.NAME, "resume")
                resume_field.send_keys("/path/to/your/resume.pdf")
            except:
                pass
                
            # Submit the application
            try:
                submit_button = self.driver.find_element(By.CSS_SELECTOR, ".ia-Form-footer button")
                submit_button.click()
                time.sleep(3)
            except:
                pass
                
        except Exception as e:
            print(f"Error handling application form: {str(e)}")
    
    def close(self):
        """Close the browser"""
        self.driver.quit()

# Example usage
if __name__ == "__main__":
    bot = IndeedAutoApplyBot()
    
    try:
        # Login
        if bot.login("your_email@example.com", "your_password"):
            # Search for jobs
            if bot.search_jobs("Software Engineer", "New York, NY"):
                # Apply for jobs (limit to 3 for example)
                applications_sent = bot.apply_for_jobs(max_applications=3)
                print(f"Successfully sent {applications_sent} applications")
    finally:
        bot.close()
