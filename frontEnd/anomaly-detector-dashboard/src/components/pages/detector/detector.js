import { Button, Container, Grid, Paper } from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';
import clsx from 'clsx';
import AnomalyTable from "./anomalyTable";
import Chart from "./Chart";
import VideoFrames from "./VideoFrame";

const useStyles = makeStyles({
    fixedHeight: {
        height: 450,
      },
  });
  

export default function Detector(props) {
    const classes = props.classes;
    const classes1 = useStyles();
    const configs = props.configs;
    const fixedHeightPaper = clsx(classes.paper, classes1.fixedHeight);
    return (<Container maxWidth="lg" className={classes.container}>
        <Grid container spacing={3}>
            
            {/* Recent Deposits */}
            <Grid item xs={12} md={6} lg={6}>
                <Paper className={fixedHeightPaper}>
                    <VideoFrames curFrame={props.curFrame} configs = {configs} />
                </Paper>
            </Grid>
            {/* Chart */}
            <Grid item xs={12} md={6} lg={6}>
                <Paper className={fixedHeightPaper}>
                    <Chart graphData = {props.graphData}/>
                </Paper>
            </Grid>
            <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        className={classes.submit}
                        onClick={() => props.startVideoAndDetectAnomaly(props.curFrame)}
                    >
                        Detect Anomaly
                    </Button>
            {/* Recent Orders */}
            <Grid item xs={12}>
                <Paper className={classes.paper}>
                    <AnomalyTable anomalyRange={props.anomalyRange} playVideo={props.playVideo}/>
                </Paper>
            </Grid>
        </Grid>
    </Container>);
}