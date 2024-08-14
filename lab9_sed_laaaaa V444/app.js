const Env = require('./models/env');
const ConfigModel = require('./models/configmodel');
const Status = require('./models/devicestatus');
const express = require('express');
var qs = require('querystring');
const mongoose = require('mongoose');
const hbs = require('hbs');
var path = require('path');
const bodyParser = require('body-parser');
const axios=require('axios');



var app = express();
app.use(express.urlencoded());  
app.use(express.json());



app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');
hbs.registerPartials(__dirname + '/views')
const static_path = path.join(__dirname, "/public")
app.use(express.static(static_path));
console.log(static_path);
const WebSocket = require('ws');
const { env } = require('process');
hbs.registerHelper('iff', function(a, operator, b, opts) {
  var bool = false;
  switch (operator) {
      case '==':
          bool = a == b;
          break;
      case '>':
          bool = a > b;
          break;
      case '<':
          bool = a < b;
          break;
      case '!=':
          bool = a != b;
          break;
      default:
          throw "Unknown operator " + operator;
  }

  if (bool) {
      return opts.fn(this);
  } else {
      return opts.inverse(this);
  }
});

hbs.registerHelper('ifCond', function(v1, options) {
if(v1%3==2) {
  return options.fn(this);
}
return options.inverse(this);
});

hbs.registerHelper('iftime', function(v1,v2, options) {
if(v1==v2) {
  return options.fn(this);
}
return options.inverse(this);
});

hbs.registerHelper('forlist', function(v1,v2 ,options) {
var i;
var cmd="<option selected value="+v2+">"+(v2)+"</option>";
for (i = 0; i < v1.length; i++) {
  if(v1[i]!=v2){
   cmd+="<option value="+v1[i]+">"+(v1[i])+"</option>"

  }   

}
return cmd;
});

const port = 3000;
var hum="30";


app.listen(port, () => {
  console.log(`Listening at http://localhost:${port}`);
});



var appPort=3001;
// Normal HTTP configuration
//let http = require('http').Server(app;

//const wss = new WebSocket.Server({ server:http });
const wss = new WebSocket.Server({ port : appPort});
wss.on('connection', async function connection(wssLocal) {
    console.log('A new client Connected!111111111111111111 11111111111111111111111111');
   // ws.send('node0_status_pir_x');
     

    wss.on('message', function incoming(message) {
      console.log('received: %s', message);
  
      wss.clients.forEach(function each(client) {
        if (client !== wss && client.readyState === WebSocket.OPEN) {
          client.send(message);
        }
      });
      
    });
   const query = {};
   const sort = { time: -1 };
   const limit = 1;
   const envs= await Env.find({}).sort(sort).limit(1);
   console.log("AAAAAAAAAAAAAAAAAAAAAAAAAA")
   console.log(envs);
   console.log("BBBBBBBBBBBBBBBBBBBB")
   var test = [{"temperature": envs[0].temperature,"humidity": envs[0].humidity,"EC": envs[0].EC,"PH": envs[0].PH,"N":envs[0].N,"P":envs[0].P,"K":envs[0].K}];
 
   
   var statusAllJson = JSON.stringify(test);
   
   wss.clients.forEach(function each(client) {
    if (client.readyState === WebSocket.OPEN) {
       
      console.log(statusAllJson);
      client.send(statusAllJson);
     
    }
   }); 
    

});



mongoose.connect('mongodb+srv://npatonpym:B1o2s4s5@cluster0.ztybuzz.mongodb.net/', {
  useNewUrlParser: true
});

app.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});
app.get('/temp', (req, res) => {
    var temp=10;
    var temperature="temp="+temp
    res.send(temperature);
});
app.get('/tracking', async (req, res) => {

  //const log = await managementlog.find();
  //console.log(log)
  const log = await Status.find();
  //var log={};
  //log=[{"type": "Delete","devicename": "pump1", "username":"admin","action": "ON","time": "00"}]
  res.render("tracking",{log:log})

});
app.get('/setting', async (req, res) => {

  //const log = await managementlog.find();
  //console.log(log)
  const log = await Status.find();
  //var log={};
  //log=[{"type": "Delete","devicename": "pump1", "username":"admin","action": "ON","time": "00"}]
  res.render("setting",{log:log})

});

app.get('/aboutus', async (req, res) => {

  //const log = await managementlog.find();
  //console.log(log)
  // const log = await Status.find();
  //var log={};
  //log=[{"type": "Delete","devicename": "pump1", "username":"admin","action": "ON","time": "00"}]
  res.render("aboutus")

});



app.get('/getenvs', async (req, res) => {
  const envs = await Env.findOne({});
  console.log(envs); // แสดงข้อมูลที่ได้รับมาใน console log
  res.json(envs);
});
app.post('/sethum', (req, res) => {
  var data = ''
  req.on('data', chunk => {
    console.log('A chunk of data has arrived: ', chunk);
    data = data + chunk;
    console.log(data);
    hum = data;
  });
  req.on('end', () => {
    console.log('No more data');
  })
  res.sendStatus(200);
});


//-------------------------MQTT-----------------------------------//
var mqtt = require('mqtt');

const MQTT_SERVER = "m15.cloudmqtt.com";
const MQTT_PORT = "12987";
//if your server don't have username and password let blank.
const MQTT_USER = "cyejnmdr"; 
const MQTT_PASSWORD = "Is7roaqnQX09";

// Connect MQTT
var client = mqtt.connect({
    host: MQTT_SERVER,
    port: MQTT_PORT,
    username: MQTT_USER,
    password: MQTT_PASSWORD
});


client.on('connect', function () {
    // Subscribe any topic
    console.log("MQTT Connect");
    client.subscribe('tttt', function (err) { //set topic
        if (err) {
            console.log(err);
        }
    });

    client.subscribe('mobileToDB', function (err) {
      if (err) {
        console.log(err);
      }
    });
});


//------- show value on website by collecting data by MQTT from PI --------
// Receive Message and print on terminal
client.on('message', async function (topic, message) {
    // message is Buffer
    console.log(message)
    console.log(message.toString());
    if (topic === 'tttt'){
    // var temp=[ '1', '2', '3','4','5','6','7'];
      var temps = message.toString().split(",");
        axios.post('http://localhost:3000/envs', {
          humidity: temps[0],
          temperature: temps[1],
          EC: temps[2],
          PH: temps[3],
          nitrogen: temps[4],
          phosphorus: temps[5],
          potassium: temps[6]
        })


      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    console.log(message.toString());
  }
    if (topic === 'mobileToDB'){
      var payload = message.toString().split(",");
        axios.post('http://localhost:3000/updateDeviceFromMobile', {
          device: payload[0],
          state: payload[1]
        })

      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    console.log(message.toString());
  }

});

//-----------------------------API--------------------------------//
app.use(express.json());
// mock data
const products = [{}];


app.post('/envs', async (req, res) => {
  const payload = req.body;

  var date_ob = new Date();
  const saveEnvs = new Env({
    temperature: payload.temperature,
    humidity: payload.humidity,
    EC: payload.EC,
    PH: payload.PH,
    N : payload.nitrogen,
    P : payload.phosphorus,
    K : payload.potassium,
    time: date_ob,

  })
  //const product = new Env(payload);
  await saveEnvs.save();
  const query = {};
  const sort = { time: -1 };
  const limit = 1;
  const envs= await Env.find({}).sort(sort).limit(1);
  
  console.log(envs);
  var test = [{"temperature": envs[0].temperature,"humidity": envs[0].humidity,"EC": envs[0].EC,"PH": envs[0].PH,"N":envs[0].N,"P":envs[0].P,"K":envs[0].K}];

  
  var statusAllJson = JSON.stringify(test);
  wss.clients.forEach(function each(client) {
    if (client.readyState === WebSocket.OPEN) {
       
      console.log(statusAllJson);
      client.send(statusAllJson);
     
    }
   }); 
  

  res.status(201).end();
});

app.post("/updateTimer", async (req, res) => {
  console.log("Received water timer update:", req.body.Interval); // Accessing req.body.Interval instead of req.body.timer
  try {
    const payload = req.body;
    console.log("Payload:", payload);

    client.publish("testsenddeviceInterval", JSON.stringify(payload), { qos: 0, retain: false }, (error) => {
      if (error) {
        console.error("Error publishing MQTT message:", error);
      } else {
        console.log("MQTT message published successfully");
      }
    });

    var date_ob = new Date();
    const saveConfig = new ConfigModel({
      type: payload.type,
      Interval: payload.Interval, // Accessing payload.Interval instead of payload.timer
      time: date_ob,
    });
    await saveConfig.save();
    console.log("Water timer updated successfully");

    return res.status(200).json({ status: true }); // Return JSON response to the client
  } catch (error) {
    console.error("Error updating water timer:", error);
    res.status(500).json({ status: false, error: "Internal server error" }); // Return JSON response to the client
  }
});

app.post("/bugkiller", async (req, res) => {
  try {
    const payload = req.body;
    console.log("Payload data:", payload.Interval);
    console.log("Payload data:", payload.type);

    client.publish("testsenddeviceInterval", JSON.stringify(payload), { qos: 0, retain: false }, (error) => {
      if (error) {
        console.error("Error publishing MQTT message:", error);
      } else {
        console.log("MQTT message published successfully");
      }
    });

    var date_ob = new Date();
    const saveConfig = new ConfigModel({
      type : payload.type,
      Interval : payload.Interval, // Accessing payload.Interval instead of payload.timer
      time: date_ob,
    });
    await saveConfig.save();
    console.log("Spray timer updated successfully");

    return res.status(200).json({ status: true }); // Return JSON response to the client
  } catch (error) {
    console.error("Error updating timer:", error);
    res.status(500).json({ status: false, error: "Internal server error" }); // Return JSON response to the client
  }
});

app.post("/fertilizerTimer", async (req, res) => {
  try {
    const payload = req.body;
    console.log("Payload data:", payload);

    client.publish("testsenddeviceInterval", JSON.stringify(payload), { qos: 0, retain: false }, (error) => {
      if (error) {
        console.error("Error publishing MQTT message:", error);
      } else {
        console.log("MQTT message published successfully");
      }
    });
    

    var date_ob = new Date();
    const saveConfig = new ConfigModel({
      type : payload.type,
      Interval : payload.Interval, // Accessing payload.Interval instead of payload.timer
      time: date_ob,
    });
    await saveConfig.save();
    console.log("fertilizer timer updated successfully");

    return res.status(200).json({ status: true }); // Return JSON response to the client
  } catch (error) {
    console.error("Error updating fertilizer timer:", error);
    res.status(500).json({ status: false, error: "Internal server error" }); // Return JSON response to the client
  }
});

app.post("/lightTimer", async (req, res) => {
  try {
    const payload = req.body;
    console.log("Payload data:", payload);

    client.publish("testsenddeviceInterval", JSON.stringify(payload), { qos: 0, retain: false }, (error) => {
      if (error) {
        console.error("Error publishing MQTT message:", error);
      } else {
        console.log("MQTT message published successfully");
      }
    });
    

    var date_ob = new Date();
    const saveConfig = new ConfigModel({
      type : payload.type,
      Interval : payload.Interval, // Accessing payload.Interval instead of payload.timer
      time: date_ob,
    });
    await saveConfig.save();
    console.log("Light timer updated successfully");

    return res.status(200).json({ status: true }); // Return JSON response to the client
  } catch (error) {
    console.error("Error updating fertilizer timer:", error);
    res.status(500).json({ status: false, error: "Internal server error" }); // Return JSON response to the client
  }
});

app.post("/updateDevicestatus", async (req, res) => {
  console.log("Received Device Status updated to :", req.body); // Accessing req.body.Interval instead of req.body.timer
  try {
    const payload = req.body;
    console.log("Payload:", payload);

    // Publish MQTT message with only the device and status fields
    client.publish("testsenddevicestatus", JSON.stringify(payload), { qos: 0, retain: false }, (error) => {
      if (error) {
        console.error("Error publishing MQTT message:", error);
      } else {
        console.log("MQTT message published successfully");
      }
    });

    var date_ob = new Date();
    const saveStatus = new Status ({
      device : payload.device,
      status : payload.state, // Accessing payload.Interval instead of payload.timer
      time: date_ob,
    });
    await saveStatus.save();
    console.log("Device status updated successfully");

    return res.status(200).json({ status: true }); // Return JSON response to the client
  } catch (error) {
    console.error("Error updating status:", error);
    res.status(500).json({ status: false, error: "Internal server error" }); // Return JSON response to the client
  }
});

app.post("/updateDeviceFromMobile", async (req, res) => {
  console.log("Received Device Status updated to :", req.body); // Accessing req.body.Interval instead of req.body.timer
  try {
    const payload = req.body;
    console.log("Payload:", payload);

    var date_ob = new Date();
    const saveStatus = new Status ({
      device : payload.device,
      status : payload.state, // Accessing payload.Interval instead of payload.timer
      time: date_ob,
    });
    await saveStatus.save();
    console.log("Device status updated successfully");

    return res.status(200).json({ status: true }); // Return JSON response to the client
  } catch (error) {
    console.error("Error updating status:", error);
    res.status(500).json({ status: false, error: "Internal server error" }); // Return JSON response to the client
  }
});












