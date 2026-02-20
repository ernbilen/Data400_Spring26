# Mini-Project 1 Proposal - Probing Localization with a Transformer
## Background
The Sine-Gordon equation with an added global coupling parameter is a differential equation that is known to host discrete breathers and chaotic phases. While the standard Sine-Gordon system is well studied our modified version is less explored and serves as a great testbed to investigate machine learning applications to science (particularly physics)!

[![Torsional pendulum chain modulational instability](https://img.youtube.com/vi/1-BOMA5wk78/hqdefault.jpg)](https://youtu.be/1-BOMA5wk78)

Previous work has focused on developing deep learning models to predict at which pendulum localization would occur. We found that our deep learning model predicted localization with higher accuracy than traditional physics approaches. Later, efforts were made to update our model to a traditional transformer architecture in order to do analysis on its attention. We found this new architecture slightly out performed our old model and that it did so by predominantly focusing on nearest neighbor interactions and characterisitics. This result is bizarre because it challenges the assumption that where localization occurs in our system is chaotic. After this machine learning based discovery additional physics analysis was done to try and make sense of the result. Quickly, a road block was hit in our ability to do the theory work and new tests need to be run with our transformer. 

- We will investigate the Lyapunov exponent of the system be decreasing the percision of our data and tracking the change in performance.
- We will investigate if our transformer can correctly predict localization with only near-neighbors.
- We will follow our newest physics analysis and see if predicitions improve with a different feature space.
- 

## Tractable & Retriveable data
We are interested in investigating ML use in physics. As such, we plan to use ML to answer model based physics questions that have escaped traditional attempts to solve. All the data we need can be simulated from the differential equation that governs our system. In this way, we can run multuiple physics simulations, save the data, and perform manipulations to look at the desired physical quantities.

## Model
We make use of a Spatiotemporal Transformer Encoder with a custom 2D Rotary Positional Embedding that encodes our temporal and spaital dimensions separately using rotational matrices. Hyperparameters my be adjusted for simplicity and easier interpretation but currently we have 8 layers of size 64 and 4 attention heads.

## Implications for stakeholders and Societal Implications
This is basic science research and the implications are for all of humanity. Notably this model and spontaneous energy localization in an otherwise thermalized system is responsible for great tragedies like the Tacoma Bridge Collapse in 1940. Better understanding these systems will allow engineers to design future structures more mindfully allowing them to prevent future catastrophe.
[![bridge collapse](https://img.youtube.com/vi/XggxeuFDaDU/hqdefault.jpg)](https://www.youtube.com/watch?v=XggxeuFDaDU&t=48s)

Many systems important to people lives and society are also chaotic. These include financial markets and the weather. Understanding and characterizing localization in this toy model my grow humanities understanding of these other systems allowing for markets to work more efficently and for the weatherman to be more accurate. This is even more true if we can classify some element of this chaotic system that is actually nonchaotic.

Finally, this model the Sine-Gordon equation with a global coupling parameter models dynamics in Josephson Junction arrays, the technology that is the foundation for superconducting qubit based quantum computing. Progress understanding this work may be directly applicable to improving quantum computing capabilities.


