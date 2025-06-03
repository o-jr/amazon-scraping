##OVERVIEW

This project implements a web scraping pipeline to collect product data from Amazon Brazil, specifically for men's eyewear products. The pipeline includes data collection, validation, storage, and visualization components.

The project's architecture is modular and follows a standard ETL pattern, with monitoring integrated for reliability. It's built using Python-based tools, making it lightweight and easy to maintain.

![Untitled-2025-06-03-1108](https://github.com/user-attachments/assets/e7dd7951-09ef-4c70-bc90-514f378dad89)


This project uses Scrapy for scraping, Spidermon for validation, DuckDB for storage, and Streamlit for visualization. This setup is perfect for tackling the challenges above, as Spidermon provides powerful monitoring, validation out of the box and generates a report file after monitoring.

Spidermon is a Scrapy extension that monitors your spider's behavior in real time, both during operations and at the end of runs, to enforce rules based on statistics, errors, and custom thresholds.

Taking on this web scraping job has reinforced how critical validation is—it's the difference between a quick script and a reliable system. If you're working on similar projects, I highly recommend integrating Spidermon—it's a game-changer for maintaining data quality and operational efficiency.

### Step-by-Step Workflow
Here's how the project operates from start to finish:

1. **Data Scraping (via Scrapy)**:
   - The process begins with Scrapy, a Python framework for web crawling. The spider sends HTTP requests to Amazon's website, parses the HTML responses, and extracts product details (e.g., brand, price, rating, and title).
   - It handles pagination to crawl multiple pages (up to 8 in your code) and includes anti-blocking measures like rotating User-Agents and request delays.
   - Scraped data is yielded as items, which are then passed to Scrapy's pipeline for validation.

2. **Data Validation and Monitoring (via Spidermon)**:
   - As items are scraped, Spidermon kicks in to monitor and validate the process. It checks for things like the number of items scraped (e.g., at least 200), response status codes (e.g., no 503 errors), and execution time (e.g., under 2 minutes).
   - Validation also includes schema checks (e.g., ensuring each item has required fields like 'brand' and 'price').
   - If any thresholds are breached (e.g., fewer than 200 items), Spidermon flags it and can generate html reports. This ensures data quality and reliability before proceeding.
   ![Spidermon Report Passed](https://github.com/user-attachments/assets/6c0043df-8d91-49df-aa87-971b90ff90f7)

  
     

3. **Data Processing and Storage (via duckdb.py)**:
   - Once validated, the scraped data is exported as JSON (by Scrapy) and processed in a separate script (duckdb.py).
   - The script loads the JSON, cleans the data (e.g., removing null values, converting data types), adds metadata (e.g., source and timestamp), and inserts it into a DuckDB database. DuckDB is an in-memory analytics database that's fast and efficient for small-to-medium datasets.

4. **Data Visualization and Analysis (via Streamlit)**:
   - Finally, the data in DuckDB is queried and displayed in a Streamlit app. This creates an interactive BI dashboard where users can view metrics (e.g., total products, average price), filter data (e.g., by price range), and explore charts and tables.
   - The dashboard provides real-time insights, making it easy to analyze the scraped data without advanced tools.

In essence, the project transforms raw web data into actionable insights while incorporating checks to meet specific requirements (e.g., 200 products, no 503 errors, and quick execution).


### Key Components and Interactions
- **Scrapy Spider (amazon.py)**:
  - Core: Defines the spider that crawls Amazon.
  - Interactions: Yields items to Scrapy's pipeline, which triggers Spidermon for monitoring.
  - Dependencies: Relies on settings.py for configurations like delays and headers.

- **Spidermon (monitors.py and settings.py)**:
  - Core: Custom monitors (e.g., ItemCountMonitor, StatusErrorMonitor) run during and after scraping.
  - Interactions: Integrates with Scrapy to access stats (e.g., response counts, execution time). If validations fail, it can halt the process or generate reports.
  - Key Settings: In settings.py, thresholds like CUSTOM_MIN_ITEMS_SCRAPED = 350 and SPIDERMON_MAX_EXECUTION_TIME = 100 ensure compliance with your job's requirements.

- **Data Processing Script (duckduck.py)**:
  - Core: Handles data cleaning and storage.
  - Interactions: Reads output from Scrapy (e.g., a JSON file), processes it into a Pandas DataFrame, and inserts it into DuckDB.
  - Schema: The DuckDB table (ml_items) includes columns like brand, price, rating, and metadata for easy querying.

- **Streamlit Dashboard (app.py)**:
  - Core: Queries DuckDB and renders visualizations.
  - Interactions: Uses cached data queries for performance, allowing users to filter and analyze data dynamically.
  - User Interface: Features tabs, sliders, and charts for interactive BI.
 
    ![streamlit dashboard](https://github.com/user-attachments/assets/6b234c0a-c090-4398-8f0c-e49bf9fb5b2f)


### Data Flow Details
- **Flow Path**: Data starts as HTML responses from Amazon, gets extracted into dictionaries by Scrapy, validated by Spidermon, transformed in duckdb.py, stored in DuckDB, and finally visualized in Streamlit.
- **Error Handling**: Scrapy retries HTTP errors (e.g., 503), Spidermon monitors for breaches, and scripts in duckdb.py use try-except blocks for robustness.
- **Scalability**: The architecture is designed for small-scale use but can scale by adding features like scheduled runs (e.g., via cron jobs) or distributed Scrapy setups.
- **Security and Compliance**: User-Agents are rotated to avoid blocks, and robots.txt is set to False (as per settings.py), but always ensure you're complying with the target site's terms.

This architecture keeps components decoupled, making it easy to update or replace parts (e.g., switch from DuckDB to another database).

+-----------------------------------+
|  External Source:                 |
|  Amazon Website                   |
+-----------------------------------+
               |
               | (HTTP Requests)
               v
+-----------------------------------+
|  Scrapy Spider (amazon.py) .JSON |
|  - Crawls and extracts data      |
|  - Yields items for processing   |
+-----------------------------------+
               |     ^
               |     | (Real-time monitoring)
               v     |
+-----------------------------------+     +-----------------------------------+
|  Spidermon Monitors (monitors.py) |     |  Data Pipeline (duckdb.py)      |
|  - Validates item count           |     |  - Cleans and processes data    |
|  - Checks for errors and time     |     |  - Stores in DuckDB             |
|  - Generates reports              |     +-----------------------------------+
+-----------------------------------+              |
               |                                   v
               +-----------------------------------+
               |                                   |
               v                                   v
+-----------------------------------+     +-----------------------------------+
|  DuckDB Database                  |     |  Streamlit Dashboard (app.py)    |
|  - Stores structured data         |     |  - Queries and visualizes data   |
|  - Supports querying              |     |  - Interactive BI interface      |
+-----------------------------------+     +-----------------------------------+

# How to Run This Project

Running the project is straightforward if you have the necessary tools installed. It assumes you're on a system with Python (version 3.8+). Below are step-by-step instructions, including prerequisites and troubleshooting tips.

### Prerequisites
- **Software Requirements**:
  - Python 3.8 or higher.
  - Pip (Python package manager).
  - Key Libraries: Install via pip with `pip install scrapy spidermon duckdb streamlit pandas`.
  - Other Tools: A code editor (e.g., VS Code) and Git for version control.
- **Environment Setup**:
  - Clone the project repository (if it's in a Git repo) or ensure all files (amazon.py, settings.py, monitors.py, duckdb.py, app.py) are in a single directory.
  - Hardcoded paths (e.g., in settings.py and duckdb.py) point to your local machine (e.g., "C:/Users/W4rne4/..."). Update these for your setup.
- **Amazon-Specific Notes**: Be mindful of Amazon's scraping policies. This is for educational purposes; use responsibly.

### Step-by-Step Instructions
1. **Set Up the Environment**:
   - Create a virtual environment to isolate dependencies:
     ```
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install required packages:
     ```
     pip install scrapy spidermon duckdb streamlit pandas
     ```

2. **Run the Scraping Process**:
   - Navigate to your project directory.
   - Start the Scrapy spider:
     ```
     scrapy crawl amazon -o data/data5.json  # This crawls the site and saves output to JSON
     ```
     - Explanation: The `-o` flag exports the scraped data to a JSON file (as specified in your code). This will trigger Spidermon monitors automatically due to settings.py.
     - Expected Output: The spider will log progress, and Spidermon will generate reports if validations pass or fail (e.g., check for amzn_report3.html).

3. **Process and Store the Data**:
   - Run the data processing script:
     ```
     python duckdb.py
     ```
     - Explanation: This loads the JSON from the scraping step, cleans it, and inserts it into the DuckDB database (e.g., at "C:/Users/W4rne4/git/ml-scraping/data/duckdb2.duckdb"). Check the logs for success messages.

4. **Launch the Dashboard**:
   - Start the Streamlit app:
     ```
     streamlit run app.py
     ```
     - Explanation: This opens a web browser with the interactive dashboard. You can now view and analyze the data.
     - Access: The app runs on http://localhost:8501 by default.

5. **Verify and Debug**:
   - Check Spidermon Reports: After scraping, look for files like "amzn_report3.html" in your project directory to review validations (e.g., if 200+ items were scraped).
   - Monitor Logs: Scrapy and duckdb.py use logging—check the console for errors.
   - Test End-to-End: Run the full pipeline and verify the dashboard shows expected data (e.g., around 200 products).

### Troubleshooting Tips
- **Common Errors**:
  - 503 Errors: If they occur, Scrapy will retry, but check your internet connection or add more delays in settings.py.
  - Validation Failures: If Spidermon reports issues (e.g., fewer items), debug the spider in amazon.py.
  - Path Issues: If files aren't found, update hardcoded paths in settings.py and duckdb.py to match your system.
  - Dependencies: If a library is missing, run `pip install -r requirements.txt` (create a requirements.txt file first with `pip freeze > requirements.txt`).
- **Performance Tuning**: If scraping takes over 2 minutes, adjust AUTOTHROTTLE settings in settings.py or reduce max_pages in amazon.py.
- **Best Practices**: Run in a virtual environment, use version control, and test on a small scale first.

This project is self-contained and can be run on a local machine. Once set up, you can automate it with scripts or schedulers for regular updates. If you encounter any issues or need customizations, let me know—I'm here to help!

