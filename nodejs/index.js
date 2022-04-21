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

let token = "";

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
app.get("/callback", async (req, res, next) => {
    let code = req.query.code;

    const {
        tokens
    } = await oauth2Client.getToken(code)
    oauth2Client.setCredentials(tokens);
    token = tokens;

    return res.status(200).json(token);
});

// get users profile
app.get("/user", async (req, res, next) => {
    // get profile data
    let gmail = await google.oauth2({
        auth: oauth2Client,
        version: 'v2'
    });

    let profile = await gmail.userinfo.get();

    return res.status(200).json(profile);
})

// revoke
app.delete("/user", async (req, res, next) => {
    await oauth2Client.setCredentials(token);

    await oauth2Client.getAccessToken(async (err, access_token) => {
        if (err) {
            reject(err);
        };

        await oauth2Client.revokeToken(access_token);

        return res.status(200).json("successful");
    });
})

app.listen(3000, console.log("Server running"));