# Project milestone 2 C1n3mada 

The current repository was created within the scope of the second project milestone during the course [CSS-401 Applied Data Analysis](https://edu.epfl.ch/coursebook/en/applied-data-analysis-CS-401) at [EPFL](https://www.epfl.ch/en/).

The authors of the repository are:
 
- Can Berk Alakir
- Said Gürbüz
- Nadezhda Ilieva
- Céline Kalbermatten
- Jennifer Shan

Together they form the group **C1n3mada**. 😊

## Table of contents:

- [Abstract](#abstract)
- [Setup](#setup)
- [Repository structure](#repository-structure)
- [Research questions](#research-questions)
- [Proposed additional datasets](#proposed-additional-datasets)
- [Methods](#methods)
- [Proposed timeline](#proposed-timeline)
- [Organization within the team](#organization-within-the-team)
- [Questions for TAs](#questions-for-tas)

## Abstract
&#x1F3AC; **C1n3mada presents: Money, Money, Movies – The secrets of movies’ box office success** :movie_camera:

It’s time to take a break from whatever you’re doing and enjoy some movies. The lineup includes 5 movies, each telling its own story. Together, they provide insights into what influences a movie's box office revenue. 
How do factors like rating, language, country, genre, director or even the release season affect a movie’s financial success? Through the selected films you will get detailed insights in a fun and engaging way. Each factor is analysed individually, with overlapping analyses across several factors, all together providing a comprehensive understanding by the end. In addition to learning about the influencing factors you will also discover possible reasons, as the movies also include explanatory elements.

You will be enjoying and learning at the same time. C1n3mada hopes that you are ready for this unique experience! :popcorn:


## Setup

### Pre-requisites

- [Python](https://www.python.org/downloads/)
- [Jupyter](https://jupyter.org/)

**`requirements.txt`** is provided to install the necessary Python dependencies.

```sh
pip install -r requirements.txt
```

## Repository structure
This repository is structured the following way:

```
ada-2024-project-c1n3mada/
├── data/                              # Directory containing all the data 
    ├── processed/                         # Directory containing data that has been processed
       ├── movies_processed.csv                # File containing the processed movies dataset used for the analysis
├── notebooks/                         # Directory containing several notebooks used for data pre-processing or analysis
    ├── analysis_inflation.ipynb           # Jupyter notebook performing the inflation correction on the data
    ├── analysis_merging.ipynb             # Jupyter notebook performing the datasets merging
    ├── data_preparation.ipynb             # Jupyter notebook performing the whole data pre-processing (including the datasets merging)
    ├── initial_analysis.ipynb             # Jupyter notebook performing some initial analysis on the data
    ├── Q1.ipynb                           # Jupyter notebook containing the implementation of movie 1
    ├── Q2.ipynb                           # Jupyter notebook containing the implementation of movie 2
    ├── Q3.ipynb                           # Jupyter notebook containing the implementation of movie 3
    ├── Q4.ipynb                           # Jupyter notebook containing the implementation of movie 4
    ├── Q5.ipynb                           # Jupyter notebook containing the implementation of movie 5
├── src/                              # Directory containing some main source code scripts 
    ├── utils/                             # Directory containing some utils scripts
       ├── data_utils.py                        # Script containing functions to pre-process the different datasets
       ├── merge_utils.py                       # Script containing functions to merge the different datasets
       ├── plot_utils.py                        # Script containing functions to plot some data
├── tests/                            # Directory containing tests for the project
├── requirements.txt/                 # File containing all requirements to run the current project
├── results.ipynb/                    # Jupyter notebook containing all the initial analysis and implementations
```

The `results.ipynb` is the Jupyter notebook containing the initial analysis and implementations done for milestone 2. 


## Research questions
**Movie 1: Echo** 📢 <br> 
How does a movie’s IMDb rating relate to its box office success? <br> 
This film explores the IMDb rating, being a reflection of audience and critic reception for movies. The correlation between rating and the box office revenue is presented, first for all movies in general and then broken down by genre.

**Movie 2: Tongues** 🗣 <br> 
How do the language and country of a movie influence its box office revenue? <br>
This film explores the importance of a movie's primary language and release country, as well as the correlation between these two aspects. Additionally, it shows whether movies with more than one original language achieve more success. 

**Movie 3: Shades** 🎭 <br> 
How does a movie's genre impact its box office revenue? <br>
This film aims to provide an understanding of whether certain genres are associated with higher revenues and if the relationship between genre and revenue changes over time.

**Movie 4: Starlight** 💫 <br> 
To what extent is a movie's box office revenue influenced by its director? <br>
This film highlights which directors produce the most movies, which ones generate the highest total revenue and which ones achieve the best average revenue per movie.

**Movie 5: Waves** 🌊 <br> 
How much is a movie’s box office revenue influenced by its release timing and duration? <br>
This film provides insights into the influence of a movie’s release season on its success. It also examines the impact of the movie’s runtime for each season individually and breaks down these factors by genre. 	


## Proposed additional datasets
**IMDb** <br> 
The [IMDb dataset](https://developer.imdb.com/non-commercial-datasets/) is a comprehensive collection of information related to movies, TV shows, and other media. It contains the IMDb user ratings for titles, offering insight into audience reception. This dataset was merged with the original CMU dataset. No new movies were added. Only those present in the CMU dataset were included. If IMDb contained a corresponding rating for a movie, it was added to the dataset. 

**TMDB** <br> 
The [TMDB dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) provides detailed information on movies and TV shows. Since it also contains the box office revenue, it was merged with the original CMU dataset to fill in some missing value in the latter. No new movies were added. 


## Methods

### Data and pre-processing

Initially, all the different datasets are cleaned individually.
- CMU dataset: The numeric fields are converted to appropriate data types. Data fields are standardised to datetime format. The structure fields (languages, countries, genres) are parsed.
- IBDb dataset: Currently, no specific pre-processing is applied.
- TMDB dataset: The date components (year, month, day) are extracted. The financial fields are converted to numeric format. Zero values in the budget and revenue columns are replaced by NaN.

After this first pre-processing step, the three datasets are merged. This happens in two steps.
- Merge CMU with TMDB: A left join on the movie title and release year is applied. Missing data for the box office revenue in the CMU dataset is filled with data from the TMDB dataset if available. Redundant columns are removed after the merge.
- Merge with IMDb: The previously combined dataset is combined with IMDb information from multiple sources. Left joins are used to add title basics, ratings and crew details. The first director is extracted and used to get director details from IMDb’s name basics dataset. Redundant columns are removed to finalise the dataset.

The next phase involves cleaning the merged dataset. Rows with missing values in the combined revenue column are removed. Missing values for the average rating and number of votes columns are replaced with 0 and missing values in the director column are replaced with 'unknown'.

Once the cleaning is completed, an inflation adjustment is made to the dataset. This step adjusts the movie revenue data for inflation to ensure that all financial values are comparable to the most recent year’s dollars. The [Consumer Price Index (CPI) data](https://fred.stlouisfed.org/series/CPIAUCNS) is loaded and pre-processed. Movies released before the earliest available CPI data are removed. The revenue values for the remaining movies are adjusted using the CPI data, aligning them with the target year (the most recent release year). This ensures that all financial values are in current-year dollars, accounting for inflation over time.

At the end of the data pre-processing, some final checks are performed. There should be no negative revenues and no future release dates. The essential columns (movie name, release year, combined revenue, inflated revenue, movie genres and average rating) should exist. The data should be complete, with no Null values. It is also verified that the revenue inflation correction has been applied correctly.

The data resulting from the pre-processing described above is saved as `movies_processed.csv` and used for the analysis.














## Proposed timeline
The following timeline provides an overview of the project implementation.
```
Topic decision — Deadline: 28.10.2024
  - Collect ideas and note preferences for the overall project idea

Define the research questions and the global structure — Deadline: 02.11.2024
  - Define the precise research questions for the chosen project
  - Define additional datasets and their purposes
  - Consider implementation methods

Data pre-processing — Deadline: 09.11.2024
  - Explore the datasets and clean them accordingly

Implementation of research questions — Deadline: 13.11.2024
  - Define a precise pipeline for each research question
  - Define subquestions 
  - Start with the implementation

Milestone 2 — Deadline: 15.11.2024
  - Merge initial implementations of the research questions
  - Complete the README with all the specific implementation details

Implementation of research questions — Deadline: 08.12.2024
  - Finalise the implementation
  - Refine details, such as the plots

Implementation of the overall story — Deadline: 15.12.2024
  - Implement the data story and put all the found results together
  - Website implementation

Code cleaning and final details — Deadline: 20.12.2024
  - Clean the code
  - Finalise the README 
  - Fix some last details
```

## Organization within the team
The following table defines the internal milestones up until project milestone 3.
| Task                             | Person in charge    | Deadline      |
|----------------------------------|---------------------|---------------|
| Movie 1 (final implementation)   | Said                | 08.12.2024    |
| Movie 2 (final implementation)   | Céline              | 08.12.2024    |
| Movie 3 (final implementation)   | Nadezhda            | 08.12.2024    |
| Movie 4 (final implementation)   | Jennifer            | 08.12.2024    |
| Movie 5 (final implementation)   | Can                 | 08.12.2024    |
| Implementation of the story      | All                 | 15.12.2024    |
| Code cleaning and final details  | All                 | 20.12.2024    |
| README                           | Céline              | 20.12.2024    |

## Questions for TAs
XXXXXXXXXXXXXX




