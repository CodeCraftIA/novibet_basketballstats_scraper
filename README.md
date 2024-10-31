### 🏀 **Novibet Basketball Stats Scraper**  
📋 **Overview**  

This project scrapes and organizes player statistics from basketball games on the Novibet website, capturing betting lines and odds for various player categories like points, rebounds, assists, and more. The collected data is saved in a structured Excel file.

Using **Selenium**, the script navigates to the Novibet page, closes any pop-ups, and scrapes the data for each filter category. **Pandas** is used to organize and export the final data to Excel.

<br />

### 🛠️ **Technologies Used**  

- **Python**  
- **Selenium** (for web scraping and browser automation)  
- **Pandas** (for data handling and exporting)  
- **TQDM** (for progress tracking)  

<br />  

### 🚀 **Project Workflow**  

- **Page Navigation & Popup Management**: The script opens a specified Novibet URL, manages any pop-ups that appear, and begins the scraping process.
- **Data Extraction**: For each player filter category (points, rebounds, assists, etc.), the script scrapes player names, betting lines, and corresponding odds for "over" and "under" bets.
- **Data Export**: Once collected, the data is organized into a DataFrame and saved as an Excel file, `Player_Bet_Data.xlsx`.

<br />  

### ⚙️ **How to Run**  

- **Clone the Repository**:  

   ```bash
   git clone https://github.com/your_username/novibet_basketballstats_scraper
   cd novibet_basketballstats_scraper
   
- **Install Requirements**:

   pip install -r requirements.txt  

- **Run the Script**:

   python novibet_scraper.py  
  

<br/>  



### 📝 **Details**  
- **Filters & Categories**: The script iterates through specific betting filters like points, rebounds, assists, and more, extracting each player’s betting odds.  
  

- **Error Handling**: Popup windows or registration prompts are managed automatically, ensuring uninterrupted scraping.
  

- **Excel Export**: Data is saved as Player_Bet_Data.xlsx for easy analysis or further processing.  
  

<br/>  
