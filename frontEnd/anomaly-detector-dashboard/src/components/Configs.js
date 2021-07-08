const defConfig = {
    SINGLE_TEST_CASE_NAME: "Test036",
    //TESTSET_PATH: "/home/sandeepsj/Downloads/ucsd_anomaly_dataset/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Test"
    TESTSET_PATH: "/Test",
    THRESHOLD_VALUE: 510
}

const getSingleTestCaseFrame = function (configs, curFrame) {
    curFrame = curFrame + "";
    for (var i = 0; i<=3-curFrame.length; i++) {
        curFrame = "0" + curFrame;
    }
    const fileName = curFrame +".tif";
    return configs.TESTSET_PATH + "/" + configs.SINGLE_TEST_CASE_NAME + "/" + fileName;
}
const getSingleTestCaseFileName =  function (configs, curFrame, dirPath) {
    if(curFrame>9 && curFrame < 100){
        curFrame = "0"+curFrame;
    }
    else if(curFrame<100){
        curFrame = "00"+curFrame;
    }
    const fileName = curFrame +".tif";
    return dirPath+ "/" + configs.SINGLE_TEST_CASE_NAME + "/" + fileName;
}
export { defConfig, getSingleTestCaseFileName };

