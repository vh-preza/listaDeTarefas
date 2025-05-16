const checkboxes = document.getElementsByClassName("checkbox-input");

for (let checkbox of checkboxes) {
    if (checkbox.checked) {
        const id = checkbox.getAttribute("id")
        document.getElementById("task-text-" + id).style.textDecoration = "line-through";
        document.getElementById("task-row-" + id).style.backgroundColor = "#9bdba6";
    }

    checkbox.addEventListener("change", () => {
        const id = checkbox.getAttribute("id")
        if (checkbox.checked) {
            document.getElementById("task-text-" + id).style.textDecoration = "line-through";
            document.getElementById("task-row-" + id).style.backgroundColor = "#9bdba6";
            saveStatus(id, 1, "Check");
        } else {
            document.getElementById("task-text-" + id).style.textDecoration = "none";
            document.getElementById("task-row-" + id).style.backgroundColor = "#ffffff";
            saveStatus(id, 0, "Check");
        }
    })
}

function updateTask(id) {
    const taskText = document.getElementById("task-text-" + id);
    const editTask = document.getElementById("task-edit-" + id);

    taskText.style.display = "none";
    editTask.style.display = "inline-block"

    editTask.value = taskText.textContent;

    editTask.focus();

    editTask.addEventListener("blur", () => {
        saveTask(id);
    });

    editTask.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            saveTask(id);
        }
    });
}

async function saveTask(id) {
    const taskText = document.getElementById("task-text-" + id);
    const editTask = document.getElementById("task-edit-" + id);

    const text = editTask.value;

    saveStatus(id, text, "Task")

    taskText.textContent = text;
    taskText.style.display = "inline-block";
    editTask.style.display = "none";

    const blurListener = () => saveTask(id);
    const keydownListener = (event) => {
        if (event.key === "Enter") {
            saveTask(id);
        }
    };

    editTask.removeEventListener("blur", blurListener);
    editTask.removeEventListener("keydown", keydownListener);
}

async function saveStatus(id, field, type) {
    let json;

    if (type === "Task") {
        json = { text: field }
    } else {
        json = { checked: field }
    }

    try {
        await fetch("/update/" + id, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(json)
        });
    } catch (error) {
        alert("Error saving task: " + error.message);
    }
}