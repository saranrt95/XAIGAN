# XAIGAN
A new framework for GANs evaluation based on eXplainable Artificial Intelligence models.

This repository contains useful code for the paper work **Narteni S., Orani V., Ferrari E., Verda D., Cambiaso E., Mongelli M. (2021). “Explainable Evaluation of Generative Adversarial Networks for Wearables Data Augmentation”** submitted to Elsevier-Engineering Applications of Artificial Intelligence


# Overall structure
The repository contains the following elements:
- Real Data and Rules folder with under 40 and over 40 real datasets and rulesets obtained from Logic Learning Machine.
- GAN_physicalFatigue.ipynb: the code used for data augmentation with GANs on physical fatigue dataset under 40 and over 40 groups. It is used to generate 10 synthetic datasets for each group.
- Fake Datasets and Rules folder: contains the result of data augmentation for under and over 40 and the "fake LLM" rulesets obtained for each run of GAN.
- Real + Fake Datasets and Rules folder: contains the combination of real+fake datasets for under and over 40 and the "real+fake LLM" rulesets obtained for each run of GAN.
- Reliability methods folder: contains the datasets selected, according to performance metrics and rule similarity, for this phase of reliability analysis and the code to individuate (*reliableTest_GAN.py*) and plot the safety regions (*plot_regions.m*)

# Usage
- For data augmentation, just run the notebook; check the import of real datasets and make sure that over and under names are consistent (for over 40, no "under" word should be present in the code and viceversa).
- Once generated the fake datasets, you can try the inference of safety regions by using the code in *Reliability methods folder*: just run *reliableTest_GAN.py*


