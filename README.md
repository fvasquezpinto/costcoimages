# costcoimages

This project consists of a scraper for gathering specific product images from the CostoJP website.
To define the products that will be processed, you have to edit the `costco_images_input_skus.csv` file as stated in the point Nº6 of the below instructions.

0. Install Python in your machine
1. Download this repository:
- In a Terminal window, go to the folder where you want to save the project.
For example: to save it in Desktop, execute the commands
- cd
- cd Desktop
Then, type `git clone git@github.com:fvasquezpinto/costcoimages.git`.
2. In the terminal, navigate to the project's folder.
For example, use the command `cd Desktop/costoimages` if you downloaded the project into the Desktop.
3. Create a virtual environment using the command
`python3 -m venv venv` (MacOS)
`python -m venv venv` (Windows)
Then, activate the virtual environment using the command
`source venv/bin/activate` (MacOS)
`venv\Scripts\activate` (Windows)
In case of doubts with the virtual environment you can find more information about it in:
https://realpython.com/python-virtual-environments-a-primer/
4. (In the same Terminal used to activate the virtual environment) Install scrapy using the command
`python -m pip install scrapy` (MacOS)
`python -m pip install scrapy` (Windows)
5. In the terminal, navigate to the `costoimages` folder inside the project's folder. For example, use the command `cd Desktop/costoimages/costoimages` if you downloaded the project into the Desktop.
6. Make sure you updated the `costco_images_input_skus.csv` file with the SKUs of the items you want to get. Such file is located inside `spiders`folder (Desktop/costcoimages/costoimages/spiders).
7. Execute the command `scrapy crawl CostcoJPbySKU --loglevel INFO` and the scraper will start working. Wait until it ends (will say so in the terminal) or finish whenever you want it using `cmd + c` (MacOS) `ctrl + d` or `ctrl + c` (Windows) keyboard keys at the same time.
8. Find the results in the `output` folder that is inside `spiders` folder (Desktop/costcoimages/costoimages/spiders/output).
