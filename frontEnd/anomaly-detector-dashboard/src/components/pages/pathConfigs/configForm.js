import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Link from '@material-ui/core/Link';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import React from 'react';


export default function otherConfigs(props) {
    const classes = props.classes;
    const configs = props.configs;
    return (
        <Container component="main" maxWidth={8}>
            <CssBaseline />
            <div className={classes.paper}>
                <Typography component="h1" variant="h5">
                    Path Configs
                </Typography>
                <form className={classes.form} noValidate>
                    <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                name="TESTSET_PATH"
                                variant="outlined"
                                fullWidth
                                id="TESTSET_PATH"
                                label="TESTSET_PATH"
                                autoFocus
                                defaultValue={configs.TESTSET_PATH}
                                onChange={(event)=>{
                                    configs.TESTSET_PATH = event.target.value;
                                    props.setConfig(configs);
                                    props.setGraphData([]);
                                    props.setAnomalyRange({});
                                    props.setCurFrame(1);
                                }}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                variant="outlined"
                                fullWidth
                                id="SINGLE_TEST_CASE_NAME"
                                label="SINGLE_TEST_CASE_NAME"
                                name="SINGLE_TEST_CASE_NAME"
                                defaultValue={configs.SINGLE_TEST_CASE_NAME}
                                onChange={(event)=>{
                                    configs.SINGLE_TEST_CASE_NAME = event.target.value;
                                    props.setConfig(configs)
                                    props.setGraphData([]);
                                    props.setAnomalyRange({});
                                    props.setCurFrame(1);
                                }}
                            />
                        </Grid>
                    </Grid>
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        className={classes.submit}
                    >
                        Submit Configs
                    </Button>
                    <Grid container justify="flex-end">
                        <Grid item>
                            <Link href="#" variant="body2">
                                Already have an account? Sign in
                            </Link>
                        </Grid>
                    </Grid>
                </form>
            </div>
        </Container>
    );
}