import Button from '@material-ui/core/Button';
import Link from '@material-ui/core/Link';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import React from 'react';
import Title from './Title';

const useStyles = makeStyles((theme) => ({
  seeMore: {
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

export default function AnomalyTable(props) {
  const classes = useStyles();
  const anomalyRange = props.anomalyRange
  return (
    <React.Fragment>
      <Title>Detected Anomalies</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Starting frame</TableCell>
            <TableCell>Ending frame</TableCell>
            <TableCell align="right"></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {Object.keys(anomalyRange).map((start) => (
            <TableRow key={start}>
              <TableCell>{start}</TableCell>
              <TableCell>{anomalyRange[start]}</TableCell>
              <TableCell align="right">
              <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        className={classes.submit}
                        onClick={() => props.playVideo(parseInt(start), parseInt(anomalyRange[start]))}
                    >
                        Play Detected Video
                    </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <div className={classes.seeMore}>
        <Link color="primary" href="#" >
          Click the play button to see the anomalous events
        </Link>
      </div>
    </React.Fragment>
  );
}