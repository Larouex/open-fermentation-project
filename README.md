[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)&nbsp;<img src="https://img.shields.io/badge/OFS v1-Open%20Fermentation%20Project%20v1-yellowgreen">

<img src="./assets/open-fermentation-project-logo-v2_500px.png" width="500"/>

## Contents

- [Mission Statement](#mission-statement)
  - [Our Mission](#our-mission)
  - [Our Story](#our-story)
  - [Our Values](#our-values)
    - [Quality](#quality)
    - [Sustainability](#sustainability)
    - [Education](#education)
    - [Community](#sommunity)
- [Welcome](#welcome)
  - [The Hardware (Overview)](#the-hardware)
  - [The Software (Overview)](#the-software)

# Mission Statement

## OUR MISSION

The Open Fermentation Project exists to make automated fermentation accessible to all. Fermentation makes food more nutritious and is a process likely used to create some of your favorite foods and drinks. Inspired by artisans and foodies alike, we give you the tools you need to engineer your personal getaway to artisanal food. The result is artisan-level produces that help people stay healthy.

## OUR STORY

Launched in 2022, the Open Fermentation Project began with a simple vision: to make automated fermentation more accessible.

It all began several years ago when I started to develop a unique software and hardware with the goal to open source it. I wanted anyone with basic engineering skills to be able to put together our system. Little did I know, it was the beginning of the Open Fermentation Project.

Today, our hallmark product is the “Saluminator” — an appliance that promises to bring precision curing and fermentation to home and custom curing chambers. We offer everything from complete DIY kits to fully assembled Saluminators to allow you to cure meats and other recipes that require temperature, humidity and time control. Recipe management is the core of the Saluminator IoT Management Automation System and we have worked closely with design experts on perfecting its user interface.

As proponents of open design, we have proudly made our design accessible and encourage everyone to build one of their own. We share all the details with you and invite you to follow our step-by-step instructions that make integration flawless.

Through open design, we have also grown to be a full-fledge community where hundreds of people come together to make automated fermentation more accessible. Our people are at the heart of what we do and allow us to further our mission. We believe that food and technology must work together to further the food industry for the better.

As we continue to grow, we promise to continue to make automated fermentation more accessible. The Open Fermentation Project is a food tech company. Moreover, it’s a place for a community of foodies — just like you and I.

## OUR VALUES

To us, food is more than just business, it’s passion. That’s why, we stand by our values with the aim to inspire the entire industry to uphold new standards.

- ### Quality

  We love artisanal food more than you can imagine. Hence, we take quality very seriously. Our products have been tested and approved to go beyond your everyday kitchen appliances to provide delicious recipes friends and families are sure to enjoy. You can find the taste of quality in everything we do and it has never tasted so good.

- ### Sustainability

  A big part of what we do is done to modernize the food industry to in turn enhance its sustainability and efficiency. We take a sustainable approach to everything we do and strive to find the perfect balance of nature, and performance. Rest assured, we develop our products for a greener and better tomorrow.

- ### Education

  We are committed to keeping the conversation around food going. Advancing the industry, is our number one priority and we believe that starts with better education. Via our innovative technologies, we’re changing the way we think and are starting the conversation around artisanal food. We promise to continue to be a tool for education.

- ### Community

  We are proud to be a place for community for people to come together and to share their passion for food. Beyond bringing solutions, we like to bring people together to take our mission to the next level. As the industry advances, our community motivates us to continue to learn and to deliver exceptional products.

# Welcome!

The Open Fermentation Project is...

- Reference Hardware for an Industrial IoT "Internet of Things" Fermentation Appliance
- The Automation Software to Manage a Fermentation Recipe Lifecycle
- Cloud Integration for Telemetry and Monitoring

# The Hardware

The curing appliance is branded and trademarked as the "Saluminator" and was developed by Larry W Jordan Jr for Larouex Gourmet Foods LLC. The trademark is registered for commercial projects.

We have opened up the design and how to build the device and you are encouraged to build one for yourself and the only restriction is that you do not pally the Saluminator our trademark for any commercial projects or usage.

We developed this appliance to bring precision curing and fermentation to home and custom curing chambers. The entire project is based on “open source” software and “open and available” components that anyone with basic engineering skills could put together our system. We share this all with you and you are welcome to just use the instructions here to build your system and/or we are happy to sell you everything you need from a complete DIY kit to everything fully assembled and ready to install.

We designed the Saluminator for the production of fermented products and specifically for the automation of dry curing meats and other recipes that require control over temperature, humidity and time. Connected to the power of the cloud and through the acquisition of stream telemetry and machine learning, the Saluminator IoT Automation tunes itself to variances in the ambient environment and the characteristics of your specific curing chamber

# The Software

Recipes in the Saluminator are fixed with a starting time and a ending time. The time between is the “Recipe Cycle” and it can be as simple as one set of settings applied to the whole fermentation cycle or more complex with three(3) phases in the cycle automatically managed by the Saluminator’s automation software.'

[Click Here for Software](./software/)

# The Cloud

Overview of the Metrics and Telemetry that Communicated to the Cloud for Analysis and Machine Learning.

## AZURE IOT CENTRAL

The Saluiminator has optional capabilities to connect and seamlessly integrate your appliance with Microsoft's Azure IoT Central subscription offering. Azure IoT Central provides scalable telemetry processing and visualizations, data export and connected communications with your Salmuninator. Learn More...

## TELEMETRY FEATURES

Each time the Samulinator takes a reading of a sensor, the data is sent to Azure IoT Central to record the values. This keeps an ongoing record of things like temperature and humidity readings.

- ### State Changes

  The Saluminator tracks the changes associated with the AC Relays that toggle the Humidifier, Dehumifier, Chiller and Heater. This data is aggregated along with the telemetry to support machine learning to create the perfect ambiance in the curing chamber.

- ### Tracking Events

  We track overrides, shut downs, restarts and other signficant events for the Saluminator.

## RECIPE REPORTING

- ### Incubation Started

  The date and time that the Incubate phase STARTED.

- ### Incubation Ended

  The date and time that the Incubate phase ENDED.

- ### Incubation Percentage Completed

  The amount of completion for the Incubate phase relative to the current date and time.

- ### Cure Started

  The date and time that the Cure phase STARTED. Cure Ended The date and time that the Cure phase ENDED.

- ### Cure Percentage Completed

  The amount of completion for the Cure phase relative to the current date and time.

- ### Finish Started

  The date and time that the Finish phase STARTED. Cure Ended The date and time that the Cure phase ENDED.

- ### Finish Percentage Completed

  The amount of completion for the Finish phase relative to the current date and time.

- ### Checkpoint Hour

  Checkpoint pointer to the exact hour that the Salumintor is at for the whole recipe cycle.

- ### Last Reported from Device

  The date and time that the last sending of the properties data from the Saluminator.
