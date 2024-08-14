const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const envSchema = new Schema({
  temperature: String,
  humidity: String,
  EC : String,
  PH : String,
  N : String,
  P : String,
  K : String,
  time: String

});

const EnvModel = mongoose.model('current_envs', envSchema);

module.exports = EnvModel;