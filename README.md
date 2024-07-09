# ISRO Nowcasting of Meteorological Satellite Images using AI/ML Techniques

![ISRO Logo](results/isro.svg)

## Output:





Demo :

https://github.com/prasannarajezzzy/ISRO-NowCasting-using-ConvLSTM/assets/30752161/aa0a7b60-2caa-40d9-8f92-4fe1c8540f59

Video: [Link to Video](results/12seq24hihihi.mp4) 
PPT: [Download PDF](SIH%20ppt.pdf)


<video width="640" height="480" controls>
  <source src="results/12seq24hihihi.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>



## Team Information
- Organization: Indian Space Research Organization (ISRO)
- Team Name: APOLLO 6
- Team Leader: Prasanna Rajendra 
- College Code: 1-4265914023
- Category: Software
- Domain: Miscellaneous

## Introduction
The goal of this project is to develop an AI/ML-based software solution that enables nowcasting of meteorological satellite images. Nowcasting refers to the short-term forecasting of weather conditions, specifically within a period of 3-6 hours. By leveraging data from INSAT-3D and INSAT-3DR, this software will generate nowcasted satellite images and their animation loops at a 30-minute interval.

Nowcasting plays a crucial role in providing location-specific weather forecasts, enabling timely preparations and responses to emergency situations. While traditional nowcasting approaches involve solving complex physics equations or using extrapolation techniques, we aim to explore machine learning techniques that have shown promising results in this domain.

## Problem Statement
The primary challenge is to capture the spatiotemporal patterns in meteorological satellite images and use them to predict future images accurately. We will focus on utilizing Convolutional LSTM (ConvLSTM) networks, which have demonstrated better performance compared to CNN and FC-LSTM networks in nowcasting tasks.

## Solution Overview
Our proposed solution involves building a deep learning model using ConvLSTM to predict satellite image sequences up to a lead time of 3-6 hours. The model will take a sequence of six present images as input and generate six future images as output. This encoding-forecasting structure, consisting of multiple stacked ConvLSTM layers, effectively captures the spatio-temporal patterns in the data.

Mathematically, the problem can be formulated as follows:

Input: T[n-5, n] (sequence of six present images) 

Output: T[n+1, n+6] (sequence of six future images)


## Technology Stack
The software solution will be developed using the following technologies and frameworks:

- **Python**: Used for data preprocessing and building the deep learning model.
- **Flask**: A web framework used to encapsulate the model and provide dynamic functionality to users.
- **ConvLSTM**: A deep learning method used to capture spatio-temporal patterns and learn long-term dependencies.

## Use Cases
The AI/ML-based software for nowcasting meteorological satellite images can be applied to various use cases, including:

- Predicting road conditions
- Providing weather guidance for aviation
- Issuing urban rainstorm warnings
- Alerting heat and cold waves

## References
1. Xingjian Shi, Zhourong Chen, Hao Wang, Dit-Yan Yeung, Wai-kin Wong, and Wang-chun Woo. Convolutional LSTM network: A machine learning approach for precipitation nowcasting. In Twenty-Ninth Conference on Neural Information Processing Systems (NIPS), 2015.

---

Please note that this README is a brief overview of the project. For detailed information on installation, usage, and contribution guidelines, please refer to the project documentation and source code.


