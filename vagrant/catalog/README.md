# an Item Catalog Application

This application provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Instrucitons to Run Project

### Steps to set up a Google auth application
1. go to https://console.developers.google.com/project and login with Google
2. Create a new project
3. Name the project
4. Select "API's and Auth-> Credentials-> Create a new OAuth client ID" from the project menu
5. Select Web Application
6. On the consent screen, type in a product name and save
7. In Authorized javascript origins add: http://0.0.0.0:8080 and http://localhost:8080
8. Click create client ID
9. Click download JSON and save it into the root director of this project
10. Rename the JSON file "client_secret.json"
11. In main.html replace the line "data-clientid="" so that it uses your Client ID from the web applciation

### Steps to set up a Facebook auth application
1. go to https://developers.facebook.com/
2. go to your app on the Facebook Developers Page
3. click Settings in the left column
4. click Advanced
5. scroll down to the Client OAuth Settings section
6. add http://localhost:5000/ to the Valid OAuth redirect URIs section
7. create fb_client_secrets.json:
```
{
  "web": {
    "app_id": "PASTE_YOUR_APP_ID_HERE",
    "app_secret": "PASTE_YOUR_CLIENT_SECRET_HERE"
  }
}
```

### Setup the Database and start the Server
1. In the root director, use the command vagrant up
2. The vagrant machine will install
3. Once it's complete, type vagrant ssh to login to the VM
4. In the vm, cd /vagrant
5. type "pyhon install_db.py" this will create the database with the categories defined in that script
6. type "python item_catalog.py" to start the server


### Open in a webpage
Now you can open in a webpage by going to either: http://0.0.0.0:8080 and http://localhost:8080
