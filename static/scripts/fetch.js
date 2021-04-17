async function getRelevantVideos(query) { /// {name, id, desc}
    let jsonData = await fetch("api/query", { // query
        method: 'POST',
        mode: "cors",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(query)
    })
    return await jsonData.json();
}

// {
//     [timestamp: prob, timestamp: prob,timestamp: prob]
// }

async function getTimeStamps(id, query, db) { // {timestamp: ..., prob = ...}
    let jsonData = await fetch("get_timestamp", { // query + id
        method: 'POST',
        mode: "cors",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: id, query: query, db: db})
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