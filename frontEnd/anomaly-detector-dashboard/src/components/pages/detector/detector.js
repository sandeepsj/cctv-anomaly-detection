import { Container, Grid, Paper } from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';
import clsx from 'clsx';
import Chart from "./Chart";
import Orders from "./Orders";
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
                    <VideoFrames curFrame={10} configs = {configs} />
                </Paper>
            </Grid>
            {/* Chart */}
            <Grid item xs={12} md={6} lg={6}>
                <Paper className={fixedHeightPaper}>
                    <Chart />
                </Paper>
            </Grid>
            {/* Recent Orders */}
            <Grid item xs={12}>
                <Paper className={classes.paper}>
                    <Orders />
                </Paper>
            </Grid>
        </Grid>
    </Container>);
}