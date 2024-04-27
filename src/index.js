// const nodeMailer = require('nodemailer');
const express = require("express");
const path = require("path");
const collection = require("./config");
const bcrypt = require('bcrypt');
const notifier = require('node-notifier');
const app = express();
const {exec} = require('child_process');
let multer = require('multer');
const { error } = require("console");
//storage and filename setting
let storage = multer.diskStorage({
    destination:'public/images/',
    filename: (req,file,cb)=>{
        cb(null,file.originalname)
    }
})
let upload = multer({
    storage: storage
})
app.use(express.json());
app.use(express.static("public"));
app.use(express.urlencoded({ extended: false }));
app.set("view engine", "ejs");
app.get("/", (req, res) => {
    res.render("login");
});
app.get("/login", (req,res)=>{
    res.render("login");
})
app.get("/signup", (req, res) => {
    res.render("signup");
});
app.post("/signup",upload.single('photo'),async (req, res) => {
    const user_aadhaar_number = req.body.aadhaar;
    const pass = req.body.password;
    const mail = req.body.email;
    const data = {
        name: req.body.username,
        password: req.body.password,
        aadhaar: req.body.aadhaar,
        phone: req.body.mobile,
        email:req.body.email,
        pagePhoto: req.file.filename
    }

    const existingUser = await collection.findOne({ aadhaar: data.aadhaar });
    if (existingUser) {
        res.send('User already exists. Please choose a different username.');
    } else {
        const saltRounds = 10; 
        const hashedPassword = await bcrypt.hash(data.password, saltRounds);
        data.password = hashedPassword;
        const userdata = await collection.insertMany(data);
        exec(`python zkpa.py ${user_aadhaar_number} ${pass} ${mail}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return;
            }
            console.log(`stdout: ${stdout}`);
        });
        console.log(userdata);
        notifier.notify({
        title: 'Successfully Created User',
        message: 'You will be redirected to login page now',
        sound: true, 
        timeout: 10 
});
        res.render('login');
    }

});

// Login user 
app.post("/login", async (req, res) => {
    try {
        const check = await collection.findOne({ Key: req.body.username });
        if (!check) {
            res.render("user")
        }
        const isPasswordMatch = await bcrypt.compare(req.body.password, check.password);
        if (!isPasswordMatch) {
            res.render("wrong");
        }
        else {
            res.render("home",{username: check.name,pagePhoto:check.pagePhoto});
        }
    }
    catch {
        res.render("error");
    }
}
);


const port = 5000;
app.listen(port, () => {
    console.log(`Server listening on port ${port}`)
});