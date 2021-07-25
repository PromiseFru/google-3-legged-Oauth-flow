require("dotenv").config();

var OAuth = require('oauth');
var express = require("express");

const app = express();

let CLIENT_ID = process.env.CLIENT_ID;
let CLIENT_SECRET = process.env.CLIENT_SECRET;
let REDIRECT_URL = process.env.REDIRECT_URL;

// start oauth
app.post("/start", (req, res, next) => {
   
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