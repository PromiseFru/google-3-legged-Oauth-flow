require("dotenv").config();

var express = require("express");
const {
    google
} = require('googleapis');

const app = express();

let CLIENT_ID = process.env.CLIENT_ID;
let CLIENT_SECRET = process.env.CLIENT_SECRET;
let REDIRECT_URL = process.env.REDIRECT_URL;

const oauth2Client = new google.auth.OAuth2(
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URL
);

// generate a url that asks permissions for Blogger and Google Calendar scopes
const scopes = [
    'https://www.googleapis.com/auth/userinfo.profile'
];

// start oauth
app.get("/start", (req, res, next) => {
    const url = oauth2Client.generateAuthUrl({
        // 'online' (default) or 'offline' (gets refresh_token)
        access_type: 'offline',

        // If you only need one scope you can pass it as a string
        scope: scopes
    });

    return res.status(200).json(url)
});

// oauth callback
app.get("/callback", (req, res, next) => {

});

// get users profile
app.get("/user", (req, res, next) => {

})

// revoke
app.delete("/user", (req, res, next) => {

})

app.listen(3000, console.log("Server running"));