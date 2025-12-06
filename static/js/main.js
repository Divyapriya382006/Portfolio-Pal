document.addEventListener("DOMContentLoaded", function() {
const body = document.body;
const toggleBtn = document.getElementById("themeToggle");

     const savedTheme = localStorage.getItem("theme");
     if (savedTheme === "light") {
        body.classList.add("light");
        body.classList.remove("dark");
        toggleBtn.textContent = "🌙 "; 
  } else {
    body.classList.add("dark");
    toggleBtn.textContent = "☀️ "; 
   }

    toggleBtn.addEventListener("click", () => {
    body.classList.toggle("light");
    body.classList.toggle("dark");

    if (body.classList.contains("light")) {
       toggleBtn.textContent = "🌙 "; 
      localStorage.setItem("theme", "light");
     } else {
      toggleBtn.textContent = "☀️ "; 
      localStorage.setItem("theme", "dark");
    }
  });
    

    document.body.addEventListener("click", function (event) {

        if (event.target.classList.contains("add-btn")) {

            const section = event.target.dataset.section;   // ex: "work-container"
            const container = document.getElementById(section);

            if (!container) return;

            let newSection = container.children[0].cloneNode(true);
            newSection.querySelectorAll("input, textarea, select").forEach(el => el.value = "");

            container.appendChild(newSection);
        }
    });


    window.showSection = function (id) {
        document.getElementById(id).style.display = "block";
    };

});
