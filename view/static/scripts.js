document.addEventListener("DOMContentLoaded", function () {
    const loginSection = document.getElementById("login-section");
    const registerSection = document.getElementById("register-section");

    document.getElementById("show-register").addEventListener("click", function () {
        loginSection.style.display = "none";
        registerSection.style.display = "block";
    });

    document.getElementById("show-login").addEventListener("click", function () {
        registerSection.style.display = "none";
        loginSection.style.display = "block";
    });
});

function toggleStatus(taskId, checked) {
    fetch("/home/task/toggle", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
            task_id: taskId,
            status: checked
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("✅ Task updated!");
            location.reload();  // <- hoặc reload nếu bạn muốn cập nhật giao diện ngay
        }
    });
}
// Tự động kích hoạt Dark Mode nếu đã chọn
window.onload = function () {
    const dark = localStorage.getItem("dark-mode");
    if (dark === "true") {
        document.body.classList.add("dark-mode");
    }
};

function toggleDarkMode() {
    document.documentElement.classList.toggle("dark-mode");
    localStorage.setItem("dark-mode", document.documentElement.classList.contains("dark-mode"));
}

