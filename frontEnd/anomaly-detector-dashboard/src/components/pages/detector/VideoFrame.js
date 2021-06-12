import { Card, CardActionArea, CardMedia, Link } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import React from 'react';
import { getSingleTestCaseFrame } from "./../../Configs";
import Title from './Title';

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
  return (
    <React.Fragment>
      <Title>Video Streaming</Title>
      <Typography component="p" variant="h4">
        {props.myVal}
      </Typography>
      <Typography color="textSecondary" className={classes.depositContext}>
        The Video you set in Config
        <Card>
          <CardActionArea>
            <CardMedia
              component="img"
              alt="Selected Test case not available"
              height="140"
              image={getSingleTestCaseFrame(configs, 1)}
              title="Selected Test Case"
            />
            <img src={getSingleTestCaseFrame(configs, 1)}/>
          </CardActionArea></Card>
      </Typography>
      <div>
        <Link color="primary" href="#" onClick={preventDefault}>
          Show Video Properies
        </Link>
      </div>
    </React.Fragment>
  );
}