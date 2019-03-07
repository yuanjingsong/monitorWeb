# monitorWeb
Try to use spider to monitor web 

func:
  * use Spider to get the information about the web
  * send email about update when upload news
  
### Requirements
  Python 3.5
  Scrapy
  MongoDB
  
### Custom ur own Spider:

  you can add ur own web site and pattern in list to get information
  
  the pattern must be the XPath pattern
  
### Tip

  * When run the spider on ur vps/ecs, use the port 465 instead of 25 because of the potential security
    So make sure that the 465 port are open 
    
  * Use environment variable instead of writing ur email information on code
