# Lab 1: Grade Processing Tools

This project contains two small tools for managing and evaluating course
grades stored in CSV format.

## Files

- `grades.csv`: the working CSV file used for grade data
- `organizer.sh`: archives the current CSV file and creates a fresh one
- `grade-evaluator.py`: validates the grade data and calculates results
- `archive/`: stores timestamped copies of previous CSV files
- `organizer.log`: records each archived file operation

## CSV format

The scripts expect the following header:

```text
assignment,group,score,weight
```

- `assignment`: assignment name
- `group`: `Formative` or `Summative`
- `score`: percentage score from 0 to 100
- `weight`: contribution of that assignment to the final mark

## How to use

Archive the current working CSV and create a new blank one:

```bash
bash organizer.sh
```

Archive a specific CSV file instead:

```bash
bash organizer.sh my-grades.csv
```

Evaluate a grade file:

```bash
python3 grade-evaluator.py
```

When prompted, enter the CSV filename to process.

## Grade rules used

- all scores must be between 0 and 100
- all weights must be zero or greater
- total weight must equal 100
- formative weight must equal 60
- summative weight must equal 40
- a student passes only if both formative and summative averages are at least 50
