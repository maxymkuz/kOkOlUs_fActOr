async function getRelevantVideos(query) { /// {name, id, desc}
    let jsonData = await fetch("http:://localhost:5000/api/query", { // query
        method: 'POST',
        mode: "cors",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({query})
    })
    return await jsonData.json(); 
}

{
    "query": "query_str"
}



{
    "query": "query_str"
    "id": "id_str"
    "db": "db_str"
}
{timestamp: [], prob: float}
->

async function getTimeStamps(id, query, db) { // {timestamp: ..., prob = ...}
    let jsonData = await fetch("http:://localhost:5000/api/...", { // query + id
        method: 'POST',
        mode: "cors",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id, query, db})
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