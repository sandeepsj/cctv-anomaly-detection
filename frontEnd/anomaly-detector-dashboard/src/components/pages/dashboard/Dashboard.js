import { Container, Grid, Paper } from "@material-ui/core";
import Chart from "./Chart";
import Deposits from "./Deposits";
import Orders from "./Orders";
export default function Main(props) {
    const classes = props.classes;
    const fixedHeightPaper = props.fixedHeightPaper;
    return (<Container maxWidth="lg" className={classes.container}>
        <Grid container spacing={3}>
            {/* Chart */}
            <Grid item xs={12} md={8} lg={9}>
                <Paper className={fixedHeightPaper}>
                    <Chart />
                </Paper>
            </Grid>
            {/* Recent Deposits */}
            <Grid item xs={12} md={4} lg={3}>
                <Paper className={fixedHeightPaper}>
                    <Deposits myVal={10} />
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