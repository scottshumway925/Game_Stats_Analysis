The data for this project has come from RAWG games, which can be found at this link: https://rawg.io/apidocs

# Game_Stats_Analysis

This repo contains a data-analysis project that takes in data for video games and board games determines which type of games are performing the best.


## Instructions for Build and Use

Steps to build and/or run the software:

1. Install python on your computer and run the code.
2. Make sure that pandas, kaggle json are installed in your environment.

Instructions for using the software:

1. Just run the program and the data will be returned to you through the console

## Development Environment 

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Same as build and use. 
* Python installed
* Libraries: pandas, json

## Useful Websites to Learn More

I found these websites useful in developing this software:

* Rawg.io
* Bro Code: Youtube Channel -- https://www.youtube.com/watch?v=VXtjG_GzO7Q
* Pandas website -- https://pandas.pydata.org/docs/getting_started/index.html#getting-started

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [1] I would like to make more data analysis files to pinpoint different parts of the data to truly narrow down which game types perform the best.
* [2] I would like to find a better way to sanitize my data then just dropping the data points that don't meet my specific requirements, requirements such as having a retail cost not at 0 and not enough people owning the game to warrant good data.
* [3] One interesting thing to note here is that the data was really hard to predict with. There was a lot of variance with the data, most likely due to it being opinion based. I would like to try to find which data points for board games show a greater correlation between predicted ratings and revenue potential. I truly do want to see this project go places.

## Questions the data answered

Here are the questions that I asked which were answered through my data analysis.

* [1] What types of board games tend to perform the best?
* * Games that contain trading, multi-use cards, tech trees, king of the hill, and hexagon grid mechanics tend to perform well. These are the mechanics listed that had multiple different games using them that grossed the most money and scored well with user ratings.
* [2] What game mechanics warrant the best overall user rating?
* * The game mechanics that perform the best in terms of user rating, with at least 5 games using the mechanic, are narrative choice, ownership, multi-use cards, movement points, tech trees, and campaign / battle card driven mechanics
* [2.5] Something interesting to note here is that the mechanics multi-use cards and tech trees were present in both of the top ranking games from these last two questions.
* [3] Which board game mechanics are the most popular in games?
* * The 10 most popular game mechanics are the following: Hand management, variable player powers, solo / solitaire game, open drafting, variable set-up, dice rolling, end game bonuses, cooperative game, and deck, bag, andpool building.
* [3.5] One thing I find really interesting here is that the most popularly used game mechanics tend not to show up in the highest rated games or the types of games that make money super consistently. Part of this may be due to their large game pool, providing a more evenly distributed bell curve. Another reason for this may be that the mechanics have grown stale for the general populace. 