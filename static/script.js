let gameMode = null; 

function runCode() {
    const code = document.getElementById("code").value;

    fetch("/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code })
    })
        .then(response => response.json())
        .then(data => {
            if (data.output) {
                document.getElementById("output").textContent = data.output;

                
                if (code === "cookie_game" || code === "dark_room") {
                    gameMode = code;
                }
            } else {
                document.getElementById("output").textContent = "No output returned.";
            }
        })
        .catch(error => {
            document.getElementById("output").textContent = "Error: " + error.message;
        });
}

function clearCode() {
    document.getElementById("code").value = "";
    document.getElementById("output").textContent = "";
    document.getElementById("outputInput").value = "";
    gameMode = null; 
}

function showHelp() {
    const helpText = `
        MiniLang Commands:
        - show <string>: Prints text to the output.
        - getinp <prompt>: Gets user input.
        - cookie_game: Starts the cookie baking game.
        - dark_room: Starts the dark room survival game.
    `;
    document.getElementById("output").textContent = helpText;
}


function handleGameCommand(event) {
    if (event.key === "Enter") {
        const command = event.target.value.trim();
        event.target.value = ""; 

        if (gameMode) {
            fetch("/game_command", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ game: gameMode, command })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.output) {
                        const output = document.getElementById("output");
                        output.textContent += `\n> ${command}\n${data.output}`;
                        output.scrollTop = output.scrollHeight; 
                    }
                });
        } else {
            document.getElementById("output").textContent += `\nUnknown command: ${command}`;
        }
    }
}
