function toggleFields(actionType) {
    const action = document.getElementById(actionType).value;
    const teamField = document.getElementById(actionType === 'action' ? 'teamField' : 'teamField2');
    teamField.style.display = action === "getScoresByTeam" ? "block" : "none";
}

async function fetchSportsData() {
    const action = document.getElementById("action").value;
    const sportKey = document.getElementById("sportKey").value;
    const teamName = document.getElementById("teamName").value;
    

    let url;
    if (action === "getEventsByKey") {
        url = `/sports/${sportKey}/scores`; 
    } else if (action === "getScoresByTeam") {
        url = `/sports/${sportKey}/teams/${teamName}/scores`;
    } 

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch data");
        const data = await response.json();

        const resultContainer = document.getElementById("result");
        resultContainer.innerHTML = "";

        data.forEach(event => {
            const item = document.createElement("div");
            item.className = "result-item";
            item.innerHTML = `
                <strong>${event.sport_title}</strong><br>
                <em>${event.commence_time}</em><br>
                ${event.home_team} vs ${event.away_team} <br>
                <strong>Score:</strong> ${event.score.map(score => `${score.name}: ${score.score}`).join(", ")}
            `;
            resultContainer.appendChild(item);
        });
    } catch (error) {
        console.error(error);
        document.getElementById("result").innerHTML = "<p>Error fetching data.</p>";
    }
}
function toggleFields(actionType) {
    const action = document.getElementById(actionType).value;
    const teamField = document.getElementById(actionType === 'action' ? 'teamField' : 'teamField2');
    teamField.style.display = action === "getScoresByTeam" ? "block" : "none";
}

async function fetchSportsData() {
    const action = document.getElementById("action").value;
    const sportKey = document.getElementById("sportKey").value;
    const teamName = document.getElementById("teamName").value;
    

    let url;
    if (action === "getEventsByKey") {
        url = `/sports/${sportKey}/scores`; 
    } else if (action === "getScoresByTeam") {
        url = `/sports/${sportKey}/teams/${teamName}/scores`;
    } 

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch data");
        const data = await response.json();

        const resultContainer = document.getElementById("result");
        resultContainer.innerHTML = "";

        data.forEach(event => {
            const item = document.createElement("div");
            item.className = "result-item";
            item.innerHTML = `
                <strong>${event.sport_title}</strong><br>
                <em>${event.commence_time}</em><br>
                ${event.home_team} vs ${event.away_team} <br>
                <strong>Score:</strong> ${event.score.map(score => `${score.name}: ${score.score}`).join(", ")}
            `;
            resultContainer.appendChild(item);
        });
    } catch (error) {
        console.error(error);
        document.getElementById("result").innerHTML = "<p>Error fetching data.</p>";
    }
}

function toggleFields2(actionType) {
    const action2 = document.getElementById(actionType).value;
    const sportKeyField2 = document.getElementById("sportKey2Field");
    const groupField2 = document.getElementById("groupField2");
    const titleField2 = document.getElementById("titleField2");
    const descriptionField2 = document.getElementById("descriptionField2");
    const activeField2 = document.getElementById("activeField2");
    const outrightsField2 = document.getElementById("outrightsField2");
    const resultContainer = document.getElementById("result2"); 

    if (resultContainer) {
        resultContainer.innerHTML = ""; 
    }
    sportKeyField2.style.display = "none";
    groupField2.style.display = "none";
    titleField2.style.display = "none";
    descriptionField2.style.display = "none";
    activeField2.style.display = "none";
    outrightsField2.style.display = "none";

    if (action2 === "getSport") {
        sportKeyField2.style.display = "block";
    } else if (action2 === "getSportByGroup") {
        groupField2.style.display = "block";
    } else if (action2 === "createSport" || action2 === "updateSport") {
        sportKeyField2.style.display = "block";
        groupField2.style.display = "block";
        titleField2.style.display = "block";
        descriptionField2.style.display = "block";
        activeField2.style.display = "block";
        outrightsField2.style.display = "block";
    } else if (action2 === "deleteSport") {
        sportKeyField2.style.display = "block";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    toggleFields2('action2'); 
});

async function fetchSportsData2() {
    const action = document.getElementById("action2").value; 
    const sportKey = document.getElementById("sportKey2").value; 
    const group = document.getElementById("group2").value; 
    const title = document.getElementById("title2").value; 
    const description = document.getElementById("description2").value; 
    const active = document.getElementById("active2").value === "true";
    const hasOutrights = document.getElementById("hasOutrights2").value === "true";

    let url = `/sports`;
    let options = { method: "GET" };

    if (action === "getSport") {
        url = `/sports/${sportKey}`;
    } else if (action === "getSportByGroup") {
        url = `/sports/${group}/group`;
    } else if (action === "createSport") {
        options = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ key: sportKey, group, title, description, active, has_outrights: hasOutrights })
        };
    } else if (action === "updateSport") {
        url = `/sports/${sportKey}`;
        options = {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ key: sportKey, group, title, description, active, has_outrights: hasOutrights })
        };
    } else if (action === "deleteSport") {
        url = `/sports/${sportKey}`;
        options = { method: "DELETE" };
    }

    try {
        const response = await fetch(url, options);
        if (!response.ok) throw new Error("Failed to fetch data");
        
        const data = await response.json();
        const resultContainer = document.getElementById("result2");
        resultContainer.innerHTML = "";

        if (Array.isArray(data)) {
            data.forEach(sport => {
                const item = document.createElement("div");
                item.className = "result-item";
                item.innerHTML = `
                    <strong>Title:</strong> ${sport.title || "N/A"}<br>
                    <strong>Group:</strong> ${sport.group || "N/A"}<br>
                    <strong>Key:</strong> ${sport.key || "N/A"}<br>
                    <strong>Description:</strong> ${sport.description || "N/A"}<br>
                    <strong>Active:</strong> ${sport.active !== undefined ? (sport.active ? "Yes" : "No") : "N/A"}<br>
                    <strong>Has Outrights:</strong> ${sport.has_outrights !== undefined ? (sport.has_outrights ? "Yes" : "No") : "N/A"}<br>
                `;
                resultContainer.appendChild(item);
            });
        } else if (data) {
            const item = document.createElement("div");
            item.className = "result-item";
            item.innerHTML = `
                <strong>Title:</strong> ${data.title || "N/A"}<br>
                <strong>Group:</strong> ${data.group || "N/A"}<br>
                <strong>Key:</strong> ${data.key || "N/A"}<br>
                <strong>Description:</strong> ${data.description || "N/A"}<br>
                <strong>Active:</strong> ${data.active !== undefined ? (data.active ? "Yes" : "No") : "N/A"}<br>
                <strong>Has Outrights:</strong> ${data.has_outrights !== undefined ? (data.has_outrights ? "Yes" : "No") : "N/A"}<br>
            `;
            resultContainer.appendChild(item);
        } else {
            resultContainer.innerHTML = "<p>No data found.</p>";
        }
    } catch (error) {
        console.error("Error fetching data:", error);
        document.getElementById("result2").innerHTML = "<p>Error fetching data.</p>"; 
    }
}
