## Predicting Weightlifting Performance from Submaximal Training Data
### Andrew Kelley

### Project Motivation
When lifting, people will sometimes try to push or squat double to triple their bodyweight . Due to the physicality of the lifting, it is possible for people to get seriously injured when trying to perform these heavy lifts. This project aims to develop a data driven approach to estimating one-rep max (1RM) performances using submaximal training data.

This project is subjective because different people use different weights. Some may be heavier and some may be lighter. I use a kaggle dataset (listed below) that has 3 years worth of recorded exercises for a singular person.

[Weight Training CSV](https://www.kaggle.com/datasets/joep89/weightlifting) 

### Who Benefits?
This project can help normal people (and athletes and their lifting coaches/trainers if they have one) determine what their possible 1RM can be. Using the prediction model I come up with, people can use their own personal data of recorded lifts to judge how much weight they should be loading onto the bar when attempting a 1RM.

### Research Question
Can weightlifting 1RM performance be accurately predicted from submaximal training data?

### Target Variables
Since there are multiple different lifts recorded in this dataset, i will either end up filtering it down to predict 1RM for either squats or bench press (or both!).

Predictor variables will include session maximums, number of repetitions, number of sets, and total training volume. I may engineer features, but am unsure as of now.

### Limitations and Expected Outcome
There are limitations here because of factors that are difficult to account for such as fatigue or what food peoiple are eating among other things

The expected outcome is to predict 1RM with reasonable error margins, providing insights for training and managing heavier weights.

