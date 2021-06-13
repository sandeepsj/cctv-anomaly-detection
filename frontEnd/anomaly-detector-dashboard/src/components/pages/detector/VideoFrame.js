import { Card, Link } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import React from 'react';
import { getSingleTestCaseFileName } from "./../../Configs";
import Title from './Title';
var Tiff = require('tiff.js');

function preventDefault(event) {
  event.preventDefault();
}

const useStyles = makeStyles({
  depositContext: {
    flex: 1,
  },
});

export default function VideoFrames(props) {
  const classes = useStyles();
  const configs = props.configs;

  const filename = getSingleTestCaseFileName(configs, props.curFrame, "Test");
  var xhr = new XMLHttpRequest();
  xhr.responseType = 'arraybuffer';
  xhr.open('GET', filename);
  xhr.onload = function (e) {
    var tiff = new Tiff({ buffer: xhr.response });
    var canvas = tiff.toCanvas();
    const imageurl = canvas.toDataURL();
    var img = document.createElement('img');
    img.src = imageurl;
    img.width = 580;
    img.height =380;
    img.id = "frame";
    document.getElementById("videoframe").replaceChild(img, document.getElementById("frame"));
    
  };
  xhr.send();
  return (
    <React.Fragment>
      <Title>Video Streaming</Title>
      <Typography component="p" variant="h4">
        {props.myVal}
      </Typography>
        <Card>
          <div id="videoframe">
            <img src="" id="frame"/>
          </div>
        </Card>
      <div>
        <Link color="primary" href="#" onClick={preventDefault}>
          Show Video Properies
        </Link>
      </div>
    </React.Fragment>
  );
}

