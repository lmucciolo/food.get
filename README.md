*This README.md file was generated on 03-02-24 by Livia Mucciolo*
# food.get
Examining food access in Chicago post-pandemic.

## Authors
- [Austin Steinhart](https://github.com/Asteinhart)
- [Danielle Rosenthal](https://github.com/RosenthalDL)
- [Livia Mucciolo](https://github.com/lmucciolo)
- [Stacy George](https://github.com/stacy-george) 

## Introduction
The project aims to analyze food access and security within the Chicago area. The scope of this work provides an updated food access metric for 2022 to understand communities’ post-pandemic food access and shows how food access has changed in the city over time.

## Installation
Note can only be run with 

1. [Install Poetry to Local Machine](https://python-poetry.org/docs/)

2. Clone the Project Repository via SSH

```bash
git@github.com:uchicago-capp122-spring24/food.get.git
```

3. Install Virtual Environment and Dependencies

```bash
poetry shell
poetry install
```

## Usage
Project **must** be run in the Poetry virtual environment. 
Upon completion of the above installation requirements and within the project terminal, 
and on each subsequent rendering of the project, initialize the virtual environment by running:

```bash
poetry shell
```
<br />

**Execute the project by running:**
```bash
python -m food_get
```
<sub> This command may take a minute to load the project to terminal.</sub>
<br />
<br />

You are then given an HTTP link, as seen below. Copy the link into your preferred browser to interact with the webpage.
<br />

```bash
Dash is running on http://127.0.0.1:8051/

 * Serving Flask app 'food_get.ui.project_dash'
 * Debug mode: off
 * Running on http://127.0.0.1:8051
Press CTRL+C to quit
```

## Overall Notes
If you encounter issues with Dash or ... please run the following commands within the poetry shell:
```bash
python3 -m pip install...
python3 pip install....
```

## Acknowledgments
CAPP 122 Instructor - Professor James Turk

CAPP 122 Project TA - Reza Rizky Pratama

Original USDA Food Access Research Atlas used for data collection and comparison:
- [Food Access Research Atlas](https://www.ers.usda.gov/data-products/food-access-research-atlas/go-to-the-atlas/)


