var express = require("express");
var bodyParser = require("body-parser");
var app = express();
app.use(express.static("public"));
app.use('/css', express.static(__dirname + '/lib/bootstrap/css'));
app.use('/JOEY2.png', express.static(__dirname + '/views/JOEY2.png'))
app.use('/style.css', express.static(__dirname + '/public/style.css'));
app.set("view engine", "ejs");
app.set("views", "./views");
app.listen(3000);

app.use(express.urlencoded({extended: false}));

const {Pool} = require('pg')
const connectionString = 'postgres://gecksmtj:8xTHFHDY7Nqu80PT8yv_0OLZi7sA1Uz9@suleiman.db.elephantsql.com:5432/gecksmtj'
const pool = new Pool({
  connectionString,
})


app.get('/', function(req, res){
  res.render("main");
});

app.post('/', async (req,res)=>{
  let fname = req.body.signfname;
  let lnane = req.body.signlname;
  let email = req.body.signemail;
  let pass = req.body.signpass;
  let pnumber = req.body.signpnumber;
  let area = req.body.signarea;
  let town = req.body.signtown;
  try{
    let rs = await pool.query("INSERT INTO customer_info VALUES ('"+email+"','"+fname+"','"+lnane+"','"+pass+"','"+pnumber+"','"+area+"','"+town+"','Active');")
    console.log("Added");
    res.render("main");
  }catch(err){
    console.log("Smthing went wrong!");
  }
});

app.post('/login', async (req, res) =>{
  var user = req.body.txtemail;
  var pass = req.body.pass;
  // console.log(user);
  // console.log(pass);
  try{
    let rs = await pool.query("Select * from customer_info where email = '"+user+"' and pass = '"+pass+"' and status = 'Active'");
    if(rs.rowCount > 0){
       res.render('customer');
    }
    else{
      rs = await pool.query("Select * from management where user_id = '"+user+"' and pass = '"+pass+"' and status = 'Actv'");
       if(rs.rows[0].designation == 'Manager'){
         res.render('manager');
       }
       else if(rs.rows[0].designation == 'Employee' || rs.rows[0].designation == 'Cook'){
        res.render('employee')
       }
    }
  }catch(err){
    console.log("Smthing went wrong!");
  }
});






// app.get('/login', function(req, res){
//     res.render("login.ejs");
// })



