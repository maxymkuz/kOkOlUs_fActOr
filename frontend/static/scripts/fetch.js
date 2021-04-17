async function getRelevantVideos(query) { /// {name, id, desc}
    let jsonData = await fetch("http:://localhost:5000/api/...", { // query
        method: 'POST',
        mode: "cors",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(query)
    })
    return await jsonData.json(); 
}

async function getTimeStamps(id, query) { // {timestamp: ..., prob = ...}
    let jsonData = await fetch("http:://localhost:5000/api/...", { // query + id
        method: 'POST',
        mode: "cors",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id, query})
    })
    return await jsonData.json();
}

async function uploadVideo(url) {
    fetch("http:://localhost/api/load", 
    {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": 'application/json'
        },
        body: JSON.stringify(url)
    })
}