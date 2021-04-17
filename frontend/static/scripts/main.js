const viewBtn = document.getElementById("view-btn");
const searchBtn = document.getElementById("search-btn");
const queryText = document.querySelector("textarea");
const next = document.getElementById("right");
const prev = document.getElementById("left");
const relatedVideosContainer = document.getElementById("related-videos")
const currQueryDOM = document.getElementById("current-phrase")
const uploadBtn = document.getElementById("upload-btn")
const currentVideoUrlDOM = document.getElementById("video-url-input")
let currentVideoId;
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
    if (relatedVideosContainer.length) {
        displayVideo(videoList[0]);
    }
}

function handleVideoSelection() {
    displayVideo(this.id)
}

function displayVideo(id) {
    currentVideoId = id;
    player.cueVideoById({"videoId": id}); //cueVideoById
    // currentTimestamps = await getTimeStamps(id, currentQuery);
    currentTimestamps = [23, 56, 200, 320];
    currentTimeStampIndex = 0;
    moveToMark();
}

function moveToMark() {
    console.log("Time stamp index: ", currentTimeStampIndex);
    if (currentTimestamps.length) {
        console.log(currentTimestamps[currentTimeStampIndex % currentTimestamps.length]);
        player.seekTo(currentTimestamps[currentTimeStampIndex % currentTimestamps.length]);
        player.pauseVideo();

    } else {
        console.log("Not time stamps identified");
    }
}

viewBtn.addEventListener("click", () => {
    currentQuery = queryText.value;
    console.log("Current Query:", currentQuery);
    // relevantVideos = await getRelevantVideos(currentQuery);
    relevantVideos = [{"name": "Suka", "id": "iHEMOdRo5u"}, {"name": "Vasya", "id": "HgzGwKwLmgM"}];
    displayRelevantVideos(relevantVideos);
})

searchBtn.addEventListener("click", () => {
    currentQuery = queryText.value;
    currQueryDOM.innerHTML = currentQuery;
    // result = await getTimeStamps(currentVideoId, currentQuery);
    currentTimestamps = [23, 56, 200, 320];
    currentTimeStampIndex = 0;
    moveToMark();
    updateGraph(currentTimestamps, [0.3, 0.4, 0.67, 0.8], "New chlen"); // map from it
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