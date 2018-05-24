# Slantometer: An exploratory study with MTurk

Slantometer is an exploratory in the slant (latent space reporting space that can serve as the seeding ground for political bias) in broadcast journalism. This repository contains the materials used. This study was performed by members of the Viral Communications group at the MIT Media Lab. For more information about the decision made behind this study and for some of the results, please reach out to the group at viral [at] media [dot] mit [dot] edu. You can also reach out to me personally at lrachana [at] gmail [dot] com

## What's here?
This repository contains:
- Broadcast new transcripts in various stages of cleansing
- Scripts that were used to gather, retrieve and calculate data
- Raw data and initial analysis

#### Transcripts
With the help of members at TV Archive, we gathered the transcripts from three broadcast news channels. The transcripts collected contained coverage on particular events that we selected over the course of several days. The transcripts are broken down into 6 phases as follows:

- Phase 1: Original transcripts in their .srt format 
- Phase 2: Transcripts with the time stamps removed and the text parsed into human readable sentences. 
- Phase 3: Transcripts with advertisements and coverage about unrelated events and topics removed
- Phase 4: Transcripts broken down into 20 sentence files
- Phase 5: Transcripts with the order in which sentences were tested and the url the HIT was posted to.
- Phase 6: The tested sentences and their label assignments according to the responses of the MTurk Workers. 

#### Scripts
The data gathering for this study occured on Amazon's Mechanical Turk (MTurk) platform. Mechanical Turk allows people to complete simple surveys online in return for compensation. We leveraged this platform to gather people's views on the sentences spoken in broadcast news. More details about the scripts are below. 

#### Data
The files in the data directory contain the raw responses of the information collected and some high level analysis on the information  collected. Please contact us for more details. 


## MTurk Scripts
The scripts folder contains several scripts that primarily helped with facilitating our surveys on MTurk. The scripts included are:

- mturk_analyze.py : Performs all of the data analysis on the raw data
- mturk_expire_hit.py: Used to delete a HIT that was released by accident. Needs a HIT ID to take HIT offline
- mturk_launch_survey.py: Launches the survey online.Takes in the text file to be tested as a parameter and outputs the  order in which the sentences were tested and the url the HIT was posted to. HIT IDs are saved into the mturk_needs_payment.txt file. 
- mturk_pay.py: Pay workers for the surveys they have completed. Reads in data from mturk_needs_payment.txt file
- mturk_retrieve.py: Reads HIT IDs from mturk_needs_payment.txt and the mturk_needs_payment.txt and retrieves the worker responses from online. 
- reporting_percentage.py: Calculated the percentage of time an event was covered in a report. Data is saved to reporting_percentage.csv
- srt_parse.py: Takes in an .srt file and removes the timestamps and reorganizes the trascription into legible sentences.
- variables.py: Contains you AWS access/secret keys, and the host names needed for the sandbox and production environment. By default all scripts will execute in the sandbox envinronment until the PROD boolean is changed. Make sure to update your AWS keys in the file as well. 

## 
You must seek permission from us before you use any of the information or code here. 
