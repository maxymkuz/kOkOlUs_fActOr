const viewBtn = document.getElementById("view-btn");
const searchBtn = document.getElementById("search-btn");
const queryText = document.querySelector("textarea");
const next = document.getElementById("right");
const prev = document.getElementById("left");
const relatedVideosContainer = document.getElementById("related-videos")
const currQueryDOM = document.getElementById("current-phrase")
const uploadBtn = document.getElementById("upload-btn")
const currentVideoUrlDOM = document.getElementById("video-url-input")
const ASRDOM = document.getElementById("ASR")
const OCRDOM = document.getElementById("OCR")


let currentVideoId = "wEoyxE0GP2M";
let currentQuery;
let currentTimestamps = [];
let relevantVideos = [];
let currentTimeStampIndex;


function displayRelevantVideos(videoList) {
    // avoid memory leak
    for (let i = 0; i < relatedVideosContainer.childNodes.length; i++) {
        relatedVideosContainer.childNodes[i].removeEventListener("click", handleVideoSelection);
    }
    relatedVideosContainer.innerHTML = "";
    for (let i = 0; i < videoList.length; i++) {
        let node = document.createElement("div");
        node.classList.add("video-more");
        node.id = videoList[i].id
        node.innerHTML = videoList[i].name;
        node.addEventListener("click", handleVideoSelection);
        relatedVideosContainer.appendChild(node);
    }

    // bring the first one onto placeholder
    if (videoList.length) {
        displayVideo(videoList[0].id);
    }
}

function handleVideoSelection() {
    displayVideo(this.id)
}

function displayVideo(id) {
    currentVideoId = id;
    player.cueVideoById({"videoId": id}); //cueVideoById
    // currentTimestamps = await getTimeStamps(id, currentQuery);
    searchBtn.click();
}

function moveToMark() {
    if (currentTimestamps.length) {
        console.log(currentTimestamps[currentTimeStampIndex % currentTimestamps.length]);
        player.seekTo(currentTimestamps[currentTimeStampIndex % currentTimestamps.length]);
        player.pauseVideo();

    } else {
        console.log("Not time stamps identified");
    }
}

// function moveToMarkValue(value) {
//     currentTimestamps.forEach((val, ind) => {
//         if (value == val) {
//             currentTimeStampIndex = ind;
//         }
//     })
//     moveToMark();
// }

viewBtn.addEventListener("click", () => {
    currentQuery = queryText.value;
    console.log("Current Query:", currentQuery);
    getRelevantVideos(currentQuery).then(result => {
        relevantVideos = result;
        displayRelevantVideos(relevantVideos)
    })
    // relevantVideos = [{"name": "Suka", "id": "spUNpyF58BY"}, {"name": "Vasya", "id": "HgzGwKwLmgM"}];
    // displayRelevantVideos(relevantVideos);
})

async function processStamps() {
    let ocrResult = await getTimeStamps(currentVideoId, currentQuery, "ocr");
    let asrResult = await getTimeStamps(currentVideoId, currentQuery, "asr");
    let ocrTimeStamps = ocrResult.map(el => el.timestamp);
    let ocrLabels = ocrResult.map(el => el.prob);
    let asrLabels = asrResult.map(el => el.prob);
    let asrTimeStamps = asrResult.map(el => el.timestamp);


    console.log(ocrTimeStamps)
    console.log(asrTimeStamps)
    currentTimeStampIndex = 0;
    updateGraphOCR(ocrTimeStamps, ocrLabels, "OCRChart"); // map from it
    updateGraphASR(asrTimeStamps, asrLabels, "ASRChart"); // map from it
    currentTimestamps = []
    if (OCRDOM.checked) {
        console.log("ocr")
        currentTimestamps = currentTimestamps.concat(ocrTimeStamps);
    }
    if (ASRDOM.checked) {
        console.log("asr")
        currentTimestamps = currentTimestamps.concat(asrTimeStamps);
    }
    console.log(currentTimestamps)
    currentTimestamps.sort((a, b)=>a-b);
    console.log(currentTimestamps)
    moveToMark();
}

searchBtn.addEventListener("click", () => {
    currentQuery = queryText.value;
    currQueryDOM.innerHTML = currentQuery;
    processStamps();
})


prev.addEventListener("click", () => {
    currentTimeStampIndex--;
    moveToMark();
})

next.addEventListener("click", () => {
    currentTimeStampIndex++;
    moveToMark();
})

uploadBtn.addEventListener("click", () => {
    let url = currentVideoUrlDOM.value;
    url && uploadVideo(url);
})