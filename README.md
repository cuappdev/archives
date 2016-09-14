# TCAT-BACKEND

Install Instructions :

1.Install NodeJs from https://nodejs.org/en/download/stable/

    Note: Use “Stable”--should be version 5.10

2.Install NPM at version 2.14.15 with `$ npm install npm@2.14.15 -g`

Note: A later version was installed along with Node--we are installing an older version
ADDENDUM after lecture: If you get an error that says "requires root/administrator privileges", add the word
"sudo" to the beginning of the sommand and run it again. Then, type in yourpassword (it won't show on the
screen) and hit ENTER.  It should work this time.

3.Clone the Chatroom application with `$ git clone https://github.com/cuappdev/tcat-backend.git`

4.Go into the TCAT-BACKEND directory you just cloned and run the following commands:

    $ npm install (This step reads the package.json file and installs all necessary Node Modules.)
    $ mkdir data (This step creates an empty "data" folder inside you chatroom application.)

5.From your original terminal window, run `$ npm start`

You should now have a running server.  Check to see if it worked by navigating to localhost:3000 in your browser.  You should see a success message.

The following endpoints are provided currently:

/schedules

/stop-locations

/stop-schedules
