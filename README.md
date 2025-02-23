Elevator Pitch:
Our web-app will allow users to generate honeypot data based on their tailored company profile, then they can run intrusion detection on their exported logs without leaving the website.

Inspiration:
Our team was inspired by envisioning the possibilities at the intersection of Gen AI and Cybersecurity.
We started by having two separate wants - one for Gen AI and one for Cybersecurity. It was the coming together of these preferences that sparked our imagination for this project.

What it does:
Our webapp will generate bait files to be used in cyber honeypots and can also be used to run intrusion detection on logs from honeypots created with the generated data.

How we built it:
For our honeypot data generator, we rely heavily on LLMs, in this case OpenAI's GPT-4o-mini, to extract meaningful keywords and information about a company based on their description. Then, from that profile, we generate spreadsheets, pdfs, and text files of fake data which looks convincingly confidential. We then run each file through a few reviews and revisions by LLMs to ensure generated data is high quality. 
For our intrusion detection, we trained a random forest classifier on cybersecurity log data from Kaggle, experimenting with hyperparameters until we reached a point where improvements to the model are negligible without overfitting. We utilized the H200's provided by NVIDIA for training with cupy to utilize the H200's hardware. We created our frontend with streamlit with a chatbot style interface.

Challenges we ran into:
Training with the number of configurations we had was very time consuming, even on an H200, but the improvements in performance were worth the extra training time. We also are new to using streamlit, but we decided to use it for the learning experience and we believe it did its job quite nicely. 

Accomplishments that we're proud of:
We are proud of the fact that we managed to train an ML model in a hackathon setting, and we're super proud of the fact we were able to effectively complete 2 project ideas in one hackathon.

What we learned:
We leaned new skills such as how to use streamlit, create and edit Gen AI software, and video editing. 

What's next for MCM Beehive:
MCM Beehive has created a valuable tool to lure would-be bad actors in cyberspace via honeypots. MCM Beehive has developed a proof of concept, which if expanded further could lead to comprehensive cybersecurity coverage spanning from identifying threats to actively going after and managing them. 
