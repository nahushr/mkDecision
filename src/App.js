import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import axios from 'axios';
import MuiAlert from '@material-ui/lab/Alert';


function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}


const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));
function validate(from_email, to_email, message, name, setState)
{
    if(from_email.length == 0)
    {
        setState({
            errorMessage: "From  email is Required",
            serverResponse: ""
        })
        return false;
    }
    else if(to_email.length == 0)
    {
        setState({
            errorMessage: "To email is required",
            serverResponse: ""
        });
        return false;
    }
    else if(message.length == 0)
    {
        setState({
            errorMessage: "Message is required",
            serverResponse: ""
        });
        return false;
    }
    else if(name.length == 0)
    {
        setState({
            errorMessage: "Name is required",
            serverResponse: ""
        });
        return false;
    }
    return true;
}

function onSend(setState)
{
    var name = document.getElementById("name").value;
    var message = document.getElementById("message").value;
    var from_email = document.getElementById("from_email").value;
    var to_email = document.getElementById("to_email").value;

    var result = validate(from_email, to_email, message, name, setState);
    if(!result) return;

    // axios call to the server
    var headers = {
        "Content-Type" : "application/json"
    }
    var payload = {
          "name": name,
          "sourceEmail": from_email,
          "destinationEmail": to_email,
          "message": message
    }
    var api_gateway_url = " https://de4lvq2a46.execute-api.us-east-2.amazonaws.com/v1/post-json"
    axios.post(api_gateway_url, payload, headers).
          then(res => {
            setState({
                errorMessage: "",
                serverResponse: res.data.body.toString()
            });
      });
}

function App() {
  const classes = useStyles();
  const [state, setState] = useState({
    errorMessage: "",
    serverResponse: ""
  });
  return (
    <div className="App">
        <AppBar position="static">
                <Toolbar>
                  <Typography variant="h6" className={classes.title}>
                    Mk decision messaging application
                  </Typography>
                </Toolbar>
        </AppBar>
        <br/><br/>
         <TextField id="name" label="Name" variant="outlined" style={{width:'40%'}}/> <br/><br/><br/>
         <TextField id="from_email" label="From Email" variant="outlined" style={{width:'40%'}} /> <br/><br/><br/>
         <TextField id="to_email" label="To Email" variant="outlined" style={{width:'40%'}}/> <br/><br/><br/>
         <TextField id="message" label="Message" variant="outlined"  multiline rowsMax={4}  style={{width:'40%'}}/> <br/><br/><br/>
         <Button variant="contained" color="primary" onClick = {() => {onSend(setState);}}> Send Message </Button><br/><br/>

          <Alert severity={state.errorMessage.length > 0 ? "error" : "info"}>
          {state.serverResponse.length > 0 ? state.serverResponse : state.errorMessage.length == 0 ? "Errors and server responses will be displayed here" : state.errorMessage}
          </Alert>

    </div>
  );
}

export default App;
