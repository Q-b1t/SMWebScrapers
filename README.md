# Web Scrapper Environment
This is a template for implementing the social network web scrapper in an environment can be deployed in a IAAS or Serverless cloud framework for automation.
# File Structure
```
.
└── Workspace/
    ├── actorInputScripts/
    │   ├── # parametrizar por argsparse si se genera para posts o para comments
    │   ├── facebookInput.py
    │   ├── instagramInput.py
    │   ├── linkedinInput.py
    │   └── tiktokInput.py
    ├── actorInputFiles/
    │   ├── posts/
    │   │   ├── facebookInput.json
    │   │   ├── instagramInput.json
    │   │   ├── tiktokInput.json
    │   │   └── linkedinInput.json
    │   └── comments/
    │       ├── facebookInput.json
    │       ├── instagramInput.json
    │       ├── tiktokInput.json
    │       └── linkedinInput.json
    ├── configurationFiles/
    │   ├── posts/
    │   │   ├── facebook.cfg
    │   │   ├── instagram.cfg
    │   │   ├── tiktok.cfg
    │   │   └── linkedin.cfg
    │   └── comments/
    │       ├── facebook.cfg
    │       ├── instagram.cfg
    │       ├── tiktok.cfg
    │       └── linkedin.cfg
    ├── postScraper/
    │   ├── PostScrapper.py
    │   └── posts
    ├── commentScraper/
    │   ├── CommentScrapper.py
    │   └── comments
    └── merger/
        └── MergeData.py
```
# Security & Organization Guidelines (READ BEFORE DEVELOPING)
- Hardcoded credentials is a common security weakness in applications that may lead to unauthorized access or use of the organization's assets, **which will traduce in additional costs in the best case and data breaches, government sactions, and reputational damage in the worst case scenario**. Therefore, before pushing changes, **make sure there are not hardcoded credentials in any of the developed code**. The configuration files are for loading credentials at runtime without the need of hardcoding them. More information on this attack vector [HERE](https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password).
- The configuration files stored here are supposed to be templates. Later on, a command line interphase will be added for the user to specify the correct config file in the pertinent scripts. In the meantime, do not upload configuration files with values unless they reference relative paths inside the workspace or non critical (anything that is not a credential) parameters that will later be added to the command line interface. Also, **do not upload configurations files filled with credentials**. 
- Also, **avoid commiting actual scrapped data in this repository**. In order to accomplish that add the inout and output files/folders to the main ```.gitgnore``` or create a new ```.gitignore``` file wherever you happen to need it. 
- Do not commit virtual environements folders or ```__pycache___```. Add them to the ```.gitignore```
