const mongoose = require('mongoose');
const connect = mongoose.connect("mongodb+srv://abhinavajay20:ijdDhmzGxB3uBeJg@cluster0.r9abfzl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0");

// Check database connected or not
connect.then(() => {
    console.log("Database Connected Successfully");
})
.catch(() => {
    console.log("Database cannot be Connected");
})

// Create Schema
const Loginschema = new mongoose.Schema({
    name: String,
    password: String,
    aadhaar: String,
    phone: String,
    email:String,
    // Key:String,
    pagePhoto:String
});

// collection part
const collection = new mongoose.model("users", Loginschema);

module.exports = collection;