# trailya-notifications

Cloud Function to process public feeds on exposure sites and publish to Firestore.


### Details 

The exposure site information is used by [trailya](https://github.com/tusharm/trailya-app/) app. Currently, it processes feeds from following datasets:
- [NSW COVID-19 case locations](https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-0a52e6c1-bc0b-48af-8b45-d791a6d8e289/details)
- [All Victorian SARS-CoV-2 (COVID-19) current exposure sites](https://discover.data.vic.gov.au/dataset/all-victorian-sars-cov-2-covid-19-current-exposure-sites/resource/afb52611-6061-4a2b-9110-74c920bede77)

#### Design 

Here's the overall architecture that it is a part of:


<img src="https://github.com/tusharm/trailya-app/blob/main/doc/images/system.png" alt="Design" width="500"/>
