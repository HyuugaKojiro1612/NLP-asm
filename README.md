# Customer Service Response System - A NLP Assignment (CO3085)

## Description

This assignment is the implementation of a simple CS response program in Vietnamese, using NLU techniques.

## Prerequisites:
- [NLTK 3.8.1](http://www.nltk.org)
- [Lark 1.1.8](https://lark-parser.readthedocs.io/en/stable/)

```bash
$ pip install -r requirements.txt
```

## Part 1:

In the first part, a simple augmented grammar is designed to generate and parse some responses from customer. Run the command below to generate the output files for part 1.

```bash
$ python part1.py
```

## Part 2: 

In the second part, a flight service-based semantic grammar is designed to process the provided questions. The sentences are transformed to syntactic tree, logical form, semantic procedure, and generate simple answers, respectively. This part also generates grammatical relations from the given database. Run the command below to generate the output files for part 2.

```bash
$ python part2.py
```