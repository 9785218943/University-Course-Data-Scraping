import requests
from bs4 import BeautifulSoup
import pandas as pd
import uuid

# 1. Target Universities ki List
seeds = [
    {"name": "University of Oxford", "url": "https://www.ox.ac.uk/admissions/undergraduate/courses/course-listing", "country": "UK", "city": "Oxford"},
    {"name": "University of Toronto", "url": "https://www.utoronto.ca/academics/programs-directory", "country": "Canada", "city": "Toronto"},
    {"name": "National University of Singapore", "url": "https://www.nus.edu.sg/registrar/prospective-students/undergraduate/programmes", "country": "Singapore", "city": "Singapore"},
    {"name": "University of Melbourne", "url": "https://study.unimelb.edu.au/find-a-course", "country": "Australia", "city": "Melbourne"},
    {"name": "ETH Zurich", "url": "https://ethz.ch/en/studies/bachelor/degree-programmes.html", "country": "Switzerland", "city": "Zurich"}
]

uni_data = []
course_data = []

def get_headers():
    return {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def scrape_universities():
    print("Scraping started... Please wait.")
    
    for seed in seeds:
        # Unique ID generate karna (Relational Integrity ke liye)
        u_id = f"UNI-{uuid.uuid4().hex[:5].upper()}"
        
        # University Sheet ka data
        uni_data.append({
            "university_id": u_id,
            "university_name": seed['name'],
            "country": seed['country'],
            "city": seed['city'],
            "website": seed['url']
        })
        
        # Course Scraping Logic
        try:
            response = requests.get(seed['url'], headers=get_headers(), timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Website se course names nikalna (Example: links ya headings)
            # Note: Real scenario mein har site ka tag alag hota hai, yahan hum generalized approach le rahe hain
            links = soup.find_all(['a', 'h3'], limit=30) 
            
            count = 0
            for link in links:
                course_name = link.get_text(strip=True)
                
                # Filter: Sirf wo text jo 10 characters se bada ho (taaki garbage na aaye)
                if len(course_name) > 10 and count < 6:
                    course_data.append({
                        "course_id": f"CRS-{uuid.uuid4().hex[:5].upper()}",
                        "university_id": u_id, # Foreign Key
                        "course_name": course_name,
                        "level": "Bachelor's / Master's",
                        "discipline": "General Science/Arts",
                        "duration": "3-4 Years",
                        "fees": "Check Official Site",
                        "eligibility": "High School / Graduate"
                    })
                    count += 1
            print(f"Done: {seed['name']}")
            
        except Exception as e:
            print(f"Error scraping {seed['name']}: {e}")

    # 2. Excel File Mein Save Karna
    with pd.ExcelWriter("University_Assignment.xlsx", engine='openpyxl') as writer:
        df_uni = pd.DataFrame(uni_data)
        df_course = pd.DataFrame(course_data)
        
        df_uni.to_excel(writer, sheet_name="Universities", index=False)
        df_course.to_excel(writer, sheet_name="Courses", index=False)

    print("\nSuccess! 'University_Assignment.xlsx' file create ho gayi hai.")

if __name__ == "__main__":
    scrape_universities()