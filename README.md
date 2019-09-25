# PitchSelection
Pitch Selection analysis on various pitcher and catcher combos in MLB, 2019 season.

I used Aaron Nola to initially develop any analysis and models, but any pitcher could be used. I pulled all 2019 Statcast data 
availbale for Nola from https://baseballsavant.mlb.com/csv-docs. I put the csv file onto a MAMP local server so I could run 
more queries on the data using mySQL and phpmyadmin.

Phase 1 - Breakdown pitch selection in each count and see if the catcher he is throwing to effects pitch selection. Data is 
also divided by batter (L/R). 

Phase 2 - Breakdown pitch selection further, using previous pitch selection to look for tendancies.
